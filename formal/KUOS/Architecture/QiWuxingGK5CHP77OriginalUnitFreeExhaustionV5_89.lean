import KUOS.Architecture.QiWuxingGK5CHP77UnitFreeFingerprintFaithfulnessV5_88

/-!
Qi v5.89 — an ORIGINAL old18D-dependent raw unit-free predicate
and the exact-fiber exhaustiveness question.

Unlike the auxiliary v5.88 grammar, the source count below is defined
by recursion ON ACTUAL ORIGINAL SelectedLocalEighteen proof values,
with all their dependent endpoints intact. UnitLeft/UnitRight contribute
one; reverse preserves; nonassociative chain adds counts.

The intended exact-fiber theorem asserts that every zero-unit raw
N→N old18D proof IS a v5.88 unit-free embedding. It must be justified
by constructor induction and elimination of the ORIGINAL dependent
17D endpoint indices, not by reading a fingerprint as raw proof
equality. Only when this completeness theorem passes Strict Lean may
v5.88 old-five/new-seven quotient faithfulness be transported to the
full actual zero-unit subfamily. No assertion about old18D witnesses
containing units, cross-fiber proofs, global old/new Type19
equivalence, WORLD/20D descent, or action authority is made.

Original Types and all previous source files untouched.
append-only / tighten-only / overwrite-forbidden / same-root.
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

/-- Count actual old18D unit generator occurrences in the unchanged
dependent raw proof itself, independently of its v5.73 fingerprint. -/
def selectedV589OriginalUnitCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) : Nat :=
  match M with
  | .strict _ => 0
  | .unitLeft _ _ _ _ _ => 1
  | .unitRight _ _ _ _ _ => 1
  | .reverse M => selectedV589OriginalUnitCount l r M
  | .chain M L =>
      selectedV589OriginalUnitCount l r M +
        selectedV589OriginalUnitCount l r L

/-- A predicate OF THE ORIGINAL typed old18D source, not an
existential membership definition using the auxiliary grammar. -/
def selectedV589OriginalIsUnitFree (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) : Prop :=
  selectedV589OriginalUnitCount l r M = 0

section OriginalDependentSource

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Independent check: counting unit generators in genuine raw
proofs agrees with counting the two unit atoms after observation. -/
theorem selectedV589OriginalUnitCount_observed
    (M : SelectedLocalEighteen W l r J N) :
    selectedV589OriginalUnitCount l r M =
      selectedV588InnerUnitCount
        (selectedLocalEighteenInnerBracket l r M) := by
  induction M with
  | strict _ => rfl
  | unitLeft _ _ _ _ _ => rfl
  | unitRight _ _ _ _ _ => rfl
  | reverse M ih => exact ih
  | chain A B ihA ihB =>
      change selectedV589OriginalUnitCount l r A +
          selectedV589OriginalUnitCount l r B =
        selectedV588InnerUnitCount
            (selectedLocalEighteenInnerBracket l r A) +
          selectedV588InnerUnitCount
            (selectedLocalEighteenInnerBracket l r B)
      exact congrArg₂ Nat.add ihA ihB

/-- In the original dependent source, strict is unit-free. -/
theorem selectedV589OriginalStrictFree
    (N : SelectedContextualSeventeen W l r H K) :
    selectedV589OriginalIsUnitFree l r
      (SelectedLocalEighteen.strict N) := rfl

/-- Both actual unit constructors have nonzero source unit count;
no old18D endpoint identification is used. -/
theorem selectedV589UnitCountPositive_ofOriginalUnit
    {M : SelectedLocalEighteen W l r J N}
    (hcount : 0 < selectedV589OriginalUnitCount l r M) :
    ¬ selectedV589OriginalIsUnitFree l r M := by
  intro hz
  dsimp [selectedV589OriginalIsUnitFree] at hz
  omega

/-- A source raw proof with zero units has a zero-unit observed
bracket, without promoting that observation to raw equality. -/
theorem selectedV589OriginalFree_observedZero
    (M : SelectedLocalEighteen W l r J N)
    (h : selectedV589OriginalIsUnitFree l r M) :
    selectedV588InnerUnitCount
      (selectedLocalEighteenInnerBracket l r M) = 0 := by
  rw [← selectedV589OriginalUnitCount_observed l r M]
  exact h

/-- v5.88 unit-free embeddings indeed inhabit the NEW ORIGINAL
source predicate, before any exhaustiveness argument. -/
theorem selectedV589EmbeddedOriginalFree
    (N : SelectedContextualSeventeen W l r H K)
    (t : SelectedV588UnitFreeTerm) :
    selectedV589OriginalIsUnitFree l r
      (selectedV588UnitFreeRawEmbed l r N t) := by
  unfold selectedV589OriginalIsUnitFree
  rw [selectedV589OriginalUnitCount_observed l r
      (selectedV588UnitFreeRawEmbed l r N t)]
  rw [selectedV588UnitFreeRaw_observed l r N t]
  exact selectedV588UnitFree_hasZeroUnits t

/-- Explicit transport across a PROVED equality of genuine raw17D
endpoints. This is a cast, not any cross-fiber invented comparison. -/
def selectedV589CastFree (h : J = N)
    (t : SelectedV588UnitFreeTerm) :
    SelectedLocalEighteen W l r J N := by
  cases h
  exact selectedV588UnitFreeRawEmbed l r J t

/-- All ORIGINAL no-unit proofs must be loops. The witness in this
statement includes the required equality of the ORIGINAL endpoints,
rather than silently treating the dependent family as homogeneous. -/
theorem selectedV589OriginalFree_exhausted
    (M : SelectedLocalEighteen W l r J N) :
    selectedV589OriginalIsUnitFree l r M →
      ∃ (h : J = N) (t : SelectedV588UnitFreeTerm),
        M = selectedV589CastFree l r h t := by
  induction M with
  | strict _ =>
      intro _
      exact ⟨rfl, .strict, rfl⟩
  | unitLeft _ _ _ _ _ =>
      intro hz
      simp [selectedV589OriginalIsUnitFree,
        selectedV589OriginalUnitCount] at hz
  | unitRight _ _ _ _ _ =>
      intro hz
      simp [selectedV589OriginalIsUnitFree,
        selectedV589OriginalUnitCount] at hz
  | reverse M ih =>
      intro hz
      have hfree : selectedV589OriginalIsUnitFree l r M := by
        simpa [selectedV589OriginalIsUnitFree,
          selectedV589OriginalUnitCount] using hz
      obtain ⟨he, t, hM⟩ := ih hfree
      cases he
      refine ⟨rfl, .reversed t, ?_⟩
      change SelectedLocalEighteen.reverse M =
        SelectedLocalEighteen.reverse
          (selectedV588UnitFreeRawEmbed l r _ t)
      exact congrArg SelectedLocalEighteen.reverse
        (by simpa only [selectedV589CastFree] using hM)
  | chain A B ihA ihB =>
      intro hz
      have hsum : selectedV589OriginalUnitCount l r A +
          selectedV589OriginalUnitCount l r B = 0 := by
        simpa only [selectedV589OriginalIsUnitFree,
          selectedV589OriginalUnitCount] using hz
      have hfreeA : selectedV589OriginalIsUnitFree l r A := by
        dsimp [selectedV589OriginalIsUnitFree]
        omega
      have hfreeB : selectedV589OriginalIsUnitFree l r B := by
        dsimp [selectedV589OriginalIsUnitFree]
        omega
      obtain ⟨heA, t, hA⟩ := ihA hfreeA
      obtain ⟨heB, u, hB⟩ := ihB hfreeB
      cases heA
      cases heB
      refine ⟨rfl, .joined t u, ?_⟩
      change SelectedLocalEighteen.chain A B =
        SelectedLocalEighteen.chain
          (selectedV588UnitFreeRawEmbed l r _ t)
          (selectedV588UnitFreeRawEmbed l r _ u)
      exact congrArg₂ SelectedLocalEighteen.chain
        (by simpa only [selectedV589CastFree] using hA)
        (by simpa only [selectedV589CastFree] using hB)

/-- Specialize the dependent theorem to an ACTUAL fixed N→N fiber:
every original source proof satisfying the independent unit-count
predicate belongs to v5.88's explicitly certified embedded image. -/
theorem selectedV589OriginalLoop_exhausted
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r N N)
    (h : selectedV589OriginalIsUnitFree l r M) :
    ∃ t : SelectedV588UnitFreeTerm,
      M = selectedV588UnitFreeRawEmbed l r N t := by
  obtain ⟨he, t, hM⟩ :=
    selectedV589OriginalFree_exhausted l r M h
  cases he
  exact ⟨t, by simpa only [selectedV589CastFree] using hM⟩

/-- Genuine ORIGINAL exact-fiber zero-unit membership is
equivalent to membership in the explicit v5.88 embedding image.
This is not a claim of any unit-containing original source. -/
theorem selectedV589OriginalLoopFree_iff_image
    (N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r N N) :
    selectedV589OriginalIsUnitFree l r M ↔
      ∃ t : SelectedV588UnitFreeTerm,
        M = selectedV588UnitFreeRawEmbed l r N t := by
  constructor
  · exact selectedV589OriginalLoop_exhausted l r N M
  · rintro ⟨t, rfl⟩
    exact selectedV589EmbeddedOriginalFree l r N t

/-- Conditional RAW equality on the entire ORIGINAL zero-unit
subfamily is reflected by the genuine source observation. -/
theorem selectedV589OriginalLoopBracketFaithful
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hm : selectedV589OriginalIsUnitFree l r M)
    (hl : selectedV589OriginalIsUnitFree l r L) :
    selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L ↔ M = L := by
  obtain ⟨t, ht⟩ := selectedV589OriginalLoop_exhausted l r N M hm
  obtain ⟨u, hu⟩ := selectedV589OriginalLoop_exhausted l r N L hl
  rw [ht, hu]
  rw [selectedV588UnitFreeRaw_observed l r N t,
    selectedV588UnitFreeRaw_observed l r N u]
  exact (selectedV588UnitFreeRawEq_iff l r N t u).symm

/-- Full ORIGINAL zero-unit same-fiber old-five class faithfulness,
obtained only AFTER exact image exhaustion, not a universal old19
equality reflection for all old18D sources. -/
theorem selectedV589OriginalLoopOldClassFaithful
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hm : selectedV589OriginalIsUnitFree l r M)
    (hl : selectedV589OriginalIsUnitFree l r L) :
    selectedNineteenClass l r (.inherited M) =
        selectedNineteenClass l r (.inherited L) ↔ M = L := by
  obtain ⟨t, ht⟩ := selectedV589OriginalLoop_exhausted l r N M hm
  obtain ⟨u, hu⟩ := selectedV589OriginalLoop_exhausted l r N L hl
  rw [ht, hu]
  constructor
  · intro h
    have htu := (selectedV588UnitFreeOldClassEq_iff l r N t u).mp h
    exact congrArg (selectedV588UnitFreeRawEmbed l r N) htu
  · intro h
    exact congrArg (fun X : SelectedLocalEighteen W l r N N =>
      selectedNineteenClass l r (SelectedContextualEighteen.inherited X)) h

/-- Independent genuine NEW seven-generator class faithfulness on
the exact same complete original no-unit old18D raw subfamily. -/
theorem selectedV589OriginalLoopNewClassFaithful
    (N : SelectedContextualSeventeen W l r H K)
    (M L : SelectedLocalEighteen W l r N N)
    (hm : selectedV589OriginalIsUnitFree l r M)
    (hl : selectedV589OriginalIsUnitFree l r L) :
    selectedRawCongruentClass l r (.inherited M) =
        selectedRawCongruentClass l r (.inherited L) ↔ M = L := by
  obtain ⟨t, ht⟩ := selectedV589OriginalLoop_exhausted l r N M hm
  obtain ⟨u, hu⟩ := selectedV589OriginalLoop_exhausted l r N L hl
  rw [ht, hu]
  constructor
  · intro h
    have htu := (selectedV588UnitFreeNewClassEq_iff l r N t u).mp h
    exact congrArg (selectedV588UnitFreeRawEmbed l r N) htu
  · intro h
    exact congrArg (fun X : SelectedLocalEighteen W l r N N =>
      selectedRawCongruentClass l r (SelectedContextualEighteen.inherited X)) h

end OriginalDependentSource

#print axioms PentagonAdjoinedSixCell.selectedV589OriginalUnitCount
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalIsUnitFree
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalUnitCount_observed
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalStrictFree
#print axioms PentagonAdjoinedSixCell.selectedV589UnitCountPositive_ofOriginalUnit
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalFree_observedZero
#print axioms PentagonAdjoinedSixCell.selectedV589EmbeddedOriginalFree
#print axioms PentagonAdjoinedSixCell.selectedV589CastFree
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalFree_exhausted
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalLoop_exhausted
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalLoopFree_iff_image
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalLoopBracketFaithful
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalLoopOldClassFaithful
#print axioms PentagonAdjoinedSixCell.selectedV589OriginalLoopNewClassFaithful

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
