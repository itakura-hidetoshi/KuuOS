# Qi Local Adapter v0.2

This addendum upgrades the prior dry-run adapter surface into a local-effect adapter.

## Position

```text
bounded step plan
  -> local runtime state
  -> append-only local run log
  -> local outbox queue
```

## Local effects

The adapter writes under a caller supplied `runtime_root`.

```text
runtime_state.json
execution_ledger.jsonl
outbox/notifications.jsonl
outbox/tickets.jsonl
outbox/handovers.jsonl
outbox/observations.jsonl
```

## Actions

```text
advance_tick: updates local tick and appends run log
hold: records local hold and appends run log
freeze: records local freeze and appends run log
notify: appends run log and notification outbox row
ticket: appends run log and ticket outbox row
handover: appends run log and handover outbox row
observe: appends run log and observation outbox row
```

## Required local license

```text
license_status = QI_LOCAL_EXECUTION_LICENSE_READY
local_runtime_state_write_allowed = true
local_execution_ledger_append_allowed = true
local_outbox_append_allowed = true for outbox actions
```

## Idempotency

The adapter computes an idempotency key from source packet ids, action, and nonce.
A replay with the same key returns `QI_LOCAL_EXECUTION_ADAPTER_REPLAYED` and does not append a second row.

## Validation

```bash
python scripts/check_qi_local_execution_adapter_v0_2.py
```

Expected:

```text
PASS: Qi local execution adapter v0.2 check
```
