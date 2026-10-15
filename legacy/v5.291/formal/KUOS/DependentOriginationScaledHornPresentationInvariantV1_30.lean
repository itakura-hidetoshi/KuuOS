import KUOS.DependentOriginationScaledDuskinHornTransportV1_29

namespace KUOS.DependentOriginationScaledHornPresentationInvariantV1_30

open CategoryTheory
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29

universe u

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
    {X Y : Type u}
    (HX : ScaledHornFamily X)
    (HY : ScaledHornFamily Y) where
  forward : ∀ P : ScaledHornExtensionProblem X, ScaledHornExtensionProblem Y
  backward : ∀ Q : ScaledHornExtensionProblem Y, ScaledHornExtensionProblem X
  forward_admissible : ∀ P, HX.admissible P → HY.admissible (forward P)
  backward_admissible : ∀ Q, HY.admissible Q → HX.admissible (backward Q)
  forward_filler :
    ∀ P,
      Nonempty (ScaledHornFiller P) →
      Nonempty (ScaledHornFiller (forward P))
  backward_filler :
    ∀ Q,
      Nonempty (ScaledHornFiller Q) →
      Nonempty (ScaledHornFiller (backward Q))
  forward_backward_filler_equiv :
    ∀ Q,
      Nonempty (ScaledHornFiller (forward (backward Q))) ↔
        Nonempty (ScaledHornFiller Q)
  backward_forward_filler_equiv :
    ∀ P,
      Nonempty (ScaledHornFiller (backward (forward P))) ↔
        Nonempty (ScaledHornFiller P)

/-- A presentation equivalence transports admissible horn fillers forward. -/
theorem hasScaledHornFillers_forward
    {X Y : Type u}
    {HX : ScaledHornFamily X}
    {HY : ScaledHornFamily Y}
    (E : ScaledHornPresentationEquivalence HX HY)
    (hX : HasScaledHornFillers HX) :
    HasScaledHornFillers HY := by
  intro Q hQ
  have hback : HX.admissible (E.backward Q) :=
    E.backward_admissible Q hQ
  have hfill : Nonempty (ScaledHornFiller (E.backward Q)) :=
    hX (E.backward Q) hback
  have hff : Nonempty (ScaledHornFiller (E.forward (E.backward Q))) :=
    E.forward_filler (E.backward Q) hfill
  exact (E.forward_backward_filler_equiv Q).mp hff

/-- Reverse transport of admissible horn fillers. -/
theorem hasScaledHornFillers_backward
    {X Y : Type u}
    {HX : ScaledHornFamily X}
    {HY : ScaledHornFamily Y}
    (E : ScaledHornPresentationEquivalence HX HY)
    (hY : HasScaledHornFillers HY) :
    HasScaledHornFillers HX := by
  intro P hP
  have hfwd : HY.admissible (E.forward P) :=
    E.forward_admissible P hP
  have hfill : Nonempty (ScaledHornFiller (E.forward P)) :=
    hY (E.forward P) hfwd
  have hbb : Nonempty (ScaledHornFiller (E.backward (E.forward P))) :=
    E.backward_filler (E.forward P) hfill
  exact (E.backward_forward_filler_equiv P).mp hbb

/-- Scaled horn fibrancy is invariant under horn-presentation equivalence. -/
theorem hasScaledHornFillers_iff
    {X Y : Type u}
    {HX : ScaledHornFamily X}
    {HY : ScaledHornFamily Y}
    (E : ScaledHornPresentationEquivalence HX HY) :
    HasScaledHornFillers HX ↔ HasScaledHornFillers HY :=
  ⟨hasScaledHornFillers_forward E, hasScaledHornFillers_backward E⟩

/-- Bundled presentation-independent scaled fibrancy certificate. -/
structure PresentationIndependentScaledFibrancy
    {X Y : Type u}
    (HX : ScaledHornFamily X)
    (HY : ScaledHornFamily Y) : Prop where
  presentationEquiv : ScaledHornPresentationEquivalence HX HY
  fibrancyInvariant : HasScaledHornFillers HX ↔ HasScaledHornFillers HY

/-- Any horn-presentation equivalence yields the bundled invariant. -/
theorem presentationIndependentScaledFibrancy
    {X Y : Type u}
    {HX : ScaledHornFamily X}
    {HY : ScaledHornFamily Y}
    (E : ScaledHornPresentationEquivalence HX HY) :
    PresentationIndependentScaledFibrancy HX HY where
  presentationEquiv := E
  fibrancyInvariant := hasScaledHornFillers_iff E

end KUOS.DependentOriginationScaledHornPresentationInvariantV1_30
