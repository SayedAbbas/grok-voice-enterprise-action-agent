from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass
class TraceEvent:
    stage: str
    detail: str


@dataclass
class AgentResult:
    customer_id: str
    intent: str
    proposed_action: str
    policy_decision: str
    action_result: str
    business_outcome: str
    human_approval_required: bool
    boundary_violations: int = 0
    trace: list[TraceEvent] = field(default_factory=list)
