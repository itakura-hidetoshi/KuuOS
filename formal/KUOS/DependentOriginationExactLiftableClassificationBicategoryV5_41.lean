import KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
import KUOS.DependentOriginationExactClassificationBicategoryV5_23
import Mathlib

namespace KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactClassificationBicategoryV5_23
open KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40

open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Global exact-liftable classification bicategory v5.41

v5.40 replaces the noncomputable chosen-lift presentation by one-cells that
carry an actual exact-universal classification lift as data.  Identity and
composition store the v5.22 identity and composition of those actual lifts
directly.

That strictness at the presentation level is exactly what is needed here.
For fixed exact-liftable objects X and Y, a 2-cell between actual-lift
one-cells f and g is simply the already-validated v5.21 classification 2-cell
between f.actualLift and g.actualLift.

All bicategorical structure is then inherited from the existing v5.23
exact-universal classification bicategory.  No comparison between independently
chosen lifts is required, and no new associativity/coherence proof is invented:
the v5.23 whiskering, associator, unitors, pentagon, and triangle are reused
literally on the stored actual lifts.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- 2-cells are the existing exact-universal classification 2-cells between
the stored actual lifts. -/
abbrev ExactLiftableClassificationActualTwoCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f g :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :=
  ExactUniversalClassificationTwoCell
    (W := W) A f.actualLift g.actualLift

/-- For fixed exact-liftable endpoints, actual-lift one-cells form a category.
The hom type and vertical composition are inherited definitionally from the
v5.22 exact-universal classification hom category. -/
noncomputable instance ExactLiftableClassificationActualOneCell.homCategory
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    Category
      (ExactLiftableClassificationActualOneCell
        (W := W) A X Y) where
  Hom f g :=
    f.actualLift ⟶ g.actualLift
  id f :=
    𝟙 f.actualLift
  comp eta theta :=
    eta ≫ theta
  id_comp := by
    intro f g eta
    exact Category.id_comp eta
  comp_id := by
    intro f g eta
    exact Category.comp_id eta
  assoc := by
    intro f g h i eta theta iota
    exact Category.assoc eta theta iota

/-- On every fixed hom category, forget the raw witness layer and retain the
stored actual exact-universal classification lift.  The map on 2-cells is
definitionally the identity. -/
noncomputable def actualLiftHomFunctor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftableClassificationActualOneCell
        (W := W) A X Y ⥤
      ExactUniversalClassificationOneCell
        (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)
        (CanonicalExactUniversalObject (W := W) A Y) where
  obj f :=
    f.actualLift
  map eta :=
    eta
  map_id := by
    intro f
    rfl
  map_comp := by
    intro f g h eta theta
    rfl

@[simp] theorem actualLiftHomFunctor_obj
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    (actualLiftHomFunctor (W := W) A X Y).obj f =
      f.actualLift :=
  rfl

@[simp] theorem actualLiftHomFunctor_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    {f g :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y}
    (eta : f ⟶ g) :
    (actualLiftHomFunctor (W := W) A X Y).map eta = eta :=
  rfl

/-- Left whiskering is inherited from the stored actual classification lifts. -/
noncomputable def ExactLiftableClassificationActualTwoCell.whiskerLeft
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y)
    {g h :
      ExactLiftableClassificationActualOneCell
        (W := W) A Y Z}
    (eta :
      ExactLiftableClassificationActualTwoCell
        (W := W) A g h) :
    ExactLiftableClassificationActualTwoCell
      (W := W) A
      (exactLiftableClassificationActualOneCellComp
        (W := W) A f g)
      (exactLiftableClassificationActualOneCellComp
        (W := W) A f h) :=
  ExactUniversalClassificationTwoCell.whiskerLeft
    (W := W) A f.actualLift eta

/-- Right whiskering is inherited from the stored actual classification lifts. -/
noncomputable def ExactLiftableClassificationActualTwoCell.whiskerRight
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    {f g :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y}
    (eta :
      ExactLiftableClassificationActualTwoCell
        (W := W) A f g)
    (h :
      ExactLiftableClassificationActualOneCell
        (W := W) A Y Z) :
    ExactLiftableClassificationActualTwoCell
      (W := W) A
      (exactLiftableClassificationActualOneCellComp
        (W := W) A f h)
      (exactLiftableClassificationActualOneCellComp
        (W := W) A g h) :=
  ExactUniversalClassificationTwoCell.whiskerRight
    (W := W) A eta h.actualLift

/-- Associator inherited from the v5.23 classification bicategory. -/
noncomputable def ExactLiftableClassificationActualTwoCell.associatorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {V X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A V X)
    (g :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y)
    (h :
      ExactLiftableClassificationActualOneCell
        (W := W) A Y Z) :
    exactLiftableClassificationActualOneCellComp
        (W := W) A
        (exactLiftableClassificationActualOneCellComp
          (W := W) A f g) h ≅
      exactLiftableClassificationActualOneCellComp
        (W := W) A f
        (exactLiftableClassificationActualOneCellComp
          (W := W) A g h) :=
  ExactUniversalClassificationTwoCell.associatorIso
    (W := W) A f.actualLift g.actualLift h.actualLift

/-- Left unitor inherited from v5.23. -/
noncomputable def ExactLiftableClassificationActualTwoCell.leftUnitorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    exactLiftableClassificationActualOneCellComp
        (W := W) A
        (exactLiftableClassificationActualOneCellId
          (W := W) A X) f ≅
      f :=
  ExactUniversalClassificationTwoCell.leftUnitorIso
    (W := W) A f.actualLift

/-- Right unitor inherited from v5.23. -/
noncomputable def ExactLiftableClassificationActualTwoCell.rightUnitorIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    exactLiftableClassificationActualOneCellComp
        (W := W) A f
        (exactLiftableClassificationActualOneCellId
          (W := W) A Y) ≅
      f :=
  ExactUniversalClassificationTwoCell.rightUnitorIso
    (W := W) A f.actualLift

/-- Exact-liftable classification objects with actual-lift one-cells form a
genuine Mathlib bicategory.

Every law reduces definitionally to the corresponding law in the already
validated v5.23 exact-universal classification bicategory. -/
noncomputable instance ExactLiftableClassificationObject.actualLiftBicategory
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Bicategory
      (ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  Hom X Y :=
    ExactLiftableClassificationActualOneCell
      (W := W) A X Y
  id X :=
    exactLiftableClassificationActualOneCellId
      (W := W) A X
  comp f g :=
    exactLiftableClassificationActualOneCellComp
      (W := W) A f g
  homCategory X Y :=
    ExactLiftableClassificationActualOneCell.homCategory
      (W := W) A X Y
  whiskerLeft {_ _ _} f {_ _} eta :=
    ExactLiftableClassificationActualTwoCell.whiskerLeft
      (W := W) A f eta
  whiskerRight {_ _ _} {_ _} eta h :=
    ExactLiftableClassificationActualTwoCell.whiskerRight
      (W := W) A eta h
  associator f g h :=
    ExactLiftableClassificationActualTwoCell.associatorIso
      (W := W) A f g h
  leftUnitor f :=
    ExactLiftableClassificationActualTwoCell.leftUnitorIso
      (W := W) A f
  rightUnitor f :=
    ExactLiftableClassificationActualTwoCell.rightUnitorIso
      (W := W) A f

  whiskerLeft_id := by
    intro X Y Z f g
    exact Bicategory.whiskerLeft_id f.actualLift g.actualLift

  whiskerLeft_comp := by
    intro X Y Z f g h i eta theta
    exact Bicategory.whiskerLeft_comp
      f.actualLift eta theta

  id_whiskerLeft := by
    intro X Y f g eta
    exact Bicategory.id_whiskerLeft eta

  comp_whiskerLeft := by
    intro X Y Z T f g h h' eta
    exact Bicategory.comp_whiskerLeft
      f.actualLift g.actualLift eta

  id_whiskerRight := by
    intro X Y Z f g
    exact Bicategory.id_whiskerRight
      f.actualLift g.actualLift

  comp_whiskerRight := by
    intro X Y Z f g h eta theta i
    exact Bicategory.comp_whiskerRight
      eta theta i.actualLift

  whiskerRight_id := by
    intro X Y f g eta
    exact Bicategory.whiskerRight_id eta

  whiskerRight_comp := by
    intro X Y Z T f f' eta g h
    exact Bicategory.whiskerRight_comp
      eta g.actualLift h.actualLift

  whisker_assoc := by
    intro X Y Z T f g g' eta h
    exact Bicategory.whisker_assoc
      f.actualLift eta h.actualLift

  whisker_exchange := by
    intro X Y Z f g h i eta theta
    exact Bicategory.whisker_exchange eta theta

  pentagon := by
    intro X Y Z T U f g h i
    exact Bicategory.pentagon
      f.actualLift g.actualLift h.actualLift i.actualLift

  triangle := by
    intro X Y Z f g
    exact Bicategory.triangle
      f.actualLift g.actualLift

/-! ## Regression checks -/

variable
  {WorldLabel : Type uW}
  {PresentationLabel : Type uP}

example :
    Bicategory
      (ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :=
  inferInstance

/-!
## Boundary after v5.41

Closed:

* exact-liftable classification objects now form a global Mathlib bicategory;
* 1-cells carry an actual exact-universal lift rather than only a liftability
  proposition;
* 2-cells are the validated v5.21 classification 2-cells between those lifts;
* horizontal whiskering is inherited from v5.23;
* associator and unitors are inherited from v5.23;
* pentagon and triangle are inherited from v5.23;
* no coherence of independent Classical.choose results is required.

The old v5.38 one-cell interface remains useful as the proposition-level
admissibility interface.  v5.40 supplies a canonical refinement from it into
this actual-lift presentation.

The next theorem unit can package the object map

  X ↦ canonical exact-universal classification object of X

and the one-cell map

  f ↦ f.actualLift

as a global pseudofunctor into the v5.23 exact-universal classification
bicategory.  Because identity and composition were defined using the stored
actual lifts, its compositor and unitor can be chosen from identity isomorphisms.
-/

#print axioms actualLiftHomFunctor
#print axioms ExactLiftableClassificationActualTwoCell.whiskerLeft
#print axioms ExactLiftableClassificationActualTwoCell.whiskerRight
#print axioms ExactLiftableClassificationActualTwoCell.associatorIso
#print axioms ExactLiftableClassificationActualTwoCell.leftUnitorIso
#print axioms ExactLiftableClassificationActualTwoCell.rightUnitorIso

end

end KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
