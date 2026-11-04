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
unchanged full chain at every cut position. -/
theorem nativeGK5CDTypedSplitHom_zeroLeft
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start right : Nat) :
    nativeGK5CDTypedSplitHom steps start 0 right =
      nativeGK5CCTypedChainHom steps start right := by
  simp only [nativeGK5CDTypedSplitHom_eq, Nat.zero_add]

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

#print axioms nativeGK5CDTypedSplitHom_eq
#print axioms nativeGK5CDTypedSplitHom_zeroLeft
#print axioms nativeGK5CDTypedSplitHom_zeroRight
#print axioms nativeGK5CDGlobalSplitEval_eq
#print axioms nativeGK5CDCompatibleSplitEval_eq

end
end Kuu.F112.Physical
