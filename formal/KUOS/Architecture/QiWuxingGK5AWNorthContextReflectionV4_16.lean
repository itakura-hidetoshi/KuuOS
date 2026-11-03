import KUOS.Architecture.QiWuxingGK5AVNorthNestedSourceVertexChainV4_15
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AWContextGeneratorReflectionGate
import Mathlib.Tactic

/-!
Qi v4.16 / F112-P94D3GK5AW — original north C60 source
whisker reflection obstruction and exact selected P92B phi-fiber gates.

Independent GK5AW proves that eight genuine ORIGINAL P89 source
context operations cannot create a new reflection obstruction
without a BadPair already present in the selected inner comparison.
It separately extracts dependent F55 phi-fibers for selected P94A
whisker/horizontal/interchange arguments under GK5AU saturation.

Specialize the genuine left/right selected F54 route-whisker
proofs to the ORIGINAL four-stage north C60 long/short pentagon:
(a) selected proof saturation recovers original F55 phi-fibers of
the actual P92B prior/suffix inputs, and (b) a hypothesized
P89/P94A BadPair at an ORIGINAL left-whiskered source pair forces
a true GK5AQ BadPair already at the original four-stage core pair.

Both conditional gates are made compatible with the existing REAL
physical north fifth-around Dart closure, the reversed physical
04/43 categorical orientations and the still CONDITIONAL original
P89/P94A four-class noninjectivity iff source GK5AQ BadPair.
No noninjective source pair is claimed to exist.

Strict 空 authority; independent Kuu -> Qi, append-only, root107.
Keep original F54 two-Nat histories, original P89 and selected
P92B/P93C/P94A files untouched; #1558 Draft/open. Pinned Lean
v4.30.0-rc2/mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray, global gluing.
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

private def fivefoldGK5AWNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5AWNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- ORIGINAL north four-stage F54 route histories: genuine selected
P94A left/right whisker proofs that are source-saturated have
ACTUAL dependent F55 original phi-fibers for the extra P92B
prior/suffix proof terms. No quotient equality is used. -/
theorem fivefoldGK5AWNorthWhisker_sourceFibers
    {u v : NativeGK5AGNorthHistory}
    (prior : NativeF55P92AssocComparison (.pentagon .north)
      u northNativeF45PentagonLong)
    (suffix : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonShort v)
    (f g : NativeGK5AINorthPentagonCells)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (cleanLeft : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.leftWhisker prior selected))
    (cleanRight : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.rightWhisker selected suffix)) :
    Nonempty (nativeGK5ATPhiFiber prior) ∧
    Nonempty (nativeGK5ATPhiFiber suffix) :=
  ⟨nativeGK5AWLeftWhisker_prior_fiber prior selected cleanLeft,
    nativeGK5AWRightWhisker_suffix_fiber selected suffix cleanRight⟩

/-- Any hypothesized nonreflecting P94A comparison of original
F55 left-whiskered NORTH long/short pentagon histories localizes
to a genuine source-typed GK5AQ BadPair of its true inner pair.
No existence of that source BadPair is asserted. -/
theorem fivefoldGK5AWNorthOriginalLeftWhisker_bad_localizes
    {u : NativeGK5AGNorthHistory}
    (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) u northNativeF45PentagonLong)
    (f g : NativeGK5AINorthPentagonCells)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair
      fivefoldGK5AWNorthFirst fivefoldGK5AWNorthLast
      (.trans prior f) (.trans prior g)) :
    nativeGK5AQBadPair fivefoldGK5AWNorthFirst
      fivefoldGK5AWNorthLast f g :=
  nativeGK5AWLeftWhisker_bad_localizes prior selected parentBad

/-- The genuine north physical five-phase frame is compatible
with the ORIGINAL P89 source-whisker obstruction localization,
the real fifth Dart closure, the orientation reversals of
physical e04/e43, and the still conditional noninjectivity iff. -/
theorem fivefoldGK5AWNorthPhysicalLeftWhiskerReflectionGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    {u : NativeGK5AGNorthHistory}
    (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) u northNativeF45PentagonLong)
    (f g : NativeGK5AINorthPentagonCells)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair
      fivefoldGK5AWNorthFirst fivefoldGK5AWNorthLast
      (.trans prior f) (.trans prior g)) :
    nativeGK5AQBadPair fivefoldGK5AWNorthFirst
      fivefoldGK5AWNorthLast f g ∧
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
  have hlocal := fivefoldGK5AWNorthOriginalLeftWhisker_bad_localizes
    prior f g selected parentBad
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨hlocal, hClosed, h04, h43, hIff⟩

/-- Even with the true north Dart closure and both historically
reversed physical 04/43 edges, the P94A selected prior/suffix
require GENUINE original F55 phi-fibers under full source
saturation. The original-source reflection obstruction stays
independent from a purely physical gauge frame. -/
theorem fivefoldGK5AWNorthPhysicalWhiskerSourceFiberGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    {u v : NativeGK5AGNorthHistory}
    (prior : NativeF55P92AssocComparison (.pentagon .north)
      u northNativeF45PentagonLong)
    (suffix : NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonShort v)
    (f g : NativeGK5AINorthPentagonCells)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (cleanLeft : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.leftWhisker prior selected))
    (cleanRight : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.rightWhisker selected suffix)) :
    (Nonempty (nativeGK5ATPhiFiber prior) ∧
     Nonempty (nativeGK5ATPhiFiber suffix)) ∧
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
  have hfiber := fivefoldGK5AWNorthWhisker_sourceFibers
    prior suffix f g selected cleanLeft cleanRight
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨hfiber, hClosed, h04, h43, hIff⟩

#print axioms fivefoldGK5AWNorthWhisker_sourceFibers
#print axioms fivefoldGK5AWNorthOriginalLeftWhisker_bad_localizes
#print axioms fivefoldGK5AWNorthPhysicalLeftWhiskerReflectionGate
#print axioms fivefoldGK5AWNorthPhysicalWhiskerSourceFiberGate

end
end KUOS.Architecture.WuxingPentagonUnified
