import KUOS.Architecture.QiWuxingGK5APNorthContextUnitMinimalityV4_9
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AQP89P94ReflectionObstruction
import Mathlib.Tactic

/-!
Qi v4.10 — north C60 original-P89→selected-P94A reflection obstruction.

Independent GK5AQ introduces a genuine Type-valued SOURCE bad pair and
proves existence IFF nonfaithfulness of original P89→P94A four-class
transport. This module instantiates that result on the ORIGINAL north
C60 long/short pentagon F54 histories, and proves the honest physical
Dart×Dart decoration can neither repair nor create a kernel pair.

Any genuine north bad pair is invisible to all full original F55
pentagon/square/odd-phase shadow coordinates, and yields equal images
for EVERY north physical gauge frame and fifth-around Dart index
while remaining distinct as original P89 classes. Faithfulness is
therefore independent of the specific physical frame/index. Neither
the missing selected P92B associator-naturality source preimage nor
GK5AO/GK5AP primitive minimality is misrepresented as an actual
noninjectivity witness: this remains an EXACT conditional criterion.

Preserve 04/43 physically reversed categorical edge directions,
true fifth-around C60 Dart pair, full original F55 histories,
GK5AN P89 structural lift and prior Qi v4.9 three-unit minimality.
Independent Kuu -> Qi only; strict 空 authority; public root107.
No old P93/P94A edits, new axioms, sorry/native_decide, Gray
or universal gluing. Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Identical TRUE north pentagon source tree, locally restated
because Qi v4.7 kept its term-private name. No source conversion. -/
private def fivefoldGK5AQNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5AQNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Exact source-indexed physical north C60 obstruction:
there exist two ORIGINAL long/short F54 pentagon three-proofs
separated by P89 but identified after structural phi and P94A. -/
def fivefoldGK5AQNorthReflectionObstruction : Prop :=
  ∃ f g : NativeGK5AINorthPentagonCells,
    nativeGK5AQBadPair
      fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast f g

/-- The north source-only quotient is nonfaithful IFF the exact
genuine GK5AQ source bad pair exists. No such pair is asserted. -/
theorem fivefoldGK5AQNorthSource_noninjective_iff_bad :
    (¬ Function.Injective
      (nativeGK5ANP89ToP94FourClassMap
        fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort)) ↔
      fivefoldGK5AQNorthReflectionObstruction :=
  (nativeGK5AQBadPair_exists_iff_not_injective
    fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast
    northNativeF45PentagonLong northNativeF45PentagonShort).symm

/-- Physical north C60 map: adding the ACTUAL fifth Dart×Dart
component cannot change the precise P89→P94A reflection kernel. -/
theorem fivefoldGK5AQNorthPhysical_noninjective_iff_bad
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
      fivefoldGK5AQNorthReflectionObstruction := by
  constructor
  · intro hnot
    by_contra hno
    apply hnot
    apply (fivefoldGK5ANP94NorthPhysical_injective_iff_reflect frame i).2
    intro f g hp94
    by_contra hnosource
    exact hno ⟨f, g, hp94, hnosource⟩
  · rintro ⟨f, g, hp94, hnosource⟩ hinj
    exact hnosource
      ((fivefoldGK5ANP94NorthPhysical_injective_iff_reflect frame i).1
        hinj f g hp94)

/-- Consequently P89→P94A physical FOUR-class injectivity is
independent of which genuine north physical gauge frame and
fifth-around Dart index were chosen. A physical measurement alone
cannot restore a missing original four-cell witness. -/
theorem fivefoldGK5AQNorthPhysical_injectivity_frame_independent
    (frame₁ frame₂ : NativeC60FivePhaseGauge)
    (i j : FivefoldIndex) :
    Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame₁ i) ↔
    Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame₂ j) := by
  constructor
  · intro h₁
    by_contra h₂
    have hbad := (fivefoldGK5AQNorthPhysical_noninjective_iff_bad
      frame₂ j).1 h₂
    exact ((fivefoldGK5AQNorthPhysical_noninjective_iff_bad
      frame₁ i).2 hbad) h₁
  · intro h₂
    by_contra h₁
    have hbad := (fivefoldGK5AQNorthPhysical_noninjective_iff_bad
      frame₁ i).1 h₁
    exact ((fivefoldGK5AQNorthPhysical_noninjective_iff_bad
      frame₂ j).2 hbad) h₂

/-- Every possible genuinely typed north nonreflection witness
has identical ORIGINAL full signed F55 shadow in the three
pentagon/square/odd-phase coordinates. -/
theorem fivefoldGK5AQNorthBadPair_shadow_eq
    (f g : NativeGK5AINorthPentagonCells)
    (h : nativeGK5AQBadPair
      fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast f g) :
    f.nativeShadow = g.nativeShadow :=
  nativeGK5AQBadPair_shadow_eq
    fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast f g h

/-- Any such conditional bad pair gives *equal physical+P94A images*
for every genuine north frame and index but unequal original P89
source classes. Uses exact quotient equality, not physical shadows. -/
theorem fivefoldGK5AQNorthBadPair_allPhysicalFrames
    (f g : NativeGK5AINorthPentagonCells)
    (h : nativeGK5AQBadPair
      fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast f g)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i
        (nativeF55P89FourClass
          fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast f) =
      fivefoldGK5ANP94NorthPhysicalFourClassMap frame i
        (nativeF55P89FourClass
          fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast g)) ∧
    (nativeF55P89FourClass
        fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast f ≠
      nativeF55P89FourClass
        fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast g) := by
  obtain ⟨htarget, hsource⟩ :=
    (nativeGK5AQBadPair_iff_class_gap
      fivefoldGK5AQNorthFirst fivefoldGK5AQNorthLast f g).1 h
  constructor
  · have hpair := congrArg
      (fun q => (fivefoldGK5AGNorthPhysicalFifthDarts frame i, q))
      htarget
    simpa only [fivefoldGK5ANP94NorthPhysicalFourClassMap_spec] using hpair
  · exact hsource

/-- Physical orientation and the source-exact noninjectivity
criterion coexist. No physical edge is promoted to a P89 filler. -/
theorem fivefoldGK5AQNorthPhysicalReflectionAndOrientation
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
       fivefoldGK5AQNorthReflectionObstruction) ∧
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
       (nativeC60GaugeDart frame .north (i + 4),
        nativeC60GaugeDart frame .north i)) ∧
    Nonempty FivefoldGK5ANP94NorthFullBoundary ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e04) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e04),
       nativeC60GaugeDart frame .north (fivefoldTo .e04))) ∧
    (¬ edgeEndpoints (fivefoldPhysicalEdge frame .north .e43) =
      (nativeC60GaugeDart frame .north (fivefoldFrom .e43),
       nativeC60GaugeDart frame .north (fivefoldTo .e43))) := by
  rcases fivefoldGK5ANP94NorthPhysicalRepairAndOrientation frame i with
    ⟨hclosed, _, hrepair, h04, h43⟩
  exact ⟨fivefoldGK5AQNorthPhysical_noninjective_iff_bad frame i,
    hclosed, hrepair, h04, h43⟩

#print axioms fivefoldGK5AQNorthReflectionObstruction
#print axioms fivefoldGK5AQNorthSource_noninjective_iff_bad
#print axioms fivefoldGK5AQNorthPhysical_noninjective_iff_bad
#print axioms fivefoldGK5AQNorthPhysical_injectivity_frame_independent
#print axioms fivefoldGK5AQNorthBadPair_shadow_eq
#print axioms fivefoldGK5AQNorthBadPair_allPhysicalFrames
#print axioms fivefoldGK5AQNorthPhysicalReflectionAndOrientation

end
end KUOS.Architecture.WuxingPentagonUnified
