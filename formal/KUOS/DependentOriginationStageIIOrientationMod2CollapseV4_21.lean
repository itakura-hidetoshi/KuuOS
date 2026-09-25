import KUOS.DependentOriginationStageIIIncidencePushforwardV4_20
import KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
import Mathlib

namespace KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
open KUOS.DependentOriginationStageIIIncidencePushforwardV4_20

set_option autoImplicit false

noncomputable section

/-!
# Stage-II orientation signs collapse over ZMod 2 v4.21

v4.20 pushes the actual eight Stage-II transport scalars onto the
incidence-selected truncated-icosahedral carrier while retaining unique source
provenance and pentagon--hexagon mate adjacency.

The next natural refinement is orientation.  The minimal sign convention uses

* +1 for forward orientation;
* -1 for reverse orientation.

However the Stage-II obstruction currently lives in `ZMod 2`.  In
characteristic two, `-1 = 1`.  Therefore a plain ±1 orientation coefficient
cannot distinguish the two orientations.

This file makes that coefficient obstruction explicit.  It proves that:

* forward and reverse sign coefficients coincide in `ZMod 2`;
* reversing orientation leaves every pushed scalar unchanged;
* the face-kind orientation convention (pentagon forward, hexagon reverse)
  is compatible with the v4.19 mate pairing;
* the complete oriented carrier total is exactly the v4.20 unoriented total;
* hence the same nonzero transport-independent Stage-II obstruction survives.

Thus orientation can matter only if it is retained as separate provenance or
if the coefficient system is enriched beyond characteristic two.
-/

/-- Two possible orientations for one incidence-carrier face. -/
inductive StageIIIncidenceOrientation
  | forward
  | reverse
  deriving DecidableEq, Repr, Fintype

/-- Reverse an incidence orientation. -/
def stageIIIncidenceOrientationFlip :
    StageIIIncidenceOrientation → StageIIIncidenceOrientation
  | .forward => .reverse
  | .reverse => .forward

@[simp] theorem stageIIIncidenceOrientationFlip_flip
    (o : StageIIIncidenceOrientation) :
    stageIIIncidenceOrientationFlip
        (stageIIIncidenceOrientationFlip o) = o := by
  cases o <;> rfl

/-- Minimal sign coefficient for orientation, valued in the existing
Stage-II coefficient ring. -/
def stageIIIncidenceOrientationCoeff :
    StageIIIncidenceOrientation → ZMod 2
  | .forward => 1
  | .reverse => -1

/-- Characteristic two identifies both orientation signs.

Use the dedicated `ZMod 2` simp theorem rather than asking `norm_num` to
discover characteristic-two negation from numeral normalization. -/
@[simp] theorem stageIIIncidenceOrientationCoeff_eq_one
    (o : StageIIIncidenceOrientation) :
    stageIIIncidenceOrientationCoeff o = 1 := by
  cases o with
  | forward =>
      rfl
  | reverse =>
      change (-1 : ZMod 2) = 1
      exact ZMod.neg_eq_self_mod_two (1 : ZMod 2)

/-- In particular, flipping orientation does not change its coefficient. -/
@[simp] theorem stageIIIncidenceOrientationCoeff_flip
    (o : StageIIIncidenceOrientation) :
    stageIIIncidenceOrientationCoeff
        (stageIIIncidenceOrientationFlip o) =
      stageIIIncidenceOrientationCoeff o := by
  simp

/-- Attach an orientation sign to one pushed incidence-carrier scalar. -/
noncomputable def counterTransportOrientedIncidenceSeedFaceAdd
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (o : StageIIIncidenceOrientation)
    (g : OctahedralStageIIIncidenceSeedFace) : ZMod 2 :=
  stageIIIncidenceOrientationCoeff o *
    counterTransportIncidenceSeedFaceAdd T g

/-- Every ±1-oriented scalar is exactly the underlying pushed scalar in
`ZMod 2`. -/
@[simp] theorem counterTransportOrientedIncidenceSeedFaceAdd_eq
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (o : StageIIIncidenceOrientation)
    (g : OctahedralStageIIIncidenceSeedFace) :
    counterTransportOrientedIncidenceSeedFaceAdd T o g =
      counterTransportIncidenceSeedFaceAdd T g := by
  simp [counterTransportOrientedIncidenceSeedFaceAdd]

/-- Reversing orientation therefore leaves every carried scalar unchanged. -/
theorem counterTransportOrientedIncidenceSeedFaceAdd_flip_eq
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (o : StageIIIncidenceOrientation)
    (g : OctahedralStageIIIncidenceSeedFace) :
    counterTransportOrientedIncidenceSeedFaceAdd T
        (stageIIIncidenceOrientationFlip o) g =
      counterTransportOrientedIncidenceSeedFaceAdd T o g := by
  rw [counterTransportOrientedIncidenceSeedFaceAdd_eq,
    counterTransportOrientedIncidenceSeedFaceAdd_eq]

/-- Orientation assigned to one truncated-icosahedral face kind. -/
def stageIIIncidenceFaceKindOrientation :
    TruncatedIcosahedralFaceKind → StageIIIncidenceOrientation
  | .pentagon => .forward
  | .hexagon => .reverse

/-- Since there are exactly two face kinds, distinct kinds have flipped
orientations.  This isolates the semantic reason for the mate flip from the
concrete eight-label placement. -/
theorem stageIIIncidenceFaceKindOrientation_of_ne
    (k l : TruncatedIcosahedralFaceKind)
    (h : k ≠ l) :
    stageIIIncidenceFaceKindOrientation l =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceFaceKindOrientation k) := by
  cases k <;> cases l
  · exact (h rfl).elim
  · rfl
  · rfl
  · exact (h rfl).elim

/-- A concrete target convention: pentagons are forward, hexagons reverse. -/
def stageIIIncidenceSeedFaceOrientation
    (g : OctahedralStageIIIncidenceSeedFace) :
    StageIIIncidenceOrientation :=
  stageIIIncidenceFaceKindOrientation
    (truncatedIcosahedralSeedFaceKind g.1)

/-- Under the v4.19 placement, every middle-switch mate pair has opposite
target orientations.  The proof now uses the already-proved opposite-face-kind
incidence theorem rather than unfolding all eight source constructors. -/
theorem stageIIIncidenceSeedFaceOrientation_mates_flip
    (f : OctahedralStageIIParityFace) :
    stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv
          (octahedralStageIIMiddleSwitchMate f)) =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceSeedFaceOrientation
          (octahedralStageIIIncidenceSeedEquiv f)) := by
  apply stageIIIncidenceFaceKindOrientation_of_ne
  exact octahedralStageIIIncidenceSeedEquiv_mates_opposite_kinds f

/-- The complete eight-face total with the face-kind orientation convention. -/
noncomputable def counterTransportFaceKindOrientedIncidenceSeedCarrierTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a00b00))
      (octahedralStageIIIncidenceSeedEquiv .a00b00) +
    counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a01b10))
      (octahedralStageIIIncidenceSeedEquiv .a01b10) +
    counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a00b01))
      (octahedralStageIIIncidenceSeedEquiv .a00b01) +
    counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a01b11))
      (octahedralStageIIIncidenceSeedEquiv .a01b11) +
    counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a10b00))
      (octahedralStageIIIncidenceSeedEquiv .a10b00) +
    counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a11b10))
      (octahedralStageIIIncidenceSeedEquiv .a11b10) +
    counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a10b01))
      (octahedralStageIIIncidenceSeedEquiv .a10b01) +
    counterTransportOrientedIncidenceSeedFaceAdd T
      (stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv .a11b11))
      (octahedralStageIIIncidenceSeedEquiv .a11b11)

/-- Face-kind orientation signs do not alter the complete carrier total. -/
theorem counterTransportFaceKindOrientedIncidenceSeedCarrierTotal_eq
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportFaceKindOrientedIncidenceSeedCarrierTotal T =
      counterTransportIncidenceSeedCarrierTotal T := by
  simp [counterTransportFaceKindOrientedIncidenceSeedCarrierTotal,
    counterTransportIncidenceSeedCarrierTotal]

/-- Raw odd parity minus the face-kind-oriented carrier total. -/
noncomputable def counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  1 + counterTransportFaceKindOrientedIncidenceSeedCarrierTotal T

/-- The oriented mismatch is still exactly the v4.12 Stage-II obstruction. -/
theorem counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch T =
      counterStageIIObstructionAdd T := by
  change 1 + counterTransportFaceKindOrientedIncidenceSeedCarrierTotal T =
    counterStageIIObstructionAdd T
  rw [counterTransportFaceKindOrientedIncidenceSeedCarrierTotal_eq]
  change counterStageIIIncidenceSeedCarrierMismatch T =
    counterStageIIObstructionAdd T
  exact counterStageIIIncidenceSeedCarrierMismatch_eq_obstruction T

/-- Hence the oriented carrier still carries a nonzero obstruction. -/
theorem counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch T ≠ 0 := by
  rw [counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch_eq_obstruction]
  exact counterStageIIObstructionAdd_ne_zero T

/-- The oriented carrier class remains independent of the coherent quotient
transport. -/
theorem counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch T =
      counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch U := by
  rw [counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch_eq_obstruction,
    counterStageIIFaceKindOrientedIncidenceSeedCarrierMismatch_eq_obstruction]
  exact counterStageIIObstructionAdd_transport_independent T U

/-!
## Boundary after v4.21

The incidence carrier now has an explicit orientation semantics, and that
semantics exposes a new obstruction:

  in ZMod 2, +1 = -1.

Therefore no sign-only orientation convention can add information to the
Stage-II carrier.  Reversing a face leaves every pushed scalar unchanged, and
the full oriented total is exactly the v4.20 total.

This is stronger than saying that one chosen orientation convention happens to
work.  It shows that characteristic-two coefficients are intrinsically blind
to ordinary orientation signs.

The next theorem unit should therefore do one of two authority-bounded things:

1. retain orientation as independent provenance rather than multiplying by a
   ZMod-2 sign; or
2. lift the incidence carrier to a richer coefficient system in which
   +1 and -1 remain distinct, then prove a reduction map back to the existing
   Stage-II ZMod-2 obstruction.

Only after such a lift should recursive star refinement be asked to preserve
an orientation-sensitive obstruction class.
-/

end

end KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
