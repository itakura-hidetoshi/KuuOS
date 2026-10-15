import KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
import KUOS.DependentOriginationStageIIObstructionClassV4_12
import Mathlib

namespace KUOS.DependentOriginationStageIIIncidencePushforwardV4_20

open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationStageIIObstructionClassV4_12
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19

set_option autoImplicit false

noncomputable section

/-!
# Stage-II incidence pushforward v4.20

v4.19 supplies an injective placement of the eight octahedral Stage-II parity
labels into actual truncated-icosahedral seed faces, preserving every
middle-switch mate pair as a pentagon--hexagon incidence.

This file attaches the actual v4.16 transport-parity values to that incidence
image without forgetting source-label provenance.

The target carrier is the range of the v4.19 embedding itself.  Because the
placement is an embedding, mathlib's `Function.Embedding.toEquivRange` gives
an equivalence between the eight source labels and the eight placed target
faces.  We use its inverse to push the scalar value on each source face to its
unique placed target face.

This proves value preservation for the incidence carrier.  It does not yet
assign orientation-dependent coefficients to pentagons or hexagons; that is
the next theorem unit.
-/

/-- The authority-bounded target carrier selected by the v4.19 incidence
placement: exactly the eight seed faces in the embedding image. -/
abbrev OctahedralStageIIIncidenceSeedFace : Type :=
  Set.range
    (octahedralStageIIPairIncidenceEmbedding :
      OctahedralStageIIParityFace → TruncatedIcosahedralSeedFace)

/-- The v4.19 embedding identifies each source parity label with exactly one
placed seed face while retaining a canonical inverse on the image. -/
def octahedralStageIIIncidenceSeedEquiv :
    OctahedralStageIIParityFace ≃ OctahedralStageIIIncidenceSeedFace :=
  octahedralStageIIPairIncidenceEmbedding.toEquivRange

/-- Every target carrier face has a unique source-label provenance. -/
theorem octahedralStageIIIncidenceSeedFace_unique_source
    (g : OctahedralStageIIIncidenceSeedFace) :
    ∃! f : OctahedralStageIIParityFace,
      octahedralStageIIPairIncidenceEmbedding f = g.1 := by
  rcases g.property with ⟨f, hf⟩
  refine ⟨f, hf, ?_⟩
  intro f' hf'
  exact octahedralStageIIPairIncidencePlacement_injective
    (hf'.trans hf.symm)

/-- Push one actual v4.16 transport-parity scalar onto the corresponding
incidence-selected seed face, using the unique inverse provenance. -/
noncomputable def counterTransportIncidenceSeedFaceAdd
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    OctahedralStageIIIncidenceSeedFace → ZMod 2 :=
  fun g =>
    counterTransportParityFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv.symm g)

/-- Pushing to the incidence carrier and pulling back at a placed source label
recovers exactly the original scalar. -/
@[simp] theorem counterTransportIncidenceSeedFaceAdd_apply
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD)
    (f : OctahedralStageIIParityFace) :
    counterTransportIncidenceSeedFaceAdd T
        (octahedralStageIIIncidenceSeedEquiv f) =
      counterTransportParityFaceAdd T f := by
  simp [counterTransportIncidenceSeedFaceAdd]

/-- The pushed target representatives of a middle-switch mate pair remain
actual pentagon--hexagon adjacent seed faces. -/
theorem octahedralStageIIIncidenceSeedEquiv_mates_adjacent
    (f : OctahedralStageIIParityFace) :
    truncatedSeedPentagonHexagonAdjacent
      (octahedralStageIIIncidenceSeedEquiv f).1
      (octahedralStageIIIncidenceSeedEquiv
        (octahedralStageIIMiddleSwitchMate f)).1 := by
  simpa [octahedralStageIIIncidenceSeedEquiv] using
    octahedralStageIIPairIncidencePlacement_mates_adjacent f

/-- The pushed target representatives of a mate pair retain opposite face
kinds. -/
theorem octahedralStageIIIncidenceSeedEquiv_mates_opposite_kinds
    (f : OctahedralStageIIParityFace) :
    truncatedIcosahedralSeedFaceKind
        (octahedralStageIIIncidenceSeedEquiv f).1 ≠
      truncatedIcosahedralSeedFaceKind
        (octahedralStageIIIncidenceSeedEquiv
          (octahedralStageIIMiddleSwitchMate f)).1 := by
  simpa [octahedralStageIIIncidenceSeedEquiv] using
    octahedralStageIIPairIncidencePlacement_mates_opposite_kinds f

/-- The eight pushed scalar values, listed in the same source-label order as
the v4.16 carrier total. -/
noncomputable def counterTransportIncidenceSeedCarrierTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a00b00) +
    counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a01b10) +
    counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a00b01) +
    counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a01b11) +
    counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a10b00) +
    counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a11b10) +
    counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a10b01) +
    counterTransportIncidenceSeedFaceAdd T
      (octahedralStageIIIncidenceSeedEquiv .a11b11)

/-- The incidence pushforward preserves the complete eight-face transport
parity total exactly. -/
theorem counterTransportIncidenceSeedCarrierTotal_eq_parityCarrierTotal
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterTransportIncidenceSeedCarrierTotal T =
      counterTransportParityCarrierTotal T := by
  simp [counterTransportIncidenceSeedCarrierTotal,
    counterTransportParityCarrierTotal]

/-- Raw odd parity minus the pushed incidence-carrier transport total. -/
noncomputable def counterStageIIIncidenceSeedCarrierMismatch
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) : ZMod 2 :=
  1 + counterTransportIncidenceSeedCarrierTotal T

/-- The pushed incidence-carrier mismatch is exactly the transport-independent
v4.12 Stage-II obstruction class. -/
theorem counterStageIIIncidenceSeedCarrierMismatch_eq_obstruction
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIIncidenceSeedCarrierMismatch T =
      counterStageIIObstructionAdd T := by
  change 1 + counterTransportIncidenceSeedCarrierTotal T =
    counterStageIIObstructionAdd T
  rw [counterTransportIncidenceSeedCarrierTotal_eq_parityCarrierTotal]
  change counterStageIIParityCarrierMismatch T =
    counterStageIIObstructionAdd T
  exact counterStageIIParityCarrierMismatch_eq_obstruction T

/-- Therefore the provenance-preserving incidence pushforward still carries the
nonzero Stage-II class. -/
theorem counterStageIIIncidenceSeedCarrierMismatch_ne_zero
    (T : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIIncidenceSeedCarrierMismatch T ≠ 0 := by
  rw [counterStageIIIncidenceSeedCarrierMismatch_eq_obstruction]
  exact counterStageIIObstructionAdd_ne_zero T

/-- The pushed incidence-carrier class remains independent of the coherent
quotient transport. -/
theorem counterStageIIIncidenceSeedCarrierMismatch_transport_independent
    (T U : CoherentQuotientTransportData
      (W := allMorphisms) counterSystem counterD) :
    counterStageIIIncidenceSeedCarrierMismatch T =
      counterStageIIIncidenceSeedCarrierMismatch U := by
  rw [counterStageIIIncidenceSeedCarrierMismatch_eq_obstruction,
    counterStageIIIncidenceSeedCarrierMismatch_eq_obstruction]
  exact counterStageIIObstructionAdd_transport_independent T U

/-!
## Boundary after v4.20

The v4.19 incidence placement now carries the actual Stage-II scalar data, not
only eight abstract labels.

For every placed target face there is a unique source label, every source value
is recovered exactly after pushforward, middle-switch adjacency is retained,
and the pushed carrier mismatch is the same nonzero transport-independent class
omega from v4.12.

This does not yet prove that the explicit v4.19 placement is uniquely canonical
among all incidence-preserving placements.  More importantly for the next
step, no pentagon/hexagon orientation coefficient has yet been inserted.

The next theorem should therefore define the target coefficient/orientation
semantics and prove, in ZMod 2, whether reversing orientation changes or leaves
unchanged the carried scalar before any recursive refinement theorem is stated.
-/

end

end KUOS.DependentOriginationStageIIIncidencePushforwardV4_20
