import KUOS.DependentOriginationResidualStabilityV2_78

namespace KUOS.DependentOriginationRelativeCorrectionV2_79

universe u r

/-!
# Relative correction and corrective descent v2.79

Corrections may be localized to an active region while exact data outside the
active region must remain exact. Global realization is deliberately separated:
it is available only through explicitly supplied descent data.

No topology, cover, or sheaf condition is invented by this generic layer.
-/

/-- Region-indexed local correction data. -/
structure RelativeCorrectionProblem
    (State : Type u) (Region : Type r) where
  active : Region → Prop
  exactAt : Region → State → Prop
  compatible : State → Prop

namespace RelativeCorrectionProblem

variable {State : Type u} {Region : Type r}

/-- Every region outside the active region remains exact. -/
def ExteriorExact
    (P : RelativeCorrectionProblem State Region)
    (x : State) : Prop :=
  ∀ region, ¬ P.active region → P.exactAt region x

end RelativeCorrectionProblem

/-- A local correction step together with explicit preservation of exterior
exactness and compatibility. -/
def RelativeStep
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region)
    (Step : State → State → Prop)
    (x y : State) : Prop :=
  Step x y ∧
  (∀ region,
    ¬ P.active region →
    P.exactAt region x →
    P.exactAt region y) ∧
  (P.compatible x → P.compatible y)

/-- Relative correction preserves every exact exterior region. -/
theorem exteriorExact_of_relativeStep
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region)
    (Step : State → State → Prop)
    {x y : State}
    (hx : P.ExteriorExact x)
    (hxy : RelativeStep P Step x y) :
    P.ExteriorExact y := by
  intro region houtside
  exact hxy.2.1 region houtside (hx region houtside)

/-- Compatibility is preserved by a relative correction step. -/
theorem compatible_of_relativeStep
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region)
    (Step : State → State → Prop)
    {x y : State}
    (hx : P.compatible x)
    (hxy : RelativeStep P Step x y) :
    P.compatible y :=
  hxy.2.2 hx

/-- Global realization is supplied only through an explicit descent principle. -/
structure CorrectiveDescentData
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region) where
  globalRealizable : State → Prop
  descend :
    ∀ x,
      P.ExteriorExact x →
      P.compatible x →
      globalRealizable x

/-- Exterior exactness plus compatibility gives global realizability only when
a corrective descent principle has been supplied. -/
theorem globalRealizable_of_correctiveDescent
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region)
    (D : CorrectiveDescentData P)
    {x : State}
    (hexterior : P.ExteriorExact x)
    (hcompat : P.compatible x) :
    D.globalRealizable x :=
  D.descend x hexterior hcompat

end KUOS.DependentOriginationRelativeCorrectionV2_79
