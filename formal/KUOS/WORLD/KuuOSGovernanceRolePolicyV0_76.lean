import Mathlib

namespace KUOS.WORLD.KuuOSGovernanceRolePolicyV0_76

inductive OperatingContext where
  | soloResearch
  | teamResearch
  | production
  deriving DecidableEq, Repr

structure RolePolicy where
  context : OperatingContext
  separateActor : Bool


def sharedPolicy (context : OperatingContext) : RolePolicy where
  context := context
  separateActor := false


def separatedPolicy (context : OperatingContext) : RolePolicy where
  context := context
  separateActor := true

end KUOS.WORLD.KuuOSGovernanceRolePolicyV0_76
