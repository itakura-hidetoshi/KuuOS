import KUOS.DependentOriginationStageIIObstructionClassV4_12
import KUOS.DependentOriginationHexagramInnerHexagonV3_88
import KUOS.DependentOriginationPentagramInnerPentagonV3_89
import Mathlib

namespace KUOS.DependentOriginationPentagramHexagramParityV4_13

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationPentagramInnerPentagonV3_89
open KUOS.DependentOriginationStageIIObstructionClassV4_12

open scoped BigOperators

set_option autoImplicit false

noncomputable section

/-!
# Uniform pentagram/hexagram parity test v4.13

v4.12 produces a transport-independent nonzero Stage-II obstruction class

  omega(T) = 1 in ZMod 2.

The pentagram and hexagram carriers have respectively five and six inner
crossings.  This file tests the simplest fully symmetric transport rule:
put the same obstruction class omega(T) on every inner crossing and sum around
the inner boundary.

The finite sums are evaluated directly on the actual crossing types.

* five copies of one sum to one;
* six copies of one sum to zero.

Thus the pentagram preserves the odd class under uniform placement, while the
hexagram annihilates it.  A nonzero recursive obstruction on the hexagram
therefore cannot be represented by a constant symmetric crossing decoration;
it needs a nonuniform/distinguished seam or richer coefficient data.
-/

/-- Uniform Stage-II obstruction total on the six hexagram crossings. -/
noncomputable def hexagramUniformStageIIObstructionTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  ∑ _ : HexagramInnerVertex, counterStageIIObstructionAdd T

/-- Six identical nonzero ZMod-2 classes cancel. -/
theorem hexagramUniformStageIIObstructionTotal_eq_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    hexagramUniformStageIIObstructionTotal T = 0 := by
  simp only [hexagramUniformStageIIObstructionTotal,
    counterStageIIObstructionAdd_eq_one]
  native_decide

/-- Uniform Stage-II obstruction total on the five pentagram crossings. -/
noncomputable def pentagramUniformStageIIObstructionTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  ∑ _ : PentagramInnerVertex, counterStageIIObstructionAdd T

/-- Five identical nonzero ZMod-2 classes retain the odd class. -/
theorem pentagramUniformStageIIObstructionTotal_eq_one
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    pentagramUniformStageIIObstructionTotal T = 1 := by
  simp only [pentagramUniformStageIIObstructionTotal,
    counterStageIIObstructionAdd_eq_one]
  native_decide

/-- The pentagram uniform total exactly reproduces the Stage-II obstruction. -/
theorem pentagramUniformStageIIObstructionTotal_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    pentagramUniformStageIIObstructionTotal T =
      counterStageIIObstructionAdd T := by
  rw [pentagramUniformStageIIObstructionTotal_eq_one,
    counterStageIIObstructionAdd_eq_one]

/-- The hexagram uniform total cannot reproduce the nonzero Stage-II
obstruction. -/
theorem hexagramUniformStageIIObstructionTotal_ne_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    hexagramUniformStageIIObstructionTotal T ≠
      counterStageIIObstructionAdd T := by
  rw [hexagramUniformStageIIObstructionTotal_eq_zero,
    counterStageIIObstructionAdd_eq_one]
  exact zero_ne_one

/-- Combined local parity contrast of the two recursive star carriers. -/
theorem uniformStageIIObstruction_pentagram_hexagram_contrast
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    pentagramUniformStageIIObstructionTotal T =
        counterStageIIObstructionAdd T ∧
      hexagramUniformStageIIObstructionTotal T ≠
        counterStageIIObstructionAdd T := by
  exact
    ⟨pentagramUniformStageIIObstructionTotal_eq_obstruction T,
      hexagramUniformStageIIObstructionTotal_ne_obstruction T⟩

/-!
## Boundary after v4.13

Uniform ZMod-2 crossing transport distinguishes the two recursive carriers:

  pentagram: 5 * omega = omega,
  hexagram:  6 * omega = 0.

Therefore the local odd/even contrast is now formal and tied to the actual
finite crossing types, not only to an informal side-count argument.

This does not yet prove a recursive obstruction theorem for the full truncated
icosahedron.  In particular, the hexagram result shows that constant symmetric
crossing data are insufficient.  The next nontrivial step is to define an
authority-bounded nonuniform seam from the comparison obstruction itself, or
to move to coefficient data that retain the crossing distinction without
mod-2 cancellation.
-/

end

end KUOS.DependentOriginationPentagramHexagramParityV4_13
