# Qi Executable Capability Sequence Runner v5.0

Bounded sequence runner for the Qi executable capability router.

This layer increases execution coverage by running more than one v4.9 capability route in a declared finite order.

## Input

- `qi_executable_capability_sequence_packet.json`

## Outputs

- `qi_executable_capability_packet.json`
- `qi_executable_capability_sequence_runner_receipt.json`
- `qi_executable_capability_sequence_runner_audit.jsonl`

## Behavior

The sequence runner writes one temporary `qi_executable_capability_packet.json` per capability and delegates each item to v4.9.

It stops when:

- the sequence is complete
- a delegated capability is blocked
- the sequence exceeds the configured cap
- a capability kind is not allowlisted
- the sequence packet or license is not ready

## Boundary

This does not create arbitrary execution. It only runs bounded v4.9 capability routes in a finite declared sequence.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_capability_sequence_runner_v5_0.py
```
