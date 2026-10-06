import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
import Mathlib.CategoryTheory.Bicategory.Modification.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55

set_option autoImplicit false

noncomputable section

/-!
# The actual backward triangle invertible modification v5.56

Keep the original F, G, eta, eps and the actual v5.55 vertical paste. Prove
that the old v5.51 contractions are natural for this very paste, with the
four object equivalences independent. No identity transformation is moved
to a replacement family of components or naturality isomorphisms.

The generic calculation removes the outer counit envelope by exchange,
uses the inverse left triangle of the original object equivalence, then
uses its original right triangle. The bicategory tactic only rearranges
structural cells; the substantive exchange, cancellation and triangle laws
are invoked explicitly. Native isoMk supplies inverse naturality and the
two global inverse laws. The integrated certificate and any additional
higher adjoint-biequivalence coherence remain separate obligations.
-/

namespace BackwardTriangleCoherence

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c x y z p q : B}

/-- An arbitrary square passes through an invertible counit envelope.
The identity whiskering is retained, since the bicategory is not strict. -/
theorem cancel_counit_envelope {l : a ⟶ a} (i : l ≅ 𝟙 a)
    {s t : a ⟶ b} (theta : s ⟶ t) :
    i.inv ▷ s ≫ l ◁ theta ≫ i.hom ▷ t = (𝟙 a) ◁ theta := by
  rw [Bicategory.whisker_exchange (B := B) i.hom theta,
    ← Category.assoc, Bicategory.inv_hom_whiskerRight, Category.id_comp]

/-- Read the fixed object's left triangle in the inverse direction. -/
theorem reverse_left_triangle_hom (e : Bicategory.Equivalence a x) :
    Bicategory.rightZigzag e.counit.inv e.unit.inv =
      (ρ_ e.hom).hom ≫ (λ_ e.hom).inv := by
  simpa only [Bicategory.leftZigzagIso_inv, Iso.trans_inv, Iso.symm_inv]
    using congrArg Iso.inv e.left_triangle

/-- The original right triangle identifies the two ways to remove the
forward/inverse pair after the original inverse one-cell. -/
theorem counit_right (e : Bicategory.Equivalence a x) :
    (α_ e.inv e.hom e.inv).inv ≫ e.counit.hom ▷ e.inv ≫ (λ_ e.inv).hom =
      e.inv ◁ e.unit.inv ≫ (ρ_ e.inv).hom := by
  have ht : e.inv ◁ e.unit.hom ≫ (α_ e.inv e.hom e.inv).inv ≫
      e.counit.hom ▷ e.inv = (ρ_ e.inv).hom ≫ (λ_ e.inv).inv := by
    calc
      _ = Bicategory.rightZigzag e.unit.hom e.counit.hom := by
        dsimp [Bicategory.rightZigzag]
        bicategory
      _ = _ := e.right_triangle_hom
  have ht' := congrArg (fun t => e.inv ◁ e.unit.inv ≫ t ≫ (λ_ e.inv).hom) ht
  simpa only [Category.assoc, Bicategory.whiskerLeft_inv_hom_assoc,
    Iso.inv_hom_id, Category.comp_id] using ht'

/-- Expose only the original middle counit in the inverse compositor.
The typed change unfolds the existing private helper without naming it. -/
private theorem compIso_inv_normal (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    (Conjugation.compIso ex ey ez f g).inv =
      𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫ ((ey.hom ≫ g) ≫ ez.inv)) ⊗≫
        (ex.hom ≫ f) ◁ ey.counit.hom ▷ (g ≫ ez.inv) ⊗≫
        𝟙 ((ex.hom ≫ (f ≫ g)) ≫ ez.inv) := by
  change (α_ ((ex.hom ≫ f) ≫ ey.inv) (ey.hom ≫ g) ez.inv).inv ≫
    ((α_ (ex.hom ≫ f) ey.inv (ey.hom ≫ g)).hom ≫
      (ex.hom ≫ f) ◁ (α_ ey.inv ey.hom g).inv ≫
      (ex.hom ≫ f) ◁ (ey.counit.hom ▷ g) ≫
      (ex.hom ≫ f) ◁ (λ_ g).hom) ▷ ez.inv ≫
    (α_ ex.hom f g).hom ▷ ez.inv = _
  bicategory

/-- The forward compositor inserts the inverse of that same counit. -/
private theorem compIso_hom_normal (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (ez : Bicategory.Equivalence c z)
    (f : x ⟶ y) (g : y ⟶ z) :
    (Conjugation.compIso ex ey ez f g).hom =
      𝟙 ((ex.hom ≫ (f ≫ g)) ≫ ez.inv) ⊗≫
        (ex.hom ≫ f) ◁ ey.counit.inv ▷ (g ≫ ez.inv) ⊗≫
        𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫ ((ey.hom ≫ g) ≫ ez.inv)) := by
  change ((α_ ex.hom f g).inv ▷ ez.inv ≫
    ((((ex.hom ≫ f) ◁ (λ_ g).inv ≫
      (ex.hom ≫ f) ◁ (ey.counit.inv ▷ g)) ≫
      (ex.hom ≫ f) ◁ (α_ ey.inv ey.hom g).hom) ≫
      (α_ (ex.hom ≫ f) ey.inv (ey.hom ≫ g)).inv) ▷ ez.inv) ≫
    (α_ ((ex.hom ≫ f) ≫ ey.inv) (ey.hom ≫ g) ez.inv).hom = _
  bicategory

/-- An intermediate diagram used only to factor the proof. Its endpoints
are explicit composites so coherence synthesis sees their full shapes. -/
private def corePaste (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (dy : Bicategory.Equivalence q b)
    (f : x ⟶ y) :
    ((ex.hom ≫ f) ≫ ey.inv) ≫ (dy.inv ≫ ((dy.hom ≫ ey.hom) ≫ ey.inv)) ⟶
      (ex.hom ≫ ex.inv) ≫ ((ex.hom ≫ f) ≫ ey.inv) :=
  𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫ (dy.inv ≫ ((dy.hom ≫ ey.hom) ≫ ey.inv))) ⊗≫
    (((ex.hom ≫ f) ≫ ey.inv) ◁ dy.counit.hom) ▷ (ey.hom ≫ ey.inv) ⊗≫
    (ex.hom ≫ f) ◁ (ey.counit.hom ▷ ey.inv) ⊗≫
    (ex.hom ◁ ex.counit.inv) ▷ (f ≫ ey.inv) ⊗≫
    𝟙 ((ex.hom ≫ ex.inv) ≫ ((ex.hom ≫ f) ≫ ey.inv))

/-- Cancel the original dx counit envelope around the exact original paste.
No relation between dx and ex, or dy and ey, is assumed. -/
private theorem remove_outer_counit (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (dx : Bicategory.Equivalence p a)
    (dy : Bicategory.Equivalence q b) (f : x ⟶ y) :
    (BackwardTriangle.naturalityIso ex ey dx dy f).hom ≫
        (ConjugationTriangle.quasiInverseIso ex dx).hom ▷
          (Conjugation.homFunctor ex ey).obj f =
      corePaste ex ey dy f ≫ ex.unit.inv ▷ ((ex.hom ≫ f) ≫ ey.inv) := by
  calc
    _ = (λ_ (((ex.hom ≫ f) ≫ ey.inv) ≫
          (dy.inv ≫ ((dy.hom ≫ ey.hom) ≫ ey.inv)))).inv ≫
        (dx.counit.inv ▷ (((ex.hom ≫ f) ≫ ey.inv) ≫
            (dy.inv ≫ ((dy.hom ≫ ey.hom) ≫ ey.inv))) ≫
          (dx.inv ≫ dx.hom) ◁ corePaste ex ey dy f ≫
          dx.counit.hom ▷ ((ex.hom ≫ ex.inv) ≫ ((ex.hom ≫ f) ≫ ey.inv))) ≫
        (λ_ ((ex.hom ≫ ex.inv) ≫ ((ex.hom ≫ f) ≫ ey.inv))).hom ≫
        ex.unit.inv ▷ ((ex.hom ≫ f) ≫ ey.inv) := by
      simp only [BackwardTriangle.naturalityIso, BackwardTriangle.counitNaturalityIso,
        Iso.trans_hom, Iso.symm_hom, Bicategory.whiskerLeftIso_hom,
        Bicategory.whiskerRightIso_hom, compIso_inv_normal, compIso_hom_normal]
      dsimp [ConjugationTriangle.quasiInverseIso, ConjugationUnit.naturalityIso,
        ConjugationCounit.naturalityIso, Conjugation.homFunctor,
        CategoryTheory.Functor.mapIso, corePaste]
      bicategory
    _ = _ := by
      rw [cancel_counit_envelope]
      bicategory

/-- The remaining diagram is exactly the old dy contraction, by the two
triangles of the original ex and ey object equivalences. -/
private theorem core_contract (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (dy : Bicategory.Equivalence q b)
    (f : x ⟶ y) :
    corePaste ex ey dy f ≫ ex.unit.inv ▷ ((ex.hom ≫ f) ≫ ey.inv) =
      (Conjugation.homFunctor ex ey).obj f ◁
          (ConjugationTriangle.quasiInverseIso ey dy).hom ≫
        (ρ_ ((Conjugation.homFunctor ex ey).obj f)).hom ≫
        (λ_ ((Conjugation.homFunctor ex ey).obj f)).inv := by
  calc
    _ = 𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫
          (dy.inv ≫ ((dy.hom ≫ ey.hom) ≫ ey.inv))) ⊗≫
        (((ex.hom ≫ f) ≫ ey.inv) ◁ dy.counit.hom) ▷ (ey.hom ≫ ey.inv) ⊗≫
        (ex.hom ≫ f) ◁ (ey.counit.hom ▷ ey.inv) ⊗≫
        (Bicategory.rightZigzag ex.counit.inv ex.unit.inv) ▷ (f ≫ ey.inv) ⊗≫
        𝟙 ((𝟙 a) ≫ ((ex.hom ≫ f) ≫ ey.inv)) := by
      dsimp [corePaste, Bicategory.rightZigzag]
      bicategory
    _ = 𝟙 (((ex.hom ≫ f) ≫ ey.inv) ≫
          (dy.inv ≫ ((dy.hom ≫ ey.hom) ≫ ey.inv))) ⊗≫
        (((ex.hom ≫ f) ≫ ey.inv) ◁ dy.counit.hom) ▷ (ey.hom ≫ ey.inv) ⊗≫
        (ex.hom ≫ f) ◁ ((α_ ey.inv ey.hom ey.inv).inv ≫
          ey.counit.hom ▷ ey.inv ≫ (λ_ ey.inv).hom) ⊗≫
        𝟙 ((𝟙 a) ≫ ((ex.hom ≫ f) ≫ ey.inv)) := by
      rw [reverse_left_triangle_hom]
      bicategory
    _ = _ := by
      rw [counit_right]
      dsimp [ConjugationTriangle.quasiInverseIso, ConjugationUnit.naturalityIso,
        Conjugation.homFunctor]
      bicategory

/-- Modification naturality for the actual v5.55 paste and the unchanged
v5.51 contractions in an arbitrary bicategory. -/
theorem naturality (ex : Bicategory.Equivalence a x)
    (ey : Bicategory.Equivalence b y) (dx : Bicategory.Equivalence p a)
    (dy : Bicategory.Equivalence q b) (f : x ⟶ y) :
    (Conjugation.homFunctor ex ey).obj f ◁ (ConjugationTriangle.quasiInverseIso ey dy).hom ≫
        (ρ_ ((Conjugation.homFunctor ex ey).obj f)).hom ≫
        (λ_ ((Conjugation.homFunctor ex ey).obj f)).inv =
      (BackwardTriangle.naturalityIso ex ey dx dy f).hom ≫
        (ConjugationTriangle.quasiInverseIso ex dx).hom ▷
          (Conjugation.homFunctor ex ey).obj f :=
  ((remove_outer_counit ex ey dx dy f).trans (core_contract ex ey dy f)).symm

end BackwardTriangleCoherence

section GenericRegression

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b x y p q : B}

-- Regression specification: the old contraction must be natural for the
-- actual five-isomorphism paste, with all four equivalences independent.
example (ex : Bicategory.Equivalence a x) (ey : Bicategory.Equivalence b y)
    (dx : Bicategory.Equivalence p a) (dy : Bicategory.Equivalence q b)
    (f : x ⟶ y) :
    (Conjugation.homFunctor ex ey).obj f ◁ (ConjugationTriangle.quasiInverseIso ey dy).hom ≫
        (ρ_ ((Conjugation.homFunctor ex ey).obj f)).hom ≫
        (λ_ ((Conjugation.homFunctor ex ey).obj f)).inv =
      (BackwardTriangle.naturalityIso ex ey dx dy f).hom ≫
        (ConjugationTriangle.quasiInverseIso ex dx).hom ▷
          (Conjugation.homFunctor ex ey).obj f :=
  BackwardTriangleCoherence.naturality ex ey dx dy f

end GenericRegression

/-! ## Native invertible modification on the original actual-lift triangle -/

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Expose exactly the existing native hom category, not a replacement. -/
local instance actualLiftBackwardStrongTransCategory :
    Category (Pseudofunctor.StrongTrans
      (B := ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (C := ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (actualLiftQuasiInversePseudofunctor (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A)) :=
  Pseudofunctor.StrongTrans.homCategory
    (F := actualLiftQuasiInversePseudofunctor (W := W) A)
    (G := actualLiftQuasiInversePseudofunctor (W := W) A)

/-- The old contractions now form a native global invertible modification
of the actual v5.55 triangle, without choosing new components. -/
def actualLiftQuasiInverseTriangleModificationIso :
    (actualLiftQuasiInverseTriangle (W := W) A :
      Pseudofunctor.StrongTrans
        (B := ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)
        (C := ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)
        (actualLiftQuasiInversePseudofunctor (W := W) A)
        (actualLiftQuasiInversePseudofunctor (W := W) A)) ≅
      Pseudofunctor.StrongTrans.id (actualLiftQuasiInversePseudofunctor (W := W) A) :=
  Pseudofunctor.StrongTrans.isoMk
    (η := actualLiftQuasiInverseTriangle (W := W) A)
    (θ := Pseudofunctor.StrongTrans.id (actualLiftQuasiInversePseudofunctor (W := W) A))
    (fun Y => actualLiftQuasiInverseTriangleComponentIso (W := W) A Y)
    (by
      intro Y Z f
      exact BackwardTriangleCoherence.naturality
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)
        (actualLiftQuasiInverseObjectEquivalence (W := W) A Z)
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))
        (actualLiftSourceObjectEquivalence (W := W) A
          ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Z)) f)

@[simp] theorem actualLiftQuasiInverseTriangleModificationIso_hom_app
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleModificationIso (W := W) A).hom.as.app Y =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).hom := rfl

@[simp] theorem actualLiftQuasiInverseTriangleModificationIso_inv_app
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseTriangleModificationIso (W := W) A).inv.as.app Y =
      (actualLiftQuasiInverseTriangleIso (W := W) A Y).inv := rfl

/-! ## Regressions for the actual modification, not just its components -/

example {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} (f : Y ⟶ Z) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriangle (W := W) A
    let c := actualLiftQuasiInverseTriangleModificationIso (W := W) A
    G.map f ◁ c.hom.as.app Z ≫ ((Pseudofunctor.StrongTrans.id G).naturality f).hom =
      (T.naturality f).hom ≫ c.hom.as.app Y ▷ G.map f :=
  (actualLiftQuasiInverseTriangleModificationIso (W := W) A).hom.as.naturality f

example {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel} (f : Y ⟶ Z) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let T := actualLiftQuasiInverseTriangle (W := W) A
    let c := actualLiftQuasiInverseTriangleModificationIso (W := W) A
    G.map f ◁ c.inv.as.app Z ≫ (T.naturality f).hom =
      ((Pseudofunctor.StrongTrans.id G).naturality f).hom ≫ c.inv.as.app Y ▷ G.map f :=
  (actualLiftQuasiInverseTriangleModificationIso (W := W) A).inv.as.naturality f

example :
    let c := actualLiftQuasiInverseTriangleModificationIso (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    c.hom ≫ c.inv = 𝟙 (actualLiftQuasiInverseTriangle (W := W) A) :=
  (actualLiftQuasiInverseTriangleModificationIso (W := W) A).hom_inv_id

example :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let c := actualLiftQuasiInverseTriangleModificationIso (W := W) A
    c.inv ≫ c.hom = 𝟙 (Pseudofunctor.StrongTrans.id G) :=
  (actualLiftQuasiInverseTriangleModificationIso (W := W) A).inv_hom_id

#print axioms BackwardTriangleCoherence.cancel_counit_envelope
#print axioms BackwardTriangleCoherence.reverse_left_triangle_hom
#print axioms BackwardTriangleCoherence.counit_right
#print axioms BackwardTriangleCoherence.compIso_inv_normal
#print axioms BackwardTriangleCoherence.compIso_hom_normal
#print axioms BackwardTriangleCoherence.remove_outer_counit
#print axioms BackwardTriangleCoherence.core_contract
#print axioms BackwardTriangleCoherence.naturality
#print axioms actualLiftBackwardStrongTransCategory
#print axioms actualLiftQuasiInverseTriangleModificationIso
#print axioms actualLiftQuasiInverseTriangleModificationIso_hom_app
#print axioms actualLiftQuasiInverseTriangleModificationIso_inv_app

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
