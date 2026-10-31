import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4JNoAnyP92Unit
import Mathlib.Tactic

/-!
# F112-P94D3GK4K — Option Nat descent of conditional genuine P92B leaf counts

The true original fully dependent F54 route carries TWO distinct observations:
(1) GK4F's physical primitive-rotation count, whose zero/positive grade
    survives every original F55 and P92B proof comparison; and
(2) GK4J's strictly positive genuine primitive route-leaf count, preserved
    by the nine original P92B comparison constructors ONLY when the
    source has ZERO physical primitive rotations.

Combine them into a SINGLE well-defined Option Nat observation on the
ACTUAL original P92B existence quotient: some(leafCount) on the genuine
zero-rotation subfiber, none on its positive-rotation complement.
The target is not the raw Type-valued comparison proof. The observer
refines the exact GK4G Boolean quotient grade via Option.isSome.

For the fixed TRUE GK4H F54-induced original P92B quotient composition,
the observer preserves an absorbing partial-addition operation:
some a * some b = some (a+b), and none absorbs on either side.
Every represented some n has n > 0, hence some 0 is absent from its
image; the ambient Option Nat operation is NOT a replacement unit
for the nonunital original P92B quotient.

In particular, no global leaf-count invariance across the real
positive-rotation pentagon (3 versus 2) is asserted, no alternative
P92B composition or P92B associativity is constructed, and no
original P92B/F19/F28/F54/F55 typed equivalence is inferred.
Genuine 14D unconditional countability, the old FJ exact aleph-null
assumption removal, true 19D fillers, global strict n and hyperdescent
remain outside this theorem's authority.

Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root, 107 public roots, no Gray, protected
validation-only PR #1558 remains Draft/open/unmerged.
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

/-- Multiplication of partial genuine zero-rotation leaf measurements:
only two defined numeric observations add; none is absorbing. -/
def nativeGK4KAdd (x y : Option Nat) : Option Nat :=
  match x, y with
  | some a, some b => some (a + b)
  | _, _ => none

@[simp] theorem nativeGK4KAdd_some_some (a b : Nat) :
    nativeGK4KAdd (some a) (some b) = some (a + b) := by
  rfl

@[simp] theorem nativeGK4KAdd_none_left (x : Option Nat) :
    nativeGK4KAdd none x = none := by
  cases x <;> rfl

@[simp] theorem nativeGK4KAdd_none_right (x : Option Nat) :
    nativeGK4KAdd x none = none := by
  cases x <;> rfl

theorem nativeGK4KAdd_assoc (x y z : Option Nat) :
    nativeGK4KAdd (nativeGK4KAdd x y) z =
      nativeGK4KAdd x (nativeGK4KAdd y z) := by
  cases x <;> cases y <;> cases z <;>
    simp [nativeGK4KAdd, Nat.add_assoc]

section Descend
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- This is a genuine raw original F54 observation. It deliberately
discards the numeric leaf count on the positive-rotation subfiber. -/
def nativeGK4KRawOption
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Option Nat :=
  if route.rotationCount = 0 then some route.gk4jLeafCount else none

/-- All nine ORIGINAL P92B comparison constructors respect the
Option Nat observation, without any false global numerical invariance. -/
theorem nativeGK4KRawOption_P92B_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    nativeGK4KRawOption first last r =
      nativeGK4KRawOption first last s := by
  by_cases hr : r.rotationCount = 0
  · have hs : s.rotationCount = 0 :=
      (nativeGK4FP92B_zero_rotation_iff cell).mp hr
    have hl : r.gk4jLeafCount = s.gk4jLeafCount :=
      nativeGK4JP92B_zero_leafCount_sound cell hr
    simp [nativeGK4KRawOption, hr, hs, hl]
  · have hs : s.rotationCount ≠ 0 := by
      intro hs
      exact hr ((nativeGK4FP92B_zero_rotation_iff cell).mpr hs)
    simp [nativeGK4KRawOption, hr, hs]

/-- Descended, representative-independent observer on the ACTUAL
original P92B proof-witness-existence quotient, not a new quotient. -/
def nativeGK4KP92Option :
    NativeF55P92AssocRouteClasses first last → Option Nat :=
  _root_.Quotient.lift (nativeGK4KRawOption first last)
    (fun r s h => h.elim (fun cell =>
      nativeGK4KRawOption_P92B_sound first last cell))

@[simp] theorem nativeGK4KP92Option_class
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4KP92Option first last
        (nativeF55P92AssocRouteClass first last route) =
      nativeGK4KRawOption first last route := by
  rfl

/-- The Option Nat observation is the unique original P92B quotient
observer agreeing with this genuine F54 definition on all classes. -/
theorem nativeGK4KP92Option_unique
    (observer : NativeF55P92AssocRouteClasses first last → Option Nat)
    (hsound : ∀ route : KuuNativeF45Tree.DepthRotationRoute p first last,
      observer (nativeF55P92AssocRouteClass first last route) =
        nativeGK4KRawOption first last route) :
    observer = nativeGK4KP92Option first last := by
  funext q
  refine _root_.Quotient.inductionOn q ?_
  intro route
  simpa only [nativeGK4KP92Option_class] using hsound route

/-- Option.isSome recovers exactly the original GK4G zero/positive
Bool grading on the same original P92B quotient. -/
theorem nativeGK4KP92Option_grade
    (q : NativeF55P92AssocRouteClasses first last) :
    (nativeGK4KP92Option first last q).isSome =
      nativeGK4GP92Grade first last q := by
  refine _root_.Quotient.inductionOn q ?_
  intro route
  change (if route.rotationCount = 0 then some route.gk4jLeafCount else none).isSome =
    decide (route.rotationCount = 0)
  by_cases hz : route.rotationCount = 0 <;> simp [hz]

/-- Every value some n on the TRUE original P92B quotient has n > 0;
the numeric part is never the additive identity. -/
theorem nativeGK4KP92Option_some_pos
    (q : NativeF55P92AssocRouteClasses first last) (k : Nat)
    (hk : nativeGK4KP92Option first last q = some k) : 0 < k := by
  revert hk
  refine _root_.Quotient.inductionOn q ?_
  intro route hk
  change (if route.rotationCount = 0 then some route.gk4jLeafCount else none) = some k at hk
  by_cases hz : route.rotationCount = 0
  · have hleaves : route.gk4jLeafCount = k := by
      simpa [hz] using hk
    simpa only [hleaves] using (nativeGK4J_leafCount_pos route)
  · simp [hz] at hk

/-- The ambient Option Nat unit some 0 is absent from EVERY actual
original P92B hom-fiber, not merely a selected zero-chain class. -/
theorem nativeGK4KP92Option_no_zero
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4KP92Option first last q ≠ some 0 := by
  intro h
  have hp := nativeGK4KP92Option_some_pos first last q 0 h
  omega

end Descend

section Composition
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

/-- Exact composition law on original F54 representatives. The real
physical rotation count is additive, as is GK4J leaf count. -/
theorem nativeGK4KRawOption_trans
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    nativeGK4KRawOption t₁ t₃ (.trans u v) =
      nativeGK4KAdd
        (nativeGK4KRawOption t₁ t₂ u)
        (nativeGK4KRawOption t₂ t₃ v) := by
  by_cases hu : u.rotationCount = 0
  · by_cases hv : v.rotationCount = 0
    · have hs : u.rotationCount + v.rotationCount = 0 := by omega
      simp [nativeGK4KRawOption, nativeGK4KAdd,
        nativeGK4H_raw_rotationCount_compose, nativeGK4J_leafCount_trans,
        hu, hv, hs]
    · have hs : u.rotationCount + v.rotationCount ≠ 0 := by omega
      simp [nativeGK4KRawOption, nativeGK4KAdd,
        nativeGK4H_raw_rotationCount_compose, nativeGK4J_leafCount_trans,
        hu, hv, hs]
  · by_cases hv : v.rotationCount = 0
    · have hs : u.rotationCount + v.rotationCount ≠ 0 := by omega
      simp [nativeGK4KRawOption, nativeGK4KAdd,
        nativeGK4H_raw_rotationCount_compose, nativeGK4J_leafCount_trans,
        hu, hv, hs]
    · have hs : u.rotationCount + v.rotationCount ≠ 0 := by omega
      simp [nativeGK4KRawOption, nativeGK4KAdd,
        nativeGK4H_raw_rotationCount_compose, nativeGK4J_leafCount_trans,
        hu, hv, hs]

/-- The TRUE F54-induced original P92B quotient composition is
observed multiplicatively, not replaced by a fabricated operation. -/
theorem nativeGK4KP92Option_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4KP92Option t₁ t₃
        (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      nativeGK4KAdd
        (nativeGK4KP92Option t₁ t₂ u)
        (nativeGK4KP92Option t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  simpa only [nativeGK4H_p92Compose_class, nativeGK4KP92Option_class] using
    nativeGK4KRawOption_trans t₁ t₂ t₃ r s

/-- The positive numeric observations add exactly under genuine
original P92B composition. -/
theorem nativeGK4KP92Option_some_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃)
    (a b : Nat)
    (hu : nativeGK4KP92Option t₁ t₂ u = some a)
    (hv : nativeGK4KP92Option t₂ t₃ v = some b) :
    nativeGK4KP92Option t₁ t₃
        (nativeGK4H_p92Compose t₁ t₂ t₃ u v) = some (a + b) := by
  rw [nativeGK4KP92Option_compose, hu, hv]
  rfl

/-- A genuine positive-rotation first route forces none. -/
theorem nativeGK4KP92Option_none_left
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃)
    (hu : nativeGK4KP92Option t₁ t₂ u = none) :
    nativeGK4KP92Option t₁ t₃
        (nativeGK4H_p92Compose t₁ t₂ t₃ u v) = none := by
  rw [nativeGK4KP92Option_compose, hu]
  simp

/-- A genuine positive-rotation second route forces none. -/
theorem nativeGK4KP92Option_none_right
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃)
    (hv : nativeGK4KP92Option t₂ t₃ v = none) :
    nativeGK4KP92Option t₁ t₃
        (nativeGK4H_p92Compose t₁ t₂ t₃ u v) = none := by
  rw [nativeGK4KP92Option_compose, hv]
  simp

end Composition

section PhysicalNorth
/-- The genuine C60 north F45 triple has a concrete original P92B
quotient whose Option Nat image excludes some 0 unconditionally. -/
theorem nativeGK4K_physical_north_P92B_no_zero :
    ∀ q : NativeF55P92AssocRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      nativeGK4KP92Option
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q ≠ some 0 := by
  intro q
  exact nativeGK4KP92Option_no_zero
    nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q
end PhysicalNorth

#print axioms nativeGK4KAdd
#print axioms nativeGK4KAdd_some_some
#print axioms nativeGK4KAdd_none_left
#print axioms nativeGK4KAdd_none_right
#print axioms nativeGK4KAdd_assoc
#print axioms nativeGK4KRawOption
#print axioms nativeGK4KRawOption_P92B_sound
#print axioms nativeGK4KP92Option
#print axioms nativeGK4KP92Option_class
#print axioms nativeGK4KP92Option_unique
#print axioms nativeGK4KP92Option_grade
#print axioms nativeGK4KP92Option_some_pos
#print axioms nativeGK4KP92Option_no_zero
#print axioms nativeGK4KRawOption_trans
#print axioms nativeGK4KP92Option_compose
#print axioms nativeGK4KP92Option_some_compose
#print axioms nativeGK4KP92Option_none_left
#print axioms nativeGK4KP92Option_none_right
#print axioms nativeGK4K_physical_north_P92B_no_zero

end
end Kuu.F112.Physical
