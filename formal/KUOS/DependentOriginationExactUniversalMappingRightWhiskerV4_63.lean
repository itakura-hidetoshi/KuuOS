import KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
import KUOS.DependentOriginationExactUniversalRestrictionWhiskeringV4_61
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63

open CategoryTheory
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

This file proves the right-whiskering analogue of v4.62.

For

  eta : f ==> g,  with f,g : X --> Y
  h : Y --> Z,

we construct

  eta ▷ h : (f ; h) ==> (g ; h).

The raw and DO₂ components are the native Mathlib right whiskerings.  The
comparison-square compatibility proof is a single pasting argument: the
2-cell is moved through the comparison square of h, the stored compatibility
of eta is used once, and bicategorical coherence closes the diagram.

With v4.62 and v4.63, both whiskering directions required for the source
bicategory are available.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Right whiskering of a compatible mapping-property 2-cell by a
mapping-property 1-cell. -/
noncomputable def ExactUniversalRawMorphismTwoCell.whiskerRight
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (h : ExactUniversalRawMorphism (W := W) A Y Z) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp (W := W) A f h)
      (ExactUniversalRawMorphism.comp (W := W) A g h) where
  raw := eta.raw ▷ h.raw
  lift := eta.lift ▷ h.lift
  compatibility := by
    change
      (restrictHigherLocalizedModification
          (W := W) (eta.lift.hom ▷ h.lift.hom) ▷
        Z.presentation.comparison) ≫
          (ExactUniversalRawMorphism.comp
            (W := W) A g h).comparison_square.hom =
        (ExactUniversalRawMorphism.comp
          (W := W) A f h).comparison_square.hom ≫
          (X.presentation.comparison ◁ (eta.raw ▷ h.raw))
    rw [restrictHigherLocalizedModification_whiskerRight]
    calc
      _ =
          𝟙 _ ⊗≫
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom) ◁
              h.comparison_square.hom ⊗≫
            (((restrictHigherLocalizedModification
                  (W := W) eta.lift.hom ▷
                    Y.presentation.comparison) ≫
                g.comparison_square.hom) ▷ h.raw) ⊗≫
          𝟙 _ := by
            bicategory
      _ =
          𝟙 _ ⊗≫
            (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom) ◁
              h.comparison_square.hom ⊗≫
            ((f.comparison_square.hom ≫
                (X.presentation.comparison ◁ eta.raw)) ▷ h.raw) ⊗≫
          𝟙 _ := by
            rw [eta.compatibility]
      _ = _ := by
            bicategory

@[simp] theorem ExactUniversalRawMorphismTwoCell.whiskerRight_raw
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (h : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphismTwoCell.whiskerRight
      (W := W) A eta h).raw =
      eta.raw ▷ h.raw :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.whiskerRight_lift
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (h : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphismTwoCell.whiskerRight
      (W := W) A eta h).lift =
      eta.lift ▷ h.lift :=
  rfl

/-!
## Boundary after v4.63

Compatible mapping-property 2-cells now support both left and right
whiskering, and both projections agree definitionally with the native
whiskerings in the raw pseudofunctor bicategory and DO₂.

The remaining source-bicategory obligations are therefore the structural
2-isomorphisms (associator and unitors) and the bicategory coherence laws.
Because both projections already preserve all local 2-cell operations, those
laws can be inherited componentwise once the structural isomorphisms are shown
compatible with the stored comparison squares.
-/

end

end KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
