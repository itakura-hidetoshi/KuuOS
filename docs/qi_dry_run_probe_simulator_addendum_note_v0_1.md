# Qi Dry-run Probe Simulator Addendum v0.1

This note documents the Qi dry-run probe simulator addendum.

The addendum connects the dry-run probe simulator to the Qi process tensor review surface without granting execution authority.

## Active files

- `runtime/kuuos_runtime_daemon_qi_dry_run_probe_simulator_v0_1.py`
- `scripts/write_qi_dry_run_probe_sim_v0_1.py`
- `tests/test_qi_dry_run_probe_simulator_v0_1.py`
- `scripts/check_qi_dry_run_probe_sim_v0_1.py`
- `manifests/qi_dry_run_probe_simulator_addendum_v0_1.json`
- `scripts/check_qi_dry_run_probe_simulator_addendum_v0_1.py`

## Boundary

The addendum is a simulation surface only.

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

Run the addendum check directly:

```bash
python scripts/check_qi_dry_run_probe_simulator_addendum_v0_1.py
```

Or run it through the Qi process tensor review suite:

```bash
python scripts/run_qi_process_tensor_review_checks_v0_1.py \
  --write-json .out/qi-supervisor/process_tensor_review_check_suite.json
```

## Position in the current line

```text
trend summary
  -> phase boundary
  -> dry-run license candidate
  -> dry-run probe simulation
  -> addendum manifest/check
```

The next natural layer is a counterfactual probe lattice, which compares chosen and unchosen probe simulations without executing probes.
