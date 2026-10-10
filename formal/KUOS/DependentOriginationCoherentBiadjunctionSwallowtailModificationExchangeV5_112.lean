import KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateTriangleModificationsV5_111
import KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
import Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo

namespace KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateTriangleModificationsV5_111
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
noncomputable section

/-!
# F15 continuation / v5.112: the original swallowtails respect local adjunction triangles

The original (non-strict) forward and reverse F/G triangulator pastes
live as 2-cells of the bicategory of pseudofunctors/strong transformations.
F14's right mates instead live in the (distinct) bicategory of oplax
functors/lax transformations.  These cells must not be conflated.

First, the already proved *original* F3/F4 swallowtail equalities
identify the canonical interchangers with left/right whiskerings of the
original global triangulator pastes.  Mathlib's bicategorical
`whisker_exchange` then shows these ORIGINAL interchangers commute with
**any** modification of the original unit/counit, including the
non-strict normalized left zigzag modifications of v5.111.

Second, expose the unchanged F14 right mates' global naturality with
the v5.111 normalized RIGHT zigzag modifications.  Both constructions
refer to the same old objectwise adjunctions, and add no new adjoints,
triangulators, invertibility assumptions, or coherence axioms.

The resulting result is a typed compatibility boundary: it does not
claim a direct equality of cells living in different functor bicategories.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

variable (D :
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101.Generic.CoherentBiadjunctionDatum B C)

/-- The original forward interchanger commutes with an ARBITRARY
unit modification.  The proof uses the *certified* forward swallowtail
rather than replacing the independently constructed interchanger by
a new choice.  All non-strict mapId/mapComp cells remain in the paste. -/
theorem forwardInterchanger_exchange
    (Γ : Pseudofunctor.StrongTrans.Modification
      D.datum.base.unit D.datum.base.unit) :
    D.forwardInterchanger.hom ≫
      (Pseudofunctor.StrongTrans.Hom.of Γ) ▷
        (sourceReverseTriangulator D.datum).triangle =
      (Pseudofunctor.StrongTrans.Hom.of Γ) ▷
        (sourceForwardTriangulator D.datum).triangle ≫
          D.forwardInterchanger.hom := by
  have hSwallowtail :
      D.forwardInterchanger = forwardTriangulatorPaste D.datum :=
    D.forward_swallowtail
  rw [hSwallowtail]
  exact Bicategory.whisker_exchange
    (Pseudofunctor.StrongTrans.Hom.of Γ)
    (sourceHorizontalPaste D.datum).hom

/-- Reverse (target counit) version.  It is the OTHER orientation of
the same bicategorical exchange law, applied to the original target
horizontal paste and an arbitrary modification of the counit. -/
theorem reverseInterchanger_exchange
    (Γ : Pseudofunctor.StrongTrans.Modification
      D.datum.base.counit D.datum.base.counit) :
    (targetForwardTriangulator D.datum).triangle ◁
        (Pseudofunctor.StrongTrans.Hom.of Γ) ≫
          D.reverseInterchanger.hom =
      D.reverseInterchanger.hom ≫
        (targetReverseTriangulator D.datum).triangle ◁
          (Pseudofunctor.StrongTrans.Hom.of Γ) := by
  have hSwallowtail :
      D.reverseInterchanger = reverseTriangulatorPaste D.datum :=
    D.reverse_swallowtail
  rw [hSwallowtail]
  exact Bicategory.whisker_exchange
    (targetHorizontalPaste D.datum).hom
    (Pseudofunctor.StrongTrans.Hom.of Γ)

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Specialize the GLOBAL forward swallowtail exchange to the normalized
left triangle modification from the ACTUAL source-unit adjunctions.
The right-hand sides are the original F/G triangulators, not redefined
cell families or strictified functors. -/
theorem actualLiftForwardInterchanger_sourceTriangle_exchange :
    let D := actualLiftCoherentBiadjunctionDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let Γ := Pseudofunctor.StrongTrans.Hom.of
      (actualLiftSourceUnitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    D.forwardInterchanger.hom ≫
        Γ ▷ (sourceReverseTriangulator D.datum).triangle =
      Γ ▷ (sourceForwardTriangulator D.datum).triangle ≫
        D.forwardInterchanger.hom := by
  exact Generic.forwardInterchanger_exchange
    (actualLiftCoherentBiadjunctionDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftSourceUnitLeftTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

/-- Specialize the GLOBAL reverse swallowtail exchange to the genuine
target-counit's normalized left triangle modification. -/
theorem actualLiftReverseInterchanger_targetTriangle_exchange :
    let D := actualLiftCoherentBiadjunctionDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    let Γ := Pseudofunctor.StrongTrans.Hom.of
      (actualLiftTargetCounitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (targetForwardTriangulator D.datum).triangle ◁ Γ ≫
        D.reverseInterchanger.hom =
      D.reverseInterchanger.hom ≫
        (targetReverseTriangulator D.datum).triangle ◁ Γ := by
  exact Generic.reverseInterchanger_exchange
    (actualLiftCoherentBiadjunctionDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (actualLiftTargetCounitLeftTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

/-- The matching ORIGINAL source right-mate triangle modification also
satisfies its genuine lax naturality square, for every 1-morphism. -/
theorem actualLiftSourceRightMateTriangle_naturality
    {X Y : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    let Δ := actualLiftSourceRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    Δ.app X ▷ f ≫ actualLiftSourceUnitRightMate (W := W) A f =
      actualLiftSourceUnitRightMate (W := W) A f ≫
        (actualLiftSourceRoundtrip (W := W) A).map f ◁ Δ.app Y := by
  exact (actualLiftSourceRightMateTriangleModification (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).naturality f

/-- The other ORIGINAL right mate satisfies the target-side lax
modification naturality square, retaining the actual R_E map f. -/
theorem actualLiftTargetRightMateTriangle_naturality
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    let Δ := actualLiftTargetRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    Δ.app X ▷ (actualLiftTargetRoundtrip (W := W) A).map f ≫
        actualLiftTargetCounitRightMate (W := W) A f =
      actualLiftTargetCounitRightMate (W := W) A f ≫
        f ◁ Δ.app Y := by
  exact (actualLiftTargetRightMateTriangleModification (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).naturality f

#print axioms Generic.forwardInterchanger_exchange
#print axioms Generic.reverseInterchanger_exchange
#print axioms actualLiftForwardInterchanger_sourceTriangle_exchange
#print axioms actualLiftReverseInterchanger_targetTriangle_exchange
#print axioms actualLiftSourceRightMateTriangle_naturality
#print axioms actualLiftTargetRightMateTriangle_naturality

end

end KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112
