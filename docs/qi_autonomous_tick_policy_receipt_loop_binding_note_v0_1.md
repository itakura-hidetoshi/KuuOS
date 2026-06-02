# Qi Autonomous Tick Policy Receipt / Daemon Loop Binding v0.1

This addendum binds the autonomous tick policy kernel to the daemon loop through an explicit receipt.

## Position

```text
DecisionOS / CBF / token ledger / process tensor
  -> autonomous tick policy kernel
  -> process-tensor-optimized receipt
  -> daemon loop binding
  -> safe resume controller
```

## Process tensor optimization

The receipt seals process tensor state before the daemon loop can advance:

```text
memory_complexity_score
memory_complexity_threshold
QCMI value
recovery_epsilon
recovery_witness_present
non_markov_unresolved
process_tensor_pressure
```

The receipt maps these into one rollout mode:

```text
markov
compressed
partial_history
full_history
```

`advance_tick` is allowed only when the policy is ready, same-root, read-only, and the process tensor surface does not require observation or full-history fallback.

## Loop binding semantics

The loop binding is deliberately narrow:

```text
advance_tick + valid receipt  -> call safe_resume_controller for exactly one tick
hold                         -> no safe resume
observe                      -> no safe resume
notify                       -> no safe resume
ticket                       -> no safe resume
handover                     -> no safe resume
freeze                       -> no safe resume
blocked receipt              -> no safe resume
```

The loop binding grants no probe, world update, memory overwrite, or control-packet authority.

## Safety invariants

```text
receipt_id_deterministic = true
policy_packet_id_bound = true
process_tensor_metrics_sealed = true
advance_delegates_only_to_safe_resume_controller = true
non_advance_never_advances_tick = true
freeze_never_delegates = true
loop_binding_grants_no_new_authority = true
memory_write_performed = false
memory_append_performed = false
memory_overwrite_performed = false
world_update_performed = false
control_packet_mutation_performed = false
probe_execution_performed = false
```

## Validation

```bash
python scripts/run_qi_autonomous_tick_policy_receipt_loop_binding_checks_v0_1.py
```

Expected result:

```text
PASS: Qi autonomous tick policy receipt loop binding checks
```

## Next layer

The next layer can add a long-horizon autonomous daemon loop window, but should still keep process tensor receipt sealing and safe-resume delegation as the only advance path.
