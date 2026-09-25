import KUOS.DependentOriginationSingleFaceSupportV4_15
import KUOS.DependentOriginationStageIIObstructionClassV4_12
import Mathlib

namespace KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12

set_option autoImplicit false

noncomputable section

/-!
# Explicit eight-face Stage-II parity carrier v4.16

The transport-independent Stage-II obstruction of v4.12 is the mismatch between

* the odd raw octahedral parity demand;
* the even sum of eight quotient-compositor face scalars.

Before transporting that class onto a larger recursive carrier, the eight
contributing faces should themselves be represented by an explicit finite
carrier independent of any HigherLocalizationFactorization.

This file introduces exactly those eight labels and attaches the corresponding
coherent-transport scalar to each label.

No truncated-icosahedral placement is chosen here.
-/

/-- The eight octahedral faces appearing in the Stage-II parity equation. -/
inductive OctahedralStageIIParityFace
  | a00b00
  | a01b10
  | a00b01
  | a01b11
  | a10b00
  | a11b10
  | a10b01
  | a11b11
  deriving DecidableEq, Repr, Fintype

@[simp] theorem octahedralStageIIParityFace_card :
    Fintype.card OctahedralStageIIParityFace = 8 := by
  native_decide

/-- Scalar carried by one of the eight parity faces. -/
noncomputable def counterTransportParityFaceAdd
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    OctahedralStageIIParityFace → ZMod 2
  | .a00b00 =>
      Multiplicative.toAdd (counterTransportCompScalar T a00 b00)
  | .a01b10 =>
      Multiplicative.toAdd (counterTransportCompScalar T a01 b10)
  | .a00b01 =>
      Multiplicative.toAdd (counterTransportCompScalar T a00 b01)
  | .a01b11 =>
      Multiplicative.toAdd (counterTransportCompScalar T a01 b11)
  | .a10b00 =>
      Multiplicative.toAdd (counterTransportCompScalar T a10 b00)
  | .a11b10 =>
      Multiplicative.toAdd (counterTransportCompScalar T a11 b10)
  | .a10b01 =>
      Multiplicative.toAdd (counterTransportCompScalar T a10 b01)
  | .a11b11 =>
      Multiplicative.toAdd (counterTransportCompScalar T a11 b11)

/-- Explicit total of the eight-face carrier, in the same order as v3.69. -/
noncomputable def counterTransportParityCarrierTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  counterTransportParityFaceAdd T .a00b00 +
    counterTransportParityFaceAdd T .a01b10 +
    counterTransportParityFaceAdd T .a00b01 +
    counterTransportParityFaceAdd T .a01b11 +
    counterTransportParityFaceAdd T .a10b00 +
    counterTransportParityFaceAdd T .a11b10 +
    counterTransportParityFaceAdd T .a10b01 +
    counterTransportParityFaceAdd T .a11b11

/-- The explicit finite carrier total is exactly the named v4.12 transport
parity. -/
theorem counterTransportParityCarrierTotal_eq_faceParityAdd
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportParityCarrierTotal T =
      counterTransportFaceParityAdd T := by
  rfl

/-- Every coherent quotient transport has even eight-face carrier total. -/
theorem counterTransportParityCarrierTotal_eq_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportParityCarrierTotal T = 0 := by
  rw [counterTransportParityCarrierTotal_eq_faceParityAdd]
  exact counterTransportFaceParityAdd_eq_zero T

/-- A successful comparison would force the same eight-face carrier total to
be the odd class one. -/
theorem counterComparisonDataAt_forces_parityCarrierTotal_eq_one
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T) :
    (1 : ZMod 2) = counterTransportParityCarrierTotal T := by
  rw [counterTransportParityCarrierTotal_eq_faceParityAdd]
  exact counterComparison_forces_transport_faceParity T C

/-- Mismatch class read directly from the explicit eight-face carrier. -/
noncomputable def counterStageIIParityCarrierMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  1 + counterTransportParityCarrierTotal T

/-- The explicit carrier mismatch is definitionally the v4.12 Stage-II
obstruction class. -/
theorem counterStageIIParityCarrierMismatch_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIParityCarrierMismatch T =
      counterStageIIObstructionAdd T := by
  rfl

/-- Therefore the explicit eight-face mismatch is nonzero. -/
theorem counterStageIIParityCarrierMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIParityCarrierMismatch T ≠ 0 := by
  rw [counterStageIIParityCarrierMismatch_eq_obstruction]
  exact counterStageIIObstructionAdd_ne_zero T

/-!
## Boundary after v4.16

The pre-factorization obstruction now has an explicit eight-element carrier.

This separates two questions cleanly:

1. algebraic truth:
   the eight-face carrier has even transport total and nonzero raw/transport
   mismatch;
2. geometric transport:
   how those eight labeled parity faces should be placed on a larger recursive
   carrier.

The second question is not answered by cardinality alone.  A placement into the
32 truncated-icosahedral seed faces can be constructed combinatorially, but an
authority-bounded placement must be justified by incidence/coherence data.
-/

end

end KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
