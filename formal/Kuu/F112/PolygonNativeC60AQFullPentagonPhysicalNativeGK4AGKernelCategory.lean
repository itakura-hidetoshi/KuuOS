import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGProductObservation
import Mathlib.Tactic

/-!
F112-P94D3GK4AG — second *attained* kernel category K_AG built from
the original P92B proof-existence Q by equality of the JOINT
four-coordinate/matrix observation. The independent structural S
maps to it by a genuine Mathlib functor, surjective on every Hom.

The proof derives associative/unital K_AG from value laws, NOT from
unproved original Q category laws. Its embedding in the joint value
category is faithful. Global S->K_AG faithfulness remains OPEN.
Append-only, same-root 107; strict 空 central; independent Kuu one
presentation; Gray excluded; protected validation-only #1558 untouched.
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

section GenuineJointSecondKernel
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
variable (t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb)

/-- Original P92B ZERO-edge representative, taken ONLY in K_AG. -/
def nativeGK4AGKernelUnit :
    NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₁ :=
  nativeGK4SKernelClass (nativeGK4AGP92Family p D E)
    t₁ t₁ (nativeGK4H_p92Unit t₁)

/-- Actual second quotient transport along the attained joint image. -/
def nativeGK4AGKernelCompose
    (u : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₂ t₃) :
    NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₃ :=
  nativeGK4SKernelCompose
    (nativeGK4AGP92Family p D E) nativeGK4AGCombine
    (nativeGK4PIdentityAction p D E NativeGK4AGValue)
    (nativeGK4PIdentityAction p D E NativeGK4AGValue)
    nativeGK4AGLaws t₁ t₂ t₃ u v

@[simp] theorem nativeGK4AGKernelCompose_class
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4AGKernelCompose t₁ t₂ t₃
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ u)
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₂ t₃ v) =
    nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₃
      (nativeGK4H_p92Compose t₁ t₂ t₃ u v) :=
  nativeGK4SKernelCompose_class
    (nativeGK4AGP92Family p D E) nativeGK4AGCombine
    (nativeGK4PIdentityAction p D E NativeGK4AGValue)
    (nativeGK4PIdentityAction p D E NativeGK4AGValue)
    nativeGK4AGLaws t₁ t₂ t₃ u v

theorem nativeGK4AGKernelCompose_assoc
    (u : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₂ t₃)
    (w : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₃ t₄) :
    nativeGK4AGKernelCompose t₁ t₃ t₄
        (nativeGK4AGKernelCompose t₁ t₂ t₃ u v) w =
      nativeGK4AGKernelCompose t₁ t₂ t₄ u
        (nativeGK4AGKernelCompose t₂ t₃ t₄ v w) := by
  exact nativeGK4SKernelCompose_assoc
    (nativeGK4AGP92Family p D E) nativeGK4AGCombine
    (nativeGK4PIdentityAction p D E NativeGK4AGValue)
    (nativeGK4PIdentityAction p D E NativeGK4AGValue)
    nativeGK4AGLaws t₁ t₂ t₃ t₄
    nativeGK4AGCombine_assoc u v w

theorem nativeGK4AGKernelCompose_leftUnit
    (u : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂) :
    nativeGK4AGKernelCompose t₁ t₁ t₂
      (nativeGK4AGKernelUnit t₁) u = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4AGKernelCompose t₁ t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₁
        (nativeGK4H_p92Unit t₁))
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q) =
    nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q
  rw [nativeGK4AGKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4AGP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4AGP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₁ t₂ (nativeGK4H_p92Unit t₁) q) =
    nativeGK4AGP92 t₁ t₂ q
  rw [nativeGK4AGP92_compose t₁ t₁ t₂ (nativeGK4H_p92Unit t₁) q,
    nativeGK4AGP92_unit t₁, nativeGK4AGCombine_leftUnit]

theorem nativeGK4AGKernelCompose_rightUnit
    (u : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂) :
    nativeGK4AGKernelCompose t₁ t₂ t₂
      u (nativeGK4AGKernelUnit t₂) = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4AGKernelCompose t₁ t₂ t₂
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q)
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₂ t₂
        (nativeGK4H_p92Unit t₂)) =
    nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q
  rw [nativeGK4AGKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4AGP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4AGP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₂ t₂ q (nativeGK4H_p92Unit t₂)) =
    nativeGK4AGP92 t₁ t₂ q
  rw [nativeGK4AGP92_compose t₁ t₂ t₂ q (nativeGK4H_p92Unit t₂),
    nativeGK4AGP92_unit t₂, nativeGK4AGCombine_rightUnit]

/-- Evaluation of SECOND K_AG classes at the actually attained
joint value; not a fabricated arbitrary value. -/
def nativeGK4AGKernelValue
    (z : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂) :
    NativeGK4AGValue :=
  (nativeGK4SKernelImageEquiv
    (nativeGK4AGP92Family p D E) t₁ t₂ z).val

@[simp] theorem nativeGK4AGKernelValue_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4AGKernelValue t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q) =
        nativeGK4AGP92 t₁ t₂ q := rfl

theorem nativeGK4AGKernelValue_injective :
    Function.Injective (nativeGK4AGKernelValue t₁ t₂) := by
  intro u v h
  apply (nativeGK4SKernelImageEquiv
    (nativeGK4AGP92Family p D E) t₁ t₂).injective
  exact Subtype.ext h

@[simp] theorem nativeGK4AGKernelValue_unit :
    nativeGK4AGKernelValue t₁ t₁
      (nativeGK4AGKernelUnit t₁) = nativeGK4AGUnit := rfl

theorem nativeGK4AGKernelValue_compose
    (u : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₂ t₃) :
    nativeGK4AGKernelValue t₁ t₃
      (nativeGK4AGKernelCompose t₁ t₂ t₃ u v) =
        nativeGK4AGCombine
          (nativeGK4AGKernelValue t₁ t₂ u)
          (nativeGK4AGKernelValue t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  change nativeGK4AGKernelValue t₁ t₃
      (nativeGK4AGKernelCompose t₁ t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q)
        (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₂ t₃ r)) =
    nativeGK4AGCombine
      (nativeGK4AGKernelValue t₁ t₂
        (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q))
      (nativeGK4AGKernelValue t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₂ t₃ r))
  rw [nativeGK4AGKernelCompose_class,
    nativeGK4AGKernelValue_class, nativeGK4AGKernelValue_class,
    nativeGK4AGKernelValue_class]
  exact nativeGK4AGP92_compose t₁ t₂ t₃ q r

/-- GENUINE structurally descended S->K_AG local comparison. -/
def nativeGK4AGComparison :
    NativeGK4EStructuralRouteClasses t₁ t₂ →
      NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂ :=
  nativeGK4TComparison (nativeGK4AGP92Family p D E)
    t₁ t₂ (nativeGK4AGSeamInvariant t₁ t₂)

theorem nativeGK4AGComparison_value
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AGKernelValue t₁ t₂
      (nativeGK4AGComparison t₁ t₂ s) =
      nativeGK4AGStructural t₁ t₂ s := by
  obtain ⟨q, rfl⟩ := nativeGK4EP92ToStructural_surjective t₁ t₂ s
  simpa only [nativeGK4AGComparison, nativeGK4TComparison_class,
    nativeGK4AGKernelValue_class] using
    (nativeGK4AG_commutes t₁ t₂ q).symm

theorem nativeGK4AGComparison_eq_iff
    (u v : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AGComparison t₁ t₂ u =
      nativeGK4AGComparison t₁ t₂ v ↔
    nativeGK4AGStructural t₁ t₂ u =
      nativeGK4AGStructural t₁ t₂ v := by
  constructor
  · intro h
    simpa only [nativeGK4AGComparison_value] using
      congrArg (nativeGK4AGKernelValue t₁ t₂) h
  · intro h
    apply nativeGK4AGKernelValue_injective t₁ t₂
    simpa only [nativeGK4AGComparison_value] using h

theorem nativeGK4AGComparison_surjective :
    Function.Surjective (nativeGK4AGComparison t₁ t₂) := by
  exact nativeGK4TComparison_surjective
    (nativeGK4AGP92Family p D E) t₁ t₂
    (nativeGK4AGSeamInvariant t₁ t₂)

end GenuineJointSecondKernel

/-- Separate typed objects from original Q, independent S and
existing four-coordinate K_AE. -/
structure NativeGK4AGKernelStage
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) where
  original : NativeGK4IStage p ma mb pa pb

instance nativeGK4AGKernelCategory
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Category (NativeGK4AGKernelStage p ma mb pa pb) where
  Hom X Y := NativeGK4SKernelClasses
    (nativeGK4AGP92Family p D E) X.original.2.2 Y.original.2.2
  id X := nativeGK4AGKernelUnit X.original.2.2
  comp f g := nativeGK4AGKernelCompose _ _ _ f g
  id_comp := by
    intro X Y f
    exact nativeGK4AGKernelCompose_leftUnit
      X.original.2.2 Y.original.2.2 f
  comp_id := by
    intro X Y f
    exact nativeGK4AGKernelCompose_rightUnit
      X.original.2.2 Y.original.2.2 f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AGKernelCompose_assoc
      W.original.2.2 X.original.2.2 Y.original.2.2 Z.original.2.2 f g h

/-- Actual structural category S -> independent refined second K_AG.
S faithfulness is NOT asserted. -/
def nativeGK4AGComparisonFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤
      NativeGK4AGKernelStage p ma mb pa pb where
  obj X := ⟨X⟩
  map := fun {X Y} f => nativeGK4AGComparison X.2.2 Y.2.2 f
  map_id := by
    intro X
    change nativeGK4AGComparison X.2.2 X.2.2
        (nativeGK4H_structuralUnit X.2.2) =
      nativeGK4AGKernelUnit X.2.2
    exact nativeGK4U_comparison_preserves_unit
      (nativeGK4AGP92Family p D E) X.2.2
      (nativeGK4AGSeamInvariant X.2.2 X.2.2)
  map_comp := by
    intro X Y Z f g
    change nativeGK4AGComparison X.2.2 Z.2.2
        (nativeGK4H_structuralCompose X.2.2 Y.2.2 Z.2.2 f g) =
      nativeGK4AGKernelCompose X.2.2 Y.2.2 Z.2.2
        (nativeGK4AGComparison X.2.2 Y.2.2 f)
        (nativeGK4AGComparison Y.2.2 Z.2.2 g)
    exact nativeGK4U_comparison_preserves_compose
      (nativeGK4AGP92Family p D E) nativeGK4AGCombine
      (nativeGK4PIdentityAction p D E NativeGK4AGValue)
      (nativeGK4PIdentityAction p D E NativeGK4AGValue)
      nativeGK4AGLaws X.2.2 Y.2.2 Z.2.2
      (nativeGK4AGSeamInvariant X.2.2 Y.2.2)
      (nativeGK4AGSeamInvariant Y.2.2 Z.2.2)
      (nativeGK4AGSeamInvariant X.2.2 Z.2.2) f g

theorem nativeGK4AGComparisonFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4AGComparisonFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AGComparison_surjective X.2.2 Y.2.2

/-- Single-object ambient category of ALL joint values, distinct
from the attained image and genuine original source Hom types. -/
inductive NativeGK4AGValuePoint : Type where
  | star

instance nativeGK4AGValueCategory : Category NativeGK4AGValuePoint where
  Hom _ _ := NativeGK4AGValue
  id _ := nativeGK4AGUnit
  comp u v := nativeGK4AGCombine u v
  id_comp := by
    intro X Y f
    exact nativeGK4AGCombine_leftUnit f
  comp_id := by
    intro X Y f
    exact nativeGK4AGCombine_rightUnit f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AGCombine_assoc f g h

/-- Actual attained joint-value embedding: faithful BY THE KERNEL
DEFINITION, not by assuming S faithfully maps to K_AG. -/
def nativeGK4AGKernelValueFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AGKernelStage p ma mb pa pb ⥤ NativeGK4AGValuePoint where
  obj _ := .star
  map := fun {X Y} f =>
    nativeGK4AGKernelValue X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4AGKernelValue_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AGKernelValue_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

theorem nativeGK4AGKernelValueFunctor_injective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AGKernelStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4AGKernelValueFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AGKernelValue_injective
    X.original.2.2 Y.original.2.2

/-- Original independent S's joint observer factors through the
genuine K_AG kernel stage and its faithful value category. -/
theorem nativeGK4AGComparison_value_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4AGKernelValueFunctor p ma mb pa pb).map
      ((nativeGK4AGComparisonFunctor p ma mb pa pb).map f) =
      nativeGK4AGStructural X.2.2 Y.2.2 f := by
  exact nativeGK4AGComparison_value X.2.2 Y.2.2 f

#print axioms nativeGK4AGKernelUnit
#print axioms nativeGK4AGKernelCompose
#print axioms nativeGK4AGKernelCompose_class
#print axioms nativeGK4AGKernelCompose_assoc
#print axioms nativeGK4AGKernelCompose_leftUnit
#print axioms nativeGK4AGKernelCompose_rightUnit
#print axioms nativeGK4AGKernelValue
#print axioms nativeGK4AGKernelValue_injective
#print axioms nativeGK4AGKernelValue_compose
#print axioms nativeGK4AGComparison
#print axioms nativeGK4AGComparison_value
#print axioms nativeGK4AGComparison_eq_iff
#print axioms nativeGK4AGComparison_surjective
#print axioms nativeGK4AGKernelCategory
#print axioms nativeGK4AGComparisonFunctor
#print axioms nativeGK4AGComparisonFunctor_surjective_hom
#print axioms nativeGK4AGValueCategory
#print axioms nativeGK4AGKernelValueFunctor
#print axioms nativeGK4AGKernelValueFunctor_injective_hom
#print axioms nativeGK4AGComparison_value_factor_map

end
end Kuu.F112.Physical
