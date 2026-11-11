import KUOS.Architecture.QiWuxingGK5CHP77MixedStrictUnitProvenanceObstructionV5_96

/-!
Qi v5.97 — exact ORIGINAL dependent primitive unit payload faithfulness.

The complete v5.92 ORIGINAL Sigma typed unit-payload history
retains each genuine unitLeft/unitRight proof *as a value*,
with its full actual before/F/G/C/after parameters and original
raw17D start/end indices.

On the precisely delimited primitive source fragment (the original
v5.73 inner bracket is literally oldUnitLeft or oldUnitRight, with
no raw reverse, strict, or chain wrapper), one unit atom is present,
and equality of original typed payload histories REFLECTS equality
of the actual original old18D proof values in one fixed J->N fiber.

The result remains true for *the source arguments* after arbitrary
genuine strict prefix/suffix insertions, because their payload
histories stay unchanged. It does NOT mean padded raw proofs with
different strict placements are equal. On the additionally restricted
mixed-padding collision presentation with equal original brackets,
v5.96 rules out all histories-equal/raw-distinct collisions.

This is local primitive-leaf faithfulness, not an assertion that
ALL one-unit original sources (which can contain nested original
reverse and chain constructors) have faithful typed payload history.
The unresolved v5.93 equal-bracket/different-raw one-unit source
existence remains NO_DATA; a restricted impossibility must not be
globally descended.

No original source Type, old-five/new-seven selected19 comparison,
Lean/mathlib pins, public root107, or protected PR #1558 is changed.
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

/-- This is a restriction OF THE EXISTING original old18D Type:
only a literal single original unit constructor at the root of
its unchanged genuine v5.73 nonassociative source bracket. -/
def selectedV597OriginalPrimitiveUnit (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) : Prop :=
  selectedLocalEighteenInnerBracket l r M =
      SelectedInheritedOldInnerBracket.oldUnitLeft ∨
    selectedLocalEighteenInnerBracket l r M =
      SelectedInheritedOldInnerBracket.oldUnitRight

section SameOriginalSourceFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)
variable (M L : SelectedLocalEighteen W l r J N)

/-- Injectively embed a value of the actual original dependent
J->N Type into the original v5.92 Sigma atom, using the true
J and N rather than surrogate untyped endpoint names. -/
theorem selectedV597FixedOriginalAtom_injective :
    Function.Injective (fun A : SelectedLocalEighteen W l r J N =>
      (⟨J, ⟨N, A⟩⟩ : SelectedV592OriginalUnitAtom l r H K)) := by
  intro A B h
  have hInner :
      (⟨N, A⟩ : Σ S : SelectedContextualSeventeen W l r H K,
        SelectedLocalEighteen W l r J S) =
        ⟨N, B⟩ :=
    sigma_mk_injective J h
  exact sigma_mk_injective N hInner

/-- A literal original unitLeft or unitRight leaf has exactly
one true original dependent unit occurrence, never just an
untyped left/right label. -/
theorem selectedV597Primitive_unitCountOne
    (hprimitive : selectedV597OriginalPrimitiveUnit l r M) :
    selectedV589OriginalUnitCount l r M = 1 := by
  rw [selectedV589OriginalUnitCount_observed l r M]
  rcases hprimitive with hleft | hright
  · rw [hleft]
    rfl
  · rw [hright]
    rfl

/-- Crucial LOCAL reconstruction identity on the FULL ORIGINAL
dependent old18D Type. At a primitive unit leaf, the entire
v5.92 Sigma history is a singleton containing that SAME
original source proof, not a reconstructed surrogate. -/
theorem selectedV597Primitive_historySingleton
    (hprimitive : selectedV597OriginalPrimitiveUnit l r M) :
    selectedV592OriginalUnitHistory l r M =
      [⟨J, ⟨N, M⟩⟩] := by
  cases M with
  | strict _ =>
      simp [selectedV597OriginalPrimitiveUnit,
        selectedLocalEighteenInnerBracket] at hprimitive
  | unitLeft _ _ _ _ _ => rfl
  | unitRight _ _ _ _ _ => rfl
  | reverse A =>
      simp [selectedV597OriginalPrimitiveUnit,
        selectedLocalEighteenInnerBracket] at hprimitive
  | chain A B =>
      simp [selectedV597OriginalPrimitiveUnit,
        selectedLocalEighteenInnerBracket] at hprimitive

/-- The FULL typed original unit payload history alone is
faithful on this restricted primitive source fragment, in
one ACTUAL fixed J->N fiber. Equality of histories reflects
the original dependent raw proof value equality. -/
theorem selectedV597Primitive_historyEq_iff_rawEq
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L) :
    (selectedV592OriginalUnitHistory l r M =
      selectedV592OriginalUnitHistory l r L) ↔ M = L := by
  constructor
  · intro hh
    rw [selectedV597Primitive_historySingleton l r J N M hM,
      selectedV597Primitive_historySingleton l r J N L hL] at hh
    have hAtom := congrArg List.head? hh
    change
      (some (⟨J, ⟨N, M⟩⟩ :
        SelectedV592OriginalUnitAtom l r H K)) =
      some (⟨J, ⟨N, L⟩⟩ :
        SelectedV592OriginalUnitAtom l r H K) at hAtom
    exact selectedV597FixedOriginalAtom_injective l r J N
      (Option.some.inj hAtom)
  · intro heq
    cases heq
    rfl

/-- Equal primitive full typed histories cannot hide
different source raw values. This is a contrapositive,
not an unlicensed global original source-faithfulness claim. -/
theorem selectedV597Primitive_rawNe_implies_historyNe
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (hne : M ≠ L) :
    selectedV592OriginalUnitHistory l r M ≠
      selectedV592OriginalUnitHistory l r L := by
  intro hh
  exact hne
    ((selectedV597Primitive_historyEq_iff_rawEq
      l r J N M L hM hL).mp hh)

/-- The JOINT observation of the exact original bracket and
the full original typed history is faithful on primitive unit
leaves. The bracket assumption does not weaken the history
requirement; it remains an independent observation. -/
theorem selectedV597Primitive_jointEq_iff_rawEq
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L) :
    ((selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L) ∧
      selectedV592OriginalUnitHistory l r M =
        selectedV592OriginalUnitHistory l r L) ↔ M = L := by
  constructor
  · rintro ⟨_, hh⟩
    exact (selectedV597Primitive_historyEq_iff_rawEq
      l r J N M L hM hL).mp hh
  · intro h
    cases h
    exact ⟨rfl, rfl⟩

/-- Genuine original strict prefixing with independent lengths
cannot change whether two primitive source payload histories agree.
Even with different padding lengths, this equals ORIGINAL raw
source equality (not equality of the padded raw values). -/
theorem selectedV597Primitive_prefixHistoryEq_iff_sourceEq
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (m n : Nat) :
    (selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J L n)) ↔ M = L :=
  (selectedV595Prefix_historyEq_iff l r J N M L m n).trans
    (selectedV597Primitive_historyEq_iff_rawEq l r J N M L hM hL)

theorem selectedV597Primitive_suffixHistoryEq_iff_sourceEq
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (m n : Nat) :
    (selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N L n)) ↔ M = L :=
  (selectedV595Suffix_historyEq_iff l r J N M L m n).trans
    (selectedV597Primitive_historyEq_iff_rawEq l r J N M L hM hL)

/-- Mixed orientation also preserves the full ORIGINAL typed
unit payloads. The historical equality remembers exactly the
original primitive raw source, but not the strict placement. -/
theorem selectedV597Primitive_mixedHistoryEq_iff_sourceEq
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (m n : Nat) :
    (selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N L n)) ↔ M = L :=
  (selectedV595Mixed_historyEq_iff l r J N M L m n).trans
    (selectedV597Primitive_historyEq_iff_rawEq l r J N M L hM hL)

/-- Given primitive original unit sources, same-size strict
prefix and equal full history force the PADDED raw values equal.
No global old18D quotient equality is needed. -/
theorem selectedV597Primitive_commonPrefix_faithful
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (n : Nat)
    (hh : selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M n) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J L n)) :
    selectedV594StrictPrefix l r J M n =
      selectedV594StrictPrefix l r J L n := by
  have hsource :=
    (selectedV597Primitive_prefixHistoryEq_iff_sourceEq
      l r J N M L hM hL n n).mp hh
  cases hsource
  rfl

theorem selectedV597Primitive_commonSuffix_faithful
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (n : Nat)
    (hh : selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M n) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N L n)) :
    selectedV594StrictSuffix l r N M n =
      selectedV594StrictSuffix l r N L n := by
  have hsource :=
    (selectedV597Primitive_suffixHistoryEq_iff_sourceEq
      l r J N M L hM hL n n).mp hh
  cases hsource
  rfl

/-- For mixed padding, even when histories reconstruct the SAME
original primitive source, nontrivial distinct raw placements
remain. If the actual ORIGINAL nonassociative brackets are equal,
an equal padded bracket AND equal typed history cannot coexist
with padded raw inequality, at any m or n. -/
theorem selectedV597Primitive_mixedJointCollision_impossible
    (hM : selectedV597OriginalPrimitiveUnit l r M)
    (hL : selectedV597OriginalPrimitiveUnit l r L)
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (m n : Nat)
    (hh : selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N L n))
    (hpbr : selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n)) :
    selectedV594StrictPrefix l r J M m =
      selectedV594StrictSuffix l r N L n := by
  have hsource :=
    (selectedV597Primitive_mixedHistoryEq_iff_sourceEq
      l r J N M L hM hL m n).mp hh
  have hunit : 0 < selectedV589OriginalUnitCount l r M := by
    rw [selectedV597Primitive_unitCountOne l r J N M hM]
    decide
  have hz := (selectedV596MixedCrossIndex_bracketEq_iff
    l r J N M L hbr hunit m n).mp hpbr
  exact (selectedV596MixedCrossIndex_rawEq_iff
    l r J N M L hbr hunit m n).mpr ⟨hz.1, hz.2, hsource⟩

end SameOriginalSourceFiber

section RestrictedPrimitiveCollisionProp

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Explicitly restricted existence proposition: both genuine
old18D sources are ORIGINAL primitive unit leaves, and their
full v5.92 dependent Sigma payload histories agree, but raw
original proof values differ. The proposition is NOT the
unrestricted v5.93 same-bracket one-unit source collision. -/
def selectedV597PrimitiveUnitSameHistoryCollisionExists
    (J N : SelectedContextualSeventeen W l r H K) : Prop :=
  ∃ M L : SelectedLocalEighteen W l r J N,
    selectedV597OriginalPrimitiveUnit l r M ∧
    selectedV597OriginalPrimitiveUnit l r L ∧
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L ∧
    selectedV592OriginalUnitHistory l r M =
      selectedV592OriginalUnitHistory l r L ∧
    M ≠ L

/-- PROVED IMPOSSIBLE only in the precisely restricted
primitive-unit + typed-history-equal source presentation. -/
theorem selectedV597PrimitiveUnitSameHistoryCollision_impossible
    (J N : SelectedContextualSeventeen W l r H K) :
    ¬ selectedV597PrimitiveUnitSameHistoryCollisionExists l r J N := by
  rintro ⟨M, L, hM, hL, _, hh, hne⟩
  exact hne
    ((selectedV597Primitive_historyEq_iff_rawEq
      l r J N M L hM hL).mp hh)

end RestrictedPrimitiveCollisionProp

#print axioms PentagonAdjoinedSixCell.selectedV597OriginalPrimitiveUnit
#print axioms PentagonAdjoinedSixCell.selectedV597FixedOriginalAtom_injective
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_unitCountOne
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_historySingleton
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_historyEq_iff_rawEq
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_rawNe_implies_historyNe
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_jointEq_iff_rawEq
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_prefixHistoryEq_iff_sourceEq
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_suffixHistoryEq_iff_sourceEq
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_mixedHistoryEq_iff_sourceEq
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_commonPrefix_faithful
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_commonSuffix_faithful
#print axioms PentagonAdjoinedSixCell.selectedV597Primitive_mixedJointCollision_impossible
#print axioms PentagonAdjoinedSixCell.selectedV597PrimitiveUnitSameHistoryCollisionExists
#print axioms PentagonAdjoinedSixCell.selectedV597PrimitiveUnitSameHistoryCollision_impossible

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
