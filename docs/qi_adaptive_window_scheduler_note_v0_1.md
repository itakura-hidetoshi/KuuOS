# Qi Adaptive Window Scheduler v0.1

This addendum introduces a pressure-aware cadence governor above the autonomous multi-tick window governor.

## Position

```text
autonomous multi-tick window governor
  -> adaptive window scheduler / pressure-aware cadence governor
```

## Core principle

The adaptive scheduler does not execute ticks directly. It computes a bounded window packet and delegates execution to the existing multi-tick window governor.

```text
adaptive scheduler
  -> bounded adaptive window packet
  -> autonomous multi-tick window governor
  -> per-tick receipt / loop binding
  -> safe resume controller exactly one tick at a time
```

## Inputs

```text
process tensor pressure
memory_complexity_score
QCMI value
recovery_witness_present
non_markov_unresolved
token budget
observation debt
safe reentry window
memory kernel preservation
```

## Cadence modes

```text
wide_compressed_window
moderate_guarded_window
single_tick_high_pressure
observe_first_single_tick
full_history_single_tick
```

## Safety boundary

The adaptive scheduler is nonsovereign. It does not grant execution, probe, world update, memory write, memory overwrite, or control-packet authority.

```text
bounded_adaptation_enforced = true
delegates_only_to_multi_tick_window_governor = true
scheduler_grants_no_new_authority = true
memory_write_performed = false
memory_append_performed = false
memory_overwrite_performed = false
world_update_performed = false
control_packet_mutation_performed = false
probe_execution_performed = false
```

## Validation

```bash
python scripts/run_qi_adaptive_window_scheduler_checks_v0_1.py
```

Expected:

```text
PASS: Qi adaptive window scheduler checks
```

## Next layer

The next layer can add long-horizon daemon rhythm memory, but should keep cadence adaptation advisory and route all execution through bounded window delegation.
