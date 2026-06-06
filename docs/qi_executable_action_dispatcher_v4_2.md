# Qi Executable Action Dispatcher v4.2

Bounded executable action dispatcher for the Qi process tensor circulation stack.

This layer increases what can be executed by turning existing safe runners into explicit allowlisted actions.

## Input

- `qi_executable_action_packet.json`

## Output

- `qi_executable_action_dispatcher_receipt.json`
- `qi_executable_action_dispatcher_audit.jsonl`

## Allowlisted actions

- `cycle_trend_summary`
- `trend_adaptive_supervisor_packet`
- `trend_adaptive_supervisor_run`
- `cycle_supervisor`
- `cycle_runner`
- `return_loop`

## Boundary

The dispatcher does not create arbitrary execution. It only dispatches to existing bounded actions when the action packet and dispatcher license both allow the action.

It does not grant clinical authority, intervention authority, theorem authority, institutional authority, unbounded execution authority, shell access, network access, or file-system authority beyond the existing bounded runtime packets.

## Validation

```bash
python scripts/check_qi_executable_action_dispatcher_v4_2.py
```
