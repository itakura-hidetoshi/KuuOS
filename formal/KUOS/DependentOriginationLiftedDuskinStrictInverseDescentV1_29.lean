import KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29

namespace KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationLiftedDuskinRoundTripBridgeV1_29
open KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Strict-inverse sufficient condition for genuinely lifted horn descent

The round-trip reflection hypotheses of the lifted correspondence are real
obligations. Here they follow from a *stronger, explicit* condition: the
two normalized maps are strict inverses on their ULift SSet carriers.
This does not assert that bicategorical quasi-inverses are strict, and
does not identify unlifted and lifted admissible horn families.
-/

/-- Pushing a horn problem along the identity does not alter the problem. -/
theorem mapScaledHornProblem_id
    {X : SSet} {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    mapScaledHornProblem (isScaledMap_id sX) P = P := by
  cases P
  simp [mapScaledHornProblem]

/-- Transport depends on the underlying simplicial morphism, not its scaled-map proof. -/
theorem mapScaledHornProblem_congr
    {X Y : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f g : X ⟶ Y}
    (hf : IsScaledMap sX sY f)
    (hg : IsScaledMap sX sY g)
    (h : f = g)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    mapScaledHornProblem hf P = mapScaledHornProblem hg P := by
  cases h
  rfl

/-- A genuinely strict left inverse reflects existence of fillers on each horn. -/
theorem roundTrip_filler_iff_of_leftInverse
    {X Y : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y} {g : Y ⟶ X}
    (hf : IsScaledMap sX sY f)
    (hg : IsScaledMap sY sX g)
    (hfg : f ≫ g = 𝟙 X)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    Nonempty (ScaledHornFiller
        (mapScaledHornProblem hg (mapScaledHornProblem hf P))) ↔
      Nonempty (ScaledHornFiller P) := by
  have hround :
      mapScaledHornProblem hg (mapScaledHornProblem hf P) = P :=
    (mapScaledHornProblem_comp hf hg P).trans
      ((mapScaledHornProblem_congr (hf.comp hg)
        (isScaledMap_id sX) hfg P).trans
        (mapScaledHornProblem_id P))
  rw [hround]

/--
On the normalized ULift carriers, a strict inverse gives the two filler
reflection clauses needed for a lifted family correspondence.
-/
def liftedFamilyCorrespondence_of_strictInverse
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    (HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C))
    (hForward : ScaledHornFamilyMap HF.map_scaled HB HC)
    (hBackward : ScaledHornFamilyMap HG.map_scaled HC HB)
    (hSource : normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G =
      𝟙 (normalizedDuskinSource B C))
    (hTarget : normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F =
      𝟙 (normalizedDuskinTarget B C)) :
    LiftedDuskinFamilyCorrespondence HF HG HB HC where
  forward_admissible := hForward.admissible_preserved
  backward_admissible := hBackward.admissible_preserved
  source_roundTrip_filler_reflect := by
    intro n i P
    exact roundTrip_filler_iff_of_leftInverse
      HF.map_scaled HG.map_scaled hSource P
  target_roundTrip_filler_reflect := by
    intro n i Q
    exact roundTrip_filler_iff_of_leftInverse
      HG.map_scaled HF.map_scaled hTarget Q

/-- Strict inverse maps and admissibility preservation imply lifted fibrancy equivalence. -/
theorem liftedFibrancy_iff_of_strictInverse
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    (HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C))
    (hForward : ScaledHornFamilyMap HF.map_scaled HB HC)
    (hBackward : ScaledHornFamilyMap HG.map_scaled HC HB)
    (hSource : normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G =
      𝟙 (normalizedDuskinSource B C))
    (hTarget : normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F =
      𝟙 (normalizedDuskinTarget B C)) :
    HasScaledHornFillers (normalizedDuskinSource B C)
        (normalizedDuskinSourceScaling B C) HB ↔
      HasScaledHornFillers (normalizedDuskinTarget B C)
        (normalizedDuskinTargetScaling B C) HC :=
  liftedFibrancy_iff
    (liftedFamilyCorrespondence_of_strictInverse HF HG HB HC
      hForward hBackward hSource hTarget)

#print axioms mapScaledHornProblem_id
#print axioms mapScaledHornProblem_congr
#print axioms roundTrip_filler_iff_of_leftInverse
#print axioms liftedFamilyCorrespondence_of_strictInverse
#print axioms liftedFibrancy_iff_of_strictInverse

end KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29
