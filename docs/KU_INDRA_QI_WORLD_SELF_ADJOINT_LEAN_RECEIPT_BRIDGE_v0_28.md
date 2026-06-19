# Kū–Indra WORLD Self-Adjoint Lean Receipt Bridge v0.28

v0.28 closes the gap between the v0.27 abstract dense-operator interface and the concrete Lean/mathlib theorem source. It does not re-prove self-adjointness in the runtime repository and it does not identify WORLD with a Hilbert vector.

```text
exact nonlinear WORLD state
  → v0.26 read-only real ℓ² analytic sidecar
  → v0.27 dense-domain / symmetric-core formal interface
  → v0.28 immutable Lean theorem receipt
```

The receipt must bind the exact v0.27 state digest, the exact v0.26 state digest, the dense-operator identity, the local bridge-schema digest, an immutable 40-hex commit in `itakura-hidetoshi/4d-mass-gap`, Lean/mathlib identity, CI run identity, theorem declarations, and source-audit attestations.

## Required proof stages

- dense `LinearPMap`;
- graph-adjoint fixed point;
- actual adjoint equals the operator;
- mathlib `IsSelfAdjoint`;
- global whole-domain Rayleigh lower bound.

The canonical declarations currently targeted are:

```text
concreteL2R2DenseDiagonalDomainLinearPMap
concrete_l2_r2_dense_diagonal_domain_linear_pmap_graph_adjoint_eq_graph
concrete_l2_r2_dense_diagonal_domain_linear_pmap_actual_adjoint_eq_self
concrete_l2_r2_dense_diagonal_domain_linear_pmap_isSelfAdjoint
concrete_l2_r2_actual_energy_ge_norm_sq
concrete_l2_r2_self_adjoint_diagonal_global_rayleigh_lower_edge_one
```

A well-formed but incomplete receipt yields `awaiting_external_lean_proof`. Digest loss, mutable branch references, source mismatch, authority escalation, or operator execution fail closed.

`world_self_adjoint_lean_receipt_bridge_ready` means only that an immutable external Lean proof receipt is exactly bound to the v0.27/v0.26 analytic identity. The runtime receipt is not the proof term and grants no theorem, truth, WORLD-update, external-actuation, or unbounded-operator execution authority.
