import KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
import Mathlib.Tactic.CategoryTheory.BicategoryCoherence

namespace KUOS.DependentOriginationGeneratedWhiskeringV2_68

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

universe u v uH vH

/-!
# Generated localization whiskering calculus v2.68

The first v2.68 file retains every localization generator, its explicit
composition-closure whiskers, and the full equivalence-closure derivation.  To
turn generated path-independence into the five v2.59/v2.60 coherence laws we
also need to whisker an *arbitrary generated derivation*, not only one base
generator.

This file closes that operation internally.  Left and right whiskering are
defined recursively on the retained Type-valued derivation, and their canonical
Cat-valued evaluations are proved to be exactly bicategorical left and right
whiskering of the evaluated 2-isomorphism.

These lemmas are the common calculus needed to express the associator, unit, and
presentation-comparison coherence diagrams as generated localization paths.
No factorization or holonomy-vanishing claim is added here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Add an outer left whisker to one fully retained composition-closure step. -/
def generatedCompClosureWhiskerLeft
    {X Y Z : LocalizationPaths W}
    (k : X ⟶ Y) {p q : Y ⟶ Z}
    (α : GeneratedCompClosure2Cell W p q) :
    GeneratedCompClosure2Cell W (k ≫ p) (k ≫ q) := by
  cases α with
  | whisker f γ g =>
      simpa only [Category.assoc] using
        (GeneratedCompClosure2Cell.whisker (W := W) (k ≫ f) γ g)

/-- Add an outer right whisker to one fully retained composition-closure step. -/
def generatedCompClosureWhiskerRight
    {X Y Z : LocalizationPaths W}
    {p q : X ⟶ Y} (k : Y ⟶ Z)
    (α : GeneratedCompClosure2Cell W p q) :
    GeneratedCompClosure2Cell W (p ≫ k) (q ≫ k) := by
  cases α with
  | whisker f γ g =>
      simpa only [Category.assoc] using
        (GeneratedCompClosure2Cell.whisker (W := W) f γ (g ≫ k))

/-- Left-whisker an arbitrary fully generated localization derivation. -/
def generatedLocalization2CellWhiskerLeft
    {X Y Z : LocalizationPaths W}
    (k : X ⟶ Y) {p q : Y ⟶ Z}
    (α : GeneratedLocalization2Cell W p q) :
    GeneratedLocalization2Cell W (k ≫ p) (k ≫ q) := by
  induction α with
  | ofCompClosure α =>
      exact GeneratedLocalization2Cell.ofCompClosure
        (generatedCompClosureWhiskerLeft W k α)
  | refl p =>
      exact GeneratedLocalization2Cell.refl _
  | symm α ih =>
      exact GeneratedLocalization2Cell.symm ih
  | trans α β ihα ihβ =>
      exact GeneratedLocalization2Cell.trans ihα ihβ

/-- Right-whisker an arbitrary fully generated localization derivation. -/
def generatedLocalization2CellWhiskerRight
    {X Y Z : LocalizationPaths W}
    {p q : X ⟶ Y} (k : Y ⟶ Z)
    (α : GeneratedLocalization2Cell W p q) :
    GeneratedLocalization2Cell W (p ≫ k) (q ≫ k) := by
  induction α with
  | ofCompClosure α =>
      exact GeneratedLocalization2Cell.ofCompClosure
        (generatedCompClosureWhiskerRight W k α)
  | refl p =>
      exact GeneratedLocalization2Cell.refl _
  | symm α ih =>
      exact GeneratedLocalization2Cell.symm ih
  | trans α β ihα ihβ =>
      exact GeneratedLocalization2Cell.trans ihα ihβ

/-- A literal equality of free paths gives a generated localization 2-cell.
This is derived from `refl`; it introduces no new localization relation. -/
def generatedLocalization2CellOfEq
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h : p = q) : GeneratedLocalization2Cell W p q := by
  subst q
  exact GeneratedLocalization2Cell.refl p

@[simp]
theorem generatedLocalization2CellOfEq_rfl
    {X Y : LocalizationPaths W} (p : X ⟶ Y) :
    generatedLocalization2CellOfEq W (rfl : p = p) =
      GeneratedLocalization2Cell.refl p := by
  rfl

/-! ## Evaluation compatibility -/

/-- Evaluation of a left-whiskered generated derivation is exactly left
whiskering of its evaluated isomorphism. -/
theorem generatedLocalization2CellEvaluationIso_whiskerLeft
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : LocalizationPaths W}
    (k : X ⟶ Y) {p q : Y ⟶ Z}
    (α : GeneratedLocalization2Cell W p q) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedLocalization2CellWhiskerLeft W k α) =
      Bicategory.whiskerLeftIso
        ((freePathEvaluator W R D).map k)
        (generatedLocalization2CellEvaluationIso W R D α) := by
  induction α with
  | ofCompClosure α =>
      cases α with
      | whisker f γ g =>
          apply Iso.ext
          simp only [generatedLocalization2CellWhiskerLeft,
            generatedCompClosureWhiskerLeft,
            generatedLocalization2CellEvaluationIso,
            generatedCompClosure2CellEvaluationIso,
            Functor.map_comp, Iso.trans_hom, whiskerLeftIso_hom,
            whiskerRightIso_hom]
          bicategory
  | refl p =>
      apply Iso.ext
      simp [generatedLocalization2CellWhiskerLeft,
        generatedLocalization2CellEvaluationIso]
  | symm α ih =>
      rw [show generatedLocalization2CellWhiskerLeft W k
          (GeneratedLocalization2Cell.symm α) =
          GeneratedLocalization2Cell.symm
            (generatedLocalization2CellWhiskerLeft W k α) by rfl]
      rw [generatedLocalization2CellEvaluationIso_symm]
      rw [ih]
      rfl
  | trans α β ihα ihβ =>
      rw [show generatedLocalization2CellWhiskerLeft W k
          (GeneratedLocalization2Cell.trans α β) =
          GeneratedLocalization2Cell.trans
            (generatedLocalization2CellWhiskerLeft W k α)
            (generatedLocalization2CellWhiskerLeft W k β) by rfl]
      rw [generatedLocalization2CellEvaluationIso_trans]
      rw [ihα, ihβ]
      apply Iso.ext
      simp only [Iso.trans_hom, whiskerLeftIso_hom]
      bicategory

/-- Evaluation of a right-whiskered generated derivation is exactly right
whiskering of its evaluated isomorphism. -/
theorem generatedLocalization2CellEvaluationIso_whiskerRight
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : LocalizationPaths W}
    {p q : X ⟶ Y} (k : Y ⟶ Z)
    (α : GeneratedLocalization2Cell W p q) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedLocalization2CellWhiskerRight W k α) =
      Bicategory.whiskerRightIso
        (generatedLocalization2CellEvaluationIso W R D α)
        ((freePathEvaluator W R D).map k) := by
  induction α with
  | ofCompClosure α =>
      cases α with
      | whisker f γ g =>
          apply Iso.ext
          simp only [generatedLocalization2CellWhiskerRight,
            generatedCompClosureWhiskerRight,
            generatedLocalization2CellEvaluationIso,
            generatedCompClosure2CellEvaluationIso,
            Functor.map_comp, Iso.trans_hom, whiskerLeftIso_hom,
            whiskerRightIso_hom]
          bicategory
  | refl p =>
      apply Iso.ext
      simp [generatedLocalization2CellWhiskerRight,
        generatedLocalization2CellEvaluationIso]
  | symm α ih =>
      rw [show generatedLocalization2CellWhiskerRight W k
          (GeneratedLocalization2Cell.symm α) =
          GeneratedLocalization2Cell.symm
            (generatedLocalization2CellWhiskerRight W k α) by rfl]
      rw [generatedLocalization2CellEvaluationIso_symm]
      rw [ih]
      rfl
  | trans α β ihα ihβ =>
      rw [show generatedLocalization2CellWhiskerRight W k
          (GeneratedLocalization2Cell.trans α β) =
          GeneratedLocalization2Cell.trans
            (generatedLocalization2CellWhiskerRight W k α)
            (generatedLocalization2CellWhiskerRight W k β) by rfl]
      rw [generatedLocalization2CellEvaluationIso_trans]
      rw [ihα, ihβ]
      apply Iso.ext
      simp only [Iso.trans_hom, whiskerRightIso_hom]
      bicategory

/-- The hom of the evaluated left whisker is the ordinary bicategorical left
whisker of the evaluated hom. -/
@[simp]
theorem generatedLocalization2CellEvaluationIso_whiskerLeft_hom
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : LocalizationPaths W}
    (k : X ⟶ Y) {p q : Y ⟶ Z}
    (α : GeneratedLocalization2Cell W p q) :
    (generatedLocalization2CellEvaluationIso W R D
        (generatedLocalization2CellWhiskerLeft W k α)).hom =
      (freePathEvaluator W R D).map k ◁
        (generatedLocalization2CellEvaluationIso W R D α).hom := by
  rw [generatedLocalization2CellEvaluationIso_whiskerLeft W R D k α]
  rfl

/-- The hom of the evaluated right whisker is the ordinary bicategorical right
whisker of the evaluated hom. -/
@[simp]
theorem generatedLocalization2CellEvaluationIso_whiskerRight_hom
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : LocalizationPaths W}
    {p q : X ⟶ Y} (k : Y ⟶ Z)
    (α : GeneratedLocalization2Cell W p q) :
    (generatedLocalization2CellEvaluationIso W R D
        (generatedLocalization2CellWhiskerRight W k α)).hom =
      (generatedLocalization2CellEvaluationIso W R D α).hom ▷
        (freePathEvaluator W R D).map k := by
  rw [generatedLocalization2CellEvaluationIso_whiskerRight W R D k α]
  rfl

/-- Evaluation of a generated cell arising only from literal path equality is
the equality-induced isomorphism between the evaluated paths. -/
theorem generatedLocalization2CellEvaluationIso_ofEq
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h : p = q) :
    generatedLocalization2CellEvaluationIso W R D
        (generatedLocalization2CellOfEq W h) =
      eqToIso (congrArg (freePathEvaluator W R D).map h) := by
  subst q
  rfl

/-- Hom-level equality form of `generatedLocalization2CellEvaluationIso_ofEq`. -/
@[simp]
theorem generatedLocalization2CellEvaluationIso_ofEq_hom
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (h : p = q) :
    (generatedLocalization2CellEvaluationIso W R D
        (generatedLocalization2CellOfEq W h)).hom =
      eqToHom (congrArg (freePathEvaluator W R D).map h) := by
  rw [generatedLocalization2CellEvaluationIso_ofEq W R D h]
  rfl

/-!
## Fixed boundary

The generated syntax is now closed under every operation needed to write the
five quotient/comparison coherence diagrams:

```text
vertical composition      GeneratedLocalization2Cell.trans
inverse                   GeneratedLocalization2Cell.symm
left whiskering           generatedLocalization2CellWhiskerLeft
right whiskering          generatedLocalization2CellWhiskerRight
literal path equality     generatedLocalization2CellOfEq
```

and canonical evaluation preserves each operation exactly.  The next theorem
slice can therefore define the three quotient coherence routes and the two
presentation-comparison routes *inside the generated syntax*, compare them by
`GeneratedEvaluationPathIndependent`, and identify the resulting five defects
with generated loop holonomy.
-/

end KUOS.DependentOriginationGeneratedWhiskeringV2_68
