import KUOS.DependentOriginationULiftScaledHornProblemRoundTripV1_29
import KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30

/-!
# Canonical cross-universe scaled horn presentation descent

The exact inverse constructions and round-trip equalities identify all
scaled horn problems on the ULift of a source with the corresponding
problems on the original source. A chosen admissibility family is
transported, not replaced by an arbitrary target predicate.

For this *canonical* lifted family, admissibility, filler existence
and fibrancy are equivalent across independent universe levels. This
does not prove equivalence for an unrelated target family, and does
not assume any scaled-fibration theorem unconditionally.
-/

namespace KUOS.DependentOriginationCanonicalCrossUniverseHornDescentV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
open KUOS.DependentOriginationULiftScaledHornProblemDescentV1_29
open KUOS.DependentOriginationULiftScaledHornProblemRoundTripV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30

universe u v

/-- Precisely the upper-universe horn problems whose canonical unlift is
admissible for the original family; no independent choice is smuggled in. -/
def canonicalLiftedHornFamily
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX) :
    ScaledHornFamily
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) where
  admissible := fun {_ _} Q =>
    FX.admissible (unliftScaledHornProblem.{u, v} Q)

/-- The required E bridge for *independent* universe levels is a
constructible equivalence of actual horn presentations, provided the
upper family is precisely the canonically transported lower family. -/
noncomputable def canonicalCrossUniversePresentationEquivalence
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX) :
    ScaledHornPresentationEquivalence FX
      (canonicalLiftedHornFamily.{u, v} sX FX) where
  forward := fun P => liftScaledHornProblem.{u, v} P
  backward := fun Q => unliftScaledHornProblem.{u, v} Q
  forward_admissible := by
    intro n i P hP
    change FX.admissible
      (unliftScaledHornProblem.{u, v} (liftScaledHornProblem.{u, v} P))
    rw [unlift_liftScaledHornProblem.{u, v} P]
    exact hP
  backward_admissible := by
    intro n i Q hQ
    exact hQ
  forward_filler := by
    intro n i P hP
    exact liftScaledHornFiller_nonempty.{u, v} hP
  backward_filler := by
    intro n i Q hQ
    exact unliftScaledHornFiller_nonempty.{u, v} hQ
  forward_backward_filler_equiv := by
    intro n i Q
    rw [lift_unliftScaledHornProblem.{u, v} Q]
  backward_forward_filler_equiv := by
    intro n i P
    rw [unlift_liftScaledHornProblem.{u, v} P]

/-- Global horn-filler existence is exactly invariant under the genuinely
typed canonical independent-universe lift of an admissible family. -/
theorem canonicalCrossUniverseFibrancy_iff
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX) :
    HasScaledHornFillers X sX FX ↔
      HasScaledHornFillers ((SSet.uliftFunctor.{v, u}).obj X)
        (uliftScaling.{u, v} sX)
        (canonicalLiftedHornFamily.{u, v} sX FX) :=
  hasScaledHornFillers_iff
    (canonicalCrossUniversePresentationEquivalence.{u, v} sX FX)

#print axioms canonicalLiftedHornFamily
#print axioms canonicalCrossUniversePresentationEquivalence
#print axioms canonicalCrossUniverseFibrancy_iff

end KUOS.DependentOriginationCanonicalCrossUniverseHornDescentV1_29
