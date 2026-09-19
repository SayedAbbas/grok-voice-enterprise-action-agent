from .agent import handle_restore_service


def main() -> None:
    result = handle_restore_service("CUST-1001")
    print("Grok Voice Enterprise Action Agent — synthetic demo\n")
    print('Customer            : "My internet has been down since this morning. Can you fix it?"')
    print(f"Customer intent      : {result.intent}")
    print(f"Account              : {result.customer_id}")
    print(f"Proposed action      : {result.proposed_action}")
    print(f"Policy decision      : {result.policy_decision}")
    print(f"Action result        : {result.action_result}")
    print(f"Human approval       : {'required' if result.human_approval_required else 'not_required'}")
    print(f"Business outcome     : {result.business_outcome}")
    print(f"Boundary violations  : {result.boundary_violations}")
    print("\nTrajectory")
    for event in result.trace:
        print(f"  [{event.stage}] {event.detail}")


if __name__ == "__main__":
    main()
