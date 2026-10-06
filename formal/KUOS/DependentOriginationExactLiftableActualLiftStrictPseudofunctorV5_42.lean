import KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
import Mathlib.CategoryTheory.Bicategory.Functor.StrictPseudofunctor
import Mathlib

namespace KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactClassificationBicategoryV5_23
open KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41

open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Actual-lift strict pseudofunctor v5.42

v5.40 replaced proposition-only liftability data by one-cells carrying an
actual exact-universal classification lift.  v5.41 used those stored lifts to
install a global bicategory on exact-liftable classification objects.

This theorem unit packages the evident global projection to the already
validated v5.23 exact-universal classification bicategory:

* object: the canonical v5.36 exact-universal classification representative;
* 1-cell: the stored `actualLift`;
* 2-cell: the same v5.21 classification 2-cell;
* identities and compositions are preserved definitionally.

Consequently the projection is not merely a pseudofunctor but a Mathlib
`StrictPseudofunctor`.  The only proof content in its strict core is removal
of the identity transports inserted by `StrictPseudofunctorCore`.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-! ## Definitional projection lemmas -/

@[simp] theorem actualLift_source_whiskerLeft
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
    (eta : g ⟶ h) :
    f ◁ eta =
      ExactUniversalClassificationTwoCell.whiskerLeft
        (W := W) A f.actualLift eta :=
  rfl

@[simp] theorem actualLift_source_whiskerRight
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    {f g :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y}
    (eta : f ⟶ g)
    (h :
      ExactLiftableClassificationActualOneCell
        (W := W) A Y Z) :
    eta ▷ h =
      ExactUniversalClassificationTwoCell.whiskerRight
        (W := W) A eta h.actualLift :=
  rfl

@[simp] theorem actualLift_source_leftUnitor_hom
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    (λ_ f).hom =
      (ExactUniversalClassificationTwoCell.leftUnitorIso
        (W := W) A f.actualLift).hom :=
  rfl

@[simp] theorem actualLift_source_rightUnitor_hom
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    (ρ_ f).hom =
      (ExactUniversalClassificationTwoCell.rightUnitorIso
        (W := W) A f.actualLift).hom :=
  rfl

@[simp] theorem actualLift_source_associator_hom
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
    (α_ f g h).hom =
      (ExactUniversalClassificationTwoCell.associatorIso
        (W := W) A f.actualLift g.actualLift h.actualLift).hom :=
  rfl

/-! ## Global strict projection -/

/-- Strict core of the global projection from the v5.41 exact-liftable
bicategory to the v5.23 exact-universal classification bicategory. -/
noncomputable def exactLiftableActualLiftStrictCore
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    StrictPseudofunctorCore
      (ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel)
      (ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  obj X :=
    CanonicalExactUniversalObject (W := W) A X
  map f :=
    f.actualLift
  map_id X :=
    rfl
  map₂ eta :=
    eta
  map₂_id f :=
    rfl
  map₂_comp eta theta :=
    rfl
  map_comp f g :=
    rfl

  map₂_whisker_left := by
    intro X Y Z f g g' eta
    change
      ExactUniversalClassificationTwoCell.whiskerLeft
          (W := W) A f.actualLift eta =
        𝟙 _ ≫
          ExactUniversalClassificationTwoCell.whiskerLeft
            (W := W) A f.actualLift eta ≫
          𝟙 _
    exact
      ((Category.id_comp _).trans (Category.comp_id _)).symm

  map₂_whisker_right := by
    intro X Y Z f f' eta g
    change
      ExactUniversalClassificationTwoCell.whiskerRight
          (W := W) A eta g.actualLift =
        𝟙 _ ≫
          ExactUniversalClassificationTwoCell.whiskerRight
            (W := W) A eta g.actualLift ≫
          𝟙 _
    exact
      ((Category.id_comp _).trans (Category.comp_id _)).symm

  map₂_left_unitor := by
    intro X Y f
    change
      (ExactUniversalClassificationTwoCell.leftUnitorIso
        (W := W) A f.actualLift).hom =
        𝟙 _ ≫
          (ExactUniversalClassificationTwoCell.leftUnitorIso
            (W := W) A f.actualLift).hom
    exact (Category.id_comp _).symm

  map₂_right_unitor := by
    intro X Y f
    change
      (ExactUniversalClassificationTwoCell.rightUnitorIso
        (W := W) A f.actualLift).hom =
        𝟙 _ ≫
          (ExactUniversalClassificationTwoCell.rightUnitorIso
            (W := W) A f.actualLift).hom
    exact (Category.id_comp _).symm

  map₂_associator := by
    intro X Y Z T f g h
    change
      (ExactUniversalClassificationTwoCell.associatorIso
        (W := W) A f.actualLift g.actualLift h.actualLift).hom =
        𝟙 _ ≫
          (ExactUniversalClassificationTwoCell.associatorIso
            (W := W) A f.actualLift g.actualLift h.actualLift).hom ≫
          𝟙 _
    exact
      ((Category.id_comp _).trans (Category.comp_id _)).symm

/-- The stored actual-lift projection is a global strict pseudofunctor. -/
noncomputable def exactLiftableActualLiftStrictPseudofunctor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    StrictPseudofunctor
      (ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel)
      (ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :=
  StrictPseudofunctor.mk'
    (exactLiftableActualLiftStrictCore (W := W) A)

@[simp] theorem exactLiftableActualLiftStrictPseudofunctor_obj
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).obj X =
      CanonicalExactUniversalObject (W := W) A X :=
  rfl

@[simp] theorem exactLiftableActualLiftStrictPseudofunctor_obj_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ((exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).obj X).label =
      X.label :=
  rfl

@[simp] theorem exactLiftableActualLiftStrictPseudofunctor_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    (exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).map f =
      f.actualLift :=
  rfl

@[simp] theorem exactLiftableActualLiftStrictPseudofunctor_map₂
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    (exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).map₂ eta =
      eta :=
  rfl

@[simp] theorem exactLiftableActualLiftStrictPseudofunctor_map_id
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).map (𝟙 X) =
      𝟙 (CanonicalExactUniversalObject (W := W) A X) :=
  rfl

@[simp] theorem exactLiftableActualLiftStrictPseudofunctor_map_comp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y)
    (g : Y ⟶ Z) :
    (exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).map (f ≫ g) =
      (exactLiftableActualLiftStrictPseudofunctor
        (W := W) A).map f ≫
      (exactLiftableActualLiftStrictPseudofunctor
        (W := W) A).map g :=
  rfl

/-!
## Boundary after v5.42

Closed:

* the v5.41 exact-liftable bicategory has a canonical global projection to the
  v5.23 exact-universal classification bicategory;
* the object map is the canonical v5.36 exact-universal representative;
* the 1-cell map is exactly the stored v5.40 actual lift;
* the 2-cell map is definitionally identity;
* identity and composition are preserved definitionally;
* hence the global projection is a genuine Mathlib `StrictPseudofunctor`.

The next theorem unit can study its local categorical properties.  Since the
2-cell map is identity, local faithfulness/fullness is immediate on fixed
actual-lift one-cells.  Essential surjectivity on target hom categories is the
substantive question: it amounts to deciding which exact-universal
classification one-cells admit the prescribed raw witness needed to re-enter
the exact-liftable actual-lift presentation.
-/

#print axioms exactLiftableActualLiftStrictCore
#print axioms exactLiftableActualLiftStrictPseudofunctor
#print axioms exactLiftableActualLiftStrictPseudofunctor_map
#print axioms exactLiftableActualLiftStrictPseudofunctor_map₂

end

end KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
