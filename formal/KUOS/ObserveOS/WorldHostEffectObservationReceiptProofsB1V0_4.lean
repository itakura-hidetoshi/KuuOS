import KUOS.ObserveOS.WorldHostEffectObservationReceiptCoreV0_4

namespace KUOS.ObserveOS
open WORLD VerifyOS LearnOS DecisionOS PlanOS ActOS
namespace WorldHostEffectObservationBridge

abbrev ReceiptB1 := WorldHostEffectObservationReceipt

theorem matched_observation_discharges_observation_debt
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge)
    (h : r.comparison.verdict = .matched) :
    r.debtSemantics.observationDebtDischarged = true ∧
      r.debtSemantics.reobservationRequired = false ∧
      r.worldPrerequisite.qualifyingObservationSupplied = true := by
  have hd : r.debtSemantics.verdict = .matched := r.verdictExact.trans h
  have hq : r.worldPrerequisite.verdict = .matched :=
    r.qualificationVerdictExact.trans h
  exact ⟨(r.debtSemantics.matchedDebt hd).1,
    (r.debtSemantics.matchedDebt hd).2,
    (r.worldPrerequisite.matchedRule hq).2.2.1⟩

theorem divergent_observation_discharges_observation_debt
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge)
    (h : r.comparison.verdict = .divergent) :
    r.debtSemantics.observationDebtDischarged = true ∧
      r.debtSemantics.reobservationRequired = false ∧
      r.worldPrerequisite.qualifyingObservationSupplied = true := by
  have hd : r.debtSemantics.verdict = .divergent := r.verdictExact.trans h
  have hq : r.worldPrerequisite.verdict = .divergent :=
    r.qualificationVerdictExact.trans h
  exact ⟨(r.debtSemantics.divergentDebt hd).1,
    (r.debtSemantics.divergentDebt hd).2,
    (r.worldPrerequisite.divergentRule hq).2.2.1⟩

theorem inconclusive_observation_requires_reobservation
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge)
    (h : r.comparison.verdict = .inconclusive) :
    r.debtSemantics.observationDebtDischarged = false ∧
      r.debtSemantics.reobservationRequired = true ∧
      r.worldPrerequisite.qualifyingObservationSupplied = false := by
  have hd : r.debtSemantics.verdict = .inconclusive := r.verdictExact.trans h
  have hq : r.worldPrerequisite.verdict = .inconclusive :=
    r.qualificationVerdictExact.trans h
  exact ⟨(r.debtSemantics.inconclusiveDebt hd).1,
    (r.debtSemantics.inconclusiveDebt hd).2,
    (r.worldPrerequisite.inconclusiveRule hq).2.2.1⟩

theorem conflicted_observation_requires_reobservation
    {Bridge : WorldHostEffectObservationBridge K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge}
    (r : ReceiptB1 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge GenerationBridge HandoffBridge SelectionBridge SynthesisBridge MaterializationBridge AdmissionBridge AuthorizationBridge InvocationBridge WorldIntakeBridge Bridge)
    (h : r.comparison.verdict = .conflicted) :
    r.debtSemantics.observationDebtDischarged = false ∧
      r.debtSemantics.reobservationRequired = true ∧
      r.worldPrerequisite.qualifyingObservationSupplied = false := by
  have hd : r.debtSemantics.verdict = .conflicted := r.verdictExact.trans h
  have hq : r.worldPrerequisite.verdict = .conflicted :=
    r.qualificationVerdictExact.trans h
  exact ⟨(r.debtSemantics.conflictedDebt hd).1,
    (r.debtSemantics.conflictedDebt hd).2,
    (r.worldPrerequisite.conflictedRule hq).2.2.1⟩

end WorldHostEffectObservationBridge
end KUOS.ObserveOS
