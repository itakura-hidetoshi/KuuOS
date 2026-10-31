import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4UCompositionalKernelFunctor
import Mathlib.Tactic

/-!
F112-P94D3GK4V: exact kernel and faithfulness criterion for the
genuine GK4U Boolean structural-to-observation-kernel comparison.
Q(original P92B), S(independent structural), and K(second observed
quotient) remain distinct. No unproved Q associativity, Q unit,
full typed equivalence, 14D countability, 19D filler or hyperdescent.
Append-only, 107 public roots, no Gray; Lean 4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 remains Draft/open/unmerged.
Copyright 板倉英俊 / Hidetoshi Itakura; Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section ExactKernel
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- Read the exact Bool grade of a genuine GK4S kernel class. -/
def nativeGK4VKernelGrade :
    NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₂ → Bool :=
  _root_.Quotient.lift (nativeGK4GP92Grade t₁ t₂)
    (by intro q r h; exact h)

@[simp] theorem nativeGK4VKernelGrade_class
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4VKernelGrade t₁ t₂
        (nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) t₁ t₂ q) =
      nativeGK4GP92Grade t₁ t₂ q := by
  rfl

theorem nativeGK4VKernelGrade_injective :
    Function.Injective (nativeGK4VKernelGrade t₁ t₂) := by
  intro u v
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r h
  exact _root_.Quotient.sound h

@[simp] theorem nativeGK4VKernelGrade_unit :
    nativeGK4VKernelGrade t₁ t₁ (nativeGK4UBoolKernelUnit t₁) = true := by
  rfl

theorem nativeGK4VKernelGrade_compose
    (u : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₂ t₃) :
    nativeGK4VKernelGrade t₁ t₃
      (nativeGK4UBoolKernelCompose t₁ t₂ t₃ u v) =
      (nativeGK4VKernelGrade t₁ t₂ u &&
        nativeGK4VKernelGrade t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro q r
  simpa only [nativeGK4UBoolKernelCompose_class,
    nativeGK4VKernelGrade_class] using
    (nativeGK4H_p92Grade_compose t₁ t₂ t₃ q r)

/-- The comparison to K_Bool reproduces the GK4G STRUCTURAL grade. -/
theorem nativeGK4VComparison_grade
    (u : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4VKernelGrade t₁ t₂
      (nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
        (nativeGK4N_boolean_seam_invariant t₁ t₂) u) =
      nativeGK4GStructuralGrade t₁ t₂ u := by
  obtain ⟨q, rfl⟩ := nativeGK4EP92ToStructural_surjective t₁ t₂ u
  rw [nativeGK4TComparison_class, nativeGK4VKernelGrade_class]
  exact nativeGK4G_grading_commutes t₁ t₂ q

/-- The canonical comparison identifies EXACTLY equal grades. -/
theorem nativeGK4VComparison_eq_iff_grade
    (u v : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
        (nativeGK4N_boolean_seam_invariant t₁ t₂) u =
      nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
        (nativeGK4N_boolean_seam_invariant t₁ t₂) v ↔
      nativeGK4GStructuralGrade t₁ t₂ u =
        nativeGK4GStructuralGrade t₁ t₂ v := by
  constructor
  · intro h
    calc
      nativeGK4GStructuralGrade t₁ t₂ u =
        nativeGK4VKernelGrade t₁ t₂
          (nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
            (nativeGK4N_boolean_seam_invariant t₁ t₂) u) :=
        (nativeGK4VComparison_grade t₁ t₂ u).symm
      _ = nativeGK4VKernelGrade t₁ t₂
          (nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
            (nativeGK4N_boolean_seam_invariant t₁ t₂) v) :=
        congrArg (nativeGK4VKernelGrade t₁ t₂) h
      _ = nativeGK4GStructuralGrade t₁ t₂ v :=
        nativeGK4VComparison_grade t₁ t₂ v
  · intro h
    apply nativeGK4VKernelGrade_injective t₁ t₂
    calc
      nativeGK4VKernelGrade t₁ t₂
          (nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
            (nativeGK4N_boolean_seam_invariant t₁ t₂) u) =
        nativeGK4GStructuralGrade t₁ t₂ u :=
        nativeGK4VComparison_grade t₁ t₂ u
      _ = nativeGK4GStructuralGrade t₁ t₂ v := h
      _ = nativeGK4VKernelGrade t₁ t₂
          (nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
            (nativeGK4N_boolean_seam_invariant t₁ t₂) v) :=
        (nativeGK4VComparison_grade t₁ t₂ v).symm

/-- Faithfulness is NOT presumed: it is EXACTLY structural grade
injectivity at this particular fully dependent original F45 Hom. -/
theorem nativeGK4VComparison_injective_iff_grade :
    Function.Injective
        (nativeGK4TComparison (nativeGK4OBooleanFamily p D E) t₁ t₂
          (nativeGK4N_boolean_seam_invariant t₁ t₂)) ↔
      Function.Injective (nativeGK4GStructuralGrade t₁ t₂) := by
  constructor
  · intro hinj u v hg
    exact hinj ((nativeGK4VComparison_eq_iff_grade t₁ t₂ u v).mpr hg)
  · intro hinj u v h
    exact hinj ((nativeGK4VComparison_eq_iff_grade t₁ t₂ u v).mp h)

end ExactKernel

#print axioms nativeGK4VKernelGrade
#print axioms nativeGK4VKernelGrade_class
#print axioms nativeGK4VKernelGrade_injective
#print axioms nativeGK4VKernelGrade_unit
#print axioms nativeGK4VKernelGrade_compose
#print axioms nativeGK4VComparison_grade
#print axioms nativeGK4VComparison_eq_iff_grade
#print axioms nativeGK4VComparison_injective_iff_grade

end
end Kuu.F112.Physical
