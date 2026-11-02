import KUOS.Architecture.QiWuxingGK5ALNorthPrimitiveObstructionV4_5
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AMContextParityNoStructuralLift
import Mathlib.Tactic

/-!
Qi v4.6 / F112-P94D3GK5AM — the ACTUAL north-C60 original
P80 context units do not structurally descend to the selected
P93 higher-four-cell presentation.

Independent Kuu GK5AL identified exactly three primitive P80
source four-cell families required for a complete original P87/P89
structural transport. Qi v4.5 exhibited all three actual original
P87 witnesses on north C60's two genuinely adjacent F45 stages.
Independent GK5AM then proved that the P92B structural images
of ANY original left/right context units are obstructed in the
CURRENT selected P93 four-cell presentation by a new ZMod2
context-constructor parity, preserved by all sixteen P93 rules.

Here we instantiate both genuine C60 left/right primitive sources,
retain the original dual-Nat F54 route and F55 proof terms, and
prove simultaneously that source P87 four-cells EXIST but selected
P93 four-cells between their GK5AI structural images DO NOT.
Consequently the north C60 universal three-primitive boundary,
the old P87 structural transport and the full P89 structural
transport are all UNINHABITED, not merely conditional unknowns.
The original horizontal P89 interchange and its selected P93
image remain separately and unconditionally available.

The Qi v4.5 physical P89/P93 four-class map is a function of a
three-primitive boundary certificate. We prove that no such
certificate can be supplied on the actual north C60 source.
This does NOT claim that every possible bare set function or an
independently extended higher presentation is impossible.

The actual physical fifth-around Dart closure and both reversed
04/43 categorical Edge orientations are retained in a single
conjunction with the formal non-descent obstruction.

No false equality .original(f) = GK5AI structural phi(f).
No fabricated P93 context units, old-source proof erasure,
unrestricted physical-to-higher authority or global gluing.
Independent Kuu -> Qi only, strict 空 authority, root107.
Append-only/tighten-only, protect draft PR #1558.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide or new axioms.
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

/- The two ACTUAL original F54 unit routes. These keep BOTH Nat
depth coordinates and the two independent native Site categories. -/
private def fivefoldGK5ANorthFirstRoute :=
  nativeF54P92UnitRoute northNativeF45FirstStage

private def fivefoldGK5ANorthSecondRoute :=
  nativeF54P92UnitRoute northNativeF45SecondStage

private def fivefoldGK5ANorthLeftRawSource :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
    (.ident fivefoldGK5ANorthFirstRoute) northNativeF45SecondStage

private def fivefoldGK5ANorthLeftRawTarget :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
    (.leftContext fivefoldGK5ANorthFirstRoute northNativeF45SecondStage)

private def fivefoldGK5ANorthRightRawSource :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
    northNativeF45FirstStage (.ident fivefoldGK5ANorthSecondRoute)

private def fivefoldGK5ANorthRightRawTarget :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
    (.rightContext northNativeF45FirstStage fivefoldGK5ANorthSecondRoute)

/-- ACTUAL source P87 FOUR-cell for the first north F45 stage
whiskered on the right by the genuine second north F45 stage.
The original source has not been quotiented or identified. -/
def fivefoldGK5ANorthLeftOriginalP87 :
    NativeF55P87ClosedFourCell
      fivefoldGK5ANorthLeftRawSource fivefoldGK5ANorthLeftRawTarget :=
  fivefoldGK5ALNorthLeftContextPrimitive.toP87

/-- ACTUAL original P87 RIGHT-context four-cell for the same
adjacent north C60 stages, in the opposite typed context. -/
def fivefoldGK5ANorthRightOriginalP87 :
    NativeF55P87ClosedFourCell
      fivefoldGK5ANorthRightRawSource fivefoldGK5ANorthRightRawTarget :=
  fivefoldGK5ALNorthRightContextPrimitive.toP87

/-- The real original north-C60 left-context P80 unit is a
CONCRETE structural-P93 four-cell obstruction, not an assumed
absence of evidence or an equality of signed C60 shadows. -/
theorem fivefoldGK5ANorthLeft_no_selectedP93 :
    ¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthLeftRawSource)
      (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthLeftRawTarget)) :=
  nativeGK5AMLeftContextUnit_no_P93
    fivefoldGK5ANorthFirstRoute northNativeF45SecondStage

/-- The genuine right-context unit gives a SECOND independent
north-C60 structural four-cell non-descent witness. -/
theorem fivefoldGK5ANorthRight_no_selectedP93 :
    ¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthRightRawSource)
      (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthRightRawTarget)) :=
  nativeGK5AMRightContextUnit_no_P93
    northNativeF45FirstStage fivefoldGK5ANorthSecondRoute

/-- Both original FOUR-cell proof histories exist at precisely
the same two physical north C60 stages where their *structural*
P93 four-cell images are IMPOSSIBLE. This separates source
authority from chosen target-presentation authority. -/
theorem fivefoldGK5ANorthSource_exists_target_fails :
    (Nonempty (NativeF55P87ClosedFourCell
      fivefoldGK5ANorthLeftRawSource fivefoldGK5ANorthLeftRawTarget) ∧
     ¬ Nonempty (NativeF55P93AssocFourCell
       (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthLeftRawSource)
       (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthLeftRawTarget))) ∧
    (Nonempty (NativeF55P87ClosedFourCell
      fivefoldGK5ANorthRightRawSource fivefoldGK5ANorthRightRawTarget) ∧
     ¬ Nonempty (NativeF55P93AssocFourCell
       (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthRightRawSource)
       (nativeGK5AIOriginalToP92Structural fivefoldGK5ANorthRightRawTarget))) :=
  ⟨⟨⟨fivefoldGK5ANorthLeftOriginalP87⟩,
     fivefoldGK5ANorthLeft_no_selectedP93⟩,
   ⟨⟨fivefoldGK5ANorthRightOriginalP87⟩,
     fivefoldGK5ANorthRight_no_selectedP93⟩⟩

/-- The Qi v4.5 north source three-primitive compatibility
interface is UNINHABITED: applying it to the ACTUAL first/second
north left-context unit contradicts GK5AM's selected P93 parity.
This is stronger than the previously conditional iff. -/
theorem fivefoldGK5ANorthPrimitiveBoundary_empty :
    ¬ Nonempty FivefoldGK5ALNorthPrimitiveBoundary := by
  rintro ⟨base⟩
  apply fivefoldGK5ANorthLeft_no_selectedP93
  exact ⟨base fivefoldGK5ALNorthLeftContextPrimitive⟩

/-- The genuine old-P87 structural four-cell transport cannot
be supplied on the north C60 Site source, by the exact iff in
Qi v4.5 and the concrete P80 context-unit parity obstruction. -/
theorem fivefoldGK5ANorthP87Boundary_empty :
    ¬ Nonempty FivefoldGK5AKNorthP87Boundary := by
  intro h
  exact fivefoldGK5ANorthPrimitiveBoundary_empty
    (fivefoldGK5ALNorthP87_iff_threePrimitive.mp h)

/-- The original P89 thirteen-constructor structural transport
also fails on real north C60, despite the independent P89
interchange generator's proven unconditional selected P93 image. -/
theorem fivefoldGK5ANorthP89Boundary_empty :
    ¬ Nonempty (NativeGK5AKP89StructuralBoundary
      (a := Site.vertex (cyclicBoundaryDart (.pentagon .north)
        (firstFourPolygonSector (.pentagon .north) 0).1.val))
      (b := Site.face (.pentagon .north))
      (x := Site.vertex (cyclicBoundaryDart (.pentagon .north)
        (firstFourPolygonSector (.pentagon .north) 0).1.val))
      (y := Site.face (.pentagon .north))
      (.pentagon .north)) := by
  intro h
  exact fivefoldGK5ANorthPrimitiveBoundary_empty
    (fivefoldGK5ALNorthP89_iff_threePrimitive.mp h)

/-- The previously CONDITIONAL Qi v4.5 physical four-class
comparison cannot be instantiated with a three-primitive
certificate, even if we separately request injectivity.
It does NOT prohibit arbitrary non-structural set functions. -/
theorem fivefoldGK5ANorthNoCertifiedPhysicalFourClassMap
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    ¬ ∃ base : FivefoldGK5ALNorthPrimitiveBoundary,
      Function.Injective
        (fivefoldGK5ALNorthPhysicalFourClassMap frame i base) := by
  rintro ⟨base, _⟩
  exact fivefoldGK5ANorthPrimitiveBoundary_empty ⟨base⟩

/-- The real north C60 fifth around-edge Dart closure, both
physically reversed 04/43 categorical edges, and the rigorous
absence of universal higher structural lift coexist. Physical
orientation and 4-cell proof evidence remain distinct types. -/
theorem fivefoldGK5ANorthPhysicalOrientationAndNoDescent
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    (¬ Nonempty FivefoldGK5ALNorthPrimitiveBoundary) ∧
    (¬ Nonempty FivefoldGK5AKNorthP87Boundary) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  rcases fivefoldGK5AKNorthPhysicalInterchangeAndOrientation frame i with
    ⟨hclosed, _, _, h04, h43⟩
  exact ⟨hclosed, fivefoldGK5ANorthPrimitiveBoundary_empty,
    fivefoldGK5ANorthP87Boundary_empty, h04, h43⟩

#print axioms fivefoldGK5ANorthLeftOriginalP87
#print axioms fivefoldGK5ANorthRightOriginalP87
#print axioms fivefoldGK5ANorthLeft_no_selectedP93
#print axioms fivefoldGK5ANorthRight_no_selectedP93
#print axioms fivefoldGK5ANorthSource_exists_target_fails
#print axioms fivefoldGK5ANorthPrimitiveBoundary_empty
#print axioms fivefoldGK5ANorthP87Boundary_empty
#print axioms fivefoldGK5ANorthP89Boundary_empty
#print axioms fivefoldGK5ANorthNoCertifiedPhysicalFourClassMap
#print axioms fivefoldGK5ANorthPhysicalOrientationAndNoDescent

end
end KUOS.Architecture.WuxingPentagonUnified
