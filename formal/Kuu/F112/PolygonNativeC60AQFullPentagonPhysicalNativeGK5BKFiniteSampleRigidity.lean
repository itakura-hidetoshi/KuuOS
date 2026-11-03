import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BJNatDepthWeightedSums
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Tactic

/-!
F112-P94D3GK5BK — FINITE INTEGER SAMPLE RIGIDITY
of genuine typed P92B inversion-depth polynomials and actual
original F55/P77 source four-cell quotient polynomial values.

For two degree-bounded polynomials P,Q∈ℤ[X], equality of evaluations
at d+1 DISTINCT integer sites, with natDegree P,Q≤d, implies P=Q.
This is an explicit application of the pinned Mathlib root-count
lemma eq_of_natDegree_lt_card_of_eval_eq', NOT an assumed
interpolation or a hypothetical P94A completion certificate.

Specialize to every genuinely dependent P92B f,g and to every
two ACTUAL original P77 source quotient classes q₁,q₂ in the
same F54 Hom. The finite observations determine the ENTIRE
original inversion-depth polynomial, all Int depth coefficients
GK5BI, all Nat coefficients GK5BJ, and N/S/W scalar grades.
The P77 conclusion is equality of descended polynomial VALUES,
NOT equality of quotient classes or existence of a P94A 4-cell.

Construct the canonical integer sample grid {0,1,...,d}
with exactly d+1 DISTINCT sites. Also prove that one unequal
coefficient forces at least one mismatch in ANY such finite
sample set. This distinguishes finite observational fidelity
from four-cell existence and raw Type-valued proof identity.

Strict 空 authority, independent Kuu→Qi, unchanged F54 two-Nat/
two-category/Blocks and Type-valued F55 proof history.
Append-only root107; #1558 remains Draft/open/unmerged.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry/admit/native_decide/new axioms, Gray, global GK5AY seam,
GK5BA kit, unconditional P89 reflection, or P94A normal form.
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

/-- A finite set of exactly d+1 distinct integer observations
determines every polynomial of natDegree at most d. The samples
can be ANY distinct integer points: not only the canonical grid. -/
theorem nativeGK5BKPolynomial_finiteSamples
    (P Q : Polynomial Int) (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hP : P.natDegree ≤ d) (hQ : Q.natDegree ≤ d)
    (heval : ∀ z ∈ samples, P.eval z = Q.eval z) : P = Q := by
  apply Polynomial.eq_of_natDegree_lt_card_of_eval_eq' P Q samples heval
  calc
    max P.natDegree Q.natDegree ≤ d := max_le hP hQ
    _ < samples.card := by omega

/-- A canonical d+1-point finite set of DISTINCT integer sites. -/
def nativeGK5BKIntegerGrid (d : Nat) : Finset Int :=
  (Finset.range (d + 1)).image (fun k : Nat => (k : Int))

/-- Integer casting is injective, so the canonical grid has d+1 sites. -/
theorem nativeGK5BKIntegerGrid_card (d : Nat) :
    (nativeGK5BKIntegerGrid d).card = d + 1 := by
  unfold nativeGK5BKIntegerGrid
  have hinj : Function.Injective (fun k : Nat => (k : Int)) := by
    intro i j h
    exact_mod_cast h
  rw [Finset.card_image_of_injective (Finset.range (d + 1)) hinj]
  exact Finset.card_range _

/-- The integer image of each index within 0,...,d lies in the grid. -/
theorem nativeGK5BKIntegerGrid_mem (d k : Nat) (hk : k ≤ d) :
    (k : Int) ∈ nativeGK5BKIntegerGrid d := by
  unfold nativeGK5BKIntegerGrid
  refine Finset.mem_image.mpr ⟨k, Finset.mem_range.mpr (by omega), rfl⟩

/-- For ALL genuine typed P92B three-proofs f,g, equality of
d+1 observations forces equality of the full depth polynomials. -/
theorem NativeF55P92AssocComparison.gk5bkFinite_eval_poly
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hf : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (hg : g.gk5bgDepthPolynomial.natDegree ≤ d)
    (heval : ∀ z ∈ samples,
      f.gk5bgDepthPolynomial.eval z = g.gk5bgDepthPolynomial.eval z) :
    f.gk5bgDepthPolynomial = g.gk5bgDepthPolynomial :=
  nativeGK5BKPolynomial_finiteSamples
    f.gk5bgDepthPolynomial g.gk5bgDepthPolynomial d samples hsize hf hg heval

/-- Finite sample agreement recovers every original GK5BI
integer depth coefficient, not just the three N/S/W grades. -/
theorem NativeF55P92AssocComparison.gk5bkFinite_eval_intCoeff
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hf : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (hg : g.gk5bgDepthPolynomial.natDegree ≤ d)
    (heval : ∀ z ∈ samples,
      f.gk5bgDepthPolynomial.eval z = g.gk5bgDepthPolynomial.eval z)
    (k : Nat) :
    f.gk5biDepthCoefficient k = g.gk5biDepthCoefficient k := by
  have hp := f.gk5bkFinite_eval_poly g d samples hsize hf hg heval
  exact congrArg (fun P : Polynomial Int => P.coeff k) hp

/-- Finite sample agreement recovers the TRUE natural-number
wrapper occurrence at every chosen inversion depth. -/
theorem NativeF55P92AssocComparison.gk5bkFinite_eval_natCoeff
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hf : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (hg : g.gk5bgDepthPolynomial.natDegree ≤ d)
    (heval : ∀ z ∈ samples,
      f.gk5bgDepthPolynomial.eval z = g.gk5bgDepthPolynomial.eval z)
    (k : Nat) :
    f.gk5bjNatDepthCoefficient k = g.gk5bjNatDepthCoefficient k :=
  congrArg Int.toNat
    (f.gk5bkFinite_eval_intCoeff g d samples hsize hf hg heval k)

/-- The entire family of Nat coefficients determines all d+1
sample values, and conversely under the degree bound. -/
theorem NativeF55P92AssocComparison.gk5bkFinite_eval_iff_natCoeffs
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hf : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (hg : g.gk5bgDepthPolynomial.natDegree ≤ d) :
    (∀ z ∈ samples,
      f.gk5bgDepthPolynomial.eval z = g.gk5bgDepthPolynomial.eval z) ↔
    (∀ k : Nat, f.gk5bjNatDepthCoefficient k =
      g.gk5bjNatDepthCoefficient k) := by
  constructor
  · intro h k
    exact f.gk5bkFinite_eval_natCoeff g d samples hsize hf hg h k
  · intro h z hz
    have hp : f.gk5bgDepthPolynomial = g.gk5bgDepthPolynomial := by
      apply Polynomial.ext
      intro k
      calc
        f.gk5bgDepthPolynomial.coeff k =
            (f.gk5bjNatDepthCoefficient k : Int) :=
          (f.gk5bjNatCoeff_cast k).symm
        _ = (g.gk5bjNatDepthCoefficient k : Int) :=
          congrArg (fun t : Nat => (t : Int)) (h k)
        _ = g.gk5bgDepthPolynomial.coeff k :=
          g.gk5bjNatCoeff_cast k
    exact congrArg (Polynomial.eval z) hp

/-- Even the explicit 0,1,...,d integer grid suffices for
finite-observation uniqueness in every typed P92B fiber. -/
theorem NativeF55P92AssocComparison.gk5bkCanonicalGrid_faithful
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s)
    (d : Nat)
    (hf : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (hg : g.gk5bgDepthPolynomial.natDegree ≤ d)
    (heval : ∀ k : Nat, k ≤ d →
      f.gk5bgDepthPolynomial.eval (k : Int) =
      g.gk5bgDepthPolynomial.eval (k : Int)) :
    f.gk5bgDepthPolynomial = g.gk5bgDepthPolynomial := by
  apply f.gk5bkFinite_eval_poly g d
    (nativeGK5BKIntegerGrid d) (nativeGK5BKIntegerGrid_card d) hf hg
  intro z hz
  change z ∈ (Finset.range (d + 1)).image (fun k : Nat => (k : Int)) at hz
  rcases Finset.mem_image.mp hz with ⟨k, hk, hzk⟩
  subst z
  exact heval k (by have := Finset.mem_range.mp hk; omega)

/-- A single Nat coefficient mismatch is visible at SOME site
in EVERY set of d+1 distinct samples. This is a finite
observational obstruction, not a newly constructed 4-cell. -/
theorem NativeF55P92AssocComparison.gk5bkExists_sample_diff_of_natCoeff_ne
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hf : f.gk5bgDepthPolynomial.natDegree ≤ d)
    (hg : g.gk5bgDepthPolynomial.natDegree ≤ d)
    (k : Nat)
    (hne : f.gk5bjNatDepthCoefficient k ≠ g.gk5bjNatDepthCoefficient k) :
    ∃ z ∈ samples,
      f.gk5bgDepthPolynomial.eval z ≠ g.gk5bgDepthPolynomial.eval z := by
  by_contra hno
  have hvalues : ∀ z ∈ samples,
      f.gk5bgDepthPolynomial.eval z = g.gk5bgDepthPolynomial.eval z := by
    intro z hz
    by_contra hneval
    exact hno ⟨z, hz, hneval⟩
  exact hne (f.gk5bkFinite_eval_natCoeff g d samples hsize hf hg hvalues k)

/-- The genuinely chosen P94A 19-constructor four-cell
preserves EVERY evaluation, whether or not a degree bound
is known. This is only a necessary invariant for a 4-cell. -/
theorem NativeF55P94UnitFourCell.gk5bkEval_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) (z : Int) :
    f.gk5bgDepthPolynomial.eval z = g.gk5bgDepthPolynomial.eval z :=
  congrArg (Polynomial.eval z) w.gk5bgDepthPolynomial_sound

/-- For TRUE original source-P77 classes, d+1 integer
observations determine the descended full polynomial VALUE. -/
theorem nativeGK5BKFinite_eval_P77_poly
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q₁ q₂ : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hq₁ : (nativeGK5BGPolyOnP77Class first last r s q₁).natDegree ≤ d)
    (hq₂ : (nativeGK5BGPolyOnP77Class first last r s q₂).natDegree ≤ d)
    (heval : ∀ z ∈ samples,
      (nativeGK5BGPolyOnP77Class first last r s q₁).eval z =
        (nativeGK5BGPolyOnP77Class first last r s q₂).eval z) :
    nativeGK5BGPolyOnP77Class first last r s q₁ =
      nativeGK5BGPolyOnP77Class first last r s q₂ :=
  nativeGK5BKPolynomial_finiteSamples
    (nativeGK5BGPolyOnP77Class first last r s q₁)
    (nativeGK5BGPolyOnP77Class first last r s q₂)
    d samples hsize hq₁ hq₂ heval

/-- The ALL-Nat-coefficient observation is equivalent to
the d+1 finite P77 class-value observations, under degree
bounds. Neither side identifies original Type-valued proofs. -/
theorem nativeGK5BKFinite_eval_P77_iff_natCoeffs
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q₁ q₂ : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hq₁ : (nativeGK5BGPolyOnP77Class first last r s q₁).natDegree ≤ d)
    (hq₂ : (nativeGK5BGPolyOnP77Class first last r s q₂).natDegree ≤ d) :
    (∀ z ∈ samples,
      (nativeGK5BGPolyOnP77Class first last r s q₁).eval z =
        (nativeGK5BGPolyOnP77Class first last r s q₂).eval z) ↔
    (∀ k : Nat,
      nativeGK5BJNatCoeffOnP77Class first last r s k q₁ =
        nativeGK5BJNatCoeffOnP77Class first last r s k q₂) := by
  constructor
  · intro heval
    exact (nativeGK5BJNatCoeffOnP77Class_all_iff_poly
      first last r s q₁ q₂).2
        (nativeGK5BKFinite_eval_P77_poly
          first last r s q₁ q₂ d samples hsize hq₁ hq₂ heval)
  · intro h z hz
    have hp := (nativeGK5BJNatCoeffOnP77Class_all_iff_poly
      first last r s q₁ q₂).1 h
    exact congrArg (Polynomial.eval z) hp

/-- The canonical integer grid provides a deterministic finite
faithful observation set for actual source-P77 polynomial values. -/
theorem nativeGK5BKCanonicalGrid_P77_poly
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q₁ q₂ : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat)
    (hq₁ : (nativeGK5BGPolyOnP77Class first last r s q₁).natDegree ≤ d)
    (hq₂ : (nativeGK5BGPolyOnP77Class first last r s q₂).natDegree ≤ d)
    (heval : ∀ k : Nat, k ≤ d →
      (nativeGK5BGPolyOnP77Class first last r s q₁).eval (k : Int) =
        (nativeGK5BGPolyOnP77Class first last r s q₂).eval (k : Int)) :
    nativeGK5BGPolyOnP77Class first last r s q₁ =
      nativeGK5BGPolyOnP77Class first last r s q₂ := by
  apply nativeGK5BKFinite_eval_P77_poly
    first last r s q₁ q₂ d
    (nativeGK5BKIntegerGrid d) (nativeGK5BKIntegerGrid_card d) hq₁ hq₂
  intro z hz
  change z ∈ (Finset.range (d + 1)).image (fun k : Nat => (k : Int)) at hz
  rcases Finset.mem_image.mp hz with ⟨k, hk, hzk⟩
  subst z
  exact heval k (by have := Finset.mem_range.mp hk; omega)

/-- One genuine source P77 Nat coefficient discrepancy
must appear in some sample evaluation of any d+1-point set.
It is NOT claimed that equal observations imply q₁=q₂. -/
theorem nativeGK5BKExists_P77_sample_diff_of_natCoeff_ne
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q₁ q₂ : NativeF55RawVerticalFourClasses first last r s)
    (d : Nat) (samples : Finset Int)
    (hsize : samples.card = d + 1)
    (hq₁ : (nativeGK5BGPolyOnP77Class first last r s q₁).natDegree ≤ d)
    (hq₂ : (nativeGK5BGPolyOnP77Class first last r s q₂).natDegree ≤ d)
    (k : Nat)
    (hne : nativeGK5BJNatCoeffOnP77Class first last r s k q₁ ≠
      nativeGK5BJNatCoeffOnP77Class first last r s k q₂) :
    ∃ z ∈ samples,
      (nativeGK5BGPolyOnP77Class first last r s q₁).eval z ≠
        (nativeGK5BGPolyOnP77Class first last r s q₂).eval z := by
  by_contra hno
  have heval : ∀ z ∈ samples,
      (nativeGK5BGPolyOnP77Class first last r s q₁).eval z =
        (nativeGK5BGPolyOnP77Class first last r s q₂).eval z := by
    intro z hz
    by_contra hneval
    exact hno ⟨z, hz, hneval⟩
  have hcoeff := (nativeGK5BKFinite_eval_P77_iff_natCoeffs
    first last r s q₁ q₂ d samples hsize hq₁ hq₂).1 heval
  exact hne (hcoeff k)

#print axioms nativeGK5BKPolynomial_finiteSamples
#print axioms nativeGK5BKIntegerGrid
#print axioms nativeGK5BKIntegerGrid_card
#print axioms nativeGK5BKIntegerGrid_mem
#print axioms NativeF55P92AssocComparison.gk5bkFinite_eval_poly
#print axioms NativeF55P92AssocComparison.gk5bkFinite_eval_intCoeff
#print axioms NativeF55P92AssocComparison.gk5bkFinite_eval_natCoeff
#print axioms NativeF55P92AssocComparison.gk5bkFinite_eval_iff_natCoeffs
#print axioms NativeF55P92AssocComparison.gk5bkCanonicalGrid_faithful
#print axioms NativeF55P92AssocComparison.gk5bkExists_sample_diff_of_natCoeff_ne
#print axioms NativeF55P94UnitFourCell.gk5bkEval_sound
#print axioms nativeGK5BKFinite_eval_P77_poly
#print axioms nativeGK5BKFinite_eval_P77_iff_natCoeffs
#print axioms nativeGK5BKCanonicalGrid_P77_poly
#print axioms nativeGK5BKExists_P77_sample_diff_of_natCoeff_ne

end
end Kuu.F112.Physical
