import KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib

namespace KUOS.DependentOriginationStageIICurrentHausdorffDimensionZeroV4_28

open MeasureTheory
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26

set_option autoImplicit false

noncomputable section

/-!
# Current Stage-II inverse-limit carrier has Hausdorff dimension zero v4.28

v4.26 proves that the supported compatible-section inverse limit is equivalent
to the original eight-element octahedral Stage-II carrier.

Hausdorff dimension requires an extended metric structure. Rather than choosing
a special metric merely to force a result, this file proves a stronger
statement:

  for every EMetricSpace structure on the current inverse-limit carrier,
  the Hausdorff dimension of the whole carrier is zero.

The reason is intrinsic to the current carrier construction: it is finite.
Mathlib provides Set.Finite.dimH_zero: every finite subset of any extended
metric space has Hausdorff dimension zero.

Thus the zero-dimensionality here is not a metric artifact. It follows from
the rigidity theorem of v4.26 that every compatible infinite-depth section is
completely determined by one of eight source labels.
-/

/-- The current infinite-depth carrier, viewed as the whole v4.26
set-theoretic inverse-limit type. -/
def XInfinityCurrent : Set StageIIFiniteDepthInverseLimit :=
  Set.univ

/-- The v4.26 equivalence with the eight-element source carrier makes the
current inverse-limit type finite. -/
noncomputable instance stageIIFiniteDepthInverseLimitFinite :
    Finite StageIIFiniteDepthInverseLimit :=
  Finite.of_injective
    octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.symm
    octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.symm.injective

/-- A noncomputable Fintype presentation, useful for explicit cardinality
checks but not needed for the Hausdorff-dimension theorem itself. -/
noncomputable instance stageIIFiniteDepthInverseLimitFintype :
    Fintype StageIIFiniteDepthInverseLimit :=
  Fintype.ofFinite StageIIFiniteDepthInverseLimit

/-- The current inverse-limit carrier has exactly eight points. -/
@[simp] theorem stageIIFiniteDepthInverseLimit_card :
    Fintype.card StageIIFiniteDepthInverseLimit = 8 := by
  calc
    Fintype.card StageIIFiniteDepthInverseLimit =
        Fintype.card OctahedralStageIIParityFace :=
      Fintype.card_congr
        octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.symm
    _ = 8 := octahedralStageIIParityFace_card

/-- The whole current carrier is a finite set. -/
theorem XInfinityCurrent_finite :
    XInfinityCurrent.Finite := by
  change (Set.univ : Set StageIIFiniteDepthInverseLimit).Finite
  exact Set.finite_univ

/-- Main current-carrier dimension theorem.

This holds for any extended metric structure on the current carrier because
the carrier itself has only eight points. -/
theorem dimH_XInfinityCurrent_eq_zero
    [EMetricSpace StageIIFiniteDepthInverseLimit] :
    dimH XInfinityCurrent = 0 := by
  exact XInfinityCurrent_finite.dimH_zero

/-- Equivalent whole-space spelling of the same theorem. -/
theorem dimH_current_inverse_limit_univ_eq_zero
    [EMetricSpace StageIIFiniteDepthInverseLimit] :
    dimH (Set.univ : Set StageIIFiniteDepthInverseLimit) = 0 := by
  exact Set.finite_univ.dimH_zero

/-!
## Boundary after v4.28

The current inverse-limit carrier has now acquired a rigorous Hausdorff
dimension statement:

  dim_H(X_{infinity,current}) = 0.

This conclusion is stronger than a statement for one chosen discrete metric:
every legal extended metric structure on the finite current carrier gives the
same zero Hausdorff dimension.

Therefore positive Hausdorff dimension cannot arise by merely re-metrizing
this same eight-point set. A positive-dimensional next carrier must genuinely
retain infinitely many independent branch choices instead of collapsing every
compatible section to one of eight source labels.

The next unit should introduce such a branching carrier together with a metric
whose branch coordinate is not forgotten, and then prove a positive lower
bound on its Hausdorff dimension.
-/

end

end KUOS.DependentOriginationStageIICurrentHausdorffDimensionZeroV4_28
