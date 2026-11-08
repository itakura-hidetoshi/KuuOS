import KUOS.Architecture.QiWuxingGK5CHP77ExactNineteenUnitNormalFormV5_48

/-!
Qi v5.49 — original selected 19D unit classes and exact typed
congruence/descent gates for raw18D syntax operators.

The ORIGINAL selected19 comparison has only strict, the two old18
direct unit pastings, reverse-of-comparison and chain-of-comparisons.
These are NOT raw reverse/chain contextual congruence constructors.

Prove three original raw unit presentations have genuine Type-valued
comparisons, while simple raw reverse / strict left/right raw chain
contexts do NOT respect those comparisons. For arbitrary fixed-fiber
raw maps, characterize precisely when a quotient action can descend.
No original constructor, evidence, endpoint, public import/root or pin
is overwritten. No assumption is weakened or global descent claimed.
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

/-- Three raw presentations associated to one ORIGINAL old18 witness.
This enumeration is not a new selected19 comparison generator. -/
inductive SelectedNineteenDirectUnitVariant where
  | inherited
  | prepend
  | append
  deriving DecidableEq

section DirectUnit

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- The exact dependent endpoints of all three old-inherited
raw18D presentations agree. -/
def selectedNineteenDirectUnitRaw
    (M : SelectedLocalEighteen W l r J N)
    (v : SelectedNineteenDirectUnitVariant) :
    SelectedContextualEighteen W l r J N :=
  match v with
  | .inherited => .inherited M
  | .prepend => .chain (.strict J) (.inherited M)
  | .append => .chain (.inherited M) (.strict N)

/-- Every direct variant compares to the ORIGINAL inherited value
by an actual Type-valued local19 proof. -/
def selectedNineteenDirectUnitToInherited
    (M : SelectedLocalEighteen W l r J N)
    (v : SelectedNineteenDirectUnitVariant) :
    SelectedLocalNineteen W l r
      (selectedNineteenDirectUnitRaw l r M v)
      (SelectedContextualEighteen.inherited M) :=
  match v with
  | .inherited => .strict _
  | .prepend => .unitPrepend M
  | .append => .unitAppend M

/-- Actual proof paths between ALL three direct unit variants,
not a replacement by mere numerical observation equality. -/
def selectedNineteenDirectUnitComparison
    (M : SelectedLocalEighteen W l r J N)
    (s t : SelectedNineteenDirectUnitVariant) :
    SelectedLocalNineteen W l r
      (selectedNineteenDirectUnitRaw l r M s)
      (selectedNineteenDirectUnitRaw l r M t) :=
  .chain
    (selectedNineteenDirectUnitToInherited l r M s)
    (.reverse (selectedNineteenDirectUnitToInherited l r M t))

theorem selectedNineteenDirectUnit_normal
    (M : SelectedLocalEighteen W l r J N)
    (s : SelectedNineteenDirectUnitVariant) :
    selectedNineteenNormal l r
      (selectedNineteenDirectUnitRaw l r M s) =
      SelectedContextualEighteen.inherited M := by
  cases s <;> rfl

theorem selectedNineteenDirectUnit_classEqual
    (M : SelectedLocalEighteen W l r J N)
    (s t : SelectedNineteenDirectUnitVariant) :
    selectedNineteenClass l r
      (selectedNineteenDirectUnitRaw l r M s) =
    selectedNineteenClass l r
      (selectedNineteenDirectUnitRaw l r M t) :=
  Quotient.sound ⟨selectedNineteenDirectUnitComparison l r M s t⟩

/-- Finite constructor-shape observation of the three DIRECT
presentations. This is only a raw syntax witness, not a 19D invariant:
all three values are genuinely selected19-comparable. -/
def selectedNineteenDirectUnitShapeTag
    (Y : SelectedContextualEighteen W l r J N) : Nat :=
  match Y with
  | .inherited _ => 0
  | .chain (.strict _) (.inherited _) => 1
  | .chain (.inherited _) (.strict _) => 2
  | _ => 3

/-- Despite having the SAME actual selected19 class, the three
raw presentations retain their distinct constructor histories.
Observe constructor shape rather than asking simp to eliminate
heterogeneous equalities of dependent raw subterms. -/
theorem selectedNineteenDirectUnit_rawInjective
    (M : SelectedLocalEighteen W l r J N) :
    Function.Injective (selectedNineteenDirectUnitRaw l r M) := by
  intro s t h
  have ht := congrArg (selectedNineteenDirectUnitShapeTag l r) h
  cases s <;> cases t <;>
    simp [selectedNineteenDirectUnitRaw,
      selectedNineteenDirectUnitShapeTag] at ht ⊢

/-- The quotient map restricted to this ORIGINAL three-element
raw unit family is constant even though raw syntax is injective. -/
theorem selectedNineteenDirectUnit_classNotInjective
    (M : SelectedLocalEighteen W l r J N) :
    ¬ Function.Injective
      (fun s : SelectedNineteenDirectUnitVariant =>
        selectedNineteenClass l r (selectedNineteenDirectUnitRaw l r M s)) := by
  intro hinj
  have h := hinj (selectedNineteenDirectUnit_classEqual l r M
    .inherited .prepend)
  cases h

/-- Original raw reverse, unlike reverse of a comparison certificate,
does NOT preserve this direct selected19 unit comparison. -/
theorem selectedNineteenRawReverse_unitObstruction
    (M : SelectedLocalEighteen W l r J N) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (SelectedContextualEighteen.reverse
        (selectedNineteenDirectUnitRaw l r M .prepend))
      (SelectedContextualEighteen.reverse
        (selectedNineteenDirectUnitRaw l r M .inherited))) := by
  rintro ⟨A⟩
  have h := selectedNineteenNormal_respects l r A
  change
    (SelectedContextualEighteen.reverse
      (SelectedContextualEighteen.chain
        (SelectedContextualEighteen.strict J)
        (SelectedContextualEighteen.inherited M))) =
      (SelectedContextualEighteen.reverse
        (SelectedContextualEighteen.inherited M)) at h
  cases h

/-- A strict identity RIGHT raw context does not carry the original
unit-prepend comparison: the nested chain stays a different normal
form from the direct unit-append variant. -/
def selectedNineteenRawRightStrict
    (Y : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain Y (.strict N)

theorem selectedNineteenRawRightStrict_unitObstruction
    (M : SelectedLocalEighteen W l r J N) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (selectedNineteenRawRightStrict l r
        (selectedNineteenDirectUnitRaw l r M .prepend))
      (selectedNineteenRawRightStrict l r
        (selectedNineteenDirectUnitRaw l r M .inherited))) := by
  rintro ⟨A⟩
  have h := selectedNineteenNormal_respects l r A
  change
    (SelectedContextualEighteen.chain
      (SelectedContextualEighteen.chain
        (SelectedContextualEighteen.strict J)
        (SelectedContextualEighteen.inherited M))
      (SelectedContextualEighteen.strict N)) =
      (SelectedContextualEighteen.inherited M) at h
  cases h

/-- The same original unit-prepend comparison is NOT congruent under
adding another strict identity on the raw LEFT. -/
def selectedNineteenRawLeftStrict
    (Y : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .chain (.strict J) Y

theorem selectedNineteenRawLeftStrict_unitObstruction
    (M : SelectedLocalEighteen W l r J N) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (selectedNineteenRawLeftStrict l r
        (selectedNineteenDirectUnitRaw l r M .prepend))
      (selectedNineteenRawLeftStrict l r
        (selectedNineteenDirectUnitRaw l r M .inherited))) := by
  rintro ⟨A⟩
  have h := selectedNineteenNormal_respects l r A
  change
    (SelectedContextualEighteen.chain
      (SelectedContextualEighteen.strict J)
      (SelectedContextualEighteen.chain
        (SelectedContextualEighteen.strict J)
        (SelectedContextualEighteen.inherited M))) =
      (SelectedContextualEighteen.inherited M) at h
  cases h

end DirectUnit

section ExactCongruenceGate

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- An EXACT raw map between two possibly different dependent
endpoint fibers descends iff it preserves all original selected19
comparisons AS A PROPOSITION of Type-valued inhabitance. This
does not manufacture a new raw transport or an authority grant. -/
theorem selectedNineteenRawMap_descends_iff
    (J N S T : SelectedContextualSeventeen W l r H K)
    (f : SelectedContextualEighteen W l r J N →
      SelectedContextualEighteen W l r S T) :
    (∀ {M L : SelectedContextualEighteen W l r J N},
      SelectedLocalNineteen W l r M L →
        Nonempty (SelectedLocalNineteen W l r (f M) (f L))) ↔
    ∃ g : Quotient (selectedNineteenSetoid l r J N) →
          Quotient (selectedNineteenSetoid l r S T),
      ∀ M : SelectedContextualEighteen W l r J N,
        g (selectedNineteenClass l r M) =
          selectedNineteenClass l r (f M) := by
  constructor
  · intro compatible
    let g : Quotient (selectedNineteenSetoid l r J N) →
        Quotient (selectedNineteenSetoid l r S T) :=
      Quotient.lift
        (fun M => selectedNineteenClass l r (f M)) (by
          intro M L h
          rcases h with ⟨A⟩
          exact Quotient.sound (compatible A))
    exact ⟨g, fun M => rfl⟩
  · rintro ⟨g, hg⟩ M L A
    have hbase : selectedNineteenClass l r M =
        selectedNineteenClass l r L := Quotient.sound ⟨A⟩
    have hout : selectedNineteenClass l r (f M) =
        selectedNineteenClass l r (f L) := by
      calc
        selectedNineteenClass l r (f M) =
            g (selectedNineteenClass l r M) := (hg M).symm
        _ = g (selectedNineteenClass l r L) := congrArg g hbase
        _ = selectedNineteenClass l r (f L) := hg L
    exact Quotient.exact hout

/-- Equivalently, a raw map's quotient action is authorized exactly
when it preserves EQUALITY OF ORIGINAL TYPED NORMAL REPRESENTATIVES,
even when source and target endpoint fibers differ. -/
theorem selectedNineteenRawMap_normalGate
    (J N S T : SelectedContextualSeventeen W l r H K)
    (f : SelectedContextualEighteen W l r J N →
      SelectedContextualEighteen W l r S T) :
    (∀ M L : SelectedContextualEighteen W l r J N,
      selectedNineteenNormal l r M = selectedNineteenNormal l r L →
      selectedNineteenNormal l r (f M) =
        selectedNineteenNormal l r (f L)) ↔
    (∃ g : Quotient (selectedNineteenSetoid l r J N) →
          Quotient (selectedNineteenSetoid l r S T),
      ∀ M : SelectedContextualEighteen W l r J N,
        g (selectedNineteenClass l r M) =
          selectedNineteenClass l r (f M)) := by
  rw [← selectedNineteenRawMap_descends_iff l r J N S T f]
  constructor
  · intro hp M L A
    have heq : selectedNineteenNormal l r M =
        selectedNineteenNormal l r L :=
      selectedNineteenNormal_respects l r A
    exact (selectedNineteenNormal_eq_iff_local l r (f M) (f L)).mp
      (hp M L heq)
  · intro hp M L heq
    have A := (selectedNineteenNormal_eq_iff_local l r M L).mp heq
    rcases A with ⟨A⟩
    rcases hp A with ⟨B⟩
    exact selectedNineteenNormal_respects l r B

/-- The ACTUAL raw reverse does not induce a quotient-level
function respecting the original class map, even at a supplied
inhabited exact J→N fiber. -/
theorem selectedNineteenRawReverse_noDescent
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ (∃ g : Quotient (selectedNineteenSetoid l r J N) →
          Quotient (selectedNineteenSetoid l r N J),
      ∀ X : SelectedContextualEighteen W l r J N,
        g (selectedNineteenClass l r X) =
          selectedNineteenClass l r (SelectedContextualEighteen.reverse X)) := by
  intro h
  have compatible :
      ∀ {A B : SelectedContextualEighteen W l r J N},
        SelectedLocalNineteen W l r A B →
          Nonempty (SelectedLocalNineteen W l r
            (SelectedContextualEighteen.reverse A)
            (SelectedContextualEighteen.reverse B)) :=
    (selectedNineteenRawMap_descends_iff l r J N N J
      (fun X : SelectedContextualEighteen W l r J N => .reverse X)).mpr h
  exact (selectedNineteenRawReverse_unitObstruction l r M)
    (compatible (selectedNineteenDirectUnitComparison l r M .prepend .inherited))

/-- No quotient action of strict right raw chain can extend that
specific raw operation at the supplied original old18 witness. -/
theorem selectedNineteenRawRightStrict_noDescent
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ (∃ g : Quotient (selectedNineteenSetoid l r J N) →
          Quotient (selectedNineteenSetoid l r J N),
      ∀ X : SelectedContextualEighteen W l r J N,
        g (selectedNineteenClass l r X) =
          selectedNineteenClass l r
            (selectedNineteenRawRightStrict l r X)) := by
  intro h
  have compatible :
      ∀ {A B : SelectedContextualEighteen W l r J N},
        SelectedLocalNineteen W l r A B →
          Nonempty (SelectedLocalNineteen W l r
            (selectedNineteenRawRightStrict l r A)
            (selectedNineteenRawRightStrict l r B)) :=
    (selectedNineteenRawMap_descends_iff l r J N J N
      (selectedNineteenRawRightStrict l r)).mpr h
  exact (selectedNineteenRawRightStrict_unitObstruction l r M)
    (compatible (selectedNineteenDirectUnitComparison l r M .prepend .inherited))

theorem selectedNineteenRawLeftStrict_noDescent
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedLocalEighteen W l r J N) :
    ¬ (∃ g : Quotient (selectedNineteenSetoid l r J N) →
          Quotient (selectedNineteenSetoid l r J N),
      ∀ X : SelectedContextualEighteen W l r J N,
        g (selectedNineteenClass l r X) =
          selectedNineteenClass l r
            (selectedNineteenRawLeftStrict l r X)) := by
  intro h
  have compatible :
      ∀ {A B : SelectedContextualEighteen W l r J N},
        SelectedLocalNineteen W l r A B →
          Nonempty (SelectedLocalNineteen W l r
            (selectedNineteenRawLeftStrict l r A)
            (selectedNineteenRawLeftStrict l r B)) :=
    (selectedNineteenRawMap_descends_iff l r J N J N
      (selectedNineteenRawLeftStrict l r)).mpr h
  exact (selectedNineteenRawLeftStrict_unitObstruction l r M)
    (compatible (selectedNineteenDirectUnitComparison l r M .prepend .inherited))

end ExactCongruenceGate

#print axioms PentagonAdjoinedSixCell.SelectedNineteenDirectUnitVariant
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnitRaw
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnitToInherited
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnitComparison
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnit_normal
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnit_classEqual
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnitShapeTag
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnit_rawInjective
#print axioms PentagonAdjoinedSixCell.selectedNineteenDirectUnit_classNotInjective
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawReverse_unitObstruction
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawRightStrict
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawRightStrict_unitObstruction
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawLeftStrict
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawLeftStrict_unitObstruction
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawMap_descends_iff
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawMap_normalGate
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawReverse_noDescent
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawRightStrict_noDescent
#print axioms PentagonAdjoinedSixCell.selectedNineteenRawLeftStrict_noDescent

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
