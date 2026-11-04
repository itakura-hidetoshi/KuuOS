import KUOS.Architecture.QiWuxingGK5CANorthMvSubstitutionCRTV4_45
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CBIteratedSubstitutionCRTTower
import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Algebra.MvPolynomial.Rename
import Mathlib.Tactic

/-!
Qi v4.46 — TRUE ORIGINAL NORTH C60 SIGNED ITERATED
MULTIVARIABLE POLYNOMIAL SUBSTITUTION AND FINITE CRT TOWERS.

Independent GK5CB upgraded the original complete noncoprime
finite CRT naturality to TWO genuine polynomial substitutions,
actual global/local substitution evaluation RingHoms,
and simultaneous noninjective reclassification and three-cover
CRT towers. Here every Fin n variable receives precisely the
ORIGINAL signed GK5BQ integer cleared numerator. We introduce
NO new F55 Type source or absolute-value proxy.

For arbitrary integer multivariable polynomials, including
negative coefficients, arbitrary finite-cover Nat moduli
including zeros, empty covers, empty variables, and variable
collisions, prove the actual global/local RingHom CRT square,
two-stage substitution, finite-cover restrictions, three-cover
commutativity, and simultaneous reclassification.

Original primitive F55 P=1 and double inverse/right-unit
P=X² have independently coherent NUMERIC CRT evaluations and
the existing conditional arithmetic zero certificates, BUT
the original→phi structural Type seam remains PRESENT versus
ABSENT. No P77 class, P89 reflection, P94A cell, universal
GK5AY seam or W=1→seam is reconstructed.

Strict 空; independent Kuu→Qi, true original F54 two Nat,
two categories/Blocks and F55 Type history. Root107.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 Draft/open/unmerged.
Append-only; no sorry/admit/axiom/native_decide/Gray/GK5BA kit.
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

/-- TRUE original GK5BQ signed coordinate vector, followed
by arbitrary polynomial substitution, as a genuine GLOBAL
ZMod finite CRT RING HOM on the outer polynomial algebra. -/
def fivefoldGK5CBNorthGlobalSubstitutionHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int) :
    MvPolynomial (Fin m) Int →+* ZMod (nativeGK5BUFiniteModulus s moduli) :=
  nativeGK5CBGlobalSubstitutionEvalHom s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) h

/-- The SAME original signed substitution, evaluated as
an ACTUAL RingHom in the genuine gcd-compatible local
finite noncoprime CRT Subring. -/
def fivefoldGK5CBNorthLocalSubstitutionHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int) :
    MvPolynomial (Fin m) Int →+* nativeGK5BWCompatibleSubring s moduli :=
  nativeGK5CBCompatibleSubstitutionEvalHom s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) h

/-- The original signed north CRT commutes with the FULL
polynomial substitution as an EQUALITY OF RING HOMS,
not only a pointwise statement for one polynomial. -/
theorem fivefoldGK5CBNorthSubstitutionCRT_RingHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (fivefoldGK5CBNorthGlobalSubstitutionHom s moduli
        m n d indices values h) =
    fivefoldGK5CBNorthLocalSubstitutionHom s moduli
      m n d indices values h :=
  nativeGK5CBCRTSubstitutionEvalHom_natural s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) h

/-- Original signed north polynomial-substitution RingHom
commutes with ANY finite-cover global ZMod restriction. -/
theorem fivefoldGK5CBNorthGlobalSubstitutionHom_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int) :
    (nativeGK5BXGlobalRestrictHom s t moduli inc).comp
      (fivefoldGK5CBNorthGlobalSubstitutionHom s moduli
        m n d indices values h) =
    fivefoldGK5CBNorthGlobalSubstitutionHom t moduli
      m n d indices values h := by
  apply RingHom.ext
  intro Q
  exact fivefoldGK5BZNorthMvGlobal_restrict s t moduli inc
    n d indices values ((MvPolynomial.bind₁ h) Q)

/-- Original signed north polynomial-substitution RingHom
commutes with ANY finite compatible-local CRT restriction. -/
theorem fivefoldGK5CBNorthLocalSubstitutionHom_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (m n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin n) Int) :
    (nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
      (fivefoldGK5CBNorthLocalSubstitutionHom s moduli
        m n d indices values h) =
    fivefoldGK5CBNorthLocalSubstitutionHom t moduli
      m n d indices values h := by
  apply RingHom.ext
  intro Q
  exact fivefoldGK5BZNorthMvLocal_restrict s t moduli inc
    n d indices values ((MvPolynomial.bind₁ h) Q)

/-- TWO genuine original signed north polynomial
substitutions yield THREE NESTED evaluations in the actual
global finite CRT residue ring. -/
theorem fivefoldGK5CBNorthMvGlobal_doubleBind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m p n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)) =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun i => nativeGK5BZGlobalMvEvalHom s moduli
        (fun j => fivefoldGK5BZNorthGlobalMvEval s moduli n d
          indices values (k j))
        (h i)) Q :=
  nativeGK5CBGlobalDoubleBind_expand s moduli
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) h k Q

/-- Same TRUE original north double-substitution formula
in the genuine compatible-local CRT Subring. -/
theorem fivefoldGK5CBNorthMvLocal_doubleBind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m p n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom s moduli
        (fun j => fivefoldGK5BZNorthLocalMvEval s moduli n d
          indices values (k j))
        (h i)) Q :=
  nativeGK5CBCompatibleDoubleBind_expand s moduli
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) h k Q

/-- The exact ORIGINAL signed integers can be substituted
and evaluated TWICE in Int BEFORE passage to the genuine
finite global CRT residue ring, including modulus zero. -/
theorem fivefoldGK5CBNorthMvSignedDoubleBind_global
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m p n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)) =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
      (fun i => MvPolynomial.eval₂Hom (Int.castRingHom Int)
        (fun j => MvPolynomial.eval₂Hom (Int.castRingHom Int)
          (fivefoldGK5BZNorthSignedCoordinates n d indices values) (k j))
        (h i)) Q : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5CBSignedIntDoubleBind_global s moduli
    (fivefoldGK5BZNorthSignedCoordinates n d indices values)
    h k Q

/-- TRUE global restriction sends both original signed
polynomial substitutions to TRIPLE nested evaluation at
the restricted quotient, with no signed-value proxy. -/
theorem fivefoldGK5CBNorthMvGlobal_doubleBind_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (m p n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BXGlobalRestrictHom s t moduli inc
      (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))) =
    nativeGK5BZGlobalMvEvalHom t moduli
      (fun i => nativeGK5BZGlobalMvEvalHom t moduli
        (fun j => fivefoldGK5BZNorthGlobalMvEval t moduli n d
          indices values (k j))
        (h i)) Q := by
  calc
    _ = fivefoldGK5BZNorthGlobalMvEval t moduli n d indices values
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)) :=
      fivefoldGK5BZNorthMvGlobal_restrict s t moduli inc
        n d indices values ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))
    _ = _ := fivefoldGK5CBNorthMvGlobal_doubleBind t moduli
      m p n d indices values h k Q

/-- Corresponding local compatible-family restriction
for BOTH signed original polynomial substitutions. -/
theorem fivefoldGK5CBNorthMvLocal_doubleBind_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (m p n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli inc
      (fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))) =
    nativeGK5BZCompatibleMvEvalHom t moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom t moduli
        (fun j => fivefoldGK5BZNorthLocalMvEval t moduli n d
          indices values (k j))
        (h i)) Q := by
  calc
    _ = fivefoldGK5BZNorthLocalMvEval t moduli n d indices values
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)) :=
      fivefoldGK5BZNorthMvLocal_restrict s t moduli inc
        n d indices values ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))
    _ = _ := fivefoldGK5CBNorthMvLocal_doubleBind t moduli
      m p n d indices values h k Q

/-- TRUE original signed north C60 three-cover CRT
coherence for TWO independent, arbitrary polynomial
substitutions: evaluate/glue on s then restrict via t,u,
or evaluate 3 stages directly in the genuine local
compatible-family Subring of u. -/
theorem fivefoldGK5CBNorthMvCRT_doubleBind_threeCover
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (m p n d : Nat) (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin m → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
            ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))))) =
    nativeGK5BZCompatibleMvEvalHom u moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom u moduli
        (fun j => fivefoldGK5BZNorthLocalMvEval u moduli n d
          indices values (k j))
        (h i)) Q := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u moduli inc'
          (nativeGK5BXCompatibleRestrictHom s t moduli inc
            (fivefoldGK5BZNorthLocalMvEval s moduli n d
              indices values ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)))) :=
      congrArg
        (fun a : nativeGK5BWCompatibleSubring s moduli =>
          nativeGK5BXCompatibleRestrictHom t u moduli inc'
            (nativeGK5BXCompatibleRestrictHom s t moduli inc a))
        (fivefoldGK5BZNorthMv_crtAgreement s moduli n d indices values
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)))
    _ = fivefoldGK5BZNorthLocalMvEval u moduli n d indices values
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q)) :=
      fivefoldGK5BZNorthMvLocal_tower s t u moduli inc inc'
        n d indices values ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))
    _ = _ := fivefoldGK5CBNorthMvLocal_doubleBind u moduli
      m p n d indices values h k Q

/-- Original signed north global evaluation commutes with
arbitrary finite variable RECLASSIFICATION before the two
polynomial substitutions, even when variables collide. -/
theorem fivefoldGK5CBNorthMvGlobal_rename_doubleBind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m r p n d : Nat) (f : Fin m → Fin r)
    (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin r → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ k)
        ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) Q))) =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun i => nativeGK5BZGlobalMvEvalHom s moduli
        (fun j => fivefoldGK5BZNorthGlobalMvEval s moduli n d
          indices values (k j))
        (h (f i))) Q :=
  nativeGK5CBGlobalRenameDoubleBind s moduli f h k
    (fun v => ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- The same variable reclassification and two substitution
coherence holds in the actual compatible-local CRT Subring. -/
theorem fivefoldGK5CBNorthMvLocal_rename_doubleBind
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m r p n d : Nat) (f : Fin m → Fin r)
    (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin r → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    fivefoldGK5BZNorthLocalMvEval s moduli n d indices values
      ((MvPolynomial.bind₁ k)
        ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) Q))) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom s moduli
        (fun j => fivefoldGK5BZNorthLocalMvEval s moduli n d
          indices values (k j))
        (h (f i))) Q :=
  nativeGK5CBCompatibleRenameDoubleBind s moduli f h k
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
      ((fivefoldGK5BZNorthSignedCoordinates n d indices values v : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli))) Q

/-- The FULL TRUE original signed north CRT reclassification
square, TWO substitutions, and the three-cover tower
commute SIMULTANEOUSLY. No coprimality or injectivity. -/
theorem fivefoldGK5CBNorthMvCRT_rename_doubleBind_threeCover
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (m r p n d : Nat) (f : Fin m → Fin r)
    (indices : Fin n → Nat) (values : Nat → Int)
    (h : Fin r → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices values
            ((MvPolynomial.bind₁ k)
              ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) Q)))))) =
    nativeGK5BZCompatibleMvEvalHom u moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom u moduli
        (fun j => fivefoldGK5BZNorthLocalMvEval u moduli n d
          indices values (k j))
        (h (f i))) Q := by
  have hreclass :
      (MvPolynomial.bind₁ k)
        ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) Q)) =
      (MvPolynomial.bind₁ k)
        ((MvPolynomial.bind₁ (h ∘ f)) Q) :=
    congrArg (MvPolynomial.bind₁ k)
      (nativeGK5CA_bind_rename f h Q)
  rw [hreclass]
  exact fivefoldGK5CBNorthMvCRT_doubleBind_threeCover s t u moduli
    inc inc' m p n d indices values (h ∘ f) k Q

/-- ORIGINAL primitive P=1 F55 Type witness numerical
polynomial values, not a newly constructed Type witness. -/
private abbrev fivefoldGK5CBNorthPrimitiveValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (r : Int)

/-- ORIGINAL distinct double inverse/right F55 unit
P=X² Type witness numerical values. -/
private abbrev fivefoldGK5CBNorthDoubleValues (r : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval (r : Int)

/-- Both original F55 Type sources have genuine signed
numerical CRT three-cover coherence after TWO arbitrary
polynomial substitutions, and retain existing conditional
arithmetic zero certificates, BUT have OPPOSITE original-phi
structural Type seam verdicts (primitive yes, double no).
Neither numerical polynomial descent implies a new
original F55 Type source nor an unconditional higher cell. -/
theorem fivefoldGK5CBNorthOriginalBothDoubleBindTowersOppositeSeams
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (m p n d : Nat) (indices : Fin n → Nat)
    (h : Fin m → MvPolynomial (Fin p) Int)
    (k : Fin p → MvPolynomial (Fin n) Int)
    (Q : MvPolynomial (Fin m) Int)
    (hbound : 2 ≤ d)
    (hL : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices
            fivefoldGK5CBNorthPrimitiveValues
            ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))))) =
      nativeGK5BZCompatibleMvEvalHom u moduli
        (fun j => nativeGK5BZCompatibleMvEvalHom u moduli
          (fun l => fivefoldGK5BZNorthLocalMvEval u moduli n d indices
            fivefoldGK5CBNorthPrimitiveValues (k l)) (h j)) Q) ∧
    (nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5BZNorthGlobalMvEval s moduli n d indices
            fivefoldGK5CBNorthDoubleValues
            ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))))) =
      nativeGK5BZCompatibleMvEvalHom u moduli
        (fun j => nativeGK5BZCompatibleMvEvalHom u moduli
          (fun l => fivefoldGK5BZNorthLocalMvEval u moduli n d indices
            fivefoldGK5CBNorthDoubleValues (k l)) (h j)) Q) ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨_, _, hzeroPrim, hzeroDouble, hyes, hno⟩ :=
    fivefoldGK5BZNorthOriginalBothMvTowerButOppositeSeams
      s t u moduli inc inc' n d indices
      ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) Q))
      hbound hL frame i
  exact ⟨fivefoldGK5CBNorthMvCRT_doubleBind_threeCover
      s t u moduli inc inc' m p n d indices
      fivefoldGK5CBNorthPrimitiveValues h k Q,
    fivefoldGK5CBNorthMvCRT_doubleBind_threeCover
      s t u moduli inc inc' m p n d indices
      fivefoldGK5CBNorthDoubleValues h k Q,
    hzeroPrim, hzeroDouble, hyes, hno⟩

#print axioms fivefoldGK5CBNorthSubstitutionCRT_RingHom
#print axioms fivefoldGK5CBNorthGlobalSubstitutionHom_restrict
#print axioms fivefoldGK5CBNorthLocalSubstitutionHom_restrict
#print axioms fivefoldGK5CBNorthMvGlobal_doubleBind
#print axioms fivefoldGK5CBNorthMvLocal_doubleBind
#print axioms fivefoldGK5CBNorthMvSignedDoubleBind_global
#print axioms fivefoldGK5CBNorthMvGlobal_doubleBind_restrict
#print axioms fivefoldGK5CBNorthMvLocal_doubleBind_restrict
#print axioms fivefoldGK5CBNorthMvCRT_doubleBind_threeCover
#print axioms fivefoldGK5CBNorthMvGlobal_rename_doubleBind
#print axioms fivefoldGK5CBNorthMvLocal_rename_doubleBind
#print axioms fivefoldGK5CBNorthMvCRT_rename_doubleBind_threeCover
#print axioms fivefoldGK5CBNorthOriginalBothDoubleBindTowersOppositeSeams

end
end KUOS.Architecture.WuxingPentagonUnified
