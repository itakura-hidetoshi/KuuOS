import Kuu.F112.PolygonDepthTrace

/-!
# F112-E7H / arbitrary-depth C60 pentagon/square 3-sources by exact traces

E7F proved arbitrary, independently weighted two-Nat-depth
pentagon and disjoint-square rotation routes on original C60 sector
brackets. E7G proved that ordered source traces preserve EVERY
real physical rotation (including full typed bracket boundaries
and original generator witnesses), whereas mere double-depth
casts contribute no physical rotation events.

We now PROVE that the physical traces of the arbitrary-depth
3-vs-2 pentagon and left-first/right-first square routes coincide
with the corresponding ORIGINAL INDEPENDENT E6A raw source traces.
The raw E7B erasures may insert identity/transport witnesses,
so this is deliberately a trace equality, NOT raw proof-tree equality.

We provide a new, explicitly TRACE-BOUND Type-valued 3-source
comparison carrying an ACTUAL E6B nine-constructor raw 3-cell
together with individually PROVED source/target trace certificates.
The pentagon/square generators at ALL Nat depths are thus available
without inventing F55 raw equalities or inferring a lift from grades.

Full native integer charges and independent ZMod2 phase are retained.
This does not assert a historical F54/F55 equivalence, a raw E7C
3-Hom without trace quotient, or global Gray/F47 3-descent.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- All arbitrary-depth long pentagon physical events are EXACTLY
the original E6A three-rotation source event list, not just the same
count or some numerical phase. -/
theorem polygonDepthPentagonLongGeneral_trace
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    (polygonDepthPentagonLongGeneral a b c d).physicalTrace =
      (polygonBracketPentagonLong a.erase b.erase c.erase d.erase).physicalTrace := by
  change
    ((polygonDepthAssocNormalized a b c).physicalTrace.map
      (fun ev => ev.leftContext d.erase) ++
      (polygonDepthAssocNormalized a (.node b c) d).physicalTrace) ++
      (polygonDepthAssocNormalized b c d).physicalTrace.map
        (fun ev => ev.rightContext a.erase) =
    (polygonBracketPentagonLong a.erase b.erase c.erase d.erase).physicalTrace
  simp only [polygonDepthAssocNormalized_physicalTrace]
  all_goals rfl

/-- Same strong full event-sequence equality for the independently
presented two-rotation pentagon raw route at arbitrary depth weights. -/
theorem polygonDepthPentagonShortGeneral_trace
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    (polygonDepthPentagonShortGeneral a b c d).physicalTrace =
      (polygonBracketPentagonShort a.erase b.erase c.erase d.erase).physicalTrace := by
  change
    (polygonDepthAssocNormalized (.node a b) c d).physicalTrace ++
      (polygonDepthAssocNormalized a b (.node c d)).physicalTrace =
    (polygonBracketPentagonShort a.erase b.erase c.erase d.erase).physicalTrace
  simp only [polygonDepthAssocNormalized_physicalTrace]
  all_goals rfl

/-- At six arbitrary independent double depths, the left-first
physical E7B route has the SAME FULL E6A disjoint-square event trace. -/
theorem polygonDepthSquareLeftGeneral_trace
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    (polygonDepthSquareLeftGeneral a b c d e f).physicalTrace =
      (polygonBracketSquareLeftFirst
        (PolygonBracketRotation.assoc a.erase b.erase c.erase)
        (PolygonBracketRotation.assoc d.erase e.erase f.erase)).physicalTrace := by
  change
    (polygonDepthAssocNormalized a b c).physicalTrace.map
      (fun ev => ev.leftContext (PolygonBracketTree.node (PolygonBracketTree.node d.erase e.erase) f.erase)) ++
    (polygonDepthAssocNormalized d e f).physicalTrace.map
      (fun ev => ev.rightContext (PolygonBracketTree.node a.erase (PolygonBracketTree.node b.erase c.erase))) =
    (polygonBracketSquareLeftFirst
      (PolygonBracketRotation.assoc a.erase b.erase c.erase)
      (PolygonBracketRotation.assoc d.erase e.erase f.erase)).physicalTrace
  simp only [polygonDepthAssocNormalized_physicalTrace]
  all_goals rfl

/-- The other physical order retains the EXACT E6A right-first
generator trace. Their order remains observable and nontrivial. -/
theorem polygonDepthSquareRightGeneral_trace
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    (polygonDepthSquareRightGeneral a b c d e f).physicalTrace =
      (polygonBracketSquareRightFirst
        (PolygonBracketRotation.assoc a.erase b.erase c.erase)
        (PolygonBracketRotation.assoc d.erase e.erase f.erase)).physicalTrace := by
  change
    (polygonDepthAssocNormalized d e f).physicalTrace.map
      (fun ev => ev.rightContext (PolygonBracketTree.node (PolygonBracketTree.node a.erase b.erase) c.erase)) ++
    (polygonDepthAssocNormalized a b c).physicalTrace.map
      (fun ev => ev.leftContext (PolygonBracketTree.node d.erase (PolygonBracketTree.node e.erase f.erase))) =
    (polygonBracketSquareRightFirst
      (PolygonBracketRotation.assoc a.erase b.erase c.erase)
      (PolygonBracketRotation.assoc d.erase e.erase f.erase)).physicalTrace
  simp only [polygonDepthAssocNormalized_physicalTrace]
  all_goals rfl

/-- A new TRUE Type-valued SOURCE comparison: two arbitrary-depth
physical F54-like routes have an actual E6B F55-shaped raw 3-proof
whose EXACT typed physical-rotation event lists agree with those routes.
This does NOT identify their raw proof trees or manufacture E7C Homs
from numerical grade equality alone. -/
structure PolygonDepthTraceThreeCell
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (r s : PolygonDepthRoute p a b) where
  e6source : PolygonBracketRoute p a.erase b.erase
  e6target : PolygonBracketRoute p a.erase b.erase
  rawCell : PolygonBracketCell p e6source e6target
  source_trace : e6source.physicalTrace = r.physicalTrace
  target_trace : e6target.physicalTrace = s.physicalTrace

/-- Source-level physical pentagon 3-proof carried across arbitrary
independent double Nat depths, with BOTH exact event traces proved. -/
def polygonDepthPentagonGeneralTraceCell
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    PolygonDepthTraceThreeCell
      (polygonDepthPentagonLongGeneral a b c d)
      (polygonDepthPentagonShortGeneral a b c d) where
  e6source := polygonBracketPentagonLong a.erase b.erase c.erase d.erase
  e6target := polygonBracketPentagonShort a.erase b.erase c.erase d.erase
  rawCell := .pentagon a.erase b.erase c.erase d.erase
  source_trace := (polygonDepthPentagonLongGeneral_trace a b c d).symm
  target_trace := (polygonDepthPentagonShortGeneral_trace a b c d).symm

/-- Source-level disjoint-square 3-proof: both distinct E6B
rotation orders and their original event traces are witnesses. -/
def polygonDepthSquareGeneralTraceCell
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    PolygonDepthTraceThreeCell
      (polygonDepthSquareLeftGeneral a b c d e f)
      (polygonDepthSquareRightGeneral a b c d e f) where
  e6source := polygonBracketSquareLeftFirst
    (PolygonBracketRotation.assoc a.erase b.erase c.erase)
    (PolygonBracketRotation.assoc d.erase e.erase f.erase)
  e6target := polygonBracketSquareRightFirst
    (PolygonBracketRotation.assoc a.erase b.erase c.erase)
    (PolygonBracketRotation.assoc d.erase e.erase f.erase)
  rawCell := .disjointSquare
    (PolygonBracketRotation.assoc a.erase b.erase c.erase)
    (PolygonBracketRotation.assoc d.erase e.erase f.erase)
  source_trace := (polygonDepthSquareLeftGeneral_trace a b c d e f).symm
  target_trace := (polygonDepthSquareRightGeneral_trace a b c d e f).symm

/-- The full independent E6B source-native shadow of an ACTUAL
trace-bound 3-proof. Trace agreement does not erase phase or charges. -/
def PolygonDepthTraceThreeCell.nativeShadow
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {r s : PolygonDepthRoute p a b}
    (C : PolygonDepthTraceThreeCell r s) :
    PolygonBracketNativeShadow :=
  C.rawCell.nativeShadow

/-- Entirely proved full-source parity, now for EVERY arbitrary-depth
trace-bound 3-cell, not just a chosen numeric generator. -/
theorem PolygonDepthTraceThreeCell.phase_squareParity
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {r s : PolygonDepthRoute p a b}
    (C : PolygonDepthTraceThreeCell r s) :
    ((C.nativeShadow.1.2 : Int) : ZMod 2) =
      C.nativeShadow.2 :=
  C.rawCell.phase_squareParity

/-- Honest new E6B shadow nonlift persists under ALL arbitrary-depth
physical trace comparisons. This is NOT original historical Δ. -/
theorem PolygonDepthTraceThreeCell.no_shadow_delta
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {r s : PolygonDepthRoute p a b}
    (C : PolygonDepthTraceThreeCell r s) :
    C.nativeShadow ≠ (((0 : Int), (1 : Int)), (0 : ZMod 2)) :=
  C.rawCell.no_shadow_delta

theorem polygonDepthPentagonGeneralTraceCell_shadow
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    (polygonDepthPentagonGeneralTraceCell a b c d).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl

theorem polygonDepthSquareGeneralTraceCell_shadow
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    (polygonDepthSquareGeneralTraceCell a b c d e f).nativeShadow =
      (((0 : Int), (1 : Int)), (1 : ZMod 2)) := rfl

/-- A genuine C60 hexagon side with an INDEPENDENT pair of
arbitrary, possibly nonzero, original-source depth weights. -/
def polygonWeightedHexagonLeaf (t : Triangle) (i : Fin 6)
    (n m : Nat) : PolygonDepthTree (.hexagon t) n m :=
  polygonDepthLeafAt (.hexagon t) ⟨i, by simp [polygonSideCount]⟩ n m

/-- On SIX DISTINCT northern true C60 hexagon sides, all twelve
original Nat depth weights are nonzero. Its source and target retain
both exact F54-shaped raw contextual orders and their full traces. -/
def northWeightedHexagonTraceSquare :=
  polygonDepthSquareGeneralTraceCell
    (polygonWeightedHexagonLeaf (.top 0) 0 1 2)
    (polygonWeightedHexagonLeaf (.top 0) 1 3 4)
    (polygonWeightedHexagonLeaf (.top 0) 2 5 6)
    (polygonWeightedHexagonLeaf (.top 0) 3 7 8)
    (polygonWeightedHexagonLeaf (.top 0) 4 9 10)
    (polygonWeightedHexagonLeaf (.top 0) 5 11 12)

/-- Nonzero second charge and a nontrivial square exchange phase
survive despite ALL SIX original physical leaves having nonzero
independent two-axis depth weights. -/
theorem northWeightedHexagonTraceSquare_native :
    northWeightedHexagonTraceSquare.nativeShadow =
      (((0 : Int), (1 : Int)), (1 : ZMod 2)) := rfl

/-- The north genuine C60 pentagon with four separately nonzero
physical sector pairs also carries the actual E6B source generator. -/
def northWeightedPentagonTraceCell :=
  polygonDepthPentagonGeneralTraceCell
    (polygonPhysicalWeightedLeaf (.pentagon .north) 0 1 2)
    (polygonPhysicalWeightedLeaf (.pentagon .north) 1 3 4)
    (polygonPhysicalWeightedLeaf (.pentagon .north) 2 5 6)
    (polygonPhysicalWeightedLeaf (.pentagon .north) 3 7 8)

theorem northWeightedPentagonTraceCell_native :
    northWeightedPentagonTraceCell.nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl

#print axioms polygonDepthPentagonLongGeneral_trace
#print axioms polygonDepthPentagonShortGeneral_trace
#print axioms polygonDepthSquareLeftGeneral_trace
#print axioms polygonDepthSquareRightGeneral_trace
#print axioms polygonDepthPentagonGeneralTraceCell
#print axioms polygonDepthSquareGeneralTraceCell
#print axioms PolygonDepthTraceThreeCell.phase_squareParity
#print axioms PolygonDepthTraceThreeCell.no_shadow_delta
#print axioms polygonDepthPentagonGeneralTraceCell_shadow
#print axioms polygonDepthSquareGeneralTraceCell_shadow
#print axioms northWeightedHexagonTraceSquare_native
#print axioms northWeightedPentagonTraceCell_native
end
end Kuu.F112.Physical
