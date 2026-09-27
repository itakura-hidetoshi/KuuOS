import KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Identity and vertical composition for mapping-property 2-cells v4.59

v4.58 fixes the correct compatible 2-cell interface.  This file proves the
first categorical closure laws.

The key auxiliary facts are that restriction along the presentation unit
preserves identity modifications and vertical composition.  These are proved
by StrongTrans modification extensionality, because restriction simply
evaluates every component at the image of the presentation unit.

With those lemmas in hand, identity 2-cells and vertical composition reduce to
the bicategory whiskering laws

  id_whiskerRight,
  whiskerLeft_id,
  comp_whiskerRight,
  whiskerLeft_comp

together with the two stored compatibility equations.

Horizontal composition is intentionally deferred to the next theorem unit.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Restriction of StrongTrans modifications preserves identity. -/
@[simp] theorem restrictHigherLocalizedModification_id
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (alpha : F ⟶ G) :
    restrictHigherLocalizedModification (W := W) (𝟙 alpha) =
      𝟙 (restrictHigherLocalizedStrongTrans (W := W) alpha) := by
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  rfl

/-- Restriction of StrongTrans modifications preserves vertical composition. -/
@[simp] theorem restrictHigherLocalizedModification_comp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta gamma : F ⟶ G}
    (eta : alpha ⟶ beta)
    (theta : beta ⟶ gamma) :
    restrictHigherLocalizedModification (W := W) (eta ≫ theta) =
      restrictHigherLocalizedModification (W := W) eta ≫
        restrictHigherLocalizedModification (W := W) theta := by
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  rfl

/-- Identity compatible 2-cell on a mapping-property 1-cell. -/
noncomputable def ExactUniversalRawMorphismTwoCell.id
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell (W := W) A f f where
  raw := 𝟙 f.raw
  lift := 𝟙 f.lift
  compatibility := by
    change
      (Bicategory.whiskerRight
          (restrictHigherLocalizedModification
            (W := W) (𝟙 (f.lift.hom)))
          Y.presentation.comparison) ≫
        f.comparison_square.hom =
      f.comparison_square.hom ≫
        Bicategory.whiskerLeft
          X.presentation.comparison (𝟙 f.raw)
    rw [restrictHigherLocalizedModification_id]
    simp

/-- Vertical composition of compatible mapping-property 2-cells. -/
noncomputable def ExactUniversalRawMorphismTwoCell.vcomp
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g h : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A g h) :
    ExactUniversalRawMorphismTwoCell (W := W) A f h where
  raw := eta.raw ≫ theta.raw
  lift := eta.lift ≫ theta.lift
  compatibility := by
    change
      (Bicategory.whiskerRight
          (restrictHigherLocalizedModification
            (W := W) (eta.lift.hom ≫ theta.lift.hom))
          Y.presentation.comparison) ≫
        h.comparison_square.hom =
      f.comparison_square.hom ≫
        Bicategory.whiskerLeft
          X.presentation.comparison (eta.raw ≫ theta.raw)
    rw [restrictHigherLocalizedModification_comp]
    rw [Bicategory.comp_whiskerRight]
    rw [Category.assoc]
    rw [theta.compatibility]
    rw [← Category.assoc]
    rw [eta.compatibility]
    rw [Category.assoc]
    rw [← Bicategory.whiskerLeft_comp]

@[simp] theorem ExactUniversalRawMorphismTwoCell.id_raw
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.id (W := W) A f).raw =
      𝟙 f.raw :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.id_lift
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.id (W := W) A f).lift =
      𝟙 f.lift :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.vcomp_raw
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g h : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A g h) :
    (ExactUniversalRawMorphismTwoCell.vcomp
      (W := W) A eta theta).raw =
      eta.raw ≫ theta.raw :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.vcomp_lift
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g h : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A g h) :
    (ExactUniversalRawMorphismTwoCell.vcomp
      (W := W) A eta theta).lift =
      eta.lift ≫ theta.lift :=
  rfl

/-!
## Boundary after v4.59

Compatible mapping-property 2-cells now have identity and vertical composition,
and restriction of localized modifications is functorial for those operations.

The next obligation is horizontal composition.  After horizontal composition
and the interchange/coherence laws are formalized, the source data can be
installed as a genuine bicategory and the DO₂ realization can be packaged as a
pseudofunctor.
-/

end

end KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
