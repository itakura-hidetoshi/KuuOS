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

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

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
  compatibility := by
    change
      (restrictHigherLocalizedModification
          (W := W) (f.lift.hom ◁ eta.lift.hom) ▷
        Z.presentation.comparison) ≫
          (ExactUniversalRawMorphism.comp
            (W := W) A f h).comparison_square.hom =
        (ExactUniversalRawMorphism.comp
          (W := W) A f g).comparison_square.hom ≫
          (X.presentation.comparison ◁ (f.raw ◁ eta.raw))
    rw [restrictHigherLocalizedModification_whiskerLeft]

    /- `⊗≫` only inserts structural bicategorical coherence.  The source
    and target below also contain KuuOS wrapper definitions.  Expose their
    definitional equalities first, then register only the remaining
    associator coherence for Mathlib's bicategorical composition. -/
    letI : BicategoricalCoherence
        (restrictHigherLocalizedStrongTrans
            (W := W) (f.lift.hom ≫ g.lift.hom) ≫
          Z.presentation.comparison)
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ≫
          restrictHigherLocalizedStrongTrans (W := W) g.lift.hom ≫
            Z.presentation.comparison) :=
      ⟨by
        change
          ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ≫
              restrictHigherLocalizedStrongTrans (W := W) g.lift.hom) ≫
            Z.presentation.comparison) ≅
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ≫
            restrictHigherLocalizedStrongTrans (W := W) g.lift.hom ≫
              Z.presentation.comparison)
        exact
          Bicategory.associator
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
            (restrictHigherLocalizedStrongTrans (W := W) g.lift.hom)
            Z.presentation.comparison⟩

    letI : BicategoricalCoherence
        ((X.presentation.comparison ≫ f.raw) ≫ h.raw)
        (X.presentation.comparison ≫
          (ExactUniversalRawMorphism.comp (W := W) A f h).raw) :=
      ⟨by
        change
          ((X.presentation.comparison ≫ f.raw) ≫ h.raw) ≅
            (X.presentation.comparison ≫ (f.raw ≫ h.raw))
        exact
          Bicategory.associator
            X.presentation.comparison f.raw h.raw⟩

    calc
      _ =
          𝟙 _ ⊗≫
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom) ◁
              ((restrictHigherLocalizedModification
                  (W := W) eta.lift.hom ▷
                    Z.presentation.comparison) ≫
                h.comparison_square.hom) ⊗≫
            f.comparison_square.hom ▷ h.raw ⊗≫
          𝟙 _ := by
            bicategory
      _ =
          𝟙 _ ⊗≫
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom) ◁
              (g.comparison_square.hom ≫
                (Y.presentation.comparison ◁ eta.raw)) ⊗≫
            f.comparison_square.hom ▷ h.raw ⊗≫
          𝟙 _ := by
            rw [eta.compatibility]
      _ = _ := by
            bicategory

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
