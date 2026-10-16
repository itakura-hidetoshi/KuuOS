import KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12

namespace KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
open KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient roundtrip counit v5.13

v5.12 constructs a genuine pseudofunctor from the ambient completion back to
the exact-universal source.  Composing it with the strict exact-universal
realization gives an ambient endopseudofunctor.

The v5.11/v5.12 section was deliberately chosen so that, after realization,
objects, one-cells, and two-cells recover the prescribed ambient data exactly.
The only nontrivial structure left in the composite is therefore the
pseudofunctor identity/composition comparison.  Those comparison cells project
to identities, so the StrongTrans counit to the identity pseudofunctor reduces
to native bicategory coherence.

No new choice of source label or local lift is introduced here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

/-- Ambient roundtrip: canonical section followed by strict realization. -/
noncomputable def exactUniversalAmbientRoundtrip :
    Pseudofunctor (Ambient (W := W) A) (Ambient (W := W) A) :=
  Pseudofunctor.comp
    (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)
    (exactUniversalRealization (W := W) A).toPseudofunctor

@[simp] theorem exactUniversalAmbientRoundtrip_obj
    (Z : Ambient (W := W) A) :
    (exactUniversalAmbientRoundtrip (W := W) A).obj Z = Z := by
  exact
    exactUniversalAmbientCanonicalSectionPseudofunctor_obj_realization
      (W := W) A Z

/-- The ambient roundtrip recovers every one-cell exactly. -/
@[simp] theorem exactUniversalAmbientRoundtrip_map
    {X Y : Ambient (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalAmbientRoundtrip (W := W) A).map f = f := by
  change
    (exactUniversalRealization (W := W) A).map
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).map f) = f
  rw [exactUniversalRealization_map,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift]

/-- The ambient roundtrip recovers every two-cell exactly. -/
@[simp] theorem exactUniversalAmbientRoundtrip_map₂
    {X Y : Ambient (W := W) A}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    (exactUniversalAmbientRoundtrip (W := W) A).map₂ eta = eta := by
  change
    (exactUniversalRealization (W := W) A).map₂
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).map₂ eta) = eta
  rw [exactUniversalRealization_map₂,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift]

/-- Identity comparison of the ambient roundtrip is the identity 2-cell. -/
@[simp] theorem exactUniversalAmbientRoundtrip_mapId_hom
    (X : Ambient (W := W) A) :
    ((exactUniversalAmbientRoundtrip (W := W) A).mapId X).hom =
      𝟙 (𝟙 X) := by
  change
    (exactUniversalAmbientSectionIdIso (W := W) A X).hom.lift ≫
      𝟙 (𝟙 X) =
        𝟙 (𝟙 X)
  rw [exactUniversalAmbientSectionIdIso_hom_lift]
  exact Category.comp_id _

/-- Composition comparison of the ambient roundtrip is the identity 2-cell. -/
@[simp] theorem exactUniversalAmbientRoundtrip_mapComp_hom
    {X Y Z : Ambient (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalAmbientRoundtrip (W := W) A).mapComp f g).hom =
      𝟙 (f ≫ g) := by
  change
    (exactUniversalAmbientSectionCompIso (W := W) A f g).hom.lift ≫
      𝟙 (f ≫ g) =
        𝟙 (f ≫ g)
  rw [exactUniversalAmbientSectionCompIso_hom_lift]
  exact Category.comp_id _

/-- The identity pseudofunctor preserves ambient one-cells. -/
@[simp] theorem exactUniversalAmbientIdentityPseudofunctor_map
    {X Y : Ambient (W := W) A}
    (f : X ⟶ Y) :
    (Pseudofunctor.id (Ambient (W := W) A)).map f = f := by
  rfl

/-- The identity pseudofunctor preserves ambient two-cells. -/
@[simp] theorem exactUniversalAmbientIdentityPseudofunctor_map₂
    {X Y : Ambient (W := W) A}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    (Pseudofunctor.id (Ambient (W := W) A)).map₂ eta = eta := by
  rfl

@[simp] theorem exactUniversalAmbientIdentityPseudofunctor_mapId_hom
    (X : Ambient (W := W) A) :
    ((Pseudofunctor.id (Ambient (W := W) A)).mapId X).hom =
      𝟙 (𝟙 X) := by
  rfl

@[simp] theorem exactUniversalAmbientIdentityPseudofunctor_mapComp_hom
    {X Y Z : Ambient (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((Pseudofunctor.id (Ambient (W := W) A)).mapComp f g).hom =
      𝟙 (f ≫ g) := by
  rfl

/-- Naturality isomorphism for the ambient counit. -/
noncomputable def exactUniversalAmbientRoundtripNaturalityIso
    {X Y : Ambient (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalAmbientRoundtrip (W := W) A).map f ≫ 𝟙 Y ≅
      𝟙 X ≫ f := by
  rw [exactUniversalAmbientRoundtrip_map]
  exact (ρ_ f) ≪≫ (λ_ f).symm

@[simp] theorem exactUniversalAmbientRoundtripNaturalityIso_hom
    {X Y : Ambient (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalAmbientRoundtripNaturalityIso
      (W := W) A f).hom =
      (ρ_ f).hom ≫ (λ_ f).inv := by
  change
    (ρ_ f).hom ≫ (λ_ f).inv =
      (ρ_ f).hom ≫ (λ_ f).inv
  rfl

/-- The ambient roundtrip admits a native StrongTrans counit to identity. -/
noncomputable def exactUniversalAmbientRoundtripCounit :
    Pseudofunctor.StrongTrans
      (exactUniversalAmbientRoundtrip (W := W) A)
      (Pseudofunctor.id (Ambient (W := W) A)) where
  app X := 𝟙 X
  naturality f :=
    exactUniversalAmbientRoundtripNaturalityIso (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    rw [exactUniversalAmbientRoundtrip_map₂,
      exactUniversalAmbientIdentityPseudofunctor_map₂,
      exactUniversalAmbientRoundtripNaturalityIso_hom,
      exactUniversalAmbientRoundtripNaturalityIso_hom]
    bicategory
  naturality_id X := by
    rw [exactUniversalAmbientRoundtripNaturalityIso_hom,
      exactUniversalAmbientIdentityPseudofunctor_mapId_hom,
      exactUniversalAmbientRoundtrip_mapId_hom]
    bicategory
  naturality_comp {a b c} f g := by
    rw [exactUniversalAmbientRoundtripNaturalityIso_hom,
      exactUniversalAmbientRoundtripNaturalityIso_hom,
      exactUniversalAmbientRoundtripNaturalityIso_hom,
      exactUniversalAmbientIdentityPseudofunctor_mapComp_hom,
      exactUniversalAmbientRoundtrip_mapComp_hom]
    bicategory

@[simp] theorem exactUniversalAmbientRoundtripCounit_app
    (X : Ambient (W := W) A) :
    (exactUniversalAmbientRoundtripCounit (W := W) A).app X =
      𝟙 X := by
  rfl

theorem exactUniversalAmbientRoundtripCounit_naturality
    {X Y : Ambient (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalAmbientRoundtripCounit (W := W) A).naturality f =
      exactUniversalAmbientRoundtripNaturalityIso (W := W) A f := by
  rfl

/-! ## Regression checks -/

#print axioms exactUniversalAmbientRoundtrip
#print axioms exactUniversalAmbientRoundtrip_obj
#print axioms exactUniversalAmbientRoundtrip_map
#print axioms exactUniversalAmbientRoundtrip_map₂
#print axioms exactUniversalAmbientRoundtrip_mapId_hom
#print axioms exactUniversalAmbientRoundtrip_mapComp_hom
#print axioms exactUniversalAmbientRoundtripNaturalityIso
#print axioms exactUniversalAmbientRoundtripCounit
#print axioms exactUniversalAmbientRoundtripCounit_app
#print axioms exactUniversalAmbientRoundtripCounit_naturality

end

end KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13
