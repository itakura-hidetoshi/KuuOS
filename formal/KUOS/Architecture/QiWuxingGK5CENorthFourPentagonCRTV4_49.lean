import KUOS.Architecture.QiWuxingGK5CDNorthSplitCRTV4_48
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CEFourSegmentPentagonCRT
import Mathlib.Tactic

/-!
Qi v4.49 — ORIGINAL NORTH C60 SIGNED FOUR-INTERVAL
PENTAGON-SHAPED RINGHOM COHERENCE AND NONCOPRIME CRT DESCENT.

Independent GK5CE verifies five parenthesizations of four
true heterogeneous integer-multivariable polynomial chain
segments as equal RingHoms after actual Nat-index transport.
Instantiate each α i as genuine Fin (arity i), with arbitrary
arity, and terminate at TRUE original GK5BQ signed Int
cleared numerators. No natAbs proxy or invented F55 Type.

The global ZMod L, compatible-local CRT Subring, true CRT
RingEquiv, global/local restriction and three-cover square
are unchanged. These five brackets agree as NUMERIC RingHoms,
not as new original F55 Type sources, higher associator cells,
P77 identities, P89 unconditional reflection, P94A four-cells,
universal GK5AY seam or W=1→seam.
Original primitive P=1 and double inverse/right unit P=X²
retain their already-proved OPPOSITE structural Type seam
verdicts independently of this numerical equality.

Strict 空 / independent Kuu→Qi; original F54 two Nat/two
categories/Blocks and F55 Type history, root107, pinned Lean
v4.30.0-rc2/mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only #1558 Draft/open/unmerged. Append-only.
No new axiom/sorry/admit/native_decide/Gray/GK5BA kit.
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


/-- The true original north LeftLeftLeft parenthesization is an
actual typed integer-polynomial RingHom, including Fin 0. -/
def fivefoldGK5CENorthFourLeftLeftLeft
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    MvPolynomial (Fin (arity start)) Int →+*
      MvPolynomial (Fin (arity (start+(a+(b+(c+e)))))) Int :=
  nativeGK5CEFourLeftLeftLeft
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start a b c e

/-- The LeftLeftLeft north RingHom equals the exact uncut
heterogeneous substitution chain of the SAME original data. -/
theorem fivefoldGK5CENorthFourLeftLeftLeft_eq
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    fivefoldGK5CENorthFourLeftLeftLeft arity steps start a b c e =
      fivefoldGK5CCNorthFiniteChainHom arity steps start (a+(b+(c+e))) :=
  nativeGK5CEFourLeftLeftLeft_eq steps start a b c e

/-- The true original north LeftMiddle parenthesization is an
actual typed integer-polynomial RingHom, including Fin 0. -/
def fivefoldGK5CENorthFourLeftMiddle
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    MvPolynomial (Fin (arity start)) Int →+*
      MvPolynomial (Fin (arity (start+(a+(b+(c+e)))))) Int :=
  nativeGK5CEFourLeftMiddle
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start a b c e

/-- The LeftMiddle north RingHom equals the exact uncut
heterogeneous substitution chain of the SAME original data. -/
theorem fivefoldGK5CENorthFourLeftMiddle_eq
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    fivefoldGK5CENorthFourLeftMiddle arity steps start a b c e =
      fivefoldGK5CCNorthFiniteChainHom arity steps start (a+(b+(c+e))) :=
  nativeGK5CEFourLeftMiddle_eq steps start a b c e

/-- The true original north Middle parenthesization is an
actual typed integer-polynomial RingHom, including Fin 0. -/
def fivefoldGK5CENorthFourMiddle
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    MvPolynomial (Fin (arity start)) Int →+*
      MvPolynomial (Fin (arity (start+(a+(b+(c+e)))))) Int :=
  nativeGK5CEFourMiddle
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start a b c e

/-- The Middle north RingHom equals the exact uncut
heterogeneous substitution chain of the SAME original data. -/
theorem fivefoldGK5CENorthFourMiddle_eq
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    fivefoldGK5CENorthFourMiddle arity steps start a b c e =
      fivefoldGK5CCNorthFiniteChainHom arity steps start (a+(b+(c+e))) :=
  nativeGK5CEFourMiddle_eq steps start a b c e

/-- The true original north RightMiddle parenthesization is an
actual typed integer-polynomial RingHom, including Fin 0. -/
def fivefoldGK5CENorthFourRightMiddle
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    MvPolynomial (Fin (arity start)) Int →+*
      MvPolynomial (Fin (arity (start+(a+(b+(c+e)))))) Int :=
  nativeGK5CEFourRightMiddle
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start a b c e

/-- The RightMiddle north RingHom equals the exact uncut
heterogeneous substitution chain of the SAME original data. -/
theorem fivefoldGK5CENorthFourRightMiddle_eq
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    fivefoldGK5CENorthFourRightMiddle arity steps start a b c e =
      fivefoldGK5CCNorthFiniteChainHom arity steps start (a+(b+(c+e))) :=
  nativeGK5CEFourRightMiddle_eq steps start a b c e

/-- The true original north RightRight parenthesization is an
actual typed integer-polynomial RingHom, including Fin 0. -/
def fivefoldGK5CENorthFourRightRight
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    MvPolynomial (Fin (arity start)) Int →+*
      MvPolynomial (Fin (arity (start+(a+(b+(c+e)))))) Int :=
  nativeGK5CEFourRightRight
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start a b c e

/-- The RightRight north RingHom equals the exact uncut
heterogeneous substitution chain of the SAME original data. -/
theorem fivefoldGK5CENorthFourRightRight_eq
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    fivefoldGK5CENorthFourRightRight arity steps start a b c e =
      fivefoldGK5CCNorthFiniteChainHom arity steps start (a+(b+(c+e))) :=
  nativeGK5CEFourRightRight_eq steps start a b c e

/-- The five genuine original NORTH C60 four-part brackets
form a pentagon-shaped strict RingHom coherence boundary.
This is a NUMERIC ring-level comparison, not a high 4-cell. -/
theorem fivefoldGK5CENorthFourPentagon_boundary
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e : Nat) :
    (fivefoldGK5CENorthFourLeftLeftLeft arity steps start a b c e =
      fivefoldGK5CENorthFourLeftMiddle arity steps start a b c e) ∧
    (fivefoldGK5CENorthFourLeftMiddle arity steps start a b c e =
      fivefoldGK5CENorthFourMiddle arity steps start a b c e) ∧
    (fivefoldGK5CENorthFourMiddle arity steps start a b c e =
      fivefoldGK5CENorthFourRightMiddle arity steps start a b c e) ∧
    (fivefoldGK5CENorthFourRightMiddle arity steps start a b c e =
      fivefoldGK5CENorthFourRightRight arity steps start a b c e) ∧
    (fivefoldGK5CENorthFourRightRight arity steps start a b c e =
      fivefoldGK5CENorthFourLeftLeftLeft arity steps start a b c e) := by
  simpa only [fivefoldGK5CENorthFourLeftLeftLeft,
    fivefoldGK5CENorthFourLeftMiddle,
    fivefoldGK5CENorthFourMiddle,
    fivefoldGK5CENorthFourRightMiddle,
    fivefoldGK5CENorthFourRightRight] using
    (nativeGK5CEFourPentagon_boundary
      (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
      steps start a b c e)

/-- EXACT original GK5BQ signed terminal numerators for
the four-part chain, not their unsigned absolute values. -/
def fivefoldGK5CENorthFourTerminalSigned
    (arity : Nat → Nat) (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    Fin (arity (start+(a+(b+(c+e))))) → Int :=
  fivefoldGK5BZNorthSignedCoordinates
    (arity (start+(a+(b+(c+e))))) depth indices values

/-- The north terminal signed variables are literally
the original GK5BQ integer numerator at each coordinate. -/
theorem fivefoldGK5CENorthFourTerminalSigned_apply
    (arity : Nat → Nat) (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (v : Fin (arity (start+(a+(b+(c+e)))))) :
    fivefoldGK5CENorthFourTerminalSigned
      arity start a b c e depth indices values v =
    nativeGK5BQClearedNumerator depth (indices v) values :=
  rfl

/-- The original signed four-part full chain evaluated
as one real global finite CRT RingHom after leftmost bracket. -/
def fivefoldGK5CENorthGlobalFourEvalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    MvPolynomial (Fin (arity start)) Int →+*
      ZMod (nativeGK5BUFiniteModulus s moduli) :=
  (nativeGK5BZGlobalMvEvalHom s moduli
    (fun v => ((fivefoldGK5CENorthFourTerminalSigned
       arity start a b c e depth indices values v : Int) :
         ZMod (nativeGK5BUFiniteModulus s moduli)))).comp
    (fivefoldGK5CENorthFourLeftLeftLeft arity steps start a b c e)

/-- The same signed north four-part full chain evaluated
in the TRUE gcd-compatible local CRT dependent-product Subring. -/
def fivefoldGK5CENorthLocalFourEvalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    MvPolynomial (Fin (arity start)) Int →+*
      nativeGK5BWCompatibleSubring s moduli :=
  (nativeGK5BZCompatibleMvEvalHom s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5CENorthFourTerminalSigned
        arity start a b c e depth indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)))).comp
    (fivefoldGK5CENorthFourLeftLeftLeft arity steps start a b c e)

/-- Original signed north four-part GLOBAL evaluation is
exactly the previous full GK5CC global RingHom evaluator. -/
theorem fivefoldGK5CENorthGlobalFourEvalHom_eq
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    fivefoldGK5CENorthGlobalFourEvalHom s moduli arity steps
      start a b c e depth indices values =
    nativeGK5CCGlobalChainEvalHom s moduli steps start (a+(b+(c+e)))
      (fun v => ((fivefoldGK5CENorthFourTerminalSigned
        arity start a b c e depth indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) := by
  rw [fivefoldGK5CENorthGlobalFourEvalHom,
    fivefoldGK5CENorthFourLeftLeftLeft_eq]
  rfl

/-- Original signed north four-part LOCAL evaluation equals
the actual full GK5CC compatible-local RingHom evaluation. -/
theorem fivefoldGK5CENorthLocalFourEvalHom_eq
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    fivefoldGK5CENorthLocalFourEvalHom s moduli arity steps
      start a b c e depth indices values =
    nativeGK5CCCompatibleChainEvalHom s moduli steps
      start (a+(b+(c+e)))
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
        ((fivefoldGK5CENorthFourTerminalSigned
          arity start a b c e depth indices values v : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli))) := by
  rw [fivefoldGK5CENorthLocalFourEvalHom,
    fivefoldGK5CENorthFourLeftLeftLeft_eq]
  rfl

/-- Complete original signed north CRT RingEquiv naturality
on all four-part polynomials, as genuine RING HOM equality. -/
theorem fivefoldGK5CENorthFourCRT_RingHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (fivefoldGK5CENorthGlobalFourEvalHom s moduli arity
        steps start a b c e depth indices values) =
    fivefoldGK5CENorthLocalFourEvalHom s moduli arity
      steps start a b c e depth indices values := by
  rw [fivefoldGK5CENorthGlobalFourEvalHom_eq,
    fivefoldGK5CENorthLocalFourEvalHom_eq]
  exact nativeGK5CCCRTChain_naturalHom s moduli steps start
    (a+(b+(c+e)))
    (fun v => ((fivefoldGK5CENorthFourTerminalSigned
      arity start a b c e depth indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)))

/-- Global restriction of original north signed
four-part evaluation commutes for arbitrary finite covers. -/
theorem fivefoldGK5CENorthFourGlobal_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat) (inc : t ⊆ s)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BXGlobalRestrictHom s t moduli inc
      (fivefoldGK5CENorthGlobalFourEvalHom s moduli arity
        steps start a b c e depth indices values P) =
    fivefoldGK5CENorthGlobalFourEvalHom t moduli arity
      steps start a b c e depth indices values P := by
  rw [fivefoldGK5CENorthGlobalFourEvalHom_eq,
    fivefoldGK5CENorthGlobalFourEvalHom_eq]
  exact fivefoldGK5CCNorthGlobalFiniteChain_restrict s t moduli inc
    arity steps start (a+(b+(c+e))) depth indices values P

/-- Local restriction of original north signed
four-part evaluation commutes for arbitrary finite covers. -/
theorem fivefoldGK5CENorthFourLocal_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat) (inc : t ⊆ s)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli inc
      (fivefoldGK5CENorthLocalFourEvalHom s moduli arity
        steps start a b c e depth indices values P) =
    fivefoldGK5CENorthLocalFourEvalHom t moduli arity
      steps start a b c e depth indices values P := by
  rw [fivefoldGK5CENorthLocalFourEvalHom_eq,
    fivefoldGK5CENorthLocalFourEvalHom_eq]
  exact fivefoldGK5CCNorthLocalFiniteChain_restrict s t moduli inc
    arity steps start (a+(b+(c+e))) depth indices values P

/-- The ORIGINAL north signed four-part CRT square remains
strictly commutative under the whole three-cover restriction tower. -/
theorem fivefoldGK5CENorthFourCRT_threeCover
    {ι : Type*} (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5CENorthGlobalFourEvalHom s moduli arity
            steps start a b c e depth indices values P))) =
    fivefoldGK5CENorthLocalFourEvalHom u' moduli arity
      steps start a b c e depth indices values P := by
  rw [fivefoldGK5CENorthGlobalFourEvalHom_eq,
    fivefoldGK5CENorthLocalFourEvalHom_eq]
  exact fivefoldGK5CCNorthFiniteChain_CRT_threeCover s t u' moduli
    inc inc' arity steps start (a+(b+(c+e))) depth indices values P

/-- Signed Int evaluation BEFORE casting to the actual
global finite CRT quotient remains the same on all four brackets. -/
theorem fivefoldGK5CENorthFourSignedInt_global
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    fivefoldGK5CENorthGlobalFourEvalHom s moduli arity steps
      start a b c e depth indices values P =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
      (fivefoldGK5CENorthFourTerminalSigned
        arity start a b c e depth indices values)
      (fivefoldGK5CENorthFourLeftLeftLeft
        arity steps start a b c e P) : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5BZSignedIntMvEval_global s moduli
    (fivefoldGK5CENorthFourTerminalSigned
      arity start a b c e depth indices values)
    (fivefoldGK5CENorthFourLeftLeftLeft
      arity steps start a b c e P)

#print axioms fivefoldGK5CENorthFourLeftLeftLeft_eq
#print axioms fivefoldGK5CENorthFourLeftMiddle_eq
#print axioms fivefoldGK5CENorthFourMiddle_eq
#print axioms fivefoldGK5CENorthFourRightMiddle_eq
#print axioms fivefoldGK5CENorthFourRightRight_eq
#print axioms fivefoldGK5CENorthFourPentagon_boundary
#print axioms fivefoldGK5CENorthFourTerminalSigned_apply
#print axioms fivefoldGK5CENorthGlobalFourEvalHom_eq
#print axioms fivefoldGK5CENorthLocalFourEvalHom_eq
#print axioms fivefoldGK5CENorthFourCRT_RingHom
#print axioms fivefoldGK5CENorthFourGlobal_restrict
#print axioms fivefoldGK5CENorthFourLocal_restrict
#print axioms fivefoldGK5CENorthFourCRT_threeCover
#print axioms fivefoldGK5CENorthFourSignedInt_global

end
end KUOS.Architecture.WuxingPentagonUnified
