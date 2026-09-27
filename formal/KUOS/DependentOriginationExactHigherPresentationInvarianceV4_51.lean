import KUOS.DependentOriginationExactHigherPresentationSectorV4_50
import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
import Mathlib

namespace KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Pointwise-equivalence invariance of the exact higher presentation sector v4.51

v4.50 identifies the exact higher dependent-origination positive sector with
raw higher contextual systems admitting a carrier in DO₂ together with a
pointwise-equivalence strong comparison

  restrict(X) --> R.

The next presentation-independence obligation is to show that this exact sector
is stable under the directed pointwise-equivalence comparisons introduced in
v2.17.

The proof is deliberately carrier-preserving.  Given an exact presentation of
R and a pointwise-equivalence comparison

  R --> S,

we keep the same localized stack carrier X and compose the two strong
transformations

  restrict(X) --> R --> S.

The componentwise equivalence proof is exactly the composition argument already
used by v2.17 for ordinary higher-localization factorizations.  No new geometric
carrier, refinement, or descent argument is required: stack descent is retained
because the DO₂ carrier itself is unchanged.

This is the Cat-valued higher analogue of the v4.49 presentation-invariance
step.  Since v2.17 comparisons are intentionally directed, one such comparison
gives forward closure.  If directed pointwise-equivalence comparisons are
available both ways, exact presentability is equivalent in both directions.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Transport an exact higher dependent-origination presentation along a
pointwise-equivalence comparison of raw higher contextual systems.

The DO₂ carrier is unchanged.  Only the comparison from its restriction to the
raw system is postcomposed with the supplied pointwise-equivalence comparison.
-/
noncomputable def exactPresentationOfPointwiseEquivalenceComparison
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (E : HigherPointwiseEquivalenceComparison R S) :
    ExactHigherDependentOriginationPresentation
      (W := W) A S where
  carrier := P.carrier
  comparison := P.comparison ≫ E.comparison
  comparison_isEquivalence := by
    intro X
    letI : (P.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      P.comparison_isEquivalence X
    letI : (E.comparison.app (.mk X)).toFunctor.IsEquivalence :=
      E.comparison_isEquivalence X
    change
      ((P.comparison.app (.mk X)).toFunctor ⋙
        (E.comparison.app (.mk X)).toFunctor).IsEquivalence
    infer_instance

/-- Pointwise-equivalence transport preserves the exact DO₂ carrier literally. -/
@[simp] theorem exactPresentationOfPointwiseEquivalenceComparison_carrier
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (E : HigherPointwiseEquivalenceComparison R S) :
    (exactPresentationOfPointwiseEquivalenceComparison
      (W := W) A P E).carrier =
      P.carrier :=
  rfl

/-- The transported comparison is literally the composite of the original
presentation comparison with the raw-system pointwise equivalence. -/
@[simp] theorem exactPresentationOfPointwiseEquivalenceComparison_comparison
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (E : HigherPointwiseEquivalenceComparison R S) :
    (exactPresentationOfPointwiseEquivalenceComparison
      (W := W) A P E).comparison =
      P.comparison ≫ E.comparison :=
  rfl

/-- Exact higher dependent-origination presentability is closed under a
directed pointwise-equivalence comparison. -/
theorem hasExactHigherDependentOriginationPresentation_of_pointwiseEquivalenceComparison
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (hR :
      HasExactHigherDependentOriginationPresentation
        (W := W) A R)
    (E : HigherPointwiseEquivalenceComparison R S) :
    HasExactHigherDependentOriginationPresentation
      (W := W) A S := by
  rcases hR with ⟨P⟩
  exact
    ⟨exactPresentationOfPointwiseEquivalenceComparison
      (W := W) A P E⟩

/-- With directed pointwise-equivalence comparisons in both directions, exact
higher dependent-origination presentability is presentation-invariant. -/
theorem hasExactHigherDependentOriginationPresentation_iff_of_pointwiseEquivalenceComparisons
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (ERS : HigherPointwiseEquivalenceComparison R S)
    (ESR : HigherPointwiseEquivalenceComparison S R) :
    HasExactHigherDependentOriginationPresentation
        (W := W) A R ↔
      HasExactHigherDependentOriginationPresentation
        (W := W) A S := by
  constructor
  · intro hR
    exact
      hasExactHigherDependentOriginationPresentation_of_pointwiseEquivalenceComparison
        (W := W) A hR ERS
  · intro hS
    exact
      hasExactHigherDependentOriginationPresentation_of_pointwiseEquivalenceComparison
        (W := W) A hS ESR

/-!
## Boundary after v4.51

The exact positive sector is now independent of a directed presentation change
in the precise sense supported by the existing v2.17 interface:

  exact DO₂ presentation of R
            +
  pointwise-equivalence comparison R --> S
            |
            v
  exact DO₂ presentation of S.

The localized stack carrier is preserved exactly; only its comparison to the
raw contextual system changes by strong-transformation composition.

This closes the first higher presentation-invariance obligation without adding
any new geometric hypothesis.  The next genuine step is comparison between two
exact presentations of the *same* raw system.  That stage must continue to
distinguish directed comparison data, pointwise equivalence, pseudonatural
equivalence, equivalence in DO₂, and uniqueness up to modification rather than
collapsing them prematurely.
-/

end

end KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51
