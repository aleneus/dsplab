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


def verify_plan_dict(plan_dict, file_name=SCHEMA_FILE_NAME):
    """Verify plan dict."""
    schema = _load_schema(file_name)
    _validate_schema(plan_dict, schema)


def _load_schema(file_name):
    with open(file_name) as buf:
        data = json.load(buf)

    return data


def _validate_schema(plan_dict, schema):
    try:
        validate(instance=plan_dict, schema=schema)

    except ValidationError as ex:
        raise VerifyError from ex
