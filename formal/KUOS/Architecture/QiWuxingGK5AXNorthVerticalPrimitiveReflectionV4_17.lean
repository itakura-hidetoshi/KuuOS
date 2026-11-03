import KUOS.Architecture.QiWuxingGK5AWNorthContextReflectionV4_16
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AXVerticalPrimitiveReflectionCertificates
import Mathlib.Tactic

/-!
Qi v4.17 / F112-P94D3GK5AX — TRUE north C60 original
F55 vertical primitive P94A/P89 source-reflection certificate gates.

GK5AX constructed three genuine selected P94A source-indexed
primitive four-cells: vertical left unit, right unit, and assoc.
For each original F55 typed source pair, selected P94A exists,
and failure of original P89 reflection is precisely a GK5AQ
BadPair. A dependent original P89 primitive-reflection record is
not asserted inhabited; CONDITIONAL on such genuine original
witness data, every finite source-vertical word descends.

Here we specialize left/right primitive gates to the TRUE north
four-stage pentagon F54/F55 long/short source history, and the
associator gate to all original north typed source triples.
The selected/source distinction and conditional descent are
compatible with the TRUE north physical fifth Dart-around closure,
physical/categorical orientation reversal of edges 04/43, and the
still CONDITIONAL original P89→P94A noninjectivity iff GK5AQ.

The physical five-phase gauge does not manufacture the missing
original P89 vertical primitive certificates. Independent Kuu→Qi,
strict 空 authority, append-only, public root 107, protected #1558
Draft/open, original F55/P89/P93C/P94A sources untouched.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No added axioms, sorry/admit/native_decide, Gray, global gluing.
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

private def fivefoldGK5AXNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5AXNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Two REAL north four-stage original F55 vertical unit source
histories. Their independently selected P94A 4-proofs are given
by GK5AX; original P89 reflection failure iff true GK5AQ BadPair.
Neither primitive is claimed to be missing or present in P89. -/
theorem fivefoldGK5AXNorthVerticalUnit_bad_iff_noP89
    (f : NativeGK5AINorthPentagonCells) :
    (nativeGK5AQBadPair fivefoldGK5AXNorthFirst
      fivefoldGK5AXNorthLast
      (.trans (.ident northNativeF45PentagonLong) f) f ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans (.ident northNativeF45PentagonLong) f) f)) ∧
    (nativeGK5AQBadPair fivefoldGK5AXNorthFirst
      fivefoldGK5AXNorthLast
      (.trans f (.ident northNativeF45PentagonShort)) f ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans f (.ident northNativeF45PentagonShort)) f)) :=
  ⟨nativeGK5AXLeftUnit_bad_iff_noP89 f,
    nativeGK5AXRightUnit_bad_iff_noP89 f⟩

/-- EXACT original north F54-typed triple source associativity:
the selected P94A verticalAssoc is already a genuine generator,
but original P89 reflection is an independent four-cell obligation.
No numerical shadow equality substitutes for that obligation. -/
theorem fivefoldGK5AXNorthVerticalAssoc_bad_iff_noP89
    {u v w z : NativeGK5AGNorthHistory}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) u v)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) v w)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) w z) :
    nativeGK5AQBadPair fivefoldGK5AXNorthFirst
      fivefoldGK5AXNorthLast
      (.trans (.trans f g) h) (.trans f (.trans g h)) ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans (.trans f g) h) (.trans f (.trans g h))) :=
  nativeGK5AXAssoc_bad_iff_noP89 f g h

/-- The exact TYPE-valued selected→original descent of any
FINITE north original-source vertical four-proof word is valid
conditional on the three-family ORIGINAL P89 primitive witness
record, NOT conditional on a physical five-phase measurement. -/
theorem fivefoldGK5AXNorthVerticalWord_conditionalDescent
    (data : NativeGK5AXVerticalPrimitiveCertificates
      fivefoldGK5AXNorthFirst fivefoldGK5AXNorthLast)
    (f g : NativeGK5AINorthPentagonCells)
    (w : NativeGK5AXSourceVerticalWord f g) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∧
    Nonempty (NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)) :=
  w.both_witnesses data

/-- The genuine north C60 fifth-around Dart closure and the
historical e04/e43 physical-versus-categorical direction reversal
coexist with the exact conditional vertical unit reflection gate
and the still CONDITIONAL original P89/P94A noninjectivity iff. -/
theorem fivefoldGK5AXNorthPhysicalVerticalUnitReflectionGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (f : NativeGK5AINorthPentagonCells) :
    ((nativeGK5AQBadPair fivefoldGK5AXNorthFirst
        fivefoldGK5AXNorthLast
        (.trans (.ident northNativeF45PentagonLong) f) f ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans (.ident northNativeF45PentagonLong) f) f)) ∧
     (nativeGK5AQBadPair fivefoldGK5AXNorthFirst
        fivefoldGK5AXNorthLast
        (.trans f (.ident northNativeF45PentagonShort)) f ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans f (.ident northNativeF45PentagonShort)) f))) ∧
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
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨fivefoldGK5AXNorthVerticalUnit_bad_iff_noP89 f,
    hClosed, h04, h43, hIff⟩

/-- A physical five-phase gauge is COMPATIBLE with, but does not
supply, an original three-family P89 vertical reflection record.
Under the explicit original certificate hypothesis every north
source vertical word has a genuine original 4-cell and an actually
selected P94A 4-cell, while all original north Dart/orientation
data remain exact and noninjectivity remains conditional. -/
theorem fivefoldGK5AXNorthPhysicalFiniteWordConditionalDescent
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (data : NativeGK5AXVerticalPrimitiveCertificates
      fivefoldGK5AXNorthFirst fivefoldGK5AXNorthLast)
    (f g : NativeGK5AINorthPentagonCells)
    (w : NativeGK5AXSourceVerticalWord f g) :
    (Nonempty (NativeF55P89InterchangeFourCell f g) ∧
     Nonempty (NativeF55P94UnitFourCell
       (nativeGK5AIOriginalToP92Structural f)
       (nativeGK5AIOriginalToP92Structural g))) ∧
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
  have hproof := fivefoldGK5AXNorthVerticalWord_conditionalDescent
    data f g w
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨hproof, hClosed, h04, h43, hIff⟩

#print axioms fivefoldGK5AXNorthVerticalUnit_bad_iff_noP89
#print axioms fivefoldGK5AXNorthVerticalAssoc_bad_iff_noP89
#print axioms fivefoldGK5AXNorthVerticalWord_conditionalDescent
#print axioms fivefoldGK5AXNorthPhysicalVerticalUnitReflectionGate
#print axioms fivefoldGK5AXNorthPhysicalFiniteWordConditionalDescent

end
end KUOS.Architecture.WuxingPentagonUnified
