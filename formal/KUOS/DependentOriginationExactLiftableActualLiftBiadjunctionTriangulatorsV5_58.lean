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
StrongTrans values, and both global invertible modifications. This file keeps
all of that data unchanged and exposes the two triangle modifications in
Mathlib's native bicategory of pseudofunctors.

In
`Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo`, pseudofunctors
are objects, StrongTrans values are 1-cells, and modifications are 2-cells.
Thus a triangle StrongTrans together with an isomorphism to the identity
StrongTrans is precisely an invertible 2-cell in that functor bicategory.

This is an interface upgrade only. No swallowtail equation, tricategory,
coherent biadjunction, or new equivalence choice is asserted.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- A triangle 1-endomorphism of a pseudofunctor together with its invertible
2-cell to the identity 1-cell in Mathlib's native functor bicategory. -/
structure FunctorBicategoryTriangulator (F : Pseudofunctor B C) where
  triangle : F ⟶ F
  contraction : triangle ≅ 𝟙 F

namespace FunctorBicategoryTriangulator

variable {F H : Pseudofunctor B C}

/-- Native left whiskering of the triangulator 2-isomorphism. -/
def leftWhiskerIso (T : FunctorBicategoryTriangulator F) (α : H ⟶ F) :
    α ≫ T.triangle ≅ α ≫ 𝟙 F :=
  Bicategory.whiskerLeftIso α T.contraction

/-- Native right whiskering of the triangulator 2-isomorphism. -/
def rightWhiskerIso (T : FunctorBicategoryTriangulator F) (α : F ⟶ H) :
    T.triangle ≫ α ≅ 𝟙 F ≫ α :=
  Bicategory.whiskerRightIso T.contraction α

end FunctorBicategoryTriangulator

/-- The two opposite-direction triangulators. No compatibility law between
them is added at this stage. -/
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
    Pseudofunctor
      (ActualLiftSource (W := W) A)
      (ActualLiftTarget (W := W) A) :=
  (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor

/-- The original v5.52 forward triangle and global modification, now typed
as a native functor-bicategory triangulator. -/
def actualLiftForwardTriangulator :
    FunctorBicategoryTriangulator
      (actualLiftForwardPseudofunctor (W := W) A) where
  triangle := actualLiftForwardTriangle (W := W) A
  contraction := actualLiftForwardTriangleModificationIso (W := W) A

/-- The original v5.55/v5.56 reverse triangle and global modification, with
the non-strict quasi-inverse pseudofunctor unchanged. -/
def actualLiftQuasiInverseTriangulator :
    FunctorBicategoryTriangulator
      (actualLiftQuasiInversePseudofunctor (W := W) A) where
  triangle := actualLiftQuasiInverseTriangle (W := W) A
  contraction := actualLiftQuasiInverseTriangleModificationIso (W := W) A

/-- The two native triangulators in one pair, without adding a swallowtail
or any other higher-coherence law. -/
def actualLiftTriangulatorPair :
    FunctorBicategoryTriangulatorPair
      (actualLiftForwardPseudofunctor (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A) where
  forward := actualLiftForwardTriangulator (W := W) A
  reverse := actualLiftQuasiInverseTriangulator (W := W) A

/-! ## Whole-record projections: the old native data are retained exactly -/

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

/-!
## Boundary after v5.58

The exact v5.52/v5.56 invertible modifications are now available through a
native functor-bicategory interface and can be whiskered by
`FunctorBicategoryTriangulator.leftWhiskerIso` and
`FunctorBicategoryTriangulator.rightWhiskerIso`.

This remains exactly the v5.57 mathematical strength. The next step is to
state the additional higher-coherence law explicitly rather than upgrading
the name of the structure.
-/

#print axioms actualLiftForwardTriangulator
#print axioms actualLiftQuasiInverseTriangulator
#print axioms actualLiftTriangulatorPair
#print axioms actualLiftForwardTriangulator_triangle_eq_certificate
#print axioms actualLiftQuasiInverseTriangulator_triangle_eq_certificate

end

end KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
