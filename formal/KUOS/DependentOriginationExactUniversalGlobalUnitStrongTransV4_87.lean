import KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86

namespace KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
open KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85
open KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Global source-roundtrip unit StrongTrans v4.87

v4.86 constructed the actual source roundtrip pseudofunctor and the naturality-
shaped isomorphism

  f ≫ 𝟙 Y ≅ 𝟙 X ≫ roundtrip.map f.

This file closes the next coherence layer: those object components and one-cell
squares are bundled into a native Mathlib `Pseudofunctor.StrongTrans`

  Id_Source ⟶ roundtrip.

The proof boundary is deliberately narrow.  The roundtrip structural cells are
first projected to DO₂.  The section comparison cells project to identities,
so naturality in 2-cells and compatibility with identity/composition reduce to
native bicategory unitor/associator coherence.  Faithfulness of exact
realization then reflects the resulting equalities back to the source.

This still does not assert ambient DO₂ object coverage, the realized-side global
counit, a final biequivalence, semantic admissibility equivalence, or
independently prescribed raw components.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

/-- The source roundtrip preserves the realized component of every 2-cell
exactly. -/
@[simp] theorem exactUniversalSourceRoundtrip_map₂_lift
    {X Y : Source (W := W) A} {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((exactUniversalSourceRoundtrip (W := W) A).map₂ eta).lift = eta.lift := by
  rfl

/-- The identity comparison of the source roundtrip realizes to the identity
2-cell on the DO₂ identity. -/
@[simp] theorem exactUniversalSourceRoundtrip_mapId_hom_lift
    (X : Source (W := W) A) :
    ((exactUniversalSourceRoundtrip (W := W) A).mapId X).hom.lift =
      𝟙 (𝟙 X.carrier) := by
  change
    (((exactUniversalSectionPseudofunctor (W := W) A).map₂
        ((exactUniversalLabelledRealization (W := W) A).toPseudofunctor.mapId X).hom) ≫
      ((exactUniversalSectionPseudofunctor (W := W) A).mapId X).hom).lift =
        𝟙 (𝟙 X.carrier)
  rw [ExactUniversalRawMorphismTwoCell.comp_lift,
    exactUniversalSectionPseudofunctor_map₂_lift,
    exactUniversalSectionIdIso_hom_lift]
  simp [exactUniversalLabelledRealization,
    exactUniversalLabelledRealizationStrictCore]

/-- The composition comparison of the source roundtrip realizes to the identity
2-cell on the realized composite. -/
@[simp] theorem exactUniversalSourceRoundtrip_mapComp_hom_lift
    {X Y Z : Source (W := W) A} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalSourceRoundtrip (W := W) A).mapComp f g).hom.lift =
      𝟙 (f.lift ≫ g.lift) := by
  change
    (((exactUniversalSectionPseudofunctor (W := W) A).map₂
        ((exactUniversalLabelledRealization (W := W) A).toPseudofunctor.mapComp f g).hom) ≫
      ((exactUniversalSectionPseudofunctor (W := W) A).mapComp
        ((exactUniversalLabelledRealization (W := W) A).map f)
        ((exactUniversalLabelledRealization (W := W) A).map g)).hom).lift =
          𝟙 (f.lift ≫ g.lift)
  rw [ExactUniversalRawMorphismTwoCell.comp_lift,
    exactUniversalSectionPseudofunctor_map₂_lift,
    exactUniversalSectionCompIso_hom_lift]
  simp [exactUniversalLabelledRealization,
    exactUniversalLabelledRealizationStrictCore]

/-- The v4.86 unit components and squares satisfy all three native StrongTrans
coherence laws. -/
def exactUniversalSourceRoundtripUnit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id (Source (W := W) A))
      (exactUniversalSourceRoundtrip (W := W) A) where
  app X := 𝟙 X
  naturality f :=
    exactUniversalSourceRoundtripNaturalityIso (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    change
      (eta.lift ▷ 𝟙 b.carrier) ≫
          (exactUniversalSourceRoundtripNaturalityIso (W := W) A g).hom.lift =
        (exactUniversalSourceRoundtripNaturalityIso (W := W) A f).hom.lift ≫
          (𝟙 a.carrier ◁
            ((exactUniversalSourceRoundtrip (W := W) A).map₂ eta).lift)
    rw [exactUniversalSourceRoundtripNaturalityIso_hom_lift,
      exactUniversalSourceRoundtripNaturalityIso_hom_lift,
      exactUniversalSourceRoundtrip_map₂_lift]
    simp only [Category.assoc, Bicategory.rightUnitor_naturality_assoc,
      Bicategory.leftUnitor_inv_naturality]
  naturality_id X := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    rw [ExactUniversalRawMorphismTwoCell.comp_lift,
      exactUniversalSourceRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceRoundtrip_mapId_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalRealization_source_leftUnitor_lift,
      exactUniversalRealization_source_rightUnitor_inv_lift]
    change
      ((ρ_ (𝟙 X.carrier)).hom ≫ (λ_ (𝟙 X.carrier)).inv) ≫
          (𝟙 X.carrier ◁ 𝟙 (𝟙 X.carrier)) =
        (𝟙 (𝟙 X.carrier) ▷ 𝟙 X.carrier) ≫
          (λ_ (𝟙 X.carrier)).hom ≫ (ρ_ (𝟙 X.carrier)).inv
    bicategory
  naturality_comp {a b c} f g := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    rw [ExactUniversalRawMorphismTwoCell.comp_lift,
      exactUniversalSourceRoundtripNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalSourceRoundtrip_mapComp_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalRealization_source_associator_lift]
    change
      ((ρ_ (f.lift ≫ g.lift)).hom ≫ (λ_ (f.lift ≫ g.lift)).inv) ≫
          (𝟙 a.carrier ◁ 𝟙 (f.lift ≫ g.lift)) =
        (𝟙 (f.lift ≫ g.lift) ▷ 𝟙 c.carrier) ≫
          (α_ f.lift g.lift (𝟙 c.carrier)).hom ≫
          f.lift ◁ ((ρ_ g.lift).hom ≫ (λ_ g.lift).inv) ≫
          (α_ f.lift (𝟙 b.carrier) g.lift).inv ≫
          ((ρ_ f.lift).hom ≫ (λ_ f.lift).inv) ▷ g.lift ≫
          (α_ (𝟙 a.carrier) f.lift g.lift).hom
    bicategory

@[simp] theorem exactUniversalSourceRoundtripUnit_app
    (X : Source (W := W) A) :
    (exactUniversalSourceRoundtripUnit (W := W) A).app X = 𝟙 X := rfl

theorem exactUniversalSourceRoundtripUnit_naturality
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalSourceRoundtripUnit (W := W) A).naturality f =
      exactUniversalSourceRoundtripNaturalityIso (W := W) A f := rfl

/-! ## Regression checks -/

variable {X Y : Source (W := W) A}

example :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id (Source (W := W) A))
      (exactUniversalSourceRoundtrip (W := W) A) :=
  exactUniversalSourceRoundtripUnit (W := W) A

example (f : X ⟶ Y) :
    ((exactUniversalSourceRoundtripUnit (W := W) A).naturality f).hom.lift =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv :=
  exactUniversalSourceRoundtripNaturalityIso_hom_lift (W := W) A f

#print axioms exactUniversalSourceRoundtrip_map₂_lift
#print axioms exactUniversalSourceRoundtrip_mapId_hom_lift
#print axioms exactUniversalSourceRoundtrip_mapComp_hom_lift
#print axioms exactUniversalSourceRoundtripUnit
#print axioms exactUniversalSourceRoundtripUnit_app
#print axioms exactUniversalSourceRoundtripUnit_naturality

end

end KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87
