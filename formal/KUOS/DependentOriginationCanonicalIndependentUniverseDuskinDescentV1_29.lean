import KUOS.DependentOriginationCanonicalCrossUniverseHornDescentV1_29
import KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29

/-!
# Canonical independent-universe global Duskin horn descent

The genuinely lifted source and target Duskin nerves can have unrelated
universe levels. The canonical family on each lifted nerve is obtained by
transporting the original admissible scaled horn problems through the
fully proved inverse universe comparison (not by assuming an E_B or E_C).

The bicategorical model maps are still required to be strict inverses
on their lifted carriers, and their action on the *chosen admissible
families* must still be certified in both directions. These independent
conditions are not erased by the universe comparison.
-/

namespace KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29
open KUOS.DependentOriginationCanonicalCrossUniverseHornDescentV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-- Precisely the normalized source's admissible horn family obtained
by ULift from the unlifted Duskin source B. -/
def canonicalLiftedDuskinSourceFamily
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (HB₀ : GlobalDuskinScaledHornFamily B) :
    ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C) :=
  canonicalLiftedHornFamily.{max (max w₁ v₁) u₁, max (max w₂ v₂) u₂}
    (duskinScaling B) HB₀

/-- The analogous target family from the original unlifted Duskin target C. -/
def canonicalLiftedDuskinTargetFamily
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (HC₀ : GlobalDuskinScaledHornFamily C) :
    ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C) :=
  canonicalLiftedHornFamily.{max (max w₂ v₂) u₂, max (max w₁ v₁) u₁}
    (duskinScaling C) HC₀

/-- The previously external E_B has an actual canonical construction
at *independent* universe levels for the transported source family. -/
theorem sourceFibrancy_iff_canonicalCrossUniverse
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (HB₀ : GlobalDuskinScaledHornFamily B) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (normalizedDuskinSource B C)
        (normalizedDuskinSourceScaling B C)
        (canonicalLiftedDuskinSourceFamily B C HB₀) :=
  canonicalCrossUniverseFibrancy_iff (duskinScaling B) HB₀

/-- The previously external E_C is likewise canonical at independent
levels for the precisely transported target family. -/
theorem targetFibrancy_iff_canonicalCrossUniverse
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (HC₀ : GlobalDuskinScaledHornFamily C) :
    HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ ↔
      HasScaledHornFillers (normalizedDuskinTarget B C)
        (normalizedDuskinTargetScaling B C)
        (canonicalLiftedDuskinTargetFamily B C HC₀) :=
  canonicalCrossUniverseFibrancy_iff (duskinScaling C) HC₀

/-- Conditional fibrancy equivalence for genuine B and C Duskin nerves
with *independent* universe levels and no assumed E_B or E_C bridges.
The precise model-map strict inverse and admissibility-transport hypotheses
remain unchanged from v1.29. -/
theorem unliftedFibrancy_iff_of_canonical_independentUniverse_strictInverse
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (hForward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀))
    (hBackward : ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
      (canonicalLiftedDuskinTargetFamily B C HC₀)
      (canonicalLiftedDuskinSourceFamily B C HB₀))
    (hSource : normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G =
      𝟙 (normalizedDuskinSource B C))
    (hTarget : normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F =
      𝟙 (normalizedDuskinTarget B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ := by
  have hLift :
      HasScaledHornFillers (normalizedDuskinSource B C)
          (normalizedDuskinSourceScaling B C)
          (canonicalLiftedDuskinSourceFamily B C HB₀) ↔
        HasScaledHornFillers (normalizedDuskinTarget B C)
          (normalizedDuskinTargetScaling B C)
          (canonicalLiftedDuskinTargetFamily B C HC₀) :=
    liftedFibrancy_iff_of_strictInverse
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀)
      hForward hBackward hSource hTarget
  exact (sourceFibrancy_iff_canonicalCrossUniverse B C HB₀).trans
    (hLift.trans (targetFibrancy_iff_canonicalCrossUniverse B C HC₀).symm)

#print axioms sourceFibrancy_iff_canonicalCrossUniverse
#print axioms targetFibrancy_iff_canonicalCrossUniverse
#print axioms unliftedFibrancy_iff_of_canonical_independentUniverse_strictInverse

end KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
