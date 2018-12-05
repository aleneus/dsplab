# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module implements the Node and Plan classes. Node can be
understood as the workplace for worker. Node can have inputs that are
also nodes. Plan is the system of linked nodes."""

import logging

from dsplab.activity import get_work_from_dict
from dsplab.activity import Activity
from dsplab.helpers import pretty_json

LOG = logging.getLogger(__name__)


class Node(Activity):
    """Base class for nodes."""
    def __init__(self, inputs=None):
        super().__init__()
        self._id = None
        self._inputs = []
        if inputs is not None:
            self._inputs = inputs
        self._res = None
        self._start_hook = None
        self._start_hook_args = None
        self._start_hook_kwargs = None
        self._stop_hook = None
        self._stop_hook_args = None
        self._stop_hook_kwargs = None

    def set_id(self, value):
        """Set ID for node."""
        self._id = value

    def get_id(self):
        """Return ID of node."""
        return self._id

    node_id = property(get_id, set_id, doc="ID of node.")

    def info(self, as_string=False):
        """Return info about node."""
        info = super().info()
        info['id'] = self.node_id

        input_ids = []
        for inpt in self.get_inputs():
            input_id = '{}'.format(inpt.node_id)
            input_ids.append(input_id)
        if len(input_ids) != 0:
            info['inputs'] = input_ids

        if as_string:
            return pretty_json(info)
        return info

    def get_inputs(self):
        """Return inputs."""
        return self._inputs

    def set_inputs(self, inputs):
        """Set inputs."""
        self._inputs = inputs

    inputs = property(get_inputs, set_inputs)

    def set_start_hook(self, func, *args, **kwargs):
        """Set start hook."""
        self._start_hook = func
        self._start_hook_args = args
        self._start_hook_kwargs = kwargs

    def set_stop_hook(self, func, *args, **kwargs):
        """Set stop hook."""
        self._stop_hook = func
        self._stop_hook_args = args
        self._stop_hook_kwargs = kwargs

    def run_start_hook(self):
        """Run function associated with start hook."""
        if self._start_hook is not None:
            self._start_hook(*self._start_hook_args,
                             **self._start_hook_kwargs)

    def run_stop_hook(self):
        """Run function associated with stop hook."""
        if self._stop_hook is not None:
            self._stop_hook(*self._stop_hook_args,
                            **self._stop_hook_kwargs)

    def is_output_ready(self):
        """Check if the calculation in the node is finished."""
        ans = self._res is not None
        return ans

    def reset(self):
        """Clear the result."""
        self._res = None

    def is_inputs_ready(self):
        """Check if data in all inputs is ready."""
        for inpt in self._inputs:
            if not inpt.is_output_ready():
                return False
        return True

    def get_result(self):
        """Return the calculated data."""
        return self._res

    def set_result_info(self, info):
        """Appent to info the desctription of the output data."""
        self._info['result'] = info

    def __call__(self, data):
        raise NotImplementedError


class WorkNode(Node):
    """Node with work."""
    def __init__(self, work=None, inputs=None):
        super().__init__(inputs)
        self._work = work

    def info(self, as_string=False):
        # LOG.debug("call info() for work node {}".format(self.node_id))
        info = super().info()
        info['work'] = self._work.info().copy()
        if as_string:
            return pretty_json(info)
        return info

    def get_work(self):
        """Return work of the node."""
        return self._work

    def set_work(self, work):
        """Set work for the node."""
        self._work = work

    work = property(get_work, set_work)

    def __call__(self, data):
        self._res = self.work(*data)


class MapNode(WorkNode):
    """Apply work to all components of iterable input and build
    iterable output."""
    def __init__(self, work=None, inputs=None):
        super().__init__(work, inputs)

    def __call__(self, data):
        self._res = []

        if len(self._inputs) > 1:
            self._res = []
            for zipped_args in map(list, zip(*data)):
                res_part = self.work(*zipped_args)
                self._res.append(res_part)
        elif len(self._inputs) == 1:
            self._res = []
            for comp in data[0]:
                comp_res = self.work(comp)
                self._res.append(comp_res)
        else:
            raise RuntimeError('MapNode must have input.')


class SelectNode(Node):
    """Select component of output."""
    def __init__(self, index, inputs=None):
        super().__init__(inputs)
        self.index = index

    def info(self, as_string=False):
        info = super().info()
        info['index'] = self.index
        if as_string:
            return pretty_json(info)
        return info

    def __call__(self, data):
        if len(data) > 1:
            data_tr = list(map(list, zip(*data)))
            self._res = data_tr[self.index]
        elif len(data) == 1:
            self._res = data[0][self.index]
        else:
            raise RuntimeError('SelectNode must have input.')


class PackNode(Node):
    """Pack input to output."""
    def __init__(self, inputs=None):
        super().__init__(inputs)

    def __call__(self, data=None):
        self._res = data


class Plan(Activity):
    """The plan. Plan is the system of linked nodes."""
    def __init__(self, descr=None, quick=False):
        super().__init__()
        if descr is not None:
            self._info['descr'] = descr
        self._nodes = []
        self._inputs = []
        self._outputs = []
        self._progress_func = None

        self._quick = quick
        if not self._quick:
            self._run_func = self.run
        else:
            self._run_func = self.quick_run

        self._sequence = []

    def _detect_sequence(self):
        """Find sequence of nodes for execution."""
        self._sequence = []
        while True:
            finished = True
            for node in self._nodes:
                if (node in self._sequence) or (node in self._inputs):
                    continue
                if set(node.inputs) <= set(self._sequence) | set(self._inputs):
                    self._sequence.append(node)
                    finished = False
            if finished:
                break

    def add_node(self, node, inputs=None):
        """Add node to plan."""
        self._nodes.append(node)
        if inputs is not None:
            node.inputs = inputs
        self._detect_sequence()

    def remove_node(self, node):
        """Remove node from plan."""
        if node not in self._nodes:
            raise RuntimeError("No such node")
        for n in self._nodes:
            if node in n.inputs:
                n.inputs.remove(node)
        self._nodes.remove(node)
        self._detect_sequence()

    def clear(self):
        """Clear plan."""
        self._nodes = []
        self._inputs = []
        self._outputs = []
        self._sequence = []

    def get_outputs(self):
        """Return output nodes."""
        return self._outputs

    def set_outputs(self, outputs):
        """Set output nodes."""
        self._outputs = outputs

    outputs = property(get_outputs,
                       set_outputs,
                       doc="The nodes with are outputs.")

    def get_inputs(self):
        """Return input nodes."""
        return self._inputs

    def set_inputs(self, inputs):
        """Set input nodes."""
        self._inputs = inputs
        self._detect_sequence()

    inputs = property(get_inputs,
                      set_inputs,
                      doc="The nodes which are inputs.")

    def info(self, as_string=False):
        """Return info about the plan."""
        info = super().info()
        info['nodes'] = [node.info() for node in self._nodes]
        info['inputs'] = [inp.get_id() for inp in self.inputs]
        info['outputs'] = [inp.get_id() for inp in self.outputs]
        if as_string:
            return pretty_json(info)
        return info

    def get_nodes(self):
        """Return the list of nodes."""
        return self._nodes

    def set_progress_hook(self, func):
        """Set progress handler."""
        self._progress_func = func

    def run(self, data):
        """Run plan."""
        for node in self._nodes:
            node.reset()

        for [node, node_data] in zip(self._inputs, data):
            node.run_start_hook()
            node([node_data])
            node.run_stop_hook()
            if self._progress_func is not None:
                self._progress_func()

        while True:
            finished = True
            for node in self._nodes:
                if not node.is_output_ready() and node.is_inputs_ready():
                    finished = False
                    input_nodes = node.get_inputs()
                    node_data = []
                    for input_node in input_nodes:
                        node_data.append(input_node.get_result())
                    node.run_start_hook()
                    node(node_data)
                    node.run_stop_hook()
                    if self._progress_func is not None:
                        self._progress_func()
            if finished:
                break

        return [output.get_result() for output in self._outputs]

    def quick_run(self, data):
        """Sequential execution of plan with no hooks (for on-line
        quick processing)."""
        for node, node_data in zip(self._inputs, data):
            node([node_data])
        for node in self._sequence:
            node_data = []
            for input_node in node.inputs:
                node_data.append(input_node.get_result())
            node(node_data)
        return [output.get_result() for output in self._outputs]

    def verify(self):
        """Validate plan.

        Returns
        -------
        : bool
            True if success, False otherwise.
        : str
            Empty string or description of error.
        """
        if len(self._inputs) == 0:
            return False, "There are no inputs in the plan."
        if len(self._outputs) == 0:
            return False, "There are no outputs in the plan."
        return True, ""

    def __call__(self, data):
        """Run plan."""
        return self._run_func(data)


def get_plan_from_dict(settings):
    """Create and return instance of Plan described in dictionary.

    **Keys**

    - 'descr' - description of the plan (optional)
    - 'nodes' - list of dicts with nodes settings
    - 'inputs' - list of inputs nodes ids
    - 'outputs' - list of output nodes ids

    **Common settings for nodes**

    - 'id' - id of node
    - 'inputs' - list of ids of input nodes for this node
    - 'result' - result description

    **Settings for WorkNode and MapNode**

    - 'work' - dict with work settings

    **Settings for PackNode**

    - 'index' - index of selected item
    """
    LOG.debug("call get_plan_from_dict()")
    plan = Plan()
    if 'descr' in settings:
        plan.set_descr(settings['descr'])

    nodes = {}
    nodes_settings = settings['nodes']
    for node_settings in nodes_settings:
        # LOG.debug('Node settings:{} '.format(node_settings))
        node_id = node_settings['id']
        LOG.debug("Parse node with id={}".format(node_id))

        try:
            node_class = node_settings['class']
        except KeyError:
            node_class = 'WorkNode'

        if node_class == 'WorkNode':
            node = WorkNode()
            work_settings = node_settings['work']
            work = get_work_from_dict(work_settings)
            node.work = work
        elif node_class == 'MapNode':
            node = MapNode()
            work_settings = node_settings['work']
            work = get_work_from_dict(work_settings)
            node.work = work
        elif node_class == 'PackNode':
            node = PackNode()
        elif node_class == 'SelectNode':
            index = node_settings['index']
            node = SelectNode(index)
        else:
            raise ValueError('Unsupported class of node')

        if 'result' in node_settings:
            node.set_result_info(node_settings['result'])

        node.set_id(node_id)
        nodes[node_id] = node

    for node_settings in nodes_settings:
        node_id = node_settings['id']
        if 'inputs' in node_settings.keys():
            inputs = [nodes[key] for key in node_settings['inputs']]
            plan.add_node(nodes[node_id], inputs=inputs)
        else:
            plan.add_node(nodes[node_id])

    if 'inputs' in settings:
        inputs = [nodes[key] for key in settings['inputs']]
        plan.set_inputs(inputs)

    if 'outputs' in settings:
        outputs = [nodes[key] for key in settings['outputs']]
        plan.set_outputs(outputs)

    return plan
