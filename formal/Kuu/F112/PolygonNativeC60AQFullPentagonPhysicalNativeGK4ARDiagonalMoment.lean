import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AQStrictLowerSlice
import Mathlib.Tactic

/-!
F112-P94D3GK4AR — the ORIGINAL GK4AD orderedMoment determines
the upper-left residue of the genuine GK4AH second integer matrix:
  M_AH(r).1.1 = 1 + 4 * (moment_AD(r) + triangle(backwardCount_AD(r)))
                   + 16 * t.
Here triangle(0)=0, triangle(n+1)=triangle(n)+n, i.e. C(n,2).
The existing GK4AQ lower-left mod16 and GK4AP upper-right mod4
congruences are RETAINED in the combined predicate.

Prove the triangular cocycle law without relying on undocumented
pinned mathlib choose identities. Derive the new diagonal cocycle from
the TRUE noncommutative Heisenberg AD product, exact AH 2x2 matrix
product, old upper-right AP and lower-left AQ congruences. All real
fully dependent F54 LocalRotation edges, chains, original five route
constructors and original P92B/independent S typed comparisons descend.
No new Type-valued source cell, original Q category axioms,
fixed infinite fiber, surjectivity, Gray or hyperdescent.
Append-only/tighten-only/same-root107; strict 空 central, independent
Kuu one presentation; protect draft/open/unmerged #1558.
Lean v4.30.0-rc2, pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Integer triangular number, canonically equal to the binomial
coefficient n choose 2, defined by an explicit proof-stable recursion. -/
def nativeGK4ARTriangle : Nat → Int
  | 0 => 0
  | n + 1 => nativeGK4ARTriangle n + (n : Int)

/-- Fundamental exact integer two-variable binomial cocycle law. -/
theorem nativeGK4ARTriangle_add (a b : Nat) :
    nativeGK4ARTriangle (a + b) =
      nativeGK4ARTriangle a + nativeGK4ARTriangle b +
      (a : Int) * (b : Int) := by
  induction b with
  | zero =>
      simp [nativeGK4ARTriangle]
  | succ b ih =>
      calc
        nativeGK4ARTriangle (a + (b + 1)) =
            nativeGK4ARTriangle (a + b) + ((a + b : Nat) : Int) := by
              rw [Nat.add_succ]
              rfl
        _ = nativeGK4ARTriangle a + nativeGK4ARTriangle b +
              (a : Int) * (b : Int) + ((a + b : Nat) : Int) := by
              rw [ih]
        _ = nativeGK4ARTriangle a + nativeGK4ARTriangle (b + 1) +
              (a : Int) * ((b + 1 : Nat) : Int) := by
              simp only [nativeGK4ARTriangle, Nat.cast_add, Nat.cast_succ]
              ring

/-- Verify that the recursive triangular number really is
n(n-1)/2, for every n (including n=0), without a division tactic. -/
theorem nativeGK4ARTriangle_double (n : Nat) :
    2 * nativeGK4ARTriangle n =
      (n : Int) * ((n : Int) - 1) := by
  induction n with
  | zero => decide
  | succ n ih =>
      change 2 * (nativeGK4ARTriangle n + (n : Int)) =
        ((n + 1 : Nat) : Int) * (((n + 1 : Nat) : Int) - 1)
      push_cast
      nlinarith [ih]

/-- Actual original AD ordered moment plus the triangular
backwardCount correction. NO independent source generator added. -/
def nativeGK4AROldDiagonalResidue (v : NativeGK4ADValue) : Int :=
  v.2 + nativeGK4ARTriangle v.1.2

/-- NEW observer compatibility, strictly retaining the full
previous GK4AQ/AP/AO predicate, not replacing it with a weak trace. -/
def nativeGK4ARDiagonalLinked
    (v : NativeGK4ADValue) (M : NativeGK4AHMatrix) : Prop :=
  nativeGK4AQLowerLinked v M ∧
    ∃ t : Int,
      M.1.1 = 1 + 4 * nativeGK4AROldDiagonalResidue v + 16 * t

/-- Real noncommutative AD * AH product preserves ordered-moment
upper-left mod16. The extra b_A*c_B term is reconciled exactly
by AP's b_A=charge_A+beta_A mod4 and AQ's c_B=4beta_B mod16.
No invented commutativity of the genuine source histories. -/
theorem nativeGK4ARDiagonalLinked_mul
    (u v : NativeGK4ADValue) (A B : NativeGK4AHMatrix)
    (hu : nativeGK4ARDiagonalLinked u A)
    (hv : nativeGK4ARDiagonalLinked v B) :
    nativeGK4ARDiagonalLinked (nativeGK4ADCombine u v)
      (nativeGK4AHMul A B) := by
  refine ⟨nativeGK4AQLowerLinked_mul u v A B hu.1 hv.1, ?_⟩
  rcases hu.2 with ⟨ta, ha⟩
  rcases hv.2 with ⟨tb, hb⟩
  rcases hu.1.1.2 with ⟨tk, hupper⟩
  rcases hv.1.2 with ⟨tl, hlower⟩
  let fu : Int := nativeGK4AROldDiagonalResidue u
  let fv : Int := nativeGK4AROldDiagonalResidue v
  let rho : Int := nativeGK4APOldUpperResidue u
  refine ⟨ta + tb + fu * fv + 4 * (fu * tb + ta * fv) +
      16 * ta * tb + rho * tl + tk * (v.1.2 : Int) + 4 * tk * tl, ?_⟩
  change A.1.1 * B.1.1 + A.1.2 * B.2.1 =
    1 + 4 * ((u.2 + v.2 + u.1.1 * (v.1.2 : Int)) +
      nativeGK4ARTriangle (u.1.2 + v.1.2)) +
    16 * (ta + tb + fu * fv + 4 * (fu * tb + ta * fv) +
      16 * ta * tb + rho * tl + tk * (v.1.2 : Int) + 4 * tk * tl)
  rw [nativeGK4ARTriangle_add, ha, hb, hupper, hlower]
  dsimp [fu, fv, rho, nativeGK4AROldDiagonalResidue,
    nativeGK4APOldUpperResidue]
  push_cast
  ring

theorem nativeGK4ARDiagonalLinked_one :
    nativeGK4ARDiagonalLinked nativeGK4ADZero nativeGK4AHOne := by
  refine ⟨nativeGK4AQLowerLinked_one, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4ARDiagonalLinked_cast :
    nativeGK4ARDiagonalLinked nativeGK4ADCast nativeGK4AHCast := by
  refine ⟨nativeGK4AQLowerLinked_cast, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4ARDiagonalLinked_forward :
    nativeGK4ARDiagonalLinked nativeGK4ADForward nativeGK4AHForward := by
  refine ⟨nativeGK4AQLowerLinked_forward, ⟨0, ?_⟩⟩
  decide

theorem nativeGK4ARDiagonalLinked_backward :
    nativeGK4ARDiagonalLinked nativeGK4ADBackward nativeGK4AHBackward := by
  refine ⟨nativeGK4AQLowerLinked_backward, ⟨0, ?_⟩⟩
  decide

section GenuineOriginalDependentSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

theorem nativeGK4AREdge_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4ARDiagonalLinked edge.gk4adValue edge.gk4ahMatrix := by
  cases edge with
  | forward _ => exact nativeGK4ARDiagonalLinked_forward
  | backward _ => exact nativeGK4ARDiagonalLinked_backward

theorem nativeGK4ARChain_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4ARDiagonalLinked chain.gk4adValue chain.gk4ahMatrix := by
  induction chain with
  | refl => exact nativeGK4ARDiagonalLinked_one
  | snoc path edge ih =>
      change nativeGK4ARDiagonalLinked
        (nativeGK4ADCombine path.gk4adValue edge.gk4adValue)
        (nativeGK4AHMul path.gk4ahMatrix edge.gk4ahMatrix)
      exact nativeGK4ARDiagonalLinked_mul _ _ _ _
        ih (nativeGK4AREdge_sound edge)

theorem nativeGK4ARRoute_sound
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4ARDiagonalLinked route.gk4adValue route.gk4ahMatrix := by
  induction route with
  | chain path => exact nativeGK4ARChain_sound path
  | castDepths _ _ _ => exact nativeGK4ARDiagonalLinked_cast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4ARDiagonalLinked_mul _ _ _ _ ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih
end GenuineOriginalDependentSource

section GenuineQuotientsAndFiber
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

theorem nativeGK4ARP92_sound
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4ARDiagonalLinked (nativeGK4ADP92Value first last q)
      (nativeGK4AHP92Value first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  change nativeGK4ARDiagonalLinked raw.gk4adValue raw.gk4ahMatrix
  exact nativeGK4ARRoute_sound raw

theorem nativeGK4ARStructural_sound
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4ARDiagonalLinked (nativeGK4ADStructuralValue first last s)
      (nativeGK4AHStructuralValue first last s) := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  change nativeGK4ARDiagonalLinked raw.gk4adValue raw.gk4ahMatrix
  exact nativeGK4ARRoute_sound raw

theorem nativeGK4ARKernel_sound
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    nativeGK4ARDiagonalLinked
      ((nativeGK4AIKernelValue first last z).1.1.2)
      ((nativeGK4AIKernelValue first last z).2) := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  change nativeGK4ARDiagonalLinked
    (nativeGK4ADP92Value first last q)
    (nativeGK4AHP92Value first last q)
  exact nativeGK4ARP92_sound first last q

theorem nativeGK4ARFiber_sound
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (z : nativeGK4AJOldFiber first last target) :
    nativeGK4ARDiagonalLinked
      ((nativeGK4AGKernelValue first last target).1.2)
      (nativeGK4AJFiberMatrix first last target z) := by
  have hz := nativeGK4ARKernel_sound first last z.1
  have hvalue := nativeGK4AIForgetMatrix_value first last z.1
  rw [z.2] at hvalue
  have hAD := congrArg
    (fun value : NativeGK4AGValue => value.1.2) hvalue
  change (nativeGK4AGKernelValue first last target).1.2 =
    (nativeGK4AIKernelValue first last z.1).1.1.2 at hAD
  change nativeGK4ARDiagonalLinked
    ((nativeGK4AGKernelValue first last target).1.2)
    ((nativeGK4AIKernelValue first last z.1).2)
  rw [hAD]
  exact hz

#print axioms nativeGK4ARTriangle
#print axioms nativeGK4ARTriangle_add
#print axioms nativeGK4ARTriangle_double
#print axioms nativeGK4AROldDiagonalResidue
#print axioms nativeGK4ARDiagonalLinked
#print axioms nativeGK4ARDiagonalLinked_mul
#print axioms nativeGK4ARDiagonalLinked_one
#print axioms nativeGK4ARDiagonalLinked_cast
#print axioms nativeGK4ARDiagonalLinked_forward
#print axioms nativeGK4ARDiagonalLinked_backward
#print axioms nativeGK4AREdge_sound
#print axioms nativeGK4ARChain_sound
#print axioms nativeGK4ARRoute_sound
#print axioms nativeGK4ARP92_sound
#print axioms nativeGK4ARStructural_sound
#print axioms nativeGK4ARKernel_sound
#print axioms nativeGK4ARFiber_sound

end GenuineQuotientsAndFiber

end
end Kuu.F112.Physical
