import KUOS.Architecture.QiWuxingGK5BXNorthCRTTowerNaturalityV4_42
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BYIntPolynomialCRTNaturality
import Mathlib.Tactic

/-!
Qi v4.43 — TRUE NORTH C60 ORIGINAL SIGNED INTEGER
POLYNOMIAL EVALUATION AND COMPLETE FINITE CRT NATURALITY.

Independent GK5BY formally proves for ALL genuine
Polynomial Int, including negative coefficients, that
polynomial evaluation is a RingHom both in the global
ZMod L and the compatible-local ZMod subring; it is
natural under arbitrary finite-cover RingHom restriction,
the actual full noncoprime CRT RingEquiv, and all finite
three-cover restriction towers, including ZMod 0 = Int.

Here the input point is the SAME actual original SIGNED
GK5BQ cleared numerator, not a new F55 Type source and
not a natAbs proxy. Evaluate any additional original Int
polynomial at that genuine signed integer; prove its value
maps into all exact original CRT local coordinates and
is natural under one- or two-stage cover restrictions.
Additive and multiplicative polynomial operations are
preserved as true ring equalities at both levels.

For the two actual north original F55 structural sources
(primitive P=1 and double-inverse/right-unit P=X²),
the same arithmetic outer-polynomial CRT tower is coherent.
Under the established explicit factorial-LCM certificate
the existing numeric CRT-zero results remain true, but
the original-phi structural Type-valued seam is present
for primitive and absent for double inverse. No inference
from arithmetic compatibility to missing F55 Type history.

Strict 空, independent Kuu→Qi; original F54 two Nat/two
categories/Blocks and original F55 Type source history
unchanged; genuine north fifth-around physical C60 gauge
and conditional P89 BadPair reflection remain separate.
Public root107, protected #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2/mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axiom/sorry/admit/native_decide; no P77 equality,
P94A 4-cells, unconditional P89, universal GK5AY seam,
W=1→seam, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Evaluate a genuine Int polynomial at the ORIGINAL
SIGNED GK5BQ source numerator in the true global CRT ring. -/
def fivefoldGK5BYNorthOriginalPolyGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    ZMod (nativeGK5BUFiniteModulus s moduli) :=
  nativeGK5BYGlobalIntPolyEvalHom s moduli
    (fivefoldGK5BWNorthSignedGlobal s moduli d j values) P

/-- Evaluate the same genuine integer polynomial at the
ORIGINAL signed numerator's compatible local CRT ring family. -/
def fivefoldGK5BYNorthOriginalPolyLocals
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    nativeGK5BWCompatibleSubring s moduli :=
  nativeGK5BYCompatibleIntPolyEvalHom s moduli
    (fivefoldGK5BWNorthSignedRingLocals s moduli d j values) P

/-- Authentic signed integer polynomial evaluation BEFORE
modular reduction agrees with global ZMod CRT evaluation.
This is not a norm-losing natAbs representation. -/
theorem fivefoldGK5BYNorthOriginalPoly_signedGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values P =
      ((P.eval (nativeGK5BQClearedNumerator d j values) : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5BYIntPolynomial_signedGlobal s moduli P
    (nativeGK5BQClearedNumerator d j values)

/-- The TRUE original signed global polynomial value
agrees with its entire genuine compatible LOCAL CRT family
under the already-proved GK5BW RingEquiv. -/
theorem fivefoldGK5BYNorthOriginalPoly_crtAgreement
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values P) =
    fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values P :=
  nativeGK5BYCRTEvaluation_apply s moduli
    (fivefoldGK5BWNorthSignedGlobal s moduli d j values) P

/-- Additive operations on original Int polynomials are
preserved in the TRUE global north CRT residue ring. -/
theorem fivefoldGK5BYNorthOriginalPolyGlobal_add
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int)
    (P Q : Polynomial Int) :
    fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values (P + Q) =
      fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values P +
        fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values Q :=
  nativeGK5BYGlobalIntPolyEval_add s moduli
    (fivefoldGK5BWNorthSignedGlobal s moduli d j values) P Q

/-- Multiplicative polynomial operations are preserved
in the TRUE global north CRT residue ring. -/
theorem fivefoldGK5BYNorthOriginalPolyGlobal_mul
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int)
    (P Q : Polynomial Int) :
    fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values (P * Q) =
      fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values P *
        fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values Q :=
  nativeGK5BYGlobalIntPolyEval_mul s moduli
    (fivefoldGK5BWNorthSignedGlobal s moduli d j values) P Q

/-- Original compatible local CRT polynomial values
preserve additions as equality IN THE ACTUAL SUBRING. -/
theorem fivefoldGK5BYNorthOriginalPolyLocals_add
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int)
    (P Q : Polynomial Int) :
    fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values (P + Q) =
      fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values P +
        fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values Q :=
  nativeGK5BYCompatibleIntPolyEval_add s moduli
    (fivefoldGK5BWNorthSignedRingLocals s moduli d j values) P Q

/-- Original compatible local CRT polynomial values
preserve products as equality IN THE ACTUAL SUBRING. -/
theorem fivefoldGK5BYNorthOriginalPolyLocals_mul
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int)
    (P Q : Polynomial Int) :
    fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values (P * Q) =
      fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values P *
        fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values Q :=
  nativeGK5BYCompatibleIntPolyEval_mul s moduli
    (fivefoldGK5BWNorthSignedRingLocals s moduli d j values) P Q

/-- Restrict the original signed integer-polynomial
GLOBAL value to ANY finite subcover: exactly the direct
polynomial value of the SAME original numerator there. -/
theorem fivefoldGK5BYNorthOriginalPolyGlobal_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    nativeGK5BXGlobalRestrictHom s t moduli h
      (fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values P) =
    fivefoldGK5BYNorthOriginalPolyGlobal t moduli d j values P := by
  calc
    _ = nativeGK5BYGlobalIntPolyEvalHom t moduli
          (nativeGK5BXGlobalRestrictHom s t moduli h
            (fivefoldGK5BWNorthSignedGlobal s moduli d j values)) P :=
      nativeGK5BYGlobalIntPolyEval_restrict s t moduli h
        (fivefoldGK5BWNorthSignedGlobal s moduli d j values) P
    _ = _ := by
      rw [fivefoldGK5BXNorthSignedGlobal_restrict s t moduli h d j values]
      rfl

/-- Restrict the original signed polynomial's entire
compatible LOCAL family: it agrees with the SAME value
directly calculated on the smaller original finite cover. -/
theorem fivefoldGK5BYNorthOriginalPolyLocals_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli h
      (fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values P) =
    fivefoldGK5BYNorthOriginalPolyLocals t moduli d j values P := by
  have H := congrArg
    (fun f : Polynomial Int →+*
      nativeGK5BWCompatibleSubring t moduli => f P)
    (nativeGK5BYCompatibleIntPolyEval_restrictHom s t moduli h
      (fivefoldGK5BWNorthSignedRingLocals s moduli d j values))
  calc
    _ = nativeGK5BYCompatibleIntPolyEvalHom t moduli
          (nativeGK5BXCompatibleRestrictHom s t moduli h
            (fivefoldGK5BWNorthSignedRingLocals s moduli d j values)) P :=
      by simpa only [RingHom.comp_apply] using H
    _ = _ := by
      rw [fivefoldGK5BXNorthSignedLocals_restrict s t moduli h d j values]
      rfl

/-- TWO successive finite-cover restrictions of a genuine
SIGNED original integer-polynomial value in the global ZMod
ring equal direct evaluation at the SAME source on the
smallest cover, with NO degree or factorial assumption. -/
theorem fivefoldGK5BYNorthOriginalPolyGlobal_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    nativeGK5BXGlobalRestrictHom t u moduli k
      (nativeGK5BXGlobalRestrictHom s t moduli h
        (fivefoldGK5BYNorthOriginalPolyGlobal s moduli d j values P)) =
    fivefoldGK5BYNorthOriginalPolyGlobal u moduli d j values P := by
  calc
    _ = nativeGK5BXGlobalRestrictHom t u moduli k
          (fivefoldGK5BYNorthOriginalPolyGlobal t moduli d j values P) :=
        congrArg (nativeGK5BXGlobalRestrictHom t u moduli k)
          (fivefoldGK5BYNorthOriginalPolyGlobal_restrict
            s t moduli h d j values P)
    _ = _ := fivefoldGK5BYNorthOriginalPolyGlobal_restrict
      t u moduli k d j values P

/-- TWO successive finite-cover restrictions of a genuine
SIGNED original integer-polynomial compatible LOCAL family
equal the direct true value at the smallest cover. -/
theorem fivefoldGK5BYNorthOriginalPolyLocals_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (d j : Nat) (values : Nat → Int) (P : Polynomial Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BYNorthOriginalPolyLocals s moduli d j values P)) =
    fivefoldGK5BYNorthOriginalPolyLocals u moduli d j values P := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u moduli k
          (fivefoldGK5BYNorthOriginalPolyLocals t moduli d j values P) :=
        congrArg (nativeGK5BXCompatibleRestrictHom t u moduli k)
          (fivefoldGK5BYNorthOriginalPolyLocals_restrict
            s t moduli h d j values P)
    _ = _ := fivefoldGK5BYNorthOriginalPolyLocals_restrict
      t u moduli k d j values P

/-- Original true north primitive F55 polynomial VALUES
are used as values, not reconstructed Type witnesses. -/
private abbrev fivefoldGK5BYNorthPrimitiveInnerValues (n : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (n : Int)

/-- Distinct genuine double-inverse/right-unit original
F55 polynomial VALUES, preserving their original Type. -/
private abbrev fivefoldGK5BYNorthDoubleInnerValues (n : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval (n : Int)

/-- Both actual north F55 sources have coherent two-stage
outer integer-polynomial evaluations in the TRUE local CRT
rings, and both still admit their existing conditional
finite CRT zero certificates, yet ORIGINAL structural seam
verdicts remain OPPOSITE. This is a typed obstruction to
identifying arithmetic and structural gluing. -/
theorem fivefoldGK5BYNorthBothOuterPolynomialTowerButOppositeSeams
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (d j : Nat) (hbound : 2 ≤ d)
    (hL : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (Q : Polynomial Int)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BYNorthOriginalPolyLocals
          s moduli d j fivefoldGK5BYNorthPrimitiveInnerValues Q)) =
      fivefoldGK5BYNorthOriginalPolyLocals
        u moduli d j fivefoldGK5BYNorthPrimitiveInnerValues Q) ∧
    (nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BYNorthOriginalPolyLocals
          s moduli d j fivefoldGK5BYNorthDoubleInnerValues Q)) =
      fivefoldGK5BYNorthOriginalPolyLocals
        u moduli d j fivefoldGK5BYNorthDoubleInnerValues Q) ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨_, _, hz1, hz2, hyes, hno⟩ :=
    fivefoldGK5BXNorthOriginalBothTowerButOppositeSeams
      s t u moduli h k d j hbound hL frame i
  exact ⟨fivefoldGK5BYNorthOriginalPolyLocals_tower
      s t u moduli h k d j fivefoldGK5BYNorthPrimitiveInnerValues Q,
    fivefoldGK5BYNorthOriginalPolyLocals_tower
      s t u moduli h k d j fivefoldGK5BYNorthDoubleInnerValues Q,
    hz1, hz2, hyes, hno⟩

#print axioms fivefoldGK5BYNorthOriginalPoly_signedGlobal
#print axioms fivefoldGK5BYNorthOriginalPoly_crtAgreement
#print axioms fivefoldGK5BYNorthOriginalPolyGlobal_add
#print axioms fivefoldGK5BYNorthOriginalPolyGlobal_mul
#print axioms fivefoldGK5BYNorthOriginalPolyLocals_add
#print axioms fivefoldGK5BYNorthOriginalPolyLocals_mul
#print axioms fivefoldGK5BYNorthOriginalPolyGlobal_restrict
#print axioms fivefoldGK5BYNorthOriginalPolyLocals_restrict
#print axioms fivefoldGK5BYNorthOriginalPolyGlobal_tower
#print axioms fivefoldGK5BYNorthOriginalPolyLocals_tower
#print axioms fivefoldGK5BYNorthBothOuterPolynomialTowerButOppositeSeams

end
end KUOS.Architecture.WuxingPentagonUnified
