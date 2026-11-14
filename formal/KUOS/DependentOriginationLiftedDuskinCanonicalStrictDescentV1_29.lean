import KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29
import KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29

namespace KUOS.DependentOriginationLiftedDuskinCanonicalStrictDescentV1_29

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open scoped Bicategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30
open KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Canonical scaling and strict-inverse sufficient descent

The full thinness of each *lifted* normalized Duskin map is already proved
by the universe-safe v1.29 bridge. It need not be hypothesized anew.

This theorem reaches the original, unlifted fibrancy conclusion under
explicitly typed unlifted-to-lifted presentation equivalences, admissibility
preservation of the lifted maps, and a strict inverse of lifted maps.

The presentation equivalences and the strict inverse remain actual additional
proof obligations. In particular a coherent bicategorical quasi-inverse is
NOT silently replaced by a strict inverse. No unlifted horn is passed directly
to a map on ULift carriers.
-/

/-- Canonical lifted scaled maps, strict inverses, and separately certified
unlifted/lifted horn presentations imply the *original* unlifted conclusion. -/
theorem unliftedFibrancy_iff_of_canonical_strictInverse
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C))
    (E_B : ScaledHornPresentationEquivalence HB₀ HB)
    (E_C : ScaledHornPresentationEquivalence HC₀ HC)
    (hForward :
      ScaledHornFamilyMap
        (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled HB HC)
    (hBackward :
      ScaledHornFamilyMap
        (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled HC HB)
    (hSource : normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G =
      𝟙 (normalizedDuskinSource B C))
    (hTarget : normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F =
      𝟙 (normalizedDuskinTarget B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ := by
  let HF : FullScaledDuskinMapCertificate F :=
    canonicalLiftedFullScaledDuskinMapCertificate F
  let HG : FullScaledDuskinMapCertificate G :=
    canonicalLiftedFullScaledDuskinMapCertificate G
  have hLift :
      HasScaledHornFillers (normalizedDuskinSource B C)
          (normalizedDuskinSourceScaling B C) HB ↔
        HasScaledHornFillers (normalizedDuskinTarget B C)
          (normalizedDuskinTargetScaling B C) HC :=
    liftedFibrancy_iff_of_strictInverse HF HG HB HC
      hForward hBackward hSource hTarget
  exact (hasScaledHornFillers_iff E_B).trans
    (hLift.trans (hasScaledHornFillers_iff E_C).symm)

#print axioms unliftedFibrancy_iff_of_canonical_strictInverse

end KUOS.DependentOriginationLiftedDuskinCanonicalStrictDescentV1_29
