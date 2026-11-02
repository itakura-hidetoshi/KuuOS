# F112-P94D3GK5AE / Qi v3.8 — exact fivefold endpoint descent and original whole Φ return

**Date:** 2026-11-02 JST  
**Canonical:** `itakura-hidetoshi/KuuOS` main, only `KuuOSFormal` public theorem aggregate, 107 retained public Lake roots.

## Authoritative exact-source certification

| Item | Independent GK5AE | Qi v3.8 physical + categorical bridge |
|---|---|---|
| Merged theorem PR | [#2961](https://github.com/itakura-hidetoshi/KuuOS/pull/2961) | [#2962](https://github.com/itakura-hidetoshi/KuuOS/pull/2962) |
| Exact-source HEAD | `ca746c6fcc62432daf569073e592e1e198aede1a` | `d0d8794b12108ebf417b377c954977976a3c70b7` |
| Merged squash SHA | `942634d99c0801232585aa85148854c44118f13c` | `8c09269d95428f703471d0e0ed06943798399690` |
| **Identical exact-source and squash Git tree** | `d6170372d2596a6ae2e1c8e8e690e445ed4a50cc` | `86f38e836db5fdf7da092bc468c680dca5206edc` |
| **Identical Lean source blob** | `5abfa16e15bff69690b40110252c78763eaabe04` | `c6bb72dcd6275ac2d2be47a5d1e2e26c97ebca1a` |
| Exact-source terminal CI | [#41440045396](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41440045396) SUCCESS | [#41441533987](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41441533987) SUCCESS |
| Strict Lean | **3852/3852** | **10141/10141**, including `KuuOSFormal` |
| Public `#print axioms` | **8/8**, at most standard three | **11/11**, at most standard three |
| `sorryAx`, Lean errors/warnings | **0**, **0/0** | **0**, **0/0** |

**Fixed pins:** Lean v4.30.0-rc2, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Both exact-source governance, Independent Kuu and workflow checks completed SUCCESS. Final public theorem dependencies are restricted to `propext`, `Classical.choice`, `Quot.sound`; no extra native-decide trusted axiom occurs in **these new theorem carriers**.

## GK5AE: full family and BOTH dependent endpoint casts

Source: [PolygonNativeC60AQFullPentagonPhysicalNativeGK5AEClosedEndpointWholePhiTransport.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AEClosedEndpointWholePhiTransport.lean).

For `f : I → I` with actual proof `hf : nativeGK5ADFiveIndex f = id` and an original finite GK5D tree `t : NativeGK5DTypedTree C i j`, GK5AE explicitly constructs:

1. `nativeGK5AEOriginalAsFivePullback f C hf t`: cast of the **full dependent family** `C` into `C ∘ f⁵`, using GK5AD's true `nativeGK5ADFiveFamily_closed`.
2. Five genuine recursively typed GK5F reindexing steps `nativeGK5ADFiveTreeReindex` with intermediate categories retained.
3. `nativeGK5AEEndpointTreeTypeEq` and `nativeGK5AEClosedFiveTree`: separate **source and target** endpoint-type equalities, no unlicensed definitional equality at `f⁵ i = i`.
4. `nativeGK5AEClosedFiveTree_eq`: the **entire original typed tree** returns, rather than merely its leaves or observed category labels.

For each original nonstrict independently recursive Mathlib direct `Φ`, the five public `nativeGK5AEFourDirectPhi0..4_return_whole` theorems and `nativeGK5AEAllFiveDirectPhi_return_whole` prove the **whole** source/target equality-induced NatIso square:

```text
Phi^I_Pq(returned tree)
    >> EqToIso(actual target whole-functor equality)
 =
EqToIso(actual source whole-functor equality)
    >> Phi^I_Pq(original tree),  q = 0,1,2,3,4.
```

The separate previous GK5AD theorem remains authoritative for the five-step-vs-one-shot reindexing whole NatIso comparison; GK5AE proves the **remaining original-presentation endpoint descent**, without identifying arbitrary raw Type-valued source proof histories.

### Full-source Lean 4 diagnostic (GK5AE)

The initial [failing exact-source run #41439603061](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41439603061) exposed two genuine elaboration issues, not a mathematical refutation. A theorem that referred to `hf` *only in its proof* did not bind that section variable in its public statement; `hf` became an unknown identifier and other applications shifted its argument into an index position. Also direct `cases hf` failed dependent elimination because the left side `nativeGK5ADFiveIndex f` is a *composite function expression*, not a free variable. The corrected whole file first proves `nativeGK5AEGenericRoundtrip` for a genuine variable map `g` and `hg : g=id`; equality elimination is then valid. It instantiates this at `g=f⁵` and composes with the **actual GK5AD five-step tree equality**. Existing theorem declarations and their assumptions were not weakened or overwritten. The fixed exact-source build and all 8 printed public axioms were independently checked.

## Qi v3.8: one real FivePhase/C60 gauge, five Φ returns, two distinct pentagons

Source: [QiWuxingGK5AEOriginalPhiReturnV3_8.lean](../../formal/KUOS/Architecture/QiWuxingGK5AEOriginalPhiReturnV3_8.lean).

On the **existing** `FivefoldIndex = FivePhase = ZMod 5` (not a new five-point graph), the original C60 gauge `fivefoldPhaseCategory frame v C` and the original four genuine Mathlib `fivefoldPhaseEquivalence frame v e₁..e₄` specialize GK5AE using real Qi phase +1 and the explicit `f⁵=id` proof. All five `fivefoldPhysicalPhi0..4_original_return_whole` and the combined `fivefoldPhysicalAllFivePhi_original_return_whole` have the **whole original Φ** at the endpoint with both `eqToIso` boundaries.

The independent theorem `fivefoldPhysicalCategoricalParallelEvidence` certifies the **original physical** C60 fifth around-edge closure (true `Edge` and `Dart`) **and** the separate **categorical whole NatIso pentagon** `01;12;23 = 04;43`, while `fivefoldPhaseTwoReversedEdges` keeps the 04 and 43 orientations reversed relative to physical positive order. The evidence lives in **different types**; no false equation `Edge = NatIso` or invented higher filler is asserted.

The architecture side imports independent Kuu GK5AE. Kuu does not import KUOS, and the sole public `KuuOSFormal` aggregate gained exactly one import without changing its 107 roots.

### Native-decide dependency located and eliminated from the NEW certified carriers

The first v3.8 [exact-source run #41440796065](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41440796065) **compiled Lean 10141/10141, with no sorry or warnings/errors**, but all original-return Φ theorem audits contained an extra axiom `fivePhase_natCast_five._native.native_decide.ax_1_1`. This originates in the older **Qi v2.5** global simp theorem `fivePhase_natCast_five : (5 : FivePhase) = 0 := by native_decide` in `QiYinYangWuxingFibonacciHistoryGeometryV2_5.lean`, inherited by the older v3.7 `fivefoldPhaseFiveIndex_id`; the historical declaration remains unchanged.

Rather than claiming that this extra axiom was absent, the new v3.8 source **appends** `fivefoldPhaseNatCastFive_kernel` with kernel-evaluated `decide`; `fivefoldPhaseFiveIndex_id_kernel` and `fivefoldPhaseLastPhysicalSide_closed_kernel` use explicit `ring`, `rw`, and `simp only [add_zero]` and avoid that historical simp dependency. All five original-return Φ and the distinct pentagon evidence are instantiated with these **new kernel-verified** certificates. The second [exact-source CI #41441533987](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41441533987) prints **11/11 standard-three-or-less axiom dependencies with no native_decide axiom**, `sorryAx=0`, Lean errors/warnings 0/0, Strict Lean 10141/10141 SUCCESS, Independent Kuu/Governance SUCCESS.

**Important provenance:** this establishes the axiom boundary of the **new GK5AE/Qi v3.8 carrier only**. It does not retroactively alter or certify all past Qi v2.5/v3.7 results as native-decide-free.

## Scope and next mathematical obligation

Keep canonical main, strict 空 authority, independent Kuu presentation, append-only/tighten-only/overwrite-forbidden/same-root107, no Gray resurrection, protected validation-only PR #1558 **Draft/open/unmerged**.

Current theorems prove fully typed finite GK5D tree closure, whole NatIso source/target returns, physical edge endpoint closure and categorical pentagon separately. They do **not** prove equality of original raw F54/F55/P92B high Type-valued histories or an unconditional higher gluing law. A candidate next study **GK5AF** should test the additional comparison/obstruction between the fivefold categorical pentagon route and physical-origin sequence using explicit typed transport, without allowing two distinct morphism types to collapse or assuming a new filler.
