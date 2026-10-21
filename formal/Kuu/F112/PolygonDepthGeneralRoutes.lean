import Kuu.F112.PolygonDepthSquare

/-!
# F112-E7F / arbitrary two-axis Nat depths: normalized physical routes

E7D and E7E proved the exact raw E6 pentagon/square 3-source bridge
at zero depth. Here we REMOVE that depth-zero limitation for the
genuine original C60 sector-indexed ROTATION ROUTES themselves.

The existing E7A polygonDepthAssoc carries two independent Nat.add_assoc
transports. Its codomain is a cast of a right-associated binary tree,
NOT definitionally the same arbitrary-depth tree. We build the
certified inverse transport and prove its cancellation by equality
induction, rather than applying an invalid rw inside dependent Eq.rec.

The resulting normalized associator is an ACTUAL E7B route with
source ((a b) c), target (a (b c)), at potentially DIFFERENT but
provably equal double-depth indices. This gives typed long/short
pentagon paths for arbitrary four double-depth leaves and both
disjoint-context square orders for arbitrary six double-depth leaves.

All raw paths remain distinct. Rotation count and genuine physical
sector order are preserved. This file does NOT assert that erasing
the additional cast/identity routing reproduces identical unquotiented
E6 words; a normalization/source 3-cell comparison is still required
before transporting E6B's pentagon and square generators to arbitrary
depths. No historical F54/F55 source equivalence is claimed.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- Two separate index-equality casts cancel for EVERY dependent
original C60 physical-sector tree. No Nat arithmetic simplification
or stronger proof irrelevance is assumed. -/
theorem PolygonDepthTree.cast_backward_forward
    {p : Polygon} {n n' m m' : Nat}
    (hn : n = n') (hm : m = m')
    (x : PolygonDepthTree p n' m') :
    cast (congrArg₂ (PolygonDepthTree p) hn hm)
      (cast (congrArg₂ (PolygonDepthTree p) hn.symm hm.symm) x) = x := by
  cases hn
  cases hm
  rfl

/-- A target renaming of the actual E7B raw route, justified
by a PROVED equality of target dependent bracket expressions.
It does not add a new generating rotation or identify proof terms. -/
def PolygonDepthRoute.castTarget
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b c : PolygonDepthTree p n' m'}
    (h : b = c) (r : PolygonDepthRoute p a b) :
    PolygonDepthRoute p a c := by
  cases h
  exact r

theorem PolygonDepthRoute.castTarget_count
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b c : PolygonDepthTree p n' m'}
    (h : b = c) (r : PolygonDepthRoute p a b) :
    (r.castTarget h).rotationCount = r.rotationCount := by
  cases h
  rfl

/-- The explicit E7A associator followed by the FORWARD original
Nat transports, with the certified back/forward cancellation,
produces the exact raw right-associated tree at arbitrary depths. -/
def polygonDepthAssocNormalized
    {p : Polygon} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃) :
    PolygonDepthRoute p
      (.node (.node a b) c)
      (.node a (.node b c)) := by
  let hn : (n₁ + n₂) + n₃ = n₁ + (n₂ + n₃) :=
    Nat.add_assoc n₁ n₂ n₃
  let hm : (m₁ + m₂) + m₃ = m₁ + (m₂ + m₃) :=
    Nat.add_assoc m₁ m₂ m₃
  have heq :
      cast (congrArg₂ (PolygonDepthTree p) hn hm)
        (polygonDepthAssoc a b c) = (.node a (.node b c)) := by
    change
      cast (congrArg₂ (PolygonDepthTree p) hn hm)
        (cast (congrArg₂ (PolygonDepthTree p)
          hn.symm hm.symm) (.node a (.node b c))) =
        (.node a (.node b c))
    exact PolygonDepthTree.cast_backward_forward hn hm
      (.node a (.node b c))
  exact PolygonDepthRoute.castTarget heq
    (.trans (.assoc a b c)
      (.castDepths hn hm (polygonDepthAssoc a b c)))

/-- The normalized associator contains ONE genuine E7B
binary rotation; the two independent Nat transports count ZERO. -/
theorem polygonDepthAssocNormalized_count
    {p : Polygon} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃) :
    (polygonDepthAssocNormalized a b c).rotationCount = 1 := by
  unfold polygonDepthAssocNormalized
  rw [PolygonDepthRoute.castTarget_count]
  rfl

/-- Full arbitrary-double-depth THREE-step associahedron route.
The four original physical-sector leaves may have any independent
Nat weights, including nonzero weights on EVERY leaf. -/
def polygonDepthPentagonLongGeneral
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) d)
      (.node a (.node b (.node c d))) :=
  .trans
    (.trans
      (.leftContext (polygonDepthAssocNormalized a b c) d)
      (polygonDepthAssocNormalized a (.node b c) d))
    (.rightContext a (polygonDepthAssocNormalized b c d))

/-- Alternative arbitrary-double-depth TWO-step pentagon path
with the same exactly typed source and target as the long route. -/
def polygonDepthPentagonShortGeneral
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) d)
      (.node a (.node b (.node c d))) :=
  .trans
    (polygonDepthAssocNormalized (.node a b) c d)
    (polygonDepthAssocNormalized a b (.node c d))

theorem polygonDepthPentagonLongGeneral_count
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    (polygonDepthPentagonLongGeneral a b c d).rotationCount = 3 := by
  change
    (polygonDepthAssocNormalized a b c).rotationCount +
      (polygonDepthAssocNormalized a (.node b c) d).rotationCount +
      (polygonDepthAssocNormalized b c d).rotationCount = 3
  rw [polygonDepthAssocNormalized_count,
    polygonDepthAssocNormalized_count,
    polygonDepthAssocNormalized_count]

theorem polygonDepthPentagonShortGeneral_count
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    (polygonDepthPentagonShortGeneral a b c d).rotationCount = 2 := by
  change
    (polygonDepthAssocNormalized (.node a b) c d).rotationCount +
      (polygonDepthAssocNormalized a b (.node c d)).rotationCount = 2
  rw [polygonDepthAssocNormalized_count,
    polygonDepthAssocNormalized_count]

theorem polygonDepthPentagonGeneral_ne
    {p : Polygon}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄) :
    polygonDepthPentagonLongGeneral a b c d ≠
      polygonDepthPentagonShortGeneral a b c d := by
  intro h
  have hc := congrArg PolygonDepthRoute.rotationCount h
  rw [polygonDepthPentagonLongGeneral_count,
    polygonDepthPentagonShortGeneral_count] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

/-- A full six-sector dual-depth exchange, left rotation first.
Both independent triples may have arbitrary, independently chosen
Nat weights; the two contexts are genuine raw E7B constructors. -/
def polygonDepthSquareLeftGeneral
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) (.node (.node d e) f))
      (.node (.node a (.node b c)) (.node d (.node e f))) :=
  .trans
    (.leftContext (polygonDepthAssocNormalized a b c) (.node (.node d e) f))
    (.rightContext (.node a (.node b c))
      (polygonDepthAssocNormalized d e f))

/-- Right rotation first, followed by the genuine left one,
over the identical six original physical-sector leaves. -/
def polygonDepthSquareRightGeneral
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    PolygonDepthRoute p
      (.node (.node (.node a b) c) (.node (.node d e) f))
      (.node (.node a (.node b c)) (.node d (.node e f))) :=
  .trans
    (.rightContext (.node (.node a b) c)
      (polygonDepthAssocNormalized d e f))
    (.leftContext (polygonDepthAssocNormalized a b c)
      (.node d (.node e f)))

theorem polygonDepthSquareLeftGeneral_count
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    (polygonDepthSquareLeftGeneral a b c d e f).rotationCount = 2 := by
  change
    (polygonDepthAssocNormalized a b c).rotationCount +
      (polygonDepthAssocNormalized d e f).rotationCount = 2
  rw [polygonDepthAssocNormalized_count,
    polygonDepthAssocNormalized_count]

theorem polygonDepthSquareRightGeneral_count
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    (polygonDepthSquareRightGeneral a b c d e f).rotationCount = 2 := by
  change
    (polygonDepthAssocNormalized d e f).rotationCount +
      (polygonDepthAssocNormalized a b c).rotationCount = 2
  rw [polygonDepthAssocNormalized_count,
    polygonDepthAssocNormalized_count]

/-- Inspect source proof constructors without dependent elimination
through the distinctly parenthesized depth-index expressions. -/
def PolygonDepthRoute.leadingContextTag {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'} :
    PolygonDepthRoute p a b → Nat
  | .leftContext _ _ => 1
  | .rightContext _ _ => 2
  | _ => 0

def PolygonDepthRoute.firstPastingTag {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'} :
    PolygonDepthRoute p a b → Nat
  | .trans u _ => u.leadingContextTag
  | _ => 0

/-- The two raw square paths are distinct EVEN WITH arbitrary
nonzero and independently chosen depths on all six physical sectors. -/
theorem polygonDepthSquareGeneral_ne
    {p : Polygon}
    {n₁ n₂ n₃ n₄ n₅ n₆ m₁ m₂ m₃ m₄ m₅ m₆ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃)
    (d : PolygonDepthTree p n₄ m₄)
    (e : PolygonDepthTree p n₅ m₅)
    (f : PolygonDepthTree p n₆ m₆) :
    polygonDepthSquareLeftGeneral a b c d e f ≠
      polygonDepthSquareRightGeneral a b c d e f := by
  intro h
  have ht := congrArg PolygonDepthRoute.firstPastingTag h
  change (1 : Nat) = 2 at ht
  exact (by decide : (1 : Nat) ≠ 2) ht

/-- A genuine original C60 physical leaf with independently chosen
source-depth weights; the physical sector is not a proxy for grade. -/
def polygonPhysicalWeightedLeaf (p : Polygon) (i : Fin 4)
    (n m : Nat) : PolygonDepthTree p n m :=
  polygonDepthLeafAt p (firstFourPolygonSector p i) n m

/-- An actual north C60 pentagon with four separately weighted
physical sectors, all of which may carry nonzero independent depths. -/
def northWeightedPentagonLong :
    PolygonDepthRoute (.pentagon .north)
      (.node
        (.node
          (.node
            (polygonPhysicalWeightedLeaf (.pentagon .north) 0 1 2)
            (polygonPhysicalWeightedLeaf (.pentagon .north) 1 3 4))
          (polygonPhysicalWeightedLeaf (.pentagon .north) 2 5 6))
        (polygonPhysicalWeightedLeaf (.pentagon .north) 3 7 8))
      (.node
        (polygonPhysicalWeightedLeaf (.pentagon .north) 0 1 2)
        (.node
          (polygonPhysicalWeightedLeaf (.pentagon .north) 1 3 4)
          (.node
            (polygonPhysicalWeightedLeaf (.pentagon .north) 2 5 6)
            (polygonPhysicalWeightedLeaf (.pentagon .north) 3 7 8)))) :=
  polygonDepthPentagonLongGeneral _ _ _ _

def northWeightedPentagonShort :
    PolygonDepthRoute (.pentagon .north)
      (.node
        (.node
          (.node
            (polygonPhysicalWeightedLeaf (.pentagon .north) 0 1 2)
            (polygonPhysicalWeightedLeaf (.pentagon .north) 1 3 4))
          (polygonPhysicalWeightedLeaf (.pentagon .north) 2 5 6))
        (polygonPhysicalWeightedLeaf (.pentagon .north) 3 7 8))
      (.node
        (polygonPhysicalWeightedLeaf (.pentagon .north) 0 1 2)
        (.node
          (polygonPhysicalWeightedLeaf (.pentagon .north) 1 3 4)
          (.node
            (polygonPhysicalWeightedLeaf (.pentagon .north) 2 5 6)
            (polygonPhysicalWeightedLeaf (.pentagon .north) 3 7 8)))) :=
  polygonDepthPentagonShortGeneral _ _ _ _

theorem northWeightedPentagon_ne :
    northWeightedPentagonLong ≠ northWeightedPentagonShort :=
  polygonDepthPentagonGeneral_ne _ _ _ _

#print axioms PolygonDepthTree.cast_backward_forward
#print axioms PolygonDepthRoute.castTarget_count
#print axioms polygonDepthAssocNormalized
#print axioms polygonDepthAssocNormalized_count
#print axioms polygonDepthPentagonLongGeneral_count
#print axioms polygonDepthPentagonShortGeneral_count
#print axioms polygonDepthPentagonGeneral_ne
#print axioms polygonDepthSquareLeftGeneral_count
#print axioms polygonDepthSquareRightGeneral_count
#print axioms polygonDepthSquareGeneral_ne
#print axioms northWeightedPentagon_ne
end
end Kuu.F112.Physical
