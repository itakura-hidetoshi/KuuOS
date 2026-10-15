import KUOS.CodeAI.IndependentTestStrengtheningV0_1

namespace KuuOSCodeAIIndependentTestStrengtheningV0_1

open KUOS.CodeAI.IndependentTestStrengtheningV0_1

example : familyCheck ErrorFamily.syntax = CheckKind.parseNegativeControl := by
  rfl

example : routeCheck RepairRoute.externalEvidenceRequired = CheckKind.externalEvidenceBinding := by
  rfl

example : baselineChecks.length = 3 :=
  baselineChecks_length

end KuuOSCodeAIIndependentTestStrengtheningV0_1
