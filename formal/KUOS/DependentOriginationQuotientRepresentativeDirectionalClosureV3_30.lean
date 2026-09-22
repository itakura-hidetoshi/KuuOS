import KUOS.DependentOriginationFreePathDirectionalPropagationV3_29

namespace KUOS.DependentOriginationQuotientRepresentativeDirectionalClosureV3_30

open CategoryTheory
open CategoryTheory.Bicategory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28
open KUOS.DependentOriginationFreePathDirectionalPropagationV3_29

universe u v uH vH uQ vQ

set_option autoImplicit false

/-!
# Quotient-representative directional closure v3.30

v3.29 proves that directional properties of generator evaluations propagate
through finite free-localization paths.  The remaining bridge to v3.28 is the
actual representative chosen by the quotient construction.

By definition,

  quotientRepresentativeMap W R D f
    = (freePathEvaluator W R D).map (Quot.out f).

This file records only the conditions that matter on the concrete chosen word
`Quot.out f`.

For each edge of that word:

* an ordinary generator `Sum.inl a` must have the corresponding directional
  property on the raw functor `R.map a`;
* a formal inverse generator `Sum.inr ⟨w, hw⟩` requires no extra hypothesis,
  because v2.56 makes its evaluation the inverse functor of a chosen
  equivalence.

Thus the v3.28 mixed-triangle criterion becomes a condition on the ordinary
letters actually occurring in the two chosen quotient representatives, rather
than a global assumption on all generators.
-/

/-- Evidence that every edge of a quiver path satisfies a dependent edge
predicate.

The recursive occurrence passes the uniform parameters explicitly. In
particular, `@P` preserves the predicate with its implicit endpoint arguments
rather than inserting an eta-expanded function at the recursive occurrence. -/
inductive PathEdgesSatisfy
    {V : Type uQ} [Q : Quiver.{vQ} V]
    (P : ∀ {X Y : V}, (X ⟶ Y) → Prop) :
    ∀ {X Y : V}, Quiver.Path X Y → Prop
  | nil (X : V) :
      @PathEdgesSatisfy V Q (@P) X X (Quiver.Path.nil : Quiver.Path X X)
  | cons {X Y Z : V} {p : Quiver.Path X Y} {e : Y ⟶ Z}
      (hp : @PathEdgesSatisfy V Q (@P) X Y p) (he : @P Y Z e) :
      @PathEdgesSatisfy V Q (@P) X Z (p.cons e)

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Edge condition for essential surjectivity: only ordinary localization
letters carry an assumption.  Formal W-inverse letters are discharged
automatically later. -/
def OrdinaryLocalizationGeneratorEssSurj
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : Localization.Construction.LocQuiver W}
    (e : X ⟶ Y) : Prop :=
  match e with
  | Sum.inl f => (R.map f.toLoc).toFunctor.EssSurj
  | Sum.inr _ => True

/-- Edge condition for faithfulness: only ordinary localization letters carry
an assumption. -/
def OrdinaryLocalizationGeneratorFaithful
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : Localization.Construction.LocQuiver W}
    (e : X ⟶ Y) : Prop :=
  match e with
  | Sum.inl f => (R.map f.toLoc).toFunctor.Faithful
  | Sum.inr _ => True

/-- The ordinary-letter essential-surjectivity condition implies the actual
v3.29 generator-evaluation condition. -/
theorem generatorEvaluatesEssSurj_of_ordinaryCondition
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Localization.Construction.LocQuiver W}
    (e : X ⟶ Y)
    (h : OrdinaryLocalizationGeneratorEssSurj W R e) :
    GeneratorEvaluatesEssSurj W R D e := by
  rcases e with f | w
  · change (R.map f.toLoc).toFunctor.EssSurj at h
    exact (ordinary_generatorEvaluatesEssSurj_iff W R D f).2 h
  · rcases w with ⟨w, hw⟩
    exact formalInverse_generatorEvaluatesEssSurj W R D w hw

/-- The ordinary-letter faithfulness condition implies the actual v3.29
generator-evaluation condition. -/
theorem generatorEvaluatesFaithful_of_ordinaryCondition
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Localization.Construction.LocQuiver W}
    (e : X ⟶ Y)
    (h : OrdinaryLocalizationGeneratorFaithful W R e) :
    GeneratorEvaluatesFaithful W R D e := by
  rcases e with f | w
  · change (R.map f.toLoc).toFunctor.Faithful at h
    exact (ordinary_generatorEvaluatesFaithful_iff W R D f).2 h
  · rcases w with ⟨w, hw⟩
    exact formalInverse_generatorEvaluatesFaithful W R D w hw

/-- A finite path whose ordinary letters are essentially surjective evaluates
to an essentially-surjective functor. -/
theorem freePathEvaluator_map_essSurj_of_pathEdges
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Localization.Construction.LocQuiver W}
    (p : Quiver.Path X Y)
    (hp :
      PathEdgesSatisfy
        (OrdinaryLocalizationGeneratorEssSurj W R) p) :
    ((freePathEvaluator W R D).map p).toFunctor.EssSurj := by
  induction hp with
  | nil X =>
      change (𝟭 _ : _ ⥤ _).EssSurj
      infer_instance
  | @cons X Y Z p e hp he ih =>
      have heEval :=
        generatorEvaluatesEssSurj_of_ordinaryCondition W R D e he
      rw [show p.cons e = p ≫ (Paths.of _).map e by rfl]
      rw [(freePathEvaluator W R D).map_comp]
      rw [freePathEvaluator_map_generator W R D e]
      change
        (((freePathEvaluator W R D).map p).toFunctor ⋙
          ((localizedGeneratorPrefunctor W R D).map e).toFunctor).EssSurj
      exact
        @Functor.essSurj_comp _ _ _ _ _ _
          ((freePathEvaluator W R D).map p).toFunctor
          ((localizedGeneratorPrefunctor W R D).map e).toFunctor
          ih heEval

/-- A finite path whose ordinary letters are faithful evaluates to a faithful
functor. -/
theorem freePathEvaluator_map_faithful_of_pathEdges
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Localization.Construction.LocQuiver W}
    (p : Quiver.Path X Y)
    (hp :
      PathEdgesSatisfy
        (OrdinaryLocalizationGeneratorFaithful W R) p) :
    ((freePathEvaluator W R D).map p).toFunctor.Faithful := by
  induction hp with
  | nil X =>
      change (𝟭 _ : _ ⥤ _).Faithful
      infer_instance
  | @cons X Y Z p e hp he ih =>
      have heEval :=
        generatorEvaluatesFaithful_of_ordinaryCondition W R D e he
      rw [show p.cons e = p ≫ (Paths.of _).map e by rfl]
      rw [(freePathEvaluator W R D).map_comp]
      rw [freePathEvaluator_map_generator W R D e]
      change
        (((freePathEvaluator W R D).map p).toFunctor ⋙
          ((localizedGeneratorPrefunctor W R D).map e).toFunctor).Faithful
      exact
        @Functor.Faithful.comp _ _ _ _ _ _
          ((freePathEvaluator W R D).map p).toFunctor
          ((localizedGeneratorPrefunctor W R D).map e).toFunctor
          ih heEval

/-- The concrete chosen representative of a quotient morphism has
essentially-surjective ordinary letters. -/
def QuotientRepresentativeOrdinaryEssSurj
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : W.Localization} (f : X ⟶ Y) : Prop :=
  PathEdgesSatisfy
    (OrdinaryLocalizationGeneratorEssSurj W R)
    (Quot.out f)

/-- The concrete chosen representative of a quotient morphism has faithful
ordinary letters. -/
def QuotientRepresentativeOrdinaryFaithful
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : W.Localization} (f : X ⟶ Y) : Prop :=
  PathEdgesSatisfy
    (OrdinaryLocalizationGeneratorFaithful W R)
    (Quot.out f)

/-- The path-local ordinary-letter condition is sufficient for the actual
quotient representative map to be essentially surjective. -/
theorem quotientRepresentativeMap_essSurj_of_representative_ordinary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y)
    (hf : QuotientRepresentativeOrdinaryEssSurj W R f) :
    (quotientRepresentativeMap W R D f).toFunctor.EssSurj := by
  change
    ((freePathEvaluator W R D).map (Quot.out f)).toFunctor.EssSurj
  exact
    freePathEvaluator_map_essSurj_of_pathEdges
      W R D (Quot.out f) hf

/-- The path-local ordinary-letter condition is sufficient for the actual
quotient representative map to be faithful. -/
theorem quotientRepresentativeMap_faithful_of_representative_ordinary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y)
    (hf : QuotientRepresentativeOrdinaryFaithful W R f) :
    (quotientRepresentativeMap W R D f).toFunctor.Faithful := by
  change
    ((freePathEvaluator W R D).map (Quot.out f)).toFunctor.Faithful
  exact
    freePathEvaluator_map_faithful_of_pathEdges
      W R D (Quot.out f) hf

/-- v3.28 separation now follows from conditions only on the ordinary letters
of the two concrete `Quot.out` representatives. -/
theorem middleIdentityWhiskerSeparating_of_representative_words
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : QuotientRepresentativeOrdinaryEssSurj W R f)
    (hg : QuotientRepresentativeOrdinaryFaithful W R g) :
    MiddleIdentityWhiskerSeparating W R D f g := by
  exact
    middleIdentityWhiskerSeparating_of_essSurj_faithful
      W R D f g
      (quotientRepresentativeMap_essSurj_of_representative_ordinary
        W R D f hf)
      (quotientRepresentativeMap_faithful_of_representative_ordinary
        W R D g hg)

/-- Consequently the actual associator/right-unitor/left-unitor overlap-star
triangle closes whenever the ordinary letters of the chosen left representative
are essentially surjective and those of the chosen right representative are
faithful. -/
theorem associatorAnchor_unitor_overlapStar_triangle_of_representative_words
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : QuotientRepresentativeOrdinaryEssSurj W R f)
    (hg : QuotientRepresentativeOrdinaryFaithful W R g)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs :
      Qs ∈ quotientRouteCorrectionLocus W R D
        (.associator f (𝟙 Y) g))
    (hQt :
      Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQu :
      Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.rightUnitor f) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.leftUnitor g) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.leftUnitor g) Qt Qu := by
  exact
    associatorAnchor_unitor_overlapStar_triangle_of_essSurj_faithful
      W R D f g
      (quotientRepresentativeMap_essSurj_of_representative_ordinary
        W R D f hf)
      (quotientRepresentativeMap_faithful_of_representative_ordinary
        W R D g hg)
      Qs Qt Qu hQs hQt hQu hst hsu

/-!
## Frontier after v3.30

The v3.26 mixed-triangle obstruction has now been pushed all the way down to
the ordinary letters of the actual `Quot.out` representatives selected by the
quotient implementation.

No global generator hypothesis is required:

* formal W-inverse letters are harmless automatically;
* only ordinary letters occurring in `Quot.out f` matter for left
  essential-surjectivity;
* only ordinary letters occurring in `Quot.out g` matter for right
  faithfulness.

This is sharper than v3.29 and directly feeds v3.28.

The next truth-test is quotient invariance of these directional word
conditions.  Since `Quot.out` is a computational choice, the condition need
not a priori be preserved when one changes representative using the four
localization relations.  The next theorem unit should therefore determine
which of the relations `id`, `comp`, `Winv₁`, and `Winv₂` preserve the
ordinary-letter directional conditions, and isolate the exact obstruction to
making them properties of the quotient morphism rather than of its chosen
representative.
-/

end KUOS.DependentOriginationQuotientRepresentativeDirectionalClosureV3_30
