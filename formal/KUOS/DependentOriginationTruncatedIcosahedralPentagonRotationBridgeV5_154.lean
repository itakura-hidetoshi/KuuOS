import KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ConditionalHigherCellTargetV5_153

namespace KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F57-B / v5.154 — ACTUAL C60 pentagon incidence edges labelled by F55 typed rotations

The original v3.85 and F57-A files exhibit real C60 pentagonal
5-edge boundaries, and each of their five edges bounds a genuine
pentagon–hexagon four-flag incidence square. F55-A/B constructs the
five actual original F45 bracket trees and five proof-relevant local
associativity rotation edges forming a Mac Lane pentagon.

We now give an explicit *five-edge labelling* of every actual geometric
C60 pentagon by the five Type-valued original F55 local-rotation routes:
  0→1, 1→2, 2→3, 4→3, 0→4.
The first three agree with the cyclic 0→1→2→3→4→0 boundary direction,
while the last two are explicitly BACKWARD from the geometric boundary
orientation. This matters: the long three-edge route and the short
two-edge route have different raw Type-valued witnesses.

Each edge-local flag square is retained together with the corresponding
genuine one-rotation path, and the real pentagon comparison is stored
as the original F55 freely presented Type-valued pentagon cell.
A separately supplied F56 higher-cell target can interpret this cell.

This is a constructed, typed GEOMETRIC-TO-PATH LABELLING with real
incidence witnesses, not an unjustified equivalence between the C60
surface and an external Gray/tricategory. In particular the physical
C60 1-skeleton has only pentagonal and hexagonal faces: squares here
are in the vertex/face flag-incidence presentation, not new polygonal
faces. A faithful native higher 3-cell realization is still open.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A vertex of the F55 Mac Lane pentagon remembers its ACTUAL old F45
binary tree and both separately indexed F19 and F28 Nat depths. -/
structure OriginalF45PentagonIndexedVertex
    {a b : D} {x y : E}
    (p₀ p₄ : Blocks a b) (q₀ q₄ : Blocks x y) where
  n : Nat
  m : Nat
  tree : OriginalF45BracketTree n m p₀ q₀ p₄ q₄

/-- An actual original F55 indexed rotation path, carrying whether its
orientation agrees with or opposes the geometric cyclic boundary.
Backward here is an *honest opposite-directed route witness*; no
fictitious equality of distinct F55 paths is introduced. -/
inductive SignedOriginalF45PentagonSide
    {a b : D} {x y : E}
    {p₀ p₄ : Blocks a b} {q₀ q₄ : Blocks x y}
    (first last : OriginalF45PentagonIndexedVertex p₀ p₄ q₀ q₄) :
    Type (max (max uD uE) (max vD vE)) where
  | forward (route : OriginalF45BracketTree.DepthRotationRoute
      first.tree last.tree) : SignedOriginalF45PentagonSide first last
  | backward (route : OriginalF45BracketTree.DepthRotationRoute
      last.tree first.tree) : SignedOriginalF45PentagonSide first last

/-- The number of REAL F54 local rotations on one signed geometric
edge; the direction bit never changes the actual rotation count. -/
def SignedOriginalF45PentagonSide.rotationCount
    {a b : D} {x y : E}
    {p₀ p₄ : Blocks a b} {q₀ q₄ : Blocks x y}
    {first last : OriginalF45PentagonIndexedVertex p₀ p₄ q₀ q₄}
    (edge : SignedOriginalF45PentagonSide first last) : Nat :=
  match edge with
  | .forward route => route.rotationCount
  | .backward route => route.rotationCount

section ActualFourSubtrees

variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)

/-- The ACTUAL five separately parenthesized F53/F55 original trees,
indexed by the REAL five cyclic v3.85 pentagonal edge slots. -/
def originalF45PentagonIndexedVertex
    (s : PentagonalSlot) :
    OriginalF45PentagonIndexedVertex p₀ p₄ q₀ q₄ :=
  match s with
  | .s0 => ⟨_, _, OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄⟩
  | .s1 => ⟨_, _, OriginalF45BracketTree.pentagon1 t₁ t₂ t₃ t₄⟩
  | .s2 => ⟨_, _, OriginalF45BracketTree.pentagon2 t₁ t₂ t₃ t₄⟩
  | .s3 => ⟨_, _, OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄⟩
  | .s4 => ⟨_, _, OriginalF45BracketTree.pentagon4 t₁ t₂ t₃ t₄⟩

/-- The original v3.85 C60 pentagon edge slot is assigned its
corresponding ACTUAL F55 one-step associativity rotation. All five
dependent source/target trees are the original F53 vertices, and
both Nat depth casts are stored inside the original F55 route.

Slots s3 and s4 are explicitly backward: the F55 pentagon has
4→3 and 0→4, rather than silently inverting a nonstrict cell. -/
def originalF45PentagonSignedSide
    (s : PentagonalSlot) :
    SignedOriginalF45PentagonSide
      (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄ s)
      (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄
        (pentagonalSlotNext s)) :=
  match s with
  | .s0 => .forward
      (OriginalF45BracketTree.DepthRotationRoute.leftContext
        (OriginalF45BracketTree.DepthRotationRoute.assoc t₁ t₂ t₃) t₄)
  | .s1 => .forward
      (OriginalF45BracketTree.DepthRotationRoute.assoc
        t₁ (OriginalF45BracketTree.node t₂ t₃) t₄)
  | .s2 => .forward
      (OriginalF45BracketTree.DepthRotationRoute.rightContext t₁
        (OriginalF45BracketTree.DepthRotationRoute.assoc t₂ t₃ t₄))
  | .s3 => .backward
      (OriginalF45BracketTree.DepthRotationRoute.assoc
        t₁ t₂ (OriginalF45BracketTree.node t₃ t₄))
  | .s4 => .backward
      (OriginalF45BracketTree.DepthRotationRoute.assoc
        (OriginalF45BracketTree.node t₁ t₂) t₃ t₄)

/-- EACH of the FIVE actual C60 geometric pentagon edges is labelled
by EXACTLY ONE real original F54 local rotation. The two inverse
geometric orientations are kept as directed witness metadata. -/
theorem originalF45PentagonSignedSide_rotationCount
    (s : PentagonalSlot) :
    (originalF45PentagonSignedSide t₁ t₂ t₃ t₄ s).rotationCount = 1 := by
  cases s <;> rfl

/-- The genuine five-sided geometric boundary carries five real
original F54 rotation edges: three along the long F55 route and
two oppositely oriented along the shorter F55 route. -/
theorem originalF45PentagonFiveRotationCount :
    (([PentagonalSlot.s0, .s1, .s2, .s3, .s4] :
      List PentagonalSlot).map
        (fun s => (originalF45PentagonSignedSide t₁ t₂ t₃ t₄ s).rotationCount)).sum =
      5 := by
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
    originalF45PentagonSignedSide_rotationCount]
  decide

/-- A fully typed bridge on one REAL truncated C60 pentagon boundary
edge: its actual pentagon/hexagon four-flag incidence square and
the specifically assigned original F55 signed one-rotation path. -/
structure OriginalF45C60GluedPentagonSide
    (v : IcosahedralVertex) (s : PentagonalSlot) where
  incidenceSquare :
    TruncatedEdgeFlagSquare (.around ⟨v, s⟩)
  pentagonFace :
    incidenceSquare.firstFace = .aroundVertex v
  rotation :
    SignedOriginalF45PentagonSide
      (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄ s)
      (originalF45PentagonIndexedVertex t₁ t₂ t₃ t₄
        (pentagonalSlotNext s))

/-- Actual C60 geometry and F55 proof-relevant rotation are
CONSTRUCTED, not existentially stipulated, at each of five slots. -/
noncomputable def originalF45C60GluedPentagonSide
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    OriginalF45C60GluedPentagonSide t₁ t₂ t₃ t₄ v s :=
  {
    incidenceSquare := aroundPentagonHexagonSquare ⟨v, s⟩
    pentagonFace := rfl
    rotation := originalF45PentagonSignedSide t₁ t₂ t₃ t₄ s
  }

/-- Each edge-local square in the explicitly glued pentagon is a
real C60 pentagon/hexagon shared-edge incidence, and its assigned
F55 original rotation has exactly one genuinely witnessed step. -/
theorem originalF45C60GluedPentagonSide_valid
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    (originalF45C60GluedPentagonSide t₁ t₂ t₃ t₄ v s).incidenceSquare.firstFace =
      .aroundVertex v ∧
    (originalF45C60GluedPentagonSide t₁ t₂ t₃ t₄ v s).rotation.rotationCount =
      1 := by
  constructor
  · exact (originalF45C60GluedPentagonSide t₁ t₂ t₃ t₄ v s).pentagonFace
  · exact originalF45PentagonSignedSide_rotationCount t₁ t₂ t₃ t₄ s

/-- A specific REAL C60 closed five-edge geometric pentagon,
its five distinct original F55 typed rotation labels and all
five genuine attached four-flag squares, together with the ACTUAL
F55 Type-valued pentagon higher generator. -/
structure OriginalF45C60PentagonPasting (v : IcosahedralVertex) where
  sides : (s : PentagonalSlot) →
    OriginalF45C60GluedPentagonSide t₁ t₂ t₃ t₄ v s
  pentagonCell :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (OriginalF45BracketTree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄)

/-- Canonical ACTUAL geometric-to-typed F55 pentagon patch on EACH
of the twelve existing C60 pentagons. The boundary source is exactly
the v3.85 cyclic pentagon rather than a newly invented five-cycle. -/
noncomputable def originalF45C60PentagonPasting
    (v : IcosahedralVertex) :
    OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v :=
  {
    sides := fun s => originalF45C60GluedPentagonSide t₁ t₂ t₃ t₄ v s
    pentagonCell :=
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell.pentagon
        t₁ t₂ t₃ t₄
  }

/-- Every geometric pentagon-patch side is truly supported on the
same ORIGINAL v3.85 C60 pentagon and labelled by one rotation. -/
theorem originalF45C60PentagonPasting_valid
    (v : IcosahedralVertex) (s : PentagonalSlot) :
    ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).pentagonFace =
      (originalF45C60GluedPentagonSide t₁ t₂ t₃ t₄ v s).pentagonFace ∧
    ((originalF45C60PentagonPasting t₁ t₂ t₃ t₄ v).sides s).rotation.rotationCount =
      1 := by
  constructor
  · rfl
  · exact originalF45PentagonSignedSide_rotationCount t₁ t₂ t₃ t₄ s

/-- The ACTUAL higher pentagon generator, now packaged with all five
C60 edge-local flag squares, can be interpreted in any independently
SUPPLIED F56 higher-cell target. No target 3-cell is inferred solely
from combinatorial arity or quotient endpoint equality. -/
def OriginalF45C60PentagonPasting.interpret
    (patch : OriginalF45C60PentagonPasting t₁ t₂ t₃ t₄ v)
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E) :
    target.Cell
      (OriginalF45BracketTree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (OriginalF45BracketTree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄) :=
  patch.pentagonCell.interpret target

#print axioms OriginalF45PentagonIndexedVertex
#print axioms SignedOriginalF45PentagonSide
#print axioms SignedOriginalF45PentagonSide.rotationCount
#print axioms originalF45PentagonIndexedVertex
#print axioms originalF45PentagonSignedSide
#print axioms originalF45PentagonSignedSide_rotationCount
#print axioms originalF45PentagonFiveRotationCount
#print axioms OriginalF45C60GluedPentagonSide
#print axioms originalF45C60GluedPentagonSide
#print axioms originalF45C60GluedPentagonSide_valid
#print axioms OriginalF45C60PentagonPasting
#print axioms originalF45C60PentagonPasting
#print axioms originalF45C60PentagonPasting_valid
#print axioms OriginalF45C60PentagonPasting.interpret

end ActualFourSubtrees

end
end KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
