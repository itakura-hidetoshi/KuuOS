# WORLD Bimodule, Sector Fusion, and Principal Graph Bridge v0.40

v0.40 extends the v0.39 canonical-endomorphism and Q-system bridge with a typed finite simple-sector system, duality, fusion multiplicities, statistical dimensions, a fundamental bimodule sector, dual-canonical decomposition data, and principal-graph adjacency.

```text
finite-index inclusion N ⊆ M
  → fundamental N–M bimodule sector X
  → conjugate sector X̄
  → Connes fusion X ⊗ X̄
  → dual canonical sector decomposition
  → finite simple-sector fusion rules Nᶜ_ab
  → statistical dimensions d(a)
  → principal graph adjacency
  → rigid C*-tensor / unitary fusion category receipts
```

Lean directly verifies:

- a finite type of simple sectors;
- a tensor unit and involutive sector duality;
- left and right tensor-unit multiplicities;
- associativity of fusion multiplicities;
- dual symmetry of fusion coefficients;
- left and right Frobenius reciprocity;
- strictly positive statistical dimensions;
- unit and dual dimension laws;
- multiplicativity of dimensions across the fusion decomposition;
- the index formula `d(X)^2 = [M:N]` for the fundamental sector;
- decomposition multiplicities of the dual canonical sector as `X ⊗ X̄`;
- equality of the dual-canonical dimension with the Jones index;
- equality of the v0.39 Q-system specialness scalar with the Jones index;
- typed principal-graph and dual-principal-graph adjacency formulas;
- symmetry of the two-step even-vertex multiplicity matrix;
- bundled fusion-ring, statistical-dimension, and Q-system/standard-invariant connection packages.

The following remain explicit analytic or categorical proof receipts:

- existence of the finite-index Hilbert bimodule;
- analytic Connes fusion;
- semisimple decomposition into irreducible sectors;
- realization as a rigid C*-tensor category;
- unitary fusion-category realization;
- connectedness and completeness of the principal graph;
- paragroup reconstruction.

The runtime validates only a hash-bound, fail-closed receipt. It does not construct Hilbert bimodules, execute Connes fusion, claim fusion-category reconstruction, or update WORLD.

The representation boundary remains:

```text
WORLD state ≠ Hilbert vector
WORLD ≠ operator algebra
WORLD ≠ Jones tower
WORLD ≠ Q-system
WORLD ≠ bimodule
WORLD ≠ sector category
WORLD ≠ principal graph
```

The bimodule-sector system is a read-only analytic sidecar. WORLD nonlinearity, noncommutativity, non-Markovianity, multi-world noncollapse, and the two-truths gap are preserved.
