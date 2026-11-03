import KUOS.Architecture.QiWuxingGK5AXNorthVerticalPrimitiveReflectionV4_17
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AYOriginalStructuralPhiSeamGate
import Mathlib.Tactic

/-!
Qi v4.18 / F112-P94D3GK5AY — north C60 original-versus-structural
phi seam and conditional original P89 reflection.

STACKED DRAFT, not a validated GitHub main theorem. The independent
GK5AY source PR #3022 has green exact-source Lean/Governance CI, but
was OPEN when this draft was made because GitHub writes were blocked.
This file has NOT been compiled by CI. It is intended to be added
as a new additive module only after preserving the GK5AY source.

The true original F55 north pentagon proof with a right identity
has distinct raw P92B.original and GK5AI's recursive phi images.
The conditional seam is an actual P94A four-cell, not an equality
of 3-cell syntax. Given a seam, raw P93C four-proofs can be transported
to structural phi endpoint comparisons, and missing original P89
four-proofs are classified as actual GK5AQ BadPairs. A raw P93C
obstruction forces noninjectivity of the original P89-to-P94A
four-class map at some exact north F54 route slot. This requires
both the seam and the raw obstruction; no such obstruction is
claimed to exist. Under an actual seam a raw P93C comparison
reflects to P89 or exhibits a genuine source BadPair. If ALL
source four-class maps are injective, raw P93C comparison reflects;
this is a conditional implication, not a proof of injectivity.

Genuine north physical fifth-around Dart closure, the e04/e43
physical-versus-categorical orientation distinctions, and the
conditional source reflection obstruction are retained unchanged.

Independent Kuu -> Qi, strict 空 authority, original F54 two-Nat
history preserved, public root 107, protect PR #1558 Draft/open.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray or global gluing.
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

private def fivefoldGK5AYNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5AYNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- A TRUE original north F55 composite has unequal raw P92B.original
and recursive-phi proofs; if a seam record is supplied, an ACTUAL
P94A four-cell bridges the unequal proof terms. -/
theorem fivefoldGK5AYNorthSeam_nontrivial
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast) :
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity) ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity) ∧
    Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity)) :=
  nativeGK5AYNorthSeam_is_not_raw_equality data

/-- With genuine selected seam four-cells, a raw P93C witness
between two ORIGINAL north F55 wrappers can be transported
across the exact dependent source endpoints to phi images. -/
def fivefoldGK5AYNorthRawP93ToStructural
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (f g : NativeGK5AINorthPentagonCells)
    (w : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g) :=
  data.transportP93 w

/-- For a REAL raw P93C comparison of two north source wrappers,
the source GK5AQ BadPair is equivalent to the absence of a
TRUE original P89 four-proof, conditional on a north seam. -/
theorem fivefoldGK5AYNorthRawP93_bad_iff_noP89
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (f g : NativeGK5AINorthPentagonCells)
    (w : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    nativeGK5AQBadPair fivefoldGK5AYNorthFirst
      fivefoldGK5AYNorthLast f g ↔
    ¬ Nonempty (NativeF55P89InterchangeFourCell f g) :=
  nativeGK5AYRawP93_bad_iff_noP89 data w

/-- An actual ORIGINAL P89 four-cell is valid in the original
source presentation AND can be mapped to a P94A phi comparison
via a given seam, without producing any GK5AQ BadPair. -/
theorem fivefoldGK5AYNorthP89Old_both
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (f g : NativeGK5AINorthPentagonCells)
    (original : NativeF55P89InterchangeFourCell f g) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∧
    Nonempty (NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)) ∧
    ¬ nativeGK5AQBadPair fivefoldGK5AYNorthFirst
      fivefoldGK5AYNorthLast f g :=
  nativeGK5AYOldP89SourceAndSelected data original

/-- A true original-source raw P93C nonreflection obstruction,
IF it exists, and a north seam together force a noninjective
original P89-to-P94A four-class map at an exact north route slot. -/
theorem fivefoldGK5AYNorthRawObstruction_noninjective
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (h : nativeGK5AYRawP93Obstruction
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast) :
    ∃ (r s : NativeGK5AGNorthHistory),
      ¬ Function.Injective
        (nativeGK5ANP89ToP94FourClassMap
          fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast r s) :=
  nativeGK5AYRawObstruction_forces_noninjective data h

/-- The TRUE north C60 physical fifth Dart closure and historical
04/43 reversed physical-versus-categorical orientations coexist
with a supplied genuine selected seam joining distinct P92B raw
and structural-phi proof terms. The physical gauge does not
supply the seam or settle original-source P89 injectivity. -/
theorem fivefoldGK5AYNorthPhysicalSeamGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast) :
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
        fivefoldGK5AQNorthReflectionObstruction) := by
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨fivefoldGK5AYNorthSeam_nontrivial data,
    hClosed, h04, h43, hIff⟩

/-- A HYPOTHESIZED raw P93C original-source obstruction and a
supplied north seam force an original class-map noninjectivity
at some F54 route slot while preserving the true physical
Dart closure and the still conditional global reflection iff. -/
theorem fivefoldGK5AYNorthPhysicalRawObstructionGate
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (h : nativeGK5AYRawP93Obstruction
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast) :
    (∃ (r s : NativeGK5AGNorthHistory),
      ¬ Function.Injective
        (nativeGK5ANP89ToP94FourClassMap
          fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast r s)) ∧
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
  have hBad := fivefoldGK5AYNorthRawObstruction_noninjective data h
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨hBad, hClosed, h04, h43, hIff⟩

/-- Exact north raw reflection iff absence of P93C/P89 source obstruction. -/
theorem fivefoldGK5AYNorthRawReflects_iff_noObstruction :
    nativeGK5AYRawP93Reflects
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast ↔
    ¬ nativeGK5AYRawP93Obstruction
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast :=
  nativeGK5AYRawP93Reflects_iff_no_obstruction
    fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast

/-- A supplied seam and an actual raw P93C comparison give
original P89 proof evidence, or a genuine source GK5AQ BadPair.
Neither disjunct is asserted to hold unconditionally. -/
theorem fivefoldGK5AYNorthRawComparison_reflect_or_bad
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (f g : NativeGK5AINorthPentagonCells)
    (w : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
    nativeGK5AQBadPair
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast f g := by
  classical
  by_cases h : Nonempty (NativeF55P89InterchangeFourCell f g)
  · exact .inl h
  · exact .inr ((nativeGK5AYRawP93_bad_iff_noP89 data w).2 h)

/-- Universal injectivity of TRUE ORIGINAL north four-class maps,
when explicitly assumed, forces raw P93C reflection under a seam.
The converse is not asserted. -/
theorem fivefoldGK5AYNorthRawReflects_of_allInjective
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (allInjective : ∀ (r s : NativeGK5AGNorthHistory),
      Function.Injective
        (nativeGK5ANP89ToP94FourClassMap
          fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast r s)) :
    nativeGK5AYRawP93Reflects
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast := by
  intro r s f g hw
  rcases hw with ⟨w⟩
  exact nativeGK5AYRawReflects_of_injective
    data (allInjective r s) f g w

/-- With an actual seam and explicitly assumed universal source
injectivity, raw reflection coexists with genuine fifth Dart
closure, e04/e43 physical orientation and conditional source
reflection obstruction. The physical frame supplies neither input. -/
theorem fivefoldGK5AYNorthPhysicalRawReflection_of_allInjective
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex)
    (data : NativeGK5AYOriginalPhiSeam
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast)
    (allInjective : ∀ (r s : NativeGK5AGNorthHistory),
      Function.Injective
        (nativeGK5ANP89ToP94FourClassMap
          fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast r s)) :
    nativeGK5AYRawP93Reflects
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast ∧
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
  have hreflect : nativeGK5AYRawP93Reflects
      fivefoldGK5AYNorthFirst fivefoldGK5AYNorthLast :=
    fivefoldGK5AYNorthRawReflects_of_allInjective data allInjective
  rcases fivefoldGK5AQNorthPhysicalReflectionAndOrientation frame i with
    ⟨hIff, hClosed, _, h04, h43⟩
  exact ⟨hreflect, hClosed, h04, h43, hIff⟩

#print axioms fivefoldGK5AYNorthSeam_nontrivial
#print axioms fivefoldGK5AYNorthRawP93ToStructural
#print axioms fivefoldGK5AYNorthRawP93_bad_iff_noP89
#print axioms fivefoldGK5AYNorthP89Old_both
#print axioms fivefoldGK5AYNorthRawObstruction_noninjective
#print axioms fivefoldGK5AYNorthPhysicalSeamGate
#print axioms fivefoldGK5AYNorthPhysicalRawObstructionGate
#print axioms fivefoldGK5AYNorthRawReflects_iff_noObstruction
#print axioms fivefoldGK5AYNorthRawComparison_reflect_or_bad
#print axioms fivefoldGK5AYNorthRawReflects_of_allInjective
#print axioms fivefoldGK5AYNorthPhysicalRawReflection_of_allInjective

end
end KUOS.Architecture.WuxingPentagonUnified