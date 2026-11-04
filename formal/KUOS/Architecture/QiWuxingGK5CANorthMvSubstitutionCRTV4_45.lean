import KUOS.Architecture.QiWuxingGK5BZNorthMultivariableCRTV4_44
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CAVariableSubstitutionCRTNaturality
import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Algebra.MvPolynomial.Rename
import Mathlib.Tactic

/-!
Qi v4.45 — ORIGINAL NORTH C60 SIGNED MULTIVARIABLE VARIABLE
REINDEXING, POLYNOMIAL SUBSTITUTION AND TRUE FINITE CRT TOWERS.

Independent GK5CA proved universal MvPolynomial σ Int renaming,
substitution and finite noncoprime CRT RingEquiv coherence.
This Qi integration instantiates those genuine polynomial
operations at the SAME actual GK5BQ original signed cleared
numerators for each Fin n variable. It handles arbitrary
finite reclassification Fin m → Fin n, including collisions,
and arbitrary polynomial substitutions Fin m → Z[Fin n].

On the global ZMod L_s and the genuine gcd-compatible local
dependent-product Subring we prove equality of original
observations before/after reindexing and substitution, with
the actual CRT, one-cover restriction and the three-cover
tower. Evaluation at signed Int variables before quotient
is retained. The two genuinely distinct F55 original Type
witnesses, primitive P=1 and double inverse/right unit
P=X², have matching NUMERIC substituted CRT towers but
the original-phi structural seam exists vs does not exist.

This module does NOT infer any new original F55 Type
source, P77 identity, P94A four-cell, unconditional P89
reflection, universal GK5AY seam, or W=1→seam from numeric
polynomial descent. Strict 空, independent Kuu→Qi; original
F54 two Nat/two categories/Blocks and F55 Type history,
public root107, protected #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only new module and public aggregate import only;
no axiom, sorry/admit/native_decide, Gray or GK5BA kit.
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

/-- Actual original GK5BQ signed-Int numerators commute
with EVERY finite-variable reclassification, including
noninjective Fin m → Fin n and empty finite indices. -/
theorem fivefoldGK5CANorthSignedCoordinates_reindex
    (m n d : Nat) (f : Fin m → Fin n)
    (indices : Fin n → Nat) (values : Nat → Int)
    (v : Fin m) :
    fivefoldGK5BZNorthSignedCoordinates m d (indices ∘ f) values v =
      fivefoldGK5BZNorthSignedCoordinates n d indices values (f v) :=
  rfl

/-- Renaming TRUE multivariable integer-polynomial variables
and then evaluating at original GK5BQ signed numerators is
the same as evaluating at the reindexed original numerators
in the actual finite global ZMod quotient. -/
theorem fivefoldGK5CANorthMvGlobal_reindex
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (f : Fin m → Fin n)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.rename f) Q) =
    fivefoldGK5BZNorthGlobalMvEval s moduli m d
      (indices ∘ f) values Q :=
  nativeGK5CAGlobalMvEval_rename s moduli f
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- The same original signed-coordinate reindexing equality
in the ACTUAL compatible-local noncoprime CRT Subring. -/
theorem fivefoldGK5CANorthMvLocal_reindex
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (f : Fin m → Fin n)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
      ((MvPolynomial.rename f) Q) =
    fivefoldGK5BZNorthLocalMvEval s moduli m d
      (indices ∘ f) values Q :=
  nativeGK5CACompatibleMvEval_rename s moduli f
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- Original signed variable reindexing and the TRUE GK5BW
CRT RingEquiv commute with the compatible-local observation. -/
theorem fivefoldGK5CANorthMvCRT_reindex
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (f : Fin m → Fin n)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
        ((MvPolynomial.rename f) Q)) =
    fivefoldGK5BZNorthLocalMvEval s moduli m d
      (indices ∘ f) values Q := by
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5BZNorthGlobalMvEval s moduli m d
            (indices ∘ f) values Q) :=
      congrArg (nativeGK5BWFiniteCRTRingEquiv s moduli)
        (fivefoldGK5CANorthMvGlobal_reindex s moduli
          m n d f indices values Q)
    _ = _ := fivefoldGK5BZNorthMv_crtAgreement s moduli m d
      (indices ∘ f) values Q

/-- For arbitrary genuine polynomial substitution of Fin m
variables into Z[Fin n], original north signed global
evaluation equals evaluation of the outer polynomial at the
GLOBAL evaluations of the substituted original polynomials. -/
theorem fivefoldGK5CANorthMvGlobal_bind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ h) Q) =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun v => fivefoldGK5BZNorthGlobalMvEval s moduli n d
        indices values (h v)) Q :=
  nativeGK5CAGlobalMvEval_bind s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) h Q

/-- Original signed finite polynomial substitution commutes
with evaluation in the true compatible-local CRT Subring. -/
theorem fivefoldGK5CANorthMvLocal_bind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ h) Q) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => fivefoldGK5BZNorthLocalMvEval s moduli n d
        indices values (h v)) Q :=
  nativeGK5CACompatibleMvEval_bind s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) h Q

/-- Original north signed integer polynomial substitution
commutes with reduction from Int to the actual global ZMod
quotient. Negative coefficients and moduli zero are allowed. -/
theorem fivefoldGK5CANorthMvSignedGlobal_bind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ h) Q) =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
      (fun v => MvPolynomial.eval₂Hom (Int.castRingHom Int)
        (fivefoldGK5BZNorthSignedCoordinates n d indices values) (h v)) Q : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5CASignedIntMvEval_bind_global s moduli
    (fivefoldGK5BZNorthSignedCoordinates n d indices values) h Q

/-- Original GK5BQ signed multivariable substitutions obey
the genuine complete noncoprime CRT RingEquiv:
evaluate each original substituted polynomial globally, glue
its TRUE residue, then evaluate the outer polynomial locally. -/
theorem fivefoldGK5CANorthMvCRT_bind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
        ((MvPolynomial.bind₁ h) Q)) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => fivefoldGK5BZNorthLocalMvEval s moduli n d
        indices values (h v)) Q := by
  calc
    _ = nativeGK5BZCompatibleMvEvalHom s moduli
          (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
            (fivefoldGK5BZNorthGlobalMvEval s moduli n d
              indices values (h v))) Q :=
      nativeGK5CACRT_bind s moduli
        (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli))) h Q
    _ = _ := congrArg
      (fun ys : Fin m → nativeGK5BWCompatibleSubring s moduli =>
        nativeGK5BZCompatibleMvEvalHom s moduli ys Q)
      (funext fun v => fivefoldGK5BZNorthMv_crtAgreement s moduli
        n d indices values (h v))

/-- Restricting an original signed polynomial substitution
from finite cover s to t equals evaluation at original signed
numerators directly on t, at each substituted polynomial. -/
theorem fivefoldGK5CANorthMvGlobal_restrict_bind
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BXGlobalRestrictHom s t moduli inc
      (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
        ((MvPolynomial.bind₁ h) Q)) =
    nativeGK5BZGlobalMvEvalHom t moduli
      (fun v => fivefoldGK5BZNorthGlobalMvEval t moduli n d
        indices values (h v)) Q := by
  calc
    _ = fivefoldGK5BZNorthGlobalMvEval t moduli n d indices values
          ((MvPolynomial.bind₁ h) Q) :=
      fivefoldGK5BZNorthMvGlobal_restrict s t moduli inc n d
        indices values ((MvPolynomial.bind₁ h) Q)
    _ = _ := fivefoldGK5CANorthMvGlobal_bind t moduli
      m n d indices values h Q

/-- Same finite-cover restriction/substitution coherence in
the TRUE compatible-local CRT dependent-product subring. -/
theorem fivefoldGK5CANorthMvLocal_restrict_bind
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli inc
      (fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
        ((MvPolynomial.bind₁ h) Q)) =
    nativeGK5BZCompatibleMvEvalHom t moduli
      (fun v => fivefoldGK5BZNorthLocalMvEval t moduli n d
        indices values (h v)) Q := by
  calc
    _ = fivefoldGK5BZNorthLocalMvEval t moduli n d indices values
          ((MvPolynomial.bind₁ h) Q) :=
      fivefoldGK5BZNorthMvLocal_restrict s t moduli inc n d
        indices values ((MvPolynomial.bind₁ h) Q)
    _ = _ := fivefoldGK5CANorthMvLocal_bind t moduli
      m n d indices values h Q

/-- True ORIGINAL north C60 three-cover CRT substitution
naturality. Evaluate/genuinely glue on s, restrict via t
then u; or evaluate every substituted signed polynomial
directly on u before evaluating the outer polynomial.
No coprime, nonempty-cover or bounded-degree hypothesis. -/
theorem fivefoldGK5CANorthMvCRT_bind_threeCover
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
            ((MvPolynomial.bind₁ h) Q)))) =
    nativeGK5BZCompatibleMvEvalHom u moduli
      (fun v => fivefoldGK5BZNorthLocalMvEval u moduli n d
        indices values (h v)) Q := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u moduli inc'
          (nativeGK5BXCompatibleRestrictHom s t moduli inc
            (fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
              ((MvPolynomial.bind₁ h) Q))) :=
      congrArg
        (fun z : nativeGK5BWCompatibleSubring s moduli =>
          nativeGK5BXCompatibleRestrictHom t u moduli inc'
            (nativeGK5BXCompatibleRestrictHom s t moduli inc z))
        (fivefoldGK5BZNorthMv_crtAgreement s moduli
          n d indices values ((MvPolynomial.bind₁ h) Q))
    _ = fivefoldGK5BZNorthLocalMvEval u moduli n d indices values
          ((MvPolynomial.bind₁ h) Q) :=
      fivefoldGK5BZNorthMvLocal_tower s t u moduli inc inc'
        n d indices values ((MvPolynomial.bind₁ h) Q)
    _ = _ := fivefoldGK5CANorthMvLocal_bind u moduli
      m n d indices values h Q

/-- Rename arbitrary original multivariable variables BEFORE
polynomial substitution: global original signed observations
are identical to those from the directly composed substitution. -/
theorem fivefoldGK5CANorthMvGlobal_bind_rename
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m k n d : Nat) (f : Fin m → Fin k)
    (h : Fin k → MvPolynomial (Fin n) Int)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) Q)) =
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ (h ∘ f)) Q) :=
  nativeGK5CAGlobalMvEval_bind_rename s moduli f h
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- The same genuine original signed rename/substitution
interchange in the compatible-local CRT subring. -/
theorem fivefoldGK5CANorthMvLocal_bind_rename
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m k n d : Nat) (f : Fin m → Fin k)
    (h : Fin k → MvPolynomial (Fin n) Int)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) Q)) =
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ (h ∘ f)) Q) :=
  nativeGK5CACompatibleMvEval_bind_rename s moduli f h
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- The FULL original-phi numerical reindexing/substitution
CRT square: arbitrary Fin m → Fin k followed by actual
polynomial substitution into original signed Fin n values. -/
theorem fivefoldGK5CANorthMvCRT_bind_rename
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m k n d : Nat) (f : Fin m → Fin k)
    (h : Fin k → MvPolynomial (Fin n) Int)
    (indices : Fin n → Nat) (values : Nat → Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
        ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) Q))) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => fivefoldGK5BZNorthLocalMvEval s moduli n d
        indices values (h (f v))) Q := by
  rw [fivefoldGK5CANorthMvGlobal_bind_rename s moduli
    m k n d f h indices values Q]
  exact fivefoldGK5CANorthMvCRT_bind s moduli
    m n d indices values (h ∘ f) Q

/-- True original primitive F55 Type source polynomial VALUES.
This abbreviation does not introduce a new original Type witness. -/
private abbrev fivefoldGK5CANorthPrimitiveValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (r : Int)

/-- True distinct original double inverse/right F55 unit source
polynomial VALUES, with no numerical proxy of the Type seam. -/
private abbrev fivefoldGK5CANorthDoubleValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval (r : Int)

/-- For BOTH original F55 sources, arbitrary polynomial
substitutions produce coherent compatible-local CRT towers,
but their original-phi STRUCTURAL Type seam remains opposite:
primitive PRESENT, double-inverse/right-unit ABSENT.
Numeric substitution never manufactures a F55 Type witness. -/
theorem fivefoldGK5CANorthOriginalBothSubstitutedTowersOppositeSeams
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (m n d : Nat) (indices : Fin n → Nat)
    (h : Fin m → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int)
    (hbound : 2 ≤ d)
    (hL : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (fivefoldGK5BZNorthLocalMvEval s moduli n d
          indices fivefoldGK5CANorthPrimitiveValues
          ((MvPolynomial.bind₁ h) Q))) =
      fivefoldGK5BZNorthLocalMvEval u moduli n d
        indices fivefoldGK5CANorthPrimitiveValues
        ((MvPolynomial.bind₁ h) Q)) ∧
    (nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (fivefoldGK5BZNorthLocalMvEval s moduli n d
          indices fivefoldGK5CANorthDoubleValues
          ((MvPolynomial.bind₁ h) Q))) =
      fivefoldGK5BZNorthLocalMvEval u moduli n d
        indices fivefoldGK5CANorthDoubleValues
        ((MvPolynomial.bind₁ h) Q)) ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨hprim, hdouble, _, _, hyes, hno⟩ :=
    fivefoldGK5BZNorthOriginalBothMvTowerButOppositeSeams
      s t u moduli inc inc' n d indices
      ((MvPolynomial.bind₁ h) Q) hbound hL frame i
  exact ⟨hprim, hdouble, hyes, hno⟩

#print axioms fivefoldGK5CANorthSignedCoordinates_reindex
#print axioms fivefoldGK5CANorthMvGlobal_reindex
#print axioms fivefoldGK5CANorthMvLocal_reindex
#print axioms fivefoldGK5CANorthMvCRT_reindex
#print axioms fivefoldGK5CANorthMvGlobal_bind
#print axioms fivefoldGK5CANorthMvLocal_bind
#print axioms fivefoldGK5CANorthMvSignedGlobal_bind
#print axioms fivefoldGK5CANorthMvCRT_bind
#print axioms fivefoldGK5CANorthMvGlobal_restrict_bind
#print axioms fivefoldGK5CANorthMvLocal_restrict_bind
#print axioms fivefoldGK5CANorthMvCRT_bind_threeCover
#print axioms fivefoldGK5CANorthMvGlobal_bind_rename
#print axioms fivefoldGK5CANorthMvLocal_bind_rename
#print axioms fivefoldGK5CANorthMvCRT_bind_rename
#print axioms fivefoldGK5CANorthOriginalBothSubstitutedTowersOppositeSeams

end
end KUOS.Architecture.WuxingPentagonUnified
