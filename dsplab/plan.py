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

from dsplab.activity import Work
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

    def is_inputs_ready(self) -> bool:
        """ Check if data in all inputs is ready. """
        for inpt in self._inputs:
            if not inpt.is_output_ready():
                return False
        return True

    def result(self):
        """ Return the calculated data. """
        return self._res

    def __call__(self, x=None):
        """ Run node. """
        if self._start_hook is not None:
            self._start_hook()
            
        if x is not None:
            y = self.work(x)
            self._res = y
        else:
            self._res = None
            if len(self._inputs) == 1:
                x = self._inputs[0].result()
            else:
                x = [inpt.result() for inpt in self._inputs]
            y = self.work(x)
            self._res = y
            
        if self._stop_hook is not None:
            self._stop_hook()

class Translator(Node):
    def __init__(self):
        super().__init__(work=None)
    
    def __call__(self, x):
        self._res = x

class Plan:
    """ The plan. Plan is the system of linked nodes. """
    def __init__(self, auto_terminals=False):
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
        self._auto_terminals = auto_terminals

    def _detect_terminals(self):
        """ Detect first and last nodes. """
        self._inputs = []
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
        if self._auto_terminals:
            self._detect_terminals()

    def remove_node(self, node):
        """ Remove node from plan. """
        if node not in self._nodes:
            raise RuntimeError("No such node")
        for n in self._nodes:
            if node in n.inputs:
                n.inputs.remove(node)
        self._nodes.remove(node)
        if self._auto_terminals:
            self._detect_terminals()

    def get_outputs(self):
        """ Return output nodes. """
        return self._outputs
    def set_outputs(self, outputs):
        """ Set output nodes. """
        if self._auto_terminals:
            raise RuntimeError("Auto detection of terminals is setted on.")
        self._outputs = outputs
    outputs = property(get_outputs, set_outputs, doc="The nodes with are outputs.")

    def get_inputs(self):
        """ Return input nodes. """
        return self._inputs
    def set_inputs(self, inputs):
        """ Set input nodes. """
        if self._auto_terminals:
            raise RuntimeError("Auto detection of terminals is setted on.")
        self._inputs = inputs
    inputs = property(get_inputs, set_inputs, doc="The nodes wich are inputs.")

    def __call__(self, xs):
        """ Run plan. """
        if len(self._inputs) == 0:
            raise RuntimeError("There are no inputs in the plan. ")
        if len(self._outputs) == 0:
            raise RuntimeError("There are no outputs in the plan. ")
        
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

def setup_plan(plan: Plan, nodes_settings) -> bool:
    """ Setup plan using dict settings. """
    nodes = {}
    
    for node_settings in nodes_settings:
        node_id = node_settings['id']
        nodes[node_id] = Node()
        
        work_settings = node_settings['work']
        if 'descr' in work_settings.keys():
            work_descr = work_settings['descr']
        else:
            work_descr = ""
        
        worker_settings = work_settings['worker']
        worker_class = worker_settings['class']
        
        if 'params' in worker_settings.keys():
            worker_params = worker_settings['params']
            worker = import_entity(worker_class)(**worker_params)
        else:
            worker = import_entity(worker_class)

        work = Work(work_descr, worker)
        nodes[node_id].work = work
        
        if 'inputs' in node_settings.keys():
            input_ids = node_settings['inputs']
            plan.add_node(nodes[node_id], inputs=[nodes[v] for v in input_ids])
        else:
            plan.add_node(nodes[node_id])
        
    return True
