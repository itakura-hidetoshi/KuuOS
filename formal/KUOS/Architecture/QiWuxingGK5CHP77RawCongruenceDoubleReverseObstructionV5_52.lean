import KUOS.Architecture.QiWuxingGK5CHP77RawCongruenceObservationsV5_51

/-!
Qi v5.52 regression contracts for the independent v5.50 raw-context
congruence quotient. The next implementation must keep both original
endpoints and the supplied raw witness. No old comparison is changed.
Regression-first draft: the two named results below are not yet defined.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Regression: two raw reversals do NOT cancel in the NEW quotient. -/
example (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentClass l r M ≠
      selectedRawCongruentClass l r (selectedContextEighteenDoubleReverse l r M) := by
  exact selectedRawCongruent_doubleReverse_classDistinct l r M

/-- Regression: no Type-valued NEW comparison can witness that cancellation. -/
example (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedRawCongruentNineteen W l r J N M
      (selectedContextEighteenDoubleReverse l r M)) := by
  exact selectedRawCongruent_doubleReverse_noComparison l r M

end ExactFiber

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
