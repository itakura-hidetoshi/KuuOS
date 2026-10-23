import Kuu.F112.PolygonNativeF55P94DK5OrientedNaturalityObstruction
import Mathlib.Tactic

/-!
# F112-P94D3I — constructive K₅ nine-face global graph shelling

The genuine P94D3A oriented faces act on NINE monotone paths from
the actual left-associated F45 vertex 13 to the right-associated
vertex 0.  All nine faces fit into ONE explicitly oriented, closed
nine-step rewrite cycle; every face is used once with its correct
outward orientation and exact shared prefix/suffix.

These are genuine graph-level spine equalities certified by finite
computation.  They DO NOT yet identify the native F54 route syntax
on the two legs with a single globally pasted TYPE-valued three-cell.
The next proof must construct the dependent F54 route transports and
P92B whiskerings.  Neither equality of shadows nor a graph cycle is
a four-dimensional filler.

No Gray, sorry, admit, new logical axioms, or public-root changes.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- All nine explicitly distinct directed 13-to-0 F54 graph spines.
Each arrow is one of the 21 ORIGINAL genuine native-F54 rotation
edges.  This is not a quotient of the dependent F45 source terms. -/
def nativeK5GlobalMonotonePath (i : Fin 9) : List (Fin 14) :=
  match i.val with
  | 0 => [13, 8, 5, 0]
  | 1 => [13, 8, 7, 2, 0]
  | 2 => [13, 11, 6, 1, 0]
  | 3 => [13, 11, 6, 5, 0]
  | 4 => [13, 11, 9, 3, 1, 0]
  | 5 => [13, 12, 7, 2, 0]
  | 6 => [13, 12, 10, 4, 2, 0]
  | 7 => [13, 12, 10, 4, 3, 1, 0]
  | 8 => [13, 12, 10, 9, 3, 1, 0]
  | _ => []

/-- The path list is injectively enumerated: no repeated 13-to-0
graph path is hidden in the subsequent nine-face cycle. -/
theorem nativeK5GlobalMonotonePath_nodup :
    ((List.finRange 9).map nativeK5GlobalMonotonePath).Nodup := by
  decide

/-- All displayed paths share the same actual K₅ graph anchors. -/
theorem nativeK5GlobalMonotonePath_endpoints (i : Fin 9) :
    (nativeK5GlobalMonotonePath i).head? = some (13 : Fin 14) ∧
      (nativeK5GlobalMonotonePath i).getLast? = some (0 : Fin 14) := by
  fin_cases i <;> decide

/-- EVERY step of EVERY path belongs to the original typed-F54
21-edge K₅ graph; there is no invented diagonal. -/
theorem nativeK5GlobalMonotonePath_edges (i : Fin 9) :
    (nativeK5GraphLegEdges (nativeK5GlobalMonotonePath i)).all
      nativeK5GraphHasOrientedEdge = true := by
  fin_cases i <;> decide

/-- Choose the true outward direction on each of the nine anchored
faces, notably reversing square #2 and pentagons #5,#7,#8. -/
def nativeK5OutwardInput (f : Fin 9) : List (Fin 14) :=
  if nativeK5FaceReverseOrientation f then
    nativeK5FaceShortGraphVertices f
  else nativeK5FaceLongGraphVertices f

def nativeK5OutwardOutput (f : Fin 9) : List (Fin 14) :=
  if nativeK5FaceReverseOrientation f then
    nativeK5FaceLongGraphVertices f
  else nativeK5FaceShortGraphVertices f

/-- One oriented rewrite of WHOLE directed 13-to-0 graph paths.
Prefix/suffix are explicit: no unproved global route casts. -/
structure NativeK5GraphShellingStep where
  source : Fin 9
  target : Fin 9
  face : Fin 9
  prePath : List (Fin 14)
  postPath : List (Fin 14)
  deriving Repr

/-- One complete outward global K₅ shelling, in cyclic order:
paths 0→3→2→4→8→7→6→5→1→0; faces 7,0,5,8,1,3,6,2,4.
The face order is NOT the tag order of P94D3H's formal word. -/
def nativeK5GraphShellingStep (k : Fin 9) : NativeK5GraphShellingStep :=
  match k.val with
  | 0 => ⟨0, 3, 7, [], [0]⟩
  | 1 => ⟨3, 2, 0, [13, 11], []⟩
  | 2 => ⟨2, 4, 5, [13], [0]⟩
  | 3 => ⟨4, 8, 8, [], [3, 1, 0]⟩
  | 4 => ⟨8, 7, 1, [13, 12], [1, 0]⟩
  | 5 => ⟨7, 6, 3, [13, 12, 10], []⟩
  | 6 => ⟨6, 5, 6, [13], [0]⟩
  | 7 => ⟨5, 1, 2, [], [2, 0]⟩
  | 8 => ⟨1, 0, 4, [13], []⟩
  | _ => ⟨0, 0, 0, [], []⟩

/-- Both full directed global paths are EXACT prefix/face/suffix
glue of the corresponding original oriented P94D3A face graph legs. -/
theorem nativeK5GraphShellingStep_exact (k : Fin 9) :
    let s := nativeK5GraphShellingStep k
    nativeK5GlobalMonotonePath s.source =
        s.prePath ++ nativeK5OutwardInput s.face ++ s.postPath ∧
      nativeK5GlobalMonotonePath s.target =
        s.prePath ++ nativeK5OutwardOutput s.face ++ s.postPath := by
  fin_cases k <;> decide

/-- The target of each step is literally the next step's source. -/
def nativeK5GraphShellingNext (k : Fin 9) : Fin 9 :=
  ⟨(k.val + 1) % 9, Nat.mod_lt _ (by decide)⟩

theorem nativeK5GraphShelling_closed (k : Fin 9) :
    (nativeK5GraphShellingStep k).target =
      (nativeK5GraphShellingStep (nativeK5GraphShellingNext k)).source := by
  fin_cases k <;> decide

/-- The source and target of the nine-step rewrite loop coincide,
without identifying any distinct underlying F54 routes. -/
theorem nativeK5GraphShelling_basepoint :
    (nativeK5GraphShellingStep 0).source =
      (nativeK5GraphShellingStep 8).target := by
  decide

/-- Every actual K₅ face occurs EXACTLY once in the oriented
nine-step shelling. In particular the reversed square #2 is not lost. -/
def nativeK5GraphShellingFaces : List (Fin 9) :=
  (List.finRange 9).map (fun k => (nativeK5GraphShellingStep k).face)

theorem nativeK5GraphShellingFaces_nodup :
    nativeK5GraphShellingFaces.Nodup := by
  decide

theorem nativeK5GraphShellingFaces_cover (f : Fin 9) :
    f ∈ nativeK5GraphShellingFaces := by
  fin_cases f <;> decide

#print axioms nativeK5GlobalMonotonePath_nodup
#print axioms nativeK5GlobalMonotonePath_endpoints
#print axioms nativeK5GlobalMonotonePath_edges
#print axioms nativeK5GraphShellingStep_exact
#print axioms nativeK5GraphShelling_closed
#print axioms nativeK5GraphShelling_basepoint
#print axioms nativeK5GraphShellingFaces_nodup
#print axioms nativeK5GraphShellingFaces_cover

end
end Kuu.F112.Physical
