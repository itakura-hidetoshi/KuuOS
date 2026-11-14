import KUOS.DependentOriginationForwardHornRectificationV1_29
import KUOS.DependentOriginationULiftScalingRoundTripV1_29

/-!
# Exact type-(A) scaling compatibility across independent ULift universes

A type-(A) family records two NONTRIVIAL scaling equalities on the genuine
represented simplex and horn, in addition to its inner horn index. An
index-only argument cannot establish its cross-universe compatibility.

Construct a family on the actual lifted target whose admissibility tests
the two canonical high-universe scaling transports of the original type-(A)
data. The already PROVED inverse round trips of both scaling transports
make this family equivalent to the actual canonical lifted original
type-(A) family, with neither maximal scaling nor any replacement of
original thin-triangle data.

Comparison with the separately defined NATIVE type-(A) scaling in the
higher universe is a distinct geometric task, explicitly isolated as
two exact scaling equalities below. Their existence is not asserted.
-/

namespace KUOS.DependentOriginationCrossUniverseTypeAScalingV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
open KUOS.DependentOriginationULiftScalingDescentV1_29
open KUOS.DependentOriginationULiftScalingRoundTripV1_29
open KUOS.DependentOriginationULiftScaledHornProblemDescentV1_29
open KUOS.DependentOriginationCanonicalCrossUniverseHornDescentV1_29
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationArbitraryFamilyAdmissibilityDescentV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30

universe u v

/-- Genuinely transported type-(A) admissibility on the full ULift target:
we require the EXACT transported horn and simplex scalings, not just n,i. -/
noncomputable def transportedTypeAHornFamily
    {X : SSet.{u}} (sX : ScaledSimplicialSet X) :
    ScaledHornFamily
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) where
  admissible := fun {n} {i} Q =>
    0 < i ∧ i < Fin.last n ∧
      Q.simplexScaling =
        liftedSimplexScaling.{u, v} n (standardTypeASimplexScaling.{u} i) ∧
      Q.hornScaling =
        liftedHornScaling.{u, v} n i (standardTypeAHornScaling.{u} i)

/-- The chosen transported type-(A) predicate is EXACTLY the canonical
ULift of the original source predicate.  Both directions use kernel-proved
round trips of the scaling structures, not proof-irrelevant coercions. -/
theorem transportedTypeA_admissible_iff
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    {n : Nat} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) n i) :
    (transportedTypeAHornFamily.{u, v} sX).admissible Q ↔
      (canonicalLiftedHornFamily.{u, v} sX
        (standardTypeAScaledHornFamily X sX)).admissible Q := by
  change
    (0 < i ∧ i < Fin.last n ∧
      Q.simplexScaling =
        liftedSimplexScaling.{u, v} n (standardTypeASimplexScaling.{u} i) ∧
      Q.hornScaling =
        liftedHornScaling.{u, v} n i (standardTypeAHornScaling.{u} i)) ↔
    (0 < i ∧ i < Fin.last n ∧
      unliftSimplexScaling.{u, v} n Q.simplexScaling =
        standardTypeASimplexScaling.{u} i ∧
      unliftHornScaling.{u, v} n i Q.hornScaling =
        standardTypeAHornScaling.{u} i)
  constructor
  · rintro ⟨h0, hi, hs, hh⟩
    refine ⟨h0, hi, ?_, ?_⟩
    · rw [hs, unlift_liftSimplexScaling.{u, v}]
    · rw [hh, unlift_liftHornScaling.{u, v}]
  · rintro ⟨h0, hi, hs, hh⟩
    refine ⟨h0, hi, ?_, ?_⟩
    · have he := congrArg (liftedSimplexScaling.{u, v} n) hs
      rw [lift_unliftSimplexScaling.{u, v} n Q.simplexScaling] at he
      exact he
    · have he := congrArg (liftedHornScaling.{u, v} n i) hh
      rw [lift_unliftHornScaling.{u, v} n i Q.hornScaling] at he
      exact he

/-- No external E witness is assumed for genuine type-(A) scaling transport:
the exact 2-sided admissibility compatibility follows from the two round trips. -/
theorem transportedTypeA_compatible
    {X : SSet.{u}} (sX : ScaledSimplicialSet X) :
    AdmissibilityCompatible
      (canonicalLiftedHornFamily.{u, v} sX
        (standardTypeAScaledHornFamily X sX))
      (transportedTypeAHornFamily.{u, v} sX) := by
  constructor
  · intro n i Q hQ
    exact (transportedTypeA_admissible_iff sX Q).2 hQ
  · intro n i Q hQ
    exact (transportedTypeA_admissible_iff sX Q).1 hQ

/-- True cross-universe scaled type-(A) fibrancy equivalence for the
*transported* higher-universe family, with both scaling structures intact. -/
theorem transportedTypeA_fibrancy_iff
    {X : SSet.{u}} (sX : ScaledSimplicialSet X) :
    HasScaledHornFillers X sX (standardTypeAScaledHornFamily X sX) ↔
      HasScaledHornFillers
        ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX)
        (transportedTypeAHornFamily.{u, v} sX) :=
  arbitraryCrossUniverseFibrancy_iff
    sX (standardTypeAScaledHornFamily X sX)
    (transportedTypeAHornFamily.{u, v} sX)
    (transportedTypeA_compatible.{u, v} sX)

/-- The precise remaining comparison with the independently defined
higher-universe native type-(A) scaling.  These are equalities of the
ACTUAL simplex/horn scaling structures, not mere index equalities. -/
structure NativeTypeAUniverseScalingCompatibility : Prop where
  simplex :
    ∀ {n : Nat} (i : Fin (n + 1)),
      liftedSimplexScaling.{u, v} n (standardTypeASimplexScaling.{u} i) =
        standardTypeASimplexScaling.{max u v} i
  horn :
    ∀ {n : Nat} (i : Fin (n + 1)),
      liftedHornScaling.{u, v} n i (standardTypeAHornScaling.{u} i) =
        standardTypeAHornScaling.{max u v} i

/-- Under those two explicit geometric equations, the transported and
native high-universe type-(A) families have exactly the same admissibility. -/
theorem transportedTypeA_native_compatible
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (h : NativeTypeAUniverseScalingCompatibility.{u, v}) :
    AdmissibilityCompatible
      (transportedTypeAHornFamily.{u, v} sX)
      (standardTypeAScaledHornFamily
        ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX)) := by
  constructor
  · intro n i Q hQ
    change
      (0 < i ∧ i < Fin.last n ∧
        Q.simplexScaling =
          liftedSimplexScaling.{u, v} n (standardTypeASimplexScaling.{u} i) ∧
        Q.hornScaling =
          liftedHornScaling.{u, v} n i (standardTypeAHornScaling.{u} i)) at hQ
    change
      (0 < i ∧ i < Fin.last n ∧
        Q.simplexScaling = standardTypeASimplexScaling.{max u v} i ∧
        Q.hornScaling = standardTypeAHornScaling.{max u v} i)
    exact ⟨hQ.1, hQ.2.1, hQ.2.2.1.trans (h.simplex i),
      hQ.2.2.2.trans (h.horn i)⟩
  · intro n i Q hQ
    change
      (0 < i ∧ i < Fin.last n ∧
        Q.simplexScaling = standardTypeASimplexScaling.{max u v} i ∧
        Q.hornScaling = standardTypeAHornScaling.{max u v} i) at hQ
    change
      (0 < i ∧ i < Fin.last n ∧
        Q.simplexScaling =
          liftedSimplexScaling.{u, v} n (standardTypeASimplexScaling.{u} i) ∧
        Q.hornScaling =
          liftedHornScaling.{u, v} n i (standardTypeAHornScaling.{u} i))
    exact ⟨hQ.1, hQ.2.1, hQ.2.2.1.trans ((h.simplex i).symm),
      hQ.2.2.2.trans ((h.horn i).symm)⟩

/-- Conditional direct comparison with the native upper-universe family.
Unlike the transported result above, this additionally needs the
actual scaling-preserving universe comparison, still an open geometry task. -/
theorem nativeTypeA_fibrancy_iff_of_scaling_compatibility
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (h : NativeTypeAUniverseScalingCompatibility.{u, v}) :
    HasScaledHornFillers X sX (standardTypeAScaledHornFamily X sX) ↔
      HasScaledHornFillers
        ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX)
        (standardTypeAScaledHornFamily
          ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX)) :=
  (transportedTypeA_fibrancy_iff.{u, v} sX).trans
    (sameCarrierFibrancy_iff
      (transportedTypeAHornFamily.{u, v} sX)
      (standardTypeAScaledHornFamily
        ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX))
      (transportedTypeA_native_compatible.{u, v} sX h))

#print axioms transportedTypeAHornFamily
#print axioms transportedTypeA_admissible_iff
#print axioms transportedTypeA_compatible
#print axioms transportedTypeA_fibrancy_iff
#print axioms transportedTypeA_native_compatible
#print axioms nativeTypeA_fibrancy_iff_of_scaling_compatibility

end KUOS.DependentOriginationCrossUniverseTypeAScalingV1_29
