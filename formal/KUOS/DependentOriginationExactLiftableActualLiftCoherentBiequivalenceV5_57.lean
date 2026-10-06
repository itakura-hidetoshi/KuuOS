import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
import KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31

namespace KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31

set_option autoImplicit false

noncomputable section

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

-- Regression: the full certificate belongs to the actual-lift source, not
-- the older localized-classification source, with all universes explicit.
example : WhiteheadTriangleRepresentativeCertificate
    (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel)
    (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :=
  exactLiftableActualLiftCoherentBiequivalenceCertificate (W := W) A

end

end KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57
