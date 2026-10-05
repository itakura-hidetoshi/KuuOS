import KUOS.DependentOriginationExactClassificationBicategoryV5_23
import KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
import Mathlib.CategoryTheory.Bicategory.Functor.StrictPseudofunctor
import Mathlib

namespace KUOS.DependentOriginationLocalizedClassificationRealizationV5_24

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
open KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
open KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactClassificationBicategoryV5_23

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Localized classification bicategory and strict realization v5.24

v5.23 made the exact-universal classification sector a genuine Mathlib
bicategory.  This theorem unit supplies the matching localized labelled
bicategory and then packages the v5.22 realization as a global strict
pseudofunctor.

The target objects retain the same external classification labels while their
mathematical carriers are objects of DO₂.  A target 1-cell therefore consists
of label equality plus a native DO₂ 1-cell, and a target 2-cell is simply the
native DO₂ 2-cell between the stored maps.

Because the target wrapper adds only proposition-valued label bookkeeping, its
bicategory structure is inherited directly from DO₂.  Likewise, the exact
classification realization is strict:

* object: X |-> X.realize;
* 1-cell: f |-> f.map.lift, retaining f.label_eq;
* 2-cell: eta |-> eta.cell.lift;
* identity and composition are preserved definitionally;
* whiskering and structural 2-cells reduce to the v4.70 strict realization
  formulas after forgetting the label wrapper.

No mapping-space equivalence or object-essential-surjectivity statement is
asserted here.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-! ## Localized labelled 2-cell wrappers -/

/-- Wrap a native DO₂ 2-cell as a localized classification 2-cell. -/
noncomputable def LocalizedClassificationTwoCell.ofUnderlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : LocalizedClassificationOneCell (W := W) A X Y}
    (eta : f.map ⟶ g.map) :
    LocalizedClassificationTwoCell
      (W := W) A f g where
  cell := eta

@[simp] theorem LocalizedClassificationTwoCell.ofUnderlying_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : LocalizedClassificationOneCell (W := W) A X Y}
    (eta : f.map ⟶ g.map) :
    (LocalizedClassificationTwoCell.ofUnderlying
      (W := W) A eta).cell = eta :=
  rfl

/-- Wrap a native DO₂ 2-isomorphism as a localized classification 2-isomorphism. -/
noncomputable def LocalizedClassificationTwoCell.isoOfUnderlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : LocalizedClassificationOneCell (W := W) A X Y}
    (e : f.map ≅ g.map) :
    f ≅ g where
  hom :=
    LocalizedClassificationTwoCell.ofUnderlying
      (W := W) A e.hom
  inv :=
    LocalizedClassificationTwoCell.ofUnderlying
      (W := W) A e.inv
  hom_inv_id := by
    apply LocalizedClassificationTwoCell.ext
    exact e.hom_inv_id
  inv_hom_id := by
    apply LocalizedClassificationTwoCell.ext
    exact e.inv_hom_id

/-! ## Localized whiskering and structural isomorphisms -/

/-- Left whiskering in the localized labelled sector. -/
noncomputable def LocalizedClassificationTwoCell.whiskerLeft
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : LocalizedClassificationOneCell (W := W) A X Y)
    {g h : LocalizedClassificationOneCell (W := W) A Y Z}
    (eta : LocalizedClassificationTwoCell (W := W) A g h) :
    LocalizedClassificationTwoCell
      (W := W) A
      (LocalizedClassificationOneCell.comp (W := W) A f g)
      (LocalizedClassificationOneCell.comp (W := W) A f h) where
  cell := f.map ◁ eta.cell

/-- Right whiskering in the localized labelled sector. -/
noncomputable def LocalizedClassificationTwoCell.whiskerRight
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : LocalizedClassificationOneCell (W := W) A X Y}
    (eta : LocalizedClassificationTwoCell (W := W) A f g)
    (h : LocalizedClassificationOneCell (W := W) A Y Z) :
    LocalizedClassificationTwoCell
      (W := W) A
      (LocalizedClassificationOneCell.comp (W := W) A f h)
      (LocalizedClassificationOneCell.comp (W := W) A g h) where
  cell := eta.cell ▷ h.map

@[simp] theorem LocalizedClassificationTwoCell.whiskerLeft_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : LocalizedClassificationOneCell (W := W) A X Y)
    {g h : LocalizedClassificationOneCell (W := W) A Y Z}
    (eta : LocalizedClassificationTwoCell (W := W) A g h) :
    (LocalizedClassificationTwoCell.whiskerLeft
      (W := W) A f eta).cell =
      f.map ◁ eta.cell :=
  rfl

@[simp] theorem LocalizedClassificationTwoCell.whiskerRight_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : LocalizedClassificationOneCell (W := W) A X Y}
    (eta : LocalizedClassificationTwoCell (W := W) A f g)
    (h : LocalizedClassificationOneCell (W := W) A Y Z) :
    (LocalizedClassificationTwoCell.whiskerRight
      (W := W) A eta h).cell =
      eta.cell ▷ h.map :=
  rfl

/-- Localized associator. -/
noncomputable def LocalizedClassificationTwoCell.associatorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {V X Y Z :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : LocalizedClassificationOneCell (W := W) A V X)
    (g : LocalizedClassificationOneCell (W := W) A X Y)
    (h : LocalizedClassificationOneCell (W := W) A Y Z) :
    LocalizedClassificationOneCell.comp
        (W := W) A
        (LocalizedClassificationOneCell.comp (W := W) A f g) h ≅
      LocalizedClassificationOneCell.comp
        (W := W) A f
        (LocalizedClassificationOneCell.comp (W := W) A g h) :=
  LocalizedClassificationTwoCell.isoOfUnderlying
    (W := W) A (α_ f.map g.map h.map)

/-- Localized left unitor. -/
noncomputable def LocalizedClassificationTwoCell.leftUnitorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : LocalizedClassificationOneCell (W := W) A X Y) :
    LocalizedClassificationOneCell.comp
        (W := W) A
        (LocalizedClassificationOneCell.id (W := W) A X) f ≅ f :=
  LocalizedClassificationTwoCell.isoOfUnderlying
    (W := W) A (λ_ f.map)

/-- Localized right unitor. -/
noncomputable def LocalizedClassificationTwoCell.rightUnitorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : LocalizedClassificationOneCell (W := W) A X Y) :
    LocalizedClassificationOneCell.comp
        (W := W) A f
        (LocalizedClassificationOneCell.id (W := W) A Y) ≅ f :=
  LocalizedClassificationTwoCell.isoOfUnderlying
    (W := W) A (ρ_ f.map)

/-! ## Genuine localized classification bicategory -/

/-- Localized labelled classification objects form a genuine bicategory. -/
noncomputable instance LocalizedClassificationObject.bicategory
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Bicategory
      (LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  Hom X Y :=
    LocalizedClassificationOneCell (W := W) A X Y
  id X :=
    LocalizedClassificationOneCell.id (W := W) A X
  comp f g :=
    LocalizedClassificationOneCell.comp (W := W) A f g
  homCategory X Y :=
    LocalizedClassificationOneCell.homCategory (W := W) A X Y
  whiskerLeft {_ _ _} f {_ _} eta :=
    LocalizedClassificationTwoCell.whiskerLeft
      (W := W) A f eta
  whiskerRight {_ _ _} {_ _} eta h :=
    LocalizedClassificationTwoCell.whiskerRight
      (W := W) A eta h
  associator f g h :=
    LocalizedClassificationTwoCell.associatorIso
      (W := W) A f g h
  leftUnitor f :=
    LocalizedClassificationTwoCell.leftUnitorIso
      (W := W) A f
  rightUnitor f :=
    LocalizedClassificationTwoCell.rightUnitorIso
      (W := W) A f

  whiskerLeft_id := by
    intro X Y Z f g
    apply LocalizedClassificationTwoCell.ext
    change f.map ◁ 𝟙 g.map = 𝟙 (f.map ≫ g.map)
    exact Bicategory.whiskerLeft_id f.map g.map

  whiskerLeft_comp := by
    intro X Y Z f g h i eta theta
    apply LocalizedClassificationTwoCell.ext
    change f.map ◁ (eta.cell ≫ theta.cell) =
      (f.map ◁ eta.cell) ≫ (f.map ◁ theta.cell)
    exact Bicategory.whiskerLeft_comp f.map eta.cell theta.cell

  id_whiskerLeft := by
    intro X Y f g eta
    apply LocalizedClassificationTwoCell.ext
    change
      (𝟙 X.carrier ◁ eta.cell) =
        (λ_ f.map).hom ≫ eta.cell ≫ (λ_ g.map).inv
    exact Bicategory.id_whiskerLeft eta.cell

  comp_whiskerLeft := by
    intro X Y Z T f g h h' eta
    apply LocalizedClassificationTwoCell.ext
    change
      ((f.map ≫ g.map) ◁ eta.cell) =
        (α_ f.map g.map h.map).hom ≫
          (f.map ◁ (g.map ◁ eta.cell)) ≫
            (α_ f.map g.map h'.map).inv
    exact Bicategory.comp_whiskerLeft f.map g.map eta.cell

  id_whiskerRight := by
    intro X Y Z f g
    apply LocalizedClassificationTwoCell.ext
    change (𝟙 f.map ▷ g.map) = 𝟙 (f.map ≫ g.map)
    exact Bicategory.id_whiskerRight f.map g.map

  comp_whiskerRight := by
    intro X Y Z f g h eta theta i
    apply LocalizedClassificationTwoCell.ext
    change
      ((eta.cell ≫ theta.cell) ▷ i.map) =
        (eta.cell ▷ i.map) ≫ (theta.cell ▷ i.map)
    exact Bicategory.comp_whiskerRight eta.cell theta.cell i.map

  whiskerRight_id := by
    intro X Y f g eta
    apply LocalizedClassificationTwoCell.ext
    change
      (eta.cell ▷ 𝟙 Y.carrier) =
        (ρ_ f.map).hom ≫ eta.cell ≫ (ρ_ g.map).inv
    exact Bicategory.whiskerRight_id eta.cell

  whiskerRight_comp := by
    intro X Y Z T f f' eta g h
    apply LocalizedClassificationTwoCell.ext
    change
      (eta.cell ▷ (g.map ≫ h.map)) =
        (α_ f.map g.map h.map).inv ≫
          ((eta.cell ▷ g.map) ▷ h.map) ≫
            (α_ f'.map g.map h.map).hom
    exact Bicategory.whiskerRight_comp eta.cell g.map h.map

  whisker_assoc := by
    intro X Y Z T f g g' eta h
    apply LocalizedClassificationTwoCell.ext
    change
      ((f.map ◁ eta.cell) ▷ h.map) =
        (α_ f.map g.map h.map).hom ≫
          (f.map ◁ (eta.cell ▷ h.map)) ≫
            (α_ f.map g'.map h.map).inv
    exact Bicategory.whisker_assoc f.map eta.cell h.map

  whisker_exchange := by
    intro X Y Z f g h i eta theta
    apply LocalizedClassificationTwoCell.ext
    exact Bicategory.whisker_exchange eta.cell theta.cell

  pentagon := by
    intro X Y Z T U f g h i
    apply LocalizedClassificationTwoCell.ext
    exact Bicategory.pentagon f.map g.map h.map i.map

  triangle := by
    intro X Y Z f g
    apply LocalizedClassificationTwoCell.ext
    exact Bicategory.triangle f.map g.map

/-! ## Strict classification realization -/

/-- Realization of classification source left whiskering is native target left
whiskering on the chosen DO₂ lifts. -/
@[simp] theorem exactClassificationRealization_source_whiskerLeft
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y)
    {g h : Y ⟶ Z}
    (eta : g ⟶ h) :
    (ExactUniversalClassificationTwoCell.realize
      (W := W) A (f ◁ eta)).cell =
      (ExactUniversalClassificationOneCell.realize
        (W := W) A f).map ◁
          (ExactUniversalClassificationTwoCell.realize
            (W := W) A eta).cell := by
  rfl

/-- Realization of classification source right whiskering is native target
right whiskering. -/
@[simp] theorem exactClassificationRealization_source_whiskerRight
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y}
    (eta : f ⟶ g)
    (h : Y ⟶ Z) :
    (ExactUniversalClassificationTwoCell.realize
      (W := W) A (eta ▷ h)).cell =
      (ExactUniversalClassificationTwoCell.realize
        (W := W) A eta).cell ▷
          (ExactUniversalClassificationOneCell.realize
            (W := W) A h).map := by
  rfl

/-- Strict realization core from the exact-universal labelled classification
bicategory to the localized labelled classification bicategory. -/
noncomputable def exactUniversalClassificationRealizationStrictCore
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    StrictPseudofunctorCore
      (ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel)
      (LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  obj X :=
    X.realize (W := W) A
  map f :=
    ExactUniversalClassificationOneCell.realize
      (W := W) A f
  map_id X := rfl
  map₂ eta :=
    ExactUniversalClassificationTwoCell.realize
      (W := W) A eta
  map₂_id f := rfl
  map₂_comp eta theta := rfl
  map_comp f g := rfl

  map₂_whisker_left := by
    intro X Y Z f g g' eta
    apply LocalizedClassificationTwoCell.ext
    change
      (ExactUniversalRawMorphismTwoCell.whiskerLeft
        (W := W) A f.map eta.cell).lift =
        𝟙 (f.map.lift ≫ g.map.lift) ≫
          (f.map.lift ◁ eta.cell.lift) ≫
            𝟙 (f.map.lift ≫ g'.map.lift)
    exact
      (ExactUniversalRawMorphismTwoCell.whiskerLeft_lift
        (W := W) A f.map eta.cell).trans
        ((Category.id_comp _).trans (Category.comp_id _)).symm

  map₂_whisker_right := by
    intro X Y Z f f' eta g
    apply LocalizedClassificationTwoCell.ext
    change
      (ExactUniversalRawMorphismTwoCell.whiskerRight
        (W := W) A eta.cell g.map).lift =
        𝟙 (f.map.lift ≫ g.map.lift) ≫
          (eta.cell.lift ▷ g.map.lift) ≫
            𝟙 (f'.map.lift ≫ g.map.lift)
    exact
      (ExactUniversalRawMorphismTwoCell.whiskerRight_lift
        (W := W) A eta.cell g.map).trans
        ((Category.id_comp _).trans (Category.comp_id _)).symm

  map₂_left_unitor := by
    intro X Y f
    apply LocalizedClassificationTwoCell.ext
    change
      (ExactUniversalRawMorphismTwoCell.leftUnitorIso
        (W := W) A f.map).hom.lift =
        𝟙 (𝟙 X.source.carrier ≫ f.map.lift) ≫
          (λ_ f.map.lift).hom
    exact
      (exactUniversalRealization_source_leftUnitor_lift
        (W := W) A f.map).trans
        (Category.id_comp _).symm

  map₂_right_unitor := by
    intro X Y f
    apply LocalizedClassificationTwoCell.ext
    change
      (ExactUniversalRawMorphismTwoCell.rightUnitorIso
        (W := W) A f.map).hom.lift =
        𝟙 (f.map.lift ≫ 𝟙 Y.source.carrier) ≫
          (ρ_ f.map.lift).hom
    exact
      (exactUniversalRealization_source_rightUnitor_lift
        (W := W) A f.map).trans
        (Category.id_comp _).symm

  map₂_associator := by
    intro X Y Z T f g h
    apply LocalizedClassificationTwoCell.ext
    change
      (ExactUniversalRawMorphismTwoCell.associatorIso
        (W := W) A f.map g.map h.map).hom.lift =
        𝟙 ((f.map.lift ≫ g.map.lift) ≫ h.map.lift) ≫
          (α_ f.map.lift g.map.lift h.map.lift).hom ≫
            𝟙 (f.map.lift ≫ (g.map.lift ≫ h.map.lift))
    exact
      (exactUniversalRealization_source_associator_lift
        (W := W) A f.map g.map h.map).trans
        ((Category.id_comp _).trans (Category.comp_id _)).symm

/-- Global strict realization pseudofunctor on labelled classification
bicategories. -/
noncomputable def exactUniversalClassificationRealization
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    StrictPseudofunctor
      (ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel)
      (LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) :=
  StrictPseudofunctor.mk'
    (exactUniversalClassificationRealizationStrictCore
      (W := W) A)

@[simp] theorem exactUniversalClassificationRealization_obj_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationRealization
      (W := W) A).obj X).label =
      X.label := by
  rfl

@[simp] theorem exactUniversalClassificationRealization_obj_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationRealization
      (W := W) A).obj X).carrier =
      X.source.carrier := by
  rfl

@[simp] theorem exactUniversalClassificationRealization_map_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    (f : X ⟶ Y) :
    ((exactUniversalClassificationRealization
      (W := W) A).map f).map =
      f.map.lift := by
  rfl

@[simp] theorem exactUniversalClassificationRealization_map₂_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel)
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    ((exactUniversalClassificationRealization
      (W := W) A).map₂ eta).cell =
      eta.cell.lift := by
  rfl

/-!
## Boundary after v5.24

The classification layer now has two genuine bicategories and a strict
label-preserving realization between them:

  ExactUniversalClassification
      -- strict realization -->
  LocalizedClassification.

This completes the categorical infrastructure that v5.21-v5.23 were preparing.
The remaining classification theorem is no longer a question of whether the
objects and cells form valid bicategories.

The next theorem unit may therefore address mapping-level equivalence:
full faithfulness / essential surjectivity of the realization on the relevant
classification sector, with v5.19's ambient-alignment boundary kept explicit.
-/

end

end KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
