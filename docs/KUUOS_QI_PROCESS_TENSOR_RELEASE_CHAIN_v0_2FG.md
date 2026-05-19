# KuuOS Qi Process Tensor Release Chain v0.2FG

This document fixes the human-readable purpose of `scripts/validate_qi_process_tensor_release_chain_v0_2FG.py`.

## Scope

The v0.2FG validator protects the release chain for:

- Qi Process Tensor v0.2F
- Qi Process Tensor conventional autonomy v0.2G

It checks that these surfaces remain visible across:

- manifest
- chain index
- release packet
- finality packet
- release closure packet
- validated baseline packet
- baseline-established-final packet

## Fixed invariants

- Qi Process Tensor is a multi-time non-Markov temporal structure.
- Qi is history-bearing relational/action flow on the Process Tensor structure.
- Process Tensor collapse to a Markov channel is forbidden.
- Qi must not be identified with the Process Tensor itself.
- Current-state-only prediction is forbidden.
- Operation history, observation backaction, environment memory, and temporal correlation must remain visible.
- Qi stagnation, counterflow, and deficiency visibility is required.
- Qi Process Tensor is a conventional-truth temporal substrate, not ultimate truth.
- Conventional autonomy is safety-gated candidate generation, not ungated execution.

## Authority boundary

The validator does not grant proof, ontology, clinical, execution, commit, belief-root commit, memory overwrite, world-root rewrite, truth, or safety override authority.

The validator is a release-chain guard only.

## CI integration

The validator is run by:

```bash
make physical-quantum-qi-deepening-checks
python3 scripts/run_all_governance_full_checks_v0_1.py
```

The validator is listed in:

- `manifests/physical_quantum_qi_deepening_manifest_v0_2.json`
- `chain_indexes/physical_quantum_qi_deepening_chain_index_v0_2.json`
- `.github/workflows/physical_quantum_qi_deepening_validation.yml`
- `Makefile`
- `scripts/run_all_governance_full_checks_v0_1.py`
