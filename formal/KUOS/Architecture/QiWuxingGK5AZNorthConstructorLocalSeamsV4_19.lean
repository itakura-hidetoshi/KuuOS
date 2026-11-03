import KUOS.Architecture.QiWuxingGK5AYNorthOriginalPhiSeamV4_18
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AZConstructorLocalSeamObstruction
import Mathlib.Tactic

/-!
Qi v4.19 / F112-P94D3GK5AZ: real north C60 original
pentagon plus right-identity F55 composite is an explicit
constructor-local original-to-recursive-phi seam problem.

The original north pentagon generator has an unconditional atom
seam. The *real source F55 identity* raw wrapper is syntactically
distinct from the selected P92B refl, so its bridge is not
obtained by equality. Given its local higher identity bridge and
one explicit original-trans shell, P94A right/left whiskering
constructs a real four-cell between the raw composite wrapper and
recursive phi. No universal GK5AY seam is required.

The same two local gates provide a raw P94A right-unit comparison
between the original F55 composite and the original pentagon
atom. They do NOT give a genuine old P89 four-cell. The exact
GK5AX source reflection obstruction remains a conditional iff.

True north C60 fifth physical Dart closure and e04/e43 category
orientation distinctions remain independent of these gates.

Independent Kuu -> Qi, strict 空 authority, original F54
two-Nat/category/Blocks history retained, root107, #1558 Draft/open.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No Gray, no new axioms, sorry/admit or unconditional descent.
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

private def fivefoldGK5AZNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5AZNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The original north pentagon is one of the two truly atomic
original F55 constructors and is reflexively phi-bridged. -/
def fivefoldGK5AZNorthPentagonAtom :
    nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell :=
  .refl _

/-- The genuine original north right identity is NOT equal to
the recursively selected P92B refl as raw Type-valued syntax.
This does not rule out a higher 4-cell between them. -/
theorem fivefoldGK5AZNorthIdent_raw_ne_phi :
    (NativeF55P92AssocComparison.original
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort)) ≠
      nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          northNativeF45PentagonShort) :=
  nativeGK5AZIdent_raw_ne_phi northNativeF45PentagonShort

/-- One actual original north F55 identity bridge plus ONE
raw-trans shell suffice to construct the nontrivial true selected
4-cell between the ORIGINAL WHOLE composite and recursive phi.
No global seam record has been used. -/
def fivefoldGK5AZNorthCompositeSeam_of_local_gates
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort))
    (rawTransShell : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.trans
        (NativeF55P92AssocComparison.original
          nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
            northNativeF45PentagonShort)))) :
    nativeGK5AZSeamAt nativeGK5AINorthPentagonWithIdentity :=
  nativeGK5AZTrans_of_shell
    nativeGK5AGNorthOriginalCell
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
      northNativeF45PentagonShort)
    rawTransShell fivefoldGK5AZNorthPentagonAtom identBridge

/-- A genuinely non-equal raw-original/phi pair has an ACTUAL
selected four-cell under just these two concrete north local
gates. Equality of raw three-cell terms is still refuted. -/
theorem fivefoldGK5AZNorthCompositeSeam_is_not_raw_equality
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort))
    (rawTransShell : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.trans
        (NativeF55P92AssocComparison.original
          nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
            northNativeF45PentagonShort)))) :
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity) ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity) ∧
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) :=
  ⟨nativeGK5AYNorthRawOriginal_ne_structuralPhi,
    ⟨fivefoldGK5AZNorthCompositeSeam_of_local_gates
      identBridge rawTransShell⟩⟩

/-- If a north identity seam is available, the true full
composite seam exists OR its precise original-trans shell is
missing. This statement never asserts which branch holds. -/
theorem fivefoldGK5AZNorthComposite_seam_or_transShellHole
    (ident : Nonempty (nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort))) :
    Nonempty (nativeGK5AZSeamAt nativeGK5AINorthPentagonWithIdentity) ∨
      nativeGK5AZTransShellHole
        nativeGK5AGNorthOriginalCell
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          northNativeF45PentagonShort) :=
  nativeGK5AZTrans_seam_or_shellHole
    nativeGK5AGNorthOriginalCell
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
      northNativeF45PentagonShort)
    ⟨fivefoldGK5AZNorthPentagonAtom⟩ ident

/-- Real original composite to real original pentagon RAW
P94A right unit from an actual ident bridge and raw trans shell.
The original P89 reflection remains separately unproven. -/
def fivefoldGK5AZNorthRawRightUnit_of_local_gates
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort))
    (rawTransShell : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.trans
        (NativeF55P92AssocComparison.original
          nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
            northNativeF45PentagonShort)))) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.original
        nativeGK5AGNorthOriginalCell) :=
  nativeGK5AZRawRightUnit_from_local_gates
    nativeGK5AGNorthOriginalCell fivefoldGK5AZNorthPentagonAtom
    identBridge rawTransShell

/-- Local selected raw-right-unit evidence coexists with the
exact genuine original P89 reflection obstruction from GK5AX.
The first conjunct is constructed; the iff is conditional and
does NOT settle the existence of its negated P89 evidence. -/
theorem fivefoldGK5AZNorthRawRightUnit_and_P89_obstruction
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort))
    (rawTransShell : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.trans
        (NativeF55P92AssocComparison.original
          nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
            northNativeF45PentagonShort)))) :
    Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.original
        nativeGK5AGNorthOriginalCell)) ∧
    (nativeGK5AQBadPair
      fivefoldGK5AZNorthFirst fivefoldGK5AZNorthLast
      nativeGK5AINorthPentagonWithIdentity nativeGK5AGNorthOriginalCell ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        nativeGK5AINorthPentagonWithIdentity
        nativeGK5AGNorthOriginalCell)) := by
  constructor
  · exact ⟨fivefoldGK5AZNorthRawRightUnit_of_local_gates
      identBridge rawTransShell⟩
  · exact nativeGK5AXRightUnit_bad_iff_noP89 nativeGK5AGNorthOriginalCell

/-- Genuinely physical north C60 fifth Dart closure and the
04/43 physical-vs-category orientation boundary coexist with
local seam-derived raw selected 4-cell. Gauge supplies neither
the identity bridge nor the trans-shell nor original P89 proof. -/
theorem fivefoldGK5AZNorthPhysicalLocalSeamGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort))
    (rawTransShell : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.trans
        (NativeF55P92AssocComparison.original
          nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
            northNativeF45PentagonShort)))) :
    Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.original
        nativeGK5AGNorthOriginalCell)) ∧
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
  exact ⟨⟨fivefoldGK5AZNorthRawRightUnit_of_local_gates
      identBridge rawTransShell⟩, hClosed, h04, h43, hIff⟩

#print axioms fivefoldGK5AZNorthPentagonAtom
#print axioms fivefoldGK5AZNorthIdent_raw_ne_phi
#print axioms fivefoldGK5AZNorthCompositeSeam_of_local_gates
#print axioms fivefoldGK5AZNorthCompositeSeam_is_not_raw_equality
#print axioms fivefoldGK5AZNorthComposite_seam_or_transShellHole
#print axioms fivefoldGK5AZNorthRawRightUnit_of_local_gates
#print axioms fivefoldGK5AZNorthRawRightUnit_and_P89_obstruction
#print axioms fivefoldGK5AZNorthPhysicalLocalSeamGate

end
end KUOS.Architecture.WuxingPentagonUnified
