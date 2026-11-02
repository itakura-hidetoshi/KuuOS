import KUOS.Architecture.QiWuxingGK5ANP94NorthPhysicalRepairV4_7
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AOHorizontalUnitNecessity
import Mathlib.Tactic

/-!
Qi v4.8 / F112-P94D3GK5AO — exact primitive horizontal four-cell
lower bound on the ACTUAL first and second adjacent north C60
F45 stages, with full two-Nat original F54 history.

Independent GK5AO proves a new Boolean P92B raw 3-proof flag is
preserved by ALL present P93 four-cells and by ALL P94A four-cell
witnesses with ZERO occurrences of P94A's explicitly adjoined
horizontalUnit. The actual P92B horizontal pair of identities
has Boolean flag TRUE, while the genuine F54 horizontal-route
identity has FALSE. Thus every such P94A comparison MUST use
horizontalUnit at least once and an explicit certificate uses
exactly one: a genuine minimality theorem relative to this
specific P94A presentation and its full nineteen-constructor
closure; no assertion about arbitrary other presentations.

Here the two witness inputs are not invented: they are the true
first and second independent north C60 native F45 stages, with
real typed F54 unit routes. Both the old P93 horizontal non-lift
and the positive P94A one-generator normalization are proven
at these exact dependent types. The actual fifth-around physical
Dart closure, reversed 04/43 categorical directions and already
proven unconditional north P89→P94A higher boundary remain
separate, faithfully retained forms of evidence.

No changes to P93/P94A source, no erasure of original F55
histories, no physical-to-higher certificate promotion, Gray,
unrestricted descent or added logical axioms. Independent Kuu
→ Qi only, strict 空 authority, append-only and public root107.
Protect PR #1558 Draft/open/unmerged. Fixed Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry or native_decide. Copyright (c) 2026 Hidetoshi
Itakura / 板倉英俊. Apache-2.0.
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

private def fivefoldGK5AONorthFirstUnit :=
  nativeF54P92UnitRoute northNativeF45FirstStage

private def fivefoldGK5AONorthSecondUnit :=
  nativeF54P92UnitRoute northNativeF45SecondStage

private def fivefoldGK5AONorthHorizontalRaw :=
  (NativeF55P92AssocComparison.refl fivefoldGK5AONorthFirstUnit).horizontal
    (NativeF55P92AssocComparison.refl fivefoldGK5AONorthSecondUnit)

private def fivefoldGK5AONorthHorizontalIdent :=
  NativeF55P92AssocComparison.refl
    (nativeF54P90HorizontalRoute
      fivefoldGK5AONorthFirstUnit fivefoldGK5AONorthSecondUnit)

/-- A real north C60 horizontal identity pair is not comparable
with the strict horizontal identity by ANY historical P93 4-cell,
including all sixteen P93 constructors and closures. -/
theorem fivefoldGK5AONorthP93Horizontal_noFourCell :
    ¬ Nonempty (NativeF55P93AssocFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent) :=
  nativeGK5AOP93HorizontalUnit_noFourCell
    fivefoldGK5AONorthFirstUnit fivefoldGK5AONorthSecondUnit

/-- The same actual F54 two-stage C60 source has a genuine
selected-P94A four-cell by its honestly new horizontalUnit
generator, with no new Lean axiom. -/
def fivefoldGK5AONorthP94HorizontalCertificate :
    NativeF55P94UnitFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent :=
  .horizontalUnit fivefoldGK5AONorthFirstUnit
    fivefoldGK5AONorthSecondUnit

/-- The actual chosen north certificate uses the P94A new
horizontalUnit constructor exactly ONCE. -/
theorem fivefoldGK5AONorthP94Certificate_count_one :
    fivefoldGK5AONorthP94HorizontalCertificate.gk5aoHorizontalUnitCount = 1 := rfl

/-- No P94A four-cell connecting the true north horizontal
identity pair to its strict F54 identity can avoid use of
horizontalUnit: all such genuine proof terms have count >= 1. -/
theorem fivefoldGK5AONorthP94AllCertificates_needHorizontal
    (w : NativeF55P94UnitFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent) :
    1 ≤ w.gk5aoHorizontalUnitCount :=
  nativeGK5AOHorizontalUnit_requires_primitive
    fivefoldGK5AONorthFirstUnit fivefoldGK5AONorthSecondUnit w

/-- Exact north C60 primitive necessity and sufficiency:
old P93 target unavailable, P94A target inhabited by one
new explicit horizontalUnit, and every actual P94A witness
requires at least one such generator. -/
theorem fivefoldGK5AONorthHorizontal_minimality :
    (¬ Nonempty (NativeF55P93AssocFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent)) ∧
    (∃ w : NativeF55P94UnitFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent,
      w.gk5aoHorizontalUnitCount = 1) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent,
      1 ≤ w.gk5aoHorizontalUnitCount) :=
  ⟨fivefoldGK5AONorthP93Horizontal_noFourCell,
    ⟨fivefoldGK5AONorthP94HorizontalCertificate,
      fivefoldGK5AONorthP94Certificate_count_one⟩,
    fivefoldGK5AONorthP94AllCertificates_needHorizontal⟩

/-- The actual fifth-around north C60 Dart closure, both
reversed physical categorical 04/43 orientations, and the
independently repaired full P89→P94A structural boundary
coexist with the one-generator north horizontal minimum.
The physical endpoints never license a P93 four-cell. -/
theorem fivefoldGK5AONorthPhysicalHorizontalMinimality
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    Nonempty FivefoldGK5ANP94NorthFullBoundary ∧
    (¬ Nonempty (NativeF55P93AssocFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent)) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5AONorthHorizontalRaw
      fivefoldGK5AONorthHorizontalIdent,
      1 ≤ w.gk5aoHorizontalUnitCount) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  rcases fivefoldGK5ANP94NorthPhysicalRepairAndOrientation frame i with
    ⟨hclosed, _, hrepair, h04, h43⟩
  exact ⟨hclosed, hrepair, fivefoldGK5AONorthP93Horizontal_noFourCell,
    fivefoldGK5AONorthP94AllCertificates_needHorizontal,
    h04, h43⟩

#print axioms fivefoldGK5AONorthP93Horizontal_noFourCell
#print axioms fivefoldGK5AONorthP94HorizontalCertificate
#print axioms fivefoldGK5AONorthP94Certificate_count_one
#print axioms fivefoldGK5AONorthP94AllCertificates_needHorizontal
#print axioms fivefoldGK5AONorthHorizontal_minimality
#print axioms fivefoldGK5AONorthPhysicalHorizontalMinimality

end
end KUOS.Architecture.WuxingPentagonUnified
