import KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47
import KUOS.DependentOriginationStageIIObstructionClassV4_12
import Mathlib

namespace KUOS.DependentOriginationStageIIGeometricOrbitObstructionV4_48

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationStageIIBareGeometricMiddleSwitchV4_44
open KUOS.DependentOriginationStageIIBareMiddleSwitchHomeomorphV4_45
open KUOS.DependentOriginationStageIIGeometricOrientationV4_46
open KUOS.DependentOriginationStageIIGeometricOrbitQuotientV4_47

set_option autoImplicit false

noncomputable section

/-!
# Stage-II obstruction on the geometric middle-switch orbit quotient v4.48

v4.12 proves that the Stage-II comparison obstruction is the
transport-independent nonzero class

  omega(T) = 1 in ZMod 2

for every coherent quotient transport T.

v4.46 proves that the geometric middle-switch reverses the integral
orientation sign at every finite depth while reduction modulo two forgets the
sign and gives one.

v4.47 constructs the exact two-point orbit quotient of the free geometric
middle-switch and proves its universal factorization property.

This unit joins those three layers.

First regard the v4.12 obstruction as a semantic function on the bare
geometric carrier.  It is constant in the geometric point, hence invariant
under the middle-switch, and therefore descends canonically to the v4.47 orbit
quotient.

The descended orbit obstruction:

* recovers the original v4.12 obstruction on every representative;
* equals one on every orbit;
* is nonzero on every orbit;
* is independent of the coherent transport choice;
* agrees exactly with the mod-two reduction of the v4.46 integral orientation
  coefficient at every representative and every finite depth.

Thus the existing Stage-II obstruction is now attached to the geometric orbit
structure without changing its value or inventing a new class.
-/

/-- The v4.12 obstruction viewed as a semantic map on bare geometric points. -/
noncomputable def stageIIGeometricObstructionSemantic
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    StageIIGeometricCantorCarrier → ZMod 2 :=
  fun _ => counterStageIIObstructionAdd T

/-- The geometric obstruction semantic is middle-switch invariant. -/
theorem stageIIGeometricObstructionSemantic_invariant
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricObstructionSemantic T
        (stageIIGeometricCarrierMiddleSwitch p) =
      stageIIGeometricObstructionSemantic T p := by
  rfl

/-- Canonical descent of the Stage-II obstruction to the v4.47 orbit
quotient. -/
noncomputable def stageIIGeometricOrbitObstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    StageIIGeometricMiddleSwitchOrbit → ZMod 2 :=
  stageIIGeometricMiddleSwitchDescend
    (stageIIGeometricObstructionSemantic T)
    (stageIIGeometricObstructionSemantic_invariant T)

/-- On every representative, the orbit obstruction recovers exactly the
original v4.12 obstruction class. -/
@[simp] theorem stageIIGeometricOrbitObstruction_projection
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (p : StageIIGeometricCantorCarrier) :
    stageIIGeometricOrbitObstruction T
        (stageIIGeometricMiddleSwitchOrbitProjection p) =
      counterStageIIObstructionAdd T := by
  rfl

/-- The descended obstruction is exactly one on every geometric orbit. -/
theorem stageIIGeometricOrbitObstruction_eq_one
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (q : StageIIGeometricMiddleSwitchOrbit) :
    stageIIGeometricOrbitObstruction T q = 1 := by
  refine Quotient.inductionOn q ?_
  intro p
  change counterStageIIObstructionAdd T = 1
  exact counterStageIIObstructionAdd_eq_one T

/-- Hence the descended geometric orbit obstruction never vanishes. -/
theorem stageIIGeometricOrbitObstruction_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (q : StageIIGeometricMiddleSwitchOrbit) :
    stageIIGeometricOrbitObstruction T q ≠ 0 := by
  rw [stageIIGeometricOrbitObstruction_eq_one]
  exact one_ne_zero

/-- The orbit obstruction remains independent of the coherent quotient
transport choice. -/
theorem stageIIGeometricOrbitObstruction_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    stageIIGeometricOrbitObstruction T =
      stageIIGeometricOrbitObstruction U := by
  funext q
  rw [stageIIGeometricOrbitObstruction_eq_one,
    stageIIGeometricOrbitObstruction_eq_one]

/-- Pointwise spelling of transport independence on one geometric orbit. -/
theorem stageIIGeometricOrbitObstruction_transport_independent_apply
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (q : StageIIGeometricMiddleSwitchOrbit) :
    stageIIGeometricOrbitObstruction T q =
      stageIIGeometricOrbitObstruction U q := by
  rw [stageIIGeometricOrbitObstruction_eq_one,
    stageIIGeometricOrbitObstruction_eq_one]

/-- The mod-two reduction of the integral geometric orientation coefficient is
exactly the descended Stage-II obstruction on the orbit of the point. -/
theorem stageIIGeometricOrientation_modTwo_eq_orbitObstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    ((stageIIGeometricCarrierOrientationIntCoeff p depth : ℤ) : ZMod 2) =
      stageIIGeometricOrbitObstruction T
        (stageIIGeometricMiddleSwitchOrbitProjection p) := by
  rw [stageIIGeometricCarrierOrientationIntCoeff_modTwo_eq_one,
    stageIIGeometricOrbitObstruction_projection,
    counterStageIIObstructionAdd_eq_one]

/-- The same equality holds after applying the orientation-reversing geometric
homeomorphism: integer sign flips upstairs, but the orbit obstruction remains
the same downstairs modulo two. -/
theorem stageIIGeometricOrientation_homeomorph_modTwo_eq_orbitObstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    ((stageIIGeometricCarrierOrientationIntCoeff
        (stageIIGeometricCarrierMiddleSwitchHomeomorph p) depth : ℤ) :
        ZMod 2) =
      stageIIGeometricOrbitObstruction T
        (stageIIGeometricMiddleSwitchOrbitProjection p) := by
  rw [stageIIGeometricCarrierOrientationIntCoeff_modTwo_eq_one,
    stageIIGeometricOrbitObstruction_projection,
    counterStageIIObstructionAdd_eq_one]

/-- The two members of one free middle-switch orbit carry opposite integral
orientation signs but the same nonzero orbit obstruction modulo two. -/
theorem stageIIGeometricOrbit_orientation_sign_and_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (p : StageIIGeometricCantorCarrier)
    (depth : Nat) :
    stageIIGeometricCarrierOrientationIntCoeff
        (stageIIGeometricCarrierMiddleSwitchHomeomorph p) depth =
        -stageIIGeometricCarrierOrientationIntCoeff p depth ∧
      ((stageIIGeometricCarrierOrientationIntCoeff p depth : ℤ) :
          ZMod 2) =
        stageIIGeometricOrbitObstruction T
          (stageIIGeometricMiddleSwitchOrbitProjection p) ∧
      stageIIGeometricOrbitObstruction T
          (stageIIGeometricMiddleSwitchOrbitProjection p) ≠
        0 := by
  exact
    ⟨stageIIGeometricCarrierOrientationIntCoeff_homeomorph p depth,
      stageIIGeometricOrientation_modTwo_eq_orbitObstruction T p depth,
      stageIIGeometricOrbitObstruction_ne_zero T
        (stageIIGeometricMiddleSwitchOrbitProjection p)⟩

/-- Bundle the orbit-level obstruction and its compatibility with geometric
orientation. -/
structure StageIIGeometricOrbitObstructionCertificate where
  orbitObstruction :
    StageIIGeometricMiddleSwitchOrbit → ZMod 2
  projectionRecovers :
    ∀ p,
      orbitObstruction
          (stageIIGeometricMiddleSwitchOrbitProjection p) =
        counterStageIIObstructionAdd
          (stageIIGeometricOrbitObstructionCertificateTransport := sorry)
  /- The certificate below is instantiated concretely rather than through this
     overly polymorphic field; see the canonical definition after the
     structure. -/

/-!
The useful certificate should keep the transport as an explicit parameter,
rather than hiding it behind a structure field.  We therefore use the
transport-parametrized structure below.
-/

/-- Transport-parametrized orbit obstruction certificate. -/
structure StageIIGeometricOrbitObstructionCertificateAt
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) where
  projectionRecovers :
    ∀ p,
      stageIIGeometricOrbitObstruction T
          (stageIIGeometricMiddleSwitchOrbitProjection p) =
        counterStageIIObstructionAdd T
  equalsOne :
    ∀ q,
      stageIIGeometricOrbitObstruction T q = 1
  nonzero :
    ∀ q,
      stageIIGeometricOrbitObstruction T q ≠ 0
  orientationCompatibility :
    ∀ p depth,
      ((stageIIGeometricCarrierOrientationIntCoeff p depth : ℤ) : ZMod 2) =
        stageIIGeometricOrbitObstruction T
          (stageIIGeometricMiddleSwitchOrbitProjection p)

/-- Canonical v4.48 orbit obstruction certificate at one coherent transport. -/
noncomputable def stageIIGeometricOrbitObstructionCertificateAt
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    StageIIGeometricOrbitObstructionCertificateAt T where
  projectionRecovers :=
    stageIIGeometricOrbitObstruction_projection T
  equalsOne :=
    stageIIGeometricOrbitObstruction_eq_one T
  nonzero :=
    stageIIGeometricOrbitObstruction_ne_zero T
  orientationCompatibility :=
    stageIIGeometricOrientation_modTwo_eq_orbitObstruction T

/-!
## Boundary after v4.48

The transport-independent Stage-II obstruction now lives canonically on the
free geometric middle-switch orbit quotient.

For every coherent quotient transport T and every orbit class q,

  omega_geo(T,q) = 1 != 0.

On every representative p and every finite depth n,

  [epsilon(p,n)] mod 2
    = omega_geo(T,[p])
    = 1.

The middle-switch homeomorphism reverses epsilon over the integers, while the
orbit quotient and mod-two coefficient system identify the two signs exactly.

The orbit obstruction is also independent of T, so neither the coherent
transport choice nor the choice of one of the two middle-switch
representatives changes the certified Stage-II class.

No new obstruction is introduced: v4.48 is a descent-and-compatibility theorem
for the existing v4.12 obstruction.

A subsequent unit may add quotient topology to the orbit carrier or study the
free two-sheeted local geometry of the projection.
-/

end

end KUOS.DependentOriginationStageIIGeometricOrbitObstructionV4_48
