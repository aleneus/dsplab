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

""" 
This module implements the Node and Plan classes. Node can be
understood as the workplace for worker. Node can have inputs that are
also nodes. Plan is the system of linked nodes.
"""

from dsplab.activity import Work, get_work_from_dict
from dsplab.helpers import *

class Node:
    """ The node. Node can be understood as the workplace for
    worker. Node can have inputs that are also nodes. """
    def __init__(self, work=None, inputs=[], start_hook=None, stop_hook=None):
        """ Initialization. """
        self._work = work
        self._res = None
        self.start_hook = start_hook
        self.stop_hook = stop_hook
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

    def get_start_hook(self):
        """ Return start hook. """
        return self._start_hook
    def set_start_hook(self, func):
        """ Set start hook. """
        self._start_hook = func
    start_hook = property(get_start_hook, set_start_hook)

    def get_stop_hook(self):
        """ Return stop hook. """
        return self._stop_hook
    def set_stop_hook(self, func):
        """ Set stop hook. """
        self._stop_hook = func
    stop_hook = property(get_stop_hook, set_stop_hook)
    
    def is_output_ready(self) -> bool:
        """ Check if the calculation of data in the node is finished. """
        ans = self._res is not None
        return ans

    def reset(self):
        """ Clear the result. """
        self._res = None

    def is_inputs_ready(self) -> bool:
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
            self._start_hook()
            
        if len(self.inputs) == 0:
            y = self.work(*args, **kwargs)
            self._res = y
        else:
            self._res = None
            x = [inpt.result() for inpt in self._inputs]
            y = self.work(*x)
            self._res = y
            
        if self._stop_hook is not None:
            self._stop_hook()
            
class Transmitter(Node):
    """ The node doing nothing except of transmitting of data from
    input to output. """
    def __init__(self):
        """ Initialization. """
        super().__init__(work=None)
    
    def __call__(self, x):
        """ Run node. """
        self._res = x

class Plan:
    """ The plan. Plan is the system of linked nodes. """
    def __init__(self):
        """ Initialization. 
        
        Parameters
        ----------
        auto_terminals: bool
            If True, the inputs and outputs will be decected
            automatically. Default value is False.

        """
        super().__init__()
        self._nodes = []
        self._inputs = []
        self._outputs = []

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
    outputs = property(get_outputs, set_outputs, doc="The nodes with are outputs.")

    def get_inputs(self):
        """ Return input nodes. """
        return self._inputs
    def set_inputs(self, inputs):
        """ Set input nodes. """
        self._inputs = inputs
    inputs = property(get_inputs, set_inputs, doc="The nodes wich are inputs.")

    def clear(self):
        pass

    def __call__(self, xs):
        """ Run plan. """
        if len(self._inputs) == 0:
            raise RuntimeError("There are no inputs in the plan. ")
        if len(self._outputs) == 0:
            raise RuntimeError("There are no outputs in the plan. ")

        for node in self._nodes:
            node.reset()
            
        for [node, x] in zip(self._inputs, xs):
            node(x)
        
        while True:
            finished = True
            for node in self._nodes:
                if not node.is_output_ready() and node.is_inputs_ready():
                    finished = False
                    node()
            if finished:
                break
            
        ys = [last_node.result() for last_node in self._outputs]
        return ys

def get_plan_from_dict(settings):
    """ Create and return instance of Plan setted from dictionary. """
    p = Plan()
    nodes = {}
    nodes_settings = settings['nodes']
    for node_settings in nodes_settings:
        node_id = node_settings['id']
        nodes[node_id] = Node()
        work_settings = node_settings['work']
        work = get_work_from_dict(work_settings)
        nodes[node_id].work = work
        if 'inputs' in node_settings.keys():
            inputs = [nodes[key] for key in node_settings['inputs']]
            p.add_node(nodes[node_id], inputs=inputs)
        else:
            p.add_node(nodes[node_id])

    if 'inputs' in settings:
        inputs = [nodes[key] for key in settings['inputs']]
        p.set_inputs(inputs)
        
    if 'outputs' in settings:
        outputs = [nodes[key] for key in settings['outputs']]
        p.set_outputs(outputs)

    return p
    

def setup_plan(plan, nodes_settings):
    print("Deprecated: setup_plan(). Use get_plan_from_dict() instead.")
    
    nodes = {}
    inputs = []
    outputs = []
    
    for node_settings in nodes_settings:
        node_id = node_settings['id']
        nodes[node_id] = Node()
        
        work_settings = node_settings['work']

        work = Work()
        work.setup_from_dict(work_settings)
        nodes[node_id].work = work
        
        if 'inputs' in node_settings.keys():
            input_ids = node_settings['inputs']
            plan.add_node(nodes[node_id], inputs=[nodes[v] for v in input_ids])
        else:
            plan.add_node(nodes[node_id])

        if 'input' in node_settings:
            if node_settings['input'] == True:
                inputs.append(nodes[node_id])

        if 'output' in node_settings:
            if node_settings['output'] == True:
                outputs.append(nodes[node_id])

    if len(inputs) > 0:
        plan.set_inputs(inputs)
    if len(outputs) > 0:
        plan.set_outputs(outputs)
        
    return True
