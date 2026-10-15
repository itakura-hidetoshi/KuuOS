import KUOS.DependentOriginationComparisonObstructionTwoPresentationsV4_11
import KUOS.DependentOriginationArbitraryTransportComparisonV3_69
import Mathlib

namespace KUOS.DependentOriginationStageIIObstructionClassV4_12

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationComparisonObstructionTwoPresentationsV4_11

set_option autoImplicit false

noncomputable section

/-!
# Transport-independent Stage-II obstruction class v4.12

For any coherent quotient transport T on the canonical octahedral countermodel,
v3.69 proves that the sum of the eight quotient-compositor face scalars is zero.
Any successful presentation comparison would force the same sum to equal one.

We package that mismatch as

  omega(T) = 1 + P(T) in ZMod 2,

where P(T) is the eight-face transport parity.

Since P(T)=0 for every coherent T, omega(T)=1 and is nonzero.  Conversely, any
comparison datum would force P(T)=1 and hence omega(T)=0.

Thus omega is a concrete transport-independent pre-factorization obstruction
class.
-/

/-- Eight-face quotient-compositor parity of one coherent quotient transport. -/
noncomputable def counterTransportFaceParityAdd
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  Multiplicative.toAdd (counterTransportCompScalar T a00 b00) +
    Multiplicative.toAdd (counterTransportCompScalar T a01 b10) +
    Multiplicative.toAdd (counterTransportCompScalar T a00 b01) +
    Multiplicative.toAdd (counterTransportCompScalar T a01 b11) +
    Multiplicative.toAdd (counterTransportCompScalar T a10 b00) +
    Multiplicative.toAdd (counterTransportCompScalar T a11 b10) +
    Multiplicative.toAdd (counterTransportCompScalar T a10 b01) +
    Multiplicative.toAdd (counterTransportCompScalar T a11 b11)

/-- v3.69 transport parity theorem in named invariant form. -/
theorem counterTransportFaceParityAdd_eq_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportFaceParityAdd T = 0 := by
  exact counterTransport_faceParity_even T

/-- Stage-II obstruction class: raw odd parity minus transport parity.
In characteristic two subtraction equals addition. -/
noncomputable def counterStageIIObstructionAdd
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  1 + counterTransportFaceParityAdd T

/-- The obstruction class is always the nonzero class one. -/
theorem counterStageIIObstructionAdd_eq_one
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIObstructionAdd T = 1 := by
  rw [counterStageIIObstructionAdd, counterTransportFaceParityAdd_eq_zero]
  exact add_zero 1

/-- Hence the Stage-II obstruction class never vanishes. -/
theorem counterStageIIObstructionAdd_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIObstructionAdd T ≠ 0 := by
  rw [counterStageIIObstructionAdd_eq_one]
  exact one_ne_zero

/-- Any successful comparison datum would force the obstruction class to
vanish. -/
theorem counterComparisonDataAt_forces_stageIIObstruction_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (C : CounterComparisonDataAt T) :
    counterStageIIObstructionAdd T = 0 := by
  unfold counterStageIIObstructionAdd
  unfold counterTransportFaceParityAdd
  rw [← counterComparison_forces_transport_faceParity T C]
  exact CharTwo.add_self_eq_zero 1

/-- Therefore no comparison datum can exist, expressed directly through the
nonzero obstruction class. -/
theorem counterComparisonDataAt_isEmpty
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    IsEmpty (CounterComparisonDataAt T) := by
  constructor
  intro C
  have hZero :=
    counterComparisonDataAt_forces_stageIIObstruction_zero T C
  have hOne :=
    counterStageIIObstructionAdd_eq_one T
  exact one_ne_zero (hOne.symm.trans hZero)

/-- The scalar obstruction class is independent of the chosen coherent
quotient transport. -/
theorem counterStageIIObstructionAdd_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIObstructionAdd T =
      counterStageIIObstructionAdd U := by
  rw [counterStageIIObstructionAdd_eq_one,
    counterStageIIObstructionAdd_eq_one]

/-!
## Boundary after v4.12

The comparison obstruction now has a transport-independent scalar
representative:

  omega(T) = 1 in ZMod 2

for every coherent quotient transport T.

A comparison would force omega(T)=0, so the obstruction is visible entirely
before any HigherLocalizationFactorization exists.

This is the scalar class to transport onto recursive combinatorial carriers.
The next unit tests the simplest symmetric placement of this class on the five
pentagram crossings and six hexagram crossings.
-/

end

end KUOS.DependentOriginationStageIIObstructionClassV4_12
