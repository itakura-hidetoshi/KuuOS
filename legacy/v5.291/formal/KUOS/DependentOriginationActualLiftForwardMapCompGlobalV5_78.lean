import KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77

namespace KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
open KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70
open KUOS.DependentOriginationStrongTransPostcompositionVcompComparisonV5_71.Generic

set_option autoImplicit false

noncomputable section

/-!
# Actual-lift global leading mapComp for forward swallowtail v5.78

v5.77 proves that the final three stages of the v5.68 four-cell paste
form a genuine global modification. The remaining leading stage is not
a fresh 2-cell: it is the non-strict quasi-inverse G's compositor on the
old v5.52 forward-triangle factors.

The v5.52 triangle is literally the original vertical composite of
  alpha = F(eta) : F => (F;G);F
  beta  = eps F : (F;G);F => F.

Apply the proved v5.71 global postcomposition-vcomp comparison with H=G,
then left-whisker its invertible modification by the unchanged unit eta.
The resulting global modification has at X precisely the first v5.68 cell,
  eta_X ◁ G.mapComp (F.map eta_X) (eps_(F X)).

The target is the native postcomposed-factor path, not silently replaced
by the v5.77 right-associated source-post path. The remaining obligation
is the equality/coherence of those two StrongTrans presentations.
Neither v5.70 naturality nor the v5.65 swallowtail equation is claimed.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- All six universe parameters are fixed in the type header. -/
abbrev sourceV578 :=
  ActualLiftSource.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel

abbrev forwardV578 :=
  actualLiftForwardPseudofunctor
    (W := W) A WorldLabel PresentationLabel

abbrev quasiInverseV578 :=
  actualLiftQuasiInversePseudofunctor
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

abbrev unitV578 :=
  actualLiftSourceRoundtripUnit
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

abbrev projectedUnitV578 :=
  actualLiftProjectedSourceUnit
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

abbrev restrictedCounitV578 :=
  actualLiftRestrictedTargetCounit
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

abbrev roundtripV578 :=
  Pseudofunctor.comp
    (forwardV578 (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (quasiInverseV578 (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- Keep the two actual v5.52 factors in their old order before G maps
their composite. -/
def sourceMapCompPathV578 :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id
        (sourceV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))
      (roundtripV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) :=
  Pseudofunctor.StrongTrans.vcomp
    (unitV578 (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (PostcompositionVcomp.postVcomp
      (quasiInverseV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (projectedUnitV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (restrictedCounitV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))

/-- Keep G.map applied separately to the old unit and counit factors. -/
def targetMapCompPathV578 :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id
        (sourceV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))
      (roundtripV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) :=
  Pseudofunctor.StrongTrans.vcomp
    (unitV578 (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (PostcompositionVcomp.vcompPost
      (quasiInverseV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (projectedUnitV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (restrictedCounitV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))

/-- The v5.65 canonical left StrongTrans is definitionally the
original unit followed by the mapped v5.52 pasted triangle. -/
theorem sourceMapCompPathV578_eq_forwardSwallowtailLeft :
    sourceMapCompPathV578
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) =
    actualLiftForwardSwallowtailLeftV70
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) :=
  rfl

local instance sourceHomCategoryV578 :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (sourceV578 (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))
        (roundtripV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := sourceV578 (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (C := sourceV578 (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (F := Pseudofunctor.id _)
    (G := roundtripV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The genuinely global first step in v5.68, obtained by whiskering
the v5.71 invertible modification by eta in the functor bicategory. -/
def forwardMapCompGlobalIso :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (sourceV578 (W := W) A (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)))
        (roundtripV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))
      (Pseudofunctor.StrongTrans.homCategory
        (B := sourceV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        (C := sourceV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))
        (F := Pseudofunctor.id _)
        (G := roundtripV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))
      (sourceMapCompPathV578 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (targetMapCompPathV578 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) :=
  Bicategory.whiskerLeftIso
    (B := Pseudofunctor
      (sourceV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (sourceV578 (W := W) A (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))
    (unitV578 (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (PostcompositionVcomp.comparisonIso
      (quasiInverseV578 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (projectedUnitV578 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (restrictedCounitV578 (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)))

/-- The first v5.68 cell is precisely G.mapComp, left-whiskered by eta_X,
without any extra 2-cell choice. -/
@[simp] theorem forwardMapCompGlobalIso_hom_app
    (X : sourceV578 (W := W) A (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    (forwardMapCompGlobalIso
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X =
    (Bicategory.whiskerLeftIso
      ((unitV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).app X)
      ((quasiInverseV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).mapComp
        ((forwardV578 (W := W) A (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).map
          ((unitV578 (W := W) A
            (WorldLabel := WorldLabel)
            (PresentationLabel := PresentationLabel)).app X))
        ((actualLiftTargetRoundtripCounit
          (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).app
            ((forwardV578 (W := W) A (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel)).obj X)))).hom := by
  simp only [forwardMapCompGlobalIso, Bicategory.whiskerLeftIso_hom,
    Pseudofunctor.StrongTrans.whiskerLeft_as_app,
    PostcompositionVcomp.comparisonIso_hom_app]
  rfl

#print axioms sourceMapCompPathV578_eq_forwardSwallowtailLeft
#print axioms forwardMapCompGlobalIso
#print axioms forwardMapCompGlobalIso_hom_app

end

end KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
