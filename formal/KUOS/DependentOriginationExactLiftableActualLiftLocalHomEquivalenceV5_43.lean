import KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib

namespace KUOS.DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42

set_option autoImplicit false

noncomputable section

/-!
# Local hom equivalence for the actual-lift projection v5.43

v5.42 packages the stored actual-lift projection as a global strict
pseudofunctor from the exact-liftable classification bicategory to the
exact-universal classification bicategory.

On a fixed pair of source objects X,Y the corresponding hom functor is much
stronger than merely full and faithful:

* every source 2-cell is already a target v5.21 classification 2-cell, so the
  map on 2-cells is definitionally the identity;
* every target exact-universal classification one-cell k between the canonical
  representatives supplies its own raw witness
      (k.label_eq, k.map.raw)
  and can therefore be re-packaged as an actual-lift one-cell with
  actualLift = k.

Thus the hom functor is a Mathlib equivalence for every fixed pair X,Y.  No
choice, lifting theorem, or target-side essential-uniqueness argument is needed.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- Repackage a target exact-universal classification one-cell as an actual-lift
one-cell over the same canonical endpoint objects. -/
noncomputable def actualOneCellOfExactUniversalClassificationOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (k :
      ExactUniversalClassificationOneCell
        (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)
        (CanonicalExactUniversalObject (W := W) A Y)) :
    ExactLiftableClassificationActualOneCell
      (W := W) A X Y where
  raw :=
    { label_eq := k.label_eq
      map := k.map.raw }
  actualLift := k
  raw_eq := rfl

@[simp] theorem actualOneCellOfExactUniversalClassificationOneCell_actualLift
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (k :
      ExactUniversalClassificationOneCell
        (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)
        (CanonicalExactUniversalObject (W := W) A Y)) :
    (actualOneCellOfExactUniversalClassificationOneCell
      (W := W) A k).actualLift = k :=
  rfl

@[simp] theorem actualOneCellOfExactUniversalClassificationOneCell_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (k :
      ExactUniversalClassificationOneCell
        (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)
        (CanonicalExactUniversalObject (W := W) A Y)) :
    (actualOneCellOfExactUniversalClassificationOneCell
      (W := W) A k).map = k.map.raw :=
  rfl

/-! ## Full and faithful -/

/-- The actual-lift hom functor is faithful because its action on 2-cells is
definitionally the identity. -/
instance actualLiftHomFunctor_faithful
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftHomFunctor (W := W) A X Y).Faithful where
  map_injective {f g} := by
    intro eta theta h
    exact h

/-- The actual-lift hom functor is full because every target 2-cell is already
a source 2-cell with the same endpoints. -/
instance actualLiftHomFunctor_full
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftHomFunctor (W := W) A X Y).Full where
  map_surjective {f g} eta :=
    ⟨eta, rfl⟩

/-! ## Essential surjectivity on 1-cells -/

/-- Every exact-universal classification one-cell between the canonical
representatives is literally the stored actual lift of a source one-cell. -/
instance actualLiftHomFunctor_essSurj
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftHomFunctor (W := W) A X Y).EssSurj where
  mem_essImage k := by
    let f :=
      actualOneCellOfExactUniversalClassificationOneCell
        (W := W) A (X := X) (Y := Y) k
    refine ⟨f, ⟨?_⟩⟩
    change f.actualLift ≅ k
    exact Iso.refl k

/-! ## Native Mathlib equivalence interface -/

/-- The actual-lift hom functor is an equivalence on every fixed pair of
exact-liftable classification objects. -/
instance actualLiftHomFunctor_isEquivalence
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftHomFunctor (W := W) A X Y).IsEquivalence where
  essSurj :=
    actualLiftHomFunctor_essSurj
      (W := W) A X Y

/-- Data-bearing fully faithful structure for the actual-lift hom functor. -/
def actualLiftHomFullyFaithful
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftHomFunctor (W := W) A X Y).FullyFaithful := by
  letI : (actualLiftHomFunctor (W := W) A X Y).Faithful :=
    actualLiftHomFunctor_faithful (W := W) A X Y
  letI : (actualLiftHomFunctor (W := W) A X Y).Full :=
    actualLiftHomFunctor_full (W := W) A X Y
  exact Functor.FullyFaithful.ofFullyFaithful _

/-- The local equivalence induced by the actual-lift projection. -/
noncomputable def actualLiftHomEquivalence
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftableClassificationActualOneCell
        (W := W) A X Y ≌
      ExactUniversalClassificationOneCell
        (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)
        (CanonicalExactUniversalObject (W := W) A Y) := by
  letI : (actualLiftHomFunctor (W := W) A X Y).IsEquivalence :=
    actualLiftHomFunctor_isEquivalence (W := W) A X Y
  exact (actualLiftHomFunctor (W := W) A X Y).asEquivalence

@[simp] theorem actualLiftHomEquivalence_functor
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftHomEquivalence (W := W) A X Y).functor =
      actualLiftHomFunctor (W := W) A X Y :=
  rfl

/-! ## Identification with the global strict pseudofunctor -/

/-- The hom functor of the v5.42 strict pseudofunctor is definitionally the
v5.41 actual-lift hom functor. -/
theorem exactLiftableActualLiftStrictPseudofunctor_mapFunctor_eq
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).mapFunctor X Y =
      actualLiftHomFunctor (W := W) A X Y := by
  apply CategoryTheory.Functor.hext
  · intro f
    rfl
  · intro f g eta
    exact heq_of_eq rfl

/-- Consequently the global strict pseudofunctor is locally an equivalence on
every hom category. -/
instance exactLiftableActualLiftStrictPseudofunctor_mapFunctor_isEquivalence
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ((exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).mapFunctor X Y).IsEquivalence := by
  rw [exactLiftableActualLiftStrictPseudofunctor_mapFunctor_eq
    (W := W) A X Y]
  exact actualLiftHomFunctor_isEquivalence (W := W) A X Y

/-!
## Boundary after v5.43

Closed:

* every local hom functor of the v5.42 strict pseudofunctor is faithful;
* every local hom functor is full;
* every target exact-universal classification one-cell between canonical
  objects is in the essential image;
* hence every local hom functor is a Mathlib equivalence.

This is stronger than the v5.39 local full/faithful statement: v5.43 includes
essential surjectivity on 1-cells because the actual-lift presentation stores
the target one-cell itself.

The remaining genuinely global issue is object-level essential surjectivity of

  X |-> CanonicalExactUniversalObject X

onto the v5.23 exact-universal classification bicategory, up to the appropriate
bicategorical equivalence.  That should be attacked next using
ExactUniversalClassificationObject.toExactLiftable together with the existing
fixed-raw coherent uniqueness/universal-target machinery.
-/

#print axioms actualOneCellOfExactUniversalClassificationOneCell
#print axioms actualLiftHomFullyFaithful
#print axioms actualLiftHomEquivalence
#print axioms exactLiftableActualLiftStrictPseudofunctor_mapFunctor_eq

end

end KUOS.DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43
