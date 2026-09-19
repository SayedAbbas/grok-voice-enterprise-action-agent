from .models import AgentResult, TraceEvent
from .policy import authorize
from .tools import check_outage, get_account, reset_session, run_diagnostic


def handle_restore_service(customer_id: str, authenticated_customer: str | None = None) -> AgentResult:
    authenticated_customer = authenticated_customer or customer_id
    trace: list[TraceEvent] = []
    violations = 0

    account = get_account(customer_id)
    trace.append(TraceEvent("tool", f"get_account -> found={account.get('found')}"))
    if not account.get("found"):
        return AgentResult(customer_id, "restore_service", "none", "ALLOW", "account_not_found", "ESCALATED", True, 0, trace)

    outage = check_outage(account["region"])
    trace.append(TraceEvent("tool", f"check_outage -> outage={outage['outage']}"))
    if outage["outage"]:
        return AgentResult(customer_id, "restore_service", "none", "ALLOW", "known_outage", "INFORMED", False, 0, trace)

    diagnostic = run_diagnostic(customer_id)
    trace.append(TraceEvent("tool", f"run_diagnostic -> {diagnostic['diagnostic']}"))

    proposed = "reset_session" if diagnostic["diagnostic"] == "stale_session" else "none"
    trace.append(TraceEvent("reasoning", f"proposed_action={proposed}"))
    if proposed == "none":
        return AgentResult(customer_id, "restore_service", proposed, "ALLOW", "no_safe_recovery", "ESCALATED", True, 0, trace)

    decision = authorize(proposed, customer_id, authenticated_customer)
    trace.append(TraceEvent("policy", decision))
    if decision != "ALLOW":
        violations = 1 if decision.startswith("DENY") else 0
        return AgentResult(customer_id, "restore_service", proposed, decision, "not_executed", "BLOCKED", decision != "ALLOW", violations, trace)

    action = reset_session(customer_id)
    trace.append(TraceEvent("action", f"reset_session -> {action['status']}"))
    outcome = "RESOLVED" if action["status"] == "service_restored" else "ESCALATED"
    return AgentResult(customer_id, "restore_service", proposed, decision, action["status"], outcome, False, violations, trace)
