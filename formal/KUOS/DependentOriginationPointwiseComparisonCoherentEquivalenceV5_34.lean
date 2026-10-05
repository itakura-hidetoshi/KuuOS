import KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33
import KUOS.DependentOriginationPointwiseInverseCoherenceV4_82
import KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
import Mathlib

namespace KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationPointwiseInverseNaturalityV4_81
open KUOS.DependentOriginationPointwiseInverseCoherenceV4_82
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftabilityCriterionV5_18
open KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Pointwise comparison to coherent raw equivalence v5.34

v2.17 deliberately packaged a directed strong transformation whose components
are equivalences of categories without assuming inverse StrongTrans data.
v4.81-v4.82 later proved, for arbitrary Cat-valued pseudofunctors, that such a
strong transformation canonically yields:

* a pointwise inverse StrongTrans;
* an invertible unit modification
    identity ~= forward >> inverse.

The only missing field in v4.55's HigherRawSystemCoherentEquivalence is then a
counit

    inverse >> forward ~= identity.

This file constructs it without new componentwise coherence calculations.
Apply v4.82 once more to the inverse StrongTrans, obtaining its inverse e and a
second unit identity ~= inverse >> e. Bicategorical unitors, associativity, and
the first unit identify e with the original forward StrongTrans. Whiskering that
identification by inverse converts the second unit into the required counit.

Thus a single directed pointwise-equivalence comparison already contains enough
data to produce the two-sided coherent raw equivalence used by v4.55.

As a classification corollary, v5.33's label-preserving localized presentation
criterion strengthens from a directed comparison to a coherent raw equivalence.
This does not imply weak admissibility -> exact liftability and does not resize
an arbitrary refinement-atlas universe.
-/

universe u v uH vH uW uP
universe uB vB wB

/-! ## Generic bicategorical two-retraction algebra -/

section Bicategorical

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {R S : B}

/-- If c has a right inverse d up to isomorphism and d has a right inverse e,
then e is isomorphic to c. This is pure bicategorical algebra. -/
def alternatingRetractions_doubleInverseIso
    (c : R ⟶ S) (d : S ⟶ R) (e : R ⟶ S)
    (eta : 𝟙 R ≅ c ≫ d)
    (theta : 𝟙 S ≅ d ≫ e) :
    e ≅ c :=
  (Bicategory.leftUnitor e).symm ≪≫
    Bicategory.whiskerRightIso eta e ≪≫
      Bicategory.associator c d e ≪≫
        Bicategory.whiskerLeftIso c theta.symm ≪≫
          Bicategory.rightUnitor c

/-- The same alternating retractions supply the missing counit d >> c ~= id. -/
def alternatingRetractions_counit
    (c : R ⟶ S) (d : S ⟶ R) (e : R ⟶ S)
    (eta : 𝟙 R ≅ c ≫ d)
    (theta : 𝟙 S ≅ d ≫ e) :
    d ≫ c ≅ 𝟙 S :=
  (theta ≪≫
    Bicategory.whiskerLeftIso d
      (alternatingRetractions_doubleInverseIso c d e eta theta)).symm

end Bicategorical

/-! ## Upgrade a directed pointwise equivalence to coherent two-sided data -/

variable {Context : Type u} [Category.{v} Context]

/-- Adapt the Context-indexed pointwise-equivalence field to every object of the
actual raw base bicategory LocallyDiscrete Context. -/
theorem pointwiseComparisonComponentIsEquivalence
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S)
    (U : LocallyDiscrete Context) :
    (E.comparison.app U).toFunctor.IsEquivalence := by
  rcases U with ⟨U⟩
  exact E.comparison_isEquivalence U

/-- The v4.82 inverse StrongTrans associated to a directed pointwise
comparison. -/
abbrev pointwiseComparisonInverseStrongTrans
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    S ⟶ R :=
  KUOS.DependentOriginationPointwiseInverseCoherenceV4_82.pointwiseInverseStrongTrans
    E.comparison
    (pointwiseComparisonComponentIsEquivalence E)

/-- The chosen inverse StrongTrans is itself pointwise an equivalence. -/
theorem pointwiseComparisonInverseComponentIsEquivalence
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S)
    (U : LocallyDiscrete Context) :
    ((pointwiseComparisonInverseStrongTrans E).app U).toFunctor.IsEquivalence := by
  change
    (KUOS.DependentOriginationPointwiseInverseNaturalityV4_81.pointwiseInverseEquivalence
      E.comparison
      (pointwiseComparisonComponentIsEquivalence E)
      U).inverse.IsEquivalence
  exact CategoryTheory.Equivalence.isEquivalence_inverse _

/-- Package the chosen inverse StrongTrans as the directed pointwise comparison
in the reverse direction. -/
noncomputable def pointwiseComparisonInverseComparison
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    HigherPointwiseEquivalenceComparison S R where
  comparison :=
    pointwiseComparisonInverseStrongTrans E
  comparison_isEquivalence := by
    intro X
    exact
      pointwiseComparisonInverseComponentIsEquivalence
        E (.mk X)

/-- Apply v4.82 a second time to the inverse StrongTrans. -/
abbrev pointwiseComparisonDoubleInverseStrongTrans
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    R ⟶ S :=
  KUOS.DependentOriginationPointwiseInverseCoherenceV4_82.pointwiseInverseStrongTrans
    (pointwiseComparisonInverseStrongTrans E)
    (pointwiseComparisonInverseComponentIsEquivalence E)

/-- The double pointwise inverse is coherently isomorphic to the original
forward StrongTrans by alternating-retraction algebra. -/
noncomputable def pointwiseComparisonDoubleInverseIsoForward
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    pointwiseComparisonDoubleInverseStrongTrans E ≅
      E.comparison :=
  alternatingRetractions_doubleInverseIso
    E.comparison
    (pointwiseComparisonInverseStrongTrans E)
    (pointwiseComparisonDoubleInverseStrongTrans E)
    (KUOS.DependentOriginationPointwiseInverseCoherenceV4_82.pointwiseInverseUnitModification
      E.comparison
      (pointwiseComparisonComponentIsEquivalence E))
    (KUOS.DependentOriginationPointwiseInverseCoherenceV4_82.pointwiseInverseUnitModification
      (pointwiseComparisonInverseStrongTrans E)
      (pointwiseComparisonInverseComponentIsEquivalence E))

/-- The missing counit for the original directed comparison. -/
noncomputable def pointwiseComparisonInverseCounit
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    pointwiseComparisonInverseStrongTrans E ≫
        E.comparison ≅
      𝟙 S :=
  alternatingRetractions_counit
    E.comparison
    (pointwiseComparisonInverseStrongTrans E)
    (pointwiseComparisonDoubleInverseStrongTrans E)
    (KUOS.DependentOriginationPointwiseInverseCoherenceV4_82.pointwiseInverseUnitModification
      E.comparison
      (pointwiseComparisonComponentIsEquivalence E))
    (KUOS.DependentOriginationPointwiseInverseCoherenceV4_82.pointwiseInverseUnitModification
      (pointwiseComparisonInverseStrongTrans E)
      (pointwiseComparisonInverseComponentIsEquivalence E))

/-- Main v5.34 theorem: a single directed pointwise-equivalence comparison
canonically yields the two-sided coherent raw-equivalence data required by
v4.55. -/
noncomputable def pointwiseComparisonToCoherentEquivalence
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    HigherRawSystemCoherentEquivalence R S where
  forward := E
  backward :=
    pointwiseComparisonInverseComparison E
  unit := by
    change
      𝟙 R ≅
        E.comparison ≫
          pointwiseComparisonInverseStrongTrans E
    exact
      KUOS.DependentOriginationPointwiseInverseCoherenceV4_82.pointwiseInverseUnitModification
        E.comparison
        (pointwiseComparisonComponentIsEquivalence E)
  counit := by
    change
      pointwiseComparisonInverseStrongTrans E ≫
          E.comparison ≅
        𝟙 S
    exact
      pointwiseComparisonInverseCounit E

@[simp] theorem pointwiseComparisonToCoherentEquivalence_forward
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    (pointwiseComparisonToCoherentEquivalence E).forward =
      E :=
  rfl

@[simp] theorem pointwiseComparisonToCoherentEquivalence_backward_comparison
    {R S :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (E : HigherPointwiseEquivalenceComparison R S) :
    (pointwiseComparisonToCoherentEquivalence E).backward.comparison =
      pointwiseComparisonInverseStrongTrans E :=
  rfl

/-! ## Coherent strengthening of the v5.33 classification criterion -/

variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Label-preserving localized classification presentation with a genuine
two-sided coherent raw equivalence from the restricted carrier to the raw
system. -/
def HasLabelPreservingLocalizedClassificationCoherentPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) : Prop :=
  ∃ Z :
      LocalizedClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
    Z.label = label ∧
      Nonempty
        (HigherRawSystemCoherentEquivalence
          (KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.localizedClassificationRestrictedCarrier
            (W := W) A Z)
          R)

/-- Under the aligned-atlas specialization, exact liftability is equivalent to
existence of a label-preserving localized presentation whose restricted carrier
is coherently raw-equivalent to the original system. -/
theorem exactLiftabilityCriterion_iff_labelPreservingLocalizedCoherentPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (label : ClassificationLabel WorldLabel PresentationLabel)
    (R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)) :
    ExactLiftabilityCriterion (W := W) A R ↔
      HasLabelPreservingLocalizedClassificationCoherentPresentation
        (W := W) A label R := by
  constructor
  · intro hExact
    have hPresentation :
        KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.HasLabelPreservingLocalizedClassificationPresentation
          (W := W) A label R :=
      (KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
        (W := W) A label R).1 hExact
    rcases hPresentation with ⟨Z, hLabel, ⟨E⟩⟩
    exact ⟨Z, hLabel, ⟨pointwiseComparisonToCoherentEquivalence E⟩⟩
  · rintro ⟨Z, hLabel, ⟨E⟩⟩
    have hPresentation :
        KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.HasLabelPreservingLocalizedClassificationPresentation
          (W := W) A label R := by
      exact ⟨Z, hLabel, ⟨E.forward⟩⟩
    exact
      (KUOS.DependentOriginationLocalizedClassificationPresentationCriterionV5_33.exactLiftabilityCriterion_iff_labelPreservingLocalizedPresentation
        (W := W) A label R).2 hPresentation

/-- Exact-liftable classification objects therefore admit a label-preserving
localized presentation coherently equivalent to their raw system. -/
theorem ExactLiftableClassificationObject.exists_labelPreserving_localizedCoherentPresentation
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    HasLabelPreservingLocalizedClassificationCoherentPresentation
      (W := W) A X.label X.raw := by
  exact
    (exactLiftabilityCriterion_iff_labelPreservingLocalizedCoherentPresentation
      (W := W) A X.label X.raw).1
      (KUOS.DependentOriginationExactLiftabilityCriterionV5_18.ExactLiftableClassificationObject.satisfiesExactLiftabilityCriterion
        (W := W) A X)

/-!
## Boundary after v5.34

The former pointwise-versus-coherent gap is closed for the actual v2.17 notion:

  HigherPointwiseEquivalenceComparison R S
      ->
  HigherRawSystemCoherentEquivalence R S.

Therefore the directed comparison produced by exact-presentation and
classification factorization theorems is sufficient for every downstream
v4.55/v5.20 theorem that asks only for HigherRawSystemCoherentEquivalence.

Still unchanged:

* weak admissibility does not imply exact liftability;
* arbitrary atlas-index universe resizing is not proved;
* arbitrary raw morphisms need not be equivalences and still require the
  mapping-property morphism machinery rather than this theorem.
-/

#print axioms pointwiseComparisonToCoherentEquivalence
#print axioms exactLiftabilityCriterion_iff_labelPreservingLocalizedCoherentPresentation
#print axioms ExactLiftableClassificationObject.exists_labelPreserving_localizedCoherentPresentation

end

end KUOS.DependentOriginationPointwiseComparisonCoherentEquivalenceV5_34
