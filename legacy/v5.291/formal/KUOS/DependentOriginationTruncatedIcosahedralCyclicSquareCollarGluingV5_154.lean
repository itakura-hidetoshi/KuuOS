import KUOS.DependentOriginationTruncatedIcosahedralPentagonIndependentSquarePastingV5_154

namespace KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F57-D / v5.154 — ACTUAL cyclic C60 pentagon-square collar gluing

F57-A constructed authentic C60 vertex/edge/face incidence squares,
F57-B labelled each actual five-edge pentagon by five original F55
signed Type-valued associativity rotation paths, and F57-C attached
real independent-order F55 finite-depth route squares.

A list of five squares is NOT yet a geometric pasting: adjacent
squares need compatible boundary flags. Here each adjacent pair
shares exactly the pentagonal vertex/face flag at their common
geometric truncated edge endpoint. This holds even for the closing
fourth-to-zero cyclic successor slot s4 -> s0, thanks to the original
v3.85 endpoint incidence theorem.

The common corner is a REAL incident flag, and both of the related
F55 labels share the identical indexed original F45 tree at the
corresponding vertex. Thus the five edge-attached squares form a
cyclic CORNER-GLUED collar around each actual C60 pentagon. This is
a combinatorial incidence gluing, not yet a chosen external Gray
3-cell realization or a claim that different geometric squares
share their neighboring hexagon faces.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualOriginalF45Pentagon

variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)

/-- The right endpoint dart of the C60 four-flag square at slot s
is EXACTLY the left endpoint dart of the next actual square.
No geometric matching is inferred from abstract equal arity. -/
theorem OriginalF45C60PentagonPasting.consecutive_shared_dart
    {v : IcosahedralVertex}
    (patch : OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (s : PentagonalSlot) :
    ((patch.sides s).incidenceSquare.vertex true) =
      ((patch.sides (pentagonalSlotNext s)).incidenceSquare.vertex false) := by
  change
    (truncatedIcosahedralEdgeEndpoints (.around ⟨v, s⟩)).2 =
      (truncatedIcosahedralEdgeEndpoints
        (.around ⟨v, pentagonalSlotNext s⟩)).1
  exact truncatedIcosahedralAroundEdge_consecutive v s

/-- Both adjacent REAL C60 four-flag squares identify the SAME
pentagon face on their shared corner. Their other, hexagon faces
are NOT assumed to be equal. -/
theorem OriginalF45C60PentagonPasting.consecutive_shared_pentagon_face
    {v : IcosahedralVertex}
    (patch : OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (s : PentagonalSlot) :
    ((patch.sides s).incidenceSquare.face false) =
      ((patch.sides (pentagonalSlotNext s)).incidenceSquare.face false) := by
  change (patch.sides s).incidenceSquare.firstFace =
    (patch.sides (pentagonalSlotNext s)).incidenceSquare.firstFace
  exact (patch.sides s).pentagonFace.trans
    (patch.sides (pentagonalSlotNext s)).pentagonFace.symm

/-- The actual shared geometric CORNER FLAG between consecutive
four-flag squares. This is a pair of the SAME original truncated
dart and the SAME original pentagon seed face. -/
theorem OriginalF45C60PentagonPasting.consecutive_shared_flag
    {v : IcosahedralVertex}
    (patch : OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (s : PentagonalSlot) :
    (((patch.sides s).incidenceSquare.vertex true),
      ((patch.sides s).incidenceSquare.face false)) =
    (((patch.sides (pentagonalSlotNext s)).incidenceSquare.vertex false),
      ((patch.sides (pentagonalSlotNext s)).incidenceSquare.face false)) :=
  Prod.ext (patch.consecutive_shared_dart t₁ t₂ t₃ t₄ s)
    (patch.consecutive_shared_pentagon_face t₁ t₂ t₃ t₄ s)

/-- The common corner is ACTUALLY incident in the v3.84–v3.86
original C60 truncated-icosahedral face poset. -/
theorem OriginalF45C60PentagonPasting.shared_flag_incident
    {v : IcosahedralVertex}
    (patch : OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (s : PentagonalSlot) :
    truncatedDartOnSeedFace
      ((patch.sides s).incidenceSquare.vertex true)
      ((patch.sides s).incidenceSquare.face false) :=
  (patch.sides s).incidenceSquare.corner_incident true false

/-- The final, fifth C60 edge-local four-flag square actually
glues back to the first square, closing the pentagonal collar. -/
theorem OriginalF45C60PentagonPasting.cyclic_closes
    {v : IcosahedralVertex}
    (patch : OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v) :
    (((patch.sides .s4).incidenceSquare.vertex true),
      ((patch.sides .s4).incidenceSquare.face false)) =
    (((patch.sides .s0).incidenceSquare.vertex false),
      ((patch.sides .s0).incidenceSquare.face false)) := by
  simpa only [pentagonalSlotNext] using
    (patch.consecutive_shared_flag t₁ t₂ t₃ t₄ .s4)

/-- All five original F55 labelled sides in the C60 collar have
CONSECUTIVE F45 tree vertices that match at each shared geometric
pentagon corner. This is an actual composable pair of SIGNED typed
local rotation-path witnesses, without inventing a fake forward
inverse for the two backward geometric pentagon sides. -/
def OriginalF45C60PentagonPasting.consecutive_typed_sides
    {v : IcosahedralVertex}
    (patch : OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (s : PentagonalSlot) :
    SignedOriginalF45PentagonSide
        (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄ s)
        (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄
          (pentagonalSlotNext s)) ×
    SignedOriginalF45PentagonSide
        (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄
          (pentagonalSlotNext s))
        (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄
          (pentagonalSlotNext (pentagonalSlotNext s))) :=
  ((patch.sides s).rotation, (patch.sides (pentagonalSlotNext s)).rotation)

/-- The TWO independently ordered typed refinement-route squares
attached to consecutive genuine C60 edges agree on their shared
geometric pentagon-corner flag, with the additional independent
depth-aware original F45 route held FIXED. -/
theorem originalF45C60AttachedSquares_consecutive_shared_flag
    (v : IcosahedralVertex) (s : PentagonalSlot)
    {k k' l l' : Nat}
    {auxBefore : OriginalF45BracketTree k l p₄ q₄ p₅ q₅}
    {auxAfter : OriginalF45BracketTree k' l' p₄ q₄ p₅ q₅}
    (aux : OriginalF45BracketTree.DepthRotationRoute auxBefore auxAfter) :
    (((originalF45C60AttachedDepthSquare t₁ t₂ t₃ t₄ v s aux).geometricSide.incidenceSquare.vertex true),
      ((originalF45C60AttachedDepthSquare t₁ t₂ t₃ t₄ v s aux).geometricSide.incidenceSquare.face false)) =
    (((originalF45C60AttachedDepthSquare t₁ t₂ t₃ t₄ v (pentagonalSlotNext s) aux).geometricSide.incidenceSquare.vertex false),
      ((originalF45C60AttachedDepthSquare t₁ t₂ t₃ t₄ v (pentagonalSlotNext s) aux).geometricSide.incidenceSquare.face false)) := by
  change
    (((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).incidenceSquare.vertex true,
      ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).incidenceSquare.face false) =
    (((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides (pentagonalSlotNext s)).incidenceSquare.vertex false,
      ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides (pentagonalSlotNext s)).incidenceSquare.face false)
  exact (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).consecutive_shared_flag
    t₁ t₂ t₃ t₄ s

#print axioms OriginalF45C60PentagonPasting.consecutive_shared_dart
#print axioms OriginalF45C60PentagonPasting.consecutive_shared_pentagon_face
#print axioms OriginalF45C60PentagonPasting.consecutive_shared_flag
#print axioms OriginalF45C60PentagonPasting.shared_flag_incident
#print axioms OriginalF45C60PentagonPasting.cyclic_closes
#print axioms OriginalF45C60PentagonPasting.consecutive_typed_sides
#print axioms originalF45C60AttachedSquares_consecutive_shared_flag

end ActualOriginalF45Pentagon

end
end KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
