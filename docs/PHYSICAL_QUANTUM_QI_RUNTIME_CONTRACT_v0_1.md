# Physical Quantum Qi Runtime Contract v0.1

This document defines the first public KuuOS runtime contract for Physical Quantum Qi.

Qi / 気 is not treated as a mystical substance, a creator principle, or a direct expression of emptiness. In KuuOS, Qi is an evidence-bound relation-flow packet that arises only on the conventional appearance side after dependent-origination difference has been organized through string/brane structure, gauge transport, curvature/holonomy accounting, current coupling, open quantum thermodynamics, and recovery accounting.

## Canonical emergence chain

```text
K
  -> delta_rel
  -> Sigma_ws
  -> StringMode
  -> BraneBoundary
  -> A_mu
  -> F_munu
  -> J_Qi_mu
  -> Z_Qi
```

Where:

- `K` is the non-reified emptiness ground.
- `delta_rel` is dependent-origination difference in `K_perp`.
- `StringMode` is relational vibration, not a self-subsisting string object.
- `BraneBoundary` is membrane/boundary support, not a creator substance.
- `A_mu` is the IndraNet gauge transport connection.
- `F_munu` and Wilson/holonomy residue record transport curvature, distortion, and residue.
- `J_Qi_mu` is the Qi current.
- `Z_Qi` is the full SK/FV history-sensitive path-integral surface.

## Qi type ladder

```text
NonQi
  < PreQi
  < ProtoQi
  < TransportableQi
  < CurvedQi
  < CurrentQi
  < PhysicalQi
  < FullPathQi
```

The runtime always separates `claimed_type` from `validated_type`. A packet may claim `FullPathQi`, but if SK/FV history evidence is missing, it is downgraded to `PhysicalQi` or lower.

## PhysicalQi evidence

A packet may validate as `PhysicalQi` only when all of the following are present:

1. `K_non_reification`
2. `delta_rel_in_K_perp`
3. `string_mode_consistency`
4. `brane_boundary_support`
5. `gauge_connection_A_mu`
6. `curvature_F_munu`
7. `Wilson_loop_residue`
8. `current_J_Qi_mu`
9. `Ward_or_leak_identity`
10. `density_state_rho`
11. `Hamiltonian_H`
12. `Lindblad_generator_L`
13. `entropy_production_Sigma`
14. `free_energy_F_beta`
15. `DPI_gap`
16. `recovery_margin`
17. `mass_gap_floor_33_20`

A packet validates as `FullPathQi` only if the PhysicalQi bundle is present and SK/FV history evidence is also present.

## Mass gap role

The MGAP4D internal-normalized `33/20` gap is a stability floor for the `K_perp` world-phase domain on which Qi flow is evaluated.

It is not:

- a source of Qi,
- a replacement for dependent-origination difference,
- a replacement for string/brane organization,
- a replacement for gauge transport,
- a replacement for Ward/leak accounting,
- a replacement for recovery accounting,
- a replacement for SK/FV history.

## Authority boundary

Validated Qi packets do not grant:

- execution authority,
- belief commit authority,
- memory overwrite authority,
- world-root rewrite authority,
- safety override authority.

Qi may inform MemoryOS, WorldModel, PlanOS, DecisionOS, BeliefOS, ReflectionOS, Safety/CBF, and ExplanationOS only as an evidence-bound flow signal: leak, residue, backaction, recoverability, irreversibility, entropy cost, DPI loss, holonomy distortion, or downgrade reason.

## Validation entrypoint

```bash
make qi-runtime-checks
```

or directly:

```bash
python3 scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py
```

Passing validation means that the public Qi packet examples obey the structural runtime contract. It does not grant proof, ontology, clinical, execution, or final decision authority.
