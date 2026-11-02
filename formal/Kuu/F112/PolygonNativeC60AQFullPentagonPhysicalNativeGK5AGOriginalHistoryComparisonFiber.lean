import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AFClosedWholePentagonInterchange
import Kuu.F112.PolygonNativeF55P92ExplicitAssocNaturalityPresentation
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

/-!
F112-P94D3GK5AG — original north-C60 F54/F55/P92B history
versus genuinely independent Mathlib whole-NatIso pentagon.

The F54/F55 source here is the independently reconstructed NATIVE
old-F54-shaped Type-valued grammar, not an asserted equivalence to
the frozen historical KUOS F54/F55 implementation.

A source F54 3-step pentagon path and 2-step pentagon path
are different in the original doubly Nat-dependent, two-category
Type-valued grammar. An actual original F55 3-cell witnesses
their comparison, and its explicitly chosen P92B original image
makes the P92B EXISTENCE quotient identify the two histories.

Separately, GK5AF proves equality of the true Mathlib whole
NatIso pentagon paths 01;12;23 and 04;43. We can construct
one heterogeneous TYPED parallel-evidence packet but do NOT
invent any functor from F54 raw paths into categorical NatIso
or identify F55 3-cells with a higher Mathlib filler.

We prove a precise P92B descent criterion and an actual
no-history-retraction theorem. Any later interpretation that
maps the two original source histories to the respective genuine
categorical pentagon paths is nonfaithful. A history-tagged
observation preserves the distinct original F54 sources.

Append-only/tighten-only, canonical main, root107; F54/F55/
P92B raw history retained; independent Kuu authority, no KUOS.
No Gray, sorry, native_decide or new axioms.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC uT

/- The SAME genuinely typed north C60 F45 four-stage endpoints,
not a replacement shape quotient or reconstructed Gray object. -/
private def nativeGK5AGNorthFirst :=
  KuuNativeF45Tree.pentagon0
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

private def nativeGK5AGNorthLast :=
  KuuNativeF45Tree.pentagon3
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

/-- The original Type-valued F54 history at both real two-Nat
endpoints and all four consecutive genuine north-C60 sectors. -/
abbrev NativeGK5AGNorthHistory :=
  KuuNativeF45Tree.DepthRotationRoute (.pentagon .north)
    nativeGK5AGNorthFirst nativeGK5AGNorthLast

/-- The actual chosen P92B proof-existence class is distinct
from the original F54 raw history even though its representative
is a genuine F54 dependent route. -/
def nativeGK5AGNorthP92Class (route : NativeGK5AGNorthHistory) :
    NativeF55P92AssocRouteClasses
      nativeGK5AGNorthFirst nativeGK5AGNorthLast :=
  nativeF55P92AssocRouteClass
    nativeGK5AGNorthFirst nativeGK5AGNorthLast route

/-- The ORIGINAL nine-constructor F55 source supplies a
genuinely Type-valued north-C60 pentagon 3-cell. -/
def nativeGK5AGNorthOriginalCell :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  northNativeF55PentagonCell

/-- The chosen P92B presentation includes the actual original
F55 comparison, without invoking its EXTRA adjoined naturality. -/
def nativeGK5AGNorthP92Cell :
    NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  .original nativeGK5AGNorthOriginalCell

/-- Both TRUE F54 raw histories remain distinct even though
there is a real original F55 higher comparison between them. -/
theorem nativeGK5AGNorthOriginalHistories_distinct :
    (northNativeF45PentagonLong : NativeGK5AGNorthHistory) ≠
      northNativeF45PentagonShort :=
  northNativeF45PentagonLong_ne_short

/-- The P92B existence quotient collapses the two original
pentagon histories, using the EXISTING ORIGINAL F55 3-cell.
This is not an equality of source F54 routes. -/
theorem nativeGK5AGNorthP92Classes_equal :
    nativeGK5AGNorthP92Class northNativeF45PentagonLong =
      nativeGK5AGNorthP92Class northNativeF45PentagonShort := by
  exact nativeF55P92AssocRouteClass_eq_of_cell
    nativeGK5AGNorthFirst nativeGK5AGNorthLast
    nativeGK5AGNorthP92Cell

/-- Precise obstruction to recovering original source HISTORY
from the P92B existence quotient by any left inverse. -/
theorem nativeGK5AGNorthNoP92HistoryRetraction :
    ¬ ∃ recover :
        NativeF55P92AssocRouteClasses
          nativeGK5AGNorthFirst nativeGK5AGNorthLast →
          NativeGK5AGNorthHistory,
        ∀ route : NativeGK5AGNorthHistory,
          recover (nativeGK5AGNorthP92Class route) = route := by
  rintro ⟨recover, hreturn⟩
  have hl :
      recover (nativeGK5AGNorthP92Class northNativeF45PentagonLong) =
        (northNativeF45PentagonLong : NativeGK5AGNorthHistory) :=
    hreturn _
  have hs :
      recover (nativeGK5AGNorthP92Class northNativeF45PentagonShort) =
        (northNativeF45PentagonShort : NativeGK5AGNorthHistory) :=
    hreturn _
  have hmap :
      recover (nativeGK5AGNorthP92Class northNativeF45PentagonLong) =
        recover (nativeGK5AGNorthP92Class northNativeF45PentagonShort) :=
    congrArg recover nativeGK5AGNorthP92Classes_equal
  exact nativeGK5AGNorthOriginalHistories_distinct
    (hl.symm.trans (hmap.trans hs))

/-- EXACT descent criterion to the original P92B existence
quotient, for arbitrary target type T: a readout factors if and
only if it identifies precisely every pair with an ACTUAL
P92B Type-valued comparison witness. No comparison is added. -/
theorem nativeGK5AGNorthFactor_throughP92_iff
    {T : Type uT} (readout : NativeGK5AGNorthHistory → T) :
    (∃ qReadout :
      NativeF55P92AssocRouteClasses
        nativeGK5AGNorthFirst nativeGK5AGNorthLast → T,
      ∀ route : NativeGK5AGNorthHistory,
        qReadout (nativeGK5AGNorthP92Class route) = readout route) ↔
    (∀ r s : NativeGK5AGNorthHistory,
      Nonempty (NativeF55P92AssocComparison (.pentagon .north) r s) →
        readout r = readout s) := by
  constructor
  · rintro ⟨qReadout, hq⟩ r s hcell
    calc
      readout r = qReadout (nativeGK5AGNorthP92Class r) := (hq r).symm
      _ = qReadout (nativeGK5AGNorthP92Class s) := by
        apply congrArg qReadout
        exact (nativeF55P92AssocRouteClass_eq_iff
          nativeGK5AGNorthFirst nativeGK5AGNorthLast r s).2 hcell
      _ = readout s := hq s
  · intro hcompat
    refine ⟨_root_.Quotient.lift readout ?_, ?_⟩
    · intro r s hcell
      exact hcompat r s hcell
    · intro route
      rfl

/-- The actual NUMBER of genuine F54 local rotations is
3 on the long pentagon and 2 on the short pentagon. Because
P92B identifies the two, this numerical original-history
readout CANNOT descend to P92B. -/
theorem nativeGK5AGNorthRotationCount_noP92Descent :
    ¬ ∃ count :
      NativeF55P92AssocRouteClasses
        nativeGK5AGNorthFirst nativeGK5AGNorthLast → Nat,
      ∀ route : NativeGK5AGNorthHistory,
        count (nativeGK5AGNorthP92Class route) =
          route.rotationCount := by
  rintro ⟨count, hcount⟩
  have hsame : northNativeF45PentagonLong.rotationCount =
      northNativeF45PentagonShort.rotationCount := by
    calc
      northNativeF45PentagonLong.rotationCount =
          count (nativeGK5AGNorthP92Class northNativeF45PentagonLong) :=
        (hcount _).symm
      _ = count (nativeGK5AGNorthP92Class northNativeF45PentagonShort) :=
        congrArg count nativeGK5AGNorthP92Classes_equal
      _ = northNativeF45PentagonShort.rotationCount := hcount _
  have h3 := KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage
  have h2 := KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage
  change (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage).rotationCount =
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      northNativeF45FirstStage northNativeF45SecondStage
      northNativeF45ThirdStage northNativeF45FourthStage).rotationCount at hsame
  rw [h3, h2] at hsame
  exact (by decide : (3 : Nat) ≠ 2) hsame

section GenuineWholeNatIso
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ x : I, C x ≌ D x)
variable (e₂ : ∀ x : I, D x ≌ E x)
variable (e₃ : ∀ x : I, E x ≌ F x)
variable (e₄ : ∀ x : I, F x ≌ G x)
variable {i j : I} (R : C i ⥤ C j)

/-- A TYPED multi-presentation evidence packet, NOT a
new map between actual F54 source paths and categorical
whole NatIso: it remembers the original F55 and selected
P92B witnesses and the independent true GK5AF equation. -/
structure NativeGK5AGParallelEvidence where
  originalF55 :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort
  chosenP92 :
    NativeF55P92AssocComparison (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort
  wholePentagon :
    nativeGK5AFLongPath e₁ e₂ e₃ e₄ R =
      nativeGK5AFShortPath e₁ e₂ e₃ e₄ R

/-- Genuine inhabited packet, retaining all THREE typed witnesses
without pretending that they have the same identity type. -/
def nativeGK5AGParallelEvidence :
    NativeGK5AGParallelEvidence e₁ e₂ e₃ e₄ R where
  originalF55 := nativeGK5AGNorthOriginalCell
  chosenP92 := nativeGK5AGNorthP92Cell
  wholePentagon := nativeGK5AFPaths_whole e₁ e₂ e₃ e₄ R

/-- An arbitrary proposed source-to-categorical whole NatIso
interpretation matching the two genuine original 3-vs-2
pentagon paths CANNOT be injective. This is a conditional
property of any map; a canonical physical-to-NatIso
comparison is NOT being postulated. -/
theorem nativeGK5AGMatchingWholeMap_not_injective
    (interpret :
      NativeGK5AGNorthHistory →
        (nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄) R ≅
         nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄) R))
    (hLong : interpret northNativeF45PentagonLong =
      nativeGK5AFLongPath e₁ e₂ e₃ e₄ R)
    (hShort : interpret northNativeF45PentagonShort =
      nativeGK5AFShortPath e₁ e₂ e₃ e₄ R) :
    ¬ Function.Injective interpret := by
  intro hinj
  apply nativeGK5AGNorthOriginalHistories_distinct
  apply hinj
  calc
    interpret northNativeF45PentagonLong =
        nativeGK5AFLongPath e₁ e₂ e₃ e₄ R := hLong
    _ = nativeGK5AFShortPath e₁ e₂ e₃ e₄ R :=
      nativeGK5AFPaths_whole e₁ e₂ e₃ e₄ R
    _ = interpret northNativeF45PentagonShort := hShort.symm

/-- Even a joint observation using the SELECTED original P92B
existence class AND the categorical WHOLE NatIso is not faithful
when both actual source pentagon routes map to the respective
genuine whole path values. -/
theorem nativeGK5AGJointP92Whole_not_injective
    (interpret :
      NativeGK5AGNorthHistory →
        (nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄) R ≅
         nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄) R))
    (hLong : interpret northNativeF45PentagonLong =
      nativeGK5AFLongPath e₁ e₂ e₃ e₄ R)
    (hShort : interpret northNativeF45PentagonShort =
      nativeGK5AFShortPath e₁ e₂ e₃ e₄ R) :
    ¬ Function.Injective
      (fun route : NativeGK5AGNorthHistory =>
        (nativeGK5AGNorthP92Class route, interpret route)) := by
  intro hinj
  apply nativeGK5AGNorthOriginalHistories_distinct
  apply hinj
  apply Prod.ext
  · exact nativeGK5AGNorthP92Classes_equal
  · calc
      interpret northNativeF45PentagonLong =
          nativeGK5AFLongPath e₁ e₂ e₃ e₄ R := hLong
      _ = nativeGK5AFShortPath e₁ e₂ e₃ e₄ R :=
        nativeGK5AFPaths_whole e₁ e₂ e₃ e₄ R
      _ = interpret northNativeF45PentagonShort := hShort.symm

/-- The minimal original-history tagged interpretation is
injective, with no false demand for a section of P92B.
Faithfulness comes from retaining the entire Type-valued
original F54 proof rather than from the categorical image. -/
theorem nativeGK5AGHistoryTagged_injective
    (interpret :
      NativeGK5AGNorthHistory →
        (nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄) R ≅
         nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄) R)) :
    Function.Injective (fun route : NativeGK5AGNorthHistory =>
      (route, nativeGK5AGNorthP92Class route, interpret route)) := by
  intro r s h
  exact congrArg Prod.fst h

#print axioms nativeGK5AGParallelEvidence
#print axioms nativeGK5AGMatchingWholeMap_not_injective
#print axioms nativeGK5AGJointP92Whole_not_injective
#print axioms nativeGK5AGHistoryTagged_injective

end GenuineWholeNatIso

#print axioms nativeGK5AGNorthOriginalHistories_distinct
#print axioms nativeGK5AGNorthP92Classes_equal
#print axioms nativeGK5AGNorthNoP92HistoryRetraction
#print axioms nativeGK5AGNorthFactor_throughP92_iff
#print axioms nativeGK5AGNorthRotationCount_noP92Descent

end
end Kuu.F112.Physical
