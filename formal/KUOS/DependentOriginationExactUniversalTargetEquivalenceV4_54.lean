import KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
import KUOS.DependentOriginationHigherStackCarrierV2_9
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic
import Mathlib.CategoryTheory.Bicategory.InducedBicategory
import Mathlib

namespace KUOS.DependentOriginationExactUniversalTargetEquivalenceV4_54

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Exact universal targets are equivalent in DO₂ v4.54

v4.53 isolates the correct universal-target interface inside the exact
presentation sector.  If Q₁ and Q₂ are both coherent universal targets for the
same raw higher contextual system R, then each receives a coherent comparison
from every exact presentation.  In particular we obtain

  Q₁ --> Q₂
  Q₂ --> Q₁.

Essential uniqueness at Q₁ identifies the composite Q₁ --> Q₂ --> Q₁ with the
coherent identity comparison on Q₁, and essential uniqueness at Q₂ does the
same for the opposite composite.

Because DO₂ is Mathlib's full induced bicategory on stack objects, the
underlying StrongTrans 1-cells and invertible modifications lift directly to
DO₂.  Mathlib's Bicategory.Equivalence.mkOfAdjointifyCounit then adjointifies
the counit and produces an actual bicategorical adjoint equivalence

  Q₁.carrier ≌ Q₂.carrier

inside DO₂.

Thus the chosen exact universal object is no longer merely essentially unique
at the StrongTrans level: any two exact coherent universal targets represent
bicategorically equivalent objects of the dependent-origination completion.

No claim is made that arbitrary exact presentations are equivalent.  The
universal-target hypotheses on both sides are essential.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Two exact coherent universal targets admit coherent comparisons in both
directions. -/
theorem hasBidirectionalCoherentComparison_of_universalTargets
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {Q₁ Q₂ : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (T₁ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₁)
    (T₂ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₂) :
    Nonempty
      ((ExactPresentationCoherentComparison (W := W) A Q₁ Q₂) ×
        (ExactPresentationCoherentComparison (W := W) A Q₂ Q₁)) := by
  rcases T₂.factor Q₁ with ⟨forward⟩
  rcases T₁.factor Q₂ with ⟨backward⟩
  exact ⟨(forward, backward)⟩

/-- The two composites of the mutual coherent comparisons supplied by two
universal targets are modification-isomorphic to the corresponding coherent
identity comparisons. -/
theorem hasTwoSidedIdentityIsos_of_universalTargets
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {Q₁ Q₂ : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (T₁ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₁)
    (T₂ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₂) :
    ∃
      (forward : ExactPresentationCoherentComparison (W := W) A Q₁ Q₂)
      (backward : ExactPresentationCoherentComparison (W := W) A Q₂ Q₁),
      Nonempty
        ((exactPresentationCoherentComparisonComp
            (W := W) A forward backward).hom ≅
          (exactPresentationCoherentComparisonId
            (W := W) A Q₁).hom) ∧
      Nonempty
        ((exactPresentationCoherentComparisonComp
            (W := W) A backward forward).hom ≅
          (exactPresentationCoherentComparisonId
            (W := W) A Q₂).hom) := by
  rcases T₂.factor Q₁ with ⟨forward⟩
  rcases T₁.factor Q₂ with ⟨backward⟩
  exact
    ⟨forward, backward,
      T₁.essential_unique Q₁
        (exactPresentationCoherentComparisonComp
          (W := W) A forward backward)
        (exactPresentationCoherentComparisonId
          (W := W) A Q₁),
      T₂.essential_unique Q₂
        (exactPresentationCoherentComparisonComp
          (W := W) A backward forward)
        (exactPresentationCoherentComparisonId
          (W := W) A Q₂)⟩

/-- Any two exact coherent universal targets are adjoint equivalent objects of
the actual DO₂ carrier.

This theorem uses only:
* factor existence from each universal target;
* essential uniqueness up to invertible modification;
* fullness of Mathlib's induced bicategory;
* Mathlib's adjointification constructor.
-/
theorem hasCompletion2AdjointEquivalence_of_universalTargets
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {Q₁ Q₂ : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (T₁ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₁)
    (T₂ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₂) :
    Nonempty (Bicategory.Equivalence Q₁.carrier Q₂.carrier) := by
  rcases T₂.factor Q₁ with ⟨forward⟩
  rcases T₁.factor Q₂ with ⟨backward⟩

  let composite₁ :
      ExactPresentationCoherentComparison (W := W) A Q₁ Q₁ :=
    exactPresentationCoherentComparisonComp
      (W := W) A forward backward
  let identity₁ :
      ExactPresentationCoherentComparison (W := W) A Q₁ Q₁ :=
    exactPresentationCoherentComparisonId (W := W) A Q₁
  rcases T₁.essential_unique Q₁ composite₁ identity₁ with ⟨e₁⟩

  let composite₂ :
      ExactPresentationCoherentComparison (W := W) A Q₂ Q₂ :=
    exactPresentationCoherentComparisonComp
      (W := W) A backward forward
  let identity₂ :
      ExactPresentationCoherentComparison (W := W) A Q₂ Q₂ :=
    exactPresentationCoherentComparisonId (W := W) A Q₂
  rcases T₂.essential_unique Q₂ composite₂ identity₂ with ⟨e₂⟩

  have h₁ :
      forward.hom ≫ backward.hom ≅
        𝟙 (higherStackObjectVal (W := W) A Q₁.carrier) := by
    simpa [composite₁, identity₁] using e₁
  have h₂ :
      backward.hom ≫ forward.hom ≅
        𝟙 (higherStackObjectVal (W := W) A Q₂.carrier) := by
    simpa [composite₂, identity₂] using e₂

  let f : Q₁.carrier ⟶ Q₂.carrier :=
    exactPresentationCoherentComparisonToCompletion2Hom
      (W := W) A forward
  let g : Q₂.carrier ⟶ Q₁.carrier :=
    exactPresentationCoherentComparisonToCompletion2Hom
      (W := W) A backward

  have unit : 𝟙 Q₁.carrier ≅ f ≫ g := by
    apply CategoryTheory.Bicategory.InducedBicategory.isoMk
    change
      𝟙 (higherStackObjectVal (W := W) A Q₁.carrier) ≅
        forward.hom ≫ backward.hom
    exact h₁.symm

  have counit : g ≫ f ≅ 𝟙 Q₂.carrier := by
    apply CategoryTheory.Bicategory.InducedBicategory.isoMk
    change
      backward.hom ≫ forward.hom ≅
        𝟙 (higherStackObjectVal (W := W) A Q₂.carrier)
    exact h₂

  exact ⟨Bicategory.Equivalence.mkOfAdjointifyCounit unit counit⟩

/-- Specialized existence theorem for exact presentations obtained from two
coherent weak higher-localization universal properties whose chosen lifts are
stacks. -/
theorem coherentUniversalPresentations_areCompletion2Equivalent
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U₁ U₂ : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack₁ :
      IsHigherGrothendieckDescentComplete W A U₁.chosen.lift)
    (hStack₂ :
      IsHigherGrothendieckDescentComplete W A U₂.chosen.lift) :
    Nonempty
      (Bicategory.Equivalence
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U₁ hStack₁).carrier
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U₂ hStack₂).carrier) := by
  exact
    hasCompletion2AdjointEquivalence_of_universalTargets
      (W := W) A
      (exactPresentationCoherentUniversalTargetOfCoherentUniversalProperty
        (W := W) A U₁ hStack₁)
      (exactPresentationCoherentUniversalTargetOfCoherentUniversalProperty
        (W := W) A U₂ hStack₂)

/-!
## Boundary after v4.54

For the exact coherent universal sector, essential uniqueness is now upgraded to
actual bicategorical equivalence inside DO₂.

The next remaining universality tasks are therefore not object-level uniqueness.
They are:

* naturality of the chosen exact universal presentation in the raw system R;
* identifying the correct admissible source bicategory/category of raw systems;
* constructing the final mapping-property equivalence into DO₂;
* deriving the coherent localization universal property from the intended
  admissibility hypotheses rather than assuming it as input.
-/

end

end KUOS.DependentOriginationExactUniversalTargetEquivalenceV4_54
