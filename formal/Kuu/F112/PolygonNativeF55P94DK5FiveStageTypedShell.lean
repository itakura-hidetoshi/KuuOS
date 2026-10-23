import Kuu.F112.PolygonNativeF55P94CNonabelianWordObstruction
import Mathlib.Data.List.FinRange
import Mathlib.Tactic

/-!
# F112-P94D1 — five genuine F45 stages and the K₅ rotation/face shell

Build the 14 planar bracketings of FIVE distinct ordered original F45
stages, and all 21 ACTUAL one-rotation F54 depth routes, with the two
independent Nat histories and intermediate native block boundaries intact.

Independently check the combinatorial K₅ 2-sphere: 14 vertices,
21 unoriented edges, 6 oriented pentagons, 3 oriented squares; every
oriented face edge has exactly one oppositely oriented partner.
The three K₅ quadrilaterals are associator-naturality squares,
NOT automatically the original SIX-leaf disjointSquare generator.
The signed face-shadow bookkeeping has 3 positive + 3 negative
pentagons and zero-shaded naturality faces; it is deliberately NOT
a proof of a global, genuinely typed F55/P92B four-dimensional filler.

No new 4-cell constructor, logical axiom, Gray structure, sorry or admit.
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

/-- Five ordered leaves; this is the SHAPE receiver, not a quotient
of the original F45 proof-relevant execution histories. -/
inductive NativeK5Shape where
  | leaf (i : Fin 5)
  | node (left right : NativeK5Shape)
  deriving DecidableEq, Repr

def NativeK5Shape.leafOrder : NativeK5Shape → List (Fin 5)
  | .leaf i => [i]
  | .node a b => a.leafOrder ++ b.leafOrder

/-- Enumerate ALL Catalan(4)=14 ordered binary association shapes. -/
def nativeK5ShapeVertex (i : Fin 14) : NativeK5Shape :=
  match i.val with
  | 0 => (.node (.leaf (0 : Fin 5)) (.node (.leaf (1 : Fin 5)) (.node (.leaf (2 : Fin 5)) (.node (.leaf (3 : Fin 5)) (.leaf (4 : Fin 5))))))
  | 1 => (.node (.leaf (0 : Fin 5)) (.node (.leaf (1 : Fin 5)) (.node (.node (.leaf (2 : Fin 5)) (.leaf (3 : Fin 5))) (.leaf (4 : Fin 5)))))
  | 2 => (.node (.leaf (0 : Fin 5)) (.node (.node (.leaf (1 : Fin 5)) (.leaf (2 : Fin 5))) (.node (.leaf (3 : Fin 5)) (.leaf (4 : Fin 5)))))
  | 3 => (.node (.leaf (0 : Fin 5)) (.node (.node (.leaf (1 : Fin 5)) (.node (.leaf (2 : Fin 5)) (.leaf (3 : Fin 5)))) (.leaf (4 : Fin 5))))
  | 4 => (.node (.leaf (0 : Fin 5)) (.node (.node (.node (.leaf (1 : Fin 5)) (.leaf (2 : Fin 5))) (.leaf (3 : Fin 5))) (.leaf (4 : Fin 5))))
  | 5 => (.node (.node (.leaf (0 : Fin 5)) (.leaf (1 : Fin 5))) (.node (.leaf (2 : Fin 5)) (.node (.leaf (3 : Fin 5)) (.leaf (4 : Fin 5)))))
  | 6 => (.node (.node (.leaf (0 : Fin 5)) (.leaf (1 : Fin 5))) (.node (.node (.leaf (2 : Fin 5)) (.leaf (3 : Fin 5))) (.leaf (4 : Fin 5))))
  | 7 => (.node (.node (.leaf (0 : Fin 5)) (.node (.leaf (1 : Fin 5)) (.leaf (2 : Fin 5)))) (.node (.leaf (3 : Fin 5)) (.leaf (4 : Fin 5))))
  | 8 => (.node (.node (.node (.leaf (0 : Fin 5)) (.leaf (1 : Fin 5))) (.leaf (2 : Fin 5))) (.node (.leaf (3 : Fin 5)) (.leaf (4 : Fin 5))))
  | 9 => (.node (.node (.leaf (0 : Fin 5)) (.node (.leaf (1 : Fin 5)) (.node (.leaf (2 : Fin 5)) (.leaf (3 : Fin 5))))) (.leaf (4 : Fin 5)))
  | 10 => (.node (.node (.leaf (0 : Fin 5)) (.node (.node (.leaf (1 : Fin 5)) (.leaf (2 : Fin 5))) (.leaf (3 : Fin 5)))) (.leaf (4 : Fin 5)))
  | 11 => (.node (.node (.node (.leaf (0 : Fin 5)) (.leaf (1 : Fin 5))) (.node (.leaf (2 : Fin 5)) (.leaf (3 : Fin 5)))) (.leaf (4 : Fin 5)))
  | 12 => (.node (.node (.node (.leaf (0 : Fin 5)) (.node (.leaf (1 : Fin 5)) (.leaf (2 : Fin 5)))) (.leaf (3 : Fin 5))) (.leaf (4 : Fin 5)))
  | 13 => (.node (.node (.node (.node (.leaf (0 : Fin 5)) (.leaf (1 : Fin 5))) (.leaf (2 : Fin 5))) (.leaf (3 : Fin 5))) (.leaf (4 : Fin 5)))
  | _ => (.node (.leaf (0 : Fin 5)) (.node (.leaf (1 : Fin 5)) (.node (.leaf (2 : Fin 5)) (.node (.leaf (3 : Fin 5)) (.leaf (4 : Fin 5))))))

/-- Exact preserved five-leaf order at every K₅ vertex. -/
theorem nativeK5ShapeVertex_order (i : Fin 14) :
    (nativeK5ShapeVertex i).leafOrder =
      [(0 : Fin 5), 1, 2, 3, 4] := by
  fin_cases i <;> rfl

theorem nativeK5ShapeVertex_nodup :
    ((List.finRange 14).map nativeK5ShapeVertex).Nodup := by
  decide

/-- One elementary forward associativity rotation at the root. -/
def NativeK5Shape.rootForward : NativeK5Shape → NativeK5Shape → Bool
  | .node (.node a b) c, .node a' (.node b' c') =>
      decide (a = a' ∧ b = b' ∧ c = c')
  | _, _ => false

/-- One rotation in either direction, recursively in either context. -/
def NativeK5Shape.adjacent : NativeK5Shape → NativeK5Shape → Bool
  | .node a b, .node c d =>
      NativeK5Shape.rootForward (.node a b) (.node c d) ||
      NativeK5Shape.rootForward (.node c d) (.node a b) ||
      (NativeK5Shape.adjacent a c && decide (b = d)) ||
      (decide (a = c) && NativeK5Shape.adjacent b d)
  | _, _ => false

/-- The edges are computed from rotations rather than posited
independently of the actual fourteen association shapes. -/
def nativeK5GraphEdges : List (Fin 14 × Fin 14) :=
  (List.finRange 14).flatMap (fun i =>
    (List.finRange 14).filterMap (fun j =>
      if i.val < j.val ∧
          (nativeK5ShapeVertex i).adjacent (nativeK5ShapeVertex j) = true then
        some (i, j)
      else none))

theorem nativeK5GraphEdge_count : nativeK5GraphEdges.length = 21 := by
  decide

/-- An outward-oriented K₅ boundary, with face ordering
quadrilaterals 0..2 then pentagons 3..8. -/
def nativeK5FaceVertices (f : Fin 9) : List (Fin 14) :=
  match f.val with
  | 0 => [(0 : Fin 14), (1 : Fin 14), (6 : Fin 14), (5 : Fin 14)]
  | 1 => [(3 : Fin 14), (4 : Fin 14), (10 : Fin 14), (9 : Fin 14)]
  | 2 => [(7 : Fin 14), (8 : Fin 14), (13 : Fin 14), (12 : Fin 14)]
  | 3 => [(2 : Fin 14), (4 : Fin 14), (3 : Fin 14), (1 : Fin 14), (0 : Fin 14)]
  | 4 => [(5 : Fin 14), (8 : Fin 14), (7 : Fin 14), (2 : Fin 14), (0 : Fin 14)]
  | 5 => [(1 : Fin 14), (3 : Fin 14), (9 : Fin 14), (11 : Fin 14), (6 : Fin 14)]
  | 6 => [(7 : Fin 14), (12 : Fin 14), (10 : Fin 14), (4 : Fin 14), (2 : Fin 14)]
  | 7 => [(5 : Fin 14), (6 : Fin 14), (11 : Fin 14), (13 : Fin 14), (8 : Fin 14)]
  | 8 => [(9 : Fin 14), (10 : Fin 14), (12 : Fin 14), (13 : Fin 14), (11 : Fin 14)]
  | _ => []

def nativeK5FaceEdges (f : Fin 9) : List (Fin 14 × Fin 14) :=
  let vs := nativeK5FaceVertices f
  List.zip vs (vs.drop 1 ++ vs.take 1)

def nativeK5AllFaceEdges : List (Fin 14 × Fin 14) :=
  (List.finRange 9).flatMap nativeK5FaceEdges

def nativeK5FaceSize (f : Fin 9) : Nat :=
  (nativeK5FaceVertices f).length

theorem nativeK5Face_sizes :
    ((List.finRange 9).filter (fun f => nativeK5FaceSize f = 4)).length = 3 ∧
    ((List.finRange 9).filter (fun f => nativeK5FaceSize f = 5)).length = 6 := by
  decide

/-- Every side of each of the nine explicit faces really is a
one-step binary-tree reassociation. -/
theorem nativeK5FaceEdges_are_rotations :
    ∀ f : Fin 9, ∀ e ∈ nativeK5FaceEdges f,
      (nativeK5ShapeVertex e.1).adjacent (nativeK5ShapeVertex e.2) = true := by
  decide

/-- Closed oriented K₅ shell: 42 distinct directed face edges and
each opposite orientation appears ONCE. -/
theorem nativeK5Shell_oriented_edges :
    nativeK5AllFaceEdges.length = 42 ∧
    nativeK5AllFaceEdges.Nodup ∧
    (∀ e ∈ nativeK5AllFaceEdges,
      nativeK5AllFaceEdges.count (e.2, e.1) = 1) := by
  decide

theorem nativeK5Shell_euler : (14 : Int) - 21 + 9 = 2 := by
  norm_num

/-- The OUTWARD face orientation has three positive and three
negative pentagon loops. Associator naturality quadrilaterals
have ZERO full P92B shadow, unlike the original F55 disjointSquare
when realized on six genuine sectors. These are FORMAL face labels,
not yet an asserted lift of all nine boundaries to the native 3-source. -/
def nativeK5CandidateFaceShadow (f : Fin 9) : KuuNativeF55Shadow :=
  match f.val with
  | 3 | 4 | 6 => (((1 : Int), (0 : Int)), (0 : ZMod 2))
  | 5 | 7 | 8 => (((-1 : Int), (0 : Int)), (0 : ZMod 2))
  | _ => 0

theorem nativeK5CandidateFaceShadow_balanced :
    ((List.finRange 9).map nativeK5CandidateFaceShadow).sum =
      (0 : KuuNativeF55Shadow) := by
  decide

/-- A counterfactual assignment of ODD original disjointSquare phases
to all three K₅ quadrilaterals has a nonzero total parity. This is
a genuine combinatorial obstruction only UNDER that assignment,
not evidence that any K₅ naturality square actually has that phase. -/
def nativeK5HypotheticalOddSquarePhase (f : Fin 9) : ZMod 2 :=
  if f.val < 3 then 1 else 0

theorem nativeK5HypotheticalOddSquarePhase_nonzero :
    ((List.finRange 9).map nativeK5HypotheticalOddSquarePhase).sum ≠
      (0 : ZMod 2) := by
  decide

/-- Realize each abstract leaf with an ACTUAL physical C60
polygon-bracket tree. The fixed shape does not replace any
dependent F45 source proof. -/
def NativeK5Shape.realize {p : Polygon}
    (leaves : Fin 5 → PolygonBracketTree p) :
    NativeK5Shape → PolygonBracketTree p
  | .leaf i => leaves i
  | .node a b => .node (a.realize leaves) (b.realize leaves)

/-- Five independently typed consecutive ORIGINAL F45 source stages.
This is a dependent sigma because the 14 true Nat parenthesizations
need NOT be definitionally identical. No fake Nat casts are imposed. -/
def nativeK5TypedVertex
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
    {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
    (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
    (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)
    (i : Fin 14) :
    Σ n : Nat, Σ m : Nat, KuuNativeF45Tree p n m p₀ q₀ p₅ q₅ :=
  match i.val with
  | 0 => ⟨_, _, (.node t1 (.node t2 (.node t3 (.node t4 t5))))⟩
  | 1 => ⟨_, _, (.node t1 (.node t2 (.node (.node t3 t4) t5)))⟩
  | 2 => ⟨_, _, (.node t1 (.node (.node t2 t3) (.node t4 t5)))⟩
  | 3 => ⟨_, _, (.node t1 (.node (.node t2 (.node t3 t4)) t5))⟩
  | 4 => ⟨_, _, (.node t1 (.node (.node (.node t2 t3) t4) t5))⟩
  | 5 => ⟨_, _, (.node (.node t1 t2) (.node t3 (.node t4 t5)))⟩
  | 6 => ⟨_, _, (.node (.node t1 t2) (.node (.node t3 t4) t5))⟩
  | 7 => ⟨_, _, (.node (.node t1 (.node t2 t3)) (.node t4 t5))⟩
  | 8 => ⟨_, _, (.node (.node (.node t1 t2) t3) (.node t4 t5))⟩
  | 9 => ⟨_, _, (.node (.node t1 (.node t2 (.node t3 t4))) t5)⟩
  | 10 => ⟨_, _, (.node (.node t1 (.node (.node t2 t3) t4)) t5)⟩
  | 11 => ⟨_, _, (.node (.node (.node t1 t2) (.node t3 t4)) t5)⟩
  | 12 => ⟨_, _, (.node (.node (.node t1 (.node t2 t3)) t4) t5)⟩
  | 13 => ⟨_, _, (.node (.node (.node (.node t1 t2) t3) t4) t5)⟩
  | _ => ⟨_, _, (.node t1 (.node t2 (.node t3 (.node t4 t5))))⟩

/-- The exact ordered physical-sector leaves are identical at all
14 genuinely typed native-F45 association trees. -/
theorem nativeK5TypedVertex_sectors
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
    {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
    (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
    (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)
    (i : Fin 14) :
    (nativeK5TypedVertex t1 t2 t3 t4 t5 i).2.2.sectors =
      t1.sectors ++ t2.sectors ++ t3.sectors ++ t4.sectors ++ t5.sectors := by
  fin_cases i <;>
    simp [nativeK5TypedVertex, KuuNativeF45Tree.sectors, List.append_assoc]

/-- A computationally closed twenty-one-constructor Type of ACTUAL
one-step Tamari rotation edges. Unlike `Fin 21` plus `fin_cases`,
elimination from this genuine inductive Type into a dependent
Type-valued F54 route is permitted by Lean's recursor. -/
inductive NativeK5TypedEdgeTag where
  | e0
  | e1
  | e2
  | e3
  | e4
  | e5
  | e6
  | e7
  | e8
  | e9
  | e10
  | e11
  | e12
  | e13
  | e14
  | e15
  | e16
  | e17
  | e18
  | e19
  | e20
  deriving DecidableEq

/-- Finite enumeration is an *index adapter*, not a proof eliminating
a proposition into a Type. Exact order follows the K₅ graph. -/
def nativeK5TypedEdgeTagOfFin (e : Fin 21) : NativeK5TypedEdgeTag :=
  match e.val with
  | 0 => .e0
  | 1 => .e1
  | 2 => .e2
  | 3 => .e3
  | 4 => .e4
  | 5 => .e5
  | 6 => .e6
  | 7 => .e7
  | 8 => .e8
  | 9 => .e9
  | 10 => .e10
  | 11 => .e11
  | 12 => .e12
  | 13 => .e13
  | 14 => .e14
  | 15 => .e15
  | 16 => .e16
  | 17 => .e17
  | 18 => .e18
  | 19 => .e19
  | _ => .e20

/-- Exact genuinely oriented elementary edges (source, target). -/
def nativeK5TaggedEdgeEndpoints (e : NativeK5TypedEdgeTag) :
    Fin 14 × Fin 14 :=
  match e with
  | .e0 => (1, 0)
  | .e1 => (2, 0)
  | .e2 => (5, 0)
  | .e3 => (3, 1)
  | .e4 => (6, 1)
  | .e5 => (4, 2)
  | .e6 => (7, 2)
  | .e7 => (4, 3)
  | .e8 => (9, 3)
  | .e9 => (10, 4)
  | .e10 => (6, 5)
  | .e11 => (8, 5)
  | .e12 => (11, 6)
  | .e13 => (8, 7)
  | .e14 => (12, 7)
  | .e15 => (13, 8)
  | .e16 => (10, 9)
  | .e17 => (11, 9)
  | .e18 => (12, 10)
  | .e19 => (13, 11)
  | .e20 => (13, 12)

/-- Retain the Fin-indexed public endpoints while delegating
dependent construction to the true Type-valued edge constructors. -/
def nativeK5TypedEdgeEndpoints (e : Fin 21) : Fin 14 × Fin 14 :=
  nativeK5TaggedEdgeEndpoints (nativeK5TypedEdgeTagOfFin e)

/-- All 21 typed edges give the exact computed unoriented K₅ graph.
This checks that no artificial or omitted rotation entered the
finite enumeration, not merely that the two lists have length 21. -/
def nativeK5TypedUndirectedEdges : List (Fin 14 × Fin 14) :=
  (List.finRange 21).map (fun e =>
    let edge := nativeK5TypedEdgeEndpoints e
    if edge.1.val < edge.2.val then edge else (edge.2, edge.1))

theorem nativeK5TypedUndirectedEdges_exact :
    nativeK5TypedUndirectedEdges = nativeK5GraphEdges := by
  decide

/-- EACH elementary edge has an ACTUAL old F54 proof-relevant route,
including all independent F19/F28 depth casts and native contexts. -/
def nativeK5TaggedEdgeRoute
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
    {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
    (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
    (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)
    (e : NativeK5TypedEdgeTag) :
    KuuNativeF45Tree.DepthRotationRoute p
      (nativeK5TypedVertex t1 t2 t3 t4 t5
        (nativeK5TaggedEdgeEndpoints e).1).2.2
      (nativeK5TypedVertex t1 t2 t3 t4 t5
        (nativeK5TaggedEdgeEndpoints e).2).2.2 := by
  cases e
  · exact (.rightContext t1 (.rightContext t2 (.assoc t3 t4 t5)))
  · exact (.rightContext t1 (.assoc t2 t3 (.node t4 t5)))
  · exact (.assoc t1 t2 (.node t3 (.node t4 t5)))
  · exact (.rightContext t1 (.assoc t2 (.node t3 t4) t5))
  · exact (.assoc t1 t2 (.node (.node t3 t4) t5))
  · exact (.rightContext t1 (.assoc (.node t2 t3) t4 t5))
  · exact (.assoc t1 (.node t2 t3) (.node t4 t5))
  · exact (.rightContext t1 (.leftContext (.assoc t2 t3 t4) t5))
  · exact (.assoc t1 (.node t2 (.node t3 t4)) t5)
  · exact (.assoc t1 (.node (.node t2 t3) t4) t5)
  · exact (.rightContext (.node t1 t2) (.assoc t3 t4 t5))
  · exact (.assoc (.node t1 t2) t3 (.node t4 t5))
  · exact (.assoc (.node t1 t2) (.node t3 t4) t5)
  · exact (.leftContext (.assoc t1 t2 t3) (.node t4 t5))
  · exact (.assoc (.node t1 (.node t2 t3)) t4 t5)
  · exact (.assoc (.node (.node t1 t2) t3) t4 t5)
  · exact (.leftContext (.rightContext t1 (.assoc t2 t3 t4)) t5)
  · exact (.leftContext (.assoc t1 t2 (.node t3 t4)) t5)
  · exact (.leftContext (.assoc t1 (.node t2 t3) t4) t5)
  · exact (.leftContext (.assoc (.node t1 t2) t3 t4) t5)
  · exact (.leftContext (.leftContext (.assoc t1 t2 t3) t4) t5)

/-- The primary Fin-indexed interface remains unchanged for
future nine-face and higher-cell glue. No `fin_cases` in Type. -/
def nativeK5TypedEdgeRoute
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
    {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
    (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
    (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)
    (e : Fin 21) :
    KuuNativeF45Tree.DepthRotationRoute p
      (nativeK5TypedVertex t1 t2 t3 t4 t5
        (nativeK5TypedEdgeEndpoints e).1).2.2
      (nativeK5TypedVertex t1 t2 t3 t4 t5
        (nativeK5TypedEdgeEndpoints e).2).2.2 :=
  nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
    (nativeK5TypedEdgeTagOfFin e)

/-- One and ONLY one actual F54 primitive rotation per tagged edge. -/
theorem nativeK5TaggedEdgeRoute_rotationCount
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
    {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
    (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
    (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)
    (e : NativeK5TypedEdgeTag) :
    (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 e).rotationCount = 1 := by
  cases e <;> rfl

/-- The same primitive count on all original Fin-indexed edges,
obtained from the Type-valued tag proof without recursing on Prop. -/
theorem nativeK5TypedEdgeRoute_rotationCount
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
    {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
    (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
    (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)
    (e : Fin 21) :
    (nativeK5TypedEdgeRoute t1 t2 t3 t4 t5 e).rotationCount = 1 :=
  nativeK5TaggedEdgeRoute_rotationCount t1 t2 t3 t4 t5
    (nativeK5TypedEdgeTagOfFin e)

/-- The FIFTH actual north C60 pentagon side has physical index 4,
which was not represented in P94C1's four-side pentagon. -/
def northK5FifthSector : PolygonBoundarySector (.pentagon .north) :=
  ⟨(4 : Fin 6), by decide⟩

def northNativeF45FirstFifth :=
  KuuNativeBlocks.snoc northNativeF45FirstFourth
    (KuuNativePath.nil (Site.face (.pentagon .north)))
def northNativeF45SecondFifth :=
  KuuNativeBlocks.snoc northNativeF45SecondFourth
    (KuuNativePath.nil (Site.face (.pentagon .north)))

/-- Five truly distinct ordered native C60 leaves; the fifth step
keeps BOTH original independent proof-relevant axis histories. -/
def northNativeF45FifthStage :
    KuuNativeF45Tree (.pentagon .north) 1 1
      northNativeF45FirstFourth northNativeF45SecondFourth
      northNativeF45FirstFifth northNativeF45SecondFifth :=
  .leaf northK5FifthSector .firstAxisFirst
    (KuuNativeAxisTrace.insertNilOnce _)
    (KuuNativeAxisTrace.insertNilOnce _)

def northK5TypedVertex (i : Fin 14) :=
  nativeK5TypedVertex
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage
    northNativeF45FifthStage i

theorem northK5TypedVertex_physical_five_sectors (i : Fin 14) :
    (northK5TypedVertex i).2.2.sectors =
      [firstFourPolygonSector (.pentagon .north) 0,
       firstFourPolygonSector (.pentagon .north) 1,
       firstFourPolygonSector (.pentagon .north) 2,
       firstFourPolygonSector (.pentagon .north) 3,
       northK5FifthSector] := by
  fin_cases i <;> rfl

#print axioms NativeK5Shape
#print axioms nativeK5ShapeVertex_order
#print axioms nativeK5ShapeVertex_nodup
#print axioms nativeK5GraphEdge_count
#print axioms nativeK5Face_sizes
#print axioms nativeK5FaceEdges_are_rotations
#print axioms nativeK5Shell_oriented_edges
#print axioms nativeK5CandidateFaceShadow_balanced
#print axioms nativeK5HypotheticalOddSquarePhase_nonzero
#print axioms nativeK5TypedVertex
#print axioms nativeK5TypedVertex_sectors
#print axioms nativeK5TypedEdgeRoute
#print axioms nativeK5TypedEdgeRoute_rotationCount
#print axioms northK5TypedVertex_physical_five_sectors

end
end Kuu.F112.Physical
