import Mathlib.CategoryTheory.Bicategory.Basic

namespace KUOS.DependentOriginationMixedLeftUnitorPastingV1_36

open CategoryTheory
open CategoryTheory.Bicategory
open scoped Bicategory

universe u v w

variable {C : Type u} [Bicategory.{w, v} C]

/-!
The mixed left-unitor equation retains the actual comparison isomorphism
and both equality-derived transports. The identity equality is explicit;
no strictness of the target bicategory or cylinder existence is assumed.
-/

/-- Right whiskering preserves the left-unitor comparison after its
explicit identity transport is pasted through the associator. -/
theorem mixedLeftUnitorPasting
    {a b c : C} {i : a ⟶ a} (hi : i = 𝟙 a)
    (f : a ⟶ b) (t : b ⟶ c)
    {p : a ⟶ b} (L : p ≅ i ≫ f) :
    (L.hom ≫ eqToHom (congrArg (fun j : a ⟶ a => j ≫ f) hi) ≫
      (λ_ f).hom) ▷ t =
      (whiskerRightIso L t ≪≫ α_ i f t).hom ≫
        eqToHom (congrArg (fun j : a ⟶ a => j ≫ (f ≫ t)) hi) ≫
          (λ_ (f ≫ t)).hom := by
  subst i
  dsimp only [Iso.trans, whiskerRightIso]
  simp only [eqToHom_refl, Category.id_comp, Category.comp_id,
    Bicategory.comp_whiskerRight, Bicategory.leftUnitor_whiskerRight,
    Category.assoc]

#print axioms mixedLeftUnitorPasting

end KUOS.DependentOriginationMixedLeftUnitorPastingV1_36
