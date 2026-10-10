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
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateTriangleModificationsV5_111
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateTriangleModificationsV5_111.Generic
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

Second, mathlib's native `Bicategory.conjugateEquiv` carries the
ORIGINAL normalized left adjunction triangle at each object to the
ORIGINAL normalized right adjunction triangle at that SAME object.
This establishes a concrete, non-strict *mate* comparison between
the left unit/counit modifications and F14's right-mate modifications.
The genuine lax naturality of those right transformations is retained.
Both constructions refer to the same old objectwise adjunctions,
and add no new adjoints,
triangulators, invertibility assumptions, or coherence axioms.

The transported left triangle components are assembled as actual lax
modifications and proved equal to the original right zigzag modifications.
The resulting result is a typed compatibility boundary: it does not
claim a direct equality of cells living in different functor bicategories.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- The normalised ORIGINAL left triangle is sent by mathlib's
genuine conjugate-mate equivalence to the normalised ORIGINAL right
triangle, for the SAME adjunction.  No replacement adjunct is used. -/
theorem normalizedLeftTriangle_conjugate_eq_right
    {a b : B} {l : a ⟶ b} {r : b ⟶ a}
    (adj : Bicategory.Adjunction l r) :
    Bicategory.conjugateEquiv adj adj (normalizedLeftZigzag adj) =
      normalizedRightZigzag adj := by
  simp only [normalizedLeftZigzag_eq_id, normalizedRightZigzag_eq_id,
    Bicategory.conjugateEquiv_id]

variable (D :
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101.Generic.CoherentBiadjunctionDatum B C)

/-! The modification-hom categories carry non-output universe parameters;
pin the exact original source/target hom categories at this generic boundary,
as in v5.64–v5.66.  The functor-bicategory instances alone do not infer
these universe levels from the projection `Iso.hom`. -/
/-! Horizontal pastes themselves live in the ENDO-StrongTrans hom
categories of the non-strict source/target roundtrips.  These are
distinct from the unit/counit hom categories pinned just below. -/
local instance sourceRoundtripStrongTransHomCategory :
    Category
      (Pseudofunctor.StrongTrans (sourceRoundtrip D.datum)
        (sourceRoundtrip D.datum)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := sourceRoundtrip D.datum) (G := sourceRoundtrip D.datum)

local instance targetRoundtripStrongTransHomCategory :
    Category
      (Pseudofunctor.StrongTrans (targetRoundtrip D.datum)
        (targetRoundtrip D.datum)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := C) (C := C)
    (F := targetRoundtrip D.datum) (G := targetRoundtrip D.datum)

local instance sourceSwallowtailHomCategory :
    Category
      (Pseudofunctor.StrongTrans (Pseudofunctor.id B)
        (sourceRoundtrip D.datum)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B) (G := sourceRoundtrip D.datum)

local instance targetSwallowtailHomCategory :
    Category
      (Pseudofunctor.StrongTrans (targetRoundtrip D.datum)
        (Pseudofunctor.id C)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := C) (C := C)
    (F := targetRoundtrip D.datum) (G := Pseudofunctor.id C)

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

/-! Give the same exact hom-category instances at the concrete actual-lift
specialization boundary; local declarations in `Generic` are not inherited. -/
local instance actualSourceSwallowtailHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (sourceRoundtrip
          (actualLiftCoherentBiadjunctionDatum (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).datum)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := Pseudofunctor.id _)
    (G := sourceRoundtrip
      (actualLiftCoherentBiadjunctionDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).datum)

local instance actualTargetSwallowtailHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (targetRoundtrip
          (actualLiftCoherentBiadjunctionDatum (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).datum)
        (Pseudofunctor.id
          (ActualLiftTarget.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (C := ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (F := targetRoundtrip
      (actualLiftCoherentBiadjunctionDatum (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).datum)
    (G := Pseudofunctor.id _)

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
    let triangleMod := actualLiftSourceRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    triangleMod.app X ▷ f ≫ actualLiftSourceUnitRightMate (W := W) A f =
      actualLiftSourceUnitRightMate (W := W) A f ≫
        (actualLiftSourceRoundtrip (W := W) A).map f ◁ triangleMod.app Y := by
  exact (actualLiftSourceRightMateTriangleModification (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).naturality f

/-- The other ORIGINAL right mate satisfies the target-side lax
modification naturality square, retaining the actual R_E map f. -/
theorem actualLiftTargetRightMateTriangle_naturality
    {X Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (f : X ⟶ Y) :
    let triangleMod := actualLiftTargetRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    triangleMod.app X ▷ (actualLiftTargetRoundtrip (W := W) A).map f ≫
        actualLiftTargetCounitRightMate (W := W) A f =
      actualLiftTargetCounitRightMate (W := W) A f ≫
        f ◁ triangleMod.app Y := by
  exact (actualLiftTargetRightMateTriangleModification (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).naturality f

/-- Source: the left triangle 2-cell of the original η_X, under
mathlib's ACTUAL conjugate equivalence, is exactly the right
triangle component of F14's original source right mate. -/
theorem actualLiftSourceTriangle_conjugate_eq_rightMate
    (X : ActualLiftSource.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.conjugateEquiv
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      ((actualLiftSourceUnitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app X) =
    (actualLiftSourceRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app X := by
  exact Generic.normalizedLeftTriangle_conjugate_eq_right
    (actualLiftSourceNativeAdjHom (W := W) A X).adj

/-- Target: the SAME conjugate-mate bridge for the original ε_Y
and its chosen right adjoint; the non-strict R_E is unchanged. -/
theorem actualLiftTargetTriangle_conjugate_eq_rightMate
    (Y : ActualLiftTarget.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    Bicategory.conjugateEquiv
      (actualLiftTargetNativeAdjHom (W := W) A Y).adj
      (actualLiftTargetNativeAdjHom (W := W) A Y).adj
      ((actualLiftTargetCounitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app Y) =
    (actualLiftTargetRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app Y := by
  exact Generic.normalizedLeftTriangle_conjugate_eq_right
    (actualLiftTargetNativeAdjHom (W := W) A Y).adj

/-- The canonical conjugate of EACH original source-unit left triangle
component assembles into a full native lax modification on the
unchanged F14 source right-mate transformation.  The naturality proof
uses the already established original right zigzag modification. -/
def actualLiftSourceConjugatedTriangleModification :
    Oplax.LaxTrans.Modification
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) where
  app X :=
    Bicategory.conjugateEquiv
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      ((actualLiftSourceUnitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app X)
  naturality {_ _} f := by
    simpa only [actualLiftSourceTriangle_conjugate_eq_rightMate] using
      (actualLiftSourceRightMateTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).naturality f

/-- The conjugated ORIGINAL left triangle is EXACTLY the already
constructed right zigzag modification, globally (not just at points). -/
theorem actualLiftSourceConjugatedTriangleModification_eq_original :
    actualLiftSourceConjugatedTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) =
    actualLiftSourceRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  exact actualLiftSourceTriangle_conjugate_eq_rightMate (W := W) A X

/-- The conjugate of each ORIGINAL target-counit left triangle also
assembles into a full native lax modification on the original target
right mate, without promoting its naturality cells to isomorphisms. -/
def actualLiftTargetConjugatedTriangleModification :
    Oplax.LaxTrans.Modification
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) where
  app Y :=
    Bicategory.conjugateEquiv
      (actualLiftTargetNativeAdjHom (W := W) A Y).adj
      (actualLiftTargetNativeAdjHom (W := W) A Y).adj
      ((actualLiftTargetCounitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).app Y)
  naturality {_ _} f := by
    simpa only [actualLiftTargetTriangle_conjugate_eq_rightMate] using
      (actualLiftTargetRightMateTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).naturality f

/-- The conjugated ORIGINAL target triangle equals the full v5.111
right-mate modification; equality includes genuine lax naturality. -/
theorem actualLiftTargetConjugatedTriangleModification_eq_original :
    actualLiftTargetConjugatedTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) =
    actualLiftTargetRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) := by
  apply Oplax.LaxTrans.Modification.ext
  funext Y
  exact actualLiftTargetTriangle_conjugate_eq_rightMate (W := W) A Y

#print axioms Generic.normalizedLeftTriangle_conjugate_eq_right
#print axioms Generic.forwardInterchanger_exchange
#print axioms Generic.reverseInterchanger_exchange
#print axioms actualLiftForwardInterchanger_sourceTriangle_exchange
#print axioms actualLiftReverseInterchanger_targetTriangle_exchange
#print axioms actualLiftSourceRightMateTriangle_naturality
#print axioms actualLiftTargetRightMateTriangle_naturality
#print axioms actualLiftSourceTriangle_conjugate_eq_rightMate
#print axioms actualLiftTargetTriangle_conjugate_eq_rightMate
#print axioms actualLiftSourceConjugatedTriangleModification
#print axioms actualLiftSourceConjugatedTriangleModification_eq_original
#print axioms actualLiftTargetConjugatedTriangleModification
#print axioms actualLiftTargetConjugatedTriangleModification_eq_original

end

end KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112
