import KUOS.Architecture.QiWuxingGK5ARNorthContextParityNormalFormV4_11
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ASSourceVertexObstructionLocalization
import Mathlib.Tactic

/-!
Qi v4.12 / F112-P94D3GK5AS — genuine north C60 local source-vertex
four-cell reflection and parity-zero no-descent boundary.

Independent Kuu GK5AS proved that finite selected P94A 4-cell
comparison chains whose outer VERTICES remain actual original F55
3-proof histories either reflect into original P89 4-cell evidence
or contain a truly nonreflecting local selected edge. Every GK5AQ
bad pair therefore obstructs EVERY such chain between the same
original endpoints (if any such chain is supplied). This does NOT
assert all P94A internal evidence admits a source-vertex normal form.

Separately, on the REAL north C60 first THREE F45 unit stages,
the new P92B assocNaturality 3-cell admits a P94A reflexive 4-cell,
and every such P94A self-comparison has left/right context count
parity (0,0), while no original F55 3-cell preimage exists.
Thus the selected grade-zero criterion CANNOT by itself be used
as an original witness recovery/descent criterion.

The original 4-sector north C60 pentagon source long/short F54
histories, GK5AN unconditional P89 structural lift, Qi v4.10
conditional nonreflection iff, fifth-around physical Dart closure,
04/43 reversed categorical orientations, and Qi v4.11 exact
3-unit primitive minimum and parity data remain distinct.

Strict 空 authority, independent Kuu → Qi only, append-only
root107, #1558 Draft/open. No original P89/P93/P94A change,
no sorry/admit/native_decide, new axioms, Gray or unrestricted gluing.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- The genuine north F54 first/last pentagon trees, re-stated
locally since Qi v4.10 used module-private source constants. -/
private def fivefoldGK5ASNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5ASNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private abbrev fivefoldGK5ASNorthOriginalUnitAssoc :=
  NativeF55P90AssocNaturalityCell
    (nativeF54P92UnitRoute northNativeF45FirstStage)
    (nativeF54P92UnitRoute northNativeF45SecondStage)
    (nativeF54P92UnitRoute northNativeF45ThirdStage)

/-- The real north original four-sector pentagon source has a
fully typed finite selected four-cell chain. Either its original
P89 endpoints are 4-cell related or SOME genuine local step does
not reflect. All intermediate chain vertices remain original F55
3-proof histories, not an assumed recovery of arbitrary P92B terms. -/
theorem fivefoldGK5ASNorthChain_reflect_or_badStep
    (f g : NativeGK5AINorthPentagonCells)
    (chain : NativeGK5ASSourceVertexChain f g) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
      chain.HasBadStep :=
  chain.reflects_or_badStep

/-- Every original north P89/P94A nonreflection BadPair forces
a bad local step in EVERY actual source-vertex chain between
these same pentagon long/short F54 original proof endpoints. -/
theorem fivefoldGK5ASNorthBadPair_forces_localStep
    (f g : NativeGK5AINorthPentagonCells)
    (chain : NativeGK5ASSourceVertexChain f g)
    (bad : nativeGK5AQBadPair
      fivefoldGK5ASNorthFirst fivefoldGK5ASNorthLast f g) :
    chain.HasBadStep :=
  chain.badPair_forces_badStep bad

/-- Even the exact zero parity-grade 4-cell loop at genuine north
assocNaturality does NOT supply an original F55 preimage for its
selected P92B endpoint. The selected proof exists nonetheless. -/
theorem fivefoldGK5ASNorthZeroGrade_noOriginalPreimage :
    (∃ w : NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell,
      (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
      (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0)) ∧
    (¬ ∃ old : fivefoldGK5ASNorthOriginalUnitAssoc,
      nativeGK5AIOriginalToP92Structural old =
        nativeGK5AINorthAddedUnitAssocCell) := by
  rcases nativeGK5ASNorthZeroGrade_not_sourceRecovery with
    ⟨⟨w⟩, hgrade, hno⟩
  exact ⟨⟨w, (hgrade w).1, (hgrade w).2⟩, hno⟩

/-- True north C60 physical Dart data cannot replace the missing
original F55 assocNaturality preimage, nor silently produce a
source P89 four-cell. Local bad-step witness localization and the
exact conditional P89→P94A noninjectivity iff remain compatible
with physical fifth closure, full structural lift and 04/43 reversal. -/
theorem fivefoldGK5ASNorthPhysicalLocalityAndNoDescent
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (¬ ∃ old : fivefoldGK5ASNorthOriginalUnitAssoc,
      nativeGK5AIOriginalToP92Structural old =
        nativeGK5AINorthAddedUnitAssocCell) ∧
    (∀ f g : NativeGK5AINorthPentagonCells,
      ∀ chain : NativeGK5ASSourceVertexChain f g,
        nativeGK5AQBadPair
          fivefoldGK5ASNorthFirst fivefoldGK5ASNorthLast f g →
          chain.HasBadStep) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    Nonempty FivefoldGK5ANP94NorthFullBoundary ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  rcases nativeGK5ASNorthZeroGrade_not_sourceRecovery with
    ⟨_, _, hno⟩
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hiff, hclosed, hrepair, h04, h43⟩
  exact ⟨hno,
    (fun f g chain hbad => chain.badPair_forces_badStep hbad),
    hiff, hclosed, hrepair, h04, h43⟩

#print axioms fivefoldGK5ASNorthChain_reflect_or_badStep
#print axioms fivefoldGK5ASNorthBadPair_forces_localStep
#print axioms fivefoldGK5ASNorthZeroGrade_noOriginalPreimage
#print axioms fivefoldGK5ASNorthPhysicalLocalityAndNoDescent

end
end KUOS.Architecture.WuxingPentagonUnified
