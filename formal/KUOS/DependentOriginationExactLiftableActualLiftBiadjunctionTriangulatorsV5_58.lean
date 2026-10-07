import KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57
import Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Native functor-bicategory triangulators v5.58

v5.57 stores the same actual-lift F, G, eta, eps, both actual triangle
StrongTrans values, and both global invertible modifications.  This file does
not strengthen those laws.  It changes the ambient interface in which the two
triangle modifications are exposed.

Mathlib's
`Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo`
provides a native bicategory whose objects are pseudofunctors, whose 1-cells
are `StrongTrans`, and whose 2-cells are modifications.  Hence each existing
triangle modification is already an invertible 2-cell in a functor bicategory.

The small generic structure below records exactly that fact.  It is designed
as the typed input for a later explicit swallowtail predicate.  In particular,
this file does not claim a tricategory, a coherent biadjunction, a swallowtail
equation, or any new equivalence choice.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- A triangle 1-endomorphism of a pseudofunctor together with an invertible
2-cell contracting it to the identity 1-cell in Mathlib's native bicategory
of pseudofunctors. -/
structure FunctorBicategoryTriangulator (F : Pseudofunctor B C) where
  triangle : F ⟶ F
  contraction : triangle ≅ 𝟙 F

namespace FunctorBicategoryTriangulator

variable {F H : Pseudofunctor B C}

/-- Native left whiskering of a triangulator contraction inside the
functor bicategory.  This is the exact operation needed by later coherence
pastes; no componentwise reconstruction is made. -/
def leftWhiskerIso (T : FunctorBicategoryTriangulator F) (α : H ⟶ F) :
    α ≫ T.triangle ≅ α ≫ 𝟙 F :=
  Bicategory.whiskerLeftIso α T.contraction

/-- Native right whiskering of a triangulator contraction inside the
functor bicategory. -/
def rightWhiskerIso (T : FunctorBicategoryTriangulator F) {H : Pseudofunctor B C}
    (α : F ⟶ H) :
    T.triangle ≫ α ≅ 𝟙 F ≫ α :=
  Bicategory.whiskerRightIso T.contraction α

@[simp] theorem leftWhiskerIso_hom
    (T : FunctorBicategoryTriangulator F) (α : H ⟶ F) :
    (T.leftWhiskerIso α).hom = α ◁ T.contraction.hom :=
  rfl

@[simp] theorem leftWhiskerIso_inv
    (T : FunctorBicategoryTriangulator F) (α : H ⟶ F) :
    (T.leftWhiskerIso α).inv = α ◁ T.contraction.inv :=
  rfl

@[simp] theorem rightWhiskerIso_hom
    (T : FunctorBicategoryTriangulator F) {H : Pseudofunctor B C}
    (α : F ⟶ H) :
    (T.rightWhiskerIso α).hom = T.contraction.hom ▷ α :=
  rfl

@[simp] theorem rightWhiskerIso_inv
    (T : FunctorBicategoryTriangulator F) {H : Pseudofunctor B C}
    (α : F ⟶ H) :
    (T.rightWhiskerIso α).inv = T.contraction.inv ▷ α :=
  rfl

end FunctorBicategoryTriangulator

/-- The two triangulators for opposite-direction pseudofunctors.  This is a
pair of functor-bicategory 2-isomorphisms only; no relation between the two
contractions is postulated here. -/
structure FunctorBicategoryTriangulatorPair
    (F : Pseudofunctor B C) (G : Pseudofunctor C B) where
  forward : FunctorBicategoryTriangulator F
  reverse : FunctorBicategoryTriangulator G

end Generic

open Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
open KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The actual-lift source bicategory. -/
abbrev ActualLiftSource :=
  ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel

/-- The exact-universal target bicategory. -/
abbrev ActualLiftTarget :=
  ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel

/-- The unchanged v5.42 forward pseudofunctor. -/
abbrev actualLiftForwardPseudofunctor :
    Pseudofunctor (ActualLiftSource (W := W) A) (ActualLiftTarget (W := W) A) :=
  (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor

/-- Regression: the pinned Mathlib instance really equips the forward
pseudofunctor type with a bicategory structure. -/
example :
    Bicategory
      (Pseudofunctor
        (ActualLiftSource (W := W) A)
        (ActualLiftTarget (W := W) A)) :=
  inferInstance

/-- Regression: likewise for the reverse pseudofunctor type. -/
example :
    Bicategory
      (Pseudofunctor
        (ActualLiftTarget (W := W) A)
        (ActualLiftSource (W := W) A)) :=
  inferInstance

/-- The original v5.52 forward triangle and modification, re-exposed as a
native 1-endomorphism plus invertible 2-cell in the functor bicategory. -/
def actualLiftForwardTriangulator :
    FunctorBicategoryTriangulator
      (actualLiftForwardPseudofunctor (W := W) A) where
  triangle := actualLiftForwardTriangle (W := W) A
  contraction := actualLiftForwardTriangleModificationIso (W := W) A

/-- The original v5.55/v5.56 reverse triangle and modification, with the
non-strict quasi-inverse pseudofunctor unchanged. -/
def actualLiftQuasiInverseTriangulator :
    FunctorBicategoryTriangulator
      (actualLiftQuasiInversePseudofunctor (W := W) A) where
  triangle := actualLiftQuasiInverseTriangle (W := W) A
  contraction := actualLiftQuasiInverseTriangleModificationIso (W := W) A

/-- Both native triangulators, with no extra higher-coherence assertion. -/
def actualLiftTriangulatorPair :
    FunctorBicategoryTriangulatorPair
      (actualLiftForwardPseudofunctor (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A) where
  forward := actualLiftForwardTriangulator (W := W) A
  reverse := actualLiftQuasiInverseTriangulator (W := W) A

/-! ## Whole-record projections: no replacement data are introduced -/

@[simp] theorem actualLiftForwardTriangulator_triangle :
    (actualLiftForwardTriangulator (W := W) A).triangle =
      actualLiftForwardTriangle (W := W) A :=
  rfl

@[simp] theorem actualLiftForwardTriangulator_contraction :
    (actualLiftForwardTriangulator (W := W) A).contraction =
      actualLiftForwardTriangleModificationIso (W := W) A :=
  rfl

@[simp] theorem actualLiftQuasiInverseTriangulator_triangle :
    (actualLiftQuasiInverseTriangulator (W := W) A).triangle =
      actualLiftQuasiInverseTriangle (W := W) A :=
  rfl

@[simp] theorem actualLiftQuasiInverseTriangulator_contraction :
    (actualLiftQuasiInverseTriangulator (W := W) A).contraction =
      actualLiftQuasiInverseTriangleModificationIso (W := W) A :=
  rfl

@[simp] theorem actualLiftTriangulatorPair_forward :
    (actualLiftTriangulatorPair (W := W) A).forward =
      actualLiftForwardTriangulator (W := W) A :=
  rfl

@[simp] theorem actualLiftTriangulatorPair_reverse :
    (actualLiftTriangulatorPair (W := W) A).reverse =
      actualLiftQuasiInverseTriangulator (W := W) A :=
  rfl

/-! ## Exact compatibility with the integrated v5.57 certificate -/

@[simp] theorem actualLiftForwardTriangulator_triangle_eq_certificate :
    (actualLiftForwardTriangulator (W := W) A).triangle =
      (exactLiftableActualLiftCoherentBiequivalenceCertificate
        (W := W) A).forwardTriangleRepresentative :=
  rfl

@[simp] theorem actualLiftForwardTriangulator_contraction_eq_certificate :
    (actualLiftForwardTriangulator (W := W) A).contraction =
      (exactLiftableActualLiftCoherentBiequivalenceCertificate
        (W := W) A).forwardTriangleModification :=
  rfl

@[simp] theorem actualLiftQuasiInverseTriangulator_triangle_eq_certificate :
    (actualLiftQuasiInverseTriangulator (W := W) A).triangle =
      (exactLiftableActualLiftCoherentBiequivalenceCertificate
        (W := W) A).quasiInverseTriangleRepresentative :=
  rfl

@[simp] theorem actualLiftQuasiInverseTriangulator_contraction_eq_certificate :
    (actualLiftQuasiInverseTriangulator (W := W) A).contraction =
      (exactLiftableActualLiftCoherentBiequivalenceCertificate
        (W := W) A).quasiInverseTriangleModification :=
  rfl

/-! ## Native whiskering regressions

These statements intentionally stay inside each functor bicategory.  They show
that the already-proved global modifications can now enter larger 2-cell
pastes using Mathlib's bicategory operations, which is the required interface
for a later explicit coherence predicate.
-/

section ForwardWhiskering

variable {H :
  Pseudofunctor
    (ActualLiftSource (W := W) A)
    (ActualLiftTarget (W := W) A)}

def actualLiftForwardTriangulator_leftWhiskerIso
    (α : H ⟶ actualLiftForwardPseudofunctor (W := W) A) :
    α ≫ (actualLiftForwardTriangulator (W := W) A).triangle ≅
      α ≫ 𝟙 (actualLiftForwardPseudofunctor (W := W) A) :=
  (actualLiftForwardTriangulator (W := W) A).leftWhiskerIso α

def actualLiftForwardTriangulator_rightWhiskerIso
    (α : actualLiftForwardPseudofunctor (W := W) A ⟶ H) :
    (actualLiftForwardTriangulator (W := W) A).triangle ≫ α ≅
      𝟙 (actualLiftForwardPseudofunctor (W := W) A) ≫ α :=
  (actualLiftForwardTriangulator (W := W) A).rightWhiskerIso α

end ForwardWhiskering

section ReverseWhiskering

variable {H :
  Pseudofunctor
    (ActualLiftTarget (W := W) A)
    (ActualLiftSource (W := W) A)}

def actualLiftQuasiInverseTriangulator_leftWhiskerIso
    (α : H ⟶ actualLiftQuasiInversePseudofunctor (W := W) A) :
    α ≫ (actualLiftQuasiInverseTriangulator (W := W) A).triangle ≅
      α ≫ 𝟙 (actualLiftQuasiInversePseudofunctor (W := W) A) :=
  (actualLiftQuasiInverseTriangulator (W := W) A).leftWhiskerIso α

def actualLiftQuasiInverseTriangulator_rightWhiskerIso
    (α : actualLiftQuasiInversePseudofunctor (W := W) A ⟶ H) :
    (actualLiftQuasiInverseTriangulator (W := W) A).triangle ≫ α ≅
      𝟙 (actualLiftQuasiInversePseudofunctor (W := W) A) ≫ α :=
  (actualLiftQuasiInverseTriangulator (W := W) A).rightWhiskerIso α

end ReverseWhiskering

/-!
## Boundary after v5.58

The v5.52 and v5.56 invertible modifications are now explicitly available as
invertible 2-cells in Mathlib's native bicategories of pseudofunctors, and can
be whiskered there without reconstructing their components.

This is still exactly the v5.57 mathematical strength.  No swallowtail law,
tricategory object, horizontal composition across different functor
bicategories, or coherent biadjoint-biequivalence structure is asserted.
The next formal step is therefore to state the required higher-coherence
pastes explicitly, with all associators, unitors, and pseudofunctor
comparators visible.
-/

#print axioms Generic.FunctorBicategoryTriangulator
#print axioms Generic.FunctorBicategoryTriangulator.leftWhiskerIso
#print axioms Generic.FunctorBicategoryTriangulator.rightWhiskerIso
#print axioms Generic.FunctorBicategoryTriangulatorPair
#print axioms actualLiftForwardTriangulator
#print axioms actualLiftQuasiInverseTriangulator
#print axioms actualLiftTriangulatorPair
#print axioms actualLiftForwardTriangulator_triangle_eq_certificate
#print axioms actualLiftForwardTriangulator_contraction_eq_certificate
#print axioms actualLiftQuasiInverseTriangulator_triangle_eq_certificate
#print axioms actualLiftQuasiInverseTriangulator_contraction_eq_certificate
#print axioms actualLiftForwardTriangulator_leftWhiskerIso
#print axioms actualLiftForwardTriangulator_rightWhiskerIso
#print axioms actualLiftQuasiInverseTriangulator_leftWhiskerIso
#print axioms actualLiftQuasiInverseTriangulator_rightWhiskerIso

end

end KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
