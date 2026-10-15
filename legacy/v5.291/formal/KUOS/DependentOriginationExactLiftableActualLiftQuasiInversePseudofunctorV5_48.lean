import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseNaturalityV5_47
import Mathlib.CategoryTheory.Bicategory.Functor.Pseudofunctor
import Mathlib.Tactic.CategoryTheory.Bicategory.Basic

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseNaturalityV5_47

set_option autoImplicit false

noncomputable section

/-!
# The actual-lift quasi-inverse as a pseudofunctor v5.48

Keep the v5.46 object choices, prelax map, identity comparison, and compositor
unchanged.  v5.47 supplies both horizontal naturality equations.  This file
addresses the remaining associator and unitor coherence conditions.

Work first in an arbitrary bicategory in the lax direction: the inverse of
the existing compositor contracts the middle counit.  Associativity is the
exchange of two independent counit contractions.  Left and right unity are
the two triangle identities of the chosen adjoint equivalence.  The
bicategory tactic only arranges structural isomorphisms; the exchange law and
triangle identities are invoked explicitly.

After re-packaging these equations, use the native LaxFunctor and its
PseudoCore to build a Pseudofunctor with exactly the old comparison isos.
This does not yet supply a global pseudonatural unit/counit or their
modifications.  No raw morphism is asserted liftable without its witness.
-/

namespace ConjugationCoherence

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c d x y z t : B}

/-- Expose the existing compositor at the 2-cell level.  Reflexivity unfolds
v5.46's private middle-cancellation helper without naming its generated private
identifier.  This is an expansion theorem, not a replacement compositor. -/
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

-- The endpoints of intermediate ⊗≫ expressions below are written as explicit
-- composites: BicategoricalCoherence is synthesized before the tactic proof,
-- so a subsequent dsimp cannot repair an endpoint hidden by homFunctor.obj.

/-- Lax associativity: contracting the two middle counits in either order
agrees by whisker exchange.  All the comparisons are the original v5.46 ones. -/
theorem associator
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (ez : Bicategory.Equivalence c z) (et : Bicategory.Equivalence d t)
    (f : x ⟶ y) (g : y ⟶ z) (h : z ⟶ t) :
    (Conjugation.compIso ex ey ez f g).inv ▷
          (Conjugation.homFunctor ez et).obj h ≫
        (Conjugation.compIso ex ez et (f ≫ g) h).inv ≫
          (Conjugation.homFunctor ex et).map (α_ f g h).hom =
      (α_ ((Conjugation.homFunctor ex ey).obj f)
        ((Conjugation.homFunctor ey ez).obj g)
        ((Conjugation.homFunctor ez et).obj h)).hom ≫
        (Conjugation.homFunctor ex ey).obj f ◁
          (Conjugation.compIso ey ez et g h).inv ≫
        (Conjugation.compIso ex ey et f (g ≫ h)).inv := by
  calc
    _ = 𝟙 (((((ex.hom ≫ f) ≫ ey.inv) ≫ ((ey.hom ≫ g) ≫ ez.inv)) ≫
          ((ez.hom ≫ h) ≫ et.inv))) ⊗≫
        (ex.hom ≫ f) ◁
          ((ey.counit.hom ▷ g) ▷ (ez.inv ≫ ez.hom) ≫
            (𝟙 y ≫ g) ◁ ez.counit.hom) ▷ (h ≫ et.inv) ⊗≫
        𝟙 ((ex.hom ≫ (f ≫ (g ≫ h))) ≫ et.inv) := by
      simp only [compIso_inv_expansion]
      dsimp [Conjugation.homFunctor]
      bicategory
    _ = 𝟙 (((((ex.hom ≫ f) ≫ ey.inv) ≫ ((ey.hom ≫ g) ≫ ez.inv)) ≫
          ((ez.hom ≫ h) ≫ et.inv))) ⊗≫
        (ex.hom ≫ f) ◁
          (((ey.inv ≫ ey.hom) ≫ g) ◁ ez.counit.hom ≫
            (ey.counit.hom ▷ g) ▷ (𝟙 z)) ▷ (h ≫ et.inv) ⊗≫
        𝟙 ((ex.hom ≫ (f ≫ (g ≫ h))) ≫ et.inv) := by
      rw [← Bicategory.whisker_exchange (B := B)
        (ey.counit.hom ▷ g) ez.counit.hom]
    _ = _ := by
      simp only [compIso_inv_expansion]
      dsimp [Conjugation.homFunctor]
      bicategory

/-- The hom-form of lax left unity is the chosen equivalence's left triangle,
whiskered by the remaining original one-cell and the final inverse leg. -/
theorem leftUnitor_hom
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (f : x ⟶ y) :
    (λ_ ((Conjugation.homFunctor ex ey).obj f)).hom =
      (Conjugation.idIso ex).inv ▷ (Conjugation.homFunctor ex ey).obj f ≫
        (Conjugation.compIso ex ex ey (𝟙 x) f).inv ≫
          (Conjugation.homFunctor ex ey).map (λ_ f).hom := by
  symm
  calc
    _ = 𝟙 (𝟙 a ≫ ((ex.hom ≫ f) ≫ ey.inv)) ⊗≫
        (Bicategory.leftZigzag ex.unit.hom ex.counit.hom) ▷
          (f ≫ ey.inv) ⊗≫
        𝟙 ((ex.hom ≫ f) ≫ ey.inv) := by
      simp only [compIso_inv_expansion]
      dsimp [Conjugation.idIso, Conjugation.homFunctor, Bicategory.leftZigzag]
      bicategory
    _ = _ := by
      rw [ex.left_triangle_hom]
      dsimp [Conjugation.homFunctor]
      bicategory

/-- The hom-form of lax right unity uses the right triangle. -/
theorem rightUnitor_hom
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (f : x ⟶ y) :
    (ρ_ ((Conjugation.homFunctor ex ey).obj f)).hom =
      (Conjugation.homFunctor ex ey).obj f ◁ (Conjugation.idIso ey).inv ≫
        (Conjugation.compIso ex ey ey f (𝟙 y)).inv ≫
          (Conjugation.homFunctor ex ey).map (ρ_ f).hom := by
  symm
  calc
    _ = 𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫ 𝟙 b) ⊗≫
        (ex.hom ≫ f) ◁
          (Bicategory.rightZigzag ey.unit.hom ey.counit.hom) ⊗≫
        𝟙 ((ex.hom ≫ f) ≫ ey.inv) := by
      simp only [compIso_inv_expansion]
      dsimp [Conjugation.idIso, Conjugation.homFunctor, Bicategory.rightZigzag]
      bicategory
    _ = _ := by
      rw [ey.right_triangle_hom]
      dsimp [Conjugation.homFunctor]
      bicategory

/-- Left unity in exactly the inverse-unitor direction required by LaxFunctor. -/
theorem leftUnitor_inv
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (f : x ⟶ y) :
    (Conjugation.homFunctor ex ey).map (λ_ f).inv =
      (λ_ ((Conjugation.homFunctor ex ey).obj f)).inv ≫
        (Conjugation.idIso ex).inv ▷ (Conjugation.homFunctor ex ey).obj f ≫
          (Conjugation.compIso ex ex ey (𝟙 x) f).inv := by
  have hs := congrArg
    (fun k => (λ_ ((Conjugation.homFunctor ex ey).obj f)).inv ≫ k ≫
      (Conjugation.homFunctor ex ey).map (λ_ f).inv)
    (leftUnitor_hom ex ey f)
  have hc :
      (Conjugation.homFunctor ex ey).map (λ_ f).hom ≫
          (Conjugation.homFunctor ex ey).map (λ_ f).inv =
        𝟙 ((Conjugation.homFunctor ex ey).obj (𝟙 x ≫ f)) :=
    ((Conjugation.homFunctor ex ey).mapIso (Bicategory.leftUnitor (B := B) f)).hom_inv_id
  simpa only [Category.assoc, Iso.inv_hom_id_assoc, hc, Category.comp_id] using hs

/-- Right unity in the inverse-unitor direction required by LaxFunctor. -/
theorem rightUnitor_inv
    (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (f : x ⟶ y) :
    (Conjugation.homFunctor ex ey).map (ρ_ f).inv =
      (ρ_ ((Conjugation.homFunctor ex ey).obj f)).inv ≫
        (Conjugation.homFunctor ex ey).obj f ◁ (Conjugation.idIso ey).inv ≫
          (Conjugation.compIso ex ey ey f (𝟙 y)).inv := by
  have hs := congrArg
    (fun k => (ρ_ ((Conjugation.homFunctor ex ey).obj f)).inv ≫ k ≫
      (Conjugation.homFunctor ex ey).map (ρ_ f).inv)
    (rightUnitor_hom ex ey f)
  have hc :
      (Conjugation.homFunctor ex ey).map (ρ_ f).hom ≫
          (Conjugation.homFunctor ex ey).map (ρ_ f).inv =
        𝟙 ((Conjugation.homFunctor ex ey).obj (f ≫ 𝟙 y)) :=
    ((Conjugation.homFunctor ex ey).mapIso (Bicategory.rightUnitor (B := B) f)).hom_inv_id
  simpa only [Category.assoc, Iso.inv_hom_id_assoc, hc, Category.comp_id] using hs

end ConjugationCoherence

/-! ## Native lax and pseudo structures on the same actual-lift data -/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The v5.46 prelax candidate now satisfies all native lax coherence fields.
The lax comparison maps are the inverses of the existing comparison isos. -/
def actualLiftQuasiInverseLax :
    LaxFunctor
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  toPrelaxFunctor := actualLiftQuasiInversePrelax (W := W) A
  mapId X := (actualLiftQuasiInverseMapIdIso (W := W) A X).inv
  mapComp f g := (actualLiftQuasiInverseMapCompIso (W := W) A f g).inv
  mapComp_naturality_left := by
    intro X Y Z f f' eta g
    exact ((ConjugationNaturality.compNatIsoLeft
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) g).hom.naturality eta).symm
  mapComp_naturality_right := by
    intro X Y Z f g g' eta
    exact ((ConjugationNaturality.compNatIsoRight
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Z) f).hom.naturality eta).symm
  map₂_associator := by
    intro X Y Z T f g h
    exact ConjugationCoherence.associator
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Z)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A T) f g h
  map₂_leftUnitor := by
    intro X Y f
    exact ConjugationCoherence.leftUnitor_inv
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y) f
  map₂_rightUnitor := by
    intro X Y f
    exact ConjugationCoherence.rightUnitor_inv
      (actualLiftQuasiInverseObjectEquivalence (W := W) A X)
      (actualLiftQuasiInverseObjectEquivalence (W := W) A Y) f

/-- The original v5.46 isomorphisms, not merely arbitrary IsIso witnesses,
provide the pseudo core of the lax functor. -/
def actualLiftQuasiInversePseudoCore :
    (actualLiftQuasiInverseLax (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).PseudoCore where
  mapIdIso X := actualLiftQuasiInverseMapIdIso (W := W) A X
  mapCompIso f g := actualLiftQuasiInverseMapCompIso (W := W) A f g
  mapIdIso_inv := by intro X; rfl
  mapCompIso_inv := by intro X Y Z f g; rfl

/-- An explicit backwards pseudofunctor for the actual-lift Whitehead data.
Its global pseudonatural roundtrips are a separate subsequent construction. -/
def actualLiftQuasiInversePseudofunctor :
    Pseudofunctor
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.mkOfLax (actualLiftQuasiInverseLax (W := W) A)
    (actualLiftQuasiInversePseudoCore (W := W) A)

@[simp] theorem actualLiftQuasiInversePseudofunctor_toPrelaxFunctor :
    (actualLiftQuasiInversePseudofunctor (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toPrelaxFunctor =
      actualLiftQuasiInversePrelax (W := W) A := rfl

@[simp] theorem actualLiftQuasiInversePseudofunctor_mapId
    (X : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInversePseudofunctor (W := W) A).mapId X =
      actualLiftQuasiInverseMapIdIso (W := W) A X := rfl

@[simp] theorem actualLiftQuasiInversePseudofunctor_mapComp
    {X Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftQuasiInversePseudofunctor (W := W) A).mapComp f g =
      actualLiftQuasiInverseMapCompIso (W := W) A f g := rfl

@[simp] theorem actualLiftQuasiInversePseudofunctor_obj_label
    (X : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((actualLiftQuasiInversePseudofunctor (W := W) A).obj X).label = X.label := rfl

/-! ## Regression checks through the native pseudofunctor interface -/

section Regression
variable {X Y Z T : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
  (W := W) A WorldLabel PresentationLabel}

example (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    G.map₂ (α_ f g h).hom = (G.mapComp (f ≫ g) h).hom ≫
      (G.mapComp f g).hom ▷ G.map h ≫ (α_ (G.map f) (G.map g) (G.map h)).hom ≫
      G.map f ◁ (G.mapComp g h).inv ≫ (G.mapComp f (g ≫ h)).inv :=
  (actualLiftQuasiInversePseudofunctor (W := W) A).map₂_associator f g h

example (f : X ⟶ Y) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    G.map₂ (λ_ f).hom = (G.mapComp (𝟙 X) f).hom ≫
      (G.mapId X).hom ▷ G.map f ≫ (λ_ (G.map f)).hom :=
  (actualLiftQuasiInversePseudofunctor (W := W) A).map₂_left_unitor f

example (f : X ⟶ Y) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    G.map₂ (ρ_ f).hom = (G.mapComp f (𝟙 Y)).hom ≫
      G.map f ◁ (G.mapId Y).hom ≫ (ρ_ (G.map f)).hom :=
  (actualLiftQuasiInversePseudofunctor (W := W) A).map₂_right_unitor f

example (f : X ⟶ Y) :
    ((actualLiftQuasiInversePseudofunctor (W := W) A).map f).actualLift.map.raw =
      ((actualLiftQuasiInversePseudofunctor (W := W) A).map f).raw.map :=
  ((actualLiftQuasiInversePseudofunctor (W := W) A).map f).raw_eq

end Regression

/-!
## Boundary after v5.48

The native backwards Pseudofunctor keeps the exact v5.46 objectwise choices,
prelax map, mapId, and mapComp.  Horizontal naturality comes from v5.47;
associativity comes from exchanging counits, and unity from the triangle laws.
Still separate: global pseudonatural unit/counit and modification-level
roundtrip coherence.  In particular this is not a strict raw-forgetting map.
-/

#print axioms ConjugationCoherence.compIso_inv_expansion
#print axioms ConjugationCoherence.associator
#print axioms ConjugationCoherence.leftUnitor_hom
#print axioms ConjugationCoherence.rightUnitor_hom
#print axioms ConjugationCoherence.leftUnitor_inv
#print axioms ConjugationCoherence.rightUnitor_inv
#print axioms actualLiftQuasiInverseLax
#print axioms actualLiftQuasiInversePseudoCore
#print axioms actualLiftQuasiInversePseudofunctor

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
