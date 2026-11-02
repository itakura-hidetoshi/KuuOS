# F112-P94D3GK5AF / Qi v3.9 — closed whole pentagon and original physical/history obstructions

**Date:** 2026-11-02 JST  
**Repository:** `itakura-hidetoshi/KuuOS` / canonical `main`, public Lean aggregate `KuuOSFormal`, 107 retained public roots.  
**Fixed toolchain:** Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.

## Certified PRs and exact-source provenance

| Item | Independent Kuu GK5AF | Qi v3.9 architecture / original C60 |
|---|---|---|
| Theorem PR | [#2964](https://github.com/itakura-hidetoshi/KuuOS/pull/2964) MERGED | [#2965](https://github.com/itakura-hidetoshi/KuuOS/pull/2965) MERGED |
| Final exact-source HEAD | `5a0608708595df166968b2852dc74273151bc301` | `2e8cbb07cc723a7dc166bae0f2fa4e3f1d82b37e` |
| Squash SHA | `40b87e2951ff1b7f2e5ee3e8208643b01b2b9c76` | `978002076144634c79e6e1f882f80049a18bb997` |
| **Exact-source / squash Git tree, identical** | `c9eec57f8c7b51a75ae250438f4c94d828567322` | `90de4448eebd5a4726950c0f1d86fd5557dd3146` |
| New Lean file blob | `9497c20ccbbeaec27499c49243abd3cea0e75fd6` | `8af5aec40f0e26c104602171048752359b3d0602` |
| Exact-source terminal governance/Strict Lean | [#41445005972](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41445005972) SUCCESS | [#41446051070](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41446051070) SUCCESS |
| Strict Lean compilation | **3853 / 3853** | **10143 / 10143**, `KuuOSFormal` included |
| New public `#print axioms` | **4 / 4**, standard 3 or fewer | **6 / 6**, standard 3 or fewer |
| Lean errors / warnings / `sorryAx` in these new declarations | **0 / 0 / 0** | **0 / 0 / 0** |

The four new independent Kuu and six new Qi published theorem declarations depend on no axioms outside `propext`, `Classical.choice`, `Quot.sound`. The original older Qi v2.5/v3.7 `native_decide` dependency is *not* claimed removed from all historical sources; these new GK5AF/Qi v3.9 theorem carriers do not inherit that extra axiom. The root-restoration, Independent Kuu and focused governance checks passed for the exact-source PRs; the dedicated Independent Kuu PR workflow is intentionally skipped when the same check runs inside Governance.

## GK5AF: both whole NatIso pentagon routes commute with fivefold dependent return

Lean: [GK5AFClosedWholePentagonInterchange.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AFClosedWholePentagonInterchange.lean).

The actual GK5X/GK5Y equivalences and independently recursively constructed whole Mathlib NatIso witnesses are retained. Their five categorical pentagon vertices do **not** identify the true fourfold Mathlib equivalence records, unit/counit or chosen inverse records.

- `nativeGK5AFLongPath` is the true, source/target typed `01;12;23` composite whole NatIso.
- `nativeGK5AFShortPath` is the actual `04;43` composite whole NatIso, not the physical positive walk on the C60 face.
- `nativeGK5AFPaths_whole` proves the equality of these two **whole** NatIso routes.
- `nativeGK5AFDirectLong_whole` and `nativeGK5AFDirectShort_whole` prove the two equations `Phi0(t) >> long = Phi3(t)` and `Phi0(t) >> short = Phi3(t)` for every finite original GK5D `unit/atom/paste` typed tree.
- `nativeGK5AFClosedBothRoutes_whole` proves the pair of equations after the **actual five-stage GK5AD/GK5AE reindexing**, with both genuine source and target `eqToIso(congrArg ...)` endpoints and the original full dependent typed-tree return. It does not take the equality of `f^5` and `id` as judgmental equality.

These are proven categorical higher coherence squares, not comparison fillers between the different data types `Edge`, `NatIso`, and historical `Type`-valued F54/F55/P92B source witnesses.

## Qi v3.9: physical orientation obstruction over the real C60

Lean: [QiWuxingGK5AFPhysicalCategoricalObstructionV3_9.lean](../../formal/KUOS/Architecture/QiWuxingGK5AFPhysicalCategoricalObstructionV3_9.lean).

Everything uses the existing `FivefoldIndex = FivePhase = ZMod 5`, original physical `Vertex` / `Slot` / `Dart` / `Edge`, and existing `fivefoldSlotEquiv frame v : FivefoldIndex ≃ Slot`. No new 5-vertex graph or fabricated physical face is introduced.

- `fivefoldOriginalDart_phase_injective` establishes injectivity of the **original** physical phase-to-`Dart` map, using true `incidentDart` and the actual C60 chart.
- `fivefoldGK5AFReversedPhysicalEndpoints` identifies the genuinely **swapped** physical dart endpoints for the reverse-oriented categorical edges.
- `fivefoldGK5AFNoForwardPhysicalComparison` proves that the reversed edge cannot simultaneously be the forward-oriented C60 endpoint pair; otherwise injectivity implies `p=p+1` in `ZMod 5`, a contradiction.
- `fivefoldGK5AFBothReverseObstructions` applies that no-go theorem to the **actual** categorical 04 and 43 edges.

This obstruction rules out a *specific false forward-orientation comparison*. It does **not** rule out a correctly reversed, orientation-aware comparison with suitable additional structure.

## Qi v3.9: original Type-valued source history cannot be recovered from shift alone

The original independent Qi v3.1 free typed `Quiver.Path` histories

`generationControlPath p` and `controlGenerationPath p`

have equal phase displacement and the same event count, yet are **provably distinct** as original proof-relevant paths, because their intermediate typed vertex differs. Neither history has been quotiented away.

- `fivefoldGK5AFPhysicalHistoryReadout` reads the original physical C60 starting/ending `Dart` and the true `WuxingShift = FivePhase × Nat`.
- `fivefoldGK5AFHistoryFactor_noFaithfulReturn` proves **for every type `T` and every readout `WuxingShift → T`** that the induced observation on the original two-primitive-interaction path space is noninjective.
- `fivefoldGK5AFPhysicalWholePhiHistory_obstruction` specializes this theorem to the actual Qi/C60 physical Dart pair, phase/count readout and **both true GK5AF whole NatIso pentagon routes**. That observation remains nonfaithful on the original two distinct free typed histories.

This is a mathematically explicit obstruction to **faithful reconstruction from these observations alone**. A higher filler, descent, or full source-history comparison would need **additional genuinely history-sensitive typed evidence**. No universal no-go statement against every possible higher comparison or faithful enriched observation is asserted; no raw F54/F55/P92B higher witness is reduced to its phase label.

## Governance and continued research

Qi imports independently proved Kuu GK5AF, never the reverse. `KuuOSFormal` receives exactly one new Qi v3.9 import; public root 107 is retained. The independent Kuu theorem and the Qi architecture extension were merged as separate PRs, followed by this separate docs-only record. No earlier theorem source is overwritten, no Gray reconstruction or unrestricted hyperdescent is declared. PR #1558 remains protected as Draft/open/unmerged.

**Next research focus:** formulate an explicit history-sensitive typed comparison interface between real C60 paths, canonical whole NatIso pentagon composites and original higher Type-valued F54/F55/P92B evidence. Separate (i) orientation-aware edge comparison, (ii) faithful history lifting, and (iii) any genuine higher filler and descent obstruction, proving each only from actually constructed evidence. All GK5AE/Qi v3.8 and earlier records remain authoritative.
