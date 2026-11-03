import KUOS.Architecture.QiWuxingGK5AUNorthNestedSourceHistoryV4_14
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AVNestedVerticalSourceChain
import Mathlib.Tactic

/-!
Qi v4.15 / F112-P94D3GK5AV — genuine north C60 four-stage
P93C-in-P94A internal vertical source-vertex reconstruction.

Independent GK5AV reconstructs an ORIGINAL F55 source witness for
the selected P92B middle of a source-saturated ACTUAL P93C vertical
trans nested within selected P94A old. Here the source/target remain
the TRUE north four-stage F54 long/short pentagon with both Nat
indices and all categorical blocks unchanged, and the source-vertex
chain carries the actual selected P94A old-ed comparison halves.

The chain gives original P89 descent when its real two-edge local
BadStep obstruction is absent. It does not claim that arbitrary
P94A proofs are normalized or that a genuine GK5AQ BadPair exists.

The TRUE north three-unit P92B assocNaturality inside an ACTUAL
two-refl P93C vertical composite, embedded into P94A old, has an
original-F55 phi-image obstruction even though BOTH context parities
are zero. The genuine physical north fifth Dart closure, 04/43
physical/categorical orientation distinction, and CONDITIONAL
original P89/P94A noninjectivity iff remain intact.

Independent Kuu -> Qi; strict 空 authority; root 107; #1558
Draft/open. Append-only, original higher proof sources untouched.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms/sorry/native_decide/Gray/unconditional gluing.
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

/-- In the original north F54/F55 long-short pentagon source,
a fully source-saturated P93C vertical trans inside a genuine
P94A old proof yields an ACTUAL original F55 midpoint and an
original source-vertex two-edge chain. The existing GK5AS
theorem then witnesses P89 reflection or an actual local BadStep. -/
theorem fivefoldGK5AVNorthP93CInsideP94_sourceChain_reflect_or_bad
    (f g : NativeGK5AINorthPentagonCells)
    (middle : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (left : NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P93AssocFourCell
      middle (nativeGK5AIOriginalToP92Structural g))
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.old
        (NativeF55P93AssocFourCell.trans left right))) :
    ∃ sourceMid : NativeGK5AINorthPentagonCells,
      ∃ hmid : nativeGK5AIOriginalToP92Structural sourceMid = middle,
      Nonempty (NativeF55P89InterchangeFourCell f g) ∨
        (nativeGK5AVTwoStepSourceChain f g
          (NativeF55P94UnitFourCell.old left)
          (NativeF55P94UnitFourCell.old right) sourceMid hmid).HasBadStep :=
  nativeGK5AVP93CInsideP94_sourceChain_reflect_or_bad
    f g middle left right clean

/-- Exact conditional physical north original P89 reflection:
the source-saturated two-edge selected P93C/P94A history is
lifted to the ORIGINAL P89 four-proof when its actual original
GK5AS source-vertex chain carries no local BadStep. -/
theorem fivefoldGK5AVNorthP93CInsideP94_descends_of_noBad
    (f g sourceMid : NativeGK5AINorthPentagonCells)
    (middle : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (left : NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P93AssocFourCell
      middle (nativeGK5AIOriginalToP92Structural g))
    (hmid : nativeGK5AIOriginalToP92Structural sourceMid = middle)
    (noBad : ¬ (nativeGK5AVTwoStepSourceChain f g
      (NativeF55P94UnitFourCell.old left)
      (NativeF55P94UnitFourCell.old right) sourceMid hmid).HasBadStep) :
    Nonempty (NativeF55P89InterchangeFourCell f g) :=
  nativeGK5AVP93CInsideP94_descends_of_noBad
    f g sourceMid middle left right hmid noBad

/-- Truly PHYSICAL north C60: nested P93C TWO-step reflexive
proof term has a non-original phi midpoint although both
P94A context-unit grades vanish. The fifth-around Dart closure
and both reversed 04/43 orientations remain exact. P89/P94A
noninjectivity stays CONDITIONAL on a genuine original BadPair. -/
theorem fivefoldGK5AVNorthPhysicalNestedP93CDoubleReflSourceGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (∃ w : NativeF55P94UnitFourCell
        nativeGK5AINorthAddedUnitAssocCell
        nativeGK5AINorthAddedUnitAssocCell,
      w = nativeGK5AVNorthNestedP93CDoubleRefl ∧
      (¬ nativeGK5AUP94SourceSaturated w) ∧
      (¬ Nonempty (nativeGK5ATPhiFiber
        nativeGK5AINorthAddedUnitAssocCell)) ∧
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
  rcases nativeGK5AVNorthNestedP93CDoubleRefl_obstruction_zeroGrade with
    ⟨hNotClean, hNoFiber, hLeft, hRight⟩
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨⟨nativeGK5AVNorthNestedP93CDoubleRefl, rfl, hNotClean,
    hNoFiber, hLeft, hRight⟩, hClosed, h04, h43, hIff⟩

#print axioms fivefoldGK5AVNorthP93CInsideP94_sourceChain_reflect_or_bad
#print axioms fivefoldGK5AVNorthP93CInsideP94_descends_of_noBad
#print axioms fivefoldGK5AVNorthPhysicalNestedP93CDoubleReflSourceGate

end
end KUOS.Architecture.WuxingPentagonUnified
