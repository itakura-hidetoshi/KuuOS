import KUOS.DependentOriginationTruncatedIcosahedralActualEtaEpsilonSquareV5_155
import KUOS.DependentOriginationTruncatedIcosahedralCyclicSquareCollarGluingV5_154

namespace KUOS.DependentOriginationTruncatedIcosahedralCyclicChargeV5_155

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F58-E / v5.155 — five REAL C60 cyclic flag squares plus additive higher charge

F57-A–D constructs authentic C60 pentagon-to-hexagon flag squares
and proves that ALL FIVE adjacent squares in one physical pentagon
collar share a true (dart, pentagonal face) incidence CORNER FLAG,
including the closing slot s4 -> s0.

F58-A defines an INDEPENDENT Type-valued additive higher target
Int × Int, distinguishes a real F55 pentagon generator (1,0)
from each externally supplied genuine F55 independent square
generator (0,1), and F58-B–D proves compatibility of those
charges with honest original chosen right mates and actual η/ε
F44/complete original F19/F28 history interpretations.

Here we attach a genuine typed F55 original disjoint-square
generator to EACH of the FIVE real C60 around-vertex edges. The
chosen left/right local rotations are explicitly supplied on the
first two original F45 subtrees of the same F55 pentagon; the
geometry alone does NOT manufacture those rotations.

The five REAL signed charge pairs sum to (0,5), and combining
the actual chosen pentagon generator gives (1,5). We prove the
actual cyclic shared-flag identity of the SAME five squares,
not just a formal list of five abstract higher symbols.

CRITICAL SCOPE: this finite additive SUM is an independent
aggregate invariant of a geometrically corner-glued family of
labelled cells. Its members need not be vertically composable as
arbitrary higher 3-cells and the sum is NOT a theorem realizing
the C60 collar in an external Gray/tricategory. No original
potentially noninvertible G.toOplax cell is inverted.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section RealPentagonCollar
variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- The actual five-edge ORIGINAL C60 pentagon boundary provides
one REAL vertex/face four-flag incidence square for each cyclic
pentagonal slot. Independently supplied original F55 left/right
local rotations provide the actual square generator at each edge.

This list records five separately typed original F55 square-cell
INTERPRETATIONS in the independent integer-charge target. -/
def originalC60SquareCollarChargeList
    (v : IcosahedralVertex) : List (Int × Int) :=
  ([PentagonalSlot.s0, .s1, .s2, .s3, .s4] : List PentagonalSlot).map
    (fun s =>
      ((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, s⟩ left right).squareCell.interpret
        OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge :
          Int × Int))

/-- All FIVE actual square generators are explicitly evaluated:
their independent charges are nontrivial in the square coordinate.
The geometry is the old C60 finite 5.6.6 carrier, not an invented
surface with quadrilateral faces. -/
theorem originalC60SquareCollarChargeList_eq
    (v : IcosahedralVertex) :
    originalC60SquareCollarChargeList t₁ t₂ left right v =
      [((0 : Int), (1 : Int)), (0, 1), (0, 1), (0, 1), (0, 1)] := by
  rfl

/-- Actual *additive invariant* of the real C60 five-edge pentagon
plus all five independent local square labels. This is a finite
aggregation over a cyclic geometric flag-collar, NOT a fabricated
vertical 3-cell composite of incompatible source/target paths. -/
def originalC60PentagonSquareCollarCharge
    (v : IcosahedralVertex) : Int × Int :=
  ((OriginalF45C60PentagonPasting.interpret
    t₁ t₂ t₃ t₄
    (originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
      (D := D) (E := E))) : Int × Int) +
    (originalC60SquareCollarChargeList t₁ t₂ left right v).sum

/-- The original C60 five-edge pentagon has independent charge (1,0),
while the FIVE genuinely labelled corner-glued four-flag squares
have aggregate charge (0,5). Their finite invariant is (1,5). -/
theorem originalC60PentagonSquareCollarCharge_eq
    (v : IcosahedralVertex) :
    originalC60PentagonSquareCollarCharge t₁ t₂ t₃ t₄ left right v =
      ((1 : Int), (5 : Int)) := by
  unfold originalC60PentagonSquareCollarCharge
  rw [originalC60Pentagon_generatorCharge t₁ t₂ t₃ t₄ v,
    originalC60SquareCollarChargeList_eq t₁ t₂ left right v]
  decide

/-- The two adjacent ACTUAL integer-charged F55 square generators
are attached to C60 geometric four-flag squares that share the SAME
real pentagonal vertex/face CORNER FLAG, not merely the same count.
The closing square, from slot s4, is included by cycling s -> next s. -/
theorem originalC60ChargedSquareCollar_consecutive_sharedFlag
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, s⟩ left right).geometricSquare.vertex true),
     ((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, s⟩ left right).geometricSquare.face false)) =
    (((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, pentagonalSlotNext s⟩ left right).geometricSquare.vertex false),
     ((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, pentagonalSlotNext s⟩ left right).geometricSquare.face false)) := by
  apply Prod.ext
  · change
      (truncatedIcosahedralEdgeEndpoints (.around ⟨v, s⟩)).2 =
        (truncatedIcosahedralEdgeEndpoints
          (.around ⟨v, pentagonalSlotNext s⟩)).1
    exact truncatedIcosahedralAroundEdge_consecutive v s
  · exact
      (OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, s⟩ left right).pentagonFace.trans
      (OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, pentagonalSlotNext s⟩ left right).pentagonFace.symm

/-- The FIFTH charged square is glued back to the FIRST along an
actual common pentagonal vertex/face flag. -/
theorem originalC60ChargedSquareCollar_closes
    (v : IcosahedralVertex) :
    (((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, .s4⟩ left right).geometricSquare.vertex true),
     ((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, .s4⟩ left right).geometricSquare.face false)) =
    (((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, .s0⟩ left right).geometricSquare.vertex false),
     ((OriginalC60FlagSquareWithF55Generator.canonical
      ⟨v, .s0⟩ left right).geometricSquare.face false)) := by
  simpa only [pentagonalSlotNext] using
    originalC60ChargedSquareCollar_consecutive_sharedFlag
      t₁ t₂ left right v .s4

/-- Exact combined concrete certification: the same five actual
corner-glued C60 flag squares carry nontrivial independent square
signatures, while the central pentagon carries its distinct
pentagon generator; their aggregate is not confused with F44's
Prop-only observation or an unrestricted external tricategory. -/
theorem originalC60PentagonSquareCollar_complete
    (v : IcosahedralVertex) :
    (∀ s : PentagonalSlot,
      (((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, s⟩ left right).geometricSquare.vertex true),
       ((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, s⟩ left right).geometricSquare.face false)) =
      (((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, pentagonalSlotNext s⟩ left right).geometricSquare.vertex false),
       ((OriginalC60FlagSquareWithF55Generator.canonical
        ⟨v, pentagonalSlotNext s⟩ left right).geometricSquare.face false))) ∧
    (originalC60PentagonSquareCollarCharge
      t₁ t₂ t₃ t₄ left right v = ((1 : Int), (5 : Int))) :=
  ⟨originalC60ChargedSquareCollar_consecutive_sharedFlag
      t₁ t₂ left right v,
   originalC60PentagonSquareCollarCharge_eq
      t₁ t₂ t₃ t₄ left right v⟩

#print axioms originalC60SquareCollarChargeList
#print axioms originalC60SquareCollarChargeList_eq
#print axioms originalC60PentagonSquareCollarCharge
#print axioms originalC60PentagonSquareCollarCharge_eq
#print axioms originalC60ChargedSquareCollar_consecutive_sharedFlag
#print axioms originalC60ChargedSquareCollar_closes
#print axioms originalC60PentagonSquareCollar_complete

end RealPentagonCollar

end
end KUOS.DependentOriginationTruncatedIcosahedralCyclicChargeV5_155
