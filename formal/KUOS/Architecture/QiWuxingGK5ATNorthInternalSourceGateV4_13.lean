import KUOS.Architecture.QiWuxingGK5ASNorthSourceVertexNoDescentV4_12
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ATInternalSourceImageObstruction
import Mathlib.Tactic

/-!
Qi v4.13 / F112-P94D3GK5AT — true north C60 P94A internal
selected P92B source-image gate, preserving physical Dart history.

Original north four-stage pentagon F54 long/short histories are
retained in their exact two-Nat typed syntax. GK5AT is specialized
to REAL source F55 pentagon three-proof endpoints and genuine
two-step selected P94A four-proof evidence, with the internal
selected P92B intermediate kept distinct from source evidence.

A two-step selected comparison either has a source P89 reflection,
or its middle has NO original F55 phi-preimage, or a genuine local
GK5AQ bad pair exists (under an original middle phi-preimage).
For an assumed original north bad pair, every such actual two-step
factorization therefore has this exact obstruction. No source
noninjectivity or arbitrary P94A 19-constructor decomposition is
claimed unconditionally.

Independently, the true north three-unit assocNaturality selected
witness is an INTERNAL middle of a real P94A double-refl four-cell
with parity (0,0), but no original F55 phi-preimage. The real
fifth Dart around closure and reversed categorical 04/43 physical
orientation are simultaneously preserved. Physical shadow data
cannot supply a missing source proof term.

Independent Kuu → Qi only; strict 空 authority; public root107,
#1558 remains Draft/open/unmerged. Append-only; no old definitions
replaced, Gray, global gluing or new axioms. No sorry/admit.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

private def fivefoldGK5ATNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5ATNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- In the genuine NORTH source long/short F54 pentagon slot,
any selected P94A two-step comparison has a true original P89
reflection OR an exact intermediate phi-image/local bad-pair
obstruction. Selected internal evidence remains explicitly typed. -/
theorem fivefoldGK5ATNorthTwoStep_reflect_or_obstruction
    (f g : NativeGK5AINorthPentagonCells)
    (middle : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
      nativeGK5ATTwoStepObstruction f g middle :=
  nativeGK5ATTwoStep_reflect_or_obstruction f g middle left right

/-- An ASSUMED true original north P89/P94A BadPair forces a
missing internal F55 phi-source OR a source-typed bad local step
for every GIVEN genuine two-stage P94A factorization. -/
theorem fivefoldGK5ATNorthBadPair_forces_internalObstruction
    (f g : NativeGK5AINorthPentagonCells)
    (middle : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural g))
    (bad : nativeGK5AQBadPair
      fivefoldGK5ATNorthFirst fivefoldGK5ATNorthLast f g) :
    nativeGK5ATTwoStepObstruction f g middle :=
  nativeGK5ATBadPair_forces_internalObstruction
    f g middle left right bad

/-- A TRUE NORTH physical five-phase gauge frame is compatible
with an explicit internally non-source P94A composite of parity
(0,0), correct fifth-around Dart closure, the historically
reversed physical 04/43 categorical directions, and the still
CONDITIONAL original P89→P94A noninjectivity comparison. -/
theorem fivefoldGK5ATNorthPhysicalInternalNoDescent
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (∃ w : NativeF55P94UnitFourCell
        nativeGK5AINorthAddedUnitAssocCell
        nativeGK5AINorthAddedUnitAssocCell,
      w = nativeGK5ATNorthDoubleRefl ∧
      (¬ Nonempty
        (nativeGK5ATPhiFiber nativeGK5AINorthAddedUnitAssocCell)) ∧
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
  rcases nativeGK5ATNorthDoubleRefl_nonimage_middle_zeroGrade with
    ⟨hno, hleft, hright⟩
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hiff, hclosed, _, h04, h43⟩
  exact ⟨⟨nativeGK5ATNorthDoubleRefl, rfl, hno, hleft, hright⟩,
    hclosed, h04, h43, hiff⟩

#print axioms fivefoldGK5ATNorthTwoStep_reflect_or_obstruction
#print axioms fivefoldGK5ATNorthBadPair_forces_internalObstruction
#print axioms fivefoldGK5ATNorthPhysicalInternalNoDescent

end
end KUOS.Architecture.WuxingPentagonUnified
