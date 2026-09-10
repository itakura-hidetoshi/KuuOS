import KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68

namespace KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedWhiskeringV2_68
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68

universe u v uH vH

/-!
# Five explicit generated coherence routes v2.68

The canonical pointwise v2.68 bundle remembers the generated derivation behind
`mapId`, `mapComp`, and `mapIso`.  This file now writes the five v2.59/v2.60
coherence comparisons themselves inside the fully generated localization syntax.

The construction is deliberately syntax-first.  We do not yet normalize the
resulting Cat-valued evaluations into the v2.65 defect formulas.  Instead we
prove that generated path-independence identifies each pair of explicit routes.
The next layer can perform the purely bicategorical normalization separately.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Embed one retained localization generator into the fully generated syntax.
The composition-closure constructor is used with identity whiskers; the path
category identity laws remove those bookkeeping whiskers. -/
def generatedLocalization2CellOfGenerating
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : LocalizationGenerating2Cell W p q) :
    GeneratedLocalization2Cell W p q := by
  simpa using
    (GeneratedLocalization2Cell.ofCompClosure
      (GeneratedCompClosure2Cell.whisker (W := W) (𝟙 X) α (𝟙 Y)))

/-! ## Quotient associativity route -/

/-- The long generated route underlying the v2.59 associativity law. -/
noncomputable def generatedQuotientAssociatorRoute
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    GeneratedLocalization2Cell W
      (Quot.out ((f ≫ g) ≫ h))
      (Quot.out (f ≫ (g ≫ h))) := by
  refine GeneratedLocalization2Cell.trans
    (generatedCompositionRepresentativeCell W (f ≫ g) h) ?_
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellWhiskerRight W (Quot.out h)
      (generatedCompositionRepresentativeCell W f g)) ?_
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellOfEq W
      (Category.assoc (Quot.out f) (Quot.out g) (Quot.out h))) ?_
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellWhiskerLeft W (Quot.out f)
      (GeneratedLocalization2Cell.symm
        (generatedCompositionRepresentativeCell W g h))) ?_
  exact GeneratedLocalization2Cell.symm
    (generatedCompositionRepresentativeCell W f (g ≫ h))

/-- The direct path-equality route between the two parenthesizations. -/
def generatedQuotientAssociatorDirect
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    GeneratedLocalization2Cell W
      (Quot.out ((f ≫ g) ≫ h))
      (Quot.out (f ≫ (g ≫ h))) :=
  generatedLocalization2CellOfEq W
    (congrArg (fun k => Quot.out k) (Category.assoc f g h))

/-! ## Quotient unit routes -/

/-- The long generated route underlying the v2.59 left-unit law. -/
noncomputable def generatedQuotientLeftUnitorRoute
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedLocalization2Cell W
      (Quot.out ((𝟙 X) ≫ f)) (Quot.out f) := by
  refine GeneratedLocalization2Cell.trans
    (generatedCompositionRepresentativeCell W (𝟙 X) f) ?_
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellWhiskerRight W (Quot.out f)
      (generatedIdentityRepresentativeCell W X)) ?_
  exact generatedLocalization2CellOfEq W
    (Category.id_comp (Quot.out f))

/-- Direct path-equality route for the localized left-unit equality. -/
def generatedQuotientLeftUnitorDirect
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedLocalization2Cell W
      (Quot.out ((𝟙 X) ≫ f)) (Quot.out f) :=
  generatedLocalization2CellOfEq W
    (congrArg (fun k => Quot.out k) (Category.id_comp f))

/-- The long generated route underlying the v2.59 right-unit law. -/
noncomputable def generatedQuotientRightUnitorRoute
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedLocalization2Cell W
      (Quot.out (f ≫ 𝟙 Y)) (Quot.out f) := by
  refine GeneratedLocalization2Cell.trans
    (generatedCompositionRepresentativeCell W f (𝟙 Y)) ?_
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellWhiskerLeft W (Quot.out f)
      (generatedIdentityRepresentativeCell W Y)) ?_
  exact generatedLocalization2CellOfEq W
    (Category.comp_id (Quot.out f))

/-- Direct path-equality route for the localized right-unit equality. -/
def generatedQuotientRightUnitorDirect
    {X Y : W.Localization} (f : X ⟶ Y) :
    GeneratedLocalization2Cell W
      (Quot.out (f ≫ 𝟙 Y)) (Quot.out f) :=
  generatedLocalization2CellOfEq W
    (congrArg (fun k => Quot.out k) (Category.comp_id f))

/-! ## Presentation comparison routes -/

/-- Raw identity comparison route: first return from the quotient representative
to the ordinary raw generator, then apply the retained localization `id`
generator. -/
noncomputable def generatedComparisonIdentityRawRoute
    (X : Context) :
    GeneratedLocalization2Cell W
      (Quot.out (W.Q.map (𝟙 X))) (𝟙 _) :=
  GeneratedLocalization2Cell.trans
    (generatedPresentationRepresentativeCell W (𝟙 X))
    (generatedLocalization2CellOfGenerating W
      (LocalizationGenerating2Cell.id X))

/-- Quotient identity route for the same raw identity comparison.  Functoriality
of `W.Q` first identifies `Q(id)` with the localized identity; the canonical
quotient identity cell then reaches the identity free path. -/
noncomputable def generatedComparisonIdentityQuotientRoute
    (X : Context) :
    GeneratedLocalization2Cell W
      (Quot.out (W.Q.map (𝟙 X))) (𝟙 _) := by
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellOfEq W
      (congrArg (fun k => Quot.out k) (W.Q.map_id X))) ?_
  exact generatedIdentityRepresentativeCell W (W.Q.obj X)

/-- Raw composition comparison route: presentation of `f ≫ g` followed by the
retained raw composition generator. -/
noncomputable def generatedComparisonCompositionRawRoute
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :
    GeneratedLocalization2Cell W
      (Quot.out (W.Q.map (f ≫ g)))
      (Localization.Construction.ψ₁ W f ≫
        Localization.Construction.ψ₁ W g) :=
  GeneratedLocalization2Cell.trans
    (generatedPresentationRepresentativeCell W (f ≫ g))
    (generatedLocalization2CellOfGenerating W
      (LocalizationGenerating2Cell.comp f g))

/-- Quotient composition route for the same raw composite.  It passes through
`Q.map_comp`, the canonical quotient `mapComp` derivation, and the two generated
presentation derivations whiskered into the composite. -/
noncomputable def generatedComparisonCompositionQuotientRoute
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :
    GeneratedLocalization2Cell W
      (Quot.out (W.Q.map (f ≫ g)))
      (Localization.Construction.ψ₁ W f ≫
        Localization.Construction.ψ₁ W g) := by
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellOfEq W
      (congrArg (fun k => Quot.out k) (W.Q.map_comp f g))) ?_
  refine GeneratedLocalization2Cell.trans
    (generatedCompositionRepresentativeCell W (W.Q.map f) (W.Q.map g)) ?_
  refine GeneratedLocalization2Cell.trans
    (generatedLocalization2CellWhiskerRight W
      (Quot.out (W.Q.map g))
      (generatedPresentationRepresentativeCell W f)) ?_
  exact generatedLocalization2CellWhiskerLeft W
    (Localization.Construction.ψ₁ W f)
    (generatedPresentationRepresentativeCell W g)

/-! ## Path-independence identifies all five route pairs -/

/-- Generated path-independence is exactly strong enough to identify the two
associativity routes. -/
theorem generatedQuotientAssociatorRoutes_evaluation_eq
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientAssociatorRoute W f g h) =
      generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientAssociatorDirect W f g h) :=
  hPI _ _

/-- Generated path-independence identifies the two left-unit routes. -/
theorem generatedQuotientLeftUnitorRoutes_evaluation_eq
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientLeftUnitorRoute W f) =
      generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientLeftUnitorDirect W f) :=
  hPI _ _

/-- Generated path-independence identifies the two right-unit routes. -/
theorem generatedQuotientRightUnitorRoutes_evaluation_eq
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientRightUnitorRoute W f) =
      generatedLocalization2CellEvaluationIso W R D
        (generatedQuotientRightUnitorDirect W f) :=
  hPI _ _

/-- Generated path-independence identifies the two identity-presentation routes. -/
theorem generatedComparisonIdentityRoutes_evaluation_eq
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D)
    (X : Context) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonIdentityRawRoute W X) =
      generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonIdentityQuotientRoute W X) :=
  hPI _ _

/-- Generated path-independence identifies the two composition-presentation
routes. -/
theorem generatedComparisonCompositionRoutes_evaluation_eq
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hPI : GeneratedEvaluationPathIndependent W R D)
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonCompositionRawRoute W f g) =
      generatedLocalization2CellEvaluationIso W R D
        (generatedComparisonCompositionQuotientRoute W f g) :=
  hPI _ _

/-!
## Boundary

The five coherence comparisons now exist as literal pairs of generated
localization derivations with common endpoints.  Nothing in this file assumes
the v2.59 or v2.60 coherence equations themselves.

The only implication proved here is

```text
GeneratedEvaluationPathIndependent
  -> equality of the evaluated associator route pair
  -> equality of the evaluated left-unit route pair
  -> equality of the evaluated right-unit route pair
  -> equality of the evaluated comparison-identity route pair
  -> equality of the evaluated comparison-composition route pair.
```

The next layer will normalize those five evaluation equalities in strict `Cat`
and identify them with the five v2.65 defect-vanishing equations for the exact
canonical generated pointwise bundle.
-/

end KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68
