# Qi Middle-Way Authority Scope Gate Addendum Note v0.1

This note documents the authority scope layer after the two-truths authority emergence gate.

The gate defines authority as a middle-way scope. Authority must not be reified as an eternal permission, and it must not be denied when the dependent conditions actually hold.

It does not execute a probe.
It does not grant actual probe execution authority.
It emits a middle-way authority scope candidate only.

## Position

```text
two-truths authority emergence gate
  -> middle-way authority scope gate
  -> future limited execution-authority grant gate
```

## Scope semantics

The gate returns:

- `MIDDLE_WAY_AUTHORITY_SCOPE_READY`
- `MIDDLE_WAY_AUTHORITY_SCOPE_HOLD`

Ready means the proposed authority scope avoids both extremes:

- eternalist authority: authority is absolute, unbounded, or irrevocable
- nihilist denial: authority is denied even when valid conditions hold

## Required conditions

- `authority_not_reified`
- `authority_not_denied_when_conditions_hold`
- `avoids_eternalism`
- `avoids_nihilism`
- `conditioned_local_authority_only`
- `ultimate_non_reification_preserved`
- `dependent_origination_trace_present`
- `two_truths_boundary_preserved`
- `local_limited_revocable`
- `mass_gap_barrier_preserved`
- `no_direct_execution_collapse`

## Forbidden claims

- `eternalist_authority_claim`
- `nihilist_authority_denial`
- `authority_scope_unbounded`
- `authority_irrevocable`
- `direct_execution_requested`

## Boundary

The gate remains non-executing:

- `middle_way_scope_only: true`
- `authority_scope_candidate_only: true`
- `actual_probe_execution_authority: false`
- `execution_requires_separate_gate: true`
- `authority: none`
- `grants_probe_execution_authority: false`
- `probe_execution_performed: false`
- `memory_write_performed: false`
- `world_update_performed: false`

## CLI

```bash
python scripts/write_qi_middle_way_authority_scope_gate_v0_1.py \
  --authority-emergence .out/qi-supervisor/qi_two_truths_authority_emergence_gate.json \
  --context .out/qi-supervisor/qi_middle_way_authority_scope_context.json \
  --write .out/qi-supervisor/qi_middle_way_authority_scope_gate.json
```

## Checks

```bash
python scripts/check_qi_middle_way_authority_scope_gate_v0_1.py
python scripts/check_qi_middle_way_authority_scope_gate_addendum_v0_1.py
python scripts/run_qi_middle_way_authority_scope_checks_v0_1.py
```

## Next integration target

The next step should be a limited execution-authority grant gate. That future gate must consume the middle-way scope result and may only open a local, one-shot, revocable authority if all downstream execution constraints hold.
