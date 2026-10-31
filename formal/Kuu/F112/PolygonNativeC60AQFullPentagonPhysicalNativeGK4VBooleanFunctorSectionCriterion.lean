import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4VBooleanFaithfulnessCriterion
import Mathlib.Tactic

/-!
F112-P94D3GK4V — categorical grade factorization and physical C60
north full faithfulness criterion. Faithfulness is classified, NOT
declared true or false without a genuine same-grade structural pair.
Kuu strict 空 centered / independent Kuu a presentation, no Gray.
Unproved Q associativity/units, 14D Countable, 19D filler,
global strict n and hyperdescent stay unproved.
Append-only, public root 107; Lean 4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- The actual observed Boolean kernel category admits a functor
to GK4I's one-object Boolean category. Its Hom map is faithful. -/
def nativeGK4VKernelGradeFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4UBoolKernelStage p ma mb pa pb ⥤ NativeGK4IBoolPoint where
  obj _ := .star
  map := fun {X Y} f =>
    nativeGK4VKernelGrade X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4VKernelGrade_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4VKernelGrade_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

theorem nativeGK4VKernelGradeFunctor_injective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4UBoolKernelStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4VKernelGradeFunctor p ma mb pa pb).map f) := by
  exact nativeGK4VKernelGrade_injective X.original.2.2 Y.original.2.2

/-- On every actual structural Hom, the two-step Boolean functor
S -> K_Bool -> Bool equals the original GK4I structural grading. -/
theorem nativeGK4VFunctor_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4VKernelGradeFunctor p ma mb pa pb).map
      ((nativeGK4UBoolKernelComparisonFunctor p ma mb pa pb).map f) =
      (nativeGK4IGradingFunctor p ma mb pa pb).map f := by
  exact nativeGK4VComparison_grade X.2.2 Y.2.2 f

/-- Object equality, retaining each original F45 stage until the
final observation target collapses to its sole Boolean object. -/
theorem nativeGK4VFunctor_factor_obj
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    (nativeGK4VKernelGradeFunctor p ma mb pa pb).obj
      ((nativeGK4UBoolKernelComparisonFunctor p ma mb pa pb).obj X) =
      (nativeGK4IGradingFunctor p ma mb pa pb).obj X := by
  rfl

/-- No false reflection of faithfulness: structural comparison is
faithful at X->Y precisely when GK4I Boolean grade is injective there. -/
theorem nativeGK4VFunctor_injective_iff_grade
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4UBoolKernelComparisonFunctor p ma mb pa pb).map f) ↔
      Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4IGradingFunctor p ma mb pa pb).map f) := by
  exact nativeGK4VComparison_injective_iff_grade X.2.2 Y.2.2

section PhysicalSection
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}

/-- An actual LocalRotation provides TWO structural Boolean sections,
but they exhaust every structural class exactly when grading is injective.
Previously proved rightInverse does NOT assert this leftInverse. -/
theorem nativeGK4VSection_exhaustive_iff_grade_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    (∀ s : NativeGK4EStructuralRouteClasses before before,
      nativeGK4GStructuralSection rot
        (nativeGK4GStructuralGrade before before s) = s) ↔
      Function.Injective (nativeGK4GStructuralGrade before before) := by
  constructor
  · intro hall u v hgrade
    calc
      u = nativeGK4GStructuralSection rot
          (nativeGK4GStructuralGrade before before u) := (hall u).symm
      _ = nativeGK4GStructuralSection rot
          (nativeGK4GStructuralGrade before before v) :=
        congrArg (nativeGK4GStructuralSection rot) hgrade
      _ = v := hall v
  · intro hinj s
    apply hinj
    exact nativeGK4GStructuralSection_rightInverse rot
      (nativeGK4GStructuralGrade before before s)

/-- Exact TRUE physical north C60 criterion, not an unconditional
positive/negative assertion about comparison faithfulness. -/
theorem nativeGK4V_physical_north_faithful_iff_section_exhaustive :
    Function.Injective
      (fun f : nativeGK4IPhysicalNorthTripleStage ⟶
          nativeGK4IPhysicalNorthTripleStage =>
        (nativeGK4UBoolKernelComparisonFunctor (.hexagon (.top 0))
          northHexagonNativeFrame.firstAxis northHexagonNativeFrame.firstAxis
          northHexagonNativeFrame.secondAxis northHexagonNativeFrame.secondAxis).map f) ↔
    (∀ s : NativeGK4EStructuralRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      nativeGK4GStructuralSection northHexagonNativeLeftRotation
        (nativeGK4GStructuralGrade
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple s) = s) := by
  change Function.Injective
    (nativeGK4TComparison (nativeGK4OBooleanFamily _ _ _)
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
      (nativeGK4N_boolean_seam_invariant
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple)) ↔ _
  have hgrade := nativeGK4VComparison_injective_iff_grade
    nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
  exact hgrade.trans
    (nativeGK4VSection_exhaustive_iff_grade_injective
      northHexagonNativeLeftRotation).symm

/-- Two REAL source morphisms of differing grades have distinct
Boolean kernel images in the actual C60 physical north context. -/
theorem nativeGK4V_physical_north_two_distinct_kernel_images :
    (nativeGK4UBoolKernelComparisonFunctor (.hexagon (.top 0))
        northHexagonNativeFrame.firstAxis northHexagonNativeFrame.firstAxis
        northHexagonNativeFrame.secondAxis northHexagonNativeFrame.secondAxis).map
      (nativeGK4GStructuralSection northHexagonNativeLeftRotation true) ≠
    (nativeGK4UBoolKernelComparisonFunctor (.hexagon (.top 0))
        northHexagonNativeFrame.firstAxis northHexagonNativeFrame.firstAxis
        northHexagonNativeFrame.secondAxis northHexagonNativeFrame.secondAxis).map
      (nativeGK4GStructuralSection northHexagonNativeLeftRotation false) := by
  intro heq
  have hg :=
    (nativeGK4VComparison_eq_iff_grade
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple _ _).mp heq
  have h : true = false := by
    simpa only [nativeGK4GStructuralSection_rightInverse] using hg
  cases h

end PhysicalSection

#print axioms nativeGK4VKernelGradeFunctor
#print axioms nativeGK4VKernelGradeFunctor_injective_hom
#print axioms nativeGK4VFunctor_factor_map
#print axioms nativeGK4VFunctor_factor_obj
#print axioms nativeGK4VFunctor_injective_iff_grade
#print axioms nativeGK4VSection_exhaustive_iff_grade_injective
#print axioms nativeGK4V_physical_north_faithful_iff_section_exhaustive
#print axioms nativeGK4V_physical_north_two_distinct_kernel_images

end
end Kuu.F112.Physical
