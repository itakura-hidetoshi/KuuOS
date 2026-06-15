import Mathlib

/-!
A discrete noncommutative gauge interface for open-horizon commitments.
Local commitment frames may change, while curvature transforms by conjugation
and flatness remains gauge invariant.
-/

namespace KUOS
namespace OpenHorizon

variable {X G : Type*} [Group G]

abbrev GaugePotential := X → X → G

def gaugeTransform (g : X → G) (A : GaugePotential (X := X) G) : GaugePotential (X := X) G :=
  fun x y => g x * A x y * (g y)⁻¹

def curvature (A : GaugePotential (X := X) G) (x y z : X) : G :=
  A x y * A y z * (A x z)⁻¹

theorem curvature_gauge_covariant
    (g : X → G) (A : GaugePotential (X := X) G) (x y z : X) :
    curvature (gaugeTransform g A) x y z =
      g x * curvature A x y z * (g x)⁻¹ := by
  simp [curvature, gaugeTransform, mul_assoc]

theorem flatness_gauge_invariant
    (g : X → G) (A : GaugePotential (X := X) G) (x y z : X) :
    curvature (gaugeTransform g A) x y z = 1 ↔ curvature A x y z = 1 := by
  rw [curvature_gauge_covariant]
  constructor
  · intro h
    have h' := congrArg (fun q => (g x)⁻¹ * q * g x) h
    simpa [mul_assoc] using h'
  · intro h
    simp [h]

end OpenHorizon
end KUOS
