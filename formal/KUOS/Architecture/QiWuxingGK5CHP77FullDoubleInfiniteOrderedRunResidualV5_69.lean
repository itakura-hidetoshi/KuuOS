import KUOS.Architecture.QiWuxingGK5CHP77UniformConsecutiveRunTowerObstructionV5_68

/-!
Qi v5.69 — the COMPLETE natural-indexed ancestor tower together with
the COMPLETE natural-indexed direct consecutive-reverse-run-count tower
and all original nine observables still does NOT reconstruct the actual
new seven-generator quotient in a supplied original dependent fiber.

Witnesses use actual 18D raw strict, reverse and chain constructors:
  A = three directly consecutive reverse nodes over
      (chain (two directly consecutive reverse nodes) (strict N))
  B = two directly consecutive reverse nodes over
      (chain (three directly consecutive reverse nodes) (strict N)).
The two ordered run-length lists are [3,2] and [2,3]. All unordered
run-count histograms coincide FOR EVERY Nat degree; ALL ancestor tower
counts coincide FOR EVERY Nat degree; the original eight/nine
observations coincide, including adjacency and top reverse.

An INDEPENDENT ordered raw-run-list invariant is defined on the actual
dependent Type18D evidence and proved preserved under all FIVE original
selected19 and all SEVEN new raw-congruence comparison constructors.
It descends separately to the old/new actual quotient and factors
along the existing old→new projection. Its list inequality witnesses
genuine distinct quotient classes and nonexistence of a typed new19
comparison. The obstruction is transported by a real original
M:J→N only within the SAME exact dependent fiber, never by assuming
arbitrary heterogeneous fiber nonemptiness.

No claim concerning completeness after adding ordered run lists,
cross-WORLD gluing, 20D comparison, global authority or other
uncertified presentations.
Keep original proof Type values, old/new comparison independence,
root107, fixed Lean/mathlib pins, protected PR #1558.
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

/-- Ordered lengths of direct raw-reverse runs in the ACTUAL dependent
18D syntax. A new reverse extends the first run precisely when its
child begins with raw reverse, and starts a new run otherwise.
A chain concatenates ordered component histories. Whiskering retains
the inside history; old inherited and strict sources add no raw runs.
This is a separate presentation, NOT an identification of Type values. -/
def selectedContextEighteenOrderedRunList (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : List Nat :=
  match M with
  | .inherited _ => []
  | .whiskerLeft _ _ _ A => selectedContextEighteenOrderedRunList l r A
  | .whiskerRight _ _ A _ => selectedContextEighteenOrderedRunList l r A
  | .strict _ => []
  | .reverse A =>
      if selectedContextEighteenTopRunLength l r A = 0 then
        1 :: selectedContextEighteenOrderedRunList l r A
      else
        (selectedContextEighteenTopRunLength l r A + 1) ::
          (selectedContextEighteenOrderedRunList l r A).drop 1
  | .chain A B =>
      selectedContextEighteenOrderedRunList l r A ++
        selectedContextEighteenOrderedRunList l r B

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Verify the old FIVE constructors, not just the new quotient.
Only old unit insertions of strict/inherited Type evidence are equated. -/
theorem selectedLocalNineteen_preservesOrderedRunList
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenOrderedRunList l r M =
      selectedContextEighteenOrderedRunList l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- The order-sensitive raw-run list is preserved by ALL SEVEN new
typed comparison generators, not only the unordered counts. In the
rawReverse case both the list induction hypothesis and the already
certified independent top-run-length equality are required. -/
theorem selectedRawCongruent_preservesOrderedRunList
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedRawCongruentNineteen W l r J N M L) :
    selectedContextEighteenOrderedRunList l r M =
      selectedContextEighteenOrderedRunList l r L := by
  induction A with
  | inherited A =>
      exact selectedLocalNineteen_preservesOrderedRunList l r A
  | strict M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'
  | rawReverse A ih =>
      change
        (if selectedContextEighteenTopRunLength l r _ = 0 then
          1 :: selectedContextEighteenOrderedRunList l r _
        else
          (selectedContextEighteenTopRunLength l r _ + 1) ::
            (selectedContextEighteenOrderedRunList l r _).drop 1) =
        (if selectedContextEighteenTopRunLength l r _ = 0 then
          1 :: selectedContextEighteenOrderedRunList l r _
        else
          (selectedContextEighteenTopRunLength l r _ + 1) ::
            (selectedContextEighteenOrderedRunList l r _).drop 1)
      rw [selectedRawCongruent_preservesTopRunLength l r A, ih]
  | rawChainRight A X ih =>
      exact congrArg
        (fun xs : List Nat => xs ++ selectedContextEighteenOrderedRunList l r X) ih
  | rawChainLeft X A ih =>
      exact congrArg
        (fun xs : List Nat => selectedContextEighteenOrderedRunList l r X ++ xs) ih

/-- Genuine descent to the NEW seven-constructor selected19 quotient. -/
def selectedRawCongruentOrderedRunListOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → List Nat :=
  Quotient.lift (selectedContextEighteenOrderedRunList l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedRawCongruent_preservesOrderedRunList l r A)

theorem selectedRawCongruentOrderedRunList_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentOrderedRunListOnQuotient l r J N
        (selectedRawCongruentClass l r M) =
      selectedContextEighteenOrderedRunList l r M := rfl

/-- Independent OLD selected19 quotient descent, without conflating
the original and the new Type-valued comparison presentations. -/
def selectedNineteenOrderedRunListOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → List Nat :=
  Quotient.lift (selectedContextEighteenOrderedRunList l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesOrderedRunList l r A)

theorem selectedOrderedRunList_factorsOld
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedRawCongruentOrderedRunListOnQuotient l r J N
        (selectedRawCongruentProject l r J N q) =
      selectedNineteenOrderedRunListOnQuotient l r J N q := by
  induction q using Quotient.inductionOn with
  | _ M => rfl

/-- The actual raw18D witness with ordered run block lengths [3,2]. -/
def selectedFullRunOrderWitnessLeft
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  selectedUniformRunReverseIter l r N 3
    (selectedConsecutiveTripleWitnessGap l r N
      (selectedUniformRunReverseIter l r N 2 (.strict N)))

/-- Same exact dependent endpoints and run multiset, but order [2,3]. -/
def selectedFullRunOrderWitnessRight
    (N : SelectedContextualSeventeen W l r H K) :
    SelectedContextualEighteen W l r N N :=
  selectedUniformRunReverseIter l r N 2
    (selectedConsecutiveTripleWitnessGap l r N
      (selectedUniformRunReverseIter l r N 3 (.strict N)))

theorem selectedFullRunOrderWitness_leftList
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderWitnessLeft l r N) = [3, 2] := by
  rfl

theorem selectedFullRunOrderWitness_rightList
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderWitnessRight l r N) = [2, 3] := by
  rfl

theorem selectedFullRunOrderWitness_listDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenOrderedRunList l r
        (selectedFullRunOrderWitnessLeft l r N) ≠
      selectedContextEighteenOrderedRunList l r
        (selectedFullRunOrderWitnessRight l r N) := by
  rw [selectedFullRunOrderWitness_leftList l r N,
    selectedFullRunOrderWitness_rightList l r N]
  decide

/-- General ACTUAL raw run-block construction from two independently
given natural lengths. A strict-chain gap is retained as Type evidence. -/
def selectedFullRunOrderGeneral
    (N : SelectedContextualSeventeen W l r H K) (p q : Nat) :
    SelectedContextualEighteen W l r N N :=
  selectedUniformRunReverseIter l r N p
    (selectedConsecutiveTripleWitnessGap l r N
      (selectedUniformRunReverseIter l r N q (.strict N)))

/-- Exact formula for the run-count tower of ANY two-block true
same-endpoint raw evidence. The formula uses Nat truncated subtraction. -/
theorem selectedFullRunOrderGeneral_count
    (N : SelectedContextualSeventeen W l r H K)
    (p q degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderGeneral l r N p q) =
      (p - degree) + (q - degree) := by
  calc
    _ = selectedContextEighteenConsecutiveRunCount l r degree
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N q (.strict N))) +
          (p - degree) :=
        selectedUniformRunReverseIter_count l r N _ (by rfl) p degree
    _ = (selectedContextEighteenConsecutiveRunCount l r degree
          (selectedUniformRunReverseIter l r N q (.strict N)) + 0) +
          (p - degree) := rfl
    _ = ((0 + (q - degree)) + 0) + (p - degree) := by
        rw [selectedUniformRunReverseIter_count l r N (.strict N)
          (by rfl) q degree]
        rfl
    _ = (p - degree) + (q - degree) := by omega

/-- A pair of run blocks has identical full run-count tower after
permuting its blocks. No finite cutoff is involved. -/
theorem selectedFullRunOrderGeneral_swapCountEq
    (N : SelectedContextualSeventeen W l r H K)
    (p q degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderGeneral l r N p q) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderGeneral l r N q p) := by
  rw [selectedFullRunOrderGeneral_count l r N p q degree,
    selectedFullRunOrderGeneral_count l r N q p degree]
  omega

/-- Strict-chain gap erasure and true reverse iteration prove every
ancestor tower coordinate equal after permuting the two run blocks.
The original terms remain distinct Type-valued proofs. -/
theorem selectedFullRunOrderGeneral_swapTowerEq
    (N : SelectedContextualSeventeen W l r H K)
    (p q degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedFullRunOrderGeneral l r N p q) =
      selectedAncestorTowerCount l r degree
        (selectedFullRunOrderGeneral l r N q p) := by
  let S : SelectedContextualEighteen W l r N N := .strict N
  have hleft : ∀ d : Nat,
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N p
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N q S))) =
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N p
          (selectedUniformRunReverseIter l r N q S)) :=
    selectedUniformRunReverseIter_preservesTower l r N _ _
      (selectedConsecutiveTripleWitness_gapTowerEq l r N
        (selectedUniformRunReverseIter l r N q S)) p
  have hright : ∀ d : Nat,
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N q
          (selectedConsecutiveTripleWitnessGap l r N
            (selectedUniformRunReverseIter l r N p S))) =
      selectedAncestorTowerCount l r d
        (selectedUniformRunReverseIter l r N q
          (selectedUniformRunReverseIter l r N p S)) :=
    selectedUniformRunReverseIter_preservesTower l r N _ _
      (selectedConsecutiveTripleWitness_gapTowerEq l r N
        (selectedUniformRunReverseIter l r N p S)) q
  calc
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N p
            (selectedUniformRunReverseIter l r N q S)) := hleft degree
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N (q + p) S) := by
          rw [selectedUniformRunReverseIter_iter l r N p q S]
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N (p + q) S) := by
          have hpq : q + p = p + q := Nat.add_comm q p
          rw [hpq]
    _ = selectedAncestorTowerCount l r degree
          (selectedUniformRunReverseIter l r N q
            (selectedUniformRunReverseIter l r N p S)) := by
          rw [selectedUniformRunReverseIter_iter l r N q p S]
    _ = _ := (hright degree).symm

/-- Entire natural-indexed ancestor tower equality for the concrete
[3,2] versus [2,3] genuine raw pair. -/
theorem selectedFullRunOrderWitness_allTowerEq
    (N : SelectedContextualSeventeen W l r H K) (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedFullRunOrderWitnessLeft l r N) =
      selectedAncestorTowerCount l r degree
        (selectedFullRunOrderWitnessRight l r N) :=
  selectedFullRunOrderGeneral_swapTowerEq l r N 3 2 degree

/-- Every natural degree of the complete consecutive-reverse-run
histogram coincides, not merely any finite prefix. -/
theorem selectedFullRunOrderWitness_allCountsEq
    (N : SelectedContextualSeventeen W l r H K) (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderWitnessLeft l r N) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderWitnessRight l r N) :=
  selectedFullRunOrderGeneral_swapCountEq l r N 3 2 degree

theorem selectedFullRunOrderWitness_traceEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTrace l r
        (selectedFullRunOrderWitnessLeft l r N) =
      selectedContextEighteenTrace l r
        (selectedFullRunOrderWitnessRight l r N) := by
  rfl

theorem selectedFullRunOrderWitness_topEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTopReverseFlag l r
        (selectedFullRunOrderWitnessLeft l r N) =
      selectedContextEighteenTopReverseFlag l r
        (selectedFullRunOrderWitnessRight l r N) := by
  rfl

theorem selectedFullRunOrderWitness_adjacentEq
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedFullRunOrderWitnessLeft l r N) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedFullRunOrderWitnessRight l r N) := by
  rw [← selectedConsecutiveRun_degreeOne_eqAdjacent l r
      (selectedFullRunOrderWitnessLeft l r N),
    ← selectedConsecutiveRun_degreeOne_eqAdjacent l r
      (selectedFullRunOrderWitnessRight l r N)]
  exact selectedFullRunOrderWitness_allCountsEq l r N 1

/-- All eight original quotiented observations agree using the
certified v5.60 links from the genuine full ancestor tower. -/
theorem selectedFullRunOrderWitness_eightSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawEightSignature l r
      (selectedFullRunOrderWitnessLeft l r N)
      (selectedFullRunOrderWitnessRight l r N) := by
  let X : SelectedContextualEighteen W l r N N :=
    selectedFullRunOrderWitnessLeft l r N
  let Y : SelectedContextualEighteen W l r N N :=
    selectedFullRunOrderWitnessRight l r N
  have ht : ∀ k : Nat,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y :=
    selectedFullRunOrderWitness_allTowerEq l r N
  refine ⟨selectedFullRunOrderWitness_traceEq l r N,
    ?_, selectedFullRunOrderWitness_adjacentEq l r N,
    selectedFullRunOrderWitness_topEq l r N, ?_, ?_, ?_, ?_⟩
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

theorem selectedFullRunOrderWitness_classDistinct
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawCongruentClass l r
        (selectedFullRunOrderWitnessLeft l r N) ≠
      selectedRawCongruentClass l r
        (selectedFullRunOrderWitnessRight l r N) := by
  intro h
  have hc := congrArg (selectedRawCongruentOrderedRunListOnQuotient l r N N) h
  change selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderWitnessLeft l r N) =
    selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderWitnessRight l r N) at hc
  exact (selectedFullRunOrderWitness_listDistinct l r N) hc

theorem selectedFullRunOrderWitness_noComparison
    (N : SelectedContextualSeventeen W l r H K) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r N N
      (selectedFullRunOrderWitnessLeft l r N)
      (selectedFullRunOrderWitnessRight l r N)) := by
  rintro ⟨A⟩
  exact (selectedFullRunOrderWitness_classDistinct l r N)
    (Quotient.sound ⟨A⟩)

/-- True prefix cancellation for List Nat: if adding the SAME
original source run history to two suffixes makes them equal, the
suffix ordered histories were equal before composition. -/
theorem selectedOrderedRunList_prefixCancel
    (prefix xs ys : List Nat) (h : prefix ++ xs = prefix ++ ys) :
    xs = ys := by
  induction prefix with
  | nil => simpa using h
  | cons a tail ih =>
      apply ih
      have hh : a :: (tail ++ xs) = a :: (tail ++ ys) := h
      exact (List.cons.inj hh).2

/-- Transport into an original dependent J→N fiber ONLY after
supplying a real proof M:J→N. No fiber is assumed inhabited. -/
def selectedFullRunOrderFiberLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedFullRunOrderWitnessLeft l r N)

def selectedFullRunOrderFiberRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (selectedFullRunOrderWitnessRight l r N)

theorem selectedFullRunOrderFiber_allTowerEq
    (M : SelectedContextualEighteen W l r J N) (degree : Nat) :
    selectedAncestorTowerCount l r degree
        (selectedFullRunOrderFiberLeft l r M) =
      selectedAncestorTowerCount l r degree
        (selectedFullRunOrderFiberRight l r M) := by
  cases degree with
  | zero => rfl
  | succ d =>
      change selectedAncestorTowerCount l r (d + 1) M +
          selectedAncestorTowerCount l r (d + 1)
            (selectedFullRunOrderWitnessLeft l r N) =
        selectedAncestorTowerCount l r (d + 1) M +
          selectedAncestorTowerCount l r (d + 1)
            (selectedFullRunOrderWitnessRight l r N)
      exact congrArg
        (fun t : Nat => selectedAncestorTowerCount l r (d + 1) M + t)
        (selectedFullRunOrderWitness_allTowerEq l r N (d + 1))

theorem selectedFullRunOrderFiber_allCountsEq
    (M : SelectedContextualEighteen W l r J N) (degree : Nat) :
    selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderFiberLeft l r M) =
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderFiberRight l r M) := by
  change selectedContextEighteenConsecutiveRunCount l r degree M +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderWitnessLeft l r N) =
    selectedContextEighteenConsecutiveRunCount l r degree M +
      selectedContextEighteenConsecutiveRunCount l r degree
        (selectedFullRunOrderWitnessRight l r N)
  exact congrArg
    (fun t : Nat => selectedContextEighteenConsecutiveRunCount l r degree M + t)
    (selectedFullRunOrderWitness_allCountsEq l r N degree)

theorem selectedFullRunOrderFiber_eightSignature
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawEightSignature l r
      (selectedFullRunOrderFiberLeft l r M)
      (selectedFullRunOrderFiberRight l r M) :=
  selectedRawEightSignature_rightChain l r M
    (selectedFullRunOrderWitnessLeft l r N)
    (selectedFullRunOrderWitnessRight l r N)
    (selectedFullRunOrderWitness_eightSignature l r N)

theorem selectedFullRunOrderFiber_listDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenOrderedRunList l r
        (selectedFullRunOrderFiberLeft l r M) ≠
      selectedContextEighteenOrderedRunList l r
        (selectedFullRunOrderFiberRight l r M) := by
  intro h
  change selectedContextEighteenOrderedRunList l r M ++
      selectedContextEighteenOrderedRunList l r
        (selectedFullRunOrderWitnessLeft l r N) =
    selectedContextEighteenOrderedRunList l r M ++
      selectedContextEighteenOrderedRunList l r
        (selectedFullRunOrderWitnessRight l r N) at h
  have hs := selectedOrderedRunList_prefixCancel
    (selectedContextEighteenOrderedRunList l r M)
    (selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderWitnessLeft l r N))
    (selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderWitnessRight l r N)) h
  exact (selectedFullRunOrderWitness_listDistinct l r N) hs

theorem selectedFullRunOrderFiber_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r (selectedFullRunOrderFiberLeft l r M) ≠
      selectedRawCongruentClass l r (selectedFullRunOrderFiberRight l r M) := by
  intro h
  have hc := congrArg
    (selectedRawCongruentOrderedRunListOnQuotient l r J N) h
  change selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderFiberLeft l r M) =
    selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderFiberRight l r M) at hc
  exact (selectedFullRunOrderFiber_listDistinct l r M) hc

/-- The truly infinite tower of consecutive-run counts descended
independently to the genuine seven-generator new quotient. -/
def selectedRawCongruentAllRunTowerObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → (Nat → Nat) :=
  fun q d => selectedRawCongruentRunCountOnQuotient l r d J N q

/-- The ACTUAL combined new-quotient observer includes all original
NINE observations, the whole Nat→Nat ancestor tower, and the whole
Nat→Nat direct consecutive reverse run-count tower. -/
def selectedRawCongruentFullDoubleInfiniteObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      (selectedRawNineObservationValue × (Nat → Nat)) × (Nat → Nat) :=
  fun q => (selectedRawCongruentNineFullTowerObservation l r J N q,
    selectedRawCongruentAllRunTowerObservation l r J N q)

theorem selectedFullRunOrderFiber_nineFullTowerEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentNineFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedFullRunOrderFiberLeft l r M)) =
      selectedRawCongruentNineFullTowerObservation l r J N
        (selectedRawCongruentClass l r (selectedFullRunOrderFiberRight l r M)) := by
  apply Prod.ext
  · apply Prod.ext
    · exact selectedRawEightSignature_toObservation l r
        (selectedFullRunOrderFiberLeft l r M)
        (selectedFullRunOrderFiberRight l r M)
        (selectedFullRunOrderFiber_eightSignature l r M)
    · change selectedAncestorTowerCount l r 6
          (selectedFullRunOrderFiberLeft l r M) =
        selectedAncestorTowerCount l r 6
          (selectedFullRunOrderFiberRight l r M)
      exact selectedFullRunOrderFiber_allTowerEq l r M 6
  · funext d
    change selectedAncestorTowerCount l r d
        (selectedFullRunOrderFiberLeft l r M) =
      selectedAncestorTowerCount l r d
        (selectedFullRunOrderFiberRight l r M)
    exact selectedFullRunOrderFiber_allTowerEq l r M d

theorem selectedFullRunOrderFiber_doubleInfiniteEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentFullDoubleInfiniteObservation l r J N
        (selectedRawCongruentClass l r (selectedFullRunOrderFiberLeft l r M)) =
      selectedRawCongruentFullDoubleInfiniteObservation l r J N
        (selectedRawCongruentClass l r (selectedFullRunOrderFiberRight l r M)) := by
  apply Prod.ext
  · exact selectedFullRunOrderFiber_nineFullTowerEq l r M
  · funext d
    change selectedContextEighteenConsecutiveRunCount l r d
        (selectedFullRunOrderFiberLeft l r M) =
      selectedContextEighteenConsecutiveRunCount l r d
        (selectedFullRunOrderFiberRight l r M)
    exact selectedFullRunOrderFiber_allCountsEq l r M d

/-- Genuine NONINJECTIVITY, in every ACTUALLY supplied exact original
fiber M:J→N, of the COMPLETE two infinite tower observation. -/
theorem selectedRawCongruentFullDoubleInfinite_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentFullDoubleInfiniteObservation l r J N) := by
  intro hinj
  exact (selectedFullRunOrderFiber_classDistinct l r M)
    (hinj (selectedFullRunOrderFiber_doubleInfiniteEq l r M))

/-- No global decoder of the separately conserved ordered run list
from the double-infinite observer of an actually inhabited fiber. -/
theorem selectedRawCongruentFullDoubleInfinite_noOrderedDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        ((selectedRawNineObservationValue × (Nat → Nat)) × (Nat → Nat)) →
          List Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFullDoubleInfiniteObservation l r J N q) =
          selectedRawCongruentOrderedRunListOnQuotient l r J N q := by
  rintro ⟨decode, h⟩
  have hc :
      selectedRawCongruentOrderedRunListOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFullRunOrderFiberLeft l r M)) =
        selectedRawCongruentOrderedRunListOnQuotient l r J N
          (selectedRawCongruentClass l r (selectedFullRunOrderFiberRight l r M)) := by
    calc
      _ = decode (selectedRawCongruentFullDoubleInfiniteObservation l r J N
            (selectedRawCongruentClass l r (selectedFullRunOrderFiberLeft l r M))) :=
        (h _).symm
      _ = decode (selectedRawCongruentFullDoubleInfiniteObservation l r J N
            (selectedRawCongruentClass l r (selectedFullRunOrderFiberRight l r M))) :=
        congrArg decode (selectedFullRunOrderFiber_doubleInfiniteEq l r M)
      _ = _ := h _
  change selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderFiberLeft l r M) =
    selectedContextEighteenOrderedRunList l r
      (selectedFullRunOrderFiberRight l r M) at hc
  exact (selectedFullRunOrderFiber_listDistinct l r M) hc

theorem selectedRawCongruentFullDoubleInfinite_noClassDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        ((selectedRawNineObservationValue × (Nat → Nat)) × (Nat → Nat)) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentFullDoubleInfiniteObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentFullDoubleInfinite_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentFullDoubleInfiniteObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentFullDoubleInfiniteObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

theorem selectedRawCongruentFullDoubleInfinite_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentFullDoubleInfiniteObservation l r J J) :=
  selectedRawCongruentFullDoubleInfinite_notInjective l r (.strict J)

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenOrderedRunList
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesOrderedRunList
#print axioms PentagonAdjoinedSixCell.selectedRawCongruent_preservesOrderedRunList
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentOrderedRunListOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentOrderedRunList_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenOrderedRunListOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedOrderedRunList_factorsOld
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitnessLeft
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitnessRight
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_leftList
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_rightList
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_listDistinct
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderGeneral
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderGeneral_count
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderGeneral_swapCountEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderGeneral_swapTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_allCountsEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_traceEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_topEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_adjacentEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderWitness_noComparison
#print axioms PentagonAdjoinedSixCell.selectedOrderedRunList_prefixCancel
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiberLeft
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiberRight
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiber_allTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiber_allCountsEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiber_listDistinct
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiber_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentAllRunTowerObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleInfiniteObservation
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiber_nineFullTowerEq
#print axioms PentagonAdjoinedSixCell.selectedFullRunOrderFiber_doubleInfiniteEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleInfinite_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleInfinite_noOrderedDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleInfinite_noClassDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentFullDoubleInfinite_endomorphismNotInjective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
