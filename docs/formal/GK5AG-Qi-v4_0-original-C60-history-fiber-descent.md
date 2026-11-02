# F112-P94D3GK5AG / Qi v4.0 — original native source-history fiber, physical C60 and whole NatIso

**Date:** 2026-11-02 JST  
**Canonical repository:** `itakura-hidetoshi/KuuOS`, main.  
**Theorem authority:** independent Kuu first; Qi architecture consumes Kuu, never the reverse. Sole public Lean aggregate: `KuuOSFormal` (107 retained public roots).  
**Fixed pins:** Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; protected PR #1558 Draft/open/unmerged.

## Verified exact-source provenance

| Field | GK5AG: independent native F54/F55/P92B | Qi v4.0: genuine north-C60 geometry |
|---|---|---|
| Theorem PR | [#2967](https://github.com/itakura-hidetoshi/KuuOS/pull/2967), MERGED | [#2968](https://github.com/itakura-hidetoshi/KuuOS/pull/2968), MERGED |
| Final exact-source HEAD | `a167e611503569a1f826a2ec1d85f72d26cd6449` | `16afc3a41e7277f34439670609dde10cc6d300ea` |
| Squash SHA | `e1085409b576bca37511c4bf3a6bb4762e4a0f3e` | `96911f7062a8fe604347e6248bd96ab52721660f` |
| **Exact-source/squash Git tree (identical)** | `cc58b2295a419f379bf68b43464c535380e9876c` | `8782988a4044e83f1912f0d41736b88588bc7788` |
| Newly added Lean blob | `9026f63b43770284bd63a718638ad4fcbf9aaaac` | `da532424d1331294d9f1f137e97da55eea4b271e` |
| Terminal exact-source CI | [#41448648845](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41448648845) SUCCESS | [#41449583910](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41449583910) SUCCESS |
| Strict Lean | **3854/3854** | **10145/10145**, including actual `KuuOSFormal` |
| New theorem `#print axioms` | **9/9** within the three standard axioms | **4/4** within the three standard axioms |
| `sorryAx`, Lean errors/warnings | **0**, **0/0** | **0**, **0/0** |
| Independent Kuu, Workflow integrity, Governance | SUCCESS | SUCCESS |

All **13 NEW printed declarations** depend on no axioms beyond `propext`, `Classical.choice` and `Quot.sound`. The pre-existing historical Qi v2.5/v3.7 `native_decide`-derived axioms are **not claimed removed** from all old sources. The new v4.0 carriers do not inherit an additional native-decide axiom. The dedicated Independent Kuu PR workflow is intentionally SKIPPED where the equivalent independent boundary check executes in the Governance gate.

## Original F54-shaped native source: original history is a TYPE, not a phase label

Lean: [GK5AG Original History Comparison Fiber](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AGOriginalHistoryComparisonFiber.lean).

The genuinely typed four original north-C60 sector stages carry **two independent Nat depths, both actual F45 Blocks/AxisTrace histories, source/target trees and proof-relevant F54-shaped paths**. This is the **independently reconstructed native old-F54-shaped grammar** of E7O, **NOT** a proved equivalence to the frozen historic KUOS F54/F55 implementation.

Two actual original-dependent routes `northNativeF45PentagonLong` and `northNativeF45PentagonShort` share exact endpoints but are **unequal raw Type-valued terms**:

```text
rotationCount(pentagonLong) = 3
rotationCount(pentagonShort) = 2
pentagonLong != pentagonShort
```

An actual original nine-constructor F55 `northNativeF55PentagonCell` has these two routes as its **different** boundaries; the source routes themselves are not rewritten into definitional equality. The *selected* P92B `NativeF55P92AssocComparison.original` constructor imports this real existing 3-cell, so `nativeGK5AGNorthP92Classes_equal` proves the **P92B comparison-existence quotient classes** coincide.

`nativeGK5AGNorthNoP92HistoryRetraction` proves there is **no left inverse** from the actual selected P92B quotient to ALL original raw F54-shaped north routes. This is independent of an invented higher mapping.

## Exact original-source descent gate

For any `T : Type` and any actual source-history readout `h : NativeGK5AGNorthHistory → T`, the theorem `nativeGK5AGNorthFactor_throughP92_iff` proves:

```text
Exists q : OriginalP92BClasses -> T,
  forall sourceRoute r, q ([r]_P92B) = h(r)

  iff

forall raw F54-shaped routes r s at the same dependent endpoints,
  Nonempty (NativeF55P92AssocComparison r s) -> h(r) = h(s).
```

No additional source comparison witness is introduced. The theorem `nativeGK5AGNorthRotationCount_noP92Descent` shows a **concrete obstruction** to this universal condition: the two raw pentagon routes have different rotation counts although their selected P92B quotient classes are equal. Thus there is no `P92BClasses → Nat` correctly recovering the original raw rotation count for every route.

## Genuine whole NatIso pentagon: parallel TYPE evidence, not an assumed filler

The original GK5AF `nativeGK5AFLongPath` (01;12;23) and `nativeGK5AFShortPath` (04;43) are TRUE whole Mathlib NatIsos. `nativeGK5AFPaths_whole` proves their equality, and GK5AF separately proves fivefold dependent reindex/whole-`Phi` return.

The GK5AG structure `NativeGK5AGParallelEvidence` preserves **three distinct components**: original F55 Type-valued cell, selected P92B Type-valued cell, and genuine categorical Mathlib NatIso equality. `nativeGK5AGParallelEvidence` constructs this packet. The packet does **not** include or assert a functor mapping F54 raw routes into Mathlib NatIso.

If an interpretation `interpret : NativeGK5AGNorthHistory → WholeNatIso` is separately supplied, and it maps these two original source routes to the respective GK5AF long/short whole paths, then `nativeGK5AGMatchingWholeMap_not_injective` proves it **cannot be injective**. Even the *joint* P92B class + whole-NatIso observation is noninjective (`nativeGK5AGJointP92Whole_not_injective`). A **history-tagged** observation remains injective (`nativeGK5AGHistoryTagged_injective`) because it retains the entire original raw route as data.

This is an exact conditional **faithfulness obstruction**, not an assertion that a canonical interpretation exists or that every history-sensitive higher filler is impossible.

## Qi v4.0: actual north C60 physical pentagon and selected P92B no-descent

Lean: [Qi v4.0 Original North History Descent](../../formal/KUOS/Architecture/QiWuxingGK5AGOriginalNorthHistoryDescentV4_0.lean).

Use the original `FivefoldIndex = FivePhase = ZMod 5`, `fivefoldSlotEquiv frame .north`, and original C60 `Vertex/Slot/Edge/Dart`. `fivefoldGK5AGNorthPhysicalFifthDarts` is literally `edgeEndpoints (fivefoldSide frame .north (p+4))`, with actual physical fifth around-edge closure.

`fivefoldGK5AGNorthRealParallelEvidence` constructs simultaneous, properly **separated** evidence for that physical boundary, raw F54 route inequality, actual P92B class comparison, real GK5AG categorical whole-NatIso/F55/P92B packet, and the two **reversed** physical directions 04/43. No physical Edge/NatIso equality is introduced.

The **unconditional** physical source-history obstruction is:

`fivefoldGK5AGNorthRotationCount_noPhysicalP92Descent`:

```text
NOT exists c : ((Dart × Dart) × OriginalP92BClasses) -> Nat
  such that, for EVERY original north F54-shaped raw route r,
  c(actualOriginalFifthDarts(frame,p), [r]_P92B) = rotationCount(r).
```

This genuinely reuses the real C60 fifth around-edge and P92B's actual existence quotient. Physical closure/phase indexing does NOT recover the missing raw history.

With an *explicitly provided* interpretation matching the GK5AF two actual whole NatIso routes, the readout of real physical C60 fifth-edge darts, P92B source class, and whole NatIso is still noninjective (`fivefoldGK5AGNorthPhysicalP92Whole_not_injective`). Consequently, no full-history recovery section can exist for **that readout** (`fivefoldGK5AGNorthNoWholeHistoryRecovery`). These results distinguish actual nonfaithfulness from any unsupported universal no-filler claim.

## Lean 4 error and exact repair

The first GK5AG exact-source [CI #41448159206](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41448159206) failed at the no-history-retraction proof's `calc` chain with:

```text
invalid 'calc' step, failed to synthesize Trans instance
Trans Eq Eq ?m.48
```

In a context with fully dependent implicit F54 route terms, the intermediate equality relation's type could not be fixed at the final `calc` step. The proof was **not** weakened: the final corrected source declares the two full `recover ([r]) = (r : NativeGK5AGNorthHistory)` return equalities and the equality of recovered P92 images **with explicit types**, then composes them by `Eq.trans`. After reviewing the **entire 312-line new file**, imports, actual original F54/F55/P92B definitions and pinned Lean `Eq.trans`, exact-source [#41448648845](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41448648845) compiled successfully with 9/9 standard-axiom audit. Existing source files were not overwritten.

## Authority and next research

Keep original/native F54/F55/P92B Type-valued evidence, independently chosen P92B existence quotient, and genuinely recursive GK5AF Mathlib whole NatIso as **different proofs**. Physical 04/43 arrows retain their reversed orientation. The general KuuOS theory and strict 空 authority are not reduced to the C60 testbed. Independent Kuu never imports Qi. No Gray reconstruction, canonical historical F54 equivalence, unlicensed descent, or global higher filler was asserted.

**Next GK5AH (candidate):** design a source-history-aware *typed comparison interface* with explicit mappings from native F54 routes AND compatibility on original F55/P92B higher witnesses; prove necessary/sufficient local compatibility conditions and exact obstruction to any faithful descent. Require actual source/target transports, 04/43 orientation awareness, independent re-observation and no unproved higher filler. Prior proof history and the protected PR #1558 remain unchanged.
