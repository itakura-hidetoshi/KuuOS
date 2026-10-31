import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIKernelCategory
import Mathlib.Tactic

/-!
F112-P94D3GK4AI — true full-on-each-Hom forgetful Mathlib
Functor K_AI -> K_AG, both genuine *different* second attained
equality-kernel quotients of the SAME original P92B Type-witness Q.
All original F54 dependent source typing and independent S->K_AG
comparison are preserved. S->K_AI->K_AG factors on actual Hom;
composition and both units are preserved WITHOUT original Q category
laws. The true GK4AH original F54 CB^6C versus B^3C^2B^3 pair is
distinguished by K_AI's new second matrix but identified by K_AG.
Consequently the forgetful Functor is NOT faithful on any witnessed
genuine F54 local rotation, including physical C60 north.
No global S->K_AI faithfulness claim or invented Type-valued
original P92B 3-cell. Strict 空 central; independent Kuu one
presentation; append-only/same-root 107; Gray excluded.
Protected validation-only PR #1558 Draft/OPEN/unmerged.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

section RealForgetfulKernel
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- A genuinely well-defined second-kernel map: joint equality
implies four-coordinate equality; not a map from raw F54 strings. -/
def nativeGK4AIForgetMatrix :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂ →
    NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂ :=
  _root_.Quotient.lift
    (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂)
    (by
      intro q r h
      apply (nativeGK4SKernelClass_eq_iff
        (nativeGK4AGP92Family p D E) t₁ t₂ q r).mpr
      exact congrArg (fun z : NativeGK4AIValue => z.1) h)

@[simp] theorem nativeGK4AIForgetMatrix_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4AIForgetMatrix t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q) =
    nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q := rfl

theorem nativeGK4AIForgetMatrix_surjective :
    Function.Surjective (nativeGK4AIForgetMatrix t₁ t₂) := by
  intro z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  exact ⟨nativeGK4SKernelClass
    (nativeGK4AIP92Family p D E) t₁ t₂ q, rfl⟩

/-- Real S->K_AG->K_AE triangle, with the same original fully typed
F54 route, not a new observation-induced P92B witness. -/
theorem nativeGK4AIForgetMatrix_comparison
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AIForgetMatrix t₁ t₂
      (nativeGK4AIComparison t₁ t₂ s) =
      nativeGK4AGComparison t₁ t₂ s := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  rfl

theorem nativeGK4AIForgetMatrix_unit :
    nativeGK4AIForgetMatrix t₁ t₁
      (nativeGK4AIKernelUnit t₁) =
      nativeGK4AGKernelUnit t₁ := rfl

theorem nativeGK4AIForgetMatrix_compose
    (u : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₂ t₃) :
    nativeGK4AIForgetMatrix t₁ t₃
      (nativeGK4AIKernelCompose t₁ t₂ t₃ u v) =
    nativeGK4AGKernelCompose t₁ t₂ t₃
      (nativeGK4AIForgetMatrix t₁ t₂ u)
      (nativeGK4AIForgetMatrix t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  change nativeGK4AIForgetMatrix t₁ t₃
      (nativeGK4AIKernelCompose t₁ t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q)
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₂ t₃ r)) =
    nativeGK4AGKernelCompose t₁ t₂ t₃
      (nativeGK4AIForgetMatrix t₁ t₂
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q))
      (nativeGK4AIForgetMatrix t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₂ t₃ r))
  rw [nativeGK4AIKernelCompose_class,
    nativeGK4AIForgetMatrix_class, nativeGK4AIForgetMatrix_class,
    nativeGK4AIForgetMatrix_class, nativeGK4AGKernelCompose_class]

/-- All original four-component information is recovered EXACTLY
after the second quotient's matrix-forgetful map. -/
theorem nativeGK4AIForgetMatrix_value
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂) :
    nativeGK4AGKernelValue t₁ t₂
        (nativeGK4AIForgetMatrix t₁ t₂ z) =
      nativeGK4AIForgetValue (nativeGK4AIKernelValue t₁ t₂ z) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  rfl

end RealForgetfulKernel

/-- Genuine Mathlib functor K_AG -> K_AE. Both categories are
attained quotients of the SAME actual original P92B typed Hom, with
different observable equality kernels. -/
def nativeGK4AIForgetMatrixFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AIKernelStage p ma mb pa pb ⥤
      NativeGK4AGKernelStage p ma mb pa pb where
  obj X := ⟨X.original⟩
  map := fun {X Y} f =>
    nativeGK4AIForgetMatrix X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4AIForgetMatrix_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AIForgetMatrix_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

theorem nativeGK4AIForgetMatrixFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4AIForgetMatrixFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AIForgetMatrix_surjective
    X.original.2.2 Y.original.2.2

/-- The source structural comparison really factors through the
new kernel and the OLD K_AE comparison on every Hom. -/
theorem nativeGK4AIComparison_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4AIForgetMatrixFunctor p ma mb pa pb).map
      ((nativeGK4AIComparisonFunctor p ma mb pa pb).map f) =
    (nativeGK4AGComparisonFunctor p ma mb pa pb).map f := by
  exact nativeGK4AIForgetMatrix_comparison X.2.2 Y.2.2 f

/-- The exact local criterion, with NO unconditional assertion of
S->K_AG faithfulness. -/
theorem nativeGK4AIComparison_injective_iff_joint
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Function.Injective (nativeGK4AIComparison first last) ↔
      Function.Injective (nativeGK4AIStructural first last) := by
  constructor
  · intro hinj u v h
    exact hinj ((nativeGK4AIComparison_eq_iff first last u v).mpr h)
  · intro hinj u v h
    exact hinj ((nativeGK4AIComparison_eq_iff first last u v).mp h)

section RealOriginalF54RefinementWitness
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- The new independent GK4AH matrix separates actual original F54
self-routes CB^6C and B^3C^2B^3 in the REAL second joint kernel K_AI. -/
theorem nativeGK4AIWords_separated :
    nativeGK4AIComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AHWordCB6C rot)) ≠
    nativeGK4AIComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AHWordB3C2B3 rot)) := by
  intro heq
  have hv := (nativeGK4AIComparison_eq_iff before before _ _).mp heq
  have hm := congrArg (fun z : NativeGK4AIValue => z.2) hv
  change (nativeGK4AHWordCB6C rot).gk4ahMatrix =
    (nativeGK4AHWordB3C2B3 rot).gk4ahMatrix at hm
  rw [nativeGK4AHWordCB6C_newMatrix, nativeGK4AHWordB3C2B3_newMatrix] at hm
  have hentry := congrArg (fun m : NativeGK4AHMatrix => m.1.1) hm
  change (-11 : Int) = (-155 : Int) at hentry
  omega

/-- Despite new-class separation, their genuine original K_AG images
are identical (both old matrices and all four components coincide). -/
theorem nativeGK4AIWords_forget_equal :
    nativeGK4AIForgetMatrix before before
      (nativeGK4AIComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4AHWordCB6C rot))) =
    nativeGK4AIForgetMatrix before before
      (nativeGK4AIComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4AHWordB3C2B3 rot))) := by
  simpa only [nativeGK4AIForgetMatrix_comparison] using
    (nativeGK4AHJointKernel_equal rot)

/-- The true K_AI -> K_AG forgetful is strictly NONFAITHFUL on
every original F54 self-Hom witnessing a real LocalRotation. -/
theorem nativeGK4AIForgetMatrix_not_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ¬ Function.Injective (nativeGK4AIForgetMatrix before before) := by
  intro hinj
  exact nativeGK4AIWords_separated rot
    (hinj (nativeGK4AIWords_forget_equal rot))

end RealOriginalF54RefinementWitness

/-- The actual physical C60 north LocalRotation is an unconditional
source witness: no artificial generators or proof axioms introduced. -/
theorem nativeGK4AIPhysicalNorth_forget_nonfaithful :
    ¬ Function.Injective
      (nativeGK4AIForgetMatrix
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4AIForgetMatrix_not_injective
    northHexagonNativeLeftRotation

/-- Composite compatibility down to the ORIGINAL FOUR-component
K_AE second kernel, not only to the prior joint K_AG kernel. -/
theorem nativeGK4AIComparison_factor_to_four
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4AGForgetMatrixFunctor p ma mb pa pb).map
        ((nativeGK4AIForgetMatrixFunctor p ma mb pa pb).map
          ((nativeGK4AIComparisonFunctor p ma mb pa pb).map f)) =
      (nativeGK4AEEnhancedKernelComparisonFunctor p ma mb pa pb).map f := by
  rw [nativeGK4AIComparison_factor_map]
  exact nativeGK4AGComparison_factor_map p ma mb pa pb X Y f

#print axioms nativeGK4AIForgetMatrix
#print axioms nativeGK4AIForgetMatrix_surjective
#print axioms nativeGK4AIForgetMatrix_comparison
#print axioms nativeGK4AIForgetMatrix_unit
#print axioms nativeGK4AIForgetMatrix_compose
#print axioms nativeGK4AIForgetMatrix_value
#print axioms nativeGK4AIForgetMatrixFunctor
#print axioms nativeGK4AIForgetMatrixFunctor_surjective_hom
#print axioms nativeGK4AIComparison_factor_map
#print axioms nativeGK4AIComparison_injective_iff_joint
#print axioms nativeGK4AIWords_separated
#print axioms nativeGK4AIWords_forget_equal
#print axioms nativeGK4AIForgetMatrix_not_injective
#print axioms nativeGK4AIPhysicalNorth_forget_nonfaithful
#print axioms nativeGK4AIComparison_factor_to_four

end
end Kuu.F112.Physical
