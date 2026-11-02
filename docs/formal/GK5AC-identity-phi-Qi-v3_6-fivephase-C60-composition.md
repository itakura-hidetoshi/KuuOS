# F112-P94D3GK5AC and Qi v3.6 — Whole Φ identity/reclassification composition and actual C60 FivePhase bridge

**Date:** 2026-11-02 JST  
**Theorem authority:** [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS), canonical `main`, one public `KuuOSFormal` aggregate, 107 public roots.

## Exact source and merged authority

| Field | F112-P94D3GK5AC | Qi v3.6 / FivePhase-C60 |
|---|---|---|
| Theorem PR | [#2955](https://github.com/itakura-hidetoshi/KuuOS/pull/2955) MERGED | [#2956](https://github.com/itakura-hidetoshi/KuuOS/pull/2956) MERGED |
| Exact-source HEAD | `98b9d44ec9548128ee3cb8998cf00eef365d13cd` | `9f6a3e6be60b0feae68d4c609cf2450c70b24ed2` |
| Squash SHA | `9461a0a837c1276faf97f3f41afa66f966f76cdb` | `a59d8b4fb6bb7c3a3690d36a7871fcc4226e1e61` |
| Exact-source/squash Git tree, identical | `0c050a9e75d2de5573500abaad8b494bcc76db4c` | `e90a0109c46b125e8f38f53c41156e280caf8089` |
| New Lean blob, identical after squash | `9e745609bdfc23f31b01cbbf82e59a7313cb5b53` | `d04ecde0729538aa9c8cbce18d1bd2d27683f99c` |
| Exact-source terminal CI | [#41428104953](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41428104953) SUCCESS | [#41429970480](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41429970480) SUCCESS |
| Strict Lean | 3850/3850 SUCCESS | 10137/10137 SUCCESS including public `KuuOSFormal` |
| Public `#print axioms` | 8/8, standard three only | 10/10, standard three only |

All 18 printed dependencies are restricted to `propext`, `Classical.choice`, `Quot.sound`. On accepted exact-source CI, **`sorryAx = 0`, Lean error/warning = 0/0**; Independent Kuu and workflow integrity/governance completed successfully. GK5AC post-merge push Lean Formal Validation, Runtime Full Check and Full Governance also succeeded. Initial failed CI revisions are NOT mathematical authority.

## GK5AC: true whole NatIso identity, not a strictified equivalence

Source: [PolygonNativeC60AQFullPentagonPhysicalNativeGK5ACIdentityReindexPhiAction.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ACIdentityReindexPhiAction.lean).

For every genuine Mathlib category-equivalence family `e` and **all finite GK5D typed unit/atom/paste trees**, GK5AC combines GK5F's typed `nativeGK5FTreeReindex_id` with GK5AA's actual recursive whole NatIso naturality. The true source and target `eqToIso` are retained and canceled as equality-induced isomorphisms, **not** as a declaration that the original chosen inverse, unit/counit or compositor becomes `rfl`.

Public theorems include `nativeGK5ACSinglePhi_unit_whole`, `nativeGK5ACSourceIso_unit_whole`, five separately recursive `nativeGK5ACFourDirectPhi0..4_unit_whole`, and `nativeGK5ACAllFiveDirectPhi_unit_whole`. Their schematic unit square is

```text
SourceEqToIso_id(t) ≪≫ Phi^I_q(Reindex_id(t))
    ≪≫ TargetEqToIso_id_to_original(t)
  = Phi^I_q(t),   q = 0,1,2,3,4.
```

With [GK5AB](GK5AB-two-stage-index-fivefold-recursive-phi-coherence.md) the formal statements now supply **identity and two-map composition compatibility** of the independently recursive whole Φ reclassification squares. This is a family of verified laws, rather than a fabricated new global 2-functor structure or an assertion of unbounded descent.

### Full-file Lean4 repair and API reasoning

Initial strict Lean [#41427619783](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41427619783) failed because `rfl` did not reduce `eqToIso p ≪≫ eqToIso q` to `Iso.refl` after cases; pinned mathlib `eqToIso_refl`/`Iso.refl_trans` and `Iso.trans_assoc` were needed. Also `rw [hnat]` did not find a syntactically identical subexpression with the explicit index representation `fun x => e (id x)`; replacing that step with an explicit whole-isomorphism `congrArg (... ≪≫ _) hnat.symm`, followed by `Iso.trans_assoc`, repaired the entire single-Φ and five-Φ proofs. The theorem claims and dependent signatures were not weakened. Final source is **495 line-split entries**; unchanged prior Lean files preserved.

## Qi v3.6: actual FivePhase chart and five independently recursive Φ composites

Source: [QiWuxingGK5ACFivePhaseShiftCoherenceV3_6.lean](../../formal/KUOS/Architecture/QiWuxingGK5ACFivePhaseShiftCoherenceV3_6.lean).

There is **one actual existing Qi** carrier `FivefoldIndex = FivePhase = ZMod 5`, not a newly invented cardinality-five object. For the genuine physical C60 gauge `γᵥ = fivefoldSlotEquiv frame v : FivefoldIndex ≃ Slot`, the proved commutation is

```text
γᵥ(p + 1) = slotNext(γᵥ(p)).
```

The proof uses the existing physical C60 gauge and `fivefoldSlot_successor`. Further public theorems `fivefoldPhaseGauge_roundtrip`, `fivefoldPhaseGauge_categories_roundtrip`, `fivefoldPhaseStep_treeReindex_comp` compare the actual chart inverse, dependent category family and **fully typed finite tree** reindexing `phase +1; γᵥ` with `γᵥ ∘ (+1)`.

Finally `fivefoldPhasePhysicalPhi0..4_comp_whole` and `fivefoldPhasePhysicalAllFivePhi_comp_whole` specialize the already certified GK5AB independently recursive **five whole NatIso Φ** comparisons to these specific maps, with **both actual source and target `eqToIso` boundaries retained**. The physical chart is an index map used to select *actual* category families and trees; a physical Edge is never incorrectly identified with a Mathlib categorical NatIso.

The **dependency direction matters**: the standalone independent Kuu GK5AC theorem module never imports KUOS/Qi. Only the architecture-side Qi v3.6 bridge imports GK5AC. To make the newly proven bridge genuinely available to the sole public theorem aggregate, the theorem PR also added exactly **one import line** to `formal/KuuOSFormal.lean` for `KUOS.Architecture.QiWuxingGK5ACFivePhaseShiftCoherenceV3_6`; no new public Lake root, no overwritten original theorem.

### Full-file Lean4 error analysis and exact-source validation

First Qi full-aggregate [CI #41429261377](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41429261377) exposed **two structural elaboration errors**, not mathematical counterexamples:

1. Missing `open KUOS.Architecture.WuxingCyclicPaths` prevented resolution of the genuine `NativeC60FivePhaseGauge` type; its namespace was open in the earlier v3.5 source but must be open in each new file.
2. For Lean4 application elaboration, `fivefoldSlotEquiv frame v` must be enclosed in parentheses when supplied as a single function argument to `nativeGK5AASingleTargetEq` or `nativeGK5FTreeReindex_comp`. Without parentheses Lean tries applying the next args to a fully instantiated equality proof. All **10 target-equality and 10 tree-fusion applications** were repaired across all five bracket proofs and their bundled conjunction.

The initial failed elaboration also printed `sorryAx` on incomplete declarations; **no such failed declaration was accepted as a proof**. The final verified source prints all 10 `#print axioms` with exactly the three standard axioms, no `sorryAx`, and compiles the new bridge and `KuuOSFormal` successfully under the fixed pins. The final exact-source and squash Git trees are identical; the new Lean blobs are identical.

## Authority, remaining boundaries and next research

Lean **v4.30.0-rc2**, mathlib commit **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**, append-only/tighten-only/overwrite-forbidden/same-root, strict 空 centered, independent Kuu as a presentation; protected validation-only PR **#1558 remains Draft/open/unmerged**.

The mathematical scope remains genuine fixed-universe Mathlib category equivalences and finite fully typed GK5D trees; Qi phase and C60 slot index is a proved concrete compatible **presentation**, not an identity of physical and categorical proof histories. No new source-Q axioms, raw F54/F55/P92B high Type-cells, unconditional F45 faithfulness, global Gray reconstruction, arbitrary hyperdescent or clinical causal assertion follows.

**Next GK5AD candidate:** strengthen the shared phase-index construction from one step `+1` to a cyclic `ZMod 5` action, prove `(+1)^5 = id` at the index/tree level with the GK5AC unit and GK5AB composition whole NatIso coherence, then compare physical C60 five-step gauge holonomy with the categorical fivefold transport without conflating their distinct morphism types.
