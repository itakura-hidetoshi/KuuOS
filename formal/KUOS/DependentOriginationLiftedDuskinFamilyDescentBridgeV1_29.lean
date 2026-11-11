import KUOS.DependentOriginationLiftedDuskinRoundTripBridgeV1_29
import KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30

namespace KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open scoped Bicategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationLiftedDuskinRoundTripBridgeV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Conditional typed descent from genuinely lifted Duskin horn families

The normalized Duskin nerve maps act on the pairwise ULift carriers. The
unlifted GlobalDuskinScaledHornFamily is NOT definitionally the family on
these carriers. Accordingly the theorem below separates: (i) genuine
lifted-to-lifted transport; (ii) independently supplied unlifted-to-lifted
presentation equivalences. No compatibility or descent witness is inferred
from a bare model equivalence.
-/

/-- The exact geometric conditions for bidirectional *lifted* family transport. -/
structure LiftedDuskinFamilyCorrespondence
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    (HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C))
    (HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C)) : Prop where
  forward_admissible :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i),
      HB.admissible P → HC.admissible (transportGlobalDuskinHornProblem HF P)
  backward_admissible :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i),
      HC.admissible Q → HB.admissible (transportGlobalDuskinHornProblem HG Q)
  source_roundTrip_filler_reflect :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i),
      Nonempty (ScaledHornFiller (liftedSourceRoundTrip HF HG P)) ↔
        Nonempty (ScaledHornFiller P)
  target_roundTrip_filler_reflect :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i),
      Nonempty (ScaledHornFiller (liftedTargetRoundTrip HF HG Q)) ↔
        Nonempty (ScaledHornFiller Q)

/-- Precisely typed equivalence between *lifted* horn presentations. -/
def liftedPresentationEquivalence
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    {HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C)}
    {HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C)}
    (D : LiftedDuskinFamilyCorrespondence HF HG HB HC) :
    ScaledHornPresentationEquivalence HB HC where
  forward := fun P => transportGlobalDuskinHornProblem HF P
  backward := fun Q => transportGlobalDuskinHornProblem HG Q
  forward_admissible := D.forward_admissible
  backward_admissible := D.backward_admissible
  forward_filler := by
    intro n i P hP
    exact mapScaledHornFiller_nonempty HF.map_scaled hP
  backward_filler := by
    intro n i Q hQ
    exact mapScaledHornFiller_nonempty HG.map_scaled hQ
  forward_backward_filler_equiv := D.target_roundTrip_filler_reflect
  backward_forward_filler_equiv := D.source_roundTrip_filler_reflect

/-- The actual theorem justified at the lifted boundary. -/
theorem liftedFibrancy_iff
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    {HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C)}
    {HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C)}
    (D : LiftedDuskinFamilyCorrespondence HF HG HB HC) :
    HasScaledHornFillers (normalizedDuskinSource B C)
        (normalizedDuskinSourceScaling B C) HB ↔
      HasScaledHornFillers (normalizedDuskinTarget B C)
        (normalizedDuskinTargetScaling B C) HC :=
  hasScaledHornFillers_iff (liftedPresentationEquivalence D)

/--
Conditional descent to the ORIGINAL unlifted conclusion. The bridges
E_B and E_C are *separate proof obligations*: their existence is not
claimed and is not hidden in the lifted round-trip calculation.
-/
theorem unliftedFibrancy_iff_of_explicit_bridges
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (HB₀ : GlobalDuskinScaledHornFamily B)
    (HC₀ : GlobalDuskinScaledHornFamily C)
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    {HB : ScaledHornFamily (normalizedDuskinSource B C)
      (normalizedDuskinSourceScaling B C)}
    {HC : ScaledHornFamily (normalizedDuskinTarget B C)
      (normalizedDuskinTargetScaling B C)}
    (E_B : ScaledHornPresentationEquivalence HB₀ HB)
    (E_C : ScaledHornPresentationEquivalence HC₀ HC)
    (D : LiftedDuskinFamilyCorrespondence HF HG HB HC) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB₀ ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC₀ := by
  exact (hasScaledHornFillers_iff E_B).trans
    ((liftedFibrancy_iff D).trans (hasScaledHornFillers_iff E_C).symm)

#print axioms liftedPresentationEquivalence
#print axioms liftedFibrancy_iff
#print axioms unliftedFibrancy_iff_of_explicit_bridges

end KUOS.DependentOriginationLiftedDuskinFamilyDescentBridgeV1_29
