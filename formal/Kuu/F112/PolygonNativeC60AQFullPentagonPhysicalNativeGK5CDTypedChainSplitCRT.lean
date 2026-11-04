import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CCTypedFiniteSubstitutionCRTNaturality
import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Tactic

/-!
F112-P94D3GK5CD — TRUE ARBITRARY-CUT CONCATENATION OF
HETEROGENEOUS TYPE-CHANGING FINITE POLYNOMIAL SUBSTITUTION CHAINS.

The independently verified GK5CC chain acts on the ACTUAL
variable type α (start+i) at each level i, with a genuine
integer multivariable-polynomial substitution RingHom.
Here we prove that splitting the chain after any finite
number left of stages and composing its two authentic
type-changing segments is exactly the UNSPLIT finite chain,
including every possible right segment length.

The final indices (start+left)+right and start+(left+right)
differ propositionally; we retain their precise Nat.add_assoc
transport rather than silently assuming an ill-typed equality.

Global ZMod L_s evaluation, the true gcd-compatible local
CRT Subring, actual finite noncoprime CRT RingEquiv, and
finite-cover restriction remain the same independent
mathematical objects; no proxy tuple, numerical absolute
value or original F55 Type-value reconstruction.

Strict 空, independent Kuu→Qi; original F54 two Nat, two
categories/Blocks and original F55 Type history preserved.
Public root107, pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 Draft/open/unmerged.
Append-only: no original theorem file modified, no
axiom/sorry/admit/native_decide/Gray/GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

/-- The GENUINE RingHom of two consecutively typed polynomial
substitution segments, transported along Nat.add_assoc to
exactly the source/target types of the corresponding full
finite chain. Neither segment is a numerical proxy. -/
def nativeGK5CDTypedSplitHom
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat) :
    MvPolynomial (α start) Int →+*
      MvPolynomial (α (start + (left + right))) Int :=
  (Nat.add_assoc start left right) ▸
    ((nativeGK5CCTypedChainHom steps (start + left) right).comp
      (nativeGK5CCTypedChainHom steps start left))

/-- Transport of a dependent polynomial RingHom through a
Nat-index equality commutes with the NEXT genuine step.
Proved by equality induction; no numerical proxy or axiom. -/
private theorem nativeGK5CDTransportStep
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start : Nat) {i j : Nat} (h : i = j)
    (g : MvPolynomial (α start) Int →+* MvPolynomial (α i) Int) :
    (congrArg (fun n : Nat => n + 1) h) ▸
      ((nativeGK5CCStepSubstitutionHom steps i).comp g) =
    (nativeGK5CCStepSubstitutionHom steps j).comp (h ▸ g) := by
  cases h
  rfl

/-- Arbitrary-cut finite typed substitution chains concatenate
as EXACTLY the original unsplit RingHom, for ALL lengths,
variable types and polynomial-valued variable maps. -/
theorem nativeGK5CDTypedSplitHom_eq
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat) :
    nativeGK5CDTypedSplitHom steps start left right =
      nativeGK5CCTypedChainHom steps start (left + right) := by
  induction right with
  | zero =>
      simp [nativeGK5CDTypedSplitHom, nativeGK5CCTypedChainHom_zero]
  | succ right ih =>
      have htransport :=
        nativeGK5CDTransportStep steps start
          (Nat.add_assoc start left right)
          ((nativeGK5CCTypedChainHom steps (start+left) right).comp
            (nativeGK5CCTypedChainHom steps start left))
      have hstep :
          nativeGK5CDTypedSplitHom steps start left (right + 1) =
            (nativeGK5CCStepSubstitutionHom steps (start + (left + right))).comp
              (nativeGK5CDTypedSplitHom steps start left right) := by
        simpa only [nativeGK5CDTypedSplitHom,
          nativeGK5CCTypedChainHom_succ, Nat.add_succ] using htransport
      rw [hstep, ih]
      simpa only [Nat.add_succ, nativeGK5CCTypedChainHom_succ]

/-- The initial zero-length segment contributes exactly the
unchanged full chain; its target is indexed by (0 + right).
This is propositionally right, and the dependent target
index is retained rather than silently identified. -/
theorem nativeGK5CDTypedSplitHom_zeroLeft
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start right : Nat) :
    nativeGK5CDTypedSplitHom steps start 0 right =
      nativeGK5CCTypedChainHom steps start (0 + right) :=
  nativeGK5CDTypedSplitHom_eq steps start 0 right

/-- If the RIGHT segment is empty, its composite leaves the
actual left-length typed chain unchanged. -/
theorem nativeGK5CDTypedSplitHom_zeroRight
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left : Nat) :
    nativeGK5CDTypedSplitHom steps start left 0 =
      nativeGK5CCTypedChainHom steps start left := by
  simpa only [Nat.add_zero] using
    (nativeGK5CDTypedSplitHom_eq steps start left 0)

/-- The entire arbitrary-cut composite has the same
genuine global ZMod evaluation as its unsplit chain. -/
theorem nativeGK5CDGlobalSplitEval_eq
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (xs : α (start + (left + right)) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BZGlobalMvEvalHom s moduli xs).comp
      (nativeGK5CDTypedSplitHom steps start left right) =
    nativeGK5CCGlobalChainEvalHom s moduli steps start
      (left + right) xs := by
  rw [nativeGK5CDTypedSplitHom_eq]
  rfl

/-- Exact equality of the split/unsplit RingHom evaluation
in the actual compatible-local finite CRT Subring. -/
theorem nativeGK5CDCompatibleSplitEval_eq
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (as : α (start + (left + right)) →
      nativeGK5BWCompatibleSubring s moduli) :
    (nativeGK5BZCompatibleMvEvalHom s moduli as).comp
      (nativeGK5CDTypedSplitHom steps start left right) =
    nativeGK5CCCompatibleChainEvalHom s moduli steps start
      (left + right) as := by
  rw [nativeGK5CDTypedSplitHom_eq]
  rfl

/-- Original global ZMod evaluation after the real typed cut
and concatenation, retaining a genuine RingHom. -/
def nativeGK5CDGlobalSplitEvalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (xs : α (start + (left + right)) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    MvPolynomial (α start) Int →+*
      ZMod (nativeGK5BUFiniteModulus s moduli) :=
  (nativeGK5BZGlobalMvEvalHom s moduli xs).comp
    (nativeGK5CDTypedSplitHom steps start left right)

/-- Genuine compatible-local CRT subring evaluation after
the original type-changing cut, as an actual RingHom. -/
def nativeGK5CDCompatibleSplitEvalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (as : α (start + (left + right)) →
      nativeGK5BWCompatibleSubring s moduli) :
    MvPolynomial (α start) Int →+*
      nativeGK5BWCompatibleSubring s moduli :=
  (nativeGK5BZCompatibleMvEvalHom s moduli as).comp
    (nativeGK5CDTypedSplitHom steps start left right)

/-- Global ZMod evaluation of any split is the original
whole finite chain as strict RingHom equality. -/
theorem nativeGK5CDGlobalSplitEvalHom_eq
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (xs : α (start + (left + right)) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    nativeGK5CDGlobalSplitEvalHom s moduli steps start left right xs =
      nativeGK5CCGlobalChainEvalHom s moduli steps start
        (left + right) xs :=
  nativeGK5CDGlobalSplitEval_eq s moduli steps start left right xs

/-- Local compatible-subring evaluation of any split
is the original whole chain as a TRUE RingHom equation. -/
theorem nativeGK5CDCompatibleSplitEvalHom_eq
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (as : α (start + (left + right)) →
      nativeGK5BWCompatibleSubring s moduli) :
    nativeGK5CDCompatibleSplitEvalHom s moduli steps start left right as =
      nativeGK5CCCompatibleChainEvalHom s moduli steps start
        (left + right) as :=
  nativeGK5CDCompatibleSplitEval_eq s moduli steps start left right as

/-- The actual GK5BW CRT RingEquiv commutes with the
WHOLE arbitrarily split typed substitution RingHom. -/
theorem nativeGK5CDCRT_Split_naturalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (xs : α (start + (left + right)) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (nativeGK5CDGlobalSplitEvalHom s moduli steps start left right xs) =
    nativeGK5CDCompatibleSplitEvalHom s moduli steps start left right
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v)) := by
  rw [nativeGK5CDGlobalSplitEvalHom_eq,
    nativeGK5CDCompatibleSplitEvalHom_eq]
  exact nativeGK5CCCRTChain_naturalHom s moduli steps start
    (left + right) xs

/-- True global ZMod finite-cover restriction commutes with
every arbitrarily cut typed chain AS RING HOM equality. -/
theorem nativeGK5CDGlobalSplit_restrictHom
    {ι : Type*} {α : Nat → Type u}
    (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (xs : α (start + (left + right)) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXGlobalRestrictHom s t moduli inc).comp
      (nativeGK5CDGlobalSplitEvalHom s moduli steps start left right xs) =
    nativeGK5CDGlobalSplitEvalHom t moduli steps start left right
      (fun v => nativeGK5BXGlobalRestrictHom s t moduli inc (xs v)) := by
  rw [nativeGK5CDGlobalSplitEvalHom_eq,
    nativeGK5CDGlobalSplitEvalHom_eq]
  exact nativeGK5CCGlobalChain_restrictHom s t moduli inc
    steps start (left + right) xs

/-- True compatible-local finite-cover restriction commutes
with the whole arbitrarily cut typed chain as RingHom. -/
theorem nativeGK5CDCompatibleSplit_restrictHom
    {ι : Type*} {α : Nat → Type u}
    (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (as : α (start + (left + right)) →
      nativeGK5BWCompatibleSubring s moduli) :
    (nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
      (nativeGK5CDCompatibleSplitEvalHom s moduli steps start left right as) =
    nativeGK5CDCompatibleSplitEvalHom t moduli steps start left right
      (fun v => nativeGK5BXCompatibleRestrictHom s t moduli inc (as v)) := by
  rw [nativeGK5CDCompatibleSplitEvalHom_eq,
    nativeGK5CDCompatibleSplitEvalHom_eq]
  exact nativeGK5CCCompatibleChain_restrictHom s t moduli inc
    steps start (left + right) as

/-- The COMPLETE genuine three-cover CRT diagram is
strictly commutative for ANY CUT of the heterogeneous
finite substitution chain, as an equality of RingHoms. -/
theorem nativeGK5CDCRT_Split_threeCoverHom
    {ι : Type*} {α : Nat → Type u}
    (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (xs : α (start + (left + right)) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXCompatibleRestrictHom t u' moduli inc').comp
      ((nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
        ((nativeGK5BWGlobalCompatibleHom s moduli).comp
          (nativeGK5CDGlobalSplitEvalHom s moduli steps start left right xs))) =
    nativeGK5CDCompatibleSplitEvalHom u' moduli steps start left right
      (fun v => nativeGK5BWFiniteCRTRingEquiv u' moduli
        (nativeGK5BXGlobalRestrictHom s u' moduli
          (fun j hj => inc (inc' hj)) (xs v))) := by
  rw [nativeGK5CDGlobalSplitEvalHom_eq,
    nativeGK5CDCompatibleSplitEvalHom_eq]
  exact nativeGK5CCCRTChain_threeCoverHom s t u' moduli inc inc'
    steps start (left + right) xs

/-- Any noninjective initial source-variable relabelling
retains the same authentic three-cover CRT gluing even
after an arbitrary split of the whole typed chain. -/
theorem nativeGK5CDCRT_Split_rename_threeCover
    {ι σ : Type*} {α : Nat → Type u}
    (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat) (f : σ → α start)
    (xs : α (start + (left + right)) →
      ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5CDGlobalSplitEvalHom s moduli steps start left right xs
            ((MvPolynomial.rename f) P)))) =
    nativeGK5CDCompatibleSplitEvalHom u' moduli steps start left right
      (fun v => nativeGK5BWFiniteCRTRingEquiv u' moduli
        (nativeGK5BXGlobalRestrictHom s u' moduli
          (fun j hj => inc (inc' hj)) (xs v)))
      ((MvPolynomial.rename f) P) := by
  simpa only [RingHom.comp_apply,
    nativeGK5BWFiniteCRTRingEquiv_apply] using
    (RingHom.congr_fun
      (nativeGK5CDCRT_Split_threeCoverHom s t u' moduli inc inc'
        steps start left right xs)
      ((MvPolynomial.rename f) P))

/-- The original SIGNED Int terminal values can be evaluated
before reduction into the true global CRT quotient for
ANY genuine arbitrary cut and any original polynomial. -/
theorem nativeGK5CDSignedIntSplit_global
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right : Nat)
    (zs : α (start + (left + right)) → Int)
    (P : MvPolynomial (α start) Int) :
    nativeGK5CDGlobalSplitEvalHom s moduli steps start left right
      (fun v => (zs v : ZMod (nativeGK5BUFiniteModulus s moduli))) P =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int) zs
      (nativeGK5CDTypedSplitHom steps start left right P) : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)) := by
  rw [nativeGK5CDGlobalSplitEvalHom_eq,
    nativeGK5CDTypedSplitHom_eq]
  exact nativeGK5CCSignedIntChain_global s moduli steps start
    (left + right) zs P

#print axioms nativeGK5CDTypedSplitHom_eq
#print axioms nativeGK5CDTypedSplitHom_zeroLeft
#print axioms nativeGK5CDTypedSplitHom_zeroRight
#print axioms nativeGK5CDGlobalSplitEval_eq
#print axioms nativeGK5CDCompatibleSplitEval_eq

#print axioms nativeGK5CDGlobalSplitEvalHom_eq
#print axioms nativeGK5CDCompatibleSplitEvalHom_eq
#print axioms nativeGK5CDCRT_Split_naturalHom
#print axioms nativeGK5CDGlobalSplit_restrictHom
#print axioms nativeGK5CDCompatibleSplit_restrictHom
#print axioms nativeGK5CDCRT_Split_threeCoverHom
#print axioms nativeGK5CDCRT_Split_rename_threeCover
#print axioms nativeGK5CDSignedIntSplit_global

end
end Kuu.F112.Physical
