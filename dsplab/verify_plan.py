class VerifyError(Exception):
    """Verification error."""


def verify_plan_dict(plan_dict):
    """Verify plan dict."""
    if len(plan_dict.keys()) == 0:
        raise VerifyError("Empty plan")
