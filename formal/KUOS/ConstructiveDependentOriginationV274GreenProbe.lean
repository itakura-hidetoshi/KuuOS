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

def robustBool :
    RobustCorrectionData boolCorrection Nat where
  robustAt := fun μ _ d => μ ≤ 3 ∧ d = false
  robust_implies_correctable := by
    intro μ x d h
    subst d
    exact ⟨false, trivial, rfl⟩
  robust_monotone := by
    intro μ₁ μ₂ x d hμ h
    exact ⟨hμ.trans h.1, h.2⟩

example : robustBool.robustAt 3 () false → robustBool.robustAt 1 () false := by
  intro h
  exact robustBool.weaken_margin (by omega) h

end KUOS.DependentOriginationCorrectionRealizationV2_74
