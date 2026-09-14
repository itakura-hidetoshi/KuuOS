import KUOS.DependentOriginationFlatCompletionV2_72
import KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

namespace KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73

open CategoryTheory
open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]

/-!
# Filtered generated-holonomy bridge v2.73

For one fixed fully generated localization loop, its evaluated automorphism is
viewed as an obstruction value.  No canonical filtration is imposed: the
filtration is explicit input.  Flatness becomes exact identity only after a
separatedness hypothesis at the reflexive automorphism.
-/

/-- A fixed generated loop has flat evaluated holonomy relative to an explicit
filtration on its automorphism carrier. -/
def FilteredGeneratedHolonomyFlat
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    (F : ObstructionFiltration
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (γ : GeneratedLocalizationLoop W p) : Prop :=
  F.Flat (generatedHolonomy W R D γ)

/-- In a filtration separated at the reflexive automorphism, flat generated
holonomy of a fixed loop is exact trivial holonomy. -/
theorem generatedHolonomy_eq_refl_of_filteredFlat
    (W : MorphismProperty Context)
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p : X ⟶ Y}
    (F : ObstructionFiltration
      ((freePathEvaluator W R D).map p ≅
        (freePathEvaluator W R D).map p))
    (γ : GeneratedLocalizationLoop W p)
    (hsep : F.SeparatedAt (Iso.refl _))
    (hflat : FilteredGeneratedHolonomyFlat W R D F γ) :
    generatedHolonomy W R D γ = Iso.refl _ := by
  exact F.flat_eq_of_separatedAt hsep hflat

end KUOS.DependentOriginationFilteredGeneratedHolonomyV2_73
