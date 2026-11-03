import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFDoubleInversionWeightObstruction
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Tactic

/-!
F112-P94D3GK5BG — COMPLETE P92B inversion-depth generating
polynomial, with genuine Type-valued P93C/P94A preservation,
actual P77 quotient descent, and scalar specialization.

For any chosen P92B 3-proof f, define P_f(X) in Int[X]:
  original -> 1; refl/assocNaturality -> 0;
  symm -> P * X; trans/horizontal -> P+Q;
  left/right F45 and pre/post F54 contexts -> P.
Every genuine P93C (16 generators) and P94A (19 generators)
Type-valued 4-cell preserves the WHOLE polynomial.

The previously independent scalar invariants are EXACTLY
N(f) = P_f(1) (cast Nat to Int),
S(f) = P_f(-1), and
W(f) = P_f(2) (cast Nat to Int).
All equalities are constructive Mathlib Polynomial.eval proofs.

A genuine original P77 source 4-cell translates by GK5AJ
to a selected P93C four-cell. Therefore P_phi(f)(X) descends
as an actual Polynomial Int VALUE through the *existing*
P77 quotient, not merely a Prop or a shadow comparison.
An actual local seam original(f) -> phi(f) forces P_phi(f)=1,
a stronger NECESSARY gate. It is not claimed sufficient.

The real north C60 primitive p has P_phi(p)=1; its original
double inverse symm(symm p) has P_phi=X^2 and no chosen seam.
We retain all original F54 two-Nat/two-category/Blocks and F55
Type witness histories and the positive/negative P77 class split.

An additional real typed P92B endomorphism-loop example exhibits
two proofs with identical N,S,W at the sample points 1,-1,2
but distinct depth polynomials; hence no selected P94A 4-cell
between them. This does NOT claim that such a pair is a local
original-to-phi seam counterexample.

Strict 空 authority, independent Kuu→Qi, append-only,
public root107, #1558 Draft/OPEN/unmerged, pinned Lean
v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry, admit, native_decide, Gray, global
GK5AY seam, GK5BA kit, unconditional P89 faithfulness or
all-P94A normalization.
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

/-- The complete depth-distribution generating polynomial in Z[X].
Each original F55 wrapper contributes 1, selected symm shifts its
inversion depth by multiplication by X, vertical/horizontal pasting
adds, and all contexts preserve the polynomial. This refines
GK5BB unsigned N, GK5BE signed S, and GK5BF weight W. -/
def NativeF55P92AssocComparison.gk5bgDepthPolynomial
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) : Polynomial Int := by
  induction f with
  | original old => exact 1
  | assocNaturality u v w => exact 0
  | refl r => exact 0
  | symm f ih => exact ih * Polynomial.X
  | trans f g ihf ihg => exact ihf + ihg
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- Genuine P92B vertical pasting adds the full polynomial,
avoiding dependent recursor unfolding in four-cell interchange. -/
theorem NativeF55P92AssocComparison.gk5bgTrans_poly
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5bgDepthPolynomial =
      f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial := rfl

/-- Genuine dependent P92B horizontal pasting adds generating
polynomials via the exact pre/post-context construction. -/
theorem NativeF55P92AssocComparison.gk5bgHorizontal_poly
    {n₁ n₁' m₁ m₁' n₂ n₂' m₂ m₂' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).gk5bgDepthPolynomial =
      f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial := rfl

/-- ALL SIXTEEN P93C true four-cell constructors preserve the
complete depth polynomial. The old P89 constructor has one
original wrapper at each endpoint, and interchange is an exact
identity in the commutative polynomial ring Int[X]. -/
theorem NativeF55P93AssocFourCell.gk5bgDepthPolynomial_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5bgDepthPolynomial = g.gk5bgDepthPolynomial := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Polynomial Int) + f.gk5bgDepthPolynomial = f.gk5bgDepthPolynomial
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5bgDepthPolynomial + (0 : Polynomial Int) = f.gk5bgDepthPolynomial
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial) +
        h.gk5bgDepthPolynomial =
        f.gk5bgDepthPolynomial + (g.gk5bgDepthPolynomial + h.gk5bgDepthPolynomial)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Polynomial Int => prior.gk5bgDepthPolynomial + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Polynomial Int => z + suffix.gk5bgDepthPolynomial) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5bgHorizontal_poly] using
        congrArg (fun z : Polynomial Int => z + other.gk5bgDepthPolynomial) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5bgHorizontal_poly] using
        congrArg (fun z : Polynomial Int => other.gk5bgDepthPolynomial + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5bgHorizontal_poly,
        NativeF55P92AssocComparison.gk5bgTrans_poly]
      ring

/-- ALL NINETEEN chosen P94A constructors preserve the complete
polynomial, including horizontalUnit and both contextUnit additions. -/
theorem NativeF55P94UnitFourCell.gk5bgDepthPolynomial_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    f.gk5bgDepthPolynomial = g.gk5bgDepthPolynomial := by
  induction w with
  | old w => exact w.gk5bgDepthPolynomial_sound
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Polynomial Int) + f.gk5bgDepthPolynomial = f.gk5bgDepthPolynomial
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5bgDepthPolynomial + (0 : Polynomial Int) = f.gk5bgDepthPolynomial
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial) +
        h.gk5bgDepthPolynomial =
        f.gk5bgDepthPolynomial + (g.gk5bgDepthPolynomial + h.gk5bgDepthPolynomial)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Polynomial Int => prior.gk5bgDepthPolynomial + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Polynomial Int => z + suffix.gk5bgDepthPolynomial) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5bgHorizontal_poly] using
        congrArg (fun z : Polynomial Int => z + other.gk5bgDepthPolynomial) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5bgHorizontal_poly] using
        congrArg (fun z : Polynomial Int => other.gk5bgDepthPolynomial + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5bgHorizontal_poly,
        NativeF55P92AssocComparison.gk5bgTrans_poly]
      ring
  | horizontalUnit u v =>
      change (0 : Polynomial Int) + 0 = 0
      ring
  | leftContextUnit route later => rfl
  | rightContextUnit earlier route => rfl



/-- An original whole F55 wrapper has constant polynomial one,
regardless of the original raw proof's internal constructor tree. -/
theorem nativeGK5BGRawOriginal_poly_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (NativeF55P92AssocComparison.original f).gk5bgDepthPolynomial = 1 := rfl

/-- Each *selected* P92B inverse shifts every original wrapper
by exactly one level of inversion depth. -/
theorem NativeF55P92AssocComparison.gk5bgSymm_poly
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    (NativeF55P92AssocComparison.symm f).gk5bgDepthPolynomial =
      f.gk5bgDepthPolynomial * Polynomial.X := rfl

/-- Genuine P92B polynomial P_f evaluated at +1 is the Nat
unsigned original-wrapper count GK5BB, cast to Int. -/
theorem NativeF55P92AssocComparison.gk5bgEval_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    f.gk5bgDepthPolynomial.eval (1 : Int) =
      (f.gk5bbOriginalCount : Int) := by
  induction f with
  | original old => change (1 : Polynomial Int).eval (1 : Int) = (1 : Int); simp
  | assocNaturality u v w =>
      change (0 : Polynomial Int).eval (1 : Int) = (0 : Int)
      simp
  | refl r => change (0 : Polynomial Int).eval (1 : Int) = (0 : Int); simp
  | symm f ih =>
      change (f.gk5bgDepthPolynomial * Polynomial.X).eval (1 : Int) =
        (f.gk5bbOriginalCount : Int)
      simpa only [Polynomial.eval_mul_X, mul_one] using ih
  | trans f g ihf ihg =>
      change (f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial).eval (1 : Int) =
        ((f.gk5bbOriginalCount + g.gk5bbOriginalCount : Nat) : Int)
      simpa only [Polynomial.eval_add, Nat.cast_add, ihf, ihg]
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- Evaluation at -1 recovers the signed ORIGINAL-wrapper
integer grade GK5BE, including real chosen inversions. -/
theorem NativeF55P92AssocComparison.gk5bgEval_neg_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    f.gk5bgDepthPolynomial.eval (-1 : Int) = f.gk5beSignedCount := by
  induction f with
  | original old => change (1 : Polynomial Int).eval (-1 : Int) = (1 : Int); simp
  | assocNaturality u v w =>
      change (0 : Polynomial Int).eval (-1 : Int) = (0 : Int)
      simp
  | refl r => change (0 : Polynomial Int).eval (-1 : Int) = (0 : Int); simp
  | symm f ih =>
      change (f.gk5bgDepthPolynomial * Polynomial.X).eval (-1 : Int) =
        - f.gk5beSignedCount
      simpa only [Polynomial.eval_mul_X, mul_neg_one] using congrArg Neg.neg ih
  | trans f g ihf ihg =>
      change (f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial).eval (-1 : Int) =
        f.gk5beSignedCount + g.gk5beSignedCount
      simpa only [Polynomial.eval_add, ihf, ihg]
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- Evaluation at +2 is exactly GK5BF inversion-depth Nat
weight, cast to Int. Thus all three established observations
are genuine specializations of one Polynomial Int. -/
theorem NativeF55P92AssocComparison.gk5bgEval_two
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    f.gk5bgDepthPolynomial.eval (2 : Int) =
      (f.gk5bfInverseDepthWeight : Int) := by
  induction f with
  | original old => change (1 : Polynomial Int).eval (2 : Int) = (1 : Int); simp
  | assocNaturality u v w =>
      change (0 : Polynomial Int).eval (2 : Int) = (0 : Int)
      simp
  | refl r => change (0 : Polynomial Int).eval (2 : Int) = (0 : Int); simp
  | symm f ih =>
      change (f.gk5bgDepthPolynomial * Polynomial.X).eval (2 : Int) =
        ((2 * f.gk5bfInverseDepthWeight : Nat) : Int)
      simp only [Polynomial.eval_mul_X, ih, Nat.cast_mul, Nat.cast_ofNat]
      ring
  | trans f g ihf ihg =>
      change (f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial).eval (2 : Int) =
        ((f.gk5bfInverseDepthWeight + g.gk5bfInverseDepthWeight : Nat) : Int)
      simpa only [Polynomial.eval_add, Nat.cast_add, ihf, ihg]
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- A genuine selected P94A original-to-phi local seam forces
equality of WHOLE polynomials, so the structural phi must have
the constant original-wrapper polynomial one. -/
theorem nativeGK5BGLocalSeam_requires_poly_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (seam : nativeGK5AZSeamAt f) :
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial = 1 := by
  have h := seam.gk5bgDepthPolynomial_sound
  change (1 : Polynomial Int) =
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial at h
  exact h.symm

/-- Full-polynomial obstruction: numerical evaluations need
not be separately recomputed when the actual P94A witness
would force equality to the raw original polynomial. -/
theorem nativeGK5BGNoSeam_if_poly_ne_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (h : (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial ≠ 1) :
    ¬ Nonempty (nativeGK5AZSeamAt f) := by
  rintro ⟨seam⟩
  exact h (nativeGK5BGLocalSeam_requires_poly_one f seam)

/-- An ACTUAL P77 original source four-cell is transported
by GK5AJ to a genuine P93C proof on structural-phi endpoints.
Its entire polynomial therefore agrees, not only N,S,W. -/
theorem nativeGK5BGPoly_sound_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) :
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial =
      (nativeGK5AIOriginalToP92Structural g).gk5bgDepthPolynomial :=
  (nativeGK5AJOriginalFourToP93 first last w).gk5bgDepthPolynomial_sound

/-- Unlike GK5BF's Prop-valued necessary gates, this is an
actual Polynomial Int-valued quotient lift of the full invariant
across the exact genuine P77 source four-cell relation. -/
def nativeGK5BGPolyOnP77Class
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55RawVerticalFourClasses first last r s → Polynomial Int :=
  _root_.Quotient.lift
    (fun f => (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact nativeGK5BGPoly_sound_P77 w)

/-- The descended polynomial exactly reconstructs the genuine
structural translation's value at every original representative. -/
theorem nativeGK5BGPolyOnP77Class_mk
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5BGPolyOnP77Class first last r s
      (nativeF55RawVerticalFourClass first last f) =
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial :=
  rfl

/-- Primitive and double-inverse original F55 proofs inhabit
the SAME genuine north C60 long→short F54 Hom fiber. -/
private def nativeGK5BGNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def nativeGK5BGNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- A genuine primitive pentagon produces constant polynomial one. -/
theorem nativeGK5BGNorthPrimitive_phi_poly :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial = 1 := rfl

/-- The actual original double inverse has polynomial X^2
under recursive structural phi, even though GK5BB N=1 and
GK5BE S=1. The raw whole original wrapper has polynomial 1. -/
theorem nativeGK5BGNorthDoubleInverse_phi_poly :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5bgDepthPolynomial =
      (Polynomial.X : Polynomial Int) ^ 2 := by
  change ((1 : Polynomial Int) * Polynomial.X) * Polynomial.X =
    Polynomial.X ^ 2
  ring

/-- The two real SOURCE-P77 quotient classes have different
full polynomial values, so the polynomial confirms their
previously proved structural inequivalence in one Hom fiber. -/
theorem nativeGK5BGNorthPrimitive_ne_doubleInverse_poly_class :
    nativeGK5BGPolyOnP77Class
      nativeGK5BGNorthFirst nativeGK5BGNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        nativeGK5BGNorthFirst nativeGK5BGNorthLast
        nativeGK5AGNorthOriginalCell) ≠
    nativeGK5BGPolyOnP77Class
      nativeGK5BGNorthFirst nativeGK5BGNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        nativeGK5BGNorthFirst nativeGK5BGNorthLast
        nativeGK5BFNorthDoubleInverse) := by
  intro h
  have hw := congrArg (Polynomial.eval (2 : Int)) h
  simp only [nativeGK5BGPolyOnP77Class_mk,
    nativeGK5BGNorthPrimitive_phi_poly,
    nativeGK5BGNorthDoubleInverse_phi_poly] at hw
  norm_num at hw

/-- This polynomial obstruction recovers the double-inverse
negative local-seam class without needing an assumed P94A
normal form or hypothetical universal constructor shell. -/
theorem nativeGK5BGNorthDoubleInverse_no_seam :
    ¬ Nonempty (nativeGK5AZSeamAt nativeGK5BFNorthDoubleInverse) := by
  apply nativeGK5BGNoSeam_if_poly_ne_one
  intro h
  have hw := congrArg (Polynomial.eval (2 : Int)) h
  rw [nativeGK5BGNorthDoubleInverse_phi_poly] at hw
  norm_num at hw

/-- A true original P92B endomorphism-loop primitive is used
only to test completeness of the three scalar observations,
not to postulate an uninhabited F55 original identity seam. -/
private def nativeGK5BGLoop
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P92AssocComparison p r r :=
  .original (.ident r)

/-- Two fully typed P92B endomorphisms with distributions
X^3+2 and 2X^2+X, respectively. Both are genuine selected
three-proofs made solely from a real original F55 identity
wrapper, selected symm and trans. -/
def nativeGK5BGTripleLeft
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P92AssocComparison p r r :=
  .trans
    (.symm (.symm (.symm (nativeGK5BGLoop r))))
    (.trans (nativeGK5BGLoop r) (nativeGK5BGLoop r))

def nativeGK5BGTripleRight
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P92AssocComparison p r r :=
  .trans
    (.symm (.symm (nativeGK5BGLoop r)))
    (.trans (.symm (.symm (nativeGK5BGLoop r)))
      (.symm (nativeGK5BGLoop r)))

/-- The two polynomials are distinct, although their values
at all three sample points 1,-1,2 coincide. -/
theorem nativeGK5BGTriple_polynomials
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (nativeGK5BGTripleLeft r).gk5bgDepthPolynomial =
      (Polynomial.X : Polynomial Int) ^ 3 + 2 ∧
    (nativeGK5BGTripleRight r).gk5bgDepthPolynomial =
      2 * (Polynomial.X : Polynomial Int) ^ 2 + Polynomial.X := by
  constructor
  · change (((1 : Polynomial Int) * Polynomial.X * Polynomial.X *
      Polynomial.X) + (1 + 1) = Polynomial.X ^ 3 + 2
    ring
  · change
      (1 : Polynomial Int) * Polynomial.X * Polynomial.X +
        ((1 : Polynomial Int) * Polynomial.X * Polynomial.X +
          (1 : Polynomial Int) * Polynomial.X) =
        2 * Polynomial.X ^ 2 + Polynomial.X
    ring

/-- The three old observations cannot distinguish these two
actual P92B endomorphisms, even though their polynomials differ. -/
theorem nativeGK5BGTriple_equal_three_scalars
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (nativeGK5BGTripleLeft r).gk5bbOriginalCount =
      (nativeGK5BGTripleRight r).gk5bbOriginalCount ∧
    (nativeGK5BGTripleLeft r).gk5beSignedCount =
      (nativeGK5BGTripleRight r).gk5beSignedCount ∧
    (nativeGK5BGTripleLeft r).gk5bfInverseDepthWeight =
      (nativeGK5BGTripleRight r).gk5bfInverseDepthWeight :=
  ⟨rfl, rfl, rfl⟩

/-- Full polynomial distinguishes the two real typed P92B
loops by evaluation at zero: left 2, right 0. -/
theorem nativeGK5BGTriple_poly_ne
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (nativeGK5BGTripleLeft r).gk5bgDepthPolynomial ≠
      (nativeGK5BGTripleRight r).gk5bgDepthPolynomial := by
  intro h
  have hz := congrArg (Polynomial.eval (0 : Int)) h
  obtain ⟨hleft, hright⟩ := nativeGK5BGTriple_polynomials r
  rw [hleft, hright] at hz
  norm_num at hz

/-- Therefore no chosen P94A four-cell compares this pair,
although all three previously known scalars N,S,W agree.
This does not create a false original-to-phi seam claim. -/
theorem nativeGK5BGTriple_no_P94
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeF55P94UnitFourCell
      (nativeGK5BGTripleLeft r) (nativeGK5BGTripleRight r)) := by
  rintro ⟨w⟩
  exact nativeGK5BGTriple_poly_ne r w.gk5bgDepthPolynomial_sound

#print axioms NativeF55P92AssocComparison.gk5bgDepthPolynomial
#print axioms NativeF55P92AssocComparison.gk5bgTrans_poly
#print axioms NativeF55P92AssocComparison.gk5bgHorizontal_poly
#print axioms NativeF55P93AssocFourCell.gk5bgDepthPolynomial_sound
#print axioms NativeF55P94UnitFourCell.gk5bgDepthPolynomial_sound
#print axioms nativeGK5BGRawOriginal_poly_one
#print axioms NativeF55P92AssocComparison.gk5bgSymm_poly
#print axioms NativeF55P92AssocComparison.gk5bgEval_one
#print axioms NativeF55P92AssocComparison.gk5bgEval_neg_one
#print axioms NativeF55P92AssocComparison.gk5bgEval_two
#print axioms nativeGK5BGLocalSeam_requires_poly_one
#print axioms nativeGK5BGNoSeam_if_poly_ne_one
#print axioms nativeGK5BGPoly_sound_P77
#print axioms nativeGK5BGPolyOnP77Class
#print axioms nativeGK5BGPolyOnP77Class_mk
#print axioms nativeGK5BGNorthPrimitive_phi_poly
#print axioms nativeGK5BGNorthDoubleInverse_phi_poly
#print axioms nativeGK5BGNorthPrimitive_ne_doubleInverse_poly_class
#print axioms nativeGK5BGNorthDoubleInverse_no_seam
#print axioms nativeGK5BGTripleLeft
#print axioms nativeGK5BGTripleRight
#print axioms nativeGK5BGTriple_polynomials
#print axioms nativeGK5BGTriple_equal_three_scalars
#print axioms nativeGK5BGTriple_poly_ne
#print axioms nativeGK5BGTriple_no_P94

end
end Kuu.F112.Physical
