import KUOS.DependentOriginationScaledDuskinHornTransportV1_29

namespace KUOS.DependentOriginationLiftedDuskinRoundTripBridgeV1_29

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Typed round-trip boundary for lifted global Duskin horns

The forward normalized Duskin map has ULift source B and ULift target C.
The reverse normalized map has exactly these two carriers in reverse order.
The definitional identifications below are *between lifted carriers*, not
between a lifted horn and any unlifted GlobalDuskinScaledHornFamily.

This is a strict one-way result: existence of a source filler transports to
existence of a filler of its normalized forward/backward round-trip image.
The converse, admissible-family descent, and equivalence with the unlifted
horn presentations require separate proofs and are not assumed here.
-/

/-- The reverse target is definitionally the forward lifted source. -/
theorem source_eq_reverse_target
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C] :
    normalizedDuskinSource B C = normalizedDuskinTarget C B := by
  rfl

/-- The reverse source is definitionally the forward lifted target. -/
theorem target_eq_reverse_source
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C] :
    normalizedDuskinTarget B C = normalizedDuskinSource C B := by
  rfl

/-- The two descriptions of the lifted source carry literally the same scaling. -/
theorem source_scaling_eq_reverse_target
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C] :
    normalizedDuskinSourceScaling B C =
      normalizedDuskinTargetScaling C B := by
  rfl

/-- Similarly for the lifted target scaling. -/
theorem target_scaling_eq_reverse_source
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C] :
    normalizedDuskinTargetScaling B C =
      normalizedDuskinSourceScaling C B := by
  rfl

/-- A genuinely typed forward-then-backward horn transport on the lifted B carrier. -/
def liftedSourceRoundTrip
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i) :
    ScaledHornExtensionProblem
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i :=
  transportGlobalDuskinHornProblem HG
    (transportGlobalDuskinHornProblem HF P)

/-- A genuinely typed backward-then-forward horn transport on the lifted C carrier. -/
def liftedTargetRoundTrip
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i) :
    ScaledHornExtensionProblem
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i :=
  transportGlobalDuskinHornProblem HF
    (transportGlobalDuskinHornProblem HG Q)

/--
The forward direction of the lifted source round-trip filler comparison
follows from the two genuine scaled maps, without a descent assumption.
-/
theorem liftedSourceRoundTrip_filler_forward
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i}
    (hP : Nonempty (ScaledHornFiller P)) :
    Nonempty (ScaledHornFiller (liftedSourceRoundTrip HF HG P)) := by
  exact mapScaledHornFiller_nonempty HG.map_scaled
    (mapScaledHornFiller_nonempty HF.map_scaled hP)

/-- The corresponding forward direction on the lifted C carrier. -/
theorem liftedTargetRoundTrip_filler_forward
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    {Q : ScaledHornExtensionProblem
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i}
    (hQ : Nonempty (ScaledHornFiller Q)) :
    Nonempty (ScaledHornFiller (liftedTargetRoundTrip HF HG Q)) := by
  exact mapScaledHornFiller_nonempty HF.map_scaled
    (mapScaledHornFiller_nonempty HG.map_scaled hQ)

#print axioms source_eq_reverse_target
#print axioms target_eq_reverse_source
#print axioms source_scaling_eq_reverse_target
#print axioms target_scaling_eq_reverse_source
#print axioms liftedSourceRoundTrip_filler_forward
#print axioms liftedTargetRoundTrip_filler_forward

/-!
## Composition in the actual lifted horn universe
The following proofs do not identify an unlifted horn with a lifted horn and
do not assume the reverse filler descent still needed for v1.31.
-/

/-- Pushing a scaled horn across two composable scaled maps equals pushing
across their composite. The three carriers live in one SSet universe. -/
theorem mapScaledHornProblem_comp
    {X Y Z : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {sZ : ScaledSimplicialSet Z}
    {f : X ⟶ Y} {g : Y ⟶ Z}
    (hf : IsScaledMap sX sY f)
    (hg : IsScaledMap sY sZ g)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    mapScaledHornProblem hg (mapScaledHornProblem hf P) =
      mapScaledHornProblem (hf.comp hg) P := by
  cases P
  simp [mapScaledHornProblem, Category.assoc]

/-- The lifted B round trip is transport along the genuine composite. -/
theorem liftedSourceRoundTrip_as_composite
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i) :
    liftedSourceRoundTrip HF HG P =
      mapScaledHornProblem (HF.map_scaled.comp HG.map_scaled) P := by
  exact mapScaledHornProblem_comp HF.map_scaled HG.map_scaled P

/-- The lifted C round trip is transport along the genuine composite. -/
theorem liftedTargetRoundTrip_as_composite
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i) :
    liftedTargetRoundTrip HF HG Q =
      mapScaledHornProblem (HG.map_scaled.comp HF.map_scaled) Q := by
  exact mapScaledHornProblem_comp HG.map_scaled HF.map_scaled Q

#print axioms mapScaledHornProblem_comp
#print axioms liftedSourceRoundTrip_as_composite
#print axioms liftedTargetRoundTrip_as_composite

end KUOS.DependentOriginationLiftedDuskinRoundTripBridgeV1_29
