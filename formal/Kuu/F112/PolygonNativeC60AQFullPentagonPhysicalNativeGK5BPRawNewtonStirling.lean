import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BOForwardDifferenceFactorial
import Mathlib.RingTheory.Polynomial.Pochhammer
import Mathlib.Combinatorics.Enumerative.Stirling
import Mathlib.Algebra.Group.ForwardDiff
import Mathlib.Tactic

/-!
F112-P94D3GK5BP — RAW OBSERVATION / SIGNED STIRLING
NEWTON COEFFICIENT CERTIFICATES.

Unlike GK5BO, the input here is ONLY an observed finite table
of values at integer indices 0,...,d. We compute the true
mathlib forward differences directly from its values, then
construct a genuine rational polynomial using the falling
factorial basis (descPochhammer). The signed first-kind
Stirling transform is implemented using the true integral
coefficients of these falling factorial polynomials.

An ACTUAL Int[X] monomial coefficient lift is equivalent to a
FINITE integer-valued signed Stirling transform, not to mere
integer-valued observations. No original F55 Type-valued source
or P94A four-cell is inferred from such a certificate.

Pinned mathlib: forward differences / Gregory–Newton,
Polynomial.descPochhammer, and Nat.stirlingFirst.
Strict 空; independent Kuu→Qi. Original F54 two Nat /
two categories / Blocks, F55 Type witness history retained.
Append-only public root107, protected #1558 Draft/open/unmerged.
Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms/sorry/admit/native_decide/Gray/GK5BA kit/
unconditional original P89 reflection or GK5AY seam.
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

/-- Signed first-kind Stirling coefficients, given by the
genuine integer coefficient of the falling factorial polynomial
X(X-1)...(X-k+1), not by a noncanonical choice of proof. -/
def nativeGK5BPSignedFirst (k j : Nat) : Int :=
  (descPochhammer Int k).coeff j

/-- The signed Stirling coefficient has the exact same value
in the rational falling factorial after the integer cast. -/
theorem nativeGK5BPSignedFirst_rat (k j : Nat) :
    (descPochhammer Rat k).coeff j =
      (nativeGK5BPSignedFirst k j : Rat) := by
  have h := descPochhammer_map (Int.castRingHom Rat) k
  have hc := congrArg (fun P : Polynomial Rat => P.coeff j) h
  simpa only [Polynomial.coeff_map, Int.coe_castRingHom,
    nativeGK5BPSignedFirst] using hc.symm

/-- The genuine k-th forward difference of the ORIGINAL
observation function itself, without access to polynomial
coefficients or truncations. -/
def nativeGK5BPRawForward (values : Nat → Rat) (k : Nat) : Rat :=
  ((fwdDiff (1 : Nat))^[k] values) 0

/-- Raw forward differences are explicitly computable from
the finite observation table through an alternating binomial
sum. Only original values at indices 0,...,k occur. -/
theorem nativeGK5BPRawForward_observations
    (values : Nat → Rat) (k : Nat) :
    nativeGK5BPRawForward values k =
      ∑ j ∈ Finset.range (k + 1),
        (((-1 : Int) ^ (k - j) * (k.choose j : Int))) •
          values ((0 : Nat) + j • (1 : Nat)) := by
  exact fwdDiff_iter_eq_sum_shift (1 : Nat) values k (0 : Nat)

/-- Gregory–Newton's exact finite observation identity,
valid for EVERY function Nat→Rat (not just polynomial values). -/
theorem nativeGK5BPRawGregoryNewton
    (values : Nat → Rat) (n : Nat) :
    values n =
      ∑ k ∈ Finset.range (n + 1),
        (n.choose k : Rat) * nativeGK5BPRawForward values k := by
  have h := shift_eq_sum_fwdDiff_iter (1 : Nat) values n (0 : Nat)
  simpa [nativeGK5BPRawForward, nsmul_eq_mul] using h

/-- CONSTRUCT a genuine rational Newton interpolation polynomial
from ONLY the observed function and its finite forward
differences. The rational factorial division is explicit. -/
def nativeGK5BPNewtonFromRaw (d : Nat) (values : Nat → Rat) :
    Polynomial Rat :=
  ∑ k ∈ Finset.range (d + 1),
    Polynomial.C
      (nativeGK5BPRawForward values k / (k.factorial : Rat)) *
      descPochhammer Rat k

/-- Exact signed first-kind Stirling conversion from raw finite
differences to the j-th MONOMIAL coefficient of the actually
constructed Newton interpolation polynomial. -/
theorem nativeGK5BPNewton_coeff_stirling
    (d j : Nat) (values : Nat → Rat) :
    (nativeGK5BPNewtonFromRaw d values).coeff j =
      ∑ k ∈ Finset.range (d + 1),
        (nativeGK5BPRawForward values k / (k.factorial : Rat)) *
          (nativeGK5BPSignedFirst k j : Rat) := by
  simp only [nativeGK5BPNewtonFromRaw, Polynomial.finset_sum_coeff,
    Polynomial.coeff_C_mul]
  apply Finset.sum_congr rfl
  intro k hk
  rw [nativeGK5BPSignedFirst_rat k j]

/-- The degree of the genuinely CONSTRUCTED Newton polynomial
never exceeds the finite observation horizon d. -/
theorem nativeGK5BPNewton_natDegree_le
    (d : Nat) (values : Nat → Rat) :
    (nativeGK5BPNewtonFromRaw d values).natDegree ≤ d := by
  apply (Polynomial.natDegree_le_iff_coeff_eq_zero).2
  intro j hj
  rw [nativeGK5BPNewtonFromRaw, Polynomial.finset_sum_coeff]
  apply Finset.sum_eq_zero
  intro k hk
  have hk' : k ≤ d := by
    have h := Finset.mem_range.mp hk
    omega
  have hdeg : (descPochhammer Rat k).natDegree ≤ k := by
    rw [descPochhammer_natDegree]
  have hzero : (descPochhammer Rat k).coeff j = 0 :=
    (Polynomial.natDegree_le_iff_coeff_eq_zero).mp hdeg j (by omega)
  simp [Polynomial.coeff_C_mul, hzero]

/-- The rational Newton polynomial recovers EVERY supplied
raw observation at n ≤ d, without assuming that the values
are polynomial-generated or integral. -/
theorem nativeGK5BPNewton_eval_raw
    (d : Nat) (values : Nat → Rat) (n : Nat) (hn : n ≤ d) :
    (nativeGK5BPNewtonFromRaw d values).eval (n : Rat) =
      values n := by
  unfold nativeGK5BPNewtonFromRaw
  rw [Polynomial.eval_finset_sum]
  simp only [Polynomial.eval_C_mul]
  have hterm (k : Nat) :
      (nativeGK5BPRawForward values k / (k.factorial : Rat)) *
        (descPochhammer Rat k).eval (n : Rat) =
        (n.choose k : Rat) * nativeGK5BPRawForward values k := by
    rw [Nat.cast_choose_eq_descPochhammer_div]
    ring
  calc
    ∑ k ∈ Finset.range (d + 1),
        (nativeGK5BPRawForward values k / (k.factorial : Rat)) *
          (descPochhammer Rat k).eval (n : Rat) =
      ∑ k ∈ Finset.range (d + 1),
        (n.choose k : Rat) * nativeGK5BPRawForward values k := by
          apply Finset.sum_congr rfl
          intro k hk
          exact hterm k
    _ = ∑ k ∈ Finset.range (n + 1),
          (n.choose k : Rat) * nativeGK5BPRawForward values k := by
          symm
          apply Finset.sum_subset (Finset.range_mono (by omega))
          intro k hk hknot
          have hnk : n < k := by
            have hnot : ¬ k < n + 1 := by
              simpa only [Finset.mem_range] using hknot
            omega
          simp [Nat.choose_eq_zero_of_lt hnk]
    _ = values n := (nativeGK5BPRawGregoryNewton values n).symm

/-- Independent constructive equality of the raw Newton
interpolant and the existing GK5BL genuine rational Lagrange
interpolant on the canonical integer observation grid. -/
theorem nativeGK5BPNewton_eq_lagrange
    (d : Nat) (values : Nat → Rat) :
    nativeGK5BPNewtonFromRaw d values =
      nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
        (fun z : Int => values z.toNat) := by
  have hdegree :
      (nativeGK5BPNewtonFromRaw d values).degree <
        (nativeGK5BKIntegerGrid d).card := by
    rw [nativeGK5BKIntegerGrid_card]
    have hd := (Polynomial.natDegree_le_iff_degree_le).mp
      (nativeGK5BPNewton_natDegree_le d values)
    exact lt_of_le_of_lt hd
      (WithBot.coe_lt_coe.mpr (Nat.lt_succ_self d))
  symm
  calc
    nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
        (fun z : Int => values z.toNat) =
      nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
        (fun z : Int =>
          (nativeGK5BPNewtonFromRaw d values).eval (z : Rat)) := by
            apply Lagrange.interpolate_eq_of_values_eq_on
            intro z hz
            change z ∈ (Finset.range (d + 1)).image
              (fun k : Nat => (k : Int)) at hz
            rcases Finset.mem_image.mp hz with ⟨k, hk, hzk⟩
            subst z
            have hk' : k ≤ d := by
              have h := Finset.mem_range.mp hk
              omega
            simpa using (nativeGK5BPNewton_eval_raw d values k hk').symm
    _ = nativeGK5BPNewtonFromRaw d values :=
      nativeGK5BLRationalInterpolant_recovers_rat _
        (nativeGK5BKIntegerGrid d) hdegree

/-- CENTRAL GK5BP: a complete FINITE integer monomial lift
criterion, using only the ORIGINAL observed values, their
forward differences, and signed first-kind Stirling coefficients.
No original rational monomial coefficients are supplied. -/
theorem nativeGK5BPNewton_integral_iff_rawStirling
    (d : Nat) (values : Nat → Rat) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d values) ↔
    (∀ j ∈ Finset.range (d + 1), ∃ z : Int,
      (z : Rat) =
        ∑ k ∈ Finset.range (d + 1),
          (nativeGK5BPRawForward values k / (k.factorial : Rat)) *
            (nativeGK5BPSignedFirst k j : Rat)) := by
  constructor
  · intro h j hj
    obtain ⟨z, hz⟩ :=
      (nativeGK5BMIntegralLift_iff _).1 h j
    refine ⟨z, ?_⟩
    rw [← nativeGK5BPNewton_coeff_stirling]
    exact hz
  · intro h
    apply (nativeGK5BMIntegralLift_iff _).2
    intro j
    by_cases hj : j ∈ Finset.range (d + 1)
    · obtain ⟨z, hz⟩ := h j hj
      refine ⟨z, ?_⟩
      rw [nativeGK5BPNewton_coeff_stirling]
      exact hz
    · have hj' : d < j := by
        have hnot : ¬ j < d + 1 := by
          simpa only [Finset.mem_range] using hj
        omega
      have hcoeff : (nativeGK5BPNewtonFromRaw d values).coeff j = 0 :=
        (Polynomial.natDegree_le_iff_coeff_eq_zero).mp
          (nativeGK5BPNewton_natDegree_le d values) j hj'
      exact ⟨0, by simp [hcoeff]⟩

/-- The criterion also applies to the ACTUAL GK5BL Lagrange
polynomial of arbitrary observed values on the canonical
integer grid, not just to the syntactic Newton polynomial. -/
theorem nativeGK5BPLagrange_integral_iff_rawStirling
    (d : Nat) (values : Nat → Rat) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
          (fun z : Int => values z.toNat)) ↔
    (∀ j ∈ Finset.range (d + 1), ∃ z : Int,
      (z : Rat) =
        ∑ k ∈ Finset.range (d + 1),
          (nativeGK5BPRawForward values k / (k.factorial : Rat)) *
            (nativeGK5BPSignedFirst k j : Rat)) := by
  rw [← nativeGK5BPNewton_eq_lagrange]
  exact nativeGK5BPNewton_integral_iff_rawStirling d values

/-- SPECIALIZE to integer-valued raw observations, without
falsely concluding an unconditional Int[X] coefficient lift. -/
theorem nativeGK5BPIntObservations_integral_iff_rawStirling
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1), ∃ z : Int,
      (z : Rat) =
        ∑ k ∈ Finset.range (d + 1),
          (nativeGK5BPRawForward (fun n : Nat => (values n : Rat)) k /
            (k.factorial : Rat)) *
            (nativeGK5BPSignedFirst k j : Rat)) :=
  nativeGK5BPLagrange_integral_iff_rawStirling d
    (fun n : Nat => (values n : Rat))

#print axioms nativeGK5BPSignedFirst_rat
#print axioms nativeGK5BPRawForward_observations
#print axioms nativeGK5BPRawGregoryNewton
#print axioms nativeGK5BPNewton_coeff_stirling
#print axioms nativeGK5BPNewton_natDegree_le
#print axioms nativeGK5BPNewton_eval_raw
#print axioms nativeGK5BPNewton_eq_lagrange
#print axioms nativeGK5BPNewton_integral_iff_rawStirling
#print axioms nativeGK5BPLagrange_integral_iff_rawStirling
#print axioms nativeGK5BPIntObservations_integral_iff_rawStirling

end
end Kuu.F112.Physical
