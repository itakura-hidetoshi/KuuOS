import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BMIntegralNatLiftCertificates
import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Tactic

/-!
F112-P94D3GK5BN — FINITE SUPPORT DENOMINATOR AND DIVISIBILITY
CERTIFICATES for constructive rational Lagrange interpolation.

GK5BM's coefficientwise Int[X] criterion is converted into TWO
finite, exact tests: (1) reduced rational denominator = 1 on
the actual finite support; (2) after a nonzero integer scalar
clears denominators, divisibility of every NONZERO coefficient
of the integer numerator by that scalar. The latter is an
exact obstruction certificate, not mere integer-valued sampling.

For true original F55/P92B proofs and source P77 quotient
polynomial VALUES, the finite denominator certificate follows
from the actual GK5BJ/GK5BM Nat coefficient witness. The
argument does not reconstruct Type-valued proof histories or
infer new original P94A four-cells.

Strict 空 authority; independent Kuu→Qi; original F54
two-Nat/two-category/Blocks and F55 Type history retained.
Append-only public root107, protected PR #1558 remains
Draft/open/unmerged. Pinned Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry, admit, native_decide, unconditional
P89 reflection, GK5AY seam, GK5BA kit, or Gray restoration.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
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

/-- Integrality of EVERY rational coefficient is equivalent
to a FINITE test of denominator one on the actual support.
Out-of-support coefficients vanish and require no inspection. -/
theorem nativeGK5BNIntegralLift_iff_finiteDenominators
    (Q : Polynomial Rat) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q) ↔
    (∀ k ∈ Q.support, (Q.coeff k).den = 1) := by
  constructor
  · rintro ⟨P, hP⟩ k hk
    have hc : (P.coeff k : Rat) = Q.coeff k := by
      simpa only [Polynomial.coeff_map] using
        congrArg (fun T : Polynomial Rat => T.coeff k) hP
    rw [← hc]
    exact Rat.den_intCast _
  · intro h
    apply (nativeGK5BMIntegralLift_iff Q).2
    intro k
    by_cases hk : k ∈ Q.support
    · refine ⟨(Q.coeff k).num, ?_⟩
      exact (Rat.den_eq_one_iff (Q.coeff k)).1 (h k hk)
    · have hz : Q.coeff k = 0 :=
        Polynomial.notMem_support_iff.mp hk
      exact ⟨0, by simp [hz]⟩

/-- Finite denominator test for the ACTUAL rational Lagrange
interpolant of any finite collection of integer sample sites. -/
theorem nativeGK5BNInterpolant_integral_iff_finiteDenominators
    (sites : Finset Int) (values : Int → Rat) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
       nativeGK5BLRationalInterpolant sites values) ↔
    (∀ k ∈ (nativeGK5BLRationalInterpolant sites values).support,
      ((nativeGK5BLRationalInterpolant sites values).coeff k).den = 1) :=
  nativeGK5BNIntegralLift_iff_finiteDenominators _

/-- A single reduced denominator > 1 on the finite support
gives a verifiable obstruction to any integral coefficient lift. -/
theorem nativeGK5BNNoIntegralLift_of_denominator
    (Q : Polynomial Rat) (k : Nat) (hk : k ∈ Q.support)
    (hden : (Q.coeff k).den ≠ 1) :
    ¬ ∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q := by
  intro h
  exact hden ((nativeGK5BNIntegralLift_iff_finiteDenominators Q).1 h k hk)

/-- The coefficient equation obtained from an ACTUAL cleared
denominator identity d·Q=N in the rational polynomial ring. -/
theorem nativeGK5BNScaled_coefficient
    (N : Polynomial Int) (Q : Polynomial Rat) (d : Int)
    (hscale : Polynomial.C (d : Rat) * Q =
      N.map (Int.castRingHom Rat)) (k : Nat) :
    (d : Rat) * Q.coeff k = (N.coeff k : Rat) := by
  have h := congrArg (fun T : Polynomial Rat => T.coeff k) hscale
  simpa only [Polynomial.coeff_C_mul, Polynomial.coeff_map] using h

/-- Exact INTEGRAL LIFT iff an integer numerator has all
coefficients divisible by its nonzero clearing denominator.
The right side is not assumed; the reverse direction
constructs the Int[X] source via GK5BM's finite-support
monomial construction. -/
theorem nativeGK5BNScaled_integral_iff_allDivisibility
    (N : Polynomial Int) (Q : Polynomial Rat) (d : Int)
    (hd : d ≠ 0)
    (hscale : Polynomial.C (d : Rat) * Q =
      N.map (Int.castRingHom Rat)) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q) ↔
      (∀ k : Nat, d ∣ N.coeff k) := by
  constructor
  · rintro ⟨P, hP⟩ k
    have hc := nativeGK5BNScaled_coefficient N Q d hscale k
    rw [← hP] at hc
    simp only [Polynomial.coeff_map] at hc
    have hi : d * P.coeff k = N.coeff k := by
      exact_mod_cast hc
    exact ⟨P.coeff k, hi.symm⟩
  · intro h
    apply (nativeGK5BMIntegralLift_iff Q).2
    intro k
    obtain ⟨z, hz⟩ := h k
    have hc := nativeGK5BNScaled_coefficient N Q d hscale k
    have hzRat : (N.coeff k : Rat) = (d : Rat) * (z : Rat) := by
      exact_mod_cast hz
    have hdRat : (d : Rat) ≠ 0 := by exact_mod_cast hd
    refine ⟨z, ?_⟩
    exact (mul_left_cancel₀ hdRat (hc.trans hzRat)).symm

/-- The divisibility criterion is FINITE: only coefficients on
the true support of N must be checked, including the constant
coefficient whenever it is nonzero. -/
theorem nativeGK5BNScaled_integral_iff_finiteDivisibility
    (N : Polynomial Int) (Q : Polynomial Rat) (d : Int)
    (hd : d ≠ 0)
    (hscale : Polynomial.C (d : Rat) * Q =
      N.map (Int.castRingHom Rat)) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q) ↔
      (∀ k ∈ N.support, d ∣ N.coeff k) := by
  rw [nativeGK5BNScaled_integral_iff_allDivisibility N Q d hd hscale]
  constructor
  · intro h k hk
    exact h k
  · intro h k
    by_cases hk : k ∈ N.support
    · exact h k hk
    · have hz : N.coeff k = 0 :=
        Polynomial.notMem_support_iff.mp hk
      simp [hz]

/-- A certified finite numerator-divisibility failure is an
explicit obstruction to an integer-coefficient reconstruction. -/
theorem nativeGK5BNScaled_noIntegralLift_of_notDvd
    (N : Polynomial Int) (Q : Polynomial Rat) (d : Int)
    (hd : d ≠ 0)
    (hscale : Polynomial.C (d : Rat) * Q =
      N.map (Int.castRingHom Rat))
    (k : Nat) (hnot : ¬ d ∣ N.coeff k) :
    ¬ ∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q := by
  intro h
  exact hnot
    ((nativeGK5BNScaled_integral_iff_allDivisibility N Q d hd hscale).1 h k)

/-- Direct criterion for any Lagrange interpolant whose
denominator has been cleared by an EXHIBITED integer numerator.
This accepts an exact equation as a certificate, not numerical
approximation. -/
theorem nativeGK5BNInterpolant_scaled_iff_finiteDivisibility
    (sites : Finset Int) (values : Int → Rat)
    (N : Polynomial Int) (d : Int) (hd : d ≠ 0)
    (hscale : Polynomial.C (d : Rat) *
       nativeGK5BLRationalInterpolant sites values =
       N.map (Int.castRingHom Rat)) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) =
       nativeGK5BLRationalInterpolant sites values) ↔
      (∀ k ∈ N.support, d ∣ N.coeff k) :=
  nativeGK5BNScaled_integral_iff_finiteDivisibility N
    (nativeGK5BLRationalInterpolant sites values) d hd hscale

/-- A proven Nat[X] lift automatically supplies the finite
integral denominator certificate; no inverse Type witness
is fabricated by this implication. -/
theorem nativeGK5BNFiniteDenominators_of_natLift
    (Q : Polynomial Rat)
    (hNat : ∃ P : Polynomial Nat,
       P.map (Nat.castRingHom Rat) = Q) :
    ∀ k ∈ Q.support, (Q.coeff k).den = 1 := by
  apply (nativeGK5BNIntegralLift_iff_finiteDenominators Q).1
  apply (nativeGK5BMIntegralLift_iff Q).2
  intro k
  obtain ⟨b, hb⟩ := (nativeGK5BMNatLift_iff Q).1 hNat k
  exact ⟨(b : Int), by simpa using hb⟩

/-- For an ACTUAL typed original P92B proof, all reconstructed
finite-support rational denominators are exactly 1. -/
theorem NativeF55P92AssocComparison.gk5bnFiniteDenominators
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : f.gk5bgDepthPolynomial.natDegree ≤ d) :
    ∀ k ∈ (nativeGK5BLRationalInterpolant sites
      (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat))).support,
      ((nativeGK5BLRationalInterpolant sites
        (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k).den = 1 :=
  nativeGK5BNFiniteDenominators_of_natLift _
    (f.gk5bmInterpolant_natLift d sites hsize hdegree)

/-- The same finite certificate holds for the polynomial VALUE
descended from every TRUE original P77 quotient class; it does
not identify the classes or create a four-cell. -/
theorem nativeGK5BNP77FiniteDenominators
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
      ((nativeGK5BLRationalInterpolant sites
        (fun z : Int =>
          (((nativeGK5BGPolyOnP77Class first last r s q).eval z : Int) : Rat))).coeff k).den = 1 :=
  nativeGK5BNFiniteDenominators_of_natLift _
    (nativeGK5BMInterpolant_P77_natLift
      first last r s q d sites hsize hdegree)

#print axioms nativeGK5BNIntegralLift_iff_finiteDenominators
#print axioms nativeGK5BNInterpolant_integral_iff_finiteDenominators
#print axioms nativeGK5BNNoIntegralLift_of_denominator
#print axioms nativeGK5BNScaled_coefficient
#print axioms nativeGK5BNScaled_integral_iff_allDivisibility
#print axioms nativeGK5BNScaled_integral_iff_finiteDivisibility
#print axioms nativeGK5BNScaled_noIntegralLift_of_notDvd
#print axioms nativeGK5BNInterpolant_scaled_iff_finiteDivisibility
#print axioms nativeGK5BNFiniteDenominators_of_natLift
#print axioms NativeF55P92AssocComparison.gk5bnFiniteDenominators
#print axioms nativeGK5BNP77FiniteDenominators

end
end Kuu.F112.Physical
