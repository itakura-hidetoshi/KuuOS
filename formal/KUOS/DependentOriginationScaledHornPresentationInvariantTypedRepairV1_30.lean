import KUOS.DependentOriginationScaledDuskinHornTransportV1_29

namespace KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29

universe u₁ u₂

/-!
# Scaled horn-presentation invariance v1.30

This layer upgrades the one-way horn transport of v1.29 to a genuinely
presentation-independent statement. The key extra datum is not merely a
scaled map, but a bidirectional correspondence between admissible horn
problems together with filler transport in both directions.

No target fibrancy is inferred from a one-way map alone. Fibrancy becomes
presentation-independent only after the reverse horn presentation is supplied.
-/

/-- A bidirectional equivalence between two presentations of the same scaled horn family. -/
structure ScaledHornPresentationEquivalence
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (HX : ScaledHornFamily X sX)
    (HY : ScaledHornFamily Y sY) where
  forward :
    ∀ {n : Nat} {i : Fin (n + 1)},
      ScaledHornExtensionProblem X sX n i →
        ScaledHornExtensionProblem Y sY n i
  backward :
    ∀ {n : Nat} {i : Fin (n + 1)},
      ScaledHornExtensionProblem Y sY n i →
        ScaledHornExtensionProblem X sX n i
  forward_admissible :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      HX.admissible P → HY.admissible (forward P)
  backward_admissible :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem Y sY n i),
      HY.admissible Q → HX.admissible (backward Q)
  forward_filler :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      Nonempty (ScaledHornFiller P) →
        Nonempty (ScaledHornFiller (forward P))
  backward_filler :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem Y sY n i),
      Nonempty (ScaledHornFiller Q) →
        Nonempty (ScaledHornFiller (backward Q))
  forward_backward_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem Y sY n i),
      Nonempty (ScaledHornFiller (forward (backward Q))) ↔
        Nonempty (ScaledHornFiller Q)
  backward_forward_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      Nonempty (ScaledHornFiller (backward (forward P))) ↔
        Nonempty (ScaledHornFiller P)

/-- A presentation equivalence transports admissible horn fillers forward. -/
theorem hasScaledHornFillers_forward
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {HX : ScaledHornFamily X sX}
    {HY : ScaledHornFamily Y sY}
    (E : ScaledHornPresentationEquivalence HX HY)
    (hX : HasScaledHornFillers X sX HX) :
    HasScaledHornFillers Y sY HY := by
  refine ⟨?_⟩
  intro n i Q hQ h0 hi
  have hback : HX.admissible (E.backward Q) :=
    E.backward_admissible Q hQ
  have hfill : Nonempty (ScaledHornFiller (E.backward Q)) :=
    hX.fill (E.backward Q) hback h0 hi
  have hff : Nonempty (ScaledHornFiller (E.forward (E.backward Q))) :=
    E.forward_filler (E.backward Q) hfill
  exact (E.forward_backward_filler_equiv Q).mp hff

/-- Reverse transport of admissible horn fillers. -/
theorem hasScaledHornFillers_backward
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {HX : ScaledHornFamily X sX}
    {HY : ScaledHornFamily Y sY}
    (E : ScaledHornPresentationEquivalence HX HY)
    (hY : HasScaledHornFillers Y sY HY) :
    HasScaledHornFillers X sX HX := by
  refine ⟨?_⟩
  intro n i P hP h0 hi
  have hfwd : HY.admissible (E.forward P) :=
    E.forward_admissible P hP
  have hfill : Nonempty (ScaledHornFiller (E.forward P)) :=
    hY.fill (E.forward P) hfwd h0 hi
  have hbb : Nonempty (ScaledHornFiller (E.backward (E.forward P))) :=
    E.backward_filler (E.forward P) hfill
  exact (E.backward_forward_filler_equiv P).mp hbb

/-- Scaled horn fibrancy is invariant under horn-presentation equivalence. -/
theorem hasScaledHornFillers_iff
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {HX : ScaledHornFamily X sX}
    {HY : ScaledHornFamily Y sY}
    (E : ScaledHornPresentationEquivalence HX HY) :
    HasScaledHornFillers X sX HX ↔ HasScaledHornFillers Y sY HY :=
  ⟨hasScaledHornFillers_forward E, hasScaledHornFillers_backward E⟩

/-- Bundled presentation-independent scaled fibrancy certificate. -/
structure PresentationIndependentScaledFibrancy
        {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (HX : ScaledHornFamily X sX)
    (HY : ScaledHornFamily Y sY) : Prop where
  presentationEquiv : ScaledHornPresentationEquivalence HX HY
  fibrancyInvariant :
    HasScaledHornFillers X sX HX ↔ HasScaledHornFillers Y sY HY

/-- Any horn-presentation equivalence yields the bundled invariant. -/
theorem presentationIndependentScaledFibrancy
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {HX : ScaledHornFamily X sX}
    {HY : ScaledHornFamily Y sY}
    (E : ScaledHornPresentationEquivalence HX HY) :
    PresentationIndependentScaledFibrancy HX HY where
  presentationEquiv := E
  fibrancyInvariant := hasScaledHornFillers_iff E

end KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30
