import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEKernelCategory
import Mathlib.Tactic

/-!
F112-P94D3GK4AE — true fourth-observation second-kernel refinement
K_AE -> K_AA. Both are ACTUAL distinct GK4S quotients of the
existing ORIGINAL P92B proof-existence quotient Q, not of raw strings.

The genuine noncommutative ordered cast/backward moment distinguishes
the fully typed original F54 paths C;B and B;C, whose previous
(Boolean,castCharge,backwardCount) values and K_AA classes agree.
The K_AE -> K_AA forgetful Mathlib functor is full per original Hom
but NOT faithful for any witnessed genuine F54 local rotation,
including physical C60 north. The full S -> K_AE faithfulness is NOT
asserted or derived from this strict refinement.

No fabricated original Type-valued 3-cell; no Q category laws;
no historical complete typed equivalence, unconditional original
14D Countable, 19D filler, global strict n or hyperdescent.
Append-only/same-root 107, strict 空 central, no Gray, protected
#1558 Draft/open/unmerged. Copyright © 2026 Hidetoshi Itakura /
板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section GenuineSecondKernelForget
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- Forget the ordered moment, NOT the original F54 Type-valued
source or the physical backwardCount. This is well-defined by
the proved original Q projection compatibility lemma. -/
def nativeGK4AEForgetMoment :
    NativeGK4SKernelClasses
        (nativeGK4AEQuadP92Family p D E) t₁ t₂ →
      NativeGK4SKernelClasses
        (nativeGK4AATripleP92Family p D E) t₁ t₂ :=
  _root_.Quotient.lift
    (nativeGK4SKernelClass (nativeGK4AATripleP92Family p D E) t₁ t₂)
    (by
      intro q r h
      apply (nativeGK4SKernelClass_eq_iff
        (nativeGK4AATripleP92Family p D E) t₁ t₂ q r).mpr
      rw [← nativeGK4AEQuadP92_forget t₁ t₂ q,
        ← nativeGK4AEQuadP92_forget t₁ t₂ r]
      exact congrArg nativeGK4AEForgetValue h)

@[simp] theorem nativeGK4AEForgetMoment_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4AEForgetMoment t₁ t₂
      (nativeGK4SKernelClass (nativeGK4AEQuadP92Family p D E)
        t₁ t₂ q) =
      nativeGK4SKernelClass (nativeGK4AATripleP92Family p D E)
        t₁ t₂ q := rfl

theorem nativeGK4AEForgetMoment_surjective :
    Function.Surjective (nativeGK4AEForgetMoment t₁ t₂) := by
  intro z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  exact ⟨nativeGK4SKernelClass
      (nativeGK4AEQuadP92Family p D E) t₁ t₂ q, rfl⟩

/-- True K_AE->K_AA factorization of the two source-compatible
S comparisons, not a hypothetical original P92B equivalence. -/
theorem nativeGK4AEForgetMoment_comparison
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AEForgetMoment t₁ t₂
      (nativeGK4AEComparison t₁ t₂ s) =
        nativeGK4AATripleComparison t₁ t₂ s := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  rfl

theorem nativeGK4AEForgetMoment_unit :
    nativeGK4AEForgetMoment t₁ t₁
      (nativeGK4AEEnhancedKernelUnit t₁) =
        nativeGK4AAEnhancedKernelUnit t₁ := rfl

theorem nativeGK4AEForgetMoment_compose
    (u : NativeGK4SKernelClasses
      (nativeGK4AEQuadP92Family p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses
      (nativeGK4AEQuadP92Family p D E) t₂ t₃) :
    nativeGK4AEForgetMoment t₁ t₃
      (nativeGK4AEEnhancedKernelCompose t₁ t₂ t₃ u v) =
        nativeGK4AAEnhancedKernelCompose t₁ t₂ t₃
          (nativeGK4AEForgetMoment t₁ t₂ u)
          (nativeGK4AEForgetMoment t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  rw [nativeGK4AEEnhancedKernelCompose_class,
    nativeGK4AEForgetMoment_class,
    nativeGK4AEForgetMoment_class,
    nativeGK4AEForgetMoment_class,
    nativeGK4AAEnhancedKernelCompose_class]

theorem nativeGK4AEForgetMoment_value
    (z : NativeGK4SKernelClasses
      (nativeGK4AEQuadP92Family p D E) t₁ t₂) :
    nativeGK4AAEnhancedKernelValue t₁ t₂
        (nativeGK4AEForgetMoment t₁ t₂ z) =
      nativeGK4AEForgetValue
        (nativeGK4AEEnhancedKernelValue t₁ t₂ z) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  simpa only [nativeGK4AEEnhancedKernelValue_class,
    nativeGK4AAEnhancedKernelValue_class,
    nativeGK4AEForgetMoment_class] using
      (nativeGK4AEQuadP92_forget t₁ t₂ q).symm

end GenuineSecondKernelForget

/-- A genuine Mathlib functor between two DIFFERENT attained
original P92B observation-kernel category presentations. -/
def nativeGK4AEForgetMomentFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AEEnhancedKernelStage p ma mb pa pb ⥤
      NativeGK4AAEnhancedKernelStage p ma mb pa pb where
  obj X := ⟨X.original⟩
  map := fun {X Y} f =>
    nativeGK4AEForgetMoment X.original.2.2 Y.original.2.2 f
  map_id := by
    intro X
    exact nativeGK4AEForgetMoment_unit X.original.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AEForgetMoment_compose
      X.original.2.2 Y.original.2.2 Z.original.2.2 f g

theorem nativeGK4AEForgetMomentFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AEEnhancedKernelStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4AEForgetMomentFunctor p ma mb pa pb).map f) := by
  exact nativeGK4AEForgetMoment_surjective
    X.original.2.2 Y.original.2.2

section RealNoncommutativeWitness
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- The true fourth kernel DOES distinguish the real original
cast-before/backtrack and backtrack-before/cast source proofs. -/
theorem nativeGK4AECastOrders_separated :
    nativeGK4AEComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastBeforeBacktrack rot)) ≠
    nativeGK4AEComparison before before
      (nativeGK4EStructuralRouteClass before before
        (nativeGK4ADCastAfterBacktrack rot)) := by
  intro heq
  have hv := (nativeGK4AEComparison_eq_iff before before _ _).mp heq
  have hm := congrArg (fun v : NativeGK4AEValue => v.2.2) hv
  change
    (nativeGK4ADCastBeforeBacktrack rot).gk4adValue.2 =
    (nativeGK4ADCastAfterBacktrack rot).gk4adValue.2 at hm
  rw [nativeGK4ADCastBefore_value, nativeGK4ADCastAfter_value] at hm
  omega

/-- The actual K_AE->K_AA forgetful Hom map has a genuine
pair of DIFFERENT second kernel classes mapped to the SAME class. -/
theorem nativeGK4AEForgetMoment_not_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ¬ Function.Injective (nativeGK4AEForgetMoment before before) := by
  intro hinj
  have hsame := nativeGK4ADTwoOrders_sameKernel rot
  have hsameAE :
      nativeGK4AEForgetMoment before before
        (nativeGK4AEComparison before before
          (nativeGK4EStructuralRouteClass before before
            (nativeGK4ADCastBeforeBacktrack rot))) =
      nativeGK4AEForgetMoment before before
        (nativeGK4AEComparison before before
          (nativeGK4EStructuralRouteClass before before
            (nativeGK4ADCastAfterBacktrack rot))) := by
    simpa only [nativeGK4AEForgetMoment_comparison] using hsame
  exact nativeGK4AECastOrders_separated rot (hinj hsameAE)

/-- The nonfaithfulness of this actual forgetful functor is witnessed
unconditionally by the genuine C60 physical north LocalRotation. -/
theorem nativeGK4AE_physical_north_forgetful_nonfaithful :
    ¬ Function.Injective
      (nativeGK4AEForgetMoment
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4AEForgetMoment_not_injective
    northHexagonNativeLeftRotation

end RealNoncommutativeWitness

#print axioms nativeGK4AEForgetMoment
#print axioms nativeGK4AEForgetMoment_class
#print axioms nativeGK4AEForgetMoment_surjective
#print axioms nativeGK4AEForgetMoment_comparison
#print axioms nativeGK4AEForgetMoment_unit
#print axioms nativeGK4AEForgetMoment_compose
#print axioms nativeGK4AEForgetMoment_value
#print axioms nativeGK4AEForgetMomentFunctor
#print axioms nativeGK4AEForgetMomentFunctor_surjective_hom
#print axioms nativeGK4AECastOrders_separated
#print axioms nativeGK4AEForgetMoment_not_injective
#print axioms nativeGK4AE_physical_north_forgetful_nonfaithful

end
end Kuu.F112.Physical
