import KUOS.Architecture.QiWuxingGK5CHP77MixedResidueBalancedUnitSupplementV5_07

/-!
Qi v5.07 PR #3238 reconciliation — nonduplicated observer compatibility.

The historical draft #3238 contained 43 Lean declarations, of which 30
collided with the already MERGED authoritative v5.07 PR #3237.
The independent balanced-unit comparison and integer-V non-descent
were salvaged and formally validated in #3240/#3241. Retain the
remaining genuinely unrepresented API: Z-valued V mod 2 descent
and the v5.07 U-parity Bool observer under the old explicit name.

This module uses the SAME original SevenRewrite and the SAME
canonical MixedResidueEightCell selected quotient. It creates no
second presentation, comparison constructor, source strict Eq, new
ninth cell or mathematical axiom. The historic #3238 source remains
in Git commit history; the canonical main formal tree includes only
this nonduplicated proof/API reconciliation.

append-only / tighten-only / overwrite-forbidden / same-root.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell
variable {W : Type uSix} {long short : W}

/-- Exact compatibility alias for the ORIGINAL v5.06 3-versus-5
source histories, with the canonical v5.07 V-mod-2 observer. -/
theorem sevenMixedResidue_totalParityValues (w : W) :
    sevenTotalReductionParity
        (sevenMixedResidueFirst (long := long) (short := short) w) = 1 ∧
    sevenTotalReductionParity
        (sevenMixedResidueSecond (long := long) (short := short) w) = 1 :=
  sevenMixedResidue_vParityValues (long := long) (short := short) w

/-- No independent proof grammar is added: reuse the canonical
FULL-constructor conservation theorem from verified Qi v5.07. -/
theorem mixedResidueEightCell_preservesTotalReductionParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : MixedResidueEightCell W long short s t) :
    sevenTotalReductionParity s = sevenTotalReductionParity t :=
  mixedResidueEightCell_preservesVParity q

/-- The missing integer representative of V mod 2 descends to
the ACTUAL canonical mixed-residue history quotient, without
identifying two original raw seven-cell proof values. -/
def mixedResidueHistoryV2 {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) →
      ℤ :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d => sevenTotalReductionParity s)
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact mixedResidueEightCell_preservesTotalReductionParity q)

theorem mixedResidueHistoryV2_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryV2
      (mixedResidueHistoryClass (long := long) (short := short) s) =
      sevenTotalReductionParity s := rfl

/-- The explicit U-parity observer name preserved by historic #3238
is definitionally the one ALREADY proved to descend in #3237. -/
def mixedResidueHistoryUnitCountParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (mixedResidueHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  mixedResidueHistoryUnitParity

theorem mixedResidueHistoryUnitCountParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    mixedResidueHistoryUnitCountParity
      (mixedResidueHistoryClass (long := long) (short := short) s) =
      decide (sevenUnitCountParity s = 1) :=
  mixedResidueHistoryUnitParity_onClass s

/-- The Z-representative and canonical Bool observer are compatible
on EVERY class, rather than only on the original 3-versus-5 witness. -/
theorem mixedResidueHistoryV2_boolCompatibility {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (q : Quotient
      (mixedResidueHistorySetoid W long short (c := c) (d := d))) :
    decide (mixedResidueHistoryV2 q = 1) =
      mixedResidueHistoryVParity q := by
  refine Quotient.inductionOn q ?_
  intro s
  rfl

#print axioms sevenMixedResidue_totalParityValues
#print axioms mixedResidueEightCell_preservesTotalReductionParity
#print axioms mixedResidueHistoryV2
#print axioms mixedResidueHistoryV2_onClass
#print axioms mixedResidueHistoryUnitCountParity
#print axioms mixedResidueHistoryUnitCountParity_onClass
#print axioms mixedResidueHistoryV2_boolCompatibility

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
