import Kuu.Strict
import Mathlib.CategoryTheory.Comma.Over.Basic
import Mathlib.CategoryTheory.Grothendieck

/-!
# Context-indexed Kuu slices and actual transport

The context category is an independent input. We do not replace an arbitrary
physical incidence category by a two-rank Boolean proxy. All its morphisms are
retained. A concrete geometric interpretation must be supplied and checked.
-/
namespace Kuu
open CategoryTheory
universe u v uI vI
set_option autoImplicit false

variable {V : Type u} [Quiver.{v} V] (r : Relations V)
variable {I : Type uI} [Category.{vI} I]

def incidenceDiagram (F : I ⥤ Space V r) : I ⥤ Cat :=
  F ⋙ Over.mapFunctor (Space V r)

abbrev IncidenceTotal (F : I ⥤ Space V r) := Grothendieck (incidenceDiagram r F)

def incidenceProjection (F : I ⥤ Space V r) : IncidenceTotal r F ⥤ I :=
  Grothendieck.forget (incidenceDiagram r F)

theorem incidence_comp (F : I ⥤ Space V r) {X Y Z : I}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (incidenceDiagram r F).map (f ≫ g) =
      (incidenceDiagram r F).map f ≫ (incidenceDiagram r F).map g :=
  (incidenceDiagram r F).map_comp f g

theorem incidence_triangle (F : I ⥤ Space V r) {X Y Z : I}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : X ⟶ Z) (e : f ≫ g = h) :
    (incidenceDiagram r F).map f ≫ (incidenceDiagram r F).map g =
      (incidenceDiagram r F).map h := by
  rw [← (incidenceDiagram r F).map_comp, e]

theorem incidence_restrict {J : Type uI} [Category.{vI} J]
    (R : J ⥤ I) (F : I ⥤ Space V r) :
    incidenceDiagram r (R ⋙ F) = R ⋙ incidenceDiagram r F :=
  Functor.assoc R F _

#print axioms incidenceDiagram
#print axioms incidence_comp
#print axioms incidence_triangle
#print axioms incidence_restrict
end Kuu
