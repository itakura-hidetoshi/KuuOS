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

/-- A typed abbreviation of the same certificate. Explicitly ordered universe
parameters are applied in ordinary terms, never inside a notation quotation.
This alias makes no choice and changes no stored field. -/
abbrev value.{u₀, v₀, uH₀, vH₀, uW₀, uP₀}
    {Ctx : Type u₀} [Category.{v₀} Ctx] (W₀ : MorphismProperty Ctx)
    (A₀ : RefinementAtlas.{u₀, max u₀ v₀, uH₀} (LocalizedContext W₀))
    (WL : Type uW₀) (PL : Type uP₀) :
    WhiteheadTriangleRepresentativeCertificate
      (ExactLiftableClassificationObject.{u₀, v₀, uH₀, vH₀, uW₀, uP₀}
        (W := W₀) A₀ WL PL)
      (ExactUniversalClassificationObject.{u₀, v₀, uH₀, vH₀, uW₀, uP₀}
        (W := W₀) A₀ WL PL) :=
  exactLiftableActualLiftCoherentBiequivalenceCertificate (W := W₀) A₀

/-! ## The complete original base data are retained -/

@[simp] theorem base :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base = (exactLiftableActualLiftUnitCounitCertificate (W := W) A :
      WhiteheadUnitCounitCertificate (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) := rfl

@[simp] theorem whitehead :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead = exactLiftableActualLiftWhiteheadBiequivalence (W := W) A := rfl

@[simp] theorem forward :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward =
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor := rfl

@[simp] theorem quasiInverse :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse = actualLiftQuasiInversePseudofunctor (W := W) A := rfl

@[simp] theorem unit :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.unit = actualLiftSourceRoundtripUnit (W := W) A := rfl

@[simp] theorem counit :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.counit = actualLiftTargetRoundtripCounit (W := W) A := rfl

/-! ## Exact native pastes, not unrelated triangle representatives -/

@[simp] theorem forwardTriangle :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleRepresentative = actualLiftForwardTriangle (W := W) A := rfl

@[simp] theorem quasiInverseTriangle :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleRepresentative = actualLiftQuasiInverseTriangle (W := W) A := rfl

/-- Equality of whole StrongTrans records, retaining the original naturality. -/
theorem forwardTriangle_eq_vcomp :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleRepresentative = Pseudofunctor.StrongTrans.vcomp
      (actualLiftProjectedSourceUnit (W := W) A)
      (actualLiftRestrictedTargetCounit (W := W) A) := rfl

/-- The middle pseudofunctor is the proved native G ; (F ; G). -/
theorem quasiInverseTriangle_eq_vcomp :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleRepresentative = Pseudofunctor.StrongTrans.vcomp
      (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A)
      (actualLiftQuasiInverseRestrictedTargetCounitReassociated (W := W) A) := rfl

/-- This formula uses the unit and counit stored in this certificate itself. -/
theorem forwardTriangle_app (X : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleRepresentative.app X =
      (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.map ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.unit.app X) ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.counit.app ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.obj X) := rfl

/-- The reverse component likewise uses precisely this certificate's base. -/
theorem quasiInverseTriangle_app (Y : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleRepresentative.app Y =
      (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.unit.app ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.obj Y) ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.map ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.counit.app Y) := rfl

/-! ## Whole modification isomorphisms and both original component maps -/

@[simp] theorem forwardModification :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification = actualLiftForwardTriangleModificationIso (W := W) A := rfl

@[simp] theorem quasiInverseModification :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification =
      actualLiftQuasiInverseTriangleModificationIso (W := W) A := rfl

@[simp] theorem forwardModification_hom_app (X : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.hom.as.app X =
      (actualLiftForwardTriangleIso (W := W) A X).hom := rfl

@[simp] theorem forwardModification_inv_app (X : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.inv.as.app X =
      (actualLiftForwardTriangleIso (W := W) A X).inv := rfl

@[simp] theorem quasiInverseModification_hom_app (Y : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.hom.as.app Y =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom := rfl

@[simp] theorem quasiInverseModification_inv_app (Y : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.inv.as.app Y =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv := rfl

/-! ## The inherited Whitehead, label and actual-lift boundaries -/

@[simp] theorem forward_obj_label (X : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.obj X).label = X.label := rfl

@[simp] theorem quasiInverse_obj_label (Y : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.obj Y).label = Y.label := rfl

/-- Only an actual-lift-carrying one-cell supplies this prescribed raw map. -/
theorem forward_map_raw {X Y : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)}
    (f : ExactLiftableClassificationActualOneCell (W := W) A X Y) :
    ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.map f).map.raw = f.raw.map := f.raw_eq

/-- The local equivalences still use this certificate's native forward map. -/
theorem homEquiv_forward (X Y : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.homEquiv X Y).functor =
      (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.toPrelaxFunctor.mapFunctor X Y :=
  (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.homEquiv_functor X Y

/-- Retain label-preserving coverage, without identifying presentations. -/
theorem sameLabel_coverage (Y : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    ∃ X : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel), X.label = Y.label ∧
      Nonempty (Bicategory.Equivalence (B := (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.obj X) Y) :=
  exactLiftableActualLiftWhiteheadBiequivalence_sameLabel_coverage (W := W) A Y

/-- The old source component equivalence witnesses the stored unit component. -/
theorem unit_component_equivalence (X : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    ∃ e : Bicategory.Equivalence (B := (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) X
        ((Pseudofunctor.comp (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse).obj X),
      e.hom = (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.unit.app X :=
  ⟨actualLiftSourceUnitComponentEquivalence (W := W) A X, rfl⟩

/-- Use the same fixed e_Y, not a new objectwise choice. -/
theorem counit_component_equivalence (Y : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    ∃ e : Bicategory.Equivalence (B := (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel))
        ((Pseudofunctor.comp (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward).obj Y) Y,
      e.hom = (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.counit.app Y :=
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

example (X Y : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.toPrelaxFunctor.mapFunctor X Y).IsEquivalence :=
  exactLiftableActualLiftNativeMapFunctor_isEquivalence (W := W) A X Y

example (X : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleRepresentative.app X =
      (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.map ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.unit.app X) ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.counit.app ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.obj X) := rfl

example (Y : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleRepresentative.app Y =
      (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.unit.app ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.obj Y) ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.map ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.counit.app Y) := rfl

example {X Y : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)} (f : X ⟶ Y) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.map f ◁ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.hom.as.app Y ≫
        ((Pseudofunctor.StrongTrans.id (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward).naturality f).hom =
      ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleRepresentative.naturality f).hom ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.hom.as.app X ▷ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.map f :=
  (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.hom.as.naturality f

example {X Y : (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)} (f : X ⟶ Y) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.map f ◁ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.inv.as.app Y ≫
        ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleRepresentative.naturality f).hom =
      ((Pseudofunctor.StrongTrans.id (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward).naturality f).hom ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.inv.as.app X ▷ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.whitehead.forward.map f :=
  (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).forwardTriangleModification.inv.as.naturality f

example {Y Z : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)} (f : Y ⟶ Z) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.map f ◁ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.hom.as.app Z ≫
        ((Pseudofunctor.StrongTrans.id (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse).naturality f).hom =
      ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleRepresentative.naturality f).hom ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.hom.as.app Y ▷ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.map f :=
  (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.hom.as.naturality f

example {Y Z : (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)} (f : Y ⟶ Z) :
    (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.map f ◁ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.inv.as.app Z ≫
        ((value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleRepresentative.naturality f).hom =
      ((Pseudofunctor.StrongTrans.id (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse).naturality f).hom ≫
        (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.inv.as.app Y ▷ (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).base.quasiInverse.map f :=
  (value.{u, v, uH, vH, uW, uP} W A WorldLabel PresentationLabel).quasiInverseTriangleModification.inv.as.naturality f

end Certificate

/-! The reused generic certificate fields retain their four global inverse
laws. These tests keep the two ambient bicategories explicit and use exactly
the native homCategory already specified by the certificate field types. -/
section GlobalInverseRegression

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (P : WhiteheadTriangleRepresentativeCertificate B C)

-- Expose exactly Mathlib's existing hom categories at these typed endpoints.
-- Neither modification composition nor its identity is replaced.
local instance forwardHomCategory :
    Category (Pseudofunctor.StrongTrans (B := B) (C := C)
      P.base.whitehead.forward P.base.whitehead.forward) :=
  Pseudofunctor.StrongTrans.homCategory (B := B) (C := C)
    (F := P.base.whitehead.forward) (G := P.base.whitehead.forward)

local instance quasiInverseHomCategory :
    Category (Pseudofunctor.StrongTrans (B := C) (C := B)
      P.base.quasiInverse P.base.quasiInverse) :=
  Pseudofunctor.StrongTrans.homCategory (B := C) (C := B)
    (F := P.base.quasiInverse) (G := P.base.quasiInverse)

example : Category (Pseudofunctor.StrongTrans (B := B) (C := C)
    P.base.whitehead.forward P.base.whitehead.forward) := inferInstance

example : Category (Pseudofunctor.StrongTrans (B := C) (C := B)
    P.base.quasiInverse P.base.quasiInverse) := inferInstance

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
#print axioms Certificate.value
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
