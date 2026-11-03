import KUOS.Architecture.QiWuxingGK5AZNorthConstructorLocalSeamsV4_19
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BANineConstructorSeamInduction
import Mathlib.Tactic

/-!
Qi v4.20 / F112-P94D3GK5BA: the true original north C60
F54/F55 source inherits a genuine dependent GK5AY seam from
the nine-constructor GK5BA local-shell kit, if such a kit is
actually supplied for the two real independent Site categories.

The kit supplies exact constructor-indexed Type-valued
P94A local shells, not a shadow, chosen quotient, or global
raw equality. Ident and trans shells extracted at the true
north pentagon/right-unit composite recover Qi v4.19's two
concrete local gates; the dependent induction constructs
the complete original→recursive-phi seam, without assuming
GK5AY's global seam as a separate hypothesis.

Original P89 reflection remains conditional on genuine
source injectivity, or else is explicitly a GK5AQ BadPair.
The original F54 two-Nat/block histories, the physical
fifth-around Dart closure and e04/e43 orientation differences
are preserved. No claimed unconditional kit existence,
P89 faithfulness/nonfaithfulness, or all-P94A normalization.

Strict 空 / independent Kuu→Qi, root107, PR #1558 Draft/open.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide or Gray.
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

private def fivefoldGK5BANorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BANorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- ACTUAL original north C60 dependent seam, with a fully
explicit constructor-KIT hypothesis instead of an assumed
GK5AY global bridge record. This is an inhabited Type-valued
four-cell family at every original north F54 route slot. -/
def fivefoldGK5BANorthSeam_of_kit
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site) :
    NativeGK5AYOriginalPhiSeam
      fivefoldGK5BANorthFirst fivefoldGK5BANorthLast :=
  kit.toGK5AY fivefoldGK5BANorthFirst fivefoldGK5BANorthLast

/-- The precise pointwise local-shell existence condition,
if actually established for the two original Site categories,
constructs a north global seam. This does NOT assert the input. -/
theorem fivefoldGK5BANorthSeam_of_allLocal
    (h : nativeGK5BAAllLocalShells (.pentagon .north) Site Site) :
    Nonempty (NativeGK5AYOriginalPhiSeam
      fivefoldGK5BANorthFirst fivefoldGK5BANorthLast) :=
  nativeGK5BAAllLocal_constructs_GK5AY
    (.pentagon .north) Site Site h
    fivefoldGK5BANorthFirst fivefoldGK5BANorthLast

/-- The genuine ORIGINAL north F55 identity shell is ONE
constructor-local kit value, not a definitionally equal raw
original and selected P92B refl proof term. -/
def fivefoldGK5BANorthIdentGate_of_kit
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site) :
    nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northNativeF45PentagonShort) :=
  kit.shell (.ident northNativeF45PentagonShort)

/-- The distinct full ORIGINAL north composite has a true
raw-unwrapping trans shell extracted from the kit; it is
a 4-cell, not raw proof-term equality. -/
def fivefoldGK5BANorthTransGate_of_kit
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.trans
        (NativeF55P92AssocComparison.original
          nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
            northNativeF45PentagonShort))) :=
  kit.shell nativeGK5AINorthPentagonWithIdentity

/-- Unconditional raw inequality remains compatible with an
actual north composite seam constructed by the full dependent
nine-constructor recursion, under the source kit only. -/
theorem fivefoldGK5BANorthComposite_nontrivial_seam
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site) :
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity) ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity) ∧
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) :=
  ⟨nativeGK5AYNorthRawOriginal_ne_structuralPhi,
    ⟨kit.bridge nativeGK5AINorthPentagonWithIdentity⟩⟩

/-- The original north composite/right-unit selected comparison
is REAL P94A Type-valued evidence constructed from the kit;
this is still not a genuine original P89 four-proof. -/
def fivefoldGK5BANorthRawRightUnit_of_kit
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (NativeF55P92AssocComparison.original
        nativeGK5AGNorthOriginalCell) :=
  nativeGK5AZRawRightVerticalUnit nativeGK5AGNorthOriginalCell
    (kit.bridge nativeGK5AINorthPentagonWithIdentity)
    (kit.bridge nativeGK5AGNorthOriginalCell)

/-- A GENUINE north original P93C four-cell with the constructor
kit either reflects to original P89 or exposes a GK5AQ BadPair.
No conclusion is asserted without a real P93C witness. -/
theorem fivefoldGK5BANorthRawP93_reflect_or_bad
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site)
    (f g : NativeGK5AINorthPentagonCells)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
      nativeGK5AQBadPair
        fivefoldGK5BANorthFirst fivefoldGK5BANorthLast f g :=
  nativeGK5BARawP93_reflect_or_bad kit f g raw

/-- A REAL raw original north P93C obstruction, if supplied,
produces a noninjective original source four-class map at an
exact north F54 slot under the constructor kit. -/
theorem fivefoldGK5BANorthRawObstruction_noninjective
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site)
    (h : nativeGK5AYRawP93Obstruction
      fivefoldGK5BANorthFirst fivefoldGK5BANorthLast) :
    ∃ (r s : NativeGK5AGNorthHistory),
      ¬ Function.Injective
        (nativeGK5ANP89ToP94FourClassMap
          fivefoldGK5BANorthFirst fivefoldGK5BANorthLast r s) :=
  nativeGK5BARawObstruction_forces_noninjective
    kit fivefoldGK5BANorthFirst fivefoldGK5BANorthLast h

/-- IF all original P89-to-P94 source class maps are injective
then the actual constructor kit forces all raw P93C reflection.
Neither source injectivity nor kit existence is proved here. -/
theorem fivefoldGK5BANorthRawReflection_of_allInjective
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site)
    (hinj : ∀ (r s : NativeGK5AGNorthHistory),
      Function.Injective
        (nativeGK5ANP89ToP94FourClassMap
          fivefoldGK5BANorthFirst fivefoldGK5BANorthLast r s)) :
    nativeGK5AYRawP93Reflects
      fivefoldGK5BANorthFirst fivefoldGK5BANorthLast :=
  fivefoldGK5AYNorthRawReflects_of_allInjective
    (fivefoldGK5BANorthSeam_of_kit kit) hinj

/-- True physical fifth Dart and the 04/43 reversed
physical/category orientations coexist with an actually
assembled seam under the independent constructor kit.
C60 gauge does not supply the kit or original P89 proof. -/
theorem fivefoldGK5BANorthPhysicalSeam_from_kit
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (kit : NativeGK5BAConstructorShellKit (.pentagon .north) Site Site) :
    (((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity) ≠
       nativeGK5AIOriginalToP92Structural
         nativeGK5AINorthPentagonWithIdentity) ∧
      Nonempty (NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original
          nativeGK5AINorthPentagonWithIdentity)
        (nativeGK5AIOriginalToP92Structural
          nativeGK5AINorthPentagonWithIdentity))) ∧
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
        fivefoldGK5AQNorthReflectionObstruction) :=
  fivefoldGK5AYNorthPhysicalSeamGate frame i
    (fivefoldGK5BANorthSeam_of_kit kit)

#print axioms fivefoldGK5BANorthSeam_of_kit
#print axioms fivefoldGK5BANorthSeam_of_allLocal
#print axioms fivefoldGK5BANorthIdentGate_of_kit
#print axioms fivefoldGK5BANorthTransGate_of_kit
#print axioms fivefoldGK5BANorthComposite_nontrivial_seam
#print axioms fivefoldGK5BANorthRawRightUnit_of_kit
#print axioms fivefoldGK5BANorthRawP93_reflect_or_bad
#print axioms fivefoldGK5BANorthRawObstruction_noninjective
#print axioms fivefoldGK5BANorthRawReflection_of_allInjective
#print axioms fivefoldGK5BANorthPhysicalSeam_from_kit

end
end KUOS.Architecture.WuxingPentagonUnified
