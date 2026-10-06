import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

set_option autoImplicit false

noncomputable section

/-!
# The actual pasted quasi-inverse triangle v5.55

Compose the original v5.53 source-unit factor with the original v5.54
reassociated target-counit factor using Mathlib's native StrongTrans.vcomp.
The result is a global transformation G => G. Its naturality is the actual
five-isomorphism paste, including both of G's original compositors around
the mapped counit square. It is not an identity transformation transported
along a newly chosen family of isomorphisms.

The components are definitionally the v5.51 triangle components. Their
contractions, including both inverse maps, are precisely the old v5.51
isomorphisms. Four equivalences remain distinct in the generic naturality:
e_Y, e_Z, e_(F G Y), and e_(F G Z).

Naturality of the contraction as a global modification and the integrated
coherent certificate remain separate obligations. No global modification
is inferred merely from the existence of these component isomorphisms.
-/

namespace BackwardTriangle

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b x y p q : B}

/-- The image of the original counit square under the original conjugation.
The first comparison is inverted, and the last comparison is not. -/
def counitNaturalityIso (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (dx : Bicategory.Equivalence p a)
    (dy : Bicategory.Equivalence q b) (f : x ⟶ y) :
    (Conjugation.homFunctor dx dy).obj ((Conjugation.homFunctor ex ey).obj f) ≫
        (Conjugation.homFunctor dy ey).obj ey.hom ≅
      (Conjugation.homFunctor dx ex).obj ex.hom ≫
        (Conjugation.homFunctor ex ey).obj f :=
  (Conjugation.compIso dx dy ey ((Conjugation.homFunctor ex ey).obj f) ey.hom).symm ≪≫
    (Conjugation.homFunctor dx ey).mapIso (ConjugationCounit.naturalityIso ex ey f) ≪≫
    Conjugation.compIso dx ex ey ex.hom f

/-- The five-isomorphism vertical paste used by the actual backward triangle.
No equality of the four equivalence choices is assumed. -/
def naturalityIso (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (dx : Bicategory.Equivalence p a)
    (dy : Bicategory.Equivalence q b) (f : x ⟶ y) :
    (Conjugation.homFunctor ex ey).obj f ≫
        (dy.inv ≫ (Conjugation.homFunctor dy ey).obj ey.hom) ≅
      (dx.inv ≫ (Conjugation.homFunctor dx ex).obj ex.hom) ≫
        (Conjugation.homFunctor ex ey).obj f :=
  (α_ ((Conjugation.homFunctor ex ey).obj f) dy.inv
    ((Conjugation.homFunctor dy ey).obj ey.hom)).symm ≪≫
    Bicategory.whiskerRightIso (B := B)
      (ConjugationUnit.naturalityIso dx dy ((Conjugation.homFunctor ex ey).obj f))
      ((Conjugation.homFunctor dy ey).obj ey.hom) ≪≫
    (α_ dx.inv ((Conjugation.homFunctor dx dy).obj ((Conjugation.homFunctor ex ey).obj f))
      ((Conjugation.homFunctor dy ey).obj ey.hom)) ≪≫
    Bicategory.whiskerLeftIso (B := B) dx.inv (counitNaturalityIso ex ey dx dy f) ≪≫
    (α_ dx.inv ((Conjugation.homFunctor dx ex).obj ex.hom)
      ((Conjugation.homFunctor ex ey).obj f)).symm

end BackwardTriangle

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The original two factors, composed at their proved common native triple.
Explicit ambient types keep all six universe parameters and both labels. -/
def actualLiftQuasiInverseTriangle :
    Pseudofunctor.StrongTrans
      (B := ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (C := ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (actualLiftQuasiInversePseudofunctor (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A) :=
  Pseudofunctor.StrongTrans.vcomp
    (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A)
    (actualLiftQuasiInverseRestrictedTargetCounitReassociated (W := W) A)

/-- The global transformation is literally the original native paste. -/
theorem actualLiftQuasiInverseTriangle_eq_vcomp :
    (actualLiftQuasiInverseTriangle (W := W) A :
      Pseudofunctor.StrongTrans
        (B := ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)
        (C := ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)
        (actualLiftQuasiInversePseudofunctor (W := W) A)
        (actualLiftQuasiInversePseudofunctor (W := W) A)) =
      Pseudofunctor.StrongTrans.vcomp
        (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A)
        (actualLiftQuasiInverseRestrictedTargetCounitReassociated (W := W) A) := rfl

@[simp] theorem actualLiftQuasiInverseTriangle_app
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangle (W := W) A).app Y =
      actualLiftQuasiInverseTriangleApp (W := W) A Y := rfl

/-- The two components are the original eta at GY followed by G(eps_Y). -/
theorem actualLiftQuasiInverseTriangle_app_factors
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangle (W := W) A).app Y =
      (actualLiftSourceRoundtripUnit (W := W) A).app
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y) ≫
        (actualLiftQuasiInversePseudofunctor (W := W) A).map
          ((actualLiftTargetRoundtripCounit (W := W) A).app Y) := rfl

/-- Project the actual pasted naturality to its exact generic diagram.
This compares the stored 2-cells, not isomorphisms in different hom categories. -/
@[simp] theorem actualLiftQuasiInverseTriangle_naturality_hom
    {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (k : Y ⟶ Z) :
    ((actualLiftQuasiInverseTriangle (W := W) A).naturality k).hom =
      (BackwardTriangle.naturalityIso
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Z)
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Z)) k).hom := rfl

/-- The inverse naturality also retains exactly the inverse of the old paste. -/
@[simp] theorem actualLiftQuasiInverseTriangle_naturality_inv
    {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (k : Y ⟶ Z) :
    ((actualLiftQuasiInverseTriangle (W := W) A).naturality k).inv =
      (BackwardTriangle.naturalityIso
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Z)
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Z)) k).inv := rfl

/-- The original v5.51 contraction, now typed on the actual global triangle.
This is a family of isomorphisms, not yet a global modification. -/
def actualLiftQuasiInverseTriangleComponentIso
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangle (W := W) A).app Y ≅
      𝟙 ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y) :=
  actualLiftQuasiInverseTriangleIso (W := W) A Y

@[simp] theorem actualLiftQuasiInverseTriangleComponentIso_eq
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    actualLiftQuasiInverseTriangleComponentIso (W := W) A Y =
      actualLiftQuasiInverseTriangleIso (W := W) A Y := rfl

@[simp] theorem actualLiftQuasiInverseTriangleComponentIso_hom
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).hom =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom := rfl

@[simp] theorem actualLiftQuasiInverseTriangleComponentIso_inv
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).inv =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv := rfl

/-! ## Native-interface regressions -/

-- Regression specification: the actual two factors must form a named native triangle.
example : Pseudofunctor.StrongTrans
    (B := ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (actualLiftQuasiInversePseudofunctor (W := W) A)
    (actualLiftQuasiInversePseudofunctor (W := W) A) :=
  actualLiftQuasiInverseTriangle (W := W) A

example {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} {f g : Y ⟶ Z} (theta : f ⟶ g) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriangle (W := W) A
    G.map₂ theta ▷ T.app Z ≫ (T.naturality g).hom =
      (T.naturality f).hom ≫ T.app Y ◁ G.map₂ theta :=
  (actualLiftQuasiInverseTriangle (W := W) A).naturality_naturality theta

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriangle (W := W) A
    (T.naturality (𝟙 Y)).hom ≫ T.app Y ◁ (G.mapId Y).hom =
      (G.mapId Y).hom ▷ T.app Y ≫ (λ_ (T.app Y)).hom ≫ (ρ_ (T.app Y)).inv :=
  (actualLiftQuasiInverseTriangle (W := W) A).naturality_id Y

example {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} (k : X ⟶ Y) (l : Y ⟶ Z) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriangle (W := W) A
    (T.naturality (k ≫ l)).hom ≫ T.app X ◁ (G.mapComp k l).hom =
      (G.mapComp k l).hom ▷ T.app Z ≫
        (α_ (G.map k) (G.map l) (T.app Z)).hom ≫
        G.map k ◁ (T.naturality l).hom ≫
        (α_ (G.map k) (T.app Y) (G.map l)).inv ≫
        (T.naturality k).hom ▷ G.map l ≫
        (α_ (T.app X) (G.map k) (G.map l)).hom :=
  (actualLiftQuasiInverseTriangle (W := W) A).naturality_comp k l

-- Regress the precise old components, rather than mere existence of some contraction.
example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    let eps := actualLiftTargetRoundtripCounit (W := W) A
    (actualLiftQuasiInverseTriangle (W := W) A).app Y =
      eta.app (G.obj Y) ≫ G.map (eps.app Y) := rfl

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).hom ≫
        (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).inv =
      𝟙 ((actualLiftQuasiInverseTriangle (W := W) A).app Y) :=
  (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).hom_inv_id

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).inv ≫
        (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).hom =
      𝟙 (𝟙 ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)) :=
  (actualLiftQuasiInverseTriangleComponentIso (W := W) A Y).inv_hom_id

/-!
## Boundary after v5.55

The actual backward triangle is now a native StrongTrans G G, not just a
pointwise expression. Its original pasted naturality and both directions of
the original v5.51 component contractions are retained explicitly.

Remaining: prove the modification square for this exact pasted naturality,
then package the invertible modification and the integrated certificate.
The former v5.51 pointwise result and v5.52 forward global result are not
weakened or used as substitutes for that remaining backwards square.
-/

#print axioms BackwardTriangle.counitNaturalityIso
#print axioms BackwardTriangle.naturalityIso
#print axioms actualLiftQuasiInverseTriangle
#print axioms actualLiftQuasiInverseTriangle_eq_vcomp
#print axioms actualLiftQuasiInverseTriangle_app
#print axioms actualLiftQuasiInverseTriangle_app_factors
#print axioms actualLiftQuasiInverseTriangle_naturality_hom
#print axioms actualLiftQuasiInverseTriangle_naturality_inv
#print axioms actualLiftQuasiInverseTriangleComponentIso
#print axioms actualLiftQuasiInverseTriangleComponentIso_eq
#print axioms actualLiftQuasiInverseTriangleComponentIso_hom
#print axioms actualLiftQuasiInverseTriangleComponentIso_inv

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
