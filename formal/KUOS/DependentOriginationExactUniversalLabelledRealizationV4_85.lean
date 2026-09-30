import KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
import KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70

namespace KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Label-preserving strict realization and exact cellwise round trip v4.85

v4.84 assembled the local hom-category sections into a pseudofunctor from the
object-labelled realized sector back to the exact-universal source.  This file
constructs the converse direction while RETAINING the same source object labels.

The target is not all of DO2.  It is exactly the induced bicategory from v4.84:
objects are the existing exact-universal source objects, while one- and two-cells
are the corresponding DO2 cells between their chosen carriers.

The labelled realization is strict:

* X maps to the same label X;
* f maps to the induced one-cell wrapping f.lift;
* eta maps to the induced two-cell wrapping eta.lift;
* identities and compositions are preserved by definitional equality;
* whiskering, associator and unitor compatibility are inherited from the
  already verified strict realization v4.70 after forgetting the induced
  wrappers.

Composing the v4.84 section followed by this labelled realization recovers every
realized one-cell and two-cell exactly (propositionally in the induced wrappers,
with underlying DO2 cells definitionally unchanged).  This is the cellwise
right-inverse direction needed before constructing global pseudonatural
unit/counit data.

No object coverage of all DO2 objects, no final biequivalence, and no
independently prescribed raw component is asserted here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The strict realization core into the object-labelled realized sector. -/
def exactUniversalLabelledRealizationStrictCore :
    StrictPseudofunctorCore
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A) where
  obj X := X
  map {X Y} f :=
    Bicategory.InducedBicategory.mkHom (X := X) (Y := Y) f.lift
  map_id X := rfl
  map₂ {X Y} {f g} eta :=
    Bicategory.InducedBicategory.mkHom₂ eta.lift
  map₂_id f := rfl
  map₂_comp eta theta := rfl
  map_comp f g := rfl
  map₂_whisker_left {X Y Z} f {g h} eta := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change (f ◁ eta).lift =
      𝟙 (f.lift ≫ g.lift) ≫
        (f.lift ◁ eta.lift) ≫ 𝟙 (f.lift ≫ h.lift)
    exact
      (exactUniversalRealization_source_whiskerLeft_lift
        (W := W) A f eta).trans
        ((Category.id_comp _).trans (Category.comp_id _)).symm
  map₂_whisker_right {X Y Z} {f g} eta h := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change (eta ▷ h).lift =
      𝟙 (f.lift ≫ h.lift) ≫
        (eta.lift ▷ h.lift) ≫ 𝟙 (g.lift ≫ h.lift)
    exact
      (exactUniversalRealization_source_whiskerRight_lift
        (W := W) A eta h).trans
        ((Category.id_comp _).trans (Category.comp_id _)).symm
  map₂_left_unitor {X Y} f := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change (λ_ f).hom.lift =
      𝟙 (𝟙 X.carrier ≫ f.lift) ≫ (λ_ f.lift).hom
    exact
      (exactUniversalRealization_source_leftUnitor_lift
        (W := W) A f).trans (Category.id_comp _).symm
  map₂_right_unitor {X Y} f := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change (ρ_ f).hom.lift =
      𝟙 (f.lift ≫ 𝟙 Y.carrier) ≫ (ρ_ f.lift).hom
    exact
      (exactUniversalRealization_source_rightUnitor_lift
        (W := W) A f).trans (Category.id_comp _).symm
  map₂_associator {V X Y Z} f g h := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change (α_ f g h).hom.lift =
      𝟙 ((f.lift ≫ g.lift) ≫ h.lift) ≫
        (α_ f.lift g.lift h.lift).hom ≫
          𝟙 (f.lift ≫ (g.lift ≫ h.lift))
    exact
      (exactUniversalRealization_source_associator_lift
        (W := W) A f g h).trans
        ((Category.id_comp _).trans (Category.comp_id _)).symm

/-- Label-preserving strict realization from the source to its realized sector. -/
def exactUniversalLabelledRealization :
    StrictPseudofunctor
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A) :=
  StrictPseudofunctor.mk'
    (exactUniversalLabelledRealizationStrictCore (W := W) A)

@[simp] theorem exactUniversalLabelledRealization_obj
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalLabelledRealization (W := W) A).obj X = X := rfl

@[simp] theorem exactUniversalLabelledRealization_map_hom
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (f : X ⟶ Y) :
    ((exactUniversalLabelledRealization (W := W) A).map f).hom = f.lift := rfl

@[simp] theorem exactUniversalLabelledRealization_map₂_hom
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((exactUniversalLabelledRealization (W := W) A).map₂ eta).hom = eta.lift := rfl

@[simp] theorem exactUniversalLabelledRealization_map_id
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalLabelledRealization (W := W) A).map (𝟙 X) =
      𝟙 ((exactUniversalLabelledRealization (W := W) A).obj X) := rfl

@[simp] theorem exactUniversalLabelledRealization_map_comp
    {X Y Z : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (exactUniversalLabelledRealization (W := W) A).map (f ≫ g) =
      (exactUniversalLabelledRealization (W := W) A).map f ≫
        (exactUniversalLabelledRealization (W := W) A).map g := rfl

/-! ## Exact section-realization round trip on the realized sector -/

variable {X Y : ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A}

@[simp] theorem exactUniversalLabelledRealization_section_obj :
    (exactUniversalLabelledRealization (W := W) A).obj
      ((exactUniversalSectionPseudofunctor (W := W) A).obj X) = X := rfl

@[simp] theorem exactUniversalLabelledRealization_section_map
    (f : X ⟶ Y) :
    (exactUniversalLabelledRealization (W := W) A).map
      ((exactUniversalSectionPseudofunctor (W := W) A).map f) = f := by
  apply Bicategory.InducedBicategory.hom_ext
  rfl

@[simp] theorem exactUniversalLabelledRealization_section_map₂
    {f g : X ⟶ Y} (eta : f ⟶ g) :
    (exactUniversalLabelledRealization (W := W) A).map₂
      ((exactUniversalSectionPseudofunctor (W := W) A).map₂ eta) = eta := by
  apply Bicategory.InducedBicategory.hom₂_ext
  rfl

/-- The local section-realization composite is the identity functor on every
realized hom category. This packages both preceding exact recovery laws. -/
theorem exactUniversalLabelledHomRoundtrip
    (X Y : ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A) :
    (exactUniversalSectionPseudofunctor (W := W) A).mapFunctor X Y ⋙
      (exactUniversalLabelledRealization (W := W) A).mapFunctor X Y =
        𝟭 (X ⟶ Y) := by
  apply CategoryTheory.Functor.hext
  · intro f
    exact exactUniversalLabelledRealization_section_map (W := W) A f
  · intro f g eta
    exact HEq.of_eq
      (exactUniversalLabelledRealization_section_map₂ (W := W) A eta)

/-! ## Regression checks -/

example :
    StrictPseudofunctor
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A) :=
  exactUniversalLabelledRealization (W := W) A

example (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalLabelledRealization (W := W) A).obj X = X := rfl

example
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (f : X ⟶ Y) :
    ((exactUniversalLabelledRealization (W := W) A).map f).hom = f.lift := rfl

example
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((exactUniversalLabelledRealization (W := W) A).map₂ eta).hom = eta.lift := rfl

example (f : X ⟶ Y) :
    (exactUniversalLabelledRealization (W := W) A).map
      ((exactUniversalSectionPseudofunctor (W := W) A).map f) = f :=
  exactUniversalLabelledRealization_section_map (W := W) A f

example {f g : X ⟶ Y} (eta : f ⟶ g) :
    (exactUniversalLabelledRealization (W := W) A).map₂
      ((exactUniversalSectionPseudofunctor (W := W) A).map₂ eta) = eta :=
  exactUniversalLabelledRealization_section_map₂ (W := W) A eta

example :
    (exactUniversalSectionPseudofunctor (W := W) A).mapFunctor X Y ⋙
      (exactUniversalLabelledRealization (W := W) A).mapFunctor X Y =
        𝟭 (X ⟶ Y) :=
  exactUniversalLabelledHomRoundtrip (W := W) A X Y

#print axioms exactUniversalLabelledRealizationStrictCore
#print axioms exactUniversalLabelledRealization
#print axioms exactUniversalLabelledRealization_map_hom
#print axioms exactUniversalLabelledRealization_section_map
#print axioms exactUniversalLabelledRealization_section_map₂
#print axioms exactUniversalLabelledHomRoundtrip

end

end KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85
