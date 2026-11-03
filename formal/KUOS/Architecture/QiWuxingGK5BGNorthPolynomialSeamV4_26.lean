import KUOS.Architecture.QiWuxingGK5BFNorthDoubleInverseClassV4_25
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BGDepthGeneratingPolynomial
import Mathlib.Tactic

/-!
Qi v4.26 / F112-P94D3GK5BG — actual NORTH C60 source-Hom
polynomial separation, plus a genuine chosen P92B loop pair
whose three old scalar invariants N,S,W agree but whose full
inversion-depth polynomials differ and forbid a P94A four-cell.

The independent Kuu GK5BG has proved that full P_f(X) is
P93C-16/P94A-19 Type-valued four-cell invariant, and descends
as an actual Polynomial Int value through original P77 classes.
Qi only IMPORTS it; the independent proof authority is not
inverted into a Qi physical gauge shadow.

At TRUE north C60 F54 long→short Hom, the positive original
pentagon primitive has P_phi=1 and a local P94A reflexive seam.
The original double inverse, including its genuine F55 right
identity extension, has P_phi=X^2 and NO local seam. These
have the same F54 dependent endpoints and GK5BB/GK5BE
necessary counts N=S=1. The P77 right-unit proof transports
the entire polynomial value without pretending the original
3-proof terms are syntactically equal.

At a TRUE north F54 short route, make TWO genuine P92B
endo-three-proofs from an ORIGINAL F55 ident wrapper:
  A(X)=X^3+2, B(X)=2X^2+X.
They share GK5BB N=3, GK5BE S=1, GK5BF W=10, but the
whole polynomials differ (already at X=0); a selected P94A
four-cell is therefore impossible. The selected P92B endo
loops are NOT misrepresented as original-to-phi seams.

Physical north fifth-Dart closure and the conditional old
P89 BadPair class-map reflection stay separate. No global
GK5AY seam, GK5BA constructor kit, all-P94A normalization,
unconditional P89 faithfulness/nonfaithfulness or Gray.

Strict 空 authority, independent Kuu→Qi, original F54 two
Nat indices/two categories/Blocks Type witness histories,
public root107, protected #1558 Draft/OPEN. Pinned Lean
v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, no new axioms/sorry/admit/native_decide.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

private def fivefoldGK5BGNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BGNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- At a genuine north C60 pentagon source primitive,
the structural phi full depth polynomial is the constant one. -/
theorem fivefoldGK5BGNorthPrimitive_full_poly :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial = 1 :=
  nativeGK5BGNorthPrimitive_phi_poly

/-- At EXACTLY the same original north F54 Hom, the source
double inverse has the nonconstant full polynomial X squared. -/
theorem fivefoldGK5BGNorthDoubleInverse_full_poly :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5bgDepthPolynomial =
      (Polynomial.X : Polynomial Int) ^ 2 :=
  nativeGK5BGNorthDoubleInverse_phi_poly

/-- Genuine original P77 right-unit witness transports the
WHOLE polynomial to the actual original double-inverse
right-unit source; no synthetic trans split shell is used. -/
theorem fivefoldGK5BGNorthDoubleInverseUnit_full_poly :
    (nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial =
      (Polynomial.X : Polynomial Int) ^ 2 := by
  have h := nativeGK5BGPoly_sound_P77
    fivefoldGK5BFNorthDoubleInverseRightUnitWord.toP77
  exact h.symm.trans nativeGK5BGNorthDoubleInverse_phi_poly

/-- P77 quotient is a TRUE source proof-class quotient, and
the entire polynomial is well-defined on each representative
of the source original F55 double-inverse-unit class. -/
theorem fivefoldGK5BGNorthDoubleInverseUnit_P77_poly_class :
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BGNorthFirst fivefoldGK5BGNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BGNorthFirst fivefoldGK5BGNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) =
      (Polynomial.X : Polynomial Int) ^ 2 := by
  simpa only [nativeGK5BGPolyOnP77Class_mk] using
    fivefoldGK5BGNorthDoubleInverseUnit_full_poly

/-- Same true dependent original F54 Hom, but local direct
selected P94A seam exists ONLY at the primitive-positive
class, not at the double-inverse-unit negative class. -/
theorem fivefoldGK5BGNorthSameFiber_local_split :
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) ∧
    ((nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial = 1) ∧
    ((nativeGK5AIOriginalToP92Structural
      fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial =
        (Polynomial.X : Polynomial Int) ^ 2) ∧
    ¬ Nonempty (NativeGK5AYOriginalPhiSeam
      fivefoldGK5BGNorthFirst fivefoldGK5BGNorthLast) :=
  ⟨⟨.refl _⟩, fivefoldGK5BFNorthDoubleInverseUnit_no_seam,
   fivefoldGK5BGNorthPrimitive_full_poly,
   fivefoldGK5BGNorthDoubleInverseUnit_full_poly,
   nativeGK5BBNorthNoGlobalSeam⟩

/-- Actual North source P77 quotient values differ at X=2;
the two genuine local source classes therefore remain
distinct, not identified by a scalar or raw syntax equality. -/
theorem fivefoldGK5BGNorthSameFiber_poly_class_ne :
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BGNorthFirst fivefoldGK5BGNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BGNorthFirst fivefoldGK5BGNorthLast
        nativeGK5AGNorthOriginalCell) ≠
    nativeGK5BGPolyOnP77Class
      fivefoldGK5BGNorthFirst fivefoldGK5BGNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BGNorthFirst fivefoldGK5BGNorthLast
        fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  intro h
  have h' := congrArg (Polynomial.eval (2 : Int)) h
  simp only [nativeGK5BGPolyOnP77Class_mk] at h'
  rw [NativeF55P92AssocComparison.gk5bgEval_two,
    NativeF55P92AssocComparison.gk5bgEval_two] at h'
  change (1 : Int) = 4 at h'
  omega

/-- A TRUE original NORTH F55 identity wrapper at the
north pentagon SHORT route underlies selected P92B endo
three-proofs with full finite proof terms, not numeric shadows. -/
def fivefoldGK5BGNorthTripleLoopA :
    NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonShort northNativeF45PentagonShort :=
  nativeGK5BGTripleLeft northNativeF45PentagonShort

def fivefoldGK5BGNorthTripleLoopB :
    NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonShort northNativeF45PentagonShort :=
  nativeGK5BGTripleRight northNativeF45PentagonShort

/-- Selected P92B genuine North loop polynomials are two
different integer polynomials in the very same source slot. -/
theorem fivefoldGK5BGNorthTripleLoop_polynomials :
    fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial =
      (Polynomial.X : Polynomial Int) ^ 3 + 2 ∧
    fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial =
      2 * (Polynomial.X : Polynomial Int) ^ 2 + Polynomial.X :=
  nativeGK5BGTriple_polynomials northNativeF45PentagonShort

/-- The old three scalar observations give EXACTLY the
same numbers (N,S,W) for both actual selected North loops. -/
theorem fivefoldGK5BGNorthTripleLoop_equal_old_grades :
    fivefoldGK5BGNorthTripleLoopA.gk5bbOriginalCount =
      fivefoldGK5BGNorthTripleLoopB.gk5bbOriginalCount ∧
    fivefoldGK5BGNorthTripleLoopA.gk5beSignedCount =
      fivefoldGK5BGNorthTripleLoopB.gk5beSignedCount ∧
    fivefoldGK5BGNorthTripleLoopA.gk5bfInverseDepthWeight =
      fivefoldGK5BGNorthTripleLoopB.gk5bfInverseDepthWeight :=
  nativeGK5BGTriple_equal_three_scalars northNativeF45PentagonShort

/-- Nevertheless the FULL polynomial is different, and no
genuine P94A selected four-cell bridges these two real
Type-valued North P92B endomorphism 3-proofs. -/
theorem fivefoldGK5BGNorthTripleLoop_no_P94 :
    ¬ Nonempty (NativeF55P94UnitFourCell
      fivefoldGK5BGNorthTripleLoopA
      fivefoldGK5BGNorthTripleLoopB) :=
  nativeGK5BGTriple_no_P94 northNativeF45PentagonShort

/-- Both the genuine North inversion polynomial obstruction
and physical fifth-around gauge closure hold, while original
P89 source-map reflection is ONLY the inherited conditional iff. -/
theorem fivefoldGK5BGNorthPhysicalPolynomialAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (¬ Nonempty (NativeF55P94UnitFourCell
      fivefoldGK5BGNorthTripleLoopA
      fivefoldGK5BGNorthTripleLoopB)) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) := by
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, _, _⟩
  exact ⟨fivefoldGK5BGNorthTripleLoop_no_P94,
    hClosed, hIff⟩

#print axioms fivefoldGK5BGNorthPrimitive_full_poly
#print axioms fivefoldGK5BGNorthDoubleInverse_full_poly
#print axioms fivefoldGK5BGNorthDoubleInverseUnit_full_poly
#print axioms fivefoldGK5BGNorthDoubleInverseUnit_P77_poly_class
#print axioms fivefoldGK5BGNorthSameFiber_local_split
#print axioms fivefoldGK5BGNorthSameFiber_poly_class_ne
#print axioms fivefoldGK5BGNorthTripleLoopA
#print axioms fivefoldGK5BGNorthTripleLoopB
#print axioms fivefoldGK5BGNorthTripleLoop_polynomials
#print axioms fivefoldGK5BGNorthTripleLoop_equal_old_grades
#print axioms fivefoldGK5BGNorthTripleLoop_no_P94
#print axioms fivefoldGK5BGNorthPhysicalPolynomialAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified
