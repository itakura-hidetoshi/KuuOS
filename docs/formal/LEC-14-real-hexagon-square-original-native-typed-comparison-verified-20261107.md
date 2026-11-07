# Living Engi LEC-14 — real historical F47 and independent C60 hexagon F55 typed-square comparison (verified)

**Date:** 2026-11-07 JST  
**Author/Copyright:** Hidetoshi Itakura / 板倉英俊  
**Repository:** `itakura-hidetoshi/KuuOS`, canonical `main`  
**Theorem PR:** [#3267](https://github.com/itakura-hidetoshi/KuuOS/pull/3267) — **MERGED**  
**Exact-source CI:** [#42368168171](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42368168171) — **completed SUCCESS**  
**Verified source HEAD:** `0c7764c2945db146c5e005b1856e0ee0d2705912`  
**Source/test-merge equal Git tree:** `456d67c205af9b18f22c2ce1a132c1ef19bb3303`  
**Main squash commit:** `5579f88776531a983103379c5b2e207afa7e793e` (same Git tree)  
**New module:** [`formal/KuuOSFormal/LivingEngiRealHexagonSquareLEC14.lean`](../../formal/KuuOSFormal/LivingEngiRealHexagonSquareLEC14.lean), 316 committed added lines, 16 `#print axioms` outputs.  
**Public aggregate:** only one additive import in `formal/KuuOSFormal.lean`, no existing Lean changes.

## 1. Mathematical result and genuine source witnesses

This theorem simultaneously uses:

1. **Historical original raw F54/F55 witness:** arbitrary separately supplied, genuinely typed old `OriginalF45BracketTree` local rotations `left/right` with `Blocks` and both `Nat` depth indices. The actual `c60F46PhysicalFlagOriginalF55Cell t₁ t₂ left right edge` carries the exact old `squareLeftFirst` and `squareRightFirst` route endpoints. Its old original categorical F55 arrow equals the `rotationStep` of the genuine old `c60F48EveryRealEdgeMixedFrame` at each real `TruncatedIcosahedralEdge` and either incident face.
2. **Independent native raw F54/F55 witness:** `northHexagonPhysicalF47Frame` retains the genuine six-sector physical F42 fan and disk and its exact `northHexagonNativeF55SquareCell` on the separately typed native `northHexagonNativeSquareLeft/Right` routes. The native four-boundary calibration is the pre-existing independently proved `northHexagonPhysicalF47Frame_calibrated`.
3. **Common full observation:** old physical disjoint-square and independent native square both evaluate under their **own original source interpreters** to `(((0:Int),(1:Int)),(1:ZMod 2))`. This uses the original `originalF55BraidedSquareGenerator_complete` and native `northHexagonNativeF55SquareCell_shadow` rather than inventing an axiom or identifying historical/native source Types.
4. **Explicit real geometry:** `ActualOriginalNativeHexagonSquare` retains historical original raw, exact old categorical arrow equality, independent native physical frame/raw and its calibration, agreed shadow, `physicalEdge : Edge`, and exact `frameKuuEdge` relation. The packet is a constructed **Type-level record**, not a shadow-only proposition.

Given old local rotations, `actual_square_comparison` constructs a packet for *every* one of the genuine old 90 edges and either of its two actual incident faces. Thus `all_real_edges_both_faces_compared` supplies 90×2 conditional inhabited packets without a separately supplied numerical agreement hypothesis. Here the independent receiver is still the **same top-hexagon native frame** for each packet: it would be INCORRECT to say that every historical edge equals a boundary edge of this one native hexagon. The physical-edge field always preserves the selected actual old site, with exact map to Kuu `Edge`.

### Real physical support equality at exactly one selected top-hexagon side

The theorem `topHexagon_same_physical_first_edge` proves:

```lean
edgeEquiv.symm (edgeEquiv (Edge.cross (.northSpoke 0))) =
  cyclicBoundaryEdge (.hexagon (.top 0)) 0
```

The theorem `topHexagon_actual_original_face` proves the selected original real adjacent face is `polygonEquiv (.hexagon (.top 0))`, and `topHexagon_actual_native_incidence` proves actual native edge-on-hexagon-face incidence. Finally `top_hexagon_inhabited_exact_source_and_support` has a concrete `∃ P` witness that retains the original categorical/raw F55 square, independent native raw square, common full shadow and exactly this real physical first side. This is **not** old F42 raw 2-cell equivalence, nor an all-sites geometric identification.

### Separate four-boundary coherence

`actual_square_comparison_original_boundary` reuses the actual **old** mixed Mathlib 3-Hom square `c60F48AllNinetyBothFaces_mixedSquare`. The independent native four-boundary calibration remains a different stored certificate. Their source comparison generators and original F42 faces have NOT been equated.

## 2. Exact-source proof diagnostics, repair and audit

Initial [CI #42367784824](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42367784824) failed in the new source because the required already imported F42 and F47 local names were not made visible: `C60F42PresentedFaceCell`, `C60F47SquareFrame`, and `c60F47FaceArrow/CompareBefore/CompareAfter`. Since the earliest structure failed to elaborate, Lean produced numerous **cascade** errors in later declarations, and `sorryAx` diagnostic traces. This was not a mathematical obstruction or evidence of a missing old/native witness. The repair [`0c7764c`](https://github.com/itakura-hidetoshi/KuuOS/commit/0c7764c2945db146c5e005b1856e0ee0d2705912) only added:
```lean
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
```
No theorem statement, assumption, old source definition, `F/G` or source history was modified.

| Item | Verified exact-source result |
| --- | --- |
| CI | [#42368168171](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42368168171) **completed SUCCESS** |
| Strict Lean | **10,320 / 10,320 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| Related PR check runs | 41; no failed/pending |
| Explicit audits in new module | 16 `#print axioms` outputs |
| `sorryAx` after repair | **none** |
| Changed Lean warnings/errors | **0 / 0** |
| Git tree source/test-merge | **identical** `456d67c205af9b18f22c2ce1a132c1ef19bb3303` |
| Changes | One new mixed formal Lean source + one additive public import |
| Main theorem squash | `5579f88776531a983103379c5b2e207afa7e793e` |

**Axiom distinction is essential.** The 16 declaration reports include the standard `propext`, `Classical.choice`, `Quot.sound` and **six existing F112 physical edge-equivalence `native_decide`-generated auxiliary axioms**. They are inherited by actual geometric/physical-support constructions; the two square-shadow proof reports itself use only standard axioms. No `axiom` was introduced in LEC-14. Thus Lean checking succeeded **but it is not correct to call all 16 audited declarations standard-axioms-only.** The six preexisting dependencies are:

```
pentagonalSlotIndex_bijective._native.native_decide.ax_1_1
pentagonalSlotIndex_next._native.native_decide.ax_1_1
pentagonalSlotIndex_next._native.native_decide.ax_1_2
pentagonalSlotIndex_next._native.native_decide.ax_1_3
pentagonalSlotIndex_next._native.native_decide.ax_1_4
pentagonalSlotIndex_next._native.native_decide.ax_1_5
```

Full kernel-axiom hardening of these already used finite geometric facts is a separate mathematical task. It is not silently discharged by this PR.

## 3. Limits and next exact frontier

- The theorem is **inhabited given genuinely typed original F54 local rotations**, not unconditional over arbitrary uninhabited original boundary indices.
- Shared `((0,1),1)` does not make the old/new F54 or F55 Types equal; old/raw and independent native raw Type-history are stored separately.
- The correct real first top-hexagon side matches physical edge and face. A general original F42 source-2-cell → independent native F42 typed face-cell comparison, exact old→native F54 source/target-indexed functor and higher Beck–Chevalley transport are **not yet proved**.
- No universal all-nine-F55-constructor structural equivalence, P77/GK5CG full higher descent, arbitrary higher-stack effectivity/nonzero Čech H¹, AI-weight change, ActOS authority or clinical effect follows.
- **Next LEC-15 frontier:** strengthen the selected physical edge/face match into an explicitly source-indexed original-F42/native-F42 comparison where genuinely available; then test source/target fidelity over old F54 routes and independent native F54 routes, keeping an explicit obstruction if the comparison does not exist. Do not equate F42 source proof terms from common numeric values.

Pinned Lean v4.30.0-rc2; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; independent `KuuOSStrict` unchanged, publicly exposed root 107 unchanged, protected PR #1558 Draft/Open/unmerged. Same-root, append-only, tighten-only, overwrite-forbidden.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

