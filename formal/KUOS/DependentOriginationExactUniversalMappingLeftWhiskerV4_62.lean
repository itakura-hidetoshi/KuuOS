import KUOS.DependentOriginationExactUniversalRestrictionWhiskeringV4_61
import KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62

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

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Left whiskering of compatible mapping-property 2-cells v4.62

The v4.61 restriction lemmas supply the remaining presentation-unit API needed
to transport Mathlib's native bicategorical whiskering into the positive
universal mapping source.

For

  f : X --> Y
  eta : g ==> h,  with g,h : Y --> Z,

this file constructs the compatible 2-cell

  f ◁ eta : (f ; g) ==> (f ; h).

The raw and DO₂ components are the native left whiskerings.  Compatibility is a
single pasting argument: bicategorical coherence moves the whiskered 2-cell next
to the target comparison square, the stored compatibility equation for eta is
used once, and coherence closes the resulting diagram.

Right whiskering remains separate so that each pasting direction is validated
independently.
-/

universe u v uH vH uB vB wB

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Pure bicategorical pasting lemma underlying left whiskering.

This lemma contains no KuuOS dependent structures.  It isolates the string
diagram from the expensive elaboration of the mapping-property wrappers. -/
private theorem leftWhiskerCompositeSquare
    {B : Type uB} [Bicategory.{wB, vB} B]
    {P Q R X₀ Y₀ Z₀ : B}
    (rf : P ⟶ Q)
    {rg rh : Q ⟶ R}
    (etaL : rg ⟶ rh)
    (cZ : R ⟶ Z₀)
    (cY : Q ⟶ Y₀)
    (cX : P ⟶ X₀)
    (fraw : X₀ ⟶ Y₀)
    {graw hraw : Y₀ ⟶ Z₀}
    (etaR : graw ⟶ hraw)
    (gsq : rg ≫ cZ ⟶ cY ≫ graw)
    (hsq : rh ≫ cZ ⟶ cY ≫ hraw)
    (fsq : rf ≫ cY ⟶ cX ≫ fraw)
    (compat :
      (etaL ▷ cZ) ≫ hsq =
        gsq ≫ (cY ◁ etaR)) :
    ((rf ◁ etaL) ▷ cZ) ≫
        (Bicategory.associator rf rh cZ).hom ≫
        (rf ◁ hsq) ≫
        (Bicategory.associator rf cY hraw).inv ≫
        (fsq ▷ hraw) ≫
        (Bicategory.associator cX fraw hraw).hom =
      (Bicategory.associator rf rg cZ).hom ≫
        (rf ◁ gsq) ≫
        (Bicategory.associator rf cY graw).inv ≫
        (fsq ▷ graw) ≫
        (Bicategory.associator cX fraw graw).hom ≫
        (cX ◁ (fraw ◁ etaR)) := by
  rw [
    Bicategory.associator_naturality_middle_assoc,
    ← Bicategory.whiskerLeft_comp_assoc,
    compat,
    Bicategory.whiskerLeft_comp_assoc,
    Bicategory.associator_inv_naturality_right_assoc,
    Bicategory.whisker_exchange_assoc,
    Bicategory.associator_naturality_right
  ]

/-- The hom component of the v4.57 composite comparison square.

Keeping this expansion behind a small theorem avoids asking later proofs to
weak-head-normalize the whole dependent structure `ExactUniversalRawMorphism.comp`
inside a large `change` target. -/
@[simp, reassoc] theorem ExactUniversalRawMorphism.comp_comparison_square_hom
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphism.comp
      (W := W) A f g).comparison_square.hom =
      (Bicategory.associator
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
        (restrictHigherLocalizedStrongTrans (W := W) g.lift.hom)
        Z.presentation.comparison).hom ≫
      (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ◁
        g.comparison_square.hom) ≫
      (Bicategory.associator
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
        Y.presentation.comparison g.raw).inv ≫
      (f.comparison_square.hom ▷ g.raw) ≫
      (Bicategory.associator
        X.presentation.comparison f.raw g.raw).hom :=
  rfl

/-- Compatibility equation for left whiskering, proved independently of
the dependent structure constructor. -/
private theorem whiskerLeftCompatibility
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    {g h : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A g h) :
    (restrictHigherLocalizedModification
        (W := W) (f.lift.hom ◁ eta.lift.hom) ▷
      Z.presentation.comparison) ≫
        (ExactUniversalRawMorphism.comp
          (W := W) A f h).comparison_square.hom =
      (ExactUniversalRawMorphism.comp
        (W := W) A f g).comparison_square.hom ≫
        (X.presentation.comparison ◁ (f.raw ◁ eta.raw)) := by
  rw [restrictHigherLocalizedModification_whiskerLeft]
  rw [
    ExactUniversalRawMorphism.comp_comparison_square_hom
      (W := W) A f h
  ]
  calc
    _ =
        ((Bicategory.associator
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
            (restrictHigherLocalizedStrongTrans (W := W) g.lift.hom)
            Z.presentation.comparison).hom ≫
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ◁
            g.comparison_square.hom) ≫
          (Bicategory.associator
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
            Y.presentation.comparison g.raw).inv ≫
          (f.comparison_square.hom ▷ g.raw) ≫
          (Bicategory.associator
            X.presentation.comparison f.raw g.raw).hom) ≫
        (X.presentation.comparison ◁ (f.raw ◁ eta.raw)) := by
      simpa only [← Category.assoc] using
        (leftWhiskerCompositeSquare
          (rf := restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
          (etaL := restrictHigherLocalizedModification (W := W) eta.lift.hom)
          (cZ := Z.presentation.comparison)
          (cY := Y.presentation.comparison)
          (cX := X.presentation.comparison)
          (fraw := f.raw)
          (etaR := eta.raw)
          (gsq := g.comparison_square.hom)
          (hsq := h.comparison_square.hom)
          (fsq := f.comparison_square.hom)
          eta.compatibility)
    _ = _ := by
      exact
        (ExactUniversalRawMorphism.comp_comparison_square_hom_assoc
          (W := W) A f g
          (X.presentation.comparison ◁ (f.raw ◁ eta.raw))).symm

/-- Left whiskering of a compatible mapping-property 2-cell by a
mapping-property 1-cell. -/
noncomputable def ExactUniversalRawMorphismTwoCell.whiskerLeft
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    {g h : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A g h) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp (W := W) A f g)
      (ExactUniversalRawMorphism.comp (W := W) A f h) where
  raw := f.raw ◁ eta.raw
  lift := f.lift ◁ eta.lift
  compatibility :=
    whiskerLeftCompatibility (W := W) A f eta

@[simp] theorem ExactUniversalRawMorphismTwoCell.whiskerLeft_raw
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    {g h : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A g h) :
    (ExactUniversalRawMorphismTwoCell.whiskerLeft
      (W := W) A f eta).raw =
      f.raw ◁ eta.raw :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.whiskerLeft_lift
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    {g h : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A g h) :
    (ExactUniversalRawMorphismTwoCell.whiskerLeft
      (W := W) A f eta).lift =
      f.lift ◁ eta.lift :=
  rfl

/-!
## Boundary after v4.62

The positive universal mapping source now supports compatible left whiskering
of 2-cells, with raw and DO₂ projections equal to the native Mathlib
whiskerings.

The next theorem unit will prove the right-whiskering analogue.  Once both
directions are available, interchange and the source bicategory coherence laws
can be installed using the corresponding laws in the raw pseudofunctor
bicategory and DO₂.
-/

end

end KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
