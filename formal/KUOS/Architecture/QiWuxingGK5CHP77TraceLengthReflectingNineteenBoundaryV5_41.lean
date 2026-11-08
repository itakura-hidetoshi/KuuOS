import KUOS.Architecture.QiWuxingGK5CHP77FaithfulNineteenBoundaryObstructionV5_40

/-!
Qi v5.41 — an inhabited, nonconstant, ANCHORED cross-fiber 19D
boundary which REFLECTS the length of the genuine ordered exterior
18D proof history.

The v5.40 constant example erased all source distinctions. Here the
actual RL double-context witness is used as a nonempty seed. Repeated
typed chain/reverse/chain constructs an unbounded family of genuine
RL 18D proofs. An explicit injective coding of source exterior trace
LENGTHS into this family makes a typed total LR-to-RL raw transport.

The true selected local 19D constructors preserve source trace, so
their proof values map to actual target strict 19D comparisons. The
construction is a genuine inhabitant of the v5.39 boundary structure,
and at the designated LR witness its image is the genuine RL witness.
It is NONCONSTANT on 19D quotient classes and REFLECTS ALL unequal
exterior trace lengths. Comparison reflection for arbitrary original
19D Type-valued witnesses is NOT established. Exact fine-order trace
reflection and global swap naturality are also NOT claimed.

No new exchange/gluing generator or original cross-fiber equality.
No old F55/P77/GK5CG or selected 6D–19D witness is changed.
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

/-- A pointed injective coding of ALL natural numbers: the
distinguished source length goes to zero; every other length
goes to its successor. No assumption on the base length. -/
def selectedMixedLengthCode (base n : Nat) : Nat :=
  if n = base then 0 else n + 1

theorem selectedMixedLengthCode_injective (base : Nat) :
    Function.Injective (selectedMixedLengthCode base) := by
  intro n m h
  unfold selectedMixedLengthCode at h
  by_cases hn : n = base
  · by_cases hm : m = base
    · exact hn.trans hm.symm
    · simp [hn, hm] at h
  · by_cases hm : m = base
    · simp [hn, hm] at h
    · simp [hn, hm] at h
      omega

/-- Every iteration is a true old 18D chain/reverse/chain in
the SAME exact target RL fiber; no heterogeneous cast. -/
def selectedMixedRightTracePower
    (R : selectedMixedRightNineteenRaw l r left F G J N right) :
    Nat → selectedMixedRightNineteenRaw l r left F G J N right :=
  Nat.rec R (fun _ acc => .chain (.chain acc (.reverse R)) R)

/-- The target trace grows by two genuine copies of R at each
step, so its length has an explicit strictly increasing factor
when the original RL exterior history is nonempty. -/
theorem selectedMixedRightTracePower_length
    (R : selectedMixedRightNineteenRaw l r left F G J N right)
    (n : Nat) :
    (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R n)).length =
      (2 * n + 1) * (selectedContextEighteenTrace l r R).length := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change ((selectedContextEighteenTrace l r
          (selectedMixedRightTracePower l r left F G J N right R n) ++
          selectedContextEighteenTrace l r R) ++
          selectedContextEighteenTrace l r R).length =
        (2 * (n + 1) + 1) * (selectedContextEighteenTrace l r R).length
      simp only [List.length_append]
      rw [ih]
      ring

/-- A concrete nonconstant typed raw map. It records the entire
source exterior trace before computing its length; the resulting
length-code is injective in that length, but does not encode the
whole original 18D Type-valued proof. -/
def selectedMixedLengthRawTransport
    (M : SelectedContextualEighteen W l r J N)
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedRightNineteenRaw l r left F G J N right :=
  selectedMixedRightTracePower l r left F G J N right
    (selectedEighteenRightAfterLeft l r left F G M right)
    (selectedMixedLengthCode
      (selectedContextEighteenTrace l r
        (selectedEighteenLeftAfterRight l r left F G M right)).length
      (selectedContextEighteenTrace l r X).length)

/-- The designated actual LR 18D proof goes to the actual RL
18D proof, not merely to an observationally equal surrogate. -/
theorem selectedMixedLengthRawTransport_chosen
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedLengthRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right) =
      selectedEighteenRightAfterLeft l r left F G M right := by
  simp [selectedMixedLengthRawTransport, selectedMixedLengthCode,
    selectedMixedRightTracePower]

/-- A total inhabited v5.39 boundary: actual 19D proof values
are preserved because every old local comparison preserves the
entire source trace, hence its numerical length code. -/
def selectedMixedLengthBoundary
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenBoundary l r left F G J N right where
  rawTransport := selectedMixedLengthRawTransport l r left F G J N right M
  localTransport := by
    intro X Y A
    have hlen := congrArg List.length
      (selectedLocalNineteen_preservesEighteenTrace l r A)
    change SelectedLocalNineteen W l r
      (selectedMixedLengthRawTransport l r left F G J N right M X)
      (selectedMixedLengthRawTransport l r left F G J N right M Y)
    have hEq :
        selectedMixedLengthRawTransport l r left F G J N right M X =
          selectedMixedLengthRawTransport l r left F G J N right M Y := by
      simp only [selectedMixedLengthRawTransport, hlen]
    rw [hEq]
    exact .strict _

/-- The selected boundary also satisfies the actual designated
19D anchoring comparison, using only true strict coherence. -/
def selectedMixedLengthAnchored
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenAnchored l r left F G J N right M where
  boundary := selectedMixedLengthBoundary l r left F G J N right M
  chosenComparison := by
    change SelectedLocalNineteen W l r
      (selectedMixedLengthRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedEighteenRightAfterLeft l r left F G M right)
    rw [selectedMixedLengthRawTransport_chosen l r left F G J N right M]
    exact .strict _

/-- The chosen 19D class equation is certified; it is NOT
an equation of unlike raw 18D dependent proof values. -/
theorem selectedMixedLengthDescend_chosen
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenClass l r
        (selectedEighteenRightAfterLeft l r left F G M right) := by
  exact selectedMixedAnchoredDescend_chosenClass
    l r left F G J N right M
    (selectedMixedLengthAnchored l r left F G J N right M)

/-- The true target RL seed has at least the two exterior
context events false/true (in the opposite order). -/
theorem selectedMixedRightSeed_tracePositive
    (M : SelectedContextualEighteen W l r J N) :
    0 < (selectedContextEighteenTrace l r
      (selectedEighteenRightAfterLeft l r left F G M right)).length := by
  rw [(selectedEighteenMixedTraceValues l r left F G M right).2]
  simp

/-- Every genuine target local 19D comparison between images
forces EQUALITY of the original source trace LENGTHS.
This is weaker than reflecting the full Type-valued comparison. -/
theorem selectedMixedLengthRaw_reflectTraceLength
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (A : SelectedLocalNineteen W l r
      (selectedMixedLengthRawTransport l r left F G J N right M X)
      (selectedMixedLengthRawTransport l r left F G J N right M Y)) :
    (selectedContextEighteenTrace l r X).length =
      (selectedContextEighteenTrace l r Y).length := by
  let R := selectedEighteenRightAfterLeft l r left F G M right
  let base := (selectedContextEighteenTrace l r
    (selectedEighteenLeftAfterRight l r left F G M right)).length
  have ht := congrArg List.length
    (selectedLocalNineteen_preservesEighteenTrace l r A)
  change (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedLengthCode base
          (selectedContextEighteenTrace l r X).length))).length =
    (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedLengthCode base
          (selectedContextEighteenTrace l r Y).length))).length at ht
  simp only [selectedMixedRightTracePower_length] at ht
  have hpos : 0 < (selectedContextEighteenTrace l r R).length :=
    selectedMixedRightSeed_tracePositive l r left F G J N right M
  have hc :
      2 * selectedMixedLengthCode base
            (selectedContextEighteenTrace l r X).length + 1 =
        2 * selectedMixedLengthCode base
            (selectedContextEighteenTrace l r Y).length + 1 :=
    Nat.mul_right_cancel hpos ht
  have hcode :
      selectedMixedLengthCode base
          (selectedContextEighteenTrace l r X).length =
        selectedMixedLengthCode base
          (selectedContextEighteenTrace l r Y).length := by
    omega
  exact selectedMixedLengthCode_injective base hcode

/-- Quotient descent reflects trace lengths on ALL input
19D classes; this is a genuine, global observational reflection
property, not global comparison reflection or raw injectivity. -/
theorem selectedMixedLengthDescend_reflectTraceLength
    (M : SelectedContextualEighteen W l r J N)
    (q₁ q₂ : selectedMixedLeftNineteenQuot l r left F G J N right)
    (h : selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M) q₁ =
      selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M) q₂) :
    (selectedNineteenTraceOnQuotient l r _ _ q₁).length =
      (selectedNineteenTraceOnQuotient l r _ _ q₂).length := by
  induction q₁ using Quotient.inductionOn with
  | _ X =>
      induction q₂ using Quotient.inductionOn with
      | _ Y =>
          change selectedNineteenClass l r
              (selectedMixedLengthRawTransport l r left F G J N right M X) =
            selectedNineteenClass l r
              (selectedMixedLengthRawTransport l r left F G J N right M Y) at h
          rcases Quotient.exact h with ⟨A⟩
          exact selectedMixedLengthRaw_reflectTraceLength
            l r left F G J N right M A

/-- Two original LR 18D values with unequal complete-trace
lengths MUST remain different after the new 19D quotient map. -/
theorem selectedMixedLengthDescend_separatesByTraceLength
    (M : SelectedContextualEighteen W l r J N)
    (X Y : selectedMixedLeftNineteenRaw l r left F G J N right)
    (hne : (selectedContextEighteenTrace l r X).length ≠
      (selectedContextEighteenTrace l r Y).length) :
    selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)
        (selectedNineteenClass l r X) ≠
      selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)
        (selectedNineteenClass l r Y) := by
  intro h
  exact hne (selectedMixedLengthDescend_reflectTraceLength
    l r left F G J N right M _ _ h)

/-- An explicit pair of DISTINCT genuine LR 19D classes
is separated in the RL 19D quotient, unlike v5.40's constant map.
This proves a nonconstant, proof-relevant boundary exists. -/
theorem selectedMixedLengthDescend_chosenVsRoundtrip
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right)) ≠
      selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)
        (selectedNineteenClass l r
          (selectedMixedLeftRoundtripAmplify l r left F G J N right
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  have hpos : 0 < (selectedContextEighteenTrace l r
      (selectedEighteenLeftAfterRight l r left F G M right)).length := by
    rw [(selectedEighteenMixedTraceValues l r left F G M right).1]
    simp
  have hne : (selectedContextEighteenTrace l r
      (selectedEighteenLeftAfterRight l r left F G M right)).length ≠
    (selectedContextEighteenTrace l r
      (selectedMixedLeftRoundtripAmplify l r left F G J N right
        (selectedEighteenLeftAfterRight l r left F G M right))).length := by
    intro hlen
    rw [selectedMixedLeftRoundtrip_traceLength l r left F G J N right
      (selectedEighteenLeftAfterRight l r left F G M right)] at hlen
    omega
  exact selectedMixedLengthDescend_separatesByTraceLength
    l r left F G J N right M _ _ hne

/-- The anchored true LR/RL swap observation equality is retained
at the CHOSEN class, without asserting a global swap-natural square. -/
theorem selectedMixedLengthAnchored_chosenSwap
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSwapObservation l r _ _
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapObservation l r _ _
        (selectedMixedBoundaryDescend l r left F G J N right
          (selectedMixedLengthBoundary l r left F G J N right M)
          (selectedNineteenClass l r
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  exact selectedMixedAnchored_chosenSwap l r left F G J N right
    M (selectedMixedLengthAnchored l r left F G J N right M)

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedMixedLengthCode
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthCode_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedRightTracePower
#print axioms PentagonAdjoinedSixCell.selectedMixedRightTracePower_length
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthRawTransport
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthRawTransport_chosen
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthDescend_chosen
#print axioms PentagonAdjoinedSixCell.selectedMixedRightSeed_tracePositive
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthRaw_reflectTraceLength
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthDescend_reflectTraceLength
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthDescend_separatesByTraceLength
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthDescend_chosenVsRoundtrip
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthAnchored_chosenSwap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
