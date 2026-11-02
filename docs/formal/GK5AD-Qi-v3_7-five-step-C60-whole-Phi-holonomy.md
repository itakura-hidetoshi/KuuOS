# F112-P94D3GK5AD and Qi v3.7 — genuine five-step index/C60 coherence with whole NatIso Φ

**Date:** 2026-11-02 JST  
**Canonical theorem authority:** `itakura-hidetoshi/KuuOS` / `main` / sole public `KuuOSFormal` aggregate / 107 retained public roots.

## Exact-source and merged proof receipts

| Authority | GK5AD independent Kuu | Qi v3.7 downstream bridge |
|---|---|---|
| Theorem PR | [#2958](https://github.com/itakura-hidetoshi/KuuOS/pull/2958), MERGED | [#2959](https://github.com/itakura-hidetoshi/KuuOS/pull/2959), MERGED |
| Exact-source HEAD | `f1e7a6c3d9ba905963e9ddcc07ab6ac207dd6fe5` | `939b4a4e4a42c056f2e65fe595cd17404f0c3e91` |
| Squash/main commit | `e6a4826082dcacb43088c63247bc346c892c9182` | `b08f7bd34edce9111e4c4db0619e8b796a13061d` |
| Exact-source and squash Git tree | `74d92a2fafb055fb0e449844040854ddb4005cec` (identical) | `b91f7df649386f96fb9a2f3d076df2ac650a2964` (identical) |
| Lean file blob (identical) | `d4f798e364d8cba1a2d359e429e5f1f0aed73a7a` | `4ef1153c2d6f42eeaa86cffca59ed3829fa0a62a` |
| Exact-source terminal CI | [#41434118220](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41434118220), SUCCESS | [#41435151217](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41435151217), SUCCESS |
| Strict Lean | **3851/3851** | **10139/10139**, including actual public `KuuOSFormal` |
| Public `#print axioms` | **10/10** | **13/13** |

Both final sources were independently compiled under Lean **v4.30.0-rc2**, mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**. All 23 printed results depend on at most `propext`, `Classical.choice`, `Quot.sound`, and the Qi physical `fivefoldSlotNext_five` depends on **no axioms**. Final accepted sources have **`sorryAx = 0`, changed-file Lean errors/warnings = 0/0**, Independent Kuu, Workflow integrity and Governance terminal SUCCESS. Earlier failed elaborations do not certify mathematics.

## GK5AD: five genuinely typed reindexings and whole Φ comparison

Source: [PolygonNativeC60AQFullPentagonPhysicalNativeGK5ADFiveStepIndexPhiHolonomy.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ADFiveStepIndexPhiHolonomy.lean).

For an arbitrary actual endomap `f : I → I`, let

```lean
nativeGK5ADFiveIndex f := fun i => f (f (f (f (f i))))
```

The first theorem constructs the **five separate** `nativeGK5FTreeReindex f` operations, retaining the true category family and typed intermediate source/target at every step, including the GK5D `unit`, `atom` and `paste` constructors. It then proves `nativeGK5ADFiveTreeReindex_eq`: the resulting full dependent typed tree is equal to reindexing by the actual composite index map `f⁵`.

The second theorem `nativeGK5ADFiveTreeFusion_whole` verifies that the *whole equality-induced Mathlib NatIso* for this true tree equality cancels with its inverse. For every one of the five **independently recursively assembled nonstrict Mathlib direct Φ** from GK5X, GK5AA and GK5AC, the public theorems

```lean
nativeGK5ADFiveDirectPhi0_reindex_whole
nativeGK5ADFiveDirectPhi1_reindex_whole
nativeGK5ADFiveDirectPhi2_reindex_whole
nativeGK5ADFiveDirectPhi3_reindex_whole
nativeGK5ADFiveDirectPhi4_reindex_whole
nativeGK5ADAllFiveDirectPhi_reindex_whole
```

compare two genuinely different presentations:

```text
Phi^pullback_q(t) >> EqToIso(target-reindex-equality)
 =
 (SourceIso_(f^5)(t)
    >> EqToIso(fivefold-source-tree-equality.inverse)
    >> Phi^I_q(five independent reindex steps))
    >> EqToIso(fivefold-target-tree-equality)
q = 0,1,2,3,4.
```

In particular, **both whole source and target EqToIso boundaries remain visible**, and neither `Equivalence.trans` record, chosen quasi-inverse, unit/counit, middle compositor nor a raw higher source witness is strictified.

The separate actual order-five hypothesis `f⁵=id` gives `nativeGK5ADFiveIndex_closed` and `nativeGK5ADFiveFamily_closed`: the index and indexed category family return exactly to the original. These statements are kept separate from the whole NatIso path-coherence square, so **an equality proved in Prop is never misrepresented as definitional equality of dependent source/target types**. Thus the certified result is *relative typed-index holonomy and path independence*, not an unconditional equality of original F54/F55/P92B higher history or a new hyperdescent filler.

### GK5AD Lean4 diagnostic

The first exact-source CI [#41433175273](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41433175273) failed: after `simp only [nativeGK5FTreeReindex_comp]`, the elaborator still saw the fully expanded map `fun z => f(f(f(f(f z))))` rather than the named `nativeGK5ADFiveIndex f`; an explicit final `rfl` discharges the definitional comparison. More fundamentally, a hypothetical `f⁵=id` does not make the true dependent categories `C(f⁵ i)` and `C i` definitionally identical before equality transportation; attempted untransported whole NatIso applications were ill-typed. The revised **whole file** (556 lines plus trailing line split) retains the intended genuine nonstrict comparison, *with* the complete source and target `eqToIso` types, through an explicit tree-equality whole witness naturality lemma, `Iso.trans_assoc`, and the existing GK5AA recursive Φ theorem. No mathematical assumptions or preexisting theorem files were weakened or overwritten.

## Qi v3.7: actual FivePhase order-five action and physical C60 closure

Source: [QiWuxingGK5ADFivePhaseHolonomyV3_7.lean](../../formal/KUOS/Architecture/QiWuxingGK5ADFivePhaseHolonomyV3_7.lean).

The proof does **not** introduce an invented 5-point model. It reuses the existing actual Qi `FivefoldIndex = FivePhase = ZMod 5` and v3.6 `fivefoldPhaseReindexOne(p) = p+1`, obtaining:

```text
fivefoldPhaseFiveIndex_id:
  nativeGK5ADFiveIndex fivefoldPhaseReindexOne = id
```

On the genuine twelve-chart C60 physics, the already certified gauge equivalence `γᵥ = fivefoldSlotEquiv frame v : FivefoldIndex ≃ Slot` conjugates every `+1` step to a true `slotNext` step. The new `fivefoldPhaseFive_physical` proves this equality through five actual consecutive steps; `fivefoldPhasePhysicalFive_closed` and `fivefoldSlotNext_five` prove the physical cyclic return. Importantly, `fivefoldPhaseLastPhysicalSide_closed` identifies the **actual original fifth physical around-edge**, with endpoint `nativeC60GaugeDart frame v (p+4)` and the original starting dart `nativeC60GaugeDart frame v p`, not a hypothetical graph cycle.

The same actual physical chart defines `fivefoldPhaseCategory` and `fivefoldPhaseEquivalence`, pulling back the *real* category families and Mathlib equivalences to the *one shared existing* phase type. `fivefoldPhaseFamilyFive_closed` proves category-family return, and `fivefoldPhaseTreeFive_reindex_eq` proves the genuine five-step fully dependent tree equality.

Finally `fivefoldPhysicalDirectPhi0..4_five_whole` and `fivefoldPhysicalAllFivePhi_five_whole` instantiate the five independently recursive GK5AD whole NatIso path-coherence certificates under this specific gauge family. The original physical C60 Edge and categorical NatIso retain **different types and evidence histories**, even though their index transport follows the same proved phase chart. This is a typed, computable bridge, not an equality asserted by both objects having five elements.

The Qi v3.7 PR makes precisely **one additional import** in canonical `formal/KuuOSFormal.lean` for this new architecture-side source. The independent Kuu GK5AD module imports **no** KUOS/Qi and the 107 public Lake roots are unchanged.

## Continuing mathematical frontier

Canonical `main`, pinned Lean/mathlib, append-only/tighten-only/overwrite-forbidden/same-root 107, strict 空 centered and independent Kuu a presentation. Protected validation-only PR **#1558 remains Draft/open/unmerged**.

**Next GK5AE candidate:** formalize the whole NatIso **closed-cycle comparison all the way to the original source presentation after explicit dependent-family endpoint transports**, then analyze whether an independent, genuinely higher typed obstruction persists. This requires an explicitly constructed path-composition certificate, not a shortcut from `(+1)^5 = id` to identity of raw source history. Compare the verified cyclic-index action with five genuine GK5 pentagon edges, retaining the two reversed categorical orientations and the distinct physical C60 evidence types. No global Gray reconstruction, unrestricted hyperdescent or clinical causality is implied.
