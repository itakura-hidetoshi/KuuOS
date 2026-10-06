import KUOS.DependentOriginationExactLiftableBundledOneCellV5_38
import KUOS.DependentOriginationExactClassificationHomFunctorV5_22
import Mathlib

namespace KUOS.DependentOriginationExactLiftableLocalHomCategoryV5_39

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37
open KUOS.DependentOriginationExactLiftableBundledOneCellV5_38

set_option autoImplicit false

noncomputable section

/-!
# Exact-liftable local hom categories v5.39

v5.38 bundles exactly the admissible label-preserving raw StrongTranses between
exact-liftable classification objects.  Each such bundled one-cell has a chosen
exact-universal classification lift.

For fixed exact-liftable objects X and Y, this file defines a 2-cell between
bundled one-cells f and g to be exactly a v5.21/v5.22 classification 2-cell
between their chosen exact-universal lifts.

This gives a genuine hom category on the bundled exact-liftable one-cells by
reusing the already-validated v5.22 hom category.  It also gives a canonical
functor from the new hom category to the exact-universal classification hom
category.  On morphisms that functor is definitionally the identity.

This is a local statement only.  Horizontal composition of 2-cells and the
coherence needed for a global bicategory still require comparison between:

  chosenLift (f ; g)

and

  chosenLift f ; chosenLift g.

v5.39 does not assume those chosen lifts are definitionally equal.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Canonical exact-universal representative attached to an exact-liftable
classification object. -/
abbrev CanonicalExactUniversalObject
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.canonicalExactUniversalClassificationObjectOfExactLiftable
    (W := W) A X

/-- Canonical exact-universal lift of a bundled exact-liftable one-cell. -/
abbrev canonicalLift
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :=
  KUOS.DependentOriginationExactLiftableBundledOneCellV5_38.exactUniversalClassificationOneCellOfExactLiftableOneCell
    (W := W) A f

/-- 2-cells between bundled exact-liftable one-cells are exactly classification
2-cells between their chosen exact-universal lifts. -/
abbrev ExactLiftableClassificationTwoCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f g :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :=
  KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21.ExactUniversalClassificationTwoCell
    (W := W) A
    (canonicalLift (W := W) A f)
    (canonicalLift (W := W) A g)

/-- For fixed exact-liftable objects X and Y, bundled liftable one-cells form a
genuine category.  The categorical operations are inherited from the v5.22
hom category of their canonical exact-universal lifts. -/
noncomputable instance exactLiftableClassificationOneCellHomCategory
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    Category
      (ExactLiftableClassificationOneCell
        (W := W) A X Y) where
  Hom f g :=
    ExactLiftableClassificationTwoCell
      (W := W) A f g
  id f :=
    KUOS.DependentOriginationExactClassificationHomFunctorV5_22.ExactUniversalClassificationTwoCell.id
      (W := W) A
      (canonicalLift (W := W) A f)
  comp eta theta :=
    KUOS.DependentOriginationExactClassificationHomFunctorV5_22.ExactUniversalClassificationTwoCell.vcomp
      (W := W) A eta theta
  id_comp := by
    intro f g eta
    exact Category.id_comp eta
  comp_id := by
    intro f g eta
    exact Category.comp_id eta
  assoc := by
    intro f g h i eta theta iota
    exact Category.assoc eta theta iota

/-- The canonical lift on objects and identity-on-2-cells map define a functor
from the v5.39 local hom category to the existing exact-universal
classification hom category. -/
noncomputable def canonicalLiftHomFunctor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftableClassificationOneCell
        (W := W) A X Y ⥤
      KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21.ExactUniversalClassificationOneCell
        (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)
        (CanonicalExactUniversalObject (W := W) A Y) where
  obj f :=
    canonicalLift (W := W) A f
  map eta :=
    eta
  map_id := by
    intro f
    rfl
  map_comp := by
    intro f g h eta theta
    rfl

@[simp] theorem canonicalLiftHomFunctor_obj
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    (canonicalLiftHomFunctor
      (W := W) A X Y).obj f =
      canonicalLift (W := W) A f :=
  rfl

@[simp] theorem canonicalLiftHomFunctor_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    {f g :
      ExactLiftableClassificationOneCell
        (W := W) A X Y}
    (eta : f ⟶ g) :
    (canonicalLiftHomFunctor
      (W := W) A X Y).map eta =
      eta :=
  rfl

/-- The canonical local lift functor is faithful.  Its map on 2-cells is
definitionally the identity. -/
theorem canonicalLiftHomFunctor_faithful
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    Function.Injective
      (fun {f g :
          ExactLiftableClassificationOneCell
            (W := W) A X Y}
        (eta : f ⟶ g) =>
          (canonicalLiftHomFunctor
            (W := W) A X Y).map eta) := by
  intro f g eta theta h
  exact h

/-- The canonical local lift functor is full on each fixed pair of bundled
one-cells because the source and target hom types are definitionally the same
classification 2-cell type. -/
theorem canonicalLiftHomFunctor_surjective_on_hom
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (f g :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    Function.Surjective
      (fun eta : f ⟶ g =>
        (canonicalLiftHomFunctor
          (W := W) A X Y).map eta) := by
  intro eta
  exact ⟨eta, rfl⟩

/-- The canonical lift functor preserves the prescribed raw StrongTrans at the
object level. -/
@[simp] theorem canonicalLiftHomFunctor_obj_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    ((canonicalLiftHomFunctor
      (W := W) A X Y).obj f).map.raw =
      f.map :=
  KUOS.DependentOriginationExactLiftableBundledOneCellV5_38.exactUniversalClassificationOneCellOfExactLiftableOneCell_raw
    (W := W) A f

/-!
## Boundary after v5.39

Closed locally:

* bundled exact-liftable one-cells between fixed objects form a hom category;
* 2-cells are exactly the validated v5.21 classification 2-cells between
  canonical exact-universal lifts;
* the canonical lift is a functor on each hom category;
* its action on 2-cells is definitionally identity, hence locally full and
  faithful;
* its object map preserves the prescribed raw StrongTrans exactly.

Still open globally:

* horizontal composition of these 2-cells is not yet installed;
* chosenLift(comp f g) need not be definitionally equal to
  comp(chosenLift f)(chosenLift g);
* therefore a bicategory of exact-liftable objects requires explicit
  comparison/coherence between those two lifts before associators, unitors,
  and whiskering can be transported.

The next theorem unit should construct that comparison rather than hide it
inside noncomputable choice.
-/

#print axioms canonicalLiftHomFunctor
#print axioms canonicalLiftHomFunctor_faithful
#print axioms canonicalLiftHomFunctor_surjective_on_hom
#print axioms canonicalLiftHomFunctor_obj_raw

end

end KUOS.DependentOriginationExactLiftableLocalHomCategoryV5_39
