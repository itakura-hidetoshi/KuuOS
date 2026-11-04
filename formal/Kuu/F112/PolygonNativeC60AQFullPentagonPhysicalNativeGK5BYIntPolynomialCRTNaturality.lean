import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BXFiniteCRTRestrictionCoherence
import Mathlib.Algebra.Polynomial.AlgebraMap
import Mathlib.Tactic

/-!
F112-P94D3GK5BY — TRUE INTEGER POLYNOMIAL EVALUATION NATURALITY
FOR COMPLETE FINITE NONCOPRIME CRT RING DESCENT.

GK5BW proves the genuine ring equivalence
  ZMod (Finset.lcm moduli) ≃+* compatible local ZMod subring
without requiring pairwise coprimality, nonzero moduli,
nonempty covers, or a dominating local modulus. GK5BX
proves strict identity and composition coherence of both
the global and compatible-local finite cover restrictions.

THIS STEP upgrades the arithmetic descent to the genuine
polynomial RING of integer coefficients, not only a selected
residue or finite table of formal powers. Polynomial.eval₂RingHom
at any global or compatible local ZMod point is a true RingHom
from Polynomial Int; addition and multiplication are preserved.
The pinned genuine Mathlib result
Polynomial.ringHom_eval₂_intCastRingHom proves evaluation
naturality under arbitrary RingHom. Apply it to BOTH the global
finite-cover restriction and the compatible-local Subring
restriction and to the true global-to-local CRT homomorphism.

The result is a commuting polynomial-evaluation natural
transformation over any tower u ⊆ t ⊆ s, for ALL original
Int polynomials, including signs and negative coefficients,
without a polynomial degree or factorial-divisibility
hypothesis. For signed source integer n, the evaluation
in ZMod L is EXACTLY the image of the original integer P.eval n.

This is numerical/polynomial descent ONLY. No new original
F55 Type source, P77 class equality, P94A four-cell,
universal GK5AY seam, unconditional P89 reflection or
W=1→seam. Strict 空; independent Kuu→Qi, genuine F54 two
Nat/two categories/Blocks and ORIGINAL F55 Type history
unchanged. Public root107, protected #1558 Draft/open.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axiom, sorry, admit, native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- True integer-polynomial evaluation as a RING HOM
into the global finite CRT quotient ZMod (Finset.lcm m). -/
def nativeGK5BYGlobalIntPolyEvalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli)) :
    Polynomial Int →+* ZMod (nativeGK5BUFiniteModulus s moduli) :=
  Polynomial.eval₂RingHom
    (Int.castRingHom (ZMod (nativeGK5BUFiniteModulus s moduli))) x

/-- True integer-polynomial evaluation as a RING HOM
into the actual compatible-local ZMod family SUBRING. -/
def nativeGK5BYCompatibleIntPolyEvalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (a : nativeGK5BWCompatibleSubring s moduli) :
    Polynomial Int →+* nativeGK5BWCompatibleSubring s moduli :=
  Polynomial.eval₂RingHom
    (Int.castRingHom (nativeGK5BWCompatibleSubring s moduli)) a

/-- Real integer-polynomial evaluation preserves addition
in every global finite CRT quotient, including ZMod 0. -/
theorem nativeGK5BYGlobalIntPolyEval_add
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli))
    (P Q : Polynomial Int) :
    nativeGK5BYGlobalIntPolyEvalHom s moduli x (P + Q) =
      nativeGK5BYGlobalIntPolyEvalHom s moduli x P +
        nativeGK5BYGlobalIntPolyEvalHom s moduli x Q :=
  (nativeGK5BYGlobalIntPolyEvalHom s moduli x).map_add P Q

/-- Real integer-polynomial evaluation preserves
multiplication in the global finite CRT ring. -/
theorem nativeGK5BYGlobalIntPolyEval_mul
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli))
    (P Q : Polynomial Int) :
    nativeGK5BYGlobalIntPolyEvalHom s moduli x (P * Q) =
      nativeGK5BYGlobalIntPolyEvalHom s moduli x P *
        nativeGK5BYGlobalIntPolyEvalHom s moduli x Q :=
  (nativeGK5BYGlobalIntPolyEvalHom s moduli x).map_mul P Q

/-- Compatible-local integer-polynomial evaluation
preserves addition as a genuine SUBRING equation. -/
theorem nativeGK5BYCompatibleIntPolyEval_add
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (a : nativeGK5BWCompatibleSubring s moduli)
    (P Q : Polynomial Int) :
    nativeGK5BYCompatibleIntPolyEvalHom s moduli a (P + Q) =
      nativeGK5BYCompatibleIntPolyEvalHom s moduli a P +
        nativeGK5BYCompatibleIntPolyEvalHom s moduli a Q :=
  (nativeGK5BYCompatibleIntPolyEvalHom s moduli a).map_add P Q

/-- Compatible-local integer-polynomial evaluation
preserves multiplication as a genuine SUBRING equation. -/
theorem nativeGK5BYCompatibleIntPolyEval_mul
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (a : nativeGK5BWCompatibleSubring s moduli)
    (P Q : Polynomial Int) :
    nativeGK5BYCompatibleIntPolyEvalHom s moduli a (P * Q) =
      nativeGK5BYCompatibleIntPolyEvalHom s moduli a P *
        nativeGK5BYCompatibleIntPolyEvalHom s moduli a Q :=
  (nativeGK5BYCompatibleIntPolyEvalHom s moduli a).map_mul P Q

/-- TRUE global polynomial evaluation commutes with any
finite-cover restriction as an EQUALITY OF RING HOMOMORPHISMS
from Polynomial Int; no degree or coprimality assumption. -/
theorem nativeGK5BYGlobalIntPolyEval_restrictHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXGlobalRestrictHom s t moduli h).comp
      (nativeGK5BYGlobalIntPolyEvalHom s moduli x) =
    nativeGK5BYGlobalIntPolyEvalHom t moduli
      (nativeGK5BXGlobalRestrictHom s t moduli h x) := by
  apply RingHom.ext
  intro P
  change
    nativeGK5BXGlobalRestrictHom s t moduli h
      (P.eval₂ (Int.castRingHom
        (ZMod (nativeGK5BUFiniteModulus s moduli))) x) =
    P.eval₂ (Int.castRingHom
      (ZMod (nativeGK5BUFiniteModulus t moduli)))
        (nativeGK5BXGlobalRestrictHom s t moduli h x)
  exact Polynomial.ringHom_eval₂_intCastRingHom P
    (nativeGK5BXGlobalRestrictHom s t moduli h) x

/-- Pointwise genuine global polynomial evaluation
naturality under arbitrary original finite cover restriction. -/
theorem nativeGK5BYGlobalIntPolyEval_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : Polynomial Int) :
    nativeGK5BXGlobalRestrictHom s t moduli h
      (nativeGK5BYGlobalIntPolyEvalHom s moduli x P) =
    nativeGK5BYGlobalIntPolyEvalHom t moduli
      (nativeGK5BXGlobalRestrictHom s t moduli h x) P := by
  have H := congrArg
    (fun f : Polynomial Int →+* ZMod (nativeGK5BUFiniteModulus t moduli) => f P)
    (nativeGK5BYGlobalIntPolyEval_restrictHom s t moduli h x)
  simpa only [RingHom.comp_apply] using H

/-- The genuine compatible-local polynomial evaluation
commutes with restriction AS A RING HOM EQUALITY, not
only as pointwise equality of a particular polynomial. -/
theorem nativeGK5BYCompatibleIntPolyEval_restrictHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (a : nativeGK5BWCompatibleSubring s moduli) :
    (nativeGK5BXCompatibleRestrictHom s t moduli h).comp
      (nativeGK5BYCompatibleIntPolyEvalHom s moduli a) =
    nativeGK5BYCompatibleIntPolyEvalHom t moduli
      (nativeGK5BXCompatibleRestrictHom s t moduli h a) := by
  apply RingHom.ext
  intro P
  change
    nativeGK5BXCompatibleRestrictHom s t moduli h
      (P.eval₂ (Int.castRingHom
        (nativeGK5BWCompatibleSubring s moduli)) a) =
    P.eval₂ (Int.castRingHom
      (nativeGK5BWCompatibleSubring t moduli))
        (nativeGK5BXCompatibleRestrictHom s t moduli h a)
  exact Polynomial.ringHom_eval₂_intCastRingHom P
    (nativeGK5BXCompatibleRestrictHom s t moduli h) a

/-- The genuine complete finite CRT ring homomorphism
commutes with evaluation of EVERY integer polynomial
as an equality of RING HOMOMORPHISMS. -/
theorem nativeGK5BYCRTEvaluation_naturalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (nativeGK5BYGlobalIntPolyEvalHom s moduli x) =
    nativeGK5BYCompatibleIntPolyEvalHom s moduli
      (nativeGK5BWGlobalCompatibleHom s moduli x) := by
  apply RingHom.ext
  intro P
  change
    nativeGK5BWGlobalCompatibleHom s moduli
      (P.eval₂ (Int.castRingHom
        (ZMod (nativeGK5BUFiniteModulus s moduli))) x) =
    P.eval₂ (Int.castRingHom
      (nativeGK5BWCompatibleSubring s moduli))
        (nativeGK5BWGlobalCompatibleHom s moduli x)
  exact Polynomial.ringHom_eval₂_intCastRingHom P
    (nativeGK5BWGlobalCompatibleHom s moduli) x

/-- Integer-polynomial evaluation commutes with the
TRUE GK5BW finite CRT RING EQUIVALENCE pointwise. -/
theorem nativeGK5BYCRTEvaluation_apply
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : Polynomial Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (nativeGK5BYGlobalIntPolyEvalHom s moduli x P) =
    nativeGK5BYCompatibleIntPolyEvalHom s moduli
      (nativeGK5BWFiniteCRTRingEquiv s moduli x) P := by
  have H := congrArg
    (fun f : Polynomial Int →+*
      nativeGK5BWCompatibleSubring s moduli => f P)
    (nativeGK5BYCRTEvaluation_naturalHom s moduli x)
  simpa only [RingHom.comp_apply, nativeGK5BWFiniteCRTRingEquiv_apply] using H

/-- Evaluate the ORIGINAL integer polynomial at an actual
SIGNED integer before reducing to the global CRT quotient:
the result equals genuine polynomial evaluation in ZMod L. -/
theorem nativeGK5BYIntPolynomial_signedGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (P : Polynomial Int) (z : Int) :
    nativeGK5BYGlobalIntPolyEvalHom s moduli
      (z : ZMod (nativeGK5BUFiniteModulus s moduli)) P =
    ((P.eval z : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) := by
  change P.eval₂ (Int.castRingHom
      (ZMod (nativeGK5BUFiniteModulus s moduli)))
      (z : ZMod (nativeGK5BUFiniteModulus s moduli)) =
    ((P.eval z : Int) : ZMod (nativeGK5BUFiniteModulus s moduli))
  exact Polynomial.eval₂_at_apply (Int.castRingHom
    (ZMod (nativeGK5BUFiniteModulus s moduli))) z

/-- Evaluation of any original integer polynomial commutes
with TWO successive genuine global ZMod CRT restrictions.
Both paths agree as the DIRECT smallest-cover restriction. -/
theorem nativeGK5BYGlobalIntPolyEval_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : Polynomial Int) :
    nativeGK5BXGlobalRestrictHom t u moduli k
      (nativeGK5BXGlobalRestrictHom s t moduli h
        (nativeGK5BYGlobalIntPolyEvalHom s moduli x P)) =
    nativeGK5BYGlobalIntPolyEvalHom u moduli
      (nativeGK5BXGlobalRestrictHom s u moduli
        (fun i hi => h (k hi)) x) P := by
  have hcomp := congrArg
    (fun f : ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      ZMod (nativeGK5BUFiniteModulus u moduli) => f x)
    (nativeGK5BXGlobalRestrict_comp s t u moduli h k)
  calc
    _ = nativeGK5BXGlobalRestrictHom t u moduli k
          (nativeGK5BYGlobalIntPolyEvalHom t moduli
            (nativeGK5BXGlobalRestrictHom s t moduli h x) P) :=
        congrArg (nativeGK5BXGlobalRestrictHom t u moduli k)
          (nativeGK5BYGlobalIntPolyEval_restrict s t moduli h x P)
    _ = nativeGK5BYGlobalIntPolyEvalHom u moduli
          (nativeGK5BXGlobalRestrictHom t u moduli k
            (nativeGK5BXGlobalRestrictHom s t moduli h x)) P :=
        nativeGK5BYGlobalIntPolyEval_restrict t u moduli k
          (nativeGK5BXGlobalRestrictHom s t moduli h x) P
    _ = _ := by
      exact congrArg
        (fun y : ZMod (nativeGK5BUFiniteModulus u moduli) =>
          nativeGK5BYGlobalIntPolyEvalHom u moduli y P)
        (by simpa only [RingHom.comp_apply] using hcomp)

/-- Compatible-local integer polynomial evaluation also
obeys the genuine two-stage versus direct restriction law. -/
theorem nativeGK5BYCompatibleIntPolyEval_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (a : nativeGK5BWCompatibleSubring s moduli)
    (P : Polynomial Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (nativeGK5BYCompatibleIntPolyEvalHom s moduli a P)) =
    nativeGK5BYCompatibleIntPolyEvalHom u moduli
      (nativeGK5BXCompatibleRestrictHom s u moduli
        (fun i hi => h (k hi)) a) P := by
  have hcomp := congrArg
    (fun f : nativeGK5BWCompatibleSubring s moduli →+*
      nativeGK5BWCompatibleSubring u moduli => f a)
    (nativeGK5BXCompatibleRestrict_comp s t u moduli h k)
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u moduli k
          (nativeGK5BYCompatibleIntPolyEvalHom t moduli
            (nativeGK5BXCompatibleRestrictHom s t moduli h a) P) :=
        congrArg (nativeGK5BXCompatibleRestrictHom t u moduli k)
          (by
            have H := congrArg
              (fun f : Polynomial Int →+*
                nativeGK5BWCompatibleSubring t moduli => f P)
              (nativeGK5BYCompatibleIntPolyEval_restrictHom
                s t moduli h a)
            simpa only [RingHom.comp_apply] using H)
    _ = nativeGK5BYCompatibleIntPolyEvalHom u moduli
          (nativeGK5BXCompatibleRestrictHom t u moduli k
            (nativeGK5BXCompatibleRestrictHom s t moduli h a)) P := by
        have H := congrArg
          (fun f : Polynomial Int →+*
            nativeGK5BWCompatibleSubring u moduli => f P)
          (nativeGK5BYCompatibleIntPolyEval_restrictHom t u moduli k
            (nativeGK5BXCompatibleRestrictHom s t moduli h a))
        simpa only [RingHom.comp_apply] using H
    _ = _ := by
      exact congrArg
        (fun y : nativeGK5BWCompatibleSubring u moduli =>
          nativeGK5BYCompatibleIntPolyEvalHom u moduli y P)
        (by simpa only [RingHom.comp_apply] using hcomp)

/-- Strong three-cover polynomial CRT coherence: evaluate
ANY original integer polynomial in the large global ring,
glue to its original compatible local residue family,
restrict TWICE, or first restrict the global argument to
the smallest cover and then evaluate. They are IDENTICAL. -/
theorem nativeGK5BYPolynomialCRTTower_natural
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : Polynomial Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5BYGlobalIntPolyEvalHom s moduli x P))) =
    nativeGK5BWFiniteCRTRingEquiv u moduli
      (nativeGK5BYGlobalIntPolyEvalHom u moduli
        (nativeGK5BXGlobalRestrictHom s u moduli
          (fun i hi => h (k hi)) x) P) := by
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv u moduli
          (nativeGK5BXGlobalRestrictHom t u moduli k
            (nativeGK5BXGlobalRestrictHom s t moduli h
              (nativeGK5BYGlobalIntPolyEvalHom s moduli x P))) := by
        rw [nativeGK5BXCRTNaturality_apply s t moduli h
          (nativeGK5BYGlobalIntPolyEvalHom s moduli x P)]
        rw [nativeGK5BXCRTNaturality_apply t u moduli k
          (nativeGK5BXGlobalRestrictHom s t moduli h
            (nativeGK5BYGlobalIntPolyEvalHom s moduli x P))]
    _ = _ := congrArg (nativeGK5BWFiniteCRTRingEquiv u moduli)
      (nativeGK5BYGlobalIntPolyEval_tower s t u moduli h k x P)

#print axioms nativeGK5BYGlobalIntPolyEval_add
#print axioms nativeGK5BYGlobalIntPolyEval_mul
#print axioms nativeGK5BYCompatibleIntPolyEval_add
#print axioms nativeGK5BYCompatibleIntPolyEval_mul
#print axioms nativeGK5BYGlobalIntPolyEval_restrictHom
#print axioms nativeGK5BYGlobalIntPolyEval_restrict
#print axioms nativeGK5BYCompatibleIntPolyEval_restrictHom
#print axioms nativeGK5BYCRTEvaluation_naturalHom
#print axioms nativeGK5BYCRTEvaluation_apply
#print axioms nativeGK5BYIntPolynomial_signedGlobal
#print axioms nativeGK5BYGlobalIntPolyEval_tower
#print axioms nativeGK5BYCompatibleIntPolyEval_tower
#print axioms nativeGK5BYPolynomialCRTTower_natural

end
end Kuu.F112.Physical
