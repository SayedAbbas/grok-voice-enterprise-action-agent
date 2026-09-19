from grok_voice_agent.agent import handle_restore_service
from grok_voice_agent.policy import authorize


def test_safe_recovery_resolves_customer():
    result = handle_restore_service("CUST-1001")
    assert result.business_outcome == "RESOLVED"
    assert result.policy_decision == "ALLOW"
    assert result.boundary_violations == 0


def test_cross_account_action_is_denied():
    assert authorize("reset_session", "CUST-2002", "CUST-1001") == "DENY_ACCOUNT_BOUNDARY"


def test_credit_requires_human_approval():
    assert authorize("issue_credit", "CUST-1001", "CUST-1001") == "REQUIRE_HUMAN_APPROVAL"
