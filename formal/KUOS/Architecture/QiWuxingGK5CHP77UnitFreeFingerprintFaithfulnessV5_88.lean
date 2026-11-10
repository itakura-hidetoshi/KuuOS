import KUOS.Architecture.QiWuxingGK5CHP77EndpointQuotientFingerprintObstructionV5_87

/-!
Qi v5.88 — exact original old18D same-fiber faithfulness on the
explicit UNIT-FREE strict/reverse/nonassociative chain fragment.

The source grammar below is an independent syntax used to SELECT a
restricted family of ACTUAL ORIGINAL dependent SelectedLocalEighteen
N→N proof values. The embedding is into the unchanged original Type,
not a proxy for the ORIGINAL comparison or quotient.

The genuine v5.73 source-inner-bracket observation has a parser
which is a left inverse on this fragment. Hence it distinguishes
source syntax and the actual embedded old18D raw proof values.
Moreover, on the genuine inherited old18D image, the separate
original FIVE-generator old19 quotient and SEVEN-generator new19
quotient, and their separately typed comparisons, faithfully reflect
the unit-free syntax. A raw reversal guard retains new-quotient
separation. This is CONDITIONAL ON MEMBERSHIP IN THIS FRAGMENT,
not a global old18D raw source classifier.

Original old18D unitLeft/unitRight proofs are ACTUAL typed values,
but their old inner-bracket observations have unit atoms which are
NOT in the image of this unit-free grammar. The free parser cannot
decode those actual old witnesses. This does NOT prove that two
different original old18D values with the same bracket exist in the
same raw exact fiber; that question remains NO_DATA.

All original 17D/18D/19D Types, exact-fiber indices, comparison
generators, Lean/mathlib pins, public root107 and protected #1558
are unmodified. No forced gluing or action authority.
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

/-- Explicit unit-free raw source grammar, retaining nonassociative
binary chain brackets. This is a fragment, not the old18D Type. -/
inductive SelectedV588UnitFreeTerm : Type where
  | strict : SelectedV588UnitFreeTerm
  | reversed : SelectedV588UnitFreeTerm → SelectedV588UnitFreeTerm
  | joined : SelectedV588UnitFreeTerm → SelectedV588UnitFreeTerm →
      SelectedV588UnitFreeTerm
  deriving DecidableEq, Repr

/-- Reading the free term using the ALREADY EXISTING v5.73
source-inner-bracket observation codomain, without quotienting. -/
def selectedV588UnitFreeBracket : SelectedV588UnitFreeTerm →
    SelectedInheritedOldInnerBracket
  | .strict => .oldStrict
  | .reversed t => .oldReversed (selectedV588UnitFreeBracket t)
  | .joined t u => .oldJoined
      (selectedV588UnitFreeBracket t) (selectedV588UnitFreeBracket u)

/-- A partial parser for unit-free source trees; both ORIGINAL
unit witness tags intentionally have no image in this grammar. -/
def selectedV588UnitFreeParse : SelectedInheritedOldInnerBracket →
    Option SelectedV588UnitFreeTerm
  | .oldStrict => some .strict
  | .oldUnitLeft => none
  | .oldUnitRight => none
  | .oldReversed t =>
      (selectedV588UnitFreeParse t).map
        (fun x => SelectedV588UnitFreeTerm.reversed x)
  | .oldJoined t u =>
      (selectedV588UnitFreeParse t).bind (fun x =>
        (selectedV588UnitFreeParse u).map
          (fun y => SelectedV588UnitFreeTerm.joined x y))

/-- The parser is an actual LEFT INVERSE on every unit-free tree;
no classical choice, quotient identification or global raw equality. -/
theorem selectedV588UnitFreeParse_onBracket
    (t : SelectedV588UnitFreeTerm) :
    selectedV588UnitFreeParse (selectedV588UnitFreeBracket t) =
      some t := by
  induction t with
  | strict => rfl
  | reversed t ih =>
      simp [selectedV588UnitFreeBracket,
        selectedV588UnitFreeParse, ih]
  | joined t u ihT ihU =>
      simp [selectedV588UnitFreeBracket,
        selectedV588UnitFreeParse, ihT, ihU]

/-- This unit-free syntax is faithfully read by the genuine old
source bracket syntax, including every nonassociative parenthesis. -/
theorem selectedV588UnitFreeBracket_injective :
    Function.Injective selectedV588UnitFreeBracket := by
  intro t u h
  have hp := congrArg selectedV588UnitFreeParse h
  rw [selectedV588UnitFreeParse_onBracket t,
    selectedV588UnitFreeParse_onBracket u] at hp
  exact Option.some.inj hp

/-- Independent literal count of original left/right old18D unit
atoms in the v5.73 free observation tree. -/
def selectedV588InnerUnitCount : SelectedInheritedOldInnerBracket → Nat
  | .oldStrict => 0
  | .oldUnitLeft => 1
  | .oldUnitRight => 1
  | .oldReversed t => selectedV588InnerUnitCount t
  | .oldJoined t u =>
      selectedV588InnerUnitCount t + selectedV588InnerUnitCount u

/-- The selected free fragment contains no original 18D unit atom,
at ANY reverse depth or binary chain branch. -/
theorem selectedV588UnitFree_hasZeroUnits
    (t : SelectedV588UnitFreeTerm) :
    selectedV588InnerUnitCount (selectedV588UnitFreeBracket t) = 0 := by
  induction t with
  | strict => rfl
  | reversed t ih =>
      simpa [selectedV588UnitFreeBracket, selectedV588InnerUnitCount] using ih
  | joined t u ihT ihU =>
      simp [selectedV588UnitFreeBracket, selectedV588InnerUnitCount,
        ihT, ihU]

/-- A source observation containing any actual unit atom cannot
belong to the unit-free fingerprint image. This is an image
obstruction, NOT an assertion that equal fingerprints collide. -/
theorem selectedV588NoFreeImage_ofUnitCountPositive
    (s : SelectedInheritedOldInnerBracket)
    (hpos : 0 < selectedV588InnerUnitCount s) :
    ¬ ∃ t : SelectedV588UnitFreeTerm,
      selectedV588UnitFreeBracket t = s := by
  rintro ⟨t, h⟩
  have hz := selectedV588UnitFree_hasZeroUnits t
  rw [h] at hz
  have hzero : selectedV588InnerUnitCount s = 0 := hz
  omega

theorem selectedV588NoFreeLeftUnitImage :
    ¬ ∃ t : SelectedV588UnitFreeTerm,
      selectedV588UnitFreeBracket t =
        SelectedInheritedOldInnerBracket.oldUnitLeft := by
  exact selectedV588NoFreeImage_ofUnitCountPositive
    .oldUnitLeft (by decide)

theorem selectedV588NoFreeRightUnitImage :
    ¬ ∃ t : SelectedV588UnitFreeTerm,
      selectedV588UnitFreeBracket t =
        SelectedInheritedOldInnerBracket.oldUnitRight := by
  exact selectedV588NoFreeImage_ofUnitCountPositive
    .oldUnitRight (by decide)

section ExactOriginalUnitFreeFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Unit-free syntax embedded into the ORIGINAL raw dependent
old18D proof Type in one genuinely fixed exact N→N fiber. -/
def selectedV588UnitFreeRawEmbed
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedV588UnitFreeTerm → SelectedLocalEighteen W l r N N
  | .strict => .strict N
  | .reversed t =>
      .reverse (selectedV588UnitFreeRawEmbed N t)
  | .joined t u =>
      .chain (selectedV588UnitFreeRawEmbed N t)
        (selectedV588UnitFreeRawEmbed N u)

/-- The ACTUAL original old18D proof's v5.73 inner-bracket
observation agrees definitionally with this independent free tree
reader, for every term of the certified restricted fragment. -/
theorem selectedV588UnitFreeRaw_observed
    (N : SelectedContextualSeventeen W l r H K)
    (t : SelectedV588UnitFreeTerm) :
    selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N t) =
      selectedV588UnitFreeBracket t := by
  induction t with
  | strict => rfl
  | reversed t ih =>
      change SelectedInheritedOldInnerBracket.oldReversed
          (selectedLocalEighteenInnerBracket l r
            (selectedV588UnitFreeRawEmbed l r N t)) =
        SelectedInheritedOldInnerBracket.oldReversed
          (selectedV588UnitFreeBracket t)
      exact congrArg SelectedInheritedOldInnerBracket.oldReversed ih
  | joined t u ihT ihU =>
      change SelectedInheritedOldInnerBracket.oldJoined
          (selectedLocalEighteenInnerBracket l r
            (selectedV588UnitFreeRawEmbed l r N t))
          (selectedLocalEighteenInnerBracket l r
            (selectedV588UnitFreeRawEmbed l r N u)) =
        SelectedInheritedOldInnerBracket.oldJoined
          (selectedV588UnitFreeBracket t)
          (selectedV588UnitFreeBracket u)
      exact congrArg₂ SelectedInheritedOldInnerBracket.oldJoined ihT ihU

/-- Source fingerprint parsing actually retrieves the supplied
fragment term from the ORIGINAL dependent old18D raw Type value. -/
theorem selectedV588UnitFreeRaw_parse
    (N : SelectedContextualSeventeen W l r H K)
    (t : SelectedV588UnitFreeTerm) :
    selectedV588UnitFreeParse
      (selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N t)) = some t := by
  rw [selectedV588UnitFreeRaw_observed l r N t]
  exact selectedV588UnitFreeParse_onBracket t

/-- Actual raw old18D Type-value equality is reflected by the
bracket fingerprint ON the unit-free embedded original fiber. -/
theorem selectedV588UnitFreeRawEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm) :
    selectedV588UnitFreeRawEmbed l r N t =
        selectedV588UnitFreeRawEmbed l r N u ↔
      selectedV588UnitFreeBracket t =
        selectedV588UnitFreeBracket u := by
  constructor
  · intro h
    have ho := congrArg (selectedLocalEighteenInnerBracket l r) h
    rwa [selectedV588UnitFreeRaw_observed l r N t,
      selectedV588UnitFreeRaw_observed l r N u] at ho
  · intro h
    exact congrArg (selectedV588UnitFreeRawEmbed l r N)
      (selectedV588UnitFreeBracket_injective h)

/-- The genuine source map is injective in this SAME raw fiber.
Do NOT promote this result to arbitrary original unit-containing
old18D source values or differently indexed fibers. -/
theorem selectedV588UnitFreeRawEmbed_injective
    (N : SelectedContextualSeventeen W l r H K) :
    Function.Injective (selectedV588UnitFreeRawEmbed l r N) := by
  intro t u h
  exact selectedV588UnitFreeBracket_injective
    ((selectedV588UnitFreeRawEq_iff l r N t u).mp h)

/-- Each independently typed ORIGINAL five-generator selected19
quotient class faithfully separates unit-free source terms on this
same raw17D N→N fiber, not across unrelated fibers. -/
theorem selectedV588UnitFreeOldClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm) :
    selectedNineteenClass l r
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N t)) =
      selectedNineteenClass l r
        (SelectedContextualEighteen.inherited
          (selectedV588UnitFreeRawEmbed l r N u)) ↔ t = u := by
  constructor
  · intro h
    have ho := congrArg
      (selectedNineteenInheritedInnerListOnQuotient l r N N) h
    change [selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N t)] =
      [selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N u)] at ho
    rw [selectedV588UnitFreeRaw_observed l r N t,
      selectedV588UnitFreeRaw_observed l r N u] at ho
    injection ho with heq
    exact selectedV588UnitFreeBracket_injective heq
  · rintro rfl
    rfl

/-- The INDEPENDENT seven-generator new selected19 quotient also
reflects equality on this particular genuine original inherited
source fragment; old and new Type19 are NOT globally identified. -/
theorem selectedV588UnitFreeNewClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm) :
    selectedRawCongruentClass l r
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N t)) =
      selectedRawCongruentClass l r
        (SelectedContextualEighteen.inherited
          (selectedV588UnitFreeRawEmbed l r N u)) ↔ t = u := by
  constructor
  · intro h
    have ho := congrArg
      (selectedRawCongruentInheritedInnerListOnQuotient l r N N) h
    change [selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N t)] =
      [selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N u)] at ho
    rw [selectedV588UnitFreeRaw_observed l r N t,
      selectedV588UnitFreeRaw_observed l r N u] at ho
    injection ho with heq
    exact selectedV588UnitFreeBracket_injective heq
  · rintro rfl
    rfl

/-- Reversal of ACTUAL raw contextual18D inherited old18D values
retains the ordered source bracket observation. No false groupoid
inverse law or new original comparison is assumed. -/
theorem selectedV588UnitFreeGuardedNewClassEq_iff
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm) :
    selectedRawCongruentClass l r
      (SelectedContextualEighteen.reverse (.inherited
        (selectedV588UnitFreeRawEmbed l r N t))) =
      selectedRawCongruentClass l r
        (SelectedContextualEighteen.reverse (.inherited
          (selectedV588UnitFreeRawEmbed l r N u))) ↔ t = u := by
  constructor
  · intro h
    have ho := congrArg
      (selectedRawCongruentInheritedInnerListOnQuotient l r N N) h
    change [selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N t)] =
      [selectedLocalEighteenInnerBracket l r
        (selectedV588UnitFreeRawEmbed l r N u)] at ho
    rw [selectedV588UnitFreeRaw_observed l r N t,
      selectedV588UnitFreeRaw_observed l r N u] at ho
    injection ho with heq
    exact selectedV588UnitFreeBracket_injective heq
  · rintro rfl
    rfl

/-- Existing ORIGINAL five-generator selected19 Type comparisons
are inhabited on this particular free image iff its source syntax
values are the same. This is not a declaration of an arbitrary
new19→old19 Type equivalence. -/
theorem selectedV588UnitFreeOldComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm) :
    Nonempty (SelectedLocalNineteen W l r
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N t))
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N u))) ↔ t = u := by
  constructor
  · rintro ⟨a⟩
    exact (selectedV588UnitFreeOldClassEq_iff l r N t u).mp
      (Quotient.sound ⟨a⟩)
  · rintro rfl
    exact ⟨.strict _⟩

/-- The genuinely separate seven-generator selected19 Type has
the same restricted inhabitation criterion, proved independently. -/
theorem selectedV588UnitFreeNewComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm) :
    Nonempty (SelectedRawCongruentNineteen W l r N N
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N t))
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N u))) ↔ t = u := by
  constructor
  · rintro ⟨a⟩
    exact (selectedV588UnitFreeNewClassEq_iff l r N t u).mp
      (Quotient.sound ⟨a⟩)
  · rintro rfl
    exact ⟨.strict _⟩

/-- The old-five and new-seven typed comparisons are equivalent
ONLY on this explicitly injected same-fiber fragment image. -/
theorem selectedV588UnitFreeOldNewComparison_iff
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm) :
    Nonempty (SelectedLocalNineteen W l r
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N t))
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N u))) ↔
    Nonempty (SelectedRawCongruentNineteen W l r N N
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N t))
      (SelectedContextualEighteen.inherited
        (selectedV588UnitFreeRawEmbed l r N u))) := by
  exact (selectedV588UnitFreeOldComparison_iff l r N t u).trans
    (selectedV588UnitFreeNewComparison_iff l r N t u).symm

/-- Unlike the total-space collision in v5.87, two DIFFERENT
unit-free syntax values CANNOT have the same actual old18D
fingerprint, or either of the genuine selected19 quotient classes
for their embedded original same-fiber proofs. -/
theorem selectedV588UnitFreeDistinctSeparated
    (N : SelectedContextualSeventeen W l r H K)
    (t u : SelectedV588UnitFreeTerm)
    (hne : t ≠ u) :
    selectedV588UnitFreeBracket t ≠ selectedV588UnitFreeBracket u ∧
    selectedNineteenClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N t)) ≠
      selectedNineteenClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N u)) ∧
    selectedRawCongruentClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N t)) ≠
      selectedRawCongruentClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N u)) := by
  constructor
  · intro h
    exact hne (selectedV588UnitFreeBracket_injective h)
  constructor
  · intro h
    exact hne ((selectedV588UnitFreeOldClassEq_iff l r N t u).mp h)
  · intro h
    exact hne ((selectedV588UnitFreeNewClassEq_iff l r N t u).mp h)

/-- An explicit ACTUAL same-fiber source pair: the strict old18D
loop and its double raw reverse are distinct, and the old/new
selected19 quotients do not collapse them. No reverse-inverse
equation was inserted into either original selected19 Type. -/
theorem selectedV588UnitFreeStrictVsDoubleReverse
    (N : SelectedContextualSeventeen W l r H K) :
    selectedV588UnitFreeRawEmbed l r N .strict ≠
      selectedV588UnitFreeRawEmbed l r N
        (.reversed (.reversed .strict)) ∧
    selectedNineteenClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N .strict)) ≠
      selectedNineteenClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N
          (.reversed (.reversed .strict)))) ∧
    selectedRawCongruentClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N .strict)) ≠
      selectedRawCongruentClass l r (.inherited
        (selectedV588UnitFreeRawEmbed l r N
          (.reversed (.reversed .strict)))) := by
  have hne : (SelectedV588UnitFreeTerm.strict) ≠
      .reversed (.reversed .strict) := by decide
  obtain ⟨_, hOld, hNew⟩ :=
    selectedV588UnitFreeDistinctSeparated l r N
      .strict (.reversed (.reversed .strict)) hne
  refine ⟨?_, hOld, hNew⟩
  intro h
  exact hne (selectedV588UnitFreeRawEmbed_injective l r N h)

end ExactOriginalUnitFreeFiber

section GenuineOriginalUnitWitnessBoundary

variable (l r : W)
variable {w z : W}
variable {b c d e : PentagonAdjoinedSixCell W l r w z}
variable (before : SevenRewrite W l r b c)
variable (F G : ContextFrameEleven W l r c d)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable (C : SelectedContextualThirteen W l r P Q)
variable (after : SevenRewrite W l r d e)

/-- The genuine ORIGINAL old18D left unit comparison proof has an
independent oldUnitLeft observation atom; it is not in the pure
strict/reverse/chain tree fragment at ANY depth. -/
theorem selectedV588ActualLeftUnitNoFreeBracket :
    ¬ ∃ t : SelectedV588UnitFreeTerm,
        selectedV588UnitFreeBracket t =
          selectedLocalEighteenInnerBracket l r
            (SelectedLocalEighteen.unitLeft before F G C after) := by
  exact selectedV588NoFreeLeftUnitImage

/-- Distinct old18D unitRight generator, retaining actual old
dependent endpoints and data; never cast to an unrelated raw fiber. -/
theorem selectedV588ActualRightUnitNoFreeBracket :
    ¬ ∃ t : SelectedV588UnitFreeTerm,
        selectedV588UnitFreeBracket t =
          selectedLocalEighteenInnerBracket l r
            (SelectedLocalEighteen.unitRight before F G C after) := by
  exact selectedV588NoFreeRightUnitImage

/-- Explicitly retain that the two original unit generators have
different independently read fingerprint atoms, even though each
family still requires its separately supplied actual typed data. -/
theorem selectedV588ActualLeftRightUnitFingerprintDistinct :
    selectedLocalEighteenInnerBracket l r
        (SelectedLocalEighteen.unitLeft before F G C after) ≠
      selectedLocalEighteenInnerBracket l r
        (SelectedLocalEighteen.unitRight before F G C after) := by
  change SelectedInheritedOldInnerBracket.oldUnitLeft ≠
    SelectedInheritedOldInnerBracket.oldUnitRight
  decide

end GenuineOriginalUnitWitnessBoundary

#print axioms PentagonAdjoinedSixCell.SelectedV588UnitFreeTerm
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeBracket
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeParse
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeParse_onBracket
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeBracket_injective
#print axioms PentagonAdjoinedSixCell.selectedV588InnerUnitCount
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFree_hasZeroUnits
#print axioms PentagonAdjoinedSixCell.selectedV588NoFreeImage_ofUnitCountPositive
#print axioms PentagonAdjoinedSixCell.selectedV588NoFreeLeftUnitImage
#print axioms PentagonAdjoinedSixCell.selectedV588NoFreeRightUnitImage
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeRawEmbed
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeRaw_observed
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeRaw_parse
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeRawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeRawEmbed_injective
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeOldClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeNewClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeGuardedNewClassEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeOldComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeNewComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeOldNewComparison_iff
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeDistinctSeparated
#print axioms PentagonAdjoinedSixCell.selectedV588UnitFreeStrictVsDoubleReverse
#print axioms PentagonAdjoinedSixCell.selectedV588ActualLeftUnitNoFreeBracket
#print axioms PentagonAdjoinedSixCell.selectedV588ActualRightUnitNoFreeBracket
#print axioms PentagonAdjoinedSixCell.selectedV588ActualLeftRightUnitFingerprintDistinct

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
