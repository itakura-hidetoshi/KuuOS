import KUOS.Architecture.QiWuxingGK5BBNorthOriginalWrapperObstructionV4_21
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BCLocalUnitSeamWithoutShell
import Mathlib.Tactic

/-!
Qi v4.22 / F112-P94D3GK5BC — positive genuine NORTH C60 local
four-cell seam via original P77 source vertical-right-unit, despite
the unconditional original-wrapper count no-go of GK5BB.

The TRUE north four-stage pentagon primitive p has a reflexive
raw original→recursive phi local seam. The real composite
c := F55.trans p (F55.ident short) is a different original raw
three-proof. We embed P77.rightUnit into chosen P94A through
ALL SEVEN historical old layers P80/P85/P86/P87/P89/P93C/P94A,
then compose with the INVERSE of P94A.verticalRightUnit to
construct a TRUE P94A four-cell original(c) → phi(c).

The previously GK5BB-UNINHABITED raw trans SPLIT SHELL
original(c) → trans(original(p),original(ident short)) is
NOT used and stays impossible. Thus existence of the local
direct 4-cell is strictly weaker than GK5BA's sufficient
trans shell, and the GK5AY global seam remains impossible
at this same actual north F54 slot.

The original P89 source reflection or BadPair boundary remains
separate; no unconditional original P89 source-map injectivity/
noninjectivity or a new higher proof construction from
physical C60 gauge is claimed. Real fifth-around Dart and
e04/e43 physical/category orientations are preserved.

Strict 空 authority, independent Kuu→Qi, original F54 2-Nat/
category/Blocks witnesses, root107, protected PR #1558 Draft/open.
Lean v4.30.0-rc2 and pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms/Gray/sorry/admit/native_decide. Append-only.
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

private def fivefoldGK5BCNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BCNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- A TRUE old ORIGINAL P77 right-unit four-proof at the real
north F54 long and short routes, without a selected-GK5BA kit. -/
def fivefoldGK5BCNorthOriginalRightUnitP77 :
    NativeF55RawVerticalFourCell
      fivefoldGK5BCNorthFirst fivefoldGK5BCNorthLast
      nativeGK5AINorthPentagonWithIdentity
      nativeGK5AGNorthOriginalCell :=
  nativeGK5AJNorthOriginalRightUnitFour

/-- All seven historical higher witness embeddings produce a
REAL selected RAW P94A four-cell at raw original endpoints,
without equating original F55 three-proof terms. -/
def fivefoldGK5BCNorthRawRightUnitP94 :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.original
        nativeGK5AGNorthOriginalCell) :=
  nativeGK5BCP77_to_rawP94 fivefoldGK5BCNorthOriginalRightUnitP77

/-- The genuine selected P94A right vertical unit provides the
second comparison edge between trans(original pentagon,refl)
and original pentagon, directly at the true original F54 slot. -/
def fivefoldGK5BCNorthSelectedRightUnitP94 :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.trans
        (NativeF55P92AssocComparison.original
          nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.refl
          northNativeF45PentagonShort))
      (NativeF55P92AssocComparison.original
        nativeGK5AGNorthOriginalCell) :=
  .verticalRightUnit _

/-- The long-unresolved direct local higher seam at the actual
north original pentagon-plus-right-identity source is CONSTRUCTED:
raw P77 right unit, reversed chosen P94A right unit. It does
NOT require an impossible original-ident seam or trans shell. -/
def fivefoldGK5BCNorthDirectSeam :
    nativeGK5AZSeamAt nativeGK5AINorthPentagonWithIdentity :=
  .trans fivefoldGK5BCNorthRawRightUnitP94
    (.symm fivefoldGK5BCNorthSelectedRightUnitP94)

/-- The direct local seam is a real 4-cell between actual
UNEQUAL raw P92B proof terms with compatible original-wrapper
count, without postulating raw proof equality. -/
theorem fivefoldGK5BCNorthDirectSeam_nontrivial :
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity) ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity) ∧
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity).gk5bbOriginalCount =
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity).gk5bbOriginalCount) :=
  ⟨nativeGK5AYNorthRawOriginal_ne_structuralPhi,
   ⟨fivefoldGK5BCNorthDirectSeam⟩,
   nativeGK5BBNorthRightIdentity_count_equal⟩

/-- An ACTUAL positive local seam, and the nonexistence of
GK5BA's strictly stronger raw trans constructor shell, hold
at EXACTLY the same original F55 north composite. -/
theorem fivefoldGK5BCNorthDirectSeam_but_no_transShell :
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    ¬ Nonempty (nativeGK5BARequiredShell
      nativeGK5AINorthPentagonWithIdentity) :=
  nativeGK5BCNorthDirectSeam_and_no_split

/-- The direct seam's existence cannot force an inhabitant of
the stronger GK5BA constructor-indexed local shell, as explicitly
witnessed by a genuine original north C60 F55 composite. -/
theorem fivefoldGK5BCNorthLocalSeam_not_implies_shell :
    ¬ (Nonempty (nativeGK5AZSeamAt
          nativeGK5AINorthPentagonWithIdentity) →
       Nonempty (nativeGK5BARequiredShell
          nativeGK5AINorthPentagonWithIdentity)) :=
  nativeGK5BCNorthSeam_does_not_force_requiredShell

/-- A LOCAL direct seam truly exists while a GLOBAL seam
record is mathematically impossible over the very same genuine
north original F54 route slot. There is no global gluing. -/
theorem fivefoldGK5BCNorthLocal_yes_global_no :
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    ¬ Nonempty (NativeGK5AYOriginalPhiSeam
      fivefoldGK5BCNorthFirst fivefoldGK5BCNorthLast) :=
  nativeGK5BCNorthLocal_yes_global_no

/-- At the genuine north right unit source pair, the existence
of a selected direct seam is independent of any actual original
P89 vertical-right-unit reflection; the exact GK5AX BadPair
boundary remains an iff, not an unconditional source failure. -/
theorem fivefoldGK5BCNorthDirectSeam_P89_boundary :
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    (nativeGK5AQBadPair
      fivefoldGK5BCNorthFirst fivefoldGK5BCNorthLast
      nativeGK5AINorthPentagonWithIdentity nativeGK5AGNorthOriginalCell ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        nativeGK5AINorthPentagonWithIdentity
        nativeGK5AGNorthOriginalCell)) :=
  ⟨⟨fivefoldGK5BCNorthDirectSeam⟩,
   nativeGK5AXRightUnit_bad_iff_noP89 nativeGK5AGNorthOriginalCell⟩

/-- A true physical north-C60 fivefold gauge and the genuine
nontrivial Type-valued direct seam coexist. The raw trans
SPLIT shell and UNIVERSAL seam do NOT exist. The e04/e43
physical-vs-category orientation gaps, and original P89
conditional class-map obstruction, remain unchanged. -/
theorem fivefoldGK5BCNorthPhysicalLocalDirectSeam
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    (¬ Nonempty (nativeGK5BARequiredShell
      nativeGK5AINorthPentagonWithIdentity)) ∧
    (¬ Nonempty (NativeGK5AYOriginalPhiSeam
      fivefoldGK5BCNorthFirst fivefoldGK5BCNorthLast)) ∧
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
  exact ⟨⟨fivefoldGK5BCNorthDirectSeam⟩,
    nativeGK5BBRequiredTrans_empty
      nativeGK5AGNorthOriginalCell
      (.ident northNativeF45PentagonShort),
    nativeGK5BBNorthNoGlobalSeam, hClosed, h04, h43, hIff⟩

#print axioms fivefoldGK5BCNorthOriginalRightUnitP77
#print axioms fivefoldGK5BCNorthRawRightUnitP94
#print axioms fivefoldGK5BCNorthSelectedRightUnitP94
#print axioms fivefoldGK5BCNorthDirectSeam
#print axioms fivefoldGK5BCNorthDirectSeam_nontrivial
#print axioms fivefoldGK5BCNorthDirectSeam_but_no_transShell
#print axioms fivefoldGK5BCNorthLocalSeam_not_implies_shell
#print axioms fivefoldGK5BCNorthLocal_yes_global_no
#print axioms fivefoldGK5BCNorthDirectSeam_P89_boundary
#print axioms fivefoldGK5BCNorthPhysicalLocalDirectSeam

end
end KUOS.Architecture.WuxingPentagonUnified
