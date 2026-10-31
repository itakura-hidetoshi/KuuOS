import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ADTripleNonfaithfulness
import Mathlib.Tactic

/-!
F112-P94D3GK4AE — genuine FOUR-component observation
    (physical grade, signed cast charge, backward count, ordered moment)
over the ACTUAL original F54 fully dependent Type-valued route source.

Do not identify original P92B proof-existence quotient Q, the separately
constructed structural quotient S, and any observation second kernel.
The AD ordered Heisenberg value is preserved by the entire F55/P92B/
14-seam/structural grammar, so the FOUR-component observation descends
separately to Q and S. Original source route composition and binary
contexts are verified. No new original Type-valued 3-cell is invented.

Strict 空 central, independent Kuu one presentation; append-only,
same-root 107, no Gray. Protected #1558 Draft/open/unmerged.
Lean 4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- A true four-component value:
Bool × ((Int × Nat) × Int). Unlike a commutative product it keeps
the NONCOMMUTATIVE ordered cast/backward history of GK4AD. -/
abbrev NativeGK4AEValue := Bool × NativeGK4ADValue

/-- Product of the original Boolean grade and actual GK4AD ordered
Heisenberg multiplication; this target is genuinely noncommutative. -/
def nativeGK4AECombine (u v : NativeGK4AEValue) : NativeGK4AEValue :=
  (u.1 && v.1, nativeGK4ADCombine u.2 v.2)

/-- Only the proved original F54 structural unit image. -/
def nativeGK4AEUnit : NativeGK4AEValue :=
  (true, nativeGK4ADZero)

theorem nativeGK4AECombine_assoc (u v w : NativeGK4AEValue) :
    nativeGK4AECombine (nativeGK4AECombine u v) w =
      nativeGK4AECombine u (nativeGK4AECombine v w) := by
  rcases u with ⟨a, x⟩
  rcases v with ⟨b, y⟩
  rcases w with ⟨c, z⟩
  apply Prod.ext
  · cases a <;> cases b <;> cases c <;> rfl
  · exact nativeGK4ADCombine_assoc x y z

theorem nativeGK4AECombine_leftUnit (u : NativeGK4AEValue) :
    nativeGK4AECombine nativeGK4AEUnit u = u := by
  rcases u with ⟨a, x⟩
  apply Prod.ext
  · cases a <;> rfl
  · exact nativeGK4ADCombine_leftUnit x

theorem nativeGK4AECombine_rightUnit (u : NativeGK4AEValue) :
    nativeGK4AECombine u nativeGK4AEUnit = u := by
  rcases u with ⟨a, x⟩
  apply Prod.ext
  · cases a <;> rfl
  · exact nativeGK4ADCombine_rightUnit x

/-- The underlying genuine GK4AA THREE-component image of a four-
component value, forgetting ONLY the ordered moment. -/
def nativeGK4AEForgetValue (u : NativeGK4AEValue) : NativeGK4AAValue :=
  ((u.1, u.2.1.1), u.2.1.2)

theorem nativeGK4AEForgetValue_combine (u v : NativeGK4AEValue) :
    nativeGK4AEForgetValue (nativeGK4AECombine u v) =
      nativeGK4AACombine
        (nativeGK4AEForgetValue u) (nativeGK4AEForgetValue v) := rfl

theorem nativeGK4AEForgetValue_unit :
    nativeGK4AEForgetValue nativeGK4AEUnit = ((true, 0), 0) := rfl

section GenuineOriginalFourObserver
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- On Q, use the preexisting exact original P92B grade and new
ordered history; Q is NOT upgraded to an unproved category. -/
def nativeGK4AEQuadP92
    (q : NativeF55P92AssocRouteClasses first middle) :
    NativeGK4AEValue :=
  (nativeGK4GP92Grade first middle q,
    nativeGK4ADP92Value first middle q)

/-- Independent S has its OWN original Type-valued structural
comparison descent, with all 14 seams retained. -/
def nativeGK4AEQuadStructural
    (s : NativeGK4EStructuralRouteClasses first middle) :
    NativeGK4AEValue :=
  (nativeGK4GStructuralGrade first middle s,
    nativeGK4ADStructuralValue first middle s)

@[simp] theorem nativeGK4AEQuadP92_class
    (r : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AEQuadP92 first middle
        (nativeF55P92AssocRouteClass first middle r) =
      (nativeGK4GRawGrade first middle r, r.gk4adValue) := rfl

@[simp] theorem nativeGK4AEQuadStructural_class
    (r : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AEQuadStructural first middle
        (nativeGK4EStructuralRouteClass first middle r) =
      (nativeGK4GRawGrade first middle r, r.gk4adValue) := rfl

theorem nativeGK4AEQuad_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4AEQuadStructural first middle
        (nativeGK4EP92ToStructural first middle q) =
      nativeGK4AEQuadP92 first middle q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  rfl

/-- The P92B original composition RESPECTS the four-component
observation, but Q's associativity/unitality remain UNPROVED. -/
theorem nativeGK4AEQuadP92_compose
    (u : NativeF55P92AssocRouteClasses first middle)
    (v : NativeF55P92AssocRouteClasses middle last) :
    nativeGK4AEQuadP92 first last
        (nativeGK4H_p92Compose first middle last u v) =
      nativeGK4AECombine
        (nativeGK4AEQuadP92 first middle u)
        (nativeGK4AEQuadP92 middle last v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro rawU rawV
  apply Prod.ext
  · exact nativeGK4H_rawGrade_compose first middle last rawU rawV
  · exact nativeGK4AD_trans rawU rawV

theorem nativeGK4AEQuadStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4AEQuadStructural first last
        (nativeGK4H_structuralCompose first middle last u v) =
      nativeGK4AECombine
        (nativeGK4AEQuadStructural first middle u)
        (nativeGK4AEQuadStructural middle last v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro rawU rawV
  apply Prod.ext
  · exact nativeGK4H_rawGrade_compose first middle last rawU rawV
  · exact nativeGK4AD_trans rawU rawV

@[simp] theorem nativeGK4AEQuadP92_unit :
    nativeGK4AEQuadP92 first first
        (nativeGK4H_p92Unit first) = nativeGK4AEUnit := rfl

@[simp] theorem nativeGK4AEQuadStructural_unit :
    nativeGK4AEQuadStructural first first
        (nativeGK4H_structuralUnit first) = nativeGK4AEUnit := rfl

end GenuineOriginalFourObserver

/-- A genuine GK4O observation family over all dependent original
F45 trees, never an invented source category. -/
def nativeGK4AEQuadP92Family
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeGK4OObserverFamily p D E NativeGK4AEValue :=
  fun first last q => nativeGK4AEQuadP92 first last q

/-- All actual F54 route composition and both original dependent
binary contexts act by the certified noncommutative product. -/
theorem nativeGK4AEQuadLaws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4PObservationLaws
      (nativeGK4AEQuadP92Family p D E) nativeGK4AECombine
      (nativeGK4PIdentityAction p D E NativeGK4AEValue)
      (nativeGK4PIdentityAction p D E NativeGK4AEValue) := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ u v
    change
      (nativeGK4GRawGrade t₁ t₃ (.trans u v),
        (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4adValue) =
        nativeGK4AECombine
          (nativeGK4GRawGrade t₁ t₂ u, u.gk4adValue)
          (nativeGK4GRawGrade t₂ t₃ v, v.gk4adValue)
    apply Prod.ext
    · exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ u v
    · exact nativeGK4AD_trans u v
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r later
    rfl
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r
    rfl

/-- FULL original 14-seam invariant. The grade is independently
certified by GK4AA; the ordered moment by GK4AD, whose proof covers
all the distinct original Type-valued comparison constructors. -/
theorem nativeGK4AEQuadSeamInvariant
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeGK4NSeamInvariant first last
      (nativeGK4AEQuadP92Family p D E first last) := by
  intro r s seam
  change (nativeGK4GRawGrade first last r, r.gk4adValue) =
    (nativeGK4GRawGrade first last s, s.gk4adValue)
  apply Prod.ext
  · have hold := nativeGK4AATripleSeamInvariant first last r s seam
    exact congrArg (fun z : NativeGK4AAValue => z.1.1) hold
  · exact nativeGK4AD_seam_sound seam

#print axioms NativeGK4AEValue
#print axioms nativeGK4AECombine
#print axioms nativeGK4AEUnit
#print axioms nativeGK4AECombine_assoc
#print axioms nativeGK4AECombine_leftUnit
#print axioms nativeGK4AECombine_rightUnit
#print axioms nativeGK4AEForgetValue
#print axioms nativeGK4AEForgetValue_combine
#print axioms nativeGK4AEForgetValue_unit
#print axioms nativeGK4AEQuadP92
#print axioms nativeGK4AEQuadStructural
#print axioms nativeGK4AEQuadP92_class
#print axioms nativeGK4AEQuadStructural_class
#print axioms nativeGK4AEQuad_commutes
#print axioms nativeGK4AEQuadP92_compose
#print axioms nativeGK4AEQuadStructural_compose
#print axioms nativeGK4AEQuadP92_unit
#print axioms nativeGK4AEQuadStructural_unit
#print axioms nativeGK4AEQuadP92Family
#print axioms nativeGK4AEQuadLaws
#print axioms nativeGK4AEQuadSeamInvariant

end
end Kuu.F112.Physical
