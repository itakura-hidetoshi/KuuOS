import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4XEnhancedFunctor
import Mathlib.Tactic

/-!
# F112-P94D3GK4Y — actual enhanced-observer kernel CATEGORY, not ambient values

GK4X established the genuine original P92B observer O_X = (Boolean,castCharge)
and its 3 source F54 composition/context laws, all F54 structural seams,
and the surjection from the SEPARATE GK4E structural quotient S onto
the actual SECOND GK4S quotient K_X of original P92B classes.

Construct a TRUE Mathlib category whose Hom objects are exactly K_X,
NOT the ambient Bool × Int product. Identity is the actual original
P92B zero-edge route's K_X class; its unit laws hold ONLY after the
SECOND quotient, by original observation laws. Associativity holds in
K_X by Bool.and/Int.add and GK4S, WITHOUT source P92B associativity.

The independent GK4I structural category S admits a genuine
hom-surjective comparison functor to the new K_X category. The genuine
second quotient K_X has a faithful observation functor to GK4X's
ambient one-object value category. Their composite agrees pointwise
with GK4X's earlier enhanced structural functor on BOTH objects and
arrows. The classification of source comparison faithfulness is the
exact enhanced structural observer injectivity condition; no
unconditional faithful/equivalence claim.

Q: original P92B source, S: independent structural comparison, K_X:
second observed kernel quotient. Preserve distinct authorities,
all D/E categorical objects, four Blocks, both Nat indices,
all genuine F45 source/target trees and original Type-valued evidence.
Never assert original Q category laws or create a Type-valued 3-cell
from observer equality. No Gray, 107 public roots, append-only same-root.
Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 remains Draft/open/unmerged.
Copyright 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section ActualEnhancedKernelAlgebra

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
variable (t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb)

/-- Genuine K_X identity is the KERNEL CLASS of the ACTUAL original
F54/P92B zero-edge route. Q itself has NO asserted identity law. -/
def nativeGK4YEnhancedKernelUnit :
    NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₁ :=
  nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₁
    (nativeGK4H_p92Unit t₁)

/-- Genuine K_X composition transported from GK4S's attained P92B
observation image; no invented alternative original Q composition. -/
def nativeGK4YEnhancedKernelCompose
    (u : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₂ t₃) :
    NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₃ :=
  nativeGK4SKernelCompose (nativeGK4XEnhancedP92Family p D E)
    nativeGK4XCombine
    (nativeGK4PIdentityAction p D E (Bool × Int))
    (nativeGK4PIdentityAction p D E (Bool × Int))
    nativeGK4XEnhancedLaws t₁ t₂ t₃ u v

/-- Original true P92B composition STRICTLY projects onto the
SECOND enhanced observational quotient, not onto raw proof equality. -/
@[simp] theorem nativeGK4YEnhancedKernelCompose_class
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4YEnhancedKernelCompose t₁ t₂ t₃
      (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ u)
      (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₂ t₃ v) =
    nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₃
      (nativeGK4H_p92Compose t₁ t₂ t₃ u v) :=
  nativeGK4SKernelCompose_class
    (nativeGK4XEnhancedP92Family p D E) nativeGK4XCombine
    (nativeGK4PIdentityAction p D E (Bool × Int))
    (nativeGK4PIdentityAction p D E (Bool × Int))
    nativeGK4XEnhancedLaws t₁ t₂ t₃ u v

/-- Associativity in the genuine SECOND quotient follows from the
Bool×Int VALUE operation, not unproved original Q associativity. -/
theorem nativeGK4YEnhancedKernelCompose_assoc
    (u : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₂ t₃)
    (w : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₃ t₄) :
    nativeGK4YEnhancedKernelCompose t₁ t₃ t₄
        (nativeGK4YEnhancedKernelCompose t₁ t₂ t₃ u v) w =
      nativeGK4YEnhancedKernelCompose t₁ t₂ t₄ u
        (nativeGK4YEnhancedKernelCompose t₂ t₃ t₄ v w) := by
  exact nativeGK4SKernelCompose_assoc
    (nativeGK4XEnhancedP92Family p D E) nativeGK4XCombine
    (nativeGK4PIdentityAction p D E (Bool × Int))
    (nativeGK4PIdentityAction p D E (Bool × Int))
    nativeGK4XEnhancedLaws t₁ t₂ t₃ t₄
    nativeGK4XCombine_assoc u v w

/-- Genuine second-quotient LEFT identity from the real original
Q representative observed as (true,0), without Q identity. -/
theorem nativeGK4YEnhancedKernelCompose_leftUnit
    (u : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂) :
    nativeGK4YEnhancedKernelCompose t₁ t₁ t₂
      (nativeGK4YEnhancedKernelUnit t₁) u = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4YEnhancedKernelCompose t₁ t₁ t₂
      (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₁
        (nativeGK4H_p92Unit t₁))
      (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q) =
    nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q
  rw [nativeGK4YEnhancedKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4XEnhancedP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4XEnhancedP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₁ t₂ (nativeGK4H_p92Unit t₁) q) =
    nativeGK4XEnhancedP92 t₁ t₂ q
  rw [nativeGK4XEnhancedP92_compose t₁ t₁ t₂
    (nativeGK4H_p92Unit t₁) q, nativeGK4XEnhancedP92_unit t₁,
    nativeGK4XCombine_leftUnit]

/-- Genuine second-quotient RIGHT identity, not original Q unitality. -/
theorem nativeGK4YEnhancedKernelCompose_rightUnit
    (u : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂) :
    nativeGK4YEnhancedKernelCompose t₁ t₂ t₂
      u (nativeGK4YEnhancedKernelUnit t₂) = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4YEnhancedKernelCompose t₁ t₂ t₂
      (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q)
      (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₂ t₂
        (nativeGK4H_p92Unit t₂)) =
    nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q
  rw [nativeGK4YEnhancedKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4XEnhancedP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4XEnhancedP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₂ t₂ q (nativeGK4H_p92Unit t₂)) =
    nativeGK4XEnhancedP92 t₁ t₂ q
  rw [nativeGK4XEnhancedP92_compose t₁ t₂ t₂ q
    (nativeGK4H_p92Unit t₂), nativeGK4XEnhancedP92_unit t₂,
    nativeGK4XCombine_rightUnit]

/-- The EXACT observed enhanced value of a SECOND quotient class,
via the genuine GK4S equivalence with the ATTAINED image. -/
def nativeGK4YEnhancedKernelValue
    (z : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂) :
    Bool × Int :=
  (nativeGK4SKernelImageEquiv
      (nativeGK4XEnhancedP92Family p D E) t₁ t₂ z).val

@[simp] theorem nativeGK4YEnhancedKernelValue_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4YEnhancedKernelValue t₁ t₂
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q) =
      nativeGK4XEnhancedP92 t₁ t₂ q := by
  rfl

/-- No two DIFFERENT enhanced kernel classes can share the SAME
value pair: K_X was DEFINED by that kernel. -/
theorem nativeGK4YEnhancedKernelValue_injective :
    Function.Injective (nativeGK4YEnhancedKernelValue t₁ t₂) := by
  intro u v huv
  apply (nativeGK4SKernelImageEquiv
    (nativeGK4XEnhancedP92Family p D E) t₁ t₂).injective
  apply Subtype.ext
  exact huv

@[simp] theorem nativeGK4YEnhancedKernelValue_unit :
    nativeGK4YEnhancedKernelValue t₁ t₁
      (nativeGK4YEnhancedKernelUnit t₁) = (true, 0) := by
  rfl

/-- Genuine K_X composition maps to exactly the original
Bool.and×Int.add product of the ACTUAL attained values. -/
theorem nativeGK4YEnhancedKernelValue_compose
    (u : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4XEnhancedP92Family p D E) t₂ t₃) :
    nativeGK4YEnhancedKernelValue t₁ t₃
      (nativeGK4YEnhancedKernelCompose t₁ t₂ t₃ u v) =
    nativeGK4XCombine
      (nativeGK4YEnhancedKernelValue t₁ t₂ u)
      (nativeGK4YEnhancedKernelValue t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  change nativeGK4YEnhancedKernelValue t₁ t₃
      (nativeGK4YEnhancedKernelCompose t₁ t₂ t₃
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q)
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₂ t₃ r)) =
    nativeGK4XCombine
      (nativeGK4YEnhancedKernelValue t₁ t₂
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₁ t₂ q))
      (nativeGK4YEnhancedKernelValue t₂ t₃
        (nativeGK4SKernelClass (nativeGK4XEnhancedP92Family p D E) t₂ t₃ r))
  rw [nativeGK4YEnhancedKernelCompose_class,
    nativeGK4YEnhancedKernelValue_class,
    nativeGK4YEnhancedKernelValue_class,
    nativeGK4YEnhancedKernelValue_class]
  exact nativeGK4XEnhancedP92_compose t₁ t₂ t₃ q r

end ActualEnhancedKernelAlgebra

/-! ### Genuine separate category on the ACTUAL second quotient. -/

/-- A DIFFERENT object presentation from original GK4I and from
GK4U Boolean kernel target. Avoid conflicting Category instances. -/
structure NativeGK4YEnhancedKernelStage
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) where
  original : NativeGK4IStage p ma mb pa pb

/-- Actual Mathlib CATEGORY whose Hom is the SECOND GK4S quotient
of actual ORIGINAL P92B classes by actual GK4X observation equality. -/
instance nativeGK4YEnhancedKernelCategory
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Category (NativeGK4YEnhancedKernelStage p ma mb pa pb) where
  Hom X Y := NativeGK4SKernelClasses
    (nativeGK4XEnhancedP92Family p D E) X.original.2.2 Y.original.2.2
  id X := nativeGK4YEnhancedKernelUnit X.original.2.2
  comp f g := nativeGK4YEnhancedKernelCompose _ _ _ f g
  id_comp := by
    intro X Y f
    exact nativeGK4YEnhancedKernelCompose_leftUnit
      X.original.2.2 Y.original.2.2 f
  comp_id := by
    intro X Y f
    exact nativeGK4YEnhancedKernelCompose_rightUnit
      X.original.2.2 Y.original.2.2 f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4YEnhancedKernelCompose_assoc
      W.original.2.2 X.original.2.2 Y.original.2.2 Z.original.2.2 f g h

/-- TRUE GK4I structural category -> genuine GK4Y second kernel
category functor; its Hom map is the certified GK4X/GK4T comparison.
This is NOT a functor from original P92B Q. -/
def nativeGK4YEnhancedKernelComparisonFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤
      NativeGK4YEnhancedKernelStage p ma mb pa pb where
  obj X := ⟨X⟩
  map := fun {X Y} f => nativeGK4XEnhancedComparison X.2.2 Y.2.2 f
  map_id := by
    intro X
    change nativeGK4XEnhancedComparison X.2.2 X.2.2
        (nativeGK4H_structuralUnit X.2.2) =
      nativeGK4YEnhancedKernelUnit X.2.2
    exact nativeGK4U_comparison_preserves_unit
      (nativeGK4XEnhancedP92Family p D E)
      X.2.2 (nativeGK4XEnhancedSeamInvariant X.2.2 X.2.2)
  map_comp := by
    intro X Y Z f g
    change nativeGK4XEnhancedComparison X.2.2 Z.2.2
        (nativeGK4H_structuralCompose X.2.2 Y.2.2 Z.2.2 f g) =
      nativeGK4YEnhancedKernelCompose X.2.2 Y.2.2 Z.2.2
        (nativeGK4XEnhancedComparison X.2.2 Y.2.2 f)
        (nativeGK4XEnhancedComparison Y.2.2 Z.2.2 g)
    exact nativeGK4U_comparison_preserves_compose
      (nativeGK4XEnhancedP92Family p D E) nativeGK4XCombine
      (nativeGK4PIdentityAction p D E (Bool × Int))
      (nativeGK4PIdentityAction p D E (Bool × Int))
      nativeGK4XEnhancedLaws X.2.2 Y.2.2 Z.2.2
      (nativeGK4XEnhancedSeamInvariant X.2.2 Y.2.2)
      (nativeGK4XEnhancedSeamInvariant Y.2.2 Z.2.2)
      (nativeGK4XEnhancedSeamInvariant X.2.2 Z.2.2) f g

/-- Every genuine attained enhanced kernel class is hit by a
structural class; certified FULL per Hom, no faithfulness inferred. -/
theorem nativeGK4YComparisonFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).map f) := by
  exact nativeGK4XEnhancedComparison_surjective X.2.2 Y.2.2

/-- The *genuine second kernel quotient* admits a faithful
observational functor into the separate ambient Bool×Int value
category. Its values are the ATTAINED ones; the ambient Hom
need not be exhausted by actual original source routes. -/
def nativeGK4YEnhancedKernelValueFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4YEnhancedKernelStage p ma mb pa pb ⥤ NativeGK4XValuePoint where
  obj _ := .star
  map := fun {X Y} f =>
    nativeGK4YEnhancedKernelValue X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4YEnhancedKernelValue_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4YEnhancedKernelValue_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

/-- The K_X->Bool×Int functor is FAITHFUL on all genuine
source-dependent Hom slots, even when S->K_X is not known faithful. -/
theorem nativeGK4YValueFunctor_injective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4YEnhancedKernelStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4YEnhancedKernelValueFunctor p ma mb pa pb).map f) := by
  exact nativeGK4YEnhancedKernelValue_injective
    X.original.2.2 Y.original.2.2

/-- At ALL actual F45 boundary objects, the real structural->K_X
comparison followed by K_X->Bool×Int faithfully reproduces exactly
the previously constructed GK4X enhanced structural observation. -/
theorem nativeGK4YComparison_value_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4YEnhancedKernelValueFunctor p ma mb pa pb).map
        ((nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).map f) =
      (nativeGK4XValueFunctor p ma mb pa pb).map f := by
  exact nativeGK4XEnhancedComparison_value X.2.2 Y.2.2 f

theorem nativeGK4YComparison_value_factor_obj
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    (nativeGK4YEnhancedKernelValueFunctor p ma mb pa pb).obj
        ((nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).obj X) =
      (nativeGK4XValueFunctor p ma mb pa pb).obj X := by
  rfl

/-- Exact remaining faithfulness criterion: genuine structural S->K_X
functor is injective per-Hom iff the actual enhanced observation is
injective on the same structural Hom. This is NOT an unconditional
unproved assertion of S->K_X global faithfulness. -/
theorem nativeGK4YComparisonFunctor_injective_iff_enhanced
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4YEnhancedKernelComparisonFunctor p ma mb pa pb).map f) ↔
      Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4XValueFunctor p ma mb pa pb).map f) := by
  exact nativeGK4XEnhancedComparison_injective_iff X.2.2 Y.2.2

#print axioms nativeGK4YEnhancedKernelUnit
#print axioms nativeGK4YEnhancedKernelCompose
#print axioms nativeGK4YEnhancedKernelCompose_class
#print axioms nativeGK4YEnhancedKernelCompose_assoc
#print axioms nativeGK4YEnhancedKernelCompose_leftUnit
#print axioms nativeGK4YEnhancedKernelCompose_rightUnit
#print axioms nativeGK4YEnhancedKernelValue
#print axioms nativeGK4YEnhancedKernelValue_class
#print axioms nativeGK4YEnhancedKernelValue_injective
#print axioms nativeGK4YEnhancedKernelValue_unit
#print axioms nativeGK4YEnhancedKernelValue_compose
#print axioms NativeGK4YEnhancedKernelStage
#print axioms nativeGK4YEnhancedKernelCategory
#print axioms nativeGK4YEnhancedKernelComparisonFunctor
#print axioms nativeGK4YComparisonFunctor_surjective_hom
#print axioms nativeGK4YEnhancedKernelValueFunctor
#print axioms nativeGK4YValueFunctor_injective_hom
#print axioms nativeGK4YComparison_value_factor_map
#print axioms nativeGK4YComparison_value_factor_obj
#print axioms nativeGK4YComparisonFunctor_injective_iff_enhanced

end
end Kuu.F112.Physical
