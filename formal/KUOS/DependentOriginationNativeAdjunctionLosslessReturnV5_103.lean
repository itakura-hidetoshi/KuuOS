import KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102

namespace KUOS.DependentOriginationNativeAdjunctionLosslessReturnV5_103

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.Generic

set_option autoImplicit false
noncomputable section

/-!
# Recover the original chosen equivalences from native mathlib adjunctions (v5.103)

v5.102 constructs the native bicategorical adjunction and mathlib's
bicategory-of-adjunctions morphism out of each *specified* equivalence.

An adjunction alone generally does not determine invertible unit/counit
2-cells. This file therefore makes the missing data explicit: the original
two invertible 2-cells and their precise equality to the adjunction's
unit/counit. From these framed data, mathlib's left triangle reconstructs
the original Bicategory.Equivalence, preserving all choices.

The actual-lift source unit and target counit each round-trip through the
v5.102 native Adj.Hom *without changing the chosen original equivalence*.
This is not an assertion that an arbitrary adjunction is an equivalence,
nor a comparison with an as-yet-unspecified tricategorical adjunction.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B] {a b : B}
variable {f : a ⟶ b} {g : b ⟶ a}

/-- An invertibly framed native mathlib adjunction restores an adjoint
equivalence using the *specified* unit and counit isomorphisms.
No adjointification or replacement counit is needed. -/
def equivalenceOfFramedAdjunction
    (adj : Bicategory.Adjunction f g)
    (η : 𝟙 a ≅ f ≫ g) (ε : g ≫ f ≅ 𝟙 b)
    (hη : η.hom = adj.unit) (hε : ε.hom = adj.counit) :
    Bicategory.Equivalence a b where
  hom := f
  inv := g
  unit := η
  counit := ε
  left_triangle := by
    apply Iso.ext
    change Bicategory.leftZigzag η.hom ε.hom =
      (λ_ f).hom ≫ (ρ_ f).inv
    rw [hη, hε]
    exact adj.left_triangle

/-- Restore from the native one-morphism in mathlib's bicategory Adj B,
rather than from an unrelated choice of adjoint arrows. -/
def equivalenceOfFramedAdjHom
    (h : Bicategory.Adj.Hom a b)
    (η : 𝟙 a ≅ h.l ≫ h.r) (ε : h.r ≫ h.l ≅ 𝟙 b)
    (hη : η.hom = h.adj.unit)
    (hε : ε.hom = h.adj.counit) :
    Bicategory.Equivalence a b :=
  equivalenceOfFramedAdjunction h.adj η ε hη hε

/-- Native-Adj transport together with the original isomorphism frames
returns the exact original equivalence. -/
def originalEquivalenceRoundtrip
    (e : Bicategory.Equivalence a b) :
    Bicategory.Equivalence a b :=
  equivalenceOfFramedAdjHom
    (nativeAdjHomOfEquivalence e)
    e.unit e.counit (by rfl) (by rfl)

/-- The recovery is not merely an isomorphic newly chosen presentation:
the complete original equivalence record is equal. -/
@[simp] theorem originalEquivalenceRoundtrip_eq
    (e : Bicategory.Equivalence a b) :
    originalEquivalenceRoundtrip e = e := by
  cases e
  rfl

@[simp] theorem originalEquivalenceRoundtrip_unit
    (e : Bicategory.Equivalence a b) :
    (originalEquivalenceRoundtrip e).unit = e.unit :=
  congrArg Bicategory.Equivalence.unit (originalEquivalenceRoundtrip_eq e)

@[simp] theorem originalEquivalenceRoundtrip_counit
    (e : Bicategory.Equivalence a b) :
    (originalEquivalenceRoundtrip e).counit = e.counit :=
  congrArg Bicategory.Equivalence.counit (originalEquivalenceRoundtrip_eq e)

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Reconstruct the genuine v5.50 actual-lift source equivalence through
the same v5.102 native adjunct that contains the coherent eta.app X. -/
def actualLiftSourceRecoveredEquivalence
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Equivalence
      X ((actualLiftSourceRoundtrip (W := W) A).obj X) :=
  Generic.equivalenceOfFramedAdjHom
    (actualLiftSourceNativeAdjHom (W := W) A X)
    (actualLiftSourceUnitComponentEquivalence (W := W) A X).unit
    (actualLiftSourceUnitComponentEquivalence (W := W) A X).counit
    (by rfl) (by rfl)

/-- Exactly the original selected v5.50 source equivalence, including
its unit, counit, inverse and both triangle identities. -/
@[simp] theorem actualLiftSourceRecoveredEquivalence_eq
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    actualLiftSourceRecoveredEquivalence (W := W) A X =
      actualLiftSourceUnitComponentEquivalence (W := W) A X :=
  Generic.originalEquivalenceRoundtrip_eq _

/-- Reconstruct the genuine selected target equivalence through the same
v5.102 adjunct that contains the coherent eps.app Y. -/
def actualLiftTargetRecoveredEquivalence
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.Equivalence
      (CanonicalExactUniversalObject (W := W) A
        ((actualLiftQuasiInversePseudofunctor (W := W) A).obj Y))
      Y :=
  Generic.equivalenceOfFramedAdjHom
    (actualLiftTargetNativeAdjHom (W := W) A Y)
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y).unit
    (actualLiftQuasiInverseObjectEquivalence (W := W) A Y).counit
    (by rfl) (by rfl)

/-- Exactly the original selected target equivalence; the inverse
and both invertible comparison 2-cells have not been reselected. -/
@[simp] theorem actualLiftTargetRecoveredEquivalence_eq
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    actualLiftTargetRecoveredEquivalence (W := W) A Y =
      actualLiftQuasiInverseObjectEquivalence (W := W) A Y :=
  Generic.originalEquivalenceRoundtrip_eq _

#print axioms Generic.equivalenceOfFramedAdjunction
#print axioms Generic.equivalenceOfFramedAdjHom
#print axioms Generic.originalEquivalenceRoundtrip
#print axioms Generic.originalEquivalenceRoundtrip_eq
#print axioms actualLiftSourceRecoveredEquivalence
#print axioms actualLiftSourceRecoveredEquivalence_eq
#print axioms actualLiftTargetRecoveredEquivalence
#print axioms actualLiftTargetRecoveredEquivalence_eq

end

end KUOS.DependentOriginationNativeAdjunctionLosslessReturnV5_103
