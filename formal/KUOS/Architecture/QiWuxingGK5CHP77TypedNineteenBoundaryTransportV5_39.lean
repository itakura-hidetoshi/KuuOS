import KUOS.Architecture.QiWuxingGK5CHP77DoubleEighteenNineteenSwapV5_38

/-!
Qi v5.39 — proof-relevant, CONDITIONAL boundary transport between
the genuinely different dependent 19D fibers of the two v5.38
double-context 18D witnesses.

The first boundary datum is a typed raw 18D map. The second is a
PROOF-VALUED action on every genuine same-fiber selected local 19D
comparison; it is deliberately stronger than merely declaring a
function on a quotient. Together they construct a valid Quotient.lift
to the distinct target 19D proof fiber. This is a sufficient descent
certificate, NOT a theorem that such a map universally exists.

An additional selected boundary condition requires an ACTUAL target
19D comparison from the transported LR proof to the original RL
proof. This produces the designated 19D class equation, the
observation-only coarse swap agreement, and a PROVEN necessary
fine-trace change. Global swap-natural compatibility is separately
typed and yields a commuting quotient-observation square. None of
these conditions identify unlike raw dependent Type values.

Every original F55/P77/GK5CG and 6D–19D value, all prior selected
presentations, the public root107 and pinned Lean/mathlib are
untouched. No axioms, sorry, heterogeneous equality or unconditional
20D gluing constructor. Append-only/tighten-only/same-root.
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

section MixedBoundary

variable (l r : W) {w z : W}
variable {a b c d : PentagonAdjoinedSixCell W l r w z}
variable (left : SevenRewrite W l r a b)
variable (F G : ContextFrameEleven W l r b c)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)
variable (right : SevenRewrite W l r c d)

/-- The source is one genuine, fixed LR 17D endpoint fiber.
This abbreviation does not erase its dependent Type indices. -/
abbrev selectedMixedLeftNineteenRaw : Type uSix :=
  SelectedContextualEighteen W l r
    (selectedSeventeenLeftAfterRight l r left F G J right)
    (selectedSeventeenLeftAfterRight l r left F G N right)

/-- Independently indexed target RL fiber of actual raw 18D terms. -/
abbrev selectedMixedRightNineteenRaw : Type uSix :=
  SelectedContextualEighteen W l r
    (selectedSeventeenRightAfterLeft l r left F G J right)
    (selectedSeventeenRightAfterLeft l r left F G N right)

/-- A source quotient is only the quotient of its ACTUAL LR fiber. -/
abbrev selectedMixedLeftNineteenQuot : Type uSix :=
  Quotient (selectedNineteenSetoid l r
    (selectedSeventeenLeftAfterRight l r left F G J right)
    (selectedSeventeenLeftAfterRight l r left F G N right))

/-- The RL target quotient is not silently unified with the LR one. -/
abbrev selectedMixedRightNineteenQuot : Type uSix :=
  Quotient (selectedNineteenSetoid l r
    (selectedSeventeenRightAfterLeft l r left F G J right)
    (selectedSeventeenRightAfterLeft l r left F G N right))

/-- Boundary descent requires a raw dependent transport and the
actual Type-valued action on LOCAL 19D comparison proofs.
There is no constructed value of this structure without additional
boundary data. -/
structure SelectedMixedNineteenBoundary : Type uSix where
  rawTransport :
    selectedMixedLeftNineteenRaw l r left F G J N right →
      selectedMixedRightNineteenRaw l r left F G J N right
  localTransport :
    ∀ {X Y : selectedMixedLeftNineteenRaw l r left F G J N right},
      SelectedLocalNineteen W l r X Y →
        SelectedLocalNineteen W l r (rawTransport X) (rawTransport Y)

/-- A genuine boundary certificate induces a function between
DIFFERENT selected 19D quotient TYPES, via the proved setoid
compatibility. It is conditional on the supplied certificate. -/
def selectedMixedBoundaryDescend
    (B : SelectedMixedNineteenBoundary l r left F G J N right) :
    selectedMixedLeftNineteenQuot l r left F G J N right →
      selectedMixedRightNineteenQuot l r left F G J N right :=
  Quotient.lift
    (fun X => selectedNineteenClass l r (B.rawTransport X))
    (by
      intro X Y h
      rcases h with ⟨A⟩
      exact Quotient.sound ⟨B.localTransport A⟩)

/-- The conditional descent acts on each genuine raw 18D class
by the supplied typed raw transport. -/
theorem selectedMixedBoundaryDescend_onClass
    (B : SelectedMixedNineteenBoundary l r left F G J N right)
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedBoundaryDescend l r left F G J N right B
        (selectedNineteenClass l r X) =
      selectedNineteenClass l r (B.rawTransport X) :=
  rfl

/-- Coarse observation naturality is a SEPARATE condition; mere
proof-quotient descent does not imply it for every raw 18D term. -/
def SelectedMixedBoundaryCoarseCompatible
    (B : SelectedMixedNineteenBoundary l r left F G J N right) : Prop :=
  ∀ X : selectedMixedLeftNineteenRaw l r left F G J N right,
    selectedOuterSwapClass (selectedContextEighteenTrace l r X) =
      selectedOuterSwapClass
        (selectedContextEighteenTrace l r (B.rawTransport X))

/-- With explicit coarse compatibility, the two observation maps
commute over the ACTUAL cross-fiber 19D quotient transport. -/
theorem selectedMixedBoundaryDescend_swapNatural
    (B : SelectedMixedNineteenBoundary l r left F G J N right)
    (compatible : SelectedMixedBoundaryCoarseCompatible
      l r left F G J N right B)
    (q : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedNineteenSwapObservation l r _ _ q =
      selectedNineteenSwapObservation l r _ _
        (selectedMixedBoundaryDescend l r left F G J N right B q) := by
  refine Quotient.inductionOn q ?_
  intro X
  exact compatible X

/-- Equality of the two finite counts follows from the separate
coarse observation certificate; it is not assumed as 19D equality. -/
theorem selectedMixedBoundaryDescend_countsNatural
    (B : SelectedMixedNineteenBoundary l r left F G J N right)
    (compatible : SelectedMixedBoundaryCoarseCompatible
      l r left F G J N right B)
    (q : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedNineteenSwapCounts l r _ _ q =
      selectedNineteenSwapCounts l r _ _
        (selectedMixedBoundaryDescend l r left F G J N right B q) := by
  exact congrArg selectedOuterSwapCountsOnQuotient
    (selectedMixedBoundaryDescend_swapNatural l r left F G J N right
      B compatible q)

/-- A pointed boundary contains a true TARGET 19D proof comparing
the transported source witness with the independently constructed
original RL witness. It does NOT require raw proof equality. -/
structure SelectedMixedNineteenAnchored
    (M : SelectedContextualEighteen W l r J N) : Type uSix where
  boundary : SelectedMixedNineteenBoundary l r left F G J N right
  chosenComparison : SelectedLocalNineteen W l r
    (boundary.rawTransport
      (selectedEighteenLeftAfterRight l r left F G M right))
    (selectedEighteenRightAfterLeft l r left F G M right)

/-- The pointed boundary descends because its unpointed part
already preserves ALL genuine local 19D comparisons. -/
def selectedMixedAnchoredDescend
    {M : SelectedContextualEighteen W l r J N}
    (B : SelectedMixedNineteenAnchored l r left F G J N right M) :
    selectedMixedLeftNineteenQuot l r left F G J N right →
      selectedMixedRightNineteenQuot l r left F G J N right :=
  selectedMixedBoundaryDescend l r left F G J N right B.boundary

/-- Only an ACTUAL selected 19D comparison justifies this chosen
equation in the TARGET quotient. No heterogeneous raw equality. -/
theorem selectedMixedAnchoredDescend_chosenClass
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenAnchored l r left F G J N right M) :
    selectedMixedAnchoredDescend l r left F G J N right B
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenClass l r
        (selectedEighteenRightAfterLeft l r left F G M right) := by
  change selectedNineteenClass l r
      (B.boundary.rawTransport
        (selectedEighteenLeftAfterRight l r left F G M right)) =
    selectedNineteenClass l r
      (selectedEighteenRightAfterLeft l r left F G M right)
  exact Quotient.sound ⟨B.chosenComparison⟩

/-- For the specific REAL LR/RL pair, the pointed 19D certificate
necessarily CHANGES the full fine exterior history. This follows
from actual 19D trace preservation and the verified v5.38 mismatch. -/
theorem selectedMixedAnchored_fineTraceChanges
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenAnchored l r left F G J N right M) :
    selectedContextEighteenTrace l r
        (selectedEighteenLeftAfterRight l r left F G M right) ≠
      selectedContextEighteenTrace l r
        (B.boundary.rawTransport
          (selectedEighteenLeftAfterRight l r left F G M right)) := by
  intro hFine
  have hTarget := selectedLocalNineteen_preservesEighteenTrace
    l r B.chosenComparison
  have hFalse :
      selectedContextEighteenTrace l r
          (selectedEighteenLeftAfterRight l r left F G M right) =
        selectedContextEighteenTrace l r
          (selectedEighteenRightAfterLeft l r left F G M right) :=
    hFine.trans hTarget
  have hValues := selectedEighteenMixedTraceValues l r left F G M right
  rw [hValues.1, hValues.2] at hFalse
  exact (selectedAdjacentSwap_changesTrace _) hFalse

/-- The pointed boundary rules out global fine-trace-preservation
even if it has genuine type-relevant 19D comparison transport. -/
theorem selectedMixedAnchored_noFinePreservation
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenAnchored l r left F G J N right M) :
    ¬ (∀ X : selectedMixedLeftNineteenRaw l r left F G J N right,
      selectedContextEighteenTrace l r X =
        selectedContextEighteenTrace l r (B.boundary.rawTransport X)) := by
  intro h
  exact (selectedMixedAnchored_fineTraceChanges
    l r left F G J N right M B)
      (h (selectedEighteenLeftAfterRight l r left F G M right))

/-- The anchored class equation, together with the REAL v5.38
selected mixed swap, ensures coarse compatibility at the chosen
class. It does NOT assert the global coarse square. -/
theorem selectedMixedAnchored_chosenSwap
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenAnchored l r left F G J N right M) :
    selectedNineteenSwapObservation l r _ _
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapObservation l r _ _
        (selectedMixedAnchoredDescend l r left F G J N right B
          (selectedNineteenClass l r
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  calc
    _ = selectedNineteenSwapObservation l r _ _
          (selectedNineteenClass l r
            (selectedEighteenRightAfterLeft l r left F G M right)) :=
      selectedEighteenMixedOrder_swapClassEq l r left F G M right
    _ = _ := by
      rw [selectedMixedAnchoredDescend_chosenClass
        l r left F G J N right M B]

/-- At the pointed class the coarse event counts also agree,
whereas the order is forced to change. -/
theorem selectedMixedAnchored_chosenCounts
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenAnchored l r left F G J N right M) :
    selectedNineteenSwapCounts l r _ _
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapCounts l r _ _
        (selectedMixedAnchoredDescend l r left F G J N right B
          (selectedNineteenClass l r
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  exact congrArg selectedOuterSwapCountsOnQuotient
    (selectedMixedAnchored_chosenSwap
      l r left F G J N right M B)

/-- The v5.38 exact no-go applies to any descended pointed
certificate: a quotient map that sends LR to RL cannot preserve
complete ordered 18D trace on every 19D class. -/
theorem selectedMixedAnchored_noFineQuotientTransport
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenAnchored l r left F G J N right M) :
    ¬ (∀ q : selectedMixedLeftNineteenQuot l r left F G J N right,
      selectedNineteenTraceOnQuotient l r _ _ q =
        selectedNineteenTraceOnQuotient l r _ _
          (selectedMixedAnchoredDescend l r left F G J N right B q)) := by
  intro h
  exact (selectedEighteenMixedOrder_noFinePreservingTransport
    l r left F G M right)
    ⟨selectedMixedAnchoredDescend l r left F G J N right B,
      h, selectedMixedAnchoredDescend_chosenClass
        l r left F G J N right M B⟩

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedMixedLeftNineteenRaw
#print axioms PentagonAdjoinedSixCell.selectedMixedRightNineteenRaw
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftNineteenQuot
#print axioms PentagonAdjoinedSixCell.selectedMixedRightNineteenQuot
#print axioms PentagonAdjoinedSixCell.SelectedMixedNineteenBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedBoundaryDescend
#print axioms PentagonAdjoinedSixCell.selectedMixedBoundaryDescend_onClass
#print axioms PentagonAdjoinedSixCell.SelectedMixedBoundaryCoarseCompatible
#print axioms PentagonAdjoinedSixCell.selectedMixedBoundaryDescend_swapNatural
#print axioms PentagonAdjoinedSixCell.selectedMixedBoundaryDescend_countsNatural
#print axioms PentagonAdjoinedSixCell.SelectedMixedNineteenAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedAnchoredDescend
#print axioms PentagonAdjoinedSixCell.selectedMixedAnchoredDescend_chosenClass
#print axioms PentagonAdjoinedSixCell.selectedMixedAnchored_fineTraceChanges
#print axioms PentagonAdjoinedSixCell.selectedMixedAnchored_noFinePreservation
#print axioms PentagonAdjoinedSixCell.selectedMixedAnchored_chosenSwap
#print axioms PentagonAdjoinedSixCell.selectedMixedAnchored_chosenCounts
#print axioms PentagonAdjoinedSixCell.selectedMixedAnchored_noFineQuotientTransport

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
