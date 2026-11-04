import KUOS.Architecture.QiWuxingGK5CBNorthDoubleSubstitutionCRTV4_46
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CCTypedFiniteSubstitutionCRTNaturality
import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Tactic

/-!
Qi v4.47 — GENUINE ORIGINAL NORTH C60 SIGNED
HETEROGENEOUS ARBITRARY FINITE POLYNOMIAL SUBSTITUTION
CHAIN, COMPLETE NONCOPRIME CRT NATURALITY AND SEAM BOUNDARY.

Independent GK5CC constructs an ACTUAL type-changing
RingHom at every Nat-indexed variable stage, with arbitrary
finite length, and proves genuine GK5BW/BX/BZ noncoprime
CRT naturality and finite-cover restriction for the whole
typed chain. We specialize alpha i := Fin (arity i)
where the number of variables may vary at each stage.

Every terminal variable receives EXACTLY the original signed
GK5BQ cleared numerator. No natAbs proxy and no invented
original F55 Type witness. The signed original Int evaluation
before quotient, genuine global ZMod L, compatible-local
Subring, CRT RingEquiv and three-cover tower commute.
Two distinct ACTUAL original F55 Type sources primitive P=1
and double inverse plus original right unit P=X² share
numeric CRT descent and existing conditional original-depth
polynomial zero certificates but retain OPPOSITE original-phi
structural seam verdicts. Numeric gluing cannot create a
F55 Type source, P77 class equality, P94A four-cell,
unconditional P89 reflection or universal GK5AY seam.

Strict 空, independent Kuu→Qi; true original F54 two Nat,
two categories/Blocks, original F55 Type source history,
genuine north C60 gauge and P89 conditional BadPair boundary.
Public root107; Lean v4.30.0-rc2/mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6 pinned.
Protected #1558 remains Draft/open/unmerged.
Append-only, no axiom/sorry/admit/native_decide/Gray/GK5BA kit.
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

/-- The ACTUAL type family Fin (arity i), whose variable
count is allowed to change at every substitution stage. -/
def fivefoldGK5CCNorthFiniteVariableTypes (arity : Nat → Nat) :
    Nat → Type :=
  fun i => Fin (arity i)

/-- The GENUINE finite, type-changing RingHom chain for
original north C60 polynomial variables, with arbitrary
arity at each stage. -/
def fivefoldGK5CCNorthFiniteChainHom
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length : Nat) :
    MvPolynomial (Fin (arity start)) Int →+*
      MvPolynomial (Fin (arity (start + length))) Int :=
  nativeGK5CCTypedChainHom (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start length

/-- Original signed north C60 finite-variable chain
evaluation in the genuine global ZMod L_s quotient. -/
def fivefoldGK5CCNorthGlobalFiniteChainEval
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    ZMod (nativeGK5BUFiniteModulus s moduli) :=
  nativeGK5CCGlobalChainEvalHom
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    s moduli steps start length
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates
      (arity (start + length)) d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) P

/-- The SAME original signed numerical finite chain in
the TRUE compatible-local CRT dependent-product Subring. -/
def fivefoldGK5CCNorthLocalFiniteChainEval
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BWCompatibleSubring s moduli :=
  nativeGK5CCCompatibleChainEvalHom
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    s moduli steps start length
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates
        (arity (start + length)) d indices values v : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli))) P

/-- At every terminal variable the coordinate is
literally the original SIGNED GK5BQ numerator. -/
theorem fivefoldGK5CCNorthTerminalSigned_apply
    (arity : Nat → Nat) (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (v : Fin (arity (start + length))) :
    fivefoldGK5BZNorthSignedCoordinates
      (arity (start + length)) d indices values v =
    nativeGK5BQClearedNumerator d (indices v) values :=
  rfl

/-- The TRUE GK5BW CRT RingEquiv commutes with the
entire arbitrary-length original signed north C60
type-changing polynomial substitution chain. -/
theorem fivefoldGK5CCNorthFiniteChain_CRT
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (fivefoldGK5CCNorthGlobalFiniteChainEval
        s moduli arity steps start length d indices values P) =
    fivefoldGK5CCNorthLocalFiniteChainEval
      s moduli arity steps start length d indices values P := by
  simpa only [fivefoldGK5CCNorthGlobalFiniteChainEval,
    fivefoldGK5CCNorthLocalFiniteChainEval,
    nativeGK5BWFiniteCRTRingEquiv_apply, RingHom.comp_apply] using
    (RingHom.congr_fun
      (nativeGK5CCCRTChain_naturalHom s moduli steps
        start length
        (fun v => ((fivefoldGK5BZNorthSignedCoordinates
          (arity (start + length)) d indices values v : Int) :
            ZMod (nativeGK5BUFiniteModulus s moduli))))
      P)

/-- The original signed Int polynomial value is evaluated
before reduction to the true global ZMod quotient, even
after every stage of an arbitrary-length typed chain. -/
theorem fivefoldGK5CCNorthFiniteChain_signedGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    fivefoldGK5CCNorthGlobalFiniteChainEval
      s moduli arity steps start length d indices values P =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
      (fivefoldGK5BZNorthSignedCoordinates
        (arity (start + length)) d indices values)
      (fivefoldGK5CCNorthFiniteChainHom arity steps start length P) : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5CCSignedIntChain_global s moduli steps start length
    (fivefoldGK5BZNorthSignedCoordinates
      (arity (start + length)) d indices values) P

/-- Arbitrary global finite-cover restriction preserves
the same ORIGINAL signed north C60 chain value. -/
theorem fivefoldGK5CCNorthGlobalFiniteChain_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BXGlobalRestrictHom s t moduli inc
      (fivefoldGK5CCNorthGlobalFiniteChainEval
        s moduli arity steps start length d indices values P) =
    fivefoldGK5CCNorthGlobalFiniteChainEval
      t moduli arity steps start length d indices values P := by
  calc
    _ = nativeGK5BXGlobalRestrictHom s t moduli inc
          (((MvPolynomial.eval₂Hom (Int.castRingHom Int)
            (fivefoldGK5BZNorthSignedCoordinates
              (arity (start + length)) d indices values)
            (fivefoldGK5CCNorthFiniteChainHom arity steps start length P) :
              Int) : ZMod (nativeGK5BUFiniteModulus s moduli)) := by
        rw [fivefoldGK5CCNorthFiniteChain_signedGlobal]
    _ = ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
            (fivefoldGK5BZNorthSignedCoordinates
              (arity (start + length)) d indices values)
            (fivefoldGK5CCNorthFiniteChainHom arity steps start length P) :
              Int) : ZMod (nativeGK5BUFiniteModulus t moduli)) :=
        map_intCast (nativeGK5BXGlobalRestrictHom s t moduli inc) _
    _ = _ := (fivefoldGK5CCNorthFiniteChain_signedGlobal t moduli
      arity steps start length d indices values P).symm

/-- TRUE compatible-local finite-cover restriction carries
the entire original signed north finite chain to exactly
the same original signed chain on the smaller cover. -/
theorem fivefoldGK5CCNorthLocalFiniteChain_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli inc
      (fivefoldGK5CCNorthLocalFiniteChainEval
        s moduli arity steps start length d indices values P) =
    fivefoldGK5CCNorthLocalFiniteChainEval
      t moduli arity steps start length d indices values P := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5CCNorthGlobalFiniteChainEval
            s moduli arity steps start length d indices values P)) :=
      congrArg (nativeGK5BXCompatibleRestrictHom s t moduli inc)
        (fivefoldGK5CCNorthFiniteChain_CRT s moduli
          arity steps start length d indices values P).symm
    _ = nativeGK5BWFiniteCRTRingEquiv t moduli
        (nativeGK5BXGlobalRestrictHom s t moduli inc
          (fivefoldGK5CCNorthGlobalFiniteChainEval
            s moduli arity steps start length d indices values P)) :=
      (nativeGK5BXCRTNaturality_apply s t moduli inc _).symm
    _ = nativeGK5BWFiniteCRTRingEquiv t moduli
        (fivefoldGK5CCNorthGlobalFiniteChainEval
          t moduli arity steps start length d indices values P) :=
      congrArg (nativeGK5BWFiniteCRTRingEquiv t moduli)
        (fivefoldGK5CCNorthGlobalFiniteChain_restrict s t moduli inc
          arity steps start length d indices values P)
    _ = _ := fivefoldGK5CCNorthFiniteChain_CRT t moduli
      arity steps start length d indices values P

/-- A genuine two-step cover restriction preserves the
SAME original signed arbitrary-length typed chain. -/
theorem fivefoldGK5CCNorthLocalFiniteChain_tower
    {ι : Type*} (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (fivefoldGK5CCNorthLocalFiniteChainEval
          s moduli arity steps start length d indices values P)) =
    fivefoldGK5CCNorthLocalFiniteChainEval
      u' moduli arity steps start length d indices values P := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (fivefoldGK5CCNorthLocalFiniteChainEval
        t moduli arity steps start length d indices values P) :=
      congrArg (nativeGK5BXCompatibleRestrictHom t u' moduli inc')
        (fivefoldGK5CCNorthLocalFiniteChain_restrict s t moduli inc
          arity steps start length d indices values P)
    _ = _ := fivefoldGK5CCNorthLocalFiniteChain_restrict
      t u' moduli inc' arity steps start length d indices values P

/-- The genuine three-cover CRT diagram for the original
signed type-changing chain is STRICTLY commutative for
EVERY finite length and every original north coordinate. -/
theorem fivefoldGK5CCNorthFiniteChain_CRT_threeCover
    {ι : Type*} (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5CCNorthGlobalFiniteChainEval
            s moduli arity steps start length d indices values P))) =
    fivefoldGK5CCNorthLocalFiniteChainEval
      u' moduli arity steps start length d indices values P := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u' moduli inc'
        (nativeGK5BXCompatibleRestrictHom s t moduli inc
          (fivefoldGK5CCNorthLocalFiniteChainEval
            s moduli arity steps start length d indices values P)) :=
      congrArg
        (fun a : nativeGK5BWCompatibleSubring s moduli =>
          nativeGK5BXCompatibleRestrictHom t u' moduli inc'
            (nativeGK5BXCompatibleRestrictHom s t moduli inc a))
        (fivefoldGK5CCNorthFiniteChain_CRT s moduli
          arity steps start length d indices values P)
    _ = _ := fivefoldGK5CCNorthLocalFiniteChain_tower
      s t u' moduli inc inc' arity steps
      start length d indices values P

/-- Unrestricted (including NONINJECTIVE) finite variable
reclassification can precede the original signed whole
type-changing chain and complete three-cover CRT descent. -/
theorem fivefoldGK5CCNorthFiniteChain_CRT_rename_threeCover
    {ι : Type*} (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d m : Nat)
    (f : Fin m → Fin (arity start))
    (indices : Fin (arity (start + length)) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin m) Int) :
    nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5CCNorthGlobalFiniteChainEval
            s moduli arity steps start length d indices values
            ((MvPolynomial.rename f) P)))) =
    fivefoldGK5CCNorthLocalFiniteChainEval
      u' moduli arity steps start length d indices values
      ((MvPolynomial.rename f) P) :=
  fivefoldGK5CCNorthFiniteChain_CRT_threeCover
    s t u' moduli inc inc' arity steps start length d indices
      values ((MvPolynomial.rename f) P)

/-- ORIGINAL primitive F55 Type witness polynomial VALUES.
These values do not create a fresh Type witness. -/
private abbrev fivefoldGK5CCNorthPrimitiveValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (r : Int)

/-- DISTINCT original double inverse/right F55 unit Type
witness polynomial VALUES, with original seam absent. -/
private abbrev fivefoldGK5CCNorthDoubleValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval (r : Int)

/-- Both TRUE ORIGINAL F55 Type witnesses carry a
numerically coherent genuinely arbitrary-length, typed
north signed CRT tower and existing conditional numerical
zero certificates; however original-phi structural Type
seam is PRESENT for primitive and ABSENT for double
inverse. No arbitrary polynomial zero is inferred. -/
theorem fivefoldGK5CCNorthOriginalBothFiniteChainsOppositeSeams
    {ι : Type*} (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i + 1))) Int)
    (start length d : Nat)
    (indices : Fin (arity (start + length)) → Nat)
    (P : MvPolynomial (Fin (arity start)) Int)
    (hbound : 2 ≤ d)
    (hL : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (fivefoldGK5CCNorthLocalFiniteChainEval
          s moduli arity steps start length d indices
            fivefoldGK5CCNorthPrimitiveValues P)) =
      fivefoldGK5CCNorthLocalFiniteChainEval
        u' moduli arity steps start length d indices
          fivefoldGK5CCNorthPrimitiveValues P) ∧
    (nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (fivefoldGK5CCNorthLocalFiniteChainEval
          s moduli arity steps start length d indices
            fivefoldGK5CCNorthDoubleValues P)) =
      fivefoldGK5CCNorthLocalFiniteChainEval
        u' moduli arity steps start length d indices
          fivefoldGK5CCNorthDoubleValues P) ∧
    fivefoldGK5BVNorthFiniteZero u' moduli d
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial ∧
    fivefoldGK5BVNorthFiniteZero u' moduli d
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨_, _, hzeroPrim, hzeroDouble, hyes, hno⟩ :=
    fivefoldGK5BZNorthOriginalBothMvTowerButOppositeSeams
      s t u' moduli inc inc'
      (arity (start + length)) d indices
      (fivefoldGK5CCNorthFiniteChainHom arity steps start length P)
      hbound hL frame i
  exact ⟨fivefoldGK5CCNorthLocalFiniteChain_tower
      s t u' moduli inc inc' arity steps start length d
      indices fivefoldGK5CCNorthPrimitiveValues P,
    fivefoldGK5CCNorthLocalFiniteChain_tower
      s t u' moduli inc inc' arity steps start length d
      indices fivefoldGK5CCNorthDoubleValues P,
    hzeroPrim, hzeroDouble, hyes, hno⟩

#print axioms fivefoldGK5CCNorthTerminalSigned_apply
#print axioms fivefoldGK5CCNorthFiniteChain_CRT
#print axioms fivefoldGK5CCNorthFiniteChain_signedGlobal
#print axioms fivefoldGK5CCNorthGlobalFiniteChain_restrict
#print axioms fivefoldGK5CCNorthLocalFiniteChain_restrict
#print axioms fivefoldGK5CCNorthLocalFiniteChain_tower
#print axioms fivefoldGK5CCNorthFiniteChain_CRT_threeCover
#print axioms fivefoldGK5CCNorthFiniteChain_CRT_rename_threeCover
#print axioms fivefoldGK5CCNorthOriginalBothFiniteChainsOppositeSeams

end
end KUOS.Architecture.WuxingPentagonUnified
