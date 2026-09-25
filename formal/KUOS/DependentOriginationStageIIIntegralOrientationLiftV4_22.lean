import KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
import Mathlib

namespace KUOS.DependentOriginationStageIIIntegralOrientationLiftV4_22

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationStageIIIncidencePushforwardV4_20
open KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21

set_option autoImplicit false

noncomputable section

/-!
# Integral orientation lift of the Stage-II incidence carrier v4.22

v4.21 proves that ordinary orientation signs collapse in the existing
`ZMod 2` coefficient system:

  +1 = -1 in ZMod 2.

The present file separates two operations that must not be conflated.

1. Each `ZMod 2` scalar has a canonical integer representative supplied by
   `ZMod.cast`.  This is a representative choice, not a ring homomorphism
   from `ZMod 2` to `ℤ`.
2. Orientation is recorded upstairs by the genuinely distinct integer
   coefficients `+1` and `-1`.

The key authority boundary is the theorem `ZMod.intCast_zmod_cast`: reducing
the canonical integer representative back modulo two recovers the original
`ZMod 2` scalar exactly.

Thus the integral carrier remembers ordinary orientation, while reduction
modulo two forgets that sign and returns the already-certified Stage-II
incidence carrier and obstruction class.
-/

/-- Integer-valued orientation sign.  Unlike the v4.21 coefficient in
`ZMod 2`, these two values are genuinely distinct. -/
def stageIIIncidenceOrientationIntCoeff :
    StageIIIncidenceOrientation → ℤ
  | .forward => 1
  | .reverse => -1

@[simp] theorem stageIIIncidenceOrientationIntCoeff_forward :
    stageIIIncidenceOrientationIntCoeff .forward = 1 := rfl

@[simp] theorem stageIIIncidenceOrientationIntCoeff_reverse :
    stageIIIncidenceOrientationIntCoeff .reverse = -1 := rfl

/-- Integer coefficients distinguish the two orientations. -/
theorem stageIIIncidenceOrientationIntCoeff_forward_ne_reverse :
    stageIIIncidenceOrientationIntCoeff .forward ≠
      stageIIIncidenceOrientationIntCoeff .reverse := by
  norm_num [stageIIIncidenceOrientationIntCoeff]

/-- Flipping orientation negates the integer coefficient. -/
@[simp] theorem stageIIIncidenceOrientationIntCoeff_flip
    (o : StageIIIncidenceOrientation) :
    stageIIIncidenceOrientationIntCoeff
        (stageIIIncidenceOrientationFlip o) =
      -stageIIIncidenceOrientationIntCoeff o := by
  cases o <;>
    norm_num [stageIIIncidenceOrientationIntCoeff,
      stageIIIncidenceOrientationFlip]

/-- Reduction modulo two forgets the integer orientation sign. -/
@[simp] theorem stageIIIncidenceOrientationIntCoeff_modTwo_eq_one
    (o : StageIIIncidenceOrientation) :
    ((stageIIIncidenceOrientationIntCoeff o : ℤ) : ZMod 2) = 1 := by
  cases o with
  | forward =>
      rfl
  | reverse =>
      change (-1 : ZMod 2) = 1
      exact ZMod.neg_eq_self_mod_two (1 : ZMod 2)

/-- Canonical integer representative of one pushed `ZMod 2` scalar.

This uses `ZMod.cast` only as a representative section.  No additivity or
multiplicativity of this map into `ℤ` is assumed. -/
def counterTransportIncidenceSeedFaceIntRepresentative
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (g : OctahedralStageIIIncidenceSeedFace) : ℤ :=
  ZMod.cast (counterTransportIncidenceSeedFaceAdd T g)

/-- Reducing the canonical integer representative modulo two recovers the
original pushed scalar exactly. -/
@[simp] theorem counterTransportIncidenceSeedFaceIntRepresentative_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (g : OctahedralStageIIIncidenceSeedFace) :
    ((counterTransportIncidenceSeedFaceIntRepresentative T g : ℤ) :
        ZMod 2) =
      counterTransportIncidenceSeedFaceAdd T g := by
  change
    (((ZMod.cast (counterTransportIncidenceSeedFaceAdd T g) : ℤ) : ZMod 2) =
      counterTransportIncidenceSeedFaceAdd T g)
  exact ZMod.intCast_zmod_cast
    (counterTransportIncidenceSeedFaceAdd T g)

/-- Orientation-sensitive integer representative of one placed scalar. -/
def counterTransportOrientedIncidenceSeedFaceIntRepresentative
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (o : StageIIIncidenceOrientation)
    (g : OctahedralStageIIIncidenceSeedFace) : ℤ :=
  stageIIIncidenceOrientationIntCoeff o *
    counterTransportIncidenceSeedFaceIntRepresentative T g

/-- Reversing orientation negates the oriented integer representative. -/
theorem counterTransportOrientedIncidenceSeedFaceIntRepresentative_flip
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (o : StageIIIncidenceOrientation)
    (g : OctahedralStageIIIncidenceSeedFace) :
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
        (stageIIIncidenceOrientationFlip o) g =
      -counterTransportOrientedIncidenceSeedFaceIntRepresentative T o g := by
  unfold counterTransportOrientedIncidenceSeedFaceIntRepresentative
  rw [stageIIIncidenceOrientationIntCoeff_flip]
  exact neg_mul _ _

/-- Modulo two, every oriented integer representative reduces to the original
unoriented pushed scalar. -/
@[simp] theorem counterTransportOrientedIncidenceSeedFaceIntRepresentative_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (o : StageIIIncidenceOrientation)
    (g : OctahedralStageIIIncidenceSeedFace) :
    ((counterTransportOrientedIncidenceSeedFaceIntRepresentative T o g : ℤ) :
        ZMod 2) =
      counterTransportIncidenceSeedFaceAdd T g := by
  change
    (((stageIIIncidenceOrientationIntCoeff o *
          counterTransportIncidenceSeedFaceIntRepresentative T g : ℤ) :
        ZMod 2) =
      counterTransportIncidenceSeedFaceAdd T g)
  rw [Int.cast_mul,
    stageIIIncidenceOrientationIntCoeff_modTwo_eq_one,
    counterTransportIncidenceSeedFaceIntRepresentative_modTwo]
  exact one_mul _

/-- Consequently, the two opposite integral orientations have the same
mod-two image even though they are represented by opposite integer signs. -/
theorem counterTransportOrientedIncidenceSeedFaceIntRepresentative_flip_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (o : StageIIIncidenceOrientation)
    (g : OctahedralStageIIIncidenceSeedFace) :
    ((counterTransportOrientedIncidenceSeedFaceIntRepresentative T
          (stageIIIncidenceOrientationFlip o) g : ℤ) : ZMod 2) =
      ((counterTransportOrientedIncidenceSeedFaceIntRepresentative T o g :
          ℤ) : ZMod 2) := by
  rw [counterTransportOrientedIncidenceSeedFaceIntRepresentative_modTwo,
    counterTransportOrientedIncidenceSeedFaceIntRepresentative_modTwo]

/-- Eight-term integer total using the same face-kind orientation convention
as v4.21. -/
def counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ℤ :=
  counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a00b00))
      (octahedralStageIIIncidenceSeedEquiv .a00b00) +
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a01b10))
      (octahedralStageIIIncidenceSeedEquiv .a01b10) +
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a00b01))
      (octahedralStageIIIncidenceSeedEquiv .a00b01) +
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a01b11))
      (octahedralStageIIIncidenceSeedEquiv .a01b11) +
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a10b00))
      (octahedralStageIIIncidenceSeedEquiv .a10b00) +
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a11b10))
      (octahedralStageIIIncidenceSeedEquiv .a11b10) +
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a10b01))
      (octahedralStageIIIncidenceSeedEquiv .a10b01) +
    counterTransportOrientedIncidenceSeedFaceIntRepresentative T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a11b11))
      (octahedralStageIIIncidenceSeedEquiv .a11b11)

/-- Reduction of the complete integer-oriented total is exactly the v4.20
incidence-carrier total. -/
theorem counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    ((counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal T : ℤ) :
        ZMod 2) =
      counterTransportIncidenceSeedCarrierTotal T := by
  simp only [counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal,
    Int.cast_add,
    counterTransportOrientedIncidenceSeedFaceIntRepresentative_modTwo,
    counterTransportIncidenceSeedCarrierTotal]

/-- Integral representative of the Stage-II mismatch.  The plus sign matches
the existing mod-two definition; no claim is made that `ZMod.cast` itself
preserves this sum before reduction. -/
def counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ℤ :=
  1 + counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal T

/-- The integral mismatch reduces exactly to the v4.20 incidence mismatch. -/
theorem counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_modTwo
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    ((counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch T : ℤ) :
        ZMod 2) =
      counterStageIIIncidenceSeedCarrierMismatch T := by
  change
    (((1 + counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal T :
        ℤ) : ZMod 2) =
      1 + counterTransportIncidenceSeedCarrierTotal T)
  rw [Int.cast_add,
    counterTransportFaceKindOrientedIncidenceSeedCarrierIntTotal_modTwo]
  rfl

/-- Hence the integral mismatch reduces to the certified nonzero
transport-independent Stage-II obstruction class. -/
theorem counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_modTwo_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    ((counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch T : ℤ) :
        ZMod 2) =
      counterStageIIObstructionAdd T := by
  rw [counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_modTwo]
  exact counterStageIIIncidenceSeedCarrierMismatch_eq_obstruction T

/-- The integral mismatch itself cannot vanish, because its mod-two reduction
is the nonzero Stage-II class. -/
theorem counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch T ≠ 0 := by
  intro hZero
  apply counterStageIIIncidenceSeedCarrierMismatch_ne_zero T
  calc
    counterStageIIIncidenceSeedCarrierMismatch T =
        ((counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch T :
          ℤ) : ZMod 2) :=
      (counterStageIIFaceKindOrientedIncidenceSeedCarrierIntMismatch_modTwo T).symm
    _ = 0 := by rw [hZero]; rfl

/-!
## Boundary after v4.22

The coefficient obstruction from v4.21 now has an explicit lift.

Upstairs in `ℤ`:
* forward and reverse orientation coefficients are distinct;
* flipping orientation negates the oriented representative.

Downstairs in `ZMod 2`:
* both signs reduce to one;
* every oriented representative reduces to the original pushed scalar;
* the eight-term total reduces to the v4.20 incidence-carrier total;
* the integral mismatch reduces to the same nonzero v4.12 Stage-II class.

Crucially, `ZMod.cast : ZMod 2 → ℤ` is used only as a canonical
representative section, not as an additive or multiplicative homomorphism.

The next theorem unit can now ask a genuinely orientation-sensitive recursive
question: transport these integer-oriented representatives through one
pentagram/hexagram refinement step, then compare the refined integer total
before reducing modulo two.
-/

end

end KUOS.DependentOriginationStageIIIntegralOrientationLiftV4_22
