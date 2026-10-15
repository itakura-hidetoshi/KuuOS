import KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50

set_option autoImplicit false

noncomputable section

/-!
# Quasi-inverse triangle source-unit factor v5.53

Retain the original F, G, eta, eps, and all chosen equivalences.  This file
constructs the first factor of the backward triangle, eta restricted along G:

  G => G ; (F ; G).

Unlike the forward projection F, G need not be strict.  The generic argument
uses the original unit's 2-cell naturality at the actual mapId and mapComp of
the precomposing pseudofunctor.  Those comparisons are not replaced by
identities.  The native composite pseudofunctor is retained literally.

The second factor (the image of eps under G), the full backward triangle,
its modification, and the integrated certificate remain separate obligations.
-/

universe uD vD wD uB vB wB u v uH vH uW uP

namespace UnitPrecomposition

variable {D : Type uD} [Bicategory.{wD, vD} D]
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable (H : Pseudofunctor D B) {R : Pseudofunctor B B}
variable (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R)

/-- Use naturality at the actual identity comparison of H, followed by
eta's original identity law.  No strictness hypothesis on H is needed. -/
theorem naturality_id (a : D) :
    (eta.naturality (H.map (𝟙 a))).hom ≫
        eta.app (H.obj a) ◁ ((Pseudofunctor.comp H R).mapId a).hom =
      (H.mapId a).hom ▷ eta.app (H.obj a) ≫
        (λ_ (eta.app (H.obj a))).hom ≫ (ρ_ (eta.app (H.obj a))).inv := by
  change (eta.naturality (H.map (𝟙 a))).hom ≫
    eta.app (H.obj a) ◁
      (R.map₂ (H.mapId a).hom ≫ (R.mapId (H.obj a)).hom) = _
  rw [Bicategory.whiskerLeft_comp, ← Category.assoc,
    ← eta.naturality_naturality (H.mapId a).hom, Category.assoc,
    eta.naturality_id]
  -- Expose only the identity source's maps before matching the unit laws.
  -- H.mapId is still its original, potentially nontrivial comparison.
  change (H.mapId a).hom ▷ eta.app (H.obj a) ≫
    (𝟙 (𝟙 (H.obj a))) ▷ eta.app (H.obj a) ≫
      (λ_ (eta.app (H.obj a))).hom ≫ (ρ_ (eta.app (H.obj a))).inv = _
  rw [Bicategory.id_whiskerRight, Category.id_comp]

/-- Use naturality at H's actual compositor before eta's composition law.
This keeps precisely the compositor of the native composite H ; R. -/
theorem naturality_comp {a b c : D} (f : a ⟶ b) (g : b ⟶ c) :
    (eta.naturality (H.map (f ≫ g))).hom ≫
        eta.app (H.obj a) ◁ ((Pseudofunctor.comp H R).mapComp f g).hom =
      (H.mapComp f g).hom ▷ eta.app (H.obj c) ≫
        (α_ (H.map f) (H.map g) (eta.app (H.obj c))).hom ≫
        H.map f ◁ (eta.naturality (H.map g)).hom ≫
        (α_ (H.map f) (eta.app (H.obj b)) (R.map (H.map g))).inv ≫
        (eta.naturality (H.map f)).hom ▷ R.map (H.map g) ≫
        (α_ (eta.app (H.obj a)) (R.map (H.map f)) (R.map (H.map g))).hom := by
  change (eta.naturality (H.map (f ≫ g))).hom ≫
    eta.app (H.obj a) ◁
      (R.map₂ (H.mapComp f g).hom ≫ (R.mapComp (H.map f) (H.map g)).hom) = _
  rw [Bicategory.whiskerLeft_comp, ← Category.assoc,
    ← eta.naturality_naturality (H.mapComp f g).hom, Category.assoc,
    eta.naturality_comp]
  -- Normalize Pseudofunctor.id, not H or R, at this generic boundary.
  change (H.mapComp f g).hom ▷ eta.app (H.obj c) ≫
    (𝟙 (H.map f ≫ H.map g)) ▷ eta.app (H.obj c) ≫
      (α_ (H.map f) (H.map g) (eta.app (H.obj c))).hom ≫
      H.map f ◁ (eta.naturality (H.map g)).hom ≫
      (α_ (H.map f) (eta.app (H.obj b)) (R.map (H.map g))).inv ≫
      (eta.naturality (H.map f)).hom ▷ R.map (H.map g) ≫
      (α_ (eta.app (H.obj a)) (R.map (H.map f)) (R.map (H.map g))).hom = _
  rw [Bicategory.id_whiskerRight, Category.id_comp]

/-- Precompose a unit StrongTrans by an arbitrary pseudofunctor.
The source is H itself, not an unproved identification of H ; Id with H. -/
def strongTrans :
    Pseudofunctor.StrongTrans H (Pseudofunctor.comp H R) where
  app a := eta.app (H.obj a)
  naturality f := eta.naturality (H.map f)
  naturality_naturality theta := eta.naturality_naturality (H.map₂ theta)
  naturality_id a := naturality_id H eta a
  naturality_comp f g := naturality_comp H eta f g

@[simp] theorem strongTrans_app (a : D) :
    (strongTrans H eta).app a = eta.app (H.obj a) := rfl

@[simp] theorem strongTrans_naturality {a b : D} (f : a ⟶ b) :
    (strongTrans H eta).naturality f = eta.naturality (H.map f) := rfl

end UnitPrecomposition

section GenericRegression

variable {D : Type uD} [Bicategory.{wD, vD} D]
variable {B : Type uB} [Bicategory.{wB, vB} B]

-- Original regression specification: the precomposing functor need not be strict.
example (H : Pseudofunctor D B) (R : Pseudofunctor B B)
    (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R) :
    Pseudofunctor.StrongTrans H (Pseudofunctor.comp H R) :=
  UnitPrecomposition.strongTrans H eta

-- Regress both repaired laws with arbitrary H and its actual comparisons.
example (H : Pseudofunctor D B) (R : Pseudofunctor B B)
    (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R) (a : D) :
    (eta.naturality (H.map (𝟙 a))).hom ≫
        eta.app (H.obj a) ◁ ((Pseudofunctor.comp H R).mapId a).hom =
      (H.mapId a).hom ▷ eta.app (H.obj a) ≫
        (λ_ (eta.app (H.obj a))).hom ≫ (ρ_ (eta.app (H.obj a))).inv :=
  (UnitPrecomposition.strongTrans H eta).naturality_id a

example (H : Pseudofunctor D B) (R : Pseudofunctor B B)
    (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R)
    {a b c : D} (f : a ⟶ b) (g : b ⟶ c) :
    (eta.naturality (H.map (f ≫ g))).hom ≫
        eta.app (H.obj a) ◁ ((Pseudofunctor.comp H R).mapComp f g).hom =
      (H.mapComp f g).hom ▷ eta.app (H.obj c) ≫
        (α_ (H.map f) (H.map g) (eta.app (H.obj c))).hom ≫
        H.map f ◁ (eta.naturality (H.map g)).hom ≫
        (α_ (H.map f) (eta.app (H.obj b)) (R.map (H.map g))).inv ≫
        (eta.naturality (H.map f)).hom ▷ R.map (H.map g) ≫
        (α_ (eta.app (H.obj a)) (R.map (H.map f)) (R.map (H.map g))).hom :=
  (UnitPrecomposition.strongTrans H eta).naturality_comp f g

end GenericRegression

/-! ## The original source unit restricted along the original G -/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Keep the native bracketing G ; (F ; G), without identifying its
comparisons with another bracketing or replacing G by a strict functor. -/
def actualLiftQuasiInverseTriple :
    Pseudofunctor
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.comp (actualLiftQuasiInversePseudofunctor (W := W) A)
    (actualLiftSourceRoundtrip (W := W) A)

/-- The first factor of the actual backward triangle, including all three
native coherence fields for the unchanged non-strict quasi-inverse. -/
def actualLiftQuasiInverseRestrictedSourceUnit :
    Pseudofunctor.StrongTrans
      ((actualLiftQuasiInversePseudofunctor (W := W) A :
        Pseudofunctor
          (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)
          (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)))
      (actualLiftQuasiInverseTriple (W := W) A) :=
  UnitPrecomposition.strongTrans
    (actualLiftQuasiInversePseudofunctor (W := W) A)
    (actualLiftSourceRoundtripUnit (W := W) A)

@[simp] theorem actualLiftQuasiInverseRestrictedSourceUnit_app
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A).app Y =
      (actualLiftSourceRoundtripUnit (W := W) A).app
        ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y) := rfl

/-- The naturality is exactly the old unit evaluated at G.map k. -/
@[simp] theorem actualLiftQuasiInverseRestrictedSourceUnit_naturality
    {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (k : Y ⟶ Z) :
    (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A).naturality k =
      (actualLiftSourceRoundtripUnit (W := W) A).naturality
        ((actualLiftQuasiInversePseudofunctor (W := W) A).map k) := rfl

/-- The component retains the inverse of the already fixed e_(F G Y). -/
@[simp] theorem actualLiftQuasiInverseRestrictedSourceUnit_app_actualLift
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftQuasiInverseRestrictedSourceUnit (W := W) A).app Y).actualLift =
      (actualLiftSourceObjectEquivalence (W := W) A
        ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)).inv := rfl

/-- The pointwise adjoint equivalence is the original v5.50 equivalence
at G.obj Y, not a fresh choice of component or inverse. -/
def actualLiftQuasiInverseUnitComponentEquivalence
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Equivalence
      (B := ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)
      ((actualLiftQuasiInverseTriple (W := W) A).obj Y) :=
  actualLiftSourceUnitComponentEquivalence (W := W) A
    ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y)

@[simp] theorem actualLiftQuasiInverseUnitComponentEquivalence_hom
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseUnitComponentEquivalence (W := W) A Y).hom =
      (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A).app Y := rfl

@[simp] theorem actualLiftQuasiInverseTriple_obj_label
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftQuasiInverseTriple (W := W) A).obj Y).label = Y.label := rfl

/-! ## Native-interface regressions -/

example :
    Pseudofunctor.StrongTrans
      ((actualLiftQuasiInversePseudofunctor (W := W) A :
        Pseudofunctor
          (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)
          (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)))
      (actualLiftQuasiInverseTriple (W := W) A) :=
  actualLiftQuasiInverseRestrictedSourceUnit (W := W) A

example {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} {f g : Y ⟶ Z} (theta : f ⟶ g) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriple (W := W) A
    let etaG := actualLiftQuasiInverseRestrictedSourceUnit (W := W) A
    G.map₂ theta ▷ etaG.app Z ≫ (etaG.naturality g).hom =
      (etaG.naturality f).hom ≫ etaG.app Y ◁ T.map₂ theta :=
  (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A).naturality_naturality theta

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriple (W := W) A
    let etaG := actualLiftQuasiInverseRestrictedSourceUnit (W := W) A
    (etaG.naturality (𝟙 Y)).hom ≫ etaG.app Y ◁ (T.mapId Y).hom =
      (G.mapId Y).hom ▷ etaG.app Y ≫
        (λ_ (etaG.app Y)).hom ≫ (ρ_ (etaG.app Y)).inv :=
  (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A).naturality_id Y

example {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriple (W := W) A
    let etaG := actualLiftQuasiInverseRestrictedSourceUnit (W := W) A
    (etaG.naturality (f ≫ g)).hom ≫ etaG.app X ◁ (T.mapComp f g).hom =
      (G.mapComp f g).hom ▷ etaG.app Z ≫ (α_ _ _ _).hom ≫
        G.map f ◁ (etaG.naturality g).hom ≫ (α_ _ _ _).inv ≫
        (etaG.naturality f).hom ▷ T.map g ≫ (α_ _ _ _).hom :=
  (actualLiftQuasiInverseRestrictedSourceUnit (W := W) A).naturality_comp f g

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseUnitComponentEquivalence (W := W) A Y).hom =
      (actualLiftSourceRoundtripUnit (W := W) A).app
        ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y) := rfl

/-!
## Boundary

Closed by this unit: the original source unit precomposed along the original
G, with literal old components and naturalities, all native StrongTrans laws,
and the inherited pointwise adjoint equivalences.  The first leg targets the
native bracketing G ; (F ; G).

Not claimed here: construction of the second leg to G, its compatibility with
this bracketing, the full backward triangle, its invertible modification, or
the integrated certificate.  The pointwise contractions of v5.51 and the
forward modification of v5.52 are retained, not weakened or reclassified.
-/

#print axioms UnitPrecomposition.naturality_id
#print axioms UnitPrecomposition.naturality_comp
#print axioms UnitPrecomposition.strongTrans
#print axioms actualLiftQuasiInverseTriple
#print axioms actualLiftQuasiInverseRestrictedSourceUnit
#print axioms actualLiftQuasiInverseRestrictedSourceUnit_app
#print axioms actualLiftQuasiInverseRestrictedSourceUnit_naturality
#print axioms actualLiftQuasiInverseRestrictedSourceUnit_app_actualLift
#print axioms actualLiftQuasiInverseUnitComponentEquivalence
#print axioms actualLiftQuasiInverseUnitComponentEquivalence_hom
#print axioms actualLiftQuasiInverseTriple_obj_label

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
