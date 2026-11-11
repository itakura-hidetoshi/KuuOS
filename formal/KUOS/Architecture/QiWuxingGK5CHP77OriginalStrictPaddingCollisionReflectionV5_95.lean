import KUOS.Architecture.QiWuxingGK5CHP77OriginalStrictPaddingHistoryV5_94

/-!
Qi v5.95 — original dependent old18D strict-padding collision reflection.

This new module studies the EXISTING original dependent old18D Type
SelectedLocalEighteen W l r J N.  Under fixed genuine raw17D
endpoints J,N, simultaneous n-fold strict prefix or suffix padding
reflects *both* actual raw equality and the existing v5.73 free,
nonassociative source-inner-bracket equality.

Hence the precise same-fingerprint/different-raw source collision
predicate of v5.93 is invariant under a FIXED common padding index,
including its one-unit restricted existential criterion.  For different
padding indices, equality of actual brackets forces the quantitative
strict-leaf balance, and equal source strict-leaf counts force equal
indices and equality of the original source brackets.

All results use the ORIGINAL strict/chain constructors, the original
v5.73 bracket observation, the original v5.89 unit count, the FULL
original v5.92 typed payload history, and the certified v5.94
padding maps. No equality between different raw17D fibers or
old5/new7 selected19 quotients is invented.

Crucially: source collision existence itself is still NO_DATA.
No unconditional collision is asserted or manufactured by strict
padding.  No source Types, old comparisons, root107 or toolchain pins
are modified. append-only / tighten-only / overwrite-forbidden /
same-root.
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

section FixedSourceFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)
variable (M L : SelectedLocalEighteen W l r J N)

/-- Original n-fold left strict padding REFLECTS true original
old18D source equality, with both raw17D indices unchanged.
No raw unit/associativity equation is used. -/
theorem selectedV595Prefix_rawEq_iff (n : Nat) :
    selectedV594StrictPrefix l r J M n =
      selectedV594StrictPrefix l r J L n ↔ M = L := by
  induction n with
  | zero => rfl
  | succ n ih =>
      constructor
      · intro h
        have hc :
            selectedV594StrictPrefix l r J M n =
              selectedV594StrictPrefix l r J L n := by
          change
            (SelectedLocalEighteen.chain
              (SelectedLocalEighteen.strict J)
              (selectedV594StrictPrefix l r J M n) :
                SelectedLocalEighteen W l r J N) =
            SelectedLocalEighteen.chain
              (SelectedLocalEighteen.strict J)
              (selectedV594StrictPrefix l r J L n) at h
          injection h with hfirst hsecond
        exact ih.mp hc
      · intro h
        cases h
        rfl

/-- Original n-fold right strict padding also REFLECTS raw source
equality; left/right padding remain separate indexed operations. -/
theorem selectedV595Suffix_rawEq_iff (n : Nat) :
    selectedV594StrictSuffix l r N M n =
      selectedV594StrictSuffix l r N L n ↔ M = L := by
  induction n with
  | zero => rfl
  | succ n ih =>
      constructor
      · intro h
        have hc :
            selectedV594StrictSuffix l r N M n =
              selectedV594StrictSuffix l r N L n := by
          change
            (SelectedLocalEighteen.chain
              (selectedV594StrictSuffix l r N M n)
              (SelectedLocalEighteen.strict N) :
                SelectedLocalEighteen W l r J N) =
            SelectedLocalEighteen.chain
              (selectedV594StrictSuffix l r N L n)
              (SelectedLocalEighteen.strict N) at h
          injection h with hfirst hsecond
        exact ih.mp hc
      · intro h
        cases h
        rfl

/-- Prefixing the SAME n retains and REFLECTS equality of the
genuine v5.73 inner-bracket syntax; it does not make the bracket
observer faithful on the full original Type. -/
theorem selectedV595Prefix_bracketEq_iff (n : Nat) :
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M n) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J L n) ↔
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L := by
  induction n with
  | zero => rfl
  | succ n ih =>
      constructor
      · intro h
        have hc :
            selectedLocalEighteenInnerBracket l r
                (selectedV594StrictPrefix l r J M n) =
              selectedLocalEighteenInnerBracket l r
                (selectedV594StrictPrefix l r J L n) := by
          change
            SelectedInheritedOldInnerBracket.oldJoined .oldStrict
              (selectedLocalEighteenInnerBracket l r
                (selectedV594StrictPrefix l r J M n)) =
            .oldJoined .oldStrict
              (selectedLocalEighteenInnerBracket l r
                (selectedV594StrictPrefix l r J L n)) at h
          injection h with hfirst hsecond
        exact ih.mp hc
      · intro h
        have hc := ih.mpr h
        change
          SelectedInheritedOldInnerBracket.oldJoined .oldStrict
            (selectedLocalEighteenInnerBracket l r
              (selectedV594StrictPrefix l r J M n)) =
          .oldJoined .oldStrict
            (selectedLocalEighteenInnerBracket l r
              (selectedV594StrictPrefix l r J L n))
        rw [hc]

/-- Suffixing the SAME n likewise reflects equality of the
actual original inner-bracket observation. -/
theorem selectedV595Suffix_bracketEq_iff (n : Nat) :
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M n) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n) ↔
    selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L := by
  induction n with
  | zero => rfl
  | succ n ih =>
      constructor
      · intro h
        have hc :
            selectedLocalEighteenInnerBracket l r
                (selectedV594StrictSuffix l r N M n) =
              selectedLocalEighteenInnerBracket l r
                (selectedV594StrictSuffix l r N L n) := by
          change
            SelectedInheritedOldInnerBracket.oldJoined
              (selectedLocalEighteenInnerBracket l r
                (selectedV594StrictSuffix l r N M n)) .oldStrict =
            .oldJoined
              (selectedLocalEighteenInnerBracket l r
                (selectedV594StrictSuffix l r N L n)) .oldStrict at h
          injection h with hfirst hsecond
        exact ih.mp hc
      · intro h
        have hc := ih.mpr h
        change
          SelectedInheritedOldInnerBracket.oldJoined
            (selectedLocalEighteenInnerBracket l r
              (selectedV594StrictSuffix l r N M n)) .oldStrict =
          .oldJoined
            (selectedLocalEighteenInnerBracket l r
              (selectedV594StrictSuffix l r N L n)) .oldStrict
        rw [hc]

/-- All original typed unit-payload-history equivalences are
unchanged by independently chosen prefix lengths. -/
theorem selectedV595Prefix_historyEq_iff (m n : Nat) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J L n) ↔
    selectedV592OriginalUnitHistory l r M =
      selectedV592OriginalUnitHistory l r L := by
  rw [selectedV594Prefix_unitHistory l r J N M m,
    selectedV594Prefix_unitHistory l r J N L n]

/-- The independent suffix lengths cannot change exact unit
history equality between the original sources. -/
theorem selectedV595Suffix_historyEq_iff (m n : Nat) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N L n) ↔
    selectedV592OriginalUnitHistory l r M =
      selectedV592OriginalUnitHistory l r L := by
  rw [selectedV594Suffix_unitHistory l r J N M m,
    selectedV594Suffix_unitHistory l r J N L n]

/-- Cross-orientation typed histories admit the same exact
reflection, even at independent padding lengths. -/
theorem selectedV595Mixed_historyEq_iff (m n : Nat) :
    selectedV592OriginalUnitHistory l r
        (selectedV594StrictPrefix l r J M m) =
      selectedV592OriginalUnitHistory l r
        (selectedV594StrictSuffix l r N L n) ↔
    selectedV592OriginalUnitHistory l r M =
      selectedV592OriginalUnitHistory l r L := by
  rw [selectedV594Prefix_unitHistory l r J N M m,
    selectedV594Suffix_unitHistory l r J N L n]

/-- Precise EXISTING source same-bracket/different-raw collision
is equivalent to the corresponding common-prefix collision.
This is an iff, not a proof that either side is inhabited. -/
theorem selectedV595Prefix_collision_iff (n : Nat) :
    (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M n) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J L n) ∧
      selectedV594StrictPrefix l r J M n ≠
        selectedV594StrictPrefix l r J L n) ↔
    (selectedLocalEighteenInnerBracket l r M =
       selectedLocalEighteenInnerBracket l r L ∧ M ≠ L) := by
  constructor
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV595Prefix_bracketEq_iff l r J N M L n).mp hbr, ?_⟩
    intro h
    exact hne ((selectedV595Prefix_rawEq_iff l r J N M L n).mpr h)
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV595Prefix_bracketEq_iff l r J N M L n).mpr hbr, ?_⟩
    intro h
    exact hne ((selectedV595Prefix_rawEq_iff l r J N M L n).mp h)

/-- Exact collision reflection for the independent common-suffix
operation in the SAME actual original raw17D endpoint fiber. -/
theorem selectedV595Suffix_collision_iff (n : Nat) :
    (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M n) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n) ∧
      selectedV594StrictSuffix l r N M n ≠
        selectedV594StrictSuffix l r N L n) ↔
    (selectedLocalEighteenInnerBracket l r M =
       selectedLocalEighteenInnerBracket l r L ∧ M ≠ L) := by
  constructor
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV595Suffix_bracketEq_iff l r J N M L n).mp hbr, ?_⟩
    intro h
    exact hne ((selectedV595Suffix_rawEq_iff l r J N M L n).mpr h)
  · rintro ⟨hbr, hne⟩
    refine ⟨(selectedV595Suffix_bracketEq_iff l r J N M L n).mpr hbr, ?_⟩
    intro h
    exact hne ((selectedV595Suffix_rawEq_iff l r J N M L n).mp h)

/-- At DIFFERENT prefix lengths, equal original brackets force
the independent strict-leaf-count balance. No source bracket
equality is inferred from this numeric necessary condition. -/
theorem selectedV595Prefix_crossIndex_strictBalance
    (m n : Nat)
    (hbr :
      selectedLocalEighteenInnerBracket l r
          (selectedV594StrictPrefix l r J M m) =
        selectedLocalEighteenInnerBracket l r
          (selectedV594StrictPrefix l r J L n)) :
    m + selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r M) =
    n + selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r L) := by
  have hc := congrArg selectedV594InnerStrictCount hbr
  rw [selectedV594Prefix_innerStrictCount l r J N M m,
    selectedV594Prefix_innerStrictCount l r J N L n] at hc
  exact hc

theorem selectedV595Suffix_crossIndex_strictBalance
    (m n : Nat)
    (hbr :
      selectedLocalEighteenInnerBracket l r
          (selectedV594StrictSuffix l r N M m) =
        selectedLocalEighteenInnerBracket l r
          (selectedV594StrictSuffix l r N L n)) :
    m + selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r M) =
    n + selectedV594InnerStrictCount
      (selectedLocalEighteenInnerBracket l r L) := by
  have hc := congrArg selectedV594InnerStrictCount hbr
  rw [selectedV594Suffix_innerStrictCount l r J N M m,
    selectedV594Suffix_innerStrictCount l r J N L n] at hc
  exact hc

/-- If the ORIGINAL source strict-leaf counts agree, different
padding lengths can NEVER have identical genuine prefix brackets.
This condition is essential; do not generalize it unconditionally. -/
theorem selectedV595Prefix_crossIndex_bracketRigidity
    (m n : Nat)
    (hcount :
      selectedV594InnerStrictCount
          (selectedLocalEighteenInnerBracket l r M) =
        selectedV594InnerStrictCount
          (selectedLocalEighteenInnerBracket l r L)) :
    (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M m) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J L n)) ↔
    (m = n ∧
      selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L) := by
  constructor
  · intro hb
    have hbalance :=
      selectedV595Prefix_crossIndex_strictBalance l r J N M L m n hb
    have heq : m = n := by omega
    subst n
    exact ⟨rfl, (selectedV595Prefix_bracketEq_iff l r J N M L m).mp hb⟩
  · rintro ⟨heq, hbr⟩
    subst n
    exact (selectedV595Prefix_bracketEq_iff l r J N M L m).mpr hbr

theorem selectedV595Suffix_crossIndex_bracketRigidity
    (m n : Nat)
    (hcount :
      selectedV594InnerStrictCount
          (selectedLocalEighteenInnerBracket l r M) =
        selectedV594InnerStrictCount
          (selectedLocalEighteenInnerBracket l r L)) :
    (selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M m) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n)) ↔
    (m = n ∧
      selectedLocalEighteenInnerBracket l r M =
        selectedLocalEighteenInnerBracket l r L) := by
  constructor
  · intro hb
    have hbalance :=
      selectedV595Suffix_crossIndex_strictBalance l r J N M L m n hb
    have heq : m = n := by omega
    subst n
    exact ⟨rfl, (selectedV595Suffix_bracketEq_iff l r J N M L m).mp hb⟩
  · rintro ⟨heq, hbr⟩
    subst n
    exact (selectedV595Suffix_bracketEq_iff l r J N M L m).mpr hbr

end FixedSourceFiber

section ConditionalOneUnitExistence

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- An explicitly RESTRICTED padded image collision predicate,
quantifying over ORIGINAL source pairs, not all old18D values.
No existence is asserted by this definition. -/
def selectedV595PrefixOneUnitCollisionExists
    (J N : SelectedContextualSeventeen W l r H K) (n : Nat) : Prop :=
  ∃ M L : SelectedLocalEighteen W l r J N,
    selectedV589OriginalUnitCount l r M = 1 ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J M n) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictPrefix l r J L n) ∧
    selectedV594StrictPrefix l r J M n ≠
      selectedV594StrictPrefix l r J L n

def selectedV595SuffixOneUnitCollisionExists
    (J N : SelectedContextualSeventeen W l r H K) (n : Nat) : Prop :=
  ∃ M L : SelectedLocalEighteen W l r J N,
    selectedV589OriginalUnitCount l r M = 1 ∧
    selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N M n) =
      selectedLocalEighteenInnerBracket l r
        (selectedV594StrictSuffix l r N L n) ∧
    selectedV594StrictSuffix l r N M n ≠
      selectedV594StrictSuffix l r N L n

/-- Exact existence equivalence with the UNRESOLVED genuine
v5.93 one-unit source collision.  This proves that padding cannot
create the missing inhabitant. -/
theorem selectedV595PrefixOneUnitCollisionExists_iff
    (J N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedV595PrefixOneUnitCollisionExists l r J N n ↔
      selectedV593OneUnitSourceCollisionExists l r J N := by
  constructor
  · rintro ⟨M, L, hone, hb, hne⟩
    have hc :=
      (selectedV595Prefix_collision_iff l r J N M L n).mp ⟨hb, hne⟩
    exact ⟨M, L, hone, hc.1, hc.2⟩
  · rintro ⟨M, L, hone, hb, hne⟩
    have hc :=
      (selectedV595Prefix_collision_iff l r J N M L n).mpr ⟨hb, hne⟩
    exact ⟨M, L, hone, hc.1, hc.2⟩

theorem selectedV595SuffixOneUnitCollisionExists_iff
    (J N : SelectedContextualSeventeen W l r H K) (n : Nat) :
    selectedV595SuffixOneUnitCollisionExists l r J N n ↔
      selectedV593OneUnitSourceCollisionExists l r J N := by
  constructor
  · rintro ⟨M, L, hone, hb, hne⟩
    have hc :=
      (selectedV595Suffix_collision_iff l r J N M L n).mp ⟨hb, hne⟩
    exact ⟨M, L, hone, hc.1, hc.2⟩
  · rintro ⟨M, L, hone, hb, hne⟩
    have hc :=
      (selectedV595Suffix_collision_iff l r J N M L n).mpr ⟨hb, hne⟩
    exact ⟨M, L, hone, hc.1, hc.2⟩

end ConditionalOneUnitExistence

#print axioms PentagonAdjoinedSixCell.selectedV595Prefix_rawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Suffix_rawEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Prefix_bracketEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Suffix_bracketEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Prefix_historyEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Suffix_historyEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Mixed_historyEq_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Prefix_collision_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Suffix_collision_iff
#print axioms PentagonAdjoinedSixCell.selectedV595Prefix_crossIndex_strictBalance
#print axioms PentagonAdjoinedSixCell.selectedV595Suffix_crossIndex_strictBalance
#print axioms PentagonAdjoinedSixCell.selectedV595Prefix_crossIndex_bracketRigidity
#print axioms PentagonAdjoinedSixCell.selectedV595Suffix_crossIndex_bracketRigidity
#print axioms PentagonAdjoinedSixCell.selectedV595PrefixOneUnitCollisionExists
#print axioms PentagonAdjoinedSixCell.selectedV595SuffixOneUnitCollisionExists
#print axioms PentagonAdjoinedSixCell.selectedV595PrefixOneUnitCollisionExists_iff
#print axioms PentagonAdjoinedSixCell.selectedV595SuffixOneUnitCollisionExists_iff

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
