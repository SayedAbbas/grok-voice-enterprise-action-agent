# Grok Voice Enterprise Action Agent

### From conversation to controlled enterprise action.

A production-inspired reference implementation showing how a realtime voice agent can move beyond conversation and safely complete business workflows using **Grok Voice**, enterprise tools, deterministic authorization, evaluation, and human escalation.

> **The conversation can be flexible. The actions remain controlled.**

This project is intentionally built around a business outcome rather than a chatbot demo. The included scenario models a telecom customer calling because their internet is not working. The agent can investigate the account and service state, propose an allowed recovery action, and produce an auditable trace. High-impact actions remain behind deterministic policy and approval boundaries.

All customers, accounts, incidents and metrics in this repository are synthetic.

## What this demonstrates

- Realtime voice-agent architecture with Grok as the conversational reasoning layer
- Enterprise tool contracts for account, outage, diagnostics and recovery workflows
- Deterministic authorization outside the model
- Bounded tool execution and explicit human-escalation paths
- Complete trajectory traces: conversation → reasoning → tool → policy → outcome
- Offline evals that test the **business outcome and action path**, not only the final response
- A local deterministic demo that requires no API key

## 90-second demo path

Run:

~~~bash
python -m grok_voice_agent.demo
~~~

The synthetic customer says:

> “My internet has been down since this morning. Can you fix it?”

The system:

1. resolves the customer account;
2. checks for a known service outage;
3. runs an account diagnostic;
4. asks the reasoning layer for the next allowed action;
5. validates the proposed action against deterministic policy;
6. either executes the safe simulated action or escalates;
7. records the complete trace and business outcome.

Then run:

~~~bash
python -m grok_voice_agent.evals
~~~

The eval suite checks whether the agent used the right tools, respected authorization boundaries, escalated when required, and achieved the expected outcome.

## Architecture

~~~mermaid
flowchart LR
    A["Customer voice"] --> B["Grok Voice / realtime conversation"]
    B --> C["Reasoning + tool selection"]
    C --> D["Enterprise tool gateway"]
    D --> E["Authorization & policy"]
    E -->|Allowed| F["Synthetic enterprise APIs"]
    E -->|Approval required| G["Human escalation"]
    F --> H["Business outcome"]
    G --> H
    C --> I["Trajectory trace"]
    D --> I
    E --> I
    H --> I
    I --> J["Offline / online evals"]
~~~

### Trust boundary

**Model proposes. System authorizes.**

The model never owns account state, permissions, policy, or irreversible business rules. Tool schemas constrain what can be requested; deterministic application code decides what is allowed.

## Business scenario

The reference workflow is deliberately simple enough to understand quickly but realistic enough to expose production concerns.

| Customer need | Agent capability | Control |
|---|---|---|
| “Is there an outage?” | Check service status | Read-only |
| “Why is my service down?” | Run synthetic diagnostic | Read-only |
| “Can you reset it?” | Propose safe recovery | Policy validated |
| “Give me a credit.” | Propose commercial action | Human approval required |
| “Access another account.” | Reject request | Tenant/account boundary |

The primary success metric is not “did the model sound human?” It is:

> **Did the conversation move the customer toward the correct business outcome without crossing an authorization boundary?**

## Quick start

Requires Python 3.10+.

~~~bash
git clone https://github.com/SayedAbbas/grok-voice-enterprise-action-agent.git
cd grok-voice-enterprise-action-agent

python -m grok_voice_agent.demo
python -m grok_voice_agent.evals
~~~

No API key is required for the default demo. The local reasoning adapter is deterministic so the complete control and evaluation path can run in CI.

## Example output

~~~text
Customer intent      : restore_service
Account              : CUST-1001
Outage detected      : false
Diagnostic           : stale_session
Proposed action      : reset_session
Policy decision      : ALLOW
Action result        : service_restored
Human approval       : not_required
Business outcome     : RESOLVED
Boundary violations  : 0
~~~

## Repository map

~~~text
grok_voice_agent/
  demo.py             end-to-end synthetic customer journey
  agent.py            orchestration and tool loop
  tools.py            enterprise tool contracts + synthetic APIs
  policy.py           deterministic authorization boundary
  models.py           typed domain objects
  evals.py            trajectory and business-outcome evaluations
tests/
  test_agent.py       behavioral and safety tests
.github/workflows/
  ci.yml              reproducible CI
docs/
  production-design.md
~~~

## Evaluation philosophy

A good voice demo proves that a conversation is possible. It does not prove that an enterprise agent is safe or useful.

This project evaluates four layers:

1. **Conversation** — did the agent understand the customer's goal?
2. **Tool trajectory** — did it select the right tools and arguments?
3. **Authorization** — were forbidden or approval-required actions handled correctly?
4. **Business outcome** — was the customer resolved, safely escalated, or blocked for the right reason?

> **Observability tells us what happened. Evals tell us whether what happened was acceptable.**

## Production extension

The local demo isolates the application architecture from the realtime transport. A production implementation would connect the conversation layer to the current xAI Voice API, map tool requests into the same gateway, authenticate every enterprise API independently, persist durable workflow state, emit OpenTelemetry-compatible traces, and run online evals against sampled production trajectories.

See [docs/production-design.md](docs/production-design.md).

## Why this project exists

Voice AI becomes materially more valuable when it can do more than answer questions. But increasing autonomy also increases the evidence and control required before deployment.

The design principle is:

**Conversation → Reasoning → Tools → Authorization → Action → Evaluation → Learning**

The higher the consequence and autonomy, the higher the evidence bar.

## Author

Built by [Shabi Abbas Sayed](https://github.com/SayedAbbas), Senior Applied AI Solutions Architect @ AWS and 2× AWS re:Invent speaker.

Related work:

- [Frontier Enterprise Agent Eval Lab](https://github.com/SayedAbbas/enterprise-agent-eval-lab)
- [Production Applied AI](https://github.com/SayedAbbas/production-applied-ai)
- [Managed Services SLA Recovery Agent](https://github.com/SayedAbbas/managed-services-sla-recovery-agent)

This is an independent personal project. It is not an official xAI or AWS project. All enterprise data and outcomes are synthetic.
