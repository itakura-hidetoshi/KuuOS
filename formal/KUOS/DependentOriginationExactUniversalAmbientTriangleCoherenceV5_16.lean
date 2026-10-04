import KUOS.DependentOriginationExactUniversalAmbientBiequivalenceCertificateV5_15

namespace KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
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

v5.15 packages the strict exact-universal realization `F`, its canonical
ambient section `G`, the source unit `η : Id ⟶ F ≫ G`, and the ambient
counit `ε : G ≫ F ⟶ Id`.

The important Lean boundary is that a bicategory is not strict: after projecting
the v5.14 unit and v5.13 counit, a triangle component becomes

  `𝟙 Z ≫ 𝟙 Z`

and this is *isomorphic* to `𝟙 Z` by a unitor; it is not equal to it.
Accordingly this file never rewrites `𝟙 ≫ 𝟙` to `𝟙`.

Pinned Mathlib does not expose a tricategorical horizontal-whiskering package
for pseudofunctors and StrongTrans.  We therefore make the boundary explicit:

1. form the two genuine triangle object components
   `F.map (η.app X) ≫ ε.app (F.obj X)` and
   `η.app (G.obj Z) ≫ G.map (ε.app Z)`;
2. construct their canonical pointwise isomorphisms to identity;
3. use those pointwise isomorphisms to transport the identity StrongTrans
   naturality, producing coherent endo-StrongTrans with exactly those object
   components;
4. package the pointwise isomorphisms as native invertible modifications by
   `Pseudofunctor.StrongTrans.isoMk`.

Thus v5.16 proves a canonical triangle-coherence representative with the exact
expected object components.  It does not claim an additional general
tricategory infrastructure or an identification with a separately implemented
horizontal composite of StrongTrans.

No new choice is introduced, and no weak-W exact-presentation implication is
used or asserted.
-/

universe u v uH vH
universe u₁ v₁ w₁ u₂ v₂ w₂

/-! ## A reusable bicategorical transport lemma

Any family of endomorphisms pointwise isomorphic to identity carries a canonical
StrongTrans structure: transport the identity StrongTrans naturality through
the chosen objectwise isomorphisms.  The three StrongTrans coherence laws then
reduce to native bicategory coherence.
-/

section PointwiseIdentityTransport

variable {B : Type u₁} [Bicategory.{w₁, v₁} B]
variable {C : Type u₂} [Bicategory.{w₂, v₂} C]
variable (F : Pseudofunctor B C)
variable (t : ∀ X : B, F.obj X ⟶ F.obj X)
variable (e : ∀ X : B, t X ≅ 𝟙 (F.obj X))

/-- Canonical naturality square obtained by conjugating the identity
StrongTrans naturality through objectwise isomorphisms to identity. -/
noncomputable def pointwiseIdentityTransportNaturality
    {X Y : B} (f : X ⟶ Y) :
    F.map f ≫ t Y ≅ t X ≫ F.map f :=
  Bicategory.whiskerLeftIso (F.map f) (e Y) ≪≫
    (ρ_ (F.map f)) ≪≫
      (λ_ (F.map f)).symm ≪≫
        Bicategory.whiskerRightIso (e X).symm (F.map f)

@[simp] theorem pointwiseIdentityTransportNaturality_hom
    {X Y : B} (f : X ⟶ Y) :
    (pointwiseIdentityTransportNaturality F t e f).hom =
      (F.map f ◁ (e Y).hom) ≫
        (ρ_ (F.map f)).hom ≫
          (λ_ (F.map f)).inv ≫
            (e X).inv ▷ F.map f := by
  simp only [pointwiseIdentityTransportNaturality, Iso.trans_hom,
    Iso.symm_hom, whiskerLeftIso_hom, whiskerRightIso_hom]

/-- Canonical endo-StrongTrans on `F` with prescribed object components
pointwise isomorphic to identity. -/
noncomputable def strongTransOfPointwiseIsoToId :
    Pseudofunctor.StrongTrans F F where
  app X := t X
  naturality f := pointwiseIdentityTransportNaturality F t e f
  naturality_naturality {a b} {f g} eta := by
    simp only [pointwiseIdentityTransportNaturality_hom,
      Iso.trans_hom, Iso.symm_hom, Iso.refl_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom]
    bicategory
  naturality_id a := by
    simp only [pointwiseIdentityTransportNaturality_hom,
      Iso.trans_hom, Iso.symm_hom, Iso.refl_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom]
    bicategory
  naturality_comp {a b c} f g := by
    simp only [pointwiseIdentityTransportNaturality_hom,
      Iso.trans_hom, Iso.symm_hom, Iso.refl_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom]
    bicategory

@[simp] theorem strongTransOfPointwiseIsoToId_app
    (X : B) :
    (strongTransOfPointwiseIsoToId F t e).app X = t X :=
  rfl

/-- The transported StrongTrans is canonically modification-isomorphic to the
identity StrongTrans. -/
noncomputable def strongTransOfPointwiseIsoToIdIso :
    strongTransOfPointwiseIsoToId F t e ≅
      Pseudofunctor.StrongTrans.id F := by
  refine Pseudofunctor.StrongTrans.isoMk
    (η := strongTransOfPointwiseIsoToId F t e)
    (θ := Pseudofunctor.StrongTrans.id F)
    (fun X => ?_) ?_
  · exact e X
  · intro X Y f
    change
      (F.map f ◁ (e Y).hom) ≫
          (((ρ_ (F.map f)) ≪≫ (λ_ (F.map f)).symm).hom) =
        (pointwiseIdentityTransportNaturality F t e f).hom ≫
          (e X).hom ▷ F.map f
    simp only [pointwiseIdentityTransportNaturality_hom,
      Iso.trans_hom, Iso.symm_hom, Iso.refl_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom]
    bicategory

@[simp] theorem strongTransOfPointwiseIsoToIdIso_hom_app
    (X : B) :
    ((strongTransOfPointwiseIsoToIdIso F t e).hom.as.app X) =
      (e X).hom :=
  rfl

end PointwiseIdentityTransport

/-! ## Exact-universal ambient specialization -/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

abbrev Forward :=
  (exactUniversalRealization (W := W) A).toPseudofunctor

abbrev QuasiInverse :=
  exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A

/-! ## Forward triangle -/

/-- Exact object component of the forward triangle composite `Fη ; εF`. -/
noncomputable def exactUniversalForwardTriangleApp
    (X : Source (W := W) A) :
    (Forward (W := W) A).obj X ⟶ (Forward (W := W) A).obj X :=
  (exactUniversalRealization (W := W) A).map
      ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X) ≫
    (exactUniversalAmbientRoundtripCounit (W := W) A).app
      ((Forward (W := W) A).obj X)

/-- The forward triangle component is canonically isomorphic, not equal, to
identity.  After projection it is `𝟙 X.carrier ≫ 𝟙 X.carrier`, so the right
unitor is the exact coherence cell. -/
noncomputable def exactUniversalForwardTriangleComponentIso
    (X : Source (W := W) A) :
    exactUniversalForwardTriangleApp (W := W) A X ≅
      𝟙 ((Forward (W := W) A).obj X) := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X).lift ≫
        (exactUniversalAmbientRoundtripCounit (W := W) A).app X.carrier ≅
      𝟙 X.carrier
  simpa only [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientRoundtripCounit_app] using
      (ρ_ (𝟙 X.carrier))

@[simp] theorem exactUniversalForwardTriangleComponentIso_hom
    (X : Source (W := W) A) :
    (exactUniversalForwardTriangleComponentIso (W := W) A X).hom =
      (ρ_ (𝟙 X.carrier)).hom := by
  change
    ((ρ_ (𝟙 X.carrier))).hom = (ρ_ (𝟙 X.carrier)).hom
  rfl

/-- Coherent forward triangle representative with the genuine triangle object
components. -/
noncomputable def exactUniversalForwardTriangleStrongTrans :
    Pseudofunctor.StrongTrans
      (Forward (W := W) A)
      (Forward (W := W) A) :=
  strongTransOfPointwiseIsoToId
    (Forward (W := W) A)
    (exactUniversalForwardTriangleApp (W := W) A)
    (exactUniversalForwardTriangleComponentIso (W := W) A)

@[simp] theorem exactUniversalForwardTriangleStrongTrans_app
    (X : Source (W := W) A) :
    (exactUniversalForwardTriangleStrongTrans (W := W) A).app X =
      exactUniversalForwardTriangleApp (W := W) A X :=
  rfl

/-- Forward triangle modification to identity. -/
noncomputable def exactUniversalForwardTriangleModification :
    exactUniversalForwardTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id (Forward (W := W) A) :=
  strongTransOfPointwiseIsoToIdIso
    (Forward (W := W) A)
    (exactUniversalForwardTriangleApp (W := W) A)
    (exactUniversalForwardTriangleComponentIso (W := W) A)

@[simp] theorem exactUniversalForwardTriangleModification_hom_app
    (X : Source (W := W) A) :
    ((exactUniversalForwardTriangleModification
      (W := W) A).hom.as.app X) =
      (exactUniversalForwardTriangleComponentIso
        (W := W) A X).hom :=
  rfl

/-! ## Quasi-inverse triangle -/

/-- The canonical ambient section object's realized carrier is the original
ambient object.  Naming this projection prevents dependent rewrites from having
to unfold the whole pseudofunctor. -/
@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_obj_carrier
    (Z : Ambient (W := W) A) :
    ((QuasiInverse (W := W) A).obj Z).carrier = Z := by
  change
    (exactUniversalAmbientCanonicalSource (W := W) A Z).carrier = Z
  exact exactUniversalAmbientCanonicalSource_carrier (W := W) A Z

/-- Exact object component of the quasi-inverse triangle composite
`ηG ; Gε`. -/
noncomputable def exactUniversalQuasiInverseTriangleApp
    (Z : Ambient (W := W) A) :
    (QuasiInverse (W := W) A).obj Z ⟶
      (QuasiInverse (W := W) A).obj Z :=
  (exactUniversalSourceAmbientRoundtripUnit (W := W) A).app
      ((QuasiInverse (W := W) A).obj Z) ≫
    (QuasiInverse (W := W) A).map
      ((exactUniversalAmbientRoundtripCounit (W := W) A).app Z)

/-- Realized quasi-inverse triangle component.  This is deliberately stated as
an isomorphism to the realized source identity; bicategorical unitors, not
strict equality, provide the comparison. -/
noncomputable def exactUniversalQuasiInverseTriangleComponentLiftIso
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleApp (W := W) A Z).lift ≅
      (ExactUniversalRawMorphism.id
        (W := W) A ((QuasiInverse (W := W) A).obj Z)).lift := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app
        ((QuasiInverse (W := W) A).obj Z)).lift ≫
      ((QuasiInverse (W := W) A).map
        ((exactUniversalAmbientRoundtripCounit (W := W) A).app Z)).lift ≅
      (ExactUniversalRawMorphism.id
        (W := W) A ((QuasiInverse (W := W) A).obj Z)).lift
  simp only [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift,
    exactUniversalAmbientRoundtripCounit_app,
    ExactUniversalRawMorphism.id_lift]
  rw [exactUniversalAmbientCanonicalSectionPseudofunctor_obj_carrier]
  exact ρ_ (𝟙 Z)

@[simp] theorem exactUniversalQuasiInverseTriangleComponentLiftIso_hom
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleComponentLiftIso
      (W := W) A Z).hom =
      (ρ_ (𝟙 Z)).hom := by
  change (ρ_ (𝟙 Z)).hom = (ρ_ (𝟙 Z)).hom
  rfl

/-- Lift the realized triangle coherence uniquely through local full
faithfulness of exact realization. -/
noncomputable def exactUniversalQuasiInverseTriangleComponentIso
    (Z : Ambient (W := W) A) :
    exactUniversalQuasiInverseTriangleApp (W := W) A Z ≅
      𝟙 ((QuasiInverse (W := W) A).obj Z) := by
  change
    exactUniversalQuasiInverseTriangleApp (W := W) A Z ≅
      ExactUniversalRawMorphism.id
        (W := W) A ((QuasiInverse (W := W) A).obj Z)
  exact
    exactUniversalSourceIsoOfLift
      (W := W) A
      (exactUniversalQuasiInverseTriangleComponentLiftIso
        (W := W) A Z)

/-- Realization of the lifted quasi-inverse triangle component is exactly the
prescribed ambient unitor. -/
theorem exactUniversalQuasiInverseTriangleComponentIso_realization
    (Z : Ambient (W := W) A) :
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      ((QuasiInverse (W := W) A).obj Z)
      ((QuasiInverse (W := W) A).obj Z)).mapIso
        (exactUniversalQuasiInverseTriangleComponentIso
          (W := W) A Z) =
      exactUniversalQuasiInverseTriangleComponentLiftIso
        (W := W) A Z := by
  apply Iso.ext
  exact
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      ((QuasiInverse (W := W) A).obj Z)
      ((QuasiInverse (W := W) A).obj Z)).map_preimage
        (X := exactUniversalQuasiInverseTriangleApp (W := W) A Z)
        (Y := ExactUniversalRawMorphism.id
          (W := W) A ((QuasiInverse (W := W) A).obj Z))
        (exactUniversalQuasiInverseTriangleComponentLiftIso
          (W := W) A Z).hom

@[simp] theorem exactUniversalQuasiInverseTriangleComponentIso_hom_lift
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleComponentIso
      (W := W) A Z).hom.lift =
      (ρ_ (𝟙 Z)).hom := by
  have h :=
    congrArg Iso.hom
      (exactUniversalQuasiInverseTriangleComponentIso_realization
        (W := W) A Z)
  simpa only [Functor.mapIso_hom,
    exactUniversalCompletion2HomFunctor_map,
    exactUniversalQuasiInverseTriangleComponentLiftIso_hom] using h

/-- Coherent quasi-inverse triangle representative with the genuine triangle
object components. -/
noncomputable def exactUniversalQuasiInverseTriangleStrongTrans :
    Pseudofunctor.StrongTrans
      (QuasiInverse (W := W) A)
      (QuasiInverse (W := W) A) :=
  strongTransOfPointwiseIsoToId
    (QuasiInverse (W := W) A)
    (exactUniversalQuasiInverseTriangleApp (W := W) A)
    (exactUniversalQuasiInverseTriangleComponentIso (W := W) A)

@[simp] theorem exactUniversalQuasiInverseTriangleStrongTrans_app
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleStrongTrans (W := W) A).app Z =
      exactUniversalQuasiInverseTriangleApp (W := W) A Z :=
  rfl

/-- Quasi-inverse triangle modification to identity. -/
noncomputable def exactUniversalQuasiInverseTriangleModification :
    exactUniversalQuasiInverseTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id (QuasiInverse (W := W) A) :=
  strongTransOfPointwiseIsoToIdIso
    (QuasiInverse (W := W) A)
    (exactUniversalQuasiInverseTriangleApp (W := W) A)
    (exactUniversalQuasiInverseTriangleComponentIso (W := W) A)

@[simp] theorem exactUniversalQuasiInverseTriangleModification_hom_app_lift
    (Z : Ambient (W := W) A) :
    ((exactUniversalQuasiInverseTriangleModification
      (W := W) A).hom.as.app Z).lift =
      (ρ_ (𝟙 Z)).hom := by
  change
    (exactUniversalQuasiInverseTriangleComponentIso
      (W := W) A Z).hom.lift =
      (ρ_ (𝟙 Z)).hom
  exact exactUniversalQuasiInverseTriangleComponentIso_hom_lift
    (W := W) A Z

/-! ## Triangle-coherence package -/

/-- v5.15 certificate together with canonical coherent representatives of both
triangle composites.  This strengthens v5.15 without claiming a separate
tricategorical horizontal-composition API. -/
structure ExactUniversalAmbientTriangleCoherenceCertificate where
  biequivalence :
    ExactUniversalAmbientBiequivalenceCertificate (W := W) A
  forwardTriangle :
    exactUniversalForwardTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id (Forward (W := W) A)
  quasiInverseTriangle :
    exactUniversalQuasiInverseTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id (QuasiInverse (W := W) A)

/-- Canonical v5.16 triangle-coherence refinement of the v5.15 ambient
biequivalence certificate. -/
noncomputable def exactUniversalAmbientTriangleCoherenceCertificate :
    ExactUniversalAmbientTriangleCoherenceCertificate (W := W) A where
  biequivalence :=
    exactUniversalAmbientBiequivalenceCertificate (W := W) A
  forwardTriangle :=
    exactUniversalForwardTriangleModification (W := W) A
  quasiInverseTriangle :=
    exactUniversalQuasiInverseTriangleModification (W := W) A

/-! ## Regression checks -/

#print axioms pointwiseIdentityTransportNaturality
#print axioms strongTransOfPointwiseIsoToId
#print axioms strongTransOfPointwiseIsoToIdIso
#print axioms exactUniversalForwardTriangleApp
#print axioms exactUniversalForwardTriangleComponentIso
#print axioms exactUniversalForwardTriangleStrongTrans
#print axioms exactUniversalForwardTriangleModification
#print axioms exactUniversalQuasiInverseTriangleApp
#print axioms exactUniversalQuasiInverseTriangleComponentLiftIso
#print axioms exactUniversalQuasiInverseTriangleComponentIso
#print axioms exactUniversalQuasiInverseTriangleStrongTrans
#print axioms exactUniversalQuasiInverseTriangleModification
#print axioms ExactUniversalAmbientTriangleCoherenceCertificate
#print axioms exactUniversalAmbientTriangleCoherenceCertificate

end

end KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16
