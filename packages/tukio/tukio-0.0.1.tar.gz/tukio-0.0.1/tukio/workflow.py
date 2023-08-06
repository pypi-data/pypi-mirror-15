import asyncio
from datetime import datetime
from enum import Enum
import functools
import inspect
import logging
from uuid import uuid4

from tukio.dag import DAG
from tukio.task import TaskTemplate, TaskRegistry
from tukio.utils import future_state


log = logging.getLogger(__name__)


class WorkflowError(Exception):
    pass


class WorkflowRootTaskError(WorkflowError):
    pass


class WorkflowNotFoundError(WorkflowError):
    def __str__(self):
        return 'no workfow bound to the task, cannot unlock it!'


class OverrunPolicy(Enum):

    """
    The overrun policy defines what to do if the previous execution of a
    workflow didn't finish yet and a new event must be dispatched by the
    workflow engine.
    This class also defines policy handlers that can create new instances
    of workflow execution objects according to the current overrun policy and
    to the list of running workflow instances (with the same template).
    """

    # Skip until all running instances are finished
    skip = 'skip'
    # Start a new workflow instance whatever the running instances
    start_new = 'start-new'
    # Skip until all running instances had been unlocked
    skip_until_unlock = 'skip-until-unlock'
    # Abort all running instances before creating a new once
    abort_running = 'abort-running'

    @classmethod
    def get_default_policy(cls):
        """
        Returns the default overrun policy.
        """
        return OverrunPolicy.skip_until_unlock


class OverrunPolicyHandler:

    """
    This class defines overrun policy handlers to create new instances
    of workflow execution objects according to the current overrun policy and
    to the list of running workflow instances (with the same template).
    """

    def __init__(self, template, loop=None):
        self._loop = loop
        # Store the workflow template for further use in policy handlers.
        self.template = template
        self.policy = template.policy

    def new_workflow(self, running=None):
        method = getattr(self, '_' + self.policy.name)
        return method(running)

    def _check_wflow(self, wflow):
        if wflow.template_id != self.template.uid:
            err = 'expected template ID {}'', got {}'
            raise ValueError(err.format(self.template.uid, wflow.template_id))

    def _new_wflow(self):
        return Workflow(self.template, loop=self._loop)

    def _skip(self, running):
        """
        Run a new instance of workflow only if there's no instance already
        running with the same template ID.
        """
        if running:
            for wflow in running:
                self._check_wflow(wflow)
            return None
        else:
            return self._new_wflow()

    def _start_new(self, _):
        """
        Always run a new instance of workflow.
        """
        return self._new_wflow()

    def _skip_until_unlock(self, running):
        """
        Run a new instance of workflow only if all the instances already
        running have been unlocked. Refer to the `Workflow` docstring for more
        details about locked/unlocked workflows.
        """
        if running:
            for wflow in running:
                self._check_wflow(wflow)
                if wflow.lock.locked():
                    break
            else:
                return self._new_wflow()
            # There's at least 1 locked workflow instance
            return None
        else:
            return self._new_wflow()

    def _abort_running(self, running):
        """
        Abort all running instances of the workflow before creating a new one.
        """
        if running:
            for wflow in running:
                self._check_wflow(wflow)
                wflow.cancel()
        return self._new_wflow()


class WorkflowTemplate(object):

    """
    A workflow template is a DAG (Directed Acyclic Graph) made up of task
    template objects (`TaskTemplate`). This class is not a workflow execution
    engine.
    It provides an API to easily build and update a consistent workflow.
    """

    def __init__(self, title, uid=None, tags=None, version=None, policy=None):
        self.title = title
        self.tags = tags or []
        self.uid = uid or str(uuid4())
        self.version = int(version) if version is not None else 1
        if policy is None:
            self.policy = OverrunPolicy.get_default_policy()
        elif isinstance(policy, OverrunPolicy):
            self.policy = policy
        else:
            self.policy = OverrunPolicy(policy)

        self.dag = DAG()

    @property
    def tasks(self):
        return list(self.dag.graph.keys())

    def add(self, task_tmpl):
        """
        Adds a new task template to the workflow. The task will remain orphan
        until it is linked to upstream/downstream tasks.
        This method must be passed a `TaskTemplate()` instance.
        """
        if not isinstance(task_tmpl, TaskTemplate):
            raise TypeError("expected a 'TaskTemplate' instance")
        self.dag.add_node(task_tmpl)

    def delete(self, task_tmpl):
        """
        Remove a task template from the workflow and delete the links to
        upstream/downstream tasks.
        """
        self.dag.delete_node(task_tmpl)

    def root(self):
        """
        Returns the root task. If no root task or several root tasks were found
        raises `WorkflowValidationError`.
        """
        root_task = self.dag.root_nodes()
        if len(root_task) == 1:
            return root_task[0]
        else:
            raise WorkflowRootTaskError("expected one root task, "
                                        "found {}".format(root_task))

    def link(self, up_task_tmpl, down_task_tmpl):
        """
        Create a directed link from an upstream to a downstream task.
        """
        self.dag.add_edge(up_task_tmpl, down_task_tmpl)

    def unlink(self, task_tmpl1, task_tmpl2):
        """
        Remove the link between two tasks.
        """
        try:
            self.dag.delete_edge(task_tmpl1, task_tmpl2)
        except KeyError:
            self.dag.delete_edge(task_tmpl2, task_tmpl1)

    @classmethod
    def from_dict(cls, wf_dict):
        """
        Build a new workflow description from the given dictionary.
        The dictionary takes the form of:
            {
                "title": <workflow-title>,
                "id": <workflow-uid>,
                "vesion": <version>,
                "tags": [<a-tag>, <another-tag>],
                "tasks": [
                    {"id": <task-uid>, "name": <name>, "config": <cfg-dict>},
                    ...
                ],
                "graph": {
                    <t1-uid>: [t2-uid, <t3-uid>],
                    <t2-uid>: [],
                    ...
                }
            }
        """
        # 'title' is the only mandatory key
        title, uid = wf_dict['title'], wf_dict.get('id')
        tags, version = wf_dict.get('tags'), wf_dict.get('version')
        policy = wf_dict.get('policy')
        wf_tmpl = cls(title, uid=uid, tags=tags,
                      version=version, policy=policy)
        task_ids = dict()
        for task_dict in wf_dict.get('tasks', []):
            task_tmpl = TaskTemplate.from_dict(task_dict)
            wf_tmpl.add(task_tmpl)
            task_ids[task_tmpl.uid] = task_tmpl
        for up_id, down_ids_set in wf_dict.get('graph', {}).items():
            up_tmpl = task_ids[up_id]
            for down_id in down_ids_set:
                down_tmpl = task_ids[down_id]
                wf_tmpl.link(up_tmpl, down_tmpl)
        return wf_tmpl

    def as_dict(self):
        """
        Builds and returns a dictionary that represents the current workflow
        template object.
        """
        wf_dict = {
            "title": self.title, "id": self.uid,
            "tags": self.tags, "version": int(self.version),
            "tasks": [], "graph": {}
        }
        for task_tmpl in self.tasks:
            wf_dict['tasks'].append(task_tmpl.as_dict())
        for up_tmpl, down_tmpls_set in self.dag.graph.items():
            _record = {up_tmpl.uid: list(map(lambda x: x.uid, down_tmpls_set))}
            wf_dict['graph'].update(_record)
        return wf_dict

    def copy(self):
        """
        Returns a new instance that is a copy of the current workflow template.
        """
        wf_tmpl = WorkflowTemplate(self.title, uid=self.uid,
                                   tags=self.tags, version=self.version)
        wf_tmpl.dag = self.dag.copy()
        return wf_tmpl

    def validate(self):
        """
        Validate the current workflow template. At that point, we already know
        the underlying DAG is valid. This methods ensures there's a single
        root task and all task names are registered tasks.
        If not valid, this method should raise either `WorkflowRootTaskError`
        or `UnknownTaskName` exceptions.
        """
        self.root()
        for task in self.tasks:
            TaskRegistry.get(task.name)
        return True


class Workflow(asyncio.Future):

    """
    This class handles the execution of a workflow. Tasks are created along the
    way of workflow execution.
    """

    def __init__(self, wf_tmpl, *, loop=None):
        super().__init__(loop=loop)
        self.uid = str(uuid4())
        # Always act on a copy of the original workflow template
        self._wf_tmpl = wf_tmpl.copy()
        # Start and end datetime (UTC) of the execution of the workflow
        self._start, self._end = None, None
        # List of tasks executed at some point
        self.tasks = set()
        self._done_tasks = set()
        self._new_task_exc = None
        self._must_cancel = False
        self.lock = asyncio.Lock()
        # Create the workflow in the 'locked' state when its overrun policy is
        # 'skip-until-unlock'.
        if self.policy is OverrunPolicy.skip_until_unlock:
            self.lock._locked = True

    @property
    def template_id(self):
        return self._wf_tmpl.uid

    @property
    def policy(self):
        return self._wf_tmpl.policy

    def _unlock(self, _):
        """
        A done callback to unlock the workflow.
        The concept of 'locked workflow' only applies when the overrun policy
        is set to 'skip-until-unlock'. Once a task has unlocked the workflow,
        new execution with the same template can be triggered.
        """
        if self.lock.locked():
            self.lock.release()

    def run(self, *args, **kwargs):
        """
        Execute the workflow following the description passed at init.
        """
        # A workflow can be ran only once
        if self.tasks:
            return
        # Run the root task
        root_tmpl = self._wf_tmpl.root()
        task = self._new_task(root_tmpl, (args, kwargs))
        self._start = datetime.utcnow()
        # The workflow may fail to start at once
        if not task:
            self._try_mark_done()

    def _new_task(self, task_tmpl, inputs):
        """
        Each new task must be created successfully, else the whole workflow
        shall stop running (wrong workflow config or bug).
        """
        try:
            args, kwargs = inputs
            task = task_tmpl.new_task(*args, loop=self._loop, **kwargs)
        except Exception as exc:
            warn = 'failed to create task {}: raised {}'
            log.warning(warn.format(task_tmpl, exc))
            self._new_task_exc = exc
            self._cancel_all_tasks()
            return None
        else:
            log.debug('new task created for {}'.format(task_tmpl))
            done_cb = functools.partial(self._run_next_tasks, task_tmpl)
            task.add_done_callback(done_cb)
            self.tasks.add(task)
            return task

    def _run_next_tasks(self, task_tmpl, future):
        """
        A callback to be added to each task in order to select and schedule
        asynchronously downstream tasks once the parent task is done.
        """
        self._done_tasks.add(future)
        if self._must_cancel:
            self._try_mark_done()
            return
        # Don't execute downstream tasks if the task's result is an exception
        # (may include task cancellation) but don't stop executing the other
        # branches of the workflow.
        try:
            result = future.result()
        except Exception as exc:
            log.warning('task {} ended on {}'.format(task_tmpl, exc))
        else:
            succ_tmpls = self._wf_tmpl.dag.successors(task_tmpl)
            for succ_tmpl in succ_tmpls:
                inputs = ((result,), {})
                succ_task = self._new_task(succ_tmpl, inputs)
                if not succ_task:
                    break
        finally:
            self._try_mark_done()

    def _try_mark_done(self):
        """
        If nothing left to execute, the workflow must be marked as done. The
        result is set to either the exec graph (represented by a dict) or to an
        exception raised at task creation.
        """
        # Note: the result of the workflow may already have been set by another
        # done callback from another task executed in the same iteration of the
        # event loop.
        if self._all_tasks_done() and not self.done():
            if self._new_task_exc:
                self.set_exception(self._new_task_exc)
            elif self._must_cancel:
                super().cancel()
            else:
                self.set_result(self.tasks)
            self._end = datetime.utcnow()

    def _all_tasks_done(self):
        """
        Returns True if all tasks are done, else returns False.
        Here, a task is considered as 'done' only if it is marked as done and
        its `_run_next_tasks()` done callback has been called.
        """
        if self.tasks == self._done_tasks:
            return True
        else:
            return False

    def _cancel_all_tasks(self):
        """
        Cancels all pending tasks and returns the number of tasks cancelled.
        """
        self._must_cancel = True
        cancelled = 0
        pending = self.tasks - self._done_tasks
        for task in pending:
            is_cancelled = task.cancel()
            if is_cancelled:
                cancelled += 1
        return cancelled

    def cancel(self):
        """
        Cancel the workflow by cancelling all pending tasks (aka all tasks not
        marked as done). We must wait for all tasks to be actually done before
        marking the workflow as cancelled (hence done).
        """
        cancelled = self._cancel_all_tasks()
        if cancelled == 0:
            super().cancel()
        return True

    def __str__(self):
        """
        Readable string representation of a workflow execution object.
        """
        string = ("<Workflow template_id={}, template_title={}, uid={}, "
                  "start={}, end={}>")
        tmpl_id, title = self.template_id, self._wf_tmpl.title
        return string.format(tmpl_id, title, self.uid, self._start, self._end)

    def report(self):
        """
        Creates and returns a complete execution report, including workflow and
        tasks templates and execution details.
        """
        wf_exec = {"id": self.uid, "start": self._start, "end": self._end}
        wf_exec['state'] = future_state(self).value
        report = self._wf_tmpl.as_dict()
        report['exec'] = wf_exec
        return report


def new_workflow(wf_tmpl, running=None, loop=None):
    """
    Returns a new workflow execution object if a new instance can be run.
    It depends on the template's overrun policy and the list of running
    workflow instances (given by `running`).
    """
    policy_handler = OverrunPolicyHandler(wf_tmpl, loop=loop)
    return policy_handler.new_workflow(running)


def unlock_workflow_when_done():
    """
    Adds a done callback to the current task so as to unlock the workflow that
    handles its execution when the task gets done.
    If no workflow linked to the task can be found, raise an exception.
    It assumes all tasks scheduled from within a workflow object have at least
    one done callback which is a bound method from the workflow object.

    Note: bound methods from distinct workflow ojects in the task's
    "call when done" list are not supported. It must never happen!
    """
    task = asyncio.Task.current_task()
    for cb in task._callbacks:
        # inspect.getcallargs() gives acces to the implicit 'self' arg of the
        # bound method but it is marked as deprecated since Python 3.5.1
        # and the new `inspect.Signature` object does do the job :((
        if inspect.ismethod(cb):
            inst = cb.__self__
        elif isinstance(cb, functools.partial):
            try:
                inst = cb.func.__self__
            except AttributeError:
                continue
        else:
            continue
        if isinstance(inst, Workflow):
            task.add_done_callback(inst._unlock)
            break
    else:
        raise WorkflowNotFoundError
