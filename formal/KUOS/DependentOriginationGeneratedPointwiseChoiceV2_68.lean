import KUOS.DependentOriginationGeneratedWhiskeringV2_68
import KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61

namespace KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedWhiskeringV2_68

universe u v uH vH

/-!
# Canonical generated pointwise choices v2.68

The v2.61 pointwise bundle is inhabited by choosing arbitrary witnesses from
`Nonempty` isomorphism statements.  That is sufficient for pointwise existence,
but it is not the right carrier for generated path-independence: the later
coherence proof must know which localization derivation produced each local
comparison.

This file reconstructs the same three local comparison types from explicit
fully generated derivations:

* identity representative -> identity free path;
* composite representative -> composite of the two representatives;
* raw presentation representative -> ordinary localization generator.

The only classical choice is the already-explicit choice of one generated lift
of an equality in the ordinary localization quotient.  Evaluation of that lift
is the canonical recursive v2.68 evaluation.  Thus `mapId`, `mapComp`, and
`mapIso` are no longer unrelated arbitrary isomorphisms.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Quotient equality used by the generated identity comparison. -/
theorem generatedIdentityRepresentativeEquality
    (X : W.Localization) :
    (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out (𝟙 X)) =
      (Quotient.functor (Localization.Construction.relations W)).map
        (𝟙 X.as) := by
  calc
    (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out (𝟙 X)) = 𝟙 X := by
          change Quot.mk _ (Quot.out (𝟙 X)) = 𝟙 X
          exact Quot.out_eq _
    _ =
        (Quotient.functor (Localization.Construction.relations W)).map
          (𝟙 X.as) := by
          simpa using
            ((Quotient.functor
              (Localization.Construction.relations W)).map_id X.as).symm

/-- Fully generated derivation underlying the quotient identity comparison. -/
noncomputable def generatedIdentityRepresentativeCell
    (X : W.Localization) :
    GeneratedLocalization2Cell W (Quot.out (𝟙 X)) (𝟙 X.as) :=
  chosenGeneratedLocalization2CellOfEquality W
    (generatedIdentityRepresentativeEquality W X)

/-- Quotient equality used by the generated composition comparison. -/
theorem generatedCompositionRepresentativeEquality
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out (f ≫ g)) =
      (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out f ≫ Quot.out g) := by
  calc
    (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out (f ≫ g)) = f ≫ g := by
          change Quot.mk _ (Quot.out (f ≫ g)) = f ≫ g
          exact Quot.out_eq _
    _ =
        (Quotient.functor (Localization.Construction.relations W)).map
            (Quot.out f) ≫
          (Quotient.functor (Localization.Construction.relations W)).map
            (Quot.out g) := by
          change
            f ≫ g =
              Quot.mk _ (Quot.out f) ≫ Quot.mk _ (Quot.out g)
          rw [Quot.out_eq, Quot.out_eq]
    _ =
        (Quotient.functor (Localization.Construction.relations W)).map
          (Quot.out f ≫ Quot.out g) := by
          exact
            ((Quotient.functor
              (Localization.Construction.relations W)).map_comp
                (Quot.out f) (Quot.out g)).symm

/-- Fully generated derivation underlying the quotient composition comparison. -/
noncomputable def generatedCompositionRepresentativeCell
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    GeneratedLocalization2Cell W
      (Quot.out (f ≫ g)) (Quot.out f ≫ Quot.out g) :=
  chosenGeneratedLocalization2CellOfEquality W
    (generatedCompositionRepresentativeEquality W f g)

/-- Quotient equality used by the generated raw-presentation comparison. -/
theorem generatedPresentationRepresentativeEquality
    {X Y : Context} (f : X ⟶ Y) :
    (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out (W.Q.map f)) =
      (Quotient.functor (Localization.Construction.relations W)).map
        (Localization.Construction.ψ₁ W f) := by
  change Quot.mk _ (Quot.out (W.Q.map f)) = W.Q.map f
  exact Quot.out_eq _

/-- Fully generated derivation underlying the comparison back to a raw arrow. -/
noncomputable def generatedPresentationRepresentativeCell
    {X Y : Context} (f : X ⟶ Y) :
    GeneratedLocalization2Cell W
      (Quot.out (W.Q.map f))
      (Localization.Construction.ψ₁ W f) :=
  chosenGeneratedLocalization2CellOfEquality W
    (generatedPresentationRepresentativeEquality W f)

/-- Canonical generated identity comparison. -/
noncomputable def generatedIdentityMapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (X : W.Localization) :
    quotientRepresentativeMap W R D (𝟙 X) ≅
      𝟙 (R.obj (.mk X.as.obj)) := by
  change
    (freePathEvaluator W R D).map (Quot.out (𝟙 X)) ≅
      𝟙 (R.obj (.mk X.as.obj))
  simpa only [Functor.map_id] using
    (generatedLocalization2CellEvaluationIso W R D
      (generatedIdentityRepresentativeCell W X))

/-- Canonical generated composition comparison. -/
noncomputable def generatedCompositionMapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    quotientRepresentativeMap W R D (f ≫ g) ≅
      quotientRepresentativeMap W R D f ≫
        quotientRepresentativeMap W R D g := by
  change
    (freePathEvaluator W R D).map (Quot.out (f ≫ g)) ≅
      (freePathEvaluator W R D).map (Quot.out f) ≫
        (freePathEvaluator W R D).map (Quot.out g)
  simpa only [Functor.map_comp] using
    (generatedLocalization2CellEvaluationIso W R D
      (generatedCompositionRepresentativeCell W f g))

/-- Canonical generated comparison from a localized raw presentation to the
original raw pseudofunctor map. -/
noncomputable def generatedPresentationMapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) :
    quotientRepresentativeMap W R D (W.Q.map f) ≅
      R.map f.toLoc := by
  change
    (freePathEvaluator W R D).map (Quot.out (W.Q.map f)) ≅
      R.map f.toLoc
  rw [← freePathEvaluator_map_ordinary W R D f]
  exact
    generatedLocalization2CellEvaluationIso W R D
      (generatedPresentationRepresentativeCell W f)

/-- The canonical pointwise v2.61 choice bundle induced by fully generated
localization derivations. -/
noncomputable def generatedPointwiseGeneralWChoiceData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    PointwiseGeneralWChoiceData (W := W) R D where
  mapId := generatedIdentityMapIso W R D
  mapComp := generatedCompositionMapIso W R D
  mapIso := generatedPresentationMapIso W R D

@[simp]
theorem generatedPointwiseGeneralWChoiceData_mapId
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (X : W.Localization) :
    (generatedPointwiseGeneralWChoiceData W R D).mapId X =
      generatedIdentityMapIso W R D X := by
  rfl

@[simp]
theorem generatedPointwiseGeneralWChoiceData_mapComp
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (generatedPointwiseGeneralWChoiceData W R D).mapComp f g =
      generatedCompositionMapIso W R D f g := by
  rfl

@[simp]
theorem generatedPointwiseGeneralWChoiceData_mapIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) :
    (generatedPointwiseGeneralWChoiceData W R D).mapIso f =
      generatedPresentationMapIso W R D f := by
  rfl

/-- Weak W-admissibility supplies the canonical generated pointwise bundle after
selecting the v2.56 pointwise adjoint-equivalence data. -/
noncomputable def generatedPointwiseGeneralWChoiceDataOfAdmissible
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R) :
    PointwiseGeneralWChoiceData (W := W) R
      (pointwiseWAdjointEquivalenceDataOfAdmissible W hR) :=
  generatedPointwiseGeneralWChoiceData W R
    (pointwiseWAdjointEquivalenceDataOfAdmissible W hR)

/-!
## Boundary

The local comparison bundle used by the remaining v2.68 coherence proof is now
canonical relative to a selected fully generated lift of each quotient equality:

```text
quotient equality
  -> chosen GeneratedLocalization2Cell
  -> canonical recursive evaluation
  -> mapId / mapComp / mapIso.
```

No arbitrary `Nonempty` isomorphism witness is used in this bundle.  The next
layer compares explicit generated associativity, unit, identity-comparison, and
composition-comparison routes.  Generated path-independence can then force the
five v2.65 defects of this exact bundle to vanish.
-/

end KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
