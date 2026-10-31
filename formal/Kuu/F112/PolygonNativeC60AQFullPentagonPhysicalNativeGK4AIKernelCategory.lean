import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIProductObservation
import Mathlib.Tactic

/-!
F112-P94D3GK4AI — the genuine independent second kernel category
of original fully typed P92B witness-existence classes Q under the
combined three-factor observation O_AI=(O_AE,M_AF,M_AH).
The category structure is transported through the ATTAINED image
of the true Q source via the certified GK4S kernel equivalence.
This uses no asserted original Q associativity or identities.
The true independent structural S maps into the new K_AI category
by an actual Mathlib Functor, surjective on every Hom.
The K_AI -> attained joint value category Functor is faithful by
kernel definition; this is NOT a claim that S -> K_AI is faithful.
True F54 double-Nat casts, LocalRotations, two typed contexts,
all original F55/P92B cells and original 14 seams retained.
Append-only; strict 空 central; independent Kuu one presentation;
no Gray or hyperdescent; 107 public roots; protect #1558.
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
def nativeGK4AIKernelUnit :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₁ :=
  nativeGK4SKernelClass (nativeGK4AIP92Family p D E)
    t₁ t₁ (nativeGK4H_p92Unit t₁)

/-- Actual second quotient transport along the attained joint image. -/
def nativeGK4AIKernelCompose
    (u : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₂ t₃) :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₃ :=
  nativeGK4SKernelCompose
    (nativeGK4AIP92Family p D E) nativeGK4AICombine
    (nativeGK4PIdentityAction p D E NativeGK4AIValue)
    (nativeGK4PIdentityAction p D E NativeGK4AIValue)
    nativeGK4AILaws t₁ t₂ t₃ u v

@[simp] theorem nativeGK4AIKernelCompose_class
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4AIKernelCompose t₁ t₂ t₃
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ u)
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₂ t₃ v) =
    nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₃
      (nativeGK4H_p92Compose t₁ t₂ t₃ u v) :=
  nativeGK4SKernelCompose_class
    (nativeGK4AIP92Family p D E) nativeGK4AICombine
    (nativeGK4PIdentityAction p D E NativeGK4AIValue)
    (nativeGK4PIdentityAction p D E NativeGK4AIValue)
    nativeGK4AILaws t₁ t₂ t₃ u v

theorem nativeGK4AIKernelCompose_assoc
    (u : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₂ t₃)
    (w : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₃ t₄) :
    nativeGK4AIKernelCompose t₁ t₃ t₄
        (nativeGK4AIKernelCompose t₁ t₂ t₃ u v) w =
      nativeGK4AIKernelCompose t₁ t₂ t₄ u
        (nativeGK4AIKernelCompose t₂ t₃ t₄ v w) := by
  exact nativeGK4SKernelCompose_assoc
    (nativeGK4AIP92Family p D E) nativeGK4AICombine
    (nativeGK4PIdentityAction p D E NativeGK4AIValue)
    (nativeGK4PIdentityAction p D E NativeGK4AIValue)
    nativeGK4AILaws t₁ t₂ t₃ t₄
    nativeGK4AICombine_assoc u v w

theorem nativeGK4AIKernelCompose_leftUnit
    (u : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂) :
    nativeGK4AIKernelCompose t₁ t₁ t₂
      (nativeGK4AIKernelUnit t₁) u = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4AIKernelCompose t₁ t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₁
        (nativeGK4H_p92Unit t₁))
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q) =
    nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q
  rw [nativeGK4AIKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4AIP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4AIP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₁ t₂ (nativeGK4H_p92Unit t₁) q) =
    nativeGK4AIP92 t₁ t₂ q
  rw [nativeGK4AIP92_compose t₁ t₁ t₂ (nativeGK4H_p92Unit t₁) q,
    nativeGK4AIP92_unit t₁, nativeGK4AICombine_leftUnit]

theorem nativeGK4AIKernelCompose_rightUnit
    (u : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂) :
    nativeGK4AIKernelCompose t₁ t₂ t₂
      u (nativeGK4AIKernelUnit t₂) = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro q
  change nativeGK4AIKernelCompose t₁ t₂ t₂
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q)
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₂ t₂
        (nativeGK4H_p92Unit t₂)) =
    nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q
  rw [nativeGK4AIKernelCompose_class]
  apply (nativeGK4SKernelClass_eq_iff
    (nativeGK4AIP92Family p D E) t₁ t₂ _ _).mpr
  change nativeGK4AIP92 t₁ t₂
      (nativeGK4H_p92Compose t₁ t₂ t₂ q (nativeGK4H_p92Unit t₂)) =
    nativeGK4AIP92 t₁ t₂ q
  rw [nativeGK4AIP92_compose t₁ t₂ t₂ q (nativeGK4H_p92Unit t₂),
    nativeGK4AIP92_unit t₂, nativeGK4AICombine_rightUnit]

/-- Evaluation of SECOND K_AG classes at the actually attained
joint value; not a fabricated arbitrary value. -/
def nativeGK4AIKernelValue
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂) :
    NativeGK4AIValue :=
  (nativeGK4SKernelImageEquiv
    (nativeGK4AIP92Family p D E) t₁ t₂ z).val

@[simp] theorem nativeGK4AIKernelValue_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4AIKernelValue t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q) =
        nativeGK4AIP92 t₁ t₂ q := rfl

theorem nativeGK4AIKernelValue_injective :
    Function.Injective (nativeGK4AIKernelValue t₁ t₂) := by
  intro u v h
  apply (nativeGK4SKernelImageEquiv
    (nativeGK4AIP92Family p D E) t₁ t₂).injective
  exact Subtype.ext h

@[simp] theorem nativeGK4AIKernelValue_unit :
    nativeGK4AIKernelValue t₁ t₁
      (nativeGK4AIKernelUnit t₁) = nativeGK4AIUnit := rfl

theorem nativeGK4AIKernelValue_compose
    (u : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₂ t₃) :
    nativeGK4AIKernelValue t₁ t₃
      (nativeGK4AIKernelCompose t₁ t₂ t₃ u v) =
        nativeGK4AICombine
          (nativeGK4AIKernelValue t₁ t₂ u)
          (nativeGK4AIKernelValue t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  change nativeGK4AIKernelValue t₁ t₃
      (nativeGK4AIKernelCompose t₁ t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q)
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₂ t₃ r)) =
    nativeGK4AICombine
      (nativeGK4AIKernelValue t₁ t₂
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₁ t₂ q))
      (nativeGK4AIKernelValue t₂ t₃
        (nativeGK4SKernelClass (nativeGK4AIP92Family p D E) t₂ t₃ r))
  rw [nativeGK4AIKernelCompose_class,
    nativeGK4AIKernelValue_class, nativeGK4AIKernelValue_class,
    nativeGK4AIKernelValue_class]
  exact nativeGK4AIP92_compose t₁ t₂ t₃ q r

/-- GENUINE structurally descended S->K_AG local comparison. -/
def nativeGK4AIComparison :
    NativeGK4EStructuralRouteClasses t₁ t₂ →
      NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) t₁ t₂ :=
  nativeGK4TComparison (nativeGK4AIP92Family p D E)
    t₁ t₂ (nativeGK4AISeamInvariant t₁ t₂)

theorem nativeGK4AIComparison_value
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AIKernelValue t₁ t₂
      (nativeGK4AIComparison t₁ t₂ s) =
      nativeGK4AIStructural t₁ t₂ s := by
  obtain ⟨q, rfl⟩ := nativeGK4EP92ToStructural_surjective t₁ t₂ s
  simpa only [nativeGK4AIComparison, nativeGK4TComparison_class,
    nativeGK4AIKernelValue_class] using
    (nativeGK4AI_commutes t₁ t₂ q).symm

theorem nativeGK4AIComparison_eq_iff
    (u v : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AIComparison t₁ t₂ u =
      nativeGK4AIComparison t₁ t₂ v ↔
    nativeGK4AIStructural t₁ t₂ u =
      nativeGK4AIStructural t₁ t₂ v := by
  constructor
  · intro h
    simpa only [nativeGK4AIComparison_value] using
      congrArg (nativeGK4AIKernelValue t₁ t₂) h
  · intro h
    apply nativeGK4AIKernelValue_injective t₁ t₂
    simpa only [nativeGK4AIComparison_value] using h

theorem nativeGK4AIComparison_surjective :
    Function.Surjective (nativeGK4AIComparison t₁ t₂) := by
  exact nativeGK4TComparison_surjective
    (nativeGK4AIP92Family p D E) t₁ t₂
    (nativeGK4AISeamInvariant t₁ t₂)

end GenuineJointSecondKernel

/-- Separate typed objects from original Q, independent S and
existing four-coordinate K_AE. -/
structure NativeGK4AIKernelStage
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) where
  original : NativeGK4IStage p ma mb pa pb

instance nativeGK4AIKernelCategory
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Category (NativeGK4AIKernelStage p ma mb pa pb) where
  Hom X Y := NativeGK4SKernelClasses
    (nativeGK4AIP92Family p D E) X.original.2.2 Y.original.2.2
  id X := nativeGK4AIKernelUnit X.original.2.2
  comp f g := nativeGK4AIKernelCompose _ _ _ f g
  id_comp := by
    intro X Y f
    exact nativeGK4AIKernelCompose_leftUnit
      X.original.2.2 Y.original.2.2 f
  comp_id := by
    intro X Y f
    exact nativeGK4AIKernelCompose_rightUnit
      X.original.2.2 Y.original.2.2 f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AIKernelCompose_assoc
      W.original.2.2 X.original.2.2 Y.original.2.2 Z.original.2.2 f g h

/-- Actual structural category S -> independent refined second K_AG.
S faithfulness is NOT asserted. -/
def nativeGK4AIComparisonFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤
      NativeGK4AIKernelStage p ma mb pa pb where
  obj X := ⟨X⟩
  map := fun {X Y} f => nativeGK4AIComparison X.2.2 Y.2.2 f
  map_id := by
    intro X
    change nativeGK4AIComparison X.2.2 X.2.2
        (nativeGK4H_structuralUnit X.2.2) =
      nativeGK4AIKernelUnit X.2.2
    exact nativeGK4U_comparison_preserves_unit
      (nativeGK4AIP92Family p D E) X.2.2
      (nativeGK4AISeamInvariant X.2.2 X.2.2)
  map_comp := by
    intro X Y Z f g
    change nativeGK4AIComparison X.2.2 Z.2.2
        (nativeGK4H_structuralCompose X.2.2 Y.2.2 Z.2.2 f g) =
      nativeGK4AIKernelCompose X.2.2 Y.2.2 Z.2.2
        (nativeGK4AIComparison X.2.2 Y.2.2 f)
        (nativeGK4AIComparison Y.2.2 Z.2.2 g)
    exact nativeGK4U_comparison_preserves_compose
      (nativeGK4AIP92Family p D E) nativeGK4AICombine
      (nativeGK4PIdentityAction p D E NativeGK4AIValue)
      (nativeGK4PIdentityAction p D E NativeGK4AIValue)
      nativeGK4AILaws X.2.2 Y.2.2 Z.2.2
      (nativeGK4AISeamInvariant X.2.2 Y.2.2)
      (nativeGK4AISeamInvariant Y.2.2 Z.2.2)
      (nativeGK4AISeamInvariant X.2.2 Z.2.2) f g

theorem nativeGK4AIComparisonFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4AIComparisonFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AIComparison_surjective X.2.2 Y.2.2

/-- Single-object ambient category of ALL joint values, distinct
from the attained image and genuine original source Hom types. -/
inductive NativeGK4AIValuePoint : Type where
  | star

instance nativeGK4AIValueCategory : Category NativeGK4AIValuePoint where
  Hom _ _ := NativeGK4AIValue
  id _ := nativeGK4AIUnit
  comp u v := nativeGK4AICombine u v
  id_comp := by
    intro X Y f
    exact nativeGK4AICombine_leftUnit f
  comp_id := by
    intro X Y f
    exact nativeGK4AICombine_rightUnit f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AICombine_assoc f g h

/-- Actual attained joint-value embedding: faithful BY THE KERNEL
DEFINITION, not by assuming S faithfully maps to K_AG. -/
def nativeGK4AIKernelValueFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AIKernelStage p ma mb pa pb ⥤ NativeGK4AIValuePoint where
  obj _ := .star
  map := fun {X Y} f =>
    nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4AIKernelValue_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AIKernelValue_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

theorem nativeGK4AIKernelValueFunctor_injective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4AIKernelValueFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AIKernelValue_injective
    X.original.2.2 Y.original.2.2

/-- Original independent S's joint observer factors through the
genuine K_AG kernel stage and its faithful value category. -/
theorem nativeGK4AIComparison_value_factor_map
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4AIKernelValueFunctor p ma mb pa pb).map
      ((nativeGK4AIComparisonFunctor p ma mb pa pb).map f) =
      nativeGK4AIStructural X.2.2 Y.2.2 f := by
  exact nativeGK4AIComparison_value X.2.2 Y.2.2 f

#print axioms nativeGK4AIKernelUnit
#print axioms nativeGK4AIKernelCompose
#print axioms nativeGK4AIKernelCompose_class
#print axioms nativeGK4AIKernelCompose_assoc
#print axioms nativeGK4AIKernelCompose_leftUnit
#print axioms nativeGK4AIKernelCompose_rightUnit
#print axioms nativeGK4AIKernelValue
#print axioms nativeGK4AIKernelValue_injective
#print axioms nativeGK4AIKernelValue_compose
#print axioms nativeGK4AIComparison
#print axioms nativeGK4AIComparison_value
#print axioms nativeGK4AIComparison_eq_iff
#print axioms nativeGK4AIComparison_surjective
#print axioms nativeGK4AIKernelCategory
#print axioms nativeGK4AIComparisonFunctor
#print axioms nativeGK4AIComparisonFunctor_surjective_hom
#print axioms nativeGK4AIValueCategory
#print axioms nativeGK4AIKernelValueFunctor
#print axioms nativeGK4AIKernelValueFunctor_injective_hom
#print axioms nativeGK4AIComparison_value_factor_map

end
end Kuu.F112.Physical
