# Qi Probe Execution Candidate Addendum Note v0.1

This note documents the first step after the process-tensor-aware scheduler state.

The probe execution candidate is not probe execution authority. It is a candidate packet for operator and governor review after the scheduler reaches `DUE`.

## Position

```text
process-tensor-aware scheduler state
  -> probe execution candidate
  -> operator / governor review
```

## Required source state

The candidate builder expects a process-tensor-aware scheduler surface with:

- `adjustment_status: QI_PROCESS_TENSOR_AWARE_SCHEDULER_STATE_UPDATED`
- nested `scheduler_result.scheduler_status: QI_SCHEDULER_STATE_UPDATED`
- nested `scheduler_result.due_status: DUE`
- a visible `scheduled_probe_type`

If the scheduler state is `WAIT` or `BLOCKED`, candidate creation is blocked.

## Authority boundary

The candidate packet is intentionally non-executing:

- `execution_candidate_only: true`
- `scheduler_due_required: true`
- `requires_operator_review: true`
- `requires_governor_approval: true`
- `authority: none`
- `grants_execution_authority: false`
- `grants_probe_execution_authority: false`
- `grants_dry_run_execution_authority: false`
- `grants_next_tick_execution_authority: false`
- `grants_scheduler_authority: false`
- `grants_control_packet_authority: false`
- `grants_memory_overwrite_authority: false`
- `grants_world_update_authority: false`

It also records that no mutation or execution occurred:

- `scheduler_state_mutation_performed: false`
- `control_packet_mutation_performed: false`
- `probe_execution_performed: false`
- `dry_run_execution_performed: false`
- `next_tick_execution_performed: false`
- `memory_write_performed: false`
- `world_update_performed: false`

## CLI

```bash
python scripts/write_qi_probe_execution_candidate_v0_1.py \
  --scheduler .out/qi-supervisor/qi_process_tensor_aware_scheduler_result.json \
  --write .out/qi-supervisor/qi_probe_execution_candidate.json
```

## Checks

```bash
python scripts/check_qi_probe_execution_candidate_v0_1.py
python scripts/check_qi_probe_execution_candidate_addendum_v0_1.py
python scripts/run_qi_process_tensor_scheduler_checks_v0_1.py
```

## Next integration target

The next step should connect the candidate addendum to the operator runbook and review workflow. The next step should still avoid opening real probe execution authority unless a separate authority gate is introduced.
