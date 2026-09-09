import KUOS.DependentOriginationHigherLocalizationNecessityV2_16

namespace KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationStrictHigherLocalizationV2_11
open KUOS.DependentOriginationWeakToStrictReductionV2_14
open KUOS.DependentOriginationHigherStrictificationPrincipleV2_15
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Pointwise-equivalence transport for higher localization v2.17

The v2.16 layer proves that weak `W`-admissibility is a necessary condition for
an actual higher localization factorization.  This file adds a second structural
property required by a presentation-independent higher semantics: the relevant
notions must be stable under strong comparisons whose components are equivalences
of categories.

We deliberately use a *directed* comparison

```text
R ⟶ S
```

with pointwise equivalence components.  No inverse comparison or global
pseudofunctor isomorphism is silently assumed.  This is exactly the amount of
data already used by the v2.10 factorization interface and the v2.14 strict
presentation model.

The main results are:

* pointwise-equivalence comparisons compose;
* higher localization factorizations transport along them;
* weak `W`-admissibility transports along them;
* strict presentation models transport along them;
* the v2.14 strictifiable sector is exactly the pointwise-equivalence saturation
  of the already-proved strict Cat-valued sector.

Thus the remaining strictification problem can be stated geometrically: whether
every weakly `W`-admissible raw higher system lies in that saturation.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A directed strong comparison of raw higher systems whose components are
equivalences of categories.

This is intentionally weaker than an isomorphism of pseudofunctors: no inverse
comparison is part of the data. -/
structure HigherPointwiseEquivalenceComparison
    (R S : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) where
  comparison : R ⟶ S
  comparison_isEquivalence :
    ∀ X : Context, (comparison.app (.mk X)).toFunctor.IsEquivalence

namespace HigherPointwiseEquivalenceComparison

/-- Identity comparison. -/
noncomputable def refl
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) :
    HigherPointwiseEquivalenceComparison (W := W) R R where
  comparison := 𝟙 _
  comparison_isEquivalence := by
    intro X
    change (𝟭 (R.obj (.mk X))).IsEquivalence
    infer_instance

/-- Composition of pointwise-equivalence comparisons. -/
noncomputable def comp
    {R S T : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (E₁ : HigherPointwiseEquivalenceComparison (W := W) R S)
    (E₂ : HigherPointwiseEquivalenceComparison (W := W) S T) :
    HigherPointwiseEquivalenceComparison (W := W) R T where
  comparison := E₁.comparison ≫ E₂.comparison
  comparison_isEquivalence := by
    intro X
    letI : (E₁.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      E₁.comparison_isEquivalence X
    letI : (E₂.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      E₂.comparison_isEquivalence X
    change
      ((E₁.comparison.app (.mk X)).toFunctor ⋙
        (E₂.comparison.app (.mk X)).toFunctor).IsEquivalence
    infer_instance

end HigherPointwiseEquivalenceComparison

/-- Transport an actual higher localization factorization along a directed
pointwise-equivalence comparison.  The localized lift itself is unchanged; only
the comparison back to the raw system is composed. -/
noncomputable def higherLocalizationFactorizationOfPointwiseEquivalenceComparison
    {R S : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R)
    (E : HigherPointwiseEquivalenceComparison (W := W) R S) :
    HigherLocalizationFactorization (W := W) S where
  lift := H.lift
  comparison := H.comparison ≫ E.comparison
  comparison_isEquivalence := by
    intro X
    letI : (H.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      H.comparison_isEquivalence X
    letI : (E.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      E.comparison_isEquivalence X
    change
      ((H.comparison.app (.mk X)).toFunctor ⋙
        (E.comparison.app (.mk X)).toFunctor).IsEquivalence
    infer_instance

/-- Existence of higher localization factorization is preserved by a directed
pointwise-equivalence comparison. -/
theorem hasHigherLocalizationFactorization_of_pointwiseEquivalenceComparison
    {R S : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hR : HasHigherLocalizationFactorization (W := W) R)
    (E : HigherPointwiseEquivalenceComparison (W := W) R S) :
    HasHigherLocalizationFactorization (W := W) S := by
  rcases hR with ⟨H⟩
  exact ⟨higherLocalizationFactorizationOfPointwiseEquivalenceComparison W H E⟩

/-- Weak `W`-admissibility itself is preserved by a directed
pointwise-equivalence strong comparison. -/
theorem isHigherWAdmissible_of_pointwiseEquivalenceComparison
    {R S : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (E : HigherPointwiseEquivalenceComparison (W := W) R S) :
    IsHigherWAdmissible W S := by
  intro X Y f hf
  have hmapR : (R.map f.toLoc).toFunctor.IsEquivalence := hR f hf
  letI : (R.map f.toLoc).toFunctor.IsEquivalence := hmapR
  letI : (E.comparison.app (.mk X)).toFunctor.IsEquivalence :=
    E.comparison_isEquivalence X
  letI : (E.comparison.app (.mk Y)).toFunctor.IsEquivalence :=
    E.comparison_isEquivalence Y
  have hnat :
      (R.map f.toLoc).toFunctor ⋙
          (E.comparison.app (.mk Y)).toFunctor ≅
        (E.comparison.app (.mk X)).toFunctor ⋙
          (S.map f.toLoc).toFunctor := by
    simpa using Cat.Hom.toNatIso (E.comparison.naturality f.toLoc)
  have hright :
      ((E.comparison.app (.mk X)).toFunctor ⋙
        (S.map f.toLoc).toFunctor).IsEquivalence :=
    Functor.isEquivalence_of_iso hnat
  letI :
      ((E.comparison.app (.mk X)).toFunctor ⋙
        (S.map f.toLoc).toFunctor).IsEquivalence :=
    hright
  exact Functor.isEquivalence_of_comp_left
    (E.comparison.app (.mk X)).toFunctor
    (S.map f.toLoc).toFunctor

/-- Transport a strict presentation model along a directed pointwise-equivalence
comparison.  This proves that the v2.14 strictifiable sector is saturated under
exactly the comparison notion used by the higher localization interface. -/
noncomputable def higherStrictPresentationModelOfPointwiseEquivalenceComparison
    {R S : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (M : HigherStrictPresentationModel (W := W) R)
    (E : HigherPointwiseEquivalenceComparison (W := W) R S) :
    HigherStrictPresentationModel (W := W) S where
  strictFunctor := M.strictFunctor
  strict_inverts := M.strict_inverts
  comparison := M.comparison ≫ E.comparison
  comparison_isEquivalence := by
    intro X
    letI : (M.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      M.comparison_isEquivalence X
    letI : (E.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      E.comparison_isEquivalence X
    change
      ((M.comparison.app (.mk X)).toFunctor ⋙
        (E.comparison.app (.mk X)).toFunctor).IsEquivalence
    infer_instance

/-- Existence-level strict-model transport. -/
theorem hasHigherStrictPresentationModel_of_pointwiseEquivalenceComparison
    {R S : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hR : HasHigherStrictPresentationModel (W := W) R)
    (E : HigherPointwiseEquivalenceComparison (W := W) R S) :
    HasHigherStrictPresentationModel (W := W) S := by
  rcases hR with ⟨M⟩
  exact ⟨higherStrictPresentationModelOfPointwiseEquivalenceComparison W M E⟩

/-- Membership in the pointwise-equivalence saturation of the strict Cat-valued
sector.

Concretely, a raw system lies in this saturation when some ordinary Cat-valued
functor strictly inverting `W` admits a pointwise-equivalence strong comparison
to the raw system. -/
def InStrictSectorPointwiseEquivalenceSaturation
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∃ (G : Context ⥤ Cat.{vH, uH}) (hG : W.IsInvertedBy G),
    Nonempty
      (HigherPointwiseEquivalenceComparison (W := W)
        (strictRawHigherSystem (uH := uH) (vH := vH) G) R)

/-- The v2.14 notion `HasHigherStrictPresentationModel` is exactly membership in
the pointwise-equivalence saturation of the strict sector. -/
theorem hasHigherStrictPresentationModel_iff_inStrictSectorPointwiseEquivalenceSaturation
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) :
    HasHigherStrictPresentationModel (W := W) R ↔
      InStrictSectorPointwiseEquivalenceSaturation (W := W) R := by
  constructor
  · rintro ⟨M⟩
    refine ⟨M.strictFunctor, M.strict_inverts, ?_⟩
    exact ⟨{
      comparison := M.comparison
      comparison_isEquivalence := M.comparison_isEquivalence
    }⟩
  · rintro ⟨G, hG, ⟨E⟩⟩
    exact ⟨{
      strictFunctor := G
      strict_inverts := hG
      comparison := E.comparison
      comparison_isEquivalence := E.comparison_isEquivalence
    }⟩

/-- Every raw system in the strict-sector saturation is weakly `W`-admissible. -/
theorem inStrictSectorPointwiseEquivalenceSaturation_isHigherWAdmissible
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hR : InStrictSectorPointwiseEquivalenceSaturation (W := W) R) :
    IsHigherWAdmissible W R := by
  apply hasHigherStrictPresentationModel_isHigherWAdmissible W
  exact
    (hasHigherStrictPresentationModel_iff_inStrictSectorPointwiseEquivalenceSaturation
      (W := W) R).2 hR

/-- Under the explicitly unproved v2.15 strictification principle, weak
`W`-admissibility is precisely membership in the pointwise-equivalence
saturation of the strict sector. -/
theorem higherWAdmissible_iff_inStrictSectorPointwiseEquivalenceSaturation_of_strictificationPrinciple
    (hstrict : HigherStrictificationPrinciple (W := W) (uH := uH) (vH := vH))
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) :
    IsHigherWAdmissible W R ↔
      InStrictSectorPointwiseEquivalenceSaturation (W := W) R := by
  constructor
  · intro hR
    exact
      (hasHigherStrictPresentationModel_iff_inStrictSectorPointwiseEquivalenceSaturation
        (W := W) R).1 (hstrict R hR)
  · exact inStrictSectorPointwiseEquivalenceSaturation_isHigherWAdmissible W

/-- The v2.15 strictification obstruction is equivalently a weakly admissible raw
system lying outside the strict-sector pointwise-equivalence saturation. -/
theorem higherStrictificationObstruction_iff_not_inStrictSectorPointwiseEquivalenceSaturation
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) :
    HigherStrictificationObstruction (W := W) R ↔
      IsHigherWAdmissible W R ∧
        ¬ InStrictSectorPointwiseEquivalenceSaturation (W := W) R := by
  rw [HigherStrictificationObstruction,
    hasHigherStrictPresentationModel_iff_inStrictSectorPointwiseEquivalenceSaturation
      (W := W) R]

/-!
After v2.17 the strictification route has a presentation-invariant formulation:

```text
strict Cat-valued W-inverting sector
          ↓ pointwise-equivalence StrongTrans saturation
strictifiable raw higher sector
          ↓ v2.14
higher localization factorization
          ↓ v2.16
weak W-admissibility.
```

The open theorem is therefore no longer merely phrased as "find a strict
functor".  It is exactly the question whether every weakly `W`-admissible raw
higher system lies in the pointwise-equivalence saturation of the strict sector,
or alternatively whether a genuine bicategorical localization theorem provides
factorizations beyond that saturation.

No such global saturation theorem is asserted here.
-/

end KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
