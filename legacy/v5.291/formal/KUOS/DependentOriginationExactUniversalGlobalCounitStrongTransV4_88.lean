import KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87

namespace KUOS.DependentOriginationExactUniversalGlobalCounitStrongTransV4_88

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
open KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85
open KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Global realized-roundtrip counit StrongTrans v4.88

v4.85 proved exact cellwise recovery after applying the section and then the
label-preserving realization.  v4.87 closed the opposite source-side global
unit as a native Mathlib StrongTrans.

This file packages the realized-side recovery globally.  We form the actual
composite pseudofunctor

  RealizedSector --section--> Source --labelled realization--> RealizedSector

and construct a native StrongTrans

  realizedRoundtrip ⟶ Id_RealizedSector.

The object components are identities.  For each realized one-cell f, the
middle comparison is the identity DO₂ 2-isomorphism between the two induced
wrappers, because the roundtrip preserves the underlying DO₂ one-cell
definitionally.  The StrongTrans naturality, identity, and composition laws
then reduce directly to native bicategory coherence after
`Bicategory.InducedBicategory.hom₂_ext`.

No ambient DO₂ object coverage and no final biequivalence are asserted here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Realized :=
  ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A

/-- The actual realized-side composite: section followed by labelled
realization. -/
def exactUniversalRealizedRoundtrip :
    Pseudofunctor (Realized (W := W) A) (Realized (W := W) A) :=
  Pseudofunctor.comp
    (exactUniversalSectionPseudofunctor (W := W) A)
    (exactUniversalLabelledRealization (W := W) A).toPseudofunctor

@[simp] theorem exactUniversalRealizedRoundtrip_obj
    (X : Realized (W := W) A) :
    (exactUniversalRealizedRoundtrip (W := W) A).obj X = X := rfl

/-- The realized roundtrip preserves every underlying DO₂ one-cell
definitionally. -/
@[simp] theorem exactUniversalRealizedRoundtrip_map_hom
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    ((exactUniversalRealizedRoundtrip (W := W) A).map f).hom = f.hom := by
  rfl

/-- The realized roundtrip preserves every underlying DO₂ two-cell
definitionally. -/
@[simp] theorem exactUniversalRealizedRoundtrip_map₂_hom
    {X Y : Realized (W := W) A} {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((exactUniversalRealizedRoundtrip (W := W) A).map₂ eta).hom = eta.hom := by
  rfl

/-- Vertical composition in the induced hom category is exactly vertical
composition of the underlying DO₂ cells. -/
@[simp] theorem exactUniversalRealizedTwoCell_comp_hom
    {X Y : Realized (W := W) A} {f g h : X ⟶ Y}
    (eta : f ⟶ g) (theta : g ⟶ h) :
    (eta ≫ theta).hom = eta.hom ≫ theta.hom := rfl

/-- The identity pseudofunctor preserves the underlying realized one-cell. -/
@[simp] theorem exactUniversalRealizedIdentityPseudofunctor_map_hom
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    ((Pseudofunctor.id (Realized (W := W) A)).map f).hom = f.hom := by
  rfl

/-- The identity pseudofunctor preserves the underlying realized two-cell. -/
@[simp] theorem exactUniversalRealizedIdentityPseudofunctor_map₂_hom
    {X Y : Realized (W := W) A} {f g : X ⟶ Y} (eta : f ⟶ g) :
    ((Pseudofunctor.id (Realized (W := W) A)).map₂ eta).hom = eta.hom := by
  rfl

/-- The identity pseudofunctor's identity comparison is underlying identity. -/
@[simp] theorem exactUniversalRealizedIdentityPseudofunctor_mapId_hom_hom
    (X : Realized (W := W) A) :
    ((Pseudofunctor.id (Realized (W := W) A)).mapId X).hom.hom =
      𝟙 (𝟙 X.carrier) := by
  rfl

/-- The identity pseudofunctor's composition comparison is underlying
identity. -/
@[simp] theorem exactUniversalRealizedIdentityPseudofunctor_mapComp_hom_hom
    {X Y Z : Realized (W := W) A} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((Pseudofunctor.id (Realized (W := W) A)).mapComp f g).hom.hom =
      𝟙 (f.hom ≫ g.hom) := by
  rfl

/-- The realized roundtrip identity comparison projects to the identity DO₂
2-cell. -/
@[simp] theorem exactUniversalRealizedRoundtrip_mapId_hom_hom
    (X : Realized (W := W) A) :
    ((exactUniversalRealizedRoundtrip (W := W) A).mapId X).hom.hom =
      𝟙 (𝟙 X.carrier) := by
  change
    ((exactUniversalLabelledRealization (W := W) A).map₂
        ((exactUniversalSectionPseudofunctor (W := W) A).mapId X).hom).hom ≫
      ((exactUniversalLabelledRealization (W := W) A).mapId X).hom.hom =
        𝟙 (𝟙 X.carrier)
  rw [exactUniversalLabelledRealization_map₂_hom,
    exactUniversalSectionPseudofunctor_mapId_hom_lift,
    exactUniversalLabelledRealization_mapId_hom_hom]
  exact Category.comp_id _

/-- The realized roundtrip composition comparison projects to identity. -/
@[simp] theorem exactUniversalRealizedRoundtrip_mapComp_hom_hom
    {X Y Z : Realized (W := W) A} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalRealizedRoundtrip (W := W) A).mapComp f g).hom.hom =
      𝟙 (f.hom ≫ g.hom) := by
  change
    ((exactUniversalLabelledRealization (W := W) A).map₂
        ((exactUniversalSectionPseudofunctor (W := W) A).mapComp f g).hom).hom ≫
      ((exactUniversalLabelledRealization (W := W) A).mapComp
        ((exactUniversalSectionPseudofunctor (W := W) A).map f)
        ((exactUniversalSectionPseudofunctor (W := W) A).map g)).hom.hom =
          𝟙 (f.hom ≫ g.hom)
  rw [exactUniversalLabelledRealization_map₂_hom,
    exactUniversalSectionPseudofunctor_mapComp_hom_lift,
    exactUniversalLabelledRealization_mapComp_hom_hom]
  change
    (𝟙 (f.hom ≫ g.hom)) ≫ 𝟙 (f.hom ≫ g.hom) =
      𝟙 (f.hom ≫ g.hom)
  exact Category.comp_id _

/-- The exact cellwise recovery gives an isomorphism from the actual realized
roundtrip image of f back to f itself. -/
def exactUniversalRealizedRoundtripCoreIso
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    (exactUniversalRealizedRoundtrip (W := W) A).map f ≅ f :=
  Bicategory.InducedBicategory.isoMk (Iso.refl f.hom)

@[simp] theorem exactUniversalRealizedRoundtripCoreIso_hom_hom
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    (exactUniversalRealizedRoundtripCoreIso (W := W) A f).hom.hom =
      𝟙 f.hom := by
  rfl

@[simp] theorem exactUniversalRealizedRoundtripCoreIso_inv_hom
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    (exactUniversalRealizedRoundtripCoreIso (W := W) A f).inv.hom =
      𝟙 f.hom := by
  rfl

/-- Naturality-shaped cell for the realized-side counit. -/
def exactUniversalRealizedRoundtripNaturalityIso
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    (exactUniversalRealizedRoundtrip (W := W) A).map f ≫ 𝟙 Y ≅
      𝟙 X ≫ f :=
  (ρ_ ((exactUniversalRealizedRoundtrip (W := W) A).map f)) ≪≫
    exactUniversalRealizedRoundtripCoreIso (W := W) A f ≪≫
      (λ_ f).symm

@[simp] theorem exactUniversalRealizedRoundtripNaturalityIso_hom_hom
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    (exactUniversalRealizedRoundtripNaturalityIso (W := W) A f).hom.hom =
      (ρ_ f.hom).hom ≫ (λ_ f.hom).inv := by
  -- Do not rewrite `roundtrip.map f).hom = f.hom` inside the dependent
  -- source/target of the following 2-cell composition.  Both equalities used
  -- here are definitional, so normalize the whole typed expression at once.
  change
    (ρ_ f.hom).hom ≫ 𝟙 f.hom ≫ (λ_ f.hom).inv =
      (ρ_ f.hom).hom ≫ (λ_ f.hom).inv
  simp only [Category.id_comp]

/-- The realized-side exact recovery is a global native StrongTrans counit. -/
def exactUniversalRealizedRoundtripCounit :
    Pseudofunctor.StrongTrans
      (exactUniversalRealizedRoundtrip (W := W) A)
      (Pseudofunctor.id (Realized (W := W) A)) where
  app X := 𝟙 X
  naturality f :=
    exactUniversalRealizedRoundtripNaturalityIso (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change
      (((exactUniversalRealizedRoundtrip (W := W) A).map₂ eta).hom ▷
          𝟙 b.carrier) ≫
        (exactUniversalRealizedRoundtripNaturalityIso (W := W) A g).hom.hom =
      (exactUniversalRealizedRoundtripNaturalityIso (W := W) A f).hom.hom ≫
        (𝟙 a.carrier ◁
          ((Pseudofunctor.id (Realized (W := W) A)).map₂ eta).hom)
    rw [exactUniversalRealizedRoundtrip_map₂_hom,
      exactUniversalRealizedRoundtripNaturalityIso_hom_hom,
      exactUniversalRealizedRoundtripNaturalityIso_hom_hom,
      exactUniversalRealizedIdentityPseudofunctor_map₂_hom]
    bicategory
  naturality_id X := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change
      (exactUniversalRealizedRoundtripNaturalityIso (W := W) A (𝟙 X)).hom.hom ≫
          (𝟙 X.carrier ◁
            ((Pseudofunctor.id (Realized (W := W) A)).mapId X).hom.hom) =
        ((exactUniversalRealizedRoundtrip (W := W) A).mapId X).hom.hom ▷
            𝟙 X.carrier ≫
          (λ_ (𝟙 X.carrier)).hom ≫ (ρ_ (𝟙 X.carrier)).inv
    rw [exactUniversalRealizedRoundtripNaturalityIso_hom_hom,
      exactUniversalRealizedIdentityPseudofunctor_mapId_hom_hom,
      exactUniversalRealizedRoundtrip_mapId_hom_hom]
    bicategory
  naturality_comp {a b c} f g := by
    apply Bicategory.InducedBicategory.hom₂_ext
    change
      (exactUniversalRealizedRoundtripNaturalityIso
          (W := W) A (f ≫ g)).hom.hom ≫
          (𝟙 a.carrier ◁
            ((Pseudofunctor.id (Realized (W := W) A)).mapComp f g).hom.hom) =
        ((exactUniversalRealizedRoundtrip (W := W) A).mapComp f g).hom.hom ▷
            𝟙 c.carrier ≫
          (α_
            ((exactUniversalRealizedRoundtrip (W := W) A).map f).hom
            ((exactUniversalRealizedRoundtrip (W := W) A).map g).hom
            (𝟙 c.carrier)).hom ≫
          ((exactUniversalRealizedRoundtrip (W := W) A).map f).hom ◁
            (exactUniversalRealizedRoundtripNaturalityIso
              (W := W) A g).hom.hom ≫
          (α_
            ((exactUniversalRealizedRoundtrip (W := W) A).map f).hom
            (𝟙 b.carrier)
            ((Pseudofunctor.id (Realized (W := W) A)).map g).hom).inv ≫
          (exactUniversalRealizedRoundtripNaturalityIso
              (W := W) A f).hom.hom ▷
            ((Pseudofunctor.id (Realized (W := W) A)).map g).hom ≫
          (α_
            (𝟙 a.carrier)
            ((Pseudofunctor.id (Realized (W := W) A)).map f).hom
            ((Pseudofunctor.id (Realized (W := W) A)).map g).hom).hom
    rw [
      exactUniversalRealizedRoundtripNaturalityIso_hom_hom
        (W := W) A (f ≫ g),
      exactUniversalRealizedRoundtripNaturalityIso_hom_hom
        (W := W) A g,
      exactUniversalRealizedRoundtripNaturalityIso_hom_hom
        (W := W) A f,
      exactUniversalRealizedIdentityPseudofunctor_mapComp_hom_hom,
      exactUniversalRealizedRoundtrip_mapComp_hom_hom]
    -- At this point only the underlying one-cell maps remain inside dependent
    -- associator/whiskering arguments.  Simplification is deliberately
    -- inside-out here; unlike `rw`, it can normalize these dependent
    -- subterms without constructing an ill-typed global rewrite motive.
    simp only [
      exactUniversalRealizedRoundtrip_map_hom,
      exactUniversalRealizedIdentityPseudofunctor_map_hom,
      CategoryTheory.Bicategory.InducedBicategory.bicategory_comp_hom]
    bicategory

@[simp] theorem exactUniversalRealizedRoundtripCounit_app
    (X : Realized (W := W) A) :
    (exactUniversalRealizedRoundtripCounit (W := W) A).app X = 𝟙 X := rfl

theorem exactUniversalRealizedRoundtripCounit_naturality
    {X Y : Realized (W := W) A} (f : X ⟶ Y) :
    (exactUniversalRealizedRoundtripCounit (W := W) A).naturality f =
      exactUniversalRealizedRoundtripNaturalityIso (W := W) A f := rfl

/-! ## Regression checks -/

variable {X Y : Realized (W := W) A}

example :
    Pseudofunctor.StrongTrans
      (exactUniversalRealizedRoundtrip (W := W) A)
      (Pseudofunctor.id (Realized (W := W) A)) :=
  exactUniversalRealizedRoundtripCounit (W := W) A

example (f : X ⟶ Y) :
    (exactUniversalRealizedRoundtripNaturalityIso (W := W) A f).hom.hom =
      (ρ_ f.hom).hom ≫ (λ_ f.hom).inv :=
  exactUniversalRealizedRoundtripNaturalityIso_hom_hom (W := W) A f

#print axioms exactUniversalRealizedRoundtrip
#print axioms exactUniversalRealizedRoundtrip_map_hom
#print axioms exactUniversalRealizedRoundtrip_map₂_hom
#print axioms exactUniversalRealizedRoundtrip_mapId_hom_hom
#print axioms exactUniversalRealizedRoundtrip_mapComp_hom_hom
#print axioms exactUniversalRealizedRoundtripCoreIso
#print axioms exactUniversalRealizedRoundtripNaturalityIso
#print axioms exactUniversalRealizedRoundtripCounit
#print axioms exactUniversalRealizedRoundtripCounit_app
#print axioms exactUniversalRealizedRoundtripCounit_naturality

end

end KUOS.DependentOriginationExactUniversalGlobalCounitStrongTransV4_88
