import KUOS.Architecture.QiWuxingGK5CHP77RightGuardedTwoSourceObstructionV5_84

/-!
Qi v5.85 — supplied indexed old18D source families with conditionally
injective inherited-inner-bracket fingerprints, and an independent
conditional obstruction when two genuinely supplied original sources
share a fingerprint but are distinct dependent Type values.

Work ALWAYS in the original right-whiskered N'→N' exact dependent 17D
fiber for GIVEN F/G, after:SevenRewrite, original 17D endpoint N,
and a GIVEN indexed family of original old selected18D Type values.

When the index→inner-bracket fingerprint is actually injective, the
family is faithfully separated by each REAL old5/new7 selected19
quotient, each separately typed original selected19 comparison,
the new quotient's reversal-guarded source classes, and the full
v5.81 new-quotient observation (including the two full Nat towers).
Finite families are a special case; no arbitrary such family is
created. This is a quantified conditional criterion, not a new
global quotient-classification theorem.

Conversely, when TWO GIVEN source proofs have equal observed inner
brackets but are unequal ORIGINAL old18D Type values, the separately
defined whisker-placement observation cannot recover both raw source
proofs. This is strictly an obstruction to raw-observer decoding;
it does NOT assert that their actual old/new quotient classes differ,
agree, or that the full v5.81 observation collides.

No modification of original dependent Type18D, independently typed
old/new Type19D generators, quotient setoids, pinned Lean/mathlib,
public root107, or protected #1558. No heterogeneous WORLD gluing,
20D descent or execution authority.
append-only / tighten-only / overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix uIndex

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

section SuppliedRightSourceFamily

variable (l r : W)
variable {w z : W}
variable {c d e : PentagonAdjoinedSixCell W l r w z}
variable (F G : ContextFrameEleven W l r c d)
variable (after : SevenRewrite W l r d e)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {ι : Type uIndex}

/-- Arbitrarily indexed SOURCE FAMILY, supplied in one genuinely
right-whiskered exact fiber. Injectivity of its fingerprint is a
SEPARATE hypothesis rather than an inferred property. -/
theorem selectedV585RightFamilyOldClassInjective
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i))) :
    Function.Injective
      (fun i : ι => selectedNineteenClass l r
        (SelectedContextualEighteen.inherited (sources i))) := by
  intro i j h
  exact hbr (selectedV584Right_twoSourceOldClassEq_impliesBracketEq
    l r F G after N (sources i) (sources j) h)

/-- The independent new seven-generator quotient has the same
injective image of this specifically certified fingerprint family. -/
theorem selectedV585RightFamilyNewClassInjective
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i))) :
    Function.Injective
      (fun i : ι => selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited (sources i))) := by
  intro i j h
  exact hbr (selectedV584Right_twoSourceNewClassEq_impliesBracketEq
    l r F G after N (sources i) (sources j) h)

/-- One genuine raw reversal guard preserves injectivity on this
family in the ACTUAL new selected19 quotient, not in a proxy Type. -/
theorem selectedV585RightFamilyGuardedNewClassInjective
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i))) :
    Function.Injective
      (fun i : ι => selectedRawCongruentClass l r
        (SelectedContextualEighteen.reverse
          (SelectedContextualEighteen.inherited (sources i)))) := by
  intro i j h
  by_contra hij
  exact (selectedV584Right_twoGuardedSourcesNewDistinct
    l r F G after N (sources i) (sources j)
    (fun heq => hij (hbr heq))) h

/-- Full v5.81 observation including EVERY earlier coordinate and
both untruncated Nat-indexed towers remains injective ON this
reversal-guarded source family, provided the bracket map is injective. -/
theorem selectedV585RightFamilyGuardedFullV581Injective
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i))) :
    Function.Injective
      (fun i : ι =>
        selectedRawCongruentFullV581QuotientObservation l r
          (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
            (SelectedContextualEighteen.reverse
              (SelectedContextualEighteen.inherited (sources i))))) := by
  intro i j h
  have ho := congrArg Prod.snd h
  change SelectedWhiskerPlacementTree.reversed
      (.source (selectedLocalEighteenInnerBracket l r (sources i))) =
    SelectedWhiskerPlacementTree.reversed
      (.source (selectedLocalEighteenInnerBracket l r (sources j))) at ho
  injection ho with hs
  injection hs with hinner
  exact hbr hinner

theorem selectedV585RightFamilyOldClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i)))
    (i j : ι) :
    selectedNineteenClass l r
        (SelectedContextualEighteen.inherited (sources i)) =
      selectedNineteenClass l r
        (SelectedContextualEighteen.inherited (sources j)) ↔ i = j := by
  constructor
  · intro h
    exact (selectedV585RightFamilyOldClassInjective
      l r F G after N sources hbr) h
  · rintro rfl
    rfl

theorem selectedV585RightFamilyNewClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i)))
    (i j : ι) :
    selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited (sources i)) =
      selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited (sources j)) ↔ i = j := by
  constructor
  · intro h
    exact (selectedV585RightFamilyNewClassInjective
      l r F G after N sources hbr) h
  · rintro rfl
    rfl

/-- The original old and separate new Type19D comparisons each exist
exactly when the source-family index is equal. Neither Type is
silently converted to the other. -/
theorem selectedV585RightFamilyOldComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i)))
    (i j : ι) :
    Nonempty (SelectedLocalNineteen W l r
      (SelectedContextualEighteen.inherited (sources i))
      (SelectedContextualEighteen.inherited (sources j))) ↔ i = j := by
  constructor
  · rintro ⟨h⟩
    exact (selectedV585RightFamilyOldClassEq_iff
      l r F G after N sources hbr i j).mp (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (SelectedContextualEighteen.inherited (sources i))⟩

theorem selectedV585RightFamilyNewComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i)))
    (i j : ι) :
    Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)
      (SelectedContextualEighteen.inherited (sources i))
      (SelectedContextualEighteen.inherited (sources j))) ↔ i = j := by
  constructor
  · rintro ⟨h⟩
    exact (selectedV585RightFamilyNewClassEq_iff
      l r F G after N sources hbr i j).mp (Quotient.sound ⟨h⟩)
  · rintro rfl
    exact ⟨.strict (SelectedContextualEighteen.inherited (sources i))⟩

theorem selectedV585RightFamilyOldNewComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (sources : ι → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i)))
    (i j : ι) :
    Nonempty (SelectedLocalNineteen W l r
      (SelectedContextualEighteen.inherited (sources i))
      (SelectedContextualEighteen.inherited (sources j))) ↔
    Nonempty (SelectedRawCongruentNineteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)
      (SelectedContextualEighteen.inherited (sources i))
      (SelectedContextualEighteen.inherited (sources j))) := by
  exact (selectedV585RightFamilyOldComparison_iff
    l r F G after N sources hbr i j).trans
    (selectedV585RightFamilyNewComparison_iff
      l r F G after N sources hbr i j).symm

/-- This finite-family version never constructs a single source:
it works for EACH externally supplied Fin n-indexed family whose
original old18D bracket fingerprint is injective. -/
theorem selectedV585RightFiniteFamilyThreeInjective
    (N : SelectedContextualSeventeen W l r H K)
    (n : Nat)
    (sources : Fin n → SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : Function.Injective
      (fun i : Fin n =>
        selectedLocalEighteenInnerBracket l r (sources i))) :
    Function.Injective
      (fun i : Fin n => selectedNineteenClass l r
        (SelectedContextualEighteen.inherited (sources i))) ∧
    Function.Injective
      (fun i : Fin n => selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited (sources i))) ∧
    Function.Injective
      (fun i : Fin n =>
        selectedRawCongruentFullV581QuotientObservation l r
          (.whiskerRight F G N after) (.whiskerRight F G N after)
          (selectedRawCongruentClass l r
            (SelectedContextualEighteen.reverse
              (SelectedContextualEighteen.inherited (sources i))))) := by
  exact ⟨selectedV585RightFamilyOldClassInjective
      l r F G after N sources hbr,
    selectedV585RightFamilyNewClassInjective
      l r F G after N sources hbr,
    selectedV585RightFamilyGuardedFullV581Injective
      l r F G after N sources hbr⟩

/-- EXACT equality kernel of this one independently descended
placement observation on two GIVEN inherited old18D sources.
This is NOT a quotient equality equivalence. -/
theorem selectedV585RightTwoSourcesPlacementEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    selectedContextEighteenWhiskerPlacement l r
        (SelectedContextualEighteen.inherited M) =
      selectedContextEighteenWhiskerPlacement l r
        (SelectedContextualEighteen.inherited L) ↔
      selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L := by
  constructor
  · intro h
    change SelectedWhiskerPlacementTree.source
        (selectedLocalEighteenInnerBracket l r M) =
      SelectedWhiskerPlacementTree.source
        (selectedLocalEighteenInnerBracket l r L) at h
    injection h
  · intro h
    exact congrArg SelectedWhiskerPlacementTree.source h

/-- One raw reverse guard does not magically add the lost old18D
proof contents to the placement observation. -/
theorem selectedV585RightTwoGuardedSourcesPlacementEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after)) :
    selectedContextEighteenWhiskerPlacement l r
        (SelectedContextualEighteen.reverse (.inherited M)) =
      selectedContextEighteenWhiskerPlacement l r
        (SelectedContextualEighteen.reverse (.inherited L)) ↔
      selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L := by
  constructor
  · intro h
    change SelectedWhiskerPlacementTree.reversed
        (.source (selectedLocalEighteenInnerBracket l r M)) =
      SelectedWhiskerPlacementTree.reversed
        (.source (selectedLocalEighteenInnerBracket l r L)) at h
    injection h with hs
    injection hs
  · intro h
    exact congrArg
      (fun s : SelectedInheritedOldInnerBracket =>
        SelectedWhiskerPlacementTree.reversed (.source s)) h

/-- A pair of actually supplied distinct old18D proof VALUES with
the same fingerprint is a precise CONDITIONAL raw-observer
obstruction; existence of such a pair is NOT asserted. -/
theorem selectedV585RightRawSourceDecoderObstruction
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hneq : M ≠ L) :
    ¬ ∃ decode : SelectedWhiskerPlacementTree →
        SelectedLocalEighteen W l r
          (.whiskerRight F G N after) (.whiskerRight F G N after),
        decode (selectedContextEighteenWhiskerPlacement l r
            (SelectedContextualEighteen.inherited M)) = M ∧
          decode (selectedContextEighteenWhiskerPlacement l r
            (SelectedContextualEighteen.inherited L)) = L := by
  rintro ⟨decode, hM, hL⟩
  apply hneq
  calc
    M = decode (selectedContextEighteenWhiskerPlacement l r
          (SelectedContextualEighteen.inherited M)) := hM.symm
    _ = decode (selectedContextEighteenWhiskerPlacement l r
          (SelectedContextualEighteen.inherited L)) :=
        congrArg decode
          ((selectedV585RightTwoSourcesPlacementEq_iff
            l r F G after N M L).mpr hbr)
    _ = L := hL

/-- The SAME conditional pair excludes one global decoder covering
every old18D source of this fixed fiber. It says nothing about whether
their original OLD/NEW quotient classes agree. -/
theorem selectedV585RightNoUniversalRawSourceDecoder
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after))
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hneq : M ≠ L) :
    ¬ ∃ decode : SelectedWhiskerPlacementTree →
        SelectedLocalEighteen W l r
          (.whiskerRight F G N after) (.whiskerRight F G N after),
        ∀ X : SelectedLocalEighteen W l r
          (.whiskerRight F G N after) (.whiskerRight F G N after),
          decode (selectedContextEighteenWhiskerPlacement l r
            (SelectedContextualEighteen.inherited X)) = X := by
  rintro ⟨decode, hAll⟩
  exact (selectedV585RightRawSourceDecoderObstruction
    l r F G after N M L hbr hneq)
      ⟨decode, hAll M, hAll L⟩

end SuppliedRightSourceFamily

#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyOldClassInjective
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyNewClassInjective
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyGuardedNewClassInjective
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyGuardedFullV581Injective
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyOldClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyNewClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyOldComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyNewComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV585RightFamilyOldNewComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV585RightFiniteFamilyThreeInjective
#print axioms PentagonAdjoinedSixCell.selectedV585RightTwoSourcesPlacementEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV585RightTwoGuardedSourcesPlacementEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV585RightRawSourceDecoderObstruction
#print axioms PentagonAdjoinedSixCell.selectedV585RightNoUniversalRawSourceDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
