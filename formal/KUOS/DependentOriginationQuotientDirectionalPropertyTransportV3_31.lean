import KUOS.DependentOriginationQuotientRepresentativeDirectionalClosureV3_30

namespace KUOS.DependentOriginationQuotientDirectionalPropertyTransportV3_31

open CategoryTheory
open CategoryTheory.Bicategory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28
open KUOS.DependentOriginationQuotientRepresentativeDirectionalClosureV3_30

universe u v uH vH

set_option autoImplicit false

/-!
# Quotient-invariant directional properties v3.31

v3.30 provides sufficient ordinary-letter certificates for a concrete free
path. Such a certificate is syntactic: composition preserving a property does
not imply that the property of a composite reflects to every factor.

Here we instead transport the semantic properties of the evaluated functors.
v2.58 already proves existence of an evaluation isomorphism whenever two paths
are equal in the localization. Mathlib's `Cat.Hom.toNatIso`,
`Functor.essSurj_of_iso`, and `Functor.Faithful.of_iso` transfer the two
properties in both directions.

All these conclusions are propositions. We eliminate `Nonempty Iso` only
locally into those propositions; no simultaneous family of evaluation
isomorphisms or new coherence datum is selected.

Consequently one good representative is sufficient, regardless of whether the
actual `Quot.out` word itself has the ordinary-letter certificate. This feeds
the existing v3.28 separation and mixed-triangle closure theorems without
changing any corrected-route or anchor-overlap hypothesis.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Essential surjectivity of a path evaluation depends only on its image in
the localization, not on the chosen free-path representative. -/
theorem freePathEvaluator_map_essSurj_iff_of_equalInLocalization
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Paths (Localization.Construction.LocQuiver W)}
    {p q : X ⟶ Y}
    (hpq :
      (Quotient.functor (Localization.Construction.relations W)).map p =
      (Quotient.functor (Localization.Construction.relations W)).map q) :
    ((freePathEvaluator W R D).map p).toFunctor.EssSurj ↔
      ((freePathEvaluator W R D).map q).toFunctor.EssSurj := by
  rcases equalInLocalization_hasEvaluationIso W R D hpq with ⟨e⟩
  have eNat := Cat.Hom.toNatIso e
  constructor
  · intro hp
    letI : ((freePathEvaluator W R D).map p).toFunctor.EssSurj := hp
    exact Functor.essSurj_of_iso eNat
  · intro hq
    letI : ((freePathEvaluator W R D).map q).toFunctor.EssSurj := hq
    exact Functor.essSurj_of_iso eNat.symm

/-- Faithfulness of a path evaluation is likewise invariant under equality in
the localization. No letterwise reflection statement is used. -/
theorem freePathEvaluator_map_faithful_iff_of_equalInLocalization
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Paths (Localization.Construction.LocQuiver W)}
    {p q : X ⟶ Y}
    (hpq :
      (Quotient.functor (Localization.Construction.relations W)).map p =
      (Quotient.functor (Localization.Construction.relations W)).map q) :
    ((freePathEvaluator W R D).map p).toFunctor.Faithful ↔
      ((freePathEvaluator W R D).map q).toFunctor.Faithful := by
  rcases equalInLocalization_hasEvaluationIso W R D hpq with ⟨e⟩
  have eNat := Cat.Hom.toNatIso e
  constructor
  · intro hp
    letI : ((freePathEvaluator W R D).map p).toFunctor.Faithful := hp
    exact Functor.Faithful.of_iso eNat
  · intro hq
    letI : ((freePathEvaluator W R D).map q).toFunctor.Faithful := hq
    exact Functor.Faithful.of_iso eNat.symm

/-- The selected quotient map is essentially surjective exactly when the
evaluation of any specified representative is essentially surjective. -/
theorem quotientRepresentativeMap_essSurj_iff_of_representative
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y)
    (p : X.as ⟶ Y.as)
    (hp :
      (Quotient.functor (Localization.Construction.relations W)).map p = f) :
    (quotientRepresentativeMap W R D f).toFunctor.EssSurj ↔
      ((freePathEvaluator W R D).map p).toFunctor.EssSurj := by
  have hOut :
      (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out f) = f := by
    exact Quot.out_eq f
  change
    ((freePathEvaluator W R D).map (Quot.out f)).toFunctor.EssSurj ↔
      ((freePathEvaluator W R D).map p).toFunctor.EssSurj
  exact
    freePathEvaluator_map_essSurj_iff_of_equalInLocalization
      W R D (hOut.trans hp.symm)

/-- The analogous semantic equivalence for faithfulness of a representative. -/
theorem quotientRepresentativeMap_faithful_iff_of_representative
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y)
    (p : X.as ⟶ Y.as)
    (hp :
      (Quotient.functor (Localization.Construction.relations W)).map p = f) :
    (quotientRepresentativeMap W R D f).toFunctor.Faithful ↔
      ((freePathEvaluator W R D).map p).toFunctor.Faithful := by
  have hOut :
      (Quotient.functor (Localization.Construction.relations W)).map
        (Quot.out f) = f := by
    exact Quot.out_eq f
  change
    ((freePathEvaluator W R D).map (Quot.out f)).toFunctor.Faithful ↔
      ((freePathEvaluator W R D).map p).toFunctor.Faithful
  exact
    freePathEvaluator_map_faithful_iff_of_equalInLocalization
      W R D (hOut.trans hp.symm)

/-- At least one representative has essentially-surjective ordinary letters.
This is a sufficient certificate on the quotient morphism, not a claimed
necessary characterization of its evaluation. -/
def HasOrdinaryEssSurjRepresentative
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : W.Localization} (f : X ⟶ Y) : Prop :=
  ∃ p : X.as ⟶ Y.as,
    (Quotient.functor (Localization.Construction.relations W)).map p = f ∧
      PathEdgesSatisfy (OrdinaryLocalizationGeneratorEssSurj W R) p

/-- At least one representative has faithful ordinary letters. The witness
need not be the word selected by `Quot.out`. -/
def HasOrdinaryFaithfulRepresentative
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : W.Localization} (f : X ⟶ Y) : Prop :=
  ∃ p : X.as ⟶ Y.as,
    (Quotient.functor (Localization.Construction.relations W)).map p = f ∧
      PathEdgesSatisfy (OrdinaryLocalizationGeneratorFaithful W R) p

/-- The v3.30 chosen-word certificate implies the new existence certificate. -/
theorem hasOrdinaryEssSurjRepresentative_of_chosen_word
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : W.Localization} (f : X ⟶ Y)
    (hf : QuotientRepresentativeOrdinaryEssSurj W R f) :
    HasOrdinaryEssSurjRepresentative W R f := by
  refine ⟨Quot.out f, ?_, hf⟩
  exact Quot.out_eq f

/-- The faithful chosen-word criterion is also a special case. -/
theorem hasOrdinaryFaithfulRepresentative_of_chosen_word
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    {X Y : W.Localization} (f : X ⟶ Y)
    (hf : QuotientRepresentativeOrdinaryFaithful W R f) :
    HasOrdinaryFaithfulRepresentative W R f := by
  refine ⟨Quot.out f, ?_, hf⟩
  exact Quot.out_eq f

/-- One good representative suffices for essential surjectivity of the actual
quotient representative map. -/
theorem quotientRepresentativeMap_essSurj_of_exists_ordinary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y)
    (hf : HasOrdinaryEssSurjRepresentative W R f) :
    (quotientRepresentativeMap W R D f).toFunctor.EssSurj := by
  rcases hf with ⟨p, hp, hLetters⟩
  exact
    (quotientRepresentativeMap_essSurj_iff_of_representative W R D f p hp).2
      (freePathEvaluator_map_essSurj_of_pathEdges W R D p hLetters)

/-- One representative with faithful ordinary letters suffices for faithfulness
of the actual quotient representative map. -/
theorem quotientRepresentativeMap_faithful_of_exists_ordinary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y)
    (hf : HasOrdinaryFaithfulRepresentative W R f) :
    (quotientRepresentativeMap W R D f).toFunctor.Faithful := by
  rcases hf with ⟨p, hp, hLetters⟩
  exact
    (quotientRepresentativeMap_faithful_iff_of_representative W R D f p hp).2
      (freePathEvaluator_map_faithful_of_pathEdges W R D p hLetters)

/-- v3.28 double-whiskering separation from existence of good representatives,
without imposing a syntactic certificate on either selected `Quot.out` word. -/
theorem middleIdentityWhiskerSeparating_of_exists_representatives
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : HasOrdinaryEssSurjRepresentative W R f)
    (hg : HasOrdinaryFaithfulRepresentative W R g) :
    MiddleIdentityWhiskerSeparating W R D f g := by
  exact
    middleIdentityWhiskerSeparating_of_essSurj_faithful W R D f g
      (quotientRepresentativeMap_essSurj_of_exists_ordinary W R D f hf)
      (quotientRepresentativeMap_faithful_of_exists_ordinary W R D g hg)

/-- Close the actual associator/right-unitor/left-unitor endpoint overlap from
existence of suitable representatives. All three corrected equations and both
anchor-overlap agreements remain explicit hypotheses. -/
theorem associatorAnchor_unitor_overlapStar_triangle_of_exists_representatives
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : HasOrdinaryEssSurjRepresentative W R f)
    (hg : HasOrdinaryFaithfulRepresentative W R g)
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
      (quotientRepresentativeMap_essSurj_of_exists_ordinary W R D f hf)
      (quotientRepresentativeMap_faithful_of_exists_ordinary W R D g hg)
      Qs Qt Qu hQs hQt hQu hst hsu

/-!
## Boundary after v3.31

Semantic essential surjectivity and faithfulness are invariant under changing
to any quotient-equal path. Existence of an ordinary-letter certificate on one
representative is now sufficient for the actual selected representative map
and hence for the specific v3.28 mixed-triangle closure.

This does not prove that the certificate holds on every representative, that
it is necessary for the semantic property, or that every quotient morphism
has such a certificate. Failure of a certificate does not establish failure
of the semantic property or noninjectivity of double whiskering.

No globally compatible correction family, coherent family of evaluation
isomorphisms, general Stage-I factorization, or Stage-II universality is
constructed by this proposition-valued transport layer.
-/

end KUOS.DependentOriginationQuotientDirectionalPropertyTransportV3_31
