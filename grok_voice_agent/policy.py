"""Deterministic policy boundary. The model does not decide authorization."""

READ_ONLY = {"get_account", "check_outage", "run_diagnostic"}
SAFE_ACTIONS = {"reset_session"}
APPROVAL_REQUIRED = {"issue_credit", "change_plan", "cancel_service"}


def authorize(tool_name: str, requested_customer: str, authenticated_customer: str) -> str:
    if requested_customer != authenticated_customer:
        return "DENY_ACCOUNT_BOUNDARY"
    if tool_name in READ_ONLY or tool_name in SAFE_ACTIONS:
        return "ALLOW"
    if tool_name in APPROVAL_REQUIRED:
        return "REQUIRE_HUMAN_APPROVAL"
    return "DENY_UNKNOWN_ACTION"
