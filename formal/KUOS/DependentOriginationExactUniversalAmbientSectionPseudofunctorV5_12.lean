import KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
import KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84

namespace KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient canonical section pseudofunctor v5.12

v5.11 chooses, for every ambient completion object, an exact-universal source
object whose carrier is definitionally that ambient object.  It also supplies
an exact local hom-section functor on every ambient hom category.

This file assembles those objectwise and homwise choices into a genuine
pseudofunctor from the ambient completion back to the exact-universal source.
The coherence proof deliberately reuses the already validated v4.84
identity/composition comparison isomorphisms and proves the cross-hom laws by
faithful realization.

The construction is not asserted to be strict: the local section preserves
ambient one- and two-cells exactly after realization, while identity and
composition in the source are connected by coherent comparison isomorphisms.
-/

private theorem removeIdentitySandwich {C : Type*} [Category C] {x y : C}
    (m : x ⟶ y) (l : x ⟶ x) (r : y ⟶ y)
    (hl : l = 𝟙 x) (hr : r = 𝟙 y) :
    l ≫ m ≫ r = m := by
  subst l
  subst r
  simp only [Category.id_comp, Category.comp_id]

private theorem removeAssociatorComparisons {B : Type*} [Bicategory B]
    {a b c d : B} (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d)
    (i₀ : (f ≫ g) ≫ h ⟶ (f ≫ g) ≫ h) (i₁ : f ≫ g ⟶ f ≫ g)
    (i₂ : g ≫ h ⟶ g ≫ h) (i₃ : f ≫ (g ≫ h) ⟶ f ≫ (g ≫ h))
    (h₀ : i₀ = 𝟙 _) (h₁ : i₁ = 𝟙 _) (h₂ : i₂ = 𝟙 _) (h₃ : i₃ = 𝟙 _) :
    i₀ ≫ i₁ ▷ h ≫ (α_ f g h).hom ≫ f ◁ i₂ ≫ i₃ =
      (α_ f g h).hom := by
  subst i₀
  subst i₁
  subst i₂
  subst i₃
  simp only [Bicategory.id_whiskerRight, Bicategory.whiskerLeft_id,
    Category.id_comp, Category.comp_id]

private theorem removeLeftUnitorComparisons {B : Type*} [Bicategory B]
    {a b : B} (f : a ⟶ b)
    (i : 𝟙 a ≫ f ⟶ 𝟙 a ≫ f) (j : 𝟙 a ⟶ 𝟙 a)
    (hi : i = 𝟙 _) (hj : j = 𝟙 _) :
    i ≫ j ▷ f ≫ (λ_ f).hom = (λ_ f).hom := by
  subst i
  subst j
  simp only [Bicategory.id_whiskerRight, Category.id_comp]

private theorem removeRightUnitorComparisons {B : Type*} [Bicategory B]
    {a b : B} (f : a ⟶ b)
    (i : f ≫ 𝟙 b ⟶ f ≫ 𝟙 b) (j : 𝟙 b ⟶ 𝟙 b)
    (hi : i = 𝟙 _) (hj : j = 𝟙 _) :
    i ≫ f ◁ j ≫ (ρ_ f).hom = (ρ_ f).hom := by
  subst i
  subst j
  simp only [Bicategory.whiskerLeft_id, Category.id_comp]

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

/-- Identity comparison for the ambient canonical section.  It is exactly the
v4.84 section comparison specialized to the canonical v5.11 source label. -/
noncomputable def exactUniversalAmbientSectionIdIso
    (Z : Ambient (W := W) A) :
    (exactUniversalAmbientCanonicalHomSection (W := W) A Z Z).obj (𝟙 Z) ≅
      𝟙 (exactUniversalAmbientCanonicalSource (W := W) A Z) :=
  exactUniversalSectionIdIso
    (W := W) A
    (exactUniversalAmbientCanonicalSource (W := W) A Z)

/-- Composition comparison for the ambient canonical section. -/
noncomputable def exactUniversalAmbientSectionCompIso
    {X Y Z : Ambient (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (exactUniversalAmbientCanonicalHomSection (W := W) A X Z).obj (f ≫ g) ≅
      (exactUniversalAmbientCanonicalHomSection (W := W) A X Y).obj f ≫
        (exactUniversalAmbientCanonicalHomSection (W := W) A Y Z).obj g :=
  exactUniversalSectionCompIso
    (W := W) A
    (exactUniversalAmbientCanonicalSource (W := W) A X)
    (exactUniversalAmbientCanonicalSource (W := W) A Y)
    (exactUniversalAmbientCanonicalSource (W := W) A Z)
    f g

@[simp] theorem exactUniversalAmbientSectionIdIso_hom_lift
    (Z : Ambient (W := W) A) :
    (exactUniversalAmbientSectionIdIso (W := W) A Z).hom.lift =
      𝟙 (𝟙 Z) := by
  exact
    exactUniversalSectionIdIso_hom_lift
      (W := W) A
      (exactUniversalAmbientCanonicalSource (W := W) A Z)

@[simp] theorem exactUniversalAmbientSectionIdIso_inv_lift
    (Z : Ambient (W := W) A) :
    (exactUniversalAmbientSectionIdIso (W := W) A Z).inv.lift =
      𝟙 (𝟙 Z) := by
  exact
    exactUniversalSectionIdIso_inv_lift
      (W := W) A
      (exactUniversalAmbientCanonicalSource (W := W) A Z)

@[simp] theorem exactUniversalAmbientSectionCompIso_hom_lift
    {X Y Z : Ambient (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (exactUniversalAmbientSectionCompIso (W := W) A f g).hom.lift =
      𝟙 (f ≫ g) := by
  exact
    exactUniversalSectionCompIso_hom_lift
      (W := W) A
      (exactUniversalAmbientCanonicalSource (W := W) A X)
      (exactUniversalAmbientCanonicalSource (W := W) A Y)
      (exactUniversalAmbientCanonicalSource (W := W) A Z)
      f g

@[simp] theorem exactUniversalAmbientSectionCompIso_inv_lift
    {X Y Z : Ambient (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (exactUniversalAmbientSectionCompIso (W := W) A f g).inv.lift =
      𝟙 (f ≫ g) := by
  exact
    exactUniversalSectionCompIso_inv_lift
      (W := W) A
      (exactUniversalAmbientCanonicalSource (W := W) A X)
      (exactUniversalAmbientCanonicalSource (W := W) A Y)
      (exactUniversalAmbientCanonicalSource (W := W) A Z)
      f g

/-- Canonical ambient quasi-inverse candidate, assembled as a genuine
pseudofunctor. -/
noncomputable def exactUniversalAmbientCanonicalSectionPseudofunctor :
    Pseudofunctor
      (Ambient (W := W) A)
      (Source (W := W) A) where
  obj Z := exactUniversalAmbientCanonicalSource (W := W) A Z
  map {X Y} f :=
    (exactUniversalAmbientCanonicalHomSection (W := W) A X Y).obj f
  map₂ {X Y} {f g} eta :=
    (exactUniversalAmbientCanonicalHomSection (W := W) A X Y).map eta
  map₂_id f :=
    (exactUniversalAmbientCanonicalHomSection (W := W) A _ _).map_id f
  map₂_comp eta theta :=
    (exactUniversalAmbientCanonicalHomSection (W := W) A _ _).map_comp eta theta
  mapId Z := exactUniversalAmbientSectionIdIso (W := W) A Z
  mapComp f g := exactUniversalAmbientSectionCompIso (W := W) A f g
  map₂_whisker_left {X Y Z} f {g h} eta := by
    apply
      exactUniversalCompletion2_map_injective
        (W := W) A
        (X := exactUniversalAmbientCanonicalSource (W := W) A X)
        (Y := exactUniversalAmbientCanonicalSource (W := W) A Z)
    change
      f ◁ eta =
        (exactUniversalAmbientSectionCompIso (W := W) A f g).hom.lift ≫
          (f ◁ eta) ≫
            (exactUniversalAmbientSectionCompIso (W := W) A f h).inv.lift
    exact
      (removeIdentitySandwich
        (C := (X ⟶ Z))
        (f ◁ eta) _ _
        (exactUniversalAmbientSectionCompIso_hom_lift
          (W := W) A f g)
        (exactUniversalAmbientSectionCompIso_inv_lift
          (W := W) A f h)).symm
  map₂_whisker_right {X Y Z} {f g} eta h := by
    apply
      exactUniversalCompletion2_map_injective
        (W := W) A
        (X := exactUniversalAmbientCanonicalSource (W := W) A X)
        (Y := exactUniversalAmbientCanonicalSource (W := W) A Z)
    change
      eta ▷ h =
        (exactUniversalAmbientSectionCompIso (W := W) A f h).hom.lift ≫
          (eta ▷ h) ≫
            (exactUniversalAmbientSectionCompIso (W := W) A g h).inv.lift
    exact
      (removeIdentitySandwich
        (C := (X ⟶ Z))
        (eta ▷ h) _ _
        (exactUniversalAmbientSectionCompIso_hom_lift
          (W := W) A f h)
        (exactUniversalAmbientSectionCompIso_inv_lift
          (W := W) A g h)).symm
  map₂_associator {X Y Z T} f g h := by
    apply
      exactUniversalCompletion2_map_injective
        (W := W) A
        (X := exactUniversalAmbientCanonicalSource (W := W) A X)
        (Y := exactUniversalAmbientCanonicalSource (W := W) A T)
    change
      (α_ f g h).hom =
        (exactUniversalAmbientSectionCompIso (W := W) A (f ≫ g) h).hom.lift ≫
          (exactUniversalAmbientSectionCompIso (W := W) A f g).hom.lift ▷ h ≫
            (α_ f g h).hom ≫
              f ◁ (exactUniversalAmbientSectionCompIso (W := W) A g h).inv.lift ≫
                (exactUniversalAmbientSectionCompIso
                  (W := W) A f (g ≫ h)).inv.lift
    exact
      (removeAssociatorComparisons
        (B := Ambient (W := W) A)
        f g h _ _ _ _
        (exactUniversalAmbientSectionCompIso_hom_lift
          (W := W) A (f ≫ g) h)
        (exactUniversalAmbientSectionCompIso_hom_lift
          (W := W) A f g)
        (exactUniversalAmbientSectionCompIso_inv_lift
          (W := W) A g h)
        (exactUniversalAmbientSectionCompIso_inv_lift
          (W := W) A f (g ≫ h))).symm
  map₂_left_unitor {X Y} f := by
    apply
      exactUniversalCompletion2_map_injective
        (W := W) A
        (X := exactUniversalAmbientCanonicalSource (W := W) A X)
        (Y := exactUniversalAmbientCanonicalSource (W := W) A Y)
    change
      (λ_ f).hom =
        (exactUniversalAmbientSectionCompIso (W := W) A (𝟙 X) f).hom.lift ≫
          (exactUniversalAmbientSectionIdIso (W := W) A X).hom.lift ▷ f ≫
            (λ_ f).hom
    exact
      (removeLeftUnitorComparisons
        (B := Ambient (W := W) A)
        f _ _
        (exactUniversalAmbientSectionCompIso_hom_lift
          (W := W) A (𝟙 X) f)
        (exactUniversalAmbientSectionIdIso_hom_lift
          (W := W) A X)).symm
  map₂_right_unitor {X Y} f := by
    apply
      exactUniversalCompletion2_map_injective
        (W := W) A
        (X := exactUniversalAmbientCanonicalSource (W := W) A X)
        (Y := exactUniversalAmbientCanonicalSource (W := W) A Y)
    change
      (ρ_ f).hom =
        (exactUniversalAmbientSectionCompIso (W := W) A f (𝟙 Y)).hom.lift ≫
          f ◁ (exactUniversalAmbientSectionIdIso (W := W) A Y).hom.lift ≫
            (ρ_ f).hom
    exact
      (removeRightUnitorComparisons
        (B := Ambient (W := W) A)
        f _ _
        (exactUniversalAmbientSectionCompIso_hom_lift
          (W := W) A f (𝟙 Y))
        (exactUniversalAmbientSectionIdIso_hom_lift
          (W := W) A Y)).symm

@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_obj_realization
    (Z : Ambient (W := W) A) :
    (exactUniversalRealization (W := W) A).obj
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).obj Z) = Z := by
  exact exactUniversalAmbientCanonicalSource_realization_obj (W := W) A Z

@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift
    {X Y : Ambient (W := W) A}
    (f : X ⟶ Y) :
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).map f).lift = f := by
  exact exactUniversalAmbientCanonicalHomSection_obj_lift (W := W) A f

@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift
    {X Y : Ambient (W := W) A}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).map₂ eta).lift = eta := by
  exact exactUniversalAmbientCanonicalHomSection_map_lift (W := W) A eta

/-! ## Regression checks -/

#print axioms exactUniversalAmbientSectionIdIso
#print axioms exactUniversalAmbientSectionCompIso
#print axioms exactUniversalAmbientSectionIdIso_hom_lift
#print axioms exactUniversalAmbientSectionIdIso_inv_lift
#print axioms exactUniversalAmbientSectionCompIso_hom_lift
#print axioms exactUniversalAmbientSectionCompIso_inv_lift
#print axioms exactUniversalAmbientCanonicalSectionPseudofunctor
#print axioms exactUniversalAmbientCanonicalSectionPseudofunctor_obj_realization
#print axioms exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift
#print axioms exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift

end

end KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12
