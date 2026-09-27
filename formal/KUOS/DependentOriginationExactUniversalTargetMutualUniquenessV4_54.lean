import KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
import KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
import Mathlib

namespace KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54

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
# Mutual essential uniqueness for exact universal targets v4.54

v4.53 proves that a coherent exact universal target receives a coherent
comparison from every exact presentation, and that any two such incoming
comparisons are isomorphic by an invertible modification.

For two exact coherent universal targets Q₁ and Q₂ of the same raw higher
contextual system R, these hypotheses immediately give coherent comparisons

  Q₁ --> Q₂
  Q₂ --> Q₁.

Applying essential uniqueness at Q₁ and Q₂ then identifies both composites with
the corresponding coherent identity comparisons:

  Q₁ --> Q₂ --> Q₁  ≅  id_{Q₁},
  Q₂ --> Q₁ --> Q₂  ≅  id_{Q₂}.

This is the exact object-level mutual-uniqueness datum available before
naturality in the raw system R has been formalized.

In particular, this file intentionally does NOT package the data as a
Bicategory.Equivalence in DO₂.  The repository roadmap requires naturality in R
to be formalized before that equivalence-level conclusion is asserted.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Two exact coherent universal targets admit coherent comparison data in both
directions, with both composites modification-isomorphic to the corresponding
coherent identities. -/
structure ExactUniversalTargetMutualCoherentUniqueness
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (Q₁ Q₂ : ExactHigherDependentOriginationPresentation
      (W := W) A R) where
  forward :
    ExactPresentationCoherentComparison (W := W) A Q₁ Q₂
  backward :
    ExactPresentationCoherentComparison (W := W) A Q₂ Q₁
  left_identity :
    (exactPresentationCoherentComparisonComp
      (W := W) A forward backward).hom ≅
      (exactPresentationCoherentComparisonId
        (W := W) A Q₁).hom
  right_identity :
    (exactPresentationCoherentComparisonComp
      (W := W) A backward forward).hom ≅
      (exactPresentationCoherentComparisonId
        (W := W) A Q₂).hom

/-- Any two exact coherent universal targets carry mutual coherent uniqueness
data. -/
theorem hasMutualCoherentUniqueness_of_universalTargets
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {Q₁ Q₂ : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (T₁ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₁)
    (T₂ : ExactPresentationCoherentUniversalTarget
      (W := W) A Q₂) :
    Nonempty
      (ExactUniversalTargetMutualCoherentUniqueness
        (W := W) A Q₁ Q₂) := by
  rcases T₂.factor Q₁ with ⟨forward⟩
  rcases T₁.factor Q₂ with ⟨backward⟩
  rcases T₁.essential_unique Q₁
      (exactPresentationCoherentComparisonComp
        (W := W) A forward backward)
      (exactPresentationCoherentComparisonId
        (W := W) A Q₁) with ⟨left_identity⟩
  rcases T₂.essential_unique Q₂
      (exactPresentationCoherentComparisonComp
        (W := W) A backward forward)
      (exactPresentationCoherentComparisonId
        (W := W) A Q₂) with ⟨right_identity⟩
  exact
    ⟨{
      forward := forward
      backward := backward
      left_identity := left_identity
      right_identity := right_identity
    }⟩

/-- Specialized mutual uniqueness for exact presentations obtained from two
coherent weak higher-localization universal properties whose chosen lifts are
stacks. -/
theorem coherentUniversalPresentations_haveMutualCoherentUniqueness
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U₁ U₂ : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack₁ :
      IsHigherGrothendieckDescentComplete W A U₁.chosen.lift)
    (hStack₂ :
      IsHigherGrothendieckDescentComplete W A U₂.chosen.lift) :
    Nonempty
      (ExactUniversalTargetMutualCoherentUniqueness
        (W := W) A
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U₁ hStack₁)
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U₂ hStack₂)) := by
  exact
    hasMutualCoherentUniqueness_of_universalTargets
      (W := W) A
      (exactPresentationCoherentUniversalTargetOfCoherentUniversalProperty
        (W := W) A U₁ hStack₁)
      (exactPresentationCoherentUniversalTargetOfCoherentUniversalProperty
        (W := W) A U₂ hStack₂)

/-!
## Boundary after v4.54

For fixed R, any two exact coherent universal targets are now mutually coherent
and their two composites are modification-isomorphic to identity.

This closes the fixed-object essential-uniqueness layer without crossing the
roadmap boundary.

The next obligation is naturality in the raw higher contextual system R.
Only after that layer is formalized should the mutual data above be promoted to
an equivalence statement inside DO₂.
-/

end

end KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54
