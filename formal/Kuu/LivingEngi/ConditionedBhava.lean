import Kuu.LivingEngi.FrameTransport

/-!
# Living Engi Cycle LEC-06: certified conventional Bhava and retained lineage

Bhava is not an absolute ontology or the same event as birth.
Here it is a *conditioned* conventional world readout together with:
- genuine typed source local sections and their exact support proof,
- a scoped LEC-04 certificate with actual mathematical admission,
- a history-aware candidate-generation kernel, and
- future-only revisions preserving the old complete proof-relevant snapshot.

The support uses the explicit LEC-05 per-context frames, not source-fiber
identification. No unchecked or refuted global claim can initialize a
Bhava through the certified constructor. Revising a Bhava appends its
entire previous source/world/certificate snapshot; previous history is
not overwritten and new source agreement must be proved again.

No claim of biological existence, Buddhist doctrinal equivalence,
a runnable self-modifying AI, non-Markov empirical dynamics, ActOS
execution or exact WORLD truth is made by these Type-level constructions.
-/

namespace Kuu.LivingEngi

set_option autoImplicit false

universe uX uI uF uA uInput uCandidate uHistory

section BhavaCore

variable {X : Type uX} {I : Type uI}
variable {F : I → Type uF} {A : Type uA}

/-- A source-preserving snapshot in one declared family of local frames.
Both source Type values and the conventional readout are stored,
together with proof that the two match on every local support. -/
structure FramedSnapshot
    (U : I → Set X) (e : Frames F A) where
  sections : FramedLocalSections U F
  readout : X → A
  supports :
    ∀ (i : I) (x : {y : X // y ∈ U i}),
      readout x.1 = (e i) (sections i x)
  certificate : PromotionEvidence (HasFramedGlobal U e sections)
  admitted : Admissible certificate

/-- Exact mathematical support is exposed, not inferred from model fluency. -/
theorem FramedSnapshot.hasFramedGlobal
    {U : I → Set X} {e : Frames F A}
    (snap : FramedSnapshot U e) :
    HasFramedGlobal U e snap.sections := by
  exact ⟨snap.readout, snap.supports⟩

/-- Construct a full Type-valued snapshot only from admission of the
actual globally supported statement for the declared local sections. -/
noncomputable def certifiedSnapshot
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev) : FramedSnapshot U e where
  sections := s
  readout := Classical.choose (admitted_sound ev hadmit)
  supports := by
    intro i x
    exact (Classical.choose_spec (admitted_sound ev hadmit)) i x
  certificate := ev
  admitted := hadmit

/-- Admitting a snapshot retains the EXACT original Type-valued
source local functions as data, not only their quotient readouts. -/
theorem certifiedSnapshot_source
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev) :
    (certifiedSnapshot U e s ev hadmit).sections = s := rfl

/-- A snapshot extracted from an admitted certificate has the exact
locally supported value that the original source requires. -/
theorem certifiedSnapshot_support
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (i : I) (x : {y : X // y ∈ U i}) :
    (certifiedSnapshot U e s ev hadmit).readout x.1 =
      (e i) (s i x) := by
  exact (certifiedSnapshot U e s ev hadmit).supports i x

/-- Bhava packages an evidence-backed conventional model with an
explicit history-aware kernel. The output is a CANDIDATE type, not a
real-world action. A history lists whole prior certified snapshots. -/
structure ConventionalBhava
    (U : I → Set X) (e : Frames F A)
    (Input : Type uInput) (Candidate : Type uCandidate) where
  current : FramedSnapshot U e
  history : List (FramedSnapshot U e)
  kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate

end BhavaCore

section History

/-- A future lineage extends a past lineage by actual append,
not by destructive rewriting or an equality between old and new worlds. -/
def HistoryExtends {T : Type uHistory}
    (oldHist newHist : List T) : Prop :=
  ∃ tail : List T, newHist = oldHist ++ tail

theorem historyExtends_refl {T : Type uHistory}
    (hist : List T) : HistoryExtends hist hist := by
  refine ⟨[], ?_⟩
  simp

theorem historyExtends_trans {T : Type uHistory}
    {a b c : List T}
    (hab : HistoryExtends a b) (hbc : HistoryExtends b c) :
    HistoryExtends a c := by
  rcases hab with ⟨xs, hxs⟩
  rcases hbc with ⟨ys, hys⟩
  refine ⟨xs ++ ys, ?_⟩
  calc
    c = b ++ ys := hys
    _ = (a ++ xs) ++ ys := by rw [hxs]
    _ = a ++ (xs ++ ys) := List.append_assoc _ _ _

end History

section BhavaTransitions

variable {X : Type uX} {I : Type uI}
variable {F : I → Type uF} {A : Type uA}
variable {Input : Type uInput} {Candidate : Type uCandidate}

/-- Construct a new conventional Bhava from one actually admitted
global-support proof. No unchecked or refuted branch is accepted. -/
noncomputable def beginBhava
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    ConventionalBhava U e Input Candidate where
  current := certifiedSnapshot U e s ev hadmit
  history := []
  kernel := kernel

/-- A birth candidate is a pure return value conditioned on the
current readout AND accumulated historical source snapshots.
It cannot manufacture an external authorization receipt. -/
def birthCandidate
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate) (input : Input) :
    Candidate :=
  b.kernel b.current.readout b.history input

/-- A newly submitted source and new kernel can replace the CURRENT
model only when accompanied by a proof of its exact local-global support.
The old model and all earlier certificates are preserved in history. -/
noncomputable def reviseBhava
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (nextSource : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e nextSource))
    (hadmit : Admissible ev)
    (nextKernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    ConventionalBhava U e Input Candidate where
  current := certifiedSnapshot U e nextSource ev hadmit
  history := b.history ++ [b.current]
  kernel := nextKernel

/-- Future-only revision retains the entire old history, then appends
the complete previous certified snapshot as a new last event. -/
theorem revision_history_exact
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    (reviseBhava b s ev hadmit kernel).history =
      b.history ++ [b.current] := rfl

/-- Every legitimate revision is monotonic on the SOURCE HISTORY. -/
theorem revision_extends_history
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    HistoryExtends b.history (reviseBhava b s ev hadmit kernel).history := by
  exact ⟨[b.current], rfl⟩

/-- The previous WORLD plus its ORIGINAL typed source/certificate exists
literally as a member of the newly retained history. -/
theorem revision_preserves_previous_snapshot
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    b.current ∈ (reviseBhava b s ev hadmit kernel).history := by
  change b.current ∈ b.history ++ [b.current]
  simp

/-- Proof of original-source preservation extends beyond just a
counting/length invariant: both previous readout and local values survive. -/
theorem revision_preserves_previous_readout_and_source
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    ∃ old : FramedSnapshot U e,
      old ∈ (reviseBhava b s ev hadmit kernel).history ∧
        old.readout = b.current.readout ∧
        old.sections = b.current.sections := by
  refine ⟨b.current, revision_preserves_previous_snapshot b s ev hadmit kernel,
    rfl, rfl⟩

/-- The revised model does not silently substitute another source:
its current section is exactly the submitted proof-carrying section. -/
theorem revision_source_exact
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    (reviseBhava b s ev hadmit kernel).current.sections = s := rfl

/-- The new common readout also agrees with the NEW local typed source. -/
theorem revision_source_supported
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate)
    (i : I) (x : {y : X // y ∈ U i}) :
    (reviseBhava b s ev hadmit kernel).current.readout x.1 =
      (e i) (s i x) := by
  exact (reviseBhava b s ev hadmit kernel).current.supports i x

/-- Every conventional Bhava in this model necessarily supports a
compatible original typed local atlas under the supplied cover. -/
theorem bhava_implies_transport_compatible
    (U : I → Set X) (e : Frames F A)
    (hcover : Covers U)
    (b : ConventionalBhava U e Input Candidate) :
    TransportCompatible U e b.current.sections := by
  exact (transportCompatible_iff_hasFramedGlobal U e b.current.sections hcover).2
    b.current.hasFramedGlobal

/-- A genuinely incompatible local source cannot underlie ANY Bhava
of this evidence-carrying type, irrespective of its proposed kernel. -/
theorem no_bhava_for_incompatible_source
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F) (hcover : Covers U)
    (hbad : ¬ TransportCompatible U e s) :
    ¬ ∃ b : ConventionalBhava U e Input Candidate,
        b.current.sections = s := by
  rintro ⟨b, hsections⟩
  have hgood := bhava_implies_transport_compatible U e hcover b
  rw [hsections] at hgood
  exact hbad hgood

/-- Conversely, compatible actual sources on a genuine cover yield
a conventional Bhava for ANY caller-supplied candidate kernel.
This says nothing about downstream authority or empirical truth. -/
theorem compatible_source_admits_bhava
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F) (hcover : Covers U)
    (hgood : TransportCompatible U e s)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate) :
    Nonempty (ConventionalBhava U e Input Candidate) := by
  have hglobal : HasFramedGlobal U e s :=
    (transportCompatible_iff_hasFramedGlobal U e s hcover).1 hgood
  exact ⟨beginBhava U e s (PromotionEvidence.certified hglobal)
    (by trivial) kernel⟩

/-- The next generated candidate explicitly receives the appended history.
One actual revision does not erase the former WORLD source/certificate. -/
theorem birth_after_revision_uses_updated_history
    {U : I → Set X} {e : Frames F A}
    (b : ConventionalBhava U e Input Candidate)
    (s : FramedLocalSections U F)
    (ev : PromotionEvidence (HasFramedGlobal U e s))
    (hadmit : Admissible ev)
    (kernel : (X → A) → List (FramedSnapshot U e) → Input → Candidate)
    (input : Input) :
    birthCandidate (reviseBhava b s ev hadmit kernel) input =
      kernel (reviseBhava b s ev hadmit kernel).current.readout
        (b.history ++ [b.current]) input := rfl

end BhavaTransitions

#print axioms FramedSnapshot.hasFramedGlobal
#print axioms certifiedSnapshot_source
#print axioms certifiedSnapshot_support
#print axioms historyExtends_refl
#print axioms historyExtends_trans
#print axioms revision_history_exact
#print axioms revision_extends_history
#print axioms revision_preserves_previous_snapshot
#print axioms revision_preserves_previous_readout_and_source
#print axioms revision_source_exact
#print axioms revision_source_supported
#print axioms bhava_implies_transport_compatible
#print axioms no_bhava_for_incompatible_source
#print axioms compatible_source_admits_bhava
#print axioms birth_after_revision_uses_updated_history

end Kuu.LivingEngi
