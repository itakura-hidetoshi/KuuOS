import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BWFiniteCRTRingEquiv
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.GCDMonoid.Finset
import Mathlib.Tactic

/-!
F112-P94D3GK5BX — FINITE CRT RING DESCENT: RESTRICTION COHERENCE.

GK5BW supplies the genuine ZMod (Finset.lcm moduli) ring
equivalence to all compatible local ZMod residues, including
zero moduli, noncoprime moduli, and empty finite covers.

This new INDEPENDENT Kuu theorem layer proves that actual
finite-cover restrictions preserve the true compatible
subrings as ring homomorphisms, with identity and two-step
composition laws, and similarly for the canonical global
ZMod restriction ring homomorphisms. The true GK5BW
ring equivalences form a NATURAL commuting square; the
inverse CRT reconstruction is natural as well. A tower of
three finite covers yields genuine ring-homomorphism
coherence without selecting any synthetic Type source.

No nonzero, positivity, coprimality, nonempty-cover,
dominating-site, or new original F55 Type existence
assumptions. Numeric CRT descent does NOT produce an
original F55 Type source, P77 equality, P94A four-cell,
global GK5AY structural seam, unconditional P89 reflection,
or W=1→seam. True F54 two Nat/two categories/Blocks and
original F55 Type histories remain distinct authorities.

Strict 空, independent Kuu→Qi, append-only public root107.
Protected #1558 Draft/open/unmerged. Pinned Lean
v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry, admit, native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The actual LCM of any finite subcover divides the LCM
of the original cover, INCLUDING zero moduli and empties. -/
theorem nativeGK5BXFiniteModulus_dvd
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) :
    nativeGK5BUFiniteModulus t moduli ∣
      nativeGK5BUFiniteModulus s moduli := by
  apply Finset.lcm_dvd
  intro i hi
  exact Finset.dvd_lcm (h hi)

/-- The true compatible-local ring restriction between
arbitrary finite original covers; its source and target
are GK5BW's exact compatible-family SUBRINGS. -/
def nativeGK5BXCompatibleRestrictHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) :
    nativeGK5BWCompatibleSubring s moduli →+*
      nativeGK5BWCompatibleSubring t moduli where
  toFun a :=
    ⟨fun i => a.1 ⟨i.1, h i.2⟩, by
      intro i j
      exact a.2 ⟨i.1, h i.2⟩ ⟨j.1, h j.2⟩⟩
  map_zero' := by
    apply Subtype.ext
    funext i
    rfl
  map_one' := by
    apply Subtype.ext
    funext i
    rfl
  map_add' := by
    intro a b
    apply Subtype.ext
    funext i
    rfl
  map_mul' := by
    intro a b
    apply Subtype.ext
    funext i
    rfl

/-- The identity finite cover restriction acts identically
on ALL original compatible ZMod local residues. -/
theorem nativeGK5BXCompatibleRestrict_id_apply
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (a : nativeGK5BWCompatibleSubring s moduli) :
    nativeGK5BXCompatibleRestrictHom s s moduli (fun _ hi => hi) a = a := by
  apply Subtype.ext
  funext i
  rfl

/-- True compositionality of two nested finite cover
restrictions, pointwise for EVERY compatible family. -/
theorem nativeGK5BXCompatibleRestrict_comp_apply
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (a : nativeGK5BWCompatibleSubring s moduli) :
    nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h a) =
    nativeGK5BXCompatibleRestrictHom s u moduli
      (fun i hi => h (k hi)) a := by
  apply Subtype.ext
  funext i
  rfl

/-- The identity law holds as EQUALITY OF RING HOMOMORPHISMS
on the true local compatible-family subring. -/
theorem nativeGK5BXCompatibleRestrict_id
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    nativeGK5BXCompatibleRestrictHom s s moduli (fun _ hi => hi) =
      RingHom.id (nativeGK5BWCompatibleSubring s moduli) := by
  apply RingHom.ext
  intro a
  exact nativeGK5BXCompatibleRestrict_id_apply s moduli a

/-- The two-step composition law holds as EQUALITY OF
TRUE RING HOMOMORPHISMS, not merely functions. -/
theorem nativeGK5BXCompatibleRestrict_comp
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t) :
    (nativeGK5BXCompatibleRestrictHom t u moduli k).comp
      (nativeGK5BXCompatibleRestrictHom s t moduli h) =
    nativeGK5BXCompatibleRestrictHom s u moduli
      (fun i hi => h (k hi)) := by
  apply RingHom.ext
  intro a
  exact nativeGK5BXCompatibleRestrict_comp_apply s t u moduli h k a

/-- The TRUE global ZMod ring restriction induced by
LCM divisibility of arbitrary original finite covers. -/
def nativeGK5BXGlobalRestrictHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) :
    ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      ZMod (nativeGK5BUFiniteModulus t moduli) :=
  ZMod.castHom (nativeGK5BXFiniteModulus_dvd s t moduli h)
    (ZMod (nativeGK5BUFiniteModulus t moduli))

/-- The global CRT quotient restriction respects the
identity finite-cover inclusion, including ZMod 0 = ℤ. -/
theorem nativeGK5BXGlobalRestrict_id
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    nativeGK5BXGlobalRestrictHom s s moduli (fun _ hi => hi) =
      RingHom.id (ZMod (nativeGK5BUFiniteModulus s moduli)) := by
  exact RingHom.ext_zmod _ _

/-- The global CRT quotient restrictions compose
STRICTLY as true ZMod ring homomorphisms. -/
theorem nativeGK5BXGlobalRestrict_comp
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t) :
    (nativeGK5BXGlobalRestrictHom t u moduli k).comp
      (nativeGK5BXGlobalRestrictHom s t moduli h) =
    nativeGK5BXGlobalRestrictHom s u moduli
      (fun i hi => h (k hi)) := by
  exact RingHom.ext_zmod _ _

/-- The GK5BW finite CRT RING EQUIVALENCES satisfy the
natural commuting square AS RING HOMOMORPHISMS on every
finite cover inclusion; not just a chosen global witness. -/
theorem nativeGK5BXCRTNaturalityHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) :
    (nativeGK5BWGlobalCompatibleHom t moduli).comp
      (nativeGK5BXGlobalRestrictHom s t moduli h) =
    (nativeGK5BXCompatibleRestrictHom s t moduli h).comp
      (nativeGK5BWGlobalCompatibleHom s moduli) := by
  exact RingHom.ext_zmod _ _

/-- Pointwise statement of true CRT RING naturality.
It is valid for EVERY GLOBAL ZMod element, not merely
chosen natural representatives, also if LCM is zero. -/
theorem nativeGK5BXCRTNaturality_apply
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli)) :
    nativeGK5BWFiniteCRTRingEquiv t moduli
      (nativeGK5BXGlobalRestrictHom s t moduli h x) =
    nativeGK5BXCompatibleRestrictHom s t moduli h
      (nativeGK5BWFiniteCRTRingEquiv s moduli x) := by
  have hn := congrArg
    (fun f : ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      nativeGK5BWCompatibleSubring t moduli => f x)
    (nativeGK5BXCRTNaturalityHom s t moduli h)
  simpa only [RingHom.comp_apply, nativeGK5BWFiniteCRTRingEquiv_apply] using hn

/-- The INVERSE true CRT ring equivalence respects finite
cover restriction as well, without new Type-valued source
reconstruction, including the signed ZMod 0 case. -/
theorem nativeGK5BXCRTInverseNaturality
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (a : nativeGK5BWCompatibleSubring s moduli) :
    (nativeGK5BWFiniteCRTRingEquiv t moduli).symm
      (nativeGK5BXCompatibleRestrictHom s t moduli h a) =
    nativeGK5BXGlobalRestrictHom s t moduli h
      ((nativeGK5BWFiniteCRTRingEquiv s moduli).symm a) := by
  apply (nativeGK5BWFiniteCRTRingEquiv t moduli).injective
  simpa only [RingEquiv.apply_symm_apply, RingEquiv.apply_symm_apply] using
    (nativeGK5BXCRTNaturality_apply s t moduli h
      ((nativeGK5BWFiniteCRTRingEquiv s moduli).symm a)).symm

/-- A three-cover tower commutes with the actual CRT
ring isomorphisms as ONE equality of RingHom maps,
expressing strict arithmetic descent coherence. -/
theorem nativeGK5BXCRTTowerHom
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t) :
    (nativeGK5BWGlobalCompatibleHom u moduli).comp
      ((nativeGK5BXGlobalRestrictHom t u moduli k).comp
        (nativeGK5BXGlobalRestrictHom s t moduli h)) =
    (nativeGK5BXCompatibleRestrictHom t u moduli k).comp
      ((nativeGK5BXCompatibleRestrictHom s t moduli h).comp
        (nativeGK5BWGlobalCompatibleHom s moduli)) := by
  exact RingHom.ext_zmod _ _

#print axioms nativeGK5BXFiniteModulus_dvd
#print axioms nativeGK5BXCompatibleRestrict_id_apply
#print axioms nativeGK5BXCompatibleRestrict_comp_apply
#print axioms nativeGK5BXCompatibleRestrict_id
#print axioms nativeGK5BXCompatibleRestrict_comp
#print axioms nativeGK5BXGlobalRestrict_id
#print axioms nativeGK5BXGlobalRestrict_comp
#print axioms nativeGK5BXCRTNaturalityHom
#print axioms nativeGK5BXCRTNaturality_apply
#print axioms nativeGK5BXCRTInverseNaturality
#print axioms nativeGK5BXCRTTowerHom

end
end Kuu.F112.Physical
