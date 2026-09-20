import KUOS.DependentOriginationRelativeCorrectionV2_79

namespace KUOS.DependentOriginationRelativeCorrectionV2_79

def twoRegionProblem : RelativeCorrectionProblem Nat Bool where
  active := fun region => region = true
  exactAt := fun region x => region = false → Even x
  compatible := fun _ => True

def addTwoStep (x y : Nat) : Prop :=
  y = x + 2

example {x y : Nat}
    (hx : twoRegionProblem.ExteriorExact x)
    (hxy : RelativeStep twoRegionProblem addTwoStep x y) :
    twoRegionProblem.ExteriorExact y :=
  exteriorExact_of_relativeStep twoRegionProblem addTwoStep hx hxy

example {x y : Nat}
    (hx : twoRegionProblem.compatible x)
    (hxy : RelativeStep twoRegionProblem addTwoStep x y) :
    twoRegionProblem.compatible y :=
  compatible_of_relativeStep twoRegionProblem addTwoStep hx hxy

end KUOS.DependentOriginationRelativeCorrectionV2_79
