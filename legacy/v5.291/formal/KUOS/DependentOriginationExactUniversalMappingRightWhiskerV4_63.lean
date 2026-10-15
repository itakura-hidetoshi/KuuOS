import KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRestrictionWhiskeringV4_61
open KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Right whiskering of compatible mapping-property 2-cells v4.63

v4.62 constructs left whiskering.  This file proves the independent
right-whiskering pasting law and transports it through the exact universal
mapping interface.

For

  eta : f ==> g,  with f,g : X --> Y,
  k : Y --> Z,

we construct the compatible 2-cell

  eta ▷ k : (f ; k) ==> (g ; k).

The proof deliberately does not obtain this by a formal left/right symmetry.
Instead it isolates the native bicategorical pasting diagram and then applies
the v4.61 restriction theorem and the v4.62 comparison-square reassociation API.
This keeps the dependent wrapper small and makes the orientation of every
associator and whiskering explicit.
-/

universe u v uH vH uB vB wB

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Pure bicategorical pasting lemma underlying right whiskering.

This contains no KuuOS dependent structures.  Starting from the compatibility
square for eta, it moves the right-whiskered 2-cell through the comparison
square for k and reassociates it to the raw right whiskering. -/
private theorem rightWhiskerCompositeSquare
    {B : Type uB} [Bicategory.{wB, vB} B]
    {P Q R X₀ Y₀ Z₀ : B}
    {rf rg : P ⟶ Q}
    (etaL : rf ⟶ rg)
    (rk : Q ⟶ R)
    (cZ : R ⟶ Z₀)
    (cY : Q ⟶ Y₀)
    (cX : P ⟶ X₀)
    {fraw graw : X₀ ⟶ Y₀}
    (etaR : fraw ⟶ graw)
    (kraw : Y₀ ⟶ Z₀)
    (fsq : rf ≫ cY ⟶ cX ≫ fraw)
    (gsq : rg ≫ cY ⟶ cX ≫ graw)
    (ksq : rk ≫ cZ ⟶ cY ≫ kraw)
    (compat :
      (etaL ▷ cY) ≫ gsq =
        fsq ≫ (cX ◁ etaR)) :
    ((etaL ▷ rk) ▷ cZ) ≫
        (Bicategory.associator rg rk cZ).hom ≫
        (rg ◁ ksq) ≫
        (Bicategory.associator rg cY kraw).inv ≫
        (gsq ▷ kraw) ≫
        (Bicategory.associator cX graw kraw).hom =
      (Bicategory.associator rf rk cZ).hom ≫
        (rf ◁ ksq) ≫
        (Bicategory.associator rf cY kraw).inv ≫
        (fsq ▷ kraw) ≫
        (Bicategory.associator cX fraw kraw).hom ≫
        (cX ◁ (etaR ▷ kraw)) := by
  rw [
    Bicategory.associator_naturality_left_assoc,
    ← Bicategory.whisker_exchange_assoc,
    Bicategory.associator_inv_naturality_left_assoc,
    ← Bicategory.comp_whiskerRight_assoc,
    compat,
    Bicategory.comp_whiskerRight_assoc,
    Bicategory.associator_naturality_middle
  ]

/-- Compatibility equation for right whiskering, separated from the dependent
structure constructor. -/
private theorem whiskerRightCompatibility
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (k : ExactUniversalRawMorphism (W := W) A Y Z) :
    (restrictHigherLocalizedModification
        (W := W) (eta.lift.hom ▷ k.lift.hom) ▷
      Z.presentation.comparison) ≫
        (ExactUniversalRawMorphism.comp
          (W := W) A g k).comparison_square.hom =
      (ExactUniversalRawMorphism.comp
        (W := W) A f k).comparison_square.hom ≫
        (X.presentation.comparison ◁ (eta.raw ▷ k.raw)) := by
  rw [restrictHigherLocalizedModification_whiskerRight]
  rw [
    ExactUniversalRawMorphism.comp_comparison_square_hom
      (W := W) A g k
  ]
  calc
    _ =
        (Bicategory.associator
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
          (restrictHigherLocalizedStrongTrans (W := W) k.lift.hom)
          Z.presentation.comparison).hom ≫
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ◁
          k.comparison_square.hom) ≫
        (Bicategory.associator
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
          Y.presentation.comparison k.raw).inv ≫
        (f.comparison_square.hom ▷ k.raw) ≫
        (Bicategory.associator
          X.presentation.comparison f.raw k.raw).hom ≫
        (X.presentation.comparison ◁ (eta.raw ▷ k.raw)) := by
      exact
        rightWhiskerCompositeSquare
          (rf := restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
          (rg := restrictHigherLocalizedStrongTrans (W := W) g.lift.hom)
          (etaL := restrictHigherLocalizedModification (W := W) eta.lift.hom)
          (rk := restrictHigherLocalizedStrongTrans (W := W) k.lift.hom)
          (cZ := Z.presentation.comparison)
          (cY := Y.presentation.comparison)
          (cX := X.presentation.comparison)
          (fraw := f.raw)
          (graw := g.raw)
          (etaR := eta.raw)
          (kraw := k.raw)
          (fsq := f.comparison_square.hom)
          (gsq := g.comparison_square.hom)
          (ksq := k.comparison_square.hom)
          eta.compatibility
    _ =
        ((Bicategory.associator
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
            (restrictHigherLocalizedStrongTrans (W := W) k.lift.hom)
            Z.presentation.comparison).hom ≫
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ◁
            k.comparison_square.hom) ≫
          (Bicategory.associator
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
            Y.presentation.comparison k.raw).inv ≫
          (f.comparison_square.hom ▷ k.raw) ≫
          (Bicategory.associator
            X.presentation.comparison f.raw k.raw).hom) ≫
        (X.presentation.comparison ◁ (eta.raw ▷ k.raw)) := by
      simp only [Category.assoc]
    _ = _ := by
      exact
        (ExactUniversalRawMorphism.comp_comparison_square_hom_assoc
          (W := W) A f k
          (X.presentation.comparison ◁ (eta.raw ▷ k.raw))).symm

/-- Right whiskering of a compatible mapping-property 2-cell by a
mapping-property 1-cell. -/
noncomputable def ExactUniversalRawMorphismTwoCell.whiskerRight
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (k : ExactUniversalRawMorphism (W := W) A Y Z) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp (W := W) A f k)
      (ExactUniversalRawMorphism.comp (W := W) A g k) where
  raw := eta.raw ▷ k.raw
  lift := eta.lift ▷ k.lift
  compatibility :=
    whiskerRightCompatibility (W := W) A eta k

@[simp] theorem ExactUniversalRawMorphismTwoCell.whiskerRight_raw
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (k : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphismTwoCell.whiskerRight
      (W := W) A eta k).raw =
      eta.raw ▷ k.raw :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.whiskerRight_lift
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (k : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphismTwoCell.whiskerRight
      (W := W) A eta k).lift =
      eta.lift ▷ k.lift :=
  rfl

/-!
## Boundary after v4.63

The positive universal mapping source now supports compatible whiskering in
both directions, and both projections agree definitionally with Mathlib's
native raw and DO₂ whiskerings.

The next theorem unit can use these two operations to prove horizontal
interchange and then the associator/unitor coherence required to assemble the
mapping-property source into a bicategory.  The crucial remaining work is no
longer presentation restriction: it is coherence of the newly internalized
horizontal 2-cell calculus.
-/

end

end KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
