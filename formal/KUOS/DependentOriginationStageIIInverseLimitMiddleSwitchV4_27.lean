import KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26
import Mathlib

namespace KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
open KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
open KUOS.DependentOriginationStageIIFiniteDepthRecursiveTransportV4_24
open KUOS.DependentOriginationStageIICoherentFiniteDepthTowerV4_25
open KUOS.DependentOriginationStageIISetTheoreticInverseLimitV4_26

set_option autoImplicit false

noncomputable section

/-!
# Middle-switch involution on the Stage-II inverse-limit carrier v4.27

v4.26 proves that the set-theoretic inverse limit of the supported finite-depth
tower is equivalent to the original eight-label Stage-II carrier.

The eight source labels already carry the fixed-point-free middle-switch mate
involution from v4.19.  This file transports that involution across the v4.26
equivalence and proves that its finite-depth incidence/orientation semantics are
preserved on every inverse-limit section.

No new topology or metric structure is introduced.  The construction is
entirely set-theoretic: the inverse-limit mate is conjugate to the source mate
through the established carrier equivalence.
-/

/-- Source label underlying one inverse-limit point. -/
noncomputable def stageIIInverseLimitSource
    (x : StageIIFiniteDepthInverseLimit) :
    OctahedralStageIIParityFace :=
  octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.symm x

/-- Every inverse-limit point is the canonical tower of its recovered source
label. -/
theorem stageIIInverseLimit_eq_canonical_source
    (x : StageIIFiniteDepthInverseLimit) :
    octahedralStageIIParityFaceEquivFiniteDepthInverseLimit
        (stageIIInverseLimitSource x) = x := by
  exact
    octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.apply_symm_apply x

/-- Evaluation of an arbitrary inverse-limit point at a finite depth is the
canonical tower cell of its recovered source label. -/
theorem stageIIInverseLimit_apply_eq_sourceTower
    (x : StageIIFiniteDepthInverseLimit)
    (depth : Nat) :
    x.1 depth =
      octahedralStageIIFiniteDepthTower
        (stageIIInverseLimitSource x) depth := by
  have h :=
    congrArg
      (fun y : StageIIFiniteDepthInverseLimit => y.1 depth)
      (stageIIInverseLimit_eq_canonical_source x)
  exact h.symm

/-- Transport the v4.19 middle-switch mate involution to the inverse-limit
carrier by conjugation through the v4.26 equivalence. -/
noncomputable def stageIIInverseLimitMate
    (x : StageIIFiniteDepthInverseLimit) :
    StageIIFiniteDepthInverseLimit :=
  octahedralStageIIParityFaceEquivFiniteDepthInverseLimit
    (octahedralStageIIMiddleSwitchMate
      (stageIIInverseLimitSource x))

/-- The recovered source of the inverse-limit mate is exactly the source mate. -/
@[simp] theorem stageIIInverseLimitSource_mate
    (x : StageIIFiniteDepthInverseLimit) :
    stageIIInverseLimitSource (stageIIInverseLimitMate x) =
      octahedralStageIIMiddleSwitchMate
        (stageIIInverseLimitSource x) := by
  simp [stageIIInverseLimitSource, stageIIInverseLimitMate]

/-- On canonical inverse-limit points, the transported mate agrees exactly with
the source-level middle-switch mate. -/
@[simp] theorem stageIIInverseLimitMate_canonical
    (f : OctahedralStageIIParityFace) :
    stageIIInverseLimitMate
        (octahedralStageIIParityFaceEquivFiniteDepthInverseLimit f) =
      octahedralStageIIParityFaceEquivFiniteDepthInverseLimit
        (octahedralStageIIMiddleSwitchMate f) := by
  simp [stageIIInverseLimitMate, stageIIInverseLimitSource]

/-- The transported inverse-limit mate is involutive. -/
theorem stageIIInverseLimitMate_involutive :
    Function.Involutive stageIIInverseLimitMate := by
  intro x
  apply octahedralStageIIParityFaceEquivFiniteDepthInverseLimit.injective
  simp [stageIIInverseLimitMate, stageIIInverseLimitSource]

/-- Hence the transported mate map is injective. -/
theorem stageIIInverseLimitMate_injective :
    Function.Injective stageIIInverseLimitMate :=
  stageIIInverseLimitMate_involutive.injective

/-- The inverse-limit mate has no fixed points. -/
theorem stageIIInverseLimitMate_ne_self
    (x : StageIIFiniteDepthInverseLimit) :
    stageIIInverseLimitMate x ≠ x := by
  intro h
  have hSource :=
    congrArg stageIIInverseLimitSource h
  have hMate :
      octahedralStageIIMiddleSwitchMate
          (stageIIInverseLimitSource x) =
        stageIIInverseLimitSource x := by
    simpa using hSource
  exact
    octahedralStageIIMiddleSwitchMate_ne_self
      (stageIIInverseLimitSource x) hMate

/-- At every finite depth, the inverse-limit mate evaluates to the canonical
tower cell of the source mate. -/
theorem stageIIInverseLimitMate_apply
    (x : StageIIFiniteDepthInverseLimit)
    (depth : Nat) :
    (stageIIInverseLimitMate x).1 depth =
      octahedralStageIIFiniteDepthTower
        (octahedralStageIIMiddleSwitchMate
          (stageIIInverseLimitSource x)) depth := by
  rw [stageIIInverseLimit_apply_eq_sourceTower,
    stageIIInverseLimitSource_mate]

/-- The parent faces carried by an inverse-limit point and its mate remain an
actual pentagon--hexagon adjacent pair at every finite depth. -/
theorem stageIIInverseLimitMate_parent_adjacent
    (x : StageIIFiniteDepthInverseLimit)
    (depth : Nat) :
    truncatedSeedPentagonHexagonAdjacent
      (x.1 depth).parent.1
      ((stageIIInverseLimitMate x).1 depth).parent.1 := by
  rw [stageIIInverseLimit_apply_eq_sourceTower,
    stageIIInverseLimitMate_apply]
  exact
    octahedralStageIIFiniteDepthTower_mates_parent_adjacent
      depth (stageIIInverseLimitSource x)

/-- The recursive inner face kinds of an inverse-limit point and its mate stay
opposite at every finite depth. -/
theorem stageIIInverseLimitMate_opposite_innerKinds
    (x : StageIIFiniteDepthInverseLimit)
    (depth : Nat) :
    (x.1 depth).innerKind ≠
      ((stageIIInverseLimitMate x).1 depth).innerKind := by
  rw [stageIIInverseLimit_apply_eq_sourceTower,
    stageIIInverseLimitMate_apply]
  exact
    octahedralStageIIFiniteDepthTower_mates_opposite_innerKinds
      depth (stageIIInverseLimitSource x)

/-- Orientation provenance of an inverse-limit mate is flipped at every finite
depth. -/
theorem stageIIInverseLimitMate_orientation_flip
    (x : StageIIFiniteDepthInverseLimit)
    (depth : Nat) :
    stageIIIncidenceRecursiveDepthCellOrientation
        ((stageIIInverseLimitMate x).1 depth) =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceRecursiveDepthCellOrientation
          (x.1 depth)) := by
  rw [stageIIInverseLimit_apply_eq_sourceTower,
    stageIIInverseLimitMate_apply]
  exact
    octahedralStageIIFiniteDepthTower_mates_orientation_flip
      depth (stageIIInverseLimitSource x)

/-- The two members of every inverse-limit mate pair remain distinct at every
finite depth, because each level retains its source parent and the source
placement is injective. -/
theorem stageIIInverseLimitMate_level_ne
    (x : StageIIFiniteDepthInverseLimit)
    (depth : Nat) :
    (stageIIInverseLimitMate x).1 depth ≠ x.1 depth := by
  rw [stageIIInverseLimitMate_apply,
    stageIIInverseLimit_apply_eq_sourceTower]
  exact
    fun h =>
      octahedralStageIIMiddleSwitchMate_ne_self
        (stageIIInverseLimitSource x)
        (octahedralStageIIFiniteDepthTower_injective depth h)

/-!
## Boundary after v4.27

The v4.19 middle-switch pairing now survives passage to the set-theoretic
inverse-limit carrier.

The transported map is:

* defined by conjugating the source mate through the v4.26 carrier equivalence;
* involutive;
* injective;
* fixed-point-free.

At every finite level of every inverse-limit section, mate pairs still retain:

* distinct supported tower cells;
* actual adjacent pentagon--hexagon parent faces;
* opposite recursive inner face kinds;
* flipped orientation provenance.

Thus the infinite compatible-section carrier retains the same two-by-two
middle-switch pairing structure as the finite octahedral source carrier.

This does not identify the transported involution with the independent
invertible 2-cell isotropy exhibited in v4.05.  Such an identification would
require an additional theorem connecting the combinatorial middle-switch action
to that higher-categorical isotropy datum.
-/

end

end KUOS.DependentOriginationStageIIInverseLimitMiddleSwitchV4_27
