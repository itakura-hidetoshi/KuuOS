# Qi Append-Only Rhythm Receipt Ledger v0.1

This addendum seals `rhythm_entry_candidate` into an append-only JSONL rhythm receipt ledger.

## Position

```text
long-horizon daemon rhythm memory / cadence history layer
  -> append-only rhythm receipt ledger
```

## Core principle

The ledger appends rhythm receipts only. It does not write MemoryOS, overwrite history, update world state, mutate control packets, or execute probes.

```text
rhythm_entry_candidate
  -> deterministic receipt
  -> prev_entry_digest / entry_digest
  -> append-only JSONL ledger
```

## Receipt fields

```text
receipt_id
entry_digest
prev_entry_digest
ledger_root_digest
rhythm_bias
rhythm_mode
cadence_mode
process_tensor_pressure_score
rhythm_stability_score
recommended_window_ticks
delegated_completed_tick_count
delegated_stop_reason
```

## Boundary

The ledger is allowed to append to its own JSONL receipt file, but it is not a MemoryOS writer.

```text
ledger_append_performed = true
memory_write_performed = false
memory_append_performed = false
memory_overwrite_performed = false
world_update_performed = false
control_packet_mutation_performed = false
probe_execution_performed = false
```

## Validation

```bash
python scripts/run_qi_append_only_rhythm_receipt_ledger_checks_v0_1.py
```

Expected result:

```text
PASS: Qi append-only rhythm receipt ledger checks
```

## Next layer

The next layer can add rhythm trend summarization over the append-only ledger, but summary must remain projection-only and must not replace receipt roots.
