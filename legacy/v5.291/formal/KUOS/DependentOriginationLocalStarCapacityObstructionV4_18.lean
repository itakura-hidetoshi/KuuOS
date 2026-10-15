import KUOS.DependentOriginationParityCarrierCapacityV4_17
import KUOS.DependentOriginationHexagramInnerHexagonV3_88
import KUOS.DependentOriginationPentagramInnerPentagonV3_89
import Mathlib

namespace KUOS.DependentOriginationLocalStarCapacityObstructionV4_18

open KUOS.DependentOriginationHexagramInnerHexagonV3_88
open KUOS.DependentOriginationPentagramInnerPentagonV3_89
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationParityCarrierCapacityV4_17

set_option autoImplicit false

/-!
# One-star capacity obstruction v4.18

v4.17 proves that the eight-element octahedral Stage-II parity carrier fits
inside the global 32-face truncated-icosahedral seed.

A different question is whether those eight parity labels can be identified
one-to-one with the crossings of one recursive local star.

They cannot:

* a pentagram has five inner crossings;
* a hexagram has six inner crossings;
* the Stage-II parity carrier has eight elements.

This file records the corresponding finite-cardinality obstruction.  Thus any
authority-bearing carrier bridge must be global/multi-face, or aggregate the
eight source terms before placing them on one local star.
-/

/-- No map from the eight parity faces to the six hexagram inner crossings can
be injective. -/
theorem octahedralStageIIParityFace_to_hexagramInnerVertex_not_injective
    (f : OctahedralStageIIParityFace → HexagramInnerVertex) :
    ¬ Function.Injective f := by
  intro hinj
  have hcard := Fintype.card_le_of_injective _ hinj
  simp only [octahedralStageIIParityFace_card,
    hexagramInnerVertex_card] at hcard
  omega

/-- Hence there is no embedding of the full eight-face parity carrier into one
hexagram crossing set. -/
theorem no_octahedralStageIIParityFace_embedding_hexagramInnerVertex :
    IsEmpty (OctahedralStageIIParityFace ↪ HexagramInnerVertex) := by
  constructor
  intro e
  exact
    (octahedralStageIIParityFace_to_hexagramInnerVertex_not_injective
      e e.injective)

/-- No map from the eight parity faces to the five pentagram inner crossings
can be injective. -/
theorem octahedralStageIIParityFace_to_pentagramInnerVertex_not_injective
    (f : OctahedralStageIIParityFace → PentagramInnerVertex) :
    ¬ Function.Injective f := by
  intro hinj
  have hcard := Fintype.card_le_of_injective _ hinj
  simp only [octahedralStageIIParityFace_card,
    pentagramInnerVertex_card] at hcard
  omega

/-- Hence there is no embedding of the full eight-face parity carrier into one
pentagram crossing set. -/
theorem no_octahedralStageIIParityFace_embedding_pentagramInnerVertex :
    IsEmpty (OctahedralStageIIParityFace ↪ PentagramInnerVertex) := by
  constructor
  intro e
  exact
    (octahedralStageIIParityFace_to_pentagramInnerVertex_not_injective
      e e.injective)

/-- Combined local-star capacity obstruction. -/
theorem octahedralStageIIParityFace_no_singleStar_embedding :
    IsEmpty (OctahedralStageIIParityFace ↪ PentagramInnerVertex) ∧
      IsEmpty (OctahedralStageIIParityFace ↪ HexagramInnerVertex) := by
  exact
    ⟨no_octahedralStageIIParityFace_embedding_pentagramInnerVertex,
      no_octahedralStageIIParityFace_embedding_hexagramInnerVertex⟩

/-!
## Boundary after v4.18

The carrier-size picture is now exact.

* Global seed carrier: 32 faces, and v4.17 explicitly embeds all eight parity
  labels.
* One pentagram: 5 crossings, too small for an injective eight-label carrier.
* One hexagram: 6 crossings, also too small.

Therefore a faithful one-to-one recursive transport cannot live inside one
local star.  The next semantic bridge must either:

1. spread the eight parity labels across several truncated-icosahedral faces;
2. aggregate source labels by a proved coherence relation before local
   placement; or
3. use richer data than a plain injective crossing assignment.

This is a structural restriction, not merely a choice of drawing.
-/

end KUOS.DependentOriginationLocalStarCapacityObstructionV4_18
