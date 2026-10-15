import KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72
import Mathlib

namespace KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Lift coherent raw-equivalence legs into the exact source v4.73

Transport the presentation of X along a coherent raw equivalence E to obtain
an exact presentation of Y.raw with the same carrier X.carrier. The factor
field of Y.universal supplies a coherent comparison into Y.presentation.
Its stored comparison triangle is exactly the square required to lift the
forward raw leg. Applying this construction to E.symm lifts the backward leg.

The chosen source-object indices are explicit throughout. No inverse source
2-cell is inferred merely from the existence of these two source 1-cells.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The induced-DO₂ wrapper exposes the underlying coherent StrongTrans. -/
@[simp] theorem exactPresentationCoherentComparisonToCompletion2Hom_hom
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (alpha : ExactPresentationCoherentComparison (W := W) A P Q) :
    (exactPresentationCoherentComparisonToCompletion2Hom
      (W := W) A alpha).hom = alpha.hom :=
  rfl

/-- The forward leg of a coherent raw equivalence is exactly liftable between
the chosen exact-universal source objects. -/
theorem ExactUniversalRawMorphism.Liftable.forward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ExactUniversalRawMorphism.Liftable
      (W := W) A (X := X) (Y := Y) E.forward.comparison := by
  rcases
      Y.universal.factor
        (transportExactPresentation (W := W) A E X.presentation) with ⟨alpha⟩
  exact
    ⟨exactPresentationCoherentComparisonToCompletion2Hom
      (W := W) A alpha, ⟨alpha.comparison_triangle⟩⟩

/-- The backward leg is exactly liftable with the source and target reversed. -/
theorem ExactUniversalRawMorphism.Liftable.backward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ExactUniversalRawMorphism.Liftable
      (W := W) A (X := Y) (Y := X) E.backward.comparison :=
  ExactUniversalRawMorphism.Liftable.forward_of_rawCoherentEquivalence
    (W := W) A Y X E.symm

/-- The forward leg is represented by an actual exact-universal source 1-cell. -/
theorem exists_exactUniversalRawMorphism_forward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y,
      f.raw = E.forward.comparison :=
  (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
    (W := W) A (X := X) (Y := Y) E.forward.comparison).1
    (ExactUniversalRawMorphism.Liftable.forward_of_rawCoherentEquivalence
      (W := W) A X Y E)

/-- The backward leg is represented by an actual source 1-cell in the opposite
direction. -/
theorem exists_exactUniversalRawMorphism_backward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ∃ f : ExactUniversalRawMorphism (W := W) A Y X,
      f.raw = E.backward.comparison :=
  (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
    (W := W) A (X := Y) (Y := X) E.backward.comparison).1
    (ExactUniversalRawMorphism.Liftable.backward_of_rawCoherentEquivalence
      (W := W) A X Y E)

/-!
## Boundary after v4.73

Both legs of a coherent raw equivalence lift to source 1-cells. The realized
objects are also equivalent by v4.71. These are distinct statements.

The raw unit and counit have not been promoted to compatible invertible source
2-cells. Their compatibility with the chosen DO₂ modifications remains a
separate obligation before claiming an equivalence in the source bicategory.
-/

end

end KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73
