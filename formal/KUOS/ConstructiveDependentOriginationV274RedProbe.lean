import KUOS.DependentOriginationCorrectionRealizationV2_74

namespace KUOS.DependentOriginationCorrectionRealizationV2_74

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration

def boolFiltration : ObstructionFiltration Bool where
  level := fun _ => {true}
  antitone_level := by
    intro m n hmn x hx
    exact hx

def boolCorrection : CorrectionRealization Unit Bool Bool where
  admissible := fun _ _ => True
  effect := fun _ p => p

example : boolCorrection.CorrectableAt () false := by
  exact ⟨false, trivial, rfl⟩

example : boolCorrection.CorrectableAt () false ∧ ¬ boolFiltration.Flat false := by
  constructor
  · exact ⟨false, trivial, rfl⟩
  · intro h
    have h0 := h 0
    simp [boolFiltration] at h0

end KUOS.DependentOriginationCorrectionRealizationV2_74
