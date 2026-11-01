import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BEEvaluationKernelFactor
import Mathlib.Tactic

/-!
F112-P94D3GK4BF — a category of the ACTUALLY ATTAINED old AH
integer matrices, with genuine typed F54 boundary objects.

GK4BE constructs the witness-bearing AH matrix image separately on
each existing second-kernel K_AI Hom. We now close these actual
images under the original noncommutative integer matrix product and
identity, obtaining a new Mathlib category with the same typed
boundary-object presentation as K_AI, but DIFFERENT Hom types.
The real K_AI -> attained AH functor is surjective on every Hom.
The inclusion into the ambient one-object integer-matrix category is
injective on every Hom (faithful in that exact sense). The composite
is the existing old-AH functor, and arbitrary integer evaluations
factor through the attained AH category by GK4BE's UNIQUE maps.

This does NOT assert that the K_AI -> attained AH functor is faithful.
Its precise local faithfulness condition is classified, not assumed.
No original Q associativity/unit laws, Type-valued new 3-cell,
unattained ambient matrix, Gray or hyperdescent are introduced.

Append-only/tighten-only/overwrite-forbidden/same-root107.
Strict 空 central; independent Kuu one presentation.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 Draft/OPEN/unmerged.
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

section ActualAHHomAlgebra
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- The old AH identity is genuinely attained by the zero route
in the existing second-kernel K_AI quotient. -/
def nativeGK4BFAHUnit : NativeGK4BEAttainedAH t₁ t₁ :=
  nativeGK4BEAttainedAHClass t₁ t₁ (nativeGK4AIKernelUnit t₁)

@[simp] theorem nativeGK4BFAHUnit_val :
    (nativeGK4BFAHUnit t₁).val = nativeGK4AHOne := by
  change (nativeGK4AIKernelValue t₁ t₁
    (nativeGK4AIKernelUnit t₁)).2 = nativeGK4AHOne
  rw [nativeGK4AIKernelValue_unit]
  rfl

/-- Actual old AH images are closed under ordered matrix product:
choose TRUE typed K_AI witnesses and compose them in K_AI, not Q. -/
def nativeGK4BFAHCompose
    (u : NativeGK4BEAttainedAH t₁ t₂)
    (v : NativeGK4BEAttainedAH t₂ t₃) :
    NativeGK4BEAttainedAH t₁ t₃ := by
  refine ⟨nativeGK4AHMul u.val v.val, ?_⟩
  obtain ⟨qu, hu⟩ := u.property
  obtain ⟨qv, hv⟩ := v.property
  refine ⟨nativeGK4AIKernelCompose t₁ t₂ t₃ qu qv, ?_⟩
  have h := congrArg (fun w : NativeGK4AIValue => w.2)
    (nativeGK4AIKernelValue_compose t₁ t₂ t₃ qu qv)
  change
    (nativeGK4AIKernelValue t₁ t₃
      (nativeGK4AIKernelCompose t₁ t₂ t₃ qu qv)).2 =
        nativeGK4AHMul u.val v.val
  calc
    _ = nativeGK4AHMul
        (nativeGK4AIKernelValue t₁ t₂ qu).2
        (nativeGK4AIKernelValue t₂ t₃ qv).2 := h
    _ = nativeGK4AHMul u.val v.val := by rw [hu, hv]

/-- The product of true attained classes is exactly the class of
the actual K_AI composition of their representatives. -/
@[simp] theorem nativeGK4BFAHCompose_class
    (u : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) t₂ t₃) :
    nativeGK4BFAHCompose t₁ t₂ t₃
      (nativeGK4BEAttainedAHClass t₁ t₂ u)
      (nativeGK4BEAttainedAHClass t₂ t₃ v) =
    nativeGK4BEAttainedAHClass t₁ t₃
      (nativeGK4AIKernelCompose t₁ t₂ t₃ u v) := by
  apply Subtype.ext
  change nativeGK4AHMul
      (nativeGK4AIKernelValue t₁ t₂ u).2
      (nativeGK4AIKernelValue t₂ t₃ v).2 =
    (nativeGK4AIKernelValue t₁ t₃
      (nativeGK4AIKernelCompose t₁ t₂ t₃ u v)).2
  exact (congrArg (fun w : NativeGK4AIValue => w.2)
    (nativeGK4AIKernelValue_compose t₁ t₂ t₃ u v)).symm

end ActualAHHomAlgebra

/-- Independent wrapper: same genuine original typed boundary objects,
but morphisms are now witness-bearing ACTUALLY attained AH matrices. -/
structure NativeGK4BFAttainedAHStage
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) where
  original : NativeGK4IStage p ma mb pa pb

/-- A genuine category of typed attained AH matrices, without
assuming original P92B Q itself is a category. -/
instance nativeGK4BFAttainedAHCategory
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Category (NativeGK4BFAttainedAHStage p ma mb pa pb) where
  Hom X Y := NativeGK4BEAttainedAH X.original.2.2 Y.original.2.2
  id X := nativeGK4BFAHUnit X.original.2.2
  comp f g := nativeGK4BFAHCompose _ _ _ f g
  id_comp := by
    intro X Y f
    apply Subtype.ext
    change nativeGK4AHMul
      (nativeGK4BFAHUnit X.original.2.2).val f.val = f.val
    rw [nativeGK4BFAHUnit_val, nativeGK4AHMul_leftUnit]
  comp_id := by
    intro X Y f
    apply Subtype.ext
    change nativeGK4AHMul
      f.val (nativeGK4BFAHUnit Y.original.2.2).val = f.val
    rw [nativeGK4BFAHUnit_val, nativeGK4AHMul_rightUnit]
  assoc := by
    intro W X Y Z f g h
    apply Subtype.ext
    change nativeGK4AHMul (nativeGK4AHMul f.val g.val) h.val =
      nativeGK4AHMul f.val (nativeGK4AHMul g.val h.val)
    exact nativeGK4AHMul_assoc f.val g.val h.val

/-- The true K_AI category maps to the attained AH category.
This quotient-like observation is NOT asserted faithful. -/
def nativeGK4BFImageFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AIKernelStage p ma mb pa pb ⥤
      NativeGK4BFAttainedAHStage p ma mb pa pb where
  obj X := ⟨X.original⟩
  map := fun {X Y} f =>
    nativeGK4BEAttainedAHClass X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z f g
    change nativeGK4BEAttainedAHClass X.original.2.2 Z.original.2.2
        (nativeGK4AIKernelCompose X.original.2.2 Y.original.2.2
          Z.original.2.2 f g) =
      nativeGK4BFAHCompose X.original.2.2 Y.original.2.2
        Z.original.2.2
        (nativeGK4BEAttainedAHClass X.original.2.2 Y.original.2.2 f)
        (nativeGK4BEAttainedAHClass Y.original.2.2 Z.original.2.2 g)
    exact (nativeGK4BFAHCompose_class
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g).symm

/-- The image functor is SURJECTIVE on each ACTUAL typed Hom.
No inverse of original source histories is manufactured. -/
theorem nativeGK4BFImageFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4BFImageFunctor p ma mb pa pb).map f) := by
  exact nativeGK4BEAttainedAHClass_surjective
    X.original.2.2 Y.original.2.2

/-- The category of attained matrices includes in the ambient
integer-matrix category, with no assertion of surjectivity into it. -/
def nativeGK4BFInclusionFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4BFAttainedAHStage p ma mb pa pb ⥤
      NativeGK4BDIntegerMatrixPoint where
  obj _ := .star
  map := fun {X Y} f => f.val
  map_id := by
    intro X
    exact nativeGK4BFAHUnit_val X.original.2.2
  map_comp := by
    intro X Y Z f g
    rfl

/-- Faithfulness of the IMAGE INCLUSION on each Hom comes
from subtype equality, not from faithfulness of K_AI -> AH. -/
theorem nativeGK4BFInclusionFunctor_injective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4BFAttainedAHStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4BFInclusionFunctor p ma mb pa pb).map f) := by
  intro f g h
  apply Subtype.ext
  exact h

/-- The inclusion after the genuine K_AI -> attained image map
recovers exactly the OLD AH observed value of every true Hom. -/
theorem nativeGK4BFInclusion_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4BFInclusionFunctor p ma mb pa pb).map
      ((nativeGK4BFImageFunctor p ma mb pa pb).map f) =
        (nativeGK4BDOldAHFunctor p ma mb pa pb).map f := rfl

/-- This is an exact equation of WHOLE Mathlib functors, with
dependent Hom transports normalized rather than ignored. -/
theorem nativeGK4BFInclusion_factor_functor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BFImageFunctor p ma mb pa pb ⋙
      nativeGK4BFInclusionFunctor p ma mb pa pb =
        nativeGK4BDOldAHFunctor p ma mb pa pb := by
  fapply CategoryTheory.Functor.ext
  · intro X
    rfl
  · intro X Y f
    simpa only [eqToHom_refl, Category.id_comp, Category.comp_id] using
      (nativeGK4BFInclusion_factor_map p ma mb pa pb X Y f)

/-- Exact obstruction criterion: the K_AI -> AH image map is
injective on a particular Hom iff AH equality detects the actual
K_AI Hom equality. Neither direction is asserted globally. -/
theorem nativeGK4BFImageFunctor_injective_hom_iff
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4BFImageFunctor p ma mb pa pb).map f) ↔
    (∀ u v : X ⟶ Y,
      (nativeGK4BDOldAHFunctor p ma mb pa pb).map u =
        (nativeGK4BDOldAHFunctor p ma mb pa pb).map v → u = v) := by
  constructor
  · intro hinj u v h
    apply hinj
    apply Subtype.ext
    exact h
  · intro h u v huv
    apply h u v
    exact congrArg Subtype.val huv

/-- The UNIQUE GK4BE evaluation of the genuinely attained AH
value is the Hom map of a real functor at each integer t. -/
def nativeGK4BFAttainedEvaluationFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : Int) :
    NativeGK4BFAttainedAHStage p ma mb pa pb ⥤
      NativeGK4BDIntegerMatrixPoint where
  obj _ := .star
  map := fun {X Y} z =>
    nativeGK4BEAttainedEval X.original.2.2 Y.original.2.2 t z
  map_id := by
    intro X
    change nativeGK4BEAttainedEval X.original.2.2 X.original.2.2 t
      (nativeGK4BEAttainedAHClass X.original.2.2 X.original.2.2
        (nativeGK4AIKernelUnit X.original.2.2)) = nativeGK4AHOne
    rw [nativeGK4BEAttainedEval_class, nativeGK4BCPolynomialOnAI_unit,
      nativeGK4AVPolyEval_one]
  map_comp := by
    intro X Y Z f g
    obtain ⟨u, rfl⟩ := nativeGK4BEAttainedAHClass_surjective
      X.original.2.2 Y.original.2.2 f
    obtain ⟨v, rfl⟩ := nativeGK4BEAttainedAHClass_surjective
      Y.original.2.2 Z.original.2.2 g
    change nativeGK4BEAttainedEval X.original.2.2 Z.original.2.2 t
        (nativeGK4BFAHCompose X.original.2.2 Y.original.2.2
          Z.original.2.2
          (nativeGK4BEAttainedAHClass X.original.2.2 Y.original.2.2 u)
          (nativeGK4BEAttainedAHClass Y.original.2.2 Z.original.2.2 v)) =
      nativeGK4AHMul
        (nativeGK4BEAttainedEval X.original.2.2 Y.original.2.2 t
          (nativeGK4BEAttainedAHClass X.original.2.2 Y.original.2.2 u))
        (nativeGK4BEAttainedEval Y.original.2.2 Z.original.2.2 t
          (nativeGK4BEAttainedAHClass Y.original.2.2 Z.original.2.2 v))
    rw [nativeGK4BFAHCompose_class,
      nativeGK4BEAttainedEval_class, nativeGK4BEAttainedEval_class,
      nativeGK4BEAttainedEval_class]
    exact nativeGK4BCPolynomialOnAI_eval_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 t u v

/-- At the ORIGINAL parameter t=4 the attained-image integer
evaluation is exactly the faithful ambient inclusion. -/
theorem nativeGK4BFAttainedEvaluation_four
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BFAttainedEvaluationFunctor p ma mb pa pb 4 =
      nativeGK4BFInclusionFunctor p ma mb pa pb := by
  fapply CategoryTheory.Functor.ext
  · intro X
    rfl
  · intro X Y f
    simpa only [eqToHom_refl, Category.id_comp, Category.comp_id] using
      (nativeGK4BEAttainedEval_four X.original.2.2 Y.original.2.2 f)

/-- Arbitrary integer evaluation of the original K_AI family
factors through its ACTUALLY ATTAINED AH-image category. -/
theorem nativeGK4BFAttainedEvaluation_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : Int)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4BFAttainedEvaluationFunctor p ma mb pa pb t).map
      ((nativeGK4BFImageFunctor p ma mb pa pb).map f) =
        (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t).map f := by
  change nativeGK4BEAttainedEval X.original.2.2 Y.original.2.2 t
    (nativeGK4BEAttainedAHClass X.original.2.2 Y.original.2.2 f) =
      nativeGK4AVPolyEval t
        (nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 f)
  exact nativeGK4BEAttainedEval_class
    X.original.2.2 Y.original.2.2 t f

/-- A true equality of functors, not only a single representative
calculation, extends the GK4BE image factorization to every t. -/
theorem nativeGK4BFAttainedEvaluation_factor_functor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : Int) :
    nativeGK4BFImageFunctor p ma mb pa pb ⋙
      nativeGK4BFAttainedEvaluationFunctor p ma mb pa pb t =
        nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t := by
  fapply CategoryTheory.Functor.ext
  · intro X
    rfl
  · intro X Y f
    simpa only [eqToHom_refl, Category.id_comp, Category.comp_id] using
      (nativeGK4BFAttainedEvaluation_factor_map
        p ma mb pa pb t X Y f)

#print axioms nativeGK4BFAHUnit
#print axioms nativeGK4BFAHUnit_val
#print axioms nativeGK4BFAHCompose
#print axioms nativeGK4BFAHCompose_class
#print axioms nativeGK4BFAttainedAHCategory
#print axioms nativeGK4BFImageFunctor
#print axioms nativeGK4BFImageFunctor_surjective_hom
#print axioms nativeGK4BFInclusionFunctor
#print axioms nativeGK4BFInclusionFunctor_injective_hom
#print axioms nativeGK4BFInclusion_factor_map
#print axioms nativeGK4BFInclusion_factor_functor
#print axioms nativeGK4BFImageFunctor_injective_hom_iff
#print axioms nativeGK4BFAttainedEvaluationFunctor
#print axioms nativeGK4BFAttainedEvaluation_four
#print axioms nativeGK4BFAttainedEvaluation_factor_map
#print axioms nativeGK4BFAttainedEvaluation_factor_functor

end
end Kuu.F112.Physical
