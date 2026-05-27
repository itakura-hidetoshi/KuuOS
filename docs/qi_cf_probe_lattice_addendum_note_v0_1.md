# Qi Counterfactual Probe Lattice Addendum v0.1

This note documents the Qi counterfactual probe lattice addendum.

The lattice compares the chosen dry-run probe with unchosen counterfactual probe candidates. It does not execute probes and does not mutate state, control packets, memory, or world state.

## Active files

- `runtime/kuuos_runtime_daemon_qi_counterfactual_probe_lattice_v0_1.py`
- `tests/test_qi_counterfactual_probe_lattice_v0_1.py`
- `scripts/write_qi_cf_probe_lattice_v0_1.py`
- `scripts/check_qi_cf_probe_lattice_v0_1.py`
- `manifests/qi_cf_probe_lattice_addendum_v0_1.json`
- `scripts/check_qi_cf_probe_lattice_addendum_v0_1.py`
- `scripts/run_qi_cf_lattice_checks_v0_1.py`

## Boundary

- `counterfactual_only: true`
- `simulation_only: true`
- `dry_run_only: true`
- `authority: none`
- `state_mutation_performed: false`
- `control_packet_mutation_performed: false`
- `memory_write_performed: false`
- `grants_execution_authority: false`
- `grants_probe_execution_authority: false`
- `grants_dry_run_execution_authority: false`
- `grants_next_tick_execution_authority: false`
- `grants_control_packet_authority: false`
- `grants_memory_overwrite_authority: false`
- `grants_world_update_authority: false`

## Check

Run the dedicated lattice suite:

```bash
python scripts/run_qi_cf_lattice_checks_v0_1.py
```

## Position in the current line

```text
trend summary
  -> phase boundary
  -> dry-run license candidate
  -> dry-run probe simulation
  -> counterfactual probe lattice
```

The next natural layer is a probe scheduler proposal surface that chooses when to revisit the lattice without executing probes.
