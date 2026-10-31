import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AAThreeComponentObserver
import Mathlib.Tactic

/-!
F112-P94D3GK4AA — actual structural S -> new second P92B
triple-observation kernel K_AA and TRUE value-category functors.

The comparison is a surjective map between separate genuine F54
quotients, not a reconstruction of a P92B Type-valued 3-cell.
The new K_AA observer retains the physical backward count that GK4X
forgets; the original GK4Z balanced tower becomes injective in K_AA,
despite being constant in the actual older enhanced kernel K_X.
This proves a strict refinement but NO global faithfulness of S->K_AA.

Append-only, public root 107, pinned Lean/mathlib, no Gray, strict 空
central. Protected #1558 unchanged. Copyright © 2026 Hidetoshi
Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-- New ambient one-object triple-value category, separate from
the old Boolean and Bool×Int value categories. -/
inductive NativeGK4AAValuePoint : Type where
  | star

instance nativeGK4AAValueCategory : Category NativeGK4AAValuePoint where
  Hom _ _ := NativeGK4AAValue
  id _ := ((true, 0), 0)
  comp u v := nativeGK4AACombine u v
  id_comp := by
    intro X Y f
    exact nativeGK4AACombine_leftUnit f
  comp_id := by
    intro X Y f
    exact nativeGK4AACombine_rightUnit f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AACombine_assoc f g h

/-- Genuine original structural F45 category S -> triple values.
The source category is the independently proved structural one,
not the original P92B Q with unproved category axioms. -/
def nativeGK4AAValueFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤ NativeGK4AAValuePoint where
  obj _ := .star
  map := fun {X Y} f => nativeGK4AATripleStructural X.2.2 Y.2.2 f
  map_id := by
    intro X
    exact nativeGK4AATripleStructural_unit X.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AATripleStructural_compose X.2.2 Y.2.2 Z.2.2 f g

/-- Canonical product projection in the ambient VALUE category,
which forgets only the original backward edge count. -/
def nativeGK4AAForgetBackwardValueFunctor :
    NativeGK4AAValuePoint ⥤ NativeGK4XValuePoint where
  obj _ := .star
  map := fun {X Y} f => f.1
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z f g
    rfl

theorem nativeGK4AAValueFunctor_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    nativeGK4AAForgetBackwardValueFunctor.map
      ((nativeGK4AAValueFunctor p ma mb pa pb).map f) =
      (nativeGK4XValueFunctor p ma mb pa pb).map f := by
  rfl

theorem nativeGK4AAValueFunctor_factor_obj
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    nativeGK4AAForgetBackwardValueFunctor.obj
      ((nativeGK4AAValueFunctor p ma mb pa pb).obj X) =
      (nativeGK4XValueFunctor p ma mb pa pb).obj X := by
  rfl

section GenuineSecondKernelComparison
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- The precise true GK4T descent criterion is satisfied by ALL
fourteen original structural seams. -/
theorem nativeGK4AATripleComparisonExists :
    NativeGK4TComparisonExists
      (nativeGK4AATripleP92Family p D E) first last := by
  exact (nativeGK4TComparisonExists_iff_seam
    (nativeGK4AATripleP92Family p D E) first last).mpr
      (nativeGK4AATripleSeamInvariant first last)

/-- True S -> K_AA map between two distinct original F54 quotients. -/
def nativeGK4AATripleComparison :
    NativeGK4EStructuralRouteClasses first last →
      NativeGK4SKernelClasses
        (nativeGK4AATripleP92Family p D E) first last :=
  nativeGK4TComparison (nativeGK4AATripleP92Family p D E)
    first last (nativeGK4AATripleSeamInvariant first last)

/-- The value of an attained triple-kernel class is exactly the
triple observation of its genuine S class. -/
theorem nativeGK4AATripleComparison_value
    (u : NativeGK4EStructuralRouteClasses first last) :
    (nativeGK4SKernelImageEquiv
        (nativeGK4AATripleP92Family p D E) first last
        (nativeGK4AATripleComparison first last u)).val =
      nativeGK4AATripleStructural first last u := by
  obtain ⟨q, rfl⟩ := nativeGK4EP92ToStructural_surjective first last u
  simpa only [nativeGK4AATripleComparison,
    nativeGK4TComparison_class, nativeGK4SKernelImageEquiv_class]
    using (nativeGK4AATriple_commutes first last q).symm

/-- Exactly the true triple-observation kernel, not a newly
fabricated equivalence between original Type-valued P92B proofs. -/
theorem nativeGK4AATripleComparison_eq_iff
    (u v : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AATripleComparison first last u =
      nativeGK4AATripleComparison first last v ↔
    nativeGK4AATripleStructural first last u =
      nativeGK4AATripleStructural first last v := by
  constructor
  · intro h
    have hval := congrArg
      (fun z : NativeGK4SKernelClasses
          (nativeGK4AATripleP92Family p D E) first last =>
        (nativeGK4SKernelImageEquiv
          (nativeGK4AATripleP92Family p D E) first last z).val) h
    simpa only [nativeGK4AATripleComparison_value] using hval
  · intro h
    apply (nativeGK4SKernelImageEquiv
      (nativeGK4AATripleP92Family p D E) first last).injective
    apply Subtype.ext
    simpa only [nativeGK4AATripleComparison_value] using h

theorem nativeGK4AATripleComparison_eq_iff_components
    (u v : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AATripleComparison first last u =
      nativeGK4AATripleComparison first last v ↔
    nativeGK4XEnhancedStructural first last u =
      nativeGK4XEnhancedStructural first last v ∧
    nativeGK4ZBackwardStructural first last u =
      nativeGK4ZBackwardStructural first last v := by
  exact (nativeGK4AATripleComparison_eq_iff first last u v).trans
    (nativeGK4AATripleStructural_eq_iff first last u v)

theorem nativeGK4AATripleComparison_surjective :
    Function.Surjective (nativeGK4AATripleComparison first last) := by
  exact nativeGK4TComparison_surjective
    (nativeGK4AATripleP92Family p D E) first last
    (nativeGK4AATripleSeamInvariant first last)

theorem nativeGK4AATripleComparison_injective_iff :
    Function.Injective (nativeGK4AATripleComparison first last) ↔
      Function.Injective (nativeGK4AATripleStructural first last) := by
  constructor
  · intro hinj u v h
    exact hinj ((nativeGK4AATripleComparison_eq_iff first last u v).mpr h)
  · intro hinj u v h
    exact hinj ((nativeGK4AATripleComparison_eq_iff first last u v).mp h)

/-- The ACTUAL second quotient K_AA -> older K_X quotient is defined
on real P92B classes, using only first projection of triple equality. -/
def nativeGK4AAForgetBackward :
    NativeGK4SKernelClasses
        (nativeGK4AATripleP92Family p D E) first last →
      NativeGK4SKernelClasses
        (nativeGK4XEnhancedP92Family p D E) first last :=
  _root_.Quotient.lift
    (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) first last)
    (by
      intro q r h
      apply (nativeGK4SKernelClass_eq_iff
        (nativeGK4XEnhancedP92Family p D E) first last q r).mpr
      exact congrArg Prod.fst h)

@[simp] theorem nativeGK4AAForgetBackward_class
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AAForgetBackward first last
      (nativeGK4SKernelClass (nativeGK4AATripleP92Family p D E)
        first last q) =
      nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E)
        first last q := rfl

theorem nativeGK4AAForgetBackward_surjective :
    Function.Surjective (nativeGK4AAForgetBackward first last) := by
  intro z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  exact ⟨nativeGK4SKernelClass
      (nativeGK4AATripleP92Family p D E) first last q, rfl⟩

theorem nativeGK4AAForgetBackward_comparison
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AAForgetBackward first last
        (nativeGK4AATripleComparison first last s) =
      nativeGK4XEnhancedComparison first last s := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  rfl

/-- The new kernel refines but does not replace the older kernel. -/
theorem nativeGK4AAForgetBackward_value
    (z : NativeGK4SKernelClasses
      (nativeGK4AATripleP92Family p D E) first last) :
    nativeGK4YEnhancedKernelValue first last
      (nativeGK4AAForgetBackward first last z) =
      (nativeGK4SKernelImageEquiv
        (nativeGK4AATripleP92Family p D E) first last z).val.1 := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  rfl

end GenuineSecondKernelComparison

section GenuineBalancedTowerSeparation
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- The older GK4X observer was constant, but the new triple
observer reads the genuine backward-edge count k+1. -/
theorem nativeGK4AABalancedTower_observation (k : Nat) :
    nativeGK4AATripleStructural before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ZBalancedTower rot k)) =
      ((false, (-2 : Int)), k + 1) := by
  apply Prod.ext
  · exact nativeGK4ZBalancedTower_observation rot k
  · exact nativeGK4ZBalancedTower_backward rot k

/-- All genuine original F54 balanced routes R_k remain SEPARATE
in the new actual P92B triple-observation second quotient K_AA. -/
theorem nativeGK4AABalancedTower_comparison_injective :
    Function.Injective
      (fun k : Nat =>
        nativeGK4AATripleComparison before before
          (nativeGK4EStructuralRouteClass before before
            (nativeGK4ZBalancedTower rot k))) := by
  intro i j hij
  have hv := (nativeGK4AATripleComparison_eq_iff before before _ _).mp hij
  have hb := congrArg Prod.snd hv
  change (nativeGK4ZBalancedTower rot i).gk4zBackwardCount =
    (nativeGK4ZBalancedTower rot j).gk4zBackwardCount at hb
  rw [nativeGK4ZBalancedTower_backward,
    nativeGK4ZBalancedTower_backward] at hb
  omega

/-- Forgetting backwards again collapses exactly these
infinitely many distinct genuine second-kernel classes. -/
theorem nativeGK4AABalancedTower_forget_constant (i j : Nat) :
    nativeGK4AAForgetBackward before before
      (nativeGK4AATripleComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4ZBalancedTower rot i))) =
    nativeGK4AAForgetBackward before before
      (nativeGK4AATripleComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4ZBalancedTower rot j))) := by
  rw [nativeGK4AAForgetBackward_comparison,
    nativeGK4AAForgetBackward_comparison]
  exact nativeGK4ZBalancedTower_comparison_constant rot i j

end GenuineBalancedTowerSeparation

#print axioms NativeGK4AAValuePoint
#print axioms nativeGK4AAValueCategory
#print axioms nativeGK4AAValueFunctor
#print axioms nativeGK4AAForgetBackwardValueFunctor
#print axioms nativeGK4AAValueFunctor_factor_map
#print axioms nativeGK4AAValueFunctor_factor_obj
#print axioms nativeGK4AATripleComparisonExists
#print axioms nativeGK4AATripleComparison
#print axioms nativeGK4AATripleComparison_value
#print axioms nativeGK4AATripleComparison_eq_iff
#print axioms nativeGK4AATripleComparison_eq_iff_components
#print axioms nativeGK4AATripleComparison_surjective
#print axioms nativeGK4AATripleComparison_injective_iff
#print axioms nativeGK4AAForgetBackward
#print axioms nativeGK4AAForgetBackward_class
#print axioms nativeGK4AAForgetBackward_surjective
#print axioms nativeGK4AAForgetBackward_comparison
#print axioms nativeGK4AAForgetBackward_value
#print axioms nativeGK4AABalancedTower_observation
#print axioms nativeGK4AABalancedTower_comparison_injective
#print axioms nativeGK4AABalancedTower_forget_constant

end
end Kuu.F112.Physical
