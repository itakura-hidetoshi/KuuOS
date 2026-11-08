import KUOS.Architecture.QiWuxingGK5CHP77PairedNineteenObstructionV5_43

/-!
Qi v5.44 — exact-fiber 19D triple observation, real typed anchored
LR-to-RL boundary reflecting trace length, active-chain count and
reverse count, and a residual nonassociativity obstruction.

A third observation, the actual reverse-node count on raw contextual
18D proofs, already descends through the five true selected 19D
constructors (v5.43). We combine it with the v5.42 trace length
and active-chain observations without replacing the source types.

The existing positive-length RL typed trace-power family and an
injective nested Nat.pair code construct a nonconstant three-variable
boundary. Its selected-19D quotient kernel equals exactly the
three-coordinate source observation equality. The v5.43
double-reversal obstruction, previously collapsed by the two-variable
boundary, is separated by this more informative transport.

A further true quotient invariant counts chain-nodes whose left
operand is itself a raw chain. This count is invariant under all
FIVE old selected local 19D constructors: their unit generators
only paste strict to an INHERITED old 18D witness. Two actual
same-endpoint contextual 18D proofs
  (X ; reverse X) ; X    and    X ; (reverse X ; X)
have identical full ordered exterior traces, active-chain counts
(for nonempty exterior history), and reverse-node counts, yet
their new left-nested count differs by one. Their genuine 19D
quotient classes are distinct and the particular triple boundary
collapses them. No raw equality, associative coherence generator,
unrestricted 20D exchange, or gluing axiom is asserted.

The obstruction concerns the CURRENT selected 19D presentation and
THIS explicitly constructed triple boundary. Existence of a
different fully faithful boundary, global swap naturality and
original higher-cell comparison are not established (NO_DATA).

Old F55/P77/GK5CG, 6D-19D Type values, independent presentations,
public root107, fixed Lean/mathlib and protected #1558 unchanged.
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

/-- Count the raw chain nodes with another raw chain on the LEFT.
The unit 19D generators only paste strict and inherited old
proofs, so they never introduce such a node. -/
def selectedContextEighteenLeftNestedCount (l r : W)
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
      selectedContextEighteenLeftNestedCount l r M
  | .whiskerRight _ _ M _ =>
      selectedContextEighteenLeftNestedCount l r M
  | .strict _ => 0
  | .reverse M => selectedContextEighteenLeftNestedCount l r M
  | .chain M L =>
      selectedContextEighteenLeftNestedCount l r M +
        selectedContextEighteenLeftNestedCount l r L +
        (if selectedContextEighteenTopTag l r M = 5 then 1 else 0)

section TripleObservation

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The actual raw contextual 18D history in the NEW triple
observation: length, active nonempty chain nodes, reverse nodes. -/
def selectedContextEighteenTriple
    (M : SelectedContextualEighteen W l r J N) : (Nat × Nat) × Nat :=
  (selectedContextEighteenLengthActive l r M,
    selectedContextEighteenReverseCount l r M)

/-- Each coordinate has already been independently proved
invariant under the five actual selected local 19D constructors. -/
theorem selectedLocalNineteen_preservesTriple
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenTriple l r M =
      selectedContextEighteenTriple l r L := by
  have ht := congrArg List.length
    (selectedLocalNineteen_preservesEighteenTrace l r A)
  have ha := selectedLocalNineteen_preservesActiveChainCount l r A
  have hr := selectedLocalNineteen_preservesReverseCount l r A
  exact Prod.ext (Prod.ext ht ha) hr

/-- Genuine quotient observation in ONE exact 17D endpoint fiber,
not an assumed equality of original Type-valued proofs. -/
def selectedNineteenTripleObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → (Nat × Nat) × Nat :=
  fun q => (selectedNineteenLengthActiveObservation l r J N q,
    selectedNineteenReverseCountOnQuotient l r J N q)

/-- Exact class computation of the three coordinates. -/
theorem selectedNineteenTriple_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenTripleObservation l r J N
      (selectedNineteenClass l r M) =
        selectedContextEighteenTriple l r M :=
  rfl

theorem selectedNineteenTriple_eq_iff
    (J N : SelectedContextualSeventeen W l r H K)
    (q₁ q₂ : Quotient (selectedNineteenSetoid l r J N)) :
    selectedNineteenTripleObservation l r J N q₁ =
      selectedNineteenTripleObservation l r J N q₂ ↔
      selectedNineteenLengthActiveObservation l r J N q₁ =
        selectedNineteenLengthActiveObservation l r J N q₂ ∧
      selectedNineteenReverseCountOnQuotient l r J N q₁ =
        selectedNineteenReverseCountOnQuotient l r J N q₂ := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨h₁, h₂⟩
    exact Prod.ext h₁ h₂

/-- Invariance is verified over EACH existing selected local
19D comparison constructor, rather than asserted as an axiom. -/
theorem selectedLocalNineteen_preservesLeftNestedCount
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenLeftNestedCount l r M =
      selectedContextEighteenLeftNestedCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- A FOURTH independent exact-fiber 19D quotient observation,
not assumed equivalent to original higher proof identity. -/
def selectedNineteenLeftNestedOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenLeftNestedCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesLeftNestedCount l r A)

/-- In one and the same dependent 17D endpoint fiber:
two raw pastings with an unchanged genuine original proof X. -/
def selectedContextEighteenAssocLeft
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain (.chain M (.reverse M)) M

def selectedContextEighteenAssocRight
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain M (.chain (.reverse M) M)

/-- Even the FULL ordered exterior List Bool traces agree.
This is list concatenation associativity, NOT a selected 19D
associativity coherence proof. -/
theorem selectedContextEighteenAssoc_trace
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r
        (selectedContextEighteenAssocLeft l r M) =
      selectedContextEighteenTrace l r
        (selectedContextEighteenAssocRight l r M) := by
  change ((selectedContextEighteenTrace l r M ++
      selectedContextEighteenTrace l r M) ++
      selectedContextEighteenTrace l r M) =
    selectedContextEighteenTrace l r M ++
      (selectedContextEighteenTrace l r M ++
        selectedContextEighteenTrace l r M)
  exact List.append_assoc _ _ _

/-- The actual reverse-node counts are the same in both
parenthesized contextual proof terms. -/
theorem selectedContextEighteenAssoc_reverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseCount l r
        (selectedContextEighteenAssocLeft l r M) =
      selectedContextEighteenReverseCount l r
        (selectedContextEighteenAssocRight l r M) := by
  change (selectedContextEighteenReverseCount l r M +
      (selectedContextEighteenReverseCount l r M + 1)) +
      selectedContextEighteenReverseCount l r M =
    selectedContextEighteenReverseCount l r M +
      ((selectedContextEighteenReverseCount l r M + 1) +
        selectedContextEighteenReverseCount l r M)
  omega

/-- For a proof X with nonempty exterior history, both
parenthesizations have identical active nonempty-chain counts. -/
theorem selectedContextEighteenAssoc_active
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedContextEighteenActiveChainCount l r
        (selectedContextEighteenAssocLeft l r M) =
      selectedContextEighteenActiveChainCount l r
        (selectedContextEighteenAssocRight l r M) := by
  let t := (selectedContextEighteenTrace l r M).length
  let a := selectedContextEighteenActiveChainCount l r M
  change (a + a + (if 0 < t + t then 1 else 0)) + a +
      (if 0 < (selectedContextEighteenTrace l r M ++
            selectedContextEighteenTrace l r M).length + t then 1 else 0) =
    a + (a + a + (if 0 < t + t then 1 else 0)) +
      (if 0 < t + (selectedContextEighteenTrace l r M ++
            selectedContextEighteenTrace l r M).length then 1 else 0)
  simp only [List.length_append]
  have htwo : 0 < t + t := by omega
  have houterLeft : 0 < (selectedContextEighteenTrace l r M).length +
      (selectedContextEighteenTrace l r M).length + t := by omega
  have houterRight : 0 < t +
      ((selectedContextEighteenTrace l r M).length +
        (selectedContextEighteenTrace l r M).length) := by omega
  simp only [if_pos htwo, if_pos houterLeft, if_pos houterRight]
  omega

/-- The raw LEFT-nested chain count differs by precisely one
for EVERY old 18D term; no new coherence is introduced. -/
theorem selectedContextEighteenAssoc_leftNested
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenLeftNestedCount l r
        (selectedContextEighteenAssocLeft l r M) =
      selectedContextEighteenLeftNestedCount l r
        (selectedContextEighteenAssocRight l r M) + 1 := by
  let a := selectedContextEighteenLeftNestedCount l r M
  let v := if selectedContextEighteenTopTag l r M = 5 then 1 else 0
  change (a + a + v) + a + 1 =
    (a + (a + a + 0) + v) + 1
  omega

/-- The old local 19D quotient DOES NOT identify the two actual
raw 18D parenthesizations: fourth invariant supplies a witness. -/
theorem selectedNineteenAssoc_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenClass l r
        (selectedContextEighteenAssocLeft l r M) ≠
      selectedNineteenClass l r
        (selectedContextEighteenAssocRight l r M) := by
  intro h
  have hc := congrArg (selectedNineteenLeftNestedOnQuotient l r _ _) h
  change selectedContextEighteenLeftNestedCount l r
      (selectedContextEighteenAssocLeft l r M) =
    selectedContextEighteenLeftNestedCount l r
      (selectedContextEighteenAssocRight l r M) at hc
  rw [selectedContextEighteenAssoc_leftNested l r M] at hc
  omega

/-- No genuine selected local 19D Type-valued comparison can
link the two bracketings, in this selected presentation. -/
theorem selectedNineteenAssoc_noLocal
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (selectedContextEighteenAssocLeft l r M)
      (selectedContextEighteenAssocRight l r M)) := by
  rintro ⟨A⟩
  exact (selectedNineteenAssoc_classDistinct l r M) (Quotient.sound ⟨A⟩)

/-- Yet all THREE numerical observations agree, given the
strictly nonempty exterior-history condition. -/
theorem selectedNineteenTriple_assocEq
    (M : SelectedContextualEighteen W l r J N)
    (hpos : 0 < (selectedContextEighteenTrace l r M).length) :
    selectedNineteenTripleObservation l r _ _
        (selectedNineteenClass l r
          (selectedContextEighteenAssocLeft l r M)) =
      selectedNineteenTripleObservation l r _ _
        (selectedNineteenClass l r
          (selectedContextEighteenAssocRight l r M)) := by
  change selectedContextEighteenTriple l r
      (selectedContextEighteenAssocLeft l r M) =
    selectedContextEighteenTriple l r
      (selectedContextEighteenAssocRight l r M)
  exact Prod.ext (Prod.ext
    (congrArg List.length (selectedContextEighteenAssoc_trace l r M))
    (selectedContextEighteenAssoc_active l r M hpos))
    (selectedContextEighteenAssoc_reverse l r M)

end TripleObservation

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

/-- Injective nested pairing of the THREE genuine source quotient
observations into the old actual RL typed trace-power index. -/
def selectedMixedTripleCode
    (base p : (Nat × Nat) × Nat) : Nat :=
  selectedMixedLengthCode
    (Nat.pair (Nat.pair base.1.1 base.1.2) base.2)
    (Nat.pair (Nat.pair p.1.1 p.1.2) p.2)

theorem selectedMixedTripleCode_injective (base : (Nat × Nat) × Nat) :
    Function.Injective (selectedMixedTripleCode base) := by
  intro p q h
  have hPair : Nat.pair (Nat.pair p.1.1 p.1.2) p.2 =
      Nat.pair (Nat.pair q.1.1 q.1.2) q.2 :=
    selectedMixedLengthCode_injective
      (Nat.pair (Nat.pair base.1.1 base.1.2) base.2) h
  have hParts := Nat.pair_eq_pair.mp hPair
  have hInner := Nat.pair_eq_pair.mp hParts.1
  exact Prod.ext (Prod.ext hInner.1 hInner.2) hParts.2

/-- A total, true Type-valued LR-to-RL 18D map.
The target remains in its INDEPENDENT exact RL 17D endpoint fiber. -/
def selectedMixedTripleRawTransport
    (M : SelectedContextualEighteen W l r J N)
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedRightNineteenRaw l r left F G J N right :=
  selectedMixedRightTracePower l r left F G J N right
    (selectedEighteenRightAfterLeft l r left F G M right)
    (selectedMixedTripleCode
      (selectedContextEighteenTriple l r
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedContextEighteenTriple l r X))

/-- The actual distinguished LR proof maps to the actual RL
proof, not an observation-equal surrogate. -/
theorem selectedMixedTripleRawTransport_chosen
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedTripleRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right) =
      selectedEighteenRightAfterLeft l r left F G M right := by
  simp [selectedMixedTripleRawTransport, selectedMixedTripleCode,
    selectedMixedLengthCode, selectedMixedRightTracePower]

/-- Equal source triples produce identical actual RL raw values. -/
theorem selectedMixedTripleRaw_eq_of_observation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (h : selectedContextEighteenTriple l r X =
      selectedContextEighteenTriple l r Y) :
    selectedMixedTripleRawTransport l r left F G J N right M X =
      selectedMixedTripleRawTransport l r left F G J N right M Y := by
  unfold selectedMixedTripleRawTransport
  rw [h]

/-- Every actual source local 19D comparison maps to a true
target local 19D comparison (its strict constructor). -/
def selectedMixedTripleBoundary
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenBoundary l r left F G J N right where
  rawTransport := selectedMixedTripleRawTransport l r left F G J N right M
  localTransport := by
    intro X Y A
    have hObs : selectedContextEighteenTriple l r X =
        selectedContextEighteenTriple l r Y :=
      selectedLocalNineteen_preservesTriple l r A
    have hEq := selectedMixedTripleRaw_eq_of_observation
      l r left F G J N right M hObs
    change SelectedLocalNineteen W l r
      (selectedMixedTripleRawTransport l r left F G J N right M X)
      (selectedMixedTripleRawTransport l r left F G J N right M Y)
    rw [hEq]
    exact .strict _

/-- Actual chosen target 19D proof value, as opposed to an
assumed heterogeneous raw equality. -/
def selectedMixedTripleAnchored
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenAnchored l r left F G J N right M where
  boundary := selectedMixedTripleBoundary l r left F G J N right M
  chosenComparison := by
    change SelectedLocalNineteen W l r
      (selectedMixedTripleRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedEighteenRightAfterLeft l r left F G M right)
    rw [selectedMixedTripleRawTransport_chosen l r left F G J N right M]
    exact .strict _

/-- The chosen 19D proof quotient class is mapped to the
independently constructed original RL class. -/
theorem selectedMixedTripleAnchored_chosenClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedTripleBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenClass l r
        (selectedEighteenRightAfterLeft l r left F G M right) := by
  exact selectedMixedAnchoredDescend_chosenClass
    l r left F G J N right M
    (selectedMixedTripleAnchored l r left F G J N right M)

/-- TARGET comparison reflection is established ONLY for
the THREE numerical source observations. -/
theorem selectedMixedTripleRaw_reflectObservation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (A : SelectedLocalNineteen W l r
      (selectedMixedTripleRawTransport l r left F G J N right M X)
      (selectedMixedTripleRawTransport l r left F G J N right M Y)) :
    selectedContextEighteenTriple l r X =
      selectedContextEighteenTriple l r Y := by
  let R := selectedEighteenRightAfterLeft l r left F G M right
  let base := selectedContextEighteenTriple l r
    (selectedEighteenLeftAfterRight l r left F G M right)
  have hlen := congrArg List.length
    (selectedLocalNineteen_preservesEighteenTrace l r A)
  change (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedTripleCode base
          (selectedContextEighteenTriple l r X)))).length =
    (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedTripleCode base
          (selectedContextEighteenTriple l r Y)))).length at hlen
  simp only [selectedMixedRightTracePower_length] at hlen
  have hpos : 0 < (selectedContextEighteenTrace l r R).length :=
    selectedMixedRightSeed_tracePositive l r left F G J N right M
  have hc :
      2 * selectedMixedTripleCode base
        (selectedContextEighteenTriple l r X) + 1 =
      2 * selectedMixedTripleCode base
        (selectedContextEighteenTriple l r Y) + 1 :=
    Nat.mul_right_cancel hpos hlen
  have hcode :
      selectedMixedTripleCode base (selectedContextEighteenTriple l r X) =
        selectedMixedTripleCode base (selectedContextEighteenTriple l r Y) := by
    omega
  exact selectedMixedTripleCode_injective base hcode

/-- Exact source kernel for THIS explicitly constructed boundary:
target 19D class equality iff equality of all three source
numbers. This does not reflect original 19D comparison values. -/
theorem selectedMixedTripleDescend_eq_iff_observation
    (M : SelectedContextualEighteen W l r J N)
    (q₁ q₂ : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedTripleBoundary l r left F G J N right M) q₁ =
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedTripleBoundary l r left F G J N right M) q₂ ↔
    selectedNineteenTripleObservation l r _ _ q₁ =
      selectedNineteenTripleObservation l r _ _ q₂ := by
  constructor
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedNineteenClass l r
                (selectedMixedTripleRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedTripleRawTransport l r left F G J N right M Y) at h
            rcases Quotient.exact h with ⟨A⟩
            exact selectedMixedTripleRaw_reflectObservation
              l r left F G J N right M A
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedContextEighteenTriple l r X =
              selectedContextEighteenTriple l r Y at h
            change selectedNineteenClass l r
                (selectedMixedTripleRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedTripleRawTransport l r left F G J N right M Y)
            exact congrArg (selectedNineteenClass l r)
              (selectedMixedTripleRaw_eq_of_observation
                l r left F G J N right M h)

/-- Unlike the v5.43 paired map, this triple map actually
separates the old genuine double-reversal classes. -/
theorem selectedMixedTripleDescend_separatesDoubleReverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedTripleBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) ≠
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedTripleBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedContextEighteenDoubleReverse l r
          (selectedEighteenLeftAfterRight l r left F G M right))) := by
  intro h
  have hobs := (selectedMixedTripleDescend_eq_iff_observation
    l r left F G J N right M _ _).mp h
  have hreverse := congrArg Prod.snd hobs
  change selectedContextEighteenReverseCount l r
      (selectedEighteenLeftAfterRight l r left F G M right) =
    selectedContextEighteenReverseCount l r
      (selectedContextEighteenDoubleReverse l r
        (selectedEighteenLeftAfterRight l r left F G M right)) at hreverse
  rw [selectedContextEighteenDoubleReverse_reverseCount
    l r (selectedEighteenLeftAfterRight l r left F G M right)] at hreverse
  omega

/-- The actual LR source proof has at least the false/true
ordered exterior events, so the association obstruction applies. -/
theorem selectedMixedLeftSeed_tracePositive
    (M : SelectedContextualEighteen W l r J N) :
    0 < (selectedContextEighteenTrace l r
      (selectedEighteenLeftAfterRight l r left F G M right)).length := by
  rw [(selectedEighteenMixedTraceValues l r left F G M right).1]
  simp

/-- The three-number quotient observation is NOT injective on
the ACTUAL original LR fiber, using the two true raw brackets. -/
theorem selectedMixedLeftTriple_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedNineteenTripleObservation l r
      (selectedSeventeenLeftAfterRight l r left F G J right)
      (selectedSeventeenLeftAfterRight l r left F G N right)) := by
  intro hinj
  let X := selectedEighteenLeftAfterRight l r left F G M right
  exact (selectedNineteenAssoc_classDistinct l r X)
    (hinj (selectedNineteenTriple_assocEq l r X
      (selectedMixedLeftSeed_tracePositive l r left F G J N right M)))

/-- Residual obstruction for THIS triple boundary: it collapses
two actually DISTINCT source classes whose full fine traces,
active-chain counts, and reverse counts all agree. -/
theorem selectedMixedTripleDescend_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedTripleBoundary l r left F G J N right M)) := by
  intro hinj
  let X := selectedEighteenLeftAfterRight l r left F G M right
  have hObs := selectedNineteenTriple_assocEq l r X
    (selectedMixedLeftSeed_tracePositive l r left F G J N right M)
  have hCollapsed := (selectedMixedTripleDescend_eq_iff_observation
    l r left F G J N right M _ _).2 hObs
  exact (selectedNineteenAssoc_classDistinct l r X) (hinj hCollapsed)

/-- The particular boundary has no full Type-valued 19D
comparison-reflecting witness, since that would imply injectivity.
No claim about OTHER possible boundaries. -/
theorem selectedMixedTripleBoundary_noReflection
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (∀ {X Y : selectedMixedLeftNineteenRaw
          l r left F G J N right},
      SelectedLocalNineteen W l r
        ((selectedMixedTripleBoundary l r left F G J N right M).rawTransport X)
        ((selectedMixedTripleBoundary l r left F G J N right M).rawTransport Y) →
      SelectedLocalNineteen W l r X Y) := by
  rintro ⟨reflectLocal⟩
  let B : SelectedMixedNineteenFaithfulBoundary
      l r left F G J N right :=
    { boundary := selectedMixedTripleBoundary l r left F G J N right M
      reflectLocal := reflectLocal }
  exact (selectedMixedTripleDescend_notInjective
    l r left F G J N right M)
    (selectedMixedFaithfulDescend_injective l r left F G J N right B)

/-- The chosen LR/RL class equality yields the certified local
coarse swap equality, NOT a global swap-natural square. -/
theorem selectedMixedTripleAnchored_chosenSwap
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSwapObservation l r _ _
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapObservation l r _ _
        (selectedMixedBoundaryDescend l r left F G J N right
          (selectedMixedTripleBoundary l r left F G J N right M)
          (selectedNineteenClass l r
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  exact selectedMixedAnchored_chosenSwap l r left F G J N right
    M (selectedMixedTripleAnchored l r left F G J N right M)

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenTriple
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesTriple
#print axioms PentagonAdjoinedSixCell.selectedNineteenTripleObservation
#print axioms PentagonAdjoinedSixCell.selectedNineteenTriple_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenTriple_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenLeftNestedCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesLeftNestedCount
#print axioms PentagonAdjoinedSixCell.selectedNineteenLeftNestedOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenAssocLeft
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenAssocRight
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenAssoc_trace
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenAssoc_reverse
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenAssoc_active
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenAssoc_leftNested
#print axioms PentagonAdjoinedSixCell.selectedNineteenAssoc_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedNineteenAssoc_noLocal
#print axioms PentagonAdjoinedSixCell.selectedNineteenTriple_assocEq
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleCode
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleCode_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleRawTransport
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleRawTransport_chosen
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleRaw_eq_of_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleAnchored_chosenClass
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleRaw_reflectObservation
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleDescend_eq_iff_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleDescend_separatesDoubleReverse
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftSeed_tracePositive
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftTriple_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleDescend_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleBoundary_noReflection
#print axioms PentagonAdjoinedSixCell.selectedMixedTripleAnchored_chosenSwap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
