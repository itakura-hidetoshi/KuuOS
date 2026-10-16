import KUOS.CBFMembrane.Defs

namespace KUOS
namespace CBFMembrane

/-- Projection soundness: the projected action satisfies the declared membrane pass. -/
theorem integrated_cbf_project_sound
  {State Action : Type}
  (C : IntegratedCBF State Action)
  (s : State)
  (a : Action) :
  C.Pass s (C.Project s a) :=
  C.project_sound s a

/-- A membrane license only packages membrane pass. -/
theorem membrane_license_contains_membrane_pass
  {State Action : Type}
  {C : IntegratedCBF State Action}
  (L : MembraneLicense C) :
  C.Pass L.state L.action :=
  L.membrane_pass

/-- Local pass is not definitionally global pass.  They are separate fields. -/
def localPassOf
  {State Action : Type}
  (L : LayeredCBFPass State Action) : State → Action → Prop :=
  L.localPass

/-- Spectral strong pass is a separate surface from local pass. -/
def spectralStrongPassOf
  {State Action : Type}
  (L : LayeredCBFPass State Action) : State → Action → Prop :=
  L.spectralStrongPass

/-- Fixed tier policies forbid slack and score offsets for grave and hard membranes. -/
theorem fixed_policy_forbids_hard_slack
  (P : MembraneTierPolicy)
  (F : FixedTierPolicy P) :
  ¬ P.hardSlackAllowed :=
  F.hard_slack_forbidden

/-- Fixed tier policies forbid grave score offset. -/
theorem fixed_policy_forbids_grave_score_offset
  (P : MembraneTierPolicy)
  (F : FixedTierPolicy P) :
  ¬ P.graveScoreOffsetAllowed :=
  F.grave_score_offset_forbidden

end CBFMembrane
end KUOS
