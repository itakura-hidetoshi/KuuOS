import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BNFiniteDivisibilityCertificates
import Mathlib.Algebra.Group.ForwardDiff
import Mathlib.Tactic

/-!
F112-P94D3GK5BO — FORWARD FINITE-DIFFERENCE / FACTORIAL
CERTIFICATES for the genuine rational reconstruction.

Exact-source pinned mathlib ForwardDiff includes the genuine
Gregory–Newton and top-degree factorial formula. We turn these
into an explicit finite-support integer-coefficient criterion.
For each k we truncate a genuine Rat[X] polynomial to degrees
≤ k, compute its k-th forward difference at 0, and check whether
that difference is k! times an actual integer.

This criterion is necessary AND sufficient for Int[X] lift:
the forward difference on the truncation is exactly k! times
the ORIGINAL monomial coefficient of degree k. Higher degrees
must be cut off; using untruncated integer-valued observations
alone must NOT be confused with an integral coefficient lift.

The existing GK5BM/GK5BN finite-support polynomial lift is
reused, without fabricating F55 Type-valued evidence, P77
source quotient equality, P94A four cells or original-phi seam.

Strict 空 authority, independent Kuu→Qi; original F54 two
Nat/two category/Blocks and F55 Type proof history preserved.
Append-only public root107; protected #1558 Draft/open/unmerged.
Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry/admit/native_decide/new axioms/Gray/GK5BA kit;
no unconditional P89 reflection or GK5AY universal seam.
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

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- The genuine finite monomial cutoff through degree k.
Every coefficient is taken from the actual rational polynomial,
not from an invented original F55 Type witness. -/
def nativeGK5BOCutoff (Q : Polynomial Rat) (k : Nat) :
    Polynomial Rat :=
  ∑ j ∈ Finset.range (k + 1), Polynomial.monomial j (Q.coeff j)

/-- All coefficients up to the cutoff are preserved. -/
theorem nativeGK5BOCutoff_coeff
    (Q : Polynomial Rat) (k j : Nat) (hj : j ≤ k) :
    (nativeGK5BOCutoff Q k).coeff j = Q.coeff j := by
  classical
  simp [nativeGK5BOCutoff, Polynomial.finset_sum_coeff,
    Polynomial.coeff_monomial, Finset.sum_ite_eq', Finset.mem_range,
    Nat.lt_succ_iff, hj, eq_comm]

/-- The cutoff cannot have polynomial degree greater than k. -/
theorem nativeGK5BOCutoff_natDegree_le
    (Q : Polynomial Rat) (k : Nat) :
    (nativeGK5BOCutoff Q k).natDegree ≤ k := by
  apply (Polynomial.natDegree_le_iff_coeff_eq_zero).2
  intro j hj
  rw [nativeGK5BOCutoff, Polynomial.finset_sum_coeff]
  apply Finset.sum_eq_zero
  intro i hi
  have hi' : i ≤ k := Nat.lt_succ_iff.mp (Finset.mem_range.mp hi)
  have hne : i ≠ j := by omega
  simp [Polynomial.coeff_monomial, hne]

/-- Actual k-th mathlib forward difference, at the origin
in the coefficient ring Rat. -/
def nativeGK5BOForwardAtZero (Q : Polynomial Rat) (k : Nat) : Rat :=
  ((fwdDiff (1 : Rat))^[k] Q.eval) 0

/-- Full Gregory–Newton formula at every natural number,
expressed using mathlib's actual iterated forward difference. -/
theorem nativeGK5BONewtonGrid (Q : Polynomial Rat) (n : Nat) :
    Q.eval (n : Rat) =
      ∑ k ∈ Finset.range (n + 1),
        (n.choose k : Rat) * nativeGK5BOForwardAtZero Q k := by
  have h := shift_eq_sum_fwdDiff_iter (1 : Rat) Q.eval n (0 : Rat)
  simpa [nativeGK5BOForwardAtZero, nsmul_eq_mul] using h

/-- Explicit finite observation formula: the k-th difference
of the k-truncation is a signed binomial sum of evaluations
on the finite integer grid 0,...,k. -/
theorem nativeGK5BOCutoff_forward_observations
    (Q : Polynomial Rat) (k : Nat) :
    nativeGK5BOForwardAtZero (nativeGK5BOCutoff Q k) k =
      ∑ j ∈ Finset.range (k + 1),
        (((-1 : Int) ^ (k - j) * (k.choose j : Int))) •
          (nativeGK5BOCutoff Q k).eval
            ((0 : Rat) + j • (1 : Rat)) := by
  exact fwdDiff_iter_eq_sum_shift (1 : Rat)
    (nativeGK5BOCutoff Q k).eval k (0 : Rat)

/-- For ANY polynomial of degree at most k, the k-th actual
forward difference is exactly k! times its monomial coefficient.
This also includes the degree-smaller-than-k case, where
BOTH sides are zero, not just the leading-degree case. -/
theorem nativeGK5BOForward_of_natDegree_le
    (Q : Polynomial Rat) (k : Nat)
    (hdegree : Q.natDegree ≤ k) :
    nativeGK5BOForwardAtZero Q k =
      (k.factorial : Rat) * Q.coeff k := by
  by_cases heq : Q.natDegree = k
  · have h := congrFun (Polynomial.fwdDiff_iter_degree_eq_factorial Q) (0 : Rat)
    simpa [nativeGK5BOForwardAtZero, ← heq,
      Polynomial.coeff_natDegree, smul_eq_mul, mul_comm] using h
  · have hlt : Q.natDegree < k := by omega
    have h := congrFun
      (Polynomial.fwdDiff_iter_eq_zero_of_degree_lt (P := Q) hlt) (0 : Rat)
    have hc : Q.coeff k = 0 :=
      (Polynomial.natDegree_le_iff_coeff_eq_zero).mp (le_refl _) k hlt
    simpa [nativeGK5BOForwardAtZero, hc] using h

/-- The EXACT triangle identity: the cutoff k-th forward
difference equals k! times the original Q.coeff k.
This identity makes the eventual divisibility test valid. -/
theorem nativeGK5BOCutoff_forward_eq_factorial_coeff
    (Q : Polynomial Rat) (k : Nat) :
    nativeGK5BOForwardAtZero (nativeGK5BOCutoff Q k) k =
      (k.factorial : Rat) * Q.coeff k := by
  rw [nativeGK5BOForward_of_natDegree_le
    (nativeGK5BOCutoff Q k) k (nativeGK5BOCutoff_natDegree_le Q k)]
  rw [nativeGK5BOCutoff_coeff Q k k (le_refl k)]

/-- Central GK5BO theorem: an ACTUAL rational polynomial
has an integer polynomial source IFF each nonzero coefficient
passes the EXACT factorial/forward-difference witness test.
This is FINITE since Q.support is a Finset. -/
theorem nativeGK5BOIntegralLift_iff_finiteFactorialDifferences
    (Q : Polynomial Rat) :
    (∃ P : Polynomial Int,
       P.map (Int.castRingHom Rat) = Q) ↔
      (∀ k ∈ Q.support, ∃ z : Int,
        (k.factorial : Rat) * (z : Rat) =
          nativeGK5BOForwardAtZero (nativeGK5BOCutoff Q k) k) := by
  constructor
  · intro h k hk
    obtain ⟨z, hz⟩ := (nativeGK5BMIntegralLift_iff Q).1 h k
    refine ⟨z, ?_⟩
    rw [nativeGK5BOCutoff_forward_eq_factorial_coeff, ← hz]
  · intro h
    apply (nativeGK5BMIntegralLift_iff Q).2
    intro k
    by_cases hk : k ∈ Q.support
    · obtain ⟨z, hz⟩ := h k hk
      rw [nativeGK5BOCutoff_forward_eq_factorial_coeff] at hz
      have hn : (k.factorial : Rat) ≠ 0 := by
        exact_mod_cast (Nat.factorial_ne_zero k)
      exact ⟨z, mul_left_cancel₀ hn hz⟩
    · have hc : Q.coeff k = 0 :=
        Polynomial.notMem_support_iff.mp hk
      exact ⟨0, by simp [hc]⟩

/-- The same finite factorial-difference criterion for ACTUAL
GK5BL Lagrange interpolation on ANY finite integer sites. -/
theorem nativeGK5BOInterpolant_integral_iff_factorialDifferences
    (sites : Finset Int) (values : Int → Rat) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites values) ↔
    (∀ k ∈ (nativeGK5BLRationalInterpolant sites values).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff (nativeGK5BLRationalInterpolant sites values) k) k) :=
  nativeGK5BOIntegralLift_iff_finiteFactorialDifferences _

/-- A single failed finite-factorial certificate gives an
explicit obstacle to reconstructing an Int[X] source. -/
theorem nativeGK5BONoIntegralLift_of_factorialObstruction
    (Q : Polynomial Rat) (k : Nat) (hk : k ∈ Q.support)
    (hnot : ¬ ∃ z : Int,
       (k.factorial : Rat) * (z : Rat) =
         nativeGK5BOForwardAtZero (nativeGK5BOCutoff Q k) k) :
    ¬ ∃ P : Polynomial Int,
       P.map (Int.castRingHom Rat) = Q := by
  intro h
  exact hnot ((nativeGK5BOIntegralLift_iff_finiteFactorialDifferences Q).1 h k hk)

/-- Any already proven Nat[X] lift supplies the finite
factorial difference certificate, preserving all original
typed-source authority boundaries. -/
theorem nativeGK5BOFactorialDifferences_of_natLift
    (Q : Polynomial Rat)
    (hNat : ∃ P : Polynomial Nat,
      P.map (Nat.castRingHom Rat) = Q) :
    ∀ k ∈ Q.support, ∃ z : Int,
      (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero (nativeGK5BOCutoff Q k) k := by
  apply (nativeGK5BOIntegralLift_iff_finiteFactorialDifferences Q).1
  exact (nativeGK5BNIntegralLift_iff_finiteDenominators Q).2
    (nativeGK5BNFiniteDenominators_of_natLift Q hNat)

/-- For EVERY actual dependent P92B source f, the rational
interpolant recovered from true original F55 proof observations
passes the finite factorial difference criterion. -/
theorem NativeF55P92AssocComparison.gk5boFactorialDifferences
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : f.gk5bgDepthPolynomial.natDegree ≤ d) :
    ∀ k ∈ (nativeGK5BLRationalInterpolant sites
      (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant sites
              (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat))) k) k :=
  nativeGK5BOFactorialDifferences_of_natLift _
    (f.gk5bmInterpolant_natLift d sites hsize hdegree)

/-- For an actual original F55/P77 class, only its DESCENDED
polynomial VALUE gets a factorial-difference certificate.
No new Type-valued source proof or quotient-class reflection. -/
theorem nativeGK5BOP77FactorialDifferences
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class first last r s q).natDegree ≤ d) :
    ∀ k ∈ (nativeGK5BLRationalInterpolant sites
      (fun z : Int =>
        (((nativeGK5BGPolyOnP77Class first last r s q).eval z : Int) : Rat))).support,
      ∃ z : Int, (k.factorial : Rat) * (z : Rat) =
        nativeGK5BOForwardAtZero
          (nativeGK5BOCutoff
            (nativeGK5BLRationalInterpolant sites
              (fun z : Int =>
                (((nativeGK5BGPolyOnP77Class first last r s q).eval z : Int) : Rat))) k) k :=
  nativeGK5BOFactorialDifferences_of_natLift _
    (nativeGK5BMInterpolant_P77_natLift first last r s q d sites hsize hdegree)

#print axioms nativeGK5BOCutoff_coeff
#print axioms nativeGK5BOCutoff_natDegree_le
#print axioms nativeGK5BONewtonGrid
#print axioms nativeGK5BOCutoff_forward_observations
#print axioms nativeGK5BOForward_of_natDegree_le
#print axioms nativeGK5BOCutoff_forward_eq_factorial_coeff
#print axioms nativeGK5BOIntegralLift_iff_finiteFactorialDifferences
#print axioms nativeGK5BOInterpolant_integral_iff_factorialDifferences
#print axioms nativeGK5BONoIntegralLift_of_factorialObstruction
#print axioms nativeGK5BOFactorialDifferences_of_natLift
#print axioms NativeF55P92AssocComparison.gk5boFactorialDifferences
#print axioms nativeGK5BOP77FactorialDifferences

end
end Kuu.F112.Physical
