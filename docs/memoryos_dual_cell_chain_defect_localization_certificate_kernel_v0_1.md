# MemoryOS v0.75 — dual-cell-chain path ordering and defect localization

## Scope

MemoryOS v0.75 extends the finite v0.74 two-cell gluing certificate to a finite chain of four tetrahedral memory cells connected by three dual edges. The layer remains future-only, read-only, and advisory. It does not rank or select candidates, synthesize or activate plans, issue decision receipts, mutate MemoryOS or DecisionOS source records, mutate persistent WORLD state, claim verification, or grant truth authority.

The implementation is a finite `S3` certificate. It does not claim a theorem for arbitrary continuum manifolds, a universal non-Abelian Stokes theorem, or physical gauge-field inference.

## Source binding

The runtime regenerates and validates the accepted MemoryOS v0.74 certificate before deriving v0.75. It binds the v0.74 certificate digest and the collection digests for shared-face gluing, dual-edge transport, lattice Stokes composition, and dual-complex confidence. Any source digest, record count, canonical seam transport, canonical seam defect, or authority-boundary change is rejected fail-closed.

## Mathematical kernel

For a chain of dual links indexed by `i`, let

- `J_i` be the seam transport,
- `D_i` be the local seam defect at the link's local basepoint,
- `P_0 = 1`,
- `P_(i+1) = P_i J_i` be the accumulated path-ordered transport.

The local defect transported to the common initial basepoint is

`D_i^root = P_i D_i P_i^-1`.

The finite chain boundary is defined by the ordered product

`H_boundary = D_0^root D_1^root ... D_(n-1)^root`.

Lean formalizes this as `pathOrderedLocalizedDefectProductAux` and `globalOuterBoundary`, with the definitional equality theorem

`global_outer_boundary_eq_path_ordered_localized_defects`.

### Compatible closure

A link is compatible exactly when `D_i = 1`. Lean proves by induction on the link list that if all seams are compatible, every transported factor is the identity and therefore

`H_boundary = 1`.

Theorems:

- `path_ordered_localized_defects_identity_of_compatible`
- `compatible_chain_global_closure`

### One mismatch

For a three-link chain with compatible first and last links and one middle mismatch, Lean proves

`H_boundary = J_0 D_1 J_0^-1`.

Thus the global boundary carries the middle defect by conjugation with the preceding path transport. A class function therefore recovers the frame-independent conjugacy-class signature of the local mismatch.

Theorems:

- `three_link_middle_mismatch_localizes`
- `three_link_middle_mismatch_wilson_localizes`
- `three_link_middle_mismatch_confidence_localizes`

### Multiple mismatches and ordering

Two direct `S3` defects are used to expose noncommutativity:

- order `A B`: `(01)(12) = (012)`,
- order `B A`: `(12)(01) = (021)`.

The exact group elements differ, so the chain records order dependence. Their permutation traces are both zero because the two 3-cycles are conjugate in `S3`. v0.75 records this limitation explicitly: a class-function signature is frame independent but does not necessarily resolve ordered representatives inside one conjugacy class.

Theorems:

- `canonical_multiple_mismatch_order_dependence`
- `canonical_ordered_mismatch_ab_boundary`
- `canonical_ordered_mismatch_ba_boundary`
- `canonical_ordered_mismatch_class_signature_limitation`

### Dual cycle

A closed dual triangle carries edge transports `J_01`, `J_12`, and `J_20` with path-ordered holonomy

`H_cycle = J_01 J_12 J_20`.

Under independent vertex frames,

- `J_01 -> g_0^-1 J_01 g_1`,
- `J_12 -> g_1^-1 J_12 g_2`,
- `J_20 -> g_2^-1 J_20 g_0`,

and Lean proves

`H_cycle -> g_0^-1 H_cycle g_0`.

Consequently, every class-function Wilson signature is invariant.

Theorems:

- `dual_cycle_holonomy_gauge_covariant`
- `dual_cycle_wilson_gauge_invariant`

## Canonical exact profiles

### All compatible curved

The v0.74 compatible curved link is repeated three times. Every local defect is the identity, so the global boundary is the identity, the permutation trace is `3`, the chain penalty is `0`, and adjusted confidence remains `1/3`.

### Single middle mismatch curved

The chain is compatible–mismatched–compatible. The local middle defect is `(021)`, the preceding transport is `(01)`, and the localized global boundary is

`(01)(021)(01) = (012)`.

The permutation trace is `0`, the advisory chain penalty is `1/6`, and adjusted confidence is `1/6`.

### Ordered double mismatch

The exact boundaries are `(012)` for `A B` and `(021)` for `B A`. They differ as group elements but share permutation trace `0`.

## Advisory confidence convention

The source base confidence remains `1/3`. For the global chain boundary,

`P_chain = (3 - chi_perm(H_boundary)) / 18`,

`C_chain = 1/3 - P_chain`.

This is a bounded finite-certificate convention. It is not a posterior probability, universal statistical optimum, physical action, decision rule, or truth authority.

## Exact runtime ledger

The accepted certificate contains:

- 5 literature records,
- 7 chain-incidence records,
- 4 canonical chain profiles,
- 12 seam-transport records,
- 12 localized-defect records,
- 4 path-ordered composition records,
- 1 single-defect localization record,
- 2 dual-cycle holonomy records,
- 4 chain Wilson records,
- 4 chain confidence records,
- 4 chain memory-fusion records,
- 8 full-rank transport retention records,
- 4 singular atomic retention records,
- 3 rank-one source boundaries.

All group elements are exact permutation triples and all confidence values are exact rationals.

## Fail-closed checks

The checker rejects:

- a modified v0.74 certificate digest,
- modified chain seam transports,
- modified transported local defects,
- a false single-mismatch localization claim,
- a modified ordered global boundary,
- modified chain confidence,
- candidate-selection claims,
- unexpected truth claims,
- collection digest mismatches,
- source count mismatches.

## Literature grounding

The finite mathematical structure remains grounded in the primary references already bound at v0.74:

1. arXiv:2604.16252 — dual incidence structures and Wilson-loop composition.
2. arXiv:1006.2059 — gauge-invariant discrete structure on glued simplicial meshes.
3. arXiv:hep-lat/0309023 — ordered lattice non-Abelian Stokes composition.
4. arXiv:1011.0371 — gauge-covariant Bianchi defects and propagation.
5. arXiv:2605.26697 — path-ordered transport and conjugacy-invariant holonomy comparison.

These references ground the structural choices. They are not cited as sources for the MemoryOS confidence penalty or authority policy.
