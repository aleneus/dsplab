# Copyright (C) 2017-2021 Aleksandr Popov
# Copyright (C) 2021 Kirill Butin

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

"""Verification of the plan."""

import json
from pkg_resources import resource_filename as resource
from jsonschema import validate
from jsonschema.exceptions import ValidationError

SCHEMA_FILE_NAME = resource('dsplab', 'data/plan-schema.json')


class VerifyError(Exception):
    """Verification error."""


def check_plan(plan_dict):
    """Check plan's dictionary."""

    schema = _load_schema(SCHEMA_FILE_NAME)
    _check_plan_schema(plan_dict, schema)

    ids = _get_ids(plan_dict)

    for node in plan_dict["nodes"]:
        _check_node(node, ids)

    _check_plan_inputs(plan_dict, ids)
    _check_plan_outputs(plan_dict, ids)


#
# plan

def _check_plan_schema(plan_dict, schema):
    try:
        validate(instance=plan_dict, schema=schema)

    except ValidationError as ex:
        raise VerifyError from ex


def _check_plan_inputs(plan_dict, ids):
    for inp in _get_plan_inputs(plan_dict):
        if inp not in ids:
            raise VerifyError("Unknown plan input: {}".format(inp))


def _check_plan_outputs(plan_dict, ids):
    for out in _get_plan_outputs(plan_dict):
        if out not in ids:
            raise VerifyError("Unknown plan output: {}".format(out))


def _get_ids(plan_dict):
    ids = {}
    for node in plan_dict["nodes"]:
        node_id = node["id"]
        if node_id in ids:
            raise VerifyError("Duplicated ID: {}".format(node_id))
        ids[node_id] = node
    return ids


def _get_plan_inputs(plan_dict):
    return _get_value_or_list(plan_dict, "inputs")


def _get_plan_outputs(plan_dict):
    return _get_value_or_list(plan_dict, "outputs")


#
# node

def _check_node(node_dict, ids):
    _check_node_inputs(node_dict, ids)

    if _get_node_class(node_dict) in ["WorkNode", "MapNode"]:
        if "work" not in node_dict:
            raise VerifyError("No work in node {}".format(node_dict["id"]))


def _check_node_inputs(node_dict, ids):
    node_id = node_dict["id"]
    for inp in _get_node_inputs(node_dict):
        if inp not in ids:
            raise VerifyError("Unknown input {} in node {}".
                              format(inp, node_id))

        if inp == node_id:
            raise VerifyError("Node {} uses itself as input".format(inp))


def _get_node_inputs(node_dict):
    return _get_value_or_list(node_dict, "inputs")


def _get_node_class(node_dict):
    if "class" in node_dict:
        return node_dict["class"]
    return "WorkNode"


#
# common

def _load_schema(file_name):
    with open(file_name) as buf:
        data = json.load(buf)

    return data


def _get_value_or_list(dct, key):
    if key not in dct:
        return []
    return dct[key]
