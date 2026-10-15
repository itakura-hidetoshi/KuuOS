import KUOS.DependentOriginationTruncatedIcosahedralGlobalParityV4_14
import KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
import Mathlib

namespace KUOS.DependentOriginationSingleFaceSupportV4_15

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationTruncatedIcosahedralGlobalParityV4_14

open scoped BigOperators

set_option autoImplicit false

noncomputable section

/-!
# Single-face support as a nonuniform existence test v4.15

v4.14 proves that a face-type-uniform truncated-icosahedral weighting loses the
nonzero Stage-II obstruction globally in ZMod 2.

This file tests the opposite extreme: support the same obstruction class on one
actual seed face and put zero on every other face.

The result is deliberately only an existence theorem for nonuniform support.
No claim is made that the selected face is canonical or authority-bounded.
That selection problem is the next geometric/coherence task.
-/

/-- Put the Stage-II obstruction on one selected truncated-icosahedral seed
face and zero elsewhere. -/
noncomputable def singleSeedFaceStageIIObstructionDecoration
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (selected f : TruncatedIcosahedralSeedFace) : ZMod 2 :=
  if f = selected then counterStageIIObstructionAdd T else 0

/-- Global total of the one-face decoration. -/
noncomputable def singleSeedFaceStageIIObstructionTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (selected : TruncatedIcosahedralSeedFace) : ZMod 2 :=
  ∑ f : TruncatedIcosahedralSeedFace,
    singleSeedFaceStageIIObstructionDecoration T selected f

/-- A singleton support reproduces the obstruction exactly. -/
theorem singleSeedFaceStageIIObstructionTotal_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (selected : TruncatedIcosahedralSeedFace) :
    singleSeedFaceStageIIObstructionTotal T selected =
      counterStageIIObstructionAdd T := by
  classical
  simp [singleSeedFaceStageIIObstructionTotal,
    singleSeedFaceStageIIObstructionDecoration]

/-- Hence every singleton-supported total is nonzero. -/
theorem singleSeedFaceStageIIObstructionTotal_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (selected : TruncatedIcosahedralSeedFace) :
    singleSeedFaceStageIIObstructionTotal T selected ≠ 0 := by
  rw [singleSeedFaceStageIIObstructionTotal_eq_obstruction]
  exact counterStageIIObstructionAdd_ne_zero T

/-- A concrete distinguished pentagonal seed face, used only as a witness. -/
def northPentagonSeedFace : TruncatedIcosahedralSeedFace :=
  .aroundVertex .north

/-- A second pentagonal seed face of the same face kind. -/
def southPentagonSeedFace : TruncatedIcosahedralSeedFace :=
  .aroundVertex .south

@[simp] theorem northPentagonSeedFace_kind :
    truncatedIcosahedralSeedFaceKind northPentagonSeedFace = .pentagon := by
  rfl

@[simp] theorem southPentagonSeedFace_kind :
    truncatedIcosahedralSeedFaceKind southPentagonSeedFace = .pentagon := by
  rfl

/-- Face-kind-uniform decorations take equal values on faces of the same kind. -/
def SeedFaceKindUniform
    (d : TruncatedIcosahedralSeedFace → ZMod 2) : Prop :=
  ∀ f g,
    truncatedIcosahedralSeedFaceKind f =
        truncatedIcosahedralSeedFaceKind g →
      d f = d g

/-- The north-pentagon singleton decoration is genuinely nonuniform even
within the pentagonal face family. -/
theorem northPentagonSingletonDecoration_not_kindUniform
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    ¬ SeedFaceKindUniform
      (singleSeedFaceStageIIObstructionDecoration
        T northPentagonSeedFace) := by
  intro hUniform
  have hEq :=
    hUniform northPentagonSeedFace southPentagonSeedFace (by rfl)
  simp [singleSeedFaceStageIIObstructionDecoration,
    northPentagonSeedFace, southPentagonSeedFace,
    counterStageIIObstructionAdd_eq_one] at hEq

/-- There exists an actual seed-face decoration whose total is the nonzero
Stage-II obstruction and which breaks face-kind uniformity. -/
theorem exists_nonuniform_seedFaceDecoration_preserving_stageIIObstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    ∃ d : TruncatedIcosahedralSeedFace → ZMod 2,
      (∑ f : TruncatedIcosahedralSeedFace, d f) =
          counterStageIIObstructionAdd T ∧
        ¬ SeedFaceKindUniform d := by
  refine
    ⟨singleSeedFaceStageIIObstructionDecoration T northPentagonSeedFace,
      ?_, northPentagonSingletonDecoration_not_kindUniform T⟩
  exact
    singleSeedFaceStageIIObstructionTotal_eq_obstruction
      T northPentagonSeedFace

/-!
## Boundary after v4.15

The global parity picture is now sharp at the purely algebraic carrier level.

* face-type-uniform support loses the obstruction globally;
* a singleton nonuniform support preserves it exactly.

So nonuniformity is sufficient algebraically, but v4.15 intentionally does not
choose a canonical face from the higher-coherence data.

The next theorem unit must replace the arbitrary north-pentagon witness by an
authority-bounded distinguished support derived from the actual Stage-II
comparison obstruction, incidence, orientation, or a proven carrier map.
-/

end

end KUOS.DependentOriginationSingleFaceSupportV4_15
