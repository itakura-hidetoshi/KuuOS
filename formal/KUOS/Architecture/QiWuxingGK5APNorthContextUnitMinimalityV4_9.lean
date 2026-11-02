import KUOS.Architecture.QiWuxingGK5AONorthHorizontalUnitMinimalityV4_8
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5APContextUnitIndependence
import Mathlib.Tactic

/-!
Qi v4.9 — true north C60 context-unit pairwise minimality.
Apply independent GK5AP exact P94A left/right 4-generator necessity
on the SAME genuine first and second adjacent north C60 F45 stages
used by Qi v4.8. Original F54 two-Nat route histories are retained,
as are north pentagon fifth-around physical Dart closure, BOTH
oppositely oriented categorical edges 04/43, and the unconditional
GK5AN original P89→P94A structural lift.

Both context-unit 4-cell families have exact primitive lower
bound ONE even when horizontalUnit and the opposite context unit
are allowed among all nineteen P94A constructors. Combined with
GK5AO horizontal independence, all three chosen unit families
are individually necessary in this selected presentation.
No promotion of physical observations to higher logical authority.
Independent Kuu -> Qi only, strict 空 authority, append-only/root107.
No new axioms, sorry, native_decide, Gray or global gluing.
Pinned Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

private def fivefoldGK5APNorthFirstUnit :=
  nativeF54P92UnitRoute northNativeF45FirstStage

private def fivefoldGK5APNorthSecondUnit :=
  nativeF54P92UnitRoute northNativeF45SecondStage

private def fivefoldGK5APNorthLeftRaw :=
  NativeF55P92AssocComparison.leftContext
    (.refl fivefoldGK5APNorthFirstUnit)
    northNativeF45SecondStage

private def fivefoldGK5APNorthLeftIdent :=
  NativeF55P92AssocComparison.refl
    (.leftContext fivefoldGK5APNorthFirstUnit northNativeF45SecondStage)

private def fivefoldGK5APNorthRightRaw :=
  NativeF55P92AssocComparison.rightContext
    northNativeF45FirstStage
    (.refl fivefoldGK5APNorthSecondUnit)

private def fivefoldGK5APNorthRightIdent :=
  NativeF55P92AssocComparison.refl
    (.rightContext northNativeF45FirstStage fivefoldGK5APNorthSecondUnit)

/-- Even all sixteen selected P93 four-rules cannot normalize
the actual first-stage north C60 left-context raw identity. -/
theorem fivefoldGK5APNorthLeftP93_noFourCell :
    ¬ Nonempty (NativeF55P93AssocFourCell
      fivefoldGK5APNorthLeftRaw fivefoldGK5APNorthLeftIdent) :=
  nativeGK5APP93LeftContextUnit_noFourCell
    fivefoldGK5APNorthFirstUnit northNativeF45SecondStage

/-- The actual second-stage right-context raw identity likewise
cannot be normalized in P93, even with all old closures. -/
theorem fivefoldGK5APNorthRightP93_noFourCell :
    ¬ Nonempty (NativeF55P93AssocFourCell
      fivefoldGK5APNorthRightRaw fivefoldGK5APNorthRightIdent) :=
  nativeGK5APP93RightContextUnit_noFourCell
    northNativeF45FirstStage fivefoldGK5APNorthSecondUnit

/-- A genuine P94A left-context primitive on two physical north F45 stages. -/
def fivefoldGK5APNorthLeftCertificate :
    NativeF55P94UnitFourCell
      fivefoldGK5APNorthLeftRaw fivefoldGK5APNorthLeftIdent :=
  .leftContextUnit fivefoldGK5APNorthFirstUnit
    northNativeF45SecondStage

/-- A genuine P94A right-context primitive on the SAME stages. -/
def fivefoldGK5APNorthRightCertificate :
    NativeF55P94UnitFourCell
      fivefoldGK5APNorthRightRaw fivefoldGK5APNorthRightIdent :=
  .rightContextUnit northNativeF45FirstStage
    fivefoldGK5APNorthSecondUnit

/-- The two chosen actual north witnesses each use its own
necessary primitive exactly once, definitionally. -/
theorem fivefoldGK5APNorthLeftCertificate_count_one :
    fivefoldGK5APNorthLeftCertificate.gk5apLeftUnitCount = 1 := rfl

theorem fivefoldGK5APNorthRightCertificate_count_one :
    fivefoldGK5APNorthRightCertificate.gk5apRightUnitCount = 1 := rfl

/-- Every actual north P94A left-context normalization needs at least
one LEFT generator, EVEN IF rightContextUnit/horizontalUnit are used. -/
theorem fivefoldGK5APNorthAllCertificates_needLeft
    (w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthLeftRaw fivefoldGK5APNorthLeftIdent) :
    1 ≤ w.gk5apLeftUnitCount :=
  nativeGK5APLeftContextUnit_requires_primitive
    fivefoldGK5APNorthFirstUnit northNativeF45SecondStage w

/-- The symmetric genuine north right-context lower bound. -/
theorem fivefoldGK5APNorthAllCertificates_needRight
    (w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthRightRaw fivefoldGK5APNorthRightIdent) :
    1 ≤ w.gk5apRightUnitCount :=
  nativeGK5APRightContextUnit_requires_primitive
    northNativeF45FirstStage fivefoldGK5APNorthSecondUnit w

/-- Simultaneous exact left/right independent primitive minimality:
P93 has neither comparison, but P94A has a one-generator witness
for each and EVERY such P94A witness needs that own generator. -/
theorem fivefoldGK5APNorthBothContextUnit_minimality :
    (¬ Nonempty (NativeF55P93AssocFourCell
      fivefoldGK5APNorthLeftRaw fivefoldGK5APNorthLeftIdent)) ∧
    (¬ Nonempty (NativeF55P93AssocFourCell
      fivefoldGK5APNorthRightRaw fivefoldGK5APNorthRightIdent)) ∧
    (∃ w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthLeftRaw fivefoldGK5APNorthLeftIdent,
      w.gk5apLeftUnitCount = 1) ∧
    (∃ w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthRightRaw fivefoldGK5APNorthRightIdent,
      w.gk5apRightUnitCount = 1) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthLeftRaw fivefoldGK5APNorthLeftIdent,
      1 ≤ w.gk5apLeftUnitCount) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthRightRaw fivefoldGK5APNorthRightIdent,
      1 ≤ w.gk5apRightUnitCount) :=
  ⟨fivefoldGK5APNorthLeftP93_noFourCell,
   fivefoldGK5APNorthRightP93_noFourCell,
   ⟨fivefoldGK5APNorthLeftCertificate,
     fivefoldGK5APNorthLeftCertificate_count_one⟩,
   ⟨fivefoldGK5APNorthRightCertificate,
     fivefoldGK5APNorthRightCertificate_count_one⟩,
   fivefoldGK5APNorthAllCertificates_needLeft,
   fivefoldGK5APNorthAllCertificates_needRight⟩

/-- The north-C60 pairwise-minimal P94A three-unit conclusion is
compatible with the actual fifth-around physical Dart pair,
original higher P89 structural repair, and the independently
preserved opposite 04/43 categorical orientations. -/
theorem fivefoldGK5APNorthPhysicalThreeUnitMinimality
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    Nonempty FivefoldGK5ANP94NorthFullBoundary ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthLeftRaw fivefoldGK5APNorthLeftIdent,
      1 ≤ w.gk5apLeftUnitCount) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5APNorthRightRaw fivefoldGK5APNorthRightIdent,
      1 ≤ w.gk5apRightUnitCount) ∧
    (∀ w : NativeF55P94UnitFourCell
      fivefoldGK5AONorthHorizontalRaw fivefoldGK5AONorthHorizontalIdent,
      1 ≤ w.gk5aoHorizontalUnitCount) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  rcases fivefoldGK5ANP94NorthPhysicalRepairAndOrientation frame i with
    ⟨hclosed, _, hrepair, h04, h43⟩
  exact ⟨hclosed, hrepair,
    fivefoldGK5APNorthAllCertificates_needLeft,
    fivefoldGK5APNorthAllCertificates_needRight,
    fivefoldGK5AONorthP94AllCertificates_needHorizontal,
    h04, h43⟩

#print axioms fivefoldGK5APNorthLeftP93_noFourCell
#print axioms fivefoldGK5APNorthRightP93_noFourCell
#print axioms fivefoldGK5APNorthLeftCertificate
#print axioms fivefoldGK5APNorthRightCertificate
#print axioms fivefoldGK5APNorthLeftCertificate_count_one
#print axioms fivefoldGK5APNorthRightCertificate_count_one
#print axioms fivefoldGK5APNorthAllCertificates_needLeft
#print axioms fivefoldGK5APNorthAllCertificates_needRight
#print axioms fivefoldGK5APNorthBothContextUnit_minimality
#print axioms fivefoldGK5APNorthPhysicalThreeUnitMinimality

end
end KUOS.Architecture.WuxingPentagonUnified
