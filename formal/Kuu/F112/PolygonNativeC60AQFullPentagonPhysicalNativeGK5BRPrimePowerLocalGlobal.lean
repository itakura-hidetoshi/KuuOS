import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BQSignedStirlingDivisibility
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic

/-!
F112-P94D3GK5BR — FINITE PRIME-POWER LOCAL / GLOBAL
FACTORIAL DIVISIBILITY FOR GENUINE INTEGER RAW OBSERVATIONS.

The original GK5BQ numerator N_(d,j)(v) is retained without
alteration, and its exact factorial divisibility is decomposed
into the prime-power moduli p^(factorization(d!,p)) for the
ACTUAL finite primeFactors support of d!. Conversely, all
those local certificates reconstruct a single global Int[X]
Newton (and GK5BL Lagrange) coefficient source.

The proof handles zero and negative integer numerators,
uses the actual pinned mathlib factorization and divisibility
API, and retains the distinction between arithmetic
obstructions and original F55 Type-valued source/4-cell/
seam obstructions. Numerical gluing does NOT reconstruct
any original Type witness or imply unconditional P89 reflection.

Strict 空; independent Kuu→Qi; original F54/F55 history.
Append-only public root107; #1558 Draft/open/unmerged.
Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No axioms, admitted propositions or synthetic sources.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open Finset
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- For every nonzero natural modulus, finitely many MAXIMAL
prime-power divisibility checks are jointly equivalent to
divisibility by the original modulus. In particular the
numerator may be zero. This invokes the genuine pinned
mathlib theorem on all prime powers and its finite support. -/
theorem nativeGK5BRNat_dvd_iff_primePower
    (m n : Nat) (hm : m ≠ 0) :
    m ∣ n ↔
      ∀ p ∈ m.primeFactors,
        p ^ (m.factorization p) ∣ n := by
  constructor
  · intro h p hp
    exact (Nat.ordProj_dvd m p).trans h
  · intro h
    apply (Nat.dvd_iff_prime_pow_dvd_dvd n m).2
    intro p k hp hpow
    by_cases hk : k = 0
    · subst k
      simp
    have hdiv : p ∣ m :=
      (dvd_pow_self p hk).trans hpow
    have hmem : p ∈ m.primeFactors :=
      Nat.mem_primeFactors.mpr ⟨hp, hdiv, hm⟩
    have hle : k ≤ m.factorization p :=
      (hp.pow_dvd_iff_le_factorization hm).1 hpow
    exact (pow_dvd_pow p hle).trans (h p hmem)

/-- The preceding local-to-global theorem remains true
over Int, including negative and zero numerators: integer
divisibility by a positive natural modulus is equivalent
to divisibility of the natural absolute value. -/
theorem nativeGK5BRInt_dvd_iff_primePower
    (m : Nat) (n : Int) (hm : m ≠ 0) :
    (m : Int) ∣ n ↔
      ∀ p ∈ m.primeFactors,
        ((p ^ (m.factorization p) : Nat) : Int) ∣ n := by
  simpa only [Int.natCast_dvd] using
    (nativeGK5BRNat_dvd_iff_primePower m n.natAbs hm)

/-- The exponent is the actual p-adic valuation of d!,
not an invented prime multiplicity. -/
theorem nativeGK5BRFactorial_exponent_eq_padic
    (d p : Nat) (hp : p.Prime) :
    (d.factorial).factorization p =
      padicValNat p d.factorial :=
  Nat.factorization_def d.factorial hp

/-- The exact original integer numerator and its maximal
prime-power local divisibility certificate. -/
def nativeGK5BRPrimeLocal
    (d j : Nat) (values : Nat → Int) (p : Nat) : Prop :=
  (((p ^ ((d.factorial).factorization p) : Nat) : Int) ∣
    nativeGK5BQClearedNumerator d j values)

/-- Every local prime-power test is literally an integer
congruence to zero, including negative integer numerators. -/
theorem nativeGK5BRPrimeLocal_iff_congruence
    (d j : Nat) (values : Nat → Int) (p : Nat) :
    nativeGK5BRPrimeLocal d j values p ↔
      nativeGK5BQClearedNumerator d j values %
        ((p ^ ((d.factorial).factorization p) : Nat) : Int) = 0 := by
  exact Int.dvd_iff_emod_eq_zero

/-- Finite local certificates at all ACTUAL prime factors
of the factorial are equivalent to the original GK5BQ
single factorial divisibility test for each coefficient. -/
theorem nativeGK5BRFactorial_dvd_iff_finiteLocal
    (d j : Nat) (values : Nat → Int) :
    (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j values ↔
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j values p := by
  simpa only [nativeGK5BRPrimeLocal] using
    (nativeGK5BRInt_dvd_iff_primePower d.factorial
      (nativeGK5BQClearedNumerator d j values)
      (Nat.factorial_ne_zero d))

/-- FULL LOCAL-TO-GLOBAL DESCENT for arbitrary integer raw
observations, using the original GK5BQ numerator exactly.
All finitely many local prime-power conditions suffice for
one actual Int[X] coefficient lift of the true Newton
interpolant. No original Type-valued source is inferred. -/
theorem nativeGK5BRNewton_integral_iff_primePower
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j values p) := by
  rw [nativeGK5BQNewton_integral_iff_divisible]
  constructor
  · intro h j hj
    exact (nativeGK5BRFactorial_dvd_iff_finiteLocal d j values).1
      (h j hj)
  · intro h j hj
    exact (nativeGK5BRFactorial_dvd_iff_finiteLocal d j values).2
      (h j hj)

/-- The same finite local-to-global criterion for the genuine
GK5BL Lagrange interpolant on the actual integer grid. -/
theorem nativeGK5BRLagrange_integral_iff_primePower
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant
          (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j values p) := by
  rw [nativeGK5BQLagrange_integral_iff_divisible]
  constructor
  · intro h j hj
    exact (nativeGK5BRFactorial_dvd_iff_finiteLocal d j values).1
      (h j hj)
  · intro h j hj
    exact (nativeGK5BRFactorial_dvd_iff_finiteLocal d j values).2
      (h j hj)

/-- The local-to-global Newton statement in the explicitly
computable finite integer-congruence presentation. -/
theorem nativeGK5BRNewton_integral_iff_congruences
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BQClearedNumerator d j values %
          ((p ^ ((d.factorial).factorization p) : Nat) : Int) = 0) := by
  simpa only [nativeGK5BRPrimeLocal,
    Int.dvd_iff_emod_eq_zero] using
    nativeGK5BRNewton_integral_iff_primePower d values

/-- The same explicit congruence reconstruction for the
genuine original GK5BL rational Lagrange interpolant. -/
theorem nativeGK5BRLagrange_integral_iff_congruences
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant
          (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BQClearedNumerator d j values %
          ((p ^ ((d.factorial).factorization p) : Nat) : Int) = 0) := by
  simpa only [nativeGK5BRPrimeLocal,
    Int.dvd_iff_emod_eq_zero] using
    nativeGK5BRLagrange_integral_iff_primePower d values

/-- A failed genuine local prime-power certificate prohibits
the Int[X] Newton coefficient lift; it is an ARITHMETIC
obstruction, not a proof of a failed F55 Type-valued seam. -/
theorem nativeGK5BRNoIntegerLift_of_localFailure
    (d : Nat) (values : Nat → Int)
    (j p : Nat) (hj : j ∈ Finset.range (d + 1))
    (hp : p ∈ (d.factorial).primeFactors)
    (hbad : ¬ nativeGK5BRPrimeLocal d j values p) :
    ¬ ∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat)) := by
  intro h
  exact hbad ((nativeGK5BRNewton_integral_iff_primePower d values).1 h j hj p hp)

/-- Failure of an integer Newton lift has a witness among
finitely many coefficient / prime-factor pairs, without a
hidden nonzero assumption on the raw integer numerator. -/
theorem nativeGK5BRNoIntegerLift_iff_exists_localFailure
    (d : Nat) (values : Nat → Int) :
    (¬ ∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∃ j ∈ Finset.range (d + 1),
      ∃ p ∈ (d.factorial).primeFactors,
        ¬ nativeGK5BRPrimeLocal d j values p) := by
  rw [nativeGK5BRNewton_integral_iff_primePower]
  push Not
  rfl

/-- Any two presentations of the finite local test, as
divisibility or a congruence, are compatible coefficient by
coefficient and prime by prime. -/
theorem nativeGK5BRFiniteLocal_iff_finiteCongruences
    (d : Nat) (values : Nat → Int) :
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BRPrimeLocal d j values p) ↔
    (∀ j ∈ Finset.range (d + 1),
      ∀ p ∈ (d.factorial).primeFactors,
        nativeGK5BQClearedNumerator d j values %
          ((p ^ ((d.factorial).factorization p) : Nat) : Int) = 0) := by
  simp only [nativeGK5BRPrimeLocal, Int.dvd_iff_emod_eq_zero]

#print axioms nativeGK5BRNat_dvd_iff_primePower
#print axioms nativeGK5BRInt_dvd_iff_primePower
#print axioms nativeGK5BRFactorial_exponent_eq_padic
#print axioms nativeGK5BRPrimeLocal_iff_congruence
#print axioms nativeGK5BRFactorial_dvd_iff_finiteLocal
#print axioms nativeGK5BRNewton_integral_iff_primePower
#print axioms nativeGK5BRLagrange_integral_iff_primePower
#print axioms nativeGK5BRNewton_integral_iff_congruences
#print axioms nativeGK5BRLagrange_integral_iff_congruences
#print axioms nativeGK5BRNoIntegerLift_of_localFailure
#print axioms nativeGK5BRNoIntegerLift_iff_exists_localFailure
#print axioms nativeGK5BRFiniteLocal_iff_finiteCongruences

end
end Kuu.F112.Physical
