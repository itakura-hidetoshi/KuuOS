import KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
import Mathlib.CategoryTheory.Whiskering

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseNaturalityV5_47

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46

set_option autoImplicit false

noncomputable section

/-!
# Horizontal naturality of the actual-lift quasi-inverse v5.47

The v5.46 compositor is assembled from associators and a chosen counit.  Its
naturality should therefore be obtained by composing natural isomorphisms,
not by assuming equality of independently chosen presentations or by expanding
all coherence diagrams into a large rewrite script.

We do this first in an arbitrary bicategory.  Mathlib's associator natural
isomorphisms and precomposing/postcomposing functors give natural versions of
middle cancellation in either variable.  Their composites have literally the
v5.46 compositor as inverse components.  Naturality supplies both horizontal
squares, and cancellation gives exactly the two whiskering equations required
by Mathlib's native Pseudofunctor constructor.

The associator and two unitor preservation equations remain separate.  This
file does not yet package a Pseudofunctor or a global unit/counit.
-/

namespace ConjugationNaturality

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c x y z : B}

-- Ordinary functor-category whiskering lives in CategoryTheory.Functor.
-- Qualify it explicitly to distinguish it from bicategorical whiskering.

/-- Middle cancellation, natural in its right-hand argument.  The four
components are precisely the four steps of v5.46's middle cancellation. -/
def cancelMiddleNatIsoRight (l : a ⟶ y)
    (ey : Bicategory.Equivalence b y) :
    Bicategory.precomp (B := B) z ey.hom ⋙
        Bicategory.precomp (B := B) z (l ≫ ey.inv) ≅
      Bicategory.precomp (B := B) z l :=
  CategoryTheory.Functor.isoWhiskerLeft (Bicategory.precomp (B := B) z ey.hom)
      (Bicategory.associatorNatIsoRight (B := B) l ey.inv z) ≪≫
    CategoryTheory.Functor.isoWhiskerRight
      (Bicategory.associatorNatIsoRight (B := B) ey.inv ey.hom z).symm
      (Bicategory.precomp (B := B) z l) ≪≫
    CategoryTheory.Functor.isoWhiskerRight
      ((Bicategory.precomposing (B := B) y y z).mapIso ey.counit)
      (Bicategory.precomp (B := B) z l) ≪≫
    CategoryTheory.Functor.isoWhiskerRight (Bicategory.leftUnitorNatIso (B := B) y z)
      (Bicategory.precomp (B := B) z l)

/-- The same middle cancellation, now natural in its left-hand argument. -/
def cancelMiddleNatIsoLeft (ey : Bicategory.Equivalence b y)
    (r : y ⟶ z) :
    Bicategory.postcomp (B := B) a ey.inv ⋙
        Bicategory.postcomp (B := B) a (ey.hom ≫ r) ≅
      Bicategory.postcomp (B := B) a r :=
  Bicategory.associatorNatIsoLeft (B := B) a ey.inv (ey.hom ≫ r) ≪≫
    (Bicategory.postcomposing (B := B) a y z).mapIso
      (Bicategory.associator (B := B) ey.inv ey.hom r).symm ≪≫
    (Bicategory.postcomposing (B := B) a y z).mapIso
      (Bicategory.whiskerRightIso (B := B) ey.counit r) ≪≫
    (Bicategory.postcomposing (B := B) a y z).mapIso
      (Bicategory.leftUnitor (B := B) r)

/-- For fixed f, the inverse compositor is a natural isomorphism in g. -/
def compNatIsoRight (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) :
    Conjugation.homFunctor ey ez ⋙
        Bicategory.precomp (B := B) c ((Conjugation.homFunctor ex ey).obj f) ≅
      Bicategory.precomp (B := B) z f ⋙ Conjugation.homFunctor ex ez :=
  CategoryTheory.Functor.isoWhiskerLeft (Bicategory.precomp (B := B) z ey.hom)
      (Bicategory.associatorNatIsoMiddle (B := B)
        ((ex.hom ≫ f) ≫ ey.inv) ez.inv).symm ≪≫
    CategoryTheory.Functor.isoWhiskerRight
      (cancelMiddleNatIsoRight (z := z) (ex.hom ≫ f) ey)
      (Bicategory.postcomp (B := B) a ez.inv) ≪≫
    CategoryTheory.Functor.isoWhiskerRight (Bicategory.associatorNatIsoRight (B := B) ex.hom f z)
      (Bicategory.postcomp (B := B) a ez.inv)

/-- For fixed g, the inverse compositor is a natural isomorphism in f. -/
def compNatIsoLeft (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (g : y ⟶ z) :
    Conjugation.homFunctor ex ey ⋙
        Bicategory.postcomp (B := B) a ((Conjugation.homFunctor ey ez).obj g) ≅
      Bicategory.postcomp (B := B) x g ⋙ Conjugation.homFunctor ex ez :=
  CategoryTheory.Functor.isoWhiskerLeft (Conjugation.homFunctor ex ey)
      (Bicategory.associatorNatIsoLeft (B := B) a (ey.hom ≫ g) ez.inv).symm ≪≫
    CategoryTheory.Functor.isoWhiskerRight
      (CategoryTheory.Functor.isoWhiskerLeft (Bicategory.precomp (B := B) y ex.hom)
        (cancelMiddleNatIsoLeft (a := a) ey g))
      (Bicategory.postcomp (B := B) a ez.inv) ≪≫
    CategoryTheory.Functor.isoWhiskerRight (Bicategory.associatorNatIsoMiddle (B := B) ex.hom g)
      (Bicategory.postcomp (B := B) a ez.inv)

/-- The natural construction uses the old compositor, not a replacement. -/
@[simp] theorem compNatIsoRight_hom_app
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (ez : Bicategory.Equivalence c z) (f : x ⟶ y) (g : y ⟶ z) :
    (compNatIsoRight ex ey ez f).hom.app g =
      (Conjugation.compIso ex ey ez f g).inv :=
  rfl

/-- The other natural construction has exactly the same old component. -/
@[simp] theorem compNatIsoLeft_hom_app
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (ez : Bicategory.Equivalence c z) (f : x ⟶ y) (g : y ⟶ z) :
    (compNatIsoLeft ex ey ez g).hom.app f =
      (Conjugation.compIso ex ey ez f g).inv :=
  rfl

/-- Naturality for an arbitrary 2-cell in the right argument. -/
theorem compIso_naturality_right
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (ez : Bicategory.Equivalence c z) (f : x ⟶ y)
    {g h : y ⟶ z} (eta : g ⟶ h) :
    (Conjugation.homFunctor ex ez).map (f ◁ eta) ≫
        (Conjugation.compIso ex ey ez f h).hom =
      (Conjugation.compIso ex ey ez f g).hom ≫
        (Conjugation.homFunctor ex ey).obj f ◁
          (Conjugation.homFunctor ey ez).map eta :=
  (compNatIsoRight ex ey ez f).inv.naturality eta

/-- Naturality for an arbitrary 2-cell in the left argument. -/
theorem compIso_naturality_left
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (ez : Bicategory.Equivalence c z) {f g : x ⟶ y}
    (eta : f ⟶ g) (h : y ⟶ z) :
    (Conjugation.homFunctor ex ez).map (eta ▷ h) ≫
        (Conjugation.compIso ex ey ez g h).hom =
      (Conjugation.compIso ex ey ez f h).hom ≫
        (Conjugation.homFunctor ex ey).map eta ▷
          (Conjugation.homFunctor ey ez).obj h :=
  (compNatIsoLeft ex ey ez h).inv.naturality eta

end ConjugationNaturality

/-! ## Native actual-lift interface -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}
variable {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
  (W := W) A WorldLabel PresentationLabel}

/-- Right-variable naturality survives the exact actual-lift re-packaging. -/
theorem actualLiftQuasiInverseMapComp_naturality_right
    (f : X ⟶ Y) {g h : Y ⟶ Z} (eta : g ⟶ h) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (f ◁ eta) ≫
        (actualLiftQuasiInverseMapCompIso (W := W) A f h).hom =
      (actualLiftQuasiInverseMapCompIso (W := W) A f g).hom ≫
        (actualLiftQuasiInversePrelax (W := W) A).map f ◁
          (actualLiftQuasiInversePrelax (W := W) A).map₂ eta := by
  exact ConjugationNaturality.compIso_naturality_right
    (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) f eta

/-- Left-variable naturality survives the same exact re-packaging. -/
theorem actualLiftQuasiInverseMapComp_naturality_left
    {f g : X ⟶ Y} (eta : f ⟶ g) (h : Y ⟶ Z) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (eta ▷ h) ≫
        (actualLiftQuasiInverseMapCompIso (W := W) A g h).hom =
      (actualLiftQuasiInverseMapCompIso (W := W) A f h).hom ≫
        (actualLiftQuasiInversePrelax (W := W) A).map₂ eta ▷
          (actualLiftQuasiInversePrelax (W := W) A).map h := by
  exact ConjugationNaturality.compIso_naturality_left
    (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) eta h

/-- Exactly the map₂_whisker_left equation in Mathlib's Pseudofunctor. -/
theorem actualLiftQuasiInverse_map₂_whisker_left
    (f : X ⟶ Y) {g h : Y ⟶ Z} (eta : g ⟶ h) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (f ◁ eta) =
      (actualLiftQuasiInverseMapCompIso (W := W) A f g).hom ≫
        (actualLiftQuasiInversePrelax (W := W) A).map f ◁
          (actualLiftQuasiInversePrelax (W := W) A).map₂ eta ≫
            (actualLiftQuasiInverseMapCompIso (W := W) A f h).inv := by
  have hs := actualLiftQuasiInverseMapComp_naturality_right (W := W) A f eta
  simpa only [Category.assoc, Iso.hom_inv_id, Category.comp_id] using
    congrArg (fun k => k ≫ (actualLiftQuasiInverseMapCompIso (W := W) A f h).inv) hs

/-- Exactly the map₂_whisker_right equation in Mathlib's Pseudofunctor. -/
theorem actualLiftQuasiInverse_map₂_whisker_right
    {f g : X ⟶ Y} (eta : f ⟶ g) (h : Y ⟶ Z) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (eta ▷ h) =
      (actualLiftQuasiInverseMapCompIso (W := W) A f h).hom ≫
        (actualLiftQuasiInversePrelax (W := W) A).map₂ eta ▷
          (actualLiftQuasiInversePrelax (W := W) A).map h ≫
            (actualLiftQuasiInverseMapCompIso (W := W) A g h).inv := by
  have hs := actualLiftQuasiInverseMapComp_naturality_left (W := W) A eta h
  simpa only [Category.assoc, Iso.hom_inv_id, Category.comp_id] using
    congrArg (fun k => k ≫ (actualLiftQuasiInverseMapCompIso (W := W) A g h).inv) hs

/-! ## Regression: arbitrary, not necessarily invertible, 2-cells -/

section Regression

example (f : X ⟶ Y) {g h : Y ⟶ Z} (eta : g ⟶ h) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (f ◁ eta) =
      (actualLiftQuasiInverseMapCompIso (W := W) A f g).hom ≫
        (actualLiftQuasiInversePrelax (W := W) A).map f ◁
          (actualLiftQuasiInversePrelax (W := W) A).map₂ eta ≫
            (actualLiftQuasiInverseMapCompIso (W := W) A f h).inv :=
  actualLiftQuasiInverse_map₂_whisker_left (W := W) A f eta

example {f g : X ⟶ Y} (eta : f ⟶ g) (h : Y ⟶ Z) :
    (actualLiftQuasiInversePrelax (W := W) A).map₂ (eta ▷ h) =
      (actualLiftQuasiInverseMapCompIso (W := W) A f h).hom ≫
        (actualLiftQuasiInversePrelax (W := W) A).map₂ eta ▷
          (actualLiftQuasiInversePrelax (W := W) A).map h ≫
            (actualLiftQuasiInverseMapCompIso (W := W) A g h).inv :=
  actualLiftQuasiInverse_map₂_whisker_right (W := W) A eta h

example (f : X ⟶ Y) :
    ((actualLiftQuasiInversePrelax (W := W) A).map f).actualLift.map.raw =
      ((actualLiftQuasiInversePrelax (W := W) A).map f).raw.map :=
  ((actualLiftQuasiInversePrelax (W := W) A).map f).raw_eq

end Regression

/-!
## Boundary after v5.47

Both horizontal whiskering obligations are now supplied as theorems for the
same v5.46 prelax map and the same v5.46 compositor.  No choice is changed.
The remaining native constructor fields are map₂_associator,
map₂_left_unitor, and map₂_right_unitor.  Global pseudonatural unit/counit
and their roundtrip coherences are not claimed here.
-/

#print axioms ConjugationNaturality.compNatIsoRight
#print axioms ConjugationNaturality.compNatIsoLeft
#print axioms ConjugationNaturality.compNatIsoRight_hom_app
#print axioms ConjugationNaturality.compNatIsoLeft_hom_app
#print axioms ConjugationNaturality.compIso_naturality_right
#print axioms ConjugationNaturality.compIso_naturality_left
#print axioms actualLiftQuasiInverseMapComp_naturality_right
#print axioms actualLiftQuasiInverseMapComp_naturality_left
#print axioms actualLiftQuasiInverse_map₂_whisker_left
#print axioms actualLiftQuasiInverse_map₂_whisker_right

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseNaturalityV5_47
