import KUOS.Architecture.QiWuxingGK5CHP77IndexedSourceFingerprintCollisionV5_85

/-!
Qi v5.86 — conditional transport of ACTUAL old18D fingerprint collisions
into an actually supplied right-whiskered exact fiber, and exact
old-five/new-seven quotient-descent criteria for additional observations.

A given source collision in another original fixed 16D context can be
wrapped with *supplied* genuine old18D bridge proofs. The resulting
two old18D values are constructed in the right N'→N' fiber, preserve
the observed inner-bracket collision and remain distinct as raw values.
Neither a source collision nor a bridge nor a SevenRewrite is invented.

For arbitrary observations of the ORIGINAL dependent contextual18D Type,
we give separate iff-criteria for descent into each REAL old/new quotient;
a sufficient seven-generator check is derived from the ORIGINAL old-five
preservation plus raw reverse and both raw chain congruences. A genuinely
descended positive joint observer and a concrete non-descending raw-top
observer demonstrate the boundary. No quotient-class collision follows
from equal inner brackets. Neither true selected19 Type is changed.

Fixed Lean/mathlib, public root107, protected #1558 and historical
proofs untouched. No arbitrary WORLD/20D gluing, global classification
or action authority. append-only / tighten-only / overwrite-forbidden /
same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix uObs

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

section ObserverDescent

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {α : Type uObs}

/-- Preservation of ALL FIVE ORIGINAL selected19 proof constructors,
in every genuinely typed old18D exact fiber of this fixed context. -/
def selectedV586OldStable
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α) : Prop :=
  ∀ {J N : SelectedContextualSeventeen W l r H K}
    {A B : SelectedContextualEighteen W l r J N},
    SelectedLocalNineteen W l r A B → obs A = obs B

/-- Preservation of ALL SEVEN genuinely typed new19 generators. -/
def selectedV586NewStable
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α) : Prop :=
  ∀ {J N : SelectedContextualSeventeen W l r H K}
    {A B : SelectedContextualEighteen W l r J N},
    SelectedRawCongruentNineteen W l r J N A B → obs A = obs B

/-- The original five-generator proof grammar needs only its two
nontrivial unit checks; refl/symmetry/transitivity follow from Eq. -/
theorem selectedV586OldStableFromUnits
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α)
    (hPre : ∀ {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedLocalEighteen W l r J N),
      obs (.chain (.strict J) (.inherited M)) = obs (.inherited M))
    (hPost : ∀ {J N : SelectedContextualSeventeen W l r H K}
      (M : SelectedLocalEighteen W l r J N),
      obs (.chain (.inherited M) (.strict N)) = obs (.inherited M)) :
    selectedV586OldStable l r obs := by
  intro J N A B h
  induction h with
  | strict A => rfl
  | unitPrepend M => exact hPre M
  | unitAppend M => exact hPost M
  | reverse h ih => exact ih.symm
  | chain h k ih ih' => exact ih.trans ih'

/-- Sufficient *explicit* local checks for all seven new generators.
Old compatibility alone is not promoted to new compatibility. -/
theorem selectedV586NewStableFromCongruences
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α)
    (hOld : selectedV586OldStable l r obs)
    (hReverse : ∀ {J N : SelectedContextualSeventeen W l r H K}
      {A B : SelectedContextualEighteen W l r J N},
      obs A = obs B → obs (.reverse A) = obs (.reverse B))
    (hRight : ∀ {J N S : SelectedContextualSeventeen W l r H K}
      {A B : SelectedContextualEighteen W l r J N},
      obs A = obs B →
        (X : SelectedContextualEighteen W l r N S) →
          obs (.chain A X) = obs (.chain B X))
    (hLeft : ∀ {J N S : SelectedContextualSeventeen W l r H K}
      (X : SelectedContextualEighteen W l r J N)
      {A B : SelectedContextualEighteen W l r N S},
      obs A = obs B → obs (.chain X A) = obs (.chain X B)) :
    selectedV586NewStable l r obs := by
  intro J N A B h
  induction h with
  | inherited a => exact hOld a
  | strict A => rfl
  | reverse a ih => exact ih.symm
  | chain a b ih ih' => exact ih.trans ih'
  | rawReverse a ih => exact hReverse ih
  | rawChainRight a X ih => exact hRight ih X
  | rawChainLeft X a ih => exact hLeft X ih

/-- New-seven compatibility implies the original old-five
compatibility, because the old grammar is explicitly inherited. -/
theorem selectedV586NewStableImpliesOld
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α)
    (h : selectedV586NewStable l r obs) :
    selectedV586OldStable l r obs := by
  intro J N A B a
  exact h (.inherited a)

/-- Necessary AND sufficient criterion for descending a new
observation into the ORIGINAL five-generator quotient in this fiber. -/
theorem selectedV586OldDescent_iff
    (J N : SelectedContextualSeventeen W l r H K)
    (obs : SelectedContextualEighteen W l r J N → α) :
    (∀ {A B : SelectedContextualEighteen W l r J N},
      SelectedLocalNineteen W l r A B → obs A = obs B) ↔
    ∃ lift : Quotient (selectedNineteenSetoid l r J N) → α,
      ∀ A, lift (selectedNineteenClass l r A) = obs A := by
  constructor
  · intro h
    refine ⟨Quotient.lift obs ?_, ?_⟩
    · intro A B rel
      rcases rel with ⟨a⟩
      exact h a
    · intro A
      rfl
  · rintro ⟨lift, hlift⟩ A B a
    calc
      obs A = lift (selectedNineteenClass l r A) := (hlift A).symm
      _ = lift (selectedNineteenClass l r B) :=
        congrArg lift (Quotient.sound ⟨a⟩)
      _ = obs B := hlift B

/-- The INDEPENDENT seven-generator quotient has its own iff,
not a redefinition of the original selected19 quotient. -/
theorem selectedV586NewDescent_iff
    (J N : SelectedContextualSeventeen W l r H K)
    (obs : SelectedContextualEighteen W l r J N → α) :
    (∀ {A B : SelectedContextualEighteen W l r J N},
      SelectedRawCongruentNineteen W l r J N A B →
        obs A = obs B) ↔
    ∃ lift : Quotient (selectedRawCongruentSetoid l r J N) → α,
      ∀ A, lift (selectedRawCongruentClass l r A) = obs A := by
  constructor
  · intro h
    refine ⟨Quotient.lift obs ?_, ?_⟩
    · intro A B rel
      rcases rel with ⟨a⟩
      exact h a
    · intro A
      rfl
  · rintro ⟨lift, hlift⟩ A B a
    calc
      obs A = lift (selectedRawCongruentClass l r A) := (hlift A).symm
      _ = lift (selectedRawCongruentClass l r B) :=
        congrArg lift (Quotient.sound ⟨a⟩)
      _ = obs B := hlift B

/-- Original old-five descent on every genuine 17D fiber. -/
def selectedV586OldLift
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α)
    (h : selectedV586OldStable l r obs)
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → α :=
  Quotient.lift
    (fun (A : SelectedContextualEighteen W l r J N) => obs A)
    (by
      intro A B rel
      rcases rel with ⟨a⟩
      exact h a)

/-- New-seven descent, conditional on the full independent grammar. -/
def selectedV586NewLift
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α)
    (h : selectedV586NewStable l r obs)
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) → α :=
  Quotient.lift
    (fun (A : SelectedContextualEighteen W l r J N) => obs A)
    (by
      intro A B rel
      rcases rel with ⟨a⟩
      exact h a)

/-- Certified conditional triangle: descent through the genuinely
new quotient factors the OLD quotient, not vice versa. -/
theorem selectedV586LiftFactorsOldToNew
    (obs : ∀ {J N : SelectedContextualSeventeen W l r H K},
      SelectedContextualEighteen W l r J N → α)
    (h : selectedV586NewStable l r obs)
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedV586NewLift l r obs h J N
        (selectedRawCongruentProject l r J N q) =
      selectedV586OldLift l r obs
        (selectedV586NewStableImpliesOld l r obs h) J N q := by
  induction q using Quotient.inductionOn with
  | _ A => rfl

/-- An actual additional observer: keep BOTH the previously defined
whisker placement tree and the ordered old18D inherited brackets.
No claim that this product is a globally complete quotient classifier. -/
def selectedV586JointObserver
    {J N : SelectedContextualSeventeen W l r H K}
    (A : SelectedContextualEighteen W l r J N) :
    SelectedWhiskerPlacementTree × List SelectedInheritedOldInnerBracket :=
  (selectedContextEighteenWhiskerPlacement l r A,
    selectedContextEighteenInheritedInnerList l r A)

include F G P Q C D V X T U H K

/-- Positive demonstration: preservation by the REAL original five. -/
theorem selectedV586JointOldStable :
    selectedV586OldStable (H := H) (K := K) l r
      (selectedV586JointObserver (H := H) (K := K) l r) := by
  intro J N A B a
  exact Prod.ext
    (selectedLocalNineteen_preservesWhiskerPlacement l r a)
    (selectedLocalNineteen_preservesInheritedInnerList l r a)

/-- Positive demonstration: preservation by all SEVEN original
independently specified NEW comparison generators. -/
theorem selectedV586JointNewStable :
    selectedV586NewStable (H := H) (K := K) l r
      (selectedV586JointObserver (H := H) (K := K) l r) := by
  intro J N A B a
  exact Prod.ext
    (selectedRawCongruent_preservesWhiskerPlacement l r a)
    (selectedRawCongruent_preservesInheritedInnerList l r a)

/-- The concrete joint observer descends through the new quotient,
and its induced old quotient observer is its OLD-to-NEW factor. -/
theorem selectedV586JointFactors
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedV586NewLift l r (selectedV586JointObserver l r)
        (selectedV586JointNewStable (H := H) (K := K) l r) J N
        (selectedRawCongruentProject l r J N q) =
      selectedV586OldLift l r (selectedV586JointObserver l r)
        (selectedV586NewStableImpliesOld l r
          (selectedV586JointObserver l r)
          (selectedV586JointNewStable (H := H) (K := K) l r)) J N q :=
  selectedV586LiftFactorsOldToNew l r
    (selectedV586JointObserver l r) (selectedV586JointNewStable (H := H) (K := K) l r) J N q

/-- Necessary obstruction: any observation that distinguishes an
ACTUAL raw prepend-unit comparison cannot descend to EITHER quotient.
This checks descent, not mere preservation of a preferred sample. -/
theorem selectedV586NoDescentIfPrependSplit
    (J N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r J N)
    (obs : SelectedContextualEighteen W l r J N → α)
    (hsep : obs (.chain (.strict J) (.inherited M)) ≠ obs (.inherited M)) :
    (¬ ∃ f : Quotient (selectedNineteenSetoid l r J N) → α,
      ∀ X, f (selectedNineteenClass l r X) = obs X) ∧
    (¬ ∃ f : Quotient (selectedRawCongruentSetoid l r J N) → α,
      ∀ X, f (selectedRawCongruentClass l r X) = obs X) := by
  constructor
  · rintro ⟨f, hf⟩
    apply hsep
    calc
      obs (.chain (.strict J) (.inherited M)) =
          f (selectedNineteenClass l r
            (.chain (.strict J) (.inherited M))) := (hf _).symm
      _ = f (selectedNineteenClass l r (.inherited M)) :=
        congrArg f (Quotient.sound ⟨SelectedLocalNineteen.unitPrepend M⟩)
      _ = obs (.inherited M) := hf _
  · rintro ⟨f, hf⟩
    apply hsep
    calc
      obs (.chain (.strict J) (.inherited M)) =
          f (selectedRawCongruentClass l r
            (.chain (.strict J) (.inherited M))) := (hf _).symm
      _ = f (selectedRawCongruentClass l r (.inherited M)) :=
        congrArg f (Quotient.sound
          ⟨SelectedRawCongruentNineteen.inherited
            (SelectedLocalNineteen.unitPrepend M)⟩)
      _ = obs (.inherited M) := hf _

/-- Concrete raw-head annotation: unlike the joint observer, the
raw chain tag is erased by the original unitPrepend comparison. -/
def selectedV586TopRawChain
    {J N : SelectedContextualSeventeen W l r H K}
    (A : SelectedContextualEighteen W l r J N) : Bool :=
  match A with
  | .chain _ _ => true
  | _ => false

/-- Explicit, actually inhabited obstruction for EVERY supplied
old18D source: this raw-top bit cannot descend to old OR new quotient. -/
theorem selectedV586RawTopCannotDescend
    (J N : SelectedContextualSeventeen W l r H K)
    (M : SelectedLocalEighteen W l r J N) :
    (¬ ∃ f : Quotient (selectedNineteenSetoid l r J N) → Bool,
      ∀ X, f (selectedNineteenClass l r X) =
        selectedV586TopRawChain l r X) ∧
    (¬ ∃ f : Quotient (selectedRawCongruentSetoid l r J N) → Bool,
      ∀ X, f (selectedRawCongruentClass l r X) =
        selectedV586TopRawChain l r X) :=
  selectedV586NoDescentIfPrependSplit l r J N M
    (selectedV586TopRawChain l r) (by simp [selectedV586TopRawChain])

end ObserverDescent

section SuppliedRightBridge

variable (l r : W)
variable {w z : W}
variable {c d e : PentagonAdjoinedSixCell W l r w z}
variable (F G : ContextFrameEleven W l r c d)
variable (after : SevenRewrite W l r d e)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}

/-- Construct, NOT postulate, an old18D proof in the right N'→N'
fiber from three genuinely supplied typed old18D pieces. -/
def selectedV586RightBridgedSource
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualSeventeen W l r
      (.whiskerRight F G H after) (.whiskerRight F G K after))
    (pre : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) A)
    (mid : SelectedLocalEighteen W l r A B)
    (post : SelectedLocalEighteen W l r B
      (.whiskerRight F G N after)) :
    SelectedLocalEighteen W l r
      (.whiskerRight F G N after) (.whiskerRight F G N after) :=
  .chain (.chain pre mid) post

/-- Source-fingerprint collisions are stable under the actual
typed two-sided old18D bridge, if all connector proofs exist. -/
theorem selectedV586RightBridgePreservesBracket
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualSeventeen W l r
      (.whiskerRight F G H after) (.whiskerRight F G K after))
    (pre : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) A)
    (M L : SelectedLocalEighteen W l r A B)
    (post : SelectedLocalEighteen W l r B
      (.whiskerRight F G N after))
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L) :
    selectedLocalEighteenInnerBracket l r
        (selectedV586RightBridgedSource l r F G after N A B pre M post) =
      selectedLocalEighteenInnerBracket l r
        (selectedV586RightBridgedSource l r F G after N A B pre L post) := by
  change SelectedInheritedOldInnerBracket.oldJoined
      (.oldJoined (selectedLocalEighteenInnerBracket l r pre)
        (selectedLocalEighteenInnerBracket l r M))
      (selectedLocalEighteenInnerBracket l r post) =
    SelectedInheritedOldInnerBracket.oldJoined
      (.oldJoined (selectedLocalEighteenInnerBracket l r pre)
        (selectedLocalEighteenInnerBracket l r L))
      (selectedLocalEighteenInnerBracket l r post)
  exact congrArg
    (fun s : SelectedInheritedOldInnerBracket =>
      SelectedInheritedOldInnerBracket.oldJoined
        (.oldJoined (selectedLocalEighteenInnerBracket l r pre) s)
        (selectedLocalEighteenInnerBracket l r post)) hbr

/-- The constructor trees also retain the DIFFERENCE of original
old18D Type proofs M and L; no quotient equality is inferred. -/
theorem selectedV586RightBridgePreservesDistinct
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualSeventeen W l r
      (.whiskerRight F G H after) (.whiskerRight F G K after))
    (pre : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) A)
    (M L : SelectedLocalEighteen W l r A B)
    (post : SelectedLocalEighteen W l r B
      (.whiskerRight F G N after))
    (hneq : M ≠ L) :
    selectedV586RightBridgedSource l r F G after N A B pre M post ≠
      selectedV586RightBridgedSource l r F G after N A B pre L post := by
  intro h
  apply hneq
  change SelectedLocalEighteen.chain
      (SelectedLocalEighteen.chain pre M) post =
    SelectedLocalEighteen.chain
      (SelectedLocalEighteen.chain pre L) post at h
  injection h
  have hchain : SelectedLocalEighteen.chain pre M =
      SelectedLocalEighteen.chain pre L := by assumption
  injection hchain
  assumption

/-- An explicit SUFFICIENT CONDITION for a same-fiber collision:
a separately supplied parallel old18D pair in another exact fiber,
its actual bracket equality / raw inequality, and both actual bridges.
The theorem constructs the right-fiber pair; it does not assert any
unconditional inhabitance of the external evidence. -/
theorem selectedV586RightBridgeConstructsCollision
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualSeventeen W l r
      (.whiskerRight F G H after) (.whiskerRight F G K after))
    (pre : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) A)
    (M L : SelectedLocalEighteen W l r A B)
    (post : SelectedLocalEighteen W l r B
      (.whiskerRight F G N after))
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hneq : M ≠ L) :
    ∃ X Y : SelectedLocalEighteen W l r
        (.whiskerRight F G N after) (.whiskerRight F G N after),
      X ≠ Y ∧
      selectedLocalEighteenInnerBracket l r X =
        selectedLocalEighteenInnerBracket l r Y := by
  refine ⟨selectedV586RightBridgedSource l r F G after N A B pre M post,
    selectedV586RightBridgedSource l r F G after N A B pre L post, ?_, ?_⟩
  · exact selectedV586RightBridgePreservesDistinct
      l r F G after N A B pre M L post hneq
  · exact selectedV586RightBridgePreservesBracket
      l r F G after N A B pre M L post hbr

/-- The constructed pair now feeds the REAL v5.85 raw decoder
obstruction on the right fiber; quotient equality/non-equality is
deliberately left unclassified. -/
theorem selectedV586RightBridgeDecoderObstruction
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualSeventeen W l r
      (.whiskerRight F G H after) (.whiskerRight F G K after))
    (pre : SelectedLocalEighteen W l r
      (.whiskerRight F G N after) A)
    (M L : SelectedLocalEighteen W l r A B)
    (post : SelectedLocalEighteen W l r B
      (.whiskerRight F G N after))
    (hbr : selectedLocalEighteenInnerBracket l r M =
      selectedLocalEighteenInnerBracket l r L)
    (hneq : M ≠ L) :
    ¬ ∃ decode : SelectedWhiskerPlacementTree →
        SelectedLocalEighteen W l r
          (.whiskerRight F G N after) (.whiskerRight F G N after),
      decode (selectedContextEighteenWhiskerPlacement l r
        (.inherited
          (selectedV586RightBridgedSource l r F G after N A B pre M post))) =
        selectedV586RightBridgedSource l r F G after N A B pre M post ∧
      decode (selectedContextEighteenWhiskerPlacement l r
        (.inherited
          (selectedV586RightBridgedSource l r F G after N A B pre L post))) =
        selectedV586RightBridgedSource l r F G after N A B pre L post := by
  exact selectedV585RightRawSourceDecoderObstruction l r F G after N
    (selectedV586RightBridgedSource l r F G after N A B pre M post)
    (selectedV586RightBridgedSource l r F G after N A B pre L post)
    (selectedV586RightBridgePreservesBracket
      l r F G after N A B pre M L post hbr)
    (selectedV586RightBridgePreservesDistinct
      l r F G after N A B pre M L post hneq)

end SuppliedRightBridge

#print axioms PentagonAdjoinedSixCell.selectedV586OldStable
#print axioms PentagonAdjoinedSixCell.selectedV586NewStable
#print axioms PentagonAdjoinedSixCell.selectedV586OldStableFromUnits
#print axioms PentagonAdjoinedSixCell.selectedV586NewStableFromCongruences
#print axioms PentagonAdjoinedSixCell.selectedV586NewStableImpliesOld
#print axioms PentagonAdjoinedSixCell.selectedV586OldDescent_iff
#print axioms PentagonAdjoinedSixCell.selectedV586NewDescent_iff
#print axioms PentagonAdjoinedSixCell.selectedV586OldLift
#print axioms PentagonAdjoinedSixCell.selectedV586NewLift
#print axioms PentagonAdjoinedSixCell.selectedV586LiftFactorsOldToNew
#print axioms PentagonAdjoinedSixCell.selectedV586JointObserver
#print axioms PentagonAdjoinedSixCell.selectedV586JointOldStable
#print axioms PentagonAdjoinedSixCell.selectedV586JointNewStable
#print axioms PentagonAdjoinedSixCell.selectedV586JointFactors
#print axioms PentagonAdjoinedSixCell.selectedV586NoDescentIfPrependSplit
#print axioms PentagonAdjoinedSixCell.selectedV586TopRawChain
#print axioms PentagonAdjoinedSixCell.selectedV586RawTopCannotDescend
#print axioms PentagonAdjoinedSixCell.selectedV586RightBridgedSource
#print axioms PentagonAdjoinedSixCell.selectedV586RightBridgePreservesBracket
#print axioms PentagonAdjoinedSixCell.selectedV586RightBridgePreservesDistinct
#print axioms PentagonAdjoinedSixCell.selectedV586RightBridgeConstructsCollision
#print axioms PentagonAdjoinedSixCell.selectedV586RightBridgeDecoderObstruction

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
