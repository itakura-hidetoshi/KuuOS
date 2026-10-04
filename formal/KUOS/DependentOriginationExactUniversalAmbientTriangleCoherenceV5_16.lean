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
set_option mathlib.tactic.category.grind true

noncomputable section

/-!
# Ambient triangle coherence v5.16

v5.15 packages the strict exact-universal realization `F`, its canonical
ambient section `G`, the source unit `η : Id ⟶ F ≫ G`, and the ambient
counit `ε : G ≫ F ⟶ Id`.

The central point is genuinely bicategorical: after projection, a triangle
component is `𝟙 Z ≫ 𝟙 Z`, so it is canonically *isomorphic* to `𝟙 Z` by a
unitor and is not identified with it by strict equality.

Pinned Mathlib does not expose a separate tricategorical horizontal-composition
API for pseudofunctors and StrongTrans.  We therefore formalize exactly the
coherence that is present and canonical:

* the forward triangle object component
  `F.map (η.app X) ≫ ε.app (F.obj X)`;
* the quasi-inverse triangle object component
  `η.app (G.obj Z) ≫ G.map (ε.app Z)`;
* canonical pointwise isomorphisms from both components to identity;
* coherent endo-StrongTrans representatives obtained by transporting identity
  naturality through those pointwise isomorphisms;
* native invertible modifications of those representatives to identity.

No arbitrary choice is introduced.  No weak-W exact-presentation implication
is used or asserted.
-/

universe u v uH vH
universe u₁ v₁ w₁ u₂ v₂ w₂

/-! ## Generic pointwise transport to an identity StrongTrans -/

section PointwiseIdentityTransport

variable {B : Type u₁} [Bicategory.{w₁, v₁} B]
variable {C : Type u₂} [Bicategory.{w₂, v₂} C]
variable (F : Pseudofunctor B C)
variable (t : ∀ X : B, F.obj X ⟶ F.obj X)
variable (e : ∀ X : B, t X ≅ 𝟙 (F.obj X))

/-- Conjugate the identity StrongTrans naturality by the prescribed objectwise
isomorphisms `e`. -/
noncomputable def pointwiseIdentityTransportNaturality
    {X Y : B} (f : X ⟶ Y) :
    F.map f ≫ t Y ≅ t X ≫ F.map f :=
  Bicategory.whiskerLeftIso (F.map f) (e Y) ≪≫
    (ρ_ (F.map f)) ≪≫
      (λ_ (F.map f)).symm ≪≫
        Bicategory.whiskerRightIso (e X).symm (F.map f)

/-- The prescribed object components carry the canonical StrongTrans structure
transported from identity.  The omitted coherence fields are discharged by
Mathlib's native `cat_disch` defaults for `StrongTrans`. -/
noncomputable def strongTransOfPointwiseIsoToId : F ⟶ F where
  app X := t X
  naturality f := pointwiseIdentityTransportNaturality F t e f
  naturality_naturality := by cat_disch
  naturality_id := by cat_disch
  naturality_comp := by cat_disch

@[simp] theorem strongTransOfPointwiseIsoToId_app
    (X : B) :
    (strongTransOfPointwiseIsoToId F t e).app X = t X :=
  rfl

/-- The transported StrongTrans is modification-isomorphic to identity. -/
noncomputable def strongTransOfPointwiseIsoToIdIso :
    strongTransOfPointwiseIsoToId F t e ≅ 𝟙 F :=
  Pseudofunctor.StrongTrans.isoMk
    (fun X => e X)
    (by cat_disch)

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

/-! ## Forward triangle -/

/-- Exact object component of the forward triangle composite `Fη ; εF`. -/
noncomputable def exactUniversalForwardTriangleApp
    (X : Source (W := W) A) :
    (exactUniversalRealization (W := W) A).obj X ⟶
      (exactUniversalRealization (W := W) A).obj X :=
  (exactUniversalRealization (W := W) A).map
      ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X) ≫
    (exactUniversalAmbientRoundtripCounit (W := W) A).app
      ((exactUniversalRealization (W := W) A).obj X)

/-- The forward triangle component is canonically isomorphic, not equal, to
identity. -/
noncomputable def exactUniversalForwardTriangleComponentIso
    (X : Source (W := W) A) :
    exactUniversalForwardTriangleApp (W := W) A X ≅
      𝟙 ((exactUniversalRealization (W := W) A).obj X) := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X).lift ≫
        (exactUniversalAmbientRoundtripCounit (W := W) A).app X.carrier ≅
      𝟙 X.carrier
  simpa only [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientRoundtripCounit_app] using
      (ρ_ (𝟙 X.carrier))

/-- Coherent forward-triangle representative with the genuine triangle object
components. -/
noncomputable def exactUniversalForwardTriangleStrongTrans :
    (exactUniversalRealization (W := W) A).toPseudofunctor ⟶
      (exactUniversalRealization (W := W) A).toPseudofunctor :=
  strongTransOfPointwiseIsoToId
    (exactUniversalRealization (W := W) A).toPseudofunctor
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
      𝟙 (exactUniversalRealization (W := W) A).toPseudofunctor :=
  strongTransOfPointwiseIsoToIdIso
    (exactUniversalRealization (W := W) A).toPseudofunctor
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

/-- The chosen ambient section object has the prescribed ambient carrier. -/
@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_obj_carrier
    (Z : Ambient (W := W) A) :
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).obj Z).carrier = Z := by
  change
    (exactUniversalAmbientCanonicalSource (W := W) A Z).carrier = Z
  exact exactUniversalAmbientCanonicalSource_carrier (W := W) A Z

/-- Exact object component of the quasi-inverse triangle composite
`ηG ; Gε`. -/
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

/-- Realized quasi-inverse triangle component.  The target is written with the
concrete source identity constructor to keep its dependent endpoints fixed. -/
noncomputable def exactUniversalQuasiInverseTriangleComponentLiftIso
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleApp (W := W) A Z).lift ≅
      (ExactUniversalRawMorphism.id
        (W := W) A
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).obj Z)).lift := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).obj Z)).lift ≫
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map
          ((exactUniversalAmbientRoundtripCounit (W := W) A).app Z)).lift ≅
      (ExactUniversalRawMorphism.id
        (W := W) A
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).obj Z)).lift
  simp only [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift,
    exactUniversalAmbientRoundtripCounit_app,
    ExactUniversalRawMorphism.id_lift]
  change (𝟙 Z ≫ 𝟙 Z) ≅ 𝟙 Z
  exact ρ_ (𝟙 Z)

/-- Lift the realized triangle coherence uniquely through local full
faithfulness of exact realization. -/
noncomputable def exactUniversalQuasiInverseTriangleComponentIso
    (Z : Ambient (W := W) A) :
    exactUniversalQuasiInverseTriangleApp (W := W) A Z ≅
      𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z) := by
  change
    exactUniversalQuasiInverseTriangleApp (W := W) A Z ≅
      ExactUniversalRawMorphism.id
        (W := W) A
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).obj Z)
  exact
    exactUniversalSourceIsoOfLift
      (W := W) A
      (exactUniversalQuasiInverseTriangleComponentLiftIso
        (W := W) A Z)

/-- Realization of the lifted quasi-inverse triangle component is exactly the
prescribed ambient unitor comparison. -/
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
        (Y := ExactUniversalRawMorphism.id
          (W := W) A
          ((exactUniversalAmbientCanonicalSectionPseudofunctor
            (W := W) A).obj Z))
        (exactUniversalQuasiInverseTriangleComponentLiftIso
          (W := W) A Z).hom

/-- Coherent quasi-inverse-triangle representative with the genuine triangle
object components. -/
noncomputable def exactUniversalQuasiInverseTriangleStrongTrans :
    exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A ⟶
      exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A :=
  strongTransOfPointwiseIsoToId
    (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)
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
      𝟙 (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A) :=
  strongTransOfPointwiseIsoToIdIso
    (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)
    (exactUniversalQuasiInverseTriangleApp (W := W) A)
    (exactUniversalQuasiInverseTriangleComponentIso (W := W) A)

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
#print axioms exactUniversalQuasiInverseTriangleComponentIso_realization
#print axioms exactUniversalQuasiInverseTriangleStrongTrans
#print axioms exactUniversalQuasiInverseTriangleModification

end

end KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16
