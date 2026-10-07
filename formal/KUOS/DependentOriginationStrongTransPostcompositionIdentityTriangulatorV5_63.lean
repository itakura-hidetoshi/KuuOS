import KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62

namespace KUOS.DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62
open KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62.StrongTransPostcomposition
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.Generic

set_option autoImplicit false

noncomputable section

/-!
# Postcomposition identity comparison and triangulator v5.63

v5.62 postcomposes arbitrary StrongTrans values, modifications, and invertible
modifications by a non-strict pseudofunctor H.

The remaining obstruction to postcomposing a triangulator is the identity
endpoint.  Postcomposing the identity StrongTrans of F has component

  H.map (𝟙 (F.obj a)),

whereas the native identity StrongTrans of F ; H has component

  𝟙 (H.obj (F.obj a)).

These are not definitionally equal for a non-strict pseudofunctor.  The
canonical comparison is exactly H.mapId at F.obj a.

This file constructs that invertible modification and then composes it with
v5.62's image of a triangulator contraction.  No strictification and no new
choice is introduced.
-/

namespace StrongTransPostcomposition

universe uB vB wB uC vC wC uD vD wD

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {D : Type uD} [Bicategory.{wD, vD} D]

variable (F : Pseudofunctor B C)
variable (H : Pseudofunctor C D)

local instance sourceStrongTransHomCategory
    {P Q : Pseudofunctor B C} :
    Category (Pseudofunctor.StrongTrans P Q) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := C) (F := P) (G := Q)

local instance postcomposedStrongTransHomCategory
    {P Q : Pseudofunctor B D} :
    Category (Pseudofunctor.StrongTrans P Q) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := D) (F := P) (G := Q)

/-- Naturality of the canonical H.mapId comparison between the postcomposed
identity StrongTrans and the native identity StrongTrans. -/
theorem identityNaturality {a b : B} (f : a ⟶ b) :
    (Pseudofunctor.comp F H).map f ◁
          (H.mapId (F.obj b)).hom ≫
        ((Pseudofunctor.StrongTrans.id
          (Pseudofunctor.comp F H)).naturality f).hom =
      (naturalityIso H (Pseudofunctor.StrongTrans.id F) f).hom ≫
        (H.mapId (F.obj a)).hom ▷
          (Pseudofunctor.comp F H).map f := by
  change
    H.map (F.map f) ◁ (H.mapId (F.obj b)).hom ≫
        (ρ_ (H.map (F.map f))).hom ≫
        (λ_ (H.map (F.map f))).inv =
      (H.mapComp (F.map f) (𝟙 (F.obj b))).inv ≫
        H.map₂ ((ρ_ (F.map f)).hom ≫ (λ_ (F.map f)).inv) ≫
        (H.mapComp (𝟙 (F.obj a)) (F.map f)).hom ≫
        (H.mapId (F.obj a)).hom ▷ H.map (F.map f)
  rw [H.mapComp_id_right_inv, PrelaxFunctor.map₂_comp,
    H.mapComp_id_left_hom]
  simp only [Category.assoc]
  rw [H.map₂_inv_hom_assoc (ρ_ (F.map f)),
    H.map₂_inv_hom_assoc (λ_ (F.map f)),
    Bicategory.inv_hom_whiskerRight, Category.id_comp]

/-- The postcomposed identity StrongTrans is canonically isomorphic to the
native identity StrongTrans of the composite pseudofunctor. -/
def identityIso :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.comp F H)
        (Pseudofunctor.comp F H))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := D)
        (F := Pseudofunctor.comp F H)
        (G := Pseudofunctor.comp F H))
      (strongTrans H (Pseudofunctor.StrongTrans.id F))
      (Pseudofunctor.StrongTrans.id (Pseudofunctor.comp F H)) :=
  Pseudofunctor.StrongTrans.isoMk
    (fun a => H.mapId (F.obj a))
    (fun f => identityNaturality F H f)

/-- Postcompose an entire triangulator.  The contraction is the image of the
old contraction followed by the canonical H.mapId identity comparison. -/
def triangulator
    (T : FunctorBicategoryTriangulator F) :
    FunctorBicategoryTriangulator (Pseudofunctor.comp F H) where
  triangle := strongTrans H T.triangle
  contraction :=
    (iso H T.contraction) ≪≫ identityIso F H

@[simp] theorem triangulator_triangle
    (T : FunctorBicategoryTriangulator F) :
    (triangulator F H T).triangle =
      strongTrans H T.triangle :=
  rfl

@[simp] theorem triangulator_contraction
    (T : FunctorBicategoryTriangulator F) :
    (triangulator F H T).contraction =
      (iso H T.contraction) ≪≫ identityIso F H :=
  rfl

@[simp] theorem identityIso_hom_app (a : B) :
    (identityIso F H).hom.as.app a =
      (H.mapId (F.obj a)).hom :=
  rfl

@[simp] theorem identityIso_inv_app (a : B) :
    (identityIso F H).inv.as.app a =
      (H.mapId (F.obj a)).inv :=
  rfl

end StrongTransPostcomposition

/-!
## Boundary after v5.63

The postcomposition interface now acts on the full triangulator package:

  triangle
    | postcompose H
    v
  postcomposed triangle
    -- image of old contraction -->
  postcompose(id_F)
    -- H.mapId -->
  id_(F ; H).

Together with v5.61, both precomposition and postcomposition now preserve
invertible triangle contractions.  The next step can therefore form the
modification-level horizontal pastes needed to state the swallowtail
equations themselves.
-/

#print axioms StrongTransPostcomposition.identityNaturality
#print axioms StrongTransPostcomposition.identityIso
#print axioms StrongTransPostcomposition.triangulator
#print axioms StrongTransPostcomposition.identityIso_hom_app
#print axioms StrongTransPostcomposition.identityIso_inv_app

end

end KUOS.DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63
