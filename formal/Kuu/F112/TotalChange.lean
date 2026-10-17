import Kuu.Incidence
import Mathlib.CategoryTheory.Grothendieck

/-!
# F112 / independent Kuu — two-dimensional source change and total descent

This re-proves the abstract categorical mechanism behind historical F112
parts 16–17, rather than importing their Gray-dependent F47 fibres.
The base is any *supplied* context category and every map of its Cat-valued
fibres has an explicit witness. No F69, F42/F54/F55, physical charge or
3-cell claim is smuggled into the statement. A later theorem must construct
these input data from genuine C60 physical incidence and independent Kuu.
-/

namespace Kuu.F112
open CategoryTheory
set_option autoImplicit false
universe uI vI uV vV

variable {I : Type uI} [Category.{vI} I]

/-- A genuine transformation of Cat-valued diagrams induces transport of
all dependent objects and arrows, without collapsing the index category. -/
def totalChange {F G : I ⥤ Cat} (α : F ⟶ G) :
    Grothendieck F ⥤ Grothendieck G := Grothendieck.map α

theorem totalChange_obj_base {F G : I ⥤ Cat} (α : F ⟶ G)
    (X : Grothendieck F) :
    ((totalChange α).obj X).base = X.base := rfl

theorem totalChange_map_base {F G : I ⥤ Cat} (α : F ⟶ G)
    {X Y : Grothendieck F} (f : X ⟶ Y) :
    ((totalChange α).map f).base = f.base := rfl

/-- The physical/contextual projection is exactly fixed, not merely
isomorphic: every original index morphism is retained. -/
theorem totalChange_overBase {F G : I ⥤ Cat} (α : F ⟶ G) :
    totalChange α ⋙ Grothendieck.forget G = Grothendieck.forget F :=
  Grothendieck.functor_comp_forget

theorem totalChange_id (F : I ⥤ Cat) :
    totalChange (𝟙 F) = 𝟭 (Grothendieck F) :=
  Grothendieck.map_id_eq

theorem totalChange_comp {F G H : I ⥤ Cat}
    (α : F ⟶ G) (β : G ⟶ H) :
    totalChange (α ≫ β) = totalChange α ⋙ totalChange β :=
  Grothendieck.map_comp_eq α β

/-- A diagram-level NatIso really gives a strict Cat isomorphism of
whole dependent source categories. This is not a raw F55 identification. -/
def totalCatIso {F G : I ⥤ Cat} (η : F ≅ G) :
    Cat.of (Grothendieck F) ≅ Cat.of (Grothendieck G) where
  hom := (totalChange η.hom).toCatHom
  inv := (totalChange η.inv).toCatHom
  hom_inv_id := by
    apply Cat.Hom.ext
    simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor,
      Cat.Hom.id_toFunctor] using
      ((totalChange_comp η.hom η.inv).symm.trans
        (congrArg totalChange η.hom_inv_id)).trans (totalChange_id F)
  inv_hom_id := by
    apply Cat.Hom.ext
    simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor,
      Cat.Hom.id_toFunctor] using
      ((totalChange_comp η.inv η.hom).symm.trans
        (congrArg totalChange η.inv_hom_id)).trans (totalChange_id G)

def totalEquivalence {F G : I ⥤ Cat} (η : F ≅ G) :
    Grothendieck F ≌ Grothendieck G :=
  Cat.equivOfIso (totalCatIso η)

theorem totalEquivalence_overBase {F G : I ⥤ Cat} (η : F ≅ G) :
    (totalEquivalence η).functor ⋙ Grothendieck.forget G =
      Grothendieck.forget F :=
  totalChange_overBase η.hom

/-- Any observer NatIso on Kuu's raw presentation that is already a
comparison of descended observers lifts to the declared quotient.
This is the Beck–Chevalley *categorical mechanism*, not an assumption
that the historical F42 sources satisfy that observer condition. -/
def quotientSourceIso {V : Type uV} [Quiver.{vV} V] (r : Relations V)
    {F G : Space V r ⥤ Cat}
    (α : project V r ⋙ F ≅ project V r ⋙ G) : F ≅ G :=
  CategoryTheory.Quotient.natIsoLift r α

theorem quotientSourceIso_hom {V : Type uV} [Quiver.{vV} V]
    (r : Relations V) {F G : Space V r ⥤ Cat}
    (α : project V r ⋙ F ≅ project V r ⋙ G) :
    (quotientSourceIso r α).hom = descendComparison r α.hom :=
  CategoryTheory.Quotient.natIsoLift_hom r α

theorem quotientSourceIso_inv {V : Type uV} [Quiver.{vV} V]
    (r : Relations V) {F G : Space V r ⥤ Cat}
    (α : project V r ⋙ F ≅ project V r ⋙ G) :
    (quotientSourceIso r α).inv = descendComparison r α.inv :=
  CategoryTheory.Quotient.natIsoLift_inv r α

#print axioms totalChange_comp
#print axioms totalChange_overBase
#print axioms totalCatIso
#print axioms totalEquivalence
#print axioms totalEquivalence_overBase
#print axioms quotientSourceIso_hom
#print axioms quotientSourceIso_inv
end Kuu.F112
