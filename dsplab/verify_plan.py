from jsonschema import validate
from dsplab.json_schema import *
import json

class VerifyError(Exception):
    """Verification error."""


def verify_plan_dict(plan_dict):
    """Verify plan dict."""
    with open('dsplab/json-schema.json') as f:
        data = json.load(f)
        try:
            validate(instance=plan_dict, schema = data)
        except Exception as e:
            raise VerifyError(str(e))
    #if len(plan_dict.keys()) == 0:
    #    raise VerifyError("Empty plan")
