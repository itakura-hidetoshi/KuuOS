import KUOS.Architecture.QiWuxingGK5CHP77FullDoubleInfiniteOrderedRunResidualV5_69

/-!
Qi v5.70 — a genuinely unit-reduced, NONASSOCIATIVE raw-bracket
shape remains after observing the ENTIRE natural-indexed ancestor
tower, ENTIRE natural-indexed direct reverse-run-count tower,
the ordered raw-reverse run-length list, and all NINE existing new
quotient observables.

Source witnesses are ORIGINAL dependent 18D Type-valued proofs:
  R = reverse (strict N)
  A = chain (chain R R) R
  B = chain R (chain R R).
The total number of reverse nodes, complete ancestor tower, complete
run count tower, ordered run list [1,1,1], full ordered raw exterior
trace, and top-reverse flag all agree; only the binary bracketing
differs.

A unit-reduced nonassociative syntax tree is an independent
interpretation of the raw18D evidence: strict and inherited nodes are
units; whiskers preserve the inner structure; raw reverse remains
unary; raw chain forms a binary join with explicit unit elimination.
Preservation is PROVED for each of the FIVE old selected19 and SEVEN
new raw-congruence constructors, including both genuine raw chain
whiskerings. Separate Quotient.lift on old and new quotients and exact
old→new factorization are constructed; no assumption of associativity
is introduced.

In every actually supplied original M:J→N exact dependent fiber,
a common unit-reduced bracket prefix does not identify the two
nonassociative shapes. Hence genuine new quotient classes are
distinct although the complete double-infinite + ordered observation
coincides, with no bracket-shape/class decoder. Endomorphism J→J has
the explicit original strict value.

This is a LOCAL noninjectivity result, not all quotient
classification after adding bracket shape; no 20D gluing, arbitrary
heterogeneous fiber inhabitance, cross-WORLD descent, interpretation
of Buddhist emptiness as a theorem, or institutional action authority.
Original Type values, comparisons, root107, pinned Lean/mathlib,
validation-only PR #1558 remain untouched.
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

/-- An independent NONASSOCIATIVE, UNIT-REDUCED observation of raw
18D proof syntax. Do not identify its values with source Type18D. -/
inductive SelectedRawUnitReducedBracket : Type where
  | unit : SelectedRawUnitReducedBracket
  | reversed : SelectedRawUnitReducedBracket → SelectedRawUnitReducedBracket
  | joined : SelectedRawUnitReducedBracket →
      SelectedRawUnitReducedBracket → SelectedRawUnitReducedBracket
  deriving DecidableEq, Repr

/-- Unit reduction is explicit, but no associativity quotient is
performed. The two binary bracketings remain distinguishable. -/
def selectedRawUnitReducedBracketJoin :
    SelectedRawUnitReducedBracket →
    SelectedRawUnitReducedBracket → SelectedRawUnitReducedBracket
  | .unit, B => B
  | A, .unit => A
  | A, B => .joined A B

/-- Genuine ORIGINAL raw18D recursion to a new independent
unit-reduced bracket shape. The old inherited proof stays in its
source Type; its coarse value is the unit, as is raw strict. -/
def selectedContextEighteenUnitReducedBracket (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedRawUnitReducedBracket :=
  match M with
  | .inherited _ => .unit
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenUnitReducedBracket l r A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenUnitReducedBracket l r A
  | .strict _ => .unit
  | .reverse A =>
      .reversed (selectedContextEighteenUnitReducedBracket l r A)
  | .chain A B =>
      selectedRawUnitReducedBracketJoin
        (selectedContextEighteenUnitReducedBracket l r A)
        (selectedContextEighteenUnitReducedBracket l r B)

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- ALL FIVE original selected19 comparison generators preserve the
unit-reduced bracket shape. The two old unit rules eliminate
strict/inherited nodes, not any arbitrary raw reverse expression. -/
theorem selectedLocalNineteen_preservesUnitReducedBracket
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenUnitReducedBracket l r M =
      selectedContextEighteenUnitReducedBracket l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- ALL SEVEN new independent raw-congruence generators preserve the
bracket tree. RawReverse and both rawChain congruences are proved,
not assumed, via the actual typed induction hypotheses. -/
theorem selectedRawCongruent_preservesUnitReducedBracket
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenUnitReducedBracket l r M =
      selectedContextEighteenUnitReducedBracket l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesUnitReducedBracket l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      exact congrArg SelectedRawUnitReducedBracket.reversed ih
  | rawChainRight A X ih =>
      exact congrArg
        (fun s : SelectedRawUnitReducedBracket =>
          selectedRawUnitReducedBracketJoin s
            (selectedContextEighteenUnitReducedBracket l r X)) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun s : SelectedRawUnitReducedBracket =>
          selectedRawUnitReducedBracketJoin
            (selectedContextEighteenUnitReducedBracket l r X) s) ih

/-- The actual new seven-generator quotient carries this independently
descended, proof-relevant unit-reduced bracket presentation. -/
def selectedRawCongruentUnitReducedBracketOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      SelectedRawUnitReducedBracket :=
  Quotient.lift (selectedContextEighteenUnitReducedBracket l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesUnitReducedBracket l r A)

theorem selectedRawCongruentUnitReducedBracket_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentUnitReducedBracketOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenUnitReducedBracket l r M := rfl

/-- Original selected19 quotient descent is proved separately and is
not an identification of old and new 19D Type-valued comparisons. -/
def selectedNineteenUnitReducedBracketOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedRawUnitReducedBracket :=
  Quotient.lift (selectedContextEighteenUnitReducedBracket l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesUnitReducedBracket l r A)

theorem selectedUnitReducedBracket_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentUnitReducedBracketOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenUnitReducedBracketOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- A true one-reversal original raw18D loop, not an invented
inhabitant of a heterogeneous exact fiber. -/
def selectedBracketShapeSpine
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.strict N)

/-- Left-associated raw chain of three original one-reversal loops. -/
def selectedBracketShapeWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain
    (.chain (selectedBracketShapeSpine l r N)
      (selectedBracketShapeSpine l r N))
    (selectedBracketShapeSpine l r N)

/-- Right-associated raw chain with precisely the same ordered
one-reversal loops and exactly the same dependent endpoints. -/
def selectedBracketShapeWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .chain (selectedBracketShapeSpine l r N)
    (.chain (selectedBracketShapeSpine l r N)
      (selectedBracketShapeSpine l r N))

def selectedBracketShapeAtom : SelectedRawUnitReducedBracket :=
  .reversed .unit

def selectedBracketShapeLeftValue : SelectedRawUnitReducedBracket :=
  .joined (.joined selectedBracketShapeAtom selectedBracketShapeAtom)
    selectedBracketShapeAtom

def selectedBracketShapeRightValue : SelectedRawUnitReducedBracket :=
  .joined selectedBracketShapeAtom
    (.joined selectedBracketShapeAtom selectedBracketShapeAtom)

/-- The true Type-valued left witness retains the exact left
parenthesization after unit reduction. -/
theorem selectedBracketShape_leftValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenUnitReducedBracket l r
        (selectedBracketShapeWitnessLeft l r N) =
      selectedBracketShapeLeftValue := by
  rfl

theorem selectedBracketShape_rightValue
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenUnitReducedBracket l r
        (selectedBracketShapeWitnessRight l r N) =
      selectedBracketShapeRightValue := by
  rfl

/-- Free nonassociative binary trees distinguish the two original
genuine raw parenthesizations. No associativity axiom is introduced. -/
theorem selectedBracketShape_valuesDistinct :
    selectedBracketShapeLeftValue ≠ selectedBracketShapeRightValue := by
  decide

theorem selectedBracketShape_witnessShapeDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenUnitReducedBracket l r
        (selectedBracketShapeWitnessLeft l r N) ≠
      selectedContextEighteenUnitReducedBracket l r
        (selectedBracketShapeWitnessRight l r N) := by
  rw [selectedBracketShape_leftValue l r N,
    selectedBracketShape_rightValue l r N]
  exact selectedBracketShape_valuesDistinct

/-- The full ordered reverse-run list is IDENTICAL [1,1,1] despite
nonassociative binary bracketing of the original raw chain. -/
theorem selectedBracketShape_orderedListEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeWitnessLeft l r N) =
      selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeWitnessRight l r N) := by
  rfl

/-- The COMPLETE Nat-indexed ancestor towers are identical. For
positive degrees, both original bracketings count three identical
one-reversal subproofs, by associativity of Nat ADDITION, not by
postulating associativity of raw typed 18D chain. -/
theorem selectedBracketShape_allTowerEq
    (N : SelectedContextualSeventeen W l r H K) (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedBracketShapeWitnessLeft l r N) =
      selectedAncestorTowerCount l r degree
        (selectedBracketShapeWitnessRight l r N) := by
  cases degree with
  | zero => rfl
  | succ d =>
      change
        (selectedAncestorTowerCount l r (d + 1)
            (selectedBracketShapeSpine l r N) +
          selectedAncestorTowerCount l r (d + 1)
            (selectedBracketShapeSpine l r N)) +
          selectedAncestorTowerCount l r (d + 1)
            (selectedBracketShapeSpine l r N) =
        selectedAncestorTowerCount l r (d + 1)
            (selectedBracketShapeSpine l r N) +
          (selectedAncestorTowerCount l r (d + 1)
              (selectedBracketShapeSpine l r N) +
            selectedAncestorTowerCount l r (d + 1)
              (selectedBracketShapeSpine l r N))
      exact Nat.add_assoc _ _ _

/-- Every Nat-indexed consecutive-reverse-run count agrees, including
the whole infinite tower introduced in Qi v5.68. -/
theorem selectedBracketShape_allRunCountsEq
    (N : SelectedContextualSeventeen W l r H K) (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeWitnessLeft l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeWitnessRight l r N) := by
  change
    (selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeSpine l r N) +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeSpine l r N)) +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeSpine l r N) =
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeSpine l r N) +
      (selectedContextEighteenConsecutiveRunCount l r degree
          (selectedBracketShapeSpine l r N) +
        selectedContextEighteenConsecutiveRunCount l r degree
          (selectedBracketShapeSpine l r N))
  exact Nat.add_assoc _ _ _

theorem selectedBracketShape_traceEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTrace l r
        (selectedBracketShapeWitnessLeft l r N) =
      selectedContextEighteenTrace l r
        (selectedBracketShapeWitnessRight l r N) := by
  rfl

theorem selectedBracketShape_topEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTopReverseFlag l r
        (selectedBracketShapeWitnessLeft l r N) =
      selectedContextEighteenTopReverseFlag l r
        (selectedBracketShapeWitnessRight l r N) := by
  rfl

theorem selectedBracketShape_adjacentEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedBracketShapeWitnessLeft l r N) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedBracketShapeWitnessRight l r N) := by
  rw [← selectedConsecutiveRun_degreeOne_eqAdjacent l r
      (selectedBracketShapeWitnessLeft l r N),
    ← selectedConsecutiveRun_degreeOne_eqAdjacent l r
      (selectedBracketShapeWitnessRight l r N)]
  exact selectedBracketShape_allRunCountsEq l r N 1

/-- Genuine simultaneous equality of all eight old new-quotient
observables from the FULL actual original dependent ancestor tower,
ordered trace, adjacency and top reverse. -/
theorem selectedBracketShape_eightSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawEightSignature l r
      (selectedBracketShapeWitnessLeft l r N)
      (selectedBracketShapeWitnessRight l r N) := by
  let X : SelectedContextualEighteen W l r N N :=
    selectedBracketShapeWitnessLeft l r N
  let Y : SelectedContextualEighteen W l r N N :=
    selectedBracketShapeWitnessRight l r N
  have ht : ∀ d : Nat,
      selectedAncestorTowerCount l r d X =
        selectedAncestorTowerCount l r d Y :=
    selectedBracketShape_allTowerEq l r N
  refine ⟨selectedBracketShape_traceEq l r N,
    ?_, selectedBracketShape_adjacentEq l r N,
    selectedBracketShape_topEq l r N, ?_, ?_, ?_, ?_⟩
  · exact (selectedAncestorTower_eqReverseCount l r X).symm.trans
      ((ht 1).trans (selectedAncestorTower_eqReverseCount l r Y))
  · exact (selectedAncestorTower_eqAncestryCount l r X).symm.trans
      ((ht 2).trans (selectedAncestorTower_eqAncestryCount l r Y))
  · exact (selectedAncestorTower_eqAncestorTripleCount l r X).symm.trans
      ((ht 3).trans (selectedAncestorTower_eqAncestorTripleCount l r Y))
  · exact (selectedAncestorTower_eqAncestorQuadrupleCount l r X).symm.trans
      ((ht 4).trans (selectedAncestorTower_eqAncestorQuadrupleCount l r Y))
  · exact (selectedAncestorTower_eqAncestorQuintupleCount l r X).symm.trans
      ((ht 5).trans (selectedAncestorTower_eqAncestorQuintupleCount l r Y))

theorem selectedBracketShape_classDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedBracketShapeWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedBracketShapeWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentUnitReducedBracketOnQuotient l r N N) h
  change selectedContextEighteenUnitReducedBracket l r
      (selectedBracketShapeWitnessLeft l r N) =
    selectedContextEighteenUnitReducedBracket l r
      (selectedBracketShapeWitnessRight l r N) at hc
  exact (selectedBracketShape_witnessShapeDistinct l r N) hc

theorem selectedBracketShape_noComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedBracketShapeWitnessLeft l r N)
      (selectedBracketShapeWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedBracketShape_classDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- Project the RIGHT child of a concrete joined bracket. This
constructor projection is used only to cancel a common prefix
without quotienting away genuine association information. -/
def selectedRawUnitReducedBracketRightChild :
    SelectedRawUnitReducedBracket → SelectedRawUnitReducedBracket
  | .joined _ B => B
  | _ => .unit

/-- Left composition with any original source bracket cannot erase
this specific difference of NONUNIT right suffixes. No unsupported
general cancellativity assertion is made for unrelated shapes. -/
theorem selectedBracketShape_joinDistinct
    (pre : SelectedRawUnitReducedBracket) :
    selectedRawUnitReducedBracketJoin pre selectedBracketShapeLeftValue ≠
      selectedRawUnitReducedBracketJoin pre selectedBracketShapeRightValue := by
  cases pre with
  | unit =>
      exact selectedBracketShape_valuesDistinct
  | reversed X =>
      intro h
      have hc := congrArg selectedRawUnitReducedBracketRightChild h
      change selectedBracketShapeLeftValue = selectedBracketShapeRightValue at hc
      exact selectedBracketShape_valuesDistinct hc
  | joined X Y =>
      intro h
      have hc := congrArg selectedRawUnitReducedBracketRightChild h
      change selectedBracketShapeLeftValue = selectedBracketShapeRightValue at hc
      exact selectedBracketShape_valuesDistinct hc

/-- A genuine specified original M:J→N is REQUIRED before right
composing the collision into that SAME exact dependent fiber. -/
def selectedBracketShapeFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedBracketShapeWitnessLeft l r N)

def selectedBracketShapeFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedBracketShapeWitnessRight l r N)

theorem selectedBracketShapeFiber_shapeDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenUnitReducedBracket l r
        (selectedBracketShapeFiberLeft l r M) ≠
      selectedContextEighteenUnitReducedBracket l r
        (selectedBracketShapeFiberRight l r M) := by
  change
    selectedRawUnitReducedBracketJoin
      (selectedContextEighteenUnitReducedBracket l r M)
      selectedBracketShapeLeftValue ≠
    selectedRawUnitReducedBracketJoin
      (selectedContextEighteenUnitReducedBracket l r M)
      selectedBracketShapeRightValue
  exact selectedBracketShape_joinDistinct _

theorem selectedBracketShapeFiber_allTowerEq
    (M : SelectedContextualEighteen W l r J N) (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedBracketShapeFiberLeft l r M) =
      selectedAncestorTowerCount l r degree
        (selectedBracketShapeFiberRight l r M) := by
  cases degree with
  | zero => rfl
  | succ d =>
      change selectedAncestorTowerCount l r (d + 1) M +
          selectedAncestorTowerCount l r (d + 1)
            (selectedBracketShapeWitnessLeft l r N) =
        selectedAncestorTowerCount l r (d + 1) M +
          selectedAncestorTowerCount l r (d + 1)
            (selectedBracketShapeWitnessRight l r N)
      exact congrArg
        (fun t : Nat => selectedAncestorTowerCount l r (d + 1) M + t)
        (selectedBracketShape_allTowerEq l r N (d + 1))

theorem selectedBracketShapeFiber_allRunCountsEq
    (M : SelectedContextualEighteen W l r J N) (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeFiberLeft l r M) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeFiberRight l r M) := by
  change selectedContextEighteenConsecutiveRunCount l r degree M +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeWitnessLeft l r N) =
    selectedContextEighteenConsecutiveRunCount l r degree M +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedBracketShapeWitnessRight l r N)
  exact congrArg
    (fun t : Nat => selectedContextEighteenConsecutiveRunCount l r degree M + t)
    (selectedBracketShape_allRunCountsEq l r N degree)

theorem selectedBracketShapeFiber_orderedListEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeFiberLeft l r M) =
      selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeFiberRight l r M) := by
  change selectedContextEighteenOrderedRunList l r M ++
      selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeWitnessLeft l r N) =
    selectedContextEighteenOrderedRunList l r M ++
      selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeWitnessRight l r N)
  exact congrArg (fun xs : List Nat =>
      selectedContextEighteenOrderedRunList l r M ++ xs)
    (selectedBracketShape_orderedListEq l r N)

theorem selectedBracketShapeFiber_eightSignature
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawEightSignature l r
      (selectedBracketShapeFiberLeft l r M)
      (selectedBracketShapeFiberRight l r M) :=
  selectedRawEightSignature_rightChain l r M
    (selectedBracketShapeWitnessLeft l r N)
    (selectedBracketShapeWitnessRight l r N)
    (selectedBracketShape_eightSignature l r N)

theorem selectedBracketShapeFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedBracketShapeFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedBracketShapeFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentUnitReducedBracketOnQuotient l r J N) h
  change selectedContextEighteenUnitReducedBracket l r
      (selectedBracketShapeFiberLeft l r M) =
    selectedContextEighteenUnitReducedBracket l r
      (selectedBracketShapeFiberRight l r M) at hc
  exact (selectedBracketShapeFiber_shapeDistinct l r M) hc

/-- The previously certified complete double-infinite observer
augmented by the fully ordered raw-reverse-run-length list. -/
def selectedRawCongruentFullDoubleOrderedObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      ((selectedRawNineObservationValue × (Nat → Nat)) × (Nat → Nat)) × List Nat :=
  fun q => (selectedRawCongruentFullDoubleInfiniteObservation l r J N q,
    selectedRawCongruentOrderedRunListOnQuotient l r J N q)

theorem selectedBracketShapeFiber_doubleInfiniteEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFullDoubleInfiniteObservation l r J N
        (selectedRawCongruentClass l r (selectedBracketShapeFiberLeft l r M)) =
      selectedRawCongruentFullDoubleInfiniteObservation l r J N
        (selectedRawCongruentClass l r (selectedBracketShapeFiberRight l r M)) := by
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact selectedRawEightSignature_toObservation l r
          (selectedBracketShapeFiberLeft l r M)
          (selectedBracketShapeFiberRight l r M)
          (selectedBracketShapeFiber_eightSignature l r M)
      · change selectedAncestorTowerCount l r 6
            (selectedBracketShapeFiberLeft l r M) =
          selectedAncestorTowerCount l r 6
            (selectedBracketShapeFiberRight l r M)
        exact selectedBracketShapeFiber_allTowerEq l r M 6
    · funext d
      change selectedAncestorTowerCount l r d
          (selectedBracketShapeFiberLeft l r M) =
        selectedAncestorTowerCount l r d
          (selectedBracketShapeFiberRight l r M)
      exact selectedBracketShapeFiber_allTowerEq l r M d
  · funext d
    change selectedContextEighteenConsecutiveRunCount l r d
        (selectedBracketShapeFiberLeft l r M) =
      selectedContextEighteenConsecutiveRunCount l r d
        (selectedBracketShapeFiberRight l r M)
    exact selectedBracketShapeFiber_allRunCountsEq l r M d

theorem selectedBracketShapeFiber_fullObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFullDoubleOrderedObservation l r J N
        (selectedRawCongruentClass l r (selectedBracketShapeFiberLeft l r M)) =
      selectedRawCongruentFullDoubleOrderedObservation l r J N
        (selectedRawCongruentClass l r (selectedBracketShapeFiberRight l r M)) := by
  apply Prod.ext
  · exact selectedBracketShapeFiber_doubleInfiniteEq l r M
  · change selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeFiberLeft l r M) =
      selectedContextEighteenOrderedRunList l r
        (selectedBracketShapeFiberRight l r M)
    exact selectedBracketShapeFiber_orderedListEq l r M

theorem selectedRawCongruentFullDoubleOrdered_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentFullDoubleOrderedObservation l r J N) := by
  intro hinj
  exact (selectedBracketShapeFiber_classDistinct l r M)
    (hinj (selectedBracketShapeFiber_fullObservedEq l r M))

/-- The augmented observer cannot decode the independently descended
unit-reduced bracket shape on a genuinely inhabited exact fiber. -/
theorem selectedRawCongruentFullDoubleOrdered_noBracketDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        (((selectedRawNineObservationValue × (Nat → Nat)) × (Nat → Nat)) ×
          List Nat) → SelectedRawUnitReducedBracket,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFullDoubleOrderedObservation l r J N q) =
          selectedRawCongruentUnitReducedBracketOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentUnitReducedBracketOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedBracketShapeFiberLeft l r M)) =
        selectedRawCongruentUnitReducedBracketOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedBracketShapeFiberRight l r M)) := by
    calc
      _ = decode (selectedRawCongruentFullDoubleOrderedObservation l r J N
            (selectedRawCongruentClass l r (selectedBracketShapeFiberLeft l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentFullDoubleOrderedObservation l r J N
            (selectedRawCongruentClass l r (selectedBracketShapeFiberRight l r M))) :=
        congrArg decode (selectedBracketShapeFiber_fullObservedEq l r M)
      _ = _ := h _
  change selectedContextEighteenUnitReducedBracket l r
      (selectedBracketShapeFiberLeft l r M) =
    selectedContextEighteenUnitReducedBracket l r
      (selectedBracketShapeFiberRight l r M) at hc
  exact (selectedBracketShapeFiber_shapeDistinct l r M) hc

theorem selectedRawCongruentFullDoubleOrdered_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        (((selectedRawNineObservationValue × (Nat → Nat)) × (Nat → Nat)) ×
          List Nat) → Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFullDoubleOrderedObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentFullDoubleOrdered_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentFullDoubleOrderedObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentFullDoubleOrderedObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

theorem selectedRawCongruentFullDoubleOrdered_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullDoubleOrderedObservation l r J J) :=
  selectedRawCongruentFullDoubleOrdered_notInjective l r (.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.SelectedRawUnitReducedBracket
#print axioms PentagonAdjoinedSixCell.selectedRawUnitReducedBracketJoin
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenUnitReducedBracket
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesUnitReducedBracket
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesUnitReducedBracket
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentUnitReducedBracketOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentUnitReducedBracket_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenUnitReducedBracketOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedUnitReducedBracket_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeSpine
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeAtom
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeLeftValue
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeRightValue
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_leftValue
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_rightValue
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_valuesDistinct
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_witnessShapeDistinct
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_orderedListEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_allRunCountsEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_traceEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_topEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_adjacentEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_noComparison
#print axioms PentagonAdjoinedSixCell.selectedRawUnitReducedBracketRightChild
#print axioms PentagonAdjoinedSixCell.selectedBracketShape_joinDistinct
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiberRight
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_shapeDistinct
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_allRunCountsEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_orderedListEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleOrderedObservation
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_doubleInfiniteEq
#print axioms PentagonAdjoinedSixCell.selectedBracketShapeFiber_fullObservedEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleOrdered_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleOrdered_noBracketDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleOrdered_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleOrdered_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
