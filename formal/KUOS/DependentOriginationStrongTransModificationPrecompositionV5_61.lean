import KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionHorizontalWhiskeringV5_60

namespace KUOS.DependentOriginationStrongTransModificationPrecompositionV5_61

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Precomposition of StrongTrans and modifications v5.61

The pinned Mathlib functor-bicategory API supplies vertical composition and
whiskering *inside a fixed functor bicategory*, but not the tricategorical
operation that precomposes a StrongTrans by a pseudofunctor with a different
source bicategory.

v5.53 proved the special case needed for the unit of the actual-lift
biequivalence.  This file extracts the fully general operation while keeping
all native mapId/mapComp comparisons of the precomposing pseudofunctor.

It then lifts the same operation to modifications and to invertible
modifications.  This is one of the two modification-level horizontal
whiskerings needed before a swallowtail equation can be stated.
-/

namespace StrongTransPrecomposition

universe uD vD wD uB vB wB uC vC wC

variable {D : Type uD} [Bicategory.{wD, vD} D]
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

variable (K : Pseudofunctor D B)
variable {F G : Pseudofunctor B C}
variable (alpha : Pseudofunctor.StrongTrans F G)

/-! Explicit native hom categories.

Although Mathlib exposes these as scoped instances, the universe of
modifications is not an output parameter of `Category`.  At the generic
three-bicategory boundary below, asking typeclass search to reconstruct that
universe from an `Iso` header is unstable.  Bind the already existing
Mathlib hom categories directly, as in the v5.57 certificate. -/

local instance sourceStrongTransHomCategory
    {P Q : Pseudofunctor B C} :
    Category (Pseudofunctor.StrongTrans P Q) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := C) (F := P) (G := Q)

local instance precomposedStrongTransHomCategory
    {P Q : Pseudofunctor D C} :
    Category (Pseudofunctor.StrongTrans P Q) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := D) (C := C) (F := P) (G := Q)

/-- Identity coherence for arbitrary precomposition.  The proof first moves
K.mapId through alpha by alpha's 2-cell naturality and only then applies the
original StrongTrans identity law. -/
theorem naturality_id (a : D) :
    (alpha.naturality (K.map (𝟙 a))).hom ≫
        alpha.app (K.obj a) ◁
          ((Pseudofunctor.comp K G).mapId a).hom =
      ((Pseudofunctor.comp K F).mapId a).hom ▷ alpha.app (K.obj a) ≫
        (λ_ (alpha.app (K.obj a))).hom ≫
        (ρ_ (alpha.app (K.obj a))).inv := by
  change
    (alpha.naturality (K.map (𝟙 a))).hom ≫
        alpha.app (K.obj a) ◁
          (G.map₂ (K.mapId a).hom ≫ (G.mapId (K.obj a)).hom) =
      (F.map₂ (K.mapId a).hom ≫ (F.mapId (K.obj a)).hom) ▷
          alpha.app (K.obj a) ≫
        (λ_ (alpha.app (K.obj a))).hom ≫
        (ρ_ (alpha.app (K.obj a))).inv
  rw [Bicategory.whiskerLeft_comp, ← Category.assoc,
    ← alpha.naturality_naturality (K.mapId a).hom, Category.assoc,
    alpha.naturality_id, Bicategory.comp_whiskerRight]
  simp only [Category.assoc]

/-- Composition coherence for arbitrary precomposition.  K.mapComp remains
visible and is transported by alpha.naturality_naturality before the original
composition law is used. -/
theorem naturality_comp {a b c : D} (f : a ⟶ b) (g : b ⟶ c) :
    (alpha.naturality (K.map (f ≫ g))).hom ≫
        alpha.app (K.obj a) ◁
          ((Pseudofunctor.comp K G).mapComp f g).hom =
      ((Pseudofunctor.comp K F).mapComp f g).hom ▷
          alpha.app (K.obj c) ≫
        (α_ ((Pseudofunctor.comp K F).map f)
          ((Pseudofunctor.comp K F).map g)
          (alpha.app (K.obj c))).hom ≫
        (Pseudofunctor.comp K F).map f ◁
          (alpha.naturality (K.map g)).hom ≫
        (α_ ((Pseudofunctor.comp K F).map f)
          (alpha.app (K.obj b))
          ((Pseudofunctor.comp K G).map g)).inv ≫
        (alpha.naturality (K.map f)).hom ▷
          (Pseudofunctor.comp K G).map g ≫
        (α_ (alpha.app (K.obj a))
          ((Pseudofunctor.comp K G).map f)
          ((Pseudofunctor.comp K G).map g)).hom := by
  change
    (alpha.naturality (K.map (f ≫ g))).hom ≫
        alpha.app (K.obj a) ◁
          (G.map₂ (K.mapComp f g).hom ≫
            (G.mapComp (K.map f) (K.map g)).hom) =
      (F.map₂ (K.mapComp f g).hom ≫
          (F.mapComp (K.map f) (K.map g)).hom) ▷
          alpha.app (K.obj c) ≫
        (α_ (F.map (K.map f)) (F.map (K.map g))
          (alpha.app (K.obj c))).hom ≫
        F.map (K.map f) ◁ (alpha.naturality (K.map g)).hom ≫
        (α_ (F.map (K.map f)) (alpha.app (K.obj b))
          (G.map (K.map g))).inv ≫
        (alpha.naturality (K.map f)).hom ▷ G.map (K.map g) ≫
        (α_ (alpha.app (K.obj a))
          (G.map (K.map f)) (G.map (K.map g))).hom
  rw [Bicategory.whiskerLeft_comp, ← Category.assoc,
    ← alpha.naturality_naturality (K.mapComp f g).hom, Category.assoc,
    alpha.naturality_comp, Bicategory.comp_whiskerRight]
  simp only [Category.assoc]

/-- Precompose an arbitrary StrongTrans by an arbitrary pseudofunctor. -/
def strongTrans :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp K F)
      (Pseudofunctor.comp K G) where
  app a := alpha.app (K.obj a)
  naturality f := alpha.naturality (K.map f)
  naturality_naturality theta :=
    alpha.naturality_naturality (K.map₂ theta)
  naturality_id a := naturality_id K alpha a
  naturality_comp f g := naturality_comp K alpha f g

@[simp] theorem strongTrans_app (a : D) :
    (strongTrans K alpha).app a = alpha.app (K.obj a) :=
  rfl

@[simp] theorem strongTrans_naturality {a b : D} (f : a ⟶ b) :
    (strongTrans K alpha).naturality f =
      alpha.naturality (K.map f) :=
  rfl

/-- Precompose a modification.  Once the two boundary StrongTrans values have
been precomposed, modification naturality is exactly the old naturality at
K.map f. -/
def modification
    {alpha beta : Pseudofunctor.StrongTrans F G}
    (Gamma : Pseudofunctor.StrongTrans.Modification alpha beta) :
    Pseudofunctor.StrongTrans.Modification
      (strongTrans K alpha)
      (strongTrans K beta) where
  app a := Gamma.app (K.obj a)
  naturality f := Gamma.naturality (K.map f)

@[simp] theorem modification_app
    {alpha beta : Pseudofunctor.StrongTrans F G}
    (Gamma : Pseudofunctor.StrongTrans.Modification alpha beta)
    (a : D) :
    (modification K Gamma).app a = Gamma.app (K.obj a) :=
  rfl

/-- Precomposition preserves an invertible modification.

The hom-category instances are written explicitly.  This avoids asking
typeclass search to reconstruct the 2-morphism universe of a StrongTrans hom
category from the surrounding Iso notation. -/
def iso
    {alpha beta : Pseudofunctor.StrongTrans F G}
    (e :
      @CategoryTheory.Iso
        (Pseudofunctor.StrongTrans F G)
        (Pseudofunctor.StrongTrans.homCategory
          (B := B) (C := C) (F := F) (G := G))
        alpha beta) :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.comp K F)
        (Pseudofunctor.comp K G))
      (Pseudofunctor.StrongTrans.homCategory
        (B := D) (C := C)
        (F := Pseudofunctor.comp K F)
        (G := Pseudofunctor.comp K G))
      (strongTrans K alpha)
      (strongTrans K beta) where
  hom.as := modification K e.hom.as
  inv.as := modification K e.inv.as
  hom_inv_id := by
    ext a
    change
      e.hom.as.app (K.obj a) ≫ e.inv.as.app (K.obj a) =
        𝟙 (alpha.app (K.obj a))
    simpa using congrArg
      (fun m => m.as.app (K.obj a))
      e.hom_inv_id
  inv_hom_id := by
    ext a
    change
      e.inv.as.app (K.obj a) ≫ e.hom.as.app (K.obj a) =
        𝟙 (beta.app (K.obj a))
    simpa using congrArg
      (fun m => m.as.app (K.obj a))
      e.inv_hom_id

/-- Precomposition of the identity StrongTrans is definitionally the native
identity StrongTrans of the composite pseudofunctor.  The non-strict
comparators belong to the pseudofunctor itself and its mapped 1-cells agree
definitionally on both sides. -/
@[simp] theorem strongTrans_id :
    strongTrans K (Pseudofunctor.StrongTrans.id F) =
      Pseudofunctor.StrongTrans.id (Pseudofunctor.comp K F) :=
  rfl

/-- Precompose an entire functor-bicategory triangulator. -/
def triangulator
    (T : KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.Generic.FunctorBicategoryTriangulator F) :
    KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.Generic.FunctorBicategoryTriangulator
      (Pseudofunctor.comp K F) where
  triangle := strongTrans K T.triangle
  contraction := by
    simpa only [strongTrans_id] using (iso K T.contraction)

@[simp] theorem triangulator_triangle
    (T : KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.Generic.FunctorBicategoryTriangulator F) :
    (triangulator K T).triangle = strongTrans K T.triangle :=
  rfl

end StrongTransPrecomposition

/-!
## Boundary after v5.61

Precomposition is now available uniformly at all levels currently represented
by Mathlib:

* StrongTrans;
* modification;
* invertible modification;
* the triangulator package used by KuuOS.

The construction keeps K.mapId and K.mapComp and proves the new StrongTrans
laws from the old naturality_naturality/identity/composition laws.

The complementary postcomposition operation is still separate.  It requires
mapping the naturality square through a non-strict pseudofunctor and therefore
uses the mapped-square machinery of v5.54.
-/

#print axioms StrongTransPrecomposition.naturality_id
#print axioms StrongTransPrecomposition.naturality_comp
#print axioms StrongTransPrecomposition.strongTrans
#print axioms StrongTransPrecomposition.modification
#print axioms StrongTransPrecomposition.iso
#print axioms StrongTransPrecomposition.triangulator

end

end KUOS.DependentOriginationStrongTransModificationPrecompositionV5_61
