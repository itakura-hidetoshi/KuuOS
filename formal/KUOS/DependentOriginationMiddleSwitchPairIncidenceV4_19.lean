import KUOS.DependentOriginationLocalStarCapacityObstructionV4_18
import KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
import Mathlib

namespace KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16
open KUOS.DependentOriginationLocalStarCapacityObstructionV4_18

set_option autoImplicit false

/-!
# Middle-switch pair incidence bridge v4.19

v4.18 shows that the full eight-face Stage-II carrier cannot be injected into
one local pentagram or hexagram crossing set.  A global/multi-face placement is
therefore necessary.

The eight parity faces are not unstructured: the middle-switch calculation of
v3.69 naturally groups them into four pairs.

This file tests a minimal incidence-preservation requirement.  Each source pair
is sent to one actual pentagon--hexagon incidence in the truncated-icosahedral
seed.  Four distinct incidences provide eight distinct target faces.

This is stronger than cardinality alone, but still does not prove that the
placement preserves the full higher-coherence semantics.
-/

/-- Pentagon--hexagon adjacency coming directly from the truncation seed:
an original vertex and an original triangular face are adjacent after
truncation exactly when the vertex lies on that triangle. -/
def truncatedSeedPentagonHexagonAdjacent :
    TruncatedIcosahedralSeedFace →
      TruncatedIcosahedralSeedFace → Prop
  | .aroundVertex v, .fromTriangle f =>
      v ∈ icosahedralFaceVertices f
  | .fromTriangle f, .aroundVertex v =>
      v ∈ icosahedralFaceVertices f
  | _, _ => False

/-- The four middle-switch pairings of the eight parity faces. -/
def octahedralStageIIMiddleSwitchMate :
    OctahedralStageIIParityFace → OctahedralStageIIParityFace
  | .a00b00 => .a01b10
  | .a01b10 => .a00b00
  | .a00b01 => .a01b11
  | .a01b11 => .a00b01
  | .a10b00 => .a11b10
  | .a11b10 => .a10b00
  | .a10b01 => .a11b11
  | .a11b11 => .a10b01

@[simp] theorem octahedralStageIIMiddleSwitchMate_involutive
    (f : OctahedralStageIIParityFace) :
    octahedralStageIIMiddleSwitchMate
        (octahedralStageIIMiddleSwitchMate f) = f := by
  cases f <;> rfl

theorem octahedralStageIIMiddleSwitchMate_ne_self
    (f : OctahedralStageIIParityFace) :
    octahedralStageIIMiddleSwitchMate f ≠ f := by
  cases f <;> decide

/-- Explicit placement of the four source pairs onto four actual
pentagon--hexagon incidences. -/
def octahedralStageIIPairIncidencePlacement :
    OctahedralStageIIParityFace → TruncatedIcosahedralSeedFace
  | .a00b00 => .aroundVertex .north
  | .a01b10 => .fromTriangle (.top 0)
  | .a00b01 => .aroundVertex .south
  | .a01b11 => .fromTriangle (.bottom 0)
  | .a10b00 => .aroundVertex (.upper 0)
  | .a11b10 => .fromTriangle (.beltUpper 0)
  | .a10b01 => .aroundVertex (.lower 0)
  | .a11b11 => .fromTriangle (.beltLower 0)

/-- The incidence-aware placement remains injective. -/
theorem octahedralStageIIPairIncidencePlacement_injective :
    Function.Injective octahedralStageIIPairIncidencePlacement := by
  native_decide

/-- Each middle-switch mate pair lands on an actual pentagon--hexagon
incidence. -/
theorem octahedralStageIIPairIncidencePlacement_mates_adjacent
    (f : OctahedralStageIIParityFace) :
    truncatedSeedPentagonHexagonAdjacent
      (octahedralStageIIPairIncidencePlacement f)
      (octahedralStageIIPairIncidencePlacement
        (octahedralStageIIMiddleSwitchMate f)) := by
  cases f <;> native_decide

/-- The two members of every source pair land on opposite face kinds. -/
theorem octahedralStageIIPairIncidencePlacement_mates_opposite_kinds
    (f : OctahedralStageIIParityFace) :
    truncatedIcosahedralSeedFaceKind
        (octahedralStageIIPairIncidencePlacement f) ≠
      truncatedIcosahedralSeedFaceKind
        (octahedralStageIIPairIncidencePlacement
          (octahedralStageIIMiddleSwitchMate f)) := by
  cases f <;> decide

/-- Package the incidence-aware candidate as an embedding. -/
def octahedralStageIIPairIncidenceEmbedding :
    OctahedralStageIIParityFace ↪ TruncatedIcosahedralSeedFace where
  toFun := octahedralStageIIPairIncidencePlacement
  inj' := octahedralStageIIPairIncidencePlacement_injective

/-!
## Boundary after v4.19

The carrier bridge has advanced beyond pure cardinality.

There exists an injective global placement of the eight Stage-II parity labels
such that every middle-switch source pair lands on a genuine pentagon--hexagon
incidence of the truncated-icosahedral seed.

What remains unproved is stronger:

* that this or any other placement is selected canonically by the comparison
  obstruction;
* that individual source scalar values push forward with the correct
  orientation/sign convention;
* that recursive refinement preserves the resulting obstruction class.

Thus pair incidence is now available as a concrete compatibility condition,
but full authority-bearing semantic transport remains the next frontier.
-/

end KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
