---
name: kuuos-control
description: Use KuuOS as the upper control plane for OpenClaw; keep external effects behind ActOS authorization and preserve host receipts as non-WORLD truth.
---

# KuuOS control boundary

Treat OpenClaw as a bounded execution host beneath KuuOS.

The canonical authority direction is:

`DecisionOS / PlanOS -> ActOS -> KuuOS OpenClaw control service -> OpenClaw tool host`.

Before an effectful tool call, preserve the exact selected operation, inputs, resource scope, stop conditions, and verification criterion. Do not reinterpret a host receipt as WORLD truth, plan completion, rollback authority, clinical authority, legal authority, institutional authority, or theorem authority.

After an external effect, leave observation and verification debt open until KuuOS closes them through its own authority chain.

Do not bypass a KuuOS block. If KuuOS asks for approval, use the OpenClaw approval path. If the KuuOS control service is unavailable, expect effectful work to fail closed.
