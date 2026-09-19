# Production design notes

The local demo focuses on the control plane so it remains runnable without credentials. A production voice deployment should preserve the same separation of responsibilities.

## Realtime layer

The voice session owns audio transport, turn taking, interruption handling and conversational state. The application owns durable business state. A production xAI integration should use the current supported Voice API and model identifiers rather than hard-coding assumptions into the domain layer.

## Tool gateway

Expose narrow business capabilities rather than generic HTTP or database access. Each tool should have a typed schema, authenticated caller context, timeout, idempotency strategy and audit record. Tool output should contain only the data required for the next decision.

## Authorization

Treat model output as a proposal. Re-authorize every requested action using trusted identity and application state. Never rely on a prompt instruction as the enforcement boundary.

## Latency

Voice latency is cumulative. Measure speech transport, model turn time, tool latency and downstream API latency independently. Parallelize independent reads, prefetch safe context, stream conversational acknowledgement where appropriate, and set explicit tool timeouts.

## State and reliability

Keep critical workflow state outside model context. Persist action IDs and approval state. Use retries only for idempotent operations, apply circuit breakers to unhealthy dependencies, and provide a deterministic human handoff path.

## Observability and evals

Trace the full trajectory: session, model turn, proposed tool, validated arguments, policy decision, tool result and outcome. Redact sensitive data before logging. Convert validated production failures into golden regression cases.

Suggested production release loop:

~~~text
Golden cases -> Offline evals -> Release gate -> Canary -> Online evals
      ^                                                   |
      +------------ validated production failures <-------+
~~~

## Security checklist

- authenticate the caller independently of model context
- authorize each action at execution time
- use least-privilege service identities
- validate all tool arguments
- isolate tenant/account data before inference
- redact secrets and sensitive fields from traces
- require explicit approval for high-impact actions
- maintain immutable audit evidence for executed actions
