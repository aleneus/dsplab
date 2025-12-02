"""Verification of the plan."""

import json
from importlib.resources import files

from jsonschema import validate
from jsonschema.exceptions import ValidationError

SCHEMA_FILE_NAME = files('dsplab').joinpath('data/plan-schema.json')


class VerifyError(Exception):
    """Verification error."""


def check_plan(plan_dict):
    """Check plan's dictionary."""

    schema = _load_schema(SCHEMA_FILE_NAME)
    _check_plan_schema(plan_dict, schema)

    ids = _get_ids(plan_dict)

    for node in plan_dict['nodes']:
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
            raise VerifyError(f'Unknown plan input: {inp}')


def _check_plan_outputs(plan_dict, ids):
    for out in _get_plan_outputs(plan_dict):
        if out not in ids:
            raise VerifyError(f'Unknown plan output: {out}')


def _get_ids(plan_dict):
    ids = {}
    for node in plan_dict['nodes']:
        node_id = node['id']
        if node_id in ids:
            raise VerifyError(f'Duplicated ID: {node_id}')

        ids[node_id] = node

    return ids


def _get_plan_inputs(plan_dict):
    return _get_value_or_list(plan_dict, 'inputs')


def _get_plan_outputs(plan_dict):
    return _get_value_or_list(plan_dict, 'outputs')


#
# node


def _check_node(node_dict, ids):
    _check_node_inputs(node_dict, ids)

    if _get_node_class(node_dict) in ['WorkNode', 'MapNode']:
        if 'work' not in node_dict:
            node_id = node_dict['id']

            raise VerifyError(f'No work in node {node_id}')


def _check_node_inputs(node_dict, ids):
    node_id = node_dict['id']
    for inp in _get_node_inputs(node_dict):
        if inp not in ids:
            raise VerifyError(f'Unknown input {inp} in node {node_id}')

        if inp == node_id:
            raise VerifyError(f'Node {inp} uses itself as input')


def _get_node_inputs(node_dict):
    return _get_value_or_list(node_dict, 'inputs')


def _get_node_class(node_dict):
    if 'class' in node_dict:
        return node_dict['class']

    return 'WorkNode'


#
# common


def _load_schema(file_name):
    with open(file_name, encoding='utf-8') as buf:
        return json.load(buf)


def _get_value_or_list(dct, key):
    if key not in dct:
        return []

    return dct[key]
