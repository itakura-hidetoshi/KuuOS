import KUOS.DependentOriginationStrictHigherUniversalityV2_13

namespace KUOS.DependentOriginationWeakToStrictReductionV2_14

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationStrictHigherLocalizationV2_11
open KUOS.DependentOriginationStrictHigherFactorizationV2_12
open KUOS.DependentOriginationStrictHigherUniversalityV2_13

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Weak-to-strict higher localization reduction v2.14

The v2.11-v2.13 layers completely solve the presentation-localization problem
in the strict Cat-valued sector: an ordinary functor `G : C ⥤ Cat` which sends
`W` to actual isomorphisms in the 1-category `Cat` has a canonical localized
lift, a strong comparison, and an essentially unique ordinary localized carrier.

The remaining higher problem starts with a raw pseudofunctor

```text
R : LocallyDiscrete C ⥤ᵖ Cat
```

whose arrows in `W` are required only to be equivalences of categories.  This
file does not assert that every such `R` can be strictified.  Instead, it isolates
a precise sufficient datum: a strict `W`-inverting ordinary Cat-valued model,
together with a strong pointwise-equivalence comparison from its promoted
pseudofunctor to `R`.

Once such a model is supplied, the strict v2.12 localization factorization can
be transported to `R` simply by composing strong transformations.  Therefore
the unresolved theorem is narrowed further: construct such strict presentation
models (or prove a genuinely bicategorical localization theorem) for arbitrary
weakly `W`-admissible raw systems.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A sufficient strict presentation model for a raw higher contextual system.

This is data, not an existence theorem.  The ordinary functor strictly inverts
`W` in `Cat`, while the promoted strict pseudofunctor is compared to the given
raw system by a strong transformation whose components are equivalences of
categories. -/
structure HigherStrictPresentationModel
    (R : RawHigherContextualSystem (Context := Context)) where
  /-- Ordinary Cat-valued strict model. -/
  strictFunctor : Context ⥤ Cat.{vH, uH}
  /-- The strict model sends every arrow in `W` to an actual isomorphism in `Cat`. -/
  strict_inverts : W.IsInvertedBy strictFunctor
  /-- Strong comparison from the promoted strict model to the raw higher system. -/
  comparison :
    strictRawHigherSystem strictFunctor ⟶ R
  /-- The comparison is pointwise an equivalence of categories. -/
  comparison_isEquivalence :
    ∀ X : Context, (comparison.app (.mk X)).toFunctor.IsEquivalence

/-- Existence of a strict presentation model is kept explicit rather than
silently assumed. -/
def HasHigherStrictPresentationModel
    (R : RawHigherContextualSystem (Context := Context)) : Prop :=
  Nonempty (HigherStrictPresentationModel (W := W) R)

/-- Transport the canonical strict higher localization factorization along a
pointwise-equivalence strong comparison to an arbitrary raw higher system. -/
noncomputable def higherLocalizationFactorizationOfStrictPresentationModel
    {R : RawHigherContextualSystem (Context := Context)}
    (S : HigherStrictPresentationModel (W := W) R) :
    HigherLocalizationFactorization (W := W) R where
  lift := strictLocalizedHigherSystem W S.strictFunctor S.strict_inverts
  comparison :=
    strictHigherLocalizationComparison W S.strictFunctor S.strict_inverts ≫
      S.comparison
  comparison_isEquivalence := by
    intro X
    letI :
        ((strictHigherLocalizationComparison W S.strictFunctor S.strict_inverts).app
          (.mk X)).toFunctor.IsEquivalence :=
      strictHigherLocalizationComparison_app_isEquivalence
        W S.strictFunctor S.strict_inverts X
    letI : (S.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      S.comparison_isEquivalence X
    change
      (((strictHigherLocalizationComparison W S.strictFunctor S.strict_inverts).app (.mk X)).toFunctor ⋙
        (S.comparison.app (.mk X)).toFunctor).IsEquivalence
    infer_instance

/-- Therefore a strict presentation model is a sufficient condition for the
exact v2.10 higher localization factorization to exist. -/
theorem hasHigherLocalizationFactorization_of_strictPresentationModel
    {R : RawHigherContextualSystem (Context := Context)}
    (h : HasHigherStrictPresentationModel (W := W) R) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases h with ⟨S⟩
  exact ⟨higherLocalizationFactorizationOfStrictPresentationModel W S⟩

/-- Every already-strict raw Cat-valued system is, tautologically, equipped with
such a strict presentation model.  This records that v2.14 genuinely extends the
v2.12 route rather than replacing it. -/
noncomputable def strictRawHigherSystem_strictPresentationModel
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    HigherStrictPresentationModel (W := W)
      (strictRawHigherSystem G) where
  strictFunctor := G
  strict_inverts := hG
  comparison := 𝟙 _
  comparison_isEquivalence := by
    intro X
    change (𝟭 (G.obj X)).IsEquivalence
    infer_instance

/-- In particular, the reduction theorem recovers existence for the original
strict sector. -/
theorem strictSector_hasHigherStrictPresentationModel
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    HasHigherStrictPresentationModel (W := W)
      (strictRawHigherSystem G) :=
  ⟨strictRawHigherSystem_strictPresentationModel W G hG⟩

/-!
The formal implication established here is

```text
raw higher system R
+ explicit strict presentation model S
        ↓
strict v2.12 localization factorization of S.strictFunctor
        ↓
compose its strong comparison with S.comparison
        ↓
HigherLocalizationFactorization R.
```

What is *not* proved is

```text
IsHigherWAdmissible W R
        ⇒
HasHigherStrictPresentationModel W R.
```

Nor is it proved that every weakly admissible pseudofunctor factors directly
through the ordinary localization.  Establishing one of those statements is the
next genuine higher-localization obligation.  This keeps the difference between
strict isomorphism-valued presentation invariance and equivalence-valued
bicategorical presentation invariance explicit in the formal development.
-/

end KUOS.DependentOriginationWeakToStrictReductionV2_14
