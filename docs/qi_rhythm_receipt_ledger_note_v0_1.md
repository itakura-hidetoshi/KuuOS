# Qi Rhythm Receipt Ledger v0.1

This addendum introduces an append-only JSONL receipt ledger for rhythm cadence history candidates.

## Position

```text
long-horizon daemon rhythm memory / cadence history layer
  -> append-only rhythm receipt ledger
```

## Core principle

The ledger writes a receipt only when an explicit `rhythm_entry_candidate` is provided and ledger context requires append-only JSONL behavior.

```text
rhythm_entry_candidate
  -> deterministic rhythm receipt
  -> append-only JSONL ledger
```

## Receipt fields

```text
receipt_id
receipt_digest
root_id
ledger_scope
rhythm_mode
rhythm_bias
cadence_mode
process_tensor_pressure_score
rhythm_stability_score
recommended_window_ticks
delegated_completed_tick_count
delegated_stop_reason
```

## Safety boundary

The ledger does not grant execution authority, probe authority, world authority, memory overwrite authority, or semantic memory authority.

```text
append_only_enforced = true
memory_write_performed = false
memory_append_performed = false
memory_overwrite_performed = false
world_update_performed = false
control_packet_mutation_performed = false
probe_execution_performed = false
grants_probe_execution_authority = false
grants_world_update_authority = false
grants_memory_overwrite_authority = false
```

`memory_append_performed` remains false because this layer appends to a receipt ledger, not to MemoryOS fact authority.

## Validation

```bash
python scripts/run_qi_rhythm_receipt_ledger_checks_v0_1.py
```

Expected result:

```text
PASS: Qi rhythm receipt ledger checks
```
