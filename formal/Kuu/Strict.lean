import Kuu.Presentation
import Mathlib.CategoryTheory.Functor.Category

/-!
# Strict comparison calculus over Kuu spaces

1-cells are genuine functors between the constructed spaces, 2-cells are
natural transformations. Units/associativity and interchange are equalities,
not extra interchanger generators. This is the strict two-dimensional core;
it is NOT a claim that a proof-relevant global strict 3-category has been built.
-/
namespace Kuu
open CategoryTheory
universe u v uD vD uE vE uF vF
set_option autoImplicit false

variable {A : Type u} [Category.{v} A]
variable {B : Type uD} [Category.{vD} B]
variable {C : Type uE} [Category.{vE} C]
variable {D : Type uF} [Category.{vF} D]

theorem one_assoc (F : A ⥤ B) (G : B ⥤ C) (H : C ⥤ D) :
    (F ⋙ G) ⋙ H = F ⋙ (G ⋙ H) := Functor.assoc F G H

theorem one_left_unit (F : A ⥤ B) : (𝟭 A) ⋙ F = F := rfl

theorem one_right_unit (F : A ⥤ B) : F ⋙ (𝟭 B) = F := rfl

theorem two_vertical_assoc {F G H I : A ⥤ B}
    (α : F ⟶ G) (β : G ⟶ H) (γ : H ⟶ I) :
    (α ≫ β) ≫ γ = α ≫ (β ≫ γ) := Category.assoc α β γ

theorem two_vertical_left_unit {F G : A ⥤ B} (α : F ⟶ G) :
    (𝟙 F) ≫ α = α := Category.id_comp α

theorem two_vertical_right_unit {F G : A ⥤ B} (α : F ⟶ G) :
    α ≫ (𝟙 G) = α := Category.comp_id α

/-- Strict middle-four interchange, before any observation into another theory. -/
theorem two_interchange {F G H : A ⥤ B} {I J L : B ⥤ C}
    (α : F ⟶ G) (β : G ⟶ H) (γ : I ⟶ J) (δ : J ⟶ L) :
    (α ≫ β) ◫ (γ ≫ δ) = (α ◫ γ) ≫ (β ◫ δ) :=
  NatTrans.exchange α β γ δ

theorem two_horizontal_assoc {F G : A ⥤ B} {H I : B ⥤ C}
    {J L : C ⥤ D} (α : F ⟶ G) (β : H ⟶ I) (γ : J ⟶ L) :
    (α ◫ β) ◫ γ = α ◫ (β ◫ γ) := by
  ext X
  simp only [NatTrans.hcomp_app, Functor.comp_obj, Functor.comp_map,
    Functor.map_comp, Category.assoc]

theorem two_horizontal_left_unit {F G : A ⥤ B} (α : F ⟶ G) :
    (𝟙 (𝟭 A)) ◫ α = α := by
  ext X
  simp only [NatTrans.hcomp_app, NatTrans.id_app, Functor.id_obj,
    Functor.map_id, Category.comp_id]

theorem two_horizontal_right_unit {F G : A ⥤ B} (α : F ⟶ G) :
    α ◫ (𝟙 (𝟭 B)) = α := by
  ext X
  simp only [NatTrans.hcomp_app, NatTrans.id_app, Functor.id_map, Category.id_comp]

section TwoDimensionalDescent
variable {V : Type u} [Quiver.{v} V] (r : Relations V)
variable {F G H : Space V r ⥤ B}

def descendComparison (α : project V r ⋙ F ⟶ project V r ⋙ G) : F ⟶ G :=
  CategoryTheory.Quotient.natTransLift r α

theorem descendComparison_comp
    (α : project V r ⋙ F ⟶ project V r ⋙ G)
    (β : project V r ⋙ G ⟶ project V r ⋙ H) :
    descendComparison r (α ≫ β) = descendComparison r α ≫ descendComparison r β :=
  (CategoryTheory.Quotient.comp_natTransLift r α β).symm

theorem descendComparison_id (F : Space V r ⥤ B) :
    descendComparison r (𝟙 (project V r ⋙ F)) = 𝟙 F :=
  CategoryTheory.Quotient.natTransLift_id r F
end TwoDimensionalDescent

#print axioms one_assoc
#print axioms two_interchange
#print axioms two_horizontal_assoc
#print axioms descendComparison_comp
#print axioms descendComparison_id
end Kuu
