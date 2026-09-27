import KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Hom categories for the exact universal mapping source v4.60

v4.57 supplies mapping-property 1-cells and v4.58-v4.59 supply compatible
2-cells with identity and vertical composition.

This file packages those data as genuine hom categories.  The only equality
principle needed is componentwise equality of the raw and DO₂ modifications;
the stored compatibility proof is proposition-valued and therefore proof
irrelevant.

The two evident projections

  mapping 1-cell |-> raw StrongTrans
  mapping 1-cell |-> DO₂ 1-cell

then become honest functors on each hom category.

Horizontal composition between hom categories is still deferred to the next
layer; this file is purely local in the pair of source objects.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Compatible mapping-property 2-cells are determined by their raw and DO₂
components. -/
@[ext] theorem ExactUniversalRawMorphismTwoCell.ext
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    {eta theta : ExactUniversalRawMorphismTwoCell (W := W) A f g}
    (hraw : eta.raw = theta.raw)
    (hlift : eta.lift = theta.lift) :
    eta = theta := by
  cases eta
  cases theta
  cases hraw
  cases hlift
  rfl

/-- Each pair of exact universal raw objects carries a genuine hom category:
objects are mapping-property 1-cells and morphisms are compatible 2-cells. -/
instance ExactUniversalRawMorphism.homCategory
    (X Y : ExactUniversalRawObject (W := W) A) :
    Category (ExactUniversalRawMorphism (W := W) A X Y) where
  Hom f g :=
    ExactUniversalRawMorphismTwoCell (W := W) A f g
  id f :=
    ExactUniversalRawMorphismTwoCell.id (W := W) A f
  comp eta theta :=
    ExactUniversalRawMorphismTwoCell.vcomp (W := W) A eta theta
  id_comp := by
    intro f g eta
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp
    · simp
  comp_id := by
    intro f g eta
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp
    · simp
  assoc := by
    intro f g h i eta theta iota
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp
    · simp

/-- Projection of one mapping hom category to the raw StrongTrans hom category. -/
def exactUniversalRawHomFunctor
    (X Y : ExactUniversalRawObject (W := W) A) :
    ExactUniversalRawMorphism (W := W) A X Y ⥤
      (X.raw ⟶ Y.raw) where
  obj f := f.raw
  map eta := eta.raw
  map_id := by
    intro f
    rfl
  map_comp := by
    intro f g h eta theta
    rfl

/-- Projection of one mapping hom category to the corresponding DO₂ hom
category. -/
def exactUniversalCompletion2HomFunctor
    (X Y : ExactUniversalRawObject (W := W) A) :
    ExactUniversalRawMorphism (W := W) A X Y ⥤
      (X.carrier ⟶ Y.carrier) where
  obj f := f.lift
  map eta := eta.lift
  map_id := by
    intro f
    rfl
  map_comp := by
    intro f g h eta theta
    rfl

@[simp] theorem exactUniversalRawHomFunctor_obj
    (X Y : ExactUniversalRawObject (W := W) A)
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalRawHomFunctor (W := W) A X Y).obj f =
      f.raw :=
  rfl

@[simp] theorem exactUniversalRawHomFunctor_map
    (X Y : ExactUniversalRawObject (W := W) A)
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : f ⟶ g) :
    (exactUniversalRawHomFunctor (W := W) A X Y).map eta =
      eta.raw :=
  rfl

@[simp] theorem exactUniversalCompletion2HomFunctor_obj
    (X Y : ExactUniversalRawObject (W := W) A)
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).obj f =
      f.lift :=
  rfl

@[simp] theorem exactUniversalCompletion2HomFunctor_map
    (X Y : ExactUniversalRawObject (W := W) A)
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : f ⟶ g) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).map eta =
      eta.lift :=
  rfl

/-!
## Boundary after v4.60

For each pair X,Y in the positive universal source, the mapping-property
1-cells X --> Y now form a category, and both the raw and DO₂ projections are
functors on that category.

The next obligation is horizontal composition of compatible 2-cells.  Once that
is proved, the local hom categories and v4.57 1-cell composition can be assembled
into a bicategory, after which the DO₂ projection becomes the desired realization
pseudofunctor.
-/

end

end KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
