import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BPRawNewtonStirling
import Mathlib.RingTheory.Polynomial.Pochhammer
import Mathlib.Combinatorics.Enumerative.Stirling
import Mathlib.Algebra.Group.ForwardDiff
import Mathlib.Tactic

/-!
F112-P94D3GK5BQ — PINNED MATHLIB SIGNED STIRLING
IDENTIFICATION AND ACTUAL FACTORIAL DIVISIBILITY CERTIFICATES.

GK5BP defined signed first-kind coefficients as the GENUINE
Int[X] coefficients of descPochhammer. GK5BQ identifies these
coefficients with the correctly signed Nat.stirlingFirst
counts using genuine polynomial and Stirling recurrences.

For integer raw observations v:Nat→Int, genuine finite
differences are integers. A canonical integer numerator for
each degree j is constructed with the explicit factorial ratios
d!/k!, the actual integer forward differences, and actual
signed polynomial/Stirling coefficients. Integer monomial
coefficient realization is EQUIVALENT to finitely many explicit
integer divisibility tests d! | numerator(j). This criterion
does NOT assume integer-valued observations alone suffice.

No inverse F55 Type history, P77 source-class equality, new
P94A four-cell, unconditional P89 reflection or global seam.
Strict 空; independent Kuu→Qi; true F54 two Nat/two category/
Blocks and F55 Type witnesses retained.
Append-only public root107, protected #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, GK5BA kit or Gray.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
open Finset
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The exact native one-step recurrence for the signed
coefficients of the true falling factorial, obtained from
the actual descPochhammer multiplication by X-n. -/
theorem nativeGK5BQSignedFirst_succ_succ (n j : Nat) :
    nativeGK5BPSignedFirst (n + 1) (j + 1) =
      nativeGK5BPSignedFirst n j -
        (n : Int) * nativeGK5BPSignedFirst n (j + 1) := by
  simp [nativeGK5BPSignedFirst, descPochhammer_succ_right,
    mul_sub, Polynomial.coeff_sub, Polynomial.coeff_mul_X] <;> ring

/-- Exact signed first-kind Stirling coefficient identity.
The exponent n+j has the same sign as n-j where j≤n, and
its addition-only form makes the recurrence total on all Nat. -/
theorem nativeGK5BQSignedFirst_eq_natStirling_addSign
    (n j : Nat) :
    nativeGK5BPSignedFirst n j =
      (-1 : Int) ^ (n + j) * (Nat.stirlingFirst n j : Int) := by
  induction n generalizing j with
  | zero =>
      cases j with
      | zero =>
          norm_num [nativeGK5BPSignedFirst, descPochhammer_zero]
      | succ j =>
          simp [nativeGK5BPSignedFirst, descPochhammer_zero,
            Nat.stirlingFirst_zero_succ, Polynomial.coeff_one]
  | succ n ih =>
      cases j with
      | zero =>
          simp [nativeGK5BPSignedFirst, descPochhammer_succ_left,
            Polynomial.coeff_X_mul_zero, Nat.stirlingFirst_succ_zero]
      | succ j =>
          rw [nativeGK5BQSignedFirst_succ_succ, ih j, ih (j + 1),
            Nat.stirlingFirst_succ_succ]
          push_cast
          have h₁ : n + (j + 1) = (n + j) + 1 := by omega
          have h₂ : (n + 1) + (j + 1) = (n + j) + 2 := by omega
          rw [h₁, h₂]
          simp only [pow_add, pow_one, pow_two]
          ring

/-- Standard signed first-kind Stirling formula with n-j.
The indicated inequality is explicitly required; no Nat
subtraction underflow is silently used. -/
theorem nativeGK5BQSignedFirst_eq_natStirling
    (n j : Nat) (hj : j ≤ n) :
    nativeGK5BPSignedFirst n j =
      (-1 : Int) ^ (n - j) * (Nat.stirlingFirst n j : Int) := by
  rw [nativeGK5BQSignedFirst_eq_natStirling_addSign]
  have heq : n + j = (n - j) + 2 * j := by omega
  rw [heq, pow_add, pow_mul]
  norm_num

/-- Observed integer forward difference, computed entirely
from original integer values by actual pinned Mathlib fwdDiff. -/
def nativeGK5BQIntRawForward (values : Nat → Int) (k : Nat) : Int :=
  ((fwdDiff (1 : Nat))^[k] values) 0

/-- Forward difference of cast integer observations equals
the exact cast of their genuine integer forward difference. -/
theorem nativeGK5BQIntRawForward_cast
    (values : Nat → Int) (k : Nat) :
    nativeGK5BPRawForward
      (fun n : Nat => (values n : Rat)) k =
      (nativeGK5BQIntRawForward values k : Rat) := by
  unfold nativeGK5BPRawForward nativeGK5BQIntRawForward
  rw [fwdDiff_iter_eq_sum_shift (1 : Nat)
        (fun n : Nat => (values n : Rat)) k (0 : Nat),
      fwdDiff_iter_eq_sum_shift (1 : Nat) values k (0 : Nat)]
  simp [zsmul_eq_mul]

/-- Explicit integer factorial quotient. For k≤d its
product with k! equals d!, by genuine Nat factorial
divisibility in the pinned Mathlib. -/
def nativeGK5BQFactorialQuotient (d k : Nat) : Nat :=
  d.factorial / k.factorial

theorem nativeGK5BQFactorialQuotient_rat
    (d k : Nat) (hk : k ≤ d) :
    (k.factorial : Rat) *
      (nativeGK5BQFactorialQuotient d k : Rat) =
        (d.factorial : Rat) := by
  have h := Nat.mul_div_cancel' (Nat.factorial_dvd_factorial hk)
  have hnat :
      k.factorial * (d.factorial / k.factorial) = d.factorial := by
    simpa only [mul_comm] using h
  exact_mod_cast hnat

/-- A CONSTRUCTED genuine integer common-denominator numerator
computed from finitely many actual integer observations,
their true integer forward differences, exact factorial
quotients, and the true signed first-kind coefficients. -/
def nativeGK5BQClearedNumerator
    (d j : Nat) (values : Nat → Int) : Int :=
  ∑ k ∈ Finset.range (d + 1),
    (nativeGK5BQFactorialQuotient d k : Int) *
      nativeGK5BQIntRawForward values k *
      nativeGK5BPSignedFirst k j

/-- Entirely in terms of Mathlib's Nat.stirlingFirst,
with the sign certified by the genuine descPochhammer
polynomial identity; not a conjectural correspondence. -/
theorem nativeGK5BQClearedNumerator_natStirling
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BQClearedNumerator d j values =
      ∑ k ∈ Finset.range (d + 1),
        (nativeGK5BQFactorialQuotient d k : Int) *
          nativeGK5BQIntRawForward values k *
          ((-1 : Int) ^ (k + j) * (Nat.stirlingFirst k j : Int)) := by
  simp only [nativeGK5BQClearedNumerator,
    nativeGK5BQSignedFirst_eq_natStirling_addSign]

/-- Main EXACT SCALING identity: d! times the j-th actual
rational Newton monomial coefficient is the cast of an
explicitly constructed integer numerator from raw samples.
There is no requirement to know any source polynomial P. -/
theorem nativeGK5BQNewton_scaledCoeff
    (d j : Nat) (values : Nat → Int) :
    (d.factorial : Rat) *
      (nativeGK5BPNewtonFromRaw d
        (fun n : Nat => (values n : Rat))).coeff j =
      (nativeGK5BQClearedNumerator d j values : Rat) := by
  rw [nativeGK5BPNewton_coeff_stirling]
  simp only [Finset.mul_sum, nativeGK5BQClearedNumerator,
    Int.cast_sum]
  apply Finset.sum_congr rfl
  intro k hk
  have hle : k ≤ d := by
    have h := Finset.mem_range.mp hk
    omega
  have hr := nativeGK5BQFactorialQuotient_rat d k hle
  have hc := nativeGK5BQIntRawForward_cast values k
  rw [hc]
  simp only [Int.cast_mul, Int.cast_natCast]
  have hn : (k.factorial : Rat) ≠ 0 := by
    exact_mod_cast Nat.factorial_ne_zero k
  calc
    (d.factorial : Rat) *
        ((nativeGK5BQIntRawForward values k : Rat) / (k.factorial : Rat) *
          (nativeGK5BPSignedFirst k j : Rat)) =
      ((k.factorial : Rat) *
          (nativeGK5BQFactorialQuotient d k : Rat)) *
        ((nativeGK5BQIntRawForward values k : Rat) / (k.factorial : Rat) *
          (nativeGK5BPSignedFirst k j : Rat)) := by rw [hr]
    _ = (nativeGK5BQFactorialQuotient d k : Rat) *
          (nativeGK5BQIntRawForward values k : Rat) *
          (nativeGK5BPSignedFirst k j : Rat) := by
            field_simp [hn] <;> ring

/-- EXACT finite integer divisibility certificate for
integer-valued raw samples, with no assumed polynomial
coefficients and no falsely inferred F55 Type witness.
The integer numerator is actually constructed above. -/
theorem nativeGK5BQNewton_integral_iff_divisible
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j values) := by
  constructor
  · intro h j hj
    obtain ⟨z, hz⟩ :=
      (nativeGK5BPNewton_integral_iff_rawStirling d
        (fun n : Nat => (values n : Rat))).1 h j hj
    have hscale := nativeGK5BQNewton_scaledCoeff d j values
    rw [nativeGK5BPNewton_coeff_stirling, ← hz] at hscale
    have hInt : (d.factorial : Int) * z =
        nativeGK5BQClearedNumerator d j values := by
      exact_mod_cast hscale
    exact ⟨z, hInt.symm⟩
  · intro h
    apply (nativeGK5BPNewton_integral_iff_rawStirling d
      (fun n : Nat => (values n : Rat))).2
    intro j hj
    obtain ⟨z, hz⟩ := h j hj
    have hscale := nativeGK5BQNewton_scaledCoeff d j values
    rw [nativeGK5BPNewton_coeff_stirling] at hscale
    have hcast : (d.factorial : Rat) * (z : Rat) =
        (nativeGK5BQClearedNumerator d j values : Rat) := by
      exact_mod_cast hz.symm
    have hn : (d.factorial : Rat) ≠ 0 := by
      exact_mod_cast Nat.factorial_ne_zero d
    exact ⟨z, mul_left_cancel₀ hn (hcast.trans hscale.symm)⟩

/-- The same EXACT complete finite integer-divisibility
criterion on original GK5BL rational Lagrange interpolation
from the canonical integer observation sites. -/
theorem nativeGK5BQLagrange_integral_iff_divisible
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant
          (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j values) := by
  simpa only [nativeGK5BPNewton_eq_lagrange] using
    (nativeGK5BQNewton_integral_iff_divisible d values)

/-- Any observed integer numerator failing divisibility by
d! at some j≤d is a genuine obstruction to an Int[X]
coefficient lift, not to Type-valued F55 sources or seams. -/
theorem nativeGK5BQNoIntegerLift_of_notDvd
    (d : Nat) (values : Nat → Int)
    (j : Nat) (hj : j ∈ Finset.range (d + 1))
    (hnot : ¬ (d.factorial : Int) ∣
      nativeGK5BQClearedNumerator d j values) :
    ¬ ∃ P : Polynomial Int,
       P.map (Int.castRingHom Rat) =
         nativeGK5BPNewtonFromRaw d
           (fun n : Nat => (values n : Rat)) := by
  intro h
  exact hnot ((nativeGK5BQNewton_integral_iff_divisible d values).1 h j hj)

#print axioms nativeGK5BQSignedFirst_succ_succ
#print axioms nativeGK5BQSignedFirst_eq_natStirling_addSign
#print axioms nativeGK5BQSignedFirst_eq_natStirling
#print axioms nativeGK5BQIntRawForward_cast
#print axioms nativeGK5BQFactorialQuotient_rat
#print axioms nativeGK5BQClearedNumerator_natStirling
#print axioms nativeGK5BQNewton_scaledCoeff
#print axioms nativeGK5BQNewton_integral_iff_divisible
#print axioms nativeGK5BQLagrange_integral_iff_divisible
#print axioms nativeGK5BQNoIntegerLift_of_notDvd

end
end Kuu.F112.Physical
