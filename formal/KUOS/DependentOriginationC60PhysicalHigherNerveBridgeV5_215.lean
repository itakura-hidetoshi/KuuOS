import Mathlib.AlgebraicTopology.Quasicategory.Nerve
import Mathlib.AlgebraicTopology.SimplicialSet.Nerve
import KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
import KUOS.DependentOriginationGrayC60F55MixedDescentObstructionV5_204
import KUOS.DependentOriginationGrayC60F55ThreeContextPhysicalV5_212

namespace KUOS.DependentOriginationC60PhysicalHigherNerveBridgeV5_215

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60F55MixedDescentObstructionV5_204
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000

noncomputable section

/-!
# Real C60 four-flag 3-Hom to the native simplicial and (infinity,2) interfaces

The input is the ORIGINAL F42 physical polygonal face 2-cell, the INDEPENDENT
ORIGINAL F54/F55 bracket-tree route, and the *explicitly adjoined* F47
four-tagged mixed-boundary 3-Hom category. The F47 construction has four
different typed source boundary positions and a complete Int × Int and ZMod 2
Gray evaluation, including the new comparison charge Delta = (0,1;0).

Here we pass to a Mathlib simplicial nerve of that genuine source 3-Hom
category. The original mixed square produces two actual 2-simplices in this
nerve with an EQUAL diagonal 1-face. Every 90-edge × two-real-face source
choice has such a quasicategory. The already proven *actual face-change
functor* gives a simplicial map between the two different nerve sources,
preserving their typed 1-simplex composition and complete native Gray image.

The existing graded F49 Gray 3-category envelope on original C60
vertices/path-boundaries supplies a SECOND native nerve: actual F43 original
interchanger 3-cells define nontrivial simplicial edges retaining the exchange
phase. This connects the source F47 nerve to the native C60 0/1/2/3 grading.
All these are nerves of ordinary 3-Hom categories (1-categorical in a shifted
dimension), not a proof of a complete globally glued (infinity,3)-category.
Original F55 non-lift and nonzero north-curvature are not erased.
-/

universe uD vD uE vE

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalMixedFrame

variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable (B : C60F47SquareFrame α β r s)

/-- The genuine simplicial nerve of an original-boundary-aware local C60
3-Hom category; it keeps all four different F42/F54 boundary tags. -/
def c60LocalMixedThreeNerve : SSet :=
  CategoryTheory.nerve (C60F47BoundaryPoint B)

/-- Mathlib strict Segal nerve: all composable F47 3-cell strings
are presented by their unique categorical simplices. -/
def c60LocalMixedThreeStrictSegal :
    SSet.StrictSegal (c60LocalMixedThreeNerve B) :=
  CategoryTheory.Nerve.strictSegal (C60F47BoundaryPoint B)

/-- The genuine F47 source 3-Hom nerve is a quasicategory. -/
theorem c60LocalMixedThreeQuasicategory :
    SSet.Quasicategory (c60LocalMixedThreeNerve B) :=
  SSet.StrictSegal.quasicategory (c60LocalMixedThreeStrictSegal B)

/-- Actual inner horn filling; no higher source 4-cell is fabricated. -/
theorem c60LocalMixedThreeInnerHorn
    {k : Nat} {i : Fin (k + 1)}
    (hi : 0 < i) (hj : i < Fin.last k)
    (h : (Λ[k, i] : SSet) ⟶ c60LocalMixedThreeNerve B) :
    ∃ filler : Δ[k] ⟶ c60LocalMixedThreeNerve B,
      h = Λ[k, i].ι ≫ filler := by
  letI : SSet.Quasicategory (c60LocalMixedThreeNerve B) :=
    c60LocalMixedThreeQuasicategory B
  exact SSet.Quasicategory.hornFilling hi hj h

/-- First genuine composable pair: original F42/F43 face 3-cell
then the new F47 target-boundary comparison. -/
def c60LocalMixedFaceTriangle :
    ComposableArrows (C60F47BoundaryPoint B) 2 :=
  ComposableArrows.mk₂ (c60F47FaceArrow B) (c60F47CompareAfter B)

/-- Second genuine composable pair: new source-boundary comparison,
then the independent original F54/F55 rotation 3-cell. -/
def c60LocalMixedRotationTriangle :
    ComposableArrows (C60F47BoundaryPoint B) 2 :=
  ComposableArrows.mk₂
    (c60F47CompareBefore B) (c60F47OriginalF55Arrow B)

/-- The two distinct actual F42/F55 2-simplices have the SAME
diagonal face in the Mathlib nerve. This is the simplicial
realization of the proved original mixed 3-Hom square, not a
numerical equality in the Gray target alone. -/
theorem c60LocalMixedTriangles_sharedDiagonal :
    (ConcreteCategory.hom
      ((c60LocalMixedThreeNerve B).δ 1))
      (c60LocalMixedFaceTriangle B) =
    (ConcreteCategory.hom
      ((c60LocalMixedThreeNerve B).δ 1))
      (c60LocalMixedRotationTriangle B) := by
  change
    (ConcreteCategory.hom
      ((CategoryTheory.nerve (C60F47BoundaryPoint B)).δ 1))
      (ComposableArrows.mk₂ (c60F47FaceArrow B)
        (c60F47CompareAfter B)) =
    (ConcreteCategory.hom
      ((CategoryTheory.nerve (C60F47BoundaryPoint B)).δ 1))
      (ComposableArrows.mk₂ (c60F47CompareBefore B)
        (c60F47OriginalF55Arrow B))
  rw [CategoryTheory.nerve.δ₁_mk₂_eq,
    CategoryTheory.nerve.δ₁_mk₂_eq]
  exact congrArg ComposableArrows.mk₁ (c60F47MixedOriginalBoundarySquare B)

end OriginalMixedFrame

section EveryPhysicalEdge

variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- The two ORIGINAL distinct real incident polygon faces at each of
all ninety C60 physical edges each have their own mixed 3-Hom nerve. -/
def c60PhysicalMixedThreeNerve
    (edge : TruncatedIcosahedralEdge) (side : Bool) : SSet :=
  c60LocalMixedThreeNerve
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)

/-- Actual C60 geometry supplies a quasicategory for each of the
180 geometrically indexed edge/adjacent-original-face choices. -/
theorem c60PhysicalMixedThreeQuasicategory
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    SSet.Quasicategory
      (c60PhysicalMixedThreeNerve t₁ t₂ left right edge side) :=
  c60LocalMixedThreeQuasicategory
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)

/-- All genuine C60 edge/face comparisons are simplicial 2-simplices
with equal diagonal, not invented square faces of the C60 polyhedron. -/
theorem c60PhysicalMixedTriangles_sharedDiagonal
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (ConcreteCategory.hom
      ((c60PhysicalMixedThreeNerve t₁ t₂ left right edge side).δ 1))
      (c60LocalMixedFaceTriangle
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)) =
    (ConcreteCategory.hom
      ((c60PhysicalMixedThreeNerve t₁ t₂ left right edge side).δ 1))
      (c60LocalMixedRotationTriangle
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)) :=
  c60LocalMixedTriangles_sharedDiagonal
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)

/-- The old original-face-choice *functor* becomes a genuine
simplicial map between the two differently typed physical nerves.
The map acts on ALL simplicial dimensions by Mathlib functoriality. -/
def c60PhysicalFaceChoiceNerveMap
    (edge : TruncatedIcosahedralEdge) :
    c60PhysicalMixedThreeNerve t₁ t₂ left right edge false ⟶
      c60PhysicalMixedThreeNerve t₁ t₂ left right edge true :=
  CategoryTheory.nerveMap
    (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge)

/-- Every genuine original face/F55 3-morphism is transported
correctly as a 1-simplex in the local nerve. -/
theorem c60PhysicalFaceChoiceNerveMap_edges
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)}
    (f : X ⟶ Y) :
    CategoryTheory.nerve.homEquiv
      ((CategoryTheory.nerve.edgeMk f).map
        (c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge)) =
    (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map f := by
  exact CategoryTheory.nerve.homEquiv_edgeMk_map_nerveMap
    f (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge)

/-- Every source mixed diagonal maps to the correct diagonal of
the OTHER physically incident C60 face, at the nerve level. -/
theorem c60PhysicalFaceChoiceNerveMap_diagonal
    (edge : TruncatedIcosahedralEdge) :
    CategoryTheory.nerve.homEquiv
      ((CategoryTheory.nerve.edgeMk
        (c60F47FaceArrow
          (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) ≫
         c60F47CompareAfter
          (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false))).map
        (c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge)) =
    c60F47FaceArrow
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) ≫
    c60F47CompareAfter
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) := by
  rw [c60PhysicalFaceChoiceNerveMap_edges]
  exact c60F48ActualEdgeFaceChoiceFunctor_square
    t₁ t₂ left right edge

/-- Faithfulness of the old original-face comparison functor
transfers to the nerve on all genuine typed F47 3-cell 1-simplices. -/
theorem c60PhysicalFaceChoiceNerveMap_reflects_edges
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)}
    (f g : X ⟶ Y)
    (heq :
      (CategoryTheory.nerve.edgeMk f).map
        (c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge) =
      (CategoryTheory.nerve.edgeMk g).map
        (c60PhysicalFaceChoiceNerveMap t₁ t₂ left right edge)) :
    f = g := by
  have hLeft :=
    c60PhysicalFaceChoiceNerveMap_edges t₁ t₂ left right edge f
  have hRight :=
    c60PhysicalFaceChoiceNerveMap_edges t₁ t₂ left right edge g
  have hNerve := congrArg CategoryTheory.nerve.homEquiv heq
  have hh :
      (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map f =
      (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map g :=
    hLeft.symm.trans (hNerve.trans hRight)
  exact c60F48ActualEdgeFaceChoiceFunctor_faithful
    t₁ t₂ left right edge hh

end EveryPhysicalEdge

/-! ## Original F49 graded 3-Hom realization on true C60 paths -/

/-- The second, grade-completed original C60 F49 3-Hom category,
indexed by genuine pairs of original physical C60 paths. -/
def c60OriginalGradedThreeNerve
    {v w : IcosahedralDart}
    (p q : Quiver.Path v w) : SSet :=
  CategoryTheory.nerve (C60F49Two p q)

/-- The F49 graded envelope yields an actual native quasicategory in
every geometrically indexed parallel-path 3-Hom, with no collapse
of its independent full integer charges or exchange phase. -/
theorem c60OriginalGradedThreeQuasicategory
    {v w : IcosahedralDart}
    (p q : Quiver.Path v w) :
    SSet.Quasicategory (c60OriginalGradedThreeNerve p q) :=
  SSet.StrictSegal.quasicategory
    (CategoryTheory.Nerve.strictSegal (C60F49Two p q))

/-- The actual F42/F43 interchange of EVERY original pentagonal or hexagonal
C60 face is an edge in the F49 3-Hom nerve with NONTRIVIAL exchange phase,
not merely an equality of an abstract path graph. -/
theorem c60PhysicalFaceGradedNerveEdge_phase
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (CategoryTheory.nerve.homEquiv
      (CategoryTheory.nerve.edgeMk
        (c60F49OriginalFaceThree
          (c60F48AdjacentFaceInterchanger edge side)))).phase =
        (1 : ZMod 2) := by
  rw [CategoryTheory.nerve.homEquiv_edgeMk]
  change (c60F48AdjacentFaceInterchanger edge side).toNative.phase = 1
  rw [c60F48AdjacentFaceInterchanger_native]
  rfl

/-- The full original F43 physical interchange 3-cell seen as a simplicial
edge has zero pair charge, but its separate braiding phase is ONE. -/
theorem c60PhysicalFaceGradedNerveEdge_charge_phase
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    (CategoryTheory.nerve.homEquiv
      (CategoryTheory.nerve.edgeMk
        (c60F49OriginalFaceThree
          (c60F48AdjacentFaceInterchanger edge side)))).charge =
          ((0 : Int), (0 : Int)) ∧
    (CategoryTheory.nerve.homEquiv
      (CategoryTheory.nerve.edgeMk
        (c60F49OriginalFaceThree
          (c60F48AdjacentFaceInterchanger edge side)))).phase =
          (1 : ZMod 2) := by
  constructor
  · rw [CategoryTheory.nerve.homEquiv_edgeMk]
    change (c60F48AdjacentFaceInterchanger edge side).toNative.charge =
      ((0 : Int), (0 : Int))
    rw [c60F48AdjacentFaceInterchanger_native]
    rfl
  · exact c60PhysicalFaceGradedNerveEdge_phase edge side


/-! ## Direct native F47 -> F49 geometric higher-nerve comparison -/

section PhysicalGradedComparison

variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- A genuine simplicial map from the original boundary-tagged F47 mixed
3-Hom category at an ACTUAL physical C60 edge/face to the F49 graded
3-Hom category indexed by that same original polygonal face's actual
boundary loop and empty reference path. The map is induced by the
preexisting complete native, faithful Gray functor; not by a phase-only
projection or invented F42/F55 source identification. -/
def c60PhysicalMixedToOriginalGradedNerve
    (edge : TruncatedIcosahedralEdge) (side : Bool) :
    c60PhysicalMixedThreeNerve t₁ t₂ left right edge side ⟶
      c60OriginalGradedThreeNerve
        (c60F41PhysicalFaceBoundaryLoop
          (c60F48AdjacentRealFace edge side)).2
        Quiver.Path.nil :=
  CategoryTheory.nerveMap
    (c60F47MixedGrayFunctor
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side))

/-- All genuinely typed F47 arrows, including the original face/F55
3-cells and explicitly NEW calibration, map to their COMPLETE
(Int × Int charge, ZMod 2 phase) F49 Gray 3-cell simplicial edge. -/
theorem c60PhysicalMixedToOriginalGradedNerve_edges
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)}
    (f : X ⟶ Y) :
    CategoryTheory.nerve.homEquiv
      ((CategoryTheory.nerve.edgeMk f).map
        (c60PhysicalMixedToOriginalGradedNerve
          t₁ t₂ left right edge side)) =
      c60F47MixedEval f := by
  exact CategoryTheory.nerve.homEquiv_edgeMk_map_nerveMap
    f (c60F47MixedGrayFunctor
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side))

/-- The actual physical F47 -> F49 nerve map is faithful on
every original four-boundary typed 3-cell edge. -/
theorem c60PhysicalMixedToOriginalGradedNerve_reflects_edges
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side)}
    (f g : X ⟶ Y)
    (h :
      (CategoryTheory.nerve.edgeMk f).map
        (c60PhysicalMixedToOriginalGradedNerve
          t₁ t₂ left right edge side) =
      (CategoryTheory.nerve.edgeMk g).map
        (c60PhysicalMixedToOriginalGradedNerve
          t₁ t₂ left right edge side)) : f = g := by
  have hf :=
    c60PhysicalMixedToOriginalGradedNerve_edges
      t₁ t₂ left right edge side f
  have hg :=
    c60PhysicalMixedToOriginalGradedNerve_edges
      t₁ t₂ left right edge side g
  have hh := congrArg CategoryTheory.nerve.homEquiv h
  have hEval : c60F47MixedEval f = c60F47MixedEval g :=
    hf.symm.trans (hh.trans hg)
  exact c60F47MixedGrayFunctor_faithful
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge side) hEval

end PhysicalGradedComparison

#print axioms c60LocalMixedThreeQuasicategory
#print axioms c60LocalMixedThreeInnerHorn
#print axioms c60LocalMixedTriangles_sharedDiagonal
#print axioms c60PhysicalMixedThreeQuasicategory
#print axioms c60PhysicalMixedTriangles_sharedDiagonal
#print axioms c60PhysicalFaceChoiceNerveMap_edges
#print axioms c60PhysicalFaceChoiceNerveMap_diagonal
#print axioms c60PhysicalFaceChoiceNerveMap_reflects_edges
#print axioms c60OriginalGradedThreeQuasicategory
#print axioms c60PhysicalFaceGradedNerveEdge_phase
#print axioms c60PhysicalFaceGradedNerveEdge_charge_phase
#print axioms c60PhysicalMixedToOriginalGradedNerve_edges
#print axioms c60PhysicalMixedToOriginalGradedNerve_reflects_edges

end
end KUOS.DependentOriginationC60PhysicalHigherNerveBridgeV5_215
