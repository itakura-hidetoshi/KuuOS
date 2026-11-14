import KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
import KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29

/-!
# Typed independent-universe Duskin fibrancy descent via family correspondence

The fixed v1.29 family correspondence is weaker than requiring strict
inverses of the normalized Duskin maps: it certifies the actual
admissibility and filler-existence reflection on the lifted horn problems.
The canonical cross-universe E_B/E_C bridges were constructed previously.
Here we compose them without *assuming* two independent presentation
equivalences or replacing a coherent bicategorical inverse by a strict one.

No unconditional global fibrancy theorem is claimed: the family
correspondence is a genuine extra hypothesis, whose existence must be
proved for a specific chosen family and model maps.
-/

namespace KUOS.DependentOriginationCanonicalIndependentUniverseFamilyCorrespondenceV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-- Canonical unlifted Duskin fibrancy descent for independent universe
levels, assuming precisely the lifted family-level correspondence.
No strict inverse equation is needed; its role is replaced by the
existing *explicit* admissibility and round-trip filler-reflection data. -/
theorem unliftedFibrancy_iff_of_canonical_independentUniverse_correspondence
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    (D : LiftedDuskinFamilyCorrespondence
      (canonicalLiftedFullScaledDuskinMapCertificate F)
      (canonicalLiftedFullScaledDuskinMapCertificate G)
      (canonicalLiftedDuskinSourceFamily B C HB₀)
      (canonicalLiftedDuskinTargetFamily B C HC₀)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ := by
  have hLift :
      HasScaledHornFillers (normalizedDuskinSource B C)
          (normalizedDuskinSourceScaling B C)
          (canonicalLiftedDuskinSourceFamily B C HB₀) ↔
        HasScaledHornFillers (normalizedDuskinTarget B C)
          (normalizedDuskinTargetScaling B C)
          (canonicalLiftedDuskinTargetFamily B C HC₀) :=
    liftedFibrancy_iff D
  exact (sourceFibrancy_iff_canonicalCrossUniverse B C HB₀).trans
    (hLift.trans (targetFibrancy_iff_canonicalCrossUniverse B C HC₀).symm)

#print axioms unliftedFibrancy_iff_of_canonical_independentUniverse_correspondence

end KUOS.DependentOriginationCanonicalIndependentUniverseFamilyCorrespondenceV1_29
