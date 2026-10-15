import KUOS.DependentOriginationMultiSlotInstrumentCombContractionV0_13

namespace KUOS.DependentOriginationTransportSpineV0_13

open KUOS.DependentOriginationQuantumChoiCombV0_9
open KUOS.DependentOriginationCPTPChoiWordV0_11
open KUOS.DependentOriginationQuantumInstrumentBornCombV0_12
open KUOS.DependentOriginationMultiSlotInstrumentCombContractionV0_13

noncomputable section

universe u

/-- Arbitrary finite Choi slots contract to the exactly decoded operational response. -/
theorem arbitrary_multislot_choi_tensor_link_is_operational_response
    {d : ℕ}
    (C : ClosedSequentialProcessCombChoi d)
    (slots : List (ChoiMat d d)) :
    C.tensorLinkScalar slots =
      matrixTraceLinear d
        (complexInterventionWordOperator d (slots.map fromChoi)
          C.initial.matrix) :=
  C.tensorLinkScalar_eq_decodedOperationalResponse slots

/-- Exact generalized Born rule for a selected finite quantum-instrument history. -/
theorem multislot_instrument_choi_contraction_is_joint_born_weight
    {d : ℕ} {Outcome : Type u} [Fintype Outcome]
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    multiSlotInstrumentChoiTensorLinkScalar schedule outcomes ρ =
      jointBornWeight schedule outcomes ρ :=
  multiSlotInstrumentChoi_tensorLink_eq_jointBornWeight
    schedule outcomes ρ hlen

/-- Real generalized-Born scalar is exactly the operational joint Born probability. -/
theorem multislot_instrument_choi_probability_is_joint_born_probability
    {d : ℕ} {Outcome : Type u} [Fintype Outcome]
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    multiSlotInstrumentChoiTensorLinkProbability schedule outcomes ρ =
      jointBornProbability schedule outcomes ρ :=
  multiSlotInstrumentChoi_tensorLinkProbability_eq_jointBornProbability
    schedule outcomes ρ hlen

/-- Exact Choi generalized-Born probabilities inherit operational nonnegativity. -/
theorem multislot_instrument_choi_probability_nonnegative
    {d : ℕ} {Outcome : Type u} [Fintype Outcome]
    (schedule : List (QuantumInstrument d Outcome))
    (outcomes : List Outcome)
    (ρ : DensityMatrix d)
    (hlen : outcomes.length = schedule.length) :
    0 ≤ multiSlotInstrumentChoiTensorLinkProbability schedule outcomes ρ :=
  multiSlotInstrumentChoi_tensorLinkProbability_nonneg
    schedule outcomes ρ hlen

end

end KUOS.DependentOriginationTransportSpineV0_13
