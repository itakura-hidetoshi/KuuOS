import KUOS.Architecture.QiWuxingGK5CHP77ActiveDepthNineteenObstructionV5_46

/-!
Qi v5.47 — a six-observation anchored typed 19D boundary and
a residual adjacent-reverse obstruction in each supplied exact fiber.
Source observations are encoded into genuine RL trace powers.
No coordinatewise target-observation preservation is asserted.
No raw equality across independent dependent fibers, extra
coherence constructor, new axiom or global swap naturality is added.
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

section SixObservation

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- All six established original raw18D numerical observations. -/
def selectedContextEighteenSix
    (M : SelectedContextualEighteen W l r J N) :
    ((((Nat × Nat) × Nat) × Nat) × Nat) × Nat :=
  ((selectedContextEighteenFour l r M,
    selectedContextEighteenReverseLeftCount l r M),
    selectedContextEighteenActiveDepth l r M)

theorem selectedLocalNineteen_preservesSix
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenSix l r M = selectedContextEighteenSix l r L := by
  exact Prod.ext (Prod.ext
    (selectedLocalNineteen_preservesFour l r A)
    (selectedLocalNineteen_preservesReverseLeftCount l r A))
    (selectedLocalNineteen_preservesActiveDepth l r A)

/-- Six-vector on ONE exact-dependent selected19 quotient. -/
def selectedNineteenSixObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      ((((Nat × Nat) × Nat) × Nat) × Nat) × Nat :=
  fun q => (selectedNineteenFiveObservation l r J N q,
    selectedNineteenActiveDepthOnQuotient l r J N q)

theorem selectedNineteenSix_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSixObservation l r J N (selectedNineteenClass l r M) =
      selectedContextEighteenSix l r M := rfl

theorem selectedNineteenSix_eq_iff
    (J N : SelectedContextualSeventeen W l r H K)
    (q1 q2 : Quotient (selectedNineteenSetoid l r J N)) :
    selectedNineteenSixObservation l r J N q1 =
      selectedNineteenSixObservation l r J N q2 ↔
    selectedNineteenFiveObservation l r J N q1 =
      selectedNineteenFiveObservation l r J N q2 ∧
    selectedNineteenActiveDepthOnQuotient l r J N q1 =
      selectedNineteenActiveDepthOnQuotient l r J N q2 := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨h1, h2⟩
    exact Prod.ext h1 h2

/-- The v5.46 bracket pair is separated in its genuine J→J fiber. -/
theorem selectedNineteenSix_depthBracketsDistinct
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedNineteenSixObservation l r J J
      (selectedNineteenClass l r (selectedDepthBracketLeft l r M)) ≠
    selectedNineteenSixObservation l r J J
      (selectedNineteenClass l r (selectedDepthBracketRight l r M)) := by
  intro h
  exact (selectedDepthBrackets_depthDistinct l r M hpos) (congrArg Prod.snd h)

end SixObservation

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

/-- Injective pointed encoding of all SIX original source observations. -/
def selectedMixedSixCode
    (base p : ((((Nat × Nat) × Nat) × Nat) × Nat) × Nat) : Nat :=
  selectedMixedLengthCode
    (Nat.pair (Nat.pair (Nat.pair (Nat.pair (Nat.pair
      base.1.1.1.1.1 base.1.1.1.1.2) base.1.1.1.2) base.1.1.2) base.1.2) base.2)
    (Nat.pair (Nat.pair (Nat.pair (Nat.pair (Nat.pair
      p.1.1.1.1.1 p.1.1.1.1.2) p.1.1.1.2) p.1.1.2) p.1.2) p.2)

theorem selectedMixedSixCode_injective
    (base : ((((Nat × Nat) × Nat) × Nat) × Nat) × Nat) :
    Function.Injective (selectedMixedSixCode base) := by
  intro p q h
  have hPair :
      Nat.pair (Nat.pair (Nat.pair (Nat.pair (Nat.pair
        p.1.1.1.1.1 p.1.1.1.1.2) p.1.1.1.2) p.1.1.2) p.1.2) p.2 =
      Nat.pair (Nat.pair (Nat.pair (Nat.pair (Nat.pair
        q.1.1.1.1.1 q.1.1.1.1.2) q.1.1.1.2) q.1.1.2) q.1.2) q.2 :=
    selectedMixedLengthCode_injective
      (Nat.pair (Nat.pair (Nat.pair (Nat.pair (Nat.pair
        base.1.1.1.1.1 base.1.1.1.1.2) base.1.1.1.2) base.1.1.2) base.1.2) base.2) h
  have h1 := Nat.pair_eq_pair.mp hPair
  have h2 := Nat.pair_eq_pair.mp h1.1
  have h3 := Nat.pair_eq_pair.mp h2.1
  have h4 := Nat.pair_eq_pair.mp h3.1
  have h5 := Nat.pair_eq_pair.mp h4.1
  exact Prod.ext (Prod.ext (Prod.ext (Prod.ext
    (Prod.ext h5.1 h5.2) h4.2) h3.2) h2.2) h1.2

/-- A total, real LR-to-RL raw proof transport into the
distinct original RL 17D endpoint fiber. -/
def selectedMixedSixRawTransport
    (M : SelectedContextualEighteen W l r J N)
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedRightNineteenRaw l r left F G J N right :=
  selectedMixedRightTracePower l r left F G J N right
    (selectedEighteenRightAfterLeft l r left F G M right)
    (selectedMixedSixCode
      (selectedContextEighteenSix l r
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedContextEighteenSix l r X))

theorem selectedMixedSixRawTransport_chosen
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedSixRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right) =
      selectedEighteenRightAfterLeft l r left F G M right := by
  simp [selectedMixedSixRawTransport, selectedMixedSixCode,
    selectedMixedLengthCode, selectedMixedRightTracePower]

theorem selectedMixedSixRaw_eq_of_observation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (h : selectedContextEighteenSix l r X =
      selectedContextEighteenSix l r Y) :
    selectedMixedSixRawTransport l r left F G J N right M X =
      selectedMixedSixRawTransport l r left F G J N right M Y := by
  unfold selectedMixedSixRawTransport
  rw [h]

/-- Preservation of actual 19D Type-valued comparison proofs,
not merely postulated existence of a quotient function. -/
def selectedMixedSixBoundary
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenBoundary l r left F G J N right where
  rawTransport := selectedMixedSixRawTransport l r left F G J N right M
  localTransport := by
    intro X Y A
    have hObs : selectedContextEighteenSix l r X =
        selectedContextEighteenSix l r Y :=
      selectedLocalNineteen_preservesSix l r A
    have hEq := selectedMixedSixRaw_eq_of_observation
      l r left F G J N right M hObs
    change SelectedLocalNineteen W l r
      (selectedMixedSixRawTransport l r left F G J N right M X)
      (selectedMixedSixRawTransport l r left F G J N right M Y)
    rw [hEq]
    exact .strict _

def selectedMixedSixAnchored
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenAnchored l r left F G J N right M where
  boundary := selectedMixedSixBoundary l r left F G J N right M
  chosenComparison := by
    change SelectedLocalNineteen W l r
      (selectedMixedSixRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedEighteenRightAfterLeft l r left F G M right)
    rw [selectedMixedSixRawTransport_chosen l r left F G J N right M]
    exact .strict _

theorem selectedMixedSixAnchored_chosenClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenClass l r
        (selectedEighteenRightAfterLeft l r left F G M right) := by
  exact selectedMixedAnchoredDescend_chosenClass
    l r left F G J N right M
    (selectedMixedSixAnchored l r left F G J N right M)

/-- Comparison in the RL target reflects the SIX original
source observations but NOT original 19D comparison values. -/
theorem selectedMixedSixRaw_reflectObservation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (A : SelectedLocalNineteen W l r
      (selectedMixedSixRawTransport l r left F G J N right M X)
      (selectedMixedSixRawTransport l r left F G J N right M Y)) :
    selectedContextEighteenSix l r X =
      selectedContextEighteenSix l r Y := by
  let R := selectedEighteenRightAfterLeft l r left F G M right
  let base := selectedContextEighteenSix l r
    (selectedEighteenLeftAfterRight l r left F G M right)
  have hlen := congrArg List.length
    (selectedLocalNineteen_preservesEighteenTrace l r A)
  change (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedSixCode base
          (selectedContextEighteenSix l r X)))).length =
    (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedSixCode base
          (selectedContextEighteenSix l r Y)))).length at hlen
  simp only [selectedMixedRightTracePower_length] at hlen
  have hpos : 0 < (selectedContextEighteenTrace l r R).length :=
    selectedMixedRightSeed_tracePositive l r left F G J N right M
  have hc :
      2 * selectedMixedSixCode base (selectedContextEighteenSix l r X) + 1 =
      2 * selectedMixedSixCode base (selectedContextEighteenSix l r Y) + 1 :=
    Nat.mul_right_cancel hpos hlen
  have hcode :
      selectedMixedSixCode base (selectedContextEighteenSix l r X) =
        selectedMixedSixCode base (selectedContextEighteenSix l r Y) := by
    omega
  exact selectedMixedSixCode_injective base hcode

/-- Exact kernel classification of THIS six-variable boundary:
target class equality iff all six source observables agree. -/
theorem selectedMixedSixDescend_eq_iff_observation
    (M : SelectedContextualEighteen W l r J N)
    (q₁ q₂ : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M) q₁ =
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M) q₂ ↔
    selectedNineteenSixObservation l r _ _ q₁ =
      selectedNineteenSixObservation l r _ _ q₂ := by
  constructor
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedNineteenClass l r
                (selectedMixedSixRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedSixRawTransport l r left F G J N right M Y) at h
            rcases Quotient.exact h with ⟨A⟩
            exact selectedMixedSixRaw_reflectObservation
              l r left F G J N right M A
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedContextEighteenSix l r X =
              selectedContextEighteenSix l r Y at h
            change selectedNineteenClass l r
                (selectedMixedSixRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedSixRawTransport l r left F G J N right M Y)
            exact congrArg (selectedNineteenClass l r)
              (selectedMixedSixRaw_eq_of_observation
                l r left F G J N right M h)

theorem selectedMixedSixAnchored_chosenSwap
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSwapObservation l r _ _
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapObservation l r _ _
        (selectedMixedBoundaryDescend l r left F G J N right
          (selectedMixedSixBoundary l r left F G J N right M)
          (selectedNineteenClass l r
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  exact selectedMixedAnchored_chosenSwap l r left F G J N right
    M (selectedMixedSixAnchored l r left F G J N right M)

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenSix
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesSix
#print axioms PentagonAdjoinedSixCell.selectedNineteenSixObservation
#print axioms PentagonAdjoinedSixCell.selectedNineteenSix_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenSix_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedNineteenSix_depthBracketsDistinct
#print axioms PentagonAdjoinedSixCell.selectedMixedSixCode
#print axioms PentagonAdjoinedSixCell.selectedMixedSixCode_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedSixRawTransport
#print axioms PentagonAdjoinedSixCell.selectedMixedSixRawTransport_chosen
#print axioms PentagonAdjoinedSixCell.selectedMixedSixRaw_eq_of_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedSixBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedSixAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedSixAnchored_chosenClass
#print axioms PentagonAdjoinedSixCell.selectedMixedSixRaw_reflectObservation
#print axioms PentagonAdjoinedSixCell.selectedMixedSixDescend_eq_iff_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedSixAnchored_chosenSwap


/-- Count adjacent raw reverse/reverse nodes. The top tag is
used only inside this explicitly proved 19D-invariant count. -/
def selectedContextEighteenAdjacentReverseCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ M => selectedContextEighteenAdjacentReverseCount l r M
  | .whiskerRight _ _ M _ => selectedContextEighteenAdjacentReverseCount l r M
  | .strict _ => 0
  | .reverse M => selectedContextEighteenAdjacentReverseCount l r M +
      (if selectedContextEighteenTopTag l r M = 4 then 1 else 0)
  | .chain M L => selectedContextEighteenAdjacentReverseCount l r M +
      selectedContextEighteenAdjacentReverseCount l r L

section AdjacentReverseObstruction

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- All five ACTUAL selected19 constructors preserve this count.
Their two unit comparisons apply only to inherited old18 values. -/
theorem selectedLocalNineteen_preservesAdjacentReverseCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenAdjacentReverseCount l r M =
      selectedContextEighteenAdjacentReverseCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

def selectedNineteenAdjacentReverseOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenAdjacentReverseCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesAdjacentReverseCount l r A)

theorem selectedNineteenAdjacentReverse_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenAdjacentReverseOnQuotient l r J N
      (selectedNineteenClass l r M) =
      selectedContextEighteenAdjacentReverseCount l r M := rfl

/-- Retain the original M and append a genuine N→N suffix
with two consecutive reverses, in the SAME original J→N fiber. -/
def selectedAdjacentReverseLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (.chain (.strict N) (.reverse (.reverse (.strict N))))

/-- The second genuine suffix has its two reverse nodes
separated by a raw chain constructor. No new comparison is added. -/
def selectedAdjacentReverseRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (.reverse (.chain (.strict N) (.reverse (.strict N))))

/-- Even the COMPLETE ordered exterior trace agrees. -/
theorem selectedAdjacentReverse_trace
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r (selectedAdjacentReverseLeft l r M) =
      selectedContextEighteenTrace l r (selectedAdjacentReverseRight l r M) := rfl

/-- Six-number equality for any supplied original proof M;
no nonempty-trace hypothesis is needed for this suffix pair. -/
theorem selectedAdjacentReverse_rawSixEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenSix l r (selectedAdjacentReverseLeft l r M) =
      selectedContextEighteenSix l r (selectedAdjacentReverseRight l r M) := rfl

theorem selectedAdjacentReverse_sixEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSixObservation l r J N
      (selectedNineteenClass l r (selectedAdjacentReverseLeft l r M)) =
    selectedNineteenSixObservation l r J N
      (selectedNineteenClass l r (selectedAdjacentReverseRight l r M)) := rfl

/-- The quotient-stable count differs by exactly one. -/
theorem selectedAdjacentReverse_countDiff
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedAdjacentReverseLeft l r M) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedAdjacentReverseRight l r M) + 1 := rfl

/-- The original selected19 quotient separates the two proof
histories even though all six numbers and the fine trace agree. -/
theorem selectedAdjacentReverse_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenClass l r (selectedAdjacentReverseLeft l r M) ≠
      selectedNineteenClass l r (selectedAdjacentReverseRight l r M) := by
  intro h
  have hc := congrArg (selectedNineteenAdjacentReverseOnQuotient l r _ _) h
  change selectedContextEighteenAdjacentReverseCount l r
      (selectedAdjacentReverseLeft l r M) =
    selectedContextEighteenAdjacentReverseCount l r
      (selectedAdjacentReverseRight l r M) at hc
  rw [selectedAdjacentReverse_countDiff l r M] at hc
  omega

theorem selectedAdjacentReverse_noLocal
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (selectedAdjacentReverseLeft l r M)
      (selectedAdjacentReverseRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedAdjacentReverse_classDistinct l r M) (Quotient.sound ⟨A⟩)

/-- Noninjectivity in any exact fiber that has the supplied M.
This theorem does not claim every dependent fiber is inhabited. -/
theorem selectedNineteenSix_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedNineteenSixObservation l r J N) := by
  intro hinj
  exact (selectedAdjacentReverse_classDistinct l r M)
    (hinj (selectedAdjacentReverse_sixEq l r M))

end AdjacentReverseObstruction

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenAdjacentReverseCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesAdjacentReverseCount
#print axioms PentagonAdjoinedSixCell.selectedNineteenAdjacentReverseOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedNineteenAdjacentReverse_onClass
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverseLeft
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverseRight
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverse_trace
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverse_rawSixEq
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverse_sixEq
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverse_countDiff
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverse_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedAdjacentReverse_noLocal
#print axioms PentagonAdjoinedSixCell.selectedNineteenSix_notInjective

section SixBoundaryResidual

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

/-- Distinct source ActiveDepth values give distinct target
classes, with both source values in the actual LR dependent fiber. -/
theorem selectedMixedSixDescend_separates_of_depth_ne
    (M : SelectedContextualEighteen W l r J N)
    (X Y : selectedMixedLeftNineteenRaw l r left F G J N right)
    (hne : selectedContextEighteenActiveDepth l r X ≠
      selectedContextEighteenActiveDepth l r Y) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M)
      (selectedNineteenClass l r X) ≠
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M)
      (selectedNineteenClass l r Y) := by
  intro h
  have hobs := (selectedMixedSixDescend_eq_iff_observation
    l r left F G J N right M _ _).mp h
  exact hne (congrArg Prod.snd hobs)

/-- The six-coordinate boundary distinguishes the v5.45 pair
by the separately retained source ReverseLeftCount. -/
theorem selectedMixedSixDescend_separatesStrictReverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedContextEighteenStrictReverseLeft l r
          (selectedEighteenLeftAfterRight l r left F G M right))) ≠
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedContextEighteenStrictReverseRight l r
          (selectedEighteenLeftAfterRight l r left F G M right))) := by
  intro h
  have hobs := (selectedMixedSixDescend_eq_iff_observation
    l r left F G J N right M _ _).mp h
  have hrl := congrArg Prod.snd (congrArg Prod.fst hobs)
  change selectedContextEighteenReverseLeftCount l r
      (selectedContextEighteenStrictReverseLeft l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
    selectedContextEighteenReverseLeftCount l r
      (selectedContextEighteenStrictReverseRight l r
        (selectedEighteenLeftAfterRight l r left F G M right)) at hrl
  rw [selectedContextEighteenStrictReverse_reverseLeftDiff] at hrl
  omega

/-- The actual LR fiber contains two genuine source classes
with equal six observations that this concrete boundary collapses. -/
theorem selectedMixedSixDescend_collapsesAdjacentReverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedAdjacentReverseLeft l r
          (selectedEighteenLeftAfterRight l r left F G M right))) =
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedSixBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedAdjacentReverseRight l r
          (selectedEighteenLeftAfterRight l r left F G M right))) := by
  apply (selectedMixedSixDescend_eq_iff_observation
    l r left F G J N right M _ _).2
  exact selectedAdjacentReverse_sixEq l r
    (selectedEighteenLeftAfterRight l r left F G M right)

/-- Nonfaithfulness of THIS six-observation transport, not of
every possible boundary between the independent LR/RL fibers. -/
theorem selectedMixedSixDescend_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedSixBoundary l r left F G J N right M)) := by
  intro hinj
  let X := selectedEighteenLeftAfterRight l r left F G M right
  exact (selectedAdjacentReverse_classDistinct l r X)
    (hinj (selectedMixedSixDescend_collapsesAdjacentReverse
      l r left F G J N right M))

/-- No full Type-valued comparison reflection can extend this
particular boundary: it would contradict its certified kernel. -/
theorem selectedMixedSixBoundary_noReflection
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (∀ {X Y : selectedMixedLeftNineteenRaw
          l r left F G J N right},
      SelectedLocalNineteen W l r
        ((selectedMixedSixBoundary l r left F G J N right M).rawTransport X)
        ((selectedMixedSixBoundary l r left F G J N right M).rawTransport Y) →
      SelectedLocalNineteen W l r X Y) := by
  rintro ⟨reflectLocal⟩
  let B : SelectedMixedNineteenFaithfulBoundary
      l r left F G J N right :=
    { boundary := selectedMixedSixBoundary l r left F G J N right M
      reflectLocal := reflectLocal }
  exact (selectedMixedSixDescend_notInjective
    l r left F G J N right M)
    (selectedMixedFaithfulDescend_injective l r left F G J N right B)

end SixBoundaryResidual

#print axioms PentagonAdjoinedSixCell.selectedMixedSixDescend_separates_of_depth_ne
#print axioms PentagonAdjoinedSixCell.selectedMixedSixDescend_separatesStrictReverse
#print axioms PentagonAdjoinedSixCell.selectedMixedSixDescend_collapsesAdjacentReverse
#print axioms PentagonAdjoinedSixCell.selectedMixedSixDescend_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedSixBoundary_noReflection

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
