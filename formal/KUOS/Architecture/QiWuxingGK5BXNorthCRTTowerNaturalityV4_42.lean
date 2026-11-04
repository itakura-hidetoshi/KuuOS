import KUOS.Architecture.QiWuxingGK5BWNorthCompatibleCRTRingV4_41
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BXFiniteCRTRestrictionCoherence
import Mathlib.Tactic

/-!
Qi v4.42 — TRUE NORTH C60 SIGNED CRT TOWER NATURALITY.

Independent GK5BX proves identity, composition and naturality
of genuine finite compatible CRT RingHom restriction maps,
for arbitrary original Nat moduli, INCLUDING ZERO moduli
(ZMod 0 = ℤ) and empty covers.

This Qi integration preserves the SAME original GK5BQ
SIGNED Int source numerator, and proves that its actual
global ZMod and compatible local ZMod observations survive
every finite restriction and TWO consecutive restrictions.
It connects the three-cover numerical tower to both actual
original north F55 Type sources (primitive P=1 and genuine
double-inverse/right-unit P=X²), whose original-phi seam
judgments remain OPPOSITE despite coherent arithmetic
descent and both existing finite CRT-zero certificates.

Numerical finite-cover presheaf coherence ≠ structural F55
Type source reconstruction, P77 class equality, P94A
four-cells, unconditional P89 reflection, universal GK5AY
seam or W=1→seam. True original F54 two Nat/two categories/
Blocks and F55 Type histories are unchanged.

Strict 空; independent Kuu→Qi, original C60 fifth-around
physical gauge; append-only public root107. Protected
#1558 remains Draft/open/unmerged. Pinned Lean
v4.30.0-rc2/mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No axioms, sorry/admit/native_decide, Gray or GK5BA kit.
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

/-- The genuine original north C60 compatible CRT local
ring system obeys the identity finite-cover restriction
law as an equality of RingHom morphisms. -/
theorem fivefoldGK5BXNorthLocalRestrict_id
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    nativeGK5BXCompatibleRestrictHom s s moduli (fun _ hi => hi) =
      RingHom.id (nativeGK5BWCompatibleSubring s moduli) :=
  nativeGK5BXCompatibleRestrict_id s moduli

/-- The true local compatible CRT ring restriction maps
compose strictly across any three original finite covers. -/
theorem fivefoldGK5BXNorthLocalRestrict_comp
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t) :
    (nativeGK5BXCompatibleRestrictHom t u moduli k).comp
      (nativeGK5BXCompatibleRestrictHom s t moduli h) =
    nativeGK5BXCompatibleRestrictHom s u moduli (fun i hi => h (k hi)) :=
  nativeGK5BXCompatibleRestrict_comp s t u moduli h k

/-- Genuine global ZMod(L) cover restrictions obey the
identity law even for ZMod 0 and an empty original cover. -/
theorem fivefoldGK5BXNorthGlobalRestrict_id
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    nativeGK5BXGlobalRestrictHom s s moduli (fun _ hi => hi) =
      RingHom.id (ZMod (nativeGK5BUFiniteModulus s moduli)) :=
  nativeGK5BXGlobalRestrict_id s moduli

/-- Genuine global ZMod(L) cover restrictions compose
strictly as real RingHom maps, without numerical or
Type-valued source-existence hypotheses. -/
theorem fivefoldGK5BXNorthGlobalRestrict_comp
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t) :
    (nativeGK5BXGlobalRestrictHom t u moduli k).comp
      (nativeGK5BXGlobalRestrictHom s t moduli h) =
    nativeGK5BXGlobalRestrictHom s u moduli (fun i hi => h (k hi)) :=
  nativeGK5BXGlobalRestrict_comp s t u moduli h k

/-- The authentic north arithmetic CRT ring equivalence
forms a natural isomorphism of the two finite-cover
restriction systems, expressed as a RingHom equality. -/
theorem fivefoldGK5BXNorthCRT_RingHom_natural
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) :
    (nativeGK5BWGlobalCompatibleHom t moduli).comp
      (nativeGK5BXGlobalRestrictHom s t moduli h) =
    (nativeGK5BXCompatibleRestrictHom s t moduli h).comp
      (nativeGK5BWGlobalCompatibleHom s moduli) :=
  nativeGK5BXCRTNaturalityHom s t moduli h

/-- Inverse reconstruction of all genuine compatible
local residues commutes with each finite restriction. -/
theorem fivefoldGK5BXNorthCRT_inverse_natural
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (a : nativeGK5BWCompatibleSubring s moduli) :
    (fivefoldGK5BWNorthCRTRingEquiv t moduli).symm
      (nativeGK5BXCompatibleRestrictHom s t moduli h a) =
    nativeGK5BXGlobalRestrictHom s t moduli h
      ((fivefoldGK5BWNorthCRTRingEquiv s moduli).symm a) :=
  nativeGK5BXCRTInverseNaturality s t moduli h a

/-- The ORIGINAL SIGNED GK5BQ numerator, not its natAbs,
is stable under restriction on the global ZMod rings. -/
theorem fivefoldGK5BXNorthSignedGlobal_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (d j : Nat) (values : Nat → Int) :
    nativeGK5BXGlobalRestrictHom s t moduli h
      (fivefoldGK5BWNorthSignedGlobal s moduli d j values) =
    fivefoldGK5BWNorthSignedGlobal t moduli d j values := by
  change
    (ZMod.cast ((nativeGK5BQClearedNumerator d j values : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) :
      ZMod (nativeGK5BUFiniteModulus t moduli)) =
    (nativeGK5BQClearedNumerator d j values :
      ZMod (nativeGK5BUFiniteModulus t moduli))
  exact ZMod.cast_intCast
    (nativeGK5BXFiniteModulus_dvd s t moduli h)
    (nativeGK5BQClearedNumerator d j values)

/-- The same true signed GK5BQ source numerator's entire
compatible LOCAL ring residue family is stable under
finite-cover restriction, not only a single coordinate. -/
theorem fivefoldGK5BXNorthSignedLocals_restrict
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (d j : Nat) (values : Nat → Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli h
      (fivefoldGK5BWNorthSignedRingLocals s moduli d j values) =
    fivefoldGK5BWNorthSignedRingLocals t moduli d j values := by
  apply Subtype.ext
  funext i
  change
    (fivefoldGK5BWNorthSignedRingLocals s moduli d j values).1
      ⟨i.1, h i.2⟩ =
    (fivefoldGK5BWNorthSignedRingLocals t moduli d j values).1 i
  calc
    _ = (nativeGK5BQClearedNumerator d j values : ZMod (moduli i.1)) :=
      fivefoldGK5BWNorthSignedRingLocals_coordinate
        s moduli d j values ⟨i.1, h i.2⟩
    _ = _ :=
      (fivefoldGK5BWNorthSignedRingLocals_coordinate
        t moduli d j values i).symm

/-- TWO consecutive global finite restrictions of the SAME
signed numerator equal the true original signed residue
observed directly on the smallest cover. -/
theorem fivefoldGK5BXNorthSignedGlobal_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BXGlobalRestrictHom t u moduli k
      (nativeGK5BXGlobalRestrictHom s t moduli h
        (fivefoldGK5BWNorthSignedGlobal s moduli d j values)) =
    fivefoldGK5BWNorthSignedGlobal u moduli d j values := by
  calc
    _ = nativeGK5BXGlobalRestrictHom t u moduli k
          (fivefoldGK5BWNorthSignedGlobal t moduli d j values) :=
      congrArg (nativeGK5BXGlobalRestrictHom t u moduli k)
        (fivefoldGK5BXNorthSignedGlobal_restrict s t moduli h d j values)
    _ = _ := fivefoldGK5BXNorthSignedGlobal_restrict t u moduli k d j values

/-- TWO consecutive compatible-local finite restrictions
of the SAME actual SIGNED source values equal the directly
observed local family on the smallest cover. -/
theorem fivefoldGK5BXNorthSignedLocals_tower
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BWNorthSignedRingLocals s moduli d j values)) =
    fivefoldGK5BWNorthSignedRingLocals u moduli d j values := by
  calc
    _ = nativeGK5BXCompatibleRestrictHom t u moduli k
          (fivefoldGK5BWNorthSignedRingLocals t moduli d j values) :=
      congrArg (nativeGK5BXCompatibleRestrictHom t u moduli k)
        (fivefoldGK5BXNorthSignedLocals_restrict s t moduli h d j values)
    _ = _ := fivefoldGK5BXNorthSignedLocals_restrict t u moduli k d j values

/-- Every valid finite factorial-LCM CRT zero certificate
descends to all finite SUBCOVERS by true LCM divisibility,
without strengthening the polynomial degree assumption. -/
theorem fivefoldGK5BXNorthIntegerPolynomialZero_subcover
    {ι : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (P : Polynomial Int) (d : Nat)
    (hdegree : P.natDegree ≤ d)
    (hL : nativeGK5BUFiniteModulus s moduli ∣ d.factorial) :
    fivefoldGK5BVNorthFiniteZero t moduli d P :=
  fivefoldGK5BVIntegerSource_finiteZero t moduli P d hdegree
    ((nativeGK5BXFiniteModulus_dvd s t moduli h).trans hL)

/-- True original north F55 primitive P=1 polynomial
VALUES; this is NOT a new F55 source or Type witness. -/
private abbrev fivefoldGK5BXNorthPrimitiveValues (n : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval (n : Int)

/-- The distinct actual north F55 double-inverse/right
unit P=X² polynomial VALUES, with unchanged Type history. -/
private abbrev fivefoldGK5BXNorthDoubleValues (n : Nat) : Int :=
  (nativeGK5AIOriginalToP92Structural
    fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval (n : Int)

/-- Both TRUE original north F55 polynomial values have
coherent two-step SIGNED numeric CRT ring restrictions.
For the SAME finite-cover factorial divisibility certificate,
both remain CRT-zero at the smallest cover, yet their TRUE
original-phi STRUCTURAL SEAMS still differ (yes vs no).
Arithmetic gluing never recovers missing F55 Type history. -/
theorem fivefoldGK5BXNorthOriginalBothTowerButOppositeSeams
    {ι : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (d j : Nat) (hbound : 2 ≤ d)
    (hL : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BWNorthSignedRingLocals
          s moduli d j fivefoldGK5BXNorthPrimitiveValues)) =
      fivefoldGK5BWNorthSignedRingLocals
        u moduli d j fivefoldGK5BXNorthPrimitiveValues) ∧
    (nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (fivefoldGK5BWNorthSignedRingLocals
          s moduli d j fivefoldGK5BXNorthDoubleValues)) =
      fivefoldGK5BWNorthSignedRingLocals
        u moduli d j fivefoldGK5BXNorthDoubleValues) ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial ∧
    fivefoldGK5BVNorthFiniteZero u moduli d
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  have hLu : nativeGK5BUFiniteModulus u moduli ∣ d.factorial :=
    (nativeGK5BXFiniteModulus_dvd s u moduli
      (fun a ha => h (k ha))).trans hL
  obtain ⟨_, hz1, hz2, hyes, hno⟩ :=
    fivefoldGK5BWNorthBothFiniteZeroRingButOppositeSeams
      u moduli d hbound hLu frame i
  exact ⟨fivefoldGK5BXNorthSignedLocals_tower
      s t u moduli h k d j fivefoldGK5BXNorthPrimitiveValues,
    fivefoldGK5BXNorthSignedLocals_tower
      s t u moduli h k d j fivefoldGK5BXNorthDoubleValues,
    hz1, hz2, hyes, hno⟩

#print axioms fivefoldGK5BXNorthLocalRestrict_id
#print axioms fivefoldGK5BXNorthLocalRestrict_comp
#print axioms fivefoldGK5BXNorthGlobalRestrict_id
#print axioms fivefoldGK5BXNorthGlobalRestrict_comp
#print axioms fivefoldGK5BXNorthCRT_RingHom_natural
#print axioms fivefoldGK5BXNorthCRT_inverse_natural
#print axioms fivefoldGK5BXNorthSignedGlobal_restrict
#print axioms fivefoldGK5BXNorthSignedLocals_restrict
#print axioms fivefoldGK5BXNorthSignedGlobal_tower
#print axioms fivefoldGK5BXNorthSignedLocals_tower
#print axioms fivefoldGK5BXNorthIntegerPolynomialZero_subcover
#print axioms fivefoldGK5BXNorthOriginalBothTowerButOppositeSeams

end
end KUOS.Architecture.WuxingPentagonUnified
