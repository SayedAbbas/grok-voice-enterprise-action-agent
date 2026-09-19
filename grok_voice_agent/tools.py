"""Synthetic enterprise APIs. Replace these adapters with authenticated APIs in production."""

ACCOUNTS = {
    "CUST-1001": {"status": "active", "region": "mumbai-west", "session": "stale"},
    "CUST-2002": {"status": "active", "region": "mumbai-east", "session": "healthy"},
}


def get_account(customer_id: str) -> dict:
    if customer_id not in ACCOUNTS:
        return {"found": False}
    return {"found": True, **ACCOUNTS[customer_id]}


def check_outage(region: str) -> dict:
    return {"outage": region == "mumbai-east"}


def run_diagnostic(customer_id: str) -> dict:
    account = ACCOUNTS.get(customer_id)
    if not account:
        return {"diagnostic": "unknown_account"}
    return {"diagnostic": "stale_session" if account["session"] == "stale" else "healthy"}


def reset_session(customer_id: str) -> dict:
    account = ACCOUNTS.get(customer_id)
    if not account:
        return {"status": "failed"}
    account["session"] = "healthy"
    return {"status": "service_restored"}
