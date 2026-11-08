import KUOS.Architecture.QiWuxingGK5CHP77ContextualEighteenNineteenV5_37

/-!
Qi v5.38 — genuine two-order 18D contextual transports and
the exact boundary between 19D proof-quotient authority and a
separately selected finite adjacent-swap observation quotient.

Starting from one ACTUAL, dependent Type-valued selected 18D
witness, construct the left-after-right and right-after-left
18D transports using genuinely matching original 7D contexts.
Their 17D endpoints and 19D quotient fibers remain SEPARATELY
TYPED. Prove the full ordered 18D exterior traces are different,
even after descent to their respective 19D quotients.

A canonical, independently constructed observation morphism
sends EACH fixed-fiber 19D proof quotient to the common
v5.36 finite List Bool adjacent-swap quotient. This is a true
Quotient.lift-based descent, NOT an original cross-fiber higher
proof or a hypothetical transport between distinct domains.
The two different 18D double whiskerings map to the SAME
coarse swap observation, and remain distinct in the shared
fine List Bool codomain. Coarse compatibility also persists
under arbitrary common finite prefix contexts, preserving
the two coarse left/right event counts.

A concrete proof-relevant mixed 18D packet keeps the actual
lower 12D–14D witnesses, both genuinely typed 18D transports,
their explicit finite adjacent-swap witness, their fine-trace
non-equality and the previous strict gate obstruction.
No total 19D-quotient transport can BOTH preserve the COMPLETE
fine order and map the designated LR class to its RL class.
This does not exclude trace-changing cross-fiber transports
with additional dependent boundary certificates.

All original F55/P77/GK5CG and 6D–14D sources, every older
v5.23–v5.37 selected presentation, public root107 and
fixed Lean/mathlib are unchanged. New file only.
Append-only / tighten-only / overwrite-forbidden / same-root.
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

/-- Real 18D source witness transported first through the original
right seventh-cell context, then through a matching left context.
Both 17D source/target indices are transported together. -/
def selectedEighteenLeftAfterRight (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    SelectedContextualEighteen W l r
      (selectedSeventeenLeftAfterRight l r left F G J right) (selectedSeventeenLeftAfterRight l r left F G N right) :=
  .whiskerLeft left
    (contextFrameRight l r F right)
    (contextFrameRight l r G right)
    (.whiskerRight F G M right)

/-- Independently typed alternate 18D transport: first left,
then right, with all original 7D source boundaries retained. -/
def selectedEighteenRightAfterLeft (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    SelectedContextualEighteen W l r
      (selectedSeventeenRightAfterLeft l r left F G J right) (selectedSeventeenRightAfterLeft l r left F G N right) :=
  .whiskerRight
    (contextFrameLeft l r left F)
    (contextFrameLeft l r left G)
    (.whiskerLeft left F G M) right

/-- The genuine exterior 18D proof histories record distinct
ordered Boolean lists; no cross-fiber raw equality is inferred. -/
theorem selectedEighteenMixedTraceValues (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    selectedContextEighteenTrace l r (selectedEighteenLeftAfterRight l r left F G M right) =
      false :: true :: selectedContextEighteenTrace l r M ∧
    selectedContextEighteenTrace l r (selectedEighteenRightAfterLeft l r left F G M right) =
      true :: false :: selectedContextEighteenTrace l r M := by
  constructor <;> rfl

/-- An observation-only map from EACH strict same-17D-fiber 19D
proof quotient to a COMMON finite adjacent-swap observation quotient.
It factors through the proven complete-ordered 18D trace lift;
this does NOT produce any cross-fiber source comparison. -/
def selectedNineteenSwapObservation (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      Quotient selectedOuterSwapSetoid :=
  fun q => selectedOuterSwapClass
    (selectedNineteenTraceOnQuotient l r J N q)

theorem selectedNineteenSwapObservation_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSwapObservation l r J N
        (selectedNineteenClass l r M) =
      selectedOuterSwapClass (selectedContextEighteenTrace l r M) :=
  rfl

/-- Composing the selected finite-swap observation with its
coarse count lift gives a canonical 19D quotient observable. -/
def selectedNineteenSwapCounts (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat × Nat :=
  fun q => selectedOuterSwapCountsOnQuotient
    (selectedNineteenSwapObservation l r J N q)

theorem selectedNineteenSwapCounts_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSwapCounts l r J N
        (selectedNineteenClass l r M) =
      selectedFifteenTraceCounts (selectedContextEighteenTrace l r M) :=
  rfl

/-- Every TRUE 19D unit/coherence witness is compatible with
the chosen coarse observation: the map is well-defined on 19D
proof classes rather than selected by an arbitrary representative. -/
theorem selectedNineteenSwapObservation_respectsNineteen (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K)
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedNineteenSwapObservation l r J N
        (selectedNineteenClass l r M) =
      selectedNineteenSwapObservation l r J N
        (selectedNineteenClass l r L) := by
  exact congrArg (selectedNineteenSwapObservation l r J N)
    (Quotient.sound ⟨A⟩)

/-- Even after taking their own (different) exact-fiber 19D
quotients, the two genuine mixed 18D transports have unequal
COMPLETE ordered fine traces in the shared List Bool codomain. -/
theorem selectedEighteenMixedOrder_fineTraceDistinct (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    selectedNineteenTraceOnQuotient l r _ _ (selectedNineteenClass l r (selectedEighteenLeftAfterRight l r left F G M right)) ≠
      selectedNineteenTraceOnQuotient l r _ _ (selectedNineteenClass l r (selectedEighteenRightAfterLeft l r left F G M right)) := by
  change false :: true :: selectedContextEighteenTrace l r M ≠
    true :: false :: selectedContextEighteenTrace l r M
  exact selectedAdjacentSwap_changesTrace _

/-- The two separate 19D-fiber quotient values map to the SAME
class only in the independently selected finite observation
swap quotient. The equality is NOT between their proof fibers. -/
theorem selectedEighteenMixedOrder_swapClassEq (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    selectedNineteenSwapObservation l r _ _ (selectedNineteenClass l r (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapObservation l r _ _ (selectedNineteenClass l r (selectedEighteenRightAfterLeft l r left F G M right)) := by
  change selectedOuterSwapClass
      (false :: true :: selectedContextEighteenTrace l r M) =
    selectedOuterSwapClass
      (true :: false :: selectedContextEighteenTrace l r M)
  exact selectedOuterSwap_headClassEq _

/-- Hence two distinct fine 18D proof histories carry the same
left/right coarse event counts in the COMMON observation codomain. -/
theorem selectedEighteenMixedOrder_countsEq (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    selectedNineteenSwapCounts l r _ _ (selectedNineteenClass l r (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapCounts l r _ _ (selectedNineteenClass l r (selectedEighteenRightAfterLeft l r left F G M right)) := by
  exact congrArg selectedOuterSwapCountsOnQuotient
    (selectedEighteenMixedOrder_swapClassEq l r left F G M right)

/-- Common finite exterior contexts preserve the OBSERVATION-level
swap equivalence of the two 18D proof histories. This is not an
extra original 19D whiskering/interchanger. -/
theorem selectedEighteenMixedOrder_prefixSwapClassEq (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d)
    (commonPrefix : List Bool) :
    selectedOuterSwapClass
        (commonPrefix ++ selectedContextEighteenTrace l r (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedOuterSwapClass
        (commonPrefix ++ selectedContextEighteenTrace l r (selectedEighteenRightAfterLeft l r left F G M right)) := by
  induction commonPrefix with
  | nil =>
      simpa using
        (selectedEighteenMixedOrder_swapClassEq l r left F G M right)
  | cons b tail ih =>
      simpa using (selectedOuterSwap_prefixClassEq b ih)

/-- No TOTAL function from the LR exact-fiber 19D proof quotient
to the DIFFERENT RL 19D fiber can both preserve the full ordered
fine trace and send this actual LR class to its RL counterpart.
Only the conjunction of those two demanded properties is refuted:
a trace-CHANGING dependent transport is not ruled out. -/
theorem selectedEighteenMixedOrder_noFinePreservingTransport (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    ¬ (∃ f :
      Quotient (selectedNineteenSetoid l r
        (selectedSeventeenLeftAfterRight l r left F G J right) (selectedSeventeenLeftAfterRight l r left F G N right)) →
      Quotient (selectedNineteenSetoid l r
        (selectedSeventeenRightAfterLeft l r left F G J right) (selectedSeventeenRightAfterLeft l r left F G N right)),
      (∀ q, selectedNineteenTraceOnQuotient l r _ _ q =
        selectedNineteenTraceOnQuotient l r _ _ (f q)) ∧
      f (selectedNineteenClass l r (selectedEighteenLeftAfterRight l r left F G M right)) = selectedNineteenClass l r (selectedEighteenRightAfterLeft l r left F G M right)) := by
  rintro ⟨f, hpreserves, hchosen⟩
  have h : selectedNineteenTraceOnQuotient l r _ _ (selectedNineteenClass l r (selectedEighteenLeftAfterRight l r left F G M right)) = selectedNineteenTraceOnQuotient l r _ _ (selectedNineteenClass l r (selectedEighteenRightAfterLeft l r left F G M right)) := by
    calc
      _ = selectedNineteenTraceOnQuotient l r _ _
          (f (selectedNineteenClass l r (selectedEighteenLeftAfterRight l r left F G M right))) := hpreserves _
      _ = _ := by rw [hchosen]
  exact (selectedEighteenMixedOrder_fineTraceDistinct l r left F G M right) h

/-- The full proof-relevant lower-to-higher 18D observation packet.
It includes actual original seventh-cell proof indices on BOTH
independent source fibers, explicit finite-order swap evidence,
and the STRICT high-gate obstruction. None of these fields
claims heterogeneous Type equality. -/
structure SelectedMixedEighteenObservationPacket (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (B : SelectedContextualThirteen W l r P Q)
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) : Type uSix where
  lower : SelectedMixedLowerHigherPacket l r left F G B right
  leftWitness : SelectedContextualEighteen W l r
    (selectedSeventeenLeftAfterRight l r left F G J right) (selectedSeventeenLeftAfterRight l r left F G N right)
  rightWitness : SelectedContextualEighteen W l r
    (selectedSeventeenRightAfterLeft l r left F G J right) (selectedSeventeenRightAfterLeft l r left F G N right)
  leftActual : leftWitness = selectedEighteenLeftAfterRight l r left F G M right
  rightActual : rightWitness = selectedEighteenRightAfterLeft l r left F G M right
  adjacent : SelectedOuterSwapClosure
    (selectedContextEighteenTrace l r leftWitness)
    (selectedContextEighteenTrace l r rightWitness)
  fineDistinct :
    selectedContextEighteenTrace l r leftWitness ≠
      selectedContextEighteenTrace l r rightWitness
  strictGateEmpty :
    ¬ Nonempty (SelectedMixedTraceRespectingHigherGate
      l r left F G B H right)

/-- Construct ALL fields from actual lower 12D–14D certificates,
the two truly typed 18D original 7D transports, and the concrete
List Bool adjacent-swap constructor. No added gluing axiom. -/
def selectedMixedEighteenObservationPacket (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (B : SelectedContextualThirteen W l r P Q)
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    SelectedMixedEighteenObservationPacket
      l r left F G B M right := by
  refine {
    lower := selectedMixedLowerHigherPacket l r left F G B right
    leftWitness := selectedEighteenLeftAfterRight l r left F G M right
    rightWitness := selectedEighteenRightAfterLeft l r left F G M right
    leftActual := rfl
    rightActual := rfl
    adjacent := ?_
    fineDistinct := ?_
    strictGateEmpty :=
      selectedMixedTraceRespectingHigherGate_empty l r left F G B H right
  }
  · change SelectedOuterSwapClosure
      (false :: true :: selectedContextEighteenTrace l r M)
      (true :: false :: selectedContextEighteenTrace l r M)
    exact .observed (.leftRightToRightLeft _)
  · change false :: true :: selectedContextEighteenTrace l r M ≠
      true :: false :: selectedContextEighteenTrace l r M
    exact selectedAdjacentSwap_changesTrace _

/-- A positive actual source-typed 18D observation packet and the
negative old trace-preserving gluing gate coexist. Their authority
levels are different; no original cross-fiber 19D proof is inferred. -/
theorem selectedMixedEighteenPacket_possible_strictGateImpossible (l r : W) {w z : W}
    {a b c d : PentagonAdjoinedSixCell W l r w z}
    (left : SevenRewrite W l r a b)
    (F G : ContextFrameEleven W l r b c)
    {P Q : SelectedUnitalCompositionTwelve W l r
      (contextFramePack l r F) (contextFramePack l r G)}
    (B : SelectedContextualThirteen W l r P Q)
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N)
    (right : SevenRewrite W l r c d) :
    Nonempty (SelectedMixedEighteenObservationPacket
      l r left F G B M right) ∧
    ¬ Nonempty (SelectedMixedTraceRespectingHigherGate
      l r left F G B H right) :=
  ⟨⟨selectedMixedEighteenObservationPacket l r left F G B M right⟩,
    selectedMixedTraceRespectingHigherGate_empty l r left F G B H right⟩

#print axioms PentagonAdjoinedSixCell.selectedEighteenLeftAfterRight
#print axioms PentagonAdjoinedSixCell.selectedEighteenRightAfterLeft
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedTraceValues
#print axioms PentagonAdjoinedSixCell.selectedNineteenSwapObservation
#print axioms PentagonAdjoinedSixCell.selectedNineteenSwapObservation_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenSwapCounts
#print axioms PentagonAdjoinedSixCell.selectedNineteenSwapCounts_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenSwapObservation_respectsNineteen
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_fineTraceDistinct
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_swapClassEq
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_countsEq
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_prefixSwapClassEq
#print axioms PentagonAdjoinedSixCell.selectedEighteenMixedOrder_noFinePreservingTransport
#print axioms PentagonAdjoinedSixCell.SelectedMixedEighteenObservationPacket
#print axioms PentagonAdjoinedSixCell.selectedMixedEighteenObservationPacket
#print axioms PentagonAdjoinedSixCell.selectedMixedEighteenPacket_possible_strictGateImpossible

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
