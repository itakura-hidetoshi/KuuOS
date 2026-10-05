import KUOS.DependentOriginationClassificationUnitCounitCertificateV5_29
import KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16
import KUOS.DependentOriginationExactClassificationHomFunctorV5_22
import KUOS.DependentOriginationExactClassificationBicategoryV5_23
import Mathlib

namespace KUOS.DependentOriginationClassificationTriangleCoherenceV5_30

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactClassificationBicategoryV5_23
open KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
open KUOS.DependentOriginationClassificationCanonicalSectionV5_28
open KUOS.DependentOriginationClassificationUnitCounitCertificateV5_29
open KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Classification triangle coherence v5.30

v5.29 gives the full labelled classification realization

  R : ExactUniversalClassification -> LocalizedClassification

together with the label-preserving canonical section

  S : LocalizedClassification -> ExactUniversalClassification,

a source unit `id => R ; S`, and a target counit `S ; R => id`.

This theorem unit mirrors the already validated ambient v5.16 triangle layer.
It does not invent a new higher-categorical coherence argument.  Instead:

* the actual forward triangle component `R η ; ε R` projects to the ambient
  double identity;
* the actual quasi-inverse triangle component `η S ; S ε` projects to the
  already validated v5.16 exact-source component;
* the coherent representatives are the generic
  `doubleIdentityStrongTrans` representatives;
* the native invertible modifications from those representatives to identity
  are exactly the generic `doubleIdentityStrongTransIso`.

The external classification labels remain untouched.  They contribute only
proposition-valued equality proofs on 1-cells and therefore do not alter the
2-dimensional triangle calculation.

As in v5.16, this records coherent triangle representatives and native
invertible modifications.  It does not claim a stronger tricategorical
adjoint-biequivalence structure absent from the current Mathlib API.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

abbrev Source
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  ExactUniversalClassificationObject
    (W := W) A WorldLabel PresentationLabel

abbrev Target
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  LocalizedClassificationObject
    (W := W) A WorldLabel PresentationLabel

/-! ## One-cell extensionality through the mathematical map -/

/-- A localized classification 1-cell is determined by its DO₂ map.  The
remaining field is a proof of the same fixed label equality and is therefore
proof-irrelevant. -/
@[ext] theorem LocalizedClassificationOneCell.ext
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    {f g : LocalizedClassificationOneCell (W := W) A X Y}
    (h : f.map = g.map) :
    f = g := by
  cases f
  cases g
  cases h
  rfl

/-- An exact-universal classification 1-cell is determined by its validated
exact-source map; label-equality proofs are again proof-irrelevant. -/
@[ext] theorem ExactUniversalClassificationOneCell.ext
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Source (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (h : f.map = g.map) :
    f = g := by
  cases f
  cases g
  cases h
  rfl

/-! ## Forward triangle -/

/-- Actual labelled forward triangle component `R η ; ε R`. -/
noncomputable def exactUniversalClassificationForwardTriangleApp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationRealization
      (W := W) A).obj X ⟶
      (exactUniversalClassificationRealization
        (W := W) A).obj X :=
  (exactUniversalClassificationRealization
    (W := W) A).map
      ((exactUniversalClassificationSourceRoundtripUnit
        (W := W) A).app X) ≫
    (exactUniversalClassificationTargetRoundtripCounit
      (W := W) A).app
        ((exactUniversalClassificationRealization
          (W := W) A).obj X)

/-- The actual forward triangle projects exactly to the ambient double
identity. -/
@[simp] theorem exactUniversalClassificationForwardTriangleApp_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationForwardTriangleApp
      (W := W) A X).map =
      𝟙 X.source.carrier ≫ 𝟙 X.source.carrier := by
  change
    ((exactUniversalClassificationSourceRoundtripUnit
      (W := W) A).app X).map.lift ≫
      ((exactUniversalClassificationTargetRoundtripCounit
        (W := W) A).app
          ((exactUniversalClassificationRealization
            (W := W) A).obj X)).map =
      𝟙 X.source.carrier ≫ 𝟙 X.source.carrier
  rw [exactUniversalClassificationSourceRoundtripUnit_app_map,
    exactUniversalSourceAmbientRoundtripUnit_app_lift,
    exactUniversalClassificationTargetRoundtripCounit_app_underlying,
    exactUniversalAmbientRoundtripCounit_app]
  rfl

/-- Coherent forward-triangle representative on the labelled realization. -/
noncomputable def exactUniversalClassificationForwardTriangleStrongTrans
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Pseudofunctor.StrongTrans
      (exactUniversalClassificationRealization
        (W := W) A).toPseudofunctor
      (exactUniversalClassificationRealization
        (W := W) A).toPseudofunctor :=
  doubleIdentityStrongTrans
    (exactUniversalClassificationRealization
      (W := W) A).toPseudofunctor

@[simp] theorem exactUniversalClassificationForwardTriangleStrongTrans_app_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationForwardTriangleStrongTrans
      (W := W) A).app X).map =
      𝟙 X.source.carrier ≫ 𝟙 X.source.carrier :=
  rfl

/-- The actual labelled forward-triangle component is exactly the component of
the coherent representative. -/
@[simp] theorem exactUniversalClassificationForwardTriangleApp_eq_representative
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    exactUniversalClassificationForwardTriangleApp (W := W) A X =
      (exactUniversalClassificationForwardTriangleStrongTrans
        (W := W) A).app X := by
  apply LocalizedClassificationOneCell.ext
  rw [exactUniversalClassificationForwardTriangleApp_map,
    exactUniversalClassificationForwardTriangleStrongTrans_app_map]

/-- Native invertible modification from the coherent forward-triangle
representative to the identity strong transformation. -/
noncomputable def exactUniversalClassificationForwardTriangleModification
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :=
  doubleIdentityStrongTransIso
    (exactUniversalClassificationRealization
      (W := W) A).toPseudofunctor

/-! ## Quasi-inverse triangle -/

/-- Actual labelled quasi-inverse triangle component `η S ; S ε`. -/
noncomputable def exactUniversalClassificationQuasiInverseTriangleApp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationCanonicalSection
      (W := W) A).obj Z ⟶
      (exactUniversalClassificationCanonicalSection
        (W := W) A).obj Z :=
  (exactUniversalClassificationSourceRoundtripUnit
    (W := W) A).app
      ((exactUniversalClassificationCanonicalSection
        (W := W) A).obj Z) ≫
    (exactUniversalClassificationCanonicalSection
      (W := W) A).map
        ((exactUniversalClassificationTargetRoundtripCounit
          (W := W) A).app Z)

/-- Forgetting the external label gives exactly the already validated v5.16
exact-source quasi-inverse triangle component. -/
@[simp] theorem exactUniversalClassificationQuasiInverseTriangleApp_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationQuasiInverseTriangleApp
      (W := W) A Z).map =
      exactUniversalQuasiInverseTriangleApp
        (W := W) A Z.carrier :=
  rfl

/-- Consequently the realized quasi-inverse triangle is the ambient double
identity. -/
@[simp] theorem exactUniversalClassificationQuasiInverseTriangleApp_map_lift
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationQuasiInverseTriangleApp
      (W := W) A Z).map.lift =
      𝟙 Z.carrier ≫ 𝟙 Z.carrier := by
  rw [exactUniversalClassificationQuasiInverseTriangleApp_map]
  exact
    exactUniversalQuasiInverseTriangleApp_lift
      (W := W) A Z.carrier

/-- Coherent quasi-inverse-triangle representative on the label-preserving
classification section. -/
noncomputable def exactUniversalClassificationQuasiInverseTriangleStrongTrans
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Pseudofunctor.StrongTrans
      (exactUniversalClassificationCanonicalSection
        (W := W) A)
      (exactUniversalClassificationCanonicalSection
        (W := W) A) :=
  doubleIdentityStrongTrans
    (exactUniversalClassificationCanonicalSection
      (W := W) A)

@[simp] theorem exactUniversalClassificationQuasiInverseTriangleStrongTrans_app_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationQuasiInverseTriangleStrongTrans
      (W := W) A).app Z).map =
      (exactUniversalQuasiInverseTriangleStrongTrans
        (W := W) A).app Z.carrier :=
  rfl

@[simp] theorem exactUniversalClassificationQuasiInverseTriangleStrongTrans_app_map_lift
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationQuasiInverseTriangleStrongTrans
      (W := W) A).app Z).map.lift =
      𝟙 Z.carrier ≫ 𝟙 Z.carrier := by
  rw [exactUniversalClassificationQuasiInverseTriangleStrongTrans_app_map]
  exact
    exactUniversalQuasiInverseTriangleStrongTrans_app_lift
      (W := W) A Z.carrier

/-- Lift the v5.16 exact-source representative comparison through the labelled
classification wrapper. -/
noncomputable def exactUniversalClassificationQuasiInverseTriangleRepresentativeIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    exactUniversalClassificationQuasiInverseTriangleApp
        (W := W) A Z ≅
      (exactUniversalClassificationQuasiInverseTriangleStrongTrans
        (W := W) A).app Z := by
  apply ExactUniversalClassificationTwoCell.isoOfUnderlying (W := W) A
  simpa only [
    exactUniversalClassificationQuasiInverseTriangleApp_map,
    exactUniversalClassificationQuasiInverseTriangleStrongTrans_app_map
  ] using
    (exactUniversalQuasiInverseTriangleRepresentativeIso
      (W := W) A Z.carrier)

@[simp] theorem
    exactUniversalClassificationQuasiInverseTriangleRepresentativeIso_hom_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationQuasiInverseTriangleRepresentativeIso
      (W := W) A Z).hom.cell =
      (exactUniversalQuasiInverseTriangleRepresentativeIso
        (W := W) A Z.carrier).hom :=
  rfl

/-- Native invertible modification from the coherent quasi-inverse-triangle
representative to the identity strong transformation. -/
noncomputable def exactUniversalClassificationQuasiInverseTriangleModification
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :=
  doubleIdentityStrongTransIso
    (exactUniversalClassificationCanonicalSection
      (W := W) A)

/-!
## Boundary after v5.30

At the classification level we now have:

* v5.27: local hom equivalence + object coverage;
* v5.28: explicit label-preserving quasi-inverse pseudofunctor;
* v5.29: source unit + target counit StrongTrans;
* v5.30: coherent forward/quasi-inverse triangle representatives and native
  invertible modifications to identity.

The statement is deliberately the same strength as ambient v5.16.  In
particular it does not manufacture a stronger tricategorical
adjoint-biequivalence object, and it does not alter the v5.19 boundary for
arbitrary raw/exact-liftable systems.
-/

/-! ## Regression checks -/

section Regression

variable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel)
    (Z : Target (W := W) A WorldLabel PresentationLabel)

example :
    exactUniversalClassificationForwardTriangleApp (W := W) A X =
      (exactUniversalClassificationForwardTriangleStrongTrans
        (W := W) A).app X :=
  exactUniversalClassificationForwardTriangleApp_eq_representative
    (W := W) A X

example :
    Nonempty
      (exactUniversalClassificationQuasiInverseTriangleApp
          (W := W) A Z ≅
        (exactUniversalClassificationQuasiInverseTriangleStrongTrans
          (W := W) A).app Z) :=
  ⟨exactUniversalClassificationQuasiInverseTriangleRepresentativeIso
    (W := W) A Z⟩

end Regression

#print axioms LocalizedClassificationOneCell.ext
#print axioms ExactUniversalClassificationOneCell.ext
#print axioms exactUniversalClassificationForwardTriangleApp
#print axioms exactUniversalClassificationForwardTriangleApp_eq_representative
#print axioms exactUniversalClassificationForwardTriangleModification
#print axioms exactUniversalClassificationQuasiInverseTriangleApp
#print axioms exactUniversalClassificationQuasiInverseTriangleRepresentativeIso
#print axioms exactUniversalClassificationQuasiInverseTriangleModification

end

end KUOS.DependentOriginationClassificationTriangleCoherenceV5_30
