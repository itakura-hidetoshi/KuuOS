import KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
import Mathlib.CategoryTheory.Bicategory.Modification.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51

set_option autoImplicit false

noncomputable section

/-!
# Actual forward triangle invertible modification v5.52

Keep the original F, G, eta, eps, and object equivalences.  Form the native
triple (F;G);F.  The two transformations F => (F;G);F => F have exactly the
projected old unit and the old counit restricted along F, including their
naturality isomorphisms.  Their native vertical composite is the actual
forward triangle, rather than an identity transported along pointwise isos.

The original counits satisfy the modification naturality square for this
paste.  The generic proof exchanges the two contractions and cancels the
original counit inverse.  Mathlib isoMk then supplies inverse naturality and
both inverse laws.  The backward global triangle remains a separate unit.
-/

namespace ForwardTriangle

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c x y z : B}

/-- The actual vertical pasting of the fixed unit/counit naturalities. -/
def naturalityIso (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (f : x ⟶ y) :
    f ≫ (ey.inv ≫ ey.hom) ≅ (ex.inv ≫ ex.hom) ≫ f :=
  (α_ f ey.inv ey.hom).symm ≪≫
    Bicategory.whiskerRightIso (B := B)
      (ConjugationUnit.naturalityIso ex ey f) ey.hom ≪≫
    (α_ ex.inv ((Conjugation.homFunctor ex ey).obj f) ey.hom) ≪≫
    Bicategory.whiskerLeftIso (B := B) ex.inv
      (ConjugationCounit.naturalityIso ex ey f) ≪≫
    (α_ ex.inv ex.hom f).symm

/-- The counit is natural for the actual paste, not just for some
transformation having the same object components. -/
theorem naturality (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (f : x ⟶ y) :
    f ◁ ey.counit.hom ≫ (ρ_ f).hom ≫ (λ_ f).inv =
      (naturalityIso ex ey f).hom ≫ ex.counit.hom ▷ f := by
  symm
  calc
    _ = 𝟙 (f ≫ (ey.inv ≫ ey.hom)) ⊗≫
        ((ex.counit.inv ▷ f) ▷ (ey.inv ≫ ey.hom) ≫
          (((ex.inv ≫ ex.hom) ≫ f) ◁ ey.counit.hom ≫
            (ex.counit.hom ▷ f) ▷ (𝟙 y))) ⊗≫
        𝟙 ((𝟙 x) ≫ f) := by
      dsimp [naturalityIso, ConjugationUnit.naturalityIso,
        ConjugationCounit.naturalityIso, Conjugation.homFunctor]
      bicategory
    _ = 𝟙 (f ≫ (ey.inv ≫ ey.hom)) ⊗≫
        (((ex.counit.inv ▷ f) ▷ (ey.inv ≫ ey.hom) ≫
          (ex.counit.hom ▷ f) ▷ (ey.inv ≫ ey.hom)) ≫
            (𝟙 x ≫ f) ◁ ey.counit.hom) ⊗≫
        𝟙 ((𝟙 x) ≫ f) := by
      rw [Bicategory.whisker_exchange (B := B)
        (ex.counit.hom ▷ f) ey.counit.hom]
      simp only [Category.assoc]
    _ = _ := by
      rw [← Bicategory.comp_whiskerRight, ← Bicategory.comp_whiskerRight,
        Iso.inv_hom_id]
      bicategory

/-- Typed identity-comparison cancellation for the native triple.
Prove this generically before specializing the concrete classification types. -/
theorem mapId_hom (ex : Bicategory.Equivalence a x) :
    ((Conjugation.homFunctor ex ex).map (𝟙 (𝟙 x)) ≫
      (Conjugation.idIso ex).hom) ≫ 𝟙 (𝟙 a) =
        (Conjugation.idIso ex).hom :=
  (Category.comp_id _).trans (ConjugationUnit.map_id_idIso_hom ex)

/-- The triple retains exactly the original conjugation compositor. -/
theorem mapComp_hom (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    ((Conjugation.homFunctor ex ez).map (𝟙 (f ≫ g)) ≫
      (Conjugation.compIso ex ey ez f g).hom) ≫
        𝟙 ((Conjugation.homFunctor ex ey).obj f ≫
          (Conjugation.homFunctor ey ez).obj g) =
            (Conjugation.compIso ex ey ez f g).hom :=
  (Category.comp_id _).trans (ConjugationUnit.map_id_compIso_hom ex ey ez f g)

end ForwardTriangle

/-! ## The fixed native triple and the two genuinely pasted factors -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The actual source roundtrip followed by the original strict projection. -/
def actualLiftForwardTriple :
    Pseudofunctor
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.comp (actualLiftSourceRoundtrip (W := W) A)
    (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor

@[simp] theorem actualLiftForwardTriple_mapId_hom
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftForwardTriple (W := W) A).mapId X).hom =
      (Conjugation.idIso (actualLiftSourceObjectEquivalence (W := W) A X)).hom :=
  ForwardTriangle.mapId_hom (actualLiftSourceObjectEquivalence (W := W) A X)

@[simp] theorem actualLiftForwardTriple_mapComp_hom
    {X Y Z : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((actualLiftForwardTriple (W := W) A).mapComp f g).hom =
      (Conjugation.compIso (actualLiftSourceObjectEquivalence (W := W) A X)
        (actualLiftSourceObjectEquivalence (W := W) A Y)
        (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift).hom :=
  ForwardTriangle.mapComp_hom (actualLiftSourceObjectEquivalence (W := W) A X)
    (actualLiftSourceObjectEquivalence (W := W) A Y)
    (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift

private theorem projection_mapId_hom
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor.mapId X).hom =
      𝟙 (𝟙 (CanonicalExactUniversalObject (W := W) A X)) := rfl

private theorem projection_mapComp_hom
    {X Y Z : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor.mapComp f g).hom =
      𝟙 (f.actualLift ≫ g.actualLift) := rfl

/-- Project the old source unit through F.  The naturality projection is
recorded below, so this is not an unrelated pointwise replacement. -/
def actualLiftProjectedSourceUnit :
    Pseudofunctor.StrongTrans
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
      (actualLiftForwardTriple (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) where
  app X := (exactLiftableActualLiftStrictPseudofunctor (W := W) A).map
    ((actualLiftSourceRoundtripUnit (W := W) A).app X)
  naturality {X Y} f := ConjugationUnit.naturalityIso
    (actualLiftSourceObjectEquivalence (W := W) A X)
    (actualLiftSourceObjectEquivalence (W := W) A Y) f.actualLift
  naturality_naturality {X Y} {f g} theta := by
    exact ConjugationUnit.naturality (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A Y) theta
  naturality_id X := by
    rw [actualLiftForwardTriple_mapId_hom, projection_mapId_hom]
    exact ConjugationUnit.id (actualLiftSourceObjectEquivalence (W := W) A X)
  naturality_comp {X Y Z} f g := by
    rw [actualLiftForwardTriple_mapComp_hom, projection_mapComp_hom]
    exact ConjugationUnit.comp (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A Y)
      (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift

/-- The naturality is exactly F applied to the old unit naturality. -/
@[simp] theorem actualLiftProjectedSourceUnit_naturality
    {X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    (actualLiftProjectedSourceUnit (W := W) A).naturality f =
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor.map₂Iso
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality f) := by
  apply Iso.ext
  rfl

/-- Restrict the original target counit along F, with its old naturality. -/
def actualLiftRestrictedTargetCounit :
    Pseudofunctor.StrongTrans
      (actualLiftForwardTriple (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor where
  app X := (actualLiftTargetRoundtripCounit (W := W) A).app
    ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).obj X)
  naturality f := (actualLiftTargetRoundtripCounit (W := W) A).naturality
    ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).map f)
  naturality_naturality {X Y} {f g} theta := by
    exact ConjugationCounit.naturality (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A Y) theta
  naturality_id X := by
    rw [actualLiftForwardTriple_mapId_hom, projection_mapId_hom]
    exact (ConjugationCounit.naturality_hom_comp_whiskerLeft_id
      (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A X)
      (𝟙 (CanonicalExactUniversalObject (W := W) A X))).trans
        (ConjugationCounit.id (actualLiftSourceObjectEquivalence (W := W) A X))
  naturality_comp {X Y Z} f g := by
    rw [actualLiftForwardTriple_mapComp_hom, projection_mapComp_hom]
    exact (ConjugationCounit.naturality_hom_comp_whiskerLeft_id
      (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A Z) (f.actualLift ≫ g.actualLift)).trans
        (ConjugationCounit.comp (actualLiftSourceObjectEquivalence (W := W) A X)
          (actualLiftSourceObjectEquivalence (W := W) A Y)
          (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift)

/-- The actual vertical composite of the two original whiskered factors. -/
def actualLiftForwardTriangle :
    Pseudofunctor.StrongTrans
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor :=
  Pseudofunctor.StrongTrans.vcomp
    (actualLiftProjectedSourceUnit (W := W) A)
    (actualLiftRestrictedTargetCounit (W := W) A)

@[simp] theorem actualLiftForwardTriangle_app
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardTriangle (W := W) A).app X =
      actualLiftForwardTriangleApp (W := W) A X := rfl

/-- The generic modification square uses the exact native pasted naturality. -/
@[simp] theorem actualLiftForwardTriangle_naturality
    {X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    (actualLiftForwardTriangle (W := W) A).naturality f =
      ForwardTriangle.naturalityIso (actualLiftSourceObjectEquivalence (W := W) A X)
        (actualLiftSourceObjectEquivalence (W := W) A Y) f.actualLift := by
  apply Iso.ext
  rfl

/-- The v5.51 contractions form a global invertible modification for the
actual pasted triangle.  isoMk proves inverse naturality and both inverse laws. -/
def actualLiftForwardTriangleModificationIso :
    actualLiftForwardTriangle (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) ≅
    Pseudofunctor.StrongTrans.id
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor :=
  Pseudofunctor.StrongTrans.isoMk
    (fun X => actualLiftForwardTriangleIso (W := W) A X)
    (by
      intro X Y f
      exact ForwardTriangle.naturality (actualLiftSourceObjectEquivalence (W := W) A X)
        (actualLiftSourceObjectEquivalence (W := W) A Y) f.actualLift)

@[simp] theorem actualLiftForwardTriangleModificationIso_hom_app
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardTriangleModificationIso (W := W) A).hom.as.app X =
      (actualLiftForwardTriangleIso (W := W) A X).hom := rfl

@[simp] theorem actualLiftForwardTriangleModificationIso_inv_app
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardTriangleModificationIso (W := W) A).inv.as.app X =
      (actualLiftForwardTriangleIso (W := W) A X).inv := rfl

/-! ## Native-interface regressions -/

example :
    Pseudofunctor.StrongTrans
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor :=
  actualLiftForwardTriangle (W := W) A

example :
    actualLiftForwardTriangle (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) ≅
    Pseudofunctor.StrongTrans.id
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor :=
  actualLiftForwardTriangleModificationIso (W := W) A

example {X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    let F := (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
    let T := actualLiftForwardTriangle (W := W) A
    let c := actualLiftForwardTriangleModificationIso (W := W) A
    F.map f ◁ c.hom.as.app Y ≫ ((Pseudofunctor.StrongTrans.id F).naturality f).hom =
      (T.naturality f).hom ≫ c.hom.as.app X ▷ F.map f :=
  (actualLiftForwardTriangleModificationIso (W := W) A).hom.as.naturality f

example {X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    let F := (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
    let T := actualLiftForwardTriangle (W := W) A
    let c := actualLiftForwardTriangleModificationIso (W := W) A
    F.map f ◁ c.inv.as.app Y ≫ (T.naturality f).hom =
      ((Pseudofunctor.StrongTrans.id F).naturality f).hom ≫ c.inv.as.app X ▷ F.map f :=
  (actualLiftForwardTriangleModificationIso (W := W) A).inv.as.naturality f

example :
    let c := actualLiftForwardTriangleModificationIso (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    c.hom ≫ c.inv = 𝟙 (actualLiftForwardTriangle (W := W) A) :=
  (actualLiftForwardTriangleModificationIso (W := W) A).hom_inv_id

example :
    let F := (exactLiftableActualLiftStrictPseudofunctor (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPseudofunctor
    let c := actualLiftForwardTriangleModificationIso (W := W) A
    c.inv ≫ c.hom = 𝟙 (Pseudofunctor.StrongTrans.id F) :=
  (actualLiftForwardTriangleModificationIso (W := W) A).inv_hom_id

/-!
## Boundary after v5.52

The actual forward triangle is now a native global StrongTrans F => F.  Its
naturality is the original unit/counit paste; the v5.51 pointwise contractions
are exactly the components of a global invertible modification to identity.
All old equivalence choices, unit/counit, and pseudofunctor comparisons remain
unchanged.  No arbitrary transport of an identity transformation is used.

Separate obligations: the backward global triangle for G, its modification
naturality, and an integrated coherent certificate.  This file does not claim
a full adjoint-biequivalence or strict preservation of original raw maps.
-/

#print axioms ForwardTriangle.naturality
#print axioms ForwardTriangle.mapId_hom
#print axioms ForwardTriangle.mapComp_hom
#print axioms actualLiftForwardTriple
#print axioms actualLiftForwardTriple_mapId_hom
#print axioms actualLiftForwardTriple_mapComp_hom
#print axioms actualLiftProjectedSourceUnit
#print axioms actualLiftProjectedSourceUnit_naturality
#print axioms actualLiftRestrictedTargetCounit
#print axioms actualLiftForwardTriangle
#print axioms actualLiftForwardTriangle_naturality
#print axioms actualLiftForwardTriangleModificationIso
#print axioms actualLiftForwardTriangleModificationIso_hom_app
#print axioms actualLiftForwardTriangleModificationIso_inv_app

end

end KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
