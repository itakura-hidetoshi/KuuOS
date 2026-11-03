import KUOS.Architecture.QiWuxingGK5ATNorthInternalSourceGateV4_13
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AUP94FullInternalSourceHistory
import Mathlib.Tactic

/-!
Qi v4.14 / F112-P94D3GK5AU — genuine north C60 history-sensitive
P93C-in-P94A phi-source obstruction and conditional P89 descent.

Reuse the independent GK5AU proofs over the ORIGINAL north F54
two-Nat pentagon long/short histories. A source-saturated genuine
P94A trans between structural phi-images either reflects into an
actual original P89 four-cell or has a GK5AQ BadPair at a genuine
source middle, never merely at an equal shadow or quotient class.
If every original preimage of the actual middle avoids both BadPairs,
P89 descent is proved.

A separate, concrete true north P93C reflexive four-proof over the
ADJOINED P92B assocNaturality is embedded inside the genuinely
selected P94A .old constructor. GK5AU recursively detects its
non-image phi-hole, while GK5AR gives both context-unit parities zero.
The original physical fifth Dart cycle and physical e04/e43 orientation
are kept alongside the conditional noninjectivity iff, WITHOUT
inventing an original F55 source of assocNaturality.

Original P89/P92B/P93C/P94A sources are unchanged. Independent Kuu→Qi,
strict 空 authority; append-only / same-root 107; #1558 Draft/open;
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry/admit/native_decide, new axioms, Gray or global gluing.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

private def fivefoldGK5AUNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5AUNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- TRUE north original source F55 endpoints, ACTUAL selected
P94A two-stage comparison, and FULL recursively audited history.
The middle is in original F55 phi-image, so a failed original P89
descent must occur at an actual local source BadPair. -/
theorem fivefoldGK5AUNorthCleanTwoStep_reflect_or_localBad
    (f g : NativeGK5AINorthPentagonCells)
    (middle : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural g))
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.trans left right)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
    ∃ mid : NativeGK5AINorthPentagonCells,
      nativeGK5AIOriginalToP92Structural mid = middle ∧
      (nativeGK5AQBadPair
          fivefoldGK5AUNorthFirst fivefoldGK5AUNorthLast f mid ∨
       nativeGK5AQBadPair
          fivefoldGK5AUNorthFirst fivefoldGK5AUNorthLast mid g) :=
  nativeGK5AU_clean_trans_reflect_or_local_bad f g middle left right clean

/-- Honest conditional original north P89 descent from a selected
two-step proof: full P94A/P93C source saturation AND no true
original-source local GK5AQ BadPair at either real half. -/
theorem fivefoldGK5AUNorthCleanTwoStep_descends
    (f g : NativeGK5AINorthPentagonCells)
    (middle : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural g))
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.trans left right))
    (noLocal : ∀ mid : NativeGK5AINorthPentagonCells,
      nativeGK5AIOriginalToP92Structural mid = middle →
      ¬ (nativeGK5AQBadPair
            fivefoldGK5AUNorthFirst fivefoldGK5AUNorthLast f mid ∨
         nativeGK5AQBadPair
            fivefoldGK5AUNorthFirst fivefoldGK5AUNorthLast mid g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) :=
  nativeGK5AU_clean_trans_descends f g middle left right clean noLocal

/-- Genuine north C60 example: a P93C certificate embedded INSIDE
P94A has an actual original-F55 phi hole even though BOTH selected
context-unit parities vanish. Physical 5th Dart closure and 04/43
orientation are preserved, and the P89/P94A noninjectivity criterion
remains conditional rather than claimed to hold automatically. -/
theorem fivefoldGK5AUNorthNestedPhysicalSourceGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (∃ w : NativeF55P94UnitFourCell
        nativeGK5AINorthAddedUnitAssocCell
        nativeGK5AINorthAddedUnitAssocCell,
      w = nativeGK5AUNorthNestedP93C ∧
      nativeGK5AUP94SourceHole w ∧
      (¬ nativeGK5ATPhiImage nativeGK5AINorthAddedUnitAssocCell) ∧
      Nonempty (NativeF55P93AssocFourCell
        nativeGK5AINorthAddedUnitAssocCell
        nativeGK5AINorthAddedUnitAssocCell) ∧
      (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
      (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0)) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) := by
  rcases nativeGK5AUNorth_nestedP93C_hole_zeroGrade with
    ⟨hHole, hLeft, hRight⟩
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨⟨nativeGK5AUNorthNestedP93C, rfl, hHole,
    nativeGK5ATNorthAddedAssoc_noPhiImage,
    ⟨NativeF55P93AssocFourCell.refl nativeGK5AINorthAddedUnitAssocCell⟩,
    hLeft, hRight⟩, hClosed, h04, h43, hIff⟩

#print axioms fivefoldGK5AUNorthCleanTwoStep_reflect_or_localBad
#print axioms fivefoldGK5AUNorthCleanTwoStep_descends
#print axioms fivefoldGK5AUNorthNestedPhysicalSourceGate

end
end KUOS.Architecture.WuxingPentagonUnified
