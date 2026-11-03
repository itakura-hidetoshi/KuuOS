import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BHUnitPolynomialWeightOne
import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Tactic

/-!
F112-P94D3GK5BI — coefficientwise inversion-depth evidence.

For each genuine typed P92B 3-proof f and k : Nat, take the ACTUAL
coefficient a_k(f) = coeff(P_f, k) : Int of the GK5BG depth polynomial.
The polynomial originates in finite P92B constructor trees, not in an
arbitrary signed polynomial. Hence every a_k is nonnegative, and only
finitely many depths carry nonzero evidence.

The selected P92B inverse shifts depth k to k+1; genuine vertical
pasting adds coefficients. All 16 P93C / 19 P94A true four-cell
constructors preserve EACH coefficient, by specialization of GK5BG's
inductively proved whole-polynomial preservation. An actual source
P77 four-cell preserves coefficients; independently construct the
Int-valued coefficient Quotient.lift on TRUE original P77 source
classes, and prove it agrees with coefficient extraction from the
previously descended polynomial. Coefficients jointly reconstruct
the full polynomial, so no three-scalar collapse is presumed.

No inference from W=1 to existence of a P94A seam, no universal
GK5AY seam or P94A normal form, no Gray, no new axioms or sorry.
Strict 空, independent Kuu→Qi, original F54 two-Nat/two-category/
Blocks and original Type-valued F55 histories are retained.
Append-only, same public root 107, protected #1558 Draft/open.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Exact depth-k original-wrapper coefficient, not a new shadow invariant. -/
def NativeF55P92AssocComparison.gk5biDepthCoefficient
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) (k : Nat) : Int :=
  f.gk5bgDepthPolynomial.coeff k

/-- At inversion depth zero, a selected inverse has no source wrapper. -/
theorem NativeF55P92AssocComparison.gk5biSymm_coeff_zero
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    (NativeF55P92AssocComparison.symm f).gk5biDepthCoefficient 0 = 0 := by
  change (f.gk5bgDepthPolynomial * Polynomial.X).coeff 0 = 0
  exact Polynomial.coeff_mul_X_zero _

/-- A chosen inverse shifts the original inversion depth by ONE. -/
theorem NativeF55P92AssocComparison.gk5biSymm_coeff_succ
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) (k : Nat) :
    (NativeF55P92AssocComparison.symm f).gk5biDepthCoefficient (k + 1) =
      f.gk5biDepthCoefficient k := by
  change (f.gk5bgDepthPolynomial * Polynomial.X).coeff (k + 1) =
    f.gk5bgDepthPolynomial.coeff k
  exact Polynomial.coeff_mul_X _ _

/-- Vertical composition adds depth coefficients without mixing degrees. -/
theorem NativeF55P92AssocComparison.gk5biTrans_coeff
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) (k : Nat) :
    (NativeF55P92AssocComparison.trans f g).gk5biDepthCoefficient k =
      f.gk5biDepthCoefficient k + g.gk5biDepthCoefficient k := by
  change (f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial).coeff k =
    f.gk5bgDepthPolynomial.coeff k + g.gk5bgDepthPolynomial.coeff k
  exact Polynomial.coeff_add _ _ _

/-- Actual P92B-generated depth coefficients are NONNEGATIVE
for every depth, by induction over all nine genuine P92B constructors.
The statement would be false for arbitrary signed polynomials. -/
theorem NativeF55P92AssocComparison.gk5biCoeff_nonneg
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    ∀ k : Nat, 0 ≤ f.gk5biDepthCoefficient k := by
  induction f with
  | original old =>
      intro k
      change 0 ≤ (1 : Polynomial Int).coeff k
      rw [Polynomial.coeff_one]
      split_ifs <;> omega
  | assocNaturality u v w =>
      intro k
      change 0 ≤ (0 : Polynomial Int).coeff k
      simp
  | refl r =>
      intro k
      change 0 ≤ (0 : Polynomial Int).coeff k
      simp
  | symm f ih =>
      intro k
      cases k with
      | zero =>
          change 0 ≤ (f.gk5bgDepthPolynomial * Polynomial.X).coeff 0
          rw [Polynomial.coeff_mul_X_zero]
      | succ k =>
          change 0 ≤ (f.gk5bgDepthPolynomial * Polynomial.X).coeff (k + 1)
          rw [Polynomial.coeff_mul_X]
          exact ih k
  | trans f g ihf ihg =>
      intro k
      change 0 ≤ (f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial).coeff k
      rw [Polynomial.coeff_add]
      exact add_nonneg (ihf k) (ihg k)
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- Only a FINITE set of inversion depths is supported. -/
theorem NativeF55P92AssocComparison.gk5biFinite_support
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    ∃ s : Finset Nat, ∀ k : Nat, k ∉ s → f.gk5biDepthCoefficient k = 0 := by
  refine ⟨f.gk5bgDepthPolynomial.support, ?_⟩
  intro k hk
  change f.gk5bgDepthPolynomial.coeff k = 0
  exact Polynomial.notMem_support_iff.mp hk

/-- The entire polynomial is reconstructed from its individual
coefficients; this is an exact invariant, not only three evaluations. -/
theorem NativeF55P92AssocComparison.gk5biAll_coeff_iff_poly
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55P92AssocComparison p r s) :
    (∀ k : Nat, f.gk5biDepthCoefficient k = g.gk5biDepthCoefficient k) ↔
      f.gk5bgDepthPolynomial = g.gk5bgDepthPolynomial := by
  constructor
  · intro h
    apply Polynomial.ext
    intro k
    exact h k
  · intro hp k
    exact congrArg (fun P : Polynomial Int => P.coeff k) hp

/-- Each of all 16 genuine P93C four-cell constructors preserves
the separate k-th depth coefficient. -/
theorem NativeF55P93AssocFourCell.gk5biCoeff_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) (k : Nat) :
    f.gk5biDepthCoefficient k = g.gk5biDepthCoefficient k :=
  congrArg (fun P : Polynomial Int => P.coeff k) w.gk5bgDepthPolynomial_sound

/-- Each of all 19 genuine P94A four-cell constructors preserves
the k-th coefficient; the GK5BG inductive proof already covers
the added horizontalUnit and both contextUnit cases. -/
theorem NativeF55P94UnitFourCell.gk5biCoeff_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) (k : Nat) :
    f.gk5biDepthCoefficient k = g.gk5biDepthCoefficient k :=
  congrArg (fun P : Polynomial Int => P.coeff k) w.gk5bgDepthPolynomial_sound

/-- A TRUE original P77 four-cell transports coefficient k
through the existing GK5AJ typed source→selected map. -/
theorem nativeGK5BICoeff_sound_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) (k : Nat) :
    (nativeGK5AIOriginalToP92Structural f).gk5biDepthCoefficient k =
      (nativeGK5AIOriginalToP92Structural g).gk5biDepthCoefficient k :=
  congrArg (fun P : Polynomial Int => P.coeff k) (nativeGK5BGPoly_sound_P77 w)

/-- Independently lift the k-th Int coefficient to the EXACT
original source P77 quotient; raw Type proofs remain distinct. -/
def nativeGK5BICoeffOnP77Class
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (k : Nat) :
    NativeF55RawVerticalFourClasses first last r s → Int :=
  _root_.Quotient.lift
    (fun f => (nativeGK5AIOriginalToP92Structural f).gk5biDepthCoefficient k)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact nativeGK5BICoeff_sound_P77 w k)

/-- Coefficient-class lift computes at genuine original representatives. -/
theorem nativeGK5BICoeffOnP77Class_mk
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (k : Nat) :
    nativeGK5BICoeffOnP77Class first last r s k
      (nativeF55RawVerticalFourClass first last f) =
      (nativeGK5AIOriginalToP92Structural f).gk5biDepthCoefficient k :=
  rfl

/-- The independent coefficient Quotient.lift is the coefficient
of GK5BG's independent whole-polynomial Quotient.lift. -/
theorem nativeGK5BICoeffOnP77Class_eq_poly
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (k : Nat) :
    nativeGK5BICoeffOnP77Class first last r s k q =
      (nativeGK5BGPolyOnP77Class first last r s q).coeff k := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  rfl

/-- Every descended source-P77 coefficient is nonnegative. -/
theorem nativeGK5BICoeffOnP77Class_nonneg
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (k : Nat) :
    0 ≤ nativeGK5BICoeffOnP77Class first last r s k q := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  change 0 ≤ (nativeGK5AIOriginalToP92Structural f).gk5biDepthCoefficient k
  exact (nativeGK5AIOriginalToP92Structural f).gk5biCoeff_nonneg k

/-- The original-P77-class depth support remains finite. -/
theorem nativeGK5BICoeffOnP77Class_finite_support
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s) :
    ∃ S : Finset Nat, ∀ k : Nat,
      k ∉ S → nativeGK5BICoeffOnP77Class first last r s k q = 0 := by
  refine ⟨(nativeGK5BGPolyOnP77Class first last r s q).support, ?_⟩
  intro k hk
  rw [nativeGK5BICoeffOnP77Class_eq_poly]
  exact Polynomial.notMem_support_iff.mp hk

/-- The full actual descended polynomial is exactly the family
of all descended coefficient witnesses; not merely N, S and W. -/
theorem nativeGK5BICoeffOnP77Class_all_iff_poly
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q₁ q₂ : NativeF55RawVerticalFourClasses first last r s) :
    (∀ k : Nat,
      nativeGK5BICoeffOnP77Class first last r s k q₁ =
        nativeGK5BICoeffOnP77Class first last r s k q₂) ↔
      nativeGK5BGPolyOnP77Class first last r s q₁ =
        nativeGK5BGPolyOnP77Class first last r s q₂ := by
  constructor
  · intro h
    apply Polynomial.ext
    intro k
    exact (nativeGK5BICoeffOnP77Class_eq_poly first last r s q₁ k).symm.trans
      ((h k).trans (nativeGK5BICoeffOnP77Class_eq_poly first last r s q₂ k))
  · intro hp k
    calc
      nativeGK5BICoeffOnP77Class first last r s k q₁ =
          (nativeGK5BGPolyOnP77Class first last r s q₁).coeff k :=
        nativeGK5BICoeffOnP77Class_eq_poly first last r s q₁ k
      _ = (nativeGK5BGPolyOnP77Class first last r s q₂).coeff k :=
        congrArg (fun P : Polynomial Int => P.coeff k) hp
      _ = nativeGK5BICoeffOnP77Class first last r s k q₂ :=
        (nativeGK5BICoeffOnP77Class_eq_poly first last r s q₂ k).symm

/-- Any specific depth coefficient mismatch obstructs a P94A comparison,
even when all three N/S/W scalar observations happen to coincide. -/
theorem nativeGK5BINoP94_of_coeff_ne
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (k : Nat)
    (h : f.gk5biDepthCoefficient k ≠ g.gk5biDepthCoefficient k) :
    ¬ Nonempty (NativeF55P94UnitFourCell f g) := by
  rintro ⟨w⟩
  exact h (w.gk5biCoeff_sound k)

#print axioms NativeF55P92AssocComparison.gk5biDepthCoefficient
#print axioms NativeF55P92AssocComparison.gk5biSymm_coeff_zero
#print axioms NativeF55P92AssocComparison.gk5biSymm_coeff_succ
#print axioms NativeF55P92AssocComparison.gk5biTrans_coeff
#print axioms NativeF55P92AssocComparison.gk5biCoeff_nonneg
#print axioms NativeF55P92AssocComparison.gk5biFinite_support
#print axioms NativeF55P92AssocComparison.gk5biAll_coeff_iff_poly
#print axioms NativeF55P93AssocFourCell.gk5biCoeff_sound
#print axioms NativeF55P94UnitFourCell.gk5biCoeff_sound
#print axioms nativeGK5BICoeff_sound_P77
#print axioms nativeGK5BICoeffOnP77Class
#print axioms nativeGK5BICoeffOnP77Class_mk
#print axioms nativeGK5BICoeffOnP77Class_eq_poly
#print axioms nativeGK5BICoeffOnP77Class_nonneg
#print axioms nativeGK5BICoeffOnP77Class_finite_support
#print axioms nativeGK5BICoeffOnP77Class_all_iff_poly
#print axioms nativeGK5BINoP94_of_coeff_ne

end
end Kuu.F112.Physical
