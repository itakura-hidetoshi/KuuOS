import Kuu.LivingEngi.BirthAuthorization

/-!
# Living Engi Cycle LEC-08: genuine history-sensitive candidates and repair

Earlier LEC-06/07 modules separate source-certified conditional Bhava,
candidate birth and externally authorized requests. Here the temporal part
is made mathematically testable, relative to an EXPLICIT observation:

1. A candidate kernel may depend on the retained typed history even when
   its current conventional WORLD readout and input are fixed.
2. A finite lag-two witness compares two histories having the same most
   recent snapshot but different older histories. The output differs.
   Thus that specific kernel cannot factor through the current WORLD and
   most recent snapshot alone. This is a genuine finite non-Markov example
   *relative to the declared projection*, not a proof about all dynamics.
3. An evidence-certified future-only revision can replace the candidate
   kernel by an explicitly history-independent policy. The complete previous
   snapshot and all prior history survive, with the same original local
   source and (under cover) the same conventional readout.

There is no claim that all feedback systems are stabilizable, that a
history-free policy is always better, that real neural weights are changed,
or that any output or receipt acquires external ActOS/clinical authority.
All existing F55/P77/GK5CG source and higher witnesses remain untouched.
-/

namespace Kuu.LivingEngi

set_option autoImplicit false

universe uX uI uF uA uInput uCandidate

section ConditionalMemory

variable {X : Type uX} {I : Type uI}
variable {F : I → Type uF} {A : Type uA}

/-- Kernel constancy on ALL histories at fixed current readout and input.
This is a declared WORLD-projection property, not a universal assertion
that a process is physically Markovian or non-Markovian. -/
def HistoryIndependent
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) (Candidate : Type uCandidate)
    (kernel :
      (X → A) → List (FramedSnapshot U e) → Input → Candidate) : Prop :=
  ∀ (readout : X → A)
    (older newer : List (FramedSnapshot U e)) (input : Input),
    kernel readout older input = kernel readout newer input

/-- Factoring a history-bearing kernel through the current readout only. -/
def HasCurrentFactor
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) (Candidate : Type uCandidate)
    (kernel :
      (X → A) → List (FramedSnapshot U e) → Input → Candidate) : Prop :=
  ∃ currentKernel : (X → A) → Input → Candidate,
    ∀ (readout : X → A)
      (history : List (FramedSnapshot U e)) (input : Input),
      kernel readout history input = currentKernel readout input

/-- History-independence and exact current-only factorization coincide.
No measure, topology, dynamics or Markov property is assumed implicitly. -/
theorem historyIndependent_iff_hasCurrentFactor
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) (Candidate : Type uCandidate)
    (kernel :
      (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    HistoryIndependent U e Input Candidate kernel ↔
      HasCurrentFactor U e Input Candidate kernel := by
  constructor
  · intro h
    refine ⟨fun readout input => kernel readout [] input, ?_⟩
    intro readout history input
    exact h readout history [] input
  · rintro ⟨current, hfactor⟩
    intro readout older newer input
    exact (hfactor readout older input).trans
      (hfactor readout newer input).symm

/-- A parameterized history-free policy: new candidate generation can
continue with the original WORLD projection while not consuming history. -/
def historyFreeKernel
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) (Candidate : Type uCandidate)
    (policy : (X → A) → Input → Candidate) :
    (X → A) → List (FramedSnapshot U e) → Input → Candidate :=
  fun readout _history input => policy readout input

theorem historyFreeKernel_independent
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) (Candidate : Type uCandidate)
    (policy : (X → A) → Input → Candidate) :
    HistoryIndependent U e Input Candidate
      (historyFreeKernel U e Input Candidate policy) := by
  intro readout older newer input
  rfl

theorem historyFreeKernel_factors
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) (Candidate : Type uCandidate)
    (policy : (X → A) → Input → Candidate) :
    HasCurrentFactor U e Input Candidate
      (historyFreeKernel U e Input Candidate policy) := by
  refine ⟨policy, ?_⟩
  intro readout history input
  rfl

/-- An actual finite second-lag detector. Length >= 2 means that the
kernel reads more than the most recent one-snapshot projection. -/
def lagTwoKernel
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) :
    (X → A) → List (FramedSnapshot U e) → Input → Bool :=
  fun _readout history _input => decide (2 ≤ history.length)

/-- A concrete witness of two differently long source histories. -/
theorem lagTwoKernel_distinguishes_histories
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput)
    (snap : FramedSnapshot U e)
    (readout : X → A) (input : Input) :
    lagTwoKernel U e Input readout [snap] input ≠
      lagTwoKernel U e Input readout [snap, snap] input := by
  change (false : Bool) ≠ true
  decide

/-- Both histories have the SAME MOST RECENT (full typed) snapshot. -/
theorem lagTwoHistories_same_latest
    (U : I → Set X) (e : Frames F A)
    (snap : FramedSnapshot U e) :
    ([snap] : List (FramedSnapshot U e)).getLast? =
      ([snap, snap] : List (FramedSnapshot U e)).getLast? := by
  rfl

/-- The older history is independently visible despite a shared latest
snapshot. This is the actual finite obstruction to a recent-only factor. -/
theorem lagTwoKernel_no_latest_factor
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput)
    (snap : FramedSnapshot U e)
    (readout : X → A) (input : Input) :
    ¬ ∃ recentKernel :
        (X → A) → Option (FramedSnapshot U e) → Input → Bool,
        ∀ history : List (FramedSnapshot U e),
          lagTwoKernel U e Input readout history input =
            recentKernel readout history.getLast? input := by
  rintro ⟨recentKernel, hfactor⟩
  have hOne := hfactor [snap]
  have hTwo := hfactor [snap, snap]
  have hbad : (false : Bool) = true := calc
    false = recentKernel readout (some snap) input := by
      simpa [lagTwoKernel] using hOne
    _ = true := by
      simpa [lagTwoKernel] using hTwo.symm
  cases hbad

/-- A stronger nonfactorization: current-only readout cannot reproduce
the lag-two kernel, since two histories with the same current readout
give different actual Bool candidates. -/
theorem lagTwoKernel_no_current_factor
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput)
    (snap : FramedSnapshot U e)
    (readout : X → A) (input : Input) :
    ¬ HasCurrentFactor U e Input Bool (lagTwoKernel U e Input) := by
  rintro ⟨currentKernel, hfactor⟩
  have hOne := hfactor readout [snap] input
  have hTwo := hfactor readout [snap, snap] input
  have hbad : (false : Bool) = true := calc
    false = currentKernel readout input := by
      simpa [lagTwoKernel] using hOne
    _ = true := by
      simpa [lagTwoKernel] using hTwo.symm
  cases hbad

/-- In particular, this finite-memory kernel is NOT history-independent
relative to the declared current-state projection. -/
theorem lagTwoKernel_not_historyIndependent
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput)
    (snap : FramedSnapshot U e)
    (readout : X → A) (input : Input) :
    ¬ HistoryIndependent U e Input Bool (lagTwoKernel U e Input) := by
  intro hindependent
  exact lagTwoKernel_no_current_factor U e Input snap readout input
    ((historyIndependent_iff_hasCurrentFactor U e Input Bool
      (lagTwoKernel U e Input)).1 hindependent)

end ConditionalMemory

section ActualBhavaRepair

variable {X : Type uX} {I : Type uI}
variable {F : I → Type uF} {A : Type uA}
variable {U : I → Set X} {e : Frames F A}
variable {Input : Type uInput} {Candidate : Type uCandidate}

/-- A future-only model revision from an already certified Bhava.
The old source proof is reused as an actual, narrowly scoped mathematical
certificate. A new caller-provided candidate policy deliberately does
not use older snapshots. This never executes a candidate. -/
noncomputable def repairToHistoryIndependent
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate) :
    ConventionalBhava U e Input Candidate :=
  reviseBhava b b.current.sections
    (PromotionEvidence.certified b.current.hasFramedGlobal)
    (by trivial)
    (historyFreeKernel U e Input Candidate policy)

/-- No original local source is replaced or silently identified with
another Type-valued section. -/
theorem repair_preserves_current_source
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate) :
    (repairToHistoryIndependent b policy).current.sections =
      b.current.sections := rfl

/-- The complete former history and the immediately previous snapshot
remain literally in the new history (append-only). -/
theorem repair_history_exact
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate) :
    (repairToHistoryIndependent b policy).history =
      b.history ++ [b.current] := rfl

theorem repair_history_extends
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate) :
    HistoryExtends b.history (repairToHistoryIndependent b policy).history := by
  exact ⟨[b.current], rfl⟩

theorem repair_retains_previous_snapshot
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate) :
    b.current ∈ (repairToHistoryIndependent b policy).history := by
  change b.current ∈ b.history ++ [b.current]
  simp

/-- Given an actual cover, same typed source + certified support determines
the identical conventional readout; a revision does not fabricate
a different current WORLD representation. -/
theorem repair_readout_unchanged
    (U : I → Set X) (e : Frames F A)
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate)
    (hcover : Covers U) :
    (repairToHistoryIndependent b policy).current.readout =
      b.current.readout := by
  apply global_unique U (framedReadout U e b.current.sections) hcover
  · intro i x
    exact (repairToHistoryIndependent b policy).current.supports i x
  · intro i x
    exact b.current.supports i x

/-- The NEW kernel is genuinely independent of older snapshots even
though the snapshots remain fully available as recorded evidence. -/
theorem repair_kernel_historyIndependent
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate) :
    HistoryIndependent U e Input Candidate
      (repairToHistoryIndependent b policy).kernel := by
  exact historyFreeKernel_independent U e Input Candidate policy

/-- The new birth candidate uses the supplied future policy rather than
silently sampling or overwriting any stored prior proof. -/
theorem repair_birth_exact
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate)
    (input : Input) :
    birthCandidate (repairToHistoryIndependent b policy) input =
      policy (repairToHistoryIndependent b policy).current.readout input := rfl

/-- Under a genuine cover, all three protections can hold at once:
old source, old current readout, and full old history remain available,
while the chosen future candidate kernel is independent of the past. -/
theorem repair_preserves_world_and_history
    (U : I → Set X) (e : Frames F A)
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate)
    (hcover : Covers U) :
    (repairToHistoryIndependent b policy).current.sections =
        b.current.sections ∧
      (repairToHistoryIndependent b policy).current.readout =
        b.current.readout ∧
      HistoryExtends b.history
        (repairToHistoryIndependent b policy).history ∧
      HistoryIndependent U e Input Candidate
        (repairToHistoryIndependent b policy).kernel := by
  exact ⟨repair_preserves_current_source b policy,
    repair_readout_unchanged U e b policy hcover,
    repair_history_extends b policy,
    repair_kernel_historyIndependent b policy⟩

/-- The repaired model still contains an actual certificate of the same
source's local-global support; the old evidence was not overwritten. -/
theorem repair_certified_source
    (b : ConventionalBhava U e Input Candidate)
    (policy : (X → A) → Input → Candidate) :
    HasFramedGlobal U e
      (repairToHistoryIndependent b policy).current.sections :=
  (repairToHistoryIndependent b policy).current.hasFramedGlobal

end ActualBhavaRepair

section ReachableLagTwoWitness

variable {X : Type uX} {I : Type uI}
variable {F : I → Type uF} {A : Type uA}
variable {Input : Type uInput}

/-- Two actual certified revisions of one initial Bhava can have the
same current readout AND the same original source but different births.
No unlicensed source/fiber identification is needed: the exact same
certified section, frame and proof are used for both revisions. -/
theorem lagTwo_reachable_history_difference
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (input : Input) :
    let k := lagTwoKernel U e Input
    let b₀ := beginBhava U e s ev hadmit k
    let b₁ := reviseBhava b₀ s ev hadmit k
    let b₂ := reviseBhava b₁ s ev hadmit k
    b₁.current.sections = b₂.current.sections ∧
      b₁.current.readout = b₂.current.readout ∧
      birthCandidate b₁ input ≠ birthCandidate b₂ input := by
  dsimp only
  refine ⟨rfl, rfl, ?_⟩
  change (false : Bool) ≠ true
  decide

end ReachableLagTwoWitness

#print axioms historyIndependent_iff_hasCurrentFactor
#print axioms historyFreeKernel_independent
#print axioms historyFreeKernel_factors
#print axioms lagTwoKernel_distinguishes_histories
#print axioms lagTwoHistories_same_latest
#print axioms lagTwoKernel_no_latest_factor
#print axioms lagTwoKernel_no_current_factor
#print axioms lagTwoKernel_not_historyIndependent
#print axioms repair_preserves_current_source
#print axioms repair_history_exact
#print axioms repair_history_extends
#print axioms repair_retains_previous_snapshot
#print axioms repair_readout_unchanged
#print axioms repair_kernel_historyIndependent
#print axioms repair_birth_exact
#print axioms repair_preserves_world_and_history
#print axioms repair_certified_source
#print axioms lagTwo_reachable_history_difference

end Kuu.LivingEngi
