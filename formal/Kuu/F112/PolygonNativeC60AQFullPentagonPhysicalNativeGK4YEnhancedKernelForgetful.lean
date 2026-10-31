import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4YEnhancedKernelCategory
import Mathlib.Tactic

/-!
# F112-P94D3GK4Y — true enriched-to-Boolean second-quotient functor

There are TWO SEPARATE true GK4S second quotients of the SAME original
P92B witness-existence quotient Q, but by DIFFERENT observations:
K_X = Q / (Bool x Int enhanced equality) and K_B = Q / Bool equality.
Define an actual canonical K_X -> K_B quotient factor, using the
original Q classes themselves, not replacing their Type-valued
F54/P92B comparison evidence with a fabricated shadow certificate.

Show the map is surjective on every genuine F45 typed hom, preserves
second-quotient unit and transported composition, and yields a true
Mathlib Functor between the separately wrapped K_X and K_B categories.
Its composite with the genuine GK4I->K_X comparison is EXACTLY
GK4U's previously constructed GK4I->K_B Boolean functor.

Crucially the true enriched->Boolean quotient functor is NOT faithful
at ANY inhabited original F45 self-hom. The entire actual GK4W
castDepths tower has pairwise distinct enhanced K_X classes whose
images in K_B are the SAME Boolean-unit kernel class. In fact the
fiber of the genuine K_X->K_B quotient over the observed Boolean unit
has EXACT cardinality aleph0 at EVERY inhabited original F45 tree.
This is NOT a result about the independent structural S vs Q fiber,
nor original unconditional 14D Countable.

Keep three different quotient authorities Q/S/K and the separate
two secondary kernel observations; do not assert original Q
associativity or identities, completeness of historical Type-valued
3-cell equivalence, global strict n, 19D filler, hyperdescent or
faithfulness of the stronger structural->K_X comparison. No Gray,
new axiom, sorry, admit. Append-only, public roots 107, same-root.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected #1558 Draft/open/unmerged.
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

section GenuineSecondQuotientRefinement
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- Genuine SECOND quotient factor: from original P92B equality of
enhanced values to the coarser equality of original Boolean values.
Its lift uses ONLY original actual P92B quotient classes. -/
def nativeGK4YForgetCharge :
    NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂ →
      NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₂ :=
  _root_.Quotient.lift
    (nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) t₁ t₂)
    (by
      intro q r h
      apply (nativeGK4SKernelClass_eq_iff
        (nativeGK4OBooleanFamily p D E) t₁ t₂ q r).mpr
      exact congrArg Prod.fst h)

/-- Forgetting the extra physical cast charge on an ACTUAL original
P92B representative gives the original Boolean kernel class. -/
@[simp] theorem nativeGK4YForgetCharge_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4YForgetCharge t₁ t₂
      (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q) =
      nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) t₁ t₂ q := by
  rfl

/-- True K_X->K_B quotient factor is ONTO every source-dependent Hom.
It is not the invalid original Q->S inverse. -/
theorem nativeGK4YForgetCharge_surjective :
    Function.Surjective (nativeGK4YForgetCharge t₁ t₂) := by
  intro z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  exact ⟨nativeGK4SKernelClass
    (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q, rfl⟩

/-- The genuine SECOND-quotient identity descends to the genuine
Boolean SECOND-quotient identity, not to original Q's missing unit. -/
@[simp] theorem nativeGK4YForgetCharge_unit :
    nativeGK4YForgetCharge t₁ t₁ (nativeGK4YEnhancedKernelUnit t₁) =
      nativeGK4UBoolKernelUnit t₁ := by
  rfl

/-- The K_X->K_B second quotient factor preserves actual induced
composition, using only GK4S's original Q-class projection theorem. -/
theorem nativeGK4YForgetCharge_compose
    (u : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₂ t₃) :
    nativeGK4YForgetCharge t₁ t₃
      (nativeGK4YEnhancedKernelCompose t₁ t₂ t₃ u v) =
    nativeGK4UBoolKernelCompose t₁ t₂ t₃
      (nativeGK4YForgetCharge t₁ t₂ u)
      (nativeGK4YForgetCharge t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  change nativeGK4YForgetCharge t₁ t₃
      (nativeGK4YEnhancedKernelCompose t₁ t₂ t₃
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q)
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₂ t₃ r)) =
    nativeGK4UBoolKernelCompose t₁ t₂ t₃
      (nativeGK4YForgetCharge t₁ t₂
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q))
      (nativeGK4YForgetCharge t₂ t₃
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₂ t₃ r))
  rw [nativeGK4YEnhancedKernelCompose_class,
    nativeGK4YForgetCharge_class,
    nativeGK4YForgetCharge_class,
    nativeGK4YForgetCharge_class,
    nativeGK4UBoolKernelCompose_class]

/-- Quotient reduction is literally the first projection of the
real attained enhanced observation, not a new map on raw F54 cells. -/
theorem nativeGK4YForgetCharge_value
    (u : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂) :
    nativeGK4VKernelGrade t₁ t₂ (nativeGK4YForgetCharge t₁ t₂ u) =
      (nativeGK4YEnhancedKernelValue t₁ t₂ u).1 := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  rfl

/-- Forgetting enhanced charge after TRUE structural comparison is
EXACTLY GK4T/GK4U's original Boolean second-quotient comparison. -/
theorem nativeGK4YForgetCharge_comparison
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4YForgetCharge t₁ t₂
        (nativeGK4XEnhancedComparison t₁ t₂ s) =
      nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
        (nativeGK4N_boolean_seam_invariant t₁ t₂) s := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  rfl

end GenuineSecondQuotientRefinement

/-- A TRUE Mathlib functor between two ACTUAL second quotients of the
same original P92B source, using their separately proven categories.
Not a forgetful functor on an invented ambient product only. -/
def nativeGK4YForgetChargeFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4YEnhancedKernelStage p ma mb pa pb ⥤
      NativeGK4UBoolKernelStage p ma mb pa pb where
  obj X := ⟨X.original⟩
  map := fun {X Y} f =>
    nativeGK4YForgetCharge X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4YForgetCharge_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4YForgetCharge_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

/-- The genuine K_X->K_B functor is FULL per Hom: every actual
Boolean-kernel class has an original P92B source class and therefore
an enhanced-kernel class above it. No faithful claim. -/
theorem nativeGK4YForgetFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4YEnhancedKernelStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4YForgetChargeFunctor p ma mb pa pb).map f) := by
  exact nativeGK4YForgetCharge_surjective
    X.original.2.2 Y.original.2.2

/-- At every fully typed F45 boundary, the ACTUAL categorical
composition S->K_X->K_B equals GK4U's original S->K_B functor
on arrows. This does not identify the K_X and K_B Hom types. -/
theorem nativeGK4YForgetFunctor_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4YForgetChargeFunctor p ma mb pa pb).map
      ((nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).map f) =
      (nativeGK4UBoolKernelComparisonFunctor p ma mb pa pb).map f := by
  exact nativeGK4YForgetCharge_comparison X.2.2 Y.2.2 f

theorem nativeGK4YForgetFunctor_factor_obj
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    (nativeGK4YForgetChargeFunctor p ma mb pa pb).obj
      ((nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).obj X) =
      (nativeGK4UBoolKernelComparisonFunctor p ma mb pa pb).obj X := by
  rfl

section GenuineInfiniteFiber
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- The true original signed-cast tower is invisible after K_X->K_B
forgetful projection: EVERY enhanced tower class has precisely the
actual Boolean SECOND quotient unit as its image. -/
theorem nativeGK4YForget_castTower_eq_boolUnit (k : Nat) :
    nativeGK4YForgetCharge tree tree
        (nativeGK4XEnhancedComparison tree tree
          (nativeGK4EStructuralRouteClass tree tree
            (nativeGK4WCastTower tree k))) =
      nativeGK4UBoolKernelUnit tree := by
  calc
    nativeGK4YForgetCharge tree tree
        (nativeGK4XEnhancedComparison tree tree
          (nativeGK4EStructuralRouteClass tree tree
            (nativeGK4WCastTower tree k))) =
        nativeGK4TComparison (nativeGK4OBooleanFamily p D E)
          tree tree (nativeGK4N_boolean_seam_invariant tree tree)
            (nativeGK4EStructuralRouteClass tree tree
              (nativeGK4WCastTower tree k)) :=
      nativeGK4YForgetCharge_comparison tree tree _
    _ = nativeGK4TComparison (nativeGK4OBooleanFamily p D E)
          tree tree (nativeGK4N_boolean_seam_invariant tree tree)
            (nativeGK4H_structuralUnit tree) := by
      apply (nativeGK4VComparison_eq_iff_grade tree tree _ _).mpr
      rw [nativeGK4WCastTower_grade]
      rfl
    _ = nativeGK4UBoolKernelUnit tree :=
      nativeGK4U_comparison_preserves_unit
        (nativeGK4OBooleanFamily p D E) tree
        (nativeGK4N_boolean_seam_invariant tree tree)

/-- EXACT fiber of K_X->K_B over the actual original zero-edge
Boolean SECOND-quotient unit, not merely the ambient grade=true set. -/
abbrev NativeGK4YBooleanUnitFiber :=
  {z : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E)
      tree tree //
    nativeGK4YForgetCharge tree tree z = nativeGK4UBoolKernelUnit tree}

/-- Each genuine original F54 cast tower lifts to the actual
K_X->K_B Boolean-unit fiber by exact second-quotient projection. -/
def nativeGK4YCastTowerUnitFiber (k : Nat) :
    NativeGK4YBooleanUnitFiber tree :=
  ⟨nativeGK4XEnhancedComparison tree tree
    (nativeGK4EStructuralRouteClass tree tree
      (nativeGK4WCastTower tree k)),
   nativeGK4YForget_castTower_eq_boolUnit tree k⟩

/-- Countably infinite actual quotient fiber: all genuine cast tower
classes remain distinct in K_X, despite projecting to one K_B class. -/
theorem nativeGK4YCastTowerUnitFiber_injective :
    Function.Injective (nativeGK4YCastTowerUnitFiber tree) := by
  intro i j hij
  exact nativeGK4XEnhancedComparison_castTower_injective tree
    (congrArg Subtype.val hij)

/-- The exact K_X fiber over the genuine Boolean-unit class is
aleph0 for ANY inhabited F45 tree, with NO generic countability
premises on the original independent D/E category. The complete
enhanced kernel quotient injects into Bool×Int, already Countable;
the original cast tower injects Nat into its Boolean-unit fiber. -/
theorem nativeGK4YBooleanUnitFiber_aleph0 :
    Cardinal.mk (NativeGK4YBooleanUnitFiber tree) = Cardinal.aleph0 := by
  letI : Countable
      (NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E)
        tree tree) :=
    Countable.of_injective
      (nativeGK4YEnhancedKernelValue tree tree)
      (nativeGK4YEnhancedKernelValue_injective tree tree)
  letI : Countable (NativeGK4YBooleanUnitFiber tree) := inferInstance
  letI : Infinite (NativeGK4YBooleanUnitFiber tree) :=
    Infinite.of_injective (nativeGK4YCastTowerUnitFiber tree)
      (nativeGK4YCastTowerUnitFiber_injective tree)
  exact Cardinal.mk_eq_aleph0 _

/-- The ACTUAL K_X->K_B forgetful second-quotient map is never
injective on an inhabited original F45 self-Hom, with the
two genuine classes k=0 and k=1 as a concrete witness. -/
theorem nativeGK4YForgetCharge_not_injective_self :
    ¬ Function.Injective (nativeGK4YForgetCharge tree tree) := by
  intro hinj
  have hsame := (nativeGK4YForget_castTower_eq_boolUnit tree 0).trans
    (nativeGK4YForget_castTower_eq_boolUnit tree 1).symm
  have hclasses := hinj hsame
  have hnat := nativeGK4XEnhancedComparison_castTower_injective tree hclasses
  omega

/-- The TRUE Mathlib functor K_X -> K_B therefore is NOT faithful
at ANY inhabited original F45 self-object. It is FULL on all Homs. -/
theorem nativeGK4YForgetFunctor_not_injective_self
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4YEnhancedKernelStage p ma mb pa pb) :
    ¬ Function.Injective
      (fun f : X ⟶ X =>
        (nativeGK4YForgetChargeFunctor p ma mb pa pb).map f) := by
  exact nativeGK4YForgetCharge_not_injective_self X.original.2.2

/-- Unconditional TRUE physical C60 north hexagon: the new
K_X->K_B quotient fiber over the zero-edge observed unit is
aleph0, and the corresponding genuine forgetful functor is
nonfaithful on the original F45 north self-Hom. -/
theorem nativeGK4Y_physical_north_infinite_forgetful_fiber :
    Cardinal.mk (NativeGK4YBooleanUnitFiber
      nativeGK4FPhysicalNorthTriple) = Cardinal.aleph0 ∧
    ¬ Function.Injective
      (nativeGK4YForgetCharge
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact ⟨nativeGK4YBooleanUnitFiber_aleph0 nativeGK4FPhysicalNorthTriple,
    nativeGK4YForgetCharge_not_injective_self nativeGK4FPhysicalNorthTriple⟩

end GenuineInfiniteFiber

#print axioms nativeGK4YForgetCharge
#print axioms nativeGK4YForgetCharge_class
#print axioms nativeGK4YForgetCharge_surjective
#print axioms nativeGK4YForgetCharge_unit
#print axioms nativeGK4YForgetCharge_compose
#print axioms nativeGK4YForgetCharge_value
#print axioms nativeGK4YForgetCharge_comparison
#print axioms nativeGK4YForgetChargeFunctor
#print axioms nativeGK4YForgetFunctor_surjective_hom
#print axioms nativeGK4YForgetFunctor_factor_map
#print axioms nativeGK4YForgetFunctor_factor_obj
#print axioms nativeGK4YForget_castTower_eq_boolUnit
#print axioms NativeGK4YBooleanUnitFiber
#print axioms nativeGK4YCastTowerUnitFiber
#print axioms nativeGK4YCastTowerUnitFiber_injective
#print axioms nativeGK4YBooleanUnitFiber_aleph0
#print axioms nativeGK4YForgetCharge_not_injective_self
#print axioms nativeGK4YForgetFunctor_not_injective_self
#print axioms nativeGK4Y_physical_north_infinite_forgetful_fiber

end
end Kuu.F112.Physical
