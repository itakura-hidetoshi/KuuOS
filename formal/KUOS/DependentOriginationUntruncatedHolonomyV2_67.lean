import KUOS.DependentOriginationGaugeObstructionV2_66
import KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58

namespace KUOS.DependentOriginationUntruncatedHolonomyV2_67

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58
open KUOS.DependentOriginationFiberIsoThinV2_64
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGaugeObstructionV2_66

universe u v uH vH

/-!
# Untruncated localization relation holonomy v2.67

Mathlib's ordinary localization identifies free paths through the proposition-valued
relation

```text
Relation.EqvGen (HomRel.CompClosure (Localization.Construction.relations W)).
```

That is exactly the correct 1-categorical quotient, but the proof of equality has
already been propositionally truncated.  For a Cat-valued pseudofunctor this can
hide the 2-dimensional information that matters for coherent descent.

This file introduces a minimal Type-valued lift of that equivalence closure.  A
`LocalizationRelation2Cell W p q` remembers an actual derivation from `p` to `q`:
a composition-closed generating relation, reflexivity, inverse, or vertical
composition.  Every ordinary quotient equality still has a nonempty space of such
lifts, but distinct lifts need not evaluate to the same natural isomorphism.

Using the v2.57 free-path evaluator and the v2.58 relation-isomorphism theorem, we
evaluate every retained derivation to an actual Cat 2-isomorphism.  Closed
relation derivations therefore acquire an automorphism-valued holonomy.  The main
theorem identifies the exact obstruction:

```text
evaluation is independent of the retained relation derivation
  ↔ every relation-loop holonomy is trivial.
```

Thus v2.66's gauge obstruction can now be attacked as a concrete path-holonomy
problem rather than as an unspecified coherence choice problem.

No claim is made here that weak W-admissibility forces all holonomy to vanish.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The free path category used in Mathlib's localization construction. -/
abbrev LocalizationPaths :=
  Paths (Localization.Construction.LocQuiver W)

/-- The composition-closed generating relation prior to equivalence closure. -/
abbrev LocalizationCompRel
    {X Y : LocalizationPaths W} :
    (X ⟶ Y) → (X ⟶ Y) → Prop :=
  @HomRel.CompClosure
    (LocalizationPaths W) _
    (Localization.Construction.relations W) X Y

/-- A Type-valued, untruncated witness of the equivalence closure used by the
ordinary localization quotient.

The `ofCompRel` constructor retains one composition-closed generating step;
`refl`, `symm`, and `trans` retain the actual equivalence-closure derivation.
Unlike `Relation.EqvGen`, this lives in `Type`, so it can be evaluated into actual
2-isomorphism data. -/
inductive LocalizationRelation2Cell :
    {X Y : LocalizationPaths W} →
      (X ⟶ Y) → (X ⟶ Y) → Type (max u v)
  | ofCompRel {X Y : LocalizationPaths W} {p q : X ⟶ Y}
      (h : LocalizationCompRel W p q) :
      LocalizationRelation2Cell p q
  | refl {X Y : LocalizationPaths W} (p : X ⟶ Y) :
      LocalizationRelation2Cell p p
  | symm {X Y : LocalizationPaths W} {p q : X ⟶ Y}
      (α : LocalizationRelation2Cell p q) :
      LocalizationRelation2Cell q p
  | trans {X Y : LocalizationPaths W} {p q r : X ⟶ Y}
      (α : LocalizationRelation2Cell p q)
      (β : LocalizationRelation2Cell q r) :
      LocalizationRelation2Cell p r

/-- Forget the retained Type-valued derivation back to Mathlib's
proposition-valued equivalence closure. -/
def relation2CellToEqvGen
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : LocalizationRelation2Cell W p q) :
    Relation.EqvGen (LocalizationCompRel W) p q := by
  induction α with
  | ofCompRel h =>
      exact Relation.EqvGen.rel _ _ h
  | refl p =>
      exact Relation.EqvGen.refl p
  | symm α ih =>
      exact Relation.EqvGen.symm _ _ ih
  | trans α β ihα ihβ =>
      exact Relation.EqvGen.trans _ _ _ ihα ihβ

/-- Every proposition-valued Mathlib derivation has a nonempty space of retained
Type-valued lifts.  The target is `Nonempty`, so this respects the fact that the
input proof itself is propositionally truncated. -/
theorem nonempty_relation2Cell_of_eqvGen
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h : Relation.EqvGen (LocalizationCompRel W) p q) :
    Nonempty (LocalizationRelation2Cell W p q) := by
  induction h with
  | rel x y hxy =>
      exact ⟨LocalizationRelation2Cell.ofCompRel hxy⟩
  | refl x =>
      exact ⟨LocalizationRelation2Cell.refl x⟩
  | symm x y hxy ih =>
      rcases ih with ⟨α⟩
      exact ⟨LocalizationRelation2Cell.symm α⟩
  | trans x y z hxy hyz ihxy ihyz =>
      rcases ihxy with ⟨α⟩
      rcases ihyz with ⟨β⟩
      exact ⟨LocalizationRelation2Cell.trans α β⟩

/-- A retained 2-cell always erases to an equality in the ordinary localization. -/
theorem relation2Cell_equalInLocalization
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : LocalizationRelation2Cell W p q) :
    (Quotient.functor (Localization.Construction.relations W)).map p =
      (Quotient.functor (Localization.Construction.relations W)).map q := by
  exact
    (Quotient.functor_homRel_eq_compClosure_eqvGen
      (r := Localization.Construction.relations W) p q).2
      (relation2CellToEqvGen W α)

/-- Conversely, every equality in the ordinary localization has a nonempty space
of retained relation 2-cell lifts. -/
theorem nonempty_relation2Cell_of_equalInLocalization
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q) :
    Nonempty (LocalizationRelation2Cell W p q) := by
  apply nonempty_relation2Cell_of_eqvGen W
  exact
    (Quotient.functor_homRel_eq_compClosure_eqvGen
      (r := Localization.Construction.relations W) p q).1 h

/-- A noncomputable retained lift of an ordinary localization equality.
This is deliberately only a *choice of derivation*; no coherence property is
claimed for this choice. -/
noncomputable def chosenRelation2CellOfEquality
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q) :
    LocalizationRelation2Cell W p q :=
  Classical.choice (nonempty_relation2Cell_of_equalInLocalization W h)

/-! ## Evaluation of retained relation 2-cells -/

/-- Evaluate an untruncated localization-relation derivation as an actual natural
isomorphism between the corresponding v2.57 free-path functors.

A composition-closed generating step uses the v2.58 existence theorem; retained
reflexivity, symmetry, and transitivity become identity, inverse, and vertical
composition of isomorphisms. -/
noncomputable def relation2CellEvaluationIso
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : LocalizationRelation2Cell W p q) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map q := by
  induction α with
  | ofCompRel h =>
      exact Classical.choice (compClosure_hasEvaluationIso W R D h)
  | refl p =>
      exact Iso.refl _
  | symm α ih =>
      exact ih.symm
  | trans α β ihα ihβ =>
      exact ihα ≪≫ ihβ

@[simp]
theorem relation2CellEvaluationIso_refl
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} (p : X ⟶ Y) :
    relation2CellEvaluationIso W R D (LocalizationRelation2Cell.refl p) =
      Iso.refl _ := by
  rfl

@[simp]
theorem relation2CellEvaluationIso_symm
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α : LocalizationRelation2Cell W p q) :
    relation2CellEvaluationIso W R D (LocalizationRelation2Cell.symm α) =
      (relation2CellEvaluationIso W R D α).symm := by
  rfl

@[simp]
theorem relation2CellEvaluationIso_trans
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q r : X ⟶ Y}
    (α : LocalizationRelation2Cell W p q)
    (β : LocalizationRelation2Cell W q r) :
    relation2CellEvaluationIso W R D (LocalizationRelation2Cell.trans α β) =
      relation2CellEvaluationIso W R D α ≪≫
        relation2CellEvaluationIso W R D β := by
  rfl

/-- Evaluate a chosen retained lift of an ordinary quotient equality. -/
noncomputable def chosenEvaluationIsoOfEquality
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map q :=
  relation2CellEvaluationIso W R D (chosenRelation2CellOfEquality W h)

/-! ## Closed relation loops and evaluation holonomy -/

/-- A retained closed relation derivation at a free path. -/
abbrev LocalizationRelationLoop
    {X Y : LocalizationPaths W} (p : X ⟶ Y) :=
  LocalizationRelation2Cell W p p

/-- Evaluation holonomy of a closed retained relation derivation. -/
noncomputable def relationLoopHolonomy
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    (γ : LocalizationRelationLoop W p) :
    (freePathEvaluator W R D).map p ≅
      (freePathEvaluator W R D).map p :=
  relation2CellEvaluationIso W R D γ

/-- The difference of two retained derivations with the same endpoints is a
closed relation loop at their common codomain path. -/
def relation2CellDifference
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : LocalizationRelation2Cell W p q) :
    LocalizationRelationLoop W q :=
  LocalizationRelation2Cell.trans (LocalizationRelation2Cell.symm α) β

@[simp]
theorem relation2CellDifference_holonomy
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : LocalizationRelation2Cell W p q) :
    relationLoopHolonomy W R D (relation2CellDifference W α β) =
      (relation2CellEvaluationIso W R D α).symm ≪≫
        relation2CellEvaluationIso W R D β := by
  rfl

/-- Two retained derivations evaluate to the same 2-isomorphism exactly when the
holonomy of their difference loop is trivial. -/
theorem relation2CellEvaluationIso_eq_iff_differenceHolonomy_trivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : LocalizationRelation2Cell W p q) :
    relation2CellEvaluationIso W R D α =
        relation2CellEvaluationIso W R D β ↔
      relationLoopHolonomy W R D (relation2CellDifference W α β) =
        Iso.refl _ := by
  constructor
  · intro h
    rw [relation2CellDifference_holonomy, h]
    simp
  · intro h
    rw [relation2CellDifference_holonomy] at h
    apply Iso.ext
    have hhom :
        (relation2CellEvaluationIso W R D α).inv ≫
            (relation2CellEvaluationIso W R D β).hom =
          𝟙 _ := by
      simpa using congrArg Iso.hom h
    calc
      (relation2CellEvaluationIso W R D α).hom =
          (relation2CellEvaluationIso W R D α).hom ≫ 𝟙 _ := by simp
      _ =
          (relation2CellEvaluationIso W R D α).hom ≫
            ((relation2CellEvaluationIso W R D α).inv ≫
              (relation2CellEvaluationIso W R D β).hom) := by
            rw [hhom]
      _ = (relation2CellEvaluationIso W R D β).hom := by simp

/-- All retained relation-loop holonomies are trivial.  This is a property of the
free-path evaluator together with the chosen pointwise W adjoint-equivalence
data, not an assumption about arbitrary noninvertible 2-cells. -/
def EvaluationHolonomyTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ {X Y : LocalizationPaths W} (p : X ⟶ Y)
    (γ : LocalizationRelationLoop W p),
    relationLoopHolonomy W R D γ = Iso.refl _

/-- Evaluation of retained relation derivations is path-independent. -/
def Relation2CellEvaluationPathIndependent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (α β : LocalizationRelation2Cell W p q),
    relation2CellEvaluationIso W R D α =
      relation2CellEvaluationIso W R D β

/-- Trivial loop holonomy forces path-independence of all retained relation
2-cell evaluations. -/
theorem relation2CellEvaluationPathIndependent_of_holonomyTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : EvaluationHolonomyTrivial W R D) :
    Relation2CellEvaluationPathIndependent W R D := by
  intro X Y p q α β
  exact
    (relation2CellEvaluationIso_eq_iff_differenceHolonomy_trivial
      W R D α β).2
      (h q (relation2CellDifference W α β))

/-- Conversely, path-independent evaluation forces every retained closed-loop
holonomy to be the identity. -/
theorem evaluationHolonomyTrivial_of_relation2CellEvaluationPathIndependent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : Relation2CellEvaluationPathIndependent W R D) :
    EvaluationHolonomyTrivial W R D := by
  intro X Y p γ
  have heq := h γ (LocalizationRelation2Cell.refl p)
  simpa [relationLoopHolonomy] using heq

/-- Main v2.67 obstruction theorem: the propositionally truncated localization
relations evaluate coherently exactly when every retained relation-loop has
trivial automorphism holonomy. -/
theorem evaluationHolonomyTrivial_iff_relation2CellEvaluationPathIndependent
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    EvaluationHolonomyTrivial W R D ↔
      Relation2CellEvaluationPathIndependent W R D := by
  constructor
  · exact relation2CellEvaluationPathIndependent_of_holonomyTrivial W R D
  · exact evaluationHolonomyTrivial_of_relation2CellEvaluationPathIndependent W R D

/-- Under trivial holonomy, any retained lift of a quotient equality evaluates to
the same natural isomorphism as the noncomputably chosen lift. -/
theorem relation2CellEvaluationIso_eq_chosen_of_holonomyTrivial
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (htriv : EvaluationHolonomyTrivial W R D)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h :
      (Quotient.functor (Localization.Construction.relations W)).map p =
        (Quotient.functor (Localization.Construction.relations W)).map q)
    (α : LocalizationRelation2Cell W p q) :
    relation2CellEvaluationIso W R D α =
      chosenEvaluationIsoOfEquality W R D h := by
  exact
    relation2CellEvaluationPathIndependent_of_holonomyTrivial W R D htriv
      α (chosenRelation2CellOfEquality W h)

/-! ## Recovery of the previously known thin sectors -/

/-- Fiber-functor iso-thinness from v2.64 forces every relation-loop holonomy to
be trivial, since the holonomy is an automorphism of a functor between image
fibers. -/
theorem evaluationHolonomyTrivial_of_fiberFunctorIsoThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hiso : IsFiberFunctorIsoThin R) :
    EvaluationHolonomyTrivial W R D := by
  intro X Y p γ
  letI : Subsingleton
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p) :=
    hiso X Y _ _
  exact Subsingleton.elim _ _

/-- The intrinsic trivial-fiber-automorphism sector from v2.64 is therefore a
special case of relation-loop holonomy triviality. -/
theorem evaluationHolonomyTrivial_of_trivialFiberAutomorphisms
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (htriv : IsFiberAutomorphismTrivial R) :
    EvaluationHolonomyTrivial W R D :=
  evaluationHolonomyTrivial_of_fiberFunctorIsoThin W R D
    (isFiberFunctorIsoThin_of_fiberCoreThin R
      (isFiberCoreThin_of_automorphismTrivial R htriv))

/-!
## Boundary fixed by v2.67

The exact logical picture is now

```text
ordinary localization equality
  = Prop-truncated EqvGen/CompClosure relation
        ↓ Nonempty lift
LocalizationRelation2Cell W p q : Type
        ↓ evaluation
freePathEvaluator(p) ≅ freePathEvaluator(q)
        ↓ compare two lifts
closed relation-loop holonomy automorphism.
```

And the obstruction theorem is exact:

```text
all relation-loop holonomies trivial
  ↔ evaluation is independent of retained relation derivation.
```

The previously proved iso-thin sector forces this condition automatically, but
weak W-admissibility alone has not been shown to do so.  The next mathematical
step is to connect the five v2.65/v2.66 gauge defects to explicit closed retained
relation loops.  If that connection is established, one can determine whether
weak admissibility always trivializes those loop classes or whether ordinary
1-categorical localization genuinely loses a nontrivial 2-dimensional monodromy
obstruction.

No unrestricted higher-localization factorization theorem is asserted here.
-/

end KUOS.DependentOriginationUntruncatedHolonomyV2_67
