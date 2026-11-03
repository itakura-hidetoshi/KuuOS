import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BIDepthCoefficientDescent
import Mathlib.Algebra.Polynomial.Degree.Lemmas
import Mathlib.Tactic

/-!
F112-P94D3GK5BJ — Nat-valued genuine inversion-depth proof counts,
finite weighted specialization sums, and explicit natDegree bounds.

The GK5BI coefficients a_k(f) are integers but NONNEGATIVE for
every genuine typed P92B proof. We construct b_k(f):Nat, prove
(b_k:Int)=a_k, and preserve the TRUE P92B constructor equations
and all 16 P93C / 19 P94A four-cell invariance.

The actual finitely supported source-depth family reconstructs
the established GK5BB N, GK5BE S, GK5BF W as sums weighted by
1, (-1)^k and 2^k. The original P77 source quotient carries
an independently defined Nat-valued coefficient Quotient.lift,
coherent with the prior Int quotient and full polynomial.

A constructive bound is the natDegree of the genuine polynomial:
b_k(f)=0 for every k strictly above that bound. This does NOT
assert a P94A normal form or a local original-to-phi seam from
the scalar threshold W=1.

Strict 空 authority, independent Kuu→Qi, F54 two-Nat and
two-category/Blocks proof indices, original F55 Type-valued
history unchanged. No new axioms, sorry/admit/native_decide,
Gray, universal GK5AY seam, GK5BA kit or unconditional P89
reflection. Append-only, public root107, protected #1558 Draft.
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

/-- Nat-valued depth-k origin-wrapper occurrence count.
The nonnegative certificate is the independently proven GK5BI result. -/
def NativeF55P92AssocComparison.gk5bjNatDepthCoefficient
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) (k : Nat) : Nat :=
  (f.gk5biDepthCoefficient k).toNat

/-- The Nat coefficient casts EXACTLY back to GK5BI's true Int coefficient. -/
theorem NativeF55P92AssocComparison.gk5bjNatCoeff_cast
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) (k : Nat) :
    (f.gk5bjNatDepthCoefficient k : Int) = f.gk5biDepthCoefficient k := by
  unfold NativeF55P92AssocComparison.gk5bjNatDepthCoefficient
  have h := f.gk5biCoeff_nonneg k
  omega

/-- A selected inverse has no original source wrapper at depth zero. -/
theorem NativeF55P92AssocComparison.gk5bjSymm_nat_zero
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    (NativeF55P92AssocComparison.symm f).gk5bjNatDepthCoefficient 0 = 0 := by
  exact congrArg Int.toNat f.gk5biSymm_coeff_zero

/-- Selected inversion shifts actual Nat occurrence counts by one depth. -/
theorem NativeF55P92AssocComparison.gk5bjSymm_nat_succ
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) (k : Nat) :
    (NativeF55P92AssocComparison.symm f).gk5bjNatDepthCoefficient (k + 1) =
      f.gk5bjNatDepthCoefficient k :=
  congrArg Int.toNat (f.gk5biSymm_coeff_succ k)

/-- Vertical pasting adds genuine nonnegative depth counts. -/
theorem NativeF55P92AssocComparison.gk5bjTrans_nat_add
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) (k : Nat) :
    (NativeF55P92AssocComparison.trans f g).gk5bjNatDepthCoefficient k =
      f.gk5bjNatDepthCoefficient k + g.gk5bjNatDepthCoefficient k := by
  have h := f.gk5biTrans_coeff g k
  have hf := f.gk5biCoeff_nonneg k
  have hg := g.gk5biCoeff_nonneg k
  unfold NativeF55P92AssocComparison.gk5bjNatDepthCoefficient
  omega

/-- The original genuine P92B polynomial's natDegree provides
a constructive bound on every actual Nat source-depth coefficient. -/
theorem NativeF55P92AssocComparison.gk5bjNatDepth_bound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) (k : Nat)
    (hk : f.gk5bgDepthPolynomial.natDegree < k) :
    f.gk5bjNatDepthCoefficient k = 0 := by
  have hzero : f.gk5bgDepthPolynomial.coeff k = 0 :=
    Polynomial.coeff_eq_zero_of_natDegree_lt hk
  change (f.gk5bgDepthPolynomial.coeff k).toNat = 0
  rw [hzero]
  rfl

/-- The set of positive Nat depth coefficients is finite. -/
theorem NativeF55P92AssocComparison.gk5bjNatFinite_support
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    ∃ S : Finset Nat, ∀ k : Nat, k ∉ S →
      f.gk5bjNatDepthCoefficient k = 0 := by
  obtain ⟨S, hs⟩ := f.gk5biFinite_support
  refine ⟨S, ?_⟩
  intro k hk
  change (f.gk5biDepthCoefficient k).toNat = 0
  rw [hs k hk]
  rfl

/-- The EXACT finite evaluation formula, at every Int input x.
No artificial finite truncation or arbitrary signed coefficient
nonnegativity assumption enters this statement. -/
theorem NativeF55P92AssocComparison.gk5bjEval_natCoefficients
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) (x : Int) :
    f.gk5bgDepthPolynomial.eval x =
      ∑ k ∈ f.gk5bgDepthPolynomial.support,
        (f.gk5bjNatDepthCoefficient k : Int) * x ^ k := by
  rw [Polynomial.eval_eq_sum]
  change (∑ k ∈ f.gk5bgDepthPolynomial.support,
    f.gk5bgDepthPolynomial.coeff k * x ^ k) = _
  apply Finset.sum_congr rfl
  intro k hk
  change f.gk5biDepthCoefficient k * x ^ k =
    (f.gk5bjNatDepthCoefficient k : Int) * x ^ k
  rw [f.gk5bjNatCoeff_cast k]

/-- GK5BB ORIGINAL wrapper count is the unweighted finite
Nat sum of occurrences at every selected inversion depth. -/
theorem NativeF55P92AssocComparison.gk5bjN_finite_sum
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    f.gk5bbOriginalCount =
      ∑ k ∈ f.gk5bgDepthPolynomial.support, f.gk5bjNatDepthCoefficient k := by
  have h : (f.gk5bbOriginalCount : Int) =
      ∑ k ∈ f.gk5bgDepthPolynomial.support,
        (f.gk5bjNatDepthCoefficient k : Int) := by
    calc
      (f.gk5bbOriginalCount : Int) = f.gk5bgDepthPolynomial.eval (1 : Int) :=
        f.gk5bgEval_one.symm
      _ = ∑ k ∈ f.gk5bgDepthPolynomial.support,
          (f.gk5bjNatDepthCoefficient k : Int) := by
        simpa only [one_pow, mul_one] using f.gk5bjEval_natCoefficients (1 : Int)
  exact_mod_cast h

/-- GK5BE signed charge is the finite ALTERNATING sum of
genuine Nat depth counts, with inversion parity (-1)^k. -/
theorem NativeF55P92AssocComparison.gk5bjS_finite_sum
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    f.gk5beSignedCount =
      ∑ k ∈ f.gk5bgDepthPolynomial.support,
        (f.gk5bjNatDepthCoefficient k : Int) * (-1 : Int) ^ k := by
  calc
    f.gk5beSignedCount = f.gk5bgDepthPolynomial.eval (-1 : Int) :=
      f.gk5bgEval_neg_one.symm
    _ = _ := f.gk5bjEval_natCoefficients (-1 : Int)

/-- GK5BF original inverse-depth weight equals a genuinely
finite NATURAL weighted count sum with factor 2^k. -/
theorem NativeF55P92AssocComparison.gk5bjW_finite_sum
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    f.gk5bfInverseDepthWeight =
      ∑ k ∈ f.gk5bgDepthPolynomial.support,
        f.gk5bjNatDepthCoefficient k * 2 ^ k := by
  have h : (f.gk5bfInverseDepthWeight : Int) =
      ∑ k ∈ f.gk5bgDepthPolynomial.support,
        (f.gk5bjNatDepthCoefficient k : Int) * (2 : Int) ^ k := by
    calc
      (f.gk5bfInverseDepthWeight : Int) = f.gk5bgDepthPolynomial.eval (2 : Int) :=
        f.gk5bgEval_two.symm
      _ = _ := f.gk5bjEval_natCoefficients (2 : Int)
  exact_mod_cast h

/-- Each of the 16 genuine chosen P93C four-cell generators
preserves the Nat occurrence count at each depth. -/
theorem NativeF55P93AssocFourCell.gk5bjNatCoeff_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) (k : Nat) :
    f.gk5bjNatDepthCoefficient k = g.gk5bjNatDepthCoefficient k :=
  congrArg Int.toNat (w.gk5biCoeff_sound k)

/-- Each of all 19 P94A constructors preserves the Nat
occurrence count, including horizontalUnit and contextUnit. -/
theorem NativeF55P94UnitFourCell.gk5bjNatCoeff_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) (k : Nat) :
    f.gk5bjNatDepthCoefficient k = g.gk5bjNatDepthCoefficient k :=
  congrArg Int.toNat (w.gk5biCoeff_sound k)

/-- True original P77 four-cell transport also preserves
the Nat coefficient of structural phi, at every depth. -/
theorem nativeGK5BJNatCoeff_sound_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) (k : Nat) :
    (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k =
      (nativeGK5AIOriginalToP92Structural g).gk5bjNatDepthCoefficient k :=
  congrArg Int.toNat (nativeGK5BICoeff_sound_P77 w k)

/-- A genuine Nat-valued Quotient.lift from original F55
source classes. This is not a quotient of numeric shadows. -/
def nativeGK5BJNatCoeffOnP77Class
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (k : Nat) :
    NativeF55RawVerticalFourClasses first last r s → Nat :=
  _root_.Quotient.lift
    (fun f => (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact nativeGK5BJNatCoeff_sound_P77 w k)

/-- The independently descended Nat coefficient, cast to Int,
is EXACTLY the old descended Int coefficient on real P77 classes. -/
theorem nativeGK5BJNatCoeffOnP77Class_cast
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (k : Nat) :
    (nativeGK5BJNatCoeffOnP77Class first last r s k q : Int) =
      nativeGK5BICoeffOnP77Class first last r s k q := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  change ((nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k : Int) =
    (nativeGK5AIOriginalToP92Structural f).gk5biDepthCoefficient k
  exact (nativeGK5AIOriginalToP92Structural f).gk5bjNatCoeff_cast k

/-- Nat coefficient at genuine P77 class equals Int-lift.toNat. -/
theorem nativeGK5BJNatCoeffOnP77Class_eq_toNat
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (k : Nat) :
    nativeGK5BJNatCoeffOnP77Class first last r s k q =
      (nativeGK5BICoeffOnP77Class first last r s k q).toNat := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  rfl

/-- Nat-valued source P77 coefficients vanish past the explicit
natDegree of the ACTUAL descended full polynomial. -/
theorem nativeGK5BJNatCoeffOnP77Class_bound
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (k : Nat)
    (hk : (nativeGK5BGPolyOnP77Class first last r s q).natDegree < k) :
    nativeGK5BJNatCoeffOnP77Class first last r s k q = 0 := by
  refine _root_.Quotient.inductionOn q ?_ hk
  intro f hk
  change (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree < k at hk
  change (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepthCoefficient k = 0
  exact (nativeGK5AIOriginalToP92Structural f).gk5bjNatDepth_bound k hk

/-- Every genuine P77 class gives finite weighted Nat coefficients
whose evaluation recovers the FULL descended polynomial. -/
theorem nativeGK5BJNatCoeffOnP77Class_eval
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s)
    (x : Int) :
    (nativeGK5BGPolyOnP77Class first last r s q).eval x =
      ∑ k ∈ (nativeGK5BGPolyOnP77Class first last r s q).support,
        (nativeGK5BJNatCoeffOnP77Class first last r s k q : Int) * x ^ k := by
  rw [Polynomial.eval_eq_sum]
  change (∑ k ∈ (nativeGK5BGPolyOnP77Class first last r s q).support,
    (nativeGK5BGPolyOnP77Class first last r s q).coeff k * x ^ k) = _
  apply Finset.sum_congr rfl
  intro k hk
  have hc := nativeGK5BJNatCoeffOnP77Class_cast first last r s q k
  have hp := nativeGK5BICoeffOnP77Class_eq_poly first last r s q k
  calc
    (nativeGK5BGPolyOnP77Class first last r s q).coeff k * x ^ k =
        nativeGK5BICoeffOnP77Class first last r s k q * x ^ k := by rw [hp]
    _ = (nativeGK5BJNatCoeffOnP77Class first last r s k q : Int) * x ^ k := by
        rw [hc]

/-- The family of all Nat source-P77 coefficients exactly retains
the polynomial, not just the three scalar evaluations. -/
theorem nativeGK5BJNatCoeffOnP77Class_all_iff_poly
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q₁ q₂ : NativeF55RawVerticalFourClasses first last r s) :
    (∀ k : Nat, nativeGK5BJNatCoeffOnP77Class first last r s k q₁ =
       nativeGK5BJNatCoeffOnP77Class first last r s k q₂) ↔
      nativeGK5BGPolyOnP77Class first last r s q₁ =
        nativeGK5BGPolyOnP77Class first last r s q₂ := by
  constructor
  · intro h
    apply (nativeGK5BICoeffOnP77Class_all_iff_poly first last r s q₁ q₂).mp
    intro k
    calc
      nativeGK5BICoeffOnP77Class first last r s k q₁ =
          (nativeGK5BJNatCoeffOnP77Class first last r s k q₁ : Int) :=
        (nativeGK5BJNatCoeffOnP77Class_cast first last r s q₁ k).symm
      _ = (nativeGK5BJNatCoeffOnP77Class first last r s k q₂ : Int) :=
        congrArg (fun t : Nat => (t : Int)) (h k)
      _ = nativeGK5BICoeffOnP77Class first last r s k q₂ :=
        nativeGK5BJNatCoeffOnP77Class_cast first last r s q₂ k
  · intro hp k
    have hc := (nativeGK5BICoeffOnP77Class_all_iff_poly
      first last r s q₁ q₂).mpr hp k
    rw [nativeGK5BJNatCoeffOnP77Class_eq_toNat,
      nativeGK5BJNatCoeffOnP77Class_eq_toNat]
    exact congrArg Int.toNat hc

#print axioms NativeF55P92AssocComparison.gk5bjNatDepthCoefficient
#print axioms NativeF55P92AssocComparison.gk5bjNatCoeff_cast
#print axioms NativeF55P92AssocComparison.gk5bjSymm_nat_zero
#print axioms NativeF55P92AssocComparison.gk5bjSymm_nat_succ
#print axioms NativeF55P92AssocComparison.gk5bjTrans_nat_add
#print axioms NativeF55P92AssocComparison.gk5bjNatDepth_bound
#print axioms NativeF55P92AssocComparison.gk5bjNatFinite_support
#print axioms NativeF55P92AssocComparison.gk5bjEval_natCoefficients
#print axioms NativeF55P92AssocComparison.gk5bjN_finite_sum
#print axioms NativeF55P92AssocComparison.gk5bjS_finite_sum
#print axioms NativeF55P92AssocComparison.gk5bjW_finite_sum
#print axioms NativeF55P93AssocFourCell.gk5bjNatCoeff_sound
#print axioms NativeF55P94UnitFourCell.gk5bjNatCoeff_sound
#print axioms nativeGK5BJNatCoeff_sound_P77
#print axioms nativeGK5BJNatCoeffOnP77Class
#print axioms nativeGK5BJNatCoeffOnP77Class_cast
#print axioms nativeGK5BJNatCoeffOnP77Class_eq_toNat
#print axioms nativeGK5BJNatCoeffOnP77Class_bound
#print axioms nativeGK5BJNatCoeffOnP77Class_eval
#print axioms nativeGK5BJNatCoeffOnP77Class_all_iff_poly

end
end Kuu.F112.Physical
