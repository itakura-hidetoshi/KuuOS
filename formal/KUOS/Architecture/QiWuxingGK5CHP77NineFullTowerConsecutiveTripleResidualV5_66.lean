import KUOS.Architecture.QiWuxingGK5CHP77FullAncestorTowerAdjacencyIndependenceV5_65

/-!
Qi v5.66 — a THIRD consecutive reverse is an independent invariant
of the original 18D raw evidence and the actual seven-generator new
comparison, even after combining ALL NINE existing quotient
observables with the full Nat-indexed ancestor tower.

Do not reuse the v5.65 witness: its adjacency differs. Instead
construct two genuine N→N raw terms with the same four reverse-depth
ancestors, exactly two adjacent reverse edges each, the same top
reverse flag and complete ordered trace, but a different arrangement:
the left contains one run of THREE directly consecutive reverses,
the right has two disjoint runs of TWO. Their full C_n counts agree
for EVERY n. A new, explicit consecutive triple count is proved
invariant under all original 5 and new 7 comparison constructors,
and independently descends to the actual new quotient.

The resulting pair is a true counterexample to injectivity of the
ACTUAL existing nine-observer JOINED with the ENTIRE infinite ancestor
tower; its full-quotient decoder and triple-count decoder do not exist
in any original J→N fiber carrying one supplied real raw18D witness.
Endomorphism fibers J→J have actual strict witness.

This theorem does NOT classify the new quotient after adding the
triple count, postulate inhabitance of arbitrary heterogeneous fibers,
perform 20D gluing, or confer institutional authority.
Keep all old Type values, 7-generator comparison, pins, root107,
validation-only #1558 and existing imports unchanged.
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

/-- Two immediate raw reverses at the top; not merely two reverse
ancestors separated by a chain. The flag remains 0 under unit
insertion because inherited/chain outer constructors are non-reverse. -/
def selectedContextEighteenTopDoubleReverseFlag (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .reverse L => selectedContextEighteenTopReverseFlag l r L
  | _ => 0

/-- Truly consecutive triple-reverse count in the ORIGINAL
dependent Type: reverse adds one iff the child starts with TWO
immediate reverses; chain adds histories, and contextual whiskering
preserves the inner count. -/
def selectedContextEighteenConsecutiveTripleCount (l r : W)
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
      selectedContextEighteenConsecutiveTripleCount l r M
  | .whiskerRight _ _ M _ =>
      selectedContextEighteenConsecutiveTripleCount l r M
  | .strict _ => 0
  | .reverse M =>
      selectedContextEighteenConsecutiveTripleCount l r M +
        selectedContextEighteenTopDoubleReverseFlag l r M
  | .chain M L =>
      selectedContextEighteenConsecutiveTripleCount l r M +
        selectedContextEighteenConsecutiveTripleCount l r L

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- All FIVE ORIGINAL selected19 comparison constructors preserve
the double-top flag. The unit rules change only non-reverse tops. -/
theorem selectedLocalNineteen_preservesTopDoubleReverseFlag
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenTopDoubleReverseFlag l r M =
      selectedContextEighteenTopDoubleReverseFlag l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- The double-top flag preserves ALL SEVEN new congruence
constructors. Raw reversal reduces exactly to the previously
CERTIFIED top-reverse flag of the input proof. -/
theorem selectedRawCongruent_preservesTopDoubleReverseFlag
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenTopDoubleReverseFlag l r M =
      selectedContextEighteenTopDoubleReverseFlag l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesTopDoubleReverseFlag l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change selectedContextEighteenTopReverseFlag l r _ =
        selectedContextEighteenTopReverseFlag l r _
      exact selectedRawCongruent_preservesTopReverseFlag l r A
  | rawChainRight A X ih => rfl
  | rawChainLeft X A ih => rfl

/-- Triple-consecutive count also survives all FIVE original
selected19 proof comparisons without changing the underlying Type. -/
theorem selectedLocalNineteen_preservesConsecutiveTripleCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenConsecutiveTripleCount l r M =
      selectedContextEighteenConsecutiveTripleCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- The new seven-generator quotient retains the truly consecutive
triple count. RawReverse closure needs BOTH the triple-count
induction hypothesis and the separately certified top-double flag. -/
theorem selectedRawCongruent_preservesConsecutiveTripleCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenConsecutiveTripleCount l r M =
      selectedContextEighteenConsecutiveTripleCount l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesConsecutiveTripleCount l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change selectedContextEighteenConsecutiveTripleCount l r _ +
          selectedContextEighteenTopDoubleReverseFlag l r _ =
        selectedContextEighteenConsecutiveTripleCount l r _ +
          selectedContextEighteenTopDoubleReverseFlag l r _
      exact congrArg₂ Nat.add ih
        (selectedRawCongruent_preservesTopDoubleReverseFlag l r A)
  | rawChainRight A X ih =>
      exact congrArg
        (fun k : Nat => k +
          selectedContextEighteenConsecutiveTripleCount l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun k : Nat =>
          selectedContextEighteenConsecutiveTripleCount l r X + k) ih

/-- Independent, genuine Quotient.lift of the new invariant through
the actual seven-constructor comparison, not an assumed descent. -/
def selectedRawCongruentConsecutiveTripleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenConsecutiveTripleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesConsecutiveTripleCount l r A)

theorem selectedRawCongruentConsecutiveTriple_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentConsecutiveTripleOnQuotient l r J N
      (selectedRawCongruentClass l r M) =
        selectedContextEighteenConsecutiveTripleCount l r M := rfl

/-- On ORIGINAL selected19, the new invariant also descends
independently and factors through the old-to-new projection. -/
def selectedNineteenConsecutiveTripleOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenConsecutiveTripleCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesConsecutiveTripleCount l r A)

theorem selectedConsecutiveTriple_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentConsecutiveTripleOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenConsecutiveTripleOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- A genuine dependent N→N one-reversal seed. -/
def selectedTripleResidualSpine
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.strict N)

/-- A raw chain gap inserts a strict identity without altering any
ancestor tower coordinate, but it interrupts immediate reversals. -/
def selectedTripleResidualGap
    (N : SelectedContextualSeventeen W l r H K)
    (A : SelectedContextualEighteen W l r N N) :
    SelectedContextualEighteen W l r N N :=
  .chain A (.strict N)

/-- Three consecutive reversals above a gap and a final reverse. -/
def selectedTripleResidualLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.reverse (.reverse
    (selectedTripleResidualGap l r N (selectedTripleResidualSpine l r N))))

/-- Two reversals above a gap and two more reversals below it. -/
def selectedTripleResidualRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  .reverse (.reverse
    (selectedTripleResidualGap l r N
      (.reverse (selectedTripleResidualSpine l r N))))

/-- Right strict-chain contributes no positive ancestor counts,
and C0 is fixed to the same seed 1. -/
theorem selectedTripleResidual_gapTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (A : SelectedContextualEighteen W l r N N) (n : Nat) :
    selectedAncestorTowerCount l r n (selectedTripleResidualGap l r N A) =
      selectedAncestorTowerCount l r n A := by
  cases n with
  | zero => rfl
  | succ n =>
      change selectedAncestorTowerCount l r (n + 1) A + 0 =
        selectedAncestorTowerCount l r (n + 1) A
      exact Nat.add_zero _

/-- At the seed stage, moving the gap past one reverse keeps EVERY
ancestor coordinate, not just a fixed finite prefix. -/
theorem selectedTripleResidual_seedTowerEq
    (N : SelectedContextualSeventeen W l r H K) :
    ∀ n : Nat,
      selectedAncestorTowerCount l r n
          (.reverse (selectedTripleResidualGap l r N
            (selectedTripleResidualSpine l r N))) =
        selectedAncestorTowerCount l r n
          (selectedTripleResidualGap l r N
            (.reverse (selectedTripleResidualSpine l r N))) := by
  intro n
  have h1 : ∀ k : Nat,
      selectedAncestorTowerCount l r k
          (.reverse (selectedTripleResidualGap l r N
            (selectedTripleResidualSpine l r N))) =
        selectedAncestorTowerCount l r k
          (.reverse (selectedTripleResidualSpine l r N)) :=
    selectedFullTowerAdjacency_reverseTowerEq l r N
      (selectedTripleResidualGap l r N (selectedTripleResidualSpine l r N))
      (selectedTripleResidualSpine l r N)
      (selectedTripleResidual_gapTowerEq l r N
        (selectedTripleResidualSpine l r N))
  exact (h1 n).trans
    (selectedTripleResidual_gapTowerEq l r N
      (.reverse (selectedTripleResidualSpine l r N)) n).symm

/-- Both genuine raw terms have an IDENTICAL FULL infinite
ancestor tower, a strictly stronger premise than any finite sample. -/
theorem selectedTripleResidual_allTowerEq
    (N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedAncestorTowerCount l r n (selectedTripleResidualLeft l r N) =
      selectedAncestorTowerCount l r n (selectedTripleResidualRight l r N) := by
  have h1 : ∀ k : Nat,
      selectedAncestorTowerCount l r k
          (.reverse (.reverse (selectedTripleResidualGap l r N
            (selectedTripleResidualSpine l r N)))) =
        selectedAncestorTowerCount l r k
          (.reverse (selectedTripleResidualGap l r N
            (.reverse (selectedTripleResidualSpine l r N)))) :=
    selectedFullTowerAdjacency_reverseTowerEq l r N
      (.reverse (selectedTripleResidualGap l r N
        (selectedTripleResidualSpine l r N)))
      (selectedTripleResidualGap l r N
        (.reverse (selectedTripleResidualSpine l r N)))
      (selectedTripleResidual_seedTowerEq l r N)
  exact selectedFullTowerAdjacency_reverseTowerEq l r N
    (.reverse (.reverse (selectedTripleResidualGap l r N
      (selectedTripleResidualSpine l r N))))
    (.reverse (selectedTripleResidualGap l r N
      (.reverse (selectedTripleResidualSpine l r N)))) h1 n

/-- Both complete ordered raw traces are precisely empty. -/
theorem selectedTripleResidual_traceEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTrace l r (selectedTripleResidualLeft l r N) =
      selectedContextEighteenTrace l r (selectedTripleResidualRight l r N) := by
  rfl

/-- Both outer raw constructors are reverse, top reverse flags 1. -/
theorem selectedTripleResidual_topEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTopReverseFlag l r (selectedTripleResidualLeft l r N) =
      selectedContextEighteenTopReverseFlag l r (selectedTripleResidualRight l r N) := by
  rfl

/-- Even the independently quotiented adjacent count agrees: 2 vs 2.
Thus the v5.65 adjacency obstruction cannot separate THIS pair. -/
theorem selectedTripleResidual_adjacentEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedTripleResidualLeft l r N) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedTripleResidualRight l r N) := by
  rfl

/-- One directly consecutive triple on the left. -/
theorem selectedTripleResidual_leftTripleOne
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualLeft l r N) = 1 := by
  rfl

/-- No directly consecutive triple on the right. -/
theorem selectedTripleResidual_rightTripleZero
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualRight l r N) = 0 := by
  rfl

/-- A new genuine quotient comparison between these N→N loops is
impossible because an independently conserved invariant differs. -/
theorem selectedTripleResidual_classDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r (selectedTripleResidualLeft l r N) ≠
      selectedRawCongruentClass l r (selectedTripleResidualRight l r N) := by
  intro h
  have ht := congrArg
    (selectedRawCongruentConsecutiveTripleOnQuotient l r N N) h
  change selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualLeft l r N) =
    selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualRight l r N) at ht
  rw [selectedTripleResidual_leftTripleOne l r N,
    selectedTripleResidual_rightTripleZero l r N] at ht
  omega

/-- No NEW genuinely Type-valued 19D comparison can identify
the two raw histories. -/
theorem selectedTripleResidual_noComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedTripleResidualLeft l r N)
      (selectedTripleResidualRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedTripleResidual_classDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- Reuse the FIVE separately certified v5.60 bridges between
actual original count functions and the complete ancestor tower. -/
theorem selectedTripleResidual_eightSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawEightSignature l r
      (selectedTripleResidualLeft l r N)
      (selectedTripleResidualRight l r N) := by
  let X : SelectedContextualEighteen W l r N N :=
    selectedTripleResidualLeft l r N
  let Y : SelectedContextualEighteen W l r N N :=
    selectedTripleResidualRight l r N
  have hT : ∀ k : Nat,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y :=
    selectedTripleResidual_allTowerEq l r N
  refine ⟨selectedTripleResidual_traceEq l r N,
    ?_, selectedTripleResidual_adjacentEq l r N,
    selectedTripleResidual_topEq l r N, ?_, ?_, ?_, ?_⟩
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

/-- Attach both genuine N→N loops to an actual supplied M:J→N,
without postulating that any heterogeneous fiber is inhabited. -/
def selectedTripleResidualFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedTripleResidualLeft l r N)

def selectedTripleResidualFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedTripleResidualRight l r N)

/-- All natural degrees remain pointwise equal in the actual
original J→N fiber. -/
theorem selectedTripleResidualFiber_allTowerEq
    (M : SelectedContextualEighteen W l r J N) (n : Nat) :
    selectedAncestorTowerCount l r n (selectedTripleResidualFiberLeft l r M) =
      selectedAncestorTowerCount l r n (selectedTripleResidualFiberRight l r M) := by
  cases n with
  | zero => rfl
  | succ n =>
      change selectedAncestorTowerCount l r (n + 1) M +
          selectedAncestorTowerCount l r (n + 1)
            (selectedTripleResidualLeft l r N) =
        selectedAncestorTowerCount l r (n + 1) M +
          selectedAncestorTowerCount l r (n + 1)
            (selectedTripleResidualRight l r N)
      exact congrArg
        (fun t : Nat => selectedAncestorTowerCount l r (n + 1) M + t)
        (selectedTripleResidual_allTowerEq l r N (n + 1))

/-- Eight existing raw observables remain equal under a genuine
right chain (including adjacency and top), by the v5.61 theorem. -/
theorem selectedTripleResidualFiber_eightSignature
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawEightSignature l r
      (selectedTripleResidualFiberLeft l r M)
      (selectedTripleResidualFiberRight l r M) :=
  selectedRawEightSignature_rightChain l r M
    (selectedTripleResidualLeft l r N)
    (selectedTripleResidualRight l r N)
    (selectedTripleResidual_eightSignature l r N)

/-- Triple consecutive count is additive under actual raw chains:
the residual +1 survives in every supplied original J→N fiber. -/
theorem selectedTripleResidualFiber_tripleGap
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenConsecutiveTripleCount l r
        (selectedTripleResidualFiberLeft l r M) =
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedTripleResidualFiberRight l r M) + 1 := by
  change selectedContextEighteenConsecutiveTripleCount l r M +
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedTripleResidualLeft l r N) =
    (selectedContextEighteenConsecutiveTripleCount l r M +
      selectedContextEighteenConsecutiveTripleCount l r
        (selectedTripleResidualRight l r N)) + 1
  rw [selectedTripleResidual_leftTripleOne l r N,
    selectedTripleResidual_rightTripleZero l r N]
  omega

theorem selectedTripleResidualFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedTripleResidualFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedTripleResidualFiberRight l r M) := by
  intro h
  have ht := congrArg
    (selectedRawCongruentConsecutiveTripleOnQuotient l r J N) h
  change selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualFiberLeft l r M) =
    selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualFiberRight l r M) at ht
  rw [selectedTripleResidualFiber_tripleGap l r M] at ht
  omega

/-- The FULL existing nine-observer, now joined with ALL natural
tower degrees, on the genuine new quotient. This includes adjacency,
so the previous v5.65 pair could not be reused. -/
def selectedRawCongruentNineFullTowerObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      selectedRawNineObservationValue × (Nat → Nat) :=
  fun q => (selectedRawCongruentNineObservation l r J N q,
    selectedRawCongruentFullTowerObservation l r J N q)

/-- Real new quotient observation equality on the genuine same-fiber
pair, simultaneously for all NINE old components and ALL C_n. -/
theorem selectedTripleResidualFiber_nineFullTowerEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentNineFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedTripleResidualFiberLeft l r M)) =
      selectedRawCongruentNineFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedTripleResidualFiberRight l r M)) := by
  apply Prod.ext
  · apply Prod.ext
    · exact selectedRawEightSignature_toObservation l r
        (selectedTripleResidualFiberLeft l r M)
        (selectedTripleResidualFiberRight l r M)
        (selectedTripleResidualFiber_eightSignature l r M)
    · change selectedAncestorTowerCount l r 6
          (selectedTripleResidualFiberLeft l r M) =
        selectedAncestorTowerCount l r 6
          (selectedTripleResidualFiberRight l r M)
      exact selectedTripleResidualFiber_allTowerEq l r M 6
  · funext n
    change selectedAncestorTowerCount l r n
        (selectedTripleResidualFiberLeft l r M) =
      selectedAncestorTowerCount l r n
        (selectedTripleResidualFiberRight l r M)
    exact selectedTripleResidualFiber_allTowerEq l r M n

/-- The nine-observer augmented by the ENTIRE infinite tower is
still noninjective, in each genuine inhabited exact original fiber. -/
theorem selectedRawCongruentNineFullTower_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentNineFullTowerObservation l r J N) := by
  intro hinj
  exact (selectedTripleResidualFiber_classDistinct l r M)
    (hinj (selectedTripleResidualFiber_nineFullTowerEq l r M))

/-- Even the combined observation cannot recover the independently
certified consecutive triple invariant, on all new quotient classes
of an actually supplied exact original 17D fiber. -/
theorem selectedRawCongruentNineFullTower_noTripleDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode : (selectedRawNineObservationValue × (Nat → Nat)) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentNineFullTowerObservation l r J N q) =
          selectedRawCongruentConsecutiveTripleOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have ht :
      selectedRawCongruentConsecutiveTripleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedTripleResidualFiberLeft l r M)) =
        selectedRawCongruentConsecutiveTripleOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedTripleResidualFiberRight l r M)) := by
    calc
      _ = decode (selectedRawCongruentNineFullTowerObservation l r J N
            (selectedRawCongruentClass l r (selectedTripleResidualFiberLeft l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentNineFullTowerObservation l r J N
            (selectedRawCongruentClass l r (selectedTripleResidualFiberRight l r M))) :=
        congrArg decode (selectedTripleResidualFiber_nineFullTowerEq l r M)
      _ = _ := h _
  change selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualFiberLeft l r M) =
    selectedContextEighteenConsecutiveTripleCount l r
      (selectedTripleResidualFiberRight l r M) at ht
  rw [selectedTripleResidualFiber_tripleGap l r M] at ht
  omega

theorem selectedRawCongruentNineFullTower_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        (selectedRawNineObservationValue × (Nat → Nat)) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentNineFullTowerObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentNineFullTower_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentNineFullTowerObservation l r J N a) := (h a).symm
    _ = decode (selectedRawCongruentNineFullTowerObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- The strict original J→J raw evidence provides this genuine
collision in EVERY specified endomorphism fiber. -/
theorem selectedRawCongruentNineFullTower_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective (selectedRawCongruentNineFullTowerObservation l r J J) :=
  selectedRawCongruentNineFullTower_notInjective l r
    (SelectedContextualEighteen.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTopDoubleReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenConsecutiveTripleCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesTopDoubleReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesTopDoubleReverseFlag
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesConsecutiveTripleCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesConsecutiveTripleCount
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentConsecutiveTripleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentConsecutiveTriple_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenConsecutiveTripleOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedConsecutiveTriple_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualSpine
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualGap
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualLeft
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualRight
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_gapTowerEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_seedTowerEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_traceEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_topEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_adjacentEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_leftTripleOne
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_rightTripleZero
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_noComparison
#print axioms PentagonAdjoinedSixCell.selectedTripleResidual_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualFiberRight
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualFiber_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualFiber_tripleGap
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTowerObservation
#print axioms PentagonAdjoinedSixCell.selectedTripleResidualFiber_nineFullTowerEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTower_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTower_noTripleDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTower_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineFullTower_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
