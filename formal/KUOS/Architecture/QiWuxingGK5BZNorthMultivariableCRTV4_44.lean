import KUOS.Architecture.QiWuxingGK5BYNorthIntPolynomialCRTV4_43
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BZMultivariableCRTNaturality
import Mathlib.Tactic

/-!
Qi v4.44 — ORIGINAL NORTH C60 SIGNED MULTIVARIABLE INTEGER
POLYNOMIAL CRT DESCENT AND THREE-COVER COHERENCE.

Independent GK5BZ now formally verifies TRUE finite CRT
RingEquiv naturality for actual MvPolynomial σ Int at any
variable type σ, in particular Fin n, including negative
coefficients, zero moduli, overlapping moduli and empty covers.

For TRUE original north C60 data, we feed a FINITE FAMILY
of the SAME original GK5BQ signed integer numerator VALUES
into each actual variable. We do NOT invent a new F55 Type
source or use a natAbs proxy. All integer polynomial
evaluations commute with the true global ZMod L quotient,
the genuine compatible-local ZMod SUBRING, additions,
multiplications and one-/two-stage finite-cover restrictions.

Two distinct ACTUAL original F55 Type sources are retained:
primitive P=1 and genuine double inverse plus right F55 unit
P=X². For either source all finite multivariable numeric
polynomial evaluations obey the same coherent CRT towers;
existing arithmetic factorial-LCM zero certificates descend
to subcovers. Yet the original-phi structural seam EXISTS
for primitive and DOES NOT EXIST for double inverse.
Numeric polynomial gluing never reconstructs original
F55 Type witnesses, P77 class equality, P94A four-cells,
unconditional P89 reflection, universal GK5AY seam or
W=1→seam. The north fifth-around physical gauge and
conditional P89 BadPair boundary remain distinct authorities.

Strict 空; independent Kuu→Qi, true original F54 two Nat,
two categories/Blocks and F55 Type histories; root107.
Protected PR #1558 Draft/open/unmerged. Pinned Lean
v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only new module and public aggregate import.
No axiom/sorry/admit/native_decide, Gray or GK5BA kit.
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

/-- A true FINITE family of ORIGINAL signed GK5BQ source
integer numerators, indexed by actual multivariable sites. -/
def fivefoldGK5BZNorthSignedCoordinates
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int) :
    Fin n → Int :=
  fun v => nativeGK5BQClearedNumerator d (indices v) values

/-- One coordinate is literally the same original signed
integer numerator, not a new F55 Type or natAbs value. -/
theorem fivefoldGK5BZNorthSignedCoordinates_apply
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (v : Fin n) :
    fivefoldGK5BZNorthSignedCoordinates n d indices values v =
      nativeGK5BQClearedNumerator d (indices v) values :=
  rfl

/-- The genuine global ZMod evaluation of an ACTUAL finite
multivariable integer polynomial at original signed north
C60 GK5BQ numerator values. -/
def fivefoldGK5BZNorthGlobalMvEval
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    ZMod (nativeGK5BUFiniteModulus s moduli) :=
  nativeGK5BZGlobalMvEvalHom s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- The same TRUE finite multivariable polynomial observed
in the original compatible-local dependent-product Subring,
via the genuine independent CRT RingEquiv on each variable. -/
def fivefoldGK5BZNorthLocalMvEval
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    nativeGK5BWCompatibleSubring s moduli :=
  nativeGK5BZCompatibleMvEvalHom s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- Evaluate the ORIGINAL signed finite integer vector
before reduction, or evaluate its residue vector in the
TRUE global finite CRT quotient: results coincide. -/
theorem fivefoldGK5BZNorthMv_signedGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values Q =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
        (fivefoldGK5BZNorthSignedCoordinates n d indices values) Q : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5BZFinSignedMvEval_global s moduli n
    (fivefoldGK5BZNorthSignedCoordinates n d indices values) Q

/-- The GK5BW CRT RingEquiv sends the exact original
global finite multivariable polynomial evaluation to the
same evaluation in its true compatible-local Subring. -/
theorem fivefoldGK5BZNorthMv_crtAgreement
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values Q) =
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values Q :=
  nativeGK5BZFinVariableCRT_natural s moduli n
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- Addition of TRUE finite multivariable integer
polynomials is preserved at original global north C60 data. -/
theorem fivefoldGK5BZNorthMvGlobal_add
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q R : MvPolynomial (Fin n) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values (Q + R) =
      fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values Q +
      fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values R :=
  nativeGK5BZGlobalMvEval_add s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) Q R

/-- Multiplication of genuine finite multivariable
integer polynomials is preserved at original global data. -/
theorem fivefoldGK5BZNorthMvGlobal_mul
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q R : MvPolynomial (Fin n) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values (Q * R) =
      fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values Q *
      fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values R :=
  nativeGK5BZGlobalMvEval_mul s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) Q R

/-- True compatible-local north multivariable evaluation
preserves addition in the actual ZMod product Subring. -/
theorem fivefoldGK5BZNorthMvLocal_add
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q R : MvPolynomial (Fin n) Int) :
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values (Q + R) =
      fivefoldGK5BZNorthLocalMvEval s moduli n d indices values Q +
      fivefoldGK5BZNorthLocalMvEval s moduli n d indices values R :=
  nativeGK5BZCompatibleMvEval_add s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) Q R

/-- True compatible-local north multivariable evaluation
preserves multiplication in the actual ZMod Subring. -/
theorem fivefoldGK5BZNorthMvLocal_mul
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q R : MvPolynomial (Fin n) Int) :
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values (Q * R) =
      fivefoldGK5BZNorthLocalMvEval s moduli n d indices values Q *
      fivefoldGK5BZNorthLocalMvEval s moduli n d indices values R :=
  nativeGK5BZCompatibleMvEval_mul s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) Q R

/-- The finite original signed multivariable polynomial
GLOBAL value is stable under ANY true finite-cover
restriction. No factorial or polynomial degree assumption. -/
theorem fivefoldGK5BZNorthMvGlobal_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (n d : Nat)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    nativeGK5BXGlobalRestrictHom s t moduli h
      (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values Q) =
    fivefoldGK5BZNorthGlobalMvEval t moduli n d indices values Q := by
  calc
    _ = nativeGK5BXGlobalRestrictHom s t moduli h
        (((MvPolynomial.eval₂Hom (Int.castRingHom Int)
          (fivefoldGK5BZNorthSignedCoordinates n d indices values) Q : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli))) := by
            rw [fivefoldGK5BZNorthMv_signedGlobal]
    _ = ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
          (fivefoldGK5BZNorthSignedCoordinates n d indices values) Q : Int) :
          ZMod (nativeGK5BUFiniteModulus t moduli)) :=
            map_intCast (nativeGK5BXGlobalRestrictHom s t moduli h) _
    _ = _ := (fivefoldGK5BZNorthMv_signedGlobal
      t moduli n d indices values Q).symm

/-- The original compatible-local multivariable polynomial
family restricts to exactly the same original signed
polynomial observations on a smaller finite cover. -/
theorem fivefoldGK5BZNorthMvLocal_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (n d : Nat)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli h
      (fivefoldGK5BZNorthLocalMvEval s moduli n d indices values Q) =
    fivefoldGK5BZNorthLocalMvEval t moduli n d indices values Q := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom s t moduli h
          (nativeGK5BWFiniteCRTRingEquiv s moduli
            (fivefoldGK5BZNorthGlobalMvEval s moduli
              n d indices values Q)) :=
        congrArg (nativeGK5BXCompatibleRestrictHom s t moduli h)
          (fivefoldGK5BZNorthMv_crtAgreement s moduli
            n d indices values Q).symm
    _ = nativeGK5BWFiniteCRTRingEquiv t moduli
          (nativeGK5BXGlobalRestrictHom s t moduli h
            (fivefoldGK5BZNorthGlobalMvEval s moduli
              n d indices values Q)) :=
        (nativeGK5BXCRTNaturality_apply s t moduli h
          (fivefoldGK5BZNorthGlobalMvEval s moduli
            n d indices values Q)).symm
    _ = nativeGK5BWFiniteCRTRingEquiv t moduli
          (fivefoldGK5BZNorthGlobalMvEval t moduli
            n d indices values Q) :=
        congrArg (nativeGK5BWFiniteCRTRingEquiv t moduli)
          (fivefoldGK5BZNorthMvGlobal_restrict s t moduli h
            n d indices values Q)
    _ = _ := fivefoldGK5BZNorthMv_crtAgreement t moduli
      n d indices values Q

/-- Two successive TRUE global finite-cover restrictions
of the same signed north C60 multivariable polynomial
evaluation coincide with its direct smallest-cover value. -/
theorem fivefoldGK5BZNorthMvGlobal_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    nativeGK5BXGlobalRestrictHom t u moduli k
      (nativeGK5BXGlobalRestrictHom s t moduli h
        (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values Q)) =
    fivefoldGK5BZNorthGlobalMvEval u moduli n d indices values Q := by
  calc
    _ = nativeGK5BXGlobalRestrictHom t u moduli k
          (fivefoldGK5BZNorthGlobalMvEval t moduli
            n d indices values Q) :=
        congrArg (nativeGK5BXGlobalRestrictHom t u moduli k)
          (fivefoldGK5BZNorthMvGlobal_restrict s t moduli h
            n d indices values Q)
    _ = _ := fivefoldGK5BZNorthMvGlobal_restrict t u moduli k
      n d indices values Q

/-- Two consecutive TRUE compatible-local restrictions
preserve the exact original signed north C60 finite
multivariable polynomial observations on the smallest cover. -/
theorem fivefoldGK5BZNorthMvLocal_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin n) Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BZNorthLocalMvEval s moduli n d indices values Q)) =
    fivefoldGK5BZNorthLocalMvEval u moduli n d indices values Q := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u moduli k
          (fivefoldGK5BZNorthLocalMvEval t moduli
            n d indices values Q) :=
        congrArg (nativeGK5BXCompatibleRestrictHom t u moduli k)
          (fivefoldGK5BZNorthMvLocal_restrict s t moduli h
            n d indices values Q)
    _ = _ := fivefoldGK5BZNorthMvLocal_restrict t u moduli k
      n d indices values Q

/-- Genuine original F55 primitive source polynomial VALUES,
never reconstructed original Type witnesses. -/
private abbrev fivefoldGK5BZNorthPrimitiveValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (r : Int)

/-- Distinct true F55 double-inverse/right-unit source
polynomial VALUES, with source-Type history unchanged. -/
private abbrev fivefoldGK5BZNorthDoubleValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval (r : Int)

/-- Both TRUE original north F55 sources have coherent
arbitrary finite-multivariable SIGNED numeric CRT towers
and existing conditional CRT-zero polynomial certificates,
yet the ORIGINAL Type-valued original-phi seam verdicts
remain OPPOSITE: primitive yes, double inverse no.
No numeric higher-cell or Type-source reconstruction. -/
theorem fivefoldGK5BZNorthOriginalBothMvTowerButOppositeSeams
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (n d : Nat) (indices : Fin n → Nat)
    (Q : MvPolynomial (Fin n) Int)
    (hbound : 2 ≤ d)
    (hL : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BZNorthLocalMvEval s moduli n d
          indices fivefoldGK5BZNorthPrimitiveValues Q)) =
      fivefoldGK5BZNorthLocalMvEval u moduli n d
        indices fivefoldGK5BZNorthPrimitiveValues Q) ∧
    (nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BZNorthLocalMvEval s moduli n d
          indices fivefoldGK5BZNorthDoubleValues Q)) =
      fivefoldGK5BZNorthLocalMvEval u moduli n d
        indices fivefoldGK5BZNorthDoubleValues Q) ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  have hLu : nativeGK5BUFiniteModulus u moduli ∣ d.factorial :=
    (nativeGK5BXFiniteModulus_dvd s u moduli
      (fun j hj => h (k hj))).trans hL
  obtain ⟨_, hz1, hz2, hyes, hno⟩ :=
    fivefoldGK5BWNorthBothFiniteZeroRingButOppositeSeams
      u moduli d hbound hLu frame i
  exact ⟨fivefoldGK5BZNorthMvLocal_tower s t u moduli h k
      n d indices fivefoldGK5BZNorthPrimitiveValues Q,
    fivefoldGK5BZNorthMvLocal_tower s t u moduli h k
      n d indices fivefoldGK5BZNorthDoubleValues Q,
    hz1, hz2, hyes, hno⟩

#print axioms fivefoldGK5BZNorthSignedCoordinates_apply
#print axioms fivefoldGK5BZNorthMv_signedGlobal
#print axioms fivefoldGK5BZNorthMv_crtAgreement
#print axioms fivefoldGK5BZNorthMvGlobal_add
#print axioms fivefoldGK5BZNorthMvGlobal_mul
#print axioms fivefoldGK5BZNorthMvLocal_add
#print axioms fivefoldGK5BZNorthMvLocal_mul
#print axioms fivefoldGK5BZNorthMvGlobal_restrict
#print axioms fivefoldGK5BZNorthMvLocal_restrict
#print axioms fivefoldGK5BZNorthMvGlobal_tower
#print axioms fivefoldGK5BZNorthMvLocal_tower
#print axioms fivefoldGK5BZNorthOriginalBothMvTowerButOppositeSeams

end
end KUOS.Architecture.WuxingPentagonUnified
