import KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45
import Mathlib.CategoryTheory.Bicategory.Functor.Prelax
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactClassificationBicategoryV5_23
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
open KUOS.DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43
open KUOS.DependentOriginationExactLiftableActualLiftObjectCoverageV5_44

set_option autoImplicit false

noncomputable section

/-!
# Quasi-inverse prelax data for the actual-lift projection v5.46

v5.45 gives a Whitehead certificate for the global actual-lift projection F.
Here the object preimage is fixed explicitly as G(Y) := Y.toExactLiftable.
Choose once for each Y the v5.44 adjoint equivalence eY : F(G(Y)) ~ Y.

A target one-cell k : Y --> Z is transported to

  (eY.hom ; k) ; eZ.inv

and then re-packaged as an actual-lift one-cell.  This is not raw forgetting:
independently chosen universal presentations need not be equal.

Mathlib precomp/postcomp make this transport a functor on every hom category.
Their assembly is a native PrelaxFunctor, preserving vertical identities and
composition.  We additionally construct invertible identity/composition
comparisons from the chosen equivalences' units and counits.

These are candidate pseudofunctor data, not yet a Pseudofunctor: horizontal
compatibility and associator/unitor coherence are separate obligations.  No
global pseudonatural unit/counit or strict preservation of raw maps is claimed.
-/

/-! ## Conjugation in an arbitrary bicategory -/

namespace Conjugation

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c x y z : B}

/-- Conjugation is the composite of Mathlib's ordinary hom-category functors. -/
def homFunctor (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) : (x ⟶ y) ⥤ (a ⟶ b) :=
  Bicategory.precomp (B := B) y ex.hom ⋙
    Bicategory.postcomp (B := B) a ey.inv

/-- The identity comparison uses the actual unit of the chosen equivalence. -/
def idIso (ex : Bicategory.Equivalence a x) :
    (homFunctor ex ex).obj (𝟙 x) ≅ 𝟙 a :=
  Bicategory.whiskerRightIso (B := B)
    (Bicategory.rightUnitor (B := B) ex.hom) ex.inv ≪≫ ex.unit.symm

/-- Cancel the middle inverse/forward pair using its counit. -/
private def cancelMiddleIso (l : a ⟶ y)
    (ey : Bicategory.Equivalence b y) (r : y ⟶ z) :
    (l ≫ ey.inv) ≫ (ey.hom ≫ r) ≅ l ≫ r :=
  Bicategory.associator (B := B) l ey.inv (ey.hom ≫ r) ≪≫
    Bicategory.whiskerLeftIso (B := B) l
      (Bicategory.associator (B := B) ey.inv ey.hom r).symm ≪≫
    Bicategory.whiskerLeftIso (B := B) l
      (Bicategory.whiskerRightIso (B := B) ey.counit r) ≪≫
    Bicategory.whiskerLeftIso (B := B) l
      (Bicategory.leftUnitor (B := B) r)

/-- Comparison in the Pseudofunctor direction: image of a composite to the
composite of the images.  The inverse composite cancels the middle counit. -/
def compIso (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    (homFunctor ex ez).obj (f ≫ g) ≅
      (homFunctor ex ey).obj f ≫ (homFunctor ey ez).obj g :=
  ((Bicategory.associator (B := B)
      ((ex.hom ≫ f) ≫ ey.inv) (ey.hom ≫ g) ez.inv).symm ≪≫
    Bicategory.whiskerRightIso (B := B)
      (cancelMiddleIso (B := B) (ex.hom ≫ f) ey g) ez.inv ≪≫
    Bicategory.whiskerRightIso (B := B)
      (Bicategory.associator (B := B) ex.hom f g) ez.inv).symm

end Conjugation

/-! ## Fixed object representatives and hom-category re-packaging -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- A single fixed choice of adjoint equivalence for each target object.
Subsequent comparisons use this same choice, not independently chosen lifts. -/
def actualLiftQuasiInverseObjectEquivalence
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Equivalence
      (B := ExactUniversalClassificationObject (W := W) A
        WorldLabel PresentationLabel)
      (CanonicalExactUniversalObject (W := W) A
        (Y.toExactLiftable (W := W) A)) Y :=
  Classical.choice
    (canonicalExactUniversalObject_toExactLiftable_equivalent (W := W) A Y)

/-- Re-packaging the v5.43 preimage construction as an ordinary functor.
The stored target one-cell and every target 2-cell are retained exactly. -/
def actualLiftRepackHomFunctor
    (X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ExactUniversalClassificationOneCell (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)
        (CanonicalExactUniversalObject (W := W) A Y) ⥤
      ExactLiftableClassificationActualOneCell (W := W) A X Y where
  obj k := actualOneCellOfExactUniversalClassificationOneCell
    (W := W) A (X := X) (Y := Y) k
  map eta := eta
  map_id _ := rfl
  map_comp _ _ := rfl

/-- The hom functor of the intended global quasi-inverse.  Conjugation moves
both endpoints to canonical representatives before the actual lift is stored. -/
def actualLiftQuasiInverseHomFunctor
    (Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (Y ⟶ Z) ⥤
      (Y.toExactLiftable (W := W) A ⟶ Z.toExactLiftable (W := W) A) :=
  Conjugation.homFunctor
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) ⋙
    actualLiftRepackHomFunctor (W := W) A
      (Y.toExactLiftable (W := W) A) (Z.toExactLiftable (W := W) A)

/-- Native prelax assembly: objects, 1-cells, 2-cells, and both vertical laws.
No horizontal coherence is silently included in this weaker structure. -/
def actualLiftQuasiInversePrelax :
    PrelaxFunctor
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  PrelaxFunctor.mkOfHomFunctors
    (fun Y => Y.toExactLiftable (W := W) A)
    (fun Y Z => actualLiftQuasiInverseHomFunctor (W := W) A Y Z)

@[simp] theorem actualLiftQuasiInversePrelax_obj_label
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftQuasiInversePrelax (W := W) A).obj Y).label = Y.label :=
  rfl

/-- The forward image retained in the actual-lift bundle is the conjugated
classification one-cell, not an independently chosen lift of a raw map. -/
@[simp] theorem actualLiftQuasiInversePrelax_map_actualLift
    {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (k : Y ⟶ Z) :
    ((actualLiftQuasiInversePrelax (W := W) A).map k).actualLift =
      ExactUniversalClassificationOneCell.comp (W := W) A
        (ExactUniversalClassificationOneCell.comp (W := W) A
          (actualLiftQuasiInverseObjectEquivalence (W := W) A Y).hom k)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Z).inv :=
  rfl

/-! ## Invertible identity and composition comparisons -/

/-- Candidate unitor of the quasi-inverse, with the chosen object equivalence
unit supplying the contraction. -/
def actualLiftQuasiInverseMapIdIso
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInversePrelax (W := W) A).map (𝟙 Y) ≅
      𝟙 ((actualLiftQuasiInversePrelax (W := W) A).obj Y) :=
  ExactLiftableClassificationActualTwoCell.isoOfActualLift
    (W := W) A
    (f := (actualLiftQuasiInversePrelax (W := W) A).map (𝟙 Y))
    (g := exactLiftableClassificationActualOneCellId
      (W := W) A (Y.toExactLiftable (W := W) A))
    (Conjugation.idIso
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y))

/-- Candidate compositor, obtained from the middle object's actual counit.
This is an isomorphism, not a claim of definitional composition preservation. -/
def actualLiftQuasiInverseMapCompIso
    {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftQuasiInversePrelax (W := W) A).map (f ≫ g) ≅
      (actualLiftQuasiInversePrelax (W := W) A).map f ≫
        (actualLiftQuasiInversePrelax (W := W) A).map g :=
  ExactLiftableClassificationActualTwoCell.isoOfActualLift
    (W := W) A
    (f := (actualLiftQuasiInversePrelax (W := W) A).map (f ≫ g))
    (g := exactLiftableClassificationActualOneCellComp (W := W) A
      ((actualLiftQuasiInversePrelax (W := W) A).map f)
      ((actualLiftQuasiInversePrelax (W := W) A).map g))
    (Conjugation.compIso
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) f g)

/-! ## Regression checks at the native interfaces -/

section Regression
variable
  {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

example (k : X ⟶ Y) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (𝟙 k) =
      𝟙 ((actualLiftQuasiInversePrelax (W := W) A).map k) :=
  (actualLiftQuasiInversePrelax (W := W) A).map₂_id k

example {f g h : X ⟶ Y} (eta : f ⟶ g) (theta : g ⟶ h) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (eta ≫ theta) =
      (actualLiftQuasiInversePrelax (W := W) A).map₂ eta ≫
        (actualLiftQuasiInversePrelax (W := W) A).map₂ theta :=
  (actualLiftQuasiInversePrelax (W := W) A).map₂_comp eta theta

example (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftQuasiInversePrelax (W := W) A).map f ≫
        (actualLiftQuasiInversePrelax (W := W) A).map g ≅
      (actualLiftQuasiInversePrelax (W := W) A).map (f ≫ g) :=
  (actualLiftQuasiInverseMapCompIso (W := W) A f g).symm

example (k : X ⟶ Y) :
    ((actualLiftQuasiInversePrelax (W := W) A).map k).actualLift.map.raw =
      ((actualLiftQuasiInversePrelax (W := W) A).map k).raw.map :=
  ((actualLiftQuasiInversePrelax (W := W) A).map k).raw_eq

end Regression

/-!
## Boundary after v5.46

Constructed: one fixed adjoint-equivalence choice per target object; a genuine
functor on every hom category; the resulting native PrelaxFunctor; invertible
identity and composition comparisons; literal external-label preservation.

Remaining: naturality of the comparisons with horizontal 2-cells, compatibility
with associators and unitors, and the global pseudonatural roundtrip data.  The
PrelaxFunctor and comparison isomorphisms are not yet a Pseudofunctor, and the
v5.45 Whitehead certificate remains the completed global statement.
-/

#print axioms Conjugation.idIso
#print axioms Conjugation.compIso
#print axioms actualLiftQuasiInverseObjectEquivalence
#print axioms actualLiftRepackHomFunctor
#print axioms actualLiftQuasiInversePrelax
#print axioms actualLiftQuasiInverseMapIdIso
#print axioms actualLiftQuasiInverseMapCompIso

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
