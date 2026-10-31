import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4WCastTowerNonfaithfulness
import Mathlib.Tactic

/-!
F112-P94D3GK4X — genuinely typed Boolean-plus-signed-cast-charge observation.

The actual original F54 dependent source is kept intact. Q denotes the
original P92B existence quotient, S the independently extended structural
comparison existence quotient. From GK4W's original all-constructor
cast-minus-rotation invariant and GK4G's original physical Boolean grade,
derive genuine observations Q/S -> Bool x Int, WITHOUT identifying those
distinct quotients or fabricating Type-valued P92B comparison evidence.

Prove the exact quotient commuting square, the original and structural
composition laws, the witnessed structural unit, all three GK4P original
F54 observation laws with both source contexts, and full new genuine
F54 seam preservation. The derived observation is information-richer
than Boolean, but NOT asserted faithful or an equivalence with S.

Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, tighten-only, same-root, no Gray; strict 空 central,
independent Kuu one presentation; public root 107. Protected #1558
Draft/open/unmerged. Original Q category axioms, historical full typed
equivalence, original unconditional 14D Countable, 19D filler, global
strict n, hyperdescent not claimed.
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

section ActualOriginalAndStructuralQuotients
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- The all-constructor W charge on TRUE ORIGINAL P92B classes. -/
def nativeGK4XChargeP92 :
    NativeF55P92AssocRouteClasses t₁ t₂ → Int :=
  _root_.Quotient.lift
    (fun r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂ =>
      r.gk4wCastCharge)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4W_p92_charge_sound cell)

/-- The SAME signed invariant, independently descended to the
genuinely larger GK4E structural-comparison quotient. -/
def nativeGK4XChargeStructural :
    NativeGK4EStructuralRouteClasses t₁ t₂ → Int :=
  _root_.Quotient.lift
    (fun r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂ =>
      r.gk4wCastCharge)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4W_structural_charge_sound cell)

@[simp] theorem nativeGK4XChargeP92_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4XChargeP92 t₁ t₂
        (nativeF55P92AssocRouteClass t₁ t₂ r) =
      r.gk4wCastCharge := by
  rfl

@[simp] theorem nativeGK4XChargeStructural_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4XChargeStructural t₁ t₂
        (nativeGK4EStructuralRouteClass t₁ t₂ r) =
      r.gk4wCastCharge := by
  rfl

/-- True ORIGINAL P92B -> INDEPENDENT STRUCTURAL charge square. -/
theorem nativeGK4XCharge_commutes
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4XChargeStructural t₁ t₂
        (nativeGK4EP92ToStructural t₁ t₂ q) =
      nativeGK4XChargeP92 t₁ t₂ q := by
  refine _root_.Quotient.inductionOn q ?_
  intro r
  rfl

/-- Charge is additive under genuinely typed original P92B quotient
composition; this does NOT make original P92B associative/unital. -/
theorem nativeGK4XChargeP92_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4XChargeP92 t₁ t₃
        (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      nativeGK4XChargeP92 t₁ t₂ u +
        nativeGK4XChargeP92 t₂ t₃ v := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  exact nativeGK4W_charge_trans r s

/-- Independently extended true structural composition also preserves
the signed charge's exact additive law. -/
theorem nativeGK4XChargeStructural_compose
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    nativeGK4XChargeStructural t₁ t₃
        (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
      nativeGK4XChargeStructural t₁ t₂ u +
        nativeGK4XChargeStructural t₂ t₃ v := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  exact nativeGK4W_charge_trans r s

/-- The TRUE structural identity has charge ZERO. Original P92B
left/right identity laws are NOT assumed. -/
@[simp] theorem nativeGK4XChargeStructural_unit :
    nativeGK4XChargeStructural t₁ t₁
      (nativeGK4H_structuralUnit t₁) = 0 := by
  rfl

/-- The REAL original zero-edge route class also has charge zero. -/
@[simp] theorem nativeGK4XChargeP92_unit :
    nativeGK4XChargeP92 t₁ t₁ (nativeGK4H_p92Unit t₁) = 0 := by
  rfl

/-- A complete two-component observation of ORIGINAL P92B classes. -/
def nativeGK4XEnhancedP92
    (q : NativeF55P92AssocRouteClasses t₁ t₂) : Bool × Int :=
  (nativeGK4GP92Grade t₁ t₂ q, nativeGK4XChargeP92 t₁ t₂ q)

/-- The same enhanced observation directly on the INDEPENDENT
extended structural-comparison quotient, not on synthetic routes. -/
def nativeGK4XEnhancedStructural
    (s : NativeGK4EStructuralRouteClasses t₁ t₂) : Bool × Int :=
  (nativeGK4GStructuralGrade t₁ t₂ s,
    nativeGK4XChargeStructural t₁ t₂ s)

@[simp] theorem nativeGK4XEnhancedP92_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4XEnhancedP92 t₁ t₂
      (nativeF55P92AssocRouteClass t₁ t₂ r) =
      (nativeGK4GRawGrade t₁ t₂ r, r.gk4wCastCharge) := by
  rfl

@[simp] theorem nativeGK4XEnhancedStructural_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4XEnhancedStructural t₁ t₂
      (nativeGK4EStructuralRouteClass t₁ t₂ r) =
      (nativeGK4GRawGrade t₁ t₂ r, r.gk4wCastCharge) := by
  rfl

/-- Complete commutative triangle: no representative selection. -/
theorem nativeGK4XEnhanced_commutes
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4XEnhancedStructural t₁ t₂
        (nativeGK4EP92ToStructural t₁ t₂ q) =
      nativeGK4XEnhancedP92 t₁ t₂ q := by
  refine _root_.Quotient.inductionOn q ?_
  intro r
  rfl

/-- The value operation is a real product monoid operation. Its
unit is (true,0) and its multiplication is Bool.and x Int.add. -/
def nativeGK4XCombine (a b : Bool × Int) : Bool × Int :=
  (a.1 && b.1, a.2 + b.2)

theorem nativeGK4XCombine_assoc
    (a b c : Bool × Int) :
    nativeGK4XCombine (nativeGK4XCombine a b) c =
      nativeGK4XCombine a (nativeGK4XCombine b c) := by
  rcases a with ⟨x, i⟩
  rcases b with ⟨y, j⟩
  rcases c with ⟨z, k⟩
  cases x <;> cases y <;> cases z <;>
    simp [nativeGK4XCombine, add_assoc]

theorem nativeGK4XCombine_leftUnit (a : Bool × Int) :
    nativeGK4XCombine (true, 0) a = a := by
  rcases a with ⟨x, i⟩
  cases x <;> simp [nativeGK4XCombine]

theorem nativeGK4XCombine_rightUnit (a : Bool × Int) :
    nativeGK4XCombine a (true, 0) = a := by
  rcases a with ⟨x, i⟩
  cases x <;> simp [nativeGK4XCombine]

/-- The REAL original P92B composite measures the product
in both components, not merely an ambient Boolean shadow. -/
theorem nativeGK4XEnhancedP92_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4XEnhancedP92 t₁ t₃ (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      nativeGK4XCombine
        (nativeGK4XEnhancedP92 t₁ t₂ u)
        (nativeGK4XEnhancedP92 t₂ t₃ v) := by
  apply Prod.ext
  · exact nativeGK4H_p92Grade_compose t₁ t₂ t₃ u v
  · exact nativeGK4XChargeP92_compose t₁ t₂ t₃ u v

/-- The independently extended structural quotient composition
maps to the exact same product value operation. -/
theorem nativeGK4XEnhancedStructural_compose
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    nativeGK4XEnhancedStructural t₁ t₃
        (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
      nativeGK4XCombine
        (nativeGK4XEnhancedStructural t₁ t₂ u)
        (nativeGK4XEnhancedStructural t₂ t₃ v) := by
  apply Prod.ext
  · exact nativeGK4H_structuralGrade_compose t₁ t₂ t₃ u v
  · exact nativeGK4XChargeStructural_compose t₁ t₂ t₃ u v

@[simp] theorem nativeGK4XEnhancedStructural_unit :
    nativeGK4XEnhancedStructural t₁ t₁
      (nativeGK4H_structuralUnit t₁) = (true, 0) := by
  rfl

@[simp] theorem nativeGK4XEnhancedP92_unit :
    nativeGK4XEnhancedP92 t₁ t₁
      (nativeGK4H_p92Unit t₁) = (true, 0) := by
  rfl

end ActualOriginalAndStructuralQuotients

/-- A family of ACTUAL P92B observer values over ALL fully dependent
original F45 endpoints, not a family of raw syntactic shadows. -/
def nativeGK4XEnhancedP92Family
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeGK4OObserverFamily p D E (Bool × Int) :=
  fun first last q => nativeGK4XEnhancedP92 first last q

/-- All three GK4P laws hold for genuine F54 route composition
and left/right original binary contexts, without a new axiom. -/
theorem nativeGK4XEnhancedLaws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4PObservationLaws
      (nativeGK4XEnhancedP92Family p D E) nativeGK4XCombine
      (nativeGK4PIdentityAction p D E (Bool × Int))
      (nativeGK4PIdentityAction p D E (Bool × Int)) := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ u v
    change (nativeGK4GRawGrade t₁ t₃ (.trans u v),
        (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4wCastCharge) =
      nativeGK4XCombine
        (nativeGK4GRawGrade t₁ t₂ u, u.gk4wCastCharge)
        (nativeGK4GRawGrade t₂ t₃ v, v.gk4wCastCharge)
    apply Prod.ext
    · exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ u v
    · exact nativeGK4W_charge_trans u v
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r later
    rfl
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r
    rfl

/-- The enhanced ORIGINAL P92B family preserves every TRUE F54
structural seam, not only the 7 primitives: the second component
uses GK4W's complete 14-constructor Type-valued seam induction. -/
theorem nativeGK4XEnhancedSeamInvariant
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeGK4NSeamInvariant first last
      (nativeGK4XEnhancedP92Family p D E first last) := by
  intro r s seam
  change nativeGK4XEnhancedP92 first last
      (nativeF55P92AssocRouteClass first last r) =
    nativeGK4XEnhancedP92 first last
      (nativeF55P92AssocRouteClass first last s)
  apply Prod.ext
  · exact nativeGK4N_boolean_seam_sound first last r s seam
  · exact nativeGK4W_seam_charge_sound seam

#print axioms nativeGK4XChargeP92
#print axioms nativeGK4XChargeStructural
#print axioms nativeGK4XChargeP92_class
#print axioms nativeGK4XChargeStructural_class
#print axioms nativeGK4XCharge_commutes
#print axioms nativeGK4XChargeP92_compose
#print axioms nativeGK4XChargeStructural_compose
#print axioms nativeGK4XChargeStructural_unit
#print axioms nativeGK4XChargeP92_unit
#print axioms nativeGK4XEnhancedP92
#print axioms nativeGK4XEnhancedStructural
#print axioms nativeGK4XEnhancedP92_class
#print axioms nativeGK4XEnhancedStructural_class
#print axioms nativeGK4XEnhanced_commutes
#print axioms nativeGK4XCombine
#print axioms nativeGK4XCombine_assoc
#print axioms nativeGK4XCombine_leftUnit
#print axioms nativeGK4XCombine_rightUnit
#print axioms nativeGK4XEnhancedP92_compose
#print axioms nativeGK4XEnhancedStructural_compose
#print axioms nativeGK4XEnhancedStructural_unit
#print axioms nativeGK4XEnhancedP92_unit
#print axioms nativeGK4XEnhancedP92Family
#print axioms nativeGK4XEnhancedLaws
#print axioms nativeGK4XEnhancedSeamInvariant

end
end Kuu.F112.Physical
