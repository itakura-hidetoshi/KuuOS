import KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116
import Mathlib.CategoryTheory.Functor.FullyFaithful

namespace KUOS.DependentOriginationCoherentBiadjunctionMateForgetfulHorizontalWhiskeringV5_117

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionInverseModificationMatesV5_115.Generic

set_option autoImplicit false
noncomputable section

/-!
# F20 / v5.117: forgetful functors and horizontal whiskering of original mates

F19 is an actual equivalence of ordinary categories of CHOSEN
right-adjoint presentations of the same original strong transformations.
This file checks that the F19 equivalence coheres with forgetting the
chosen adjunct information, not only with abstract hom equivalences.

The left chosen-presentation category forgets to the NATIVE mathlib
category of strong transformations and their modifications. This
functor is fully faithful: no arbitrary modification is lost. On
the right-opposite side the corresponding forgetful functor uses the
original F18 inverse mate, and the two forgetful routes agree on
objects and arrows by a native `NatIso`.

The horizontal extension is checked against pinned mathlib:
for any original adjunct family, arbitrary strong modification, and
independently chosen *fixed* adjunction, the mate of left/right
whiskering is the corresponding right/left whiskering of the SAME
original right-mate modification component. These are exact
non-strict bicategorical equations, not a claim of a global horizontal
functor on arbitrary new adjunction families or of biequivalence of B,C.

All F/G, η/ε, mapId/mapComp, objectwise equivalences and triangulators
remain unchanged; the right transformations remain LAX.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Forget the chosen adjunctions but retain the original full strong
transformation and each original (possibly noninvertible) modification.
The target is mathlib's actual StrongTrans hom category. -/
def forgetOriginalStrong :
    LeftMatePresentation F G ⥤ Pseudofunctor.StrongTrans F G where
  obj a := a.core.left
  map {_ _} f := Pseudofunctor.StrongTrans.Hom.of f
  map_id _ := rfl
  map_comp _ _ := rfl

/-- No modification is lost when the selected adjunction presentation
is forgotten; the inverse on 2-Homs is the underlying modification. -/
def forgetOriginalStrongFullyFaithful :
    (forgetOriginalStrong F G).FullyFaithful where
  preimage {_ _} f := f.as
  map_preimage {_ _} f := by
    cases f
    rfl
  preimage_map {_ _} f := rfl

/-- Forget a RIGHT-opposite presentation via F18 inverse mates,
recovering the same ORIGINAL strong transformation. -/
def forgetRightThroughMate :
    RightMateOppPresentation F G ⥤ Pseudofunctor.StrongTrans F G :=
  leftMateFunctor F G ⋙ forgetOriginalStrong F G

/-- The right-side forgetting is lossless as well: every old strong
modification is recovered by the F17 right-mate inverse. -/
def forgetRightThroughMateFullyFaithful :
    (forgetRightThroughMate F G).FullyFaithful where
  preimage {a b} f :=
    rightModification a.core.datum b.core.datum f.as
  map_preimage {a b} f := by
    change
      Pseudofunctor.StrongTrans.Hom.of
        (leftModification a.core.datum b.core.datum
          (rightModification a.core.datum b.core.datum f.as)) = f
    rw [leftModification_rightModification]
    cases f
    rfl
  preimage_map {a b} m := by
    change
      rightModification a.core.datum b.core.datum
        (leftModification a.core.datum b.core.datum m) = m
    exact rightModification_leftModification a.core.datum b.core.datum m

/-- Forgetting after F19 right-mate transport is the SAME strong
modification as forgetting directly on the left. -/
theorem forgetOriginalStrong_rightMate_map
    {a b : LeftMatePresentation F G} (m : a ⟶ b) :
    (forgetRightThroughMate F G).map ((rightMateFunctor F G).map m) =
      (forgetOriginalStrong F G).map m := by
  change
    Pseudofunctor.StrongTrans.Hom.of
      (leftModification a.core.datum b.core.datum
        (rightModification a.core.datum b.core.datum m)) =
      Pseudofunctor.StrongTrans.Hom.of m
  rw [leftModification_rightModification]

/-- A real native natural isomorphism comparing BOTH paths to the
original strong-transformation category: no reselected adjunctions. -/
def originalForgetfulComparison :
    (rightMateFunctor F G ⋙ forgetRightThroughMate F G) ≅
      forgetOriginalStrong F G :=
  NatIso.ofComponents
    (fun a => Iso.refl a.core.left)
    (by
      intro a b m
      change
        (forgetRightThroughMate F G).map ((rightMateFunctor F G).map m) ≫
          𝟙 (b.core.left) =
        𝟙 (a.core.left) ≫ (forgetOriginalStrong F G).map m
      rw [Category.comp_id, Category.id_comp,
        forgetOriginalStrong_rightMate_map F G m])

/-- All components of the forgetful comparison are literally the
identity of the original (unmodified) strong transformation. -/
theorem originalForgetfulComparison_app
    (a : LeftMatePresentation F G) :
    (originalForgetfulComparison F G).app a = Iso.refl a.core.left := rfl

/-! ## Horizontal whiskering, with the SAME original right mate cells. -/

variable {F G}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- Left whiskering an arbitrary original strong modification by an
independently fixed adjunction becomes RIGHT whiskering the unchanged
right-mate modification component. Every 2-cell retains its direction. -/
theorem rightModification_whiskerLeft
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B) {e : C}
    {u : e ⟶ F.obj X} {v : F.obj X ⟶ e}
    (fixed : Bicategory.Adjunction u v) :
    Bicategory.conjugateEquiv
        (fixed.comp (dθ.adj X))
        (fixed.comp (dσ.adj X))
        (u ◁ Γ.app X) =
      (rightModification dσ dθ Γ).app X ▷ v := by
  exact Bicategory.conjugateEquiv_whiskerLeft
    fixed (dθ.adj X) (dσ.adj X) (Γ.app X)

/-- Right whiskering an arbitrary original strong modification by a
fixed adjunction becomes LEFT whiskering the unchanged right mate
component, with the actual reversed order of composite adjoints. -/
theorem rightModification_whiskerRight
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (X : B) {e : C}
    {u : G.obj X ⟶ e} {v : e ⟶ G.obj X}
    (fixed : Bicategory.Adjunction u v) :
    Bicategory.conjugateEquiv
        ((dθ.adj X).comp fixed)
        ((dσ.adj X).comp fixed)
        (Γ.app X ▷ u) =
      v ◁ (rightModification dσ dθ Γ).app X := by
  exact Bicategory.conjugateEquiv_whiskerRight
    (dθ.adj X) (dσ.adj X) fixed (Γ.app X)

#print axioms forgetOriginalStrong
#print axioms forgetOriginalStrongFullyFaithful
#print axioms forgetRightThroughMate
#print axioms forgetRightThroughMateFullyFaithful
#print axioms forgetOriginalStrong_rightMate_map
#print axioms originalForgetfulComparison
#print axioms originalForgetfulComparison_app
#print axioms rightModification_whiskerLeft
#print axioms rightModification_whiskerRight

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionMateForgetfulHorizontalWhiskeringV5_117
