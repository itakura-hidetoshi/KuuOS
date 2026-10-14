import KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264

namespace KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuPhysicalOverlapObstructionV5_259
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263
open KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.265 / F108 fourth stage — BOTH ACTUAL adjacent polygons in F42/F51 sources

The v5.264 native F51 whole-star functor used the *same chosen original
polygon generator twice* for its two original F42 horizontal source
pasting orders. Here the two different original C60 faces adjacent to
EACH of the ninety real physical edges are BOTH present as independent,
genuinely path-indexed original F42 physical-face generators.

The two original face loops generally have DIFFERENT base darts.
We connect their genuine original bases by an actual Quiver.Path, use
F42 left-whiskering to bring the second face to the first face's source,
and then paste two DIFFERENT original physical face 2-cells in the two
horizontal orders. The EXACT original F43 interchanger is transported
through typed prior and suffix paths into the open physical edge
endpoint-to-endpoint F51 3-Hom. Charge remains (0,0), but native
braiding phase equals 1. No raw F42 witness is silently identified.

F109's proven real C60 sixty-dart graph connectivity supplies ALL
three necessary original context paths, including the between-face
base bridge, for arbitrary finite physical edge families and all
ninety edge stars. The two distinct original face sites are retained
as separate physical F69 objects. An actual nonidentity native F51
functor on every star Hom factors through the Boolean physical
vertex-vs-upper-stratum order and the new both-face interchanger.

BOUNDARY: Both different polygon GENERATORS are preserved within
the original F42 double-face words, but the two distinct upper
polygon SITES still share one common upper F42 composite object.
This does not prove separately face-indexed local F42 object
assignment, original F55 nine-constructor source identification,
F68 north-pentagon curvature removal, or global descent.
-/

/-! ## I. Three ORIGINAL typed C60 paths joining both REAL face bases -/

/-- Distinct real original polygon faces are used on every edge.
Prior is from the first actual edge dart to face-false base,
bridge joins the two DIFFERENT face base darts, and suffix
continues from face-true base to the other physical edge dart. -/
structure C60F108BothFaceContexts (n : Nat) where
  edge : Fin n → TruncatedIcosahedralEdge
  prior : (i : Fin n) →
    Quiver.Path (truncatedIcosahedralEdgeEndpoints (edge i)).1
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edge i) false)).1
  bridge : (i : Fin n) →
    Quiver.Path
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edge i) false)).1
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edge i) true)).1
  suffix : (i : Fin n) →
    Quiver.Path
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edge i) true)).1
      (truncatedIcosahedralEdgeEndpoints (edge i)).2

/-- The ORIGINAL F42 generator at the first real adjacent face. -/
def c60F108FirstPhysicalFaceCell {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F42PresentedFaceCell
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (C.edge i) false)).2
      Quiver.Path.nil :=
  c60F48AdjacentFaceTwoCell (C.edge i) false

/-- The ORIGINAL *different* face at the other side of the same edge.
A genuine typed ORIGINAL C60 path, not an equality between bases,
moves its source and target path boundaries to the first base. -/
def c60F108SecondPhysicalFaceBridged {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F42PresentedFaceCell
      ((C.bridge i).comp
        (c60F41PhysicalFaceBoundaryLoop
          (c60F48AdjacentRealFace (C.edge i) true)).2)
      ((C.bridge i).comp Quiver.Path.nil) :=
  .whiskerLeft (C.bridge i)
    (c60F48AdjacentFaceTwoCell (C.edge i) true)

/-- The actual two distinct geometric faces are never silently
equalized by the path bridge or the F95 observer. -/
theorem c60F108BothPolygonFaces_distinct {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    c60F48AdjacentRealFace (C.edge i) false ≠
      c60F48AdjacentRealFace (C.edge i) true :=
  c60F48BothRealFaces_distinct (C.edge i)

/-- BOTH independent original real polygon generators have source
face degree ONE, before the two are horizontally composed. -/
theorem c60F108BothPrimitiveFaceDegrees_one {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    c60F43FaceDegree (c60F108FirstPhysicalFaceCell C i) = (1 : ZMod 2) ∧
      c60F43FaceDegree (c60F108SecondPhysicalFaceBridged C i) =
        (1 : ZMod 2) := by
  exact ⟨rfl, rfl⟩

/-! ## II. Different original face loops in one CORRECT open path pair -/

/-- Original 5/6-gon false LOOP then TRUE LOOP, connected by the
actual original C60 base-to-base bridge, with true physical
endpoint-to-endpoint prior/suffix paths. No 4-gon face is added. -/
def c60F108BothFacePatchFamily {n : Nat}
    (C : C60F108BothFaceContexts n) :
    C60F105PhysicalEdgePatchFamily n where
  edge := C.edge
  p i :=
    ((C.prior i).comp
      ((c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (C.edge i) false)).2.comp
        ((C.bridge i).comp
          (c60F41PhysicalFaceBoundaryLoop
            (c60F48AdjacentRealFace (C.edge i) true)).2))).comp
              (C.suffix i)
  q i :=
    ((C.prior i).comp
      ((Quiver.Path.nil).comp
        ((C.bridge i).comp Quiver.Path.nil))).comp (C.suffix i)

/-- First of the two SOURCE F42 horizontal orders. Both genuinely
different physical face generators are present in this term. -/
def c60F108BothFaceLeft {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F42PresentedFaceCell
      ((c60F108BothFacePatchFamily C).p i)
      ((c60F108BothFacePatchFamily C).q i) :=
  .whiskerRight
    (.whiskerLeft (C.prior i)
      ((c60F108FirstPhysicalFaceCell C i).horizontalLeftFirst
        (c60F108SecondPhysicalFaceBridged C i)))
    (C.suffix i)

/-- Second, independent original F42 horizontal order, not raw
equal to the left order; the genuine F43 interchange compares them. -/
def c60F108BothFaceRight {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F42PresentedFaceCell
      ((c60F108BothFacePatchFamily C).p i)
      ((c60F108BothFacePatchFamily C).q i) :=
  .whiskerRight
    (.whiskerLeft (C.prior i)
      ((c60F108FirstPhysicalFaceCell C i).horizontalRightFirst
        (c60F108SecondPhysicalFaceBridged C i)))
    (C.suffix i)

/-- A truly source-typed ORIGINAL F43 generator, included in the
F51 source grammar and whiskered on BOTH true open path contexts.
Unlike F108 part 3 it interchanges TWO DIFFERENT actual polygons. -/
def c60F108BothFaceOriginalExchange {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F51PresentedThreeCell
      (c60F108BothFaceLeft C i)
      (c60F108BothFaceRight C i) :=
  .whiskerRight
    (.whiskerLeft (C.prior i)
      (.original
        (.interchange
          (c60F108FirstPhysicalFaceCell C i)
          (c60F108SecondPhysicalFaceBridged C i))))
    (C.suffix i)

/-- Both distinct original pentagon/hexagon face 2-cells have odd
parity, so their ACTUAL F43 interchanger evaluates exactly to the
old north odd/odd exchange; no synthetic Gray phase is inserted. -/
theorem c60F108BothFaceOriginalExchange_native {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    (c60F108BothFaceOriginalExchange C i).toNative =
      c60F43NorthPentagonInterchange.toNative := by
  apply GradedThreeCell.ext
  · rfl
  · rfl

/-- The original TWO INTEGER charges and the independent NONZERO
phase of the genuine different-face F51 interchange are separate. -/
theorem c60F108BothFaceOriginalExchange_components {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    (c60F108BothFaceOriginalExchange C i).toNative.charge =
        ((0 : Int), (0 : Int)) ∧
      (c60F108BothFaceOriginalExchange C i).toNative.phase =
        (1 : ZMod 2) := by
  rw [c60F108BothFaceOriginalExchange_native]
  exact c60F43NorthPentagonInterchange_components

theorem c60F108BothFaceOriginalExchange_nonidentity {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    (c60F108BothFaceOriginalExchange C i).toNative ≠
      (0 : GradedThreeCell 0 0) := by
  rw [c60F108BothFaceOriginalExchange_native]
  exact c60F43NorthPentagonInterchange_ne_identity

/-- The genuine full ORIGINAL F51 Hom between the two separate,
proof-relevant F42 two-face horizontal pasting orders. -/
def c60F108BothFaceExchangeHom {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n) :
    (⟨c60F108BothFaceLeft C i⟩ :
      C60F51OriginalTwo
        ((c60F108BothFacePatchFamily C).p i)
        ((c60F108BothFacePatchFamily C).q i)) ⟶
    (⟨c60F108BothFaceRight C i⟩ :
      C60F51OriginalTwo
        ((c60F108BothFacePatchFamily C).p i)
        ((c60F108BothFacePatchFamily C).q i)) :=
  c60F51Of (c60F108BothFaceOriginalExchange C i)

/-! ## III. No PATH input needed: actual 60-dart connectivity -/

/-- Original physical edge paths from the first edge endpoint to
the first REAL face base, BETWEEN the two distinct polygon bases,
and from second polygon base to the other endpoint. -/
noncomputable def c60F108BothFaceContextsFromGeometry
    {n : Nat} (edges : Fin n → TruncatedIcosahedralEdge) :
    C60F108BothFaceContexts n where
  edge := edges
  prior i :=
    c60F109EveryDartToDart
      (truncatedIcosahedralEdgeEndpoints (edges i)).1
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edges i) false)).1
  bridge i :=
    c60F109EveryDartToDart
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edges i) false)).1
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edges i) true)).1
  suffix i :=
    c60F109EveryDartToDart
      (c60F41PhysicalFaceBoundaryLoop
        (c60F48AdjacentRealFace (edges i) true)).1
      (truncatedIcosahedralEdgeEndpoints (edges i)).2

/-- All 90 original actual physical edges are represented, with
BOTH genuinely distinct adjacent five-/six-gon face 2-cells. -/
noncomputable def c60F108AllNinetyBothFaces :
    C60F108BothFaceContexts
      (Fintype.card TruncatedIcosahedralEdge) :=
  c60F108BothFaceContextsFromGeometry
    (fun i => (Fintype.equivFin TruncatedIcosahedralEdge).symm i)

theorem c60F108AllNinetyBothFaces_distinct
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    c60F48AdjacentRealFace (c60F108AllNinetyBothFaces.edge i) false ≠
      c60F48AdjacentRealFace (c60F108AllNinetyBothFaces.edge i) true :=
  c60F108BothPolygonFaces_distinct c60F108AllNinetyBothFaces i

theorem c60F108AllNinetyBothFaceExchange_phase_one
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    (c60F108BothFaceOriginalExchange c60F108AllNinetyBothFaces i).toNative.phase =
      (1 : ZMod 2) :=
  (c60F108BothFaceOriginalExchange_components
    c60F108AllNinetyBothFaces i).2

/-! ## IV. All ORIGINAL physical-incidence star Homs -/

/-- The exact genuine F69 vertex/edge/face order. The same rank
theorem as F108 part 3 now acts on the differently typed
two-ADJACENT-face ORIGINAL F42 path-pair family. -/
def c60F108BothFaceStarToWalking
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i} : Finset (Fin n)) ⥤ Bool where
  obj X := c60F108OriginalIncidenceStage X.1
  map := fun {_ _} f => by
    apply CategoryTheory.homOfLE
    exact c60F108OriginalIncidenceStage_monotone (CategoryTheory.leOfHom f)
  map_id := by
    intro X
    apply Subsingleton.elim
  map_comp := by
    intro X Y Z f g
    apply Subsingleton.elim

def c60F108BothFaceWalkingObject
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (b : Bool) :
    C60F51OriginalTwo
      ((c60F108BothFacePatchFamily C).p i)
      ((c60F108BothFacePatchFamily C).q i) :=
  if b then ⟨c60F108BothFaceRight C i⟩
  else ⟨c60F108BothFaceLeft C i⟩

/-- Nonidentity Bool arrow is the exact original F43 exchange of
TWO DIFFERENT actual pentagon/hexagon generators, unlike F108-3. -/
def c60F108BothFaceWalkingMap
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    {b c : Bool} (f : b ⟶ c) :
    c60F108BothFaceWalkingObject C i b ⟶
      c60F108BothFaceWalkingObject C i c := by
  cases b <;> cases c
  · exact 𝟙 _
  · exact c60F108BothFaceExchangeHom C i
  · have hf : (true : Bool) ≤ false := CategoryTheory.leOfHom f
    exact False.elim ((by decide : ¬ ((true : Bool) ≤ false)) hf)
  · exact 𝟙 _

def c60F108BothFaceWalkingNative
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    Bool ⥤
      C60F51OriginalTwo
        ((c60F108BothFacePatchFamily C).p i)
        ((c60F108BothFacePatchFamily C).q i) where
  obj := c60F108BothFaceWalkingObject C i
  map := fun {_ _} f => c60F108BothFaceWalkingMap C i f
  map_id := by
    intro b
    cases b <;> rfl
  map_comp := by
    intro b c d f g
    cases b <;> cases c <;> cases d
    all_goals
      first
      | exact False.elim
          ((by decide : ¬ ((true : Bool) ≤ false))
            (CategoryTheory.leOfHom f))
      | exact False.elim
          ((by decide : ¬ ((true : Bool) ≤ false))
            (CategoryTheory.leOfHom g))
      | simp [c60F108BothFaceWalkingMap, c60F108BothFaceWalkingObject]

/-- A real Mathlib native F51 functor on the WHOLE genuine physical
incidence star using TWO DISTINCT original face generators,
not merely two copies of one chosen original face. -/
def c60F108BothFaceNativeStar
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i} : Finset (Fin n)) ⥤
      C60F51OriginalTwo
        ((c60F108BothFacePatchFamily C).p i)
        ((c60F108BothFacePatchFamily C).q i) :=
  c60F108BothFaceStarToWalking C i ⋙
    c60F108BothFaceWalkingNative C i

def c60F108BothFaceKuuStar
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i} : Finset (Fin n)) ⥤
      C60F95LocalKuuQuotient
        ((c60F108BothFacePatchFamily C).p i)
        ((c60F108BothFacePatchFamily C).q i) :=
  c60F108BothFaceNativeStar C i ⋙
    c60F95LocalProjection
      ((c60F108BothFacePatchFamily C).p i)
      ((c60F108BothFacePatchFamily C).q i)

/-- The genuine source vertex at either of the two actual
distinct endpoint darts, not an artificially flattened 0-cell. -/
def c60F108BothFaceStarVertex
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (endpoint : Bool) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i} : Finset (Fin n)) :=
  ⟨.vertex ((c60F46PhysicalFourFlagSquare (C.edge i)).vertex endpoint), by
    intro j hj
    have hji : j = i := Finset.mem_singleton.mp hj
    subst j
    exact (c60F106AllPhysicalFlags_in_star (C.edge i) endpoint false).1⟩

def c60F108BothFaceStarEdge
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i} : Finset (Fin n)) :=
  ⟨.edge (C.edge i), by
    intro j hj
    have hji : j = i := Finset.mem_singleton.mp hj
    subst j
    exact Or.inl (le_refl _)⟩

/-- BOTH true polygon faces, kept as SEPARATE ORIGINAL physical
incidence sites. They are not regarded as a fictitious square. -/
def c60F108BothFaceStarPolygon
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (side : Bool) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i} : Finset (Fin n)) :=
  ⟨.face (c60F48AdjacentRealFace (C.edge i) side), by
    intro j hj
    have hji : j = i := Finset.mem_singleton.mp hj
    subst j
    exact Or.inr (c60F69PhysicalEdgeFace
      (C.edge i) (c60F48AdjacentRealFace (C.edge i) side)
      (c60F48AdjacentRealFace_incident (C.edge i) side))⟩

/-- Original F69 real incidence Homs along both polygon sides. -/
def c60F108BothFaceStarVertexEdge
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (endpoint : Bool) :
    c60F108BothFaceStarVertex C i endpoint ⟶
      c60F108BothFaceStarEdge C i :=
  CategoryTheory.homOfLE
    (c60F69PhysicalVertexEdge
      ((c60F46PhysicalFourFlagSquare (C.edge i)).vertex endpoint)
      (C.edge i) (c60F69ActualFlagEndpoint (C.edge i) endpoint))

def c60F108BothFaceStarEdgePolygon
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (side : Bool) :
    c60F108BothFaceStarEdge C i ⟶
      c60F108BothFaceStarPolygon C i side :=
  CategoryTheory.homOfLE
    (c60F69PhysicalEdgeFace (C.edge i)
      (c60F48AdjacentRealFace (C.edge i) side)
      (c60F48AdjacentRealFace_incident (C.edge i) side))

/-- BOTH 360 actual physical endpoint/face flags have precisely
the SAME original F43 exchange of two DISTINCT polygon GENERATORS
on the vertex→edge morphism, with nonzero original native phase. -/
theorem c60F108BothFaceStarVertexEdge_map
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (endpoint : Bool) :
    (c60F108BothFaceNativeStar C i).map
      (c60F108BothFaceStarVertexEdge C i endpoint) =
        c60F108BothFaceExchangeHom C i := rfl

theorem c60F108BothFaceStarVertexEdge_components
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (endpoint : Bool) :
    (c60F51Eval
      ((c60F108BothFaceNativeStar C i).map
        (c60F108BothFaceStarVertexEdge C i endpoint))).charge =
        ((0 : Int), (0 : Int)) ∧
      (c60F51Eval
        ((c60F108BothFaceNativeStar C i).map
          (c60F108BothFaceStarVertexEdge C i endpoint))).phase =
        (1 : ZMod 2) := by
  rw [c60F108BothFaceStarVertexEdge_map]
  exact c60F108BothFaceOriginalExchange_components C i

/-- The ACTUAL F69 real vertex→edge→face physical 2-simplex
composes compatibly with the original two-face F51 functor
for EACH of the TWO distinct real polygon faces. -/
theorem c60F108BothFaceStarTriangle_coherent
    {n : Nat} (C : C60F108BothFaceContexts n) (i : Fin n)
    (endpoint side : Bool) :
    (c60F108BothFaceNativeStar C i).map
      (c60F108BothFaceStarVertexEdge C i endpoint ≫
        c60F108BothFaceStarEdgePolygon C i side) =
      (c60F108BothFaceNativeStar C i).map
        (CategoryTheory.homOfLE
          (c60F69PhysicalVertexFace
            ((c60F46PhysicalFourFlagSquare (C.edge i)).vertex endpoint)
            (c60F48AdjacentRealFace (C.edge i) side)
            (c60F69EveryPhysicalFlagCorner_incident
              (C.edge i) endpoint side))) := by
  exact congrArg
    (fun f => (c60F108BothFaceNativeStar C i).map f)
    (Subsingleton.elim _ _)

/-! ## V. Ninety genuine edge stars, TWO real polygon generators -/

/-- In each actual original physical edge's incidence-star category
this native F51 functor contains BOTH different 5-/6-gon generators. -/
noncomputable def c60F108AllNinetyBothFaceNativeStar
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily c60F108AllNinetyBothFaces)
      ({i} : Finset (Fin (Fintype.card TruncatedIcosahedralEdge))) ⥤
      C60F51OriginalTwo
        ((c60F108BothFacePatchFamily c60F108AllNinetyBothFaces).p i)
        ((c60F108BothFacePatchFamily c60F108AllNinetyBothFaces).q i) :=
  c60F108BothFaceNativeStar c60F108AllNinetyBothFaces i

theorem c60F108AllNinetyBothFaceStar_phase_one
    (i : Fin (Fintype.card TruncatedIcosahedralEdge))
    (endpoint : Bool) :
    (c60F51Eval
      ((c60F108AllNinetyBothFaceNativeStar i).map
        (c60F108BothFaceStarVertexEdge
          c60F108AllNinetyBothFaces i endpoint))).phase =
      (1 : ZMod 2) :=
  (c60F108BothFaceStarVertexEdge_components
    c60F108AllNinetyBothFaces i endpoint).2

#print axioms c60F108BothPolygonFaces_distinct
#print axioms c60F108BothPrimitiveFaceDegrees_one
#print axioms c60F108BothFaceOriginalExchange_native
#print axioms c60F108BothFaceOriginalExchange_components
#print axioms c60F108BothFaceOriginalExchange_nonidentity
#print axioms c60F108AllNinetyBothFaces_distinct
#print axioms c60F108AllNinetyBothFaceExchange_phase_one
#print axioms c60F108BothFaceWalkingNative
#print axioms c60F108BothFaceNativeStar
#print axioms c60F108BothFaceKuuStar
#print axioms c60F108BothFaceStarVertexEdge_map
#print axioms c60F108BothFaceStarVertexEdge_components
#print axioms c60F108BothFaceStarTriangle_coherent
#print axioms c60F108AllNinetyBothFaceNativeStar
#print axioms c60F108AllNinetyBothFaceStar_phase_one

end
end KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
