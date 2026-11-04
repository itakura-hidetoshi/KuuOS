import KUOS.Architecture.QiWuxingGK5CCNorthTypedFiniteChainCRTV4_47
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CDTypedChainSplitCRT
import Mathlib.Tactic

/-!
Qi v4.48 — TRUE ORIGINAL NORTH C60 ARBITRARY-CUT
CONCATENATION OF FINITE HETEROGENEOUS INTEGER
POLYNOMIAL SUBSTITUTION CHAINS AND NONCOPRIME CRT DESCENT.

The independent GK5CD equality of the actual concatenated
type-changing RingHom and the full unsplit finite chain is
instantiated at α i = Fin (arity i), allowing arbitrary
changing variable counts and noninjective initial rename.
The indispensable dependent Nat.add_assoc transport is
retained instead of asserting false definitional type equality.

Every terminal variable remains EXACTLY the original signed
GK5BQ integer cleared numerator, not its natAbs. Global ZMod
LCM, true gcd-compatible local Subring, CRT RingEquiv,
one-stage and three-cover restrictions are unchanged.

The two ACTUAL original F55 Type sources primitive P=1
and double inverse/right-unit P=X² may agree numerically
on all of these CRT chain evaluations while remaining
opposite in the existence of the original→phi structural
Type seam. No new Type source, P77 class equality, P94A
4-cell, unconditional P89 reflection, GK5AY global seam,
or W=1→seam arises from numeric gluing.

Strict 空; independent Kuu→Qi; genuine F54 two Nat,
two categories/Blocks, original F55 Type histories,
root107, pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected #1558 stays Draft/open/unmerged.
Append-only, no axioms, sorry/admit/native_decide or
Gray/GK5BA kit.
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

/-- A TRUE arbitrary-cut original north finite-variable
chain, using independent GK5CD's genuine type-transported
composition of two real heterogeneous polynomial RingHoms. -/
def fivefoldGK5CDNorthSplitChainHom
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right : Nat) :
    MvPolynomial (Fin (arity start)) Int →+*
      MvPolynomial (Fin (arity (start+(left+right)))) Int :=
  nativeGK5CDTypedSplitHom
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start left right

/-- Splitting the TRUE original north heterogeneous chain
at ANY position preserves its exact entire RingHom. -/
theorem fivefoldGK5CDNorthSplitChainHom_eq
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right : Nat) :
    fivefoldGK5CDNorthSplitChainHom arity steps start left right =
      fivefoldGK5CCNorthFiniteChainHom arity steps start (left+right) :=
  nativeGK5CDTypedSplitHom_eq steps start left right

/-- The original signed global numeric CRT evaluation at
the end of the ACTUAL two-segment chain as an entire RingHom. -/
def fivefoldGK5CDNorthGlobalSplitEvalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    MvPolynomial (Fin (arity start)) Int →+*
      ZMod (nativeGK5BUFiniteModulus s moduli) :=
  (nativeGK5BZGlobalMvEvalHom s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates
        (arity (start+(left+right))) d indices values v : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli)))).comp
    (fivefoldGK5CDNorthSplitChainHom arity steps start left right)

/-- Genuine compatible-local original signed CRT evaluator
of the two authentic type-changing chain segments. -/
def fivefoldGK5CDNorthLocalSplitEvalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    MvPolynomial (Fin (arity start)) Int →+*
      nativeGK5BWCompatibleSubring s moduli :=
  (nativeGK5BZCompatibleMvEvalHom s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates
        (arity (start+(left+right))) d indices values v : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli)))).comp
    (fivefoldGK5CDNorthSplitChainHom arity steps start left right)

/-- The entire original signed north GLOBAL split evaluator
is exactly the previous GK5CC unsplit evaluator RingHom. -/
theorem fivefoldGK5CDNorthGlobalSplitEvalHom_eq
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    fivefoldGK5CDNorthGlobalSplitEvalHom s moduli arity
      steps start left right d indices values =
    nativeGK5CCGlobalChainEvalHom s moduli steps start (left+right)
      (fun v => ((fivefoldGK5BZNorthSignedCoordinates
        (arity (start+(left+right))) d indices values v : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli))) := by
  rw [fivefoldGK5CDNorthGlobalSplitEvalHom,
    fivefoldGK5CDNorthSplitChainHom_eq]
  rfl

/-- Same RingHom equality for the TRUE compatible-local
dependent-product CRT subring (no proxy family). -/
theorem fivefoldGK5CDNorthLocalSplitEvalHom_eq
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    fivefoldGK5CDNorthLocalSplitEvalHom s moduli arity
      steps start left right d indices values =
    nativeGK5CCCompatibleChainEvalHom s moduli steps start (left+right)
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
        ((fivefoldGK5BZNorthSignedCoordinates
          (arity (start+(left+right))) d indices values v : Int) :
            ZMod (nativeGK5BUFiniteModulus s moduli))) := by
  rw [fivefoldGK5CDNorthLocalSplitEvalHom,
    fivefoldGK5CDNorthSplitChainHom_eq]
  rfl

/-- ACTUAL CRT RingEquiv commutes with every original signed
north chain split as an EQUALITY OF RING HOMS. -/
theorem fivefoldGK5CDNorthCRT_SplitRingHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (fivefoldGK5CDNorthGlobalSplitEvalHom s moduli arity
        steps start left right d indices values) =
    fivefoldGK5CDNorthLocalSplitEvalHom s moduli arity
      steps start left right d indices values := by
  rw [fivefoldGK5CDNorthGlobalSplitEvalHom_eq,
    fivefoldGK5CDNorthLocalSplitEvalHom_eq]
  exact nativeGK5CCCRTChain_naturalHom s moduli steps start
    (left+right)
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates
      (arity (start+(left+right))) d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)))

/-- Original SIGNED north global numerical evaluator for an
arbitrary split agrees at every actual polynomial input with
the prior entire unsplit original-chain evaluation. -/
theorem fivefoldGK5CDNorthGlobalSplit_apply
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    fivefoldGK5CDNorthGlobalSplitEvalHom s moduli arity
      steps start left right d indices values P =
    fivefoldGK5CCNorthGlobalFiniteChainEval s moduli arity
      steps start (left+right) d indices values P := by
  rw [fivefoldGK5CDNorthGlobalSplitEvalHom_eq]
  rfl

/-- Corresponding equality of ORIGINAL signed values
in the TRUE compatible-local CRT subring after any split. -/
theorem fivefoldGK5CDNorthLocalSplit_apply
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    fivefoldGK5CDNorthLocalSplitEvalHom s moduli arity
      steps start left right d indices values P =
    fivefoldGK5CCNorthLocalFiniteChainEval s moduli arity
      steps start (left+right) d indices values P := by
  rw [fivefoldGK5CDNorthLocalSplitEvalHom_eq]
  rfl

/-- Both actual CRT split evaluations commute under any
finite-cover restriction of the global quotient as an
equality of genuine RingHoms on all polynomials. -/
theorem fivefoldGK5CDNorthGlobalSplit_restrictHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    (nativeGK5BXGlobalRestrictHom s t moduli inc).comp
      (fivefoldGK5CDNorthGlobalSplitEvalHom s moduli arity
        steps start left right d indices values) =
    fivefoldGK5CDNorthGlobalSplitEvalHom t moduli arity
      steps start left right d indices values := by
  rw [fivefoldGK5CDNorthGlobalSplitEvalHom_eq,
    fivefoldGK5CDNorthGlobalSplitEvalHom_eq]
  apply RingHom.ext
  intro P
  exact fivefoldGK5CCNorthGlobalFiniteChain_restrict s t moduli inc
    arity steps start (left+right) d indices values P

/-- The same full original signed arbitrary split respects
genuine local compatible subring restriction as RingHom. -/
theorem fivefoldGK5CDNorthLocalSplit_restrictHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    (nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
      (fivefoldGK5CDNorthLocalSplitEvalHom s moduli arity
        steps start left right d indices values) =
    fivefoldGK5CDNorthLocalSplitEvalHom t moduli arity
      steps start left right d indices values := by
  rw [fivefoldGK5CDNorthLocalSplitEvalHom_eq,
    fivefoldGK5CDNorthLocalSplitEvalHom_eq]
  apply RingHom.ext
  intro P
  exact fivefoldGK5CCNorthLocalFiniteChain_restrict s t moduli inc
    arity steps start (left+right) d indices values P

/-- THE COMPLETE original north finite noncoprime CRT
three-cover diagram for an arbitrary split, as a strict
equation of TRUE RingHoms. -/
theorem fivefoldGK5CDNorthCRT_SplitThreeCoverHom
    {ι : Type*} (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int) :
    (nativeGK5BXCompatibleRestrictHom t u' moduli inc').comp
      ((nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
        ((nativeGK5BWGlobalCompatibleHom s moduli).comp
          (fivefoldGK5CDNorthGlobalSplitEvalHom s moduli arity
            steps start left right d indices values))) =
    fivefoldGK5CDNorthLocalSplitEvalHom u' moduli arity
      steps start left right d indices values := by
  rw [fivefoldGK5CDNorthGlobalSplitEvalHom_eq,
    fivefoldGK5CDNorthLocalSplitEvalHom_eq]
  apply RingHom.ext
  intro P
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u' moduli inc'
          (nativeGK5BXCompatibleRestrictHom s t moduli inc
            (nativeGK5BWFiniteCRTRingEquiv s moduli
              (fivefoldGK5CCNorthGlobalFiniteChainEval s moduli
                arity steps start (left+right) d indices values P))) := rfl
    _ = fivefoldGK5CCNorthLocalFiniteChainEval u' moduli
          arity steps start (left+right) d indices values P :=
      fivefoldGK5CCNorthFiniteChain_CRT_threeCover s t u' moduli
        inc inc' arity steps start (left+right) d indices values P
    _ = _ := rfl

/-- Independently original signed Int evaluation before
reduction also holds for the ACTUAL arbitrary-cut composite. -/
theorem fivefoldGK5CDNorthSignedSplit_beforeCRT
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start left right d : Nat)
    (indices : Fin (arity (start+(left+right))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    fivefoldGK5CDNorthGlobalSplitEvalHom s moduli arity
      steps start left right d indices values P =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
      (fivefoldGK5BZNorthSignedCoordinates
        (arity (start+(left+right))) d indices values)
      (fivefoldGK5CDNorthSplitChainHom arity steps start left right P) : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)) := by
  rw [fivefoldGK5CDNorthGlobalSplit_apply,
    fivefoldGK5CDNorthSplitChainHom_eq]
  exact fivefoldGK5CCNorthFiniteChain_signedGlobal s moduli arity steps
    start (left+right) d indices values P

#print axioms fivefoldGK5CDNorthSplitChainHom_eq
#print axioms fivefoldGK5CDNorthGlobalSplitEvalHom_eq
#print axioms fivefoldGK5CDNorthLocalSplitEvalHom_eq
#print axioms fivefoldGK5CDNorthCRT_SplitRingHom
#print axioms fivefoldGK5CDNorthGlobalSplit_apply
#print axioms fivefoldGK5CDNorthLocalSplit_apply
#print axioms fivefoldGK5CDNorthGlobalSplit_restrictHom
#print axioms fivefoldGK5CDNorthLocalSplit_restrictHom
#print axioms fivefoldGK5CDNorthCRT_SplitThreeCoverHom
#print axioms fivefoldGK5CDNorthSignedSplit_beforeCRT

end
end KUOS.Architecture.WuxingPentagonUnified
