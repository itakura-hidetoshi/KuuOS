import Kuu.F112.PolygonSource

/-!
# F112-E1 / independently typed genuine C60 cyclic rotation paths

A rotation changes the original boundary base dart, not the physical
polygon or its five/six original edges. A rotation is constructed as
the real suffix from dart k to the closing dart, followed by the
original prefix from the first dart to dart k. The first and last
site are checked in the dependent raw Zigzag type.

Every boundary segment is composed from its actual physical edge
incidence arrows, with two uncancelled raw legs per edge. All proofs
are independent of historical Gray/F51/F77 and do NOT establish the
old F54 full higher source or F55 interchanger.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

/-- An actual consecutive subpath of a physical C60 polygon boundary,
whose starting vertex is NOT necessarily the original first dart. -/
def polygonRawSegment (p : Polygon) (start : Nat) :
    (k : Nat) → start + k ≤ polygonSideCount p →
      Zigzag (Site.vertex (cyclicBoundaryDart p start))
        (Site.vertex (cyclicBoundaryDart p (start + k)))
  | 0, _ => Zigzag.nil _
  | k + 1, hk => by
      have hlt : start + k < polygonSideCount p :=
        Nat.lt_of_succ_le hk
      have hk' : start + k ≤ polygonSideCount p := Nat.le_of_lt hlt
      have hmax : polygonSideCount p ≤ 6 := by
        cases p <;> simp [polygonSideCount]
      let i : Fin 6 := ⟨start + k, Nat.lt_of_lt_of_le hlt hmax⟩
      have hi : i.val < polygonSideCount p := hlt
      exact append (polygonRawSegment p start k hk') (polygonRawSide p i hi)

/-- A dependent segment is an honest ordered word of two incidence
legs per physically traversed original edge. -/
theorem polygonRawSegment_legCount (p : Polygon) (start : Nat) :
    ∀ (k : Nat) (hk : start + k ≤ polygonSideCount p),
      zigzagLegCount (polygonRawSegment p start k hk) = 2 * k := by
  intro k
  induction k with
  | zero =>
      intro hk
      rfl
  | succ k ih =>
      intro hk
      have hk' : start + k ≤ polygonSideCount p :=
        Nat.le_of_lt (Nat.lt_of_succ_le hk)
      have hstep :
          zigzagLegCount (polygonRawSegment p start (k + 1) hk) =
            zigzagLegCount (polygonRawSegment p start k hk') + 2 := by
        simp only [polygonRawSegment, zigzagLegCount_append, polygonRawSide_two]
      rw [hstep, ih hk']
      simp [Nat.mul_succ]

/-- A certified split at a genuine boundary dart.
The tail visits precisely the remaining original physical sides. -/
def polygonRotationTail (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p k))
      (Site.vertex (cyclicBoundaryDart p 0)) := by
  have hs : k + (polygonSideCount p - k) = polygonSideCount p :=
    Nat.add_sub_of_le hk
  have hbound : k + (polygonSideCount p - k) ≤ polygonSideCount p :=
    le_of_eq hs
  have hclose :
      Site.vertex (cyclicBoundaryDart p (k + (polygonSideCount p - k))) =
        Site.vertex (cyclicBoundaryDart p 0) :=
    congrArg Site.vertex
      ((congrArg (cyclicBoundaryDart p) hs).trans (cyclicBoundary_closed p))
  exact changeZigzagTarget hclose
    (polygonRawSegment p k (polygonSideCount p - k) hbound)

/-- The genuine F54-like cyclicly rotated RAW boundary path:
the original suffix followed by the original prefix, based at the
kth physical vertex. No arrow is inserted into the original Site. -/
def polygonRotatedRawLoop (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p k))
      (Site.vertex (cyclicBoundaryDart p k)) :=
  append (polygonRotationTail p k hk) (polygonRawPrefix p k hk)

/-- The split does not lose, identify or reverse any raw generators.
Both original 5/6-sided polygons have exactly 10/12 raw legs under
every cyclic rotation, even before any localization. -/
theorem polygonRotatedRawLoop_legCount (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    zigzagLegCount (polygonRotatedRawLoop p k hk) =
      2 * polygonSideCount p := by
  have htail :
      zigzagLegCount (polygonRotationTail p k hk) =
        2 * (polygonSideCount p - k) := by
    unfold polygonRotationTail
    rw [zigzagLegCount_transport]
    exact polygonRawSegment_legCount p k
      (polygonSideCount p - k) (by
        rw [Nat.add_sub_of_le hk])
  unfold polygonRotatedRawLoop
  rw [zigzagLegCount_append, htail, polygonRawPrefix_legCount p k hk]
  calc
    2 * (polygonSideCount p - k) + 2 * k =
        2 * ((polygonSideCount p - k) + k) := by
          rw [Nat.mul_add]
    _ = 2 * polygonSideCount p := by
          rw [Nat.sub_add_cancel hk]

/-- A change of chosen cyclic base dart never converts a real raw
polygon word into an empty identity path. -/
theorem polygonRotatedRawLoop_ne_nil (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    polygonRotatedRawLoop p k hk ≠ Zigzag.nil _ := by
  intro h
  have hzero : zigzagLegCount (polygonRotatedRawLoop p k hk) = 0 := by
    rw [h]
    rfl
  rw [polygonRotatedRawLoop_legCount p k hk] at hzero
  cases p <;> simp [polygonSideCount] at hzero

/-- Each of the physical 5/6 possible original boundary base darts
selects a separately typed cyclic raw word. -/
def polygonRotationAt (p : Polygon) (i : PolygonBoundarySector p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p i.1.val))
      (Site.vertex (cyclicBoundaryDart p i.1.val)) :=
  polygonRotatedRawLoop p i.1.val (Nat.le_of_lt i.2)

theorem polygonRotationAt_nonempty (p : Polygon)
    (i : PolygonBoundarySector p) :
    polygonRotationAt p i ≠ Zigzag.nil _ :=
  polygonRotatedRawLoop_ne_nil p i.1.val (Nat.le_of_lt i.2)

#print axioms polygonRawSegment
#print axioms polygonRawSegment_legCount
#print axioms polygonRotationTail
#print axioms polygonRotatedRawLoop
#print axioms polygonRotatedRawLoop_legCount
#print axioms polygonRotatedRawLoop_ne_nil
#print axioms polygonRotationAt_nonempty
end Kuu.F112.Physical
