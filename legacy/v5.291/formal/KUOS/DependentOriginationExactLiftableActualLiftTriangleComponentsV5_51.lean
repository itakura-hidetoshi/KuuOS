import KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50

namespace KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51

open CategoryTheory
open scoped CategoryTheory.Bicategory
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

set_option autoImplicit false

noncomputable section

/-!
# Actual-lift triangle component contractions v5.51

Keep the v5.42 projection F, v5.48 quasi-inverse G, v5.49 counit eps,
and v5.50 unit eta unchanged.  Define the actual components

  F(eta_X) ; eps_(F X),       eta_(G Y) ; G(eps_Y)

and contract each to the corresponding identity by explicit isomorphisms.
The forward contraction is the original counit at F X.  For the backwards
contraction, undo the existing inverse-component naturality insertion at
`eps_Y`, then use the inverse of the original unit at Y.

The two equivalence choices e_Y and e_(F G Y) are retained separately.
No equality between them, fresh choice, or replacement compositor is used.
This is a pointwise triangle theorem: global modification naturality and the
integrated coherent certificate remain separate obligations.
-/

/-! ## The inverse triangle in an arbitrary bicategory -/

namespace ConjugationTriangle

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b x : B}

/-- Undo the already-proved unit naturality insertion and contract the
remaining forward/inverse pair with the original unit.  The two equivalences
have different endpoints and are never identified. -/
def quasiInverseIso (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    d.inv ≫ (Conjugation.homFunctor d e).obj e.hom ≅ 𝟙 a :=
  (ConjugationUnit.naturalityIso d e e.hom).symm ≪≫ e.unit.symm

@[simp] theorem quasiInverseIso_hom (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    (quasiInverseIso e d).hom =
      (ConjugationUnit.naturalityIso d e e.hom).inv ≫ e.unit.inv := rfl

@[simp] theorem quasiInverseIso_inv (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    (quasiInverseIso e d).inv =
      e.unit.hom ≫ (ConjugationUnit.naturalityIso d e e.hom).hom := rfl

end ConjugationTriangle

/-! ## The actual components of the fixed pair -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The actual forward triangle component, not a chosen representative. -/
def actualLiftForwardTriangleApp
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    CanonicalExactUniversalObject (W := W) A X ⟶
      CanonicalExactUniversalObject (W := W) A X :=
  (exactLiftableActualLiftStrictPseudofunctor (W := W) A).map
      ((actualLiftSourceRoundtripUnit (W := W) A).app X) ≫
    (actualLiftTargetRoundtripCounit (W := W) A).app
      ((exactLiftableActualLiftStrictPseudofunctor (W := W) A).obj X)

/-- Both factors use the same original e_(F X). -/
@[simp] theorem actualLiftForwardTriangleApp_eq
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    actualLiftForwardTriangleApp (W := W) A X =
      (actualLiftSourceObjectEquivalence (W := W) A X).inv ≫
        (actualLiftSourceObjectEquivalence (W := W) A X).hom := rfl

/-- The forward triangle contracts by exactly the original counit. -/
def actualLiftForwardTriangleIso
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    actualLiftForwardTriangleApp (W := W) A X ≅
      𝟙 (CanonicalExactUniversalObject (W := W) A X) :=
  (actualLiftSourceObjectEquivalence (W := W) A X).counit

@[simp] theorem actualLiftForwardTriangleIso_hom
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardTriangleIso (W := W) A X).hom =
      (actualLiftSourceObjectEquivalence (W := W) A X).counit.hom := rfl

@[simp] theorem actualLiftForwardTriangleIso_inv
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardTriangleIso (W := W) A X).inv =
      (actualLiftSourceObjectEquivalence (W := W) A X).counit.inv := rfl

/-- The actual quasi-inverse triangle component eta_(G Y) ; G(eps_Y). -/
def actualLiftQuasiInverseTriangleApp
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInversePseudofunctor (W := W) A).obj Y ⟶
      (actualLiftQuasiInversePseudofunctor (W := W) A).obj Y :=
  (actualLiftSourceRoundtripUnit (W := W) A).app
      ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y) ≫
    (actualLiftQuasiInversePseudofunctor (W := W) A).map
      ((actualLiftTargetRoundtripCounit (W := W) A).app Y)

/-- Expose the stored target component, keeping e_Y and e_(F G Y) distinct. -/
@[simp] theorem actualLiftQuasiInverseTriangleApp_actualLift
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleApp (W := W) A Y).actualLift =
      (actualLiftSourceObjectEquivalence (W := W) A
        ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)).inv ≫
      (Conjugation.homFunctor
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)).obj
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y).hom := rfl

/-- Specialize the typed generic contraction before crossing the actual-lift
wrapper boundary.  No large concrete `change` expression is elaborated. -/
def actualLiftQuasiInverseTriangleLiftIso
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleApp (W := W) A Y).actualLift ≅
      𝟙 (CanonicalExactUniversalObject (W := W) A
        ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)) :=
  ConjugationTriangle.quasiInverseIso
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
    (actualLiftSourceObjectEquivalence (W := W) A
      ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))

/-- The contraction lives in the actual source bicategory, not just its
image.  The established wrapper retains the target hom and inverse literally. -/
def actualLiftQuasiInverseTriangleIso
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    actualLiftQuasiInverseTriangleApp (W := W) A Y ≅
      𝟙 ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y) :=
  ExactLiftableClassificationActualTwoCell.isoOfActualLift (W := W) A
    (f := actualLiftQuasiInverseTriangleApp (W := W) A Y)
    (g := 𝟙 ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))
    (actualLiftQuasiInverseTriangleLiftIso (W := W) A Y)

@[simp] theorem actualLiftQuasiInverseTriangleIso_hom
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom =
      (actualLiftQuasiInverseTriangleLiftIso (W := W) A Y).hom := rfl

@[simp] theorem actualLiftQuasiInverseTriangleIso_inv
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv =
      (actualLiftQuasiInverseTriangleLiftIso (W := W) A Y).inv := rfl

/-! ## Regressions through the actual native pair and both inverse laws -/

example (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    let F := (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    let eps := actualLiftTargetRoundtripCounit (W := W) A
    F.map (eta.app X) ≫ eps.app (F.obj X) ≅ 𝟙 (F.obj X) :=
  actualLiftForwardTriangleIso (W := W) A X

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    let eps := actualLiftTargetRoundtripCounit (W := W) A
    eta.app (G.obj Y) ≫ G.map (eps.app Y) ≅ 𝟙 (G.obj Y) :=
  actualLiftQuasiInverseTriangleIso (W := W) A Y

example (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardTriangleIso (W := W) A X).hom ≫
      (actualLiftForwardTriangleIso (W := W) A X).inv =
        𝟙 (actualLiftForwardTriangleApp (W := W) A X) :=
  (actualLiftForwardTriangleIso (W := W) A X).hom_inv_id

example (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    (actualLiftForwardTriangleIso (W := W) A X).inv ≫
      (actualLiftForwardTriangleIso (W := W) A X).hom =
        𝟙 (𝟙 (CanonicalExactUniversalObject (W := W) A X)) :=
  (actualLiftForwardTriangleIso (W := W) A X).inv_hom_id

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom ≫
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv =
        𝟙 (actualLiftQuasiInverseTriangleApp (W := W) A Y) :=
  (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom_inv_id

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv ≫
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom =
        𝟙 (𝟙 ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)) :=
  (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv_hom_id

/-!
## Boundary after v5.51

Both actual triangle components of the fixed F/G/eta/eps pair have explicit
invertible 2-cells to identity.  The source contraction is built by re-packaging
the concrete target contraction, rather than assuming faithfulness gives an
object-level equality.  Original fixed equivalences and external labels are
unchanged; no strict preservation of the original raw map is asserted.

Still separate: coherent global triangle transformations, naturality of their
invertible modifications, and the integrated certificate for this pair.
-/

#print axioms ConjugationTriangle.quasiInverseIso
#print axioms ConjugationTriangle.quasiInverseIso_hom
#print axioms ConjugationTriangle.quasiInverseIso_inv
#print axioms actualLiftForwardTriangleApp
#print axioms actualLiftForwardTriangleApp_eq
#print axioms actualLiftForwardTriangleIso
#print axioms actualLiftQuasiInverseTriangleApp
#print axioms actualLiftQuasiInverseTriangleApp_actualLift
#print axioms actualLiftQuasiInverseTriangleLiftIso
#print axioms actualLiftQuasiInverseTriangleIso
#print axioms actualLiftQuasiInverseTriangleIso_hom
#print axioms actualLiftQuasiInverseTriangleIso_inv

end

end KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
