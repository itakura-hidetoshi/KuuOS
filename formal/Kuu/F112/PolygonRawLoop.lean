import Kuu.F112.PolygonBoundary

/-!
# F112-C / genuine finite C60 polygon boundary loops

The previous F112-B layer certifies all twelve physical pentagon boundaries
and all twenty physical hexagon boundaries. Here every certified actual
side is interpreted as two proof-relevant original F69 raw incidence legs.
One DEPENDENT induction on prefix length, not a sequence of special-purpose
5/6 compositions, then constructs a single original-site raw loop.

The last dart is identified with the first dart by the proved cyclic
length of the physical polygon. The 5/6-sided loop remains distinct from
raw nil; no historical Gray/F51/F77 evaluator or quotient is imported.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

/-- A cyclically indexed real C60 dart; the default is never reached at
a certified original polygon side. -/
def cyclicBoundaryDart (p : Polygon) (i : Nat) : Dart :=
  (polygonBoundaryDarts p).getD (i % polygonSideCount p)
    (.first (.northSpoke 0))

def cyclicBoundaryEdge (p : Polygon) (i : Nat) : Edge :=
  (polygonBoundaryEdges p).getD (i % polygonSideCount p)
    (.cross (.northSpoke 0))

/-- Every legally indexed side in the genuine 5/6 polygon is one real
physical edge between its actual consecutive darts and on the same face. -/
theorem cyclicBoundarySide_real :
    ∀ (p : Polygon) (i : Fin 6), i.val < polygonSideCount p →
      edgeJoins (cyclicBoundaryEdge p i.val)
        (cyclicBoundaryDart p i.val)
        (cyclicBoundaryDart p (i.val + 1)) ∧
      edgeOnFace (cyclicBoundaryEdge p i.val) p ∧
      cyclicBoundaryEdge p i.val ∈ polygonBoundaryEdges p := by
  decide

/-- The two uncancelled genuine physical incidence arrows on a side. -/
def polygonRawSide (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p i.val))
      (Site.vertex (cyclicBoundaryDart p (i.val + 1))) :=
  rawBoundaryStep (cyclicBoundaryEdge p i.val)
    (cyclicBoundaryDart p i.val)
    (cyclicBoundaryDart p (i.val + 1))
    (cyclicBoundarySide_real p i hi).1

/-- Count forward and backward raw legs without introducing a quotient. -/
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

/-- Generic length-indexed dependent raw path: at stage k the target
is PRECISELY the kth genuine cyclic dart. Every gluing interface is
checked by the Lean kernel, for arbitrary k bounded by the polygon. -/
def polygonRawPrefix (p : Polygon) :
    (k : Nat) → k ≤ polygonSideCount p →
      Zigzag (Site.vertex (cyclicBoundaryDart p 0))
        (Site.vertex (cyclicBoundaryDart p k))
  | 0, _ => Zigzag.nil _
  | k + 1, hk => by
      have hklt : k < polygonSideCount p := Nat.lt_of_succ_le hk
      have hk' : k ≤ polygonSideCount p := Nat.le_of_lt hklt
      have hmax : polygonSideCount p ≤ 6 := by
        cases p <;> simp [polygonSideCount]
      let i : Fin 6 := ⟨k, Nat.lt_of_lt_of_le hklt hmax⟩
      have hi : i.val < polygonSideCount p := hklt
      exact append (polygonRawPrefix p k hk') (polygonRawSide p i hi)

/-- Proof that the physical kth dart at a full boundary traversal is
the original starting dart: a true 5/6-cycle, never an added edge. -/
theorem cyclicBoundary_closed (p : Polygon) :
    cyclicBoundaryDart p (polygonSideCount p) =
      cyclicBoundaryDart p 0 := by
  cases p <;> rfl

/-- A single closed, genuinely typed 10-/12-leg raw word for EVERY
authentic 5-/6-sided C60 physical polygon. -/
def polygonRawLoop (p : Polygon) :
    Zigzag (Site.vertex (cyclicBoundaryDart p 0))
      (Site.vertex (cyclicBoundaryDart p 0)) :=
  (congrArg Site.vertex (cyclicBoundary_closed p)) ▸
    polygonRawPrefix p (polygonSideCount p) (Nat.le_refl _)

/-- Transport of a target site does not erase either kind of raw leg. -/
theorem zigzagLegCount_transport {s t u : Site}
    (h : t = u) (z : Zigzag s t) :
    zigzagLegCount (h ▸ z) = zigzagLegCount z := by
  cases h
  rfl

/-- Dependent induction on the genuine certified prefix. The statement
is available for every partial boundary, not only the full 5/6 cycles. -/
theorem polygonRawPrefix_legCount (p : Polygon) :
    ∀ (k : Nat) (hk : k ≤ polygonSideCount p),
      zigzagLegCount (polygonRawPrefix p k hk) = 2 * k := by
  intro k
  induction k with
  | zero =>
      intro _
      rfl
  | succ k ih =>
      intro hk
      have hk' : k ≤ polygonSideCount p :=
        Nat.le_trans (Nat.le_succ k) hk
      have hsplit :
          zigzagLegCount (polygonRawPrefix p (k + 1) hk) =
            zigzagLegCount (polygonRawPrefix p k hk') + 2 := by
        simp only [polygonRawPrefix, zigzagLegCount_append,
          polygonRawSide_two]
      rw [hsplit, ih hk']
      simp [Nat.mul_succ]

/-- Exactly two genuine F69 raw legs per side, with no raw cancellation. -/
theorem polygonRawLoop_legCount (p : Polygon) :
    zigzagLegCount (polygonRawLoop p) = 2 * polygonSideCount p := by
  unfold polygonRawLoop
  rw [zigzagLegCount_transport]
  exact polygonRawPrefix_legCount p (polygonSideCount p) (Nat.le_refl _)

/-- The independently typed raw loop is NOT the identity/empty path. -/
theorem polygonRawLoop_ne_nil (p : Polygon) :
    polygonRawLoop p ≠ Zigzag.nil _ := by
  intro h
  have hz : zigzagLegCount (polygonRawLoop p) = 0 := by
    rw [h]
    rfl
  rw [polygonRawLoop_legCount] at hz
  cases p <;> simp [polygonSideCount] at hz

def pentagonRawLoop (v : Vertex) :=
  polygonRawLoop (.pentagon v)

def hexagonRawLoop (t : Triangle) :=
  polygonRawLoop (.hexagon t)

theorem pentagonRawLoop_ten (v : Vertex) :
    zigzagLegCount (pentagonRawLoop v) = 10 := by
  simpa [pentagonRawLoop, polygonSideCount] using
    polygonRawLoop_legCount (.pentagon v)

theorem hexagonRawLoop_twelve (t : Triangle) :
    zigzagLegCount (hexagonRawLoop t) = 12 := by
  simpa [hexagonRawLoop, polygonSideCount] using
    polygonRawLoop_legCount (.hexagon t)

#print axioms cyclicBoundarySide_real
#print axioms polygonRawSide
#print axioms zigzagLegCount_append
#print axioms polygonRawPrefix
#print axioms cyclicBoundary_closed
#print axioms polygonRawLoop
#print axioms zigzagLegCount_transport
#print axioms polygonRawPrefix_legCount
#print axioms polygonRawLoop_legCount
#print axioms polygonRawLoop_ne_nil
#print axioms pentagonRawLoop_ten
#print axioms hexagonRawLoop_twelve
end Kuu.F112.Physical
