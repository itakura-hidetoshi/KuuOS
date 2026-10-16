import Mathlib.CategoryTheory.PathCategory.Basic
import Mathlib.CategoryTheory.Quotient

/-!
# Kuu: boundary-typed presentations and declared replacement

The primitive data are a quiver and relations between parallel paths. There is
no prior evaluation target, charge, exchange phase, or reconstruction condition.
Replacement is the equivalence/composition closure of the declared relations.
-/
namespace Kuu
open CategoryTheory
universe u v uD vD
set_option autoImplicit false

abbrev Raw (V : Type u) [Quiver.{v} V] := Paths V
abbrev Relations (V : Type u) [Quiver.{v} V] := HomRel (Raw V)
abbrev Space (V : Type u) [Quiver.{v} V] (r : Relations V) :=
  CategoryTheory.Quotient r

def project (V : Type u) [Quiver.{v} V] (r : Relations V) :
    Raw V ⥤ Space V r := CategoryTheory.Quotient.functor r

def Replaceable {V : Type u} [Quiver.{v} V] (r : Relations V)
    {X Y : Raw V} (f g : X ⟶ Y) : Prop :=
  Relation.EqvGen (@HomRel.CompClosure (Raw V) _ r X Y) f g

theorem project_exact {V : Type u} [Quiver.{v} V] (r : Relations V)
    {X Y : Raw V} (f g : X ⟶ Y) :
    (project V r).map f = (project V r).map g ↔ Replaceable r f g :=
  CategoryTheory.Quotient.functor_homRel_eq_compClosure_eqvGen r f g

theorem declared_replacement {V : Type u} [Quiver.{v} V] (r : Relations V)
    {X Y : Raw V} {f g : X ⟶ Y} (h : r f g) :
    (project V r).map f = (project V r).map g :=
  CategoryTheory.Quotient.sound r h

theorem replacement_context {V : Type u} [Quiver.{v} V] (r : Relations V)
    {W X Y Z : Raw V} (l : W ⟶ X) (h : Y ⟶ Z)
    {f g : X ⟶ Y} (e : Replaceable r f g) :
    Replaceable r (l ≫ f ≫ h) (l ≫ g ≫ h) := by
  apply (project_exact r _ _).mp
  have e' := (project_exact r f g).mpr e
  simp only [Functor.map_comp, e']

theorem replacement_comp {V : Type u} [Quiver.{v} V] (r : Relations V)
    {X Y Z : Raw V} {f f' : X ⟶ Y} {g g' : Y ⟶ Z}
    (hf : Replaceable r f f') (hg : Replaceable r g g') :
    Replaceable r (f ≫ g) (f' ≫ g') := by
  apply (project_exact r _ _).mp
  have ef := (project_exact r f f').mpr hf
  have eg := (project_exact r g g').mpr hg
  simp only [Functor.map_comp, ef, eg]

variable {V : Type u} [Quiver.{v} V] (r : Relations V)
variable {D : Type uD} [Category.{vD} D]

/-- An observer may be used only when it respects the declared replacements. -/
def Respects (F : Raw V ⥤ D) : Prop :=
  ∀ (X Y : Raw V) (f g : X ⟶ Y), r f g → F.map f = F.map g

def descend (F : Raw V ⥤ D) (h : Respects r F) : Space V r ⥤ D :=
  CategoryTheory.Quotient.lift r F h

theorem descend_spec (F : Raw V ⥤ D) (h : Respects r F) :
    project V r ⋙ descend r F h = F :=
  CategoryTheory.Quotient.lift_spec r F h

theorem descend_unique (F : Raw V ⥤ D) (h : Respects r F)
    (G : Space V r ⥤ D) (hG : project V r ⋙ G = F) :
    G = descend r F h :=
  CategoryTheory.Quotient.lift_unique r F h G hG

theorem observer_existsUnique (F : Raw V ⥤ D) (h : Respects r F) :
    ∃! G : Space V r ⥤ D, project V r ⋙ G = F := by
  refine ⟨descend r F h, descend_spec r F h, ?_⟩
  intro G hG
  exact descend_unique r F h G hG

/-- A declared presentation relation is not the relation of an evaluator. -/
def identityRelations (V : Type u) [Quiver.{v} V] : Relations V :=
  fun {_ _} f g => f = g

instance identityRelations_congruence (V : Type u) [Quiver.{v} V] :
    Congruence (identityRelations V) := by
  change Congruence (𝟭 (Raw V)).homRel
  infer_instance

/-- No additional replacement means that distinct parallel paths survive. -/
theorem identity_projection_reflects {X Y : Raw V} (f g : X ⟶ Y) :
    (project V (identityRelations V)).map f =
      (project V (identityRelations V)).map g ↔ f = g :=
  CategoryTheory.Quotient.functor_map_eq_iff (identityRelations V) f g

#print axioms project_exact
#print axioms replacement_context
#print axioms replacement_comp
#print axioms observer_existsUnique
#print axioms identity_projection_reflects
end Kuu
