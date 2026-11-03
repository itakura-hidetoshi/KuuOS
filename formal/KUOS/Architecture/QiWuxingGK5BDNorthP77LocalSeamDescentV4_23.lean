import KUOS.Architecture.QiWuxingGK5BCNorthDirectLocalSeamV4_22
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BDP77ClassLocalSeamDescent
import Mathlib.Tactic

/-!
Qi v4.23 / F112-P94D3GK5BD — concrete genuine NORTH C60
P77 finite-source-word certificates and quotient-descended
local original-to-recursive-phi P94A seam existence.

This Qi layer IMPORTS the already verified independent Kuu
GK5BD theorem; it does not reverse its authority or manufacture
a new global seam. We explicitly construct a length-one P77
word from the TRUE north F55 pentagon to its original right-unit
composite, and a length-two word to a DOUBLE original right-unit
composite. Their original four-cell quotient classes coincide.

The resulting positive class property is an actual
Quotient.lift of local seam EXISTENCE, not an equality of
underlying 3-proof syntax or Type-valued 4-cell witnesses.
In the same genuine north F54 slot, the original identity
class remains negative, raw trans split shells remain absent,
and GK5AY universal gluing remains impossible.

The independent top hexagon disjointSquare atom produces
its own true original left-identity composite local seam;
its strong trans split shell is impossible too. The north
physical C60 fifth Dart closure, e04/e43 orientation gaps,
and exact conditional original-P89 BadPair boundary are not
identified with the wrapper-count obstruction.

Strict 空 authority; independent Kuu→Qi; original F54 two-Nat,
categories and Blocks histories preserved. Same public root107;
protected PR #1558 Draft/open; Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, no Gray, sorry, admit, native_decide, or axioms.
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

private def fivefoldGK5BDNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BDNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- A genuinely different original F55 source proof: the
pentagon with TWO actual F55 right identity insertions. -/
def fivefoldGK5BDNorthDoubleRightUnit :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
    nativeGK5AINorthPentagonWithIdentity
    (.ident northNativeF45PentagonShort)

/-- One genuine source-P77 right-unit 4-cell, reversed to
orient the finite certificate word FROM the original atom. -/
def fivefoldGK5BDNorthFirstRightUnitWord :
    NativeGK5BDP77Word fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
      nativeGK5AGNorthOriginalCell
      nativeGK5AINorthPentagonWithIdentity :=
  .snoc .nil (.symm (.rightUnit nativeGK5AGNorthOriginalCell))

/-- A TRUE two-step dependent word from the original primitive
to the doubly right-unit-extended source, retaining all
original F54 route indices. -/
def fivefoldGK5BDNorthDoubleRightUnitWord :
    NativeGK5BDP77Word fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
      nativeGK5AGNorthOriginalCell
      fivefoldGK5BDNorthDoubleRightUnit :=
  .snoc fivefoldGK5BDNorthFirstRightUnitWord
    (.symm (.rightUnit nativeGK5AINorthPentagonWithIdentity))

/-- The actual north pentagon and double-right-unit original
F55 proofs have EXACTLY the same true P77 four-cell quotient
class; this equality is not a raw Type-valued proof equality. -/
theorem fivefoldGK5BDNorthDoubleRightUnit_same_class :
    nativeF55RawVerticalFourClass
      fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
      nativeGK5AGNorthOriginalCell =
    nativeF55RawVerticalFourClass
      fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
      fivefoldGK5BDNorthDoubleRightUnit :=
  (nativeGK5BDWord_iff_same_P77_class
    nativeGK5AGNorthOriginalCell
    fivefoldGK5BDNorthDoubleRightUnit).mp
      ⟨fivefoldGK5BDNorthDoubleRightUnitWord⟩

/-- A constructed P94A direct bridge exists at the doubly
unit-extended ORIGINAL source. No impossible GK5BA split shell
nor an original-identity local seam is required. -/
def fivefoldGK5BDNorthDoubleRightUnitSeam :
    nativeGK5AZSeamAt fivefoldGK5BDNorthDoubleRightUnit :=
  nativeGK5BDSeam_of_word
    fivefoldGK5BDNorthDoubleRightUnitWord
    nativeGK5AZNorthPentagonAtom

/-- This is a concrete P77-QUOTIENT class predicate, defined
by the GK5BD genuine Quotient.lift, at a real north C60 class. -/
theorem fivefoldGK5BDNorthDoubleRightUnit_class_positive :
    nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
        fivefoldGK5BDNorthDoubleRightUnit) :=
  nativeGK5BDPositiveClass_of_word
    fivefoldGK5BDNorthDoubleRightUnitWord
    nativeGK5AZNorthPentagonAtom

/-- The original identity quotient class is NEGATIVE in the
same real north F54 source slot: positive local P77 orbit
does NOT imply a global original→phi seam. -/
theorem fivefoldGK5BDNorthIdentityClass_negative :
    ¬ nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
      northNativeF45PentagonShort northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          northNativeF45PentagonShort)) :=
  nativeGK5BDIdentityClass_no_seam northNativeF45PentagonShort

/-- True double-unit north local seam coexists with absence of
the strictly stronger trans shell AND of universal global
descent. Neither contradiction nor proof-class collapse occurs. -/
theorem fivefoldGK5BDNorthDoubleUnit_local_yes_shell_global_no :
    Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BDNorthDoubleRightUnit) ∧
    ¬ Nonempty (nativeGK5BARequiredShell
      fivefoldGK5BDNorthDoubleRightUnit) ∧
    ¬ Nonempty (NativeGK5AYOriginalPhiSeam
      fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast) :=
  ⟨⟨fivefoldGK5BDNorthDoubleRightUnitSeam⟩,
    (nativeGK5BDNorthDoubleRightUnit_seam_but_no_shell).2,
    nativeGK5BBNorthNoGlobalSeam⟩

/-- Independent actual north hexagon disjointSquare primitive:
its left original F55 identity extension also has a DIRECT local
P94A seam and NO GK5BA raw trans split shell. -/
theorem fivefoldGK5BDNorthSquareLeftUnit_seam_but_no_shell :
    Nonempty (nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northHexagonNativeSquareLeft)
        northHexagonNativeF55SquareCell)) ∧
    ¬ Nonempty (nativeGK5BARequiredShell
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northHexagonNativeSquareLeft)
        northHexagonNativeF55SquareCell)) :=
  ⟨⟨nativeGK5BDNorthSquareLeftUnitDirectSeam⟩,
    nativeGK5BBRequiredTrans_empty
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northHexagonNativeSquareLeft)
      northHexagonNativeF55SquareCell⟩

/-- The north physical gauge and genuine positive quotient
class do not settle the distinct original P89 class-map
reflection problem: its exact BadPair criterion remains an iff. -/
theorem fivefoldGK5BDNorthPhysicalClassAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    nativeGK5BDSeamExistsOnP77Class
      fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        fivefoldGK5BDNorthFirst fivefoldGK5BDNorthLast
        fivefoldGK5BDNorthDoubleRightUnit) ∧
    ¬ Nonempty (nativeGK5BARequiredShell
      fivefoldGK5BDNorthDoubleRightUnit) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) :=
  ⟨fivefoldGK5BDNorthDoubleRightUnit_class_positive,
    (nativeGK5BDNorthDoubleRightUnit_seam_but_no_shell).2,
    (fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i).1⟩

#print axioms fivefoldGK5BDNorthDoubleRightUnit
#print axioms fivefoldGK5BDNorthFirstRightUnitWord
#print axioms fivefoldGK5BDNorthDoubleRightUnitWord
#print axioms fivefoldGK5BDNorthDoubleRightUnit_same_class
#print axioms fivefoldGK5BDNorthDoubleRightUnitSeam
#print axioms fivefoldGK5BDNorthDoubleRightUnit_class_positive
#print axioms fivefoldGK5BDNorthIdentityClass_negative
#print axioms fivefoldGK5BDNorthDoubleUnit_local_yes_shell_global_no
#print axioms fivefoldGK5BDNorthSquareLeftUnit_seam_but_no_shell
#print axioms fivefoldGK5BDNorthPhysicalClassAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified
