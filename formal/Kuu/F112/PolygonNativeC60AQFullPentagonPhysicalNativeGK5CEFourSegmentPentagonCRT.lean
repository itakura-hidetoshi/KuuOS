import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CDTypedChainSplitCRT
import Mathlib.Tactic

/-!
F112-P94D3GK5CE: genuine four-interval RingHom-level pentagon coherence.
Arbitrary heterogeneous variable types and integer polynomial substitutions.
Five parenthesizations of four positive OR zero Nat lengths are normalized
via true dependent type transport to the same total polynomial RingHom.
Complete CRT RingEquiv and global/local finite-cover restriction inherited
from GK5BW/BX/BZ/CC/CD, including empty cover, ZMod 0, noncoprime moduli.
No higher associator 2-cell, P94A four-cell or reconstructed F55 Type seam
is asserted by this strictly RingHom-level pentagon-shaped comparison.
Strict 空 / independent Kuu→Qi, original F54/F55 Type histories, root107,
pinned Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6;
protected #1558 Draft/open/unmerged. Append-only. No sorry, axiom,
admit, native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe u

/-- A genuine two-part GK5CD chain with explicit dependent
transport from the actual split length to a chosen equal length. -/
def nativeGK5CENormalizedSplitHom
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total) :
    MvPolynomial (α start) Int →+*
      MvPolynomial (α (start+total)) Int :=
  (congrArg (fun n : Nat => start+n) h) ▸
    nativeGK5CDTypedSplitHom steps start left right

/-- At every real cut, the normalized split IS the unsplit
polynomial RingHom. No abstract association axiom is added. -/
theorem nativeGK5CENormalizedSplitHom_eq
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total) :
    nativeGK5CENormalizedSplitHom steps start left right total h =
      nativeGK5CCTypedChainHom steps start total := by
  cases h
  simpa only [nativeGK5CENormalizedSplitHom] using
    (nativeGK5CDTypedSplitHom_eq steps start left right)

/-- The TRUE global ZMod L_s evaluation of a normalized
real typed split, preserving the whole substitution RingHom. -/
def nativeGK5CEGlobalEvalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (xs : α (start+total) → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    MvPolynomial (α start) Int →+*
      ZMod (nativeGK5BUFiniteModulus s moduli) :=
  (nativeGK5BZGlobalMvEvalHom s moduli xs).comp
    (nativeGK5CENormalizedSplitHom steps start left right total h)

/-- The TRUE compatible-local gcd CRT subring evaluation of
the same normalized real type-changing substitution RingHom. -/
def nativeGK5CELocalEvalHom
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (as : α (start+total) → nativeGK5BWCompatibleSubring s moduli) :
    MvPolynomial (α start) Int →+*
      nativeGK5BWCompatibleSubring s moduli :=
  (nativeGK5BZCompatibleMvEvalHom s moduli as).comp
    (nativeGK5CENormalizedSplitHom steps start left right total h)

/-- A global normalized-split evaluator equals the whole
GK5CC evaluation as an actual RingHom equality. -/
theorem nativeGK5CEGlobalEvalHom_eq
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (xs : α (start+total) → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    nativeGK5CEGlobalEvalHom s moduli steps start left right total h xs =
      nativeGK5CCGlobalChainEvalHom s moduli steps start total xs := by
  rw [nativeGK5CEGlobalEvalHom, nativeGK5CENormalizedSplitHom_eq]
  rfl

/-- A local normalized-split evaluator equals the whole
GK5CC compatible-subring evaluation as a RingHom equality. -/
theorem nativeGK5CELocalEvalHom_eq
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (as : α (start+total) → nativeGK5BWCompatibleSubring s moduli) :
    nativeGK5CELocalEvalHom s moduli steps start left right total h as =
      nativeGK5CCCompatibleChainEvalHom s moduli steps start total as := by
  rw [nativeGK5CELocalEvalHom, nativeGK5CENormalizedSplitHom_eq]
  rfl

/-- CRT RingEquiv naturality for every genuine normalized
cut, with no nonzero modulus or coprimality hypothesis. -/
theorem nativeGK5CECRT_normalized
    {ι : Type*} {α : Nat → Type u}
    (s : Finset ι) (moduli : ι → Nat)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (xs : α (start+total) → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (nativeGK5CEGlobalEvalHom s moduli steps start left right total h xs) =
    nativeGK5CELocalEvalHom s moduli steps start left right total h
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v)) := by
  rw [nativeGK5CEGlobalEvalHom_eq, nativeGK5CELocalEvalHom_eq]
  exact nativeGK5CCCRTChain_naturalHom s moduli steps start total xs

/-- Strict true global finite-cover restriction for EVERY
rebracketed, type-transported genuine substitution RingHom. -/
theorem nativeGK5CEGlobal_restrict
    {ι : Type*} {α : Nat → Type u}
    (s t : Finset ι) (moduli : ι → Nat) (inc : t ⊆ s)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (xs : α (start+total) → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXGlobalRestrictHom s t moduli inc).comp
      (nativeGK5CEGlobalEvalHom s moduli steps start left right total h xs) =
    nativeGK5CEGlobalEvalHom t moduli steps start left right total h
      (fun v => nativeGK5BXGlobalRestrictHom s t moduli inc (xs v)) := by
  rw [nativeGK5CEGlobalEvalHom_eq, nativeGK5CEGlobalEvalHom_eq]
  exact nativeGK5CCGlobalChain_restrictHom s t moduli inc steps start total xs

/-- Strict true local compatible-subring restriction for
EVERY normalized heterogeneous substitution RingHom. -/
theorem nativeGK5CELocal_restrict
    {ι : Type*} {α : Nat → Type u}
    (s t : Finset ι) (moduli : ι → Nat) (inc : t ⊆ s)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (as : α (start+total) → nativeGK5BWCompatibleSubring s moduli) :
    (nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
      (nativeGK5CELocalEvalHom s moduli steps start left right total h as) =
    nativeGK5CELocalEvalHom t moduli steps start left right total h
      (fun v => nativeGK5BXCompatibleRestrictHom s t moduli inc (as v)) := by
  rw [nativeGK5CELocalEvalHom_eq, nativeGK5CELocalEvalHom_eq]
  exact nativeGK5CCCompatibleChain_restrictHom s t moduli inc steps start total as

/-- The full three-cover CRT diagram is strictly commutative
for arbitrary normalized genuine type-changing chain splits. -/
theorem nativeGK5CECRT_threeCover
    {ι : Type*} {α : Nat → Type u}
    (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start left right total : Nat) (h : left+right=total)
    (xs : α (start+total) → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXCompatibleRestrictHom t u' moduli inc').comp
      ((nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
        ((nativeGK5BWGlobalCompatibleHom s moduli).comp
          (nativeGK5CEGlobalEvalHom s moduli steps
            start left right total h xs))) =
    nativeGK5CELocalEvalHom u' moduli steps start left right total h
      (fun v => nativeGK5BWFiniteCRTRingEquiv u' moduli
        (nativeGK5BXGlobalRestrictHom s u' moduli
          (fun j hj => inc (inc' hj)) (xs v))) := by
  rw [nativeGK5CEGlobalEvalHom_eq, nativeGK5CELocalEvalHom_eq]
  exact nativeGK5CCCRTChain_threeCoverHom s t u' moduli inc inc'
    steps start total xs


/-- LeftLeftLeft: one genuine top cut of four type-changing chain intervals.
The dependent target is normalized to the common full length. -/
def nativeGK5CEFourLeftLeftLeft
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    MvPolynomial (α start) Int →+*
      MvPolynomial (α (start + (a + (b + (c + d))))) Int :=
  nativeGK5CENormalizedSplitHom steps start
    ((a+b)+c) d (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- LeftLeftLeft equals the actual unsplit typed polynomial RingHom. -/
theorem nativeGK5CEFourLeftLeftLeft_eq
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    nativeGK5CEFourLeftLeftLeft steps start a b c d =
      nativeGK5CCTypedChainHom steps start (a + (b + (c + d))) :=
  nativeGK5CENormalizedSplitHom_eq steps start
    ((a+b)+c) d (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- LeftMiddle: one genuine top cut of four type-changing chain intervals.
The dependent target is normalized to the common full length. -/
def nativeGK5CEFourLeftMiddle
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    MvPolynomial (α start) Int →+*
      MvPolynomial (α (start + (a + (b + (c + d))))) Int :=
  nativeGK5CENormalizedSplitHom steps start
    (a+(b+c)) d (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- LeftMiddle equals the actual unsplit typed polynomial RingHom. -/
theorem nativeGK5CEFourLeftMiddle_eq
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    nativeGK5CEFourLeftMiddle steps start a b c d =
      nativeGK5CCTypedChainHom steps start (a + (b + (c + d))) :=
  nativeGK5CENormalizedSplitHom_eq steps start
    (a+(b+c)) d (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- Middle: one genuine top cut of four type-changing chain intervals.
The dependent target is normalized to the common full length. -/
def nativeGK5CEFourMiddle
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    MvPolynomial (α start) Int →+*
      MvPolynomial (α (start + (a + (b + (c + d))))) Int :=
  nativeGK5CENormalizedSplitHom steps start
    (a+b) (c+d) (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- Middle equals the actual unsplit typed polynomial RingHom. -/
theorem nativeGK5CEFourMiddle_eq
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    nativeGK5CEFourMiddle steps start a b c d =
      nativeGK5CCTypedChainHom steps start (a + (b + (c + d))) :=
  nativeGK5CENormalizedSplitHom_eq steps start
    (a+b) (c+d) (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- RightMiddle: one genuine top cut of four type-changing chain intervals.
The dependent target is normalized to the common full length. -/
def nativeGK5CEFourRightMiddle
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    MvPolynomial (α start) Int →+*
      MvPolynomial (α (start + (a + (b + (c + d))))) Int :=
  nativeGK5CENormalizedSplitHom steps start
    a ((b+c)+d) (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- RightMiddle equals the actual unsplit typed polynomial RingHom. -/
theorem nativeGK5CEFourRightMiddle_eq
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    nativeGK5CEFourRightMiddle steps start a b c d =
      nativeGK5CCTypedChainHom steps start (a + (b + (c + d))) :=
  nativeGK5CENormalizedSplitHom_eq steps start
    a ((b+c)+d) (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- RightRight: one genuine top cut of four type-changing chain intervals.
The dependent target is normalized to the common full length. -/
def nativeGK5CEFourRightRight
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    MvPolynomial (α start) Int →+*
      MvPolynomial (α (start + (a + (b + (c + d))))) Int :=
  nativeGK5CENormalizedSplitHom steps start
    a (b+(c+d)) (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- RightRight equals the actual unsplit typed polynomial RingHom. -/
theorem nativeGK5CEFourRightRight_eq
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    nativeGK5CEFourRightRight steps start a b c d =
      nativeGK5CCTypedChainHom steps start (a + (b + (c + d))) :=
  nativeGK5CENormalizedSplitHom_eq steps start
    a (b+(c+d)) (a + (b + (c + d))) (by simp only [Nat.add_assoc])

/-- The five parenthesizations form a strictly coherent
pentagon-shaped RingHom equality boundary. This does not
construct categorical higher associator or four-cell data. -/
theorem nativeGK5CEFourPentagon_boundary
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    (nativeGK5CEFourLeftLeftLeft steps start a b c d =
      nativeGK5CEFourLeftMiddle steps start a b c d) ∧
    (nativeGK5CEFourLeftMiddle steps start a b c d =
      nativeGK5CEFourMiddle steps start a b c d) ∧
    (nativeGK5CEFourMiddle steps start a b c d =
      nativeGK5CEFourRightMiddle steps start a b c d) ∧
    (nativeGK5CEFourRightMiddle steps start a b c d =
      nativeGK5CEFourRightRight steps start a b c d) ∧
    (nativeGK5CEFourRightRight steps start a b c d =
      nativeGK5CEFourLeftLeftLeft steps start a b c d) := by
  have h0 := nativeGK5CEFourLeftLeftLeft_eq steps start a b c d
  have h1 := nativeGK5CEFourLeftMiddle_eq steps start a b c d
  have h2 := nativeGK5CEFourMiddle_eq steps start a b c d
  have h3 := nativeGK5CEFourRightMiddle_eq steps start a b c d
  have h4 := nativeGK5CEFourRightRight_eq steps start a b c d
  exact ⟨h0.trans h1.symm, h1.trans h2.symm,
    h2.trans h3.symm, h3.trans h4.symm, h4.trans h0.symm⟩

/-- The leftmost four-interval parenthesization obeys the
actual full three-cover CRT square as a RingHom equation. -/
theorem nativeGK5CEFourLeftLeftLeftCRT_threeCover
    {ι : Type*} {α : Nat → Type u}
    (s t u' : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u' ⊆ t)
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat)
    (xs : α (start + (a + (b + (c + d)))) →
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXCompatibleRestrictHom t u' moduli inc').comp
      ((nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
        ((nativeGK5BWGlobalCompatibleHom s moduli).comp
          ((nativeGK5BZGlobalMvEvalHom s moduli xs).comp
            (nativeGK5CEFourLeftLeftLeft steps start a b c d)))) =
    (nativeGK5BZCompatibleMvEvalHom u' moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv u' moduli
        (nativeGK5BXGlobalRestrictHom s u' moduli
          (fun j hj => inc (inc' hj)) (xs v)))).comp
      (nativeGK5CEFourLeftLeftLeft steps start a b c d) := by
  rw [nativeGK5CEFourLeftLeftLeft_eq]
  exact nativeGK5CCCRTChain_threeCoverHom s t u' moduli inc inc'
    steps start (a + (b + (c + d))) xs

#print axioms nativeGK5CENormalizedSplitHom_eq
#print axioms nativeGK5CEGlobalEvalHom_eq
#print axioms nativeGK5CELocalEvalHom_eq
#print axioms nativeGK5CECRT_normalized
#print axioms nativeGK5CEGlobal_restrict
#print axioms nativeGK5CELocal_restrict
#print axioms nativeGK5CECRT_threeCover
#print axioms nativeGK5CEFourLeftLeftLeft_eq
#print axioms nativeGK5CEFourLeftMiddle_eq
#print axioms nativeGK5CEFourMiddle_eq
#print axioms nativeGK5CEFourRightMiddle_eq
#print axioms nativeGK5CEFourRightRight_eq
#print axioms nativeGK5CEFourPentagon_boundary
#print axioms nativeGK5CEFourLeftLeftLeftCRT_threeCover

end
end Kuu.F112.Physical
