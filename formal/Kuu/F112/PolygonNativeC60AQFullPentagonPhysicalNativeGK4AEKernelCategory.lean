import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEComparison
import Mathlib.Tactic

/-!
F112-P94D3GK4AE — the GENUINE second four-observation quotient category.

K_AA is the real GK4S equality-kernel quotient of ORIGINAL P92B
source-existence classes by the true triple (Boolean grade, signed cast
charge, actual backward rotation count), not a raw observer category.
Its associative/unital composition is transported through attained
observations, not through the unproved original P92B quotient category.
The separately constructed structural S category maps to K_AA by an
actual Hom-surjective Mathlib functor; K_AA maps faithfully to the
ambient triple-value category. Global S->K_AA faithfulness is NOT claimed.

This is an append-only four-component generalization of the certified
GK4Y second-quotient construction; there are no changed older proofs.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6. No Gray.
Public roots 107 and protected validation-only PR #1558 unchanged.
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

/-- Genuine K_AE identity is the KERNEL CLASS of the ACTUAL original
F54/P92B zero-edge route. Q itself has NO asserted identity law. -/
def nativeGK4AEEnhancedKernelUnit :
    NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₁ :=
  nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₁
    (nativeGK4H_p92Unit t₁)

/-- Genuine K_AE composition transported from GK4S's attained P92B
observation image; no invented alternative original Q composition. -/
def nativeGK4AEEnhancedKernelCompose
    (u : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₂ t₃) :
    NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₃ :=
  nativeGK4SKernelCompose (nativeGK4AEQuadP92Family p D E)
    nativeGK4AECombine
    (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
    (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
    nativeGK4AEQuadLaws t₁ t₂ t₃ u v

/-- Original true P92B composition STRICTLY projects onto the
SECOND enhanced observational quotient, not onto raw proof equality. -/
@[simp] theorem nativeGK4AEEnhancedKernelCompose_class
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4AEEnhancedKernelCompose t₁ t₂ t₃
      (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ u)
      (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₂ t₃ v) =
    nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₃
      (nativeGK4H_p92Compose t₁ t₂ t₃ u v) :=
  nativeGK4SKernelCompose_class
    (nativeGK4AEQuadP92Family p D E) nativeGK4AECombine
    (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
    (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
    nativeGK4AEQuadLaws t₁ t₂ t₃ u v

/-- Associativity in the genuine SECOND quotient follows from the
noncommutative Bool×Heisenberg value operation, not unproved original Q associativity. -/
theorem nativeGK4AEEnhancedKernelCompose_assoc
    (u : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₂ t₃)
    (w : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₃ t₄) :
    nativeGK4AEEnhancedKernelCompose t₁ t₃ t₄
        (nativeGK4AEEnhancedKernelCompose t₁ t₂ t₃ u v) w =
      nativeGK4AEEnhancedKernelCompose t₁ t₂ t₄ u
        (nativeGK4AEEnhancedKernelCompose t₂ t₃ t₄ v w) := by
  exact nativeGK4SKernelCompose_assoc
    (nativeGK4AEQuadP92Family p D E) nativeGK4AECombine
    (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
    (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
    nativeGK4AEQuadLaws t₁ t₂ t₃ t₄
    nativeGK4AECombine_assoc u v w

/-- Genuine second-quotient LEFT identity from the real original
Q representative observed as (true,0), without Q identity. -/
theorem nativeGK4AEEnhancedKernelCompose_leftUnit
    (u : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₂) :
    nativeGK4AEEnhancedKernelCompose t₁ t₁ t₂
      (nativeGK4AEEnhancedKernelUnit t₁) u = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4AEEnhancedKernelCompose t₁ t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₁
        (nativeGK4H_p92Unit t₁))
      (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q) =
    nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q
  rw [nativeGK4AEEnhancedKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4AEQuadP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4AEQuadP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₁ t₂ (nativeGK4H_p92Unit t₁) q) =
    nativeGK4AEQuadP92 t₁ t₂ q
  rw [nativeGK4AEQuadP92_compose t₁ t₁ t₂
    (nativeGK4H_p92Unit t₁) q, nativeGK4AEQuadP92_unit t₁,
    nativeGK4AECombine_leftUnit]

/-- Genuine second-quotient RIGHT identity, not original Q unitality. -/
theorem nativeGK4AEEnhancedKernelCompose_rightUnit
    (u : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₂) :
    nativeGK4AEEnhancedKernelCompose t₁ t₂ t₂
      u (nativeGK4AEEnhancedKernelUnit t₂) = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4AEEnhancedKernelCompose t₁ t₂ t₂
      (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q)
      (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₂ t₂
        (nativeGK4H_p92Unit t₂)) =
    nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q
  rw [nativeGK4AEEnhancedKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4AEQuadP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4AEQuadP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₂ t₂ q (nativeGK4H_p92Unit t₂)) =
    nativeGK4AEQuadP92 t₁ t₂ q
  rw [nativeGK4AEQuadP92_compose t₁ t₂ t₂ q
    (nativeGK4H_p92Unit t₂), nativeGK4AEQuadP92_unit t₂,
    nativeGK4AECombine_rightUnit]

/-- The EXACT observed enhanced value of a SECOND quotient class,
via the genuine GK4S equivalence with the ATTAINED image. -/
def nativeGK4AEEnhancedKernelValue
    (z : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₂) :
    NativeGK4AEValue :=
  (nativeGK4SKernelImageEquiv
      (nativeGK4AEQuadP92Family p D E) t₁ t₂ z).val

@[simp] theorem nativeGK4AEEnhancedKernelValue_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4AEEnhancedKernelValue t₁ t₂
        (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q) =
      nativeGK4AEQuadP92 t₁ t₂ q := by
  rfl

/-- No two DIFFERENT enhanced kernel classes can share the SAME
value pair: K_AE was DEFINED by that kernel. -/
theorem nativeGK4AEEnhancedKernelValue_injective :
    Function.Injective (nativeGK4AEEnhancedKernelValue t₁ t₂) := by
  intro u v huv
  apply (nativeGK4SKernelImageEquiv
    (nativeGK4AEQuadP92Family p D E) t₁ t₂).injective
  apply Subtype.ext
  exact huv

@[simp] theorem nativeGK4AEEnhancedKernelValue_unit :
    nativeGK4AEEnhancedKernelValue t₁ t₁
      (nativeGK4AEEnhancedKernelUnit t₁) = nativeGK4AEUnit := by
  rfl

/-- Genuine K_AE composition maps to exactly the original
Bool.and×Int.add product of the ACTUAL attained values. -/
theorem nativeGK4AEEnhancedKernelValue_compose
    (u : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AEQuadP92Family p D E) t₂ t₃) :
    nativeGK4AEEnhancedKernelValue t₁ t₃
      (nativeGK4AEEnhancedKernelCompose t₁ t₂ t₃ u v) =
    nativeGK4AECombine
      (nativeGK4AEEnhancedKernelValue t₁ t₂ u)
      (nativeGK4AEEnhancedKernelValue t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  change nativeGK4AEEnhancedKernelValue t₁ t₃
      (nativeGK4AEEnhancedKernelCompose t₁ t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q)
        (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₂ t₃ r)) =
    nativeGK4AECombine
      (nativeGK4AEEnhancedKernelValue t₁ t₂
        (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₁ t₂ q))
      (nativeGK4AEEnhancedKernelValue t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E) t₂ t₃ r))
  rw [nativeGK4AEEnhancedKernelCompose_class,
    nativeGK4AEEnhancedKernelValue_class,
    nativeGK4AEEnhancedKernelValue_class,
    nativeGK4AEEnhancedKernelValue_class]
  exact nativeGK4AEQuadP92_compose t₁ t₂ t₃ q r

end ActualEnhancedKernelAlgebra

/-! ### Genuine separate category on the ACTUAL second quotient. -/

/-- A DIFFERENT object presentation from original GK4I and from
GK4U Boolean kernel target. Avoid conflicting Category instances. -/
structure NativeGK4AEEnhancedKernelStage
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) where
  original : NativeGK4IStage p ma mb pa pb

/-- Actual Mathlib CATEGORY whose Hom is the SECOND GK4S quotient
of actual ORIGINAL P92B classes by actual GK4AE observation equality. -/
instance nativeGK4AEEnhancedKernelCategory
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Category (NativeGK4AEEnhancedKernelStage p ma mb pa pb) where
  Hom X Y := NativeGK4SKernelClasses
    (nativeGK4AEQuadP92Family p D E) X.original.2.2 Y.original.2.2
  id X := nativeGK4AEEnhancedKernelUnit X.original.2.2
  comp f g := nativeGK4AEEnhancedKernelCompose _ _ _ f g
  id_comp := by
    intro X Y f
    exact nativeGK4AEEnhancedKernelCompose_leftUnit
      X.original.2.2 Y.original.2.2 f
  comp_id := by
    intro X Y f
    exact nativeGK4AEEnhancedKernelCompose_rightUnit
      X.original.2.2 Y.original.2.2 f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AEEnhancedKernelCompose_assoc
      W.original.2.2 X.original.2.2 Y.original.2.2 Z.original.2.2 f g h

/-- TRUE GK4I structural category -> genuine GK4AE second kernel
category functor; its Hom map is the certified GK4AE/GK4T comparison.
This is NOT a functor from original P92B Q. -/
def nativeGK4AEEnhancedKernelComparisonFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤
      NativeGK4AEEnhancedKernelStage p ma mb pa pb where
  obj X := ⟨X⟩
  map := fun {X Y} f => nativeGK4AEQuadComparison X.2.2 Y.2.2 f
  map_id := by
    intro X
    change nativeGK4AEQuadComparison X.2.2 X.2.2
        (nativeGK4H_structuralUnit X.2.2) =
      nativeGK4AEEnhancedKernelUnit X.2.2
    exact nativeGK4U_comparison_preserves_unit
      (nativeGK4AEQuadP92Family p D E)
      X.2.2 (nativeGK4AEQuadSeamInvariant X.2.2 X.2.2)
  map_comp := by
    intro X Y Z f g
    change nativeGK4AEQuadComparison X.2.2 Z.2.2
        (nativeGK4H_structuralCompose X.2.2 Y.2.2 Z.2.2 f g) =
      nativeGK4AEEnhancedKernelCompose X.2.2 Y.2.2 Z.2.2
        (nativeGK4AEQuadComparison X.2.2 Y.2.2 f)
        (nativeGK4AEQuadComparison Y.2.2 Z.2.2 g)
    exact nativeGK4U_comparison_preserves_compose
      (nativeGK4AEQuadP92Family p D E) nativeGK4AECombine
      (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
      (nativeGK4PIdentityAction p D E (NativeGK4AEValue))
      nativeGK4AEQuadLaws X.2.2 Y.2.2 Z.2.2
      (nativeGK4AEQuadSeamInvariant X.2.2 Y.2.2)
      (nativeGK4AEQuadSeamInvariant Y.2.2 Z.2.2)
      (nativeGK4AEQuadSeamInvariant X.2.2 Z.2.2) f g

/-- Every genuine attained enhanced kernel class is hit by a
structural class; certified FULL per Hom, no faithfulness inferred. -/
theorem nativeGK4AEComparisonFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4AEEnhancedKernelComparisonFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AEQuadComparison_surjective X.2.2 Y.2.2

/-- The *genuine second kernel quotient* admits a faithful
observational functor into the separate ambient Bool×Int value
category. Its values are the ATTAINED ones; the ambient Hom
need not be exhausted by actual original source routes. -/
def nativeGK4AEEnhancedKernelValueFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AEEnhancedKernelStage p ma mb pa pb ⥤ NativeGK4AEValuePoint where
  obj _ := .star
  map := fun {X Y} f =>
    nativeGK4AEEnhancedKernelValue X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4AEEnhancedKernelValue_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AEEnhancedKernelValue_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

/-- The K_AE->Bool×Int functor is FAITHFUL on all genuine
source-dependent Hom slots, even when S->K_AE is not known faithful. -/
theorem nativeGK4AEValueFunctor_injective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AEEnhancedKernelStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4AEEnhancedKernelValueFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AEEnhancedKernelValue_injective
    X.original.2.2 Y.original.2.2

/-- At ALL actual F45 boundary objects, the real structural->K_AE
comparison followed by K_AE->Bool×Int faithfully reproduces exactly
the previously constructed GK4AE enhanced structural observation. -/
theorem nativeGK4AEComparison_value_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4AEEnhancedKernelValueFunctor p ma mb pa pb).map
        ((nativeGK4AEEnhancedKernelComparisonFunctor p ma mb pa pb).map f) =
      (nativeGK4AEValueFunctor p ma mb pa pb).map f := by
  exact nativeGK4AEQuadComparison_value X.2.2 Y.2.2 f

theorem nativeGK4AEComparison_value_factor_obj
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    (nativeGK4AEEnhancedKernelValueFunctor p ma mb pa pb).obj
        ((nativeGK4AEEnhancedKernelComparisonFunctor p ma mb pa pb).obj X) =
      (nativeGK4AEValueFunctor p ma mb pa pb).obj X := by
  rfl

/-- Exact remaining faithfulness criterion: genuine structural S->K_AE
functor is injective per-Hom iff the actual enhanced observation is
injective on the same structural Hom. This is NOT an unconditional
unproved assertion of S->K_AE global faithfulness. -/
theorem nativeGK4AEComparisonFunctor_injective_iff_enhanced
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4AEEnhancedKernelComparisonFunctor p ma mb pa pb).map f) ↔
      Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4AEValueFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AEQuadComparison_injective_iff X.2.2 Y.2.2

#print axioms nativeGK4AEEnhancedKernelUnit
#print axioms nativeGK4AEEnhancedKernelCompose
#print axioms nativeGK4AEEnhancedKernelCompose_class
#print axioms nativeGK4AEEnhancedKernelCompose_assoc
#print axioms nativeGK4AEEnhancedKernelCompose_leftUnit
#print axioms nativeGK4AEEnhancedKernelCompose_rightUnit
#print axioms nativeGK4AEEnhancedKernelValue
#print axioms nativeGK4AEEnhancedKernelValue_class
#print axioms nativeGK4AEEnhancedKernelValue_injective
#print axioms nativeGK4AEEnhancedKernelValue_unit
#print axioms nativeGK4AEEnhancedKernelValue_compose
#print axioms NativeGK4AEEnhancedKernelStage
#print axioms nativeGK4AEEnhancedKernelCategory
#print axioms nativeGK4AEEnhancedKernelComparisonFunctor
#print axioms nativeGK4AEComparisonFunctor_surjective_hom
#print axioms nativeGK4AEEnhancedKernelValueFunctor
#print axioms nativeGK4AEValueFunctor_injective_hom
#print axioms nativeGK4AEComparison_value_factor_map
#print axioms nativeGK4AEComparison_value_factor_obj
#print axioms nativeGK4AEComparisonFunctor_injective_iff_enhanced

end
end Kuu.F112.Physical
