# Qi Executable Action Sequence Runner v4.3

Bounded sequence runner for the Qi executable action dispatcher.

This layer increases execution coverage by running more than one allowlisted v4.2 action in a declared order.

## Input

- `qi_executable_action_sequence_packet.json`

## Outputs

- `qi_executable_action_sequence_runner_receipt.json`
- `qi_executable_action_sequence_runner_audit.jsonl`

## Behavior

The sequence runner writes one temporary `qi_executable_action_packet.json` per action and delegates execution to v4.2.

It stops when:

- the sequence is complete
- a delegated action is blocked
- the sequence exceeds the configured cap
- an action is not allowlisted
- the sequence packet or license is not ready

## Boundary

This does not create arbitrary execution. It only runs bounded v4.2 dispatcher actions in a finite declared sequence.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, shell access, network access, or unbounded execution authority.

## Validation

```bash
python scripts/check_qi_executable_action_sequence_runner_v4_3.py
```
