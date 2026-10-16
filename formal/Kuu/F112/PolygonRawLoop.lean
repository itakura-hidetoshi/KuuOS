import Kuu.F112.PolygonBoundary

/-!
# F112-C / real polygon boundaries as one closed Type-valued raw zigzag

The previous F112-B layer proves every one of 12 pentagons and 20 hexagons
has its genuine 5/6-cycle of original C60 edges, darts and incidences.
Here we COMPOSE those independently certified sides in the raw F69 zigzag
category, retaining original physical sites in dependent source/target
indices. The last side returns to the same original first physical dart.

The resulting cycle consists of 10 (pentagon) or 12 (hexagon) raw incidence
legs. It is NOT an original direct Site arrow, NOT an equality to nil and
NOT a silently contracted F42 2-source. No Gray/F51/F77 code is imported.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

/-- The actual old-dart cycle, with arithmetic wrapping only at the
PROVEN 5/6 boundary length; the default cannot occur for any valid side. -/
def cyclicBoundaryDart (p : Polygon) (i : Nat) : Dart :=
  (polygonBoundaryDarts p).getD (i % polygonSideCount p)
    (.first (.northSpoke 0))

def cyclicBoundaryEdge (p : Polygon) (i : Nat) : Edge :=
  (polygonBoundaryEdges p).getD (i % polygonSideCount p)
    (.cross (.northSpoke 0))

/-- Every genuine polygon and every legal 0..4/0..5 boundary slot has
its ORIGINAL incident physical edge joining these consecutive actual
darts, and not merely an abstract proxy path. -/
theorem cyclicBoundarySide_real :
    ∀ (p : Polygon) (i : Fin 6), i.val < polygonSideCount p →
      edgeJoins (cyclicBoundaryEdge p i.val)
        (cyclicBoundaryDart p i.val)
        (cyclicBoundaryDart p (i.val + 1)) ∧
      edgeOnFace (cyclicBoundaryEdge p i.val) p ∧
      cyclicBoundaryEdge p i.val ∈ polygonBoundaryEdges p := by
  decide

/-- A single genuine oriented boundary side has exactly the two
non-cancelled F69 raw legs: vertex -> original edge <- vertex. -/
def polygonRawSide (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p i.val))
      (Site.vertex (cyclicBoundaryDart p (i.val + 1))) :=
  rawBoundaryStep (cyclicBoundaryEdge p i.val)
    (cyclicBoundaryDart p i.val)
    (cyclicBoundaryDart p (i.val + 1))
    (cyclicBoundarySide_real p i hi).1

/-- The physical five-edge pentagon is an honest single CLOSED raw
zigzag. Source and target are the SAME actual first old dart. -/
def pentagonRawLoop (v : Vertex) :
    Zigzag
      (Site.vertex (cyclicBoundaryDart (.pentagon v) 0))
      (Site.vertex (cyclicBoundaryDart (.pentagon v) 0)) :=
  append (polygonRawSide (.pentagon v) (⟨0, by decide⟩ : Fin 6) (by decide))
    (append (polygonRawSide (.pentagon v) (⟨1, by decide⟩ : Fin 6) (by decide))
    (append (polygonRawSide (.pentagon v) (⟨2, by decide⟩ : Fin 6) (by decide))
    (append (polygonRawSide (.pentagon v) (⟨3, by decide⟩ : Fin 6) (by decide))
    (polygonRawSide (.pentagon v) (⟨4, by decide⟩ : Fin 6) (by decide)))))

/-- The real six-edge original-triangle hexagon is likewise a single
dependent, CLOSED original-site raw zigzag, with no square-face proxy. -/
def hexagonRawLoop (t : Triangle) :
    Zigzag
      (Site.vertex (cyclicBoundaryDart (.hexagon t) 0))
      (Site.vertex (cyclicBoundaryDart (.hexagon t) 0)) :=
  append (polygonRawSide (.hexagon t) (⟨0, by decide⟩ : Fin 6) (by decide))
    (append (polygonRawSide (.hexagon t) (⟨1, by decide⟩ : Fin 6) (by decide))
    (append (polygonRawSide (.hexagon t) (⟨2, by decide⟩ : Fin 6) (by decide))
    (append (polygonRawSide (.hexagon t) (⟨3, by decide⟩ : Fin 6) (by decide))
    (append (polygonRawSide (.hexagon t) (⟨4, by decide⟩ : Fin 6) (by decide))
    (polygonRawSide (.hexagon t) (⟨5, by decide⟩ : Fin 6) (by decide))))))

/-- All 32 physical C60 polygon boundaries are now single raw loops.
This is a concrete dependent expression, not merely a list of sides. -/
def polygonRawLoop (p : Polygon) :
    Zigzag (Site.vertex (cyclicBoundaryDart p 0))
      (Site.vertex (cyclicBoundaryDart p 0)) :=
  match p with
  | .pentagon v => pentagonRawLoop v
  | .hexagon t => hexagonRawLoop t

/-- Count genuine raw FORWARD and BACKWARD incidence legs separately
from polygon side count, without quotienting by localization. -/
def zigzagLegCount {s t : Site} : Zigzag s t → Nat
  | .nil _ => 0
  | .forward _ q => 1 + zigzagLegCount q
  | .backward _ q => 1 + zigzagLegCount q

theorem zigzagLegCount_append {s t u : Site}
    (p : Zigzag s t) (q : Zigzag t u) :
    zigzagLegCount (append p q) =
      zigzagLegCount p + zigzagLegCount q := by
  induction p with
  | nil _ => simp [append, zigzagLegCount]
  | forward h rest ih =>
      simp [append, zigzagLegCount, ih, Nat.add_assoc]
  | backward h rest ih =>
      simp [append, zigzagLegCount, ih, Nat.add_assoc]

theorem polygonRawSide_two (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    zigzagLegCount (polygonRawSide p i hi) = 2 := rfl

theorem pentagonRawLoop_ten (v : Vertex) :
    zigzagLegCount (pentagonRawLoop v) = 10 := by
  simp [pentagonRawLoop, zigzagLegCount_append, polygonRawSide_two]

theorem hexagonRawLoop_twelve (t : Triangle) :
    zigzagLegCount (hexagonRawLoop t) = 12 := by
  simp [hexagonRawLoop, zigzagLegCount_append, polygonRawSide_two]

/-- The original C60 polygon cycle has exactly TWICE its number of
uncancelled original incidence legs, rather than being silently nil. -/
theorem polygonRawLoop_legCount (p : Polygon) :
    zigzagLegCount (polygonRawLoop p) = 2 * polygonSideCount p := by
  cases p with
  | pentagon v =>
      simpa [polygonRawLoop, polygonSideCount] using pentagonRawLoop_ten v
  | hexagon t =>
      simpa [polygonRawLoop, polygonSideCount] using hexagonRawLoop_twelve t

/-- Each original five/six side raw word survives even though both its
endpoints coincide as genuine C60 physical darts. A separate relation,
if later specified, is needed to contract it. -/
theorem polygonRawLoop_ne_nil (p : Polygon) :
    polygonRawLoop p ≠ Zigzag.nil _ := by
  intro h
  have hzero : zigzagLegCount (polygonRawLoop p) = 0 := by
    rw [h]
    rfl
  rw [polygonRawLoop_legCount] at hzero
  cases p <;> simp [polygonSideCount] at hzero

#print axioms cyclicBoundarySide_real
#print axioms polygonRawSide
#print axioms pentagonRawLoop
#print axioms hexagonRawLoop
#print axioms polygonRawLoop
#print axioms zigzagLegCount_append
#print axioms polygonRawSide_two
#print axioms pentagonRawLoop_ten
#print axioms hexagonRawLoop_twelve
#print axioms polygonRawLoop_legCount
#print axioms polygonRawLoop_ne_nil
end Kuu.F112.Physical
