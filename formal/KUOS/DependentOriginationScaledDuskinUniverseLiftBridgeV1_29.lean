import KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22

namespace KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29

open CategoryTheory
open Simplicial
open Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22

universe u v

/-!
# Universe-safe scaling bridge (append-only)

The existing scalings on `SSet.{u}` are transported to the literal
`SSet.uliftFunctor.{v,u}` at the pinned mathlib API. This does not identify
different universes or silently change an existing scaled-horn certificate.
The converse descent and compatibility with both Duskin nerves remain separate
proof obligations.
-/

/-- Lift a scaling without changing which underlying 2-simplices are thin. -/
@[reducible] def uliftScaling
    {X : SSet.{u}} (sX : ScaledSimplicialSet X) :
    ScaledSimplicialSet ((SSet.uliftFunctor.{v, u}).obj X) where
  thin := fun x => sX.thin x.down
  thin_sigma_zero := by
    intro x
    change sX.thin (X.σ 0 x.down)
    exact sX.thin_sigma_zero x.down
  thin_sigma_one := by
    intro x
    change sX.thin (X.σ 1 x.down)
    exact sX.thin_sigma_one x.down

/-- Lifting reflects and preserves the original thinness predicate exactly. -/
@[simp] theorem uliftScaling_thin_iff
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (x : X.obj (op ⦋2⦌)) :
    (uliftScaling.{u, v} sX).thin (ULift.up x) ↔ sX.thin x := by
  rfl

/-- Every scaled map lifts to a scaled map at the common universe. -/
theorem isScaledMap_ulift
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y} (hf : IsScaledMap sX sY f) :
    IsScaledMap (uliftScaling.{u, v} sX) (uliftScaling.{u, v} sY)
      ((SSet.uliftFunctor.{v, u}).map f) := by
  intro x hx
  change sY.thin (f.app (op ⦋2⦌) x.down)
  exact hf x.down hx

#print axioms uliftScaling
#print axioms uliftScaling_thin_iff
#print axioms isScaledMap_ulift

end KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
