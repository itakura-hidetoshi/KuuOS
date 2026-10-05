import KUOS.DependentOriginationExactClassificationHomFunctorV5_22
import KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
import Mathlib

namespace KUOS.DependentOriginationExactClassificationBicategoryV5_23

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
open KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
open KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
open KUOS.DependentOriginationExactUniversalMappingCoherenceV4_68
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Exact-universal classification bicategory v5.23

v5.21 restored label-preserving classification 1/2-cells and v5.22 installed
their local hom categories.  This theorem unit lifts the already-validated
v4.69 exact-universal source bicategory through that label wrapper.

The label equality carried by a classification 1-cell remains proposition-valued
bookkeeping.  All bicategorical 2-dimensional mathematics is inherited from the
underlying exact-universal source:

* whiskering uses v4.62/v4.63;
* associator and unitors use the v4.67 structural isomorphisms;
* pentagon and triangle use v4.68;
* the complete underlying bicategory is v4.69.

No labels are erased: composition composes their equality proofs and identities
use reflexivity.  The structural 2-cells never manufacture new label equality.

This file installs only the exact-universal classification bicategory.  The
localized labelled bicategory and the global realization pseudofunctor are kept
for the next theorem unit.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-! ## Lift underlying source 2-cells and 2-isomorphisms -/

/-- Wrap one already-compatible source 2-cell as a classification 2-cell. -/
noncomputable def ExactUniversalClassificationTwoCell.ofUnderlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta : f.map ⟶ g.map) :
    ExactUniversalClassificationTwoCell
      (W := W) A f g where
  cell := eta

@[simp] theorem ExactUniversalClassificationTwoCell.ofUnderlying_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta : f.map ⟶ g.map) :
    (ExactUniversalClassificationTwoCell.ofUnderlying
      (W := W) A eta).cell = eta :=
  rfl

/-- Wrap an underlying source 2-isomorphism as a classification 2-isomorphism. -/
noncomputable def ExactUniversalClassificationTwoCell.isoOfUnderlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (e : f.map ≅ g.map) :
    f ≅ g where
  hom :=
    ExactUniversalClassificationTwoCell.ofUnderlying
      (W := W) A e.hom
  inv :=
    ExactUniversalClassificationTwoCell.ofUnderlying
      (W := W) A e.inv
  hom_inv_id := by
    apply ExactUniversalClassificationTwoCell.ext
    exact e.hom_inv_id
  inv_hom_id := by
    apply ExactUniversalClassificationTwoCell.ext
    exact e.inv_hom_id

@[simp] theorem ExactUniversalClassificationTwoCell.isoOfUnderlying_hom_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (e : f.map ≅ g.map) :
    (ExactUniversalClassificationTwoCell.isoOfUnderlying
      (W := W) A e).hom.cell = e.hom :=
  rfl

@[simp] theorem ExactUniversalClassificationTwoCell.isoOfUnderlying_inv_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (e : f.map ≅ g.map) :
    (ExactUniversalClassificationTwoCell.isoOfUnderlying
      (W := W) A e).inv.cell = e.inv :=
  rfl

/-! ## Whiskering and structural isomorphisms -/

/-- Left whiskering is inherited from the exact-universal source bicategory. -/
noncomputable def ExactUniversalClassificationTwoCell.whiskerLeft
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y)
    {g h : ExactUniversalClassificationOneCell (W := W) A Y Z}
    (eta : ExactUniversalClassificationTwoCell (W := W) A g h) :
    ExactUniversalClassificationTwoCell
      (W := W) A
      (ExactUniversalClassificationOneCell.comp (W := W) A f g)
      (ExactUniversalClassificationOneCell.comp (W := W) A f h) where
  cell :=
    ExactUniversalRawMorphismTwoCell.whiskerLeft
      (W := W) A f.map eta.cell

/-- Right whiskering is inherited from the exact-universal source bicategory. -/
noncomputable def ExactUniversalClassificationTwoCell.whiskerRight
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta : ExactUniversalClassificationTwoCell (W := W) A f g)
    (h : ExactUniversalClassificationOneCell (W := W) A Y Z) :
    ExactUniversalClassificationTwoCell
      (W := W) A
      (ExactUniversalClassificationOneCell.comp (W := W) A f h)
      (ExactUniversalClassificationOneCell.comp (W := W) A g h) where
  cell :=
    ExactUniversalRawMorphismTwoCell.whiskerRight
      (W := W) A eta.cell h.map

@[simp] theorem ExactUniversalClassificationTwoCell.whiskerLeft_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y)
    {g h : ExactUniversalClassificationOneCell (W := W) A Y Z}
    (eta : ExactUniversalClassificationTwoCell (W := W) A g h) :
    (ExactUniversalClassificationTwoCell.whiskerLeft
      (W := W) A f eta).cell =
      ExactUniversalRawMorphismTwoCell.whiskerLeft
        (W := W) A f.map eta.cell :=
  rfl

@[simp] theorem ExactUniversalClassificationTwoCell.whiskerRight_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta : ExactUniversalClassificationTwoCell (W := W) A f g)
    (h : ExactUniversalClassificationOneCell (W := W) A Y Z) :
    (ExactUniversalClassificationTwoCell.whiskerRight
      (W := W) A eta h).cell =
      ExactUniversalRawMorphismTwoCell.whiskerRight
        (W := W) A eta.cell h.map :=
  rfl

/-- Classification associator lifted from v4.67. -/
noncomputable def ExactUniversalClassificationTwoCell.associatorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {V X Y Z :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A V X)
    (g : ExactUniversalClassificationOneCell (W := W) A X Y)
    (h : ExactUniversalClassificationOneCell (W := W) A Y Z) :
    ExactUniversalClassificationOneCell.comp
        (W := W) A
        (ExactUniversalClassificationOneCell.comp (W := W) A f g) h ≅
      ExactUniversalClassificationOneCell.comp
        (W := W) A f
        (ExactUniversalClassificationOneCell.comp (W := W) A g h) :=
  ExactUniversalClassificationTwoCell.isoOfUnderlying
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.associatorIso
      (W := W) A f.map g.map h.map)

/-- Classification left unitor lifted from v4.67. -/
noncomputable def ExactUniversalClassificationTwoCell.leftUnitorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y) :
    ExactUniversalClassificationOneCell.comp
        (W := W) A
        (ExactUniversalClassificationOneCell.id (W := W) A X) f ≅ f :=
  ExactUniversalClassificationTwoCell.isoOfUnderlying
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.leftUnitorIso
      (W := W) A f.map)

/-- Classification right unitor lifted from v4.67. -/
noncomputable def ExactUniversalClassificationTwoCell.rightUnitorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y) :
    ExactUniversalClassificationOneCell.comp
        (W := W) A f
        (ExactUniversalClassificationOneCell.id (W := W) A Y) ≅ f :=
  ExactUniversalClassificationTwoCell.isoOfUnderlying
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.rightUnitorIso
      (W := W) A f.map)

/-! ## Genuine bicategory instance -/

/-- Exact-universal classification objects with label-preserving 1-cells form a
Mathlib bicategory.  Every bicategorical law is inherited from the underlying
v4.69 source bicategory after forgetting the proposition-valued label proof. -/
noncomputable instance ExactUniversalClassificationObject.bicategory
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Bicategory
      (ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  Hom X Y :=
    ExactUniversalClassificationOneCell (W := W) A X Y
  id X :=
    ExactUniversalClassificationOneCell.id (W := W) A X
  comp f g :=
    ExactUniversalClassificationOneCell.comp (W := W) A f g
  homCategory X Y :=
    ExactUniversalClassificationOneCell.homCategory (W := W) A X Y
  whiskerLeft {_ _ _} f {_ _} eta :=
    ExactUniversalClassificationTwoCell.whiskerLeft
      (W := W) A f eta
  whiskerRight {_ _ _} {_ _} eta h :=
    ExactUniversalClassificationTwoCell.whiskerRight
      (W := W) A eta h
  associator f g h :=
    ExactUniversalClassificationTwoCell.associatorIso
      (W := W) A f g h
  leftUnitor f :=
    ExactUniversalClassificationTwoCell.leftUnitorIso
      (W := W) A f
  rightUnitor f :=
    ExactUniversalClassificationTwoCell.rightUnitorIso
      (W := W) A f

  whiskerLeft_id := by
    intro X Y Z f g
    apply ExactUniversalClassificationTwoCell.ext
    change f.map ◁ 𝟙 g.map = 𝟙 (f.map ≫ g.map)
    exact Bicategory.whiskerLeft_id f.map g.map

  whiskerLeft_comp := by
    intro X Y Z f g h i eta theta
    apply ExactUniversalClassificationTwoCell.ext
    change f.map ◁ (eta.cell ≫ theta.cell) =
      (f.map ◁ eta.cell) ≫ (f.map ◁ theta.cell)
    exact Bicategory.whiskerLeft_comp f.map eta.cell theta.cell

  id_whiskerLeft := by
    intro X Y f g eta
    apply ExactUniversalClassificationTwoCell.ext
    change
      (𝟙 X.source ◁ eta.cell) =
        (ExactUniversalRawMorphismTwoCell.leftUnitorIso
          (W := W) A f.map).hom ≫
          eta.cell ≫
            (ExactUniversalRawMorphismTwoCell.leftUnitorIso
              (W := W) A g.map).inv
    exact Bicategory.id_whiskerLeft eta.cell

  comp_whiskerLeft := by
    intro X Y Z T f g h h' eta
    apply ExactUniversalClassificationTwoCell.ext
    change
      ((f.map ≫ g.map) ◁ eta.cell) =
        (ExactUniversalRawMorphismTwoCell.associatorIso
          (W := W) A f.map g.map h.map).hom ≫
          (f.map ◁ (g.map ◁ eta.cell)) ≫
            (ExactUniversalRawMorphismTwoCell.associatorIso
              (W := W) A f.map g.map h'.map).inv
    exact Bicategory.comp_whiskerLeft f.map g.map eta.cell

  id_whiskerRight := by
    intro X Y Z f g
    apply ExactUniversalClassificationTwoCell.ext
    change
      (𝟙 f.map ▷ g.map) = 𝟙 (f.map ≫ g.map)
    exact Bicategory.id_whiskerRight f.map g.map

  comp_whiskerRight := by
    intro X Y Z f g h eta theta i
    apply ExactUniversalClassificationTwoCell.ext
    change
      ((eta.cell ≫ theta.cell) ▷ i.map) =
        (eta.cell ▷ i.map) ≫ (theta.cell ▷ i.map)
    exact Bicategory.comp_whiskerRight eta.cell theta.cell i.map

  whiskerRight_id := by
    intro X Y f g eta
    apply ExactUniversalClassificationTwoCell.ext
    change
      (eta.cell ▷ 𝟙 Y.source) =
        (ExactUniversalRawMorphismTwoCell.rightUnitorIso
          (W := W) A f.map).hom ≫
          eta.cell ≫
            (ExactUniversalRawMorphismTwoCell.rightUnitorIso
              (W := W) A g.map).inv
    exact Bicategory.whiskerRight_id eta.cell

  whiskerRight_comp := by
    intro X Y Z T f f' eta g h
    apply ExactUniversalClassificationTwoCell.ext
    change
      (eta.cell ▷ (g.map ≫ h.map)) =
        (ExactUniversalRawMorphismTwoCell.associatorIso
          (W := W) A f.map g.map h.map).inv ≫
          ((eta.cell ▷ g.map) ▷ h.map) ≫
            (ExactUniversalRawMorphismTwoCell.associatorIso
              (W := W) A f'.map g.map h.map).hom
    exact Bicategory.whiskerRight_comp eta.cell g.map h.map

  whisker_assoc := by
    intro X Y Z T f g g' eta h
    apply ExactUniversalClassificationTwoCell.ext
    change
      ((f.map ◁ eta.cell) ▷ h.map) =
        (ExactUniversalRawMorphismTwoCell.associatorIso
          (W := W) A f.map g.map h.map).hom ≫
          (f.map ◁ (eta.cell ▷ h.map)) ≫
            (ExactUniversalRawMorphismTwoCell.associatorIso
              (W := W) A f.map g'.map h.map).inv
    exact Bicategory.whisker_assoc f.map eta.cell h.map

  whisker_exchange := by
    intro X Y Z f g h i eta theta
    apply ExactUniversalClassificationTwoCell.ext
    exact Bicategory.whisker_exchange eta.cell theta.cell

  pentagon := by
    intro X Y Z T U f g h i
    apply ExactUniversalClassificationTwoCell.ext
    exact
      ExactUniversalRawMorphismTwoCell.pentagon
        (W := W) A f.map g.map h.map i.map

  triangle := by
    intro X Y Z f g
    apply ExactUniversalClassificationTwoCell.ext
    exact
      ExactUniversalRawMorphismTwoCell.triangle
        (W := W) A f.map g.map

/-! ## Regression checks -/

variable
  {WorldLabel : Type uW}
  {PresentationLabel : Type uP}

example :
    Bicategory
      (ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :=
  inferInstance

/-!
## Boundary after v5.23

The exact-universal classification sector is now a genuine Mathlib bicategory:

* objects retain external world/presentation labels;
* 1-cells preserve those labels by explicit equality;
* 2-cells are the validated compatible exact-universal cells;
* all bicategorical coherence is inherited from v4.69.

No equality of external labels is inferred from carrier equivalence.

The next theorem unit can construct the localized labelled bicategory and then
promote the v5.22 realization hom functors to a global strict pseudofunctor.
That is the correct categorical foundation before proving any mapping-side
biequivalence or final classification theorem.
-/

end

end KUOS.DependentOriginationExactClassificationBicategoryV5_23
