# F112-P94D3GK5AT / Qi v4.13 — internal P92B phi-image and genuine north C60 reflection

**Verified:** 2026-11-03 JST. Repository: itakura-hidetoshi/KuuOS, canonical branch: main.
Independent theorem GK5AT, physical integration Qi v4.13. Direction of authority: **independent Kuu → Qi**. Strict 空 is not identified with a selected proof presentation, a C60 numerical shadow, or a physical gauge frame.

All original F54/F55/P80/P87/P89 and selected P92B/P93/P94A declarations are preserved. This work adds modules and aggregate imports only. The public KuuOSFormal root **107** is retained, and protected PR #1558 is Draft/OPEN/unmerged. Pinned Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.

## 1. Verification and immutable proof trail

| Item | Exact evidence |
| --- | --- |
| Independent GK5AT theorem | [PR #3007](https://github.com/itakura-hidetoshi/KuuOS/pull/3007), MERGED |
| GK5AT source HEAD | `6fa213cc1be17f07f56c532f2261a550269cf43d` |
| GK5AT squash SHA | `37f2a11e5c8b48ae85ef6c076ea0a0562d75fa40` |
| GK5AT exact-source CI | [Governance #41571114729](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41571114729), SUCCESS; 30/30 Governance jobs SUCCESS |
| GK5AT Strict Lean | **9244 / 9244 built successfully** |
| GK5AT explicit axiom inspections | 11 `#print axioms` output items: none or standard `propext`, `Classical.choice`, `Quot.sound` only |
| Qi v4.13 physical integration | [PR #3008](https://github.com/itakura-hidetoshi/KuuOS/pull/3008), MERGED |
| Qi v4.13 source HEAD | `9977912cbf5b74877e20d20dda8b938a6acb2ea3` |
| Qi v4.13 squash SHA | `4bc7026edb6c38c2c7b4da7202e972d7b6ea2441` |
| Qi v4.13 exact-source CI | [Governance #41571750724](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41571750724), SUCCESS; 30/30 Governance jobs SUCCESS |
| Qi v4.13 Strict Lean | **10171 / 10171 built successfully** |
| Qi v4.13 explicit axiom inspections | 3 `#print axioms` output items: allowed standard axioms only |

The new Lean files have no compiler errors or warnings under warningAsError, and no newly declared axioms, `sorry`, `admit`, `native_decide`, or `sorryAx`. The exact underlying source is the named PR HEAD of each validation, and the final merge commits are distinct from these validation HEADs.

## 2. Independent GK5AT: source fiber is evidence, not parity

The structural map defined in GK5AI is:

- `φ := nativeGK5AIOriginalToP92Structural`
- `φ : OriginalF55(p,r,s) → SelectedP92B(p,r,s)`

All indices remain dependent on original F54 source/target trees, the two Nat indices and the original categorical blocks. For an actual selected Type-valued P92B proof term `q`, GK5AT defines the original-source fiber:

```text
PhiFiber(q) = { original : OriginalF55(p,r,s) // phi(original) = q }
PhiImage(q) = Exists original : OriginalF55(p,r,s), phi(original) = q
PhiImage(q) <-> Nonempty (PhiFiber(q))
```

The equivalence is constructive and preserves a genuine source witness. It is not a comparison of signed shadows, P93/P94A quotient-class equalities, or a numerical C60 endpoint. Direct definitional reductions of the original nine-constructor map prove image closure for F55 identity, symmetry, vertical composition, left context and right context. The new P92B `assocNaturality` is **not** assumed to be in the source image.

Source Lean: [GK5AT internal source-image module](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ATInternalSourceImageObstruction.lean).

## 3. Actual two-step selected P94A comparison: reflection or localized obstruction

Choose genuine original F55 proof terms `f,g` with the same exact original F54 route boundaries, a freely selected P92B proof `q`, and **actual Type-valued selected** four-cell witnesses

```text
left  : P94A(phi(f), q)
right : P94A(q, phi(g)).
```

GK5AT proves the following disjunction:

```text
Nonempty (P89(f,g))
OR
NOT PhiImage(q)
OR
EXISTS (m : OriginalF55),
  phi(m) = q AND
  (BadPair(f,m) OR BadPair(m,g)).
```

The `BadPair` in the last branch is the **existing GK5AQ** proof-relevant original/source pair: selected P94A evidence exists between its structural images, but **no** original P89 4-cell evidence exists. In particular, the actual half `left` or `right` is used to construct the selected component of the local BadPair; no nonreflection is inferred from mere equality of shadows.

Proof mechanism: if `q` has no original preimage, take the first obstruction. If it has a source witness `m`, split on actual P89 reflections of `f→m` and `m→g`. Two actual reflections compose by P89 `trans`. If either original reflection is absent, the corresponding supplied P94A half becomes a genuinely typed local GK5AQ BadPair. The original P89 composition is not silently inferred from a selected comparison.

The theorem `nativeGK5ATBadPair_forces_internalObstruction` additionally shows that an **assumed** global GK5AQ BadPair at `f,g` rules out the reflecting branch for *every supplied two-step factorization*, and therefore forces source nonmembership of the middle or a local source bad pair. **Neither this theorem nor GK5AT asserts existence of an original global bad pair.**

This improves GK5AS's source-vertex chain analysis by evaluating an **actual internal selected midpoint** instead of requiring its original-source status upfront.

## 4. Exact genuine north C60 counterexample to parity-only source recovery

Take the real first, second and third north F45 unit-stage routes. GK5AI's chosen P92B `assocNaturality` proof `q_N` exists, while its exact original F55 witness type has no element and therefore `PhiFiber(q_N)` is empty.

GK5AT constructs the **actual nontrivial proof-term composite**

```text
w_N = P94A.trans (P94A.refl q_N) (P94A.refl q_N)
    : P94A(q_N, q_N).
```

The selected internal intermediate is exactly `q_N`. Its left/right chosen context-unit primitive counts obey

```text
(countLeft(w_N) mod 2, countRight(w_N) mod 2) = (0, 0),
PhiFiber(q_N) = empty.
```

This is stronger than citing an isolated reflexive P94A endpoint: a selected *two-step proof history with a real intermediate P92B proof term* fails original-source membership even while parity vanishes. It remains **not** a GK5AQ BadPair, because original F55 endpoint proof terms do not exist for this exact associator-naturality slot. Do not infer P89→P94A noninjectivity from it.

## 5. Qi v4.13: physical north integration

Qi v4.13 specializes GK5AT's new two-step reflection/obstruction disjunction to the genuine north four-sector pentagon original F54/F55 long/short path objects. It simultaneously establishes compatibility with:

- The true fifth-around physical Dart×Dart closure on the north C60 face.
- The physical 04 and 43 edge-endpoint directions, which remain distinguished from reversed categorical orientations.
- GK5AN's unconditional P89→P94A structural transportation, with source and selected proof authorities distinct.
- Qi v4.10's **conditional** physical P94A four-class noninjectivity iff original GK5AQ reflection obstruction.
- GK5AR/Qi v4.11's exact context-unit parity normal form and GK5AS/Qi v4.12's source-vertex locality.

Qi source Lean: [Qi v4.13 north physical internal source gate](../../formal/KUOS/Architecture/QiWuxingGK5ATNorthInternalSourceGateV4_13.lean).

The true physical Dart frame is not used to create missing original F55 evidence. Strict 空 authority, independent Kuu, selected P92B/P94A proofs and Qi's physical presentation remain distinct.

## 6. Exact boundary and next task

GK5AT proves a **single explicit selected vertical trans node** and source-image closure for five original constructor forms. It does **not** establish a recursive source-saturation criterion through all 19 selected P94A constructors, or a separate recursive inspection of hidden P93C histories inside the `old` constructor. It does not establish unconditional source-descent, noninjectivity, full higher coherence, Gray reconstruction or arbitrary gluing.

Recommended next proof module (tentative **GK5AU**) should construct an honest recursively typed internal-P92B occurrence/saturation predicate, handle all 19 constructors and the P93C `old` boundary explicitly, and prove precisely when fully source-saturated selected subcomparisons can produce a GK5AS source-vertex chain. Identify residual non-source intermediates as obstructions, not as invented original proofs. A genuine P89→P94A BadPair may only be claimed if two actual source F55 endpoints and a nonreflecting selected comparison are constructed.

**Status:** GK5AT and Qi v4.13 theorem proofs and CI are completed and merged. This document is an additive formal proof record; it does not change Lean theorem authority or source code.
