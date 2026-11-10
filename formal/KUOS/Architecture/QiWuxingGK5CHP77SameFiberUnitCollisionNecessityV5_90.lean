import KUOS.Architecture.QiWuxingGK5CHP77OriginalUnitFreeExhaustionV5_89

/-!
Qi v5.90 — genuine ORIGINAL old18D exact-fiber fingerprint collision
NECESSARILY contains original unit generators on BOTH sides.

Input: v5.89 has proved that all zero-unit original dependent
old18D N→N witnesses, not merely selected examples, are exhausted
by the v5.88 faithful unit-free embedding. Therefore, if two
genuine raw old18D N→N proof values are distinct but the actual
v5.73 source-inner-bracket observation agrees, both values must
have positive ORIGINAL (not auxiliary-grammar) unit counts.

We independently transfer this NECESSARY condition to equality
of the original five-generator selected19 quotient classes and
equality of the separate seven-generator raw-congruent quotient
classes, and to existence of their differently typed 19D
comparisons. The original quotient class equality is reduced to
an original source-bracket equality using the independently
proved v5.73 inherited-inner-list descent, not an asserted
global old19/new19 equivalence.

A positive unit count is only a NECESSARY CONDITION. Nothing here
constructs an actual same-fiber collision or asserts sufficiency.
v5.87's distinct-fiber total-space collision remains distinct.

All dependent old17D/old18D/old19D sources unchanged; no
heterogeneous transport, WORLD/20D descent, or action authority.
append-only / tighten-only / overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

section OriginalExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- This count equality is valid for any pair of ACTUAL original
old18D proof values sharing exactly the SAME dependent endpoints.
It is an observation consequence, not a raw proof equality. -/
theorem selectedV590BracketEq_originalCountEq
    (M L : SelectedLocalEighteen W l r J N)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L) :
    selectedV589OriginalUnitCount l r M =
      selectedV589OriginalUnitCount l r L := by
  calc
    selectedV589OriginalUnitCount l r M =
        selectedV588InnerUnitCount
          (selectedLocalEighteenInnerBracket l r M) :=
      selectedV589OriginalUnitCount_observed l r M
    _ = selectedV588InnerUnitCount
          (selectedLocalEighteenInnerBracket l r L) :=
      congrArg selectedV588InnerUnitCount hbr
    _ = selectedV589OriginalUnitCount l r L :=
      (selectedV589OriginalUnitCount_observed l r L).symm

/-- If the ACTUAL zero-unit predicate holds for the LEFT old18D
source in one N→N fiber, equal fingerprints force RAW equality.
The right side is not assumed unit-free: that is derived. -/
theorem selectedV590BracketEq_leftFreeReflect
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hfree : selectedV589OriginalIsUnitFree l r M) :
    M = L := by
  have hc := selectedV590BracketEq_originalCountEq l r M L hbr
  have hfreeL : selectedV589OriginalIsUnitFree l r L := by
    change selectedV589OriginalUnitCount l r L = 0
    exact hc.symm.trans hfree
  exact (selectedV589OriginalLoopBracketFaithful l r N M L
    hfree hfreeL).mp hbr

/-- If EITHER genuine original proof is unit-free, equality of
inner bracket observations implies equality of original proofs. -/
theorem selectedV590BracketEq_eitherFreeReflect
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hfree : selectedV589OriginalIsUnitFree l r M ∨
      selectedV589OriginalIsUnitFree l r L) :
    M = L := by
  rcases hfree with hM | hL
  · exact selectedV590BracketEq_leftFreeReflect l r N M L hbr hM
  · exact (selectedV590BracketEq_leftFreeReflect l r N L M
      hbr.symm hL).symm

/-- An actual equal-bracket/different-raw collision, IF one exists
in a SAME original N→N fiber, must contain one or more old18D unit
generators in EACH of its two original dependent proof values. -/
theorem selectedV590BracketCollision_requiresPositiveUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hne : M ≠ L) :
    0 < selectedV589OriginalUnitCount l r M ∧
      0 < selectedV589OriginalUnitCount l r L := by
  have hc := selectedV590BracketEq_originalCountEq l r M L hbr
  have hp : 0 < selectedV589OriginalUnitCount l r M := by
    by_contra hnot
    have hz : selectedV589OriginalUnitCount l r M = 0 := by
      omega
    exact hne (selectedV590BracketEq_leftFreeReflect l r N M L
      hbr hz)
  constructor
  · exact hp
  · omega

/-- Genuine OLD five-generator selected19 quotient equality in
the same original raw17D N→N fiber implies equality of original
old18D source-inner bracket observations. -/
theorem selectedV590OldClassEq_impliesBracketEq
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedNineteenClass l r (.inherited M) =
        selectedNineteenClass l r (.inherited L)) :
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L := by
  have ho := congrArg
    (selectedNineteenInheritedInnerListOnQuotient l r N N) hclass
  change [selectedLocalEighteenInnerBracket l r M] =
    [selectedLocalEighteenInnerBracket l r L] at ho
  injection ho with hbr
  exact hbr

/-- Genuine independent NEW seven-generator selected19 quotient
also faithfully preserves the original inherited source bracket;
we do NOT identify the old and new quotient Types. -/
theorem selectedV590NewClassEq_impliesBracketEq
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedRawCongruentClass l r (.inherited M) =
        selectedRawCongruentClass l r (.inherited L)) :
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L := by
  have ho := congrArg
    (selectedRawCongruentInheritedInnerListOnQuotient l r N N) hclass
  change [selectedLocalEighteenInnerBracket l r M] =
    [selectedLocalEighteenInnerBracket l r L] at ho
  injection ho with hbr
  exact hbr

/-- Even ONE genuine unit-free source is sufficient for original
old5 quotient equality to reflect actual raw old18D proof equality.
The other source is proved unit-free by the quotient's invariant. -/
theorem selectedV590OldClassEq_leftFreeReflect
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedNineteenClass l r (.inherited M) =
        selectedNineteenClass l r (.inherited L))
    (hfree : selectedV589OriginalIsUnitFree l r M) :
    M = L := by
  exact selectedV590BracketEq_leftFreeReflect l r N M L
    (selectedV590OldClassEq_impliesBracketEq l r N M L hclass)
    hfree

/-- The same one-sided zero-unit criterion holds INDEPENDENTLY for
the NEW seven-generator quotient and original 18D raw witnesses. -/
theorem selectedV590NewClassEq_leftFreeReflect
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedRawCongruentClass l r (.inherited M) =
        selectedRawCongruentClass l r (.inherited L))
    (hfree : selectedV589OriginalIsUnitFree l r M) :
    M = L := by
  exact selectedV590BracketEq_leftFreeReflect l r N M L
    (selectedV590NewClassEq_impliesBracketEq l r N M L hclass)
    hfree

/-- A hypothetical old5 quotient collapse of genuinely distinct
old18D same-fiber raw proofs requires positive unit count on BOTH
sides. This does not construct such a collapse. -/
theorem selectedV590OldClassCollision_requiresPositiveUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedNineteenClass l r (.inherited M) =
        selectedNineteenClass l r (.inherited L))
    (hne : M ≠ L) :
    0 < selectedV589OriginalUnitCount l r M ∧
      0 < selectedV589OriginalUnitCount l r L := by
  exact selectedV590BracketCollision_requiresPositiveUnits l r
    N M L
    (selectedV590OldClassEq_impliesBracketEq l r N M L hclass) hne

/-- Independent genuinely NEW seven-generator quotient collision
also needs original unit constructors in BOTH source proof values. -/
theorem selectedV590NewClassCollision_requiresPositiveUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hclass :
      selectedRawCongruentClass l r (.inherited M) =
        selectedRawCongruentClass l r (.inherited L))
    (hne : M ≠ L) :
    0 < selectedV589OriginalUnitCount l r M ∧
      0 < selectedV589OriginalUnitCount l r L := by
  exact selectedV590BracketCollision_requiresPositiveUnits l r
    N M L
    (selectedV590NewClassEq_impliesBracketEq l r N M L hclass) hne

/-- Genuinely typed ORIGINAL old selected19 evidence comparing
different inherited sources would also force unit atoms on both
sides. No virtual comparison or heterogeneous transport is added. -/
theorem selectedV590OldTypedCollision_requiresPositiveUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hcomp : Nonempty (SelectedLocalNineteen W l r
      (.inherited M) (.inherited L)))
    (hne : M ≠ L) :
    0 < selectedV589OriginalUnitCount l r M ∧
      0 < selectedV589OriginalUnitCount l r L := by
  obtain ⟨a⟩ := hcomp
  exact selectedV590OldClassCollision_requiresPositiveUnits l r
    N M L (Quotient.sound ⟨a⟩) hne

/-- The genuinely separate NEW seven-generator typed selected19
comparison has the same conditional obstruction, independently. -/
theorem selectedV590NewTypedCollision_requiresPositiveUnits
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hcomp : Nonempty (SelectedRawCongruentNineteen W l r N N
      (.inherited M) (.inherited L)))
    (hne : M ≠ L) :
    0 < selectedV589OriginalUnitCount l r M ∧
      0 < selectedV589OriginalUnitCount l r L := by
  obtain ⟨a⟩ := hcomp
  exact selectedV590NewClassCollision_requiresPositiveUnits l r
    N M L (Quotient.sound ⟨a⟩) hne

end OriginalExactFiber

#print axioms PentagonAdjoinedSixCell.selectedV590BracketEq_originalCountEq
#print axioms PentagonAdjoinedSixCell.selectedV590BracketEq_leftFreeReflect
#print axioms PentagonAdjoinedSixCell.selectedV590BracketEq_eitherFreeReflect
#print axioms PentagonAdjoinedSixCell.selectedV590BracketCollision_requiresPositiveUnits
#print axioms PentagonAdjoinedSixCell.selectedV590OldClassEq_impliesBracketEq
#print axioms PentagonAdjoinedSixCell.selectedV590NewClassEq_impliesBracketEq
#print axioms PentagonAdjoinedSixCell.selectedV590OldClassEq_leftFreeReflect
#print axioms PentagonAdjoinedSixCell.selectedV590NewClassEq_leftFreeReflect
#print axioms PentagonAdjoinedSixCell.selectedV590OldClassCollision_requiresPositiveUnits
#print axioms PentagonAdjoinedSixCell.selectedV590NewClassCollision_requiresPositiveUnits
#print axioms PentagonAdjoinedSixCell.selectedV590OldTypedCollision_requiresPositiveUnits
#print axioms PentagonAdjoinedSixCell.selectedV590NewTypedCollision_requiresPositiveUnits

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
