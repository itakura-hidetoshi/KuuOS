import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CBIteratedSubstitutionCRTTower
import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Algebra.MvPolynomial.Rename
import Mathlib.Tactic

/-!
F112-P94D3GK5CC — ARBITRARY FINITE LENGTH, HETEROGENEOUS
TYPED MULTIVARIABLE INTEGER-POLYNOMIAL SUBSTITUTION
CHAINS AND TRUE FINITE NONCOPRIME CRT DESCENT.

The variable type at depth i is an ACTUAL type alpha i;
the transition at each depth is an ACTUAL polynomial-valued
map alpha i -> MvPolynomial (alpha (i+1)) Int. We fold
arbitrary finite lengths to a REAL RingHom from the source
polynomial ring into the terminal polynomial ring, rather
than merely postulating an associative numerical evaluator.
The types may differ at every step, may be empty, and
no substitution, injectivity, nonzero modulus, coprimality,
or polynomial degree assumption is introduced.

The genuine global ZMod (LCM s) and compatible-local
dependent-product CRT Subring receive these chains through
their already formally verified GK5BZ RingHom evaluations.
The genuine GK5BW CRT RingEquiv, GK5BX finite cover
restrictions, and three-cover gluing commute with the
ENTIRE arbitrary-length typed chain AS RING HOM equations.
Stepwise induction equations and original SIGNED Int
evaluation-before-quotient are included. An arbitrary
noninjective initial variable reclassification may precede
the entire chain without changing the CRT square.

All of these are NUMERIC polynomial/CRT statements, NOT
original F55 Type source reconstruction, P77 equality,
P94A four-cell, unconditional P89 reflection, universal
GK5AY seam, or W=1 -> seam. Strict 空, independent Kuu
to Qi, true F54 two Nat/two categories/Blocks and original
F55 Type source history remain authoritative separately.

Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6,
public root107; protected validation-only #1558
Draft/open/unmerged. Append-only, no axiom/sorry/admit/
native_decide/Gray/GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

/-- One transition changes the genuine polynomial-variable
TYPE, not just its data presentation. -/
def nativeGK5CCStepSubstitutionHom
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (i : Nat) :
    MvPolynomial (α i) Int →+* MvPolynomial (α (i + 1)) Int :=
  nativeGK5CBSubstitutionRingHom (steps i)

/-- Fold a FINITE, arbitrarily long sequence of GENUINE
type-changing polynomial substitutions to one RingHom.
At level i the variables are alpha i, and at level i+1
they are alpha (i+1); each index can be a distinct Type. -/
def nativeGK5CCTypedChainHom
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start : Nat) :
    (length : Nat) →
      MvPolynomial (α start) Int →+*
        MvPolynomial (α (start + length)) Int
  | 0 => RingHom.id _
  | length + 1 =>
      (nativeGK5CCStepSubstitutionHom steps (start + length)).comp
        (nativeGK5CCTypedChainHom steps start length)

/-- The length-zero substitution chain is exactly the
identity RingHom on its ACTUAL original variable type. -/
theorem nativeGK5CCTypedChainHom_zero
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start : Nat) :
    nativeGK5CCTypedChainHom steps start 0 =
      RingHom.id (MvPolynomial (α start) Int) :=
  rfl

/-- The successor step appends the ACTUAL type-changing
polynomial substitution RingHom, with no coherence axiom. -/
theorem nativeGK5CCTypedChainHom_succ
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat) :
    nativeGK5CCTypedChainHom steps start (length + 1) =
      (nativeGK5CCStepSubstitutionHom steps (start + length)).comp
        (nativeGK5CCTypedChainHom steps start length) :=
  rfl

/-- Evaluate the entire typed finite substitution chain in
the ACTUAL global ZMod finite noncoprime CRT residue ring,
AS A RING HOM. -/
def nativeGK5CCGlobalChainEvalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (xs : α (start + length) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    MvPolynomial (α start) Int →+*
      ZMod (nativeGK5BUFiniteModulus s moduli) :=
  (nativeGK5BZGlobalMvEvalHom s moduli xs).comp
    (nativeGK5CCTypedChainHom steps start length)

/-- Evaluate the same genuine finite chain in the ACTUAL
gcd-compatible local CRT dependent-product Subring. -/
def nativeGK5CCCompatibleChainEvalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (as : α (start + length) → nativeGK5BWCompatibleSubring s moduli) :
    MvPolynomial (α start) Int →+*
      nativeGK5BWCompatibleSubring s moduli :=
  (nativeGK5BZCompatibleMvEvalHom s moduli as).comp
    (nativeGK5CCTypedChainHom steps start length)

/-- At length zero, original global typed chain evaluation
is exactly the GK5BZ original multivariable RingHom. -/
theorem nativeGK5CCGlobalChainEvalHom_zero
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start : Nat)
    (xs : α start → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    nativeGK5CCGlobalChainEvalHom s moduli steps start 0 xs =
      nativeGK5BZGlobalMvEvalHom s moduli xs := by
  apply RingHom.ext
  intro P
  rfl

/-- At length zero, compatible-local typed chain evaluation
is precisely the original GK5BZ local RingHom. -/
theorem nativeGK5CCCompatibleChainEvalHom_zero
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start : Nat)
    (as : α start → nativeGK5BWCompatibleSubring s moduli) :
    nativeGK5CCCompatibleChainEvalHom s moduli steps start 0 as =
      nativeGK5BZCompatibleMvEvalHom s moduli as := by
  apply RingHom.ext
  intro P
  rfl

/-- The typed chain evaluates recursively: first perform
length substitutions, then evaluate each substituted
variable of the final step in the actual GLOBAL ZMod ring. -/
theorem nativeGK5CCGlobalChainEval_succ
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (xs : α (start + (length + 1)) →
      ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial (α start) Int) :
    nativeGK5CCGlobalChainEvalHom s moduli steps start (length + 1) xs P =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun v => nativeGK5BZGlobalMvEvalHom s moduli xs
        (steps (start + length) v))
      (nativeGK5CCTypedChainHom steps start length P) := by
  change
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.bind₁ (steps (start + length)))
        (nativeGK5CCTypedChainHom steps start length P)) = _
  exact nativeGK5CAGlobalMvEval_bind s moduli xs
    (steps (start + length))
    (nativeGK5CCTypedChainHom steps start length P)

/-- Identical arbitrary-length successor recursion IN THE
TRUE compatible-local CRT Subring, not a proxy tuple. -/
theorem nativeGK5CCCompatibleChainEval_succ
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (as : α (start + (length + 1)) →
      nativeGK5BWCompatibleSubring s moduli)
    (P : MvPolynomial (α start) Int) :
    nativeGK5CCCompatibleChainEvalHom s moduli steps
      start (length + 1) as P =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BZCompatibleMvEvalHom s moduli as
        (steps (start + length) v))
      (nativeGK5CCTypedChainHom steps start length P) := by
  change
    nativeGK5BZCompatibleMvEvalHom s moduli as
      ((MvPolynomial.bind₁ (steps (start + length)))
        (nativeGK5CCTypedChainHom steps start length P)) = _
  exact nativeGK5CACompatibleMvEval_bind s moduli as
    (steps (start + length))
    (nativeGK5CCTypedChainHom steps start length P)

/-- For ALL finite lengths, the genuine complete noncoprime
CRT RingEquiv commutes with the entire typed substitution
chain AS A STRICT EQUALITY OF RING HOMOMORPHISMS. -/
theorem nativeGK5CCCRTChain_naturalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (xs : α (start + length) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (nativeGK5CCGlobalChainEvalHom s moduli steps
        start length xs) =
    nativeGK5CCCompatibleChainEvalHom s moduli steps start length
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v)) := by
  apply RingHom.ext
  intro P
  simpa only [RingHom.comp_apply, nativeGK5CCGlobalChainEvalHom,
    nativeGK5CCCompatibleChainEvalHom,
    nativeGK5BWFiniteCRTRingEquiv_apply] using
    (nativeGK5BZCRTMvEval_apply s moduli xs
      (nativeGK5CCTypedChainHom steps start length P))

/-- Every original GLOBAL finite-cover restriction
commutes with the WHOLE arbitrary finite typed chain
as an equation of genuine RING HOMOMORPHISMS. -/
theorem nativeGK5CCGlobalChain_restrictHom
    {ι : Type*} {α : Nat → Type u}
    (s t : Finset ι) (moduli : ι → Nat) (inc : t ⊆ s)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (xs : α (start + length) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXGlobalRestrictHom s t moduli inc).comp
      (nativeGK5CCGlobalChainEvalHom s moduli steps start length xs) =
    nativeGK5CCGlobalChainEvalHom t moduli steps start length
      (fun v => nativeGK5BXGlobalRestrictHom s t moduli inc (xs v)) := by
  apply RingHom.ext
  intro P
  simpa only [RingHom.comp_apply, nativeGK5CCGlobalChainEvalHom] using
    (nativeGK5BZGlobalMvEval_restrict s t moduli inc xs
      (nativeGK5CCTypedChainHom steps start length P))

/-- Every TRUE compatible-local finite-cover restriction
commutes with the whole type-changing finite substitution
chain AS AN EQUALITY OF RING HOMOMORPHISMS. -/
theorem nativeGK5CCCompatibleChain_restrictHom
    {ι : Type*} {α : Nat → Type u}
    (s t : Finset ι) (moduli : ι → Nat) (inc : t ⊆ s)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (as : α (start + length) → nativeGK5BWCompatibleSubring s moduli) :
    (nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
      (nativeGK5CCCompatibleChainEvalHom s moduli steps start length as) =
    nativeGK5CCCompatibleChainEvalHom t moduli steps start length
      (fun v => nativeGK5BXCompatibleRestrictHom s t moduli inc (as v)) := by
  apply RingHom.ext
  intro P
  simpa only [RingHom.comp_apply, nativeGK5CCCompatibleChainEvalHom] using
    (nativeGK5BZCompatibleMvEval_restrict s t moduli inc as
      (nativeGK5CCTypedChainHom steps start length P))

/-- The complete three-cover noncoprime CRT diagram
commutes for ANY FINITE LENGTH of ACTUAL type-changing
polynomial substitutions, as a strict RingHom equation. -/
theorem nativeGK5CCCRTChain_threeCoverHom
    {ι : Type*} {α : Nat → Type u}
    (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (xs : α (start + length) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXCompatibleRestrictHom t u' moduli inc').comp
      ((nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
        ((nativeGK5BWGlobalCompatibleHom s moduli).comp
          (nativeGK5CCGlobalChainEvalHom s moduli
            steps start length xs))) =
    nativeGK5CCCompatibleChainEvalHom u' moduli steps start length
      (fun v => nativeGK5BWFiniteCRTRingEquiv u' moduli
        (nativeGK5BXGlobalRestrictHom s u' moduli
          (fun j hj => inc (inc' hj)) (xs v))) := by
  apply RingHom.ext
  intro P
  have htower :=
    nativeGK5BZMultivariableCRTTower_natural s t u' moduli
      inc inc' xs (nativeGK5CCTypedChainHom steps start length P)
  have hcrt :=
    nativeGK5BZCRTMvEval_apply u' moduli
      (fun v => nativeGK5BXGlobalRestrictHom s u' moduli
        (fun j hj => inc (inc' hj)) (xs v))
      (nativeGK5CCTypedChainHom steps start length P)
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv u' moduli
          (nativeGK5BZGlobalMvEvalHom u' moduli
            (fun v => nativeGK5BXGlobalRestrictHom s u' moduli
              (fun j hj => inc (inc' hj)) (xs v))
            (nativeGK5CCTypedChainHom steps start length P)) := by
        simpa only [RingHom.comp_apply, nativeGK5CCGlobalChainEvalHom,
          nativeGK5BWFiniteCRTRingEquiv_apply] using htower
    _ = _ := by
        simpa only [RingHom.comp_apply, nativeGK5CCCompatibleChainEvalHom,
          nativeGK5BWFiniteCRTRingEquiv_apply] using hcrt

/-- The same true CRT three-cover commuting square holds
when an arbitrary (even NONINJECTIVE) variable
reclassification precedes the complete typed chain. -/
theorem nativeGK5CCCRTRenameChain_threeCover
    {ι σ : Type*} {α : Nat → Type u}
    (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat) (f : σ → α start)
    (xs : α (start + length) →
      ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom t u' moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5CCGlobalChainEvalHom s moduli
            steps start length xs ((MvPolynomial.rename f) P)))) =
    nativeGK5CCCompatibleChainEvalHom u' moduli steps start length
      (fun v => nativeGK5BWFiniteCRTRingEquiv u' moduli
        (nativeGK5BXGlobalRestrictHom s u' moduli
          (fun j hj => inc (inc' hj)) (xs v)))
      ((MvPolynomial.rename f) P) := by
  simpa only [RingHom.comp_apply,
    nativeGK5BWFiniteCRTRingEquiv_apply] using
    (RingHom.congr_fun
      (nativeGK5CCCRTChain_threeCoverHom s t u' moduli
        inc inc' steps start length xs)
      ((MvPolynomial.rename f) P))

/-- Original SIGNED integer terminal variables can be
evaluated in Int BEFORE taking the genuine global ZMod
residue class even after an arbitrary typed finite chain.
This includes the modulus-zero identity ZMod 0 = Int. -/
theorem nativeGK5CCSignedIntChain_global
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i + 1)) Int)
    (start length : Nat)
    (zs : α (start + length) → Int)
    (P : MvPolynomial (α start) Int) :
    nativeGK5CCGlobalChainEvalHom s moduli steps start length
      (fun v => (zs v : ZMod (nativeGK5BUFiniteModulus s moduli))) P =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int) zs
      (nativeGK5CCTypedChainHom steps start length P) : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5BZSignedIntMvEval_global s moduli zs
    (nativeGK5CCTypedChainHom steps start length P)

#print axioms nativeGK5CCTypedChainHom_zero
#print axioms nativeGK5CCTypedChainHom_succ
#print axioms nativeGK5CCGlobalChainEvalHom_zero
#print axioms nativeGK5CCCompatibleChainEvalHom_zero
#print axioms nativeGK5CCGlobalChainEval_succ
#print axioms nativeGK5CCCompatibleChainEval_succ
#print axioms nativeGK5CCCRTChain_naturalHom
#print axioms nativeGK5CCGlobalChain_restrictHom
#print axioms nativeGK5CCCompatibleChain_restrictHom
#print axioms nativeGK5CCCRTChain_threeCoverHom
#print axioms nativeGK5CCCRTRenameChain_threeCover
#print axioms nativeGK5CCSignedIntChain_global

end
end Kuu.F112.Physical
