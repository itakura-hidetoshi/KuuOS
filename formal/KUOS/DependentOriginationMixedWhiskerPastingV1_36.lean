import Mathlib.CategoryTheory.Bicategory.Basic

namespace KUOS.DependentOriginationMixedWhiskerPastingV1_36

open CategoryTheory
open CategoryTheory.Bicategory
open scoped Bicategory

universe u v w

variable {C : Type u} [Bicategory.{w, v} C]

/-!
Typed pasting for the mixed right-whiskering case of v1.36.

The three equations separate genuine two-cell interchange, associator
naturality, and composition with the pseudofunctor comparison isomorphisms.
They use only the pinned bicategory API; no cylinder, fibrancy, strictness,
or universe-descent conclusion is assumed.
-/

/-- Interchange followed by cancellation of a whiskered isomorphism. -/
theorem whiskerIsoConjugation
    {a b c : C} {f g : a ⟶ b} (θ : f ⟶ g)
    {h k : b ⟶ c} (e : h ≅ k) :
    (f ◁ e.hom) ≫ (θ ▷ k) ≫ (g ◁ e.inv) = θ ▷ h := by
  rw [Bicategory.whisker_exchange_assoc]
  simp only [Bicategory.whiskerLeft_hom_inv, Category.comp_id]

/-- Pasting the interchange square between the two associators. -/
theorem reassociatedRightWhisker
    {a b c d e : C} {f g : a ⟶ b} (θ : f ⟶ g)
    (h : b ⟶ c) (t : c ⟶ e) (s : b ⟶ d) (k : d ⟶ e)
    (ν : h ≫ t ≅ s ≫ k) :
    (θ ▷ h) ▷ t =
      (α_ f h t).hom ≫ (f ◁ ν.hom) ≫
        (α_ f s k).inv ≫ ((θ ▷ s) ▷ k) ≫
          (α_ g s k).hom ≫ (g ◁ ν.inv) ≫ (α_ g h t).inv := by
  calc
    (θ ▷ h) ▷ t =
        (α_ f h t).hom ≫ (θ ▷ (h ≫ t)) ≫ (α_ g h t).inv :=
      Bicategory.whiskerRight_comp_symm θ h t
    _ = (α_ f h t).hom ≫
        ((f ◁ ν.hom) ≫ (θ ▷ (s ≫ k)) ≫ (g ◁ ν.inv)) ≫
          (α_ g h t).inv :=
      congrArg (fun χ => (α_ f h t).hom ≫ χ ≫ (α_ g h t).inv)
        (whiskerIsoConjugation θ ν).symm
    _ = _ := by
      rw [Bicategory.whiskerRight_comp θ s k]
      simp only [Category.assoc]

/-- The exact mixed equation, with both comparison isomorphisms retained. -/
theorem mixedRightWhiskerPasting
    {a b c d e : C} {f g : a ⟶ b} (θ : f ⟶ g)
    (h : b ⟶ c) (t : c ⟶ e) (s : b ⟶ d) (k : d ⟶ e)
    (ν : h ≫ t ≅ s ≫ k)
    {p q : a ⟶ c} (L : p ≅ f ≫ h) (R : q ≅ g ≫ h) :
    (L.hom ≫ (θ ▷ h) ≫ R.inv) ▷ t =
      (whiskerRightIso L t ≪≫ α_ f h t ≪≫
        whiskerLeftIso f ν ≪≫ (α_ f s k).symm).hom ≫
        ((θ ▷ s) ▷ k) ≫
      (whiskerRightIso R t ≪≫ α_ g h t ≪≫
        whiskerLeftIso g ν ≪≫ (α_ g s k).symm).inv := by
  dsimp only [Iso.trans, Iso.symm, whiskerRightIso, whiskerLeftIso]
  simp only [Bicategory.comp_whiskerRight,
    reassociatedRightWhisker θ h t s k ν, Category.assoc]

#print axioms whiskerIsoConjugation
#print axioms reassociatedRightWhisker
#print axioms mixedRightWhiskerPasting

end KUOS.DependentOriginationMixedWhiskerPastingV1_36
