# F112-P94D3GK4BV — Exact two-target composition coherence of the chosen inverse

2026-11-01 JST. **[Theorem PR #2887](https://github.com/itakura-hidetoshi/KuuOS/pull/2887) MERGED.** Append-only proof receipt; only the pinned Lean theorem source on canonical `main` carries theorem authority.

## Exact source and provenance

- [Complete GK4BV Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BVChosenInverseCompositionCoherence.lean): **one appended 319-line Lean file, five public declarations** (two NatIso definitions, three theorems), five private lemmas. Five public `#print axioms` receipts.
- Final source HEAD `6fd24887dee2ef1ec9b4760f2caa6a2160437a40`; test-merge commit `eab1c47bf15ee3d4f661fc44b93f10dece7264fb`. The two Git commits have **identical tree `c06899e9f85283ed280bb120b123bc379c76f4e4`**. Test-merge parents are the exact base `731f5d5f4ecb326d4f5c31d0cec9cad06368119a` and the source HEAD.
- [Exact-source CI #41296105367](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41296105367): **Strict Lean 3817/3817 SUCCESS**, Independent Kuu SUCCESS, workflow integrity SUCCESS, Governance terminal SUCCESS. Changed Lean warning/error **0/0**, `sorryAx` **0**. All five declarations depend on at most `propext`, `Classical.choice`, `Quot.sound`.
- Theorem squash / canonical main HEAD after integration: `b9818a9c74ca159c4a2ffce134a163e03df58246`.

## Original source and formal boundary

Retain the fully typed original F45 dependent structural category `S = NativeGK4IStage`, the genuinely **attained** old-AH observation category `A_att = NativeGK4BFAttainedAHStage`, and GK4BM's actual `ObjectProperty.FullSubcategory` of AH-kernel-compatible source functors `Comp_T`.

The genuine forward precomposition `C_T`, the explicit GK4BP inverse `P_T`, and the GK4BM `asEquivalence` **choice-based** inverse `Q_T` remain distinct. GK4BQ gives the true whole NatIso `κ_T : Q_T ≅ P_T`, and GK4BT builds `Θ_R : C_R ⋙ Q_U ≅ Q_T ⋙ A_R` by whiskering κ and transporting GK4BP's strict inverse square. GK4BU already proves the whole target-NatTrans modification square for Θ.

## GK4BV's stronger new theorem

For arbitrary target functors `R : T ⥤ U`, `L : U ⥤ V`, define the two-step comparison `Θ²_(R,L)` using:

1. The **exact GK4BN compatible target-composition equality**, lifted by `eqToIso`.
2. The genuine `Functor.associator` and `Functor.isoWhiskerLeft` carrying `Θ_L`.
3. The inverse associator and `Functor.isoWhiskerRight` carrying `Θ_R`.
4. The final associator and the actual attained-target-composition `eqToIso`.

This is a bona fide whole Mathlib `NatIso` of the **arbitrary choice inverse**, not an untyped 3-cell or a strict equation of `Q_T` with `P_T`.

GK4BV proves, **as equality of whole NatIso values**:

```text
nativeGK4BVChosenInverse_twoTargetCompositeIso R L
  = nativeGK4BTChosenInverse_targetNatIso (R ⋙ L)
```

It first proves the corresponding strict explicit-`P` comparison by converting associators and left/right whiskered `eqToIso` into equality transports and applying `eqToIso_trans`. It then proves a reusable abstract `nativeGK4BVGaugeComposition` lemma: naturality of the final κ, cancellation of `κ_U.inv` against `κ_U.hom` after right-whiskering, and naturality of the initial inverse κ, with the genuine associators and target-composition transports kept typed. This transports strict-`P` coherence to the separately chosen `Q` without assuming its strict target naturality.

## Five public declarations

- `nativeGK4BVAttainedTarget_comp`: whole attained target postcomposition preserves two-step composition strictly.
- `nativeGK4BVChosenInverse_twoTargetCompositeIso`: true two-step Mathlib natural isomorphism for the chosen inverse.
- `nativeGK4BVExplicitInverse_twoTargetCompositeIso`: corresponding two-step natural isomorphism for the explicitly factored inverse.
- `nativeGK4BVExplicitInverse_twoTarget_eq_direct`: equality of explicit-`P` two-step and direct transport isomorphisms.
- `nativeGK4BVChosenInverse_composition_coherence`: exact `Θ²_(R,L) = Θ_(R⋙L)` as whole Mathlib NatIso, via gauge transport.

## CI repair and Lean 4 elaboration lessons

The nontrivial elaboration obstruction was **not** a missing category axiom. A naïve `rw [κ.naturality]` does not match composite expressions where `Functor.associator` leaves actual identity components and `Category.assoc` changes the grouping. Likewise `eqToIso` of an independently proved functor equality is not silently `Iso.refl`. The final checked source first expands `Iso.trans_hom`, whiskered homs, `NatTrans.comp_app`, and associator components; then normalizes category composition and applies κ naturality plus the true `Iso.inv_hom_id_app` via `Functor.map_comp`. The last target-change naturality is applied as a typed `congrArg` equality, not an unchecked tactic rewrite. The original source, previous proofs, pinned API, and authority boundaries were not weakened.

## Remaining boundaries

No unconditional original-S faithfulness, source-Q category laws, raw F54/F55/P92B Type-valued higher fillers, all ambient integer matrix reachability, reconstructed global Gray category or unrestricted hyperdescent is claimed. No definitional equality of `Q_T` and `P_T`. Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Public `KuuOSFormal`, root 107 unchanged, strict 空 center, independent Kuu one presentation, validation-only PR #1558 Draft/OPEN/unmerged.

Append-only / tighten-only / overwrite-forbidden / same-root107. Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
