import KUOS.Architecture.QiWuxingGK5CHP77ContextClosedTwelfthV5_25

/-!
Qi v5.26: strict unit and same-side composition obstructions for
the genuine context-closed twelfth quotient of v5.25.

Unlike the ordered raw trace and v5.24's drop-two suffix, raw tenth
WHISKERING TRACE LENGTH is unchanged by every comparison constructor
of the NEW context-closed twelfth grammar: original 12D comparisons,
actual double-whisker, reverse/chain and both typed outer contexts.

The preserved length descends to the global v5.25 quotient and each
fixed-six-boundary quotient. Genuine left/right context application
increases it by exactly one, including when the context is a reflexive
old seventh-cell witness. Consequently those reflexive witnesses are
NOT identity actions on any inhabited boundary fiber. Two successive
same-side context operations are NOT strictly equal on the new
quotient to a single composite original seventh-cell context:
the observed lengths differ by one.

Opposite-side commutation from v5.25 is retained, not weakened. This
module adds no original or selected comparison constructor and does
not assert that a future unit/composition-completed presentation is
impossible. No classical choice of proof representatives is used.
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

/-- Total number of raw left/right whisker events at the original 10D source. -/
def contextTraceLength (l r : W) (F : FramedEleven W l r) : Nat :=
  (framedWhiskerRawTrace F).length

/-- Original full-framed twelfth comparisons preserve event length
even though they may swap the first two events. -/
theorem framedDoubleWhisker_preservesTraceLength (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedDoubleWhiskerTwelveCell W l r F G) :
    contextTraceLength l r F = contextTraceLength l r G := by
  induction T with
  | strict F => rfl
  | previous T => rfl
  | doubleWhisker before H after => rfl
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'

/-- New 12D outer-whiskering rules prepend the SAME single event
on both sides. Unlike ordered trace, length therefore remains equal. -/
theorem contextClosed_preservesTraceLength (l r : W)
    {F G : FramedEleven W l r}
    (T : ContextClosedFramedTwelve W l r F G) :
    contextTraceLength l r F = contextTraceLength l r G := by
  induction T with
  | strict F => rfl
  | previous T => exact framedDoubleWhisker_preservesTraceLength l r T
  | reverse T ih => exact ih.symm
  | chain T U ih ih' => exact ih.trans ih'
  | whiskerLeft before F G T ih =>
      change Nat.succ (contextTraceLength l r (contextFramePack l r F)) =
        Nat.succ (contextTraceLength l r (contextFramePack l r G))
      exact congrArg Nat.succ ih
  | whiskerRight F G T after ih =>
      change Nat.succ (contextTraceLength l r (contextFramePack l r F)) =
        Nat.succ (contextTraceLength l r (contextFramePack l r G))
      exact congrArg Nat.succ ih

/-- Globally retained invariant on the independent context-closed quotient. -/
def contextClosedTraceLength (l r : W) :
    Quotient (contextClosedSetoid W l r) → Nat :=
  Quotient.lift (contextTraceLength l r) (by
    intro F G h
    rcases h with ⟨T⟩
    exact contextClosed_preservesTraceLength l r T)

theorem contextClosedTraceLength_onClass (l r : W)
    (F : FramedEleven W l r) :
    contextClosedTraceLength l r (contextClosedClass l r F) =
      contextTraceLength l r F := rfl

/-- The original v5.18 full quotient has the SAME invariant. -/
def originalFramedTraceLength (l r : W) :
    Quotient (framedDoubleWhiskerSetoid W l r) → Nat :=
  Quotient.lift (contextTraceLength l r) (by
    intro F G h
    rcases h with ⟨T⟩
    exact framedDoubleWhisker_preservesTraceLength l r T)

theorem originalFramedTraceLength_onClass (l r : W)
    (F : FramedEleven W l r) :
    originalFramedTraceLength l r (framedDoubleWhiskerClass F) =
      contextTraceLength l r F := rfl

/-- The noninjective old-to-new quotient map preserves the event
length even though the ordered tail no longer descends. -/
theorem contextClosedTraceLength_factorsOld (l r : W)
    (q : Quotient (framedDoubleWhiskerSetoid W l r)) :
    contextClosedTraceLength l r (oldToContextClosedQuotient l r q) =
      originalFramedTraceLength l r q := by
  refine Quotient.inductionOn q ?_
  intro F
  rfl

/-- The exact original 6D boundaries still index every fiber. -/
def contextBoundaryTraceLength (l r : W) {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    Quotient (contextBoundarySetoid W l r c d) → Nat :=
  Quotient.lift
    (fun F : ContextFrameEleven W l r c d =>
      contextTraceLength l r (contextFramePack l r F)) (by
      intro F G h
      rcases h with ⟨T⟩
      exact contextClosed_preservesTraceLength l r T)

/-- An actual left context adds exactly one raw tenth whisker event. -/
theorem contextLeftAction_traceLength (l r : W) {w z : W}
    {b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r b c)
    (q : Quotient (contextBoundarySetoid W l r c d)) :
    contextBoundaryTraceLength l r b d
      (contextClosedLeftAction l r before q) =
      Nat.succ (contextBoundaryTraceLength l r c d q) := by
  refine Quotient.inductionOn q ?_
  intro F
  rfl

/-- An actual right context adds exactly one raw tenth whisker event. -/
theorem contextRightAction_traceLength (l r : W) {w z : W}
    {c d e : PentagonAdjoinedSixCell W l r w z}
    (after : SevenRewrite W l r d e)
    (q : Quotient (contextBoundarySetoid W l r c d)) :
    contextBoundaryTraceLength l r c e
      (contextClosedRightAction l r after q) =
      Nat.succ (contextBoundaryTraceLength l r c d q) := by
  refine Quotient.inductionOn q ?_
  intro F
  rfl

/-- Reflexive seventh-cell syntax is NOT a strict identity left
action on any inhabited exact six-boundary fiber. -/
theorem contextLeftReflexive_notIdentity (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d) :
    contextClosedLeftAction l r (.refl c) (Quotient.mk _ F) ≠
      (Quotient.mk _ F : Quotient (contextBoundarySetoid W l r c d)) := by
  intro he
  have h := congrArg (contextBoundaryTraceLength l r c d) he
  change Nat.succ (contextTraceLength l r (contextFramePack l r F)) =
    contextTraceLength l r (contextFramePack l r F) at h
  omega

theorem contextRightReflexive_notIdentity (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d) :
    contextClosedRightAction l r (.refl d) (Quotient.mk _ F) ≠
      (Quotient.mk _ F : Quotient (contextBoundarySetoid W l r c d)) := by
  intro he
  have h := congrArg (contextBoundaryTraceLength l r c d) he
  change Nat.succ (contextTraceLength l r (contextFramePack l r F)) =
    contextTraceLength l r (contextFramePack l r F) at h
  omega

/-- Two same-side left contexts have TWO events; one composite
original seventh word, though correctly typed, has only ONE event. -/
theorem contextLeftAction_compositionGap (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r a b)
    (after : SevenRewrite W l r b c)
    (F : ContextFrameEleven W l r c d) :
    contextClosedLeftAction l r before
        (contextClosedLeftAction l r after (Quotient.mk _ F)) ≠
      contextClosedLeftAction l r (.trans before after)
        (Quotient.mk _ F) := by
  intro he
  have h := congrArg (contextBoundaryTraceLength l r a d) he
  change Nat.succ (Nat.succ
      (contextTraceLength l r (contextFramePack l r F))) =
    Nat.succ (contextTraceLength l r (contextFramePack l r F)) at h
  omega

/-- Same strict failure for two successive original right contexts. -/
theorem contextRightAction_compositionGap (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r d e)
    (after : SevenRewrite W l r e f₆)
    (F : ContextFrameEleven W l r c d) :
    contextClosedRightAction l r after
        (contextClosedRightAction l r before (Quotient.mk _ F)) ≠
      contextClosedRightAction l r (.trans before after)
        (Quotient.mk _ F) := by
  intro he
  have h := congrArg (contextBoundaryTraceLength l r c f₆) he
  change Nat.succ (Nat.succ
      (contextTraceLength l r (contextFramePack l r F))) =
    Nat.succ (contextTraceLength l r (contextFramePack l r F)) at h
  omega

/-- Each inhabited exact fiber refutes global unitality of its
left action; a formal reflexive context is not a proof of a unit law. -/
theorem contextLeftAction_noUniversalUnit (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d) :
    ¬ (∀ q : Quotient (contextBoundarySetoid W l r c d),
      contextClosedLeftAction l r (.refl c) q = q) := by
  intro h
  exact contextLeftReflexive_notIdentity l r F (h _)

theorem contextRightAction_noUniversalUnit (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (F : ContextFrameEleven W l r c d) :
    ¬ (∀ q : Quotient (contextBoundarySetoid W l r c d),
      contextClosedRightAction l r (.refl d) q = q) := by
  intro h
  exact contextRightReflexive_notIdentity l r F (h _)

#print axioms PentagonAdjoinedSixCell.contextTraceLength
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_preservesTraceLength
#print axioms PentagonAdjoinedSixCell.contextClosed_preservesTraceLength
#print axioms PentagonAdjoinedSixCell.contextClosedTraceLength
#print axioms PentagonAdjoinedSixCell.contextClosedTraceLength_onClass
#print axioms PentagonAdjoinedSixCell.originalFramedTraceLength
#print axioms PentagonAdjoinedSixCell.originalFramedTraceLength_onClass
#print axioms PentagonAdjoinedSixCell.contextClosedTraceLength_factorsOld
#print axioms PentagonAdjoinedSixCell.contextBoundaryTraceLength
#print axioms PentagonAdjoinedSixCell.contextLeftAction_traceLength
#print axioms PentagonAdjoinedSixCell.contextRightAction_traceLength
#print axioms PentagonAdjoinedSixCell.contextLeftReflexive_notIdentity
#print axioms PentagonAdjoinedSixCell.contextRightReflexive_notIdentity
#print axioms PentagonAdjoinedSixCell.contextLeftAction_compositionGap
#print axioms PentagonAdjoinedSixCell.contextRightAction_compositionGap
#print axioms PentagonAdjoinedSixCell.contextLeftAction_noUniversalUnit
#print axioms PentagonAdjoinedSixCell.contextRightAction_noUniversalUnit

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
