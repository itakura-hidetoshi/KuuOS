import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4EQuotientInfiniteFiber

/-!
# F112-P94D3GK4F — two different countably infinite quotient-collapse fibers

GK4E constructs the canonical surjection from the ACTUAL original P92B
Type-valued route quotient to the DISTINCT structural-comparison route
quotient. One structural class receives aleph-null different P92B
classes from original zero-rotation F54 unit towers.

We construct an ACTUAL, nontrivial, physically based closed F54 loop
from an original forward local rotation and its original backward
witness. Unlike the zero-rotation unit towers, this original F54 route
contains TWO genuine primitive local rotation edges.

We prove that whether the primitive rotation count is ZERO is preserved
by ALL nine ORIGINAL F55 PresentedCell constructors, ALL nine P92B
constructors including newly adjoined assocNaturality, and ALL three
StructuralComparison constructors (using the original F54 structural
seam rotation count theorem). Thus a 0-rotation original F54 unit route
and the 2-rotation genuine backtrack represent DISTINCT structural
quotient classes, without asserting the entire structural quotient is
a singleton or classifying all its other components.

Precompose the original F54 unit tower by the genuine backtrack, and
connect each stage to the backtrack via ORIGINAL Type-valued F54
precompose and rightUnit structural seams. Different stages are STILL
separated in P92B by GK4C's independent original zero-chain atom count.

Consequently TWO DISTICT fibers of the canonical quotient surjection
each have exactly aleph-null distinct original P92B classes, under
explicit D/E object/Hom countability or unconditionally on a TRUE
Site×Site physical north C60 triple. No shadow/coherence assumed,
no nonoriginal 3-cell, no Gray, no higher filler or historical equivalence.
Lean v4.30.0-rc2; pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root, 107 public roots and protected #1558 retained.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

/-! ### Zero-count preservation by every actual comparison generator. -/

private theorem nativeGK4F_zero_add_left
    (a b c : Nat) (h : b = 0 ↔ c = 0) :
    (a + b = 0 ↔ a + c = 0) := by
  constructor
  · intro hab
    have hb : b = 0 := by omega
    have hc : c = 0 := h.mp hb
    omega
  · intro hac
    have hc : c = 0 := by omega
    have hb : b = 0 := h.mpr hc
    omega

private theorem nativeGK4F_zero_add_right
    (a b c : Nat) (h : b = 0 ↔ c = 0) :
    (b + a = 0 ↔ c + a = 0) := by
  constructor
  · intro hba
    have hb : b = 0 := by omega
    have hc : c = 0 := h.mp hb
    omega
  · intro hca
    have hc : c = 0 := by omega
    have hb : b = 0 := h.mpr hc
    omega

/-- Every originally adjoined nine-constructor F55 cell preserves
whether there were NO genuine physical F54 local rotation edges.
Pentagon count 3 vs 2 is NOT equality of total counts, but both >0. -/
theorem nativeGK4FOriginal_zero_rotation_iff
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (r.rotationCount = 0 ↔ s.rotationCount = 0) := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      change (3 : Nat) = 0 ↔ (2 : Nat) = 0
      decide
  | disjointSquare left right =>
      change (2 : Nat) = 0 ↔ (2 : Nat) = 0
      decide
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose priorRoute cell ih =>
      change (priorRoute.rotationCount + _ = 0) ↔
        (priorRoute.rotationCount + _ = 0)
      exact nativeGK4F_zero_add_left _ _ _ ih
  | postcompose cell suffix ih =>
      change (_ + suffix.rotationCount = 0) ↔
        (_ + suffix.rotationCount = 0)
      exact nativeGK4F_zero_add_right _ _ _ ih

/-- The NEW original-P92B associator-naturality comparison preserves
the exact rotation count, and hence also whether that count vanishes.
All other eight constructor cases are inherited from true original F55
or handled by structural recursion over raw witness pasting. -/
theorem nativeGK4FP92B_zero_rotation_iff
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    (r.rotationCount = 0 ↔ s.rotationCount = 0) := by
  induction cell with
  | original old => exact nativeGK4FOriginal_zero_rotation_iff old
  | assocNaturality u v w =>
      rw [nativeF54P90AssocNaturality_rotationCount_eq u v w]
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose priorRoute cell ih =>
      change (priorRoute.rotationCount + _ = 0) ↔
        (priorRoute.rotationCount + _ = 0)
      exact nativeGK4F_zero_add_left _ _ _ ih
  | postcompose cell suffix ih =>
      change (_ + suffix.rotationCount = 0) ↔
        (_ + suffix.rotationCount = 0)
      exact nativeGK4F_zero_add_right _ _ _ ih

/-- All THREE independent structural comparison constructors preserve
the 0-vs-positive source-local-rotation distinction. The added F54
structural seam preserves even the complete physical rotation count. -/
theorem nativeGK4FStructural_zero_rotation_iff
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55StructuralComparison p r s) :
    (r.rotationCount = 0 ↔ s.rotationCount = 0) := by
  induction cell with
  | original old => exact nativeGK4FP92B_zero_rotation_iff old
  | structural seam =>
      rw [seam.rotationCount_sound]
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight

section Backtrack

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}

/-- The ACTUAL nontrivial forward-then-backward original F54 route.
The original RotationEdge.backward reuses THE SAME typed LocalRotation
witness, not an invented inverse between unrelated F45 proof objects. -/
def nativeGK4FBacktrack
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .chain (.snoc (.snoc (.refl before) (.forward rot)) (.backward rot))

@[simp] theorem nativeGK4FBacktrack_rotationCount
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    (nativeGK4FBacktrack rot).rotationCount = 2 := by
  rfl

@[simp] theorem nativeGK4FBacktrack_unitCount
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    (nativeGK4FBacktrack rot).gk4cUnitCount = 0 := by
  rfl

/-- Repeat the original zero-edge unit only after an ACTUAL two-edge
backtrack, retaining the same original F45 source/target and both Nat axes. -/
def nativeGK4FPositiveTower
    (rot : KuuNativeF45Tree.LocalRotation p before after) (k : Nat) :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4FBacktrack rot) (nativeGK4DUnitTower before k)

@[simp] theorem nativeGK4FPositiveTower_unitCount
    (rot : KuuNativeF45Tree.LocalRotation p before after) (k : Nat) :
    (nativeGK4FPositiveTower rot k).gk4cUnitCount = k + 1 := by
  simp only [nativeGK4FPositiveTower, nativeGK4C_unitCount_trans,
    nativeGK4FBacktrack_unitCount, nativeGK4DUnitTower_count]
  omega

/-- The original positive-tower stages are connected to the TWO-edge
backtrack by original F54 structural precompose and rightUnit seams. -/
def nativeGK4FPositiveTower_seam_to_backtrack
    (rot : KuuNativeF45Tree.LocalRotation p before after) (k : Nat) :
    NativeF54StructuralSeam p (nativeGK4FPositiveTower rot k)
      (nativeGK4FBacktrack rot) :=
  .trans
    (.precompose (nativeGK4FBacktrack rot)
      (nativeGK4DUnitTower_connect before k 0))
    (.rightUnit (nativeGK4FBacktrack rot))

/-- The original zero-unit tower and an ACTUAL two-edge backtrack are
not connected even by the EXTENDED structural comparison. -/
theorem nativeGK4F_zero_positive_structural_classes_ne
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    nativeGK4EStructuralRouteClass before before
        (nativeGK4DUnitTower before 0) ≠
      nativeGK4EStructuralRouteClass before before
        (nativeGK4FBacktrack rot) := by
  intro heq
  have hcell := (nativeGK4EStructuralRouteClass_eq_iff before before
    (nativeGK4DUnitTower before 0) (nativeGK4FBacktrack rot)).mp heq
  rcases hcell with ⟨w⟩
  have hzero : (nativeGK4DUnitTower before 0).rotationCount = 0 := rfl
  have hpos : (nativeGK4FBacktrack rot).rotationCount ≠ 0 := by
    rw [nativeGK4FBacktrack_rotationCount]
    omega
  exact hpos ((nativeGK4FStructural_zero_rotation_iff w).mp hzero)

/-- A concrete original local rotation guarantees that the ENTIRE
structural-comparison quotient contains at least TWO classes. -/
theorem nativeGK4F_structural_quotient_not_subsingleton
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ¬ Subsingleton (NativeGK4EStructuralRouteClasses before before) := by
  intro hs
  haveI : Subsingleton (NativeGK4EStructuralRouteClasses before before) := hs
  exact nativeGK4F_zero_positive_structural_classes_ne rot
    (Subsingleton.elim _ _)

/-- One DIFFERENT fiber of the same GK4E canonical quotient surjection,
this time over the genuine physical 2-edge backtrack class. -/
abbrev NativeGK4FPositiveCollapsedFiber
    (rot : KuuNativeF45Tree.LocalRotation p before after) :=
  {q : NativeF55P92AssocRouteClasses before before //
    nativeGK4EP92ToStructural before before q =
      nativeGK4EStructuralRouteClass before before (nativeGK4FBacktrack rot)}

/-- Actual P92B quotient classes of the positive unit tower live in
this second, distinct structural-quotient fiber. -/
def nativeGK4FPositiveTowerFiber
    (rot : KuuNativeF45Tree.LocalRotation p before after) (k : Nat) :
    NativeGK4FPositiveCollapsedFiber rot := by
  refine ⟨nativeF55P92AssocRouteClass before before
    (nativeGK4FPositiveTower rot k), ?_⟩
  change nativeGK4EStructuralRouteClass before before
    (nativeGK4FPositiveTower rot k) =
      nativeGK4EStructuralRouteClass before before (nativeGK4FBacktrack rot)
  exact _root_.Quotient.sound ⟨.structural
    (nativeGK4FPositiveTower_seam_to_backtrack rot k)⟩

/-- Even within this SECOND structural fiber, the original P92B
classes are pairwise distinct, by the full zero-chain count invariant. -/
theorem nativeGK4FPositiveTowerFiber_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Function.Injective (nativeGK4FPositiveTowerFiber rot) := by
  intro i j hij
  have hclasses := congrArg
    (fun q : NativeGK4FPositiveCollapsedFiber rot => q.1) hij
  have hex := (nativeF55P92AssocRouteClass_eq_iff before before
    (nativeGK4FPositiveTower rot i)
    (nativeGK4FPositiveTower rot j)).mp hclasses
  rcases hex with ⟨cell⟩
  have hcount := nativeGK4C_P92B_unitCount_sound cell
  rw [nativeGK4FPositiveTower_unitCount,
    nativeGK4FPositiveTower_unitCount] at hcount
  omega

/-- EXACT aleph-null size of the SECOND canonical-surjection fiber.
We retain explicit generic object and each categorical Hom countability.
The source is the ORIGINAL P92B equivalence-class quotient, not raw
F54 proofs, and the target is an ACTUAL distinct structural class. -/
theorem nativeGK4FPositiveCollapsedFiber_aleph0
    (rot : KuuNativeF45Tree.LocalRotation p before after)
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Cardinal.mk (NativeGK4FPositiveCollapsedFiber rot) = Cardinal.aleph0 := by
  letI : Countable (NativeF55P92AssocRouteClasses before before) :=
    nativeGK4EP92Classes_countable before before hobjD hhomD hobjE hhomE
  letI : Countable (NativeGK4FPositiveCollapsedFiber rot) := inferInstance
  letI : Infinite (NativeGK4FPositiveCollapsedFiber rot) :=
    Infinite.of_injective (nativeGK4FPositiveTowerFiber rot)
      (nativeGK4FPositiveTowerFiber_injective rot)
  exact Cardinal.mk_eq_aleph0 _

end Backtrack

/-! ### True C60 north-hexagon triple: both quotient fibers exist. -/

/-- Original source F45 triple, NOT a chosen synthetic geometric graph. -/
def nativeGK4FPhysicalNorthTriple :=
  KuuNativeF45Tree.node
    (KuuNativeF45Tree.node (northHexagonNativeUnit 0)
      (northHexagonNativeUnit 1))
    (northHexagonNativeUnit 2)

/-- The genuine physical structural-comparison quotient is NOT a point.
The actual original F54 two-edge rotation backtrack witnesses a SECOND
class distinct from the true zero-edge unit class. -/
theorem nativeGK4F_physical_north_structural_not_subsingleton :
    ¬ Subsingleton (NativeGK4EStructuralRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) :=
  nativeGK4F_structural_quotient_not_subsingleton
    northHexagonNativeLeftRotation

/-- On ONE AND THE SAME original physical C60 F45 triple, TWO
DISTINCT structural quotient fibers each contain exactly aleph-null
distinct original P92B equivalence classes. -/
theorem nativeGK4F_physical_north_two_distinct_aleph0_fibers :
    Cardinal.mk (NativeGK4ECollapsedFiber nativeGK4FPhysicalNorthTriple) =
        Cardinal.aleph0 ∧
    Cardinal.mk (NativeGK4FPositiveCollapsedFiber
        northHexagonNativeLeftRotation) = Cardinal.aleph0 ∧
    nativeGK4EStructuralRouteClass nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple
        (nativeGK4DUnitTower nativeGK4FPhysicalNorthTriple 0) ≠
      nativeGK4EStructuralRouteClass nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple
        (nativeGK4FBacktrack northHexagonNativeLeftRotation) := by
  refine ⟨?_, ?_, ?_⟩
  · exact nativeGK4ECollapsedFiber_aleph0 nativeGK4FPhysicalNorthTriple
      nativeC60GEPhysicalSite_countable
      nativeC60GEPhysicalIncidenceHom_countable
      nativeC60GEPhysicalSite_countable
      nativeC60GEPhysicalIncidenceHom_countable
  · exact nativeGK4FPositiveCollapsedFiber_aleph0
      northHexagonNativeLeftRotation
      nativeC60GEPhysicalSite_countable
      nativeC60GEPhysicalIncidenceHom_countable
      nativeC60GEPhysicalSite_countable
      nativeC60GEPhysicalIncidenceHom_countable
  · exact nativeGK4F_zero_positive_structural_classes_ne
      northHexagonNativeLeftRotation

#print axioms nativeGK4FOriginal_zero_rotation_iff
#print axioms nativeGK4FP92B_zero_rotation_iff
#print axioms nativeGK4FStructural_zero_rotation_iff
#print axioms nativeGK4FBacktrack
#print axioms nativeGK4FBacktrack_rotationCount
#print axioms nativeGK4FBacktrack_unitCount
#print axioms nativeGK4FPositiveTower
#print axioms nativeGK4FPositiveTower_unitCount
#print axioms nativeGK4FPositiveTower_seam_to_backtrack
#print axioms nativeGK4F_zero_positive_structural_classes_ne
#print axioms nativeGK4F_structural_quotient_not_subsingleton
#print axioms nativeGK4FPositiveTowerFiber
#print axioms nativeGK4FPositiveTowerFiber_injective
#print axioms nativeGK4FPositiveCollapsedFiber_aleph0
#print axioms nativeGK4FPhysicalNorthTriple
#print axioms nativeGK4F_physical_north_structural_not_subsingleton
#print axioms nativeGK4F_physical_north_two_distinct_aleph0_fibers

end
end Kuu.F112.Physical
