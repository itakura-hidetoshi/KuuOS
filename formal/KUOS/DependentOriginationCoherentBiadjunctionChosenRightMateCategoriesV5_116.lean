import KUOS.DependentOriginationCoherentBiadjunctionInverseModificationMatesV5_115

namespace KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116

open CategoryTheory
open scoped CategoryTheory.Bicategory

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionInverseModificationMatesV5_115.Generic

set_option autoImplicit false
noncomputable section

/-!
# F19 / v5.116: categories of original chosen right-mate presentations

An object is an ORIGINAL pseudonatural strong transformation together
with its genuine F16 `RightMateLaxData`: the original pointwise chosen
adjunctions and the correct lax right mate. No new adjunct is selected.

Left morphisms are ALL strong modifications between the left legs.
Right-opposite morphisms are ALL lax modifications between the right
legs, with their direction deliberately reversed.

F17 and F18 then form a pair of actual ordinary category functors
between these categories: `rightMateFunctor` and `leftMateFunctor`.
These preserve identities and compositions, using the pinned mathlib
mate laws; their composite actions on all homs are mutually inverse.

This is an equivalence of the ordinary categories of CHOSEN adjunct
presentations and their already available modifications. It is not a
new biequivalence between the underlying bicategories B and C, and
it makes no arbitrary mate square invertible.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- A complete, originally chosen adjunct presentation of a single
strong transformation. Every object retains its exact right mate. -/
structure MatePresentation where
  left : Pseudofunctor.StrongTrans F G
  datum : RightMateLaxData left

/-- The left view is the ordinary category of these presentations
with ALL (not necessarily invertible) strong modifications. -/
structure LeftMatePresentation where
  core : MatePresentation F G

/-- The right-opposite view has the same chosen objectwise adjunct
presentations but opposite-direction lax modifications as morphisms. -/
structure RightMateOppPresentation where
  core : MatePresentation F G

instance leftCategory : Category (LeftMatePresentation F G) where
  Hom a b :=
    Pseudofunctor.StrongTrans.Modification a.core.left b.core.left
  id a := Pseudofunctor.StrongTrans.Modification.id a.core.left
  comp f g := Pseudofunctor.StrongTrans.Modification.vcomp f g
  id_comp f := by
    apply Pseudofunctor.StrongTrans.Modification.ext
    funext X
    exact Category.id_comp (f.app X)
  comp_id f := by
    apply Pseudofunctor.StrongTrans.Modification.ext
    funext X
    exact Category.comp_id (f.app X)
  assoc f g h := by
    apply Pseudofunctor.StrongTrans.Modification.ext
    funext X
    exact Category.assoc (f.app X) (g.app X) (h.app X)

/-- Composition in the right-opposite category genuinely REVERSES the
underlying vertical pasting of right lax modifications. -/
instance rightOppCategory : Category (RightMateOppPresentation F G) where
  Hom a b :=
    Oplax.LaxTrans.Modification b.core.datum.right a.core.datum.right
  id a := Oplax.LaxTrans.Modification.id a.core.datum.right
  comp f g := Oplax.LaxTrans.Modification.vcomp g f
  id_comp f := by
    apply Oplax.LaxTrans.Modification.ext
    funext X
    exact Category.comp_id (f.app X)
  comp_id f := by
    apply Oplax.LaxTrans.Modification.ext
    funext X
    exact Category.id_comp (f.app X)
  assoc f g h := by
    apply Oplax.LaxTrans.Modification.ext
    funext X
    exact (Category.assoc (h.app X) (g.app X) (f.app X)).symm

/-- The original F17 mate transport is an ACTUAL functor,
not just an objectwise correspondence. -/
def rightMateFunctor :
    LeftMatePresentation F G ⥤ RightMateOppPresentation F G where
  obj a := ⟨a.core⟩
  map {_ _} f := rightModification _ _ f
  map_id a := by
    exact rightModification_id a.core.datum
  map_comp {_ _ _} f g := by
    exact rightModification_vcomp _ _ _ f g

/-- F18 inverse mate transport is also an ACTUAL functor from the
right-opposite presentation category back to the left. -/
def leftMateFunctor :
    RightMateOppPresentation F G ⥤ LeftMatePresentation F G where
  obj a := ⟨a.core⟩
  map {_ _} f := leftModification _ _ f
  map_id a := by
    apply Pseudofunctor.StrongTrans.Modification.ext
    funext X
    change
      (Bicategory.conjugateEquiv
        (a.core.datum.adj X) (a.core.datum.adj X)).symm (𝟙 _) = 𝟙 _
    exact Bicategory.conjugateEquiv_symm_id (a.core.datum.adj X)
  map_comp {_ _ _} f g := by
    exact leftModification_vcomp _ _ _ f g

/-- The composite left-then-right-then-left acts IDENTICALLY on every
arbitrary left strong modification, not just original triangle cells. -/
theorem left_right_map (a b : LeftMatePresentation F G)
    (f : a ⟶ b) :
    (leftMateFunctor F G).map ((rightMateFunctor F G).map f) = f :=
  leftModification_rightModification a.core.datum b.core.datum f

/-- The composite right-then-left-then-right acts IDENTICALLY on every
arbitrary right lax modification, not just invertible examples. -/
theorem right_left_map (a b : RightMateOppPresentation F G)
    (m : a ⟶ b) :
    (rightMateFunctor F G).map ((leftMateFunctor F G).map m) = m :=
  rightModification_leftModification a.core.datum b.core.datum m

/-- Functoriality automatically gives simultaneous naturality of the
hom correspondence in both arguments, including the non-strict
compositor corrections inherited from the genuine right mates. -/
theorem rightMateFunctor_hom_naturality
    {a b c d : LeftMatePresentation F G}
    (f : a ⟶ b) (m : b ⟶ c) (g : c ⟶ d) :
    (rightMateFunctor F G).map (f ≫ m ≫ g) =
      (rightMateFunctor F G).map f ≫
        (rightMateFunctor F G).map m ≫
          (rightMateFunctor F G).map g := by
  rw [Functor.map_comp, Functor.map_comp]

#print axioms MatePresentation
#print axioms LeftMatePresentation
#print axioms RightMateOppPresentation
#print axioms leftCategory
#print axioms rightOppCategory
#print axioms rightMateFunctor
#print axioms leftMateFunctor
#print axioms left_right_map
#print axioms right_left_map
#print axioms rightMateFunctor_hom_naturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116
