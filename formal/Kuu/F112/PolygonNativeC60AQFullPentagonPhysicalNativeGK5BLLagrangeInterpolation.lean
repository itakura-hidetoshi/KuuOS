import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BKFiniteSampleRigidity
import Mathlib.LinearAlgebra.Lagrange
import Mathlib.Tactic

/-!
F112-P94D3GK5BL — CONSTRUCTIVE RATIONAL LAGRANGE RECONSTRUCTION
from finite integer observations of actual typed P92B depth polynomials.

GK5BK proved uniqueness from any d+1 distinct integer samples.
GK5BL CONSTRUCTS an explicit polynomial in Rat[X] from the
observed integer values using the actual pinned mathlib
Lagrange.interpolate and its basisDivisor/product formula.

For every genuine Int[X] polynomial P of natDegree≤d, the
reconstruction from its d+1 distinct integer evaluations
equals the genuine coefficient embedding P.map (Int.castRingHom Rat).
Thus every integer coefficient is recovered, and when P
originates from an actual P92B proof its nonnegative original
Nat coefficient b_k is recovered as a rational number.

We separately track the necessary conditions:
* arbitrary rational sample data need NOT yield Int coefficients;
* Int coefficients need NOT all be nonnegative;
* even nonnegative Int coefficients need NOT realize a genuine
  F55 Type-valued source proof, nor a P94A four-cell;
* P77 interpolation restores only a DESCENDED Polynomial VALUE,
  never identifies source P77 quotient classes.

No new axioms, sorry/admit/native_decide; no universal GK5AY
seam, GK5BA kit, unconditional original P89 reflection, Gray,
or invented sufficiency W=1→local original/phi seam.
Strict 空 authority, independent Kuu→Qi, F54 two Nat/two
categories/Blocks and original F55 Type witnesses retained.
Append-only public root107, protected #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Distinct integers give distinct rational interpolation nodes. -/
theorem nativeGK5BLIntToRat_injective :
    Function.Injective (fun z : Int => (z : Rat)) := by
  intro i j h
  change (i : Rat) = (j : Rat) at h
  exact_mod_cast h

/-- The original integer sites inject into rational nodes. -/
theorem nativeGK5BLIntToRat_injOn (sites : Finset Int) :
    Set.InjOn (fun z : Int => (z : Rat)) sites :=
  nativeGK5BLIntToRat_injective.injOn

/-- The CONSTRUCTED rational polynomial from a finite family
of rational node values, at actual integer sampling sites. -/
def nativeGK5BLRationalInterpolant (sites : Finset Int) (values : Int → Rat) :
    Polynomial Rat :=
  Lagrange.interpolate sites (fun z : Int => (z : Rat)) values

/-- At every supplied integer site the rational interpolant
evaluates EXACTLY to the supplied rational observation. -/
theorem nativeGK5BLRationalInterpolant_eval_node
    (sites : Finset Int) (values : Int → Rat) (z : Int) (hz : z ∈ sites) :
    (nativeGK5BLRationalInterpolant sites values).eval (z : Rat) = values z :=
  Lagrange.eval_interpolate_at_node values (nativeGK5BLIntToRat_injOn sites) hz

/-- The actual interpolant has rational polynomial degree
strictly below the finite number of observed sites. -/
theorem nativeGK5BLRationalInterpolant_degree_lt
    (sites : Finset Int) (values : Int → Rat) :
    (nativeGK5BLRationalInterpolant sites values).degree < sites.card :=
  Lagrange.degree_interpolate_lt values (nativeGK5BLIntToRat_injOn sites)

/-- Explicit, computable-in-Rat Lagrange denominator/product
presentation. The denominators are nonzero at pairwise distinct
sites, as proved by the pinned Lagrange basis theorems. -/
theorem nativeGK5BLRationalInterpolant_explicit
    (sites : Finset Int) (values : Int → Rat) :
    nativeGK5BLRationalInterpolant sites values =
      ∑ i ∈ sites,
        Polynomial.C
          (values i /
            ∏ j ∈ sites.erase i, ((i : Rat) - (j : Rat))) *
          (∏ j ∈ sites.erase i,
            (Polynomial.X - Polynomial.C (j : Rat))) :=
  Lagrange.interpolate_eq_sum values

/-- Any Rat[X] polynomial of degree below #sites is
CONSTRUCTIVELY recovered, not merely distinguished by roots. -/
theorem nativeGK5BLRationalInterpolant_recovers_rat
    (Q : Polynomial Rat) (sites : Finset Int)
    (hdegree : Q.degree < sites.card) :
    nativeGK5BLRationalInterpolant sites
      (fun z : Int => Q.eval (z : Rat)) = Q :=
  (Lagrange.eq_interpolate (s := sites)
    (v := fun z : Int => (z : Rat))
    (f := Q) (nativeGK5BLIntToRat_injOn sites) hdegree).symm

/-- Mapping integer coefficients to Rat commutes with
evaluation at genuinely integer points. -/
theorem nativeGK5BLRatMap_eval_int (P : Polynomial Int) (z : Int) :
    (P.map (Int.castRingHom Rat)).eval (z : Rat) =
      ((P.eval z : Int) : Rat) := by
  change (P.map (Int.castRingHom Rat)).eval ((Int.castRingHom Rat) z) =
    (Int.castRingHom Rat) (P.eval z)
  exact Polynomial.eval_map_apply (p := P) (f := Int.castRingHom Rat) z

/-- Mapping an Int polynomial to Rat cannot increase
its true natDegree; interpolate at d+1 sites hence applies. -/
theorem nativeGK5BLRatMap_degree_lt
    (P : Polynomial Int) (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : P.natDegree ≤ d) :
    (P.map (Int.castRingHom Rat)).degree < sites.card := by
  have hmap : (P.map (Int.castRingHom Rat)).natDegree ≤ d :=
    (Polynomial.natDegree_map_le).trans hdegree
  have hle : (P.map (Int.castRingHom Rat)).degree ≤ (d : WithBot Nat) :=
    Polynomial.natDegree_le_iff_degree_le.mp hmap
  have hlt : (d : WithBot Nat) < (sites.card : WithBot Nat) := by
    rw [hsize]
    exact WithBot.coe_lt_coe.mpr (Nat.lt_succ_self d)
  exact lt_of_le_of_lt hle hlt

/-- The interpolant of d+1 genuine integer samples is exactly
the rational coefficient embedding of the original Int[X].
This is the constructive complement to GK5BK uniqueness. -/
theorem nativeGK5BLRationalInterpolant_recovers_int
    (P : Polynomial Int) (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : P.natDegree ≤ d) :
    nativeGK5BLRationalInterpolant sites
      (fun z : Int => ((P.eval z : Int) : Rat)) =
      P.map (Int.castRingHom Rat) := by
  have h := nativeGK5BLRationalInterpolant_recovers_rat
    (P.map (Int.castRingHom Rat)) sites
    (nativeGK5BLRatMap_degree_lt P d sites hsize hdegree)
  have hfun :
      (fun z : Int => (P.map (Int.castRingHom Rat)).eval (z : Rat)) =
      (fun z : Int => ((P.eval z : Int) : Rat)) := by
    funext z
    exact nativeGK5BLRatMap_eval_int P z
  rw [hfun] at h
  exact h

/-- The reconstructed rational polynomial returns EVERY
original Int coefficient at EVERY inversion depth, including
depths beyond the known bound (where both coefficients vanish). -/
theorem nativeGK5BLRationalInterpolant_recovers_int_coeff
    (P : Polynomial Int) (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : P.natDegree ≤ d) (k : Nat) :
    (nativeGK5BLRationalInterpolant sites
      (fun z : Int => ((P.eval z : Int) : Rat))).coeff k = (P.coeff k : Rat) := by
  rw [nativeGK5BLRationalInterpolant_recovers_int P d sites hsize hdegree]
  simp only [Polynomial.coeff_map]
  rfl

/-- Arbitrary supplied Int observations that agree with
the actual polynomial on the finite sampling sites recover
the original rational embedding. Off-site values are irrelevant. -/
theorem nativeGK5BLRationalInterpolant_recovers_data
    (P : Polynomial Int) (d : Nat) (sites : Finset Int)
    (values : Int → Int)
    (hsize : sites.card = d + 1)
    (hdegree : P.natDegree ≤ d)
    (hdata : ∀ z ∈ sites, values z = P.eval z) :
    nativeGK5BLRationalInterpolant sites
      (fun z : Int => (values z : Rat)) =
      P.map (Int.castRingHom Rat) := by
  calc
    nativeGK5BLRationalInterpolant sites
        (fun z : Int => (values z : Rat)) =
        nativeGK5BLRationalInterpolant sites
          (fun z : Int => ((P.eval z : Int) : Rat)) := by
            apply Lagrange.interpolate_eq_of_values_eq_on
            intro z hz
            exact congrArg (fun t : Int => (t : Rat)) (hdata z hz)
    _ = _ := nativeGK5BLRationalInterpolant_recovers_int P d sites hsize hdegree

/-- A genuinely typed P92B proof is reconstructed from its
integer evaluation data AS A RATIONAL COEFFICIENT POLYNOMIAL. -/
theorem NativeF55P92AssocComparison.gk5blInterpolate_genuine
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : f.gk5bgDepthPolynomial.natDegree ≤ d) :
    nativeGK5BLRationalInterpolant sites
      (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat)) =
      f.gk5bgDepthPolynomial.map (Int.castRingHom Rat) :=
  nativeGK5BLRationalInterpolant_recovers_int
    f.gk5bgDepthPolynomial d sites hsize hdegree

/-- Every rationally recovered coefficient is the original
NONNEGATIVE Nat wrapper count b_k, cast to Rat. -/
theorem NativeF55P92AssocComparison.gk5blInterpolate_natCoeff
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (k : Nat) :
    (nativeGK5BLRationalInterpolant sites
      (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k =
      (f.gk5bjNatDepthCoefficient k : Rat) := by
  calc
    (nativeGK5BLRationalInterpolant sites
       (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k =
        (f.gk5biDepthCoefficient k : Rat) := by
          exact nativeGK5BLRationalInterpolant_recovers_int_coeff
            f.gk5bgDepthPolynomial d sites hsize hdegree k
    _ = (f.gk5bjNatDepthCoefficient k : Rat) := by
      exact_mod_cast (f.gk5bjNatCoeff_cast k).symm

/-- Interpolating actual P77 source polynomial VALUES returns
the rational embedding of the DESCENDED Polynomial Int,
without identifying original source quotient classes. -/
theorem nativeGK5BLRationalInterpolant_recovers_P77
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class first last r s q).natDegree ≤ d) :
    nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5BGPolyOnP77Class first last r s q).eval z : Int) : Rat)) =
      (nativeGK5BGPolyOnP77Class first last r s q).map (Int.castRingHom Rat) :=
  nativeGK5BLRationalInterpolant_recovers_int
    (nativeGK5BGPolyOnP77Class first last r s q) d sites hsize hdegree

/-- The rationally recovered coefficients on an actual P77
source class equal the Nat-valued coefficient Quotient.lift. -/
theorem nativeGK5BLRationalInterpolant_recovers_P77_natCoeff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : (nativeGK5BGPolyOnP77Class first last r s q).natDegree ≤ d)
    (k : Nat) :
    (nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5BGPolyOnP77Class first last r s q).eval z : Int) : Rat))).coeff k =
      (nativeGK5BJNatCoeffOnP77Class first last r s k q : Rat) := by
  have hcoef := nativeGK5BLRationalInterpolant_recovers_int_coeff
    (nativeGK5BGPolyOnP77Class first last r s q) d sites hsize hdegree k
  have hInt := nativeGK5BICoeffOnP77Class_eq_poly first last r s q k
  have hNat := nativeGK5BJNatCoeffOnP77Class_cast first last r s q k
  calc
    (nativeGK5BLRationalInterpolant sites
      (fun z : Int => (((nativeGK5BGPolyOnP77Class first last r s q).eval z : Int) : Rat))).coeff k =
      ((nativeGK5BGPolyOnP77Class first last r s q).coeff k : Rat) := hcoef
    _ = (nativeGK5BICoeffOnP77Class first last r s k q : Rat) := by
      exact congrArg (fun t : Int => (t : Rat)) hInt.symm
    _ = (nativeGK5BJNatCoeffOnP77Class first last r s k q : Rat) := by
      exact_mod_cast hNat.symm

/-- An arbitrary rational interpolation polynomial can have
integer coefficients only if EVERY recovered coefficient lies
in the embedded image of Int. This is a NECESSARY condition. -/
theorem nativeGK5BLNoIntegralLift_of_coeff_not_int
    (Q : Polynomial Rat) (k : Nat)
    (h : ¬ ∃ z : Int, (z : Rat) = Q.coeff k) :
    ¬ ∃ P : Polynomial Int, P.map (Int.castRingHom Rat) = Q := by
  rintro ⟨P, hp⟩
  apply h
  refine ⟨P.coeff k, ?_⟩
  have hc := congrArg (fun T : Polynomial Rat => T.coeff k) hp
  simpa only [Polynomial.coeff_map] using hc

/-- Every actual P92B proof has NONNEGATIVE recovered rational
coefficients; arbitrary rational interpolation need not. -/
theorem NativeF55P92AssocComparison.gk5blRecovered_coeff_nonneg
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (d : Nat) (sites : Finset Int)
    (hsize : sites.card = d + 1)
    (hdegree : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (k : Nat) :
    0 ≤ (nativeGK5BLRationalInterpolant sites
      (fun z : Int => ((f.gk5bgDepthPolynomial.eval z : Int) : Rat))).coeff k := by
  rw [f.gk5blInterpolate_natCoeff d sites hsize hdegree k]
  exact Nat.cast_nonneg _

#print axioms nativeGK5BLIntToRat_injective
#print axioms nativeGK5BLIntToRat_injOn
#print axioms nativeGK5BLRationalInterpolant
#print axioms nativeGK5BLRationalInterpolant_eval_node
#print axioms nativeGK5BLRationalInterpolant_degree_lt
#print axioms nativeGK5BLRationalInterpolant_explicit
#print axioms nativeGK5BLRationalInterpolant_recovers_rat
#print axioms nativeGK5BLRatMap_eval_int
#print axioms nativeGK5BLRatMap_degree_lt
#print axioms nativeGK5BLRationalInterpolant_recovers_int
#print axioms nativeGK5BLRationalInterpolant_recovers_int_coeff
#print axioms nativeGK5BLRationalInterpolant_recovers_data
#print axioms NativeF55P92AssocComparison.gk5blInterpolate_genuine
#print axioms NativeF55P92AssocComparison.gk5blInterpolate_natCoeff
#print axioms nativeGK5BLRationalInterpolant_recovers_P77
#print axioms nativeGK5BLRationalInterpolant_recovers_P77_natCoeff
#print axioms nativeGK5BLNoIntegralLift_of_coeff_not_int
#print axioms NativeF55P92AssocComparison.gk5blRecovered_coeff_nonneg

end
end Kuu.F112.Physical
