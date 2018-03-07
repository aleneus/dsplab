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
    def __init__(self, work=None, inputs=[]):
        """ Initialization. """
        self._work = work
        self._res = None
        self.set_inputs(inputs)

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
        if x is not None:
            y = self.work(x)
            self._res = y
            return
        
        self._res = None
        if len(self._inputs) == 1:
            x = self._inputs[0].result()
        else:
            x = [inpt.result() for inpt in self._inputs]
        y = self.work(x)
        self._res = y
    
class Plan:
    """ The plan. Plan is the system of linked nodes. """
    def __init__(self):
        """ Initialization. """
        super().__init__()
        self._nodes = []
        self._first_nodes = []
        self._last_nodes = []

    def _detect_terminals(self):
        """ Detect first and last nodes. """
        self._first_nodes = []
        all_inputs = []
        for node in self._nodes:
            if len(node.inputs) == 0:
                self._first_nodes.append(node)
            for inpt in node.inputs:
                if inpt not in all_inputs:
                    all_inputs.append(inpt)

        self._last_nodes = []
        for node in self._nodes:
            if node not in all_inputs:
                self._last_nodes.append(node)

    def add_node(self, node, inputs=[]):
        """ Add node to plan. """
        self._nodes.append(node)
        if len(inputs) > 0:
            node.inputs = inputs

    def __call__(self, xs):
        """ Run plan. """
        self._detect_terminals()
        for [node, x] in zip(self._first_nodes, xs):
            node(x)
        
        while True:
            finished = True
            for node in self._nodes:
                if not node.is_output_ready() and node.is_inputs_ready():
                    finished = False
                    node()
            if finished:
                break
            
        ys = [last_node.result() for last_node in self._last_nodes]
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
