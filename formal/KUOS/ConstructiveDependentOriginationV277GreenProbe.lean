import KUOS.DependentOriginationCofinalCorrectionV2_77

namespace KUOS.DependentOriginationCofinalCorrectionV2_77

def nonMonotoneSchedule (j : Nat) : Nat :=
  if j = 0 then 1 else if j = 1 then 0 else j

example : CofinalOrderSchedule nonMonotoneSchedule := by
  intro N
  refine ⟨N + 2, ?_⟩
  simp [nonMonotoneSchedule]
  omega

example : ¬ Monotone nonMonotoneSchedule := by
  intro h
  have h01 := h (show 0 ≤ 1 by omega)
  norm_num [nonMonotoneSchedule] at h01

example (loss N : Nat) :
    ∃ j, N + loss ≤ nonMonotoneSchedule j :=
  cofinalOrderSchedule_add_loss
    (g := nonMonotoneSchedule)
    (by
      intro k
      refine ⟨k + 2, ?_⟩
      simp [nonMonotoneSchedule]
      omega)
    loss N

end KUOS.DependentOriginationCofinalCorrectionV2_77
