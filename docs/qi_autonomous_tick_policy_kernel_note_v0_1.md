# Qi Autonomous Tick Policy Kernel v0.1

This addendum binds DecisionOS, CBF, token ledger, and process tensor packets into a daemon tick policy surface.

## Position

```text
DecisionOS / CBF / token ledger / process tensor
  -> autonomous tick policy kernel
  -> autonomous tick policy receipt / daemon loop binding
```

## Actions

The kernel selects exactly one action:

```text
advance_tick
hold
observe
notify
ticket
handover
freeze
```

## Advance conditions

`advance_tick` is allowed only when:

```text
same_root = true
cbf_ok = true
token_ledger_ok = true
process_tensor_ok = true
DecisionOS allows advance
read_only_policy_surface = true
no blocking reason is present
```

The result includes `next_tick_number` only for a valid `advance_tick` decision.

## Fallback semantics

```text
hold      = insufficient token budget or recovery witness gap
observe   = unresolved non-Markov process tensor state
ticket    = uncertainty above ticket threshold or DecisionOS ticket request
handover  = uncertainty above handover threshold or DecisionOS handover request
freeze    = CBF closed barrier or DecisionOS freeze request
```

## Boundary

The policy kernel is a read-only policy surface. It selects the daemon's next admissible action, but it does not mutate memory, update the world, grant control, or execute probes.

## Validation

```bash
python scripts/run_qi_autonomous_tick_policy_kernel_checks_v0_1.py
```

Expected result:

```text
PASS: Qi autonomous tick policy kernel checks
```

## Next layer

The next addendum should bind this policy packet into the daemon loop as an explicit receipt, while keeping execution authority separate from policy selection.
