import KUOS.DependentOriginationPentagramHexagramParityV4_13
import KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
import Mathlib

namespace KUOS.DependentOriginationTruncatedIcosahedralGlobalParityV4_14

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationPentagramHexagramParityV4_13

set_option autoImplicit false

noncomputable section

/-!
# Global truncated-icosahedral parity test v4.14

v4.13 proves the local uniform-crossing rule

  pentagram: five copies of omega retain omega,
  hexagram:  six copies of omega cancel to zero.

The truncated icosahedron contains 12 pentagonal faces and 20 hexagonal faces.
This file sums those local uniform contributions over the actual face
multiplicities.

Because both face multiplicities are even, the global constant face-type
weighting vanishes in ZMod 2 even though one pentagonal face locally preserves
the obstruction.

Thus a nonzero global recursive obstruction cannot be represented by assigning
the same Stage-II class uniformly to every crossing of every face.
-/

/-- Total contribution of the 12 pentagonal faces under uniform local
crossing decoration. -/
noncomputable def truncatedIcosahedralUniformPentagonContribution
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  truncatedIcosahedralFaceMultiplicity .pentagon •
    pentagramUniformStageIIObstructionTotal T

/-- Total contribution of the 20 hexagonal faces under uniform local crossing
decoration. -/
noncomputable def truncatedIcosahedralUniformHexagonContribution
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  truncatedIcosahedralFaceMultiplicity .hexagon •
    hexagramUniformStageIIObstructionTotal T

/-- Twelve locally surviving pentagonal contributions cancel globally mod 2. -/
theorem truncatedIcosahedralUniformPentagonContribution_eq_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    truncatedIcosahedralUniformPentagonContribution T = 0 := by
  rw [truncatedIcosahedralUniformPentagonContribution,
    pentagramUniformStageIIObstructionTotal_eq_one]
  native_decide

/-- Every hexagonal local contribution is already zero, so the whole hexagon
family contributes zero. -/
theorem truncatedIcosahedralUniformHexagonContribution_eq_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    truncatedIcosahedralUniformHexagonContribution T = 0 := by
  rw [truncatedIcosahedralUniformHexagonContribution,
    hexagramUniformStageIIObstructionTotal_eq_zero]
  simp

/-- Global face-type-uniform Stage-II obstruction total. -/
noncomputable def truncatedIcosahedralUniformStageIIObstructionTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  truncatedIcosahedralUniformPentagonContribution T +
    truncatedIcosahedralUniformHexagonContribution T

/-- The global constant face-type weighting vanishes. -/
theorem truncatedIcosahedralUniformStageIIObstructionTotal_eq_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    truncatedIcosahedralUniformStageIIObstructionTotal T = 0 := by
  rw [truncatedIcosahedralUniformStageIIObstructionTotal,
    truncatedIcosahedralUniformPentagonContribution_eq_zero,
    truncatedIcosahedralUniformHexagonContribution_eq_zero]
  exact zero_add 0

/-- Therefore the global uniform truncated-icosahedral total cannot represent
the nonzero Stage-II obstruction class. -/
theorem truncatedIcosahedralUniformStageIIObstructionTotal_ne_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    truncatedIcosahedralUniformStageIIObstructionTotal T ≠
      counterStageIIObstructionAdd T := by
  rw [truncatedIcosahedralUniformStageIIObstructionTotal_eq_zero,
    counterStageIIObstructionAdd_eq_one]
  exact zero_ne_one

/-- Local-vs-global contrast: one pentagram preserves omega, while the complete
uniform truncated-icosahedral face family loses it. -/
theorem pentagram_local_survives_but_global_uniform_vanishes
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    pentagramUniformStageIIObstructionTotal T =
        counterStageIIObstructionAdd T ∧
      truncatedIcosahedralUniformStageIIObstructionTotal T = 0 := by
  exact
    ⟨pentagramUniformStageIIObstructionTotal_eq_obstruction T,
      truncatedIcosahedralUniformStageIIObstructionTotal_eq_zero T⟩

/-!
## Boundary after v4.14

The parity obstruction now has both local and global carrier tests.

Locally:
* pentagram preserves the odd class;
* hexagram kills a constant symmetric class.

Globally:
* 12 pentagons contribute an even number of surviving local classes;
* 20 hexagons contribute zero;
* hence the uniform face-type total vanishes.

Therefore any nonzero recursive obstruction on the full truncated icosahedron
must break this uniformity.  It needs a distinguished/nonuniform cocycle,
orientation-sensitive incidence data, or a richer coefficient system.

This formally confirms that local 5-vs-6 parity alone is insufficient as a
global obstruction.
-/

end

end KUOS.DependentOriginationTruncatedIcosahedralGlobalParityV4_14
