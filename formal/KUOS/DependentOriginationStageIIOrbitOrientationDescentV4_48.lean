import KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47
import KUOS.DependentOriginationStageIIObstructionClassV4_12
import Mathlib

namespace KUOS.DependentOriginationStageIIOrbitOrientationDescentV4_48

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationStageIIGeometricCantorTopologyV4_30
open KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44
open KUOS.DependentOriginationStageIIGeometricOrientationV4_46
open KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47

set_option autoImplicit false

noncomputable section

/-!
# Orientation descent dichotomy on the Stage-II geometric orbit quotient v4.48

v4.47 constructs the exact two-point orbit quotient of the free geometric
middle-switch and proves its universal factorization property.

v4.46 proves that the integer orientation coefficient changes sign under the
middle-switch, while its reduction modulo two is unchanged.

This unit combines those two facts into an exact descent dichotomy.

At every finite depth:

* the integer orientation coefficient is always +1 or -1, hence nonzero;
* middle-switch sends it to its negative, so it is never invariant;
* therefore it cannot factor through the orbit quotient.

By contrast:

* the mod-two orientation coefficient is always one;
* hence it is middle-switch invariant;
* it descends uniquely to the orbit quotient;
* the descended orbit value is identically one;
* this orbit value agrees exactly with the existing transport-independent
  Stage-II obstruction class omega(T).

Thus the geometric quotient makes precise which orientation information
survives descent: the integer sign is obstructed, while its mod-two class
descends canonically.
-/

/-- The integer orientation coefficient is never zero. -/
theorem stageIIGeometricCarrierOrientationIntCoeff_ne_zero
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientationIntCoeff p depth ≠ 0 := by
  unfold stageIIGeometricCarrierOrientationIntCoeff
  cases h : stageIIGeometricCarrierOrientation p depth <;>
    norm_num [stageIIIncidenceOrientationIntCoeff]

/-- At every point and depth, the integer orientation coefficient is changed
by the middle-switch. -/
theorem stageIIGeometricCarrierOrientationIntCoeff_middleSwitch_ne
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientationIntCoeff
        (stageIIGeometricCarrierMiddleSwitch p) depth ≠
      stageIIGeometricCarrierOrientationIntCoeff p depth := by
  rw [stageIIGeometricCarrierOrientationIntCoeff_middleSwitch]
  intro h
  have hzero :
      stageIIGeometricCarrierOrientationIntCoeff p depth = 0 := by
    linarith
  exact
    stageIIGeometricCarrierOrientationIntCoeff_ne_zero p depth hzero

/-- Therefore the integer orientation semantic is not invariant under the
middle-switch at any fixed depth. -/
theorem stageIIGeometricCarrierOrientationIntCoeff_not_invariant
    (depth : Nat) :
    ¬ ∀ p : StageIIGeometricCantorCarrier,
        stageIIGeometricCarrierOrientationIntCoeff
            (stageIIGeometricCarrierMiddleSwitch p) depth =
          stageIIGeometricCarrierOrientationIntCoeff p depth := by
  intro hInvariant
  rcases XInfinityGeometricFractal_nonempty with ⟨z, hz⟩
  let p : StageIIGeometricCantorCarrier := ⟨z, hz⟩
  exact
    stageIIGeometricCarrierOrientationIntCoeff_middleSwitch_ne
      p depth (hInvariant p)

/-- Main negative descent theorem: the integer orientation semantic cannot
factor through the two-point orbit quotient. -/
theorem stageIIGeometricCarrierOrientationIntCoeff_no_orbit_factorization
    (depth : Nat) :
    ¬ ∃ orbitSemantic : StageIIGeometricMiddleSwitchOrbit → ℤ,
        ∀ p : StageIIGeometricCantorCarrier,
          orbitSemantic
              (stageIIGeometricMiddleSwitchOrbitProjection p) =
            stageIIGeometricCarrierOrientationIntCoeff p depth := by
  intro hFactor
  have hInvariant :
      ∀ p : StageIIGeometricCantorCarrier,
        stageIIGeometricCarrierOrientationIntCoeff
            (stageIIGeometricCarrierMiddleSwitch p) depth =
          stageIIGeometricCarrierOrientationIntCoeff p depth :=
    (stageIIGeometricMiddleSwitch_factors_through_orbit_iff
      (fun p : StageIIGeometricCantorCarrier =>
        stageIIGeometricCarrierOrientationIntCoeff p depth)).1
      hFactor
  exact
    stageIIGeometricCarrierOrientationIntCoeff_not_invariant
      depth hInvariant

/-- The mod-two orientation semantic on the bare geometric carrier. -/
noncomputable def stageIIGeometricCarrierOrientationModTwo
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) : ZMod 2 :=
  ((stageIIGeometricCarrierOrientationIntCoeff p depth : ℤ) : ZMod 2)

/-- The bare mod-two orientation semantic is identically one. -/
@[simp] theorem stageIIGeometricCarrierOrientationModTwo_eq_one
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientationModTwo p depth = 1 := by
  unfold stageIIGeometricCarrierOrientationModTwo
  exact stageIIGeometricCarrierOrientationIntCoeff_modTwo_eq_one p depth

/-- Therefore the mod-two orientation semantic is middle-switch invariant. -/
theorem stageIIGeometricCarrierOrientationModTwo_invariant
    (depth : Nat) :
    ∀ p : StageIIGeometricCantorCarrier,
      stageIIGeometricCarrierOrientationModTwo
          (stageIIGeometricCarrierMiddleSwitch p) depth =
        stageIIGeometricCarrierOrientationModTwo p depth := by
  intro p
  rw [stageIIGeometricCarrierOrientationModTwo_eq_one,
    stageIIGeometricCarrierOrientationModTwo_eq_one]

/-- Canonical orbit-level mod-two orientation semantic. -/
noncomputable def stageIIGeometricOrbitOrientationModTwo
    (depth : Nat) :
    StageIIGeometricMiddleSwitchOrbit → ZMod 2 :=
  stageIIGeometricMiddleSwitchDescend
    (fun p : StageIIGeometricCantorCarrier =>
      stageIIGeometricCarrierOrientationModTwo p depth)
    (stageIIGeometricCarrierOrientationModTwo_invariant depth)

/-- Projection to the orbit quotient recovers the bare mod-two orientation
semantic. -/
@[simp] theorem stageIIGeometricOrbitOrientationModTwo_projection
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricOrbitOrientationModTwo depth
        (stageIIGeometricMiddleSwitchOrbitProjection p) =
      stageIIGeometricCarrierOrientationModTwo p depth := by
  rfl

/-- The orbit-level mod-two orientation semantic is identically one. -/
theorem stageIIGeometricOrbitOrientationModTwo_eq_one
    (q : StageIIGeometricMiddleSwitchOrbit)
    (depth : Nat) :
    stageIIGeometricOrbitOrientationModTwo depth q = 1 := by
  refine Quotient.inductionOn q ?_
  intro p
  rw [stageIIGeometricOrbitOrientationModTwo_projection,
    stageIIGeometricCarrierOrientationModTwo_eq_one]

/-- The mod-two orientation semantic has a unique orbit-level descent. -/
theorem stageIIGeometricCarrierOrientationModTwo_existsUnique_orbitSemantic
    (depth : Nat) :
    ∃! orbitSemantic : StageIIGeometricMiddleSwitchOrbit → ZMod 2,
      ∀ p : StageIIGeometricCantorCarrier,
        orbitSemantic
            (stageIIGeometricMiddleSwitchOrbitProjection p) =
          stageIIGeometricCarrierOrientationModTwo p depth := by
  refine
    ⟨stageIIGeometricOrbitOrientationModTwo depth,
      stageIIGeometricOrbitOrientationModTwo_projection,
      ?_⟩
  intro candidate hcandidate
  exact
    stageIIGeometricMiddleSwitchDescend_unique
      (fun p : StageIIGeometricCantorCarrier =>
        stageIIGeometricCarrierOrientationModTwo p depth)
      (stageIIGeometricCarrierOrientationModTwo_invariant depth)
      candidate
      hcandidate

/-- The descended orbit-level mod-two value is exactly the already-certified
transport-independent Stage-II obstruction class. -/
theorem stageIIGeometricOrbitOrientationModTwo_eq_stageIIObstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (q : StageIIGeometricMiddleSwitchOrbit)
    (depth : Nat) :
    stageIIGeometricOrbitOrientationModTwo depth q =
      counterStageIIObstructionAdd T := by
  rw [stageIIGeometricOrbitOrientationModTwo_eq_one,
    counterStageIIObstructionAdd_eq_one]

/-- The descent dichotomy at one finite depth: integer orientation does not
factor, while mod-two orientation has a unique orbit semantic. -/
theorem stageIIGeometricOrientation_descent_dichotomy
    (depth : Nat) :
    (¬ ∃ orbitSemantic : StageIIGeometricMiddleSwitchOrbit → ℤ,
        ∀ p : StageIIGeometricCantorCarrier,
          orbitSemantic
              (stageIIGeometricMiddleSwitchOrbitProjection p) =
            stageIIGeometricCarrierOrientationIntCoeff p depth) ∧
      (∃! orbitSemantic : StageIIGeometricMiddleSwitchOrbit → ZMod 2,
        ∀ p : StageIIGeometricCantorCarrier,
          orbitSemantic
              (stageIIGeometricMiddleSwitchOrbitProjection p) =
            stageIIGeometricCarrierOrientationModTwo p depth) := by
  exact
    ⟨stageIIGeometricCarrierOrientationIntCoeff_no_orbit_factorization depth,
      stageIIGeometricCarrierOrientationModTwo_existsUnique_orbitSemantic depth⟩

/-- Certificate bundling the integral obstruction and the mod-two descent. -/
structure StageIIOrbitOrientationDescentCertificate where
  integerNonzero :
    ∀ p depth,
      stageIIGeometricCarrierOrientationIntCoeff p depth ≠ 0
  integerSignChanges :
    ∀ p depth,
      stageIIGeometricCarrierOrientationIntCoeff
          (stageIIGeometricCarrierMiddleSwitch p) depth ≠
        stageIIGeometricCarrierOrientationIntCoeff p depth
  integerNoDescent :
    ∀ depth,
      ¬ ∃ orbitSemantic : StageIIGeometricMiddleSwitchOrbit → ℤ,
          ∀ p : StageIIGeometricCantorCarrier,
            orbitSemantic
                (stageIIGeometricMiddleSwitchOrbitProjection p) =
              stageIIGeometricCarrierOrientationIntCoeff p depth
  modTwoUniqueDescent :
    ∀ depth,
      ∃! orbitSemantic : StageIIGeometricMiddleSwitchOrbit → ZMod 2,
        ∀ p : StageIIGeometricCantorCarrier,
          orbitSemantic
              (stageIIGeometricMiddleSwitchOrbitProjection p) =
            stageIIGeometricCarrierOrientationModTwo p depth
  modTwoOrbitValue :
    ∀ q depth,
      stageIIGeometricOrbitOrientationModTwo depth q = 1

/-- Canonical v4.48 orientation-descent certificate. -/
noncomputable def stageIIOrbitOrientationDescentCertificate :
    StageIIOrbitOrientationDescentCertificate where
  integerNonzero :=
    stageIIGeometricCarrierOrientationIntCoeff_ne_zero
  integerSignChanges :=
    stageIIGeometricCarrierOrientationIntCoeff_middleSwitch_ne
  integerNoDescent :=
    stageIIGeometricCarrierOrientationIntCoeff_no_orbit_factorization
  modTwoUniqueDescent :=
    stageIIGeometricCarrierOrientationModTwo_existsUnique_orbitSemantic
  modTwoOrbitValue :=
    stageIIGeometricOrbitOrientationModTwo_eq_one

/-!
## Boundary after v4.48

The geometric orbit quotient now exhibits an exact orientation-descent
obstruction.

At every finite depth:

* integer orientation is nonzero and changes sign under the free middle-switch;
* therefore integer orientation cannot descend to the orbit quotient;
* mod-two orientation is invariant and descends uniquely;
* the descended mod-two value is identically one;
* that value is exactly the transport-independent Stage-II obstruction
  omega(T).

This separates two meanings of orientation with no ambiguity:

  integral orientation = genuine sign-sensitive data obstructed by quotient
  descent;

  mod-two orientation = sign-blind class that survives quotient descent and
  carries the existing obstruction.

A subsequent unit can attach the full inverse-limit obstruction section to the
orbit carrier, or introduce quotient topology only after this coefficient-level
descent boundary is fixed.
-/

end

end KUOS.DependentOriginationStageIIOrbitOrientationDescentV4_48
