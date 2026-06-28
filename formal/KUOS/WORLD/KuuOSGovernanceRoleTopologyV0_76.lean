import Mathlib
import KUOS.WORLD.KuuOSAuthorizedMemoryApplicationV0_75

namespace KUOS.WORLD.KuuOSGovernanceRoleTopologyV0_76

inductive GovernanceMode where
  | soloResearch
  | teamResearch
  | production
  deriving DecidableEq, Repr

end KUOS.WORLD.KuuOSGovernanceRoleTopologyV0_76
