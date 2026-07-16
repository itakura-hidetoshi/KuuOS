# MemoryOS v0.98 — Sensor–Kernel Polarity

MemoryOS v0.98 exposes the antitone Galois polarity already implicit in the v0.89 sensor-support closure and transports the v0.97 finite closed-context lattice to the representable invisible-kernel side.

## Exact polarity

For a finite sensor support `S`, let `K(S)` be its exact invisible kernel. For any subgroup `Q` of global normalized word sections, define

`Dom(Q) = { i | Q ≤ K_i }`,

where `K_i` is the individual invisible kernel of sensor `i`.

The formal layer proves

`Q ≤ K(S) ↔ S ⊆ Dom(Q)`.

Thus `S ↦ K(S)` and `Q ↦ Dom(Q)` form an antitone Galois connection.

## Dual closure operators

The support-side composite is exactly the existing closure:

`cl(S) = Dom(K(S))`.

The kernel-side composite is

`Env(Q) = K(Dom(Q))`.

The Lean layer proves that `Env` is extensive, monotone, and idempotent. Its fixed points are precisely kernels represented by finite sensor supports. `Dom(Q)` is always a closed support, and every closed support is recovered from its exact kernel.

## Fixed-point order duality

For closed supports `C` and `D`,

`C ⊆ D ↔ K(D) ≤ K(C)`.

Therefore the finite lattice of closed supports is anti-isomorphic, at the order level, to the fixed-point lattice of representable kernels. No unique support representative is selected.

## Finite-family transport

For a finite family of closed supports `F`:

- the support join transports to the ambient subgroup infimum:
  `K(∨ F) = inf { K(C) | C ∈ F }`;
- the support meet transports to the kernel envelope of the ambient subgroup supremum:
  `K(∧ F) = Env(sup { K(C) | C ∈ F })`.

The envelope is required because an ambient subgroup supremum need not itself be sensor-representable. Both transported results are fixed points of `Env`.

## Exact runtime ledger

- literature records: 13
- canonical profiles: 8
- support–kernel polarity records: 81
- kernel-envelope records: 24
- closed-support fixed-point records: 16
- closed-support order-duality records: 36
- finite-family kernel-transport records: 36
- polarity root-independence records: 1296
- kernel-envelope root-independence records: 384
- confidence-preservation records: 4

The canonical S3 runtime exhaustively checks all finite supports, the three kernel levels used by the established profiles, every closed-support pair, every finite closed-support family, and all 16 source/target route-root pairs.

## Literature alignment

The immediate structural reference is the polarity/Galois-connection account in arXiv:2408.09080. The finite-lattice reconstruction context includes arXiv:2507.14068 and the closure-generation line in arXiv:2509.05299. The retrieval-grounded FCA motivation remains arXiv:2607.01773.

Only the finite polarity, closure fixed points, reverse order, and finite-family transport pattern is imported. No category-level equivalence, complete-lattice typeclass, infinite-family theorem, distributivity theorem, modularity theorem, universal sensor representation, or basis-minimization result is claimed.

## Governance boundary

The inherited confidence vector is preserved exactly and the new penalty is zero. Kernel levels and fixed-point counts are diagnostic only. This step grants no retrieval authority, candidate ranking, pruning, selection, activation, execution, persistent-state mutation, or truth authority.
