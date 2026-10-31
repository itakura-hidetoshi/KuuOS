import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4WCastChargeInvariant
import Mathlib.Tactic

/-!
F112-P94D3GK4W — genuine structural Boolean NONFAITHFULNESS.

An original F54 castDepths rfl rfl is a real Type-valued route
with NO physical local rotation, but one explicit cast constructor.
A true chain-refl zero route has neither. GK4W's full original
P92B and independent extended structural seam charge invariance
separates these genuine structural quotient classes. Their Boolean
grades are both true, so GK4U's comparison functor is nonfaithful on
EVERY inhabited original F45 self-Hom. This is STRONGER than GK4V's
previous iff and is not inferred from Q->K noninjectivity.

Repeat actual castDepths generators in a raw F54 tower: its signed
cast-rotation charge is the tower index, so all genuine structural
classes remain distinct, with the SAME true Boolean grade. Thus
physical north C60 has countably infinitely many distinct structural
self-arrows in one observed Boolean fiber, while the Boolean kernel
hom remains a separate, much smaller observational quotient.

No original P92B unitality, associativity or new source composition;
no historical complete Type-valued equivalence, genuine 14D unconditional
Countable, 19D filler, global strict n or hyperdescent. No Gray/new
axioms/sorry/admit. Appendix-only same-root 107 public roots.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Keep validation-only #1558 Draft/OPEN/unmerged.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section ExplicitWitness
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- A genuine original two-depth identity CAST constructor,
not a synthetic external route or abstract Boolean witness. -/
def nativeGK4WCastRoute :
    KuuNativeF45Tree.DepthRotationRoute p tree tree :=
  .castDepths rfl rfl tree

@[simp] theorem nativeGK4WCastRoute_charge :
    (nativeGK4WCastRoute tree).gk4wCastCharge = 1 := by
  rfl

@[simp] theorem nativeGK4WCastRoute_rotation :
    (nativeGK4WCastRoute tree).rotationCount = 0 := by
  rfl

/-- The actual original zero-edge F54 route is the GK4I independent
structural category's unit representative, carrying charge ZERO. -/
@[simp] theorem nativeGK4WReflRoute_charge :
    ((KuuNativeF45Tree.DepthRotationRoute.chain
      (KuuNativeF45Tree.RotationChain.refl tree)).gk4wCastCharge : Int) = 0 := by
  rfl

/-- The independent STRUCTURAL quotient DOES NOT identify a true
castDepths constructor with the original zero-edge identity class.
Every old P92B cell and every new structural seam preserves the
signed charge, so a genuine typed 3-cell equivalence is impossible. -/
theorem nativeGK4WCastClass_ne_structuralUnit :
    nativeGK4EStructuralRouteClass tree tree (nativeGK4WCastRoute tree) ≠
      nativeGK4H_structuralUnit tree := by
  intro h
  have hclasses :
      nativeGK4EStructuralRouteClass tree tree (nativeGK4WCastRoute tree) =
        nativeGK4EStructuralRouteClass tree tree (.chain (.refl tree)) := h
  rcases (nativeGK4EStructuralRouteClass_eq_iff tree tree
      (nativeGK4WCastRoute tree) (.chain (.refl tree))).mp hclasses with ⟨cell⟩
  have hcharge := nativeGK4W_structural_charge_sound cell
  change (1 : Int) = 0 at hcharge
  omega

/-- Both structurally UNEQUAL genuine F54 routes have the SAME TRUE
observed Boolean grade, because neither has a physical rotation. -/
theorem nativeGK4WCastClass_and_unit_same_grade :
    nativeGK4GStructuralGrade tree tree
        (nativeGK4EStructuralRouteClass tree tree (nativeGK4WCastRoute tree)) =
      nativeGK4GStructuralGrade tree tree (nativeGK4H_structuralUnit tree) := by
  rfl

/-- Actual opposite of the once-unresolved GK4V faithfulness branch:
the GK4U structure->Boolean kernel comparison is NOT injective at
ANY inhabited original dependent F45 self-Hom. -/
theorem nativeGK4WBooleanComparison_not_injective :
    ¬ Function.Injective
      (nativeGK4TComparison (nativeGK4OBooleanFamily p D E)
        tree tree (nativeGK4N_boolean_seam_invariant tree tree)) := by
  intro hinj
  have heq :=
    (nativeGK4VComparison_eq_iff_grade tree tree
      (nativeGK4EStructuralRouteClass tree tree (nativeGK4WCastRoute tree))
      (nativeGK4H_structuralUnit tree)).mpr
        (nativeGK4WCastClass_and_unit_same_grade tree)
  exact nativeGK4WCastClass_ne_structuralUnit tree (hinj heq)

/-- Mathlib GK4I->GK4U actual functor is NONFAITHFUL on the
self-Hom of any original typed F45 stage. Its proven GK4U Hom
surjectivity/fullness remains true; neither implies equivalence. -/
theorem nativeGK4WBooleanFunctor_not_injective_self
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    ¬ Function.Injective
      (fun f : X ⟶ X =>
        (nativeGK4UBoolKernelComparisonFunctor p ma mb pa pb).map f) := by
  exact nativeGK4WBooleanComparison_not_injective X.2.2

end ExplicitWitness

section InfiniteCastTower
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- ACTUAL original F54 syntax: recursively compose k genuinely
typed castDepths self-routes, without inventing external 3-cells. -/
def nativeGK4WCastTower : Nat →
    KuuNativeF45Tree.DepthRotationRoute p tree tree
  | 0 => .chain (.refl tree)
  | k + 1 => .trans (nativeGK4WCastRoute tree) (nativeGK4WCastTower k)

/-- Signed charge of every truly typed F54 cast tower is EXACTLY k. -/
theorem nativeGK4WCastTower_charge (k : Nat) :
    (nativeGK4WCastTower tree k).gk4wCastCharge = (k : Int) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      rw [nativeGK4WCastTower, nativeGK4W_charge_trans,
        nativeGK4WCastRoute_charge, ih]
      omega

/-- Each raw tower has genuine primitive physical rotation count ZERO. -/
theorem nativeGK4WCastTower_rotation (k : Nat) :
    (nativeGK4WCastTower tree k).rotationCount = 0 := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change (nativeGK4WCastRoute tree).rotationCount +
        (nativeGK4WCastTower tree k).rotationCount = 0
      rw [nativeGK4WCastRoute_rotation, ih]

/-- The entire cast tower lies inside ONE true Boolean observable grade. -/
theorem nativeGK4WCastTower_grade (k : Nat) :
    nativeGK4GStructuralGrade tree tree
      (nativeGK4EStructuralRouteClass tree tree
        (nativeGK4WCastTower tree k)) = true := by
  change decide ((nativeGK4WCastTower tree k).rotationCount = 0) = true
  rw [nativeGK4WCastTower_rotation]
  decide

/-- Full Type-valued original/structural soundness of charge makes
all cast-tower STRUCTURAL existence classes genuinely distinct. -/
theorem nativeGK4WCastTower_structural_injective :
    Function.Injective
      (fun k : Nat => nativeGK4EStructuralRouteClass tree tree
        (nativeGK4WCastTower tree k)) := by
  intro i j heq
  rcases (nativeGK4EStructuralRouteClass_eq_iff tree tree
    (nativeGK4WCastTower tree i)
    (nativeGK4WCastTower tree j)).mp heq with ⟨cell⟩
  have hcharge := nativeGK4W_structural_charge_sound cell
  rw [nativeGK4WCastTower_charge, nativeGK4WCastTower_charge] at hcharge
  exact_mod_cast hcharge

/-- A TRUE fiber, not an abstract or fabricated quotient: all actual
independent structural classes with physical grade true. -/
abbrev NativeGK4WTrueStructuralFiber :=
  {s : NativeGK4EStructuralRouteClasses tree tree //
    nativeGK4GStructuralGrade tree tree s = true}

/-- Inject infinitely many actual original cast towers into the SAME
physical grade fiber of independently extended F54 structural Hom. -/
def nativeGK4WCastTowerFiber (k : Nat) :
    NativeGK4WTrueStructuralFiber tree :=
  ⟨nativeGK4EStructuralRouteClass tree tree (nativeGK4WCastTower tree k),
    nativeGK4WCastTower_grade tree k⟩

theorem nativeGK4WCastTowerFiber_injective :
    Function.Injective (nativeGK4WCastTowerFiber tree) := by
  intro i j hij
  apply nativeGK4WCastTower_structural_injective tree
  exact congrArg Subtype.val hij

end InfiniteCastTower

section PhysicalNorth

/-- Genuine physical C60 north F45 triple has provably nonfaithful
GK4I structural->GK4U Boolean kernel functor, not merely a conditional
GK4V obstruction. No user-imposed geometry reduction or shadow. -/
theorem nativeGK4W_physical_north_nonfaithful :
    ¬ Function.Injective
      (fun f : nativeGK4IPhysicalNorthTripleStage ⟶
          nativeGK4IPhysicalNorthTripleStage =>
        (nativeGK4UBoolKernelComparisonFunctor (.hexagon (.top 0))
          northHexagonNativeFrame.firstAxis northHexagonNativeFrame.firstAxis
          northHexagonNativeFrame.secondAxis northHexagonNativeFrame.secondAxis).map f) := by
  exact nativeGK4WBooleanComparison_not_injective nativeGK4FPhysicalNorthTriple

/-- In the TRUE physical C60 north geometry, the full STRUCTURAL
Boolean-true fiber has cardinal exactly aleph-null: an actual
Nat-injective cast tower and the existing physical Hom countability.
This is not the separate original 14D conditional countability. -/
theorem nativeGK4W_physical_north_true_structural_fiber_aleph0 :
    Cardinal.mk (NativeGK4WTrueStructuralFiber
      nativeGK4FPhysicalNorthTriple) = Cardinal.aleph0 := by
  letI : Countable (NativeGK4EStructuralRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) :=
    (nativeGK4G_physical_north_structural_countable_and_graded).1
  letI : Countable (NativeGK4WTrueStructuralFiber
      nativeGK4FPhysicalNorthTriple) := inferInstance
  letI : Infinite (NativeGK4WTrueStructuralFiber
      nativeGK4FPhysicalNorthTriple) :=
    Infinite.of_injective
      (nativeGK4WCastTowerFiber nativeGK4FPhysicalNorthTriple)
      (nativeGK4WCastTowerFiber_injective nativeGK4FPhysicalNorthTriple)
  exact Cardinal.mk_eq_aleph0 _

end PhysicalNorth

#print axioms nativeGK4WCastRoute
#print axioms nativeGK4WCastRoute_charge
#print axioms nativeGK4WCastRoute_rotation
#print axioms nativeGK4WReflRoute_charge
#print axioms nativeGK4WCastClass_ne_structuralUnit
#print axioms nativeGK4WCastClass_and_unit_same_grade
#print axioms nativeGK4WBooleanComparison_not_injective
#print axioms nativeGK4WBooleanFunctor_not_injective_self
#print axioms nativeGK4WCastTower
#print axioms nativeGK4WCastTower_charge
#print axioms nativeGK4WCastTower_rotation
#print axioms nativeGK4WCastTower_grade
#print axioms nativeGK4WCastTower_structural_injective
#print axioms NativeGK4WTrueStructuralFiber
#print axioms nativeGK4WCastTowerFiber
#print axioms nativeGK4WCastTowerFiber_injective
#print axioms nativeGK4W_physical_north_nonfaithful
#print axioms nativeGK4W_physical_north_true_structural_fiber_aleph0

end
end Kuu.F112.Physical
