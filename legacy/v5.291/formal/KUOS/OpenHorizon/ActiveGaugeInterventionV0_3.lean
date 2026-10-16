import Mathlib

/-!
A proof surface for the active gauge intervention loop.
An intervention receipt compares intended and realized transport. Its discrete
curvature transforms by conjugation, so flatness is independent of local frame.
-/

namespace KUOS
namespace OpenHorizon

variable {G : Type*} [Group G]

structure EffectReceipt (G : Type*) where
  intended : G
  realized : G

def discreteCurvature (r : EffectReceipt G) : G :=
  r.realized * r.intended⁻¹

def transformReceipt (g : G) (r : EffectReceipt G) : EffectReceipt G where
  intended := g * r.intended * g⁻¹
  realized := g * r.realized * g⁻¹

theorem discreteCurvature_gauge_covariant (g : G) (r : EffectReceipt G) :
    discreteCurvature (transformReceipt g r) =
      g * discreteCurvature r * g⁻¹ := by
  simp [discreteCurvature, transformReceipt, mul_assoc]

theorem flat_effect_gauge_invariant (g : G) (r : EffectReceipt G) :
    discreteCurvature (transformReceipt g r) = 1 ↔
      discreteCurvature r = 1 := by
  rw [discreteCurvature_gauge_covariant]
  constructor
  · intro h
    have h' := congrArg (fun q => g⁻¹ * q * g) h
    simpa [mul_assoc] using h'
  · intro h
    simp [h]

end OpenHorizon
end KUOS
