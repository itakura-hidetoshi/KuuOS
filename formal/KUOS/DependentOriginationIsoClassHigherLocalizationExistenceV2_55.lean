import Mathlib.CategoryTheory.Localization.Predicate
import KUOS.DependentOriginationDetectingFamilyObstructionEliminationV2_54
import KUOS.DependentOriginationHigherLocalizationNecessityV2_16

namespace KUOS.DependentOriginationIsoClassHigherLocalizationExistenceV2_55

open CategoryTheory
open Opposite
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Isomorphism-class higher-localization existence v2.55

The v2.42--v2.54 obstruction-elimination layers close increasingly broad
*uniqueness/coherence* routes once a chosen higher-localization carrier already
exists.  The genuinely different Track A1 problem is existence:

```text
IsHigherWAdmissible W R
        ?⇒
HasHigherLocalizationFactorization W R.
```

That implication remains open in general.  In particular, ordinary localization
of Cat-valued functors cannot simply be substituted for bicategorical
localization of arbitrary pseudofunctors.

This file proves a restricted but genuine higher existence theorem.  Assume that
the declared presentation morphisms were already isomorphisms in the original
context category:

```text
W ≤ MorphismProperty.isomorphisms Context.
```

Mathlib then proves that `𝟭 Context` itself is a localization of `Context` at
`W`.  Hence the canonical localization carrier `W.Localization` is equivalent
to `Context`.  We use that equivalence on the *source* of an arbitrary raw
Cat-valued pseudofunctor `R`; we do not replace `R` by an ordinary functor and do
not assume a strict presentation model.

The construction is

```text
((W.Localization)ᵒᵖ)ᵒᵖ
      --unopUnop--> W.Localization
      --E---------> Context
      --R---------> Cat,
```

where `E : W.Localization ≌ Context` is supplied by Mathlib's localization
universal property.  Restriction back along the presentation unit is compared
to `R` by the canonical triangle

```text
W.Q ⋙ E.functor ≅ 𝟭 Context.
```

Its components are actual isomorphisms in `Context`; the existing v2.16 lemma
then shows that `R` sends each component to an equivalence of categories.

Thus this theorem advances Track A1 without asserting the still-missing general
weak bicategorical localization theorem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- When every arrow declared by `W` is already an isomorphism, Mathlib's
canonical localization is equivalent to the original context category.

This is an equivalence of *base categories*.  It does not strictify the
Cat-valued pseudofunctor that will later be transported along it. -/
noncomputable def isoClassLocalizationEquivalence
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    LocalizedContext W ≌ Context := by
  letI : (𝟭 Context).IsLocalization W :=
    Functor.IsLocalization.for_id (W := W) hW
  exact Localization.equivalenceFromModel (𝟭 Context) W

/-- The canonical localization triangle for the base equivalence used in v2.55. -/
noncomputable def isoClassPresentationTriangleIso
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    W.Q ⋙ (isoClassLocalizationEquivalence W hW).functor ≅ 𝟭 Context := by
  letI : (𝟭 Context).IsLocalization W :=
    Functor.IsLocalization.for_id (W := W) hW
  exact Localization.qCompEquivalenceFromModelFunctorIso (𝟭 Context) W

/-- The ordinary base functor underlying the localized source of an arbitrary
raw higher system in the isomorphism-only sector. -/
noncomputable def isoClassLocalizedBaseFunctor
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    (HigherLocalizedSite W)ᵒᵖ ⥤ Context :=
  unopUnop (LocalizedContext W) ⋙
    (isoClassLocalizationEquivalence W hW).functor

/-- Transport an arbitrary raw Cat-valued pseudofunctor along the equivalence of
base categories.  No ordinary Cat-valued replacement of `R` is introduced. -/
noncomputable def isoClassLocalizedHigherSystem
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    HigherLocalizedDescentSystem (W := W) :=
  Pseudofunctor.comp
    (isoClassLocalizedBaseFunctor W hW).toPseudofunctor R

/-- The strong comparison from the restriction of the transported localized
system back to the original arbitrary pseudofunctor.

The component at `X` is `R` applied to the `X`-component of the canonical base
triangle.  Naturality is obtained by pasting the two pseudofunctor compositors
around the image under `R` of the ordinary naturality equality. -/
noncomputable def isoClassHigherLocalizationComparison
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    restrictHigherLocalizedSystem W
        (isoClassLocalizedHigherSystem W R hW) ⟶ R := by
  let E := isoClassLocalizationEquivalence W hW
  let η := isoClassPresentationTriangleIso W hW
  refine
    { app := fun X => R.map ((η.hom.app X.as).toLoc)
      naturality := ?_ }
  intro X Y f
  change
    R.map (((W.Q ⋙ E.functor).map f.as).toLoc) ≫
          R.map ((η.hom.app Y.as).toLoc) ≅
      R.map ((η.hom.app X.as).toLoc) ≫ R.map (f.as.toLoc)
  refine
    (R.mapComp
        (((W.Q ⋙ E.functor).map f.as).toLoc)
        ((η.hom.app Y.as).toLoc)).symm ≪≫
      R.map₂Iso (eqToIso ?_) ≪≫
      R.mapComp ((η.hom.app X.as).toLoc) (f.as.toLoc)
  simpa only [Quiver.Hom.comp_toLoc] using
    congrArg (fun k => k.toLoc) (η.hom.naturality f.as)

/-- Every component of the v2.55 comparison is an equivalence of categories,
because it is the image under `R` of an actual isomorphism in `Context`. -/
theorem isoClassHigherLocalizationComparison_app_isEquivalence
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hW : W ≤ MorphismProperty.isomorphisms Context)
    (X : Context) :
    ((isoClassHigherLocalizationComparison W R hW).app (.mk X)).toFunctor.IsEquivalence := by
  change
    (R.map
      (((isoClassPresentationTriangleIso W hW).hom.app X).toLoc)).toFunctor.IsEquivalence
  exact pseudofunctor_map_of_isIso_isEquivalence R
    ((isoClassPresentationTriangleIso W hW).hom.app X)

/-- Actual v2.10 higher-localization factorization data for an arbitrary raw
higher system when `W` contains only morphisms that were already isomorphisms. -/
noncomputable def isoClassHigherLocalizationFactorization
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    HigherLocalizationFactorization (W := W) R where
  lift := isoClassLocalizedHigherSystem W R hW
  comparison := isoClassHigherLocalizationComparison W R hW
  comparison_isEquivalence :=
    isoClassHigherLocalizationComparison_app_isEquivalence W R hW

/-- Restricted Track A1 existence theorem.

If all declared presentation maps are already isomorphisms in `Context`, every
raw Cat-valued pseudofunctor admits an actual higher-localization factorization
in the exact v2.10 interface. -/
theorem hasHigherLocalizationFactorization_of_le_isomorphisms
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    HasHigherLocalizationFactorization (W := W) R :=
  ⟨isoClassHigherLocalizationFactorization W R hW⟩

/-- In the same restricted sector every raw pseudofunctor is automatically
weakly `W`-admissible.  This is also forced by v2.16 from the factorization just
constructed, but the direct proof records the elementary reason. -/
theorem isHigherWAdmissible_of_le_isomorphisms
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    IsHigherWAdmissible W R := by
  intro X Y f hf
  letI : IsIso f := hW f hf
  exact pseudofunctor_map_of_isIso_isEquivalence R f

/-- Therefore, in the isomorphism-only presentation sector the exact v2.10
existence predicate and weak admissibility are both inhabited for every raw
higher system.  This is deliberately not stated as a general equivalence beyond
that sector. -/
theorem isoClassSector_admissible_and_hasFactorization
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hW : W ≤ MorphismProperty.isomorphisms Context) :
    IsHigherWAdmissible W R ∧
      HasHigherLocalizationFactorization (W := W) R :=
  ⟨isHigherWAdmissible_of_le_isomorphisms W R hW,
    hasHigherLocalizationFactorization_of_le_isomorphisms W R hW⟩

/-!
## Authority boundary

The theorem proved here is exactly

```text
W ≤ isomorphisms(Context)
+ arbitrary R : LocallyDiscrete Context ⥤ᵖ Cat
        ↓
base localization equivalence W.Localization ≌ Context
        ↓
transport R on the source
        ↓
HigherLocalizationFactorization W R.
```

It does **not** prove

```text
IsHigherWAdmissible W R
        ⇒
HasHigherLocalizationFactorization W R
```

for a general morphism class `W`.  No strict presentation model is constructed,
no weak equivalence-valued pseudofunctor is silently replaced by an ordinary
functor, and no general bicategorical localization principle is asserted.
Likewise this file proves no stack-descent existence, no coherent universal-data
existence beyond the displayed factorization, no strictification, and no final
global dependent-origination theorem.
-/

end KUOS.DependentOriginationIsoClassHigherLocalizationExistenceV2_55
