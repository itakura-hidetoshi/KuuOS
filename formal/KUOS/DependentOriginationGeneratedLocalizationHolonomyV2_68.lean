import KUOS.DependentOriginationUntruncatedHolonomyV2_67

namespace KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58
open KUOS.DependentOriginationFiberIsoThinV2_64
open KUOS.DependentOriginationUntruncatedHolonomyV2_67

universe u v uH vH

/-!
# Fully generated localization 2-holonomy v2.68

The v2.67 layer untruncated Mathlib's outer `Relation.EqvGen`, but its base
constructor still accepted an already proposition-valued

```text
HomRel.CompClosure (Localization.Construction.relations W) p q.
```

Consequently the identity of the underlying localization generator and its left
and right whiskers were still hidden by proof irrelevance.  Evaluation of that
base step therefore had to use `Classical.choice` on the v2.58 existence theorem.

This file removes that remaining truncation before evaluation.  It introduces a
three-stage Type-valued syntax:

```text
LocalizationGenerating2Cell
        ↓ retain one of id / comp / Winv₁ / Winv₂
GeneratedCompClosure2Cell
        ↓ retain explicit left and right whiskers
GeneratedLocalization2Cell
        ↓ retain refl / symm / trans
```

Every generated cell erases to Mathlib's ordinary localization relation, and
every ordinary localization equality has a nonempty generated lift.  Crucially,
once a generated lift has been chosen, its evaluation is structurally determined:
there is no `Classical.choice` in the evaluation of a generating or whiskered
relation step.

Closed generated derivations carry an automorphism-valued holonomy.  As in v2.67,
the exact theorem is

```text
all generated loop holonomies are trivial
  ↔ generated relation evaluation is path-independent.
```

This is the syntax/evaluation half of the v2.68 mathematical unit.  The next
step is to identify the five v2.65 coherence defects with explicit generated
relation loops and derive higher-localization factorization from their generated
holonomy triviality.  No unrestricted factorization theorem is asserted here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The free path category underlying Mathlib's localization construction. -/
abbrev LocalizationPaths :=
  Paths (Localization.Construction.LocQuiver W)

/-- A fully retained Type-valued localization generating relation.

Unlike `Localization.Construction.relations W`, which is proposition-valued,
this syntax remembers which of the four localization generators was used and all
of the data carried by that generator. -/
inductive LocalizationGenerating2Cell :
    {X Y : LocalizationPaths W} →
      (X ⟶ Y) → (X ⟶ Y) → Type (max u v)
  | id (X : Context) :
      LocalizationGenerating2Cell
        (Localization.Construction.ψ₁ W (𝟙 X)) (𝟙 _)
  | comp {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z) :
      LocalizationGenerating2Cell
        (Localization.Construction.ψ₁ W (f ≫ g))
        (Localization.Construction.ψ₁ W f ≫
          Localization.Construction.ψ₁ W g)
  | Winv₁ {X Y : Context} (w : X ⟶ Y) (hw : W w) :
      LocalizationGenerating2Cell
        (Localization.Construction.ψ₁ W w ≫
          Localization.Construction.ψ₂ W w hw)
        (𝟙 _)
  | Winv₂ {X Y : Context} (w : X ⟶ Y) (hw : W w) :
      LocalizationGenerating2Cell
        (Localization.Construction.ψ₂ W w hw ≫
          Localization.Construction.ψ₁ W w)
        (𝟙 _)

/-- Erase a retained generating 2-cell back to Mathlib's proposition-valued
localization generating relation. -/
def generating2CellToRelation
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : LocalizationGenerating2Cell W p q) :
    Localization.Construction.relations W p q := by
  cases α with
  | id X =>
      exact Localization.Construction.relations.id X
  | comp f g =>
      exact Localization.Construction.relations.comp f g
  | Winv₁ w hw =>
      exact Localization.Construction.relations.Winv₁ w hw
  | Winv₂ w hw =>
      exact Localization.Construction.relations.Winv₂ w hw

/-- Every proposition-valued generating relation has a nonempty retained lift.
The result is `Nonempty`, so no proof-irrelevant witness is extracted into data. -/
theorem nonempty_generating2Cell_of_relation
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h : Localization.Construction.relations W p q) :
    Nonempty (LocalizationGenerating2Cell W p q) := by
  cases h with
  | id X =>
      exact ⟨LocalizationGenerating2Cell.id X⟩
  | comp f g =>
      exact ⟨LocalizationGenerating2Cell.comp f g⟩
  | Winv₁ w hw =>
      exact ⟨LocalizationGenerating2Cell.Winv₁ w hw⟩
  | Winv₂ w hw =>
      exact ⟨LocalizationGenerating2Cell.Winv₂ w hw⟩

/-- Type-valued composition closure retaining the exact central generator and
both surrounding paths.

This constructor is the untruncated analogue of `HomRel.CompClosure.intro`. -/
inductive GeneratedCompClosure2Cell :
    {X Y : LocalizationPaths W} →
      (X ⟶ Y) → (X ⟶ Y) → Type (max u v)
  | whisker {s t a b : LocalizationPaths W}
      (f : s ⟶ a) {m₁ m₂ : a ⟶ b}
      (α : LocalizationGenerating2Cell W m₁ m₂)
      (g : b ⟶ t) :
      GeneratedCompClosure2Cell
        (f ≫ m₁ ≫ g) (f ≫ m₂ ≫ g)

/-- Erase an explicit generated composition-closure step to Mathlib's
proposition-valued `HomRel.CompClosure`. -/
def generatedCompClosure2CellToCompRel
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : GeneratedCompClosure2Cell W p q) :
    @HomRel.CompClosure
      (LocalizationPaths W) _
      (Localization.Construction.relations W) X Y p q := by
  cases α with
  | whisker f α g =>
      exact HomRel.CompClosure.intro _ _ f _ _ g
        (generating2CellToRelation W α)

/-- Every proposition-valued composition-closure proof has a nonempty fully
retained lift containing the generator and both whiskers. -/
theorem nonempty_generatedCompClosure2Cell_of_compClosure
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h : @HomRel.CompClosure
      (LocalizationPaths W) _
      (Localization.Construction.relations W) X Y p q) :
    Nonempty (GeneratedCompClosure2Cell W p q) := by
  rcases h with ⟨a, b, f, m₁, m₂, g, hm⟩
  rcases nonempty_generating2Cell_of_relation W hm with ⟨α⟩
  exact ⟨GeneratedCompClosure2Cell.whisker f α g⟩

/-- Fully generated Type-valued localization relation syntax.

The outer layer retains the actual equivalence-closure derivation rather than
collapsing it into `Relation.EqvGen`. -/
inductive GeneratedLocalization2Cell :
    {X Y : LocalizationPaths W} →
      (X ⟶ Y) → (X ⟶ Y) → Type (max u v)
  | ofCompClosure {X Y : LocalizationPaths W} {p q : X ⟶ Y}
      (α : GeneratedCompClosure2Cell W p q) :
      GeneratedLocalization2Cell p q
  | refl {X Y : LocalizationPaths W} (p : X ⟶ Y) :
      GeneratedLocalization2Cell p p
  | symm {X Y : LocalizationPaths W} {p q : X ⟶ Y}
      (α : GeneratedLocalization2Cell p q) :
      GeneratedLocalization2Cell q p
  | trans {X Y : LocalizationPaths W} {p q r : X ⟶ Y}
      (α : GeneratedLocalization2Cell p q)
      (β : GeneratedLocalization2Cell q r) :
      GeneratedLocalization2Cell p r

/-- Erase the fully generated syntax to Mathlib's proposition-valued equivalence
closure. -/
def generatedLocalization2CellToEqvGen
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell W p q) :
    Relation.EqvGen
      (@HomRel.CompClosure
        (LocalizationPaths W) _
        (Localization.Construction.relations W) X Y) p q := by
  induction α with
  | ofCompClosure α =>
      exact Relation.EqvGen.rel _ _
        (generatedCompClosure2CellToCompRel W α)
  | refl p =>
      exact Relation.EqvGen.refl p
  | symm α ih =>
      exact Relation.EqvGen.symm _ _ ih
  | trans α β ihα ihβ =>
      exact Relation.EqvGen.trans _ _ _ ihα ihβ

/-- Every Mathlib equivalence-closure derivation has a nonempty fully generated
Type-valued lift. -/
theorem nonempty_generatedLocalization2Cell_of_eqvGen
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h : Relation.EqvGen
      (@HomRel.CompClosure
        (LocalizationPaths W) _
        (Localization.Construction.relations W) X Y) p q) :
    Nonempty (GeneratedLocalization2Cell W p q) := by
  induction h with
  | rel x y hxy =>
      rcases nonempty_generatedCompClosure2Cell_of_compClosure W hxy with ⟨α⟩
      exact ⟨GeneratedLocalization2Cell.ofCompClosure α⟩
  | refl x =>
      exact ⟨GeneratedLocalization2Cell.refl x⟩
  | symm x y hxy ih =>
      rcases ih with ⟨α⟩
      exact ⟨GeneratedLocalization2Cell.symm α⟩
  | trans x y z hxy hyz ihxy ihyz =>
      rcases ihxy with ⟨α⟩
      rcases ihyz with ⟨β⟩
      exact ⟨GeneratedLocalization2Cell.trans α β⟩

/-- A fully generated localization 2-cell always erases to equality in the
ordinary localization quotient. -/
theorem generatedLocalization2Cell_equalInLocalization
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell W p q) :
    (Quotient.functor (Localization.Construction.relations W)).map p =
      (Quotient.functor (Localization.Construction.relations W)).map q := by
  exact
    (Quotient.functor_homRel_eq_compClosure_eqvGen
      (r := Localization.Construction.relations W) p q).2
      (generatedLocalization2CellToEqvGen W α)

/-- Conversely, every equality in the ordinary localization quotient has a
nonempty fully generated lift. -/
theorem nonempty_generatedLocalization2Cell_of_equalInLocalization
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q) :
    Nonempty (GeneratedLocalization2Cell W p q) := by
  apply nonempty_generatedLocalization2Cell_of_eqvGen W
  exact
    (Quotient.functor_homRel_eq_compClosure_eqvGen
      (r := Localization.Construction.relations W) p q).1 h

/-- Noncomputably choose a generated derivation of an ordinary localization
equality.  Choice occurs only at the level of selecting a derivation; evaluation
of that retained derivation below is canonical and recursive. -/
noncomputable def chosenGeneratedLocalization2CellOfEquality
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q) :
    GeneratedLocalization2Cell W p q :=
  Classical.choice (nonempty_generatedLocalization2Cell_of_equalInLocalization W h)

/-- Forget fully generated syntax to the v2.67 partially untruncated syntax. -/
def generatedLocalization2CellToV267
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell W p q) :
    LocalizationRelation2Cell W p q := by
  induction α with
  | ofCompClosure α =>
      exact LocalizationRelation2Cell.ofCompRel
        (generatedCompClosure2CellToCompRel W α)
  | refl p =>
      exact LocalizationRelation2Cell.refl p
  | symm α ih =>
      exact LocalizationRelation2Cell.symm ih
  | trans α β ihα ihβ =>
      exact LocalizationRelation2Cell.trans ihα ihβ

/-! ## Canonical recursive evaluation -/

/-- Canonical evaluation of one retained localization generator.

There is no local `Classical.choice`: the four cases are exactly the
pseudofunctor identity/composition isomorphisms and the chosen W-adjoint
unit/counit isomorphisms. -/
noncomputable def generating2CellEvaluationIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : LocalizationGenerating2Cell W p q) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map q := by
  cases α with
  | id X =>
      simpa using R.mapId (.mk X)
  | comp f g =>
      simpa [Functor.map_comp] using R.mapComp f.toLoc g.toLoc
  | Winv₁ w hw =>
      simpa [Functor.map_comp] using forwardInverseIso W R D w hw
  | Winv₂ w hw =>
      simpa [Functor.map_comp] using inverseForwardIso W R D w hw

/-- Canonical evaluation of an explicitly whiskered generating relation. -/
noncomputable def generatedCompClosure2CellEvaluationIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : GeneratedCompClosure2Cell W p q) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map q := by
  cases α with
  | whisker f α g =>
      simpa only [Functor.map_comp] using
        (Bicategory.whiskerRightIso
          (Bicategory.whiskerLeftIso
            ((freePathEvaluator W R D).map f)
            (generating2CellEvaluationIso W R D α))
          ((freePathEvaluator W R D).map g))

/-- Canonical recursive evaluation of a fully generated localization 2-cell. -/
noncomputable def generatedLocalization2CellEvaluationIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell W p q) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map q := by
  induction α with
  | ofCompClosure α =>
      exact generatedCompClosure2CellEvaluationIso W R D α
  | refl p =>
      exact Iso.refl _
  | symm α ih =>
      exact ih.symm
  | trans α β ihα ihβ =>
      exact ihα ≪≫ ihβ

@[simp]
theorem generatedLocalization2CellEvaluationIso_refl
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} (p : X ⟶ Y) :
    generatedLocalization2CellEvaluationIso W R D
        (GeneratedLocalization2Cell.refl p) = Iso.refl _ := by
  rfl

@[simp]
theorem generatedLocalization2CellEvaluationIso_symm
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : GeneratedLocalization2Cell W p q) :
    generatedLocalization2CellEvaluationIso W R D
        (GeneratedLocalization2Cell.symm α) =
      (generatedLocalization2CellEvaluationIso W R D α).symm := by
  rfl

@[simp]
theorem generatedLocalization2CellEvaluationIso_trans
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q r : X ⟶ Y}
    (α : GeneratedLocalization2Cell W p q)
    (β : GeneratedLocalization2Cell W q r) :
    generatedLocalization2CellEvaluationIso W R D
        (GeneratedLocalization2Cell.trans α β) =
      generatedLocalization2CellEvaluationIso W R D α ≪≫
        generatedLocalization2CellEvaluationIso W R D β := by
  rfl

/-- Evaluate a chosen fully generated lift of an ordinary localization equality. -/
noncomputable def chosenGeneratedEvaluationIsoOfEquality
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map q :=
  generatedLocalization2CellEvaluationIso W R D
    (chosenGeneratedLocalization2CellOfEquality W h)

/-! ## Generated relation-loop holonomy -/

/-- A closed fully generated localization derivation at a free path. -/
abbrev GeneratedLocalizationLoop
    {X Y : LocalizationPaths W} (p : X ⟶ Y) :=
  GeneratedLocalization2Cell W p p

/-- Holonomy automorphism obtained by canonically evaluating a generated loop. -/
noncomputable def generatedHolonomy
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    (γ : GeneratedLocalizationLoop W p) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map p :=
  generatedLocalization2CellEvaluationIso W R D γ

/-- Difference loop of two fully generated derivations with common endpoints. -/
def generatedLocalization2CellDifference
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : GeneratedLocalization2Cell W p q) :
    GeneratedLocalizationLoop W q :=
  GeneratedLocalization2Cell.trans (GeneratedLocalization2Cell.symm α) β

@[simp]
theorem generatedLocalization2CellDifference_holonomy
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : GeneratedLocalization2Cell W p q) :
    generatedHolonomy W R D (generatedLocalization2CellDifference W α β) =
      (generatedLocalization2CellEvaluationIso W R D α).symm ≪≫
        generatedLocalization2CellEvaluationIso W R D β := by
  rfl

/-- Two generated derivations evaluate equally exactly when the holonomy of their
difference loop is trivial. -/
theorem generatedLocalization2CellEvaluationIso_eq_iff_differenceHolonomy_trivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : GeneratedLocalization2Cell W p q) :
    generatedLocalization2CellEvaluationIso W R D α =
        generatedLocalization2CellEvaluationIso W R D β ↔
      generatedHolonomy W R D
          (generatedLocalization2CellDifference W α β) = Iso.refl _ := by
  constructor
  · intro h
    rw [generatedLocalization2CellDifference_holonomy, h]
    simp
  · intro h
    rw [generatedLocalization2CellDifference_holonomy] at h
    apply Iso.ext
    have hhom :
        (generatedLocalization2CellEvaluationIso W R D α).inv ≫
            (generatedLocalization2CellEvaluationIso W R D β).hom =
          𝟙 _ := by
      simpa using congrArg Iso.hom h
    calc
      (generatedLocalization2CellEvaluationIso W R D α).hom =
          (generatedLocalization2CellEvaluationIso W R D α).hom ≫ 𝟙 _ := by simp
      _ =
          (generatedLocalization2CellEvaluationIso W R D α).hom ≫
            ((generatedLocalization2CellEvaluationIso W R D α).inv ≫
              (generatedLocalization2CellEvaluationIso W R D β).hom) := by
            rw [hhom]
      _ = (generatedLocalization2CellEvaluationIso W R D β).hom := by simp

/-- Every fully generated closed localization derivation has trivial evaluated
holonomy. -/
def GeneratedHolonomyTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ {X Y : LocalizationPaths W} (p : X ⟶ Y)
    (γ : GeneratedLocalizationLoop W p),
    generatedHolonomy W R D γ = Iso.refl _

/-- Canonical evaluation of fully generated localization derivations is
path-independent. -/
def GeneratedEvaluationPathIndependent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : GeneratedLocalization2Cell W p q),
    generatedLocalization2CellEvaluationIso W R D α =
      generatedLocalization2CellEvaluationIso W R D β

/-- Trivial generated holonomy forces path-independent generated evaluation. -/
theorem generatedEvaluationPathIndependent_of_holonomyTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : GeneratedHolonomyTrivial W R D) :
    GeneratedEvaluationPathIndependent W R D := by
  intro X Y p q α β
  exact
    (generatedLocalization2CellEvaluationIso_eq_iff_differenceHolonomy_trivial
      W R D α β).2
      (h q (generatedLocalization2CellDifference W α β))

/-- Path-independent generated evaluation forces every generated loop holonomy to
be the identity. -/
theorem generatedHolonomyTrivial_of_evaluationPathIndependent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : GeneratedEvaluationPathIndependent W R D) :
    GeneratedHolonomyTrivial W R D := by
  intro X Y p γ
  have heq := h γ (GeneratedLocalization2Cell.refl p)
  simpa [generatedHolonomy] using heq

/-- Main generated-holonomy theorem: generated relation evaluation is
path-independent exactly when every fully retained relation-loop holonomy is
trivial. -/
theorem generatedHolonomyTrivial_iff_evaluationPathIndependent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedHolonomyTrivial W R D ↔
      GeneratedEvaluationPathIndependent W R D := by
  constructor
  · exact generatedEvaluationPathIndependent_of_holonomyTrivial W R D
  · exact generatedHolonomyTrivial_of_evaluationPathIndependent W R D

/-- Under trivial generated holonomy, every generated lift of a fixed ordinary
localization equality evaluates to the same iso as the selected generated lift. -/
theorem generatedLocalization2CellEvaluationIso_eq_chosen_of_holonomyTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (htriv : GeneratedHolonomyTrivial W R D)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q)
    (α : GeneratedLocalization2Cell W p q) :
    generatedLocalization2CellEvaluationIso W R D α =
      chosenGeneratedEvaluationIsoOfEquality W R D h := by
  exact
    generatedEvaluationPathIndependent_of_holonomyTrivial W R D htriv
      α (chosenGeneratedLocalization2CellOfEquality W h)

/-! ## Compatibility with previously proved thin sectors -/

/-- v2.64 fiber-functor iso-thinness forces every generated loop holonomy to be
trivial. -/
theorem generatedHolonomyTrivial_of_fiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hiso : IsFiberFunctorIsoThin R) :
    GeneratedHolonomyTrivial W R D := by
  intro X Y p γ
  letI : Subsingleton
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p) :=
    hiso X Y _ _
  exact Subsingleton.elim _ _

/-- Trivial fiber automorphisms from v2.64 are therefore a sufficient special
case of generated holonomy triviality. -/
theorem generatedHolonomyTrivial_of_trivialFiberAutomorphisms
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (htriv : IsFiberAutomorphismTrivial R) :
    GeneratedHolonomyTrivial W R D :=
  generatedHolonomyTrivial_of_fiberFunctorIsoThin W R D
    (isFiberFunctorIsoThin_of_fiberCoreThin R
      (isFiberCoreThin_of_automorphismTrivial R htriv))

/-!
## Boundary fixed by the first v2.68 theorem slice

The retained hierarchy is now

```text
LocalizationGenerating2Cell
  remembers id / comp / Winv₁ / Winv₂ and their data
        ↓
GeneratedCompClosure2Cell
  remembers explicit left and right whiskers
        ↓
GeneratedLocalization2Cell
  remembers refl / symm / trans
        ↓ erase
Relation.EqvGen (HomRel.CompClosure relations)
        ↓ quotient
ordinary W.Localization equality.
```

For any selected fully generated derivation, evaluation is canonical:

```text
id     ↦ R.mapId
comp   ↦ R.mapComp
Winv₁  ↦ chosen adjoint-equivalence unit
Winv₂  ↦ chosen adjoint-equivalence counit
whisker ↦ bicategorical whiskering
refl/symm/trans ↦ identity/inverse/vertical composition.
```

Thus the remaining question is no longer hidden inside `CompClosure` proof
irrelevance or local evaluation choice.  It is whether the explicit generated
loop holonomies needed by the five v2.65 coherence laws vanish.

This file deliberately does not identify those five defects yet and therefore
does not assert

```text
GeneratedHolonomyTrivial W R D
  → HasHigherLocalizationFactorization W R
```

nor the unrestricted implication from weak W-admissibility.  Those are the next
steps of the same v2.68 mathematical unit.
-/

end KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
