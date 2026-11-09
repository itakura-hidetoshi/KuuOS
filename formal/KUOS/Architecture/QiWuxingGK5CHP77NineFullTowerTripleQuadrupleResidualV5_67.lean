import KUOS.Architecture.QiWuxingGK5CHP77NineFullTowerConsecutiveTripleResidualV5_66

/-!
Qi v5.67 — independently preserved FOUR-consecutive raw reversal
obstructs full classification even after observing all previous nine
quotient measurements, the complete Nat-indexed ancestor tower, AND
the independently conserved v5.66 triple-consecutive count.

A genuine original dependent raw18D N→N pair has reverse runs 4+2
and 3+3, separated by a strict chain. The pair agrees on every
ancestor-tower coordinate, the full ordered raw trace, top reverse,
adjacent reverse count, and triple-consecutive count (2 vs 2);
but its four-consecutive count is 1 vs 0. The new invariant is checked
against all five old selected19 and seven new raw-congruence constructors,
and descends separately to the old/new actual quotients.

The collision extends by chain into an EXACT original J→N fiber only
when a genuine M:J→N is supplied. No arbitrary fiber inhabitance,
new 20D comparison, all-WORLD gluing, completeness after adding this
new invariant, or external authority is claimed.

Preserve old 18D Type-valued evidence, original and new independent
19D comparisons, Lean/mathlib pins, public root107, and protected
validation-only PR #1558. append-only/tighten-only/overwrite-forbidden/same-root.
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

/-- An actual triple of immediate raw reversals at the outermost level.
A chain gap, even one containing many reverses, has flag zero. -/
def selectedContextEighteenTopTripleReverseFlag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .reverse L => selectedContextEighteenTopDoubleReverseFlag l r L
  | _ => 0

/-- The number of directly consecutive quadruples in a true 18D raw
proof term. Reversing creates one only when the child has a top triple.
All other inherited/whiskered/strict/chain constructors behave locally. -/
def selectedContextEighteenConsecutiveQuadrupleCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ M =>
      selectedContextEighteenConsecutiveQuadrupleCount l r M
  | .whiskerRight _ _ M _ =>
      selectedContextEighteenConsecutiveQuadrupleCount l r M
  | .strict _ => 0
  | .reverse M =>
      selectedContextEighteenConsecutiveQuadrupleCount l r M +
        selectedContextEighteenTopTripleReverseFlag l r M
  | .chain M L =>
      selectedContextEighteenConsecutiveQuadrupleCount l r M +
        selectedContextEighteenConsecutiveQuadrupleCount l r L

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The top-triple flag respects each original five-constructor typed
comparison. It does not assume any general raw proof identification. -/
theorem selectedLocalNineteen_preservesTopTripleReverseFlag
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenTopTripleReverseFlag l r M =
      selectedContextEighteenTopTripleReverseFlag l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Raw reverse in the new comparison requires the separately proved
top-double flag. Other six constructors have no new top-triple effect. -/
theorem selectedRawCongruent_preservesTopTripleReverseFlag
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenTopTripleReverseFlag l r M =
      selectedContextEighteenTopTripleReverseFlag l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesTopTripleReverseFlag l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change selectedContextEighteenTopDoubleReverseFlag l r _ =
        selectedContextEighteenTopDoubleReverseFlag l r _
      exact selectedRawCongruent_preservesTopDoubleReverseFlag l r A
  | rawChainRight A X ih => rfl
  | rawChainLeft X A ih => rfl

/-- The four-consecutive count respects ALL original five comparison
constructors, so its old quotient descent is not postulated. -/
theorem selectedLocalNineteen_preservesConsecutiveQuadrupleCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenConsecutiveQuadrupleCount l r M =
      selectedContextEighteenConsecutiveQuadrupleCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Independent preservation through ALL SEVEN constructors of the
actual v5.50 raw congruence; rawReverse uses the preceding flag. -/
theorem selectedRawCongruent_preservesConsecutiveQuadrupleCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenConsecutiveQuadrupleCount l r M =
      selectedContextEighteenConsecutiveQuadrupleCount l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesConsecutiveQuadrupleCount l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change selectedContextEighteenConsecutiveQuadrupleCount l r _ +
          selectedContextEighteenTopTripleReverseFlag l r _ =
        selectedContextEighteenConsecutiveQuadrupleCount l r _ +
          selectedContextEighteenTopTripleReverseFlag l r _
      exact congrArg₂ Nat.add ih
        (selectedRawCongruent_preservesTopTripleReverseFlag l r A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun k : Nat => k +
          selectedContextEighteenConsecutiveQuadrupleCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun k : Nat =>
          selectedContextEighteenConsecutiveQuadrupleCount l r X + k) ih

/-- Genuine descent to the new seven-constructor quotient. -/
def selectedRawCongruentConsecutiveQuadrupleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenConsecutiveQuadrupleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesConsecutiveQuadrupleCount l r A)

theorem selectedRawCongruentConsecutiveQuadruple_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentConsecutiveQuadrupleOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenConsecutiveQuadrupleCount l r M := rfl

/-- The same invariant descends independently to the old selected19
quotient, without identifying the old and the new presentations. -/
def selectedNineteenConsecutiveQuadrupleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenConsecutiveQuadrupleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesConsecutiveQuadrupleCount l r A)

theorem selectedConsecutiveQuadruple_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentConsecutiveQuadrupleOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenConsecutiveQuadrupleOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Exactly two immediate raw reversals over the true strict N→N. -/
def selectedQuadrupleWitnessDouble
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (selectedConsecutiveTripleWitnessSpine l r N)

/-- Exactly three immediate raw reversals over the true strict N→N. -/
def selectedQuadrupleWitnessTriple
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (selectedQuadrupleWitnessDouble l r N)

/-- Four directly consecutive reversals ABOVE the strict-chain gap,
two BELOW. Reverse blocks: [4,2]. -/
def selectedQuadrupleWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.reverse (.reverse
    (.reverse (selectedConsecutiveTripleWitnessGap l r N
      (selectedQuadrupleWitnessDouble l r N)))))

/-- Three directly consecutive reversals ABOVE the strict-chain gap,
three BELOW. Reverse blocks: [3,3]. -/
def selectedQuadrupleWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.reverse (.reverse
    (selectedConsecutiveTripleWitnessGap l r N
      (selectedQuadrupleWitnessTriple l r N))))

/-- A strict-chain gap commutes with one raw reverse as observed by
EVERY degree of the ancestor tower; it does NOT equate actual raw
proof terms or quotient classes. -/
theorem selectedQuadrupleWitness_gapMoveTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (A : SelectedContextualEighteen W l r N N)
    (n : Nat) :
    selectedAncestorTowerCount l r n
        (.reverse (selectedConsecutiveTripleWitnessGap l r N A)) =
      selectedAncestorTowerCount l r n
        (selectedConsecutiveTripleWitnessGap l r N (.reverse A)) := by
  have h : ∀ k : Nat,
      selectedAncestorTowerCount l r k
          (.reverse (selectedConsecutiveTripleWitnessGap l r N A)) =
        selectedAncestorTowerCount l r k (.reverse A) :=
    selectedFullTowerAdjacency_reverseTowerEq l r N
      (selectedConsecutiveTripleWitnessGap l r N A) A
      (selectedConsecutiveTripleWitness_gapTowerEq l r N A)
  exact (h n).trans
    (selectedConsecutiveTripleWitness_gapTowerEq l r N (.reverse A) n).symm

/-- Real [4,2] and [3,3] original Type-valued proof histories have
identical full infinite ancestor towers, not only finite samples.
The gap is moved by one reverse; three outer reverses preserve equality. -/
theorem selectedQuadrupleWitness_allTowerEq
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedAncestorTowerCount l r n (selectedQuadrupleWitnessLeft l r N) =
      selectedAncestorTowerCount l r n (selectedQuadrupleWitnessRight l r N) := by
  have h0 : ∀ k : Nat,
      selectedAncestorTowerCount l r k
        (.reverse (selectedConsecutiveTripleWitnessGap l r N
          (selectedQuadrupleWitnessDouble l r N))) =
      selectedAncestorTowerCount l r k
        (selectedConsecutiveTripleWitnessGap l r N
          (selectedQuadrupleWitnessTriple l r N)) :=
    selectedQuadrupleWitness_gapMoveTowerEq l r N
      (selectedQuadrupleWitnessDouble l r N)
  have h1 : ∀ k : Nat,
      selectedAncestorTowerCount l r k
        (.reverse (.reverse (selectedConsecutiveTripleWitnessGap l r N
          (selectedQuadrupleWitnessDouble l r N)))) =
      selectedAncestorTowerCount l r k
        (.reverse (selectedConsecutiveTripleWitnessGap l r N
          (selectedQuadrupleWitnessTriple l r N))) :=
    selectedFullTowerAdjacency_reverseTowerEq l r N
      (.reverse (selectedConsecutiveTripleWitnessGap l r N
        (selectedQuadrupleWitnessDouble l r N)))
      (selectedConsecutiveTripleWitnessGap l r N
        (selectedQuadrupleWitnessTriple l r N)) h0
  have h2 : ∀ k : Nat,
      selectedAncestorTowerCount l r k
        (.reverse (.reverse (.reverse (selectedConsecutiveTripleWitnessGap l r N
          (selectedQuadrupleWitnessDouble l r N))))) =
      selectedAncestorTowerCount l r k
        (.reverse (.reverse (selectedConsecutiveTripleWitnessGap l r N
          (selectedQuadrupleWitnessTriple l r N)))) :=
    selectedFullTowerAdjacency_reverseTowerEq l r N
      (.reverse (.reverse (selectedConsecutiveTripleWitnessGap l r N
        (selectedQuadrupleWitnessDouble l r N))))
      (.reverse (selectedConsecutiveTripleWitnessGap l r N
        (selectedQuadrupleWitnessTriple l r N))) h1
  exact selectedFullTowerAdjacency_reverseTowerEq l r N
    (.reverse (.reverse (.reverse (selectedConsecutiveTripleWitnessGap l r N
      (selectedQuadrupleWitnessDouble l r N)))))
    (.reverse (.reverse (selectedConsecutiveTripleWitnessGap l r N
      (selectedQuadrupleWitnessTriple l r N)))) h2 n

/-- The complete ordered external trace, not only its length, agrees. -/
theorem selectedQuadrupleWitness_traceEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTrace l r (selectedQuadrupleWitnessLeft l r N) =
      selectedContextEighteenTrace l r (selectedQuadrupleWitnessRight l r N) := by
  rfl

theorem selectedQuadrupleWitness_topEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTopReverseFlag l r (selectedQuadrupleWitnessLeft l r N) =
      selectedContextEighteenTopReverseFlag l r (selectedQuadrupleWitnessRight l r N) := by
  rfl

/-- Both pairs have exactly FOUR adjacent-reverse edges: 3+1=2+2. -/
theorem selectedQuadrupleWitness_adjacentEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedQuadrupleWitnessLeft l r N) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedQuadrupleWitnessRight l r N) := by
  rfl

/-- Both pairs have exactly TWO three-consecutive subruns: 2+0=1+1.
Thus the already independent v5.66 triple cannot distinguish them. -/
theorem selectedQuadrupleWitness_tripleEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessLeft l r N) =
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessRight l r N) := by
  rfl

/-- FOUR consecutive reverses occur exactly once on the left. -/
theorem selectedQuadrupleWitness_leftQuadOne
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenConsecutiveQuadrupleCount l r
        (selectedQuadrupleWitnessLeft l r N) = 1 := by
  rfl

/-- No four-consecutive reversal occurs in the right [3,3] term. -/
theorem selectedQuadrupleWitness_rightQuadZero
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenConsecutiveQuadrupleCount l r
        (selectedQuadrupleWitnessRight l r N) = 0 := by
  rfl

/-- All eight original quotient-observable raw equalities hold for
the actual new pair, by the five tower/count comparison bridges. -/
theorem selectedQuadrupleWitness_eightSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawEightSignature l r
      (selectedQuadrupleWitnessLeft l r N)
      (selectedQuadrupleWitnessRight l r N) := by
  let X : SelectedContextualEighteen W l r N N :=
    selectedQuadrupleWitnessLeft l r N
  let Y : SelectedContextualEighteen W l r N N :=
    selectedQuadrupleWitnessRight l r N
  have hT : ∀ k : Nat,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y :=
    selectedQuadrupleWitness_allTowerEq l r N
  refine ⟨selectedQuadrupleWitness_traceEq l r N,
    ?_, selectedQuadrupleWitness_adjacentEq l r N,
    selectedQuadrupleWitness_topEq l r N, ?_, ?_, ?_, ?_⟩
  · exact (selectedAncestorTower_eqReverseCount l r X).symm.trans
      ((hT 1).trans (selectedAncestorTower_eqReverseCount l r Y))
  · exact (selectedAncestorTower_eqAncestryCount l r X).symm.trans
      ((hT 2).trans (selectedAncestorTower_eqAncestryCount l r Y))
  · exact (selectedAncestorTower_eqAncestorTripleCount l r X).symm.trans
      ((hT 3).trans (selectedAncestorTower_eqAncestorTripleCount l r Y))
  · exact (selectedAncestorTower_eqAncestorQuadrupleCount l r X).symm.trans
      ((hT 4).trans (selectedAncestorTower_eqAncestorQuadrupleCount l r Y))
  · exact (selectedAncestorTower_eqAncestorQuintupleCount l r X).symm.trans
      ((hT 5).trans (selectedAncestorTower_eqAncestorQuintupleCount l r Y))

/-- The true new seven-generator quotient classes differ despite all
previous observations including the triple count agreeing. -/
theorem selectedQuadrupleWitness_classDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r (selectedQuadrupleWitnessLeft l r N) ≠
      selectedRawCongruentClass l r (selectedQuadrupleWitnessRight l r N) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentConsecutiveQuadrupleOnQuotient l r N N) h
  change selectedContextEighteenConsecutiveQuadrupleCount l r
      (selectedQuadrupleWitnessLeft l r N) =
    selectedContextEighteenConsecutiveQuadrupleCount l r
      (selectedQuadrupleWitnessRight l r N) at hc
  rw [selectedQuadrupleWitness_leftQuadOne l r N,
    selectedQuadrupleWitness_rightQuadZero l r N] at hc
  omega

/-- There is no Type-valued new19 comparison between these particular
two same-endpoint 18D terms. -/
theorem selectedQuadrupleWitness_noComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedQuadrupleWitnessLeft l r N)
      (selectedQuadrupleWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedQuadrupleWitness_classDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- Inject a true N→N collision into only an ACTUALLY INHABITED J→N
original dependent fiber. -/
def selectedQuadrupleWitnessFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedQuadrupleWitnessLeft l r N)

def selectedQuadrupleWitnessFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedQuadrupleWitnessRight l r N)

/-- The complete infinite tower remains equal after exact right
composition by the original supplied M:J→N. -/
theorem selectedQuadrupleWitnessFiber_allTowerEq
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedAncestorTowerCount l r n (selectedQuadrupleWitnessFiberLeft l r M) =
      selectedAncestorTowerCount l r n (selectedQuadrupleWitnessFiberRight l r M) := by
  cases n with
  | zero => rfl
  | succ n =>
      change selectedAncestorTowerCount l r (n + 1) M +
          selectedAncestorTowerCount l r (n + 1)
            (selectedQuadrupleWitnessLeft l r N) =
        selectedAncestorTowerCount l r (n + 1) M +
          selectedAncestorTowerCount l r (n + 1)
            (selectedQuadrupleWitnessRight l r N)
      exact congrArg
        (fun t : Nat => selectedAncestorTowerCount l r (n + 1) M + t)
        (selectedQuadrupleWitness_allTowerEq l r N (n + 1))

theorem selectedQuadrupleWitnessFiber_eightSignature
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawEightSignature l r
      (selectedQuadrupleWitnessFiberLeft l r M)
      (selectedQuadrupleWitnessFiberRight l r M) :=
  selectedRawEightSignature_rightChain l r M
    (selectedQuadrupleWitnessLeft l r N)
    (selectedQuadrupleWitnessRight l r N)
    (selectedQuadrupleWitness_eightSignature l r N)

/-- The triple count remains equal even after transport into the
supplied fiber, because raw chain only adds subtree counts. -/
theorem selectedQuadrupleWitnessFiber_tripleEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessFiberLeft l r M) =
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessFiberRight l r M) := by
  change selectedContextEighteenConsecutiveTripleCount l r M +
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessLeft l r N) =
    selectedContextEighteenConsecutiveTripleCount l r M +
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessRight l r N)
  exact congrArg
    (fun k : Nat => selectedContextEighteenConsecutiveTripleCount l r M + k)
    (selectedQuadrupleWitness_tripleEq l r N)

/-- The one-unit new quadruple residual survives the exact fiber. -/
theorem selectedQuadrupleWitnessFiber_quadGap
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenConsecutiveQuadrupleCount l r
        (selectedQuadrupleWitnessFiberLeft l r M) =
      selectedContextEighteenConsecutiveQuadrupleCount l r
        (selectedQuadrupleWitnessFiberRight l r M) + 1 := by
  change selectedContextEighteenConsecutiveQuadrupleCount l r M +
      selectedContextEighteenConsecutiveQuadrupleCount l r
        (selectedQuadrupleWitnessLeft l r N) =
    (selectedContextEighteenConsecutiveQuadrupleCount l r M +
      selectedContextEighteenConsecutiveQuadrupleCount l r
        (selectedQuadrupleWitnessRight l r N)) + 1
  rw [selectedQuadrupleWitness_leftQuadOne l r N,
    selectedQuadrupleWitness_rightQuadZero l r N]

theorem selectedQuadrupleWitnessFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentConsecutiveQuadrupleOnQuotient l r J N) h
  change selectedContextEighteenConsecutiveQuadrupleCount l r
      (selectedQuadrupleWitnessFiberLeft l r M) =
    selectedContextEighteenConsecutiveQuadrupleCount l r
      (selectedQuadrupleWitnessFiberRight l r M) at hc
  rw [selectedQuadrupleWitnessFiber_quadGap l r M] at hc
  omega

/-- The actual nine-observer joined to the full Nat→Nat tower and
the independently certified v5.66 consecutive-triple count. -/
def selectedRawCongruentNineFullTowerTripleObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (selectedRawNineObservationValue × (Nat → Nat)) × Nat :=
  fun q => (selectedRawCongruentNineFullTowerObservation l r J N q,
    selectedRawCongruentConsecutiveTripleOnQuotient l r J N q)

/-- The original nine plus entire tower agrees on both actual
same-fiber classes; this is not obtained from finite sampling. -/
theorem selectedQuadrupleWitnessFiber_nineFullTowerEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentNineFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberLeft l r M)) =
      selectedRawCongruentNineFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberRight l r M)) := by
  apply Prod.ext
  · apply Prod.ext
    · exact selectedRawEightSignature_toObservation l r
        (selectedQuadrupleWitnessFiberLeft l r M)
        (selectedQuadrupleWitnessFiberRight l r M)
        (selectedQuadrupleWitnessFiber_eightSignature l r M)
    · change selectedAncestorTowerCount l r 6
          (selectedQuadrupleWitnessFiberLeft l r M) =
        selectedAncestorTowerCount l r 6
          (selectedQuadrupleWitnessFiberRight l r M)
      exact selectedQuadrupleWitnessFiber_allTowerEq l r M 6
  · funext n
    change selectedAncestorTowerCount l r n
        (selectedQuadrupleWitnessFiberLeft l r M) =
      selectedAncestorTowerCount l r n
        (selectedQuadrupleWitnessFiberRight l r M)
    exact selectedQuadrupleWitnessFiber_allTowerEq l r M n

/-- The augmented observation ALSO agrees after adding triple count.
This does not include the new four-consecutive count. -/
theorem selectedQuadrupleWitnessFiber_nineFullTowerTripleEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentNineFullTowerTripleObservation l r J N
        (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberLeft l r M)) =
      selectedRawCongruentNineFullTowerTripleObservation l r J N
        (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberRight l r M)) := by
  apply Prod.ext
  · exact selectedQuadrupleWitnessFiber_nineFullTowerEq l r M
  · change selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessFiberLeft l r M) =
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedQuadrupleWitnessFiberRight l r M)
    exact selectedQuadrupleWitnessFiber_tripleEq l r M

/-- The full NINE + INFINITE tower + triple observer remains
noninjective on every actually supplied original exact fiber. -/
theorem selectedRawCongruentNineFullTowerTriple_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentNineFullTowerTripleObservation l r J N) := by
  intro hinj
  exact (selectedQuadrupleWitnessFiber_classDistinct l r M)
    (hinj (selectedQuadrupleWitnessFiber_nineFullTowerTripleEq l r M))

/-- No decoder of the separately conserved FOUR-consecutive raw
reverse count exists from the enlarged observation. -/
theorem selectedRawCongruentNineFullTowerTriple_noQuadrupleDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : ((selectedRawNineObservationValue × (Nat → Nat)) × Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentNineFullTowerTripleObservation l r J N q) =
          selectedRawCongruentConsecutiveQuadrupleOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentConsecutiveQuadrupleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberLeft l r M)) =
        selectedRawCongruentConsecutiveQuadrupleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberRight l r M)) := by
    calc
      _ = decode (selectedRawCongruentNineFullTowerTripleObservation l r J N
            (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberLeft l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentNineFullTowerTripleObservation l r J N
            (selectedRawCongruentClass l r (selectedQuadrupleWitnessFiberRight l r M))) :=
        congrArg decode (selectedQuadrupleWitnessFiber_nineFullTowerTripleEq l r M)
      _ = _ := h _
  change selectedContextEighteenConsecutiveQuadrupleCount l r
      (selectedQuadrupleWitnessFiberLeft l r M) =
    selectedContextEighteenConsecutiveQuadrupleCount l r
      (selectedQuadrupleWitnessFiberRight l r M) at hc
  rw [selectedQuadrupleWitnessFiber_quadGap l r M] at hc
  omega

/-- Equally, no global right-inverse/class decoder is available
on that genuinely inhabited quotient fiber. -/
theorem selectedRawCongruentNineFullTowerTriple_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        ((selectedRawNineObservationValue × (Nat → Nat)) × Nat) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentNineFullTowerTripleObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentNineFullTowerTriple_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentNineFullTowerTripleObservation l r J N a) := (h a).symm
    _ = decode (selectedRawCongruentNineFullTowerTripleObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- Explicit strict J→J witness: no arbitrary heterogeneous inhabitance
is needed to exhibit a genuine collision in any endomorphism fiber. -/
theorem selectedRawCongruentNineFullTowerTriple_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentNineFullTowerTripleObservation l r J J) :=
  selectedRawCongruentNineFullTowerTriple_notInjective l r
    (SelectedContextualEighteen.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTopTripleReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenConsecutiveQuadrupleCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesTopTripleReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesTopTripleReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesConsecutiveQuadrupleCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesConsecutiveQuadrupleCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentConsecutiveQuadrupleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentConsecutiveQuadruple_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenConsecutiveQuadrupleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedConsecutiveQuadruple_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessDouble
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessTriple
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_gapMoveTowerEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_traceEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_topEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_adjacentEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_tripleEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_leftQuadOne
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_rightQuadZero
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitness_noComparison
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiberRight
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiber_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiber_tripleEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiber_quadGap
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTowerTripleObservation
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiber_nineFullTowerEq
#print axioms PentagonAdjoinedSixCell.selectedQuadrupleWitnessFiber_nineFullTowerTripleEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTowerTriple_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTowerTriple_noQuadrupleDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTowerTriple_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTowerTriple_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
