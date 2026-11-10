import KUOS.Architecture.QiWuxingGK5CHP77SourceBridgeDescentCriterionV5_86

/-!
Qi v5.87 — a CONSTRUCTED collision in the total space of genuine
old18D typed evidence, arising from the ORIGINAL 17D unit critical
pair. The two actual old17D endpoints are raw distinct but share a
genuine local18D comparison, hence the same ORIGINAL quotient class.
Their distinct strict old18D LOOP proofs share the same independently
observed old18D inner-bracket fingerprint.

Thus even the JOINT observer (genuine 17D quotient class,
old18D inner bracket) cannot decode the total dependent raw proof.
The pair is in DISTINCT ORIGINAL 17D J→J and N→N fibers,
NOT a fabricated same-fiber pair. It cannot satisfy the v5.86
right-bridge hypothesis without separately supplied compatible
typed transport, and neither old5/new7 selected19 comparison
can be formed directly across these differing raw endpoints.

Separate LEFT and RIGHT unit critical pair certificates use the
ORIGINAL v5.35/v5.36 constructions, not a proxy proof type.
No original Type, 17D/18D quotient, mathlib pin, public root107
or protected #1558 altered. No WORLD/20D gluing or action authority.
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

section TotalOriginalOld18DFibers

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}

/-- The TOTAL SPACE of the ORIGINAL dependent old18D proof family,
retaining BOTH genuine 17D endpoints in every element. This
is not a common fixed fiber nor a replacement comparison Type. -/
def SelectedV587TotalOldEighteen
    (H K : SelectedContextualSixteen W l r T U) : Type uSix :=
  Σ J : SelectedContextualSeventeen W l r H K,
    Σ N : SelectedContextualSeventeen W l r H K,
      SelectedLocalEighteen W l r J N

/-- An actual strict old18D proof at J→J, with its two raw endpoint
indices still packaged as dependent Sigma fields. -/
def selectedV587StrictTotal
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    SelectedV587TotalOldEighteen l r H K :=
  ⟨J, J, .strict J⟩

/-- Reading a genuine old18D proof in the total space deliberately
forgets the original endpoints; it is NOT a fiberwise injection. -/
def selectedV587TotalInnerBracket
    (H K : SelectedContextualSixteen W l r T U)
    (M : SelectedV587TotalOldEighteen l r H K) :
    SelectedInheritedOldInnerBracket :=
  selectedLocalEighteenInnerBracket l r M.2.2

/-- An actual, independently named combined observation:
the original local18D quotient class of the source 17D endpoint,
AND the raw old18D proof's independent inner-bracket fingerprint.
Both coordinates are genuine pre-existing proof/observation layers. -/
def selectedV587TotalJoint
    (H K : SelectedContextualSixteen W l r T U)
    (M : SelectedV587TotalOldEighteen l r H K) :
    Quotient (selectedEighteenSetoid l r H K) ×
      SelectedInheritedOldInnerBracket :=
  (selectedEighteenClass l r M.1,
    selectedV587TotalInnerBracket l r H K M)

/-- Every strict old18D loop has the SAME free raw source fingerprint,
regardless of its original 17D endpoint. This is equality of
observations, not equality of typed proof values. -/
theorem selectedV587StrictTotalFingerprint
    {H K : SelectedContextualSixteen W l r T U}
    (J : SelectedContextualSeventeen W l r H K) :
    selectedV587TotalInnerBracket l r H K
      (selectedV587StrictTotal l r J) =
        SelectedInheritedOldInnerBracket.oldStrict := rfl

/-- Strict proof packaging does not lose the raw 17D endpoint itself:
the dependent-total-space embedding is injective. -/
theorem selectedV587StrictTotal_injective
    (H K : SelectedContextualSixteen W l r T U) :
    Function.Injective
      (fun J : SelectedContextualSeventeen W l r H K =>
        selectedV587StrictTotal l r J) := by
  intro J N h
  exact congrArg Sigma.fst h

/-- Exact kernel calculation ON the strict-loop image:
combined quotient class + inner bracket is equal exactly when
the two ORIGINAL 17D quotient classes are equal. Nothing is
claimed for arbitrary original old18D sources. -/
theorem selectedV587StrictJointEq_iff
    (H K : SelectedContextualSixteen W l r T U)
    (J N : SelectedContextualSeventeen W l r H K) :
    selectedV587TotalJoint l r H K (selectedV587StrictTotal l r J) =
        selectedV587TotalJoint l r H K (selectedV587StrictTotal l r N) ↔
      selectedEighteenClass l r J = selectedEighteenClass l r N := by
  change
    (selectedEighteenClass l r J,
        SelectedInheritedOldInnerBracket.oldStrict) =
      (selectedEighteenClass l r N,
        SelectedInheritedOldInnerBracket.oldStrict) ↔
      selectedEighteenClass l r J = selectedEighteenClass l r N
  constructor
  · intro h
    exact congrArg Prod.fst h
  · intro h
    exact congrArg
      (fun q : Quotient (selectedEighteenSetoid l r H K) =>
        (q, SelectedInheritedOldInnerBracket.oldStrict)) h

/-- For strict loops, the JOINT observer's injectivity is precisely
the injectivity of the real v5.36 quotient map on 17D endpoints.
Thus a quotient collapse produces an actual total-space collision,
not a comparison between differently indexed old19D proof types. -/
theorem selectedV587StrictJointInjective_iff
    (H K : SelectedContextualSixteen W l r T U) :
    Function.Injective
      (fun J : SelectedContextualSeventeen W l r H K =>
        selectedV587TotalJoint l r H K (selectedV587StrictTotal l r J)) ↔
    Function.Injective
      (fun J : SelectedContextualSeventeen W l r H K =>
        selectedEighteenClass l r J) := by
  constructor
  · intro hinj J N h
    exact hinj ((selectedV587StrictJointEq_iff l r H K J N).mpr h)
  · intro hinj J N h
    exact hinj ((selectedV587StrictJointEq_iff l r H K J N).mp h)

/-- A raw-different 17D pair with equal genuine quotient classes
constructs two actually distinct TOTAL original old18D Type values
which have equal joint observations. This does NOT return a pair
in any single fixed J→N fiber. -/
theorem selectedV587StrictTotalCollisionOfClass
    (H K : SelectedContextualSixteen W l r T U)
    (J N : SelectedContextualSeventeen W l r H K)
    (hneq : J ≠ N)
    (hclass : selectedEighteenClass l r J =
      selectedEighteenClass l r N) :
    selectedV587StrictTotal l r J ≠ selectedV587StrictTotal l r N ∧
    selectedV587TotalJoint l r H K (selectedV587StrictTotal l r J) =
      selectedV587TotalJoint l r H K
        (selectedV587StrictTotal l r N) := by
  constructor
  · intro h
    exact hneq (congrArg Sigma.fst h)
  · exact (selectedV587StrictJointEq_iff l r H K J N).mpr hclass

/-- Precise upgrade of the quotient noninjectivity certificate:
the genuine total old18D joint observer is also noninjective. The
proof retains the dependent endpoints in Sigma rather than casting
the two strict loops into a falsely common old18D exact fiber. -/
theorem selectedV587TotalJointNoninjectiveOfEndpointQuotient
    (H K : SelectedContextualSixteen W l r T U)
    (hnoninj : ¬ Function.Injective
      (fun J : SelectedContextualSeventeen W l r H K =>
        selectedEighteenClass l r J)) :
    ¬ Function.Injective (selectedV587TotalJoint l r H K) := by
  intro hinj
  apply hnoninj
  intro J N hclass
  have htot := hinj
    ((selectedV587StrictJointEq_iff l r H K J N).mpr hclass)
  exact congrArg Sigma.fst htot

/-- A noninjective total observer has no globally valid left-inverse
recovering ALL ORIGINAL dependent old18D proof values. No claims
about existence or failure of a decoder on a separately fixed
single J→N fiber are made. -/
theorem selectedV587NoTotalJointDecoderOfEndpointQuotient
    (H K : SelectedContextualSixteen W l r T U)
    (hnoninj : ¬ Function.Injective
      (fun J : SelectedContextualSeventeen W l r H K =>
        selectedEighteenClass l r J)) :
    ¬ ∃ decode :
      (Quotient (selectedEighteenSetoid l r H K) ×
        SelectedInheritedOldInnerBracket) →
        SelectedV587TotalOldEighteen l r H K,
      ∀ M, decode (selectedV587TotalJoint l r H K M) = M := by
  rintro ⟨decode, hdecode⟩
  exact (selectedV587TotalJointNoninjectiveOfEndpointQuotient
    l r H K hnoninj) (by
    intro M L h
    calc
      M = decode (selectedV587TotalJoint l r H K M) := (hdecode M).symm
      _ = decode (selectedV587TotalJoint l r H K L) :=
        congrArg decode h
      _ = L := hdecode L)

end TotalOriginalOld18DFibers

section ActualLeftRightUnitCollision

variable (l r : W)
variable {w z : W}
variable {b c d e : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable (C : SelectedContextualThirteen W l r P Q)
variable (after : SevenRewrite W l r d e)

/-- The first ACTUAL strict old18D loop from the original LEFT unit
critical-pair endpoint, WITH the genuine raw endpoints retained. -/
def selectedV587LeftStrictPrepend :
    SelectedV587TotalOldEighteen l r
      (selectedSixteenUnitPrependLeft l r before F G C after)
      (selectedSixteenUnitAppendLeft l r before F G C after) :=
  selectedV587StrictTotal l r
    (selectedSeventeenUnitPrependLeft l r before F G C after)

/-- The other ACTUAL strict old18D loop lives in the DISTINCT raw
17D endpoint fiber, though the original 17D quotient classes agree. -/
def selectedV587LeftStrictAppend :
    SelectedV587TotalOldEighteen l r
      (selectedSixteenUnitPrependLeft l r before F G C after)
      (selectedSixteenUnitAppendLeft l r before F G C after) :=
  selectedV587StrictTotal l r
    (selectedSeventeenUnitAppendLeft l r before F G C after)

/-- An actual LEFT unit generator from v5.35/v5.36 constructs a
joint-observation collision on two DIFFERENT genuine strict-loop
fibers in the original dependent total old18D proof family. -/
theorem selectedV587LeftActualTotalCollision :
    selectedV587LeftStrictPrepend l r before F G C after ≠
        selectedV587LeftStrictAppend l r before F G C after ∧
    selectedV587TotalJoint l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after)
        (selectedV587LeftStrictPrepend l r before F G C after) =
      selectedV587TotalJoint l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after)
        (selectedV587LeftStrictAppend l r before F G C after) := by
  exact selectedV587StrictTotalCollisionOfClass l r
    (selectedSixteenUnitPrependLeft l r before F G C after)
    (selectedSixteenUnitAppendLeft l r before F G C after)
    (selectedSeventeenUnitPrependLeft l r before F G C after)
    (selectedSeventeenUnitAppendLeft l r before F G C after)
    (selectedSeventeenUnitLeft_rawDistinct l r before F G C after)
    (selectedEighteenLeftUnit_classEq l r before F G C after)

/-- The original LEFT unit comparison witnesses the failure of
injectivity of (real 17D quotient class × old18D bracket) on the
total genuine old18D Type, NOT on each individually fixed fiber. -/
theorem selectedV587LeftJointNotInjective :
    ¬ Function.Injective
      (selectedV587TotalJoint l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after)) := by
  intro hinj
  obtain ⟨hne, heq⟩ :=
    selectedV587LeftActualTotalCollision l r before F G C after
  exact hne (hinj heq)

/-- The same LEFT critical-pair certificate disallows any
global decoder from the genuine quotient endpoint + bracket pair. -/
theorem selectedV587LeftNoTotalDecoder :
    ¬ ∃ decode :
      (Quotient (selectedEighteenSetoid l r
          (selectedSixteenUnitPrependLeft l r before F G C after)
          (selectedSixteenUnitAppendLeft l r before F G C after)) ×
        SelectedInheritedOldInnerBracket) →
        SelectedV587TotalOldEighteen l r
          (selectedSixteenUnitPrependLeft l r before F G C after)
          (selectedSixteenUnitAppendLeft l r before F G C after),
      ∀ M, decode (selectedV587TotalJoint l r
        (selectedSixteenUnitPrependLeft l r before F G C after)
        (selectedSixteenUnitAppendLeft l r before F G C after) M) = M := by
  rintro ⟨decode, hdecode⟩
  exact (selectedV587LeftJointNotInjective l r before F G C after) (by
    intro M L h
    calc
      M = decode (selectedV587TotalJoint l r _ _ M) :=
        (hdecode M).symm
      _ = decode (selectedV587TotalJoint l r _ _ L) :=
        congrArg decode h
      _ = L := hdecode L)

/-- The independent RIGHT unit pair also supplies two original
strict old18D loops, with the distinct raw endpoints retained. -/
def selectedV587RightStrictPrepend :
    SelectedV587TotalOldEighteen l r
      (selectedSixteenUnitPrependRight l r before F G C after)
      (selectedSixteenUnitAppendRight l r before F G C after) :=
  selectedV587StrictTotal l r
    (selectedSeventeenUnitPrependRight l r before F G C after)

def selectedV587RightStrictAppend :
    SelectedV587TotalOldEighteen l r
      (selectedSixteenUnitPrependRight l r before F G C after)
      (selectedSixteenUnitAppendRight l r before F G C after) :=
  selectedV587StrictTotal l r
    (selectedSeventeenUnitAppendRight l r before F G C after)

/-- Actual right unit 17D quotient equality plus raw 17D inequality
produces a second independently typed total old18D collision. -/
theorem selectedV587RightActualTotalCollision :
    selectedV587RightStrictPrepend l r before F G C after ≠
        selectedV587RightStrictAppend l r before F G C after ∧
    selectedV587TotalJoint l r
        (selectedSixteenUnitPrependRight l r before F G C after)
        (selectedSixteenUnitAppendRight l r before F G C after)
        (selectedV587RightStrictPrepend l r before F G C after) =
      selectedV587TotalJoint l r
        (selectedSixteenUnitPrependRight l r before F G C after)
        (selectedSixteenUnitAppendRight l r before F G C after)
        (selectedV587RightStrictAppend l r before F G C after) := by
  exact selectedV587StrictTotalCollisionOfClass l r
    (selectedSixteenUnitPrependRight l r before F G C after)
    (selectedSixteenUnitAppendRight l r before F G C after)
    (selectedSeventeenUnitPrependRight l r before F G C after)
    (selectedSeventeenUnitAppendRight l r before F G C after)
    (selectedSeventeenUnitRight_rawDistinct l r before F G C after)
    (selectedEighteenRightUnit_classEq l r before F G C after)

/-- The right original unit obstruction is also a real noninjection
of the total typed old18D joint observation, without false descent
into a single local raw 17D fiber. -/
theorem selectedV587RightJointNotInjective :
    ¬ Function.Injective
      (selectedV587TotalJoint l r
        (selectedSixteenUnitPrependRight l r before F G C after)
        (selectedSixteenUnitAppendRight l r before F G C after)) := by
  intro hinj
  obtain ⟨hne, heq⟩ :=
    selectedV587RightActualTotalCollision l r before F G C after
  exact hne (hinj heq)

theorem selectedV587RightNoTotalDecoder :
    ¬ ∃ decode :
      (Quotient (selectedEighteenSetoid l r
          (selectedSixteenUnitPrependRight l r before F G C after)
          (selectedSixteenUnitAppendRight l r before F G C after)) ×
        SelectedInheritedOldInnerBracket) →
        SelectedV587TotalOldEighteen l r
          (selectedSixteenUnitPrependRight l r before F G C after)
          (selectedSixteenUnitAppendRight l r before F G C after),
      ∀ M, decode (selectedV587TotalJoint l r
        (selectedSixteenUnitPrependRight l r before F G C after)
        (selectedSixteenUnitAppendRight l r before F G C after) M) = M := by
  rintro ⟨decode, hdecode⟩
  exact (selectedV587RightJointNotInjective l r before F G C after) (by
    intro M L h
    calc
      M = decode (selectedV587TotalJoint l r _ _ M) :=
        (hdecode M).symm
      _ = decode (selectedV587TotalJoint l r _ _ L) :=
        congrArg decode h
      _ = L := hdecode L)

end ActualLeftRightUnitCollision

#print axioms PentagonAdjoinedSixCell.SelectedV587TotalOldEighteen
#print axioms PentagonAdjoinedSixCell.selectedV587StrictTotal
#print axioms PentagonAdjoinedSixCell.selectedV587TotalInnerBracket
#print axioms PentagonAdjoinedSixCell.selectedV587TotalJoint
#print axioms PentagonAdjoinedSixCell.selectedV587StrictTotalFingerprint
#print axioms PentagonAdjoinedSixCell.selectedV587StrictTotal_injective
#print axioms PentagonAdjoinedSixCell.selectedV587StrictJointEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV587StrictJointInjective_iff
#print axioms PentagonAdjoinedSixCell.selectedV587StrictTotalCollisionOfClass
#print axioms PentagonAdjoinedSixCell.selectedV587TotalJointNoninjectiveOfEndpointQuotient
#print axioms PentagonAdjoinedSixCell.selectedV587NoTotalJointDecoderOfEndpointQuotient
#print axioms PentagonAdjoinedSixCell.selectedV587LeftStrictPrepend
#print axioms PentagonAdjoinedSixCell.selectedV587LeftStrictAppend
#print axioms PentagonAdjoinedSixCell.selectedV587LeftActualTotalCollision
#print axioms PentagonAdjoinedSixCell.selectedV587LeftJointNotInjective
#print axioms PentagonAdjoinedSixCell.selectedV587LeftNoTotalDecoder
#print axioms PentagonAdjoinedSixCell.selectedV587RightStrictPrepend
#print axioms PentagonAdjoinedSixCell.selectedV587RightStrictAppend
#print axioms PentagonAdjoinedSixCell.selectedV587RightActualTotalCollision
#print axioms PentagonAdjoinedSixCell.selectedV587RightJointNotInjective
#print axioms PentagonAdjoinedSixCell.selectedV587RightNoTotalDecoder

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
