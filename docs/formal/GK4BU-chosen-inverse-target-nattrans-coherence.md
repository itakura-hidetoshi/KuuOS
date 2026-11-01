# F112-P94D3GK4BU — Chosen-inverse target-NatTrans modification and typed transport

2026-11-01 JST. **[Theorem PR #2885](https://github.com/itakura-hidetoshi/KuuOS/pull/2885) MERGED.** This is a docs-only historical receipt; the appended Lean theorem file on canonical `main` is authoritative.

## Exact Lean source, Git tree, and CI

- [Complete GK4BU Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BUChosenInverseTargetNatTransCoherence.lean): one **new 324-line file**, nine new public declarations and one private transport helper, each public declaration audited by `#print axioms`.
- Final theorem source HEAD `d49f8df5021562590e70db2640221aa20e7bc10d`. Test-merge HEAD `3fe8cd56d664c5571f8b991adb6d6b6b5e5ca7c9`. Their **identical Git tree** is `d5f8b4cf33e8a5f072b936c2c4391b998ed72afd`; the test-merge parents are base canonical `774b07d77c5dcb62de26bb09310ccea9713214ad` and the exact source HEAD.
- [Exact-head CI #41284678233](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41284678233): **Strict Lean 3816/3816 SUCCESS**, Independent Kuu SUCCESS, Governance terminal SUCCESS, final status `passed`.
- All nine `#print axioms` results contain only `propext`, `Classical.choice`, `Quot.sound`; **sorryAx 0**, changed-Lean warnings/errors **0/0**.
- Theorem squash and canonical main HEAD after merge: `118d5f2f4121cdc4465f8407ef5b6684ddeace94`.

## Preserved source and target authority

The original genuine dependent F45 structural category `S = NativeGK4IStage`, the **actually attained** original-AH category `A_att = NativeGK4BFAttainedAHStage`, and the exact `Comp_T` AH-kernel-compatible `ObjectProperty.FullSubcategory` from GK4BM are unchanged.

For each actual target category T, let `C_T` be genuine precomposition by the original GK4BJ observer; let `P_T` be the separately explicit GK4BP factor inverse; and let `Q_T` denote the **arbitrarily chosen** GK4BM `asEquivalence` inverse. The whole Mathlib comparison `κ_T : Q_T ≅ P_T` is from GK4BQ, and `P_T` alone has GK4BP's strict target-postcomposition square. GK4BT combines these using `isoWhiskerLeft`, `eqToIso`, and `isoWhiskerRight` into the whole NatIso

```text
Θ_R : (R_*^Comp ⋙ Q_U) ≅ (Q_T ⋙ R_*^A),    R : T ⥤ U.
```

Its source and target are actual functors between the specified Mathlib functor categories, not F54/F55 raw higher cells. The quasi-inverse `Q_T` is **not** asserted to commute strictly with `R` or target natural transformations.

## Main new modification-type theorem

For every genuine target NatTrans `ρ : R ⟶ R'`, GK4BU proves the **typed equality of entire Mathlib natural transformations**

```text
(ρ_*^Comp ▷ Q_U) ≫ Θ_R'.hom
  = Θ_R.hom ≫ (Q_T ◁ ρ_*^A).
```

The source is `R_*^Comp ⋙ Q_U` and the target is `Q_T ⋙ (R'_*)^A`. This is a comparison-square naturality theorem for `Θ`, **not** the false definitional equality of the two arbitrary-choice inverse composites.

The argument pastes three independently typed squares:

1. Genuine Mathlib horizontal interchange with `κ_U.hom`, yielding the left square.
2. GK4BP's whole target-NatTrans square, transported through **both** nontrivial `eqToIso` morphisms associated to `R` and `R'`.
3. Genuine Mathlib interchange with `κ_T.inv`, yielding the right square.

For step 2, the separate private general transport lemma `nativeGK4BUEqToHom_square` formally derives

```text
f ≫ eqToHom h' = eqToHom h ≫ g
```

from `h : A = B`, `h' : A' = B'`, and `HEq f g`. It is proved by equality induction and `eq_of_heq`. Thus `eqToIso` is **not incorrectly replaced by an identity** without a definitional equality; that earlier elaboration obstruction is resolved at the type level.

## Genuine action laws and compositional boundaries

GK4BU additionally gives a whole `Θ` square for:

- `ρ = 𝟙 R`: target identity, with the previously proven GK4BO/GK4BT identity preservation.
- `ρ ≫ σ`: target vertical composition, with GK4BT whole target-map preservation.
- Horizontal target transformations `ρ : R⟶R'` and `σ : Q⟶Q'`, identifying their two pasting presentations by actual GK4BT attained-AH interchange.
- A two-step target change `T --R--> U --Q--> V`, first varying `R` by `whiskerRight ρ Q`, then separately varying `Q` by `whiskerLeft R σ`.

These are **genuine typed full-natural-transformation statements**. This file does not separately prove a full arbitrary-choice `Θ_(R⋙Q)` factorization equality with a composite of `Θ_R` and `Θ_Q` after all associativity transports; such a stronger pseudofunctor coherence should be distinguished from the verified two-stage target-NatTrans squares.

## Audited public declarations

1. `nativeGK4BUChosenInverse_leftInterchange`
2. `nativeGK4BUChosenInverse_rightInterchange`
3. `nativeGK4BUExplicitInverse_middleTransport`
4. `nativeGK4BUChosenInverse_targetNat_square`
5. `nativeGK4BUChosenInverse_targetNat_id`
6. `nativeGK4BUChosenInverse_targetNat_vertical`
7. `nativeGK4BUChosenInverse_targetNat_horizontal`
8. `nativeGK4BUChosenInverse_firstTarget_whisker`
9. `nativeGK4BUChosenInverse_secondTarget_whisker`

The new helper `nativeGK4BUEqToHom_square` is private and transitively included in the audited public axiom dependencies.

## Proof and scope limitations

No unconditional source-S faithfulness, original raw-Q category laws, raw F54/F55/P92B Type-valued higher cells, total ambient integer-matrix reachability, global Gray reconstruction, or global hyperdescent are inferred. The true theorem carrier remains canonical `main`; the public library is `KuuOSFormal` with retained **107 roots**. Strict 空 center and independent Kuu presentation remain separate. Lean is pinned to `v4.30.0-rc2`, mathlib to `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; protected validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) stays **Draft, OPEN, unmerged**.

Append-only / tighten-only / overwrite-forbidden / same-root107. Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
