import KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15

namespace KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
open KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86
open KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
open KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12
open KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13
open KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14
open KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient triangle coherence v5.16

v5.15 packages the strict exact-universal realization `F`, its canonical ambient
section `G`, the source unit `η : Id ⟶ F ≫ G`, and the ambient counit
`ε : G ≫ F ⟶ Id`.

This file adds the two triangle coherences without introducing any new choice.
Because Mathlib does not currently package horizontal composition of
pseudonatural transformations as a tricategory, we expose the two triangle
composites directly by their canonical object components:

* forward side: `F.map (η.app X) ≫ ε.app (F.obj X)`;
* quasi-inverse side: `η.app (G.obj Z) ≫ G.map (ε.app Z)`.

The forward component is literally the ambient identity after the existing
projection theorems.  The quasi-inverse component realizes to the ambient
identity; local full faithfulness of exact realization then lifts the canonical
ambient coherence uniquely to the source.  Both families are bundled as native
Mathlib `StrongTrans` and then as invertible modifications to the corresponding
identity StrongTrans.

No weak-W exact-presentation implication is used or asserted.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

/-! ## Forward triangle -/

/-- Object component of the forward triangle composite `Fη ; εF`. -/
noncomputable def exactUniversalForwardTriangleApp
    (X : Source (W := W) A) :
    (exactUniversalRealization (W := W) A).obj X ⟶
      (exactUniversalRealization (W := W) A).obj X :=
  (exactUniversalRealization (W := W) A).map
      ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X) ≫
    (exactUniversalAmbientRoundtripCounit (W := W) A).app
      ((exactUniversalRealization (W := W) A).obj X)

/-- The forward triangle component is exactly the ambient identity. -/
@[simp] theorem exactUniversalForwardTriangleApp_eq_id
    (X : Source (W := W) A) :
    exactUniversalForwardTriangleApp (W := W) A X =
      𝟙 ((exactUniversalRealization (W := W) A).obj X) := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X).lift ≫
      (exactUniversalAmbientRoundtripCounit (W := W) A).app X.carrier =
        𝟙 X.carrier
  rw [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientRoundtripCounit_app]
  exact Category.comp_id _

/-- Naturality square for the forward triangle family. -/
noncomputable def exactUniversalForwardTriangleNaturalityIso
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalRealization (W := W) A).map f ≫
        exactUniversalForwardTriangleApp (W := W) A Y ≅
      exactUniversalForwardTriangleApp (W := W) A X ≫
        (exactUniversalRealization (W := W) A).map f := by
  rw [exactUniversalForwardTriangleApp_eq_id,
    exactUniversalForwardTriangleApp_eq_id]
  exact
    (ρ_ ((exactUniversalRealization (W := W) A).map f)) ≪≫
      (λ_ ((exactUniversalRealization (W := W) A).map f)).symm

@[simp] theorem exactUniversalForwardTriangleNaturalityIso_hom
    {X Y : Source (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalForwardTriangleNaturalityIso (W := W) A f).hom =
      (ρ_ ((exactUniversalRealization (W := W) A).map f)).hom ≫
        (λ_ ((exactUniversalRealization (W := W) A).map f)).inv := by
  change
    (ρ_ ((exactUniversalRealization (W := W) A).map f)).hom ≫
        (λ_ ((exactUniversalRealization (W := W) A).map f)).inv =
      (ρ_ ((exactUniversalRealization (W := W) A).map f)).hom ≫
        (λ_ ((exactUniversalRealization (W := W) A).map f)).inv
  rfl

/-- Native StrongTrans carried by the forward triangle components. -/
noncomputable def exactUniversalForwardTriangleStrongTrans :
    Pseudofunctor.StrongTrans
      (exactUniversalRealization (W := W) A).toPseudofunctor
      (exactUniversalRealization (W := W) A).toPseudofunctor where
  app X := exactUniversalForwardTriangleApp (W := W) A X
  naturality f :=
    exactUniversalForwardTriangleNaturalityIso (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    simpa only [exactUniversalForwardTriangleApp_eq_id,
      exactUniversalForwardTriangleNaturalityIso_hom] using
      (Pseudofunctor.StrongTrans.id
        (exactUniversalRealization (W := W) A).toPseudofunctor).naturality_naturality eta
  naturality_id X := by
    simpa only [exactUniversalForwardTriangleApp_eq_id,
      exactUniversalForwardTriangleNaturalityIso_hom] using
      (Pseudofunctor.StrongTrans.id
        (exactUniversalRealization (W := W) A).toPseudofunctor).naturality_id X
  naturality_comp {a b c} f g := by
    simpa only [exactUniversalForwardTriangleApp_eq_id,
      exactUniversalForwardTriangleNaturalityIso_hom] using
      (Pseudofunctor.StrongTrans.id
        (exactUniversalRealization (W := W) A).toPseudofunctor).naturality_comp f g

/-- Forward triangle modification: the explicit triangle StrongTrans is
canonically isomorphic to identity. -/
noncomputable def exactUniversalForwardTriangleModification :
    exactUniversalForwardTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id
        (exactUniversalRealization (W := W) A).toPseudofunctor := by
  refine Pseudofunctor.StrongTrans.isoMk (fun X => ?_) ?_
  · rw [exactUniversalForwardTriangleApp_eq_id]
    exact Iso.refl _
  · intro X Y f
    simpa only [exactUniversalForwardTriangleApp_eq_id,
      exactUniversalForwardTriangleNaturalityIso_hom] using
      (Pseudofunctor.StrongTrans.Modification.id
        (Pseudofunctor.StrongTrans.id
          (exactUniversalRealization (W := W) A).toPseudofunctor)).naturality f

/-! ## Quasi-inverse triangle -/

/-- The canonical section's identity comparison realizes to identity. -/
@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_mapId_hom_lift
    (Z : Ambient (W := W) A) :
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).mapId Z).hom.lift =
      𝟙 (𝟙 Z) := by
  exact exactUniversalAmbientSectionIdIso_hom_lift (W := W) A Z

/-- The canonical section's composition comparison realizes to identity. -/
@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_mapComp_hom_lift
    {X Y Z : Ambient (W := W) A}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).mapComp f g).hom.lift =
      𝟙 (f ≫ g) := by
  exact exactUniversalAmbientSectionCompIso_hom_lift (W := W) A f g

/-- Object component of the quasi-inverse triangle composite `ηG ; Gε`. -/
noncomputable def exactUniversalQuasiInverseTriangleApp
    (Z : Ambient (W := W) A) :
    (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A).obj Z ⟶
      (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A).obj Z :=
  (exactUniversalSourceAmbientRoundtripUnit (W := W) A).app
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z) ≫
    (exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).map
        ((exactUniversalAmbientRoundtripCounit (W := W) A).app Z)

/-- The quasi-inverse triangle component realizes exactly to identity. -/
@[simp] theorem exactUniversalQuasiInverseTriangleApp_lift
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleApp (W := W) A Z).lift =
      𝟙 Z := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)).lift ≫
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map
          ((exactUniversalAmbientRoundtripCounit (W := W) A).app Z)).lift =
        𝟙 Z
  rw [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift,
    exactUniversalAmbientRoundtripCounit_app,
    exactUniversalAmbientCanonicalSource_carrier]
  exact Category.comp_id _

/-- Ambient naturality square underlying the quasi-inverse triangle. -/
noncomputable def exactUniversalQuasiInverseTriangleNaturalityLiftIso
    {Z T : Ambient (W := W) A}
    (f : Z ⟶ T) :
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map f ≫
      exactUniversalQuasiInverseTriangleApp (W := W) A T).lift ≅
      (exactUniversalQuasiInverseTriangleApp (W := W) A Z ≫
        (exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).map f).lift := by
  rw [ExactUniversalRawMorphism.comp_lift,
    ExactUniversalRawMorphism.comp_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift,
    exactUniversalQuasiInverseTriangleApp_lift,
    exactUniversalQuasiInverseTriangleApp_lift]
  exact (ρ_ f) ≪≫ (λ_ f).symm

@[simp] theorem exactUniversalQuasiInverseTriangleNaturalityLiftIso_hom
    {Z T : Ambient (W := W) A}
    (f : Z ⟶ T) :
    (exactUniversalQuasiInverseTriangleNaturalityLiftIso
      (W := W) A f).hom =
      (ρ_ f).hom ≫ (λ_ f).inv := by
  change
    ((ρ_ f) ≪≫ (λ_ f).symm).hom =
      (ρ_ f).hom ≫ (λ_ f).inv
  simp only [Iso.trans_hom, Iso.symm_hom]

/-- Lift the ambient quasi-inverse triangle square uniquely to the source. -/
noncomputable def exactUniversalQuasiInverseTriangleNaturalityIso
    {Z T : Ambient (W := W) A}
    (f : Z ⟶ T) :
    (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map f ≫
        exactUniversalQuasiInverseTriangleApp (W := W) A T ≅
      exactUniversalQuasiInverseTriangleApp (W := W) A Z ≫
        (exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).map f :=
  exactUniversalSourceIsoOfLift
    (W := W) A
    (exactUniversalQuasiInverseTriangleNaturalityLiftIso
      (W := W) A f)

/-- Realization of the lifted quasi-inverse triangle square. -/
theorem exactUniversalQuasiInverseTriangleNaturalityIso_realization
    {Z T : Ambient (W := W) A}
    (f : Z ⟶ T) :
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj T)).mapIso
        (exactUniversalQuasiInverseTriangleNaturalityIso
          (W := W) A f) =
      exactUniversalQuasiInverseTriangleNaturalityLiftIso
        (W := W) A f := by
  apply Iso.ext
  exact
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj T)).map_preimage
        (X := (exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).map f ≫
          exactUniversalQuasiInverseTriangleApp (W := W) A T)
        (Y := exactUniversalQuasiInverseTriangleApp (W := W) A Z ≫
          (exactUniversalAmbientCanonicalSectionPseudofunctor
            (W := W) A).map f)
        (exactUniversalQuasiInverseTriangleNaturalityLiftIso
          (W := W) A f).hom

/-- Hom projection of the source quasi-inverse triangle square. -/
@[simp] theorem exactUniversalQuasiInverseTriangleNaturalityIso_hom_lift
    {Z T : Ambient (W := W) A}
    (f : Z ⟶ T) :
    (exactUniversalQuasiInverseTriangleNaturalityIso
      (W := W) A f).hom.lift =
      (ρ_ f).hom ≫ (λ_ f).inv := by
  have h :=
    congrArg Iso.hom
      (exactUniversalQuasiInverseTriangleNaturalityIso_realization
        (W := W) A f)
  simpa only [Functor.mapIso_hom,
    exactUniversalCompletion2HomFunctor_map,
    exactUniversalQuasiInverseTriangleNaturalityLiftIso_hom] using h

/-- Native StrongTrans carried by the quasi-inverse triangle components. -/
noncomputable def exactUniversalQuasiInverseTriangleStrongTrans :
    Pseudofunctor.StrongTrans
      (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)
      (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A) where
  app Z := exactUniversalQuasiInverseTriangleApp (W := W) A Z
  naturality f :=
    exactUniversalQuasiInverseTriangleNaturalityIso (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift,
      exactUniversalQuasiInverseTriangleApp_lift,
      exactUniversalQuasiInverseTriangleNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift]
    bicategory
  naturality_id Z := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalQuasiInverseTriangleNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalAmbientCanonicalSectionPseudofunctor_mapId_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalQuasiInverseTriangleApp_lift,
      exactUniversalRealization_source_leftUnitor_lift,
      exactUniversalRealization_source_rightUnitor_inv_lift]
    bicategory
  naturality_comp {a b c} f g := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    simp only [exactUniversalSourceTwoCell_comp_lift,
      exactUniversalQuasiInverseTriangleNaturalityIso_hom_lift,
      exactUniversalRealization_source_whiskerLeft_lift,
      exactUniversalAmbientCanonicalSectionPseudofunctor_mapComp_hom_lift,
      exactUniversalRealization_source_whiskerRight_lift,
      exactUniversalQuasiInverseTriangleApp_lift,
      exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift,
      exactUniversalRealization_source_associator_lift,
      exactUniversalRealization_source_associator_inv_lift]
    bicategory

/-- The source identity over a canonical ambient source realizes to identity. -/
@[simp] theorem exactUniversalCanonicalSource_id_lift
    (Z : Ambient (W := W) A) :
    (𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).obj Z)).lift = 𝟙 Z := by
  rw [ExactUniversalRawMorphism.id_lift,
    exactUniversalAmbientCanonicalSource_carrier]

/-- Ambient identity isomorphism underlying the pointwise quasi-inverse triangle. -/
noncomputable def exactUniversalQuasiInverseTriangleComponentLiftIso
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleApp (W := W) A Z).lift ≅
      (𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)).lift := by
  rw [exactUniversalQuasiInverseTriangleApp_lift,
    exactUniversalCanonicalSource_id_lift]
  exact Iso.refl _

@[simp] theorem exactUniversalQuasiInverseTriangleComponentLiftIso_hom
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleComponentLiftIso
      (W := W) A Z).hom = 𝟙 (𝟙 Z) := by
  change (Iso.refl (𝟙 Z)).hom = 𝟙 (𝟙 Z)
  rfl

/-- Pointwise source isomorphism from the quasi-inverse triangle component to
identity, obtained uniquely from the realized identity. -/
noncomputable def exactUniversalQuasiInverseTriangleComponentIso
    (Z : Ambient (W := W) A) :
    exactUniversalQuasiInverseTriangleApp (W := W) A Z ≅
      𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z) :=
  exactUniversalSourceIsoOfLift
    (W := W) A
    (exactUniversalQuasiInverseTriangleComponentLiftIso
      (W := W) A Z)

/-- Realization of the pointwise quasi-inverse triangle isomorphism. -/
theorem exactUniversalQuasiInverseTriangleComponentIso_realization
    (Z : Ambient (W := W) A) :
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)).mapIso
        (exactUniversalQuasiInverseTriangleComponentIso
          (W := W) A Z) =
      exactUniversalQuasiInverseTriangleComponentLiftIso
        (W := W) A Z := by
  apply Iso.ext
  exact
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)).map_preimage
        (X := exactUniversalQuasiInverseTriangleApp (W := W) A Z)
        (Y := 𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).obj Z))
        (exactUniversalQuasiInverseTriangleComponentLiftIso
          (W := W) A Z).hom

@[simp] theorem exactUniversalQuasiInverseTriangleComponentIso_hom_lift
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleComponentIso
      (W := W) A Z).hom.lift =
      𝟙 (𝟙 Z) := by
  have h :=
    congrArg Iso.hom
      (exactUniversalQuasiInverseTriangleComponentIso_realization
        (W := W) A Z)
  simpa only [Functor.mapIso_hom,
    exactUniversalCompletion2HomFunctor_map,
    exactUniversalQuasiInverseTriangleComponentLiftIso_hom] using h

/-- Quasi-inverse triangle modification to identity. -/
noncomputable def exactUniversalQuasiInverseTriangleModification :
    exactUniversalQuasiInverseTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id
        (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A) := by
  refine Pseudofunctor.StrongTrans.isoMk
    (fun Z => exactUniversalQuasiInverseTriangleComponentIso
      (W := W) A Z) ?_
  intro Z T f
  apply exactUniversalCompletion2_map_injective (W := W) A
  simp only [exactUniversalSourceTwoCell_comp_lift,
    exactUniversalRealization_source_whiskerLeft_lift,
    exactUniversalQuasiInverseTriangleComponentIso_hom_lift,
    exactUniversalRealization_source_whiskerRight_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift,
    exactUniversalQuasiInverseTriangleNaturalityIso_hom_lift,
    exactUniversalRealization_source_rightUnitor_lift,
    exactUniversalRealization_source_leftUnitor_inv_lift]
  bicategory

/-! ## Triangle package -/

/-- v5.15 certificate together with the two explicit triangle modifications. -/
structure ExactUniversalAmbientTriangleCertificate where
  biequivalence :
    ExactUniversalAmbientBiequivalenceCertificate (W := W) A
  forwardTriangle :
    exactUniversalForwardTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id
        (exactUniversalRealization (W := W) A).toPseudofunctor
  quasiInverseTriangle :
    exactUniversalQuasiInverseTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id
        (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)

/-- Canonical triangle-coherent refinement of the v5.15 ambient certificate. -/
noncomputable def exactUniversalAmbientTriangleCertificate :
    ExactUniversalAmbientTriangleCertificate (W := W) A where
  biequivalence :=
    exactUniversalAmbientBiequivalenceCertificate (W := W) A
  forwardTriangle :=
    exactUniversalForwardTriangleModification (W := W) A
  quasiInverseTriangle :=
    exactUniversalQuasiInverseTriangleModification (W := W) A

/-! ## Regression checks -/

#print axioms exactUniversalForwardTriangleApp
#print axioms exactUniversalForwardTriangleStrongTrans
#print axioms exactUniversalForwardTriangleModification
#print axioms exactUniversalQuasiInverseTriangleApp
#print axioms exactUniversalQuasiInverseTriangleStrongTrans
#print axioms exactUniversalQuasiInverseTriangleModification
#print axioms ExactUniversalAmbientTriangleCertificate
#print axioms exactUniversalAmbientTriangleCertificate

end

end KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16
