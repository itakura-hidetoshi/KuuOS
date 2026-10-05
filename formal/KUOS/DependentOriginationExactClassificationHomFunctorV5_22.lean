import KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
import KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
import Mathlib

namespace KUOS.DependentOriginationExactClassificationHomFunctorV5_22

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Classification hom categories and realization functor v5.22

v5.21 restores the typed classification 1-cell / 2-cell interfaces.  This file
adds the first categorical structure on those interfaces.

For fixed labelled source objects X and Y:

* exact-universal classification 1-cells X --> Y are objects of a hom category;
* exact-universal classification 2-cells are its morphisms;
* localized classification 1-cells between the realized objects form the
  corresponding ambient hom category;
* realization is an honest functor between those two hom categories.

The additional label-equality proof stored in each 1-cell is proposition-valued.
It does not alter vertical 2-cell composition.  The actual categorical laws are
therefore inherited from the already-validated v4.59/v4.60 exact-universal hom
category and from the native DO₂ hom category.

This theorem unit also exposes identity and horizontal composition at the
classification 1-cell level.  It does not yet install a global bicategory
instance: associators, unitors, whiskering, and their coherence are kept for the
next theorem unit.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-! ## Exact-universal classification 1-cell identity and composition -/

/-- Identity exact-universal classification 1-cell. -/
noncomputable def ExactUniversalClassificationOneCell.id
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ExactUniversalClassificationOneCell
      (W := W) A X X where
  label_eq := rfl
  map :=
    ExactUniversalRawMorphism.id
      (W := W) A X.source

/-- Horizontal composition of exact-universal classification 1-cells. -/
noncomputable def ExactUniversalClassificationOneCell.comp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y)
    (g : ExactUniversalClassificationOneCell (W := W) A Y Z) :
    ExactUniversalClassificationOneCell
      (W := W) A X Z where
  label_eq := f.label_eq.trans g.label_eq
  map :=
    ExactUniversalRawMorphism.comp
      (W := W) A f.map g.map

@[simp] theorem ExactUniversalClassificationOneCell.id_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (ExactUniversalClassificationOneCell.id
      (W := W) A X).map =
      ExactUniversalRawMorphism.id
        (W := W) A X.source :=
  rfl

@[simp] theorem ExactUniversalClassificationOneCell.comp_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y)
    (g : ExactUniversalClassificationOneCell (W := W) A Y Z) :
    (ExactUniversalClassificationOneCell.comp
      (W := W) A f g).map =
      ExactUniversalRawMorphism.comp
        (W := W) A f.map g.map :=
  rfl

/-! ## Localized classification 1-cell identity and composition -/

/-- Identity localized classification 1-cell. -/
noncomputable def LocalizedClassificationOneCell.id
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    LocalizedClassificationOneCell
      (W := W) A X X where
  label_eq := rfl
  map := 𝟙 X.carrier

/-- Horizontal composition of localized classification 1-cells. -/
noncomputable def LocalizedClassificationOneCell.comp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : LocalizedClassificationOneCell (W := W) A X Y)
    (g : LocalizedClassificationOneCell (W := W) A Y Z) :
    LocalizedClassificationOneCell
      (W := W) A X Z where
  label_eq := f.label_eq.trans g.label_eq
  map := f.map ≫ g.map

@[simp] theorem LocalizedClassificationOneCell.id_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (LocalizedClassificationOneCell.id
      (W := W) A X).map =
      𝟙 X.carrier :=
  rfl

@[simp] theorem LocalizedClassificationOneCell.comp_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : LocalizedClassificationOneCell (W := W) A X Y)
    (g : LocalizedClassificationOneCell (W := W) A Y Z) :
    (LocalizedClassificationOneCell.comp
      (W := W) A f g).map =
      f.map ≫ g.map :=
  rfl

/-! ## Vertical 2-cell structure -/

/-- Exact-universal classification 2-cells are determined by their validated
underlying v4.58 compatible 2-cell. -/
@[ext] theorem ExactUniversalClassificationTwoCell.ext
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    {eta theta :
      ExactUniversalClassificationTwoCell
        (W := W) A f g}
    (h : eta.cell = theta.cell) :
    eta = theta := by
  cases eta
  cases theta
  cases h
  rfl

/-- Identity exact-universal classification 2-cell. -/
noncomputable def ExactUniversalClassificationTwoCell.id
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y) :
    ExactUniversalClassificationTwoCell
      (W := W) A f f where
  cell :=
    ExactUniversalRawMorphismTwoCell.id
      (W := W) A f.map

/-- Vertical composition of exact-universal classification 2-cells. -/
noncomputable def ExactUniversalClassificationTwoCell.vcomp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g h : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta :
      ExactUniversalClassificationTwoCell
        (W := W) A f g)
    (theta :
      ExactUniversalClassificationTwoCell
        (W := W) A g h) :
    ExactUniversalClassificationTwoCell
      (W := W) A f h where
  cell :=
    ExactUniversalRawMorphismTwoCell.vcomp
      (W := W) A eta.cell theta.cell

@[simp] theorem ExactUniversalClassificationTwoCell.id_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y) :
    (ExactUniversalClassificationTwoCell.id
      (W := W) A f).cell =
      ExactUniversalRawMorphismTwoCell.id
        (W := W) A f.map :=
  rfl

@[simp] theorem ExactUniversalClassificationTwoCell.vcomp_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g h : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta :
      ExactUniversalClassificationTwoCell
        (W := W) A f g)
    (theta :
      ExactUniversalClassificationTwoCell
        (W := W) A g h) :
    (ExactUniversalClassificationTwoCell.vcomp
      (W := W) A eta theta).cell =
      ExactUniversalRawMorphismTwoCell.vcomp
        (W := W) A eta.cell theta.cell :=
  rfl

/-- Exact-universal classification 1-cells form a genuine hom category. -/
instance ExactUniversalClassificationOneCell.homCategory
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    Category
      (ExactUniversalClassificationOneCell
        (W := W) A X Y) where
  Hom f g :=
    ExactUniversalClassificationTwoCell
      (W := W) A f g
  id f :=
    ExactUniversalClassificationTwoCell.id
      (W := W) A f
  comp eta theta :=
    ExactUniversalClassificationTwoCell.vcomp
      (W := W) A eta theta
  id_comp := by
    intro f g eta
    apply ExactUniversalClassificationTwoCell.ext
    simp
  comp_id := by
    intro f g eta
    apply ExactUniversalClassificationTwoCell.ext
    simp
  assoc := by
    intro f g h i eta theta iota
    apply ExactUniversalClassificationTwoCell.ext
    simp

/-- Localized classification 2-cells are determined by their native DO₂
component. -/
@[ext] theorem LocalizedClassificationTwoCell.ext
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : LocalizedClassificationOneCell (W := W) A X Y}
    {eta theta :
      LocalizedClassificationTwoCell
        (W := W) A f g}
    (h : eta.cell = theta.cell) :
    eta = theta := by
  cases eta
  cases theta
  cases h
  rfl

/-- Localized classification 1-cells form the corresponding ambient hom
category. -/
instance LocalizedClassificationOneCell.homCategory
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    Category
      (LocalizedClassificationOneCell
        (W := W) A X Y) where
  Hom f g :=
    LocalizedClassificationTwoCell
      (W := W) A f g
  id f :=
    { cell := 𝟙 f.map }
  comp eta theta :=
    { cell := eta.cell ≫ theta.cell }
  id_comp := by
    intro f g eta
    apply LocalizedClassificationTwoCell.ext
    simp
  comp_id := by
    intro f g eta
    apply LocalizedClassificationTwoCell.ext
    simp
  assoc := by
    intro f g h i eta theta iota
    apply LocalizedClassificationTwoCell.ext
    simp

/-! ## Realization as a hom functor -/

/-- On every pair of exact-universal labelled objects, realization is an honest
functor from the classification source hom category to the localized hom
category. -/
noncomputable def exactUniversalClassificationRealizationHomFunctor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ExactUniversalClassificationOneCell
        (W := W) A X Y ⥤
      LocalizedClassificationOneCell
        (W := W) A
        (X.realize (W := W) A)
        (Y.realize (W := W) A) where
  obj f :=
    ExactUniversalClassificationOneCell.realize
      (W := W) A f
  map eta :=
    ExactUniversalClassificationTwoCell.realize
      (W := W) A eta
  map_id f := by
    apply LocalizedClassificationTwoCell.ext
    change
      (ExactUniversalRawMorphismTwoCell.id
        (W := W) A f.map).lift =
        𝟙 f.map.lift
    exact
      ExactUniversalRawMorphismTwoCell.id_lift
        (W := W) A f.map
  map_comp eta theta := by
    apply LocalizedClassificationTwoCell.ext
    change
      (ExactUniversalRawMorphismTwoCell.vcomp
        (W := W) A eta.cell theta.cell).lift =
        eta.cell.lift ≫ theta.cell.lift
    exact
      ExactUniversalRawMorphismTwoCell.vcomp_lift
        (W := W) A eta.cell theta.cell

@[simp] theorem exactUniversalClassificationRealizationHomFunctor_obj_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    (f : ExactUniversalClassificationOneCell (W := W) A X Y) :
    (exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).obj f |>.map =
      f.map.lift :=
  rfl

@[simp] theorem exactUniversalClassificationRealizationHomFunctor_map_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta : f ⟶ g) :
    ((exactUniversalClassificationRealizationHomFunctor
      (W := W) A X Y).map eta).cell =
      eta.cell.lift :=
  rfl

/-- Realization preserves classification 1-cell identity on the underlying
localized map. -/
@[simp] theorem ExactUniversalClassificationOneCell.realize_id_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (ExactUniversalClassificationOneCell.realize
      (W := W) A
      (ExactUniversalClassificationOneCell.id
        (W := W) A X)).map =
      (LocalizedClassificationOneCell.id
        (W := W) A (X.realize (W := W) A)).map := by
  rfl

/-- Realization preserves horizontal classification 1-cell composition on the
underlying localized map. -/
@[simp] theorem ExactUniversalClassificationOneCell.realize_comp_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y)
    (g : ExactUniversalClassificationOneCell (W := W) A Y Z) :
    (ExactUniversalClassificationOneCell.realize
      (W := W) A
      (ExactUniversalClassificationOneCell.comp
        (W := W) A f g)).map =
      (LocalizedClassificationOneCell.comp
        (W := W) A
        (ExactUniversalClassificationOneCell.realize
          (W := W) A f)
        (ExactUniversalClassificationOneCell.realize
          (W := W) A g)).map := by
  rfl

/-!
## Boundary after v5.22

The classification morphism interface now has genuine local category structure:

  exact-universal labelled 1-cells / 2-cells
      -- realization hom functor -->
  localized labelled 1-cells / 2-cells.

Identity, horizontal 1-cell composition, identity 2-cells, and vertical
2-cell composition are explicit.  Realization preserves the local category
laws and preserves 1-cell identity/composition on underlying DO₂ maps.

The next theorem unit can assemble the classification objects and these hom
categories into bicategories by lifting the already-validated source/DO₂
whiskering, associator, unitors, pentagon, and triangle.  Only after that
assembly should the mapping-side restriction be promoted from an object-level
definition to a bicategorical precomposition construction.
-/

end

end KUOS.DependentOriginationExactClassificationHomFunctorV5_22
