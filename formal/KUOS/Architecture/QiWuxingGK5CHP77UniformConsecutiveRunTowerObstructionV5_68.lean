import KUOS.Architecture.QiWuxingGK5CHP77NineFullTowerTripleQuadrupleResidualV5_67

/-!
Qi v5.68 — a genuinely uniform finite-prefix obstruction for ALL
direct-consecutive reverse-run statistics, even when the COMPLETE
infinite ancestor tower and the original nine quotient observers
are supplied.

For every n : Nat, build ORIGINAL dependent raw18D N→N values
with two reverse runs [n+4,n+2] versus [n+3,n+3], separated by one
genuine chain with the strict identity. All run counts of length
1 through n+3 agree, every infinite ancestor coordinate agrees,
the full ordered trace and old nine observable values agree,
but the run count of length n+4 differs by exactly one.

The run statistics descend separately through ALL five original
selected19 and ALL seven new raw-congruence constructors, not by
postulating a comparison. After actual right composition with an
explicitly supplied original M:J→N, the enlarged new-quotient
observation remains noninjective, with no decoder for the next count
or the entire quotient class. A strict J→J witness is explicit.

Neither arbitrary heterogeneous-fiber inhabitance, complete
classification after ALL run counts, independent WORLD gluing,
20D descent nor action authority is claimed.
Keep original Type values, old/new presentations, public root107,
pinned Lean/mathlib, protected validation-only #1558 unchanged.
append-only/tighten-only/overwrite-forbidden/same-root.
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

/-- Length of the immediately consecutive raw-reverse prefix.
A chain, including insertion of strict identity, resets this length. -/
def selectedContextEighteenTopRunLength (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .reverse A => Nat.succ (selectedContextEighteenTopRunLength l r A)
  | _ => 0

/-- Count every consecutive raw-reversal subrun of length (degree+1).
For degree=0 this is total reversals; degree=1 counts direct
adjacencies, degree=2 triples and degree=3 quadruples.
The original dependent 18D proof is never erased to a proxy. -/
def selectedContextEighteenConsecutiveRunCount (l r : W) (degree : Nat)
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
  | .whiskerLeft _ _ _ A =>
      selectedContextEighteenConsecutiveRunCount l r degree A
  | .whiskerRight _ _ A _ =>
      selectedContextEighteenConsecutiveRunCount l r degree A
  | .strict _ => 0
  | .reverse A =>
      selectedContextEighteenConsecutiveRunCount l r degree A +
        (if degree ≤ selectedContextEighteenTopRunLength l r A then 1 else 0)
  | .chain A B =>
      selectedContextEighteenConsecutiveRunCount l r degree A +
        selectedContextEighteenConsecutiveRunCount l r degree B

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The top-run length respects all FIVE ORIGINAL selected19 rules.
Old unit rules compare only non-reverse outer constructors. -/
theorem selectedLocalNineteen_preservesTopRunLength
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenTopRunLength l r M =
      selectedContextEighteenTopRunLength l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- ALL SEVEN new comparison generators preserve top-run length.
The rawReverse constructor uses the induction hypothesis under succ;
rawChainLeft/Right have outermost chain, hence both top lengths zero. -/
theorem selectedRawCongruent_preservesTopRunLength
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenTopRunLength l r M =
      selectedContextEighteenTopRunLength l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesTopRunLength l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change Nat.succ (selectedContextEighteenTopRunLength l r _) =
        Nat.succ (selectedContextEighteenTopRunLength l r _)
      exact congrArg Nat.succ ih
  | rawChainRight A X ih => rfl
  | rawChainLeft X A ih => rfl

/-- The whole Nat-indexed family of run counts respects all FIVE old
19D rules, independently of the new comparison presentation. -/
theorem selectedLocalNineteen_preservesConsecutiveRunCount
    (degree : Nat) {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenConsecutiveRunCount l r degree M =
      selectedContextEighteenConsecutiveRunCount l r degree L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Every degree, without a finite cutoff, preserves all SEVEN new
raw-congruence generators. The rawReverse case requires BOTH the
run-count induction hypothesis and the independently conserved
top-run length. -/
theorem selectedRawCongruent_preservesConsecutiveRunCount
    (degree : Nat) {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenConsecutiveRunCount l r degree M =
      selectedContextEighteenConsecutiveRunCount l r degree L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesConsecutiveRunCount l r degree A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change selectedContextEighteenConsecutiveRunCount l r degree _ +
          (if degree ≤ selectedContextEighteenTopRunLength l r _ then 1 else 0) =
        selectedContextEighteenConsecutiveRunCount l r degree _ +
          (if degree ≤ selectedContextEighteenTopRunLength l r _ then 1 else 0)
      rw [ih, selectedRawCongruent_preservesTopRunLength l r A]
  | rawChainRight A X ih =>
      exact congrArg
        (fun k : Nat => k +
          selectedContextEighteenConsecutiveRunCount l r degree X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun k : Nat =>
          selectedContextEighteenConsecutiveRunCount l r degree X + k) ih

/-- Genuine Quotient.lift, for every degree, on the independently
defined seven-generator new raw-congruence presentation. -/
def selectedRawCongruentRunCountOnQuotient
    (degree : Nat) (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenConsecutiveRunCount l r degree) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesConsecutiveRunCount l r degree A)

theorem selectedRawCongruentRunCount_onClass
    (degree : Nat) (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentRunCountOnQuotient l r degree J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenConsecutiveRunCount l r degree M := rfl

/-- Independent old selected19 quotient descent of the SAME
original 18D invariant. Do not identify the two quotient types. -/
def selectedNineteenRunCountOnQuotient
    (degree : Nat) (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenConsecutiveRunCount l r degree) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesConsecutiveRunCount l r degree A)

theorem selectedConsecutiveRun_factorsOld
    (degree : Nat) (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentRunCountOnQuotient l r degree J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenRunCountOnQuotient l r degree J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- Top-run length detects EXACTLY the independently existing raw
top-reverse flag. No extra comparison constructor is postulated. -/
theorem selectedConsecutiveRun_degreeOneTopFlag
    (M : SelectedContextualEighteen W l r J N) :
    (if 1 ≤ selectedContextEighteenTopRunLength l r M then 1 else 0) =
      selectedContextEighteenTopReverseFlag l r M := by
  cases M <;>
    simp [selectedContextEighteenTopRunLength,
      selectedContextEighteenTopReverseFlag, selectedContextEighteenTopTag]

/-- Degree one of the new recursive count is precisely the EXISTING
certified direct-adjacency invariant, on every original raw18D value. -/
theorem selectedConsecutiveRun_degreeOne_eqAdjacent
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenConsecutiveRunCount l r 1 M =
      selectedContextEighteenAdjacentReverseCount l r M := by
  induction M with
  | inherited A => rfl
  | whiskerLeft before F G A ih => exact ih
  | whiskerRight F G A after ih => exact ih
  | strict J => rfl
  | reverse A ih =>
      change selectedContextEighteenConsecutiveRunCount l r 1 A +
          (if 1 ≤ selectedContextEighteenTopRunLength l r A then 1 else 0) =
        selectedContextEighteenAdjacentReverseCount l r A +
          selectedContextEighteenTopReverseFlag l r A
      rw [ih, selectedConsecutiveRun_degreeOneTopFlag l r A]
  | chain A B ih ih' =>
      change selectedContextEighteenConsecutiveRunCount l r 1 A +
          selectedContextEighteenConsecutiveRunCount l r 1 B =
        selectedContextEighteenAdjacentReverseCount l r A +
          selectedContextEighteenAdjacentReverseCount l r B
      rw [ih, ih']

/-- Iterate the ACTUAL raw-reverse constructor on the ORIGINAL
dependent endomorphism fiber, without quotienting the source. -/
def selectedUniformRunReverseIter
    (N : SelectedContextualSeventeen W l r H K) (p : Nat)
    (A : SelectedContextualEighteen W l r N N) :
    SelectedContextualEighteen W l r N N :=
  Nat.rec A (fun _ B => .reverse B) p

theorem selectedUniformRunReverseIter_topLength
    (N : SelectedContextualSeventeen W l r H K)
    (p : Nat) (A : SelectedContextualEighteen W l r N N) :
    selectedContextEighteenTopRunLength l r
        (selectedUniformRunReverseIter l r N p A) =
      selectedContextEighteenTopRunLength l r A + p := by
  induction p with
  | zero => rfl
  | succ p ih =>
      change Nat.succ
          (selectedContextEighteenTopRunLength l r
            (selectedUniformRunReverseIter l r N p A)) =
        selectedContextEighteenTopRunLength l r A + (p + 1)
      rw [ih]
      omega

/-- Count of (degree+1)-runs in p raw reverses over any original
endomorphism A whose top is not a raw reverse. -/
theorem selectedUniformRunReverseIter_count
    (N : SelectedContextualSeventeen W l r H K)
    (A : SelectedContextualEighteen W l r N N)
    (htop : selectedContextEighteenTopRunLength l r A = 0)
    (p degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunReverseIter l r N p A) =
      selectedContextEighteenConsecutiveRunCount l r degree A +
        (p - degree) := by
  induction p with
  | zero =>
      change selectedContextEighteenConsecutiveRunCount l r degree A =
        selectedContextEighteenConsecutiveRunCount l r degree A + (0 - degree)
      simp
  | succ p ih =>
      change selectedContextEighteenConsecutiveRunCount l r degree
          (selectedUniformRunReverseIter l r N p A) +
          (if degree ≤ selectedContextEighteenTopRunLength l r
            (selectedUniformRunReverseIter l r N p A) then 1 else 0) =
        selectedContextEighteenConsecutiveRunCount l r degree A +
          ((p + 1) - degree)
      rw [ih, selectedUniformRunReverseIter_topLength l r N p A, htop]
      simp only [Nat.zero_add]
      split_ifs <;> omega

theorem selectedUniformRunReverseIter_trace
    (N : SelectedContextualSeventeen W l r H K)
    (p : Nat) (A : SelectedContextualEighteen W l r N N) :
    selectedContextEighteenTrace l r (selectedUniformRunReverseIter l r N p A) =
      selectedContextEighteenTrace l r A := by
  induction p with
  | zero => rfl
  | succ p ih =>
      change selectedContextEighteenTrace l r
          (selectedUniformRunReverseIter l r N p A) =
        selectedContextEighteenTrace l r A
      exact ih

/-- Raw-reversal iteration composes without a loss of the original
dependent Type value. Reversals are accumulated in one Nat index. -/
theorem selectedUniformRunReverseIter_iter
    (N : SelectedContextualSeventeen W l r H K)
    (p q : Nat) (A : SelectedContextualEighteen W l r N N) :
    selectedUniformRunReverseIter l r N p
        (selectedUniformRunReverseIter l r N q A) =
      selectedUniformRunReverseIter l r N (q + p) A := by
  induction p with
  | zero => rfl
  | succ p ih =>
      change SelectedContextualEighteen.reverse
          (selectedUniformRunReverseIter l r N p
            (selectedUniformRunReverseIter l r N q A)) =
        SelectedContextualEighteen.reverse
          (selectedUniformRunReverseIter l r N (q + p) A)
      rw [ih]

/-- Equality of ALL tower degrees is respected by every finite number
of genuine raw reversals. The induction hypothesis is pointwise for
all degrees, not merely the specific degree being inspected. -/
theorem selectedUniformRunReverseIter_preservesTower
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : ∀ degree : Nat, selectedAncestorTowerCount l r degree A =
      selectedAncestorTowerCount l r degree B) :
    ∀ p degree : Nat,
      selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N p A) =
        selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N p B) := by
  intro p
  induction p with
  | zero =>
      intro degree
      exact h degree
  | succ p ih =>
      intro degree
      exact selectedFullTowerAdjacency_reverseTowerEq l r N
        (selectedUniformRunReverseIter l r N p A)
        (selectedUniformRunReverseIter l r N p B) ih degree

/-- The concrete original strict-chain gap does not change a tower
coordinate and has no outermost reverse. -/
theorem selectedUniformRunGap_trace
    (N : SelectedContextualSeventeen W l r H K)
    (A : SelectedContextualEighteen W l r N N) :
    selectedContextEighteenTrace l r
        (selectedConsecutiveTripleWitnessGap l r N A) =
      selectedContextEighteenTrace l r A := by
  change selectedContextEighteenTrace l r A ++ [] =
    selectedContextEighteenTrace l r A
  exact List.append_nil _

/-- For each n, reverse-run lengths [n+4,n+2] with a strict-chain gap. -/
def selectedUniformRunWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    SelectedContextualEighteen W l r N N :=
  selectedUniformRunReverseIter l r N (n + 4)
    (selectedConsecutiveTripleWitnessGap l r N
      (selectedUniformRunReverseIter l r N (n + 2) (.strict N)))

/-- For the same n, reverse-run lengths [n+3,n+3].
These are actual raw18D values in exactly the same dependent fiber. -/
def selectedUniformRunWitnessRight
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    SelectedContextualEighteen W l r N N :=
  selectedUniformRunReverseIter l r N (n + 3)
    (selectedConsecutiveTripleWitnessGap l r N
      (selectedUniformRunReverseIter l r N (n + 3) (.strict N)))

/-- The left raw run count is the SUM of two genuine reverse blocks.
The gap contributes no new adjacent run across the chain. -/
theorem selectedUniformRunWitness_leftCount
    (N : SelectedContextualSeventeen W l r H K)
    (n degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessLeft l r N n) =
      (n + 4 - degree) + (n + 2 - degree) := by
  calc
    _ = selectedContextEighteenConsecutiveRunCount l r degree
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N (n + 2) (.strict N))) +
          (n + 4 - degree) :=
        selectedUniformRunReverseIter_count l r N _ (by rfl) (n + 4) degree
    _ = (selectedContextEighteenConsecutiveRunCount l r degree
          (selectedUniformRunReverseIter l r N (n + 2) (.strict N)) + 0) +
          (n + 4 - degree) := rfl
    _ = ((0 + (n + 2 - degree)) + 0) + (n + 4 - degree) := by
        rw [selectedUniformRunReverseIter_count l r N (.strict N)
          (by rfl) (n + 2) degree]
        rfl
    _ = (n + 4 - degree) + (n + 2 - degree) := by omega

theorem selectedUniformRunWitness_rightCount
    (N : SelectedContextualSeventeen W l r H K)
    (n degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessRight l r N n) =
      (n + 3 - degree) + (n + 3 - degree) := by
  calc
    _ = selectedContextEighteenConsecutiveRunCount l r degree
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N (n + 3) (.strict N))) +
          (n + 3 - degree) :=
        selectedUniformRunReverseIter_count l r N _ (by rfl) (n + 3) degree
    _ = (selectedContextEighteenConsecutiveRunCount l r degree
          (selectedUniformRunReverseIter l r N (n + 3) (.strict N)) + 0) +
          (n + 3 - degree) := rfl
    _ = ((0 + (n + 3 - degree)) + 0) + (n + 3 - degree) := by
        rw [selectedUniformRunReverseIter_count l r N (.strict N)
          (by rfl) (n + 3) degree]
        rfl
    _ = (n + 3 - degree) + (n + 3 - degree) := by omega

/-- All shorter consecutive-run counts, including the v5.53
adjacency (degree=1), v5.66 triple (2), and v5.67 quadruple (3)
when included in the finite prefix, coincide pointwise. -/
theorem selectedUniformRunWitness_shortCountEq
    (N : SelectedContextualSeventeen W l r H K)
    (n degree : Nat) (hd : degree ≤ n + 2) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessLeft l r N n) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessRight l r N n) := by
  rw [selectedUniformRunWitness_leftCount l r N n degree,
    selectedUniformRunWitness_rightCount l r N n degree]
  omega

/-- The FIRST new run count differs by exactly one, for EVERY n.
No estimate or asymptotic argument is used. -/
theorem selectedUniformRunWitness_nextCountGap
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedContextEighteenConsecutiveRunCount l r (n + 3)
        (selectedUniformRunWitnessLeft l r N n) =
      selectedContextEighteenConsecutiveRunCount l r (n + 3)
        (selectedUniformRunWitnessRight l r N n) + 1 := by
  rw [selectedUniformRunWitness_leftCount l r N n (n + 3),
    selectedUniformRunWitness_rightCount l r N n (n + 3)]
  omega

/-- The two actual raw terms have identical FULL infinite ancestor
towers. Inserting the strict gap and moving it through reversals is
invisible to every ancestor C_degree, while the exact raw Type values
remain different. -/
theorem selectedUniformRunWitness_allTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (n degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedUniformRunWitnessLeft l r N n) =
      selectedAncestorTowerCount l r degree
        (selectedUniformRunWitnessRight l r N n) := by
  let S : SelectedContextualEighteen W l r N N := .strict N
  have hleft : ∀ d : Nat,
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N (n + 4)
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N (n + 2) S))) =
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N (n + 4)
          (selectedUniformRunReverseIter l r N (n + 2) S)) :=
    selectedUniformRunReverseIter_preservesTower l r N _ _
      (selectedConsecutiveTripleWitness_gapTowerEq l r N
        (selectedUniformRunReverseIter l r N (n + 2) S)) (n + 4)
  have hright : ∀ d : Nat,
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N (n + 3)
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N (n + 3) S))) =
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N (n + 3)
          (selectedUniformRunReverseIter l r N (n + 3) S)) :=
    selectedUniformRunReverseIter_preservesTower l r N _ _
      (selectedConsecutiveTripleWitness_gapTowerEq l r N
        (selectedUniformRunReverseIter l r N (n + 3) S)) (n + 3)
  calc
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N (n + 4)
            (selectedUniformRunReverseIter l r N (n + 2) S)) :=
      hleft degree
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N ((n + 2) + (n + 4)) S) := by
      rw [selectedUniformRunReverseIter_iter l r N (n + 4) (n + 2) S]
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N ((n + 3) + (n + 3)) S) := by
      have hlen : (n + 2) + (n + 4) = (n + 3) + (n + 3) := by omega
      rw [hlen]
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N (n + 3)
            (selectedUniformRunReverseIter l r N (n + 3) S)) := by
      rw [selectedUniformRunReverseIter_iter l r N (n + 3) (n + 3) S]
    _ = _ := (hright degree).symm

theorem selectedUniformRunWitness_traceEmptyLeft
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedContextEighteenTrace l r
      (selectedUniformRunWitnessLeft l r N n) = [] := by
  calc
    _ = selectedContextEighteenTrace l r
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N (n + 2) (.strict N))) :=
      selectedUniformRunReverseIter_trace l r N (n + 4) _
    _ = selectedContextEighteenTrace l r
          (selectedUniformRunReverseIter l r N (n + 2) (.strict N)) :=
      selectedUniformRunGap_trace l r N _
    _ = [] := by
      exact selectedUniformRunReverseIter_trace l r N (n + 2) (.strict N)

theorem selectedUniformRunWitness_traceEmptyRight
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedContextEighteenTrace l r
      (selectedUniformRunWitnessRight l r N n) = [] := by
  calc
    _ = selectedContextEighteenTrace l r
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N (n + 3) (.strict N))) :=
      selectedUniformRunReverseIter_trace l r N (n + 3) _
    _ = selectedContextEighteenTrace l r
          (selectedUniformRunReverseIter l r N (n + 3) (.strict N)) :=
      selectedUniformRunGap_trace l r N _
    _ = [] :=
      selectedUniformRunReverseIter_trace l r N (n + 3) (.strict N)

theorem selectedUniformRunWitness_traceEq
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedContextEighteenTrace l r (selectedUniformRunWitnessLeft l r N n) =
      selectedContextEighteenTrace l r (selectedUniformRunWitnessRight l r N n) :=
  (selectedUniformRunWitness_traceEmptyLeft l r N n).trans
    (selectedUniformRunWitness_traceEmptyRight l r N n).symm

/-- Both outer raw constructors are reverse, independently of n. -/
theorem selectedUniformRunWitness_topEq
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedContextEighteenTopReverseFlag l r
        (selectedUniformRunWitnessLeft l r N n) =
      selectedContextEighteenTopReverseFlag l r
        (selectedUniformRunWitnessRight l r N n) := by
  rfl

/-- Degree one equals the independently certified AdjacentReverseCount,
hence the old adjacency observation is identical for this pair. -/
theorem selectedUniformRunWitness_adjacentEq
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedUniformRunWitnessLeft l r N n) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedUniformRunWitnessRight l r N n) := by
  rw [← selectedConsecutiveRun_degreeOne_eqAdjacent l r
      (selectedUniformRunWitnessLeft l r N n),
    ← selectedConsecutiveRun_degreeOne_eqAdjacent l r
      (selectedUniformRunWitnessRight l r N n)]
  exact selectedUniformRunWitness_shortCountEq l r N n 1 (by omega)

/-- All EIGHT established raw observation coordinates agree, using
the true previous v5.60 bridges from tower C1..C5 to the original
source counts, and the new adjacency bridge. -/
theorem selectedUniformRunWitness_eightSignature
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedRawEightSignature l r
      (selectedUniformRunWitnessLeft l r N n)
      (selectedUniformRunWitnessRight l r N n) := by
  let X : SelectedContextualEighteen W l r N N :=
    selectedUniformRunWitnessLeft l r N n
  let Y : SelectedContextualEighteen W l r N N :=
    selectedUniformRunWitnessRight l r N n
  have hT : ∀ k : Nat,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y :=
    selectedUniformRunWitness_allTowerEq l r N n
  refine ⟨selectedUniformRunWitness_traceEq l r N n,
    ?_, selectedUniformRunWitness_adjacentEq l r N n,
    selectedUniformRunWitness_topEq l r N n, ?_, ?_, ?_, ?_⟩
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

/-- The true new seven-generator quotient classes are distinguishable
by the next, independently conserved run count (degree n+3). -/
theorem selectedUniformRunWitness_classDistinct
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedRawCongruentClass l r (selectedUniformRunWitnessLeft l r N n) ≠
      selectedRawCongruentClass l r (selectedUniformRunWitnessRight l r N n) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentRunCountOnQuotient l r (n + 3) N N) h
  change selectedContextEighteenConsecutiveRunCount l r (n + 3)
      (selectedUniformRunWitnessLeft l r N n) =
    selectedContextEighteenConsecutiveRunCount l r (n + 3)
      (selectedUniformRunWitnessRight l r N n) at hc
  rw [selectedUniformRunWitness_nextCountGap l r N n] at hc
  omega

theorem selectedUniformRunWitness_noComparison
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedUniformRunWitnessLeft l r N n)
      (selectedUniformRunWitnessRight l r N n)) := by
  rintro ⟨A⟩
  exact (selectedUniformRunWitness_classDistinct l r N n)
    (Quotient.sound ⟨A⟩)

/-- Right-compose the pair into only an ACTUALLY supplied original
M:J→N exact dependent fiber. -/
def selectedUniformRunWitnessFiberLeft
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedUniformRunWitnessLeft l r N n)

def selectedUniformRunWitnessFiberRight
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedUniformRunWitnessRight l r N n)

theorem selectedUniformRunWitnessFiber_allTowerEq
    (M : SelectedContextualEighteen W l r J N)
    (n degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedUniformRunWitnessFiberLeft l r M n) =
      selectedAncestorTowerCount l r degree
        (selectedUniformRunWitnessFiberRight l r M n) := by
  cases degree with
  | zero => rfl
  | succ degree =>
      change selectedAncestorTowerCount l r (degree + 1) M +
          selectedAncestorTowerCount l r (degree + 1)
            (selectedUniformRunWitnessLeft l r N n) =
        selectedAncestorTowerCount l r (degree + 1) M +
          selectedAncestorTowerCount l r (degree + 1)
            (selectedUniformRunWitnessRight l r N n)
      exact congrArg
        (fun t : Nat => selectedAncestorTowerCount l r (degree + 1) M + t)
        (selectedUniformRunWitness_allTowerEq l r N n (degree + 1))

theorem selectedUniformRunWitnessFiber_eightSignature
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedRawEightSignature l r
      (selectedUniformRunWitnessFiberLeft l r M n)
      (selectedUniformRunWitnessFiberRight l r M n) :=
  selectedRawEightSignature_rightChain l r M
    (selectedUniformRunWitnessLeft l r N n)
    (selectedUniformRunWitnessRight l r N n)
    (selectedUniformRunWitness_eightSignature l r N n)

theorem selectedUniformRunWitnessFiber_shortCountEq
    (M : SelectedContextualEighteen W l r J N)
    (n degree : Nat) (hd : degree ≤ n + 2) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessFiberLeft l r M n) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessFiberRight l r M n) := by
  change selectedContextEighteenConsecutiveRunCount l r degree M +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessLeft l r N n) =
    selectedContextEighteenConsecutiveRunCount l r degree M +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedUniformRunWitnessRight l r N n)
  exact congrArg
    (fun t : Nat => selectedContextEighteenConsecutiveRunCount l r degree M + t)
    (selectedUniformRunWitness_shortCountEq l r N n degree hd)

theorem selectedUniformRunWitnessFiber_nextCountGap
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedContextEighteenConsecutiveRunCount l r (n + 3)
        (selectedUniformRunWitnessFiberLeft l r M n) =
      selectedContextEighteenConsecutiveRunCount l r (n + 3)
        (selectedUniformRunWitnessFiberRight l r M n) + 1 := by
  change selectedContextEighteenConsecutiveRunCount l r (n + 3) M +
      selectedContextEighteenConsecutiveRunCount l r (n + 3)
        (selectedUniformRunWitnessLeft l r N n) =
    (selectedContextEighteenConsecutiveRunCount l r (n + 3) M +
      selectedContextEighteenConsecutiveRunCount l r (n + 3)
        (selectedUniformRunWitnessRight l r N n)) + 1
  rw [selectedUniformRunWitness_nextCountGap l r N n]

theorem selectedUniformRunWitnessFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedRawCongruentClass l r (selectedUniformRunWitnessFiberLeft l r M n) ≠
      selectedRawCongruentClass l r (selectedUniformRunWitnessFiberRight l r M n) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentRunCountOnQuotient l r (n + 3) J N) h
  change selectedContextEighteenConsecutiveRunCount l r (n + 3)
      (selectedUniformRunWitnessFiberLeft l r M n) =
    selectedContextEighteenConsecutiveRunCount l r (n + 3)
      (selectedUniformRunWitnessFiberRight l r M n) at hc
  rw [selectedUniformRunWitnessFiber_nextCountGap l r M n] at hc
  omega

/-- True new quotient observation: all NINE existing measurements,
the FULL Nat→Nat ancestor tower, and each independently descended
run count of length one through n+3 (Fin(n+3)). These additional
statistics are finite but their number is arbitrarily large. -/
def selectedRawCongruentUniformRunObservation
    (n : Nat) (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (selectedRawNineObservationValue × (Nat → Nat)) × (Fin (n + 3) → Nat) :=
  fun q => (selectedRawCongruentNineFullTowerObservation l r J N q,
    fun i => selectedRawCongruentRunCountOnQuotient l r i.val J N q)

/-- Explicit genuine quotient collision in the exact supplied fiber.
This uses all Nat tower degrees and all shorter reverse-run lengths,
rather than any finite sampled tower prefix. -/
theorem selectedUniformRunWitnessFiber_observationEq
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedRawCongruentUniformRunObservation l r n J N
        (selectedRawCongruentClass l r (selectedUniformRunWitnessFiberLeft l r M n)) =
      selectedRawCongruentUniformRunObservation l r n J N
        (selectedRawCongruentClass l r (selectedUniformRunWitnessFiberRight l r M n)) := by
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact selectedRawEightSignature_toObservation l r
          (selectedUniformRunWitnessFiberLeft l r M n)
          (selectedUniformRunWitnessFiberRight l r M n)
          (selectedUniformRunWitnessFiber_eightSignature l r M n)
      · change selectedAncestorTowerCount l r 6
            (selectedUniformRunWitnessFiberLeft l r M n) =
          selectedAncestorTowerCount l r 6
            (selectedUniformRunWitnessFiberRight l r M n)
        exact selectedUniformRunWitnessFiber_allTowerEq l r M n 6
    · funext degree
      change selectedAncestorTowerCount l r degree
          (selectedUniformRunWitnessFiberLeft l r M n) =
        selectedAncestorTowerCount l r degree
          (selectedUniformRunWitnessFiberRight l r M n)
      exact selectedUniformRunWitnessFiber_allTowerEq l r M n degree
  · funext i
    change selectedContextEighteenConsecutiveRunCount l r i.val
        (selectedUniformRunWitnessFiberLeft l r M n) =
      selectedContextEighteenConsecutiveRunCount l r i.val
        (selectedUniformRunWitnessFiberRight l r M n)
    exact selectedUniformRunWitnessFiber_shortCountEq l r M n i.val (by omega)

/-- Noninjectivity and decoder obstructions are stated only for
genuinely inhabited exact original fibers. -/
theorem selectedRawCongruentUniformRun_notInjective
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    ¬ Function.Injective
        (selectedRawCongruentUniformRunObservation l r n J N) := by
  intro hinj
  exact (selectedUniformRunWitnessFiber_classDistinct l r M n)
    (hinj (selectedUniformRunWitnessFiber_observationEq l r M n))

theorem selectedRawCongruentUniformRun_noNextDecoder
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    ¬ ∃ decode :
        ((selectedRawNineObservationValue × (Nat → Nat)) ×
          (Fin (n + 3) → Nat)) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentUniformRunObservation l r n J N q) =
          selectedRawCongruentRunCountOnQuotient l r (n + 3) J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentRunCountOnQuotient l r (n + 3) J N
          (selectedRawCongruentClass l r
            (selectedUniformRunWitnessFiberLeft l r M n)) =
        selectedRawCongruentRunCountOnQuotient l r (n + 3) J N
          (selectedRawCongruentClass l r
            (selectedUniformRunWitnessFiberRight l r M n)) := by
    calc
      _ = decode (selectedRawCongruentUniformRunObservation l r n J N
          (selectedRawCongruentClass l r
            (selectedUniformRunWitnessFiberLeft l r M n))) := (h _).symm
      _ = decode (selectedRawCongruentUniformRunObservation l r n J N
          (selectedRawCongruentClass l r
            (selectedUniformRunWitnessFiberRight l r M n))) :=
          congrArg decode (selectedUniformRunWitnessFiber_observationEq l r M n)
      _ = _ := h _
  change selectedContextEighteenConsecutiveRunCount l r (n + 3)
      (selectedUniformRunWitnessFiberLeft l r M n) =
    selectedContextEighteenConsecutiveRunCount l r (n + 3)
      (selectedUniformRunWitnessFiberRight l r M n) at hc
  rw [selectedUniformRunWitnessFiber_nextCountGap l r M n] at hc
  omega

theorem selectedRawCongruentUniformRun_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    ¬ ∃ decode :
        ((selectedRawNineObservationValue × (Nat → Nat)) ×
          (Fin (n + 3) → Nat)) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentUniformRunObservation l r n J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentUniformRun_notInjective l r M n
  intro a b hab
  calc
    a = decode (selectedRawCongruentUniformRunObservation l r n J N a) := (h a).symm
    _ = decode (selectedRawCongruentUniformRunObservation l r n J N b) :=
      congrArg decode hab
    _ = b := h b

theorem selectedRawCongruentUniformRun_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) (n : Nat) :
    ¬ Function.Injective (selectedRawCongruentUniformRunObservation l r n J J) :=
  selectedRawCongruentUniformRun_notInjective l r (.strict J) n

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTopRunLength
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenConsecutiveRunCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesTopRunLength
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesTopRunLength
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesConsecutiveRunCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesConsecutiveRunCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentRunCountOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentRunCount_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenRunCountOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedConsecutiveRun_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedConsecutiveRun_degreeOneTopFlag
#print axioms PentagonAdjoinedSixCell.selectedConsecutiveRun_degreeOne_eqAdjacent
#print axioms PentagonAdjoinedSixCell.selectedUniformRunReverseIter
#print axioms PentagonAdjoinedSixCell.selectedUniformRunReverseIter_topLength
#print axioms PentagonAdjoinedSixCell.selectedUniformRunReverseIter_count
#print axioms PentagonAdjoinedSixCell.selectedUniformRunReverseIter_trace
#print axioms PentagonAdjoinedSixCell.selectedUniformRunReverseIter_iter
#print axioms PentagonAdjoinedSixCell.selectedUniformRunReverseIter_preservesTower
#print axioms PentagonAdjoinedSixCell.selectedUniformRunGap_trace
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_leftCount
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_rightCount
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_shortCountEq
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_nextCountGap
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_traceEmptyLeft
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_traceEmptyRight
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_traceEq
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_topEq
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_adjacentEq
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitness_noComparison
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiberRight
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiber_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiber_shortCountEq
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiber_nextCountGap
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentUniformRunObservation
#print axioms PentagonAdjoinedSixCell.selectedUniformRunWitnessFiber_observationEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentUniformRun_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentUniformRun_noNextDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentUniformRun_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentUniformRun_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
