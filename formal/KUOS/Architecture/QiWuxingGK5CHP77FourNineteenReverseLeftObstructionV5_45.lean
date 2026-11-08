import KUOS.Architecture.QiWuxingGK5CHP77TripleNineteenAssocObstructionV5_44

/-!
Qi v5.45 — exact-fiber 19D FOUR-coordinate observation, an
actually inhabited typed anchored LR-to-RL boundary reflecting
these four coordinates, and a further local nonfaithfulness
obstruction with strictly typed proof values.

The prior genuine 19D invariants are exterior trace LENGTH,
active nonempty-chain count, raw reverse-node count, and
left-nested-chain count. Together they descend to each SAME
17D dependent endpoint 19D proof quotient. An injective
nested Nat.pair code and the real RL trace-power witness
construct a pointed boundary whose exact quotient kernel
is equality of the FOUR source observations. This concrete
map separates the v5.44 association witness.

The selected local 19D presentation has exactly five
constructors and its unit comparisons apply ONLY to
old inherited 18D proof terms. We prove those constructors
also preserve a fifth raw 18D count: chain nodes whose LEFT
operand has the top-level reverse constructor.

In one genuine exact 17D fiber, compare
  chain (chain (strict J) (reverse (strict J))) X
  chain (chain (reverse (strict J)) (strict J)) X.
Both have the SAME complete exterior fine trace and
the SAME four existing observations, even for arbitrary X.
But their fifth reverse-left count differs by one,
so their genuine 19D quotient classes are distinct;
the constructed four-coordinate boundary collapses them.
There is NO claimed 19D comparison between the pair.

This certifies NON-faithfulness of the PARTICULAR boundary;
another faithful boundary's existence/nonexistence remains
NO_DATA. The chosen-point swap equality is independent of
global swap naturality, which remains unproved. No original
Type-valued proof equality, heterogeneous 20D exchange,
new coherence constructor, or unrestricted gluing is added.

Old F55/P77/GK5CG, original 6D–19D Type evidence,
independent selected presentations, public root107,
fixed Lean/mathlib and protected PR #1558 remain unchanged.
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

/-- Count raw contextual chain nodes with an immediate
reverse node on their LEFT. Defined polymorphically over
all genuine dependent 17D endpoints for recursive calls. -/
def selectedContextEighteenReverseLeftCount (l r : W)
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
  | .whiskerLeft _ _ _ M =>
      selectedContextEighteenReverseLeftCount l r M
  | .whiskerRight _ _ M _ =>
      selectedContextEighteenReverseLeftCount l r M
  | .strict _ => 0
  | .reverse M => selectedContextEighteenReverseLeftCount l r M
  | .chain M L =>
      selectedContextEighteenReverseLeftCount l r M +
        selectedContextEighteenReverseLeftCount l r L +
        (if selectedContextEighteenTopTag l r M = 4 then 1 else 0)

section FourObservation

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Four original quotient-stable raw Type-witness observations. -/
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
  exact Prod.ext
    (selectedLocalNineteen_preservesTriple l r A)
    (selectedLocalNineteen_preservesLeftNestedCount l r A)

/-- The FOUR-vector genuinely descends through old local
selected 19D proofs, independently at each dependent fiber. -/
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

/-- This fifth observation is also invariant under each of
the FIVE genuine selected local 19D comparison constructors:
the unit generators can only paste strict to inherited old 18D. -/
theorem selectedLocalNineteen_preservesReverseLeftCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseLeftCount l r M =
      selectedContextEighteenReverseLeftCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

def selectedNineteenReverseLeftOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenReverseLeftCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseLeftCount l r A)

/-- Both genuine source values have the SAME dependent
17D endpoints, not a heterogeneous mixed-fiber cast. -/
def selectedContextEighteenStrictReverseLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain (.chain (.strict J) (.reverse (.strict J))) M

def selectedContextEighteenStrictReverseRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain (.chain (.reverse (.strict J)) (.strict J)) M

/-- Even the FULL ordered exterior List Bool trace is the same. -/
theorem selectedContextEighteenStrictReverse_trace
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r
      (selectedContextEighteenStrictReverseLeft l r M) =
    selectedContextEighteenTrace l r
      (selectedContextEighteenStrictReverseRight l r M) :=
  rfl

/-- The TWO genuinely distinct raw 18D terms have exactly
the same four quotient-stable numerical invariants. -/
theorem selectedContextEighteenStrictReverse_fourEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenFour l r
        (selectedContextEighteenStrictReverseLeft l r M) =
      selectedContextEighteenFour l r
        (selectedContextEighteenStrictReverseRight l r M) :=
  rfl

theorem selectedNineteenFour_strictReverseEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenFourObservation l r J N
      (selectedNineteenClass l r
        (selectedContextEighteenStrictReverseLeft l r M)) =
    selectedNineteenFourObservation l r J N
      (selectedNineteenClass l r
        (selectedContextEighteenStrictReverseRight l r M)) :=
  rfl

/-- The fifth quotient-stable raw count differs by one,
despite full trace equality and equality of FOUR coordinates. -/
theorem selectedContextEighteenStrictReverse_reverseLeftDiff
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseLeftCount l r
        (selectedContextEighteenStrictReverseRight l r M) =
      selectedContextEighteenReverseLeftCount l r
        (selectedContextEighteenStrictReverseLeft l r M) + 1 := by
  change (0 + 0 + 1) +
      selectedContextEighteenReverseLeftCount l r M + 0 =
    ((0 + 0 + 0) +
      selectedContextEighteenReverseLeftCount l r M + 0) + 1
  omega

theorem selectedNineteenStrictReverse_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenClass l r
        (selectedContextEighteenStrictReverseLeft l r M) ≠
      selectedNineteenClass l r
        (selectedContextEighteenStrictReverseRight l r M) := by
  intro h
  have hc := congrArg (selectedNineteenReverseLeftOnQuotient l r _ _) h
  change selectedContextEighteenReverseLeftCount l r
      (selectedContextEighteenStrictReverseLeft l r M) =
    selectedContextEighteenReverseLeftCount l r
      (selectedContextEighteenStrictReverseRight l r M) at hc
  rw [selectedContextEighteenStrictReverse_reverseLeftDiff l r M] at hc
  omega

theorem selectedNineteenStrictReverse_noLocal
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (selectedContextEighteenStrictReverseLeft l r M)
      (selectedContextEighteenStrictReverseRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedNineteenStrictReverse_classDistinct l r M)
    (Quotient.sound ⟨A⟩)

/-- The nontrivial four-observation fiber exists whenever
an original genuine contextual 18D witness exists. -/
theorem selectedNineteenFour_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedNineteenFourObservation l r J N) := by
  intro hinj
  exact (selectedNineteenStrictReverse_classDistinct l r M)
    (hinj (selectedNineteenFour_strictReverseEq l r M))

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

/-- An injective pointed code for FOUR original 19D source
quotient invariants, using only pinned Mathlib Nat.pair. -/
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
  have hPair :
      Nat.pair (Nat.pair (Nat.pair p.1.1.1 p.1.1.2) p.1.2) p.2 =
      Nat.pair (Nat.pair (Nat.pair q.1.1.1 q.1.1.2) q.1.2) q.2 :=
    selectedMixedLengthCode_injective
      (Nat.pair (Nat.pair (Nat.pair base.1.1.1 base.1.1.2)
        base.1.2) base.2) h
  have hout := Nat.pair_eq_pair.mp hPair
  have hmid := Nat.pair_eq_pair.mp hout.1
  have hin := Nat.pair_eq_pair.mp hmid.1
  exact Prod.ext (Prod.ext (Prod.ext hin.1 hin.2) hmid.2) hout.2

/-- A total, real LR-to-RL raw proof transport into the
distinct original RL 17D endpoint fiber. -/
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

/-- Preservation of actual 19D Type-valued comparison proofs,
not merely postulated existence of a quotient function. -/
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

theorem selectedMixedFourAnchored_chosenClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedFourBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenClass l r
        (selectedEighteenRightAfterLeft l r left F G M right) := by
  exact selectedMixedAnchoredDescend_chosenClass
    l r left F G J N right M
    (selectedMixedFourAnchored l r left F G J N right M)

/-- Comparison in the RL target reflects the FOUR original
source observations but NOT original 19D comparison values. -/
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
      2 * selectedMixedFourCode base (selectedContextEighteenFour l r X) + 1 =
      2 * selectedMixedFourCode base (selectedContextEighteenFour l r Y) + 1 :=
    Nat.mul_right_cancel hpos hlen
  have hcode :
      selectedMixedFourCode base (selectedContextEighteenFour l r X) =
        selectedMixedFourCode base (selectedContextEighteenFour l r Y) := by
    omega
  exact selectedMixedFourCode_injective base hcode

/-- Exact kernel classification of THIS four-variable boundary:
target class equality iff all four source observables agree. -/
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

/-- The concrete four-coordinate boundary now separates
the old v5.44 association-bracketing source witnesses. -/
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
  have hobs := (selectedMixedFourDescend_eq_iff_observation
    l r left F G J N right M _ _).mp h
  have hleft := congrArg Prod.snd hobs
  change selectedContextEighteenLeftNestedCount l r
      (selectedContextEighteenAssocLeft l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
    selectedContextEighteenLeftNestedCount l r
      (selectedContextEighteenAssocRight l r
        (selectedEighteenLeftAfterRight l r left F G M right)) at hleft
  rw [selectedContextEighteenAssoc_leftNested l r
    (selectedEighteenLeftAfterRight l r left F G M right)] at hleft
  omega

/-- Unlike that earlier association pair, the new exact
same-FIBER strict/reverse ordered pair remains COLLAPSED
by this four-coordinate map. -/
theorem selectedMixedFourDescend_collapsesStrictReverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedFourBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedContextEighteenStrictReverseLeft l r
          (selectedEighteenLeftAfterRight l r left F G M right))) =
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedFourBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedContextEighteenStrictReverseRight l r
          (selectedEighteenLeftAfterRight l r left F G M right))) := by
  apply (selectedMixedFourDescend_eq_iff_observation
    l r left F G J N right M _ _).2
  exact selectedNineteenFour_strictReverseEq l r
    (selectedEighteenLeftAfterRight l r left F G M right)

theorem selectedMixedFourDescend_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedFourBoundary l r left F G J N right M)) := by
  intro hinj
  let X := selectedEighteenLeftAfterRight l r left F G M right
  exact (selectedNineteenStrictReverse_classDistinct l r X)
    (hinj (selectedMixedFourDescend_collapsesStrictReverse
      l r left F G J N right M))

theorem selectedMixedFourBoundary_noReflection
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (∀ {X Y : selectedMixedLeftNineteenRaw
          l r left F G J N right},
      SelectedLocalNineteen W l r
        ((selectedMixedFourBoundary l r left F G J N right M).rawTransport X)
        ((selectedMixedFourBoundary l r left F G J N right M).rawTransport Y) →
      SelectedLocalNineteen W l r X Y) := by
  rintro ⟨reflectLocal⟩
  let B : SelectedMixedNineteenFaithfulBoundary
      l r left F G J N right :=
    { boundary := selectedMixedFourBoundary l r left F G J N right M
      reflectLocal := reflectLocal }
  exact (selectedMixedFourDescend_notInjective
    l r left F G J N right M)
    (selectedMixedFaithfulDescend_injective l r left F G J N right B)

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

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseLeftCount
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenFour
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesFour
#print axioms PentagonAdjoinedSixCell.selectedNineteenFourObservation
#print axioms PentagonAdjoinedSixCell.selectedNineteenFour_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenFour_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseLeftCount
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseLeftOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictReverseLeft
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictReverseRight
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictReverse_trace
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictReverse_fourEq
#print axioms PentagonAdjoinedSixCell.selectedNineteenFour_strictReverseEq
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenStrictReverse_reverseLeftDiff
#print axioms PentagonAdjoinedSixCell.selectedNineteenStrictReverse_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedNineteenStrictReverse_noLocal
#print axioms PentagonAdjoinedSixCell.selectedNineteenFour_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedFourCode
#print axioms PentagonAdjoinedSixCell.selectedMixedFourCode_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRawTransport
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRawTransport_chosen
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRaw_eq_of_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedFourBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedFourAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedFourAnchored_chosenClass
#print axioms PentagonAdjoinedSixCell.selectedMixedFourRaw_reflectObservation
#print axioms PentagonAdjoinedSixCell.selectedMixedFourDescend_eq_iff_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedFourDescend_separatesAssoc
#print axioms PentagonAdjoinedSixCell.selectedMixedFourDescend_collapsesStrictReverse
#print axioms PentagonAdjoinedSixCell.selectedMixedFourDescend_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedFourBoundary_noReflection
#print axioms PentagonAdjoinedSixCell.selectedMixedFourAnchored_chosenSwap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
