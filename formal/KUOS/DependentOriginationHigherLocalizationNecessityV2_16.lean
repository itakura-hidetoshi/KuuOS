import KUOS.DependentOriginationHigherStrictificationPrincipleV2_15

namespace KUOS.DependentOriginationHigherLocalizationNecessityV2_16

open CategoryTheory
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakToStrictReductionV2_14
open KUOS.DependentOriginationHigherStrictificationPrincipleV2_15

universe u v uH vH

/-!
# Weak higher localization necessity v2.16

The previous layers separated two logically different statements:

```text
weak W-admissibility
        ?⇒ higher localization factorization
```

and the proved strict-model sufficient route.  This file establishes the reverse
implication *without* any strictification hypothesis:

```text
higher localization factorization
        ⇒ weak W-admissibility.
```

The proof has two ingredients.

1. A Cat-valued pseudofunctor on a locally discrete source sends an isomorphism
   in the underlying 1-category to an equivalence of categories.  Since the
   pinned Mathlib revision does not expose a dedicated pseudofunctor
   `mapAdjunction` helper, we prove this directly from `mapId`, `mapComp`, and
   `Functor.IsEquivalence.mk'`.
2. The localization unit sends every arrow in `W` to an isomorphism.  Therefore
   every restricted localized higher system is weakly `W`-admissible.  A
   pointwise-equivalence strong comparison then transports this property to the
   raw system by the two-out-of-three property for equivalences of categories.

Thus weak `W`-admissibility is not merely a plausible input condition: it is a
necessary condition for the exact v2.10 factorization interface.
-/

/-- A Cat-valued pseudofunctor from a locally discrete bicategory sends an
ordinary isomorphism to an equivalence of categories.

This is proved directly at the pinned Mathlib API level. -/
theorem pseudofunctor_map_of_isIso_isEquivalence
    {Base : Type u} [Category.{v} Base]
    (F : Pseudofunctor (LocallyDiscrete Base) Cat.{vH, uH})
    {X Y : Base} (f : X ⟶ Y) [IsIso f] :
    (F.map f.toLoc).toFunctor.IsEquivalence := by
  apply Functor.IsEquivalence.mk'
    (F.map (inv f).toLoc).toFunctor
  · apply Cat.Hom.toNatIso
    refine (F.mapId (.mk X)).symm ≪≫ ?_
    simpa only [← Quiver.Hom.comp_toLoc, IsIso.hom_inv_id,
      Quiver.Hom.id_toLoc] using
      F.mapComp f.toLoc (inv f).toLoc
  · apply Cat.Hom.toNatIso
    refine ?_ ≪≫ F.mapId (.mk Y)
    simpa only [← Quiver.Hom.comp_toLoc, IsIso.inv_hom_id,
      Quiver.Hom.id_toLoc] using
      (F.mapComp (inv f).toLoc f.toLoc).symm

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Restricting any localized higher system along the presentation-localization
unit automatically produces a weakly `W`-admissible raw system. -/
theorem restrictHigherLocalizedSystem_isHigherWAdmissible
    (F : HigherLocalizedDescentSystem (W := W)) :
    IsHigherWAdmissible W (restrictHigherLocalizedSystem W F) := by
  intro X Y f hf
  haveI : IsIso (W.Q.map f) := W.Q_inverts f hf
  haveI : IsIso ((higherPresentationUnitFunctor W).map f) := by
    dsimp [higherPresentationUnitFunctor]
    infer_instance
  change
    (F.map ((higherPresentationUnitFunctor W).map f).toLoc).toFunctor.IsEquivalence
  exact pseudofunctor_map_of_isIso_isEquivalence
    F ((higherPresentationUnitFunctor W).map f)

/-- Any actual v2.10 higher localization factorization forces the raw system to
satisfy weak `W`-admissibility. -/
theorem higherLocalizationFactorization_isHigherWAdmissible
    {R : RawHigherContextualSystem (Context := Context)}
    (H : HigherLocalizationFactorization (W := W) R) :
    IsHigherWAdmissible W R := by
  intro X Y f hf
  have hlocal :
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc).toFunctor.IsEquivalence :=
    restrictHigherLocalizedSystem_isHigherWAdmissible W H.lift f hf
  letI :
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc).toFunctor.IsEquivalence :=
    hlocal
  letI : (H.comparison.app (.mk X)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence X
  letI : (H.comparison.app (.mk Y)).toFunctor.IsEquivalence :=
    H.comparison_isEquivalence Y
  have hnat :
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc).toFunctor ⋙
          (H.comparison.app (.mk Y)).toFunctor ≅
        (H.comparison.app (.mk X)).toFunctor ⋙
          (R.map f.toLoc).toFunctor := by
    simpa using Cat.Hom.toNatIso (H.comparison.naturality f.toLoc)
  have hright :
      ((H.comparison.app (.mk X)).toFunctor ⋙
        (R.map f.toLoc).toFunctor).IsEquivalence :=
    Functor.isEquivalence_of_iso hnat
  letI :
      ((H.comparison.app (.mk X)).toFunctor ⋙
        (R.map f.toLoc).toFunctor).IsEquivalence :=
    hright
  exact Functor.isEquivalence_of_comp_left
    (H.comparison.app (.mk X)).toFunctor
    (R.map f.toLoc).toFunctor

/-- Existence-level form of the necessity theorem. -/
theorem hasHigherLocalizationFactorization_isHigherWAdmissible
    {R : RawHigherContextualSystem (Context := Context)}
    (h : HasHigherLocalizationFactorization (W := W) R) :
    IsHigherWAdmissible W R := by
  rcases h with ⟨H⟩
  exact higherLocalizationFactorization_isHigherWAdmissible W H

/-- In particular, the strict-presentation-model sufficient datum introduced in
v2.14 can only exist for a weakly `W`-admissible raw system. -/
theorem hasHigherStrictPresentationModel_isHigherWAdmissible
    {R : RawHigherContextualSystem (Context := Context)}
    (h : HasHigherStrictPresentationModel (W := W) R) :
    IsHigherWAdmissible W R :=
  hasHigherLocalizationFactorization_isHigherWAdmissible W
    (hasHigherLocalizationFactorization_of_strictPresentationModel W h)

/-- Under the still-unproved v2.15 strictification principle, weak
`W`-admissibility is equivalent to existence of a higher localization
factorization.  The reverse implication is unconditional; only the forward
implication uses the principle. -/
theorem higherWAdmissible_iff_hasHigherLocalizationFactorization_of_strictificationPrinciple
    (hstrict : HigherStrictificationPrinciple (W := W))
    (R : RawHigherContextualSystem (Context := Context)) :
    IsHigherWAdmissible W R ↔ HasHigherLocalizationFactorization (W := W) R := by
  constructor
  · intro hR
    exact hasHigherLocalizationFactorization_of_strictPresentationModel W
      (hstrict R hR)
  · exact hasHigherLocalizationFactorization_isHigherWAdmissible W

/-!
The logical boundary is now sharper:

```text
HasHigherLocalizationFactorization W R
        ⇒                         [proved, unconditional]
IsHigherWAdmissible W R
        ⇒                         [open in general]
HasHigherLocalizationFactorization W R.
```

The second arrow follows from the explicit v2.15 strictification principle, but
that principle itself remains unproved.  Consequently v2.16 establishes a
necessary condition and a conditional equivalence; it does not assert the full
weak bicategorical localization theorem.
-/

end KUOS.DependentOriginationHigherLocalizationNecessityV2_16
