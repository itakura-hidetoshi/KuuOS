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

v5.15 packages the strict exact-universal realization `F`, its canonical
ambient section `G`, the source unit `η : Id ⟶ F ≫ G`, and the ambient
counit `ε : G ≫ F ⟶ Id`.

The previous draft tried to prove a much stronger generic statement: every
family of endomorphisms pointwise isomorphic to identity carries a canonical
StrongTrans structure.  That statement is true, but it is unnecessary here and
its transport proof obscures the actual exact-universal geometry.

For the present unit/counit the triangle components have a much simpler normal
form.  After realization, both are exactly

  `𝟙 Z ≫ 𝟙 Z`.

A bicategory does not identify this composite strictly with `𝟙 Z`; the
comparison is the native right unitor.  This file therefore isolates the
canonical `double identity` StrongTrans once, using only associators and
unitors, and relates the two actual triangle object components to that coherent
representative:

* on the forward/ambient side the actual component is equal to the double
  identity component after the existing v5.13/v5.14 projections;
* on the quasi-inverse/source side the two components have the same realized
  lift, so local full faithfulness produces their unique canonical source
  isomorphism.

Pinned Mathlib does not expose a separate tricategorical horizontal-composition
API for pseudofunctors and StrongTrans.  Accordingly we claim exactly the
coherent representative and its native invertible modification to identity,
not a stronger unidentified tricategory structure.

No arbitrary choice is introduced, and no weak-W exact-presentation implication
is used or asserted.
-/

universe u v uH vH
universe uB vB wB

/-! ## Pure bicategorical double-identity coherence -/

section DoubleIdentity

variable {B : Type uB} [Bicategory.{wB, vB} B]

/-- Canonical comparison from
`f ≫ (𝟙 ≫ 𝟙)` to `(𝟙 ≫ 𝟙) ≫ f`.
It is the unique structural path obtained by reducing both sides to `f`. -/
noncomputable def doubleIdentityNaturalityIso
    {X Y : B} (f : X ⟶ Y) :
    f ≫ (𝟙 Y ≫ 𝟙 Y) ≅ (𝟙 X ≫ 𝟙 X) ≫ f :=
  (α_ f (𝟙 Y) (𝟙 Y)).symm ≪≫
    Bicategory.whiskerRightIso (ρ_ f) (𝟙 Y) ≪≫
      (ρ_ f) ≪≫
        (λ_ f).symm ≪≫
          (Bicategory.whiskerLeftIso (𝟙 X) (λ_ f)).symm ≪≫
            (α_ (𝟙 X) (𝟙 X) f).symm

@[simp] theorem doubleIdentityNaturalityIso_hom
    {X Y : B} (f : X ⟶ Y) :
    (doubleIdentityNaturalityIso f).hom =
      (α_ f (𝟙 Y) (𝟙 Y)).inv ≫
        (ρ_ f).hom ▷ (𝟙 Y) ≫
          (ρ_ f).hom ≫
            (λ_ f).inv ≫
              (𝟙 X) ◁ (λ_ f).inv ≫
                (α_ (𝟙 X) (𝟙 X) f).inv := by
  rfl

end DoubleIdentity

section DoubleIdentityStrongTrans

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type u} [Bicategory.{uH, vH} C]
variable (F : Pseudofunctor B C)

/-- The canonical endo-StrongTrans whose component at `X` is
`𝟙 (F.obj X) ≫ 𝟙 (F.obj X)`. -/
noncomputable def doubleIdentityStrongTrans :
    Pseudofunctor.StrongTrans F F where
  app X := 𝟙 (F.obj X) ≫ 𝟙 (F.obj X)
  naturality f := doubleIdentityNaturalityIso (F.map f)
  naturality_naturality {a b} {f g} eta := by
    change
      F.map₂ eta ▷ (𝟙 (F.obj b) ≫ 𝟙 (F.obj b)) ≫
          (doubleIdentityNaturalityIso (F.map g)).hom =
        (doubleIdentityNaturalityIso (F.map f)).hom ≫
          (𝟙 (F.obj a) ≫ 𝟙 (F.obj a)) ◁ F.map₂ eta
    rw [doubleIdentityNaturalityIso_hom,
      doubleIdentityNaturalityIso_hom]
    bicategory
  naturality_id a := by
    change
      (doubleIdentityNaturalityIso (F.map (𝟙 a))).hom ≫
          (𝟙 (F.obj a) ≫ 𝟙 (F.obj a)) ◁ (F.mapId a).hom =
        (F.mapId a).hom ▷ (𝟙 (F.obj a) ≫ 𝟙 (F.obj a)) ≫
          (λ_ (𝟙 (F.obj a) ≫ 𝟙 (F.obj a))).hom ≫
            (ρ_ (𝟙 (F.obj a) ≫ 𝟙 (F.obj a))).inv
    rw [doubleIdentityNaturalityIso_hom]
    bicategory
  naturality_comp {a b c} f g := by
    change
      (doubleIdentityNaturalityIso (F.map (f ≫ g))).hom ≫
          (𝟙 (F.obj a) ≫ 𝟙 (F.obj a)) ◁ (F.mapComp f g).hom =
        (F.mapComp f g).hom ▷ (𝟙 (F.obj c) ≫ 𝟙 (F.obj c)) ≫
          (α_ (F.map f) (F.map g)
            (𝟙 (F.obj c) ≫ 𝟙 (F.obj c))).hom ≫
            F.map f ◁ (doubleIdentityNaturalityIso (F.map g)).hom ≫
              (α_ (F.map f)
                (𝟙 (F.obj b) ≫ 𝟙 (F.obj b))
                (F.map g)).inv ≫
                (doubleIdentityNaturalityIso (F.map f)).hom ▷ F.map g ≫
                  (α_
                    (𝟙 (F.obj a) ≫ 𝟙 (F.obj a))
                    (F.map f) (F.map g)).hom
    rw [doubleIdentityNaturalityIso_hom,
      doubleIdentityNaturalityIso_hom,
      doubleIdentityNaturalityIso_hom]
    bicategory

@[simp] theorem doubleIdentityStrongTrans_app
    (X : B) :
    (doubleIdentityStrongTrans F).app X =
      𝟙 (F.obj X) ≫ 𝟙 (F.obj X) :=
  rfl

/-- The double-identity StrongTrans is canonically modification-isomorphic to
the identity StrongTrans. -/
noncomputable def doubleIdentityStrongTransIso :
    doubleIdentityStrongTrans F ≅
      Pseudofunctor.StrongTrans.id F := by
  refine Pseudofunctor.StrongTrans.isoMk
    (fun X => ρ_ (𝟙 (F.obj X))) ?_
  intro X Y f
  change
    F.map f ◁ (ρ_ (𝟙 (F.obj Y))).hom ≫
        (ρ_ (F.map f)).hom ≫ (λ_ (F.map f)).inv =
      (doubleIdentityNaturalityIso (F.map f)).hom ≫
        (ρ_ (𝟙 (F.obj X))).hom ▷ F.map f
  rw [doubleIdentityNaturalityIso_hom]
  bicategory

@[simp] theorem doubleIdentityStrongTransIso_hom_app
    (X : B) :
    ((doubleIdentityStrongTransIso F).hom.as.app X) =
      (ρ_ (𝟙 (F.obj X))).hom :=
  rfl

end DoubleIdentityStrongTrans

/-! ## Exact-universal specialization -/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Ambient :=
  DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A

/-! ## Forward triangle -/

/-- Actual object component of the forward triangle `Fη ; εF`. -/
noncomputable def exactUniversalForwardTriangleApp
    (X : Source (W := W) A) :
    (exactUniversalRealization (W := W) A).obj X ⟶
      (exactUniversalRealization (W := W) A).obj X :=
  (exactUniversalRealization (W := W) A).map
      ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X) ≫
    (exactUniversalAmbientRoundtripCounit (W := W) A).app
      ((exactUniversalRealization (W := W) A).obj X)

/-- Projection of the actual forward triangle component: it is exactly the
ambient double identity, with no strict collapse of `𝟙 ≫ 𝟙`. -/
@[simp] theorem exactUniversalForwardTriangleApp_eq_doubleIdentity
    (X : Source (W := W) A) :
    exactUniversalForwardTriangleApp (W := W) A X =
      𝟙 X.carrier ≫ 𝟙 X.carrier := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X).lift ≫
        (exactUniversalAmbientRoundtripCounit (W := W) A).app X.carrier =
      𝟙 X.carrier ≫ 𝟙 X.carrier
  rw [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientRoundtripCounit_app]

/-- Coherent forward triangle representative. -/
noncomputable def exactUniversalForwardTriangleStrongTrans :
    Pseudofunctor.StrongTrans
      (exactUniversalRealization (W := W) A).toPseudofunctor
      (exactUniversalRealization (W := W) A).toPseudofunctor :=
  doubleIdentityStrongTrans
    (exactUniversalRealization (W := W) A).toPseudofunctor

/-- The coherent representative has exactly the projected actual triangle
component. -/
@[simp] theorem exactUniversalForwardTriangleApp_eq_representative
    (X : Source (W := W) A) :
    exactUniversalForwardTriangleApp (W := W) A X =
      (exactUniversalForwardTriangleStrongTrans (W := W) A).app X := by
  rw [exactUniversalForwardTriangleApp_eq_doubleIdentity]
  rfl

/-- Native forward triangle modification of the coherent representative to
identity. -/
noncomputable def exactUniversalForwardTriangleModification :
    exactUniversalForwardTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id
        (exactUniversalRealization (W := W) A).toPseudofunctor :=
  doubleIdentityStrongTransIso
    (exactUniversalRealization (W := W) A).toPseudofunctor

@[simp] theorem exactUniversalForwardTriangleModification_hom_app
    (X : Source (W := W) A) :
    ((exactUniversalForwardTriangleModification
      (W := W) A).hom.as.app X) =
      (ρ_ (𝟙 X.carrier)).hom :=
  rfl

/-! ## Quasi-inverse triangle -/

/-- The chosen ambient section object has the prescribed realized carrier. -/
@[simp] theorem exactUniversalAmbientCanonicalSectionPseudofunctor_obj_carrier
    (Z : Ambient (W := W) A) :
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).obj Z).carrier = Z := by
  change
    (exactUniversalAmbientCanonicalSource (W := W) A Z).carrier = Z
  exact exactUniversalAmbientCanonicalSource_carrier (W := W) A Z

/-- Actual object component of the quasi-inverse triangle `ηG ; Gε`. -/
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

/-- The actual quasi-inverse triangle component realizes exactly to the ambient
double identity. -/
@[simp] theorem exactUniversalQuasiInverseTriangleApp_lift
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleApp (W := W) A Z).lift =
      𝟙 Z ≫ 𝟙 Z := by
  change
    ((exactUniversalSourceAmbientRoundtripUnit (W := W) A).app
        ((exactUniversalAmbientCanonicalSectionPseudofunctor
          (W := W) A).obj Z)).lift ≫
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map
          ((exactUniversalAmbientRoundtripCounit (W := W) A).app Z)).lift =
      𝟙 Z ≫ 𝟙 Z
  simp only [exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift,
    exactUniversalAmbientRoundtripCounit_app,
    exactUniversalAmbientCanonicalSectionPseudofunctor_obj_carrier]

/-- Coherent quasi-inverse triangle representative. -/
noncomputable def exactUniversalQuasiInverseTriangleStrongTrans :
    Pseudofunctor.StrongTrans
      (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)
      (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A) :=
  doubleIdentityStrongTrans
    (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)

@[simp] theorem exactUniversalQuasiInverseTriangleStrongTrans_app_lift
    (Z : Ambient (W := W) A) :
    ((exactUniversalQuasiInverseTriangleStrongTrans
      (W := W) A).app Z).lift =
      𝟙 Z ≫ 𝟙 Z := by
  change
    ((𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).obj Z)) ≫
      𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)).lift =
      𝟙 Z ≫ 𝟙 Z
  rw [ExactUniversalRawMorphism.comp_lift,
    ExactUniversalRawMorphism.id_lift,
    ExactUniversalRawMorphism.id_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_obj_carrier]

/-- Realized equality of the actual quasi-inverse triangle component and the
coherent representative component. -/
noncomputable def exactUniversalQuasiInverseTriangleRepresentativeLiftIso
    (Z : Ambient (W := W) A) :
    (exactUniversalQuasiInverseTriangleApp (W := W) A Z).lift ≅
      ((exactUniversalQuasiInverseTriangleStrongTrans
        (W := W) A).app Z).lift := by
  rw [exactUniversalQuasiInverseTriangleApp_lift,
    exactUniversalQuasiInverseTriangleStrongTrans_app_lift]
  exact Iso.refl _

/-- Local full faithfulness lifts the realized equality to the unique canonical
source isomorphism from the actual quasi-inverse triangle component to the
coherent representative component. -/
noncomputable def exactUniversalQuasiInverseTriangleRepresentativeIso
    (Z : Ambient (W := W) A) :
    exactUniversalQuasiInverseTriangleApp (W := W) A Z ≅
      (exactUniversalQuasiInverseTriangleStrongTrans (W := W) A).app Z :=
  exactUniversalSourceIsoOfLift
    (W := W) A
    (f := exactUniversalQuasiInverseTriangleApp (W := W) A Z)
    (g := (exactUniversalQuasiInverseTriangleStrongTrans (W := W) A).app Z)
    (exactUniversalQuasiInverseTriangleRepresentativeLiftIso
      (W := W) A Z)

/-- Realization of the lifted comparison is exactly the prescribed reflexive
ambient comparison. -/
theorem exactUniversalQuasiInverseTriangleRepresentativeIso_realization
    (Z : Ambient (W := W) A) :
    (exactUniversalCompletion2HomFunctor
      (W := W) A
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)
      ((exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z)).mapIso
        (exactUniversalQuasiInverseTriangleRepresentativeIso
          (W := W) A Z) =
      exactUniversalQuasiInverseTriangleRepresentativeLiftIso
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
        (Y := (exactUniversalQuasiInverseTriangleStrongTrans
          (W := W) A).app Z)
        (exactUniversalQuasiInverseTriangleRepresentativeLiftIso
          (W := W) A Z).hom

/-- Native quasi-inverse triangle modification of the coherent representative
to identity. -/
noncomputable def exactUniversalQuasiInverseTriangleModification :
    exactUniversalQuasiInverseTriangleStrongTrans (W := W) A ≅
      Pseudofunctor.StrongTrans.id
        (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A) :=
  doubleIdentityStrongTransIso
    (exactUniversalAmbientCanonicalSectionPseudofunctor (W := W) A)

@[simp] theorem exactUniversalQuasiInverseTriangleModification_hom_app_lift
    (Z : Ambient (W := W) A) :
    ((exactUniversalQuasiInverseTriangleModification
      (W := W) A).hom.as.app Z).lift =
      (ρ_ (𝟙 Z)).hom := by
  change
    (ρ_ (𝟙 ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).obj Z))).hom.lift =
      (ρ_ (𝟙 Z)).hom
  rw [exactUniversalRealization_source_rightUnitor_lift,
    ExactUniversalRawMorphism.id_lift,
    exactUniversalAmbientCanonicalSectionPseudofunctor_obj_carrier]

/-! ## Regression checks -/

#print axioms doubleIdentityNaturalityIso
#print axioms doubleIdentityStrongTrans
#print axioms doubleIdentityStrongTransIso
#print axioms exactUniversalForwardTriangleApp
#print axioms exactUniversalForwardTriangleApp_eq_doubleIdentity
#print axioms exactUniversalForwardTriangleStrongTrans
#print axioms exactUniversalForwardTriangleModification
#print axioms exactUniversalQuasiInverseTriangleApp
#print axioms exactUniversalQuasiInverseTriangleApp_lift
#print axioms exactUniversalQuasiInverseTriangleStrongTrans
#print axioms exactUniversalQuasiInverseTriangleRepresentativeIso
#print axioms exactUniversalQuasiInverseTriangleRepresentativeIso_realization
#print axioms exactUniversalQuasiInverseTriangleModification
#print axioms exactUniversalQuasiInverseTriangleModification_hom_app_lift

end

end KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16
