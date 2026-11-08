import KUOS.Architecture.QiWuxingGK5CHP77TripleNineteenAssocObstructionV5_44

/-!
Qi v5.45 — a four-component quotient observation on the actual selected
19D Type-valued proof presentation, an inhabited anchored LR→RL
boundary with EXACT observational kernel, and an additional
independent raw active-chain-depth invariant.

The four coordinates are (trace length, active-chain count,
reverse-node count, left-nested chain count); the last coordinate
was proved quotient-stable in v5.44. A nested Nat.pair injection
and actual RL typed trace-power witness construct a concrete
total LR→RL boundary, respecting every old Type-valued 19D
local comparison. Its exact quotient kernel is equality of
the four source observations, not equality of original proofs.
This boundary distinguishes the two genuine v5.44 bracketings.

For the next obstruction filtration, active-chain-depth records
the sum of ancestral active-chain nodes in a raw 18D proof tree.
It is quotient-stable because unitPrepend and unitAppend act
only on old inherited 18D proofs with empty exterior trace.
No unrestricted association coherence, 20D gluing or extra
local comparison generator is added. Whether four coordinates
classify all original 19D classes is not assumed.

The original F55/P77/GK5CG, 6D–19D Type values, independent
presentations, public root107, Lean/mathlib pins and #1558
remain unchanged. Append-only / tighten-only /
overwrite-forbidden / same-root.
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

/-- Number of ancestor/descendant ordered pairs of ACTIVE raw
18D chain nodes. Inactive strict/inherited unit pastings do
not increase this count, so this is selected-19D invariant. -/
def selectedContextEighteenActiveDepth (l r : W)
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
  | .whiskerLeft _ _ _ M => selectedContextEighteenActiveDepth l r M
  | .whiskerRight _ _ M _ => selectedContextEighteenActiveDepth l r M
  | .strict _ => 0
  | .reverse M => selectedContextEighteenActiveDepth l r M
  | .chain M L =>
      selectedContextEighteenActiveDepth l r M +
        selectedContextEighteenActiveDepth l r L +
        selectedContextEighteenActiveChainCount l r M +
        selectedContextEighteenActiveChainCount l r L

/-- This fifth observable is separately invariant under all five
genuine selected local 19D Type-valued comparison constructors. -/
theorem selectedLocalNineteen_preservesActiveDepth (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenActiveDepth l r M =
      selectedContextEighteenActiveDepth l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Genuine fifth numeric observation descended through an
existing exact-fiber 19D setoid, not a new proof quotient. -/
def selectedNineteenActiveDepthOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenActiveDepth l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesActiveDepth l r A)

section FourObservation

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Trace length, active chain count, reverse count,
and left-nested chain count without Type-valued proof erasure. -/
def selectedContextEighteenFour
    (M : SelectedContextualEighteen W l r J N) :
    ((Nat × Nat) × Nat) × Nat :=
  (selectedContextEighteenTriple l r M,
    selectedContextEighteenLeftNestedCount l r M)

theorem selectedLocalNineteen_preservesFour
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenFour l r M =
      selectedContextEighteenFour l r L := by
  exact Prod.ext (selectedLocalNineteen_preservesTriple l r A)
    (selectedLocalNineteen_preservesLeftNestedCount l r A)

/-- The genuine four-coordinate 19D observation is a
function on each OLD same-endpoint proof quotient. -/
def selectedNineteenFourObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      ((Nat × Nat) × Nat) × Nat :=
  fun q => (selectedNineteenTripleObservation l r J N q,
    selectedNineteenLeftNestedOnQuotient l r J N q)

theorem selectedNineteenFour_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenFourObservation l r J N
      (selectedNineteenClass l r M) =
      selectedContextEighteenFour l r M :=
  rfl

theorem selectedNineteenFour_eq_iff
    (J N : SelectedContextualSeventeen W l r H K)
    (q₁ q₂ : Quotient (selectedNineteenSetoid l r J N)) :
    selectedNineteenFourObservation l r J N q₁ =
      selectedNineteenFourObservation l r J N q₂ ↔
    selectedNineteenTripleObservation l r J N q₁ =
      selectedNineteenTripleObservation l r J N q₂ ∧
    selectedNineteenLeftNestedOnQuotient l r J N q₁ =
      selectedNineteenLeftNestedOnQuotient l r J N q₂ := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨h₁, h₂⟩
    exact Prod.ext h₁ h₂

/-- The v5.44 genuine two-parenthesization counterexample
is separated by the new FOUR-coordinate observation. -/
theorem selectedNineteenFour_separatesAssoc
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenFourObservation l r J N
      (selectedNineteenClass l r
        (selectedContextEighteenAssocLeft l r M)) ≠
    selectedNineteenFourObservation l r J N
      (selectedNineteenClass l r
        (selectedContextEighteenAssocRight l r M)) := by
  intro h
  have hv := congrArg Prod.snd h
  change selectedContextEighteenLeftNestedCount l r
      (selectedContextEighteenAssocLeft l r M) =
    selectedContextEighteenLeftNestedCount l r
      (selectedContextEighteenAssocRight l r M) at hv
  rw [selectedContextEighteenAssoc_leftNested l r M] at hv
  omega

end FourObservation

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

/-- A pointed injective four-observation code, grounded in
the PINNED mathlib Nat.pair and existing v5.41 lengthCode. -/
def selectedMixedFourCode
    (base p : ((Nat × Nat) × Nat) × Nat) : Nat :=
  selectedMixedLengthCode
    (Nat.pair (Nat.pair (Nat.pair base.1.1.1 base.1.1.2)
      base.1.2) base.2)
    (Nat.pair (Nat.pair (Nat.pair p.1.1.1 p.1.1.2)
      p.1.2) p.2)

theorem selectedMixedFourCode_injective
    (base : ((Nat × Nat) × Nat) × Nat) :
    Function.Injective (selectedMixedFourCode base) := by
  intro p q h
  have hPair : Nat.pair (Nat.pair (Nat.pair p.1.1.1 p.1.1.2) p.1.2) p.2 =
      Nat.pair (Nat.pair (Nat.pair q.1.1.1 q.1.1.2) q.1.2) q.2 :=
    selectedMixedLengthCode_injective
      (Nat.pair (Nat.pair (Nat.pair base.1.1.1 base.1.1.2)
        base.1.2) base.2) h
  have hParts := Nat.pair_eq_pair.mp hPair
  have hInner := Nat.pair_eq_pair.mp hParts.1
  have hDeep := Nat.pair_eq_pair.mp hInner.1
  exact Prod.ext (Prod.ext (Prod.ext hDeep.1 hDeep.2) hInner.2) hParts.2

/-- The original true RL 18D proof family remains distinct
from the LR source endpoint family. -/
def selectedMixedFourRawTransport
    (M : SelectedContextualEighteen W l r J N)
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedRightNineteenRaw l r left F G J N right :=
  selectedMixedRightTracePower l r left F G J N right
    (selectedEighteenRightAfterLeft l r left F G M right)
    (selectedMixedFourCode
      (selectedContextEighteenFour l r
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedContextEighteenFour l r X))

theorem selectedMixedFourRawTransport_chosen
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedFourRawTransport l r left F G J N right M
      (selectedEighteenLeftAfterRight l r left F G M right) =
      selectedEighteenRightAfterLeft l r left F G M right := by
  simp [selectedMixedFourRawTransport, selectedMixedFourCode,
    selectedMixedLengthCode, selectedMixedRightTracePower]

theorem selectedMixedFourRaw_eq_of_observation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (h : selectedContextEighteenFour l r X =
      selectedContextEighteenFour l r Y) :
    selectedMixedFourRawTransport l r left F G J N right M X =
      selectedMixedFourRawTransport l r left F G J N right M Y := by
  unfold selectedMixedFourRawTransport
  rw [h]

/-- Preserve EVERY existing original local 19D Type-valued
comparison, constructing a true target strict comparison. -/
def selectedMixedFourBoundary
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenBoundary l r left F G J N right where
  rawTransport := selectedMixedFourRawTransport l r left F G J N right M
  localTransport := by
    intro X Y A
    have hObs : selectedContextEighteenFour l r X =
        selectedContextEighteenFour l r Y :=
      selectedLocalNineteen_preservesFour l r A
    have hEq := selectedMixedFourRaw_eq_of_observation
      l r left F G J N right M hObs
    change SelectedLocalNineteen W l r
      (selectedMixedFourRawTransport l r left F G J N right M X)
      (selectedMixedFourRawTransport l r left F G J N right M Y)
    rw [hEq]
    exact .strict _

/-- The designated original LR-to-RL witness is ANCHORED
by a real target Type-valued strict 19D comparison. -/
def selectedMixedFourAnchored
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenAnchored l r left F G J N right M where
  boundary := selectedMixedFourBoundary l r left F G J N right M
  chosenComparison := by
    change SelectedLocalNineteen W l r
      (selectedMixedFourRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedEighteenRightAfterLeft l r left F G M right)
    rw [selectedMixedFourRawTransport_chosen l r left F G J N right M]
    exact .strict _

theorem selectedMixedFourRaw_reflectObservation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (A : SelectedLocalNineteen W l r
      (selectedMixedFourRawTransport l r left F G J N right M X)
      (selectedMixedFourRawTransport l r left F G J N right M Y)) :
    selectedContextEighteenFour l r X =
      selectedContextEighteenFour l r Y := by
  let R := selectedEighteenRightAfterLeft l r left F G M right
  let base := selectedContextEighteenFour l r
    (selectedEighteenLeftAfterRight l r left F G M right)
  have hlen := congrArg List.length
    (selectedLocalNineteen_preservesEighteenTrace l r A)
  change (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedFourCode base
          (selectedContextEighteenFour l r X)))).length =
    (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedFourCode base
          (selectedContextEighteenFour l r Y)))).length at hlen
  simp only [selectedMixedRightTracePower_length] at hlen
  have hpos : 0 < (selectedContextEighteenTrace l r R).length :=
    selectedMixedRightSeed_tracePositive l r left F G J N right M
  have hc :
      2 * selectedMixedFourCode base
        (selectedContextEighteenFour l r X) + 1 =
      2 * selectedMixedFourCode base
        (selectedContextEighteenFour l r Y) + 1 :=
    Nat.mul_right_cancel hpos hlen
  have hcode :
      selectedMixedFourCode base (selectedContextEighteenFour l r X) =
        selectedMixedFourCode base (selectedContextEighteenFour l r Y) := by
    omega
  exact selectedMixedFourCode_injective base hcode

/-- Exact kernel of THIS concrete typed boundary, not a
classification of all old Type-valued 19D proof classes. -/
theorem selectedMixedFourDescend_eq_iff_observation
    (M : SelectedContextualEighteen W l r J N)
    (q₁ q₂ : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedFourBoundary l r left F G J N right M) q₁ =
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedFourBoundary l r left F G J N right M) q₂ ↔
    selectedNineteenFourObservation l r _ _ q₁ =
      selectedNineteenFourObservation l r _ _ q₂ := by
  constructor
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedNineteenClass l r
                (selectedMixedFourRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedFourRawTransport l r left F G J N right M Y) at h
            rcases Quotient.exact h with ⟨A⟩
            exact selectedMixedFourRaw_reflectObservation
              l r left F G J N right M A
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedContextEighteenFour l r X =
              selectedContextEighteenFour l r Y at h
            change selectedNineteenClass l r
                (selectedMixedFourRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedFourRawTransport l r left F G J N right M Y)
            exact congrArg (selectedNineteenClass l r)
              (selectedMixedFourRaw_eq_of_observation
                l r left F G J N right M h)

/-- The old selected 19D associativity obstruction is
no longer collapsed by the new FOUR-coordinate boundary. -/
theorem selectedMixedFourDescend_separatesAssoc
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedFourBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedContextEighteenAssocLeft l r
          (selectedEighteenLeftAfterRight l r left F G M right))) ≠
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedFourBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedContextEighteenAssocRight l r
          (selectedEighteenLeftAfterRight l r left F G M right))) := by
  intro h
  exact (selectedNineteenFour_separatesAssoc l r
      (selectedEighteenLeftAfterRight l r left F G M right))
    ((selectedMixedFourDescend_eq_iff_observation
      l r left F G J N right M _ _).mp h)

/-- The target anchored witness agrees at the CHOSEN coarse
swap observation only. Global swap naturality is NO_DATA. -/
theorem selectedMixedFourAnchored_chosenSwap
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSwapObservation l r _ _
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
    selectedNineteenSwapObservation l r _ _
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedFourBoundary l r left F G J N right M)
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right))) := by
  exact selectedMixedAnchored_chosenSwap l r left F G J N right
    M (selectedMixedFourAnchored l r left F G J N right M)

/-- Fifth-coordinate separation is sufficient for new
four-observation transport noninjectivity IF an actual equal-four
pair with different active depths is provided; no such witness
is smuggled in as an axiom here. -/
theorem selectedMixedFour_obstruction_of_depth
    (M : SelectedContextualEighteen W l r J N)
    (X Y : selectedMixedLeftNineteenRaw l r left F G J N right)
    (heq : selectedContextEighteenFour l r X =
      selectedContextEighteenFour l r Y)
    (hne : selectedContextEighteenActiveDepth l r X ≠
      selectedContextEighteenActiveDepth l r Y) :
    ¬ Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedFourBoundary l r left F G J N right M)) := by
  intro hinj
  have hClasses : selectedNineteenClass l r X =
      selectedNineteenClass l r Y :=
    hinj ((selectedMixedFourDescend_eq_iff_observation
      l r left F G J N right M _ _).2 heq)
  exact hne (congrArg (selectedNineteenActiveDepthOnQuotient l r _ _) hClasses)

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenActiveDepth
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesActiveDepth
#print axioms PentagonAdjoinedSixCell.selectedNineteenActiveDepthOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenFour
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesFour
#print axioms PentagonAdjoinedSixCell.selectedNineteenFourObservation
#print axioms PentagonAdjoinedSixCell.selectedNineteenFour_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenFour_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedNineteenFour_separatesAssoc
#print axioms PentagonAdjoinedSixCell.selectedMixedFourCode
#print axioms PentagonAdjoinedSixCell.selectedMixedFourCode_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRawTransport
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRawTransport_chosen
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRaw_eq_of_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedFourBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedFourAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRaw_reflectObservation
#print axioms PentagonAdjoinedSixCell.selectedMixedFourDescend_eq_iff_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedFourDescend_separatesAssoc
#print axioms PentagonAdjoinedSixCell.selectedMixedFourAnchored_chosenSwap
#print axioms PentagonAdjoinedSixCell.selectedMixedFour_obstruction_of_depth
end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
