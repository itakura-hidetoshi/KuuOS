import KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
import KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
import Mathlib

namespace KUOS.DependentOriginationParityCarrierCapacityV4_17

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16

set_option autoImplicit false

/-!
# Truncated-icosahedral capacity for the eight-face parity carrier v4.17

v4.16 isolates the transport-independent Stage-II parity data on an explicit
eight-element octahedral face carrier.

The truncated-icosahedral seed has 32 faces, including 12 pentagons.  This file
checks only the finite combinatorial capacity question: can the eight parity
labels be placed injectively on actual seed faces?

Yes.  We give one explicit injection into eight distinct pentagonal seed faces.

This is intentionally not yet a semantic or authority-bounded carrier map.
The particular placement below is a combinatorial witness only.
-/

/-- One explicit capacity-only placement of the eight parity labels into eight
distinct pentagonal seed faces. -/
def octahedralStageIIParityFaceSeedPlacement :
    OctahedralStageIIParityFace → TruncatedIcosahedralSeedFace
  | .a00b00 => .aroundVertex .north
  | .a01b10 => .aroundVertex .south
  | .a00b01 => .aroundVertex (.upper 0)
  | .a01b11 => .aroundVertex (.upper 1)
  | .a10b00 => .aroundVertex (.upper 2)
  | .a11b10 => .aroundVertex (.upper 3)
  | .a10b01 => .aroundVertex (.upper 4)
  | .a11b11 => .aroundVertex (.lower 0)

/-- The explicit placement is injective. -/
theorem octahedralStageIIParityFaceSeedPlacement_injective :
    Function.Injective octahedralStageIIParityFaceSeedPlacement := by
  native_decide

/-- The placement as a genuine embedding of finite carriers. -/
def octahedralStageIIParityFaceSeedEmbedding :
    OctahedralStageIIParityFace ↪ TruncatedIcosahedralSeedFace where
  toFun := octahedralStageIIParityFaceSeedPlacement
  inj' := octahedralStageIIParityFaceSeedPlacement_injective

/-- Every placed face is pentagonal. -/
@[simp] theorem octahedralStageIIParityFaceSeedPlacement_kind
    (f : OctahedralStageIIParityFace) :
    truncatedIcosahedralSeedFaceKind
        (octahedralStageIIParityFaceSeedPlacement f) =
      .pentagon := by
  cases f <;> rfl

/-- The explicit image contains exactly eight actual seed faces. -/
@[simp] theorem octahedralStageIIParityFaceSeedPlacement_image_card :
    (Finset.univ.image
      octahedralStageIIParityFaceSeedPlacement).card = 8 := by
  native_decide

/-- The image is contained in the actual pentagonal seed-face family. -/
theorem octahedralStageIIParityFaceSeedPlacement_image_subset_pentagons :
    Finset.univ.image octahedralStageIIParityFaceSeedPlacement ⊆
      truncatedIcosahedralSeedFacesOfKind .pentagon := by
  intro f hf
  rcases Finset.mem_image.mp hf with ⟨i, _, rfl⟩
  simp [truncatedIcosahedralSeedFacesOfKind,
    octahedralStageIIParityFaceSeedPlacement_kind]

/-- Eight parity labels fit inside the twelve pentagonal faces with room left
over. -/
theorem octahedralStageIIParityFaceSeedPlacement_image_lt_pentagon_family :
    (Finset.univ.image
        octahedralStageIIParityFaceSeedPlacement).card <
      (truncatedIcosahedralSeedFacesOfKind .pentagon).card := by
  native_decide

/-!
## Boundary after v4.17

The finite-capacity issue is settled:

  8 parity faces inject into 12 pentagonal seed faces.

But this is deliberately weaker than the desired recursive obstruction bridge.
Nothing in v4.17 says that north, south, or any selected ring face is singled
out by the Stage-II comparison obstruction.

The remaining theorem must justify a carrier placement from incidence,
orientation, comparison parity, or another authority-bearing coherence datum.
Cardinality alone is no longer an obstacle, but it is also not a proof of
semantic transport.
-/

end KUOS.DependentOriginationParityCarrierCapacityV4_17
