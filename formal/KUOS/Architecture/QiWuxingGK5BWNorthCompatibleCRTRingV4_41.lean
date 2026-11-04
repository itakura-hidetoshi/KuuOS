import KUOS.Architecture.QiWuxingGK5BVNorthGeneralFiniteCRTV4_40
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BWFiniteCRTRingEquiv
import Mathlib.Tactic

/-!
Qi v4.41 — TRUE NORTH C60 SIGNED CRT RING DESCENT AND FINITE
RESTRICTION NATURALITY.

The independent GK5BW result is a genuine ring equivalence:
  ZMod (Finset.lcm moduli) ≃+* compatible original local ZMod families.
Here this actual equivalence is used on ORIGINAL integer
GK5BQ signed numerators, without reducing signs via natAbs.
Finite-cover restriction respects both its canonical ring
maps and the original local source values.

A separate typed theorem retains actual north original F55
primitive/double-inverse seam contrast even while BOTH
numeric sources are representable in the SAME finite CRT
compatible-residue ring and both satisfy existing arithmetic
zero certificates. Numerical gluing never reconstructs
original F55 Type witnesses, P77 equality, P94A four-cells,
universal GK5AY seam, unconditional P89 or W=1→seam.

Strict 空 / independent Kuu→Qi; original F54 two Nat, two
categories/Blocks, original F55 Type-valued history, root
107, and protected validation-only PR #1558 unchanged.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only: new Qi module and one KuuOSFormal import,
no modifications of existing Lean theorem sources.
No axiom, sorry, admit, native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The actual complete finite compatible CRT RING
EQUIVALENCE, including arbitrary zero and overlapping moduli. -/
def fivefoldGK5BWNorthCRTRingEquiv
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    ZMod (nativeGK5BUFiniteModulus s moduli) ≃+*
      nativeGK5BWCompatibleSubring s moduli :=
  nativeGK5BWFiniteCRTRingEquiv s moduli

/-- The TRUE original SIGNED GK5BQ numerator, expressed
in the canonical global ZMod L ring without natAbs. -/
def fivefoldGK5BWNorthSignedGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    ZMod (nativeGK5BUFiniteModulus s moduli) :=
  (nativeGK5BQClearedNumerator d j values : Int)

/-- GENUINE compatible finite local ZMod ring element
of the original signed integer numerator, not a new F55
Type source or a norm-losing replacement. -/
def fivefoldGK5BWNorthSignedRingLocals
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BWCompatibleSubring s moduli :=
  fivefoldGK5BWNorthCRTRingEquiv s moduli
    (fivefoldGK5BWNorthSignedGlobal s moduli d j values)

/-- Every true local ring coordinate is EXACTLY the
original signed integer numerator cast modulo that site. -/
theorem fivefoldGK5BWNorthSignedRingLocals_coordinate
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int)
    (i : {i : ι // i ∈ s}) :
    (fivefoldGK5BWNorthSignedRingLocals s moduli d j values).1 i =
      (nativeGK5BQClearedNumerator d j values : ZMod (moduli i.1)) := by
  change
    (ZMod.cast ((nativeGK5BQClearedNumerator d j values : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) : ZMod (moduli i.1)) =
    (nativeGK5BQClearedNumerator d j values : ZMod (moduli i.1))
  exact ZMod.cast_intCast (Finset.dvd_lcm i.2)
    (nativeGK5BQClearedNumerator d j values)

/-- The signed numeric ring family is genuinely compatible
under all pairwise original gcd-overlap ring maps. -/
theorem fivefoldGK5BWNorthSignedRingLocals_compatible
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BWCompatible s moduli
      (fivefoldGK5BWNorthSignedRingLocals s moduli d j values).1 :=
  (fivefoldGK5BWNorthSignedRingLocals s moduli d j values).2

/-- The inverse ring equivalence reconstructs the
ORIGINAL signed global ZMod L value, not an F55 Type witness. -/
theorem fivefoldGK5BWNorthSignedRingLocals_inverse
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    (fivefoldGK5BWNorthCRTRingEquiv s moduli).symm
        (fivefoldGK5BWNorthSignedRingLocals s moduli d j values) =
      fivefoldGK5BWNorthSignedGlobal s moduli d j values :=
  (fivefoldGK5BWNorthCRTRingEquiv s moduli).left_inv _

/-- The canonical finite LCM is contravariantly divisible
under actual inclusion of original finite local covers. -/
theorem fivefoldGK5BWNorthLCM_dvd_of_subset
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) :
    nativeGK5BUFiniteModulus t moduli ∣
      nativeGK5BUFiniteModulus s moduli := by
  apply Finset.lcm_dvd
  intro i hi
  exact Finset.dvd_lcm (h hi)

/-- A TRUE ring homomorphism restricting local compatible
residues from the larger finite cover to its smaller cover. -/
def fivefoldGK5BWNorthRestrictRingHom
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) :
    nativeGK5BWCompatibleSubring s moduli →+*
      nativeGK5BWCompatibleSubring t moduli where
  toFun a :=
    ⟨fun i => a.1 ⟨i.1, h i.2⟩,
      by
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

/-- The complete CRT RING EQUIVALENCE is natural with
respect to arbitrary finite-cover restriction, including
zero moduli and empty subcovers. -/
theorem fivefoldGK5BWNorthCRTRingEquiv_restrict_natural
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli)) :
    fivefoldGK5BWNorthCRTRingEquiv t moduli
      ((ZMod.castHom (fivefoldGK5BWNorthLCM_dvd_of_subset s t moduli h)
        (ZMod (nativeGK5BUFiniteModulus t moduli))) x) =
      fivefoldGK5BWNorthRestrictRingHom s t moduli h
        (fivefoldGK5BWNorthCRTRingEquiv s moduli x) := by
  apply Subtype.ext
  funext i
  change
    ((ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1))).comp
      (ZMod.castHom (fivefoldGK5BWNorthLCM_dvd_of_subset s t moduli h)
        (ZMod (nativeGK5BUFiniteModulus t moduli)))) x =
    (ZMod.castHom (Finset.dvd_lcm (h i.2))
      (ZMod (moduli i.1))) x
  exact congrArg
    (fun f : ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      ZMod (moduli i.1) => f x)
    (RingHom.ext_zmod _ _)

/-- The ORIGINAL signed numerator coordinates remain
literally the same when a finite original cover is
restricted. This is value-level naturality, not Type descent. -/
theorem fivefoldGK5BWNorthSignedRingLocals_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (d j : Nat) (values : Nat → Int)
    (i : {i : ι // i ∈ t}) :
    (fivefoldGK5BWNorthRestrictRingHom s t moduli h
      (fivefoldGK5BWNorthSignedRingLocals s moduli d j values)).1 i =
      (fivefoldGK5BWNorthSignedRingLocals t moduli d j values).1 i := by
  calc
    (fivefoldGK5BWNorthRestrictRingHom s t moduli h
      (fivefoldGK5BWNorthSignedRingLocals s moduli d j values)).1 i =
        (nativeGK5BQClearedNumerator d j values : ZMod (moduli i.1)) :=
      fivefoldGK5BWNorthSignedRingLocals_coordinate s moduli d j values
        ⟨i.1, h i.2⟩
    _ = (fivefoldGK5BWNorthSignedRingLocals t moduli d j values).1 i :=
      (fivefoldGK5BWNorthSignedRingLocals_coordinate
        t moduli d j values i).symm

/-- Genuine primitive and double-inverse north ORIGINAL
F55 sources share all finite numerical CRT ring descent
capabilities, but their ORIGINAL Type-valued seam verdicts
remain opposite. No numeric arithmetic may erase this. -/
theorem fivefoldGK5BWNorthCRTRingAndOppositeOriginalSeams
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    Nonempty (ZMod (nativeGK5BUFiniteModulus s moduli) ≃+*
      nativeGK5BWCompatibleSubring s moduli) ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨hyes, hno, _, _⟩ :=
    fivefoldGK5BQNorthPhysicalAndP89Boundary frame i
  exact ⟨⟨fivefoldGK5BWNorthCRTRingEquiv s moduli⟩, hyes, hno⟩

/-- Under the SAME finite factorial LCM certificate,
BOTH distinct true F55 north sources have zero arithmetic
CRT glues and inhabit a globally representable compatible
residue ring, but original-phi Type seam judgments differ. -/
theorem fivefoldGK5BWNorthBothFiniteZeroRingButOppositeSeams
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d : Nat) (hbound : 2 ≤ d)
    (hlcm : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    Nonempty (ZMod (nativeGK5BUFiniteModulus s moduli) ≃+*
      nativeGK5BWCompatibleSubring s moduli) ∧
    fivefoldGK5BVNorthFiniteZero s moduli d
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial ∧
    fivefoldGK5BVNorthFiniteZero s moduli d
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨hz1, hz2, hs1, hs2⟩ :=
    fivefoldGK5BVNorthBothFiniteZeroButOppositeSeams
      s moduli d hbound hlcm frame i
  exact ⟨⟨fivefoldGK5BWNorthCRTRingEquiv s moduli⟩,
    hz1, hz2, hs1, hs2⟩

#print axioms fivefoldGK5BWNorthSignedRingLocals_coordinate
#print axioms fivefoldGK5BWNorthSignedRingLocals_compatible
#print axioms fivefoldGK5BWNorthSignedRingLocals_inverse
#print axioms fivefoldGK5BWNorthLCM_dvd_of_subset
#print axioms fivefoldGK5BWNorthCRTRingEquiv_restrict_natural
#print axioms fivefoldGK5BWNorthSignedRingLocals_restrict
#print axioms fivefoldGK5BWNorthCRTRingAndOppositeOriginalSeams
#print axioms fivefoldGK5BWNorthBothFiniteZeroRingButOppositeSeams

end
end KUOS.Architecture.WuxingPentagonUnified
