# MemoryOS v0.99 — Typed Closed-Support / Representable-Kernel Order Anti-Isomorphism

MemoryOS v0.99 packages the fixed-point duality proved in v0.98 as an explicit, type-safe Lean `OrderIso` from closed finite sensor supports to the order dual of sensor-representable invisible kernels.

## Literature-guided frontier

The immediate frontier was selected after checking the current MemoryOS `main` state and recent primary literature.

- arXiv:2607.01773 separates retrieval-based candidate generation from formal-concept closure verification. MemoryOS keeps that boundary: literature informs the theorem frontier but does not grant retrieval-result authority.
- arXiv:2606.30782 demonstrates current Lean 4 / mathlib practice for order-theoretic structures and equivalences. MemoryOS adopts the typed equivalence pattern without claiming a complete lattice instance.
- The polarity, closure, fixed-point, and finite-lattice background remains aligned with arXiv:2408.09080, arXiv:2509.05299, arXiv:1309.5134, and Guigues–Duquenne (1986).

No theorem from those sources is treated as already proved for MemoryOS. Every MemoryOS law below is proved or exhaustively checked in the repository-specific model.

## Fixed-point types

For fixed sensors, atlas, target defect, and route root, the formal layer defines:

```lean
ClosedSensorSupport :=
  { support : Finset ι // SensorSupportClosed sensors support atlas targetDefect root }

RepresentableSensorKernel :=
  { kernel : Subgroup GlobalNormalizedWordSection //
      SensorKernelRepresentable sensors kernel atlas targetDefect root }
```

The maps are:

- closed support to kernel: `C ↦ K(C)`;
- representable kernel to closed support: `Q ↦ Dom(Q)`.

The v0.98 fixed-point theorems yield exact inverse laws:

```text
Dom(K(C)) = C
K(Dom(Q)) = Q
```

## Explicit order anti-isomorphism

The formal layer constructs:

```lean
ClosedSensorSupport sensors atlas targetDefect root ≃o
  OrderDual (RepresentableSensorKernel sensors atlas targetDefect root)
```

Thus, for closed supports `C` and `D`:

```text
C ⊆ D  ↔  K(D) ≤ K(C).
```

This is an anti-isomorphism only between the two fixed-point subtypes. It is not an anti-isomorphism with the ambient subgroup lattice.

## Typed operation compatibility

Binary closed-support operations are defined within the closed-support subtype.

- binary join is closure of the union and maps to ambient kernel infimum;
- binary meet is support intersection and maps to the sensor-kernel envelope of ambient kernel supremum.

The existing finite-family laws remain checked at runtime, while the new Lean layer exposes the binary compatibility through typed support values.

The envelope remains essential:

```text
K(C ∧ D) = Env(K(C) ⊔ K(D)).
```

An ambient subgroup supremum need not itself be sensor-representable.

## Root independence

The underlying values of both typed maps are independent of the selected route root:

- `C ↦ K(C)` follows finite support kernel root independence;
- `Q ↦ Dom(Q)` follows dominated-support root independence.

The proof does not assert definitional equality of root-indexed subtype proofs; it asserts equality of the underlying support or kernel values.

## Exact runtime ledger

The canonical runtime exhaustively validates:

- literature records: 14
- canonical profiles: 8
- closed-support typed-map records: 16
- representable-kernel typed-map records: 16
- order-isomorphism pair records: 36
- binary-operation transport records: 36
- finite-family transport records: 36
- support-map root-independence records: 256
- kernel-map root-independence records: 256
- confidence-preservation records: 4

The inherited confidence vector is preserved exactly and the new penalty is zero. Kernel levels and fixed-point cardinalities remain diagnostic only.

## Exact source binding

The runtime is fail-closed bound to the merged v0.98 artifacts:

- source runtime Git blob SHA-1: `74a3ed60af4f01f3a2f21f47a338ffcde3e414fe`
- source manifest Git blob SHA-1: `d64d5e1e06110d1490c0888d184403014a9579db`
- generated runtime SHA-256: `6a3ca7fadb385620c74bf5b3678f3d6b81bfa8bf534b01697eb6b808fb5023a4`
- generated checker SHA-256: `6444510d8b1d71fc7af7b6e6daaf4eebcda08d628c298ee28d6a9a7f1d710a91`

## Governance boundary

MemoryOS v0.99 does not introduce:

- a Lean `CompleteLattice` instance;
- arbitrary or infinite indexed suprema/infima;
- distributivity or modularity;
- an order isomorphism with all ambient subgroups;
- universal subgroup representability;
- a unique sensor-support representation;
- a canonical minimum support;
- external-oracle or retrieval-result authority;
- candidate ranking, pruning, selection, or plan activation;
- execution, source mutation, persistent-state mutation, or truth authority.
