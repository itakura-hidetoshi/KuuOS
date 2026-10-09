import KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
import Mathlib.CategoryTheory.Bicategory.Adjunction.Adj

namespace KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101

set_option autoImplicit false
noncomputable section

/-!
# Native mathlib bicategorical adjunction boundary (v5.102)

The KuuOS v5.101 coherent biadjunction carrier relates *pseudofunctors*
through two original swallowtail modifications. It is not definitionally
a single mathlib `Bicategory.Adjunction` between 1-morphisms.

This file establishes the precise interface that is already available:
every chosen KuuOS adjoint equivalence gives a mathlib
`Bicategory.Adjunction`, and hence an actual 1-morphism of mathlib's
bicategory `Bicategory.Adj`.

We then specialize this construction to the original source-unit and
target-counit object equivalences of the v5.101 actual-lift datum.
The resulting left adjoints are exactly eta.app and eps.app of that
same coherent carrier. Their native units, counits, and both triangle
identities are inherited from the *original chosen equivalences*.

No new choice, strictification, axiom, or assertion of a universal
tricategorical equivalence is introduced.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B] {a b : B}

/-- The original 2-isomorphism unit and counit of an adjoint equivalence
satisfy precisely mathlib's native bicategorical adjunction axioms. -/
def nativeAdjunctionOfEquivalence (e : Bicategory.Equivalence a b) :
    Bicategory.Adjunction e.hom e.inv where
  unit := e.unit.hom
  counit := e.counit.hom
  left_triangle := e.left_triangle_hom
  right_triangle := e.right_triangle_hom

@[simp] theorem nativeAdjunctionOfEquivalence_unit
    (e : Bicategory.Equivalence a b) :
    (nativeAdjunctionOfEquivalence e).unit = e.unit.hom := rfl

@[simp] theorem nativeAdjunctionOfEquivalence_counit
    (e : Bicategory.Equivalence a b) :
    (nativeAdjunctionOfEquivalence e).counit = e.counit.hom := rfl

/-- The same data as an original morphism of mathlib's bicategory
of adjunctions, with neither leg re-selected. -/
def nativeAdjHomOfEquivalence (e : Bicategory.Equivalence a b) :
    Bicategory.Adj.Hom a b where
  adj := nativeAdjunctionOfEquivalence e

@[simp] theorem nativeAdjHomOfEquivalence_left
    (e : Bicategory.Equivalence a b) :
    (nativeAdjHomOfEquivalence e).l = e.hom := rfl

@[simp] theorem nativeAdjHomOfEquivalence_right
    (e : Bicategory.Equivalence a b) :
    (nativeAdjHomOfEquivalence e).r = e.inv := rfl

@[simp] theorem nativeAdjHomOfEquivalence_adj_unit
    (e : Bicategory.Equivalence a b) :
    (nativeAdjHomOfEquivalence e).adj.unit = e.unit.hom := rfl

@[simp] theorem nativeAdjHomOfEquivalence_adj_counit
    (e : Bicategory.Equivalence a b) :
    (nativeAdjHomOfEquivalence e).adj.counit = e.counit.hom := rfl

end Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The *unchanged source unit component* is the left leg of a real
mathlib bicategorical adjunction from X to F(G(X)). The right leg and
triangle 2-cells are those of the original v5.50 equivalence. -/
def actualLiftSourceNativeAdjHom
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Adj.Hom X
      ((actualLiftSourceRoundtrip (W := W) A).obj X) :=
  Generic.nativeAdjHomOfEquivalence
    (actualLiftSourceUnitComponentEquivalence (W := W) A X)

/-- The *unchanged target counit component* is the left leg of a real
mathlib bicategorical adjunction from F(G(Y)) to Y, using the original
chosen equivalence eY. -/
def actualLiftTargetNativeAdjHom
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Adj.Hom
      (CanonicalExactUniversalObject (W := W) A
        ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))
      Y :=
  Generic.nativeAdjHomOfEquivalence
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y)

/-- No substitute left adjoint: the native source leg is eta_X itself. -/
@[simp] theorem actualLiftSourceNativeAdjHom_left_eq_unit_app
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftSourceNativeAdjHom (W := W) A X).l =
      (actualLiftSourceRoundtripUnit (W := W) A).app X := rfl

/-- No substitute left adjoint: the native target leg is eps_Y itself. -/
@[simp] theorem actualLiftTargetNativeAdjHom_left_eq_counit_app
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftTargetNativeAdjHom (W := W) A Y).l =
      (actualLiftTargetRoundtripCounit (W := W) A).app Y := rfl

/-- The source adjunction is attached to the very same unit stored
in the v5.101 coherent datum, not a newly constructed unit. -/
theorem actualLiftSourceNativeAdjHom_left_eq_coherent_unit
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftSourceNativeAdjHom (W := W) A X).l =
      ((actualLiftCoherentBiadjunctionDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).datum.base.unit).app X := rfl

/-- The target adjunction is attached to the very same counit stored
in the v5.101 coherent datum. -/
theorem actualLiftTargetNativeAdjHom_left_eq_coherent_counit
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftTargetNativeAdjHom (W := W) A Y).l =
      ((actualLiftCoherentBiadjunctionDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).datum.base.counit).app Y := rfl

/-- Native mathlib left and right triangle identities are present for
each original source-unit component. -/
theorem actualLiftSourceNativeAdjHom_triangles
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.leftZigzag
        (actualLiftSourceNativeAdjHom (W := W) A X).adj.unit
        (actualLiftSourceNativeAdjHom (W := W) A X).adj.counit =
      (λ_ (actualLiftSourceNativeAdjHom (W := W) A X).l).hom ≫
        (ρ_ (actualLiftSourceNativeAdjHom (W := W) A X).l).inv ∧
    Bicategory.rightZigzag
        (actualLiftSourceNativeAdjHom (W := W) A X).adj.unit
        (actualLiftSourceNativeAdjHom (W := W) A X).adj.counit =
      (ρ_ (actualLiftSourceNativeAdjHom (W := W) A X).r).hom ≫
        (λ_ (actualLiftSourceNativeAdjHom (W := W) A X).r).inv :=
  ⟨(actualLiftSourceNativeAdjHom (W := W) A X).adj.left_triangle,
   (actualLiftSourceNativeAdjHom (W := W) A X).adj.right_triangle⟩

/-- The same two native mathlib triangle identities hold at the
original target counit component. -/
theorem actualLiftTargetNativeAdjHom_triangles
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.leftZigzag
        (actualLiftTargetNativeAdjHom (W := W) A Y).adj.unit
        (actualLiftTargetNativeAdjHom (W := W) A Y).adj.counit =
      (λ_ (actualLiftTargetNativeAdjHom (W := W) A Y).l).hom ≫
        (ρ_ (actualLiftTargetNativeAdjHom (W := W) A Y).l).inv ∧
    Bicategory.rightZigzag
        (actualLiftTargetNativeAdjHom (W := W) A Y).adj.unit
        (actualLiftTargetNativeAdjHom (W := W) A Y).adj.counit =
      (ρ_ (actualLiftTargetNativeAdjHom (W := W) A Y).r).hom ≫
        (λ_ (actualLiftTargetNativeAdjHom (W := W) A Y).r).inv :=
  ⟨(actualLiftTargetNativeAdjHom (W := W) A Y).adj.left_triangle,
   (actualLiftTargetNativeAdjHom (W := W) A Y).adj.right_triangle⟩

#print axioms Generic.nativeAdjunctionOfEquivalence
#print axioms Generic.nativeAdjHomOfEquivalence
#print axioms actualLiftSourceNativeAdjHom
#print axioms actualLiftTargetNativeAdjHom
#print axioms actualLiftSourceNativeAdjHom_left_eq_coherent_unit
#print axioms actualLiftTargetNativeAdjHom_left_eq_coherent_counit
#print axioms actualLiftSourceNativeAdjHom_triangles
#print axioms actualLiftTargetNativeAdjHom_triangles

end

end KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
