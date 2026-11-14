import KUOS.DependentOriginationULiftScalingDescentV1_29

/-!
# Exact round-trip of horn and simplex scalings across independent universes

The forward scaling on a represented horn/simplex uses the certified
ULift comparison isomorphism. The reverse scaling evaluates thinness on
the corresponding simplex in the original universe. By the two inverse
laws of the comparison isomorphism, both round trips recover the original
thinness predicate, hence the full scaled-simplicial-set structures.

No new scaled horn admissibility or fibrancy hypothesis is used. These
identities are local compatibility witnesses, not global descent.
-/

namespace KUOS.DependentOriginationULiftScalingRoundTripV1_29

open CategoryTheory Simplicial Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
open KUOS.DependentOriginationULiftScalingDescentV1_29

universe u v

/-- Two scalings coincide if and only if their thinness predicates coincide.
The two degeneracy fields contain proof data in Prop and add no other data. -/
private theorem scaling_eq_of_thin
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : ∀ x, s.thin x ↔ t.thin x) : s = t := by
  cases s with
  | mk thinS zeroS oneS =>
    cases t with
    | mk thinT zeroT oneT =>
      have hp : thinS = thinT := funext (fun x => propext (h x))
      cases hp
      rfl

/-- Pulling back a scaling along the inverse of an isomorphism, then
evaluating at its forward map, gives precisely the original thinness. -/
private theorem scaling_pullback_iso_hom
    {A B : SSet.{u}} (s : ScaledSimplicialSet A)
    (e : A ≅ B) (x : A.obj (op ⦋2⦌)) :
    (pullbackScaling s e.inv).thin (e.hom.app (op ⦋2⦌) x) ↔
      s.thin x := by
  change s.thin ((e.hom ≫ e.inv).app (op ⦋2⦌) x) ↔ s.thin x
  rw [e.hom_inv_id]
  rfl

/-- Unlifting a canonically lifted horn scaling recovers the exact
original lower-universe scaling. -/
theorem unlift_liftHornScaling (n : ℕ) (i : Fin (n + 1))
    (s : ScaledSimplicialSet (SSet.horn.{u} n i : SSet.{u})) :
    unliftHornScaling.{u, v} n i
      (liftedHornScaling.{u, v} n i s) = s := by
  apply scaling_eq_of_thin
  intro x
  change
    (pullbackScaling (uliftScaling.{u, v} s)
      (hornUniverseIso.{u, v} n i).inv).thin
        (hornUniverseEquiv.{u, v} n i (op ⦋2⦌) x) ↔ s.thin x
  have h :
      (hornUniverseIso.{u, v} n i).hom.app (op ⦋2⦌) (ULift.up x) =
        hornUniverseEquiv.{u, v} n i (op ⦋2⦌) x := rfl
  rw [← h]
  exact scaling_pullback_iso_hom (uliftScaling.{u, v} s)
    (hornUniverseIso.{u, v} n i) (ULift.up x)

/-- Unlifting a canonically lifted simplex scaling likewise recovers
the entire original simplex scaling, not only a weaker approximation. -/
theorem unlift_liftSimplexScaling (n : ℕ)
    (s : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    unliftSimplexScaling.{u, v} n
      (liftedSimplexScaling.{u, v} n s) = s := by
  apply scaling_eq_of_thin
  intro x
  change
    (pullbackScaling (uliftScaling.{u, v} s)
      (simplexUniverseIso.{u, v} n).inv).thin
        (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) x) ↔ s.thin x
  have h :
      (simplexUniverseIso.{u, v} n).hom.app (op ⦋2⦌) (ULift.up x) =
        simplexUniverseEquiv.{u, v} n (op ⦋2⦌) x := rfl
  rw [← h]
  exact scaling_pullback_iso_hom (uliftScaling.{u, v} s)
    (simplexUniverseIso.{u, v} n) (ULift.up x)

/-- Lifting the inverse horn scaling also returns the exact original
higher-universe predicate; this prevents losing thin triangles on descent. -/
theorem lift_unliftHornScaling (n : ℕ) (i : Fin (n + 1))
    (s : ScaledSimplicialSet (SSet.horn.{max u v} n i : SSet.{max u v})) :
    liftedHornScaling.{u, v} n i
      (unliftHornScaling.{u, v} n i s) = s := by
  apply scaling_eq_of_thin
  intro x
  change s.thin (hornUniverseEquiv.{u, v} n i (op ⦋2⦌)
      (((hornUniverseIso.{u, v} n i).inv.app (op ⦋2⦌) x).down)) ↔ s.thin x
  have h := congrArg
    (fun f : (SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
      (SSet.horn.{max u v} n i : SSet.{max u v}) => f.app (op ⦋2⦌) x)
      (hornUniverseIso.{u, v} n i).inv_hom_id
  change hornUniverseEquiv.{u, v} n i (op ⦋2⦌)
      (((hornUniverseIso.{u, v} n i).inv.app (op ⦋2⦌) x).down) = x at h
  rw [h]

/-- And similarly for an arbitrary higher-universe simplex scaling. -/
theorem lift_unliftSimplexScaling (n : ℕ)
    (s : ScaledSimplicialSet (Δ[n] : SSet.{max u v})) :
    liftedSimplexScaling.{u, v} n
      (unliftSimplexScaling.{u, v} n s) = s := by
  apply scaling_eq_of_thin
  intro x
  change s.thin (simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
      (((simplexUniverseIso.{u, v} n).inv.app (op ⦋2⦌) x).down)) ↔ s.thin x
  have h := congrArg
    (fun f : (Δ[n] : SSet.{max u v}) ⟶ (Δ[n] : SSet.{max u v}) =>
      f.app (op ⦋2⦌) x)
      (simplexUniverseIso.{u, v} n).inv_hom_id
  change simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
      (((simplexUniverseIso.{u, v} n).inv.app (op ⦋2⦌) x).down) = x at h
  rw [h]

#print axioms unlift_liftHornScaling
#print axioms unlift_liftSimplexScaling
#print axioms lift_unliftHornScaling
#print axioms lift_unliftSimplexScaling

end KUOS.DependentOriginationULiftScalingRoundTripV1_29
