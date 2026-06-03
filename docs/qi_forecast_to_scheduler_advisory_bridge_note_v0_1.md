# Qi Forecast-to-Scheduler Advisory Bridge v0.1

This addendum turns a projection-only rhythm trend forecast into bounded scheduler advisory hints.

## Position

```text
rhythm trend summarizer / projection-only cadence forecast
  -> forecast-to-scheduler advisory bridge
```

## Core principle

Forecast does not directly set the scheduler window. The bridge emits advisory hints only.

```text
forecast packet
  -> advisory context patch
  -> adaptive / rhythm scheduler may read hints
```

## Advisory outputs

```text
advisory_packet_id
source_forecast_packet_id
source_ledger_root_digest
source_last_entry_digest
forecast_window_bias
forecast_cadence_mode_hint
forecast_risk_class
advisory_min_window_ticks_hint
advisory_max_window_ticks_hint
advisory_cadence_mode_hint
advisory_reason
```

## Boundary

```text
advisory_only = true
scheduler_context_patch_authoritative = false
forecast_directly_sets_window = false
bounded_hint_enforced = true
replaces_forecast_packet = false
replaces_ledger_root = false
memory_write_performed = false
memory_append_performed = false
memory_overwrite_performed = false
world_update_performed = false
control_packet_mutation_performed = false
probe_execution_performed = false
```

## Validation

```bash
python scripts/check_qi_forecast_to_scheduler_advisory_bridge_v0_1.py
```

Expected result:

```text
PASS: Qi forecast-to-scheduler advisory bridge check
```

## Next layer

The next layer can let rhythm memory read the advisory patch as an optional bounded hint, but the scheduler must continue to compute its own window from live process tensor state.
