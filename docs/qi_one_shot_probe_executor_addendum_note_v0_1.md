# Qi One-Shot Probe Executor Addendum Note v0.1

This note documents the first one-shot executor after the limited one-shot execution-authority grant gate.

The executor consumes a `single_use_probe_execution_authority` token and emits an artifact-only probe result. It does not preserve authority after use, and it does not mutate memory, world state, scheduler state, or control packets.

## Position

```text
limited one-shot execution-authority grant gate
  -> one-shot probe executor
  -> artifact-only probe result
```

## Execution semantics

The executor may return:

- `QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED`
- `QI_ONE_SHOT_PROBE_EXECUTION_BLOCKED`

A performed result means exactly one probe was executed and the token was consumed.

## Authority consumption

The executor requires:

- `gate_status: QI_LIMITED_ONE_SHOT_EXECUTION_AUTHORITY_GRANT_GATE_READY`
- `grant_outcome: LIMITED_ONE_SHOT_PROBE_EXECUTION_AUTHORITY_GRANTED`
- `authority_token_kind: single_use_probe_execution_authority`
- `grants_probe_execution_authority: true`
- `grants_execution_authority: true`
- `one_shot: true`
- `single_probe_only: true`
- `rollback_required: true`
- `reentry_window_bound: true`
- `authority_expires_after_use: true`
- `authority_revocable: true`

After consuming the token, the executor output resets authority grants:

- `grants_probe_execution_authority: false`
- `grants_execution_authority: false`
- `grants_memory_overwrite_authority: false`
- `grants_world_update_authority: false`

## Boundary

The executor remains artifact-only:

- `probe_result_artifact_only: true`
- `one_shot_token_consumed: true`
- `token_reuse_allowed: false`
- `single_probe_only: true`
- `rollback_required: true`
- `reentry_window_bound: true`
- `probe_execution_performed: true` only when all checks pass
- `memory_write_performed: false`
- `world_update_performed: false`
- `control_packet_mutation_performed: false`
- `scheduler_state_mutation_performed: false`

## Blockers

The executor blocks if it sees:

- `token_already_consumed`
- `request_multi_probe`
- `request_memory_write`
- `request_world_update`
- `request_control_packet_mutation`
- `request_scheduler_mutation`

## CLI

```bash
python scripts/write_qi_one_shot_probe_executor_v0_1.py \
  --grant .out/qi-supervisor/qi_limited_one_shot_execution_authority_grant_gate.json \
  --probe-payload .out/qi-supervisor/qi_one_shot_probe_payload.json \
  --write .out/qi-supervisor/qi_one_shot_probe_result.json
```

## Checks

```bash
python scripts/check_qi_one_shot_probe_executor_v0_1.py
python scripts/check_qi_one_shot_probe_executor_addendum_v0_1.py
python scripts/run_qi_one_shot_probe_executor_checks_v0_1.py
```

## Next integration target

The next step should append the artifact-only probe result into the process-tensor review flow. That append should still avoid memory/world/control mutation unless a separate future authority layer grants it.
