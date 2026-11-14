import KUOS.DependentOriginationCanonicalIndependentUniverseNativeQuasiInverseDescentV1_29
import KUOS.DependentOriginationArbitraryFamilyNativeCorrespondenceV1_29

/-!
# Indexed admissibility: genuinely constructed B/C family-map certificates

An index-selected family tests only the horn dimension n and vertex i.
Its admissibility is independent of the chosen horn map and of universe
lifting. A matching index condition on B/C therefore constructs BOTH
lifted admissibility-preserving family maps, without any unproved
identification between unlifted and lifted simplicial carriers.

The resulting fibrancy statement still requires a native normalized
coherent quasi-inverse and genuine homotopy-to-strict rectification.
It is not unconditional Duskin fibrancy or the full scaled-anodyne family.
-/

namespace KUOS.DependentOriginationIndexedDuskinAdmissibilityV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseDuskinDescentV1_29
open KUOS.DependentOriginationCanonicalIndependentUniverseNativeQuasiInverseDescentV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33

universe u u₁ u₂ v₁ v₂ w₁ w₂

/-- A genuine scaled horn family whose admissibility is an indexed
predicate. The horn map and the thinness certificates are retained. -/
def indexedScaledHornFamily
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (allowed : ∀ n : Nat, Fin (n + 1) → Prop) :
    ScaledHornFamily X sX where
  admissible := fun {n} {i} _ => allowed n i

/-- Canonical independent-universe lifting of an indexed source family
preserves the exact admissibility predicate. -/
theorem indexedSource_admissible_iff
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (allowed : ∀ n : Nat, Fin (n + 1) → Prop)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i) :
    (canonicalLiftedDuskinSourceFamily B C
      (indexedScaledHornFamily (duskinScaling B) allowed)).admissible P ↔
        allowed n i :=
  Iff.rfl

/-- Canonical lifting likewise preserves the actual target indexed predicate. -/
theorem indexedTarget_admissible_iff
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (allowed : ∀ n : Nat, Fin (n + 1) → Prop)
    {n : Nat} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i) :
    (canonicalLiftedDuskinTargetFamily B C
      (indexedScaledHornFamily (duskinScaling C) allowed)).admissible Q ↔
        allowed n i :=
  Iff.rfl

/-- Index-preserving transport directly constructs the canonical forward
family map. This is not an assumption that any arbitrary horn family maps. -/
def indexedSourceToTargetFamilyMap
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (AB AC : ∀ n : Nat, Fin (n + 1) → Prop)
    (h : ∀ (n : Nat) (i : Fin (n + 1)), AB n i → AC n i) :
    ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate F).map_scaled
      (canonicalLiftedDuskinSourceFamily B C
        (indexedScaledHornFamily (duskinScaling B) AB))
      (canonicalLiftedDuskinTargetFamily B C
        (indexedScaledHornFamily (duskinScaling C) AC)) := by
  refine ⟨?_⟩
  intro n i P hP
  change AB n i at hP
  change AC n i
  exact h n i hP

/-- The independent reverse family-map certificate uses the SAME two
normalized lifted carriers in reverse. No strict inverse is needed. -/
def indexedTargetToSourceFamilyMap
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (AB AC : ∀ n : Nat, Fin (n + 1) → Prop)
    (h : ∀ (n : Nat) (i : Fin (n + 1)), AC n i → AB n i) :
    ScaledHornFamilyMap
      (canonicalLiftedFullScaledDuskinMapCertificate G).map_scaled
      (canonicalLiftedDuskinTargetFamily B C
        (indexedScaledHornFamily (duskinScaling C) AC))
      (canonicalLiftedDuskinSourceFamily B C
        (indexedScaledHornFamily (duskinScaling B) AB)) := by
  refine ⟨?_⟩
  intro n i Q hQ
  change AC n i at hQ
  change AB n i
  exact h n i hQ

/-- A matched pair of index-selected, ORIGINAL unlifted horn families
has equivalent fibrancy under native coherent quasi-inverse and genuine
homotopy rectification. BOTH family-map conditions are now CONSTRUCTED,
not extra hypotheses. The comparison of index predicates remains explicit. -/
theorem unliftedFibrancy_iff_of_matching_indexed_families
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (AB AC : ∀ n : Nat, Fin (n + 1) → Prop)
    (hIndex : ∀ (n : Nat) (i : Fin (n + 1)), AB n i ↔ AC n i)
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B)
      (indexedScaledHornFamily (duskinScaling B) AB) ↔
    HasScaledHornFillers (duskinNerve C) (duskinScaling C)
      (indexedScaledHornFamily (duskinScaling C) AC) :=
  unliftedFibrancy_iff_of_canonical_nativeQuasiInverse
    B C F G
    (indexedScaledHornFamily (duskinScaling B) AB)
    (indexedScaledHornFamily (duskinScaling C) AC)
    (indexedSourceToTargetFamilyMap B C F AB AC
      (fun n i => (hIndex n i).mp))
    (indexedTargetToSourceFamilyMap B C G AB AC
      (fun n i => (hIndex n i).mpr))
    K RB RC

/-- In particular, the actual inner-horn index condition is matched on
the two original Duskin nerves. This does not replace rectification by
an unsupported all-bicategories claim. -/
def allInnerScaledHornFamily
    {X : SSet.{u}} (sX : ScaledSimplicialSet X) :
    ScaledHornFamily X sX :=
  indexedScaledHornFamily sX (fun n i => 0 < i ∧ i < Fin.last n)

/-- Concrete original inner-horn fibrancy equivalence: no family-map or
chosen-admissibility compatibility hypotheses are left, but the actual
native coherent quasi-inverse and strict-filler rectification remain. -/
theorem unliftedInnerHornFibrancy_iff_of_nativeQuasiInverse
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ScaledHornHomotopyRectification
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ScaledHornHomotopyRectification
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B)
      (allInnerScaledHornFamily (duskinScaling B)) ↔
    HasScaledHornFillers (duskinNerve C) (duskinScaling C)
      (allInnerScaledHornFamily (duskinScaling C)) :=
  unliftedFibrancy_iff_of_matching_indexed_families
    B C F G
    (fun n i => 0 < i ∧ i < Fin.last n)
    (fun n i => 0 < i ∧ i < Fin.last n)
    (fun n i => Iff.rfl) K RB RC

#print axioms indexedScaledHornFamily
#print axioms indexedSource_admissible_iff
#print axioms indexedTarget_admissible_iff
#print axioms indexedSourceToTargetFamilyMap
#print axioms indexedTargetToSourceFamilyMap
#print axioms unliftedFibrancy_iff_of_matching_indexed_families
#print axioms allInnerScaledHornFamily
#print axioms unliftedInnerHornFibrancy_iff_of_nativeQuasiInverse

end KUOS.DependentOriginationIndexedDuskinAdmissibilityV1_29
