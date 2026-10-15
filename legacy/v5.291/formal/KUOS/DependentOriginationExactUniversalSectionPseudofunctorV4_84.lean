import KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
import Mathlib.CategoryTheory.Bicategory.InducedBicategory

namespace KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Coherent section pseudofunctor on the object-labelled realized sector v4.84

v4.83 constructs the inverse functor on each realization hom category. These
functors now assemble across hom categories into a native Pseudofunctor.

The domain keeps EXACTLY the existing exact-universal object labels, including
chosen raw systems, presentations and universal witnesses. Its hom categories
are induced from DO2 via the carrier map. This does not assert coverage of all
DO2 objects and does not identify different presentations with equal carriers.

Identity and composition comparison isomorphisms are lifted from DO2 identities
using local full faithfulness. Both their hom and inverse project to identity.
All five cross-hom coherence equations are proved by faithful realization:
left/right whiskering, associator, and left/right unitors. Native structural
cells are retained. The section is a pseudofunctor, not asserted to be strict.

This file does not construct an object-level inverse on all DO2, a global
pseudonatural unit/counit, a final mapping biequivalence, or independent raw-data
preservation. The exact/weak-sector boundary remains unchanged.
-/

/-! Homogeneous diagram algebra keeps simplification outside the chosen
presentation wrappers. No transparency or resource setting is changed. -/

private theorem removeIdentitySandwich {C : Type*} [Category C] {x y : C}
    (m : x ⟶ y) (l : x ⟶ x) (r : y ⟶ y)
    (hl : l = 𝟙 x) (hr : r = 𝟙 y) : l ≫ m ≫ r = m := by
  subst l
  subst r
  simp only [Category.id_comp, Category.comp_id]

private theorem removeAssociatorComparisons {B : Type*} [Bicategory B]
    {a b c d : B} (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d)
    (i₀ : (f ≫ g) ≫ h ⟶ (f ≫ g) ≫ h) (i₁ : f ≫ g ⟶ f ≫ g)
    (i₂ : g ≫ h ⟶ g ≫ h) (i₃ : f ≫ (g ≫ h) ⟶ f ≫ (g ≫ h))
    (h₀ : i₀ = 𝟙 _) (h₁ : i₁ = 𝟙 _) (h₂ : i₂ = 𝟙 _) (h₃ : i₃ = 𝟙 _) :
    i₀ ≫ i₁ ▷ h ≫ (α_ f g h).hom ≫ f ◁ i₂ ≫ i₃ = (α_ f g h).hom := by
  subst i₀
  subst i₁
  subst i₂
  subst i₃
  simp only [Bicategory.id_whiskerRight, Bicategory.whiskerLeft_id,
    Category.id_comp, Category.comp_id]

private theorem removeLeftUnitorComparisons {B : Type*} [Bicategory B]
    {a b : B} (f : a ⟶ b) (i : 𝟙 a ≫ f ⟶ 𝟙 a ≫ f) (j : 𝟙 a ⟶ 𝟙 a)
    (hi : i = 𝟙 _) (hj : j = 𝟙 _) :
    i ≫ j ▷ f ≫ (λ_ f).hom = (λ_ f).hom := by
  subst i
  subst j
  simp only [Bicategory.id_whiskerRight, Category.id_comp]

private theorem removeRightUnitorComparisons {B : Type*} [Bicategory B]
    {a b : B} (f : a ⟶ b) (i : f ≫ 𝟙 b ⟶ f ≫ 𝟙 b) (j : 𝟙 b ⟶ 𝟙 b)
    (hi : i = 𝟙 _) (hj : j = 𝟙 _) :
    i ≫ f ◁ j ≫ (ρ_ f).hom = (ρ_ f).hom := by
  subst i
  subst j
  simp only [Bicategory.whiskerLeft_id, Category.id_comp]

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The comparison between lifting an identity and the source identity. -/
def exactUniversalSectionIdIso
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    exactUniversalOneCellOfLift (W := W) A X X (𝟙 X.carrier) ≅
      ExactUniversalRawMorphism.id (W := W) A X :=
  exactUniversalSourceIsoOfLift (W := W) A (X := X) (Y := X)
    (f := exactUniversalOneCellOfLift (W := W) A X X (𝟙 X.carrier))
    (g := ExactUniversalRawMorphism.id (W := W) A X) (Iso.refl _)

/-- The comparison between lifting a composite and composing the chosen lifts. -/
def exactUniversalSectionCompIso
    (X Y Z : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) (k : Y.carrier ⟶ Z.carrier) :
    exactUniversalOneCellOfLift (W := W) A X Z (ell ≫ k) ≅
      ExactUniversalRawMorphism.comp (W := W) A
        (exactUniversalOneCellOfLift (W := W) A X Y ell)
        (exactUniversalOneCellOfLift (W := W) A Y Z k) :=
  exactUniversalSourceIsoOfLift (W := W) A (X := X) (Y := Z)
    (f := exactUniversalOneCellOfLift (W := W) A X Z (ell ≫ k))
    (g := ExactUniversalRawMorphism.comp (W := W) A
      (exactUniversalOneCellOfLift (W := W) A X Y ell)
      (exactUniversalOneCellOfLift (W := W) A Y Z k)) (Iso.refl _)

@[simp] theorem exactUniversalSectionIdIso_hom_lift
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalSectionIdIso (W := W) A X).hom.lift = 𝟙 (𝟙 X.carrier) :=
  (exactUniversalCompletion2HomFunctor (W := W) A X X).map_preimage
    (X := exactUniversalOneCellOfLift (W := W) A X X (𝟙 X.carrier))
    (Y := ExactUniversalRawMorphism.id (W := W) A X) (𝟙 (𝟙 X.carrier))

@[simp] theorem exactUniversalSectionIdIso_inv_lift
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalSectionIdIso (W := W) A X).inv.lift = 𝟙 (𝟙 X.carrier) :=
  (exactUniversalCompletion2HomFunctor (W := W) A X X).map_preimage
    (X := ExactUniversalRawMorphism.id (W := W) A X)
    (Y := exactUniversalOneCellOfLift (W := W) A X X (𝟙 X.carrier)) (𝟙 (𝟙 X.carrier))

@[simp] theorem exactUniversalSectionCompIso_hom_lift
    (X Y Z : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) (k : Y.carrier ⟶ Z.carrier) :
    (exactUniversalSectionCompIso (W := W) A X Y Z ell k).hom.lift = 𝟙 (ell ≫ k) :=
  (exactUniversalCompletion2HomFunctor (W := W) A X Z).map_preimage
    (X := exactUniversalOneCellOfLift (W := W) A X Z (ell ≫ k))
    (Y := ExactUniversalRawMorphism.comp (W := W) A
      (exactUniversalOneCellOfLift (W := W) A X Y ell)
      (exactUniversalOneCellOfLift (W := W) A Y Z k)) (𝟙 (ell ≫ k))

@[simp] theorem exactUniversalSectionCompIso_inv_lift
    (X Y Z : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) (k : Y.carrier ⟶ Z.carrier) :
    (exactUniversalSectionCompIso (W := W) A X Y Z ell k).inv.lift = 𝟙 (ell ≫ k) :=
  (exactUniversalCompletion2HomFunctor (W := W) A X Z).map_preimage
    (X := ExactUniversalRawMorphism.comp (W := W) A
      (exactUniversalOneCellOfLift (W := W) A X Y ell)
      (exactUniversalOneCellOfLift (W := W) A Y Z k))
    (Y := exactUniversalOneCellOfLift (W := W) A X Z (ell ≫ k)) (𝟙 (ell ≫ k))

/-- Objects retain source labels; all one- and two-cells between their carriers
come from DO2. This is not an assertion of object coverage of the whole DO2.
Infer the carrier universes from the typed object map: the generated universe
parameter list of DO2 is not the four-parameter source-object list. -/
abbrev ExactUniversalRealizedSector :=
  Bicategory.InducedBicategory
    (DependentOriginationCompletion2 (W := W) A)
    (fun X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A => X.carrier)

-- The source fibre object/hom universes stay independent, also after a level shift.
example : Bicategory (ExactUniversalRealizedSector.{u, v, uH + 1, vH} (W := W) A) :=
  inferInstance

example {X Y : ExactUniversalRealizedSector.{u, v, uH + 1, vH} (W := W) A}
    (f : X ⟶ Y) : X.carrier ⟶ Y.carrier := f.hom

/-- Assemble the local sections into a coherent, generally non-strict,
object-label-preserving pseudofunctor. Every coherence field is proved. -/
def exactUniversalSectionPseudofunctor :
    Pseudofunctor (ExactUniversalRealizedSector (W := W) A)
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) where
  obj X := X
  map {X Y} f := exactUniversalOneCellOfLift (W := W) A X Y f.hom
  map₂ {X Y} {f g} eta := (exactUniversalHomSection (W := W) A X Y).map eta.hom
  map₂_id f := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    rfl
  map₂_comp eta theta := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    rfl
  mapId X := exactUniversalSectionIdIso (W := W) A X
  mapComp {X Y Z} f g := exactUniversalSectionCompIso (W := W) A X Y Z f.hom g.hom
  map₂_whisker_left {X Y Z} f {g h} eta := by
    apply exactUniversalCompletion2_map_injective (W := W) A (X := X) (Y := Z)
    change f.hom ◁ eta.hom =
      (exactUniversalSectionCompIso (W := W) A X Y Z f.hom g.hom).hom.lift ≫
        (f.hom ◁ eta.hom) ≫
          (exactUniversalSectionCompIso (W := W) A X Y Z f.hom h.hom).inv.lift
    exact (removeIdentitySandwich (C := (X.carrier ⟶ Z.carrier))
      (f.hom ◁ eta.hom) _ _
      (exactUniversalSectionCompIso_hom_lift (W := W) A X Y Z f.hom g.hom)
      (exactUniversalSectionCompIso_inv_lift (W := W) A X Y Z f.hom h.hom)).symm
  map₂_whisker_right {X Y Z} {f g} eta h := by
    apply exactUniversalCompletion2_map_injective (W := W) A (X := X) (Y := Z)
    change eta.hom ▷ h.hom =
      (exactUniversalSectionCompIso (W := W) A X Y Z f.hom h.hom).hom.lift ≫
        (eta.hom ▷ h.hom) ≫
          (exactUniversalSectionCompIso (W := W) A X Y Z g.hom h.hom).inv.lift
    exact (removeIdentitySandwich (C := (X.carrier ⟶ Z.carrier))
      (eta.hom ▷ h.hom) _ _
      (exactUniversalSectionCompIso_hom_lift (W := W) A X Y Z f.hom h.hom)
      (exactUniversalSectionCompIso_inv_lift (W := W) A X Y Z g.hom h.hom)).symm
  map₂_associator {X Y Z T} f g h := by
    apply exactUniversalCompletion2_map_injective (W := W) A (X := X) (Y := T)
    change (α_ f.hom g.hom h.hom).hom =
      (exactUniversalSectionCompIso (W := W) A X Z T (f.hom ≫ g.hom) h.hom).hom.lift ≫
        (exactUniversalSectionCompIso (W := W) A X Y Z f.hom g.hom).hom.lift ▷ h.hom ≫
          (α_ f.hom g.hom h.hom).hom ≫
            f.hom ◁ (exactUniversalSectionCompIso (W := W) A Y Z T g.hom h.hom).inv.lift ≫
              (exactUniversalSectionCompIso (W := W) A X Y T f.hom (g.hom ≫ h.hom)).inv.lift
    exact (removeAssociatorComparisons
      (B := DependentOriginationCompletion2 (W := W) A)
      (a := X.carrier) (b := Y.carrier) (c := Z.carrier) (d := T.carrier)
      f.hom g.hom h.hom _ _ _ _
      (exactUniversalSectionCompIso_hom_lift (W := W) A X Z T (f.hom ≫ g.hom) h.hom)
      (exactUniversalSectionCompIso_hom_lift (W := W) A X Y Z f.hom g.hom)
      (exactUniversalSectionCompIso_inv_lift (W := W) A Y Z T g.hom h.hom)
      (exactUniversalSectionCompIso_inv_lift (W := W) A X Y T f.hom (g.hom ≫ h.hom))).symm
  map₂_left_unitor {X Y} f := by
    apply exactUniversalCompletion2_map_injective (W := W) A (X := X) (Y := Y)
    change (λ_ f.hom).hom =
      (exactUniversalSectionCompIso (W := W) A X X Y (𝟙 X.carrier) f.hom).hom.lift ≫
        (exactUniversalSectionIdIso (W := W) A X).hom.lift ▷ f.hom ≫ (λ_ f.hom).hom
    exact (removeLeftUnitorComparisons
      (B := DependentOriginationCompletion2 (W := W) A)
      (a := X.carrier) (b := Y.carrier) f.hom _ _
      (exactUniversalSectionCompIso_hom_lift (W := W) A X X Y (𝟙 X.carrier) f.hom)
      (exactUniversalSectionIdIso_hom_lift (W := W) A X)).symm
  map₂_right_unitor {X Y} f := by
    apply exactUniversalCompletion2_map_injective (W := W) A (X := X) (Y := Y)
    change (ρ_ f.hom).hom =
      (exactUniversalSectionCompIso (W := W) A X Y Y f.hom (𝟙 Y.carrier)).hom.lift ≫
        f.hom ◁ (exactUniversalSectionIdIso (W := W) A Y).hom.lift ≫ (ρ_ f.hom).hom
    exact (removeRightUnitorComparisons
      (B := DependentOriginationCompletion2 (W := W) A)
      (a := X.carrier) (b := Y.carrier) f.hom _ _
      (exactUniversalSectionCompIso_hom_lift (W := W) A X Y Y f.hom (𝟙 Y.carrier))
      (exactUniversalSectionIdIso_hom_lift (W := W) A Y)).symm

@[simp] theorem exactUniversalSectionPseudofunctor_map_lift
    {X Y : ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A} (f : X ⟶ Y) :
    ((exactUniversalSectionPseudofunctor (W := W) A).map f).lift = f.hom := rfl

@[simp] theorem exactUniversalSectionPseudofunctor_map₂_lift
    {X Y : ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A}
    {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((exactUniversalSectionPseudofunctor (W := W) A).map₂ eta).lift = eta.hom := rfl

/-! Regression checks exercise the native fields, not merely unrelated laws. -/

variable {X Y Z T : ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A}
local notation "S" => exactUniversalSectionPseudofunctor (W := W) A

example : Pseudofunctor (ExactUniversalRealizedSector (W := W) A)
    (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) := S

example : (S).obj X = (X : ExactUniversalRawObject (W := W) A) := rfl

example (f : X ⟶ Y) : ((S).map f).lift = f.hom := rfl

example {f g : X ⟶ Y} (eta : f ⟶ g) : ((S).map₂ eta).lift = eta.hom := rfl

example (f : X ⟶ Y) : (S).map₂ (𝟙 f) = 𝟙 ((S).map f) := (S).map₂_id f

example {f g h : X ⟶ Y} (eta : f ⟶ g) (theta : g ⟶ h) :
    (S).map₂ (eta ≫ theta) = (S).map₂ eta ≫ (S).map₂ theta := (S).map₂_comp eta theta

example : ((S).mapId X).hom.lift = 𝟙 (𝟙 X.carrier) :=
  exactUniversalSectionIdIso_hom_lift (W := W) A X

example : ((S).mapId X).inv.lift = 𝟙 (𝟙 X.carrier) :=
  exactUniversalSectionIdIso_inv_lift (W := W) A X

example (f : X ⟶ Y) (g : Y ⟶ Z) : ((S).mapComp f g).hom.lift = 𝟙 (f.hom ≫ g.hom) :=
  exactUniversalSectionCompIso_hom_lift (W := W) A X Y Z f.hom g.hom

example (f : X ⟶ Y) (g : Y ⟶ Z) : ((S).mapComp f g).inv.lift = 𝟙 (f.hom ≫ g.hom) :=
  exactUniversalSectionCompIso_inv_lift (W := W) A X Y Z f.hom g.hom

example : (exactUniversalCompletion2HomFunctor (W := W) A X X).mapIso
    ((S).mapId X) = Iso.refl (𝟙 X.carrier) := by
  apply Iso.ext
  exact exactUniversalSectionIdIso_hom_lift (W := W) A X

example (f : X ⟶ Y) (g : Y ⟶ Z) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Z).mapIso
      ((S).mapComp f g) = Iso.refl (f.hom ≫ g.hom) := by
  apply Iso.ext
  exact exactUniversalSectionCompIso_hom_lift (W := W) A X Y Z f.hom g.hom

example (f : X ⟶ Y) {g h : Y ⟶ Z} (eta : g ⟶ h) :
    (S).map₂ (f ◁ eta) = ((S).mapComp f g).hom ≫ (S).map f ◁ (S).map₂ eta ≫
      ((S).mapComp f h).inv := (S).map₂_whisker_left f eta

example {f g : X ⟶ Y} (eta : f ⟶ g) (h : Y ⟶ Z) :
    (S).map₂ (eta ▷ h) = ((S).mapComp f h).hom ≫ (S).map₂ eta ▷ (S).map h ≫
      ((S).mapComp g h).inv := (S).map₂_whisker_right eta h

example (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    (S).map₂ (α_ f g h).hom = ((S).mapComp (f ≫ g) h).hom ≫
      ((S).mapComp f g).hom ▷ (S).map h ≫ (α_ ((S).map f) ((S).map g) ((S).map h)).hom ≫
      (S).map f ◁ ((S).mapComp g h).inv ≫ ((S).mapComp f (g ≫ h)).inv :=
  (S).map₂_associator f g h

example (f : X ⟶ Y) : (S).map₂ (λ_ f).hom = ((S).mapComp (𝟙 X) f).hom ≫
    ((S).mapId X).hom ▷ (S).map f ≫ (λ_ ((S).map f)).hom := (S).map₂_left_unitor f

example (f : X ⟶ Y) : (S).map₂ (ρ_ f).hom = ((S).mapComp f (𝟙 Y)).hom ≫
    (S).map f ◁ ((S).mapId Y).hom ≫ (ρ_ ((S).map f)).hom := (S).map₂_right_unitor f

example (ell : X.carrier ⟶ Y.carrier) :
    ((S).map (Bicategory.InducedBicategory.mkHom (X := X) (Y := Y) ell)).lift = ell := rfl

#print axioms exactUniversalSectionIdIso
#print axioms exactUniversalSectionCompIso
#print axioms exactUniversalSectionIdIso_inv_lift
#print axioms exactUniversalSectionCompIso_hom_lift
#print axioms exactUniversalSectionCompIso_inv_lift
#print axioms exactUniversalSectionPseudofunctor
#print axioms exactUniversalSectionPseudofunctor_map₂_lift

end

end KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
