import KUOS.DependentOriginationCertifiedQuotientSectorClosureV3_32

namespace KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33

open CategoryTheory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28
open KUOS.DependentOriginationQuotientDirectionalPropertyTransportV3_31

universe u v uH vH

set_option autoImplicit false

/-!
# Quotient split directional separation v3.33

v3.32 proves the multiplicative algebra of existence of certified words.
This layer works with the semantic properties of the evaluated functors
instead. The existing v2.61 identity and composition isomorphism-existence
lemmas transfer those properties without constructing a coherent quotient
pseudofunctor.

The directions of reflection are essential:

* essential surjectivity of the evaluation of `f ≫ g` implies essential
  surjectivity of the evaluation of `g`;
* faithfulness of the evaluation of `f ≫ g` implies faithfulness of the
  evaluation of `f`.

Consequently a section `s ≫ f = 𝟙` makes the left evaluation essentially
surjective, and a retraction `g ≫ r = 𝟙` makes the right evaluation faithful.
These quotient equations supply a further sufficient separation criterion,
without imposing letterwise certificates on any selected representatives.

All isomorphism witnesses are eliminated locally into propositions. No
simultaneous coherent isomorphism family is selected here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- An identity quotient arrow evaluates to an essentially-surjective functor. -/
theorem quotientRepresentativeMap_id_essSurj (X : W.Localization) :
    (quotientRepresentativeMap W R D (𝟙 X)).toFunctor.EssSurj := by
  rcases quotientIdentity_hasMapIso W R D X with ⟨e⟩
  exact Functor.essSurj_of_iso (Cat.Hom.toNatIso e).symm

/-- An identity quotient arrow evaluates to a faithful functor. -/
theorem quotientRepresentativeMap_id_faithful (X : W.Localization) :
    (quotientRepresentativeMap W R D (𝟙 X)).toFunctor.Faithful := by
  rcases quotientIdentity_hasMapIso W R D X with ⟨e⟩
  exact Functor.Faithful.of_iso (Cat.Hom.toNatIso e).symm

/-- Semantic essential surjectivity of a quotient composite is exactly that
of the composite of its two evaluated functors. -/
theorem quotientRepresentativeMap_comp_essSurj_iff
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.EssSurj ↔
      ((quotientRepresentativeMap W R D f).toFunctor ⋙
        (quotientRepresentativeMap W R D g).toFunctor).EssSurj := by
  rcases quotientComposition_hasMapIso W R D f g with ⟨e⟩
  have eNat := Cat.Hom.toNatIso e
  constructor
  · intro h
    letI : (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.EssSurj := h
    exact Functor.essSurj_of_iso eNat
  · intro h
    letI : ((quotientRepresentativeMap W R D f).toFunctor ⋙
      (quotientRepresentativeMap W R D g).toFunctor).EssSurj := h
    exact Functor.essSurj_of_iso eNat.symm

/-- Semantic faithfulness is transported through the same local composition
isomorphism, without imposing any associativity equation on the choices. -/
theorem quotientRepresentativeMap_comp_faithful_iff
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.Faithful ↔
      ((quotientRepresentativeMap W R D f).toFunctor ⋙
        (quotientRepresentativeMap W R D g).toFunctor).Faithful := by
  rcases quotientComposition_hasMapIso W R D f g with ⟨e⟩
  have eNat := Cat.Hom.toNatIso e
  constructor
  · intro h
    letI : (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.Faithful := h
    exact Functor.Faithful.of_iso eNat
  · intro h
    letI : ((quotientRepresentativeMap W R D f).toFunctor ⋙
      (quotientRepresentativeMap W R D g).toFunctor).Faithful := h
    exact Functor.Faithful.of_iso eNat.symm

/-- Essential surjectivity of both evaluations propagates to a quotient
composite. Pass the two existing proofs directly to the Mathlib instance. -/
theorem quotientRepresentativeMap_comp_essSurj
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : (quotientRepresentativeMap W R D f).toFunctor.EssSurj)
    (hg : (quotientRepresentativeMap W R D g).toFunctor.EssSurj) :
    (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.EssSurj := by
  exact (quotientRepresentativeMap_comp_essSurj_iff W R D f g).2
    (@Functor.essSurj_comp _ _ _ _ _ _
      (quotientRepresentativeMap W R D f).toFunctor
      (quotientRepresentativeMap W R D g).toFunctor hf hg)

/-- Faithfulness of both evaluations propagates to a quotient composite. -/
theorem quotientRepresentativeMap_comp_faithful
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : (quotientRepresentativeMap W R D f).toFunctor.Faithful)
    (hg : (quotientRepresentativeMap W R D g).toFunctor.Faithful) :
    (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.Faithful := by
  exact (quotientRepresentativeMap_comp_faithful_iff W R D f g).2
    (@Functor.Faithful.comp _ _ _ _ _ _
      (quotientRepresentativeMap W R D f).toFunctor
      (quotientRepresentativeMap W R D g).toFunctor hf hg)

/-- Essential surjectivity reflects to the right factor only. An object
witness for the composite supplies a witness in the intermediate category. -/
theorem quotientRepresentativeMap_essSurj_right_of_comp
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hfg : (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.EssSurj) :
    (quotientRepresentativeMap W R D g).toFunctor.EssSurj := by
  have hComp := (quotientRepresentativeMap_comp_essSurj_iff W R D f g).1 hfg
  refine ⟨?_⟩
  intro B
  rcases @Functor.EssSurj.mem_essImage _ _ _ _
      ((quotientRepresentativeMap W R D f).toFunctor ⋙
        (quotientRepresentativeMap W R D g).toFunctor) hComp B with ⟨A, hA⟩
  exact ⟨(quotientRepresentativeMap W R D f).toFunctor.obj A, hA⟩

/-- Faithfulness reflects to the left factor only, by Mathlib's functor
cancellation lemma. No faithfulness of the right factor is assumed. -/
theorem quotientRepresentativeMap_faithful_left_of_comp
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hfg : (quotientRepresentativeMap W R D (f ≫ g)).toFunctor.Faithful) :
    (quotientRepresentativeMap W R D f).toFunctor.Faithful := by
  exact @Functor.Faithful.of_comp _ _ _ _ _ _
    (quotientRepresentativeMap W R D f).toFunctor
    (quotientRepresentativeMap W R D g).toFunctor
    ((quotientRepresentativeMap_comp_faithful_iff W R D f g).1 hfg)

/-- The semantic EssSurj property is declared with the complete
`MorphismProperty` family type, rather than a partially applied predicate. -/
def quotientEssSurjSector : MorphismProperty W.Localization :=
  fun _ _ f => (quotientRepresentativeMap W R D f).toFunctor.EssSurj

/-- The semantic Faithful property on quotient arrows. -/
def quotientFaithfulSector : MorphismProperty W.Localization :=
  fun _ _ f => (quotientRepresentativeMap W R D f).toFunctor.Faithful

instance quotientEssSurjSector_isMultiplicative :
    (quotientEssSurjSector W R D).IsMultiplicative where
  id_mem X := quotientRepresentativeMap_id_essSurj W R D X
  comp_mem f g hf hg := quotientRepresentativeMap_comp_essSurj W R D f g hf hg

instance quotientFaithfulSector_isMultiplicative :
    (quotientFaithfulSector W R D).IsMultiplicative where
  id_mem X := quotientRepresentativeMap_id_faithful W R D X
  comp_mem f g hf hg := quotientRepresentativeMap_comp_faithful W R D f g hf hg

/-- The v3.31/v3.32 certified EssSurj sector lies in the semantic sector.
The explicit endpoint abstraction preserves the whole dependent family. -/
theorem certifiedEssSurj_le_quotientEssSurjSector :
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryEssSurjRepresentative W R f) : MorphismProperty W.Localization) ≤
        quotientEssSurjSector W R D := by
  intro X Y f hf
  exact quotientRepresentativeMap_essSurj_of_exists_ordinary W R D f hf

/-- The analogous containment for the certified Faithful sector. -/
theorem certifiedFaithful_le_quotientFaithfulSector :
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryFaithfulRepresentative W R f) : MorphismProperty W.Localization) ≤
        quotientFaithfulSector W R D := by
  intro X Y f hf
  exact quotientRepresentativeMap_faithful_of_exists_ordinary W R D f hf

/-- A section in the actual quotient makes the evaluation of `f` essentially
surjective. Neither `f` nor its section needs a word certificate. -/
theorem quotientRepresentativeMap_essSurj_of_section
    {X Y : W.Localization} (f : X ⟶ Y) (s : Y ⟶ X)
    (hs : s ≫ f = 𝟙 Y) :
    (quotientRepresentativeMap W R D f).toFunctor.EssSurj := by
  apply quotientRepresentativeMap_essSurj_right_of_comp W R D s f
  rw [hs]
  exact quotientRepresentativeMap_id_essSurj W R D Y

/-- A retraction in the actual quotient makes the evaluation of `g` faithful.
The direction is `g ≫ r = 𝟙`, not the split-epimorphism direction. -/
theorem quotientRepresentativeMap_faithful_of_retraction
    {Y Z : W.Localization} (g : Y ⟶ Z) (r : Z ⟶ Y)
    (hr : g ≫ r = 𝟙 Y) :
    (quotientRepresentativeMap W R D g).toFunctor.Faithful := by
  apply quotientRepresentativeMap_faithful_left_of_comp W R D g r
  rw [hr]
  exact quotientRepresentativeMap_id_faithful W R D Y

/-- Split epimorphisms on the left and split monomorphisms on the right give
separation without requiring equivalences or certified words. -/
theorem middleIdentityWhiskerSeparating_of_section_retraction
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (s : Y ⟶ X) (r : Z ⟶ Y)
    (hs : s ≫ f = 𝟙 Y) (hr : g ≫ r = 𝟙 Y) :
    MiddleIdentityWhiskerSeparating W R D f g := by
  exact middleIdentityWhiskerSeparating_of_essSurj_faithful W R D f g
    (quotientRepresentativeMap_essSurj_of_section W R D f s hs)
    (quotientRepresentativeMap_faithful_of_retraction W R D g r hr)

/-- The actual mixed incidence triangle closes under the split criterion.
All three corrected equations and both anchor agreements remain hypotheses. -/
theorem associatorAnchor_unitor_overlapStar_triangle_of_section_retraction
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (s : Y ⟶ X) (r : Z ⟶ Y)
    (hs : s ≫ f = 𝟙 Y) (hr : g ≫ r = 𝟙 Y)
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs : Qs ∈ quotientRouteCorrectionLocus W R D
      (.associator f (𝟙 Y) g))
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D (.rightUnitor f))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D (.leftUnitor g))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.rightUnitor f) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.associator f (𝟙 Y) g) (.leftUnitor g) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor f) (.leftUnitor g) Qt Qu := by
  exact associatorAnchor_unitor_overlapStar_triangle_of_essSurj_faithful
    W R D f g
    (quotientRepresentativeMap_essSurj_of_section W R D f s hs)
    (quotientRepresentativeMap_faithful_of_retraction W R D g r hr)
    Qs Qt Qu hQs hQt hQu hst hsu

/-!
## Boundary after v3.33

The semantic sectors are multiplicative and contain the certified sectors.
The split criterion requires explicit one-sided inverse equations in the
actual quotient, not a letterwise condition. No strictness or equality of
certificate and semantic sectors is asserted.

Reflection from a composite is directional: right for EssSurj and left for
Faithful. This does not reflect either property to every factor or letter,
nor assert inverse closure of the certified sectors. Failure of these
sufficient conditions is not a noninjectivity witness.

The endpoint-overlap theorem still requires the same three correcting gauges
and two anchor agreements. No globally compatible correction family, coherent
selection of isomorphisms, general Stage-I factorization, or Stage-II
universality follows merely from these semantic transport propositions.
-/

end KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33
