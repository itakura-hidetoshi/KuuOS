import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGKernelCategory
import Mathlib.Tactic

/-!
F112-P94D3GK4AG — actual FULL-on-Hom forgetful Mathlib functor
K_AG -> K_AE, with S -> K_AG -> K_AE factorization. This is a
STRICT refinement on genuine original F54 C/B words: the GK4AF
counterexample is separated by K_AG but identified by K_AE.

NO claim that S -> K_AG is globally faithful. In particular neither
the original P92B Q category laws nor an original Type-valued 3-cell
between observations is manufactured. Append-only, same-root 107,
strict 空 central, no Gray. Protected #1558 untouched.
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
def nativeGK4AGForgetMatrix :
    NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂ →
    NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₂ :=
  _root_.Quotient.lift
    (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂)
    (by
      intro q r h
      apply (nativeGK4SKernelClass_eq_iff
        (nativeGK4AEQuadP92Family p D E) t₁ t₂ q r).mpr
      exact congrArg (fun z : NativeGK4AGValue => z.1) h)

@[simp] theorem nativeGK4AGForgetMatrix_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4AGForgetMatrix t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AGP92Family p D E) t₁ t₂ q) =
    nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q := rfl

theorem nativeGK4AGForgetMatrix_surjective :
    Function.Surjective (nativeGK4AGForgetMatrix t₁ t₂) := by
  intro z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  exact ⟨nativeGK4SKernelClass
    (nativeGK4AGP92Family p D E) t₁ t₂ q, rfl⟩

/-- Real S->K_AG->K_AE triangle, with the same original fully typed
F54 route, not a new observation-induced P92B witness. -/
theorem nativeGK4AGForgetMatrix_comparison
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AGForgetMatrix t₁ t₂
      (nativeGK4AGComparison t₁ t₂ s) =
      nativeGK4AEComparison t₁ t₂ s := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  rfl

theorem nativeGK4AGForgetMatrix_unit :
    nativeGK4AGForgetMatrix t₁ t₁
      (nativeGK4AGKernelUnit t₁) =
      nativeGK4AEEnhancedKernelUnit t₁ := rfl

theorem nativeGK4AGForgetMatrix_compose
    (u : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₂ t₃) :
    nativeGK4AGForgetMatrix t₁ t₃
      (nativeGK4AGKernelCompose t₁ t₂ t₃ u v) =
    nativeGK4AEEnhancedKernelCompose t₁ t₂ t₃
      (nativeGK4AGForgetMatrix t₁ t₂ u)
      (nativeGK4AGForgetMatrix t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  rw [nativeGK4AGKernelCompose_class,
    nativeGK4AGForgetMatrix_class, nativeGK4AGForgetMatrix_class,
    nativeGK4AGForgetMatrix_class, nativeGK4AEEnhancedKernelCompose_class]

/-- All original four-component information is recovered EXACTLY
after the second quotient's matrix-forgetful map. -/
theorem nativeGK4AGForgetMatrix_value
    (z : NativeGK4SKernelClasses (nativeGK4AGP92Family p D E) t₁ t₂) :
    nativeGK4AEEnhancedKernelValue t₁ t₂
        (nativeGK4AGForgetMatrix t₁ t₂ z) =
      nativeGK4AGForgetValue (nativeGK4AGKernelValue t₁ t₂ z) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  rfl

end RealForgetfulKernel

/-- Genuine Mathlib functor K_AG -> K_AE. Both categories are
attained quotients of the SAME actual original P92B typed Hom, with
different observable equality kernels. -/
def nativeGK4AGForgetMatrixFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AGKernelStage p ma mb pa pb ⥤
      NativeGK4AEEnhancedKernelStage p ma mb pa pb where
  obj X := ⟨X.original⟩
  map := fun {X Y} f =>
    nativeGK4AGForgetMatrix X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4AGForgetMatrix_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AGForgetMatrix_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

theorem nativeGK4AGForgetMatrixFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AGKernelStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4AGForgetMatrixFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AGForgetMatrix_surjective
    X.original.2.2 Y.original.2.2

/-- The source structural comparison really factors through the
new kernel and the OLD K_AE comparison on every Hom. -/
theorem nativeGK4AGComparison_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4AGForgetMatrixFunctor p ma mb pa pb).map
      ((nativeGK4AGComparisonFunctor p ma mb pa pb).map f) =
    (nativeGK4AEEnhancedKernelComparisonFunctor p ma mb pa pb).map f := by
  exact nativeGK4AGForgetMatrix_comparison X.2.2 Y.2.2 f

/-- The exact local criterion, with NO unconditional assertion of
S->K_AG faithfulness. -/
theorem nativeGK4AGComparison_injective_iff_joint
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Function.Injective (nativeGK4AGComparison first last) ↔
      Function.Injective (nativeGK4AGStructural first last) := by
  constructor
  · intro hinj u v h
    exact hinj ((nativeGK4AGComparison_eq_iff first last u v).mpr h)
  · intro hinj u v h
    exact hinj ((nativeGK4AGComparison_eq_iff first last u v).mp h)

section RealOriginalF54RefinementWitness
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- GK4AF's GENUINE original F54 paths differ in the new kernel,
because the independently descended noncommutative matrices differ. -/
theorem nativeGK4AGWords_separated :
    nativeGK4AGComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordCBBC rot)) ≠
    nativeGK4AGComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4AFWordBCCB rot)) := by
  intro heq
  have hv := (nativeGK4AGComparison_eq_iff before before _ _).mp heq
  have hm := congrArg (fun z : NativeGK4AGValue => z.2) hv
  change (nativeGK4AFWordCBBC rot).gk4afMatrix =
    (nativeGK4AFWordBCCB rot).gk4afMatrix at hm
  rw [nativeGK4AFWordCBBC_matrix, nativeGK4AFWordBCCB_matrix] at hm
  have hentry := congrArg (fun m : NativeGK4AFMatrix => m.1.1) hm
  change (0 : Int) = (-1 : Int) at hentry
  omega

/-- Yet the two NEW K_AG classes become IDENTICAL under actual
K_AG -> K_AE forgetful functor, as seen in original GK4AF. -/
theorem nativeGK4AGWords_forget_equal :
    nativeGK4AGForgetMatrix before before
      (nativeGK4AGComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4AFWordCBBC rot))) =
    nativeGK4AGForgetMatrix before before
      (nativeGK4AGComparison before before
        (nativeGK4EStructuralRouteClass before before
          (nativeGK4AFWordBCCB rot))) := by
  simpa only [nativeGK4AGForgetMatrix_comparison] using
    (nativeGK4AFFourKernel_equal rot)

/-- Genuine strict refinement on ANY original F54 witnessed local
rotation: the forgetful Hom map is NOT injective. -/
theorem nativeGK4AGForgetMatrix_not_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ¬ Function.Injective (nativeGK4AGForgetMatrix before before) := by
  intro hinj
  exact nativeGK4AGWords_separated rot
    (hinj (nativeGK4AGWords_forget_equal rot))

end RealOriginalF54RefinementWitness

/-- No artificial witness: the physical C60 north hexagon already
realizes the distinct joint values with identical old observations. -/
theorem nativeGK4AGPhysicalNorth_forget_nonfaithful :
    ¬ Function.Injective
      (nativeGK4AGForgetMatrix
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4AGForgetMatrix_not_injective
    northHexagonNativeLeftRotation

#print axioms nativeGK4AGForgetMatrix
#print axioms nativeGK4AGForgetMatrix_surjective
#print axioms nativeGK4AGForgetMatrix_comparison
#print axioms nativeGK4AGForgetMatrix_unit
#print axioms nativeGK4AGForgetMatrix_compose
#print axioms nativeGK4AGForgetMatrix_value
#print axioms nativeGK4AGForgetMatrixFunctor
#print axioms nativeGK4AGForgetMatrixFunctor_surjective_hom
#print axioms nativeGK4AGComparison_factor_map
#print axioms nativeGK4AGComparison_injective_iff_joint
#print axioms nativeGK4AGWords_separated
#print axioms nativeGK4AGWords_forget_equal
#print axioms nativeGK4AGForgetMatrix_not_injective
#print axioms nativeGK4AGPhysicalNorth_forget_nonfaithful

end
end Kuu.F112.Physical
