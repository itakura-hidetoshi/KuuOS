import Kuu.F112.PolygonNativeC60PhysicalGaugeAtlas
import Mathlib.Tactic

/-!
# F112 — all 360 genuine C60 flag curvatures distinguish gauge orbits

The already constructed C60 site gauge atlas acts on the ORIGINAL
182-object incidence source (60 physical darts, 90 physical edges
and 32 physical pentagon/hexagon faces). No graph path is substituted
for source-level transport.

Prove that each of the original 360 typed dart-edge-face flag
curvatures factors through the gauge-orbit quotient. Construct
an EXPLICIT additive calibration field which has defect -a on
EVERY real physical flag, for any chosen coefficient a in an
additive commutative group. It cannot be gauged flat if a is
nonzero, and its gauge class is distinct from the zero field.

This example is a CHOSEN C60 incidence calibration, not the
historical F55 charge/odd phase or an asserted Yang--Mills
physical connection. It demonstrates an actual nonflat orbit
in the new gauge presentation without changing the original
60/90/32 geometry or inventing a 4-gon face.

No Gray, new logical axiom, sorry, admit, arbitrary graph-coherence
substitute, or deletion of any earlier theorem/public root.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u
variable {A : Type u} [AddCommGroup A]

/-- A selected calibration assigning a to the GENUINE original
direct dart-to-face incidence and 0 elsewhere. This uses only
existing comparable sites of the real C60 physical source. -/
def nativeC60DiagonalIncidenceGaugeField (a : A) :
    NativeC60IncidenceGaugeField A :=
  fun s t _ =>
    match s, t with
    | .vertex _, .face _ => a
    | _, _ => 0

/-- All 360 existing original physical flags have exact defect -a.
The true two-step dart-to-edge-to-face route has grade 0,
and the distinct original direct dart-to-face route has grade a.
No equality of these genuinely different raw source paths is assumed. -/
theorem nativeC60DiagonalIncidenceGaugeField_flagCurvature
    (a : A) (e : Edge) (endpoint faceSide : Bool) :
    nativeC60FlagGaugeCurvature
      (nativeC60DiagonalIncidenceGaugeField a) e endpoint faceSide = -a := by
  simp [nativeC60FlagGaugeCurvature, nativeC60GaugeIntegral,
    nativeC60DiagonalIncidenceGaugeField, flagRawTwoStep, flagRawDiagonal]

/-- The trivial incidence connection has zero defect on every
real flag, with no assumption that arbitrary fields are flat. -/
theorem nativeC60ZeroIncidenceGaugeField_flagCurvature
    (e : Edge) (endpoint faceSide : Bool) :
    nativeC60FlagGaugeCurvature
      (fun _ _ _ => (0 : A)) e endpoint faceSide = 0 := by
  simp [nativeC60FlagGaugeCurvature, nativeC60GaugeIntegral,
    flagRawTwoStep, flagRawDiagonal]

/-- Exact source-level notion of flatness on ALL physical flags.
This is stronger than asserting equality of endpoints and does
NOT change the original physical polygon face holonomies. -/
def NativeC60FlagFlat (field : NativeC60IncidenceGaugeField A) : Prop :=
  ∀ (e : Edge) (endpoint faceSide : Bool),
    nativeC60FlagGaugeCurvature field e endpoint faceSide = 0

/-- Flag flatness is preserved and reflected by every actual
local gauge transformation at the original 182 physical sites. -/
theorem nativeC60FlagFlat_gauge_iff
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A) :
    NativeC60FlagFlat (nativeC60GaugeTransform field phi) ↔
      NativeC60FlagFlat field := by
  simp only [NativeC60FlagFlat, nativeC60FlagGaugeCurvature_invariant]

/-- If the selected calibration value is nonzero, not even one
physical flag can be made flat by a mere change of local frame. -/
theorem nativeC60DiagonalGauge_nonflat_under_every_frame
    (a : A) (ha : a ≠ 0)
    (phi : NativeC60LocalGauge A)
    (e : Edge) (endpoint faceSide : Bool) :
    nativeC60FlagGaugeCurvature
      (nativeC60GaugeTransform
        (nativeC60DiagonalIncidenceGaugeField a) phi)
        e endpoint faceSide ≠ 0 := by
  rw [nativeC60FlagGaugeCurvature_invariant,
    nativeC60DiagonalIncidenceGaugeField_flagCurvature]
  exact fun h => ha (neg_eq_zero.mp h)

/-- Existing arbitrary-site gauge equivalence cannot erase the
nonzero flag curvature of this concrete C60 calibration field. -/
theorem nativeC60DiagonalGauge_not_equivalent_zero
    (a : A) (ha : a ≠ 0) :
    ¬ nativeC60GaugeEquivalent
      (nativeC60DiagonalIncidenceGaugeField a)
      (fun _ _ _ => (0 : A)) := by
  intro h
  rcases h with ⟨phi, hphi⟩
  let e : Edge := .cross (.northSpoke (0 : Ring))
  have heq := congrArg
    (fun field : NativeC60IncidenceGaugeField A =>
      nativeC60FlagGaugeCurvature field e false false) hphi
  have hzero :
      nativeC60FlagGaugeCurvature
        (fun _ _ _ => (0 : A)) e false false = 0 :=
    nativeC60ZeroIncidenceGaugeField_flagCurvature e false false
  rw [hzero, nativeC60FlagGaugeCurvature_invariant,
    nativeC60DiagonalIncidenceGaugeField_flagCurvature] at heq
  exact ha (neg_eq_zero.mp heq.symm)

/-- The original 360 flag curvatures are functions on actual
gauge classes. Quotient descent follows from an actual
gauge-invariance proof, not from graph connectivity. -/
def nativeC60GaugeClassFlagCurvature
    (e : Edge) (endpoint faceSide : Bool) :
    NativeC60GaugeClasses A → A :=
  Quotient.lift
    (fun field => nativeC60FlagGaugeCurvature field e endpoint faceSide)
    (by
      intro field next h
      rcases h with ⟨phi, rfl⟩
      exact (nativeC60FlagGaugeCurvature_invariant
        field phi e endpoint faceSide).symm)

/-- A complete spec for evaluating the gauge-class flag
curvature on the chosen ORIGINAL field representative. -/
theorem nativeC60GaugeClassFlagCurvature_spec
    (field : NativeC60IncidenceGaugeField A)
    (e : Edge) (endpoint faceSide : Bool) :
    nativeC60GaugeClassFlagCurvature e endpoint faceSide
      (Quotient.mk (nativeC60GaugeSetoid (A := A)) field) =
        nativeC60FlagGaugeCurvature field e endpoint faceSide := rfl

/-- Two genuine physical gauge orbits are DISTINGUISHED by any
one actual C60 flag whenever a ≠ 0; this is stronger than
merely observing that their raw field terms differ. -/
theorem nativeC60DiagonalGaugeClass_ne_zero
    (a : A) (ha : a ≠ 0) :
    (Quotient.mk (nativeC60GaugeSetoid (A := A))
        (nativeC60DiagonalIncidenceGaugeField a)) ≠
      (Quotient.mk (nativeC60GaugeSetoid (A := A))
        (fun _ _ _ => (0 : A))) := by
  intro h
  let e : Edge := .cross (.northSpoke (0 : Ring))
  have hc := congrArg
    (nativeC60GaugeClassFlagCurvature (A := A) e false false) h
  rw [nativeC60GaugeClassFlagCurvature_spec,
    nativeC60GaugeClassFlagCurvature_spec,
    nativeC60DiagonalIncidenceGaugeField_flagCurvature,
    nativeC60ZeroIncidenceGaugeField_flagCurvature] at hc
  exact ha (neg_eq_zero.mp hc)

/-- Explicit integral calibration: -1 occurs on each of the
original 360 true physical flags in the nontrivial gauge orbit. -/
theorem nativeC60IntegerDiagonalGauge_flagCurvature
    (e : Edge) (endpoint faceSide : Bool) :
    nativeC60FlagGaugeCurvature
      (nativeC60DiagonalIncidenceGaugeField (1 : ℤ))
      e endpoint faceSide = -1 := by
  exact nativeC60DiagonalIncidenceGaugeField_flagCurvature
    (1 : ℤ) e endpoint faceSide

/-- The ZMod5 Qi phase coefficient is an equally valid independent
native C60 gauge *test connection*: no historical pentagram
Quiver or Gray semantics is imported or identified. -/
theorem nativeC60QiDiagonalGauge_class_nontrivial :
    (Quotient.mk (nativeC60GaugeSetoid (A := ZMod 5))
        (nativeC60DiagonalIncidenceGaugeField (1 : ZMod 5))) ≠
      (Quotient.mk (nativeC60GaugeSetoid (A := ZMod 5))
        (fun _ _ _ => (0 : ZMod 5))) := by
  exact nativeC60DiagonalGaugeClass_ne_zero (1 : ZMod 5) (by decide)

#print axioms nativeC60DiagonalIncidenceGaugeField_flagCurvature
#print axioms nativeC60ZeroIncidenceGaugeField_flagCurvature
#print axioms nativeC60FlagFlat_gauge_iff
#print axioms nativeC60DiagonalGauge_nonflat_under_every_frame
#print axioms nativeC60DiagonalGauge_not_equivalent_zero
#print axioms nativeC60GaugeClassFlagCurvature
#print axioms nativeC60GaugeClassFlagCurvature_spec
#print axioms nativeC60DiagonalGaugeClass_ne_zero
#print axioms nativeC60IntegerDiagonalGauge_flagCurvature
#print axioms nativeC60QiDiagonalGauge_class_nontrivial

end
end Kuu.F112.Physical
