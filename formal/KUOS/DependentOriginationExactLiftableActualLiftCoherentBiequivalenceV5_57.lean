import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
import KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31

namespace KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
open KUOS.DependentOriginationClassificationUnitCounitCertificateV5_29
open KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31

set_option autoImplicit false

noncomputable section

/-!
# Integrated actual-lift coherent biequivalence certificate v5.57

Reuse the generic certificate TYPES of v5.29/v5.31, not their old
localized-classification instances. Every stored datum belongs to the same
actual-lift pair: the v5.45 Whitehead datum, v5.48 G, v5.50 eta, v5.49 eps,
the actual v5.52/v5.55 triangles, and their v5.52/v5.56 modifications.

The generic type allows triangle representatives. This concrete certificate
stores the ACTUAL native vcomp constructions. Reflexive projection equations
retain the complete old transformations and modification isomorphisms, not
merely their object components. Component equations additionally connect the
stored triangles directly to the unit/counit in the certificate's own base.

No new equivalence, inverse, comparison, or proof of a stronger coherence
property is chosen. Additional higher adjoint-biequivalence coherence,
arbitrary raw-morphism liftability, equality of independent presentations,
atlas-universe reindexing, and strict preservation of conjugated raw maps
are not asserted by this integration.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The original Whitehead datum, G, eta and eps in one native base package.
The explicit endpoint types fix all six universes before the body. -/
def exactLiftableActualLiftUnitCounitCertificate :
    WhiteheadUnitCounitCertificate
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  whitehead := exactLiftableActualLiftWhiteheadBiequivalence (W := W) A
  quasiInverse := actualLiftQuasiInversePseudofunctor (W := W) A
  unit := actualLiftSourceRoundtripUnit (W := W) A
  counit := actualLiftTargetRoundtripCounit (W := W) A

/-- The integrated certificate at exactly the already-proved native level.
The modification fields retain the old isomorphisms, including their inverse
naturality and global inverse laws. They are not rebuilt from components. -/
def exactLiftableActualLiftCoherentBiequivalenceCertificate :
    WhiteheadTriangleRepresentativeCertificate
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  base := exactLiftableActualLiftUnitCounitCertificate (W := W) A
  forwardTriangleRepresentative := actualLiftForwardTriangle (W := W) A
  forwardTriangleModification := actualLiftForwardTriangleModificationIso (W := W) A
  quasiInverseTriangleRepresentative := actualLiftQuasiInverseTriangle (W := W) A
  quasiInverseTriangleModification := actualLiftQuasiInverseTriangleModificationIso (W := W) A

namespace Certificate

-- These local notations are only explicit type annotations. In particular,
-- vH and the two label universes remain independent in every declaration.
local notation "L" => ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
  (W := W) A WorldLabel PresentationLabel
local notation "E" => ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
  (W := W) A WorldLabel PresentationLabel
local notation "C₀" => (exactLiftableActualLiftCoherentBiequivalenceCertificate (W := W) A :
  WhiteheadTriangleRepresentativeCertificate L E)

/-! ## The complete original base data are retained -/

@[simp] theorem base :
    C₀.base = (exactLiftableActualLiftUnitCounitCertificate (W := W) A :
      WhiteheadUnitCounitCertificate L E) := rfl

@[simp] theorem whitehead :
    C₀.base.whitehead = exactLiftableActualLiftWhiteheadBiequivalence (W := W) A := rfl

@[simp] theorem forward :
    C₀.base.whitehead.forward =
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor := rfl

@[simp] theorem quasiInverse :
    C₀.base.quasiInverse = actualLiftQuasiInversePseudofunctor (W := W) A := rfl

@[simp] theorem unit :
    C₀.base.unit = actualLiftSourceRoundtripUnit (W := W) A := rfl

@[simp] theorem counit :
    C₀.base.counit = actualLiftTargetRoundtripCounit (W := W) A := rfl

/-! ## Exact native pastes, not unrelated triangle representatives -/

@[simp] theorem forwardTriangle :
    C₀.forwardTriangleRepresentative = actualLiftForwardTriangle (W := W) A := rfl

@[simp] theorem quasiInverseTriangle :
    C₀.quasiInverseTriangleRepresentative = actualLiftQuasiInverseTriangle (W := W) A := rfl

/-- Equality of whole StrongTrans records, retaining the original naturality. -/
theorem forwardTriangle_eq_vcomp :
    C₀.forwardTriangleRepresentative = Pseudofunctor.StrongTrans.vcomp
      (actualLiftProjectedSourceUnit (W := W) A)
      (actualLiftRestrictedTargetCounit (W := W) A) := rfl

/-- The middle pseudofunctor is the proved native G ; (F ; G). -/
theorem quasiInverseTriangle_eq_vcomp :
    C₀.quasiInverseTriangleRepresentative = Pseudofunctor.StrongTrans.vcomp
      (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A)
      (actualLiftQuasiInverseRestrictedTargetCounitReassociated (W := W) A) := rfl

/-- This formula uses the unit and counit stored in this certificate itself. -/
theorem forwardTriangle_app (X : L) :
    C₀.forwardTriangleRepresentative.app X =
      C₀.base.whitehead.forward.map (C₀.base.unit.app X) ≫
        C₀.base.counit.app (C₀.base.whitehead.forward.obj X) := rfl

/-- The reverse component likewise uses precisely this certificate's base. -/
theorem quasiInverseTriangle_app (Y : E) :
    C₀.quasiInverseTriangleRepresentative.app Y =
      C₀.base.unit.app (C₀.base.quasiInverse.obj Y) ≫
        C₀.base.quasiInverse.map (C₀.base.counit.app Y) := rfl

/-! ## Whole modification isomorphisms and both original component maps -/

@[simp] theorem forwardModification :
    C₀.forwardTriangleModification = actualLiftForwardTriangleModificationIso (W := W) A := rfl

@[simp] theorem quasiInverseModification :
    C₀.quasiInverseTriangleModification =
      actualLiftQuasiInverseTriangleModificationIso (W := W) A := rfl

@[simp] theorem forwardModification_hom_app (X : L) :
    C₀.forwardTriangleModification.hom.as.app X =
      (actualLiftForwardTriangleIso (W := W) A X).hom := rfl

@[simp] theorem forwardModification_inv_app (X : L) :
    C₀.forwardTriangleModification.inv.as.app X =
      (actualLiftForwardTriangleIso (W := W) A X).inv := rfl

@[simp] theorem quasiInverseModification_hom_app (Y : E) :
    C₀.quasiInverseTriangleModification.hom.as.app Y =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom := rfl

@[simp] theorem quasiInverseModification_inv_app (Y : E) :
    C₀.quasiInverseTriangleModification.inv.as.app Y =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv := rfl

/-! ## The inherited Whitehead, label and actual-lift boundaries -/

@[simp] theorem forward_obj_label (X : L) :
    (C₀.base.whitehead.forward.obj X).label = X.label := rfl

@[simp] theorem quasiInverse_obj_label (Y : E) :
    (C₀.base.quasiInverse.obj Y).label = Y.label := rfl

/-- Only an actual-lift-carrying one-cell supplies this prescribed raw map. -/
theorem forward_map_raw {X Y : L}
    (f : ExactLiftableClassificationActualOneCell (W := W) A X Y) :
    (C₀.base.whitehead.forward.map f).map.raw = f.raw.map := f.raw_eq

/-- The local equivalences still use this certificate's native forward map. -/
theorem homEquiv_forward (X Y : L) :
    (C₀.base.whitehead.homEquiv X Y).functor =
      C₀.base.whitehead.forward.toPrelaxFunctor.mapFunctor X Y :=
  C₀.base.whitehead.homEquiv_functor X Y

/-- Retain label-preserving coverage, without identifying presentations. -/
theorem sameLabel_coverage (Y : E) :
    ∃ X : L, X.label = Y.label ∧
      Nonempty (Bicategory.Equivalence (B := E) (C₀.base.whitehead.forward.obj X) Y) :=
  exactLiftableActualLiftWhiteheadBiequivalence_sameLabel_coverage (W := W) A Y

/-- The old source component equivalence witnesses the stored unit component. -/
theorem unit_component_equivalence (X : L) :
    ∃ e : Bicategory.Equivalence (B := L) X
        ((Pseudofunctor.comp C₀.base.whitehead.forward C₀.base.quasiInverse).obj X),
      e.hom = C₀.base.unit.app X :=
  ⟨actualLiftSourceUnitComponentEquivalence (W := W) A X, rfl⟩

/-- Use the same fixed e_Y, not a new objectwise choice. -/
theorem counit_component_equivalence (Y : E) :
    ∃ e : Bicategory.Equivalence (B := E)
        ((Pseudofunctor.comp C₀.base.quasiInverse C₀.base.whitehead.forward).obj Y) Y,
      e.hom = C₀.base.counit.app Y :=
  ⟨actualLiftQuasiInverseObjectEquivalence (W := W) A Y, rfl⟩

/-! ## Concrete regressions through the integrated native interface -/

-- Regression: the full certificate belongs to the actual-lift source, not
-- the older localized-classification source, with all universes explicit.
example : WhiteheadTriangleRepresentativeCertificate
    (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  exactLiftableActualLiftCoherentBiequivalenceCertificate (W := W) A

example (X Y : L) :
    (C₀.base.whitehead.forward.toPrelaxFunctor.mapFunctor X Y).IsEquivalence :=
  exactLiftableActualLiftNativeMapFunctor_isEquivalence (W := W) A X Y

example (X : L) :
    C₀.forwardTriangleRepresentative.app X =
      C₀.base.whitehead.forward.map (C₀.base.unit.app X) ≫
        C₀.base.counit.app (C₀.base.whitehead.forward.obj X) := rfl

example (Y : E) :
    C₀.quasiInverseTriangleRepresentative.app Y =
      C₀.base.unit.app (C₀.base.quasiInverse.obj Y) ≫
        C₀.base.quasiInverse.map (C₀.base.counit.app Y) := rfl

example {X Y : L} (f : X ⟶ Y) :
    C₀.base.whitehead.forward.map f ◁ C₀.forwardTriangleModification.hom.as.app Y ≫
        ((Pseudofunctor.StrongTrans.id C₀.base.whitehead.forward).naturality f).hom =
      (C₀.forwardTriangleRepresentative.naturality f).hom ≫
        C₀.forwardTriangleModification.hom.as.app X ▷ C₀.base.whitehead.forward.map f :=
  C₀.forwardTriangleModification.hom.as.naturality f

example {X Y : L} (f : X ⟶ Y) :
    C₀.base.whitehead.forward.map f ◁ C₀.forwardTriangleModification.inv.as.app Y ≫
        (C₀.forwardTriangleRepresentative.naturality f).hom =
      ((Pseudofunctor.StrongTrans.id C₀.base.whitehead.forward).naturality f).hom ≫
        C₀.forwardTriangleModification.inv.as.app X ▷ C₀.base.whitehead.forward.map f :=
  C₀.forwardTriangleModification.inv.as.naturality f

example {Y Z : E} (f : Y ⟶ Z) :
    C₀.base.quasiInverse.map f ◁ C₀.quasiInverseTriangleModification.hom.as.app Z ≫
        ((Pseudofunctor.StrongTrans.id C₀.base.quasiInverse).naturality f).hom =
      (C₀.quasiInverseTriangleRepresentative.naturality f).hom ≫
        C₀.quasiInverseTriangleModification.hom.as.app Y ▷ C₀.base.quasiInverse.map f :=
  C₀.quasiInverseTriangleModification.hom.as.naturality f

example {Y Z : E} (f : Y ⟶ Z) :
    C₀.base.quasiInverse.map f ◁ C₀.quasiInverseTriangleModification.inv.as.app Z ≫
        (C₀.quasiInverseTriangleRepresentative.naturality f).hom =
      ((Pseudofunctor.StrongTrans.id C₀.base.quasiInverse).naturality f).hom ≫
        C₀.quasiInverseTriangleModification.inv.as.app Y ▷ C₀.base.quasiInverse.map f :=
  C₀.quasiInverseTriangleModification.inv.as.naturality f

end Certificate

/-! The reused generic certificate fields retain their four global inverse
laws. These tests keep the two ambient bicategories explicit and use exactly
the native homCategory already specified by the certificate field types. -/
section GlobalInverseRegression

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (P : WhiteheadTriangleRepresentativeCertificate B C)

example : P.forwardTriangleModification.hom ≫ P.forwardTriangleModification.inv =
    𝟙 P.forwardTriangleRepresentative := P.forwardTriangleModification.hom_inv_id

example : P.forwardTriangleModification.inv ≫ P.forwardTriangleModification.hom =
    𝟙 (Pseudofunctor.StrongTrans.id P.base.whitehead.forward) :=
  P.forwardTriangleModification.inv_hom_id

example : P.quasiInverseTriangleModification.hom ≫ P.quasiInverseTriangleModification.inv =
    𝟙 P.quasiInverseTriangleRepresentative := P.quasiInverseTriangleModification.hom_inv_id

example : P.quasiInverseTriangleModification.inv ≫ P.quasiInverseTriangleModification.hom =
    𝟙 (Pseudofunctor.StrongTrans.id P.base.quasiInverse) :=
  P.quasiInverseTriangleModification.inv_hom_id

end GlobalInverseRegression

/-!
## Boundary after v5.57

The same actual-lift F/G/eta/eps, Whitehead datum, two actual native triangles,
and their original global invertible modifications are now one certificate.
The projection equations are stronger than a claim that some representatives
exist: they identify the complete stored records with the original pastes.
This closes integration at the proved native level, without manufacturing
additional higher adjoint-biequivalence coherence or changing the raw boundary.
-/

#print axioms exactLiftableActualLiftUnitCounitCertificate
#print axioms exactLiftableActualLiftCoherentBiequivalenceCertificate
#print axioms Certificate.base
#print axioms Certificate.whitehead
#print axioms Certificate.forward
#print axioms Certificate.quasiInverse
#print axioms Certificate.unit
#print axioms Certificate.counit
#print axioms Certificate.forwardTriangle_eq_vcomp
#print axioms Certificate.quasiInverseTriangle_eq_vcomp
#print axioms Certificate.forwardTriangle_app
#print axioms Certificate.quasiInverseTriangle_app
#print axioms Certificate.forwardModification
#print axioms Certificate.quasiInverseModification
#print axioms Certificate.forwardModification_hom_app
#print axioms Certificate.forwardModification_inv_app
#print axioms Certificate.quasiInverseModification_hom_app
#print axioms Certificate.quasiInverseModification_inv_app
#print axioms Certificate.forward_obj_label
#print axioms Certificate.quasiInverse_obj_label
#print axioms Certificate.forward_map_raw
#print axioms Certificate.homEquiv_forward
#print axioms Certificate.sameLabel_coverage
#print axioms Certificate.unit_component_equivalence
#print axioms Certificate.counit_component_equivalence

end

end KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57
