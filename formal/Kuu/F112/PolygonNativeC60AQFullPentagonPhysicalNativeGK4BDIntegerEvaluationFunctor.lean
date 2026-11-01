import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BCPolynomialFunctorAI
import Mathlib.Tactic

/-!
F112-P94D3GK4BD — genuinely original polynomial evaluation
as a family of Mathlib functors, and the exact OLD AH t=4 triangle.

GK4BC already proved that the full genuine F54 polynomial invariant
on the EXISTING second kernel K_AI is a functor into noncommutative
2x2 matrices over Z[X]. For EVERY integer t we construct the
evaluation functor to integer 2x2 matrices, and factor the K_AI
polynomial functor through it. The specialization at the original
AH parameter t=4 is EQUAL as a functor to the actual AH-component
observer of the existing K_AI joint observation.

The original independent structural S still commutes at arbitrary t.
No original Q associativity or units, fabricated Type-valued 3-cell,
source-route equality, polynomial functor faithfulness, Gray, global
strict or hyperdescent is asserted. No claim that all ambient matrices
are attained by actual F54 routes.
Append-only/tighten-only/overwrite-forbidden/same-root107;
strict 空 central, independent Kuu one presentation.
Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 stays Draft/OPEN/unmerged.
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

/-- The ambient one-object category of ALL 2x2 integer matrices,
not the generally proper image of any genuine F54 observation. -/
inductive NativeGK4BDIntegerMatrixPoint : Type where
  | star

instance nativeGK4BDIntegerMatrixCategory :
    Category NativeGK4BDIntegerMatrixPoint where
  Hom _ _ := NativeGK4AHMatrix
  id _ := nativeGK4AHOne
  comp f g := nativeGK4AHMul f g
  id_comp := by
    intro X Y f
    exact nativeGK4AHMul_leftUnit f
  comp_id := by
    intro X Y f
    exact nativeGK4AHMul_rightUnit f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AHMul_assoc f g h

/-- For each integer t, evaluate EVERY entry in the entire polynomial
matrix. Multiplication and identity are preserved in the genuine
noncommutative order, by the preexisting GK4AV Lean theorems. -/
def nativeGK4BDIntegerEvaluationFunctor (t : Int) :
    NativeGK4BCPolynomialValuePoint ⥤ NativeGK4BDIntegerMatrixPoint where
  obj _ := .star
  map := fun {X Y} M => nativeGK4AVPolyEval t M
  map_id := by
    intro X
    exact nativeGK4AVPolyEval_one t
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AVPolyEval_mul t f g

@[simp] theorem nativeGK4BDIntegerEvaluationFunctor_map
    (t : Int) (M : NativeGK4AVValue) :
    (nativeGK4BDIntegerEvaluationFunctor t).map
        (X := .star) (Y := .star) M =
      nativeGK4AVPolyEval t M := rfl

/-- The genuine second-kernel K_AI polynomial functor followed by
evaluation at arbitrary t: categorical composition, not a raw
representative map and not a new quotient. -/
def nativeGK4BDKAIIntegerEvaluationFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : Int) :
    NativeGK4AIKernelStage p ma mb pa pb ⥤
      NativeGK4BDIntegerMatrixPoint :=
  nativeGK4BCPolynomialValueFunctor p ma mb pa pb ⋙
    nativeGK4BDIntegerEvaluationFunctor t

/-- Evaluation of an actual typed K_AI morphism is exactly
evaluation of its existing GK4BB full-polynomial lift. -/
@[simp] theorem nativeGK4BDKAIIntegerEvaluationFunctor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : Int)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t).map f =
      nativeGK4AVPolyEval t
        (nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 f) := rfl

/-- The OLD AH component, not a new invented integer observation,
is a genuine functor on the existing K_AI category: its laws follow
from the ALREADY proved combined K_AI value functor. -/
def nativeGK4BDOldAHFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AIKernelStage p ma mb pa pb ⥤
      NativeGK4BDIntegerMatrixPoint where
  obj _ := .star
  map := fun {X Y} f =>
    (nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 f).2
  map_id := by
    intro X
    change
      (nativeGK4AIKernelValue X.original.2.2 X.original.2.2
        (nativeGK4AIKernelUnit X.original.2.2)).2 = nativeGK4AHOne
    rw [nativeGK4AIKernelValue_unit]
    rfl
  map_comp := by
    intro X Y Z f g
    change
      (nativeGK4AIKernelValue X.original.2.2 Z.original.2.2
        (nativeGK4AIKernelCompose X.original.2.2 Y.original.2.2
          Z.original.2.2 f g)).2 =
        nativeGK4AHMul
          (nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 f).2
          (nativeGK4AIKernelValue Y.original.2.2 Z.original.2.2 g).2
    exact congrArg (fun v : NativeGK4AIValue => v.2)
      (nativeGK4AIKernelValue_compose
        X.original.2.2 Y.original.2.2 Z.original.2.2 f g)

/-- The composite evaluation at t=4 EXACTLY recovers the original
AH-component on each genuine K_AI Hom, not only its matrix determinant,
trace, or raw route string. -/
theorem nativeGK4BDKAIIntegerEvaluation_four_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map f =
      (nativeGK4BDOldAHFunctor p ma mb pa pb).map f := by
  change
    nativeGK4AVPolyEval 4
        (nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 f) =
      (nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 f).2
  exact nativeGK4BBPolynomialOnAI_eval_four
    X.original.2.2 Y.original.2.2 f

/-- The exact t=4 equality is an equality of WHOLE Mathlib functors,
including the values on every dependent Hom and their identity and
composition laws; it is not an equality of source Type-valued paths. -/
theorem nativeGK4BDKAIIntegerEvaluation_four_triangle
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4 =
      nativeGK4BDOldAHFunctor p ma mb pa pb := by
  fapply CategoryTheory.Functor.ext
  · intro X
    rfl
  · intro X Y f
    simpa only [eqToHom_refl, Category.id_comp, Category.comp_id] using
      (nativeGK4BDKAIIntegerEvaluation_four_map p ma mb pa pb X Y f)

/-- The independent structural S is evaluated at ANY integer t
via the genuine K_AI comparison and the already existing original
S-side polynomial family, with no source Type-valued new 3-cell. -/
theorem nativeGK4BDKAIIntegerEvaluation_structural
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : Int)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (s : X ⟶ Y) :
    (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t).map
        ((nativeGK4AIComparisonFunctor p ma mb pa pb).map s) =
      nativeGK4AUStructuralValue X.2.2 Y.2.2 s t := by
  change
    nativeGK4AVPolyEval t
      (nativeGK4BBPolynomialOnAI X.2.2 Y.2.2
        (nativeGK4AIComparison X.2.2 Y.2.2 s)) =
    nativeGK4AUStructuralValue X.2.2 Y.2.2 s t
  rw [nativeGK4BBPolynomialOnAI_structural]
  exact nativeGK4AVStructural_eval X.2.2 Y.2.2 s t

/-- Original AH specialization of the independent S observation,
factored through the same genuine K_AI comparison triangle. -/
theorem nativeGK4BDKAIIntegerEvaluation_four_structural
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (s : X ⟶ Y) :
    (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map
        ((nativeGK4AIComparisonFunctor p ma mb pa pb).map s) =
      nativeGK4AHStructuralValue X.2.2 Y.2.2 s := by
  rw [nativeGK4BDKAIIntegerEvaluation_structural]
  exact (nativeGK4AUStructural_specialize X.2.2 Y.2.2 s).2

#print axioms nativeGK4BDIntegerMatrixCategory
#print axioms nativeGK4BDIntegerEvaluationFunctor
#print axioms nativeGK4BDIntegerEvaluationFunctor_map
#print axioms nativeGK4BDKAIIntegerEvaluationFunctor
#print axioms nativeGK4BDKAIIntegerEvaluationFunctor_map
#print axioms nativeGK4BDOldAHFunctor
#print axioms nativeGK4BDKAIIntegerEvaluation_four_map
#print axioms nativeGK4BDKAIIntegerEvaluation_four_triangle
#print axioms nativeGK4BDKAIIntegerEvaluation_structural
#print axioms nativeGK4BDKAIIntegerEvaluation_four_structural

end
end Kuu.F112.Physical
