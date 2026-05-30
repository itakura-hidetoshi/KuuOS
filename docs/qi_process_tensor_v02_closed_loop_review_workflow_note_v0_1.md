# Qi Process Tensor v0.2 Closed-Loop Review Workflow Note v0.1

This note documents the v0.2 closed-loop review surface for the Qi Process Tensor Daemon.

The closed loop is a formal step in `.github/workflows/qi-process-tensor-review.yml`.

## Closed-loop path

```text
v0.2 append-only MemoryOS writeback
  -> MemoryOS process-tensor retrieval/replay
  -> scheduler state replay-hint apply
  -> probe scheduler proposal reuse
  -> process-tensor-aware scheduler state v0.2 reintegration
```

## Workflow step

```bash
python scripts/run_qi_v02_memoryos_replay_loop_closure_checks.py
```

The addendum manifest is checked with:

```bash
python scripts/check_qi_process_tensor_review_v02_closed_loop_workflow_addendum_v0_1.py
```

## Authority boundary

Allowed within the closed-loop review surface:

- `memory_read_only`
- `scheduler_state_only`
- `workflow_ci_only`
- `scheduler_state_mutation_performed: true`
- `scheduler_update_scope: replay_hint_only`

Still forbidden:

- probe execution authority during replay
- world update authority
- control packet authority
- memory overwrite authority
- MemoryOS write during replay

## Operational meaning

The v0.2 loop lets MemoryOS process-tensor history influence the next scheduler state through replay hints. It does not convert replay into execution. Execution remains behind the existing candidate, review, two-truths, middle-way, and one-shot grant chain.

## Additive status

This note and the corresponding manifest are additive-only. They do not replace `qi_process_tensor_review_bundle_manifest_v0_1.json`; they extend it with a v0.2 closed-loop workflow layer.
