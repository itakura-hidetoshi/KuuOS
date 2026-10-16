import Kuu.F112.PolygonThreeProof

/-!
# F112-E6A / genuine C60-sector F54-shaped bracket rotation source

The historical F54 changes the association of *binary bracket trees*,
with independent depth-index transports. E4 instead changes a base
dart on a physical polygon boundary. These are NOT the same types.

This file constructs the FIRST INDEPENDENT F54-SHAPED source using
actual sectors of each of the 32 C60 polygons as the leaves of
binary bracket trees. It proves that genuine local reassociations
preserve the original ordered physical-sector boundary and constructs
two DISTINCT 3-vs-2-step routes through the classical associahedron
pentagon. There is no import of historical KUOS, Gray, F51 or F77,
no asserted equivalence to F54, and no new axiom.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- A binary bracket tree whose leaves are actual sides of ONE true
five- or six-sided C60 polygon. Unlike an arbitrary abstract leaf,
each leaf carries the checked original finite physical-sector index. -/
inductive PolygonBracketTree (p : Polygon) : Type where
  | leaf (i : PolygonBoundarySector p) : PolygonBracketTree p
  | node (left right : PolygonBracketTree p) : PolygonBracketTree p

/-- The ordered list of real sides is the boundary invariant of
any formal association change. -/
def PolygonBracketTree.leaves {p : Polygon} :
    PolygonBracketTree p → List (PolygonBoundarySector p)
  | .leaf i => [i]
  | .node a b => a.leaves ++ b.leaves

/-- One F54-shaped primitive binary reassociation; left/right
contexts are actual typed constructors, not fictional Site arrows. -/
inductive PolygonBracketRotation (p : Polygon) :
    PolygonBracketTree p → PolygonBracketTree p → Type where
  | assoc (a b c : PolygonBracketTree p) :
      PolygonBracketRotation p (.node (.node a b) c) (.node a (.node b c))
  | leftContext {a b : PolygonBracketTree p}
      (f : PolygonBracketRotation p a b) (c : PolygonBracketTree p) :
      PolygonBracketRotation p (.node a c) (.node b c)
  | rightContext (a : PolygonBracketTree p)
      {b c : PolygonBracketTree p} (f : PolygonBracketRotation p b c) :
      PolygonBracketRotation p (.node a b) (.node a c)

/-- EVERY primitive contextual association preserves exactly the
ordered, proof-carrying physical sectors. -/
theorem PolygonBracketRotation.leaves_sound
    {p : Polygon} {a b : PolygonBracketTree p}
    (f : PolygonBracketRotation p a b) : a.leaves = b.leaves := by
  induction f with
  | assoc a b c =>
      simp [PolygonBracketTree.leaves, List.append_assoc]
  | leftContext f c ih =>
      simpa only [PolygonBracketTree.leaves] using
        congrArg (fun x => x ++ c.leaves) ih
  | rightContext a f ih =>
      simpa only [PolygonBracketTree.leaves] using
        congrArg (fun x => a.leaves ++ x) ih

/-- Free finite F54-shaped routes, separate from E4 base-dart loops.
No quotient or interchange is silently imposed on this raw grammar. -/
inductive PolygonBracketRoute (p : Polygon) :
    PolygonBracketTree p → PolygonBracketTree p → Type where
  | ident (a : PolygonBracketTree p) : PolygonBracketRoute p a a
  | step {a b : PolygonBracketTree p}
      (f : PolygonBracketRotation p a b) : PolygonBracketRoute p a b
  | trans {a b c : PolygonBracketTree p}
      (f : PolygonBracketRoute p a b)
      (g : PolygonBracketRoute p b c) : PolygonBracketRoute p a c
  | leftContext {a b : PolygonBracketTree p}
      (f : PolygonBracketRoute p a b) (c : PolygonBracketTree p) :
      PolygonBracketRoute p (.node a c) (.node b c)
  | rightContext (a : PolygonBracketTree p)
      {b c : PolygonBracketTree p} (f : PolygonBracketRoute p b c) :
      PolygonBracketRoute p (.node a b) (.node a c)

/-- The ordered physical C60-sector source is stable along arbitrary
nested F54-like rotation routes. -/
theorem PolygonBracketRoute.leaves_sound
    {p : Polygon} {a b : PolygonBracketTree p}
    (f : PolygonBracketRoute p a b) : a.leaves = b.leaves := by
  induction f with
  | ident a => rfl
  | step f => exact f.leaves_sound
  | trans f g ihf ihg => exact ihf.trans ihg
  | leftContext f c ih =>
      simpa only [PolygonBracketTree.leaves] using
        congrArg (fun x => x ++ c.leaves) ih
  | rightContext a f ih =>
      simpa only [PolygonBracketTree.leaves] using
        congrArg (fun x => a.leaves ++ x) ih

/-- Count actual primitive reassociations, not contexts/identity.
This is a genuine raw-source invariant; no quotient is used. -/
def PolygonBracketRoute.rotationCount
    {p : Polygon} {a b : PolygonBracketTree p} :
    PolygonBracketRoute p a b → Nat
  | .ident _ => 0
  | .step _ => 1
  | .trans f g => f.rotationCount + g.rotationCount
  | .leftContext f _ => f.rotationCount
  | .rightContext _ f => f.rotationCount

/-- The five actual bracketing positions of four sector-bearing
trees. The geometry is C60, while these five vertices belong to
the *associahedron*, not to a fabricated 5-sided physical face. -/
def polygonBracketPentagon0 {p : Polygon}
    (a b c d : PolygonBracketTree p) : PolygonBracketTree p :=
  .node (.node (.node a b) c) d

def polygonBracketPentagon3 {p : Polygon}
    (a b c d : PolygonBracketTree p) : PolygonBracketTree p :=
  .node a (.node b (.node c d))

/-- F54-shaped THREE-step route:
((ab)c)d -> (a(bc))d -> a((bc)d) -> a(b(cd)). -/
def polygonBracketPentagonLong {p : Polygon}
    (a b c d : PolygonBracketTree p) :
    PolygonBracketRoute p
      (polygonBracketPentagon0 a b c d)
      (polygonBracketPentagon3 a b c d) :=
  .trans
    (.trans
      (.leftContext (.step (.assoc a b c)) d)
      (.step (.assoc a (.node b c) d)))
    (.rightContext a (.step (.assoc b c d)))

/-- F54-shaped TWO-step route:
((ab)c)d -> (ab)(cd) -> a(b(cd)). -/
def polygonBracketPentagonShort {p : Polygon}
    (a b c d : PolygonBracketTree p) :
    PolygonBracketRoute p
      (polygonBracketPentagon0 a b c d)
      (polygonBracketPentagon3 a b c d) :=
  .trans
    (.step (.assoc (.node a b) c d))
    (.step (.assoc a b (.node c d)))

theorem polygonBracketPentagonLong_count {p : Polygon}
    (a b c d : PolygonBracketTree p) :
    (polygonBracketPentagonLong a b c d).rotationCount = 3 := by
  rfl

theorem polygonBracketPentagonShort_count {p : Polygon}
    (a b c d : PolygonBracketTree p) :
    (polygonBracketPentagonShort a b c d).rotationCount = 2 := by
  rfl

/-- The original F54 pentagon phenomenon is reconstructed in a NEW
C60-sector grammar: three steps and two steps are distinct RAW terms,
even though they have the same properly typed bracket endpoints. -/
theorem polygonBracketPentagonLong_ne_short {p : Polygon}
    (a b c d : PolygonBracketTree p) :
    polygonBracketPentagonLong a b c d ≠
      polygonBracketPentagonShort a b c d := by
  intro h
  have hc := congrArg PolygonBracketRoute.rotationCount h
  rw [polygonBracketPentagonLong_count, polygonBracketPentagonShort_count] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

/-- Every polygon (five or six sides) provides four genuine ordered
original boundary-side witnesses, carrying certified bounds. -/
def firstFourPolygonSector (p : Polygon) (i : Fin 4) :
    PolygonBoundarySector p :=
  ⟨⟨i.val, Nat.lt_trans i.isLt (by decide : 4 < 6)⟩,
    Nat.lt_of_lt_of_le i.isLt (by
      cases p <;> simp [polygonSideCount] : 4 ≤ polygonSideCount p)⟩

def physicalFourBracketLeaf (p : Polygon) (i : Fin 4) :
    PolygonBracketTree p :=
  .leaf (firstFourPolygonSector p i)

/-- Four *actual adjacent C60 polygon sides*, never arbitrary objects. -/
def physicalFourBracketSource (p : Polygon) : PolygonBracketTree p :=
  polygonBracketPentagon0
    (physicalFourBracketLeaf p 0) (physicalFourBracketLeaf p 1)
    (physicalFourBracketLeaf p 2) (physicalFourBracketLeaf p 3)

/-- Both physical bracketing routes start with the real first four
ordered sectors of the SAME authentic pentagon/hexagon. -/
theorem physicalFourBracketSource_leaves (p : Polygon) :
    (physicalFourBracketSource p).leaves =
      [firstFourPolygonSector p 0, firstFourPolygonSector p 1,
        firstFourPolygonSector p 2, firstFourPolygonSector p 3] := by
  simp [physicalFourBracketSource, polygonBracketPentagon0,
    physicalFourBracketLeaf, PolygonBracketTree.leaves]

/-- The same four actual sides have an independently constructed,
typed original F69 physical raw zigzag (eight uncancelled legs).
This is a common geometric source, NOT an equivalence identifying
original F54 trees with E4 based-loop words. -/
def physicalFourBoundaryWord (p : Polygon) :
    Zigzag (Site.vertex (cyclicBoundaryDart p 0))
      (Site.vertex (cyclicBoundaryDart p 4)) :=
  polygonRawSegment p 0 4 (by
    cases p <;> simp [polygonSideCount])

theorem physicalFourBoundaryWord_legCount (p : Polygon) :
    zigzagLegCount (physicalFourBoundaryWord p) = 8 := by
  change zigzagLegCount
    (polygonRawSegment p 0 4 (by cases p <;> simp [polygonSideCount])) = 8
  rw [polygonRawSegment_legCount]
  rfl

/-- The north genuine C60 pentagon has different 3-step and
2-step raw F54-shaped bracket routes on its first four real sides. -/
theorem northPhysicalBracketPentagon_ne :
    polygonBracketPentagonLong
      (physicalFourBracketLeaf (.pentagon .north) 0)
      (physicalFourBracketLeaf (.pentagon .north) 1)
      (physicalFourBracketLeaf (.pentagon .north) 2)
      (physicalFourBracketLeaf (.pentagon .north) 3) ≠
    polygonBracketPentagonShort
      (physicalFourBracketLeaf (.pentagon .north) 0)
      (physicalFourBracketLeaf (.pentagon .north) 1)
      (physicalFourBracketLeaf (.pentagon .north) 2)
      (physicalFourBracketLeaf (.pentagon .north) 3) :=
  polygonBracketPentagonLong_ne_short _ _ _ _

#print axioms PolygonBracketRotation.leaves_sound
#print axioms PolygonBracketRoute.leaves_sound
#print axioms PolygonBracketRoute.rotationCount
#print axioms polygonBracketPentagonLong_count
#print axioms polygonBracketPentagonShort_count
#print axioms polygonBracketPentagonLong_ne_short
#print axioms firstFourPolygonSector
#print axioms physicalFourBracketSource_leaves
#print axioms physicalFourBoundaryWord_legCount
#print axioms northPhysicalBracketPentagon_ne
end
end Kuu.F112.Physical
