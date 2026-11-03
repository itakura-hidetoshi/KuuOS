import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BLLagrangeInterpolation
import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Tactic

/-!
F112-P94D3GK5BM — EXACT coefficientwise integral/Nat-lift
certificates for constructive rational Lagrange interpolation.

GK5BL constructed genuine Rat[X] interpolants from integer
nodes and distinguished recovery from a true Int[X] source.
GK5BM proves precise necessary AND sufficient CONDITIONS for
a given Rat[X] to be a coefficientwise image of some Int[X]
or of some Nat[X], without fabricating F55 typed proofs.

The integer criterion is: each rational coefficient is a cast
of an integer. The Nat criterion is: each rational coefficient
is an integer cast AND nonnegative. A polynomial lift is actually
CONSTRUCTED by a finite sum of monomials over the original
Rat[X] support, using actual coefficient witnesses. These are
not claims that arbitrary integer SAMPLE VALUES yield integer
coefficients, and not sufficient conditions for existence of a
genuine Type-valued P92B source or a P94A four-cell.

For real genuine P92B proofs, the GK5BJ nonnegative Nat count
provides an actual Nat[X] lift of their GK5BL interpolant.
The analogous certificate for true original P77 source quotient
applies to the descended Polynomial Int VALUE only, never
identifies original F55 proof classes.

Strict 空 authority; independent Kuu→Qi; original F54 two-Nat/
two-category/Blocks and F55 Type proof history preserved.
Append-only public root107, protected #1558 Draft/open/unmerged,
pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray, GK5AY universal
seam, GK5BA kit, unconditional P89 reflection or P94A normal form.
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

/-- A generic and actual polynomial-lifting construction:
a witness for EVERY rational coefficient gives a polynomial
over the source semiring, using only the finite support of Q. -/
theorem nativeGK5BMLiftPolynomial_of_coeffWitness
    {R : Type*} [Semiring R]
    (φ : R →+* Rat) (Q : Polynomial Rat) (c : Nat → R)
    (hc : ∀ k : Nat, φ (c k) = Q.coeff k) :
    ∃ P : Polynomial R, P.map φ = Q := by
  let P : Polynomial R :=
    ∑ k ∈ Q.support, Polynomial.monomial k (c k)
  refine ⟨P, ?_⟩
  calc
    P.map φ =
        ∑ k ∈ Q.support, (Polynomial.monomial k (c k)).map φ := by
          simp only [P, Polynomial.map_sum]
    _ = ∑ k ∈ Q.support, Polynomial.monomial k (Q.coeff k) := by
          apply Finset.sum_congr rfl
          intro k hk
          rw [Polynomial.map_monomial, hc k]
    _ = Q := by
          change (Q.sum fun k a => Polynomial.monomial k a) = Q
          exact Polynomial.sum_monomial_eq Q

/-- EXACT integral coefficient certificate: not simply
integer-valued finite observations. No degree or node hypothesis
is needed, since Q has finite support by its Polynomial type. -/
theorem nativeGK5BMIntegralLift_iff (Q : Polynomial Rat) :
    (∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q) ↔
      (∀ k : Nat, ∃ z : Int, (z : Rat) = Q.coeff k) := by
  constructor
  · rintro ⟨P, hP⟩ k
    refine ⟨P.coeff k, ?_⟩
    have h := congrArg (fun T : Polynomial Rat => T.coeff k) hP
    simpa only [Polynomial.coeff_map] using h
  · intro h
    classical
    let c : Nat → Int := fun k => Classical.choose (h k)
    have hc : ∀ k : Nat, (c k : Rat) = Q.coeff k := by
      intro k
      exact Classical.choose_spec (h k)
    exact nativeGK5BMLiftPolynomial_of_coeffWitness
      (Int.castRingHom Rat) Q c hc

/-- EXACT nonnegative Nat coefficient certificate for a full
Rat[X] polynomial, represented by an actual Nat[X] source. -/
theorem nativeGK5BMNatLift_iff (Q : Polynomial Rat) :
    (∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) = Q) ↔
      (∀ k : Nat, ∃ b : Nat, (b : Rat) = Q.coeff k) := by
  constructor
  · rintro ⟨P, hP⟩ k
    refine ⟨P.coeff k, ?_⟩
    have h := congrArg (fun T : Polynomial Rat => T.coeff k) hP
    simpa only [Polynomial.coeff_map] using h
  · intro h
    classical
    let c : Nat → Nat := fun k => Classical.choose (h k)
    have hc : ∀ k : Nat, (c k : Rat) = Q.coeff k := by
      intro k
      exact Classical.choose_spec (h k)
    exact nativeGK5BMLiftPolynomial_of_coeffWitness
      (Nat.castRingHom Rat) Q c hc

/-- Being a NAT coefficient at every depth is EQUIVALENT to
coefficientwise integrality AND rational nonnegativity. -/
theorem nativeGK5BMCoeffNat_iff_integral_nonneg (Q : Polynomial Rat) :
    (∀ k : Nat, ∃ b : Nat, (b : Rat) = Q.coeff k) ↔
    (∀ k : Nat, (∃ z : Int, (z : Rat) = Q.coeff k) ∧
      0 ≤ Q.coeff k) := by
  constructor
  · intro h k
    obtain ⟨b, hb⟩ := h k
    refine ⟨⟨(b : Int), by simpa using hb⟩, ?_⟩
    rw [←hb]
    exact Nat.cast_nonneg _
  · intro h k
    obtain ⟨⟨z, hz⟩, hnonneg⟩ := h k
    have hznonneg : (0 : Int) ≤ z := by
      have hc : (0 : Rat) ≤ (z : Rat) := by rw [hz]; exact hnonneg
      exact_mod_cast hc
    refine ⟨z.toNat, ?_⟩
    have ht : (z.toNat : Int) = z := Int.toNat_of_nonneg hznonneg
    calc
      (z.toNat : Rat) = (z : Rat) := by exact_mod_cast ht
      _ = Q.coeff k := hz

/-- FULL necessary-and-sufficient Nat polynomial certificate:
integrality alone is not enough; nonnegativity is independent. -/
theorem nativeGK5BMNatLift_iff_integral_nonneg (Q : Polynomial Rat) :
    (∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) = Q) ↔
    (∀ k : Nat, (∃ z : Int, (z : Rat) = Q.coeff k) ∧
      0 ≤ Q.coeff k) :=
  (nativeGK5BMNatLift_iff Q).trans
    (nativeGK5BMCoeffNat_iff_integral_nonneg Q)

/-- An arbitrary rational interpolant admits an Int polynomial
lift precisely when every coefficient is an integer image. -/
theorem nativeGK5BMInterpolant_integral_iff
    (sites : Finset Int) (values : Int → Rat) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant sites values) ↔
    (∀ k : Nat, ∃ z : Int,
      (z : Rat) = (nativeGK5BLRationalInterpolant sites values).coeff k) :=
  nativeGK5BMIntegralLift_iff _

/-- An arbitrary rational interpolant admits a Nat polynomial
lift precisely when each coefficient is integral and nonnegative. -/
theorem nativeGK5BMInterpolant_nat_iff
    (sites : Finset Int) (values : Int → Rat) :
    (∃ P : Polynomial Nat,
      P.map (Nat.castRingHom Rat) =
        nativeGK5BLRationalInterpolant sites values) ↔
    (∀ k : Nat, (∃ z : Int,
      (z : Rat) = (nativeGK5BLRationalInterpolant sites values).coeff k) ∧
      0 ≤ (nativeGK5BLRationalInterpolant sites values).coeff k) :=
  nativeGK5BMNatLift_iff_integral_nonneg _

/-- A negative coefficient forbids a Nat[X] polynomial lift.
Integer sample values do NOT remove this obstruction. -/
theorem nativeGK5BMNoNatLift_of_negative_coeff
    (Q : Polynomial Rat) (k : Nat)
    (hneg : Q.coeff k < 0) :
    ¬ ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) = Q := by
  intro h
  have hc := (nativeGK5BMNatLift_iff_integral_nonneg Q).1 h k
  exact (not_le_of_gt hneg) hc.2

/-- A nonintegral coefficient obstructs an Int[X] source and
hence also obstructs any source Nat[X] certificate. -/
theorem nativeGK5BMNoNatLift_of_nonintegral_coeff
    (Q : Polynomial Rat) (k : Nat)
    (hnot : ¬ ∃ z : Int, (z : Rat) = Q.coeff k) :
    ¬ ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) = Q := by
  intro h
  exact hnot ((nativeGK5BMNatLift_iff_integral_nonneg Q).1 h k).1

/-- For any ACTUAL dependent P92B 3-proof f, GK5BL gives
Nat coefficients at ALL depths; the rational interpolant hence
admits a genuine Nat[X] polynomial lift. This makes NO claim
that the lifted polynomial represents a new F55 typed source. -/
theorem NativeF55P92AssocComparison.gk5bmInterpolant_natLift
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : f.gk5bgDepthPolynomial.natDegree ≤ d) :
    ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites
        (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat)) := by
  apply (nativeGK5BMNatLift_iff _).2
  intro k
  refine ⟨f.gk5bjNatDepthCoefficient k, ?_⟩
  exact (f.gk5blInterpolate_natCoeff d sites hsize hdegree k).symm

/-- For any ACTUAL original F55/P77 source class q, the
descended polynomial interpolant has Nat[X] coefficient lift
from the already-established true source Nat certificates.
This only reconstructs its polynomial VALUE. -/
theorem nativeGK5BMInterpolant_P77_natLift
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class first last r s q).natDegree ≤ d) :
    ∃ P : Polynomial Nat, P.map (Nat.castRingHom Rat) =
      nativeGK5BLRationalInterpolant sites
        (fun z : Int =>
          (((nativeGK5BGPolyOnP77Class first last r s q).eval z : Int) : Rat)) := by
  apply (nativeGK5BMNatLift_iff _).2
  intro k
  refine ⟨nativeGK5BJNatCoeffOnP77Class first last r s k q, ?_⟩
  exact (nativeGK5BLRationalInterpolant_recovers_P77_natCoeff
    first last r s q d sites hsize hdegree k).symm

#print axioms nativeGK5BMLiftPolynomial_of_coeffWitness
#print axioms nativeGK5BMIntegralLift_iff
#print axioms nativeGK5BMNatLift_iff
#print axioms nativeGK5BMCoeffNat_iff_integral_nonneg
#print axioms nativeGK5BMNatLift_iff_integral_nonneg
#print axioms nativeGK5BMInterpolant_integral_iff
#print axioms nativeGK5BMInterpolant_nat_iff
#print axioms nativeGK5BMNoNatLift_of_negative_coeff
#print axioms nativeGK5BMNoNatLift_of_nonintegral_coeff
#print axioms NativeF55P92AssocComparison.gk5bmInterpolant_natLift
#print axioms nativeGK5BMInterpolant_P77_natLift

end
end Kuu.F112.Physical
