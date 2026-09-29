import KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72
import Mathlib

namespace KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
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

v4.71 shows that coherently equivalent raw systems have equivalent universal
DO₂ carriers.  v4.72 identifies exact source-morphism existence with the
compatible-liftability predicate.

The universal factorization field now closes the bridge between those two
statements.

Given exact-universal source objects X and Y and a coherent raw equivalence
E : X.raw <-> Y.raw, transport X's exact presentation along E.  It is an exact
presentation of Y.raw with the same DO₂ carrier X.carrier.  Since Y.presentation
is a coherent universal target, its factorization field supplies a coherent
comparison from that transported presentation into Y.presentation.  This is
exactly the compatible DO₂ lift required for E.forward.comparison.

The same argument for E.symm gives the backward leg.

Thus both legs of every coherent raw equivalence are actual morphisms of the
generalized exact-universal source.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The induced-DO₂ wrapper exposes the underlying coherent StrongTrans
without any transport or cast.  This projection theorem keeps later proofs
inside Lean 4.30's reducible simplification boundary. -/
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
exact-universal source objects. -/
theorem ExactUniversalRawMorphism.Liftable.forward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ExactUniversalRawMorphism.Liftable
      (W := W) A E.forward.comparison := by
  rcases
      Y.universal.factor
        (transportExactPresentation (W := W) A E X.presentation) with
    ⟨alpha⟩
  refine
    ⟨exactPresentationCoherentComparisonToCompletion2Hom
        (W := W) A alpha, ⟨?_⟩⟩
  simp only [
    exactPresentationCoherentComparisonToCompletion2Hom_hom,
    transportExactPresentation_comparison
  ]
  exact alpha.comparison_triangle

/-- The backward leg is likewise exactly liftable. -/
theorem ExactUniversalRawMorphism.Liftable.backward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ExactUniversalRawMorphism.Liftable
      (W := W) A E.backward.comparison := by
  simpa only [HigherRawSystemCoherentEquivalence.symm] using
    (ExactUniversalRawMorphism.Liftable.forward_of_rawCoherentEquivalence
      (W := W) A Y X E.symm)

/-- Therefore the forward leg is represented by an actual exact-universal
source 1-cell. -/
theorem exists_exactUniversalRawMorphism_forward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y,
      f.raw = E.forward.comparison := by
  exact
    (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
      (W := W) A E.forward.comparison).1
      (ExactUniversalRawMorphism.Liftable.forward_of_rawCoherentEquivalence
        (W := W) A X Y E)

/-- And the backward leg is represented by an actual source 1-cell in the
opposite direction. -/
theorem exists_exactUniversalRawMorphism_backward_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ∃ f : ExactUniversalRawMorphism (W := W) A Y X,
      f.raw = E.backward.comparison := by
  exact
    (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
      (W := W) A E.backward.comparison).1
      (ExactUniversalRawMorphism.Liftable.backward_of_rawCoherentEquivalence
        (W := W) A X Y E)

/-!
## Boundary after v4.73

Coherent raw equivalence is now represented at both levels:

* object level: the realized DO₂ carriers are bicategorically equivalent;
* morphism level: each forward/backward raw leg lifts to an actual source
  1-cell.

The remaining distinction is intentional.  The raw unit/counit of E have not
yet been promoted to invertible source 2-cells between the chosen lifted
composites and source identities.  Doing so requires essential uniqueness in
the relevant source-morphism fibers.  That is the next coherence step toward
lifting a coherent raw equivalence to a bicategorical equivalence in the
exact-universal source itself.
-/

end

end KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73
