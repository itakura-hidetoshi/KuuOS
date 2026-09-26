import KUOS.DependentOriginationStageIIBareMiddleSwitchHomeomorphV4_45
import KUOS.DependentOriginationStageIIIntegralOrientationLiftV4_22
import Mathlib

namespace KUOS.DependentOriginationStageIIGeometricOrientationV4_46

open KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
open KUOS.DependentOriginationStageIIIntegralOrientationLiftV4_22
open KUOS.DependentOriginationStageIIFiniteDepthRecursiveTransportV4_24
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
open KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
open KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44
open KUOS.DependentOriginationStageIIBareMiddleSwitchHomeomorphV4_45

set_option autoImplicit false

noncomputable section

/-!
# Orientation semantics on the geometric Stage-II homeomorphism v4.46

v4.45 upgrades the descended middle-switch to a fixed-point-free
self-homeomorphism of the bare geometric Cantor carrier.

The present unit transports the already-certified finite-depth orientation
semantics through that geometric symmetry.

For a bare geometric point p and finite depth n, read its unique branch and
then read the orientation of the corresponding recursive depth cell.  This
defines a geometric orientation observable

  O(p,n).

The middle-switch homeomorphism sends the selected branch to its inverse-limit
mate.  By v4.27, the mate reverses orientation at every finite depth.  Hence

  O(M p,n) = flip(O(p,n)).

Using the integral orientation lift from v4.22, this becomes genuine sign
reversal upstairs in the integers,

  epsilon(M p,n) = - epsilon(p,n),

while modulo two both signs collapse to the same class one.

Thus the same geometric involution simultaneously retains:

* topological symmetry on the Cantor carrier;
* finite-depth orientation reversal;
* integer sign sensitivity;
* mod-two orientation blindness.

No new obstruction class is invented here; this unit transports the existing
orientation semantics through the validated geometric homeomorphism.
-/

/-- Finite-depth orientation observable attached to a bare geometric point via
its unique recovered Stage-II branch. -/
noncomputable def stageIIGeometricCarrierOrientation
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    StageIIIncidenceOrientation :=
  stageIIIncidenceRecursiveDepthCellOrientation
    ((stageIIGeometricBranch p).1 depth)

/-- Integer orientation coefficient of one bare geometric point at one finite
depth. -/
noncomputable def stageIIGeometricCarrierOrientationIntCoeff
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) : ℤ :=
  stageIIIncidenceOrientationIntCoeff
    (stageIIGeometricCarrierOrientation p depth)

/-- The descended middle-switch reverses the finite-depth geometric
orientation observable at every depth. -/
theorem stageIIGeometricCarrierOrientation_middleSwitch
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientation
        (stageIIGeometricCarrierMiddleSwitch p) depth =
      stageIIIncidenceOrientationFlip
        (stageIIGeometricCarrierOrientation p depth) := by
  unfold stageIIGeometricCarrierOrientation
  rw [stageIIGeometricBranch_middleSwitch]
  exact
    stageIIInverseLimitMate_orientation_flip
      (stageIIGeometricBranch p) depth

/-- The same orientation reversal stated for the v4.45 self-homeomorphism. -/
theorem stageIIGeometricCarrierOrientation_homeomorph
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientation
        (stageIIGeometricCarrierMiddleSwitchHomeomorph p) depth =
      stageIIIncidenceOrientationFlip
        (stageIIGeometricCarrierOrientation p depth) := by
  change
    stageIIGeometricCarrierOrientation
        (stageIIGeometricCarrierMiddleSwitch p) depth =
      stageIIIncidenceOrientationFlip
        (stageIIGeometricCarrierOrientation p depth)
  exact stageIIGeometricCarrierOrientation_middleSwitch p depth

/-- The integer orientation coefficient changes sign under the descended
middle-switch. -/
theorem stageIIGeometricCarrierOrientationIntCoeff_middleSwitch
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientationIntCoeff
        (stageIIGeometricCarrierMiddleSwitch p) depth =
      -stageIIGeometricCarrierOrientationIntCoeff p depth := by
  unfold stageIIGeometricCarrierOrientationIntCoeff
  rw [stageIIGeometricCarrierOrientation_middleSwitch]
  exact
    stageIIIncidenceOrientationIntCoeff_flip
      (stageIIGeometricCarrierOrientation p depth)

/-- Integer sign reversal stated directly for the geometric self-homeomorphism. -/
theorem stageIIGeometricCarrierOrientationIntCoeff_homeomorph
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientationIntCoeff
        (stageIIGeometricCarrierMiddleSwitchHomeomorph p) depth =
      -stageIIGeometricCarrierOrientationIntCoeff p depth := by
  change
    stageIIGeometricCarrierOrientationIntCoeff
        (stageIIGeometricCarrierMiddleSwitch p) depth =
      -stageIIGeometricCarrierOrientationIntCoeff p depth
  exact
    stageIIGeometricCarrierOrientationIntCoeff_middleSwitch p depth

/-- Every geometric orientation coefficient reduces to one modulo two. -/
@[simp] theorem stageIIGeometricCarrierOrientationIntCoeff_modTwo_eq_one
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    ((stageIIGeometricCarrierOrientationIntCoeff p depth : ℤ) : ZMod 2) =
      1 := by
  unfold stageIIGeometricCarrierOrientationIntCoeff
  exact
    stageIIIncidenceOrientationIntCoeff_modTwo_eq_one
      (stageIIGeometricCarrierOrientation p depth)

/-- Although the homeomorphism reverses the integer sign, reduction modulo two
forgets that reversal exactly. -/
theorem stageIIGeometricCarrierOrientationIntCoeff_homeomorph_modTwo
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    ((stageIIGeometricCarrierOrientationIntCoeff
        (stageIIGeometricCarrierMiddleSwitchHomeomorph p) depth : ℤ) :
        ZMod 2) =
      ((stageIIGeometricCarrierOrientationIntCoeff p depth : ℤ) :
        ZMod 2) := by
  rw [stageIIGeometricCarrierOrientationIntCoeff_modTwo_eq_one,
    stageIIGeometricCarrierOrientationIntCoeff_modTwo_eq_one]

/-- The homeomorphism also sends the selected recursive cell to one of opposite
inner-face kind at every finite depth. -/
theorem stageIIGeometricCarrierHomeomorph_opposite_innerKinds
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    ((stageIIGeometricBranch p).1 depth).innerKind ≠
      ((stageIIGeometricBranch
        (stageIIGeometricCarrierMiddleSwitchHomeomorph p)).1 depth).innerKind := by
  change
    ((stageIIGeometricBranch p).1 depth).innerKind ≠
      ((stageIIGeometricBranch
        (stageIIGeometricCarrierMiddleSwitch p)).1 depth).innerKind
  rw [stageIIGeometricBranch_middleSwitch]
  exact
    stageIIInverseLimitMate_opposite_innerKinds
      (stageIIGeometricBranch p) depth

/-- The homeomorphism sends the selected recursive branch to an actually
adjacent pentagon--hexagon parent pair at every finite depth. -/
theorem stageIIGeometricCarrierHomeomorph_parent_adjacent
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19.truncatedSeedPentagonHexagonAdjacent
      ((stageIIGeometricBranch p).1 depth).parent.1
      ((stageIIGeometricBranch
        (stageIIGeometricCarrierMiddleSwitchHomeomorph p)).1 depth).parent.1 := by
  change
    KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19.truncatedSeedPentagonHexagonAdjacent
      ((stageIIGeometricBranch p).1 depth).parent.1
      ((stageIIGeometricBranch
        (stageIIGeometricCarrierMiddleSwitch p)).1 depth).parent.1
  rw [stageIIGeometricBranch_middleSwitch]
  exact
    stageIIInverseLimitMate_parent_adjacent
      (stageIIGeometricBranch p) depth

/-- Bundle the geometric/topological and orientation-sensitive information
carried by the v4.45 homeomorphism. -/
structure StageIIGeometricOrientationHomeomorphCertificate where
  homeomorph :
    StageIIGeometricCantorCarrier ≃ₜ
      StageIIGeometricCantorCarrier
  noFixedPoint :
    ∀ p, homeomorph p ≠ p
  involutive :
    Function.Involutive homeomorph
  orientationFlip :
    ∀ p depth,
      stageIIGeometricCarrierOrientation (homeomorph p) depth =
        stageIIIncidenceOrientationFlip
          (stageIIGeometricCarrierOrientation p depth)
  integerSignFlip :
    ∀ p depth,
      stageIIGeometricCarrierOrientationIntCoeff (homeomorph p) depth =
        -stageIIGeometricCarrierOrientationIntCoeff p depth
  modTwoCollapse :
    ∀ p depth,
      ((stageIIGeometricCarrierOrientationIntCoeff
          (homeomorph p) depth : ℤ) : ZMod 2) =
        ((stageIIGeometricCarrierOrientationIntCoeff p depth : ℤ) : ZMod 2)
  oppositeInnerKinds :
    ∀ p depth,
      ((stageIIGeometricBranch p).1 depth).innerKind ≠
        ((stageIIGeometricBranch (homeomorph p)).1 depth).innerKind

/-- Canonical v4.46 certificate for the free orientation-reversing geometric
middle-switch. -/
noncomputable def stageIIGeometricOrientationHomeomorphCertificate :
    StageIIGeometricOrientationHomeomorphCertificate where
  homeomorph :=
    stageIIGeometricCarrierMiddleSwitchHomeomorph
  noFixedPoint :=
    stageIIGeometricCarrierMiddleSwitchHomeomorph_ne_self
  involutive :=
    stageIIGeometricCarrierMiddleSwitchHomeomorph_involutive
  orientationFlip :=
    stageIIGeometricCarrierOrientation_homeomorph
  integerSignFlip :=
    stageIIGeometricCarrierOrientationIntCoeff_homeomorph
  modTwoCollapse :=
    stageIIGeometricCarrierOrientationIntCoeff_homeomorph_modTwo
  oppositeInnerKinds :=
    stageIIGeometricCarrierHomeomorph_opposite_innerKinds

/-!
## Boundary after v4.46

The Stage-II geometric middle-switch now carries explicit orientation
semantics all the way to the bare Cantor homeomorphism.

For every bare geometric point p and every finite depth n:

  O(M p,n) = flip(O(p,n)),

and therefore, upstairs in integers,

  epsilon(M p,n) = -epsilon(p,n).

After reduction modulo two,

  epsilon(M p,n) = epsilon(p,n) = 1 mod 2.

Thus the same free involutive homeomorphism is orientation-reversing in the
integral lift while orientation-blind in the original ZMod 2 coefficient
system.

The existing finite-depth adjacency and opposite-inner-kind provenance also
survive the passage to bare geometric points.

A subsequent unit can use this certified free Z/2 action to construct a
quotient/orbit carrier, or attach the existing Stage-II obstruction class to
the geometric orbit structure without changing its transport-independent
value.
-/

end

end KUOS.DependentOriginationStageIIGeometricOrientationV4_46
