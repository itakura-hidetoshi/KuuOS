import KUOS.Architecture.QiWuxingGK5CHP77EighthToEleventhConditionalTransportV5_20

/-!
Qi v5.21 — actual ORIGINAL inverse-context transport at eighth,
ninth, tenth, eleventh AND twelfth proof levels.

Unlike v5.20's fixed-six-cell TraceFaithfulHigherTower,
inverseContext genuinely changes the original underlying six-cell
boundary (w→z becomes z→w, c becomes symm c). It cannot be a
literal eighth-cell comparison between differently indexed seventh
proofs, nor can it be obtained by equating original raw indices.

Every level of transport is already an ORIGINAL constructor:
SevenRewrite.congrInv, PentagonAssocEightCell.inverseContext,
MixedCancelNineCell.inverseContext, MixedUnitAssocTenCell.inverseContext,
MixedExchangeUnitElevenCell.inverseContext, and
MixedExchangeInverseTwelveCell.inverseContext.
The new implementation merely packages and verifies their actual
dependent composition and preserves the ordered tenth raw trace.
The inherited-only twelfth grammar admits this context action.

On genuine reflexive original sixth-cell inputs, transport yields a
provably different raw framed packet, while its trace is unchanged.
No v5.20 fixed-six-cell tower can realize the new contextual packet.
Original left/right whiskering instead adds a nonempty trace prefix;
this intrinsic trace defect is never silently deleted.

No universal nontrivial eighth associator → transport or all-framed
twelfth naturality is claimed; only the old-only comparison grammar
is propagated. No previous source Type or constructor is altered.
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

/-- A genuinely nonidentity dependent context action on the entire
ORIGINAL raw sixth-to-eleventh proof packet. Each field is an
original inverseContext/congrInv constructor, not a retyped Eq. -/
def inverseContextTransportFrame (l r : W)
    (F : FramedEleven W l r) : FramedEleven W l r :=
  { w := F.z, z := F.w,
    c := .symm F.c, d := .symm F.d,
    s := .congrInv F.s, t := .congrInv F.t,
    q₀ := .inverseContext F.q₀,
    q₁ := .inverseContext F.q₁,
    alpha := .inverseContext F.alpha,
    beta := .inverseContext F.beta,
    xi := .inverseContext F.xi,
    zeta := .inverseContext F.zeta,
    H := .inverseContext F.H }

/-- Its action on a fixed original proof is exactly the original
eleventh inverse-context constructor, with all indices retained. -/
theorem inverseContextTransportFrame_onRaw (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    inverseContextTransportFrame l r (framedEleven_ofRaw l r H) =
      framedEleven_ofRaw l r (.inverseContext H) := rfl

/-- Every raw tenth-level ordered whisker event is preserved by
the actual inverse-context original ten-cell constructor. -/
theorem inverseContextTransportFrame_preservesTrace (l r : W)
    (F : FramedEleven W l r) :
    framedWhiskerRawTrace (inverseContextTransportFrame l r F) =
      framedWhiskerRawTrace F := rfl

/-- Repeating the actual inverse-context operation preserves
the trace again, without falsely identifying raw double inverses. -/
theorem inverseContextTransportFrame_twice_preservesTrace (l r : W)
    (F : FramedEleven W l r) :
    framedWhiskerRawTrace
        (inverseContextTransportFrame l r
          (inverseContextTransportFrame l r F)) =
      framedWhiskerRawTrace F := by
  exact (inverseContextTransportFrame_preservesTrace l r
      (inverseContextTransportFrame l r F)).trans
    (inverseContextTransportFrame_preservesTrace l r F)

/-- A true ORIGINAL v5.17 twelfth proof transports naturally
through the existing twelfth inverse-context constructor. The
result remains a genuine original proof in the moved fiber. -/
def inverseContextOldTwelfth (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    {H K : MixedExchangeUnitElevenCell W l r xi zeta}
    (T : MixedExchangeInverseTwelveCell W l r H K) :
    FramedInheritedTwelfth W l r
      (inverseContextTransportFrame l r (framedEleven_ofRaw l r H))
      (inverseContextTransportFrame l r (framedEleven_ofRaw l r K)) := by
  change FramedInheritedTwelfth W l r
    (framedEleven_ofRaw l r (.inverseContext H))
    (framedEleven_ofRaw l r (.inverseContext K))
  exact .previous (.inverseContext T)

/-- The inherited-only grammar (and ONLY that restricted grammar)
is closed under the entire context operation. No extra primitive. -/
def inverseContextInheritedTwelfth (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedInheritedTwelfth W l r F G) :
    FramedInheritedTwelfth W l r
      (inverseContextTransportFrame l r F)
      (inverseContextTransportFrame l r G) := by
  induction T with
  | strict F =>
      exact .strict _
  | previous T =>
      exact inverseContextOldTwelfth l r T
  | reverse T ih =>
      exact .reverse ih
  | chain T U ih ih' =>
      exact .chain ih ih'

/-- Consequent descent for genuine old-only comparisons;
this is NOT a universal action on the newer doubleWhisker rule. -/
theorem inverseContextInheritedTwelfth_exists (l r : W)
    (F G : FramedEleven W l r)
    (h : Nonempty (FramedInheritedTwelfth W l r F G)) :
    Nonempty (FramedInheritedTwelfth W l r
      (inverseContextTransportFrame l r F)
      (inverseContextTransportFrame l r G)) := by
  rcases h with ⟨T⟩
  exact ⟨inverseContextInheritedTwelfth l r T⟩

/-- Genuine old-only transported comparisons embed in the actual
v5.18 full framed grammar via its existing previous inclusion. -/
theorem inverseContextInheritedTwelfth_toFull (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedInheritedTwelfth W l r F G) :
    Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (inverseContextTransportFrame l r F)
      (inverseContextTransportFrame l r G)) :=
  ⟨framedInheritedTwelfth_toFull l r
    (inverseContextInheritedTwelfth l r T)⟩

/-- The outer constructor of the ORIGINAL six-cell source is a
fully well-typed observable on a framed packet, independent of
the chosen v5.18 twelfth quotient. -/
def frameSourceSixInverseTag (l r : W)
    (F : FramedEleven W l r) : Bool :=
  match F.c with
  | .symm _ => true
  | _ => false

/-- At genuine original reflexive six-cell boundaries, the new
context action is not identity on RAW FramedEleven terms. -/
theorem inverseContextFrame_nonidentityAtRefl (l r : W)
    (w : W)
    {s t : SevenRewrite W l r (.refl w) (.refl w)}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    inverseContextTransportFrame l r (framedEleven_ofRaw l r H) ≠
      framedEleven_ofRaw l r H := by
  intro h
  have ht := congrArg (frameSourceSixInverseTag l r) h
  change (true : Bool) = false at ht
  cases ht

/-- The v5.20 fixed-six-cell tower cannot realize inverse-context
transport on genuine original reflexive source six-cell packets.
The obstruction is the untouched original SIXTH index, not merely
the higher trace. -/
theorem inverseContextFrame_notFixedSixTower (l r : W)
    (w : W)
    {s t : SevenRewrite W l r (.refl w) (.refl w)}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    {s' t' : SevenRewrite W l r (.refl w) (.refl w)}
    (A : TraceFaithfulHigherTower W l r s t s' t') :
    traceFaithfulTowerTransportFrame l r A H ≠
      inverseContextTransportFrame l r (framedEleven_ofRaw l r H) := by
  intro h
  have ht := congrArg (frameSourceSixInverseTag l r) h
  change (false : Bool) = true at ht
  cases ht

/-- A concrete ORIGINAL (not ad hoc uninhabited) reflexive
sixth–eleventh packet, constructed by the actual original
higher reflexivity constructors. -/
def originalReflexiveElevenFrame (l r w : W) :
    FramedEleven W l r :=
  let c : PentagonAdjoinedSixCell W l r w w := .refl w
  let s : SevenRewrite W l r c c := .refl c
  let q : PentagonAssocEightCell W l r s s :=
    pentagonAssocEightCell_refl s
  let alpha : MixedCancelNineCell W l r q q :=
    mixedCancelNineCell_refl q
  let xi : MixedUnitAssocTenCell W l r alpha alpha :=
    mixedUnitAssocTenCell_refl alpha
  let H : MixedExchangeUnitElevenCell W l r xi xi := .strict rfl
  framedEleven_ofRaw l r H

/-- A fully inhabited concrete raw nonidentity and simultaneously
the preservation of the complete tenth whiskering trace. -/
theorem originalReflexive_inverseContext_nonidentity (l r w : W) :
    inverseContextTransportFrame l r
        (originalReflexiveElevenFrame l r w) ≠
      originalReflexiveElevenFrame l r w ∧
    framedWhiskerRawTrace
        (inverseContextTransportFrame l r
          (originalReflexiveElevenFrame l r w)) =
      framedWhiskerRawTrace (originalReflexiveElevenFrame l r w) := by
  constructor
  · intro h
    have ht := congrArg (frameSourceSixInverseTag l r) h
    change (true : Bool) = false at ht
    cases ht
  · exact inverseContextTransportFrame_preservesTrace l r _

/-- ORIGINAL left whiskering has a genuinely NEW ordered tenth
prefix: this is an exact formula, not a chosen quotient count. -/
theorem originalLeftWhisker_tracePrefix (l r : W)
    {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta) :
    mixedTenWhiskerRawTrace (.whiskerLeft before xi) =
      false :: mixedTenWhiskerRawTrace xi := rfl

/-- ORIGINAL right whiskering has the opposite new prefix. -/
theorem originalRightWhisker_tracePrefix (l r : W)
    {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta)
    (after : SevenRewrite W l r d e) :
    mixedTenWhiskerRawTrace (.whiskerRight xi after) =
      true :: mixedTenWhiskerRawTrace xi := rfl

/-- One new event cannot equal the untouched finite raw trace,
regardless of the input. No cancellation of witness history. -/
theorem originalLeftWhisker_traceObstruction (l r : W)
    {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta) :
    mixedTenWhiskerRawTrace (.whiskerLeft before xi) ≠
      mixedTenWhiskerRawTrace xi := by
  intro h
  have hl := congrArg List.length h
  change (mixedTenWhiskerRawTrace xi).length + 1 =
    (mixedTenWhiskerRawTrace xi).length at hl
  omega

theorem originalRightWhisker_traceObstruction (l r : W)
    {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    (xi : MixedUnitAssocTenCell W l r alpha beta)
    (after : SevenRewrite W l r d e) :
    mixedTenWhiskerRawTrace (.whiskerRight xi after) ≠
      mixedTenWhiskerRawTrace xi := by
  intro h
  have hl := congrArg List.length h
  change (mixedTenWhiskerRawTrace xi).length + 1 =
    (mixedTenWhiskerRawTrace xi).length at hl
  omega

#print axioms PentagonAdjoinedSixCell.inverseContextTransportFrame
#print axioms PentagonAdjoinedSixCell.inverseContextTransportFrame_onRaw
#print axioms PentagonAdjoinedSixCell.inverseContextTransportFrame_preservesTrace
#print axioms PentagonAdjoinedSixCell.inverseContextTransportFrame_twice_preservesTrace
#print axioms PentagonAdjoinedSixCell.inverseContextOldTwelfth
#print axioms PentagonAdjoinedSixCell.inverseContextInheritedTwelfth
#print axioms PentagonAdjoinedSixCell.inverseContextInheritedTwelfth_exists
#print axioms PentagonAdjoinedSixCell.inverseContextInheritedTwelfth_toFull
#print axioms PentagonAdjoinedSixCell.frameSourceSixInverseTag
#print axioms PentagonAdjoinedSixCell.inverseContextFrame_nonidentityAtRefl
#print axioms PentagonAdjoinedSixCell.inverseContextFrame_notFixedSixTower
#print axioms PentagonAdjoinedSixCell.originalReflexiveElevenFrame
#print axioms PentagonAdjoinedSixCell.originalReflexive_inverseContext_nonidentity
#print axioms PentagonAdjoinedSixCell.originalLeftWhisker_tracePrefix
#print axioms PentagonAdjoinedSixCell.originalRightWhisker_tracePrefix
#print axioms PentagonAdjoinedSixCell.originalLeftWhisker_traceObstruction
#print axioms PentagonAdjoinedSixCell.originalRightWhisker_traceObstruction

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
