import KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49

namespace KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48

set_option autoImplicit false

noncomputable section

/-!
# Source unit for the actual-lift classification pair v5.50

Keep the v5.42 projection F, v5.48 quasi-inverse G, and the single fixed v5.46
object equivalences unchanged.  The source roundtrip R is the native composite
F;G.  Its unit component at X is the actual-lift re-packaging of e_(F X).inv.

First construct the inverse-component conjugation transformation in an arbitrary
bicategory.  Its naturality inserts the inverse of the original counit.
Identity coherence is the inverse of the original right triangle; composition
coherence exchanges the two counit contractions after reversing the diagram.
The latter proof uses exactly the old compositor, not a replacement choice.

Then re-package the components, their adjoint equivalences, and naturality
isomorphisms in the actual-lift bicategory.  Its inherited 2-cell operations
allow the generic laws to inhabit the native StrongTrans fields directly.
Global triangle modifications and their integrated certificate remain separate.
-/

namespace ConjugationUnit

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c x y z : B}

/-- Insert the fixed source inverse/forward pair by reversing its counit
contraction.  The displayed parentheses agree with the v5.46 hom functor. -/
def naturalityIso (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (f : x ⟶ y) :
    f ≫ ey.inv ≅ ex.inv ≫ (Conjugation.homFunctor ex ey).obj f :=
  ((α_ ex.inv (ex.hom ≫ f) ey.inv).symm ≪≫
    Bicategory.whiskerRightIso (B := B)
      ((α_ ex.inv ex.hom f).symm ≪≫
        Bicategory.whiskerRightIso (B := B) ex.counit f ≪≫ (λ_ f)) ey.inv).symm

/-- Naturality for arbitrary 2-cells, not just invertible ones. -/
theorem naturality (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) {f g : x ⟶ y} (theta : f ⟶ g) :
    theta ▷ ey.inv ≫ (naturalityIso ex ey g).hom =
      (naturalityIso ex ey f).hom ≫
        ex.inv ◁ (Conjugation.homFunctor ex ey).map theta := by
  calc
    _ = 𝟙 (f ≫ ey.inv) ⊗≫
        ((𝟙 x) ◁ theta ≫ ex.counit.inv ▷ g) ▷ ey.inv ⊗≫
        𝟙 (ex.inv ≫ ((ex.hom ≫ g) ≫ ey.inv)) := by
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory
    _ = 𝟙 (f ≫ ey.inv) ⊗≫
        (ex.counit.inv ▷ f ≫ (ex.inv ≫ ex.hom) ◁ theta) ▷ ey.inv ⊗≫
        𝟙 (ex.inv ≫ ((ex.hom ≫ g) ≫ ey.inv)) := by
      rw [Bicategory.whisker_exchange (B := B) ex.counit.inv theta]
    _ = _ := by
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory

/-- Reversing the original right triangle gives the left triangle for the
inverse component, with the original unit and counit simply inverted. -/
theorem reverseTriangle_hom (ex : Bicategory.Equivalence a x) :
    Bicategory.leftZigzag ex.counit.inv ex.unit.inv =
      (λ_ ex.inv).hom ≫ (ρ_ ex.inv).inv := by
  simpa only [Bicategory.rightZigzagIso_inv, Iso.trans_inv, Iso.symm_inv]
    using congrArg Iso.inv ex.right_triangle

/-- The complete native identity law, including the identity comparison of
its source identity pseudofunctor. -/
theorem id (ex : Bicategory.Equivalence a x) :
    (naturalityIso ex ex (𝟙 x)).hom ≫ ex.inv ◁ (Conjugation.idIso ex).hom =
      (𝟙 (𝟙 x)) ▷ ex.inv ≫ (λ_ ex.inv).hom ≫ (ρ_ ex.inv).inv := by
  rw [Bicategory.id_whiskerRight, Category.id_comp]
  calc
    _ = 𝟙 ((𝟙 x) ≫ ex.inv) ⊗≫
        Bicategory.leftZigzag ex.counit.inv ex.unit.inv ⊗≫
        𝟙 (ex.inv ≫ (𝟙 a)) := by
      dsimp [naturalityIso, Conjugation.idIso, Bicategory.leftZigzag]
      bicategory
    _ = _ := by
      rw [reverseTriangle_hom ex]
      bicategory

/-- Expose the unchanged v5.46 compositor without referencing the private
middle-cancellation declaration by its compiler-generated name. -/
private theorem compIso_inv_expansion
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (ez : Bicategory.Equivalence c z) (f : x ⟶ y) (g : y ⟶ z) :
    (Conjugation.compIso ex ey ez f g).inv =
      (α_ ((ex.hom ≫ f) ≫ ey.inv) (ey.hom ≫ g) ez.inv).inv ≫
        ((α_ (ex.hom ≫ f) ey.inv (ey.hom ≫ g)).hom ≫
          (ex.hom ≫ f) ◁ (α_ ey.inv ey.hom g).inv ≫
          (ex.hom ≫ f) ◁ (ey.counit.hom ▷ g) ≫
          (ex.hom ≫ f) ◁ (λ_ g).hom) ▷ ez.inv ≫
        (α_ ex.hom f g).hom ▷ ez.inv := rfl

/-- Reverse the composition diagram so that both paths only contract
counits.  The substantive equality is their explicit exchange law. -/
theorem comp_inv (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    Bicategory.whiskerLeftIso (B := B) ex.inv
        (Conjugation.compIso ex ey ez f g).symm ≪≫
        (naturalityIso ex ez (f ≫ g)).symm =
      (α_ ex.inv ((Conjugation.homFunctor ex ey).obj f)
        ((Conjugation.homFunctor ey ez).obj g)).symm ≪≫
        Bicategory.whiskerRightIso (B := B) (naturalityIso ex ey f).symm
          ((Conjugation.homFunctor ey ez).obj g) ≪≫
        (α_ f ey.inv ((Conjugation.homFunctor ey ez).obj g)) ≪≫
        Bicategory.whiskerLeftIso (B := B) f (naturalityIso ey ez g).symm ≪≫
        (α_ f g ez.inv).symm := by
  apply Iso.ext
  change ex.inv ◁ (Conjugation.compIso ex ey ez f g).inv ≫
    (naturalityIso ex ez (f ≫ g)).inv = _
  calc
    _ = 𝟙 (ex.inv ≫ (((ex.hom ≫ f) ≫ ey.inv) ≫
          ((ey.hom ≫ g) ≫ ez.inv))) ⊗≫
        ((((ex.inv ≫ ex.hom) ≫ f) ◁ ey.counit.hom ≫
          (ex.counit.hom ▷ f) ▷ (𝟙 y)) ▷ g) ▷ ez.inv ⊗≫
        𝟙 ((f ≫ g) ≫ ez.inv) := by
      rw [compIso_inv_expansion]
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory
    _ = 𝟙 (ex.inv ≫ (((ex.hom ≫ f) ≫ ey.inv) ≫
          ((ey.hom ≫ g) ≫ ez.inv))) ⊗≫
        (((ex.counit.hom ▷ f) ▷ (ey.inv ≫ ey.hom) ≫
          (𝟙 x ≫ f) ◁ ey.counit.hom) ▷ g) ▷ ez.inv ⊗≫
        𝟙 ((f ≫ g) ≫ ez.inv) := by
      rw [Bicategory.whisker_exchange (B := B)
        (ex.counit.hom ▷ f) ey.counit.hom]
    _ = _ := by
      dsimp [Conjugation.homFunctor, naturalityIso]
      bicategory

/-- Invert the proved isomorphism equality to obtain the full native
StrongTrans composition law for the original forward compositor. -/
theorem comp (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    (naturalityIso ex ez (f ≫ g)).hom ≫
        ex.inv ◁ (Conjugation.compIso ex ey ez f g).hom =
      (𝟙 (f ≫ g)) ▷ ez.inv ≫ (α_ f g ez.inv).hom ≫
        f ◁ (naturalityIso ey ez g).hom ≫
        (α_ f ey.inv ((Conjugation.homFunctor ey ez).obj g)).inv ≫
        (naturalityIso ex ey f).hom ▷ ((Conjugation.homFunctor ey ez).obj g) ≫
        (α_ ex.inv ((Conjugation.homFunctor ex ey).obj f)
          ((Conjugation.homFunctor ey ez).obj g)).hom := by
  have h := congrArg Iso.inv (comp_inv ex ey ez f g)
  simpa only [Iso.trans_inv, Iso.symm_inv, Bicategory.whiskerLeftIso_inv,
    Bicategory.whiskerRightIso_inv, Category.assoc, Bicategory.id_whiskerRight,
    Category.id_comp] using h

/-- Cancel the image of an identity 2-cell before the fixed identity comparison.
Keep the bicategory explicit here.  The fully qualified theorem is the
categorical functor law, not the root programming Functor.map_id. -/
theorem map_id_idIso_hom (ex : Bicategory.Equivalence a x) :
    (Conjugation.homFunctor ex ex).map (𝟙 (𝟙 x)) ≫
        (Conjugation.idIso ex).hom = (Conjugation.idIso ex).hom := by
  rw [CategoryTheory.Functor.map_id, Category.id_comp]

/-- The same typed cancellation for the original compositor.  Specializing
this equality avoids elaborating a new composite hom-category expression
inside the concrete actual-lift classification bicategory. -/
theorem map_id_compIso_hom (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    (Conjugation.homFunctor ex ez).map (𝟙 (f ≫ g)) ≫
        (Conjugation.compIso ex ey ez f g).hom =
      (Conjugation.compIso ex ey ez f g).hom := by
  rw [CategoryTheory.Functor.map_id, Category.id_comp]

end ConjugationUnit

/-! ## The fixed source roundtrip and its native comparisons -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The native source roundtrip of exactly the v5.42/v5.48 pair. -/
def actualLiftSourceRoundtrip :
    Pseudofunctor
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.comp
    (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
    (actualLiftQuasiInversePseudofunctor (W := W) A)

/-- This is an alias of the original fixed e_(F X), not a fresh choice. -/
def actualLiftSourceObjectEquivalence
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Equivalence
      (CanonicalExactUniversalObject (W := W) A
        ((actualLiftSourceRoundtrip (W := W) A).obj X))
      (CanonicalExactUniversalObject (W := W) A X) :=
  actualLiftQuasiInverseObjectEquivalence (W := W) A
    (CanonicalExactUniversalObject (W := W) A X)

@[simp] theorem actualLiftSourceRoundtrip_obj_label
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftSourceRoundtrip (W := W) A).obj X).label = X.label := rfl

@[simp] theorem actualLiftSourceRoundtrip_map_actualLift
    {X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    ((actualLiftSourceRoundtrip (W := W) A).map f).actualLift =
      (Conjugation.homFunctor (actualLiftSourceObjectEquivalence (W := W) A X)
        (actualLiftSourceObjectEquivalence (W := W) A Y)).obj f.actualLift := rfl

@[simp] theorem actualLiftSourceRoundtrip_map₂
    {X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y} (theta : f ⟶ g) :
    (actualLiftSourceRoundtrip (W := W) A).map₂ theta =
      (Conjugation.homFunctor (actualLiftSourceObjectEquivalence (W := W) A X)
        (actualLiftSourceObjectEquivalence (W := W) A Y)).map theta := rfl

/-- Remove the mapped identity comparison contributed by the strict F. -/
@[simp] theorem actualLiftSourceRoundtrip_mapId_hom
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftSourceRoundtrip (W := W) A).mapId X).hom =
      (Conjugation.idIso (actualLiftSourceObjectEquivalence (W := W) A X)).hom := by
  exact ConjugationUnit.map_id_idIso_hom
    (actualLiftSourceObjectEquivalence (W := W) A X)

/-- The native source compositor has exactly the original conjugation image. -/
@[simp] theorem actualLiftSourceRoundtrip_mapComp_hom
    {X Y Z : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom =
      (Conjugation.compIso (actualLiftSourceObjectEquivalence (W := W) A X)
        (actualLiftSourceObjectEquivalence (W := W) A Y)
        (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift).hom := by
  exact ConjugationUnit.map_id_compIso_hom
    (actualLiftSourceObjectEquivalence (W := W) A X)
    (actualLiftSourceObjectEquivalence (W := W) A Y)
    (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift

/-! ## Re-packaged inverse components and the native source unit -/

/-- Source unit component, storing the inverse of the fixed e_(F X). -/
def actualLiftSourceUnitComponent
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    X ⟶ (actualLiftSourceRoundtrip (W := W) A).obj X :=
  actualOneCellOfExactUniversalClassificationOneCell (W := W) A
    (X := X) (Y := (actualLiftSourceRoundtrip (W := W) A).obj X)
    (actualLiftSourceObjectEquivalence (W := W) A X).inv

/-- The inverse component stores the corresponding fixed forward one-cell. -/
def actualLiftSourceUnitComponentInverse
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftSourceRoundtrip (W := W) A).obj X ⟶ X :=
  actualOneCellOfExactUniversalClassificationOneCell (W := W) A
    (X := (actualLiftSourceRoundtrip (W := W) A).obj X) (Y := X)
    (actualLiftSourceObjectEquivalence (W := W) A X).hom

/-- The source component is an actual adjoint equivalence, not just a
one-cell whose image happens to be an equivalence. -/
def actualLiftSourceUnitComponentEquivalence
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Equivalence X ((actualLiftSourceRoundtrip (W := W) A).obj X) where
  hom := actualLiftSourceUnitComponent (W := W) A X
  inv := actualLiftSourceUnitComponentInverse (W := W) A X
  unit := ExactLiftableClassificationActualTwoCell.isoOfActualLift (W := W) A
    (f := 𝟙 X)
    (g := actualLiftSourceUnitComponent (W := W) A X ≫
      actualLiftSourceUnitComponentInverse (W := W) A X)
    (actualLiftSourceObjectEquivalence (W := W) A X).counit.symm
  counit := ExactLiftableClassificationActualTwoCell.isoOfActualLift (W := W) A
    (f := actualLiftSourceUnitComponentInverse (W := W) A X ≫
      actualLiftSourceUnitComponent (W := W) A X)
    (g := 𝟙 ((actualLiftSourceRoundtrip (W := W) A).obj X))
    (actualLiftSourceObjectEquivalence (W := W) A X).unit.symm
  left_triangle := by
    apply Iso.ext
    exact ConjugationUnit.reverseTriangle_hom
      (actualLiftSourceObjectEquivalence (W := W) A X)

/-- Re-package the generic naturality isomorphism without forgetting the
stored target one-cells or replacing the source roundtrip map. -/
def actualLiftSourceUnitNaturality
    {X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    f ≫ actualLiftSourceUnitComponent (W := W) A Y ≅
      actualLiftSourceUnitComponent (W := W) A X ≫
        (actualLiftSourceRoundtrip (W := W) A).map f :=
  ExactLiftableClassificationActualTwoCell.isoOfActualLift (W := W) A
    (f := f ≫ actualLiftSourceUnitComponent (W := W) A Y)
    (g := actualLiftSourceUnitComponent (W := W) A X ≫
      (actualLiftSourceRoundtrip (W := W) A).map f)
    (ConjugationUnit.naturalityIso (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A Y) f.actualLift)

/-- The global source unit for the unchanged actual-lift pair, with all
three native coherence fields. -/
def actualLiftSourceRoundtripUnit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id
        (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel))
      (actualLiftSourceRoundtrip (W := W) A) where
  app X := actualLiftSourceUnitComponent (W := W) A X
  naturality {X Y} f := actualLiftSourceUnitNaturality (W := W) A f
  naturality_naturality {X Y} {f g} theta := by
    exact ConjugationUnit.naturality (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A Y) theta
  naturality_id X := by
    rw [actualLiftSourceRoundtrip_mapId_hom]
    exact ConjugationUnit.id (actualLiftSourceObjectEquivalence (W := W) A X)
  naturality_comp {X Y Z} f g := by
    rw [actualLiftSourceRoundtrip_mapComp_hom]
    exact ConjugationUnit.comp (actualLiftSourceObjectEquivalence (W := W) A X)
      (actualLiftSourceObjectEquivalence (W := W) A Y)
      (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift

@[simp] theorem actualLiftSourceRoundtripUnit_app_actualLift
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftSourceRoundtripUnit (W := W) A).app X).actualLift =
      (actualLiftQuasiInverseObjectEquivalence (W := W) A
        (CanonicalExactUniversalObject (W := W) A X)).inv := rfl

/-! ## Regression checks through the full native interface -/

-- Regression specification: the unit must belong to the actual v5.42/v5.48
-- pair, in the source direction, without replacing either pseudofunctor.
example : Pseudofunctor.StrongTrans
    (Pseudofunctor.id
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel))
    (Pseudofunctor.comp
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
      (actualLiftQuasiInversePseudofunctor (W := W) A)) :=
  actualLiftSourceRoundtripUnit (W := W) A

section Regression
variable {X Y Z : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
  (W := W) A WorldLabel PresentationLabel}

-- Direct comparison regressions cover both projection lemmas repaired here.
example :
    ((actualLiftSourceRoundtrip (W := W) A).mapId X).hom =
      (Conjugation.idIso (actualLiftSourceObjectEquivalence (W := W) A X)).hom :=
  actualLiftSourceRoundtrip_mapId_hom (W := W) A X

example (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom =
      (Conjugation.compIso (actualLiftSourceObjectEquivalence (W := W) A X)
        (actualLiftSourceObjectEquivalence (W := W) A Y)
        (actualLiftSourceObjectEquivalence (W := W) A Z) f.actualLift g.actualLift).hom :=
  actualLiftSourceRoundtrip_mapComp_hom (W := W) A f g

example :
    let R := actualLiftSourceRoundtrip (W := W) A
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    (eta.naturality (𝟙 X)).hom ≫ eta.app X ◁ (R.mapId X).hom =
      (𝟙 (𝟙 X)) ▷ eta.app X ≫ (λ_ (eta.app X)).hom ≫ (ρ_ (eta.app X)).inv :=
  (actualLiftSourceRoundtripUnit (W := W) A).naturality_id X

example (f : X ⟶ Y) (g : Y ⟶ Z) :
    let R := actualLiftSourceRoundtrip (W := W) A
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    (eta.naturality (f ≫ g)).hom ≫ eta.app X ◁ (R.mapComp f g).hom =
      (𝟙 (f ≫ g)) ▷ eta.app Z ≫ (α_ f g (eta.app Z)).hom ≫
        f ◁ (eta.naturality g).hom ≫ (α_ f (eta.app Y) (R.map g)).inv ≫
        (eta.naturality f).hom ▷ R.map g ≫ (α_ (eta.app X) (R.map f) (R.map g)).hom :=
  (actualLiftSourceRoundtripUnit (W := W) A).naturality_comp f g

example {f g : X ⟶ Y} (theta : f ⟶ g) :
    let R := actualLiftSourceRoundtrip (W := W) A
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    theta ▷ eta.app Y ≫ (eta.naturality g).hom =
      (eta.naturality f).hom ≫ eta.app X ◁ R.map₂ theta :=
  (actualLiftSourceRoundtripUnit (W := W) A).naturality_naturality theta

example (f : X ⟶ Y) :
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom ≫
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).inv =
      𝟙 (f ≫ (actualLiftSourceRoundtripUnit (W := W) A).app Y) :=
  ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom_inv_id

example : ∃ e : Bicategory.Equivalence X
    ((actualLiftSourceRoundtrip (W := W) A).obj X),
    e.hom = (actualLiftSourceRoundtripUnit (W := W) A).app X :=
  ⟨actualLiftSourceUnitComponentEquivalence (W := W) A X, rfl⟩

end Regression

/-!
## Boundary after v5.50

The source unit is a native StrongTrans Id_L => F;G for the same pair that has
the v5.49 target counit.  Each component is an adjoint equivalence in L and
projects literally to the inverse of the original fixed e_(F X).  Naturality
holds for arbitrary 2-cells, and both native identity/composition laws retain
the original comparison maps.  External labels are preserved literally.

Still separate: triangle representatives and invertible modifications for
this particular pair, followed by their integrated coherent certificate.
No strict raw-forgetting claim or equality of independent presentations is made.
-/

#print axioms ConjugationUnit.naturality
#print axioms ConjugationUnit.reverseTriangle_hom
#print axioms ConjugationUnit.id
#print axioms ConjugationUnit.comp_inv
#print axioms ConjugationUnit.comp
#print axioms ConjugationUnit.map_id_idIso_hom
#print axioms ConjugationUnit.map_id_compIso_hom
#print axioms actualLiftSourceRoundtrip
#print axioms actualLiftSourceObjectEquivalence
#print axioms actualLiftSourceRoundtrip_mapId_hom
#print axioms actualLiftSourceRoundtrip_mapComp_hom
#print axioms actualLiftSourceUnitComponentEquivalence
#print axioms actualLiftSourceUnitNaturality
#print axioms actualLiftSourceRoundtripUnit

end

end KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
