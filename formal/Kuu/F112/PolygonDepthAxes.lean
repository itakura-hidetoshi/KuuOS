import Kuu.F112.PolygonBracketThreeCategory

/-!
# F112-E7A / two independent depth axes on authentic C60 sector brackets

The historical F54 carried two separately indexed Nat depths and
explicit equality transports. This NEW construction equips the genuine
C60-sector bracket tree with TWO additive depth axes, proves their
associative reindexing and constructs typed transports without
importing old KUOS, Gray, F51 or F77.

The two axes are deliberately independent data: no equivalence to
historical Blocks or F19/F28 depths is asserted.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- A real C60 polygon-sector leaf carries two independent natural
depth weights. -/
structure PolygonDepthLeaf (p : Polygon) where
  sector : PolygonBoundarySector p
  firstDepth : Nat
  secondDepth : Nat

/-- A genuinely typed, binary source with TWO independent Nat indices. -/
inductive PolygonDepthTree (p : Polygon) : Nat → Nat → Type where
  | leaf (x : PolygonDepthLeaf p) :
      PolygonDepthTree p x.firstDepth x.secondDepth
  | node {n m k l : Nat}
      (left : PolygonDepthTree p n m)
      (right : PolygonDepthTree p k l) :
      PolygonDepthTree p (n + k) (m + l)

/-- Forget only the numerical indices; preserve the original sector
witnesses and binary association. -/
def PolygonDepthTree.erase {p : Polygon} :
    {n m : Nat} → PolygonDepthTree p n m → PolygonBracketTree p
  | _, _, .leaf x => .leaf x.sector
  | _, _, .node a b => .node a.erase b.erase

/-- Transporting BOTH independent depth indices leaves the
unindexed, genuinely sector-bearing bracket source unchanged.
The proof is by equality induction, so there is no attempt to
rewrite through a dependent Eq.rec motive. -/
theorem PolygonDepthTree.erase_cast {p : Polygon}
    {n n' m m' : Nat}
    (hn : n = n') (hm : m = m') (t : PolygonDepthTree p n m) :
    (cast (congrArg₂ (PolygonDepthTree p) hn hm) t).erase =
      t.erase := by
  cases hn
  cases hm
  rfl

/-- Explicit dependent transport along both Nat associativities.
The ORIGINAL four-index boundary and genuine physical sector leaves
are retained; only the parentheses on the two Nat indices change. -/
def polygonDepthAssoc {p : Polygon}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃) :
    PolygonDepthTree p ((n₁ + n₂) + n₃) ((m₁ + m₂) + m₃) :=
  cast (congrArg₂ (PolygonDepthTree p)
    (Nat.add_assoc n₁ n₂ n₃).symm
    (Nat.add_assoc m₁ m₂ m₃).symm)
    (.node a (.node b c))

/-- The concrete Nat transport is erased exactly, yielding the
original F54-shaped association. No erasure of physical sectors. -/
theorem polygonDepthAssoc_erase {p : Polygon}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃) :
    (polygonDepthAssoc a b c).erase =
      .node a.erase (.node b.erase c.erase) := by
  change
    (cast (congrArg₂ (PolygonDepthTree p)
      (Nat.add_assoc n₁ n₂ n₃).symm
      (Nat.add_assoc m₁ m₂ m₃).symm)
      (.node a (.node b c))).erase =
        (.node a.erase (.node b.erase c.erase))
  exact PolygonDepthTree.erase_cast
    (Nat.add_assoc n₁ n₂ n₃).symm
    (Nat.add_assoc m₁ m₂ m₃).symm
    (.node a (.node b c))

/-- The two axes can vary independently on the SAME genuine
physical sector, without a fabricated change of physical face. -/
def polygonDepthLeafAt (p : Polygon) (i : PolygonBoundarySector p)
    (n m : Nat) : PolygonDepthTree p n m :=
  .leaf ⟨i, n, m⟩

theorem polygonDepthLeafAt_erase (p : Polygon)
    (i : PolygonBoundarySector p) (n m : Nat) :
    (polygonDepthLeafAt p i n m).erase =
      PolygonBracketTree.leaf i := rfl

/-- The first and second depth weights are independent even for
the actual north pentagon's first physical sector. -/
def northDepthFirst : PolygonDepthTree (.pentagon .north) 1 0 :=
  polygonDepthLeafAt (.pentagon .north)
    (firstFourPolygonSector (.pentagon .north) 0) 1 0

def northDepthSecond : PolygonDepthTree (.pentagon .north) 0 1 :=
  polygonDepthLeafAt (.pentagon .north)
    (firstFourPolygonSector (.pentagon .north) 0) 0 1

theorem northDepthAxes_same_physical_leaf :
    northDepthFirst.erase = northDepthSecond.erase := rfl

#print axioms PolygonDepthTree.erase
#print axioms PolygonDepthTree.erase_cast
#print axioms polygonDepthAssoc
#print axioms polygonDepthAssoc_erase
#print axioms polygonDepthLeafAt_erase
#print axioms northDepthAxes_same_physical_leaf
end
end Kuu.F112.Physical
