import KUOS.DependentOriginationULiftScaledHornProblemDescentV1_29

/-!
# Exact round-trip of genuine cross-universe scaled horn problems

The actual horn/scaling/vertex-index data are returned by both
unlift(lift P) and lift(unlift Q). This follows from the separately
kernel-certified round trips of the two scaling structures and
the fully faithful equivalences of the horn map. The remaining
proof-only fields are propositionally proof-irrelevant.

No arbitrary admissibility-family equivalence is asserted in this file.
-/

namespace KUOS.DependentOriginationULiftScaledHornProblemRoundTripV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationULiftHornMapEquivalenceV1_29
open KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29
open KUOS.DependentOriginationULiftHornExtensionReflectionV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
open KUOS.DependentOriginationULiftScalingDescentV1_29
open KUOS.DependentOriginationULiftScalingRoundTripV1_29
open KUOS.DependentOriginationULiftScaledHornProblemDescentV1_29

universe u v

/-- The complete lower-universe scaled horn problem is recovered after
a canonical cross-universe lift followed by descent. -/
theorem unlift_liftScaledHornProblem
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    unliftScaledHornProblem.{u, v} (liftScaledHornProblem.{u, v} P) = P := by
  cases P with
  | mk hornS simplexS inclusion hornMap scaled =>
    have hm :
        unliftHornMap.{u, v} n i
          (liftHornMap.{u, v} n i hornMap) = hornMap := by
      rw [← hornMapUniverseEquiv_apply]
      exact unliftHornMap_equiv_lift.{u, v} n i hornMap
    simp only [unliftScaledHornProblem, liftScaledHornProblem,
      unlift_liftHornScaling, unlift_liftSimplexScaling, hm]
    rfl

/-- An arbitrary scaled horn problem on a genuinely lifted target is
recovered after descent and re-lifting, with no loss of thinness. -/
theorem lift_unliftScaledHornProblem
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) n i) :
    liftScaledHornProblem.{u, v} (unliftScaledHornProblem.{u, v} Q) = Q := by
  cases Q with
  | mk hornS simplexS inclusion hornMap scaled =>
    have hm :
        liftHornMap.{u, v} n i
          (unliftHornMap.{u, v} n i hornMap) = hornMap :=
      lift_unliftHornMap.{u, v} n i hornMap
    simp only [unliftScaledHornProblem, liftScaledHornProblem,
      lift_unliftHornScaling, lift_unliftSimplexScaling, hm]
    rfl

/-- Consequently filler *existence* on the original problem is equivalent
to filler existence on the canonical independent-universe lift. -/
theorem liftScaledHornFiller_nonempty_iff
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    Nonempty (ScaledHornFiller (liftScaledHornProblem.{u, v} P)) ↔
      Nonempty (ScaledHornFiller P) := by
  constructor
  · intro h
    have hh := unliftScaledHornFiller_nonempty.{u, v} h
    rw [unlift_liftScaledHornProblem.{u, v} P] at hh
    exact hh
  · exact liftScaledHornFiller_nonempty.{u, v}

/-- Conversely every high-universe horn problem with an actually lifted
target has filler existence precisely when its unlifted problem does. -/
theorem unliftScaledHornFiller_nonempty_iff
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) n i) :
    Nonempty (ScaledHornFiller (unliftScaledHornProblem.{u, v} Q)) ↔
      Nonempty (ScaledHornFiller Q) := by
  constructor
  · intro h
    have hh := liftScaledHornFiller_nonempty.{u, v} h
    rw [lift_unliftScaledHornProblem.{u, v} Q] at hh
    exact hh
  · exact unliftScaledHornFiller_nonempty.{u, v}

#print axioms unlift_liftScaledHornProblem
#print axioms lift_unliftScaledHornProblem
#print axioms liftScaledHornFiller_nonempty_iff
#print axioms unliftScaledHornFiller_nonempty_iff

end KUOS.DependentOriginationULiftScaledHornProblemRoundTripV1_29
