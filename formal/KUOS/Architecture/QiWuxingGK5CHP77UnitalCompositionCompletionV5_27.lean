import KUOS.Architecture.QiWuxingGK5CHP77ContextActionLengthObstructionV5_26

/-!
Qi v5.27 — independent, explicitly SELECTED, typed unit and
same-side composition completion of v5.25's context-closed twelfth.

No original 6D–14D proof Type or its constructors are modified.
Four new comparison generators are admitted only at original,
boundary-compatible seventh-cell reflexive/composite contexts.
Old context-closed proof histories are embedded as raw Type values.
The selected grammar is itself closed under both actual original
left and right whiskerings.

On exact original six-boundary quotients the selected context
operations satisfy the left and right unit and same-side composition
laws; opposite-side commutation remains valid, by the actual previous
doubleWhisker proof. They are not raw equality of old eleven-cell
proof packets. The old total whisker-event length does NOT descend
to this quotient: the new unit and composition generators change
that length. Three existing old tenth-event count observers still
descend, and the original tenSymm obstruction remains.

This is a local chosen presentation, not a claim of automatic
thirteenth/fourteenth coherence, universal categorical coherence,
complete quotient classification, or altered source authority.
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

/-- Independent 12D syntax: retain EVERY prior v5.25 proof term via
previous. Only the FOUR unit/composition comparison rules are new.
The ordinary boundary-compatible context rules preserve closure. -/
inductive SelectedUnitalCompositionTwelve (W : Type uSix) (l r : W) :
    FramedEleven W l r → FramedEleven W l r → Type uSix where
  | strict (F : FramedEleven W l r) :
      SelectedUnitalCompositionTwelve W l r F F
  | previous {F G : FramedEleven W l r}
      (T : ContextClosedFramedTwelve W l r F G) :
      SelectedUnitalCompositionTwelve W l r F G
  | reverse {F G : FramedEleven W l r}
      (T : SelectedUnitalCompositionTwelve W l r F G) :
      SelectedUnitalCompositionTwelve W l r G F
  | chain {F G H : FramedEleven W l r}
      (T : SelectedUnitalCompositionTwelve W l r F G)
      (U : SelectedUnitalCompositionTwelve W l r G H) :
      SelectedUnitalCompositionTwelve W l r F H
  | whiskerLeft {w z : W}
      {b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r b c)
      (F G : ContextFrameEleven W l r c d)
      (T : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G)) :
      SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r (contextFrameLeft l r before F))
        (contextFramePack l r (contextFrameLeft l r before G))
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (F G : ContextFrameEleven W l r c d)
      (T : SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r F) (contextFramePack l r G))
      (after : SevenRewrite W l r d e) :
      SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r (contextFrameRight l r F after))
        (contextFramePack l r (contextFrameRight l r G after))
  | unitLeft {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (F : ContextFrameEleven W l r c d) :
      SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r (contextFrameLeft l r (.refl c) F))
        (contextFramePack l r F)
  | unitRight {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (F : ContextFrameEleven W l r c d) :
      SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r (contextFrameRight l r F (.refl d)))
        (contextFramePack l r F)
  | compLeft {w z : W}
      {a b c d : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r a b)
      (after : SevenRewrite W l r b c)
      (F : ContextFrameEleven W l r c d) :
      SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r
          (contextFrameLeft l r before (contextFrameLeft l r after F)))
        (contextFramePack l r
          (contextFrameLeft l r (.trans before after) F))
  | compRight {w z : W}
      {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r d e)
      (after : SevenRewrite W l r e f₆)
      (F : ContextFrameEleven W l r c d) :
      SelectedUnitalCompositionTwelve W l r
        (contextFramePack l r
          (contextFrameRight l r (contextFrameRight l r F before) after))
        (contextFramePack l r
          (contextFrameRight l r F (.trans before after)))

/-- The new inclusion stores original v5.25 proof terms faithfully AS
RAW DATA, even though the induced quotient map will be noninjective. -/
theorem selectedUnital_previous_injective (l r : W)
    {F G : FramedEleven W l r} :
    Function.Injective
      (fun T : ContextClosedFramedTwelve W l r F G =>
        SelectedUnitalCompositionTwelve.previous T) := by
  intro T U h
  cases h
  rfl

/-- A typed ambient congruence containing the existing v5.25 grammar
and respecting precisely the four chosen local laws. -/
structure IsSelectedUnitalCongruence (l r : W)
    (R : FramedEleven W l r → FramedEleven W l r → Prop) : Prop where
  refl : ∀ F, R F F
  symm : ∀ {F G}, R F G → R G F
  trans : ∀ {F G H}, R F G → R G H → R F H
  previous : ∀ {F G}, ContextClosedFramedTwelve W l r F G → R F G
  left : ∀ {w z : W} {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c) (F G : ContextFrameEleven W l r c d),
    R (contextFramePack l r F) (contextFramePack l r G) →
      R (contextFramePack l r (contextFrameLeft l r before F))
        (contextFramePack l r (contextFrameLeft l r before G))
  right : ∀ {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
    (F G : ContextFrameEleven W l r c d),
    R (contextFramePack l r F) (contextFramePack l r G) →
      ∀ (after : SevenRewrite W l r d e),
        R (contextFramePack l r (contextFrameRight l r F after))
          (contextFramePack l r (contextFrameRight l r G after))
  unitLeft : ∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d),
    R (contextFramePack l r (contextFrameLeft l r (.refl c) F))
      (contextFramePack l r F)
  unitRight : ∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d),
    R (contextFramePack l r (contextFrameRight l r F (.refl d)))
      (contextFramePack l r F)
  compLeft : ∀ {w z : W} {a b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r a b) (after : SevenRewrite W l r b c)
    (F : ContextFrameEleven W l r c d),
    R (contextFramePack l r
        (contextFrameLeft l r before (contextFrameLeft l r after F)))
      (contextFramePack l r (contextFrameLeft l r (.trans before after) F))
  compRight : ∀ {w z : W} {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r d e) (after : SevenRewrite W l r e f₆)
    (F : ContextFrameEleven W l r c d),
    R (contextFramePack l r
        (contextFrameRight l r (contextFrameRight l r F before) after))
      (contextFramePack l r (contextFrameRight l r F (.trans before after)))

theorem selectedUnital_least (l r : W)
    (R : FramedEleven W l r → FramedEleven W l r → Prop)
    (hR : IsSelectedUnitalCongruence l r R)
    {F G : FramedEleven W l r}
    (T : SelectedUnitalCompositionTwelve W l r F G) :
    R F G := by
  induction T with
  | strict F => exact hR.refl F
  | previous T => exact hR.previous T
  | reverse T ih => exact hR.symm ih
  | chain T U ih ih' => exact hR.trans ih ih'
  | whiskerLeft before F G T ih => exact hR.left before F G ih
  | whiskerRight F G T after ih => exact hR.right F G ih after
  | unitLeft F => exact hR.unitLeft F
  | unitRight F => exact hR.unitRight F
  | compLeft before after F => exact hR.compLeft before after F
  | compRight before after F => exact hR.compRight before after F

def selectedUnitalSetoid (W : Type uSix) (l r : W) :
    Setoid (FramedEleven W l r) where
  r := fun F G => Nonempty (SelectedUnitalCompositionTwelve W l r F G)
  iseqv := by
    constructor
    · intro F
      exact ⟨.strict F⟩
    · intro F G h
      rcases h with ⟨T⟩
      exact ⟨.reverse T⟩
    · intro F G H h h'
      rcases h with ⟨T⟩
      rcases h' with ⟨U⟩
      exact ⟨.chain T U⟩

def selectedUnitalClass (l r : W) (F : FramedEleven W l r) :
    Quotient (selectedUnitalSetoid W l r) :=
  Quotient.mk _ F

theorem selectedUnitalClass_eq_iff (l r : W)
    (F G : FramedEleven W l r) :
    selectedUnitalClass l r F = selectedUnitalClass l r G ↔
      Nonempty (SelectedUnitalCompositionTwelve W l r F G) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- A well-defined map from the v5.25 quotient; injectivity is
NOT claimed and will be refuted below. -/
def contextToSelectedUnital (l r : W) :
    Quotient (contextClosedSetoid W l r) →
      Quotient (selectedUnitalSetoid W l r) :=
  Quotient.lift (selectedUnitalClass l r) (by
    intro F G h
    rcases h with ⟨T⟩
    exact Quotient.sound ⟨.previous T⟩)

theorem contextToSelectedUnital_onClass (l r : W)
    (F : FramedEleven W l r) :
    contextToSelectedUnital l r (contextClosedClass l r F) =
      selectedUnitalClass l r F := rfl

/-- Chosen quotient at an exact original sixth-cell boundary. -/
def selectedUnitalBoundarySetoid (W : Type uSix) (l r : W) {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    Setoid (ContextFrameEleven W l r c d) where
  r := fun F G => Nonempty (SelectedUnitalCompositionTwelve W l r
    (contextFramePack l r F) (contextFramePack l r G))
  iseqv := by
    constructor
    · intro F
      exact ⟨.strict _⟩
    · intro F G h
      rcases h with ⟨T⟩
      exact ⟨.reverse T⟩
    · intro F G H h h'
      rcases h with ⟨T⟩
      rcases h' with ⟨U⟩
      exact ⟨.chain T U⟩

def selectedUnitalLeftAction (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c) :
    Quotient (selectedUnitalBoundarySetoid W l r c d) →
      Quotient (selectedUnitalBoundarySetoid W l r b d) :=
  Quotient.lift
    (fun F => Quotient.mk _ (contextFrameLeft l r before F)) (by
      intro F G h
      rcases h with ⟨T⟩
      exact Quotient.sound ⟨.whiskerLeft before F G T⟩)

def selectedUnitalRightAction (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (after : SevenRewrite W l r d e) :
    Quotient (selectedUnitalBoundarySetoid W l r c d) →
      Quotient (selectedUnitalBoundarySetoid W l r c e) :=
  Quotient.lift
    (fun F => Quotient.mk _ (contextFrameRight l r F after)) (by
      intro F G h
      rcases h with ⟨T⟩
      exact Quotient.sound ⟨.whiskerRight F G T after⟩)

theorem selectedUnitalLeft_unit (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (x : Quotient (selectedUnitalBoundarySetoid W l r c d)) :
    selectedUnitalLeftAction l r (.refl c) x = x := by
  refine Quotient.inductionOn x ?_
  intro F
  exact Quotient.sound ⟨.unitLeft F⟩

theorem selectedUnitalRight_unit (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (x : Quotient (selectedUnitalBoundarySetoid W l r c d)) :
    selectedUnitalRightAction l r (.refl d) x = x := by
  refine Quotient.inductionOn x ?_
  intro F
  exact Quotient.sound ⟨.unitRight F⟩

theorem selectedUnitalLeft_comp (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r a b)
    (after : SevenRewrite W l r b c)
    (x : Quotient (selectedUnitalBoundarySetoid W l r c d)) :
    selectedUnitalLeftAction l r before
        (selectedUnitalLeftAction l r after x) =
      selectedUnitalLeftAction l r (.trans before after) x := by
  refine Quotient.inductionOn x ?_
  intro F
  exact Quotient.sound ⟨.compLeft before after F⟩

theorem selectedUnitalRight_comp (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r d e)
    (after : SevenRewrite W l r e f₆)
    (x : Quotient (selectedUnitalBoundarySetoid W l r c d)) :
    selectedUnitalRightAction l r after
        (selectedUnitalRightAction l r before x) =
      selectedUnitalRightAction l r (.trans before after) x := by
  refine Quotient.inductionOn x ?_
  intro F
  exact Quotient.sound ⟨.compRight before after F⟩

/-- Opposite-side interchange was established by an actual old
doubleWhisker; no new interchange rule is introduced here. -/
theorem selectedUnital_actions_commute (l r : W) {w z : W}
    {b c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (after : SevenRewrite W l r d e)
    (x : Quotient (selectedUnitalBoundarySetoid W l r c d)) :
    selectedUnitalLeftAction l r before
        (selectedUnitalRightAction l r after x) =
      selectedUnitalRightAction l r after
        (selectedUnitalLeftAction l r before x) := by
  refine Quotient.inductionOn x ?_
  intro F
  exact Quotient.sound
    ⟨.previous (.previous (.doubleWhisker before F.H after))⟩

/-- No equality of old raw packet data follows from the unit law. -/
theorem selectedUnital_unitLeft_rawDistinct (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d) :
    contextFramePack l r (contextFrameLeft l r (.refl c) F) ≠
      contextFramePack l r F := by
  intro h
  have ht := congrArg (contextTraceLength l r) h
  change Nat.succ (contextTraceLength l r (contextFramePack l r F)) =
    contextTraceLength l r (contextFramePack l r F) at ht
  omega

/-- Actual original exchangeUnit supplies an inhabited 11D packet,
rather than quantifying over a possibly empty abstract context. -/
def selectedUnitalOriginalWitness (l r : W) : FramedEleven W l r :=
  contextFramePack l r
    (contextFrameOfRaw l r (MixedExchangeUnitElevenCell.exchangeUnit))

theorem selectedUnital_contextQuotient_notInjective (l r : W) :
    ¬ Function.Injective (contextToSelectedUnital l r) := by
  intro hinj
  let F := contextFrameOfRaw l r (MixedExchangeUnitElevenCell.exchangeUnit)
  have hOld :
      contextClosedClass l r
          (contextFramePack l r (contextFrameLeft l r (.refl _) F)) ≠
        contextClosedClass l r (contextFramePack l r F) := by
    intro h
    have ht := congrArg (contextClosedTraceLength l r) h
    change Nat.succ (contextTraceLength l r (contextFramePack l r F)) =
      contextTraceLength l r (contextFramePack l r F) at ht
    omega
  apply hOld
  apply hinj
  change selectedUnitalClass l r
      (contextFramePack l r (contextFrameLeft l r (.refl _) F)) =
    selectedUnitalClass l r (contextFramePack l r F)
  exact Quotient.sound ⟨.unitLeft F⟩

/-- The old v5.26 total length is genuinely LOST at the selected quotient.
Raw length still exists on every original packet. -/
theorem selectedUnital_noLengthDescent (l r : W) :
    ¬ (∃ observe : Quotient (selectedUnitalSetoid W l r) → Nat,
      ∀ F, observe (selectedUnitalClass l r F) = contextTraceLength l r F) := by
  rintro ⟨observe, onClass⟩
  let F := contextFrameOfRaw l r (MixedExchangeUnitElevenCell.exchangeUnit)
  have h : selectedUnitalClass l r
        (contextFramePack l r (contextFrameLeft l r (.refl _) F)) =
      selectedUnitalClass l r (contextFramePack l r F) :=
    Quotient.sound ⟨.unitLeft F⟩
  have ht := congrArg observe h
  rw [onClass _, onClass _] at ht
  change Nat.succ (contextTraceLength l r (contextFramePack l r F)) =
    contextTraceLength l r (contextFramePack l r F) at ht
  omega

/-- The genuine three original 10D-event observers SURVIVE all ten
selected constructors, even though the total whisker wrapper count does not. -/
theorem selectedUnital_preservesCounts (l r : W)
    {F G : FramedEleven W l r}
    (T : SelectedUnitalCompositionTwelve W l r F G) :
    framedContextEventCounts l r F = framedContextEventCounts l r G := by
  induction T with
  | strict F => rfl
  | previous T => exact contextClosed_preservesEventCounts l r T
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'
  | whiskerLeft before F G T ih => exact ih
  | whiskerRight F G T after ih => exact ih
  | unitLeft F => rfl
  | unitRight F => rfl
  | compLeft before after F => rfl
  | compRight before after F => rfl

def selectedUnitalEventCounts (l r : W) :
    Quotient (selectedUnitalSetoid W l r) → Nat × Nat × Nat :=
  Quotient.lift (framedContextEventCounts l r) (by
    intro F G h
    rcases h with ⟨T⟩
    exact selectedUnital_preservesCounts l r T)

theorem selectedUnitalEventCounts_onClass (l r : W)
    (F : FramedEleven W l r) :
    selectedUnitalEventCounts l r (selectedUnitalClass l r F) =
      framedContextEventCounts l r F := rfl

/-- The old tenSymm event obstruction is not washed away by the chosen
unit/composition completion. -/
theorem selectedUnital_retainsTenSymmObstruction (l r : W) :
    ¬ Nonempty (SelectedUnitalCompositionTwelve W l r
      (framedOriginalTenSymmCriticalLoop l r)
      (framedOriginalTenSymmCriticalRefl l r)) := by
  rintro ⟨T⟩
  have h := congrArg (fun n : Nat × Nat × Nat => n.2.2)
    (selectedUnital_preservesCounts l r T)
  change (1 : Nat) = 0 at h
  cases h

/-- Old 6D source witnesses remain in their distinct original Types,
and v5.25's quotient classification is strictly coarsened. -/
theorem selectedUnital_strictCompletion (l r : W) :
    (¬ Function.Injective (contextToSelectedUnital l r)) ∧
    (¬ ∃ observe : Quotient (selectedUnitalSetoid W l r) → Nat,
      ∀ F, observe (selectedUnitalClass l r F) = contextTraceLength l r F) ∧
    (¬ Nonempty (SelectedUnitalCompositionTwelve W l r
      (framedOriginalTenSymmCriticalLoop l r)
      (framedOriginalTenSymmCriticalRefl l r))) :=
  ⟨selectedUnital_contextQuotient_notInjective l r,
    selectedUnital_noLengthDescent l r,
    selectedUnital_retainsTenSymmObstruction l r⟩

#print axioms PentagonAdjoinedSixCell.SelectedUnitalCompositionTwelve
#print axioms PentagonAdjoinedSixCell.selectedUnital_previous_injective
#print axioms PentagonAdjoinedSixCell.IsSelectedUnitalCongruence
#print axioms PentagonAdjoinedSixCell.selectedUnital_least
#print axioms PentagonAdjoinedSixCell.selectedUnitalSetoid
#print axioms PentagonAdjoinedSixCell.selectedUnitalClass
#print axioms PentagonAdjoinedSixCell.selectedUnitalClass_eq_iff
#print axioms PentagonAdjoinedSixCell.contextToSelectedUnital
#print axioms PentagonAdjoinedSixCell.contextToSelectedUnital_onClass
#print axioms PentagonAdjoinedSixCell.selectedUnitalBoundarySetoid
#print axioms PentagonAdjoinedSixCell.selectedUnitalLeftAction
#print axioms PentagonAdjoinedSixCell.selectedUnitalRightAction
#print axioms PentagonAdjoinedSixCell.selectedUnitalLeft_unit
#print axioms PentagonAdjoinedSixCell.selectedUnitalRight_unit
#print axioms PentagonAdjoinedSixCell.selectedUnitalLeft_comp
#print axioms PentagonAdjoinedSixCell.selectedUnitalRight_comp
#print axioms PentagonAdjoinedSixCell.selectedUnital_actions_commute
#print axioms PentagonAdjoinedSixCell.selectedUnital_unitLeft_rawDistinct
#print axioms PentagonAdjoinedSixCell.selectedUnitalOriginalWitness
#print axioms PentagonAdjoinedSixCell.selectedUnital_contextQuotient_notInjective
#print axioms PentagonAdjoinedSixCell.selectedUnital_noLengthDescent
#print axioms PentagonAdjoinedSixCell.selectedUnital_preservesCounts
#print axioms PentagonAdjoinedSixCell.selectedUnitalEventCounts
#print axioms PentagonAdjoinedSixCell.selectedUnitalEventCounts_onClass
#print axioms PentagonAdjoinedSixCell.selectedUnital_retainsTenSymmObstruction
#print axioms PentagonAdjoinedSixCell.selectedUnital_strictCompletion

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
