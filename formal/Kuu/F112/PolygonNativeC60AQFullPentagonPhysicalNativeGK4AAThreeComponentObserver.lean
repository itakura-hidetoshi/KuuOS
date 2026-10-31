import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ZResidualNonfaithfulness
import Mathlib.Tactic

/-!
F112-P94D3GK4AA — the genuine THREE-component F54 physical observation.

On actual fully dependent F54 original routes we observe
  ((physical Boolean grade, signed cast-minus-rotation charge),
    count of ACTUAL backward Type-valued F54 RotationEdges).
The ORIGINAL P92B proof-existence quotient Q and the independently
extended structural quotient S receive SEPARATE, certified descents.
The new SECOND P92B observation-kernel quotient K_AA is not Q or S.

Preservation uses the independently proved complete nine F55 and nine
P92B source constructors, fourteen genuine F54 structural seams,
and three structural comparison constructors. No observational
equality is promoted to a new Type-valued source comparison witness.
The new observer strictly refines GK4X and distinguishes the GK4Z
balanced tower without claiming globally faithful S -> K_AA.

Append-only, tighten-only, same-root (107 public roots), no Gray,
strict 空 central, independent Kuu one presentation. No original Q
category laws, 14D unconditional Countable, 19D filler, global strict
n, historical complete typed equivalence, or hyperdescent asserted.
Lean 4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 remains Draft/open/unmerged.
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

/-- A pair of the actual GK4X values, and a separate natural
backward-rotation count. The nesting exposes the canonical
projection to GK4X without confusing the three observers. -/
abbrev NativeGK4AAValue := (Bool × Int) × Nat

/-- The source-independent product operation used by the genuine
second observation kernel; NOT a law asserted of original P92B Q. -/
def nativeGK4AACombine (u v : NativeGK4AAValue) : NativeGK4AAValue :=
  (nativeGK4XCombine u.1 v.1, u.2 + v.2)

theorem nativeGK4AACombine_assoc (a b c : NativeGK4AAValue) :
    nativeGK4AACombine (nativeGK4AACombine a b) c =
      nativeGK4AACombine a (nativeGK4AACombine b c) := by
  rcases a with ⟨x, i⟩
  rcases b with ⟨y, j⟩
  rcases c with ⟨z, k⟩
  simp only [nativeGK4AACombine, nativeGK4XCombine_assoc, add_assoc]

theorem nativeGK4AACombine_leftUnit (a : NativeGK4AAValue) :
    nativeGK4AACombine ((true, 0), 0) a = a := by
  rcases a with ⟨x, i⟩
  simp only [nativeGK4AACombine, nativeGK4XCombine_leftUnit, zero_add]

theorem nativeGK4AACombine_rightUnit (a : NativeGK4AAValue) :
    nativeGK4AACombine a ((true, 0), 0) = a := by
  rcases a with ⟨x, i⟩
  simp only [nativeGK4AACombine, nativeGK4XCombine_rightUnit, add_zero]

section ActualP92AndStructural
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

/-- The genuine original P92B existence classes Q. -/
def nativeGK4AATripleP92
    (q : NativeF55P92AssocRouteClasses t₁ t₂) : NativeGK4AAValue :=
  (nativeGK4XEnhancedP92 t₁ t₂ q, nativeGK4ZBackwardP92 t₁ t₂ q)

/-- The independently descended structural-comparison classes S. -/
def nativeGK4AATripleStructural
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) : NativeGK4AAValue :=
  (nativeGK4XEnhancedStructural t₁ t₂ s,
    nativeGK4ZBackwardStructural t₁ t₂ s)

@[simp] theorem nativeGK4AATripleP92_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4AATripleP92 t₁ t₂
      (nativeF55P92AssocRouteClass t₁ t₂ r) =
      ((nativeGK4GRawGrade t₁ t₂ r, r.gk4wCastCharge),
        r.gk4zBackwardCount) := rfl

@[simp] theorem nativeGK4AATripleStructural_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4AATripleStructural t₁ t₂
      (nativeGK4EStructuralRouteClass t₁ t₂ r) =
      ((nativeGK4GRawGrade t₁ t₂ r, r.gk4wCastCharge),
        r.gk4zBackwardCount) := rfl

/-- Q -> S commutes componentwise, but is NOT inverted. -/
theorem nativeGK4AATriple_commutes
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4AATripleStructural t₁ t₂
      (nativeGK4EP92ToStructural t₁ t₂ q) =
      nativeGK4AATripleP92 t₁ t₂ q := by
  refine _root_.Quotient.inductionOn q ?_
  intro r
  rfl

/-- The original P92B quotient still has an actual additive backward
observation despite lacking any asserted P92B category law. -/
theorem nativeGK4AABackwardP92_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4ZBackwardP92 t₁ t₃ (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      nativeGK4ZBackwardP92 t₁ t₂ u +
        nativeGK4ZBackwardP92 t₂ t₃ v := by
  refine _root_.Quotient.inductionOn u ?_
  intro rawU
  refine _root_.Quotient.inductionOn v ?_
  intro rawV
  exact nativeGK4ZBackward_trans rawU rawV

theorem nativeGK4AATripleP92_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4AATripleP92 t₁ t₃ (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      nativeGK4AACombine
        (nativeGK4AATripleP92 t₁ t₂ u)
        (nativeGK4AATripleP92 t₂ t₃ v) := by
  apply Prod.ext
  · exact nativeGK4XEnhancedP92_compose t₁ t₂ t₃ u v
  · exact nativeGK4AABackwardP92_compose t₁ t₂ t₃ u v

theorem nativeGK4AATripleStructural_compose
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    nativeGK4AATripleStructural t₁ t₃
        (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
      nativeGK4AACombine
        (nativeGK4AATripleStructural t₁ t₂ u)
        (nativeGK4AATripleStructural t₂ t₃ v) := by
  apply Prod.ext
  · exact nativeGK4XEnhancedStructural_compose t₁ t₂ t₃ u v
  · exact nativeGK4ZBackwardStructural_compose t₁ t₂ t₃ u v

@[simp] theorem nativeGK4AATripleP92_unit :
    nativeGK4AATripleP92 t₁ t₁ (nativeGK4H_p92Unit t₁) =
      ((true, 0), 0) := rfl

@[simp] theorem nativeGK4AATripleStructural_unit :
    nativeGK4AATripleStructural t₁ t₁ (nativeGK4H_structuralUnit t₁) =
      ((true, 0), 0) := rfl

/-- Equality of genuine triple values amounts to the existing
GK4X pair and the independent GK4Z backward count. -/
theorem nativeGK4AATripleStructural_eq_iff
    (u v : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4AATripleStructural t₁ t₂ u =
      nativeGK4AATripleStructural t₁ t₂ v ↔
    nativeGK4XEnhancedStructural t₁ t₂ u =
      nativeGK4XEnhancedStructural t₁ t₂ v ∧
    nativeGK4ZBackwardStructural t₁ t₂ u =
      nativeGK4ZBackwardStructural t₁ t₂ v := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨hx, hz⟩
    exact Prod.ext hx hz

end ActualP92AndStructural

/-- The observer runs over EVERY genuinely typed source and target
F45 tree, including both independent D/E categories and all Blocks. -/
def nativeGK4AATripleP92Family
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeGK4OObserverFamily p D E NativeGK4AAValue :=
  fun first last q => nativeGK4AATripleP92 first last q

/-- Full original F54 route composition plus BOTH source contexts.
The third component uses the original backward proof history. -/
theorem nativeGK4AATripleLaws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4PObservationLaws
      (nativeGK4AATripleP92Family p D E) nativeGK4AACombine
      (nativeGK4PIdentityAction p D E NativeGK4AAValue)
      (nativeGK4PIdentityAction p D E NativeGK4AAValue) := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ u v
    change
      ((nativeGK4GRawGrade t₁ t₃ (.trans u v),
          (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4wCastCharge),
        (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4zBackwardCount) =
        nativeGK4AACombine
          ((nativeGK4GRawGrade t₁ t₂ u, u.gk4wCastCharge),
            u.gk4zBackwardCount)
          ((nativeGK4GRawGrade t₂ t₃ v, v.gk4wCastCharge),
            v.gk4zBackwardCount)
    apply Prod.ext
    · apply Prod.ext
      · exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ u v
      · exact nativeGK4W_charge_trans u v
    · exact nativeGK4ZBackward_trans u v
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r later
    rfl
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r
    rfl

/-- The exact original 14-constructor F54 seam invariance;
GK4X's pair and GK4Z's backward count are PROVED independently. -/
theorem nativeGK4AATripleSeamInvariant
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeGK4NSeamInvariant first last
      (nativeGK4AATripleP92Family p D E first last) := by
  intro r s seam
  change nativeGK4AATripleP92 first last
      (nativeF55P92AssocRouteClass first last r) =
    nativeGK4AATripleP92 first last
      (nativeF55P92AssocRouteClass first last s)
  apply Prod.ext
  · exact nativeGK4XEnhancedSeamInvariant first last r s seam
  · exact nativeGK4ZBackward_seam_sound seam

#print axioms NativeGK4AAValue
#print axioms nativeGK4AACombine
#print axioms nativeGK4AACombine_assoc
#print axioms nativeGK4AACombine_leftUnit
#print axioms nativeGK4AACombine_rightUnit
#print axioms nativeGK4AATripleP92
#print axioms nativeGK4AATripleStructural
#print axioms nativeGK4AATripleP92_class
#print axioms nativeGK4AATripleStructural_class
#print axioms nativeGK4AATriple_commutes
#print axioms nativeGK4AABackwardP92_compose
#print axioms nativeGK4AATripleP92_compose
#print axioms nativeGK4AATripleStructural_compose
#print axioms nativeGK4AATripleP92_unit
#print axioms nativeGK4AATripleStructural_unit
#print axioms nativeGK4AATripleStructural_eq_iff
#print axioms nativeGK4AATripleP92Family
#print axioms nativeGK4AATripleLaws
#print axioms nativeGK4AATripleSeamInvariant

end
end Kuu.F112.Physical
