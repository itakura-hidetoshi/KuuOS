import KUOS.Architecture.QiWuxingGK5AKNorthPhysicalInterchangeV4_4
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ALPrimitiveUnitObstruction
import Mathlib.Tactic

/-!
Qi v4.5 / F112-P94D3GK5AL — genuine north C60 source P80
primitive units and exact P87/P89 structural transport boundary.

Independent GK5AL establishes an iff reduction of the entire
P89 structural P93 four-cell comparison to THREE explicitly adjoined
original P80 units (horizontal / left context / right context).
Here we instantiate the primitive generator families on genuine
native north C60 F45 first and second stage trees, with their
true original F54 unit routes and F55 Type-valued 3-proof endpoints.

Each primitive yields an unconditional ORIGINAL P87 Type-valued
four-cell. A corresponding SELECTED P93 structural image is not
claimed automatically. A total P87/P89 lift over the actual north
polygon is EQUIVALENT to all three selected primitive lifting
families, rather than implied by the physical Dart information.
Conditional on the exact primitive interface, reuse the true
C60 physical fifth Dart pair from Qi v4.4 and its exact
four-class quotient reflection / shadow factorization.

No substitution of .original(f) for phi(f), no fabricated 4-cell,
no P92B naturality backport, no physical-to-higher-certificate
authority escalation. Independent Kuu -> Qi, strict 空 authority,
root107, append-only/tighten-only, protected draft #1558 untouched.
Lean v4.30.0-rc2 / pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide, or new axioms.
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

private def fivefoldGK5ALNorthFirstRoute :=
  nativeF54P92UnitRoute northNativeF45FirstStage

private def fivefoldGK5ALNorthSecondRoute :=
  nativeF54P92UnitRoute northNativeF45SecondStage

/-- The ORIGINAL P80 horizontal-unit source generator instantiated
on two real north-C60 adjacent F45 stages (not a mock route). -/
def fivefoldGK5ALNorthHorizontalPrimitive :
    NativeGK5ALPrimitiveUnitFourCell
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        fivefoldGK5ALNorthFirstRoute).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          fivefoldGK5ALNorthSecondRoute))
      (.ident (nativeF55HorizontalUnitRoute
        fivefoldGK5ALNorthFirstRoute fivefoldGK5ALNorthSecondRoute)) :=
  .horizontalUnit fivefoldGK5ALNorthFirstRoute fivefoldGK5ALNorthSecondRoute

/-- The original P80 LEFT-context unit on actual first / second
north F45 stages. Its structural image is a separate condition. -/
def fivefoldGK5ALNorthLeftContextPrimitive :
    NativeGK5ALPrimitiveUnitFourCell
      (.leftContext (.ident fivefoldGK5ALNorthFirstRoute)
        northNativeF45SecondStage)
      (.ident (.leftContext fivefoldGK5ALNorthFirstRoute
        northNativeF45SecondStage)) :=
  .leftContextUnit fivefoldGK5ALNorthFirstRoute northNativeF45SecondStage

/-- The original P80 RIGHT-context unit on actual north F45
stages; typed original F54 boundaries are never quotiented. -/
def fivefoldGK5ALNorthRightContextPrimitive :
    NativeGK5ALPrimitiveUnitFourCell
      (.rightContext northNativeF45FirstStage
        (.ident fivefoldGK5ALNorthSecondRoute))
      (.ident (.rightContext northNativeF45FirstStage
        fivefoldGK5ALNorthSecondRoute)) :=
  .rightContextUnit northNativeF45FirstStage fivefoldGK5ALNorthSecondRoute

/-- The three actual SOURCE primitive generators embed as real
original P87 four-cells, independently of any P93 evidence. -/
theorem fivefoldGK5ALNorthThreeOriginalP87Witnesses :
    Nonempty (NativeF55P87ClosedFourCell
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        fivefoldGK5ALNorthFirstRoute).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          fivefoldGK5ALNorthSecondRoute))
      (.ident (nativeF55HorizontalUnitRoute
        fivefoldGK5ALNorthFirstRoute fivefoldGK5ALNorthSecondRoute))) ∧
    Nonempty (NativeF55P87ClosedFourCell
      (.leftContext (.ident fivefoldGK5ALNorthFirstRoute)
        northNativeF45SecondStage)
      (.ident (.leftContext fivefoldGK5ALNorthFirstRoute
        northNativeF45SecondStage))) ∧
    Nonempty (NativeF55P87ClosedFourCell
      (.rightContext northNativeF45FirstStage
        (.ident fivefoldGK5ALNorthSecondRoute))
      (.ident (.rightContext northNativeF45FirstStage
        fivefoldGK5ALNorthSecondRoute))) := by
  exact ⟨⟨fivefoldGK5ALNorthHorizontalPrimitive.toP87⟩,
    ⟨fivefoldGK5ALNorthLeftContextPrimitive.toP87⟩,
    ⟨fivefoldGK5ALNorthRightContextPrimitive.toP87⟩⟩

private abbrev fivefoldGK5ALNorthOrigin :=
  Site.vertex (cyclicBoundaryDart (.pentagon .north)
    (firstFourPolygonSector (.pentagon .north) 0).1.val)

private abbrev fivefoldGK5ALNorthTarget :=
  Site.face (.pentagon .north)

/-- The COMPLETE three-constructor primitive structural boundary
specialized to the true two-Site north C60 physical context.
This universal indexed Type-valued interface is NOT assumed inhabited. -/
abbrev FivefoldGK5ALNorthPrimitiveBoundary :=
  NativeGK5ALPrimitiveBoundary
    (a := fivefoldGK5ALNorthOrigin)
    (b := fivefoldGK5ALNorthTarget)
    (x := fivefoldGK5ALNorthOrigin)
    (y := fivefoldGK5ALNorthTarget)
    (.pentagon .north)

/-- The old P87 structural boundary of Qi v4.4 is present exactly
when the three original P80 north-C60 primitive families lift. -/
theorem fivefoldGK5ALNorthP87_iff_threePrimitive :
    Nonempty FivefoldGK5AKNorthP87Boundary ↔
      Nonempty FivefoldGK5ALNorthPrimitiveBoundary :=
  nativeGK5ALP87Structural_nonempty_iff_primitive (.pentagon .north)

/-- The same iff for the COMPLETE THIRTEEN constructors of
the original P89 interchange presentation. No P87 closure or
source Type-valued proof history is silently discarded. -/
theorem fivefoldGK5ALNorthP89_iff_threePrimitive :
    Nonempty (NativeGK5AKP89StructuralBoundary
      (a := fivefoldGK5ALNorthOrigin)
      (b := fivefoldGK5ALNorthTarget)
      (x := fivefoldGK5ALNorthOrigin)
      (y := fivefoldGK5ALNorthTarget)
      (.pentagon .north)) ↔
      Nonempty FivefoldGK5ALNorthPrimitiveBoundary :=
  nativeGK5ALP89Structural_nonempty_iff_primitive (.pentagon .north)

/-- The TRUE physical fifth-around north C60 Dart pair is paired
with the actual original P89→P93 four-class quotient map once,
and ONLY once, the three typed P80 primitive boundaries are supplied. -/
def fivefoldGK5ALNorthPhysicalFourClassMap
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (base : FivefoldGK5ALNorthPrimitiveBoundary) :
    FivefoldGK5AKNorthP89FourClasses →
      (Dart × Dart) × FivefoldGK5AKNorthP93FourClasses :=
  fivefoldGK5AKNorthPhysicalFourClassMap frame i
    (nativeGK5ALP87_of_primitive (.pentagon .north) base)

/-- Conditional exact injectivity/reflection gate remains the
same TRUE P89/P93 four-cell comparison, not physical Dart equality. -/
theorem fivefoldGK5ALNorthPhysicalInjective_iff_reflect
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (base : FivefoldGK5ALNorthPrimitiveBoundary) :
    Function.Injective
      (fivefoldGK5ALNorthPhysicalFourClassMap frame i base) ↔
    (∀ f g : NativeGK5AINorthPentagonCells,
      Nonempty (NativeF55P93AssocFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)) →
      Nonempty (NativeF55P89InterchangeFourCell f g)) :=
  fivefoldGK5AKNorthPhysicalFourClass_injective_iff_reflect
    frame i (nativeGK5ALP87_of_primitive (.pentagon .north) base)

/-- All three signed/odd coordinates of actual north C60
retain their value under the conditional primitive-based map. -/
theorem fivefoldGK5ALNorthPhysicalShadow_commutes
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (base : FivefoldGK5ALNorthPrimitiveBoundary)
    (q : FivefoldGK5AKNorthP89FourClasses) :
    nativeF55P93AssocFourToShadow
      (KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      (KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      northNativeF45PentagonLong northNativeF45PentagonShort
      (fivefoldGK5ALNorthPhysicalFourClassMap frame i base q).2 =
    nativeF55P89FourToShadow
      (KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      (KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      northNativeF45PentagonLong northNativeF45PentagonShort q :=
  fivefoldGK5AKNorthPhysicalFourShadow_commutes
    frame i (nativeGK5ALP87_of_primitive (.pentagon .north) base) q

#print axioms fivefoldGK5ALNorthHorizontalPrimitive
#print axioms fivefoldGK5ALNorthLeftContextPrimitive
#print axioms fivefoldGK5ALNorthRightContextPrimitive
#print axioms fivefoldGK5ALNorthThreeOriginalP87Witnesses
#print axioms fivefoldGK5ALNorthP87_iff_threePrimitive
#print axioms fivefoldGK5ALNorthP89_iff_threePrimitive
#print axioms fivefoldGK5ALNorthPhysicalFourClassMap
#print axioms fivefoldGK5ALNorthPhysicalInjective_iff_reflect
#print axioms fivefoldGK5ALNorthPhysicalShadow_commutes

end
end KUOS.Architecture.WuxingPentagonUnified
