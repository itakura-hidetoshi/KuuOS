import Mathlib.CategoryTheory.Bicategory.Basic
import Mathlib.CategoryTheory.Bicategory.Strict.Basic
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

namespace KUOS.DependentOriginationMixedRightUnitorPastingV1_36

open CategoryTheory
open CategoryTheory.Bicategory
open scoped Bicategory

universe u v w

variable {C : Type u} [Bicategory.{w, v} C]

/-!
Typed mixed right-unitor pasting. The comparison isomorphism and the
strong-transformation identity naturality are both retained explicitly.
The two identity transports are separate data, not hidden by simp.
-/

/-- Paste the right-unitor comparison, identity naturality, and both
pseudofunctorial comparison 2-cells in a general bicategory. -/
theorem mixedRightUnitorPasting
    {a b c : C} (f : a ⟶ b) (t : b ⟶ c)
    {i : b ⟶ b} (hi : i = 𝟙 b)
    {k : c ⟶ c} (hk : k = 𝟙 c)
    {p : a ⟶ b} (L : p ≅ f ≫ i)
    (N : i ≫ t ≅ t ≫ k)
    (hN : N.hom =
      (eqToHom hi ▷ t) ≫ (λ_ t).hom ≫
        (ρ_ t).inv ≫ (t ◁ eqToHom hk.symm)) :
    (L.hom ≫ eqToHom (congrArg (fun j : b ⟶ b => f ≫ j) hi) ≫
      (ρ_ f).hom) ▷ t =
      (whiskerRightIso L t ≪≫ α_ f i t ≪≫
        whiskerLeftIso f N ≪≫ (α_ f t k).symm).hom ≫
        eqToHom (congrArg (fun j : c ⟶ c => (f ≫ t) ≫ j) hk) ≫
          (ρ_ (f ≫ t)).hom := by
  subst i
  subst k
  simp only [eqToHom_refl, id_whiskerRight, whiskerLeft_id,
    Category.id_comp, Category.comp_id, Category.assoc] at hN
  dsimp only [Iso.trans, Iso.symm, whiskerRightIso, whiskerLeftIso]
  simp only [eqToHom_refl, Category.id_comp, Category.comp_id, Category.assoc]
  rw [hN]
  bicategory

#print axioms mixedRightUnitorPasting

end KUOS.DependentOriginationMixedRightUnitorPastingV1_36
