import KUOS.ActOS.VacuumExpectationBoundedAdapterInvocationCoreV0_4

namespace KUOS.ActOS
open WORLD ObserveOS VerifyOS LearnOS DecisionOS PlanOS
namespace VacuumExpectationBoundedAdapterInvocationBridge

abbrev ReceiptE2 := VacuumExpectationBoundedAdapterInvocationReceipt

theorem invocation_digest_is_exact
    {Bridge : VacuumExpectationBoundedAdapterInvocationBridge
      K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
        GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
          MaterializationBridge AdmissionBridge AuthorizationBridge}
    (r : ReceiptE2 K O Intake ObserveBridge VerifyBridge LearnBridge ReplanBridge
      GenerationBridge HandoffBridge SelectionBridge SynthesisBridge
        MaterializationBridge AdmissionBridge AuthorizationBridge Bridge) :
    r.digest = Bridge.digestOf r.source r.activation r.binding r.projection
      r.invocation r.route r.hostReceipt r.hostBinding r.postEffectDebt
      r.activationIndex r.invocationIndex r.hostReceiptIndex r.historyAfter := by
  exact r.digestExact

end VacuumExpectationBoundedAdapterInvocationBridge
end KUOS.ActOS
