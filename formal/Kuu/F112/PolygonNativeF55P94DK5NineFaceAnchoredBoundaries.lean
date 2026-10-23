import Kuu.F112.PolygonNativeF55P94DK5NineGenuineFaceCells
import Mathlib.Data.List.Rotate
import Mathlib.Tactic

/-!
# F112-P94D3A: nine K₅ combinatorial face paths and dependent 3-cell anchors

The previous P94D1/D2 files supplied genuine original five-stage F45
vertices, 21 F54 one-rotation Type routes, and nine ORIGINAL F55 / NEW
P92B 3-cell generators. Here give EVERY K₅ face its TWO complete ordered
graph legs, check the 42 oriented face sides match the precise K₅
2-sphere, and anchor each P92B face comparison in the actual
dependent pair of bracket-tree endpoints.

Crucial distinction: rotation words on the combinatorial graph are
NOT automatically judgmentally identical to original F54 route syntax.
The new certificate records indexed, proof-relevant 3-cell source
and the graph-level carrier separately; it does not forge a raw
route equality, a 4D filling, or a universal 3-category coherence.

No Gray, no sorry or admit, no new logical axioms.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Nine real K₅ face tags; Type elimination is honest and does not
project Fin-membership Prop proofs into dependent execution data. -/
inductive NativeK5FaceTag where
  | square0 | square1 | square2
  | pentagon3 | pentagon4 | pentagon5
  | pentagon6 | pentagon7 | pentagon8
  deriving DecidableEq, Repr

def nativeK5FaceTagOfFin (f : Fin 9) : NativeK5FaceTag :=
  match f.val with
  | 0 => .square0
  | 1 => .square1
  | 2 => .square2
  | 3 => .pentagon3
  | 4 => .pentagon4
  | 5 => .pentagon5
  | 6 => .pentagon6
  | 7 => .pentagon7
  | _ => .pentagon8

def nativeK5FaceTagFin : NativeK5FaceTag → Fin 9
  | .square0 => 0
  | .square1 => 1
  | .square2 => 2
  | .pentagon3 => 3
  | .pentagon4 => 4
  | .pentagon5 => 5
  | .pentagon6 => 6
  | .pentagon7 => 7
  | .pentagon8 => 8

theorem nativeK5FaceTagFin_leftInverse (f : Fin 9) :
    nativeK5FaceTagFin (nativeK5FaceTagOfFin f) = f := by
  fin_cases f <;> rfl

/-- These are the genuine one-rotation edge *sequences* of the two
parallel routes on each closed K₅ face; they are the combinatorial
spines of the genuinely typed route witnesses. -/
def nativeK5FaceLongGraphVertices (f : Fin 9) : List (Fin 14) :=
  match f.val with
  | 0 => [(6 : Fin 14), (5 : Fin 14), (0 : Fin 14)]
  | 1 => [(10 : Fin 14), (9 : Fin 14), (3 : Fin 14)]
  | 2 => [(13 : Fin 14), (8 : Fin 14), (7 : Fin 14)]
  | 3 => [(4 : Fin 14), (3 : Fin 14), (1 : Fin 14), (0 : Fin 14)]
  | 4 => [(8 : Fin 14), (7 : Fin 14), (2 : Fin 14), (0 : Fin 14)]
  | 5 => [(11 : Fin 14), (9 : Fin 14), (3 : Fin 14), (1 : Fin 14)]
  | 6 => [(12 : Fin 14), (10 : Fin 14), (4 : Fin 14), (2 : Fin 14)]
  | 7 => [(13 : Fin 14), (11 : Fin 14), (6 : Fin 14), (5 : Fin 14)]
  | 8 => [(13 : Fin 14), (12 : Fin 14), (10 : Fin 14), (9 : Fin 14)]
  | _ => []

def nativeK5FaceShortGraphVertices (f : Fin 9) : List (Fin 14) :=
  match f.val with
  | 0 => [(6 : Fin 14), (1 : Fin 14), (0 : Fin 14)]
  | 1 => [(10 : Fin 14), (4 : Fin 14), (3 : Fin 14)]
  | 2 => [(13 : Fin 14), (12 : Fin 14), (7 : Fin 14)]
  | 3 => [(4 : Fin 14), (2 : Fin 14), (0 : Fin 14)]
  | 4 => [(8 : Fin 14), (5 : Fin 14), (0 : Fin 14)]
  | 5 => [(11 : Fin 14), (6 : Fin 14), (1 : Fin 14)]
  | 6 => [(12 : Fin 14), (7 : Fin 14), (2 : Fin 14)]
  | 7 => [(13 : Fin 14), (8 : Fin 14), (5 : Fin 14)]
  | 8 => [(13 : Fin 14), (11 : Fin 14), (9 : Fin 14)]
  | _ => []

/-- The oriented 3-cell is inverted on square 2 and pentagons 5/7/8,
matching the outward orientation of the WHOLE K₅ 2-sphere. The
quadrilateral generator always has ZERO P92B full shadow, but its
orientation still matters for noncommutative coherence. -/
def nativeK5FaceReverseOrientation (f : Fin 9) : Bool :=
  f.val = 2 || f.val = 5 || f.val = 7 || f.val = 8

def nativeK5FaceCycleFromLegs (f : Fin 9) : List (Fin 14) :=
  let long := nativeK5FaceLongGraphVertices f
  let short := nativeK5FaceShortGraphVertices f
  if nativeK5FaceReverseOrientation f then
    short ++ long.reverse.drop 1
  else
    long ++ short.reverse.drop 1

/-- Boundary cycle has no inferred second copy of its starting
point in the raw face-vertex record. -/
def nativeK5FaceCycleVertices (f : Fin 9) : List (Fin 14) :=
  (nativeK5FaceCycleFromLegs f).dropLast

def nativeK5FaceCycleEdgesFromLegs (f : Fin 9) :
    List (Fin 14 × Fin 14) :=
  let path := nativeK5FaceCycleFromLegs f
  List.zip path (path.drop 1)

/-- All nine oriented edge cycles are cyclic permutations of the
independently declared K₅ shell face edges. This is stronger than
checking merely their lengths or overall numerical charges. -/
theorem nativeK5FaceCycleEdges_exact (f : Fin 9) :
    List.IsRotated (nativeK5FaceEdges f)
      (nativeK5FaceCycleEdgesFromLegs f) := by
  fin_cases f <;> decide

theorem nativeK5FaceCycleVertices_exact (f : Fin 9) :
    List.IsRotated (nativeK5FaceVertices f)
      (nativeK5FaceCycleVertices f) := by
  fin_cases f <;> decide

/-- Underlying genuine F54 adjacency for EVERY STEP in either
leg of EVERY face. The independent typed F54 edge constructors
in P94D1 witness each unoriented graph edge. -/
def nativeK5GraphHasOrientedEdge (edge : Fin 14 × Fin 14) : Bool :=
  nativeK5GraphEdges.contains
    (if edge.1.val < edge.2.val then edge else (edge.2, edge.1))

def nativeK5GraphLegEdges (vs : List (Fin 14)) :
    List (Fin 14 × Fin 14) :=
  List.zip vs (vs.drop 1)

theorem nativeK5NineFaceLegs_actual_edges :
    ∀ f : Fin 9,
      (nativeK5GraphLegEdges (nativeK5FaceLongGraphVertices f)).all
        nativeK5GraphHasOrientedEdge = true ∧
      (nativeK5GraphLegEdges (nativeK5FaceShortGraphVertices f)).all
        nativeK5GraphHasOrientedEdge = true := by
  intro f
  fin_cases f <;> decide

/-- Recorded endpoints for all nine parallel F54 route alternatives.
These are not invented abstract vertices: the source tree indices
refer to the actual dependent sigma-typed native F45 terms. -/
def nativeK5FaceAnchorVertices (f : Fin 9) : Fin 14 × Fin 14 :=
  match f.val with
  | 0 => (6, 0)
  | 1 => (10, 3)
  | 2 => (13, 7)
  | 3 => (4, 0)
  | 4 => (8, 0)
  | 5 => (11, 1)
  | 6 => (12, 2)
  | 7 => (13, 5)
  | 8 => (13, 9)
  | _ => (0, 0)

theorem nativeK5FaceLegAnchors (f : Fin 9) :
    (nativeK5FaceLongGraphVertices f).head? =
      some (nativeK5FaceAnchorVertices f).1 ∧
    (nativeK5FaceShortGraphVertices f).head? =
      some (nativeK5FaceAnchorVertices f).1 ∧
    (nativeK5FaceLongGraphVertices f).getLast? =
      some (nativeK5FaceAnchorVertices f).2 ∧
    (nativeK5FaceShortGraphVertices f).getLast? =
      some (nativeK5FaceAnchorVertices f).2 := by
  fin_cases f <;> decide

/-- Real rotation counts: each quadrilateral compares 2 and 2,
each pentagon compares 3 and 2. The SOURCE remains two distinct
original F54 routes, not 4D coherence. -/
def nativeK5FaceExpectedCounts (f : Fin 9) : Nat × Nat :=
  if f.val < 3 then (2, 2) else (3, 2)

theorem nativeK5FaceGraphLegCounts (f : Fin 9) :
    ((nativeK5FaceLongGraphVertices f).length - 1,
      (nativeK5FaceShortGraphVertices f).length - 1) =
        nativeK5FaceExpectedCounts f := by
  fin_cases f <;> decide

theorem nativeK5FaceEdgesAndTypedAnchors_consistent (f : Fin 9) :
    (nativeK5FaceCycleEdgesFromLegs f).length =
      nativeK5FaceSize f ∧
    (nativeK5FaceCycleVertices f).length =
      nativeK5FaceSize f := by
  fin_cases f <;> decide

section FiveNativeStages

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- Fully dependent ORIGINAL F45 trees are retained at BOTH
common endpoints of a parallel pair of native F54 routes, and the
comparison is an ACTUAL P92B Type-valued 3-cell, not just shadow. -/
abbrev NativeK5AnchoredThreeCell (i j : Fin 14) :=
  Σ r : KuuNativeF45Tree.DepthRotationRoute p
    (nativeK5TypedVertex t1 t2 t3 t4 t5 i).2.2
    (nativeK5TypedVertex t1 t2 t3 t4 t5 j).2.2,
  Σ s : KuuNativeF45Tree.DepthRotationRoute p
    (nativeK5TypedVertex t1 t2 t3 t4 t5 i).2.2
    (nativeK5TypedVertex t1 t2 t3 t4 t5 j).2.2,
    NativeF55P92AssocComparison p r s

/-- Nine distinct exact source proof boundaries, ordered according
to the outward K₅ shell. Each face has its ORIGINAL typed 3-cell
generator with all dependent F45 intermediate Blocks and Nat casts. -/
def nativeK5AnchoredFace (tag : NativeK5FaceTag) :
    Σ ij : Fin 14 × Fin 14,
      NativeK5AnchoredThreeCell t1 t2 t3 t4 t5 ij.1 ij.2 := by
  cases tag
  · exact ⟨(6, 0), _, _, (nativeK5NaturalitySquare0 t1 t2 t3 t4 t5)⟩
  · exact ⟨(10, 3), _, _, (nativeK5NaturalitySquare1 t1 t2 t3 t4 t5)⟩
  · exact ⟨(13, 7), _, _, (NativeF55P92AssocComparison.symm (nativeK5NaturalitySquare2 t1 t2 t3 t4 t5))⟩
  · exact ⟨(4, 0), _, _, (nativeK5PentagonFace3 t1 t2 t3 t4 t5)⟩
  · exact ⟨(8, 0), _, _, (nativeK5PentagonFace4 t1 t2 t3 t4 t5)⟩
  · exact ⟨(11, 1), _, _, (NativeF55P92AssocComparison.symm (nativeK5PentagonFace5 t1 t2 t3 t4 t5))⟩
  · exact ⟨(12, 2), _, _, (nativeK5PentagonFace6 t1 t2 t3 t4 t5)⟩
  · exact ⟨(13, 5), _, _, (NativeF55P92AssocComparison.symm (nativeK5PentagonFace7 t1 t2 t3 t4 t5))⟩
  · exact ⟨(13, 9), _, _, (NativeF55P92AssocComparison.symm (nativeK5PentagonFace8 t1 t2 t3 t4 t5))⟩

/-- Recover exact graph source/target anchors from each ACTUAL
dependent type-indexed original P92B face source. -/
theorem nativeK5AnchoredFace_index (tag : NativeK5FaceTag) :
    (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).1 =
      nativeK5FaceAnchorVertices (nativeK5FaceTagFin tag) := by
  cases tag <;> rfl

/-- The full original F55/P92B shadow attached to each selected
dependent 3-cell agrees with the independently computed outward
orientation sign of its exact K₅ face. This does NOT infer 4-cell. -/
theorem nativeK5AnchoredFace_fullShadow (tag : NativeK5FaceTag) :
    (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.2.nativeShadow =
      nativeK5CandidateFaceShadow (nativeK5FaceTagFin tag) := by
  cases tag <;> rfl

/-- Nonnegative actual primitive original F54 rotation counts of
both sides of EACH anchored P92B 3-cell. Oriented reversed faces
swap (3,2) to (2,3); naturality squares remain (2,2). -/
def nativeK5AnchoredFaceExpectedCounts (tag : NativeK5FaceTag) : Nat × Nat :=
  match tag with
  | .square0 | .square1 | .square2 => (2, 2)
  | .pentagon3 | .pentagon4 | .pentagon6 => (3, 2)
  | .pentagon5 | .pentagon7 | .pentagon8 => (2, 3)

theorem nativeK5AnchoredFace_rotationCounts (tag : NativeK5FaceTag) :
    ((nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.1.rotationCount,
     (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.1.rotationCount) =
       nativeK5AnchoredFaceExpectedCounts tag := by
  cases tag <;> rfl

#print axioms nativeK5AnchoredFace
#print axioms nativeK5AnchoredFace_index
#print axioms nativeK5AnchoredFace_fullShadow
#print axioms nativeK5AnchoredFace_rotationCounts

end FiveNativeStages

#print axioms nativeK5FaceTagFin_leftInverse
#print axioms nativeK5FaceCycleEdges_exact
#print axioms nativeK5FaceCycleVertices_exact
#print axioms nativeK5NineFaceLegs_actual_edges
#print axioms nativeK5FaceLegAnchors
#print axioms nativeK5FaceGraphLegCounts
#print axioms nativeK5FaceEdgesAndTypedAnchors_consistent

end
end Kuu.F112.Physical
