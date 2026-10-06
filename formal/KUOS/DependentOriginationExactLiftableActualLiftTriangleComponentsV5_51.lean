import KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50

namespace KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50

set_option autoImplicit false

noncomputable section

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-! Regression specification: both contractions must use the actual unchanged
v5.42/v5.48 pair and its v5.49/v5.50 counit/unit, not unrelated representatives.
This regression-only commit intentionally precedes the new constructions. -/

example (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    let F := (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    let eps := actualLiftTargetRoundtripCounit (W := W) A
    F.map (eta.app X) ≫ eps.app (F.obj X) ≅ 𝟙 (F.obj X) :=
  actualLiftForwardTriangleIso (W := W) A X

example (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel) :
    let G := actualLiftQuasiInversePseudofunctor (W := W) A
    let eta := actualLiftSourceRoundtripUnit (W := W) A
    let eps := actualLiftTargetRoundtripCounit (W := W) A
    eta.app (G.obj Y) ≫ G.map (eps.app Y) ≅ 𝟙 (G.obj Y) :=
  actualLiftQuasiInverseTriangleIso (W := W) A Y

end

end KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51
