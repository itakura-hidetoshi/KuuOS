import KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21
import Mathlib

namespace KUOS.DependentOriginationStageIIOrientationProvenanceV4_22

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
open KUOS.DependentOriginationStageIIIncidencePushforwardV4_20
open KUOS.DependentOriginationStageIIOrientationMod2CollapseV4_21

set_option autoImplicit false

noncomputable section

/-!
# Stage-II orientation as independent provenance v4.22

v4.21 proves that ordinary orientation signs collapse in the existing
coefficient ring:

  (+1 : ZMod 2) = -1.

Therefore multiplying a Stage-II scalar by a sign cannot retain orientation
information.  The authority-safe alternative is to keep orientation as
independent provenance while leaving the obstruction scalar itself in its
already validated `ZMod 2` coefficient system.

This file packages, for every one of the eight Stage-II source labels:

* its original octahedral source label;
* its v4.19/v4.20 incidence-selected seed face;
* the proof that this target is exactly the incidence pushforward;
* its pentagon/hexagon orientation provenance;
* the proof that the orientation is the one induced by the target face kind.

The scalar is then read only from the target face.  Thus forgetting orientation
recovers the v4.20 carrier exactly, while the provenance layer still
distinguishes the opposite orientations of every middle-switch mate pair.

No compression of eight labels into one five- or six-crossing local star is
introduced here.
-/

/-- One Stage-II carrier point with source, target, and orientation provenance
kept separately from the `ZMod 2` scalar coefficient. -/
structure StageIIIncidenceOrientedProvenance where
  source : OctahedralStageIIParityFace
  target : OctahedralStageIIIncidenceSeedFace
  target_eq :
    target = octahedralStageIIIncidenceSeedEquiv source
  orientation : StageIIIncidenceOrientation
  orientation_eq :
    orientation = stageIIIncidenceSeedFaceOrientation target

/-- Canonical provenance record attached to one of the eight source labels. -/
def stageIIIncidenceCanonicalProvenance
    (f : OctahedralStageIIParityFace) :
    StageIIIncidenceOrientedProvenance where
  source := f
  target := octahedralStageIIIncidenceSeedEquiv f
  target_eq := rfl
  orientation :=
    stageIIIncidenceSeedFaceOrientation
      (octahedralStageIIIncidenceSeedEquiv f)
  orientation_eq := rfl

@[simp] theorem stageIIIncidenceCanonicalProvenance_source
    (f : OctahedralStageIIParityFace) :
    (stageIIIncidenceCanonicalProvenance f).source = f := by
  rfl

@[simp] theorem stageIIIncidenceCanonicalProvenance_target
    (f : OctahedralStageIIParityFace) :
    (stageIIIncidenceCanonicalProvenance f).target =
      octahedralStageIIIncidenceSeedEquiv f := by
  rfl

@[simp] theorem stageIIIncidenceCanonicalProvenance_orientation
    (f : OctahedralStageIIParityFace) :
    (stageIIIncidenceCanonicalProvenance f).orientation =
      stageIIIncidenceSeedFaceOrientation
        (octahedralStageIIIncidenceSeedEquiv f) := by
  rfl

/-- Forgetting orientation and source provenance leaves exactly the v4.20
incidence-selected target face. -/
def stageIIIncidenceProvenanceForgetTarget :
    StageIIIncidenceOrientedProvenance →
      OctahedralStageIIIncidenceSeedFace :=
  fun p => p.target

@[simp] theorem stageIIIncidenceProvenanceForgetTarget_canonical
    (f : OctahedralStageIIParityFace) :
    stageIIIncidenceProvenanceForgetTarget
        (stageIIIncidenceCanonicalProvenance f) =
      octahedralStageIIIncidenceSeedEquiv f := by
  rfl

/-- The canonical provenance targets remain injective, so retaining provenance
introduces no identification of distinct Stage-II source labels. -/
theorem stageIIIncidenceCanonicalProvenance_target_injective :
    Function.Injective
      (fun f : OctahedralStageIIParityFace =>
        stageIIIncidenceProvenanceForgetTarget
          (stageIIIncidenceCanonicalProvenance f)) := by
  intro f g h
  exact octahedralStageIIIncidenceSeedEquiv.injective h

/-- The `ZMod 2` scalar attached to a provenance point is still the validated
v4.20 scalar on its target face; orientation is deliberately not multiplied
into the coefficient. -/
noncomputable def counterTransportIncidenceProvenanceFaceAdd
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (p : StageIIIncidenceOrientedProvenance) : ZMod 2 :=
  counterTransportIncidenceSeedFaceAdd T p.target

/-- On a canonical provenance point, the carried scalar is exactly the original
v4.16 source scalar. -/
@[simp] theorem counterTransportIncidenceProvenanceFaceAdd_canonical
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (f : OctahedralStageIIParityFace) :
    counterTransportIncidenceProvenanceFaceAdd T
        (stageIIIncidenceCanonicalProvenance f) =
      counterTransportParityFaceAdd T f := by
  simp [counterTransportIncidenceProvenanceFaceAdd,
    stageIIIncidenceCanonicalProvenance]

/-- Orientation reversal has no fixed point at the provenance level. -/
@[simp] theorem stageIIIncidenceOrientationFlip_ne_self
    (o : StageIIIncidenceOrientation) :
    stageIIIncidenceOrientationFlip o ≠ o := by
  cases o <;> decide

/-- Middle-switch mates retain opposite orientation provenance. -/
theorem stageIIIncidenceCanonicalProvenance_mates_orientation_flip
    (f : OctahedralStageIIParityFace) :
    (stageIIIncidenceCanonicalProvenance
        (octahedralStageIIMiddleSwitchMate f)).orientation =
      stageIIIncidenceOrientationFlip
        (stageIIIncidenceCanonicalProvenance f).orientation := by
  simpa [stageIIIncidenceCanonicalProvenance] using
    stageIIIncidenceSeedFaceOrientation_mates_flip f

/-- Hence the two orientations of every middle-switch mate pair remain
genuinely distinct even though their `ZMod 2` sign coefficients coincide. -/
theorem stageIIIncidenceCanonicalProvenance_mates_orientation_ne
    (f : OctahedralStageIIParityFace) :
    (stageIIIncidenceCanonicalProvenance f).orientation ≠
      (stageIIIncidenceCanonicalProvenance
        (octahedralStageIIMiddleSwitchMate f)).orientation := by
  intro h
  have hFlip :=
    stageIIIncidenceCanonicalProvenance_mates_orientation_flip f
  exact stageIIIncidenceOrientationFlip_ne_self
    (stageIIIncidenceCanonicalProvenance f).orientation
    (hFlip.symm.trans h.symm)

/-- Nevertheless the two ordinary sign coefficients are equal after reduction
to `ZMod 2`. -/
theorem stageIIIncidenceCanonicalProvenance_mates_coeff_eq
    (f : OctahedralStageIIParityFace) :
    stageIIIncidenceOrientationCoeff
        (stageIIIncidenceCanonicalProvenance f).orientation =
      stageIIIncidenceOrientationCoeff
        (stageIIIncidenceCanonicalProvenance
          (octahedralStageIIMiddleSwitchMate f)).orientation := by
  simp only [stageIIIncidenceOrientationCoeff_eq_one]

/-- Provenance therefore separates two data that the current coefficient map
identifies: mate orientations are distinct while their mod-2 signs agree. -/
theorem stageIIIncidenceCanonicalProvenance_orientation_refines_coeff
    (f : OctahedralStageIIParityFace) :
    (stageIIIncidenceCanonicalProvenance f).orientation ≠
        (stageIIIncidenceCanonicalProvenance
          (octahedralStageIIMiddleSwitchMate f)).orientation ∧
      stageIIIncidenceOrientationCoeff
          (stageIIIncidenceCanonicalProvenance f).orientation =
        stageIIIncidenceOrientationCoeff
          (stageIIIncidenceCanonicalProvenance
            (octahedralStageIIMiddleSwitchMate f)).orientation := by
  exact ⟨
    stageIIIncidenceCanonicalProvenance_mates_orientation_ne f,
    stageIIIncidenceCanonicalProvenance_mates_coeff_eq f⟩

/-- The target faces in each provenance mate pair are still genuinely adjacent
pentagon--hexagon seed faces. -/
theorem stageIIIncidenceCanonicalProvenance_mates_adjacent
    (f : OctahedralStageIIParityFace) :
    truncatedSeedPentagonHexagonAdjacent
      (stageIIIncidenceCanonicalProvenance f).target.1
      (stageIIIncidenceCanonicalProvenance
        (octahedralStageIIMiddleSwitchMate f)).target.1 := by
  simpa [stageIIIncidenceCanonicalProvenance] using
    octahedralStageIIIncidenceSeedEquiv_mates_adjacent f

/-- The eight provenance-carried scalars, listed in the original source-label
order. -/
noncomputable def counterTransportIncidenceProvenanceCarrierTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a00b00) +
    counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a01b10) +
    counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a00b01) +
    counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a01b11) +
    counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a10b00) +
    counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a11b10) +
    counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a10b01) +
    counterTransportIncidenceProvenanceFaceAdd T
      (stageIIIncidenceCanonicalProvenance .a11b11)

/-- Forgetting the independent orientation provenance recovers exactly the
v4.20 incidence-carrier total. -/
theorem counterTransportIncidenceProvenanceCarrierTotal_eq
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportIncidenceProvenanceCarrierTotal T =
      counterTransportIncidenceSeedCarrierTotal T := by
  simp [counterTransportIncidenceProvenanceCarrierTotal,
    counterTransportIncidenceSeedCarrierTotal]

/-- Stage-II mismatch read from the provenance-refined carrier. -/
noncomputable def counterStageIIIncidenceProvenanceCarrierMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  1 + counterTransportIncidenceProvenanceCarrierTotal T

/-- Forgetting orientation provenance does not alter the obstruction class. -/
theorem counterStageIIIncidenceProvenanceCarrierMismatch_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIIncidenceProvenanceCarrierMismatch T =
      counterStageIIObstructionAdd T := by
  change 1 + counterTransportIncidenceProvenanceCarrierTotal T =
    counterStageIIObstructionAdd T
  rw [counterTransportIncidenceProvenanceCarrierTotal_eq]
  change counterStageIIIncidenceSeedCarrierMismatch T =
    counterStageIIObstructionAdd T
  exact counterStageIIIncidenceSeedCarrierMismatch_eq_obstruction T

/-- The provenance-refined carrier therefore still carries the nonzero Stage-II
obstruction. -/
theorem counterStageIIIncidenceProvenanceCarrierMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIIncidenceProvenanceCarrierMismatch T ≠ 0 := by
  rw [counterStageIIIncidenceProvenanceCarrierMismatch_eq_obstruction]
  exact counterStageIIObstructionAdd_ne_zero T

/-- The provenance-refined class remains transport-independent. -/
theorem counterStageIIIncidenceProvenanceCarrierMismatch_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIIncidenceProvenanceCarrierMismatch T =
      counterStageIIIncidenceProvenanceCarrierMismatch U := by
  rw [counterStageIIIncidenceProvenanceCarrierMismatch_eq_obstruction,
    counterStageIIIncidenceProvenanceCarrierMismatch_eq_obstruction]
  exact counterStageIIObstructionAdd_transport_independent T U

/-!
## Boundary after v4.22

The orientation problem is now separated cleanly into two layers.

Scalar layer:
  the Stage-II class remains the nonzero, transport-independent
  `ZMod 2` obstruction already validated in v4.12 and v4.20.

Provenance layer:
  source labels, incidence-selected target faces, and target orientations are
  retained explicitly.  Middle-switch mates have genuinely different
  orientations even though the coefficient map sends both signs to the same
  element of `ZMod 2`.

This avoids inventing a nonexistent characteristic-two sign distinction.

The next recursive theorem may therefore transport the provenance record
through one star-refinement step while testing the scalar class separately.
Because v4.18 forbids injecting all eight source labels into one local star,
that refinement must be multi-face or must provide an independently proved
aggregation/compression rule.
-/

end

end KUOS.DependentOriginationStageIIOrientationProvenanceV4_22
