# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This module implements the Node and Plan classes. Node can be
understood as the workplace for worker. Node can have inputs that are
also nodes. Plan is the system of linked nodes. """

from dsplab.activity import get_work_from_dict
from dsplab.activity import Activity


class Node:
    """ The node. Node can be understood as the workplace for
    worker. Node can have inputs that are also nodes. """
    def __init__(self, work=None, inputs=[]):
        """ Initialization. """
        self._work = work
        self._res = None
        self._start_hook = None
        self._start_hook_args = None
        self._start_hook_kwargs = None
        self._stop_hook = None
        self._stop_hook_args = None
        self._stop_hook_kwargs = None
        self.inputs = inputs

    def get_work(self):
        return self._work

    def set_work(self, work):
        self._work = work

    work = property(get_work, set_work)

    def get_inputs(self):
        """ Return inputs. """
        return self._inputs

    def set_inputs(self, inputs):
        """ Set inputs. """
        self._inputs = inputs

    inputs = property(get_inputs, set_inputs)

    def set_start_hook(self, func, *args, **kwargs):
        """ Set start hook. """
        self._start_hook = func
        self._start_hook_args = args
        self._start_hook_kwargs = kwargs

    def set_stop_hook(self, func, *args, **kwargs):
        """ Set stop hook. """
        self._stop_hook = func
        self._stop_hook_args = args
        self._stop_hook_kwargs = kwargs

    def is_output_ready(self):
        """ Check if the calculation of data in the node is finished. """
        ans = self._res is not None
        return ans

    def reset(self):
        """ Clear the result. """
        self._res = None

    def is_inputs_ready(self):
        """ Check if data in all inputs is ready. """
        for inpt in self._inputs:
            if not inpt.is_output_ready():
                return False
        return True

    def result(self):
        """ Return the calculated data. """
        return self._res

    def __call__(self, *args, **kwargs):
        if self._start_hook is not None:
            self._start_hook(*self._start_hook_args, *self._start_hook_kwargs)

        if len(self.inputs) == 0:
            y = self.work(*args, **kwargs)
            self._res = y
        else:
            self._res = None
            x = [inpt.result() for inpt in self._inputs]
            y = self.work(*x)
            self._res = y

        if self._stop_hook is not None:
            self._stop_hook(*self._stop_hook_args, *self._stop_hook_kwargs)


class Transmitter(Node):
    """ The node doing nothing except of transmitting of data from
    input to output. """
    def __init__(self):
        """ Initialization. """
        super().__init__(work=None)

    def __call__(self, x):
        """ Run node. """
        self._res = x


class Plan(Activity):
    """ The plan. Plan is the system of linked nodes. """
    def __init__(self, descr=None):
        super().__init__()
        if descr is not None:
            self._info['descr'] = descr
        self._nodes = []
        self._inputs = []
        self._outputs = []
        self._progress_func = None

    def _detect_terminals(self):
        """ Detect first and last nodes. """
        self._inputs = []
        self._outputs = []
        all_inputs = []
        for node in self._nodes:
            if len(node.inputs) == 0:
                self._inputs.append(node)
            for inpt in node.inputs:
                if inpt not in all_inputs:
                    all_inputs.append(inpt)

        for node in self._nodes:
            if node not in all_inputs:
                self._outputs.append(node)

    def add_node(self, node, inputs=[]):
        """ Add node to plan. """
        self._nodes.append(node)
        if len(inputs) > 0:
            node.inputs = inputs
        self._detect_terminals()

    def remove_node(self, node):
        """ Remove node from plan. """
        if node not in self._nodes:
            raise RuntimeError("No such node")
        for n in self._nodes:
            if node in n.inputs:
                n.inputs.remove(node)
        self._nodes.remove(node)
        self._detect_terminals()

    def get_outputs(self):
        """ Return output nodes. """
        return self._outputs

    def set_outputs(self, outputs):
        """ Set output nodes. """
        self._outputs = outputs

    outputs = property(
        get_outputs,
        set_outputs,
        doc="The nodes with are outputs."
    )

    def get_inputs(self):
        """ Return input nodes. """
        return self._inputs

    def set_inputs(self, inputs):
        """ Set input nodes. """
        self._inputs = inputs

    inputs = property(get_inputs, set_inputs, doc="The nodes wich are inputs.")

    def clear(self):
        pass

    def info(self, as_string=False):
        """ Return info about the plan. """
        nodes_info = []
        for node in self._nodes:
            node_info = {}
            work_info = node.work.info().copy()
            node_info['work'] = work_info
            input_ids = []
            for input_obj in node.inputs:
                input_id = '{}'.format(self._nodes.index(input_obj))
                input_ids.append(input_id)
            node_info['id'] = '{}'.format(self._nodes.index(node))
            if len(input_ids) != 0:
                node_info['inputs'] = input_ids
            nodes_info.append(node_info)
        self._info['nodes'] = nodes_info

        plan_input_ids = []
        for input_obj in self.inputs:
            plan_input_id = '{}'.format(self._nodes.index(input_obj))
            plan_input_ids.append(plan_input_id)
        self._info['inputs'] = plan_input_ids

        plan_output_ids = []
        for output_obj in self.outputs:
            plan_output_id = '{}'.format(self._nodes.index(output_obj))
            plan_output_ids.append(plan_output_id)
        self._info['outputs'] = plan_output_ids

        res = super().info(as_string)
        return res

    def get_nodes(self):
        """ Return list of nodes. """
        return self._nodes

    def set_progress_hook(self, func):
        """ Set progress handler. """
        self._progress_func = func

    def __call__(self, xs):
        """ Run plan. """
        if len(self._inputs) == 0:
            raise RuntimeError("There are no inputs in the plan. ")
        if len(self._outputs) == 0:
            raise RuntimeError("There are no outputs in the plan. ")

        for node in self._nodes:
            node.reset()

        progress = 0
        nodes_number = len(self._nodes)

        for [node, x] in zip(self._inputs, xs):
            node(x)
            progress += 1
            if self._progress_func is not None:
                self._progress_func()

        while True:
            finished = True
            for node in self._nodes:
                if not node.is_output_ready() and node.is_inputs_ready():
                    finished = False
                    node()
                    progress += 1
                    if self._progress_func is not None:
                        self._progress_func()
            if finished:
                break

        ys = [last_node.result() for last_node in self._outputs]
        return ys


def get_plan_from_dict(settings):
    """ Create and return instance of Plan setted from dictionary.

    **Keys**

    - 'descr' - description of the plan (optional)
    - 'nodes' - list of dicts with nodes settings
    - 'inputs' - list of inputs nodes ids
    - 'outputs' - list of output nodes ids

    **Node settings**

    - 'id' - id of node
    - 'work' - dict with work settings
    - 'inputs' - list of ids of input nodes for this node

    """
    plan = Plan()
    if 'descr' in settings:
        plan.set_descr(settings['descr'])

    nodes = {}
    nodes_settings = settings['nodes']
    for node_settings in nodes_settings:
        node_id = node_settings['id']
        nodes[node_id] = Node()
        work_settings = node_settings['work']
        work = get_work_from_dict(work_settings)
        nodes[node_id].work = work

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
