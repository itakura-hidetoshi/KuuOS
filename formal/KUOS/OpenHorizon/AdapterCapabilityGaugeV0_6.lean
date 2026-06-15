import Mathlib

/-!
A finite formal surface for context-local adapter capability calibration.
The observed effect defines curvature relative to the current connection, and one
bounded affine update transports the connection toward that observation.
-/

namespace KUOS
namespace OpenHorizon

structure CapabilitySection where
  connection : ℚ

def capabilityCurvature (section : CapabilitySection) (observed : ℚ) : ℚ :=
  observed - section.connection

def calibrate (α : ℚ) (section : CapabilitySection) (observed : ℚ) :
    CapabilitySection where
  connection := section.connection + α * capabilityCurvature section observed

theorem calibrate_eq_connection_add_curvature
    (α : ℚ) (section : CapabilitySection) (observed : ℚ) :
    (calibrate α section observed).connection =
      section.connection + α * capabilityCurvature section observed := by
  rfl

theorem flat_observation_has_zero_curvature
    (section : CapabilitySection) :
    capabilityCurvature section section.connection = 0 := by
  simp [capabilityCurvature]

theorem flat_observation_preserves_connection
    (α : ℚ) (section : CapabilitySection) :
    (calibrate α section section.connection).connection = section.connection := by
  simp [calibrate, capabilityCurvature]

theorem full_rate_reaches_observation
    (section : CapabilitySection) (observed : ℚ) :
    (calibrate 1 section observed).connection = observed := by
  simp [calibrate, capabilityCurvature]
  ring

theorem zero_rate_preserves_connection
    (section : CapabilitySection) (observed : ℚ) :
    (calibrate 0 section observed).connection = section.connection := by
  simp [calibrate]

structure AdapterSelection where
  selectedAdapterCount : ℕ
  uniqueSelection : selectedAdapterCount ≤ 1

theorem selectedAdapterCount_eq_zero_or_one (selection : AdapterSelection) :
    selection.selectedAdapterCount = 0 ∨ selection.selectedAdapterCount = 1 := by
  omega

structure CapabilityHistory where
  observations : ℕ
  calibrations : ℕ
  calibrationBound : calibrations ≤ observations

def assimilateObservation (history : CapabilityHistory) : CapabilityHistory where
  observations := history.observations + 1
  calibrations := history.calibrations + 1
  calibrationBound := by omega

theorem assimilateObservation_observations_strict (history : CapabilityHistory) :
    history.observations < (assimilateObservation history).observations := by
  simp [assimilateObservation]

theorem iterate_assimilateObservation
    (history : CapabilityHistory) (n : ℕ) :
    (Function.iterate assimilateObservation n history).observations =
      history.observations + n := by
  induction n with
  | zero => simp
  | succ n ih =>
      simp [Function.iterate_succ_apply, ih, assimilateObservation, Nat.add_assoc]

end OpenHorizon
end KUOS
