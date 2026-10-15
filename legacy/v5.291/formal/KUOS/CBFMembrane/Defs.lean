import Mathlib.Data.Set.Basic

/-!
CBF Membrane-Gap Kernel v1.0: minimal Lean surface.

This file intentionally keeps the kernel abstract.  It fixes the authority
boundary: a CBF pass is a membrane license, not truth and not execution.
-/

namespace KUOS
namespace CBFMembrane

structure IntegratedCBF (State Action : Type) where
  Pass : State → Action → Prop
  Project : State → Action → Action
  project_sound : ∀ s a, Pass s (Project s a)

structure MembraneLicense
  {State Action : Type}
  (C : IntegratedCBF State Action) where
  state : State
  action : Action
  membrane_pass : C.Pass state action

structure ExecuteAuthority (Action : Type) where
  may_execute : Action → Prop

structure TruthAuthority (State Action : Type) where
  true_claim : State → Action → Prop

structure CBFIsNotExecuteAuthority
  {State Action : Type}
  (C : IntegratedCBF State Action)
  (E : ExecuteAuthority Action) where
  no_implication : ¬ (∀ s a, C.Pass s a → E.may_execute a)

structure CBFIsNotTruthAuthority
  {State Action : Type}
  (C : IntegratedCBF State Action)
  (T : TruthAuthority State Action) where
  no_implication : ¬ (∀ s a, C.Pass s a → T.true_claim s a)

structure LayeredCBFPass (State Action : Type) where
  localPass : State → Action → Prop
  beliefPass : State → Action → Prop
  globalPass : State → Action → Prop
  spectralStrongPass : State → Action → Prop

structure GapBundle (State Action : Type) where
  stateGap : State → Int
  actionGap : State → Action → Int
  beliefEffectiveGap : State → Action → Int
  temporalRecoveryGap : State → Action → Int
  gluingGap : State → Action → Int
  spectralExpectedGap : State → Action → Int
  negativeSpectralMassPresent : State → Action → Prop

structure MembraneTierPolicy where
  graveSlackAllowed : Prop
  hardSlackAllowed : Prop
  graveScoreOffsetAllowed : Prop
  hardScoreOffsetAllowed : Prop

structure FixedTierPolicy (P : MembraneTierPolicy) where
  grave_slack_forbidden : ¬ P.graveSlackAllowed
  hard_slack_forbidden : ¬ P.hardSlackAllowed
  grave_score_offset_forbidden : ¬ P.graveScoreOffsetAllowed
  hard_score_offset_forbidden : ¬ P.hardScoreOffsetAllowed

end CBFMembrane
end KUOS
