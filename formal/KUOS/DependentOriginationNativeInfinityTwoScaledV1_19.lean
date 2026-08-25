import Mathlib.AlgebraicTopology.Quasicategory.Nerve
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic
import KUOS.DependentOriginationInfinityTwoYonedaV1_18

namespace KUOS.DependentOriginationNativeInfinityTwoScaledV1_19

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationInfinityTwoYonedaV1_18

universe u v w

/-!
# Native locally-quasicategorical infinity-two and scaled-simplicial classes v1.19

The pinned Mathlib revision supplies native bicategories, bicategorical 2-Yoneda,
simplicial sets, strict Segal nerves, and quasicategories, but no single bundled
`InfinityTwoCategory` class.  This file adds a KuuOS-native class with an exact,
non-vacuous meaning:

* the source is a genuine Mathlib bicategory;
* for every pair of objects, the hom-category nerve is a native Mathlib
  quasicategory;
* bicategorical composition/coherence remains the existing native bicategory
  and 2-Yoneda structure.

Thus every ordinary bicategory embeds canonically as a 2-truncated
`(infinity,2)` object whose mapping `(infinity,1)`-categories are nerves of
ordinary hom-categories.  No nontrivial higher cells above the original
2-morphisms are invented.
-/

/--
A KuuOS-native `(infinity,2)` class at the locally-quasicategorical level.

The ambient `Bicategory` instance carries objects, 1-morphisms, 2-morphisms,
associators, unitors, whiskering, pentagon, and triangle.  This class certifies
that every hom-category has been promoted to a genuine Mathlib quasicategory by
its simplicial nerve.
-/
class InfinityTwoCategory
    (B : Type u) [Bicategory.{w, v} B] : Prop where
  mapping_quasicategory :
    forall X Y : B, SSet.Quasicategory (mappingNerve X Y)

/-- Every Mathlib bicategory canonically defines the 2-truncated native class. -/
instance bicategoryInfinityTwoCategory
    (B : Type u) [Bicategory.{w, v} B] :
    InfinityTwoCategory B where
  mapping_quasicategory := by
    intro X Y
    exact mappingNerve_quasicategory X Y

/-- Re-export the mapping-quasicategory certificate from the native class. -/
theorem mapping_quasicategory
    {B : Type u} [Bicategory.{w, v} B]
    [InfinityTwoCategory B]
    (X Y : B) :
    SSet.Quasicategory (mappingNerve X Y) :=
  InfinityTwoCategory.mapping_quasicategory X Y

/-- The native class therefore gives every inner horn in every mapping object a filler. -/
theorem mapping_innerHornFilling
    {B : Type u} [Bicategory.{w, v} B]
    [InfinityTwoCategory B]
    (X Y : B)
    {n : Nat} {i : Fin (n + 1)}
    (h0 : 0 < i) (hn : i < Fin.last n)
    (sigma0 : (Lambda[n, i] : SSet) ⟶ mappingNerve X Y) :
    exists sigma : Delta[n] ⟶ mappingNerve X Y,
      sigma0 = Lambda[n, i].ι ≫ sigma := by
  letI : SSet.Quasicategory (mappingNerve X Y) :=
    InfinityTwoCategory.mapping_quasicategory X Y
  exact SSet.Quasicategory.hornFilling h0 hn sigma0

/--
A scaling on a simplicial set in the standard minimal sense needed for scaled
simplicial-set semantics: a distinguished predicate on 2-simplices containing
all degenerate 2-simplices.

The two fields correspond to the two degeneracies `[1] -> [2]`.
-/
class ScaledSimplicialSet (X : SSet) where
  thin : X.obj (Opposite.op ⦋2⦌) -> Prop
  thin_sigma_zero :
    forall x : X.obj (Opposite.op ⦋1⦌), thin (X.σ 0 x)
  thin_sigma_one :
    forall x : X.obj (Opposite.op ⦋1⦌), thin (X.σ 1 x)

namespace ScaledSimplicialSet

/-- Maximal scaling: every 2-simplex is thin.  This is always a valid scaling. -/
def maximal (X : SSet) : ScaledSimplicialSet X where
  thin := fun _ => True
  thin_sigma_zero := by
    intro x
    trivial
  thin_sigma_one := by
    intro x
    trivial

/-- Under maximal scaling every 2-simplex is thin. -/
@[simp] theorem maximal_thin
    (X : SSet) (s : X.obj (Opposite.op ⦋2⦌)) :
    (maximal X).thin s := by
  trivial

end ScaledSimplicialSet

/--
A locally scaled native `(infinity,2)` structure: each mapping quasicategory is
also supplied with an explicit scaled-simplicial-set structure.

This is deliberately called *locally* scaled.  It does not identify these
mapping scalings with a global Duskin/scaled nerve of the whole bicategory.
-/
class LocallyScaledInfinityTwoCategory
    (B : Type u) [Bicategory.{w, v} B]
    extends InfinityTwoCategory B where
  mapping_scaling :
    forall X Y : B, ScaledSimplicialSet (mappingNerve X Y)

/-- Every bicategory has a canonical locally scaled model using maximal mapping scalings. -/
instance bicategoryLocallyScaledInfinityTwoCategory
    (B : Type u) [Bicategory.{w, v} B] :
    LocallyScaledInfinityTwoCategory B where
  mapping_quasicategory := by
    intro X Y
    exact mappingNerve_quasicategory X Y
  mapping_scaling := by
    intro X Y
    exact ScaledSimplicialSet.maximal (mappingNerve X Y)

/-- The native 2-Yoneda pseudofunctor remains the composition/coherence carrier. -/
def nativeTwoYoneda
    {B : Type u} [Bicategory.{w, v} B]
    [InfinityTwoCategory B] :=
  twoYoneda (B := B)

/-!
The exact proved hierarchy is therefore

```text
Mathlib bicategory B
  -> hom-categories B(X,Y)
  -> nerves N(B(X,Y))
  -> native Mathlib quasicategories
  -> KuuOS.InfinityTwoCategory B
  -> optional explicit mapping scalings
  -> KuuOS.LocallyScaledInfinityTwoCategory B.
```

The scaled structure here is mathematically genuine but local to mapping
objects.  A global scaled/Duskin nerve is a stronger construction and is not
silently asserted by this file.
-/

end KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
