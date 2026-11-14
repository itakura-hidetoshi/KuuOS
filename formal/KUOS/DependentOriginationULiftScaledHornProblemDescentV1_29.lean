import KUOS.DependentOriginationULiftScaledMapReflectionV1_29
import KUOS.DependentOriginationULiftScalingRoundTripV1_29

/-!
# Genuine reverse transport of scaled horns and their fillers

A horn problem whose target is the ULift of a lower-universe scaled
simplicial set is reflected to the lower universe without forgetting
the original simplex/horn scaling, face index or inclusion. Both
thinness predicates are transported by the exact universe comparison,
and the inverse maps are provided by the certified fully faithful
functor. The filler equation descends through the certified commutative
horn-inclusion square.

No assumption is made that an arbitrary, independently chosen horn
family is admissible; family descent remains a separate obligation.
-/

namespace KUOS.DependentOriginationULiftScaledHornProblemDescentV1_29

open CategoryTheory Simplicial Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftHornMapEquivalenceV1_29
open KUOS.DependentOriginationULiftHornExtensionReflectionV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
open KUOS.DependentOriginationULiftScalingDescentV1_29
open KUOS.DependentOriginationULiftScalingRoundTripV1_29
open KUOS.DependentOriginationULiftScaledMapReflectionV1_29

universe u v

/-- A higher-universe horn problem with an actually lifted target has a
well-typed lower-universe preimage, including its exact two scalings. -/
noncomputable def unliftScaledHornProblem
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) n i) :
    ScaledHornExtensionProblem X sX n i where
  hornScaling := unliftHornScaling.{u, v} n i Q.hornScaling
  simplexScaling := unliftSimplexScaling.{u, v} n Q.simplexScaling
  inclusion_scaled := by
    intro t ht
    change Q.simplexScaling.thin
      (simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
        ((SSet.horn.{u} n i).ι.app (op ⦋2⦌) t))
    have hThin :
        Q.hornScaling.thin
          (hornUniverseEquiv.{u, v} n i (op ⦋2⦌) t) := ht
    have hIncl :
        simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
          ((SSet.horn.{u} n i).ι.app (op ⦋2⦌) t) =
        (SSet.horn.{max u v} n i).ι.app (op ⦋2⦌)
          (hornUniverseEquiv.{u, v} n i (op ⦋2⦌) t) := rfl
    rw [hIncl]
    exact Q.inclusion_scaled _ hThin
  hornMap := unliftHornMap.{u, v} n i Q.hornMap
  hornMap_scaled := by
    have hHi :
        IsScaledMap
          (liftedHornScaling.{u, v} n i
            (unliftHornScaling.{u, v} n i Q.hornScaling))
          (uliftScaling.{u, v} sX) Q.hornMap := by
      rw [lift_unliftHornScaling]
      exact Q.hornMap_scaled
    exact unliftHornMap_scaled.{u, v} sX n i
      (unliftHornScaling.{u, v} n i Q.hornScaling) Q.hornMap hHi

/-- Every scaled filler of an arbitrary horn problem with an actually lifted
target descends to the corresponding exact lower-universe problem. -/
noncomputable def unliftScaledHornFiller
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) n i}
    (Q : ScaledHornFiller P) :
    ScaledHornFiller (unliftScaledHornProblem.{u, v} P) where
  simplexMap := unliftSimplexMap.{u, v} n Q.simplexMap
  extends_horn :=
    unliftHornMap_extends.{u, v} n i P.hornMap
      Q.simplexMap Q.extends_horn
  simplexMap_scaled := by
    have hHi :
        IsScaledMap
          (liftedSimplexScaling.{u, v} n
            (unliftSimplexScaling.{u, v} n P.simplexScaling))
          (uliftScaling.{u, v} sX) Q.simplexMap := by
      rw [lift_unliftSimplexScaling]
      exact Q.simplexMap_scaled
    exact unliftSimplexMap_scaled.{u, v} sX n
      (unliftSimplexScaling.{u, v} n P.simplexScaling) Q.simplexMap hHi

/-- Existential reverse filler transport, independently of any
admissibility-family descent claim. -/
theorem unliftScaledHornFiller_nonempty
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) n i}
    (h : Nonempty (ScaledHornFiller P)) :
    Nonempty (ScaledHornFiller (unliftScaledHornProblem.{u, v} P)) :=
  h.map unliftScaledHornFiller

#print axioms unliftScaledHornProblem
#print axioms unliftScaledHornFiller
#print axioms unliftScaledHornFiller_nonempty

end KUOS.DependentOriginationULiftScaledHornProblemDescentV1_29
