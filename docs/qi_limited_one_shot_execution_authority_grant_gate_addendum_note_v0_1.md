# Qi Limited One-Shot Execution-Authority Grant Gate Addendum Note v0.1

This note documents the first gate that can emit a limited probe execution authority grant.

This gate grants authority only as a local, single-use, revocable token. It does not execute the probe. It does not allow memory writes, world updates, control-packet mutation, scheduler mutation, or persistent authority.

## Position

```text
middle-way authority scope gate
  -> limited one-shot execution-authority grant gate
  -> future one-shot probe executor
```

## Grant semantics

The gate returns:

- `LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED`
- `LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_HOLD`

A grant means only that a future executor may consume the token once if it still verifies all constraints. This gate itself performs no execution.

## Required conditions

- `operator_approved_one_shot`
- `governor_approved_one_shot`
- `single_probe_only`
- `rollback_path_verified`
- `safe_reentry_window_bound`
- `memory_write_forbidden`
- `world_update_forbidden`
- `control_packet_mutation_forbidden`
- `authority_expires_after_use`
- `authority_revocable`

## Forbidden requests

- `request_multi_probe`
- `request_memory_write`
- `request_world_update`
- `request_control_packet_mutation`
- `request_persistent_authority`
- `rollback_unavailable`

## Boundary

- `grants_probe_execution_authority: true` only when all conditions hold
- `grants_execution_authority: true` only when all conditions hold
- `one_shot: true`
- `single_probe_only: true`
- `rollback_required: true`
- `reentry_window_bound: true`
- `authority_expires_after_use: true`
- `authority_revocable: true`
- `memory_write_allowed: false`
- `world_update_allowed: false`
- `control_packet_mutation_allowed: false`
- `probe_execution_performed: false`
- `memory_write_performed: false`
- `world_update_performed: false`

## CLI

```bash
python scripts/write_qi_limited_one_shot_execution_authority_grant_gate_v0_1.py \
  --middle-way-scope .out/qi-supervisor/qi_middle_way_authority_scope_gate.json \
  --context .out/qi-supervisor/qi_limited_one_shot_execution_authority_context.json \
  --write .out/qi-supervisor/qi_limited_one_shot_execution_authority_grant_gate.json
```

## Checks

```bash
python scripts/check_qi_limited_one_shot_execution_authority_grant_gate_v0_1.py
python scripts/check_qi_limited_one_shot_execution_authority_grant_gate_addendum_v0_1.py
python scripts/run_qi_limited_one_shot_execution_authority_grant_checks_v0_1.py
```

## Next integration target

The next step should be a one-shot probe executor that consumes this grant once. That executor must recheck the token, perform at most one probe, and still forbid memory/world/control mutation unless a separate future authority layer is introduced.
