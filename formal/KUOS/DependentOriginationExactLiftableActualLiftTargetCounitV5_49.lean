import KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
import KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48

set_option autoImplicit false

noncomputable section

/-!
# Target counit for the actual-lift classification pair v5.49

Compose the actual v5.48 backwards pseudofunctor G with the v5.42 strict
projection F.  The resulting target endopseudofunctor is not definitionally
identity: its one-cell map is conjugation by the single fixed v5.46 object
choices.  Its counit component at Y is the same chosen eY.hom.

First prove the three strong-transformation laws in an arbitrary bicategory.
Naturality exchanges an arbitrary 2-cell with the final counit.  Identity uses
the chosen equivalence's left triangle.  Composition exchanges the two
independent counit contractions.  The old v5.46 compositor is kept unchanged;
its inverse is exposed by a reflexive expansion, not replaced by a new choice.

Then project the native composite's comparison maps and assemble all fields of
Pseudofunctor.StrongTrans.  Source unit and triangle modifications for this
particular pair remain separate.  No equality of independently chosen
presentations or strict preservation of the original raw map is asserted.
-/

namespace ConjugationCounit

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c x y z : B}

/-- Contract the final inverse/forward pair with the chosen target counit. -/
def naturalityIso (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (f : x ⟶ y) :
    (Conjugation.homFunctor ex ey).obj f ≫ ey.hom ≅ ex.hom ≫ f :=
  (α_ (ex.hom ≫ f) ey.inv ey.hom) ≪≫
    Bicategory.whiskerLeftIso (B := B) (ex.hom ≫ f) ey.counit ≪≫
    (ρ_ (ex.hom ≫ f))

/-- An arbitrary, not necessarily invertible, 2-cell commutes with the final
counit contraction by the bicategorical exchange law. -/
theorem naturality (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) {f g : x ⟶ y} (eta : f ⟶ g) :
    (Conjugation.homFunctor ex ey).map eta ▷ ey.hom ≫
        (naturalityIso ex ey g).hom =
      (naturalityIso ex ey f).hom ≫ ex.hom ◁ eta := by
  calc
    _ = 𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫ ey.hom) ⊗≫
        ((ex.hom ◁ eta) ▷ (ey.inv ≫ ey.hom) ≫
          (ex.hom ≫ g) ◁ ey.counit.hom) ⊗≫
        𝟙 (ex.hom ≫ g) := by
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory
    _ = 𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫ ey.hom) ⊗≫
        ((ex.hom ≫ f) ◁ ey.counit.hom ≫
          (ex.hom ◁ eta) ▷ (𝟙 y)) ⊗≫
        𝟙 (ex.hom ≫ g) := by
      rw [← Bicategory.whisker_exchange (B := B)
        (ex.hom ◁ eta) ey.counit.hom]
    _ = _ := by
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory

/-- Identity coherence in the insertion direction is the left triangle. -/
theorem id_lax (ex : Bicategory.Equivalence a x) :
    (Conjugation.idIso ex).inv ▷ ex.hom ≫
        (naturalityIso ex ex (𝟙 x)).hom ≫ (ρ_ ex.hom).hom =
      (λ_ ex.hom).hom := by
  calc
    _ = 𝟙 (𝟙 a ≫ ex.hom) ⊗≫
        Bicategory.leftZigzag ex.unit.hom ex.counit.hom ⊗≫
        𝟙 ex.hom := by
      dsimp [Conjugation.idIso, naturalityIso, Bicategory.leftZigzag]
      bicategory
    _ = _ := by
      rw [ex.left_triangle_hom]
      bicategory

/-- Identity coherence in the direction required by native StrongTrans. -/
theorem id (ex : Bicategory.Equivalence a x) :
    (naturalityIso ex ex (𝟙 x)).hom =
      (Conjugation.idIso ex).hom ▷ ex.hom ≫
        (λ_ ex.hom).hom ≫ (ρ_ ex.hom).inv := by
  let i := Bicategory.whiskerRightIso (B := B) (Conjugation.idIso ex) ex.hom
  change (naturalityIso ex ex (𝟙 x)).hom =
    i.hom ≫ (λ_ ex.hom).hom ≫ (ρ_ ex.hom).inv
  apply (cancel_epi i.inv).1
  apply (cancel_mono (ρ_ ex.hom).hom).1
  have h := id_lax ex
  change i.inv ≫ (naturalityIso ex ex (𝟙 x)).hom ≫
    (ρ_ ex.hom).hom = (λ_ ex.hom).hom at h
  simpa only [Category.assoc, Iso.inv_hom_id_assoc, Iso.inv_hom_id,
    Category.comp_id] using h

/-- Expose v5.46's private middle cancellation without depending on its
compiler-generated private name or changing the compositor. -/
private theorem compIso_inv_expansion
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (ez : Bicategory.Equivalence c z) (f : x ⟶ y) (g : y ⟶ z) :
    (Conjugation.compIso ex ey ez f g).inv =
      (α_ ((ex.hom ≫ f) ≫ ey.inv) (ey.hom ≫ g) ez.inv).inv ≫
        ((α_ (ex.hom ≫ f) ey.inv (ey.hom ≫ g)).hom ≫
          (ex.hom ≫ f) ◁ (α_ ey.inv ey.hom g).inv ≫
          (ex.hom ≫ f) ◁ (ey.counit.hom ▷ g) ≫
          (ex.hom ≫ f) ◁ (λ_ g).hom) ▷ ez.inv ≫
        (α_ ex.hom f g).hom ▷ ez.inv :=
  rfl

/-- The inverse-compositor form compares the two orders of counit
contraction.  The exchange law is explicit; bicategory only rearranges
structural associators and unitors. -/
theorem comp_lax (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    (Conjugation.compIso ex ey ez f g).inv ▷ ez.hom ≫
        (naturalityIso ex ez (f ≫ g)).hom =
      (α_ ((Conjugation.homFunctor ex ey).obj f)
        ((Conjugation.homFunctor ey ez).obj g) ez.hom).hom ≫
        (Conjugation.homFunctor ex ey).obj f ◁ (naturalityIso ey ez g).hom ≫
        (α_ ((Conjugation.homFunctor ex ey).obj f) ey.hom g).inv ≫
        (naturalityIso ex ey f).hom ▷ g ≫ (α_ ex.hom f g).hom := by
  calc
    _ = 𝟙 ((((ex.hom ≫ f) ≫ ey.inv) ≫
          ((ey.hom ≫ g) ≫ ez.inv)) ≫ ez.hom) ⊗≫
        (ex.hom ≫ f) ◁
          ((ey.counit.hom ▷ g) ▷ (ez.inv ≫ ez.hom) ≫
            (𝟙 y ≫ g) ◁ ez.counit.hom) ⊗≫
        𝟙 (ex.hom ≫ (f ≫ g)) := by
      simp only [compIso_inv_expansion]
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory
    _ = 𝟙 ((((ex.hom ≫ f) ≫ ey.inv) ≫
          ((ey.hom ≫ g) ≫ ez.inv)) ≫ ez.hom) ⊗≫
        (ex.hom ≫ f) ◁
          (((ey.inv ≫ ey.hom) ≫ g) ◁ ez.counit.hom ≫
            (ey.counit.hom ▷ g) ▷ (𝟙 z)) ⊗≫
        𝟙 (ex.hom ≫ (f ≫ g)) := by
      rw [← Bicategory.whisker_exchange (B := B)
        (ey.counit.hom ▷ g) ez.counit.hom]
    _ = _ := by
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory

/-- Composition coherence for the unchanged forward compositor. -/
theorem comp (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    (naturalityIso ex ez (f ≫ g)).hom =
      (Conjugation.compIso ex ey ez f g).hom ▷ ez.hom ≫
        (α_ ((Conjugation.homFunctor ex ey).obj f)
          ((Conjugation.homFunctor ey ez).obj g) ez.hom).hom ≫
        (Conjugation.homFunctor ex ey).obj f ◁ (naturalityIso ey ez g).hom ≫
        (α_ ((Conjugation.homFunctor ex ey).obj f) ey.hom g).inv ≫
        (naturalityIso ex ey f).hom ▷ g ≫ (α_ ex.hom f g).hom := by
  let i := Bicategory.whiskerRightIso (B := B)
    (Conjugation.compIso ex ey ez f g) ez.hom
  change (naturalityIso ex ez (f ≫ g)).hom =
    i.hom ≫
      (α_ ((Conjugation.homFunctor ex ey).obj f)
        ((Conjugation.homFunctor ey ez).obj g) ez.hom).hom ≫
      (Conjugation.homFunctor ex ey).obj f ◁ (naturalityIso ey ez g).hom ≫
      (α_ ((Conjugation.homFunctor ex ey).obj f) ey.hom g).inv ≫
      (naturalityIso ex ey f).hom ▷ g ≫ (α_ ex.hom f g).hom
  apply (cancel_epi i.inv).1
  simpa only [Category.assoc, Iso.inv_hom_id_assoc] using comp_lax ex ey ez f g

end ConjugationCounit

/-! ## The actual composite, with no change of objectwise choices -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Target roundtrip: the v5.48 backwards map followed by the v5.42 projection. -/
def actualLiftTargetRoundtrip :
    Pseudofunctor
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.comp
    (actualLiftQuasiInversePseudofunctor (W := W) A)
    (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor

@[simp] theorem actualLiftTargetRoundtrip_obj_label
    (X : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftTargetRoundtrip (W := W) A).obj X).label = X.label := rfl

@[simp] theorem actualLiftTargetRoundtrip_map
    {X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    (actualLiftTargetRoundtrip (W := W) A).map f =
      (Conjugation.homFunctor
        (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)).obj f := rfl

@[simp] theorem actualLiftTargetRoundtrip_map₂
    {X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y} (eta : f ⟶ g) :
    (actualLiftTargetRoundtrip (W := W) A).map₂ eta =
      (Conjugation.homFunctor
        (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)).map eta := rfl

/-- Native composite identity comparison projects to the original idIso. -/
@[simp] theorem actualLiftTargetRoundtrip_mapId_hom
    (X : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftTargetRoundtrip (W := W) A).mapId X).hom =
      (Conjugation.idIso
        (actualLiftQuasiInverseObjectEquivalence (W := W) A X)).hom := by
  change (Conjugation.idIso
    (actualLiftQuasiInverseObjectEquivalence (W := W) A X)).hom ≫ 𝟙 _ = _
  exact Category.comp_id _

/-- Native composite compositor projects to the same v5.46 compIso. -/
@[simp] theorem actualLiftTargetRoundtrip_mapComp_hom
    {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((actualLiftTargetRoundtrip (W := W) A).mapComp f g).hom =
      (Conjugation.compIso
        (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) f g).hom := by
  change (Conjugation.compIso
    (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) f g).hom ≫ 𝟙 _ = _
  exact Category.comp_id _

private theorem targetIdentity_mapId_hom
    (X : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((Pseudofunctor.id
      (ExactUniversalClassificationObject (W := W) A WorldLabel PresentationLabel)).mapId X).hom =
      𝟙 (𝟙 X) := rfl

private theorem targetIdentity_mapComp_hom
    {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((Pseudofunctor.id
      (ExactUniversalClassificationObject (W := W) A WorldLabel PresentationLabel)).mapComp f g).hom =
      𝟙 (f ≫ g) := rfl

/-- Global target counit for this specific actual-lift pair, including all
native 2-cell naturality, identity, and composition coherence fields. -/
def actualLiftTargetRoundtripCounit :
    Pseudofunctor.StrongTrans
      (actualLiftTargetRoundtrip (W := W) A)
      (Pseudofunctor.id
        (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)) where
  app X := (actualLiftQuasiInverseObjectEquivalence (W := W) A X).hom
  naturality {X Y} f := ConjugationCounit.naturalityIso
    (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y) f
  naturality_naturality {X Y} {f g} eta := by
    exact ConjugationCounit.naturality
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y) eta
  naturality_id X := by
    rw [targetIdentity_mapId_hom, actualLiftTargetRoundtrip_mapId_hom]
    simpa only [Bicategory.whiskerLeft_id, Category.comp_id] using
      ConjugationCounit.id (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
  naturality_comp {X Y Z} f g := by
    rw [targetIdentity_mapComp_hom, actualLiftTargetRoundtrip_mapComp_hom]
    simpa only [Bicategory.whiskerLeft_id, Category.comp_id] using
      ConjugationCounit.comp
        (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) f g

@[simp] theorem actualLiftTargetRoundtripCounit_app
    (X : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftTargetRoundtripCounit (W := W) A).app X =
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X).hom := rfl

@[simp] theorem actualLiftTargetRoundtripCounit_naturality
    {X Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    (actualLiftTargetRoundtripCounit (W := W) A).naturality f =
      ConjugationCounit.naturalityIso
        (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y) f := rfl

/-! ## Regression checks at the actual native interface -/

-- Regression specification: the new result must inhabit the native StrongTrans
-- for the actual v5.42/v5.48 pair, not an unrelated old roundtrip.
example : Pseudofunctor.StrongTrans
    (Pseudofunctor.comp
      (actualLiftQuasiInversePseudofunctor (W := W) A)
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor)
    (Pseudofunctor.id
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)) :=
  actualLiftTargetRoundtripCounit (W := W) A

section Regression
variable {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
  (W := W) A WorldLabel PresentationLabel}

example {f g : X ⟶ Y} (eta : f ⟶ g) :
    (actualLiftTargetRoundtrip (W := W) A).map₂ eta ▷
        (actualLiftTargetRoundtripCounit (W := W) A).app Y ≫
        ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom =
      ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom ≫
        (actualLiftTargetRoundtripCounit (W := W) A).app X ◁ eta :=
  (actualLiftTargetRoundtripCounit (W := W) A).naturality_naturality eta

example (f : X ⟶ Y) :
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom ≫
        ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).inv =
      𝟙 ((actualLiftTargetRoundtrip (W := W) A).map f ≫
        (actualLiftTargetRoundtripCounit (W := W) A).app Y) :=
  ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom_inv_id

example : ∃ e : Bicategory.Equivalence
    (B := ExactUniversalClassificationObject (W := W) A WorldLabel PresentationLabel)
    ((actualLiftTargetRoundtrip (W := W) A).obj X) X,
    e.hom = (actualLiftTargetRoundtripCounit (W := W) A).app X :=
  ⟨actualLiftQuasiInverseObjectEquivalence (W := W) A X, rfl⟩

end Regression

/-!
## Boundary after v5.49

The target roundtrip of the unchanged v5.42/v5.48 pair has a global native
StrongTrans counit with the same chosen objectwise equivalence components.
Naturality is proved for every 2-cell, and its identity/composition laws use
the actual native comparison maps.  Labels remain literal throughout.

Still separate for this pair: the source StrongTrans unit, actual triangle
components, invertible modifications, and their integrated certificate.
Existing ambient/localized-classification roundtrip results are unchanged.
-/

#print axioms ConjugationCounit.naturality
#print axioms ConjugationCounit.id_lax
#print axioms ConjugationCounit.id
#print axioms ConjugationCounit.compIso_inv_expansion
#print axioms ConjugationCounit.comp_lax
#print axioms ConjugationCounit.comp
#print axioms actualLiftTargetRoundtrip
#print axioms actualLiftTargetRoundtrip_mapId_hom
#print axioms actualLiftTargetRoundtrip_mapComp_hom
#print axioms actualLiftTargetRoundtripCounit

end

end KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
