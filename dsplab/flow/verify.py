# Copyright (C) 2017-2020 Aleksandr Popov

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


def check_plan(plan_dict, file_name=SCHEMA_FILE_NAME):
    """Check plan's dictionary."""

    schema = _load_schema(file_name)
    _validate_schema(plan_dict, schema)

    nodes = plan_dict["nodes"]

    ids = {}

    for node in nodes:
        id = node["id"]
        if id in ids:
            raise VerifyError(f"Duplicated ID: {id}")
        ids[id] = node

    for node in nodes:
        id = node["id"]
        if "inputs" in node:
            inputs = node["inputs"]
            for inp_id in inputs:
                if inp_id not in ids:
                    raise VerifyError(f"Unknown input {inp_id} in node {id}")
                if inp_id == id:
                    raise VerifyError(f"Node {id} uses itself as input")

        workInNode = "work" in node
        if "class" in node:
            nodeClass = node["class"]
            if (nodeClass in ["WorkNode", "MapNode"]):
                if (not workInNode):
                    raise VerifyError(f"No work in node {id}")
            else:
                if (workInNode):
                    raise VerifyError(f"There must be no work in node {id}")

        else:
            if not workInNode:
                raise VerifyError(f"No work in node {id}")


    if "inputs" in plan_dict:
        inputs = plan_dict["inputs"]
        for inp_id in inputs:
            if inp_id not in ids:
                raise VerifyError(f"Unknown plan input: {inp_id}")

    if "outputs" in plan_dict:
        outs = plan_dict["outputs"]
        for out_id in outs:
            if out_id not in ids:
                raise VerifyError(f"Unknown plan output: {out_id}")


def _load_schema(file_name):
    with open(file_name) as buf:
        data = json.load(buf)

    return data


def _validate_schema(plan_dict, schema):
    try:
        validate(instance=plan_dict, schema=schema)

    except ValidationError as ex:
        raise VerifyError from ex
