import KUOS.Architecture.QiWuxingGK5CHP77FramedExactFiberDescentV5_19

/-!
Qi v5.20: conditional higher transport from genuine eighth-cell
boundary associators through original ninth, tenth and eleventh
proof families. No eighth associator is promoted to an equality.

A trace-faithful tower is explicit extra typed DATA: two original
eighth-cell boundary comparisons, an eighth-proof map, dependent
ninth/tenth/eleventh-proof maps, and preservation of the ORIGINAL
ordered tenth-whisker trace. It is not derived solely from the
associators. The identity and composition of such towers are
constructed and their actions on original proof packets verified.

If a genuine old twelfth comparison is subsequently provided on
the TRANSPORTED original eleventh fiber, it embeds into the old-only
and full framed twelfth comparisons. There is no claim of an old
twelfth comparison between the unequal original input/output fibers.

The actual double-whisker critical peak has two original eighth
associators but opposite raw tenth-context prefixes. No trace-faithful
tower can realize its right-after-left output from its
left-after-right input, for ANY original typed context.
This is a conditional obstruction, not universal higher thinness.
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

/-- Original eighth associators are only boundary comparisons.
Actual transport of ninth/ten/eleventh proof Type-values requires
separate dependent maps, one at EACH level. The final condition is
conservation of the original ordered tenth-level context trace. -/
structure TraceFaithfulHigherTower (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    (s t s' t' : SevenRewrite W l r c d) : Type uSix where
  sourceEight : EightCell W l r s s'
  targetEight : EightCell W l r t t'
  moveEight :
    PentagonAssocEightCell W l r s t →
      PentagonAssocEightCell W l r s' t'
  moveNine :
    ∀ {q q' : PentagonAssocEightCell W l r s t},
      MixedCancelNineCell W l r q q' →
        MixedCancelNineCell W l r (moveEight q) (moveEight q')
  moveTen :
    ∀ {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'},
      MixedUnitAssocTenCell W l r alpha beta →
        MixedUnitAssocTenCell W l r
          (moveNine alpha) (moveNine beta)
  moveEleven :
    ∀ {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta},
      MixedExchangeUnitElevenCell W l r xi zeta →
        MixedExchangeUnitElevenCell W l r
          (moveTen xi) (moveTen zeta)
  preserveTenthTrace :
    ∀ {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      (xi : MixedUnitAssocTenCell W l r alpha beta),
      mixedTenWhiskerRawTrace (moveTen xi) =
        mixedTenWhiskerRawTrace xi

/-- The genuinely original eighth reflexivity constructors and
identity maps at every proof level form an explicit identity tower. -/
def traceFaithfulTowerId (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    (s t : SevenRewrite W l r c d) :
    TraceFaithfulHigherTower W l r s t s t where
  sourceEight := .reflexive s
  targetEight := .reflexive t
  moveEight := fun q => q
  moveNine := by
    intro q q' P
    exact P
  moveTen := by
    intro q q' alpha beta T
    exact T
  moveEleven := by
    intro q q' alpha beta xi zeta H
    exact H
  preserveTenthTrace := by
    intro q q' alpha beta xi
    rfl

/-- Tower composition transports actual ninth, tenth and eleventh
raw proof terms, and does not replace any with an untyped witness.
Its eighth boundaries compose by the ORIGINAL eighth-cell chain. -/
def traceFaithfulTowerComp (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    {s t s' t' s'' t'' : SevenRewrite W l r c d}
    (A : TraceFaithfulHigherTower W l r s t s' t')
    (B : TraceFaithfulHigherTower W l r s' t' s'' t'') :
    TraceFaithfulHigherTower W l r s t s'' t'' where
  sourceEight := .chain A.sourceEight B.sourceEight
  targetEight := .chain A.targetEight B.targetEight
  moveEight := fun q => B.moveEight (A.moveEight q)
  moveNine := by
    intro q q' P
    exact B.moveNine (A.moveNine P)
  moveTen := by
    intro q q' alpha beta T
    exact B.moveTen (A.moveTen T)
  moveEleven := by
    intro q q' alpha beta xi zeta H
    exact B.moveEleven (A.moveEleven H)
  preserveTenthTrace := by
    intro q q' alpha beta xi
    exact (B.preserveTenthTrace (A.moveTen xi)).trans
      (A.preserveTenthTrace xi)

/-- The tower acts on the ORIGINAL type-indexed eleventh witness.
Its output is a new faithful framed packet in the target lower
fiber, not an equality of that packet with the source packet. -/
def traceFaithfulTowerTransportFrame (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    {s t s' t' : SevenRewrite W l r c d}
    (A : TraceFaithfulHigherTower W l r s t s' t')
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    FramedEleven W l r :=
  { w := w, z := z, c := c, d := d,
    s := s', t := t',
    q₀ := A.moveEight q, q₁ := A.moveEight q',
    alpha := A.moveNine alpha, beta := A.moveNine beta,
    xi := A.moveTen xi, zeta := A.moveTen zeta,
    H := A.moveEleven H }

/-- The transported original tenth trace is identical, by the
explicit compatibility certificate, not by an eighth associator. -/
theorem traceFaithfulTowerTransportFrame_preservesTrace (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t s' t' : SevenRewrite W l r c d}
    (A : TraceFaithfulHigherTower W l r s t s' t')
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    framedWhiskerRawTrace (traceFaithfulTowerTransportFrame l r A H) =
      mixedTenWhiskerRawTrace xi :=
  A.preserveTenthTrace xi

/-- Identity transports the entire original proof packet exactly. -/
theorem traceFaithfulTowerTransportFrame_id (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    traceFaithfulTowerTransportFrame l r
      (traceFaithfulTowerId l r s t) H =
        framedEleven_ofRaw l r H := rfl

/-- The action on raw 11D packets composes definitionally; no
additional higher coherence axiom or quotient Eq is introduced. -/
theorem traceFaithfulTowerTransportFrame_comp (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t s' t' s'' t'' : SevenRewrite W l r c d}
    (A : TraceFaithfulHigherTower W l r s t s' t')
    (B : TraceFaithfulHigherTower W l r s' t' s'' t'')
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta) :
    traceFaithfulTowerTransportFrame l r
      (traceFaithfulTowerComp l r A B) H =
    traceFaithfulTowerTransportFrame l r B (A.moveEleven H) := rfl

/-- POSITIVE CONDITIONAL DESCENT: once a genuine v5.17 original
twelfth proof is supplied in the MOVED original 11D fiber, it is
valid in the inherited-only framed grammar. This does not claim
old-fiber descent from the original input packet. -/
def traceFaithfulTowerOldTwelfth (l r : W) {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    {s t s' t' : SevenRewrite W l r c d}
    (A : TraceFaithfulHigherTower W l r s t s' t')
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (K : MixedExchangeUnitElevenCell W l r
      (A.moveTen xi) (A.moveTen zeta))
    (C : MixedExchangeInverseTwelveCell W l r (A.moveEleven H) K) :
    FramedInheritedTwelfth W l r
      (traceFaithfulTowerTransportFrame l r A H)
      (framedEleven_ofRaw l r K) := by
  change FramedInheritedTwelfth W l r
    (framedEleven_ofRaw l r (A.moveEleven H))
    (framedEleven_ofRaw l r K)
  exact .previous C

/-- The transported old twelfth comparison also enters the
v5.18 full framed grammar, with no new equality interpretation. -/
theorem traceFaithfulTowerOldTwelfth_toFull (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t s' t' : SevenRewrite W l r c d}
    (A : TraceFaithfulHigherTower W l r s t s' t')
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (K : MixedExchangeUnitElevenCell W l r
      (A.moveTen xi) (A.moveTen zeta))
    (C : MixedExchangeInverseTwelveCell W l r (A.moveEleven H) K) :
    Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (traceFaithfulTowerTransportFrame l r A H)
      (framedEleven_ofRaw l r K)) :=
  ⟨framedInheritedTwelfth_toFull l r
    (traceFaithfulTowerOldTwelfth l r A H K C)⟩

/-- NEGATIVE: even with two actual eighth associators, a tower
that conserves the original ordered tenth trace cannot send the
left-after-right original proof packet to the right-after-left one.
This is for ALL original sixth–eleventh source terms. -/
theorem doubleWhisker_noTraceFaithfulTower (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    ¬ ∃ (A : TraceFaithfulHigherTower W l r
        (.trans before (.trans s after))
        (.trans before (.trans t after))
        (.trans (.trans before s) after)
        (.trans (.trans before t) after)),
      traceFaithfulTowerTransportFrame l r A
        (doubleWhiskerLeftAfterRightFrame l r before H after).H =
      doubleWhiskerRightAfterLeftFrame l r before H after := by
  rintro ⟨A, h⟩
  have ht := congrArg framedWhiskerRawTrace h
  have hPreserve := traceFaithfulTowerTransportFrame_preservesTrace
    l r A (doubleWhiskerLeftAfterRightFrame l r before H after).H
  rw [hPreserve] at ht
  change false :: true :: mixedTenWhiskerRawTrace xi =
    true :: false :: mixedTenWhiskerRawTrace xi at ht
  cases ht

/-- Both true eighth associators EXIST at the peak, but the
conditional typed 8→9→10→11 transport cannot realize the swapped
raw witness while the original tenth trace is protected. -/
theorem doubleWhiskerEightCompatible_notTraceLiftable (l r : W)
    {w z : W} {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    (Nonempty (EightCell W l r
      (.trans before (.trans s after))
      (.trans (.trans before s) after)) ∧
     Nonempty (EightCell W l r
      (.trans before (.trans t after))
      (.trans (.trans before t) after))) ∧
    ¬ ∃ (A : TraceFaithfulHigherTower W l r
        (.trans before (.trans s after))
        (.trans before (.trans t after))
        (.trans (.trans before s) after)
        (.trans (.trans before t) after)),
      traceFaithfulTowerTransportFrame l r A
        (doubleWhiskerLeftAfterRightFrame l r before H after).H =
      doubleWhiskerRightAfterLeftFrame l r before H after := by
  exact ⟨doubleWhiskerBoundaryCompatibility l r before after,
    doubleWhisker_noTraceFaithfulTower l r before H after⟩

#print axioms PentagonAdjoinedSixCell.TraceFaithfulHigherTower
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerId
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerComp
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerTransportFrame
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerTransportFrame_preservesTrace
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerTransportFrame_id
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerTransportFrame_comp
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerOldTwelfth
#print axioms PentagonAdjoinedSixCell.traceFaithfulTowerOldTwelfth_toFull
#print axioms PentagonAdjoinedSixCell.doubleWhisker_noTraceFaithfulTower
#print axioms PentagonAdjoinedSixCell.doubleWhiskerEightCompatible_notTraceLiftable

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
