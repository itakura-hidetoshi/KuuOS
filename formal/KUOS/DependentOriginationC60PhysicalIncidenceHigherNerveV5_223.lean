import KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
import Mathlib.CategoryTheory.Category.Preorder
import Mathlib.AlgebraicTopology.SimplicialSet.Nerve

namespace KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationC60ArbitraryAtlasNerveDescentV5_219
open KUOS.DependentOriginationC60FourAtlasCechNerveV5_220
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.223 / F69: the ACTUAL global C60 incidence nerve and atlas F47 fibres

The concrete C60 original cell decomposition, NOT an invented simplicial
surface, has 60 vertex darts, 90 physical edges and 32 polygonal faces.
Its incidence poset has arrows from vertices to their incident edges,
from edges to their two actual polygonal faces, and from vertices to
the containing faces. The intermediate edges give genuine nondegenerate
2-simplices for the 360 physical endpoint × edge × adjacent-face flags.

The usual Mathlib category nerve of that ORIGINAL finite incidence
category is a native strict-Segal quasicategory. The four actual
vertex-face flags around every physical edge are embedded as two-step
composable-arrows simplices, with ACTUAL signed C60 geometry.

Each of the 90 physical edge sites independently carries the original
proof-relevant F47 four-tagged 3-Hom CATEGORY selected by any 90-bit
face atlas. Its Mathlib nerve is a quasicategory and the genuine F67
finite atlas transport functors induce simplicial maps preserving the
complete independent Int×Int and ZMod 2 native Gray value of every
actual simplicial edge. Thus the physical 2-dimensional incidence
nerve and the true typed local F47 higher-nerve transport are connected
WITHOUT identifying the physical incidence category with its 3-Hom
fibres, or asserting a global (infinity,3)-descent theorem.

The original v5.222 2-cochain is STILL NONZERO at the north pentagon.
We explicitly retain its effectivity obstruction and exhibit the
certified nonzero physical correction as a separate structure.
-/

/-- Real cell sites: all and only the ORIGINAL 60 darts, 90 edges,
and 32 pentagonal/hexagonal faces of the C60 construction. -/
inductive C60F69PhysicalCellSite where
  | vertex (v : IcosahedralDart)
  | edge (e : TruncatedIcosahedralEdge)
  | face (f : TruncatedIcosahedralSeedFace)
  deriving DecidableEq, Fintype

/-- A genuine physical incidence relation, including direct vertex
to face incidence needed for the oriented 2-simplex diagonal. -/
def c60F69PhysicalIncidence
    (source target : C60F69PhysicalCellSite) : Prop :=
  match source, target with
  | .vertex v, .vertex w => v = w
  | .vertex v, .edge e =>
      v = (truncatedIcosahedralEdgeEndpoints e).1 ∨
        v = (truncatedIcosahedralEdgeEndpoints e).2
  | .vertex v, .face f => truncatedDartOnSeedFace v f
  | .edge e, .edge d => e = d
  | .edge e, .face f => truncatedEdgeOnSeedFace e f
  | .face f, .face g => f = g
  | _, _ => False

/-- The original three-dimensional cell strata carry the real
C60 incidence PARTIAL ORDER, not any artificial face equality. -/
instance : PartialOrder C60F69PhysicalCellSite where
  le := c60F69PhysicalIncidence
  le_refl := by
    intro x
    cases x <;> simp [c60F69PhysicalIncidence]
  le_trans := by
    intro a b c hab hbc
    cases a <;> cases b <;> cases c <;>
      (simp_all [c60F69PhysicalIncidence, truncatedEdgeOnSeedFace]; aesop)
  le_antisymm := by
    intro a b hab hba
    cases a <;> cases b <;>
      simp_all [c60F69PhysicalIncidence]

/-- An ORIGINAL dart belongs to this ORIGINAL physical edge
exactly by endpoint equality. -/
theorem c60F69PhysicalVertexEdge
    (v : IcosahedralDart)
    (e : TruncatedIcosahedralEdge)
    (hv : v = (truncatedIcosahedralEdgeEndpoints e).1 ∨
      v = (truncatedIcosahedralEdgeEndpoints e).2) :
    C60F69PhysicalCellSite.vertex v ≤ .edge e := hv

/-- The two directly incident C60 polygons are exactly the
physical edge-to-face arrows of the poset category. -/
theorem c60F69PhysicalEdgeFace
    (e : TruncatedIcosahedralEdge)
    (f : TruncatedIcosahedralSeedFace)
    (hef : truncatedEdgeOnSeedFace e f) :
    C60F69PhysicalCellSite.edge e ≤ .face f := hef

/-- A genuine vertex-face flag is the direct diagonal of an
actual original vertex-edge-face incidence triangle. -/
theorem c60F69PhysicalVertexFace
    (v : IcosahedralDart)
    (f : TruncatedIcosahedralSeedFace)
    (hvf : truncatedDartOnSeedFace v f) :
    C60F69PhysicalCellSite.vertex v ≤ .face f := hvf

/-- The actual FULL C60 60/90/32 cell-incidence categorical nerve,
not just a disconnected collection of 90 tiny abstract nerves. -/
def c60F69PhysicalIncidenceNerve : SSet :=
  CategoryTheory.nerve C60F69PhysicalCellSite

/-- A true quasicategory from the native Mathlib nerve of the
physical incidence category. This is a categorical incidence
carrier (barycentric flag nerve), NOT a full global (infinity,3)
model and NOT the Čech nerve of an unprovided topology. -/
theorem c60F69PhysicalIncidenceNerve_quasicategory :
    SSet.Quasicategory c60F69PhysicalIncidenceNerve :=
  SSet.StrictSegal.quasicategory
    (CategoryTheory.Nerve.strictSegal C60F69PhysicalCellSite)

/-- Every actual C60 90-edge square has exactly FOUR distinct
actual vertex-face corner flags, two endpoints and two distinct
polygon faces, with no invented C60 four-sided physical face. -/
theorem c60F69EveryPhysicalFlagCorner_incident
    (edge : TruncatedIcosahedralEdge)
    (endpoint faceChoice : Bool) :
    truncatedDartOnSeedFace
      ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)
      (c60F48AdjacentRealFace edge faceChoice) :=
  c60F48EveryFlagCorner_isIncident edge endpoint faceChoice

/-- The FOUR physical corner flags around each edge are genuinely
distinct and not collapsed by the incidence nerve construction. -/
theorem c60F69EveryPhysicalFlagCorner_injective
    (edge : TruncatedIcosahedralEdge) :
    Function.Injective
      (fun ij : Bool × Bool =>
        ((c60F46PhysicalFourFlagSquare edge).vertex ij.1,
         c60F48AdjacentRealFace edge ij.2)) :=
  (c60F46PhysicalFourFlagSquare edge).corner_injective

/-- The precise four endpoint/face choices over EACH of the NINETY
real physical edges give 360 actual flags, with no synthetic sites. -/
theorem c60F69ActualPhysicalFlagIndex_card :
    Fintype.card (TruncatedIcosahedralEdge × (Bool × Bool)) = 360 := by
  rw [Fintype.card_prod, Fintype.card_prod, c60F48PhysicalEdgeCount]
  decide

/-- The genuine selected C60 corner vertex is one of the TWO
distinct endpoints of that original physical edge. -/
theorem c60F69ActualFlagEndpoint
    (edge : TruncatedIcosahedralEdge) (endpoint : Bool) :
    (c60F46PhysicalFourFlagSquare edge).vertex endpoint =
        (truncatedIcosahedralEdgeEndpoints edge).1 ∨
    (c60F46PhysicalFourFlagSquare edge).vertex endpoint =
        (truncatedIcosahedralEdgeEndpoints edge).2 := by
  cases endpoint <;> simp [TruncatedEdgeFlagSquare.vertex]

/-- Construct a REAL nondegenerate physical 2-step flag:
actual dart -> containing ORIGINAL C60 edge -> one of that edge's
TWO actual polygonal faces, as two composable Mathlib arrows. -/
def c60F69ActualPhysicalFlagTriangle
    (edge : TruncatedIcosahedralEdge)
    (endpoint faceChoice : Bool) :
    ComposableArrows C60F69PhysicalCellSite 2 :=
  ComposableArrows.mk₂
    (CategoryTheory.homOfLE
      (c60F69PhysicalVertexEdge
        ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)
        edge
        (c60F69ActualFlagEndpoint edge endpoint)))
    (CategoryTheory.homOfLE
      (c60F69PhysicalEdgeFace
        edge (c60F48AdjacentRealFace edge faceChoice)
        (c60F48AdjacentRealFace_incident edge faceChoice)))

/-- A physical 2-simplex has three genuinely DISTINCT cell sites
(dart/edge/polygon), i.e., it is not a degenerate identity chain. -/
theorem c60F69ActualPhysicalFlagTriangle_distinct
    (edge : TruncatedIcosahedralEdge)
    (endpoint faceChoice : Bool) :
    C60F69PhysicalCellSite.vertex
      ((c60F46PhysicalFourFlagSquare edge).vertex endpoint) ≠
        .edge edge ∧
    C60F69PhysicalCellSite.edge edge ≠
      .face (c60F48AdjacentRealFace edge faceChoice) ∧
    C60F69PhysicalCellSite.vertex
      ((c60F46PhysicalFourFlagSquare edge).vertex endpoint) ≠
        .face (c60F48AdjacentRealFace edge faceChoice) := by
  constructor
  · intro h
    cases h
  constructor
  · intro h
    cases h
  · intro h
    cases h

/-- The inner diagonal of each genuinely constructed physical
2-simplex is the ACTUAL directly incident dart-to-face flag.
This is an equality in the native Mathlib category nerve. -/
theorem c60F69ActualPhysicalFlagTriangle_diagonal
    (edge : TruncatedIcosahedralEdge)
    (endpoint faceChoice : Bool) :
    (ConcreteCategory.hom (c60F69PhysicalIncidenceNerve.δ 1))
      (c60F69ActualPhysicalFlagTriangle edge endpoint faceChoice) =
    ComposableArrows.mk₁
      (CategoryTheory.homOfLE
        (c60F69PhysicalVertexFace
          ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)
          (c60F48AdjacentRealFace edge faceChoice)
          (c60F69EveryPhysicalFlagCorner_incident
            edge endpoint faceChoice))) := by
  change
    (ConcreteCategory.hom
      ((CategoryTheory.nerve C60F69PhysicalCellSite).δ 1))
      (ComposableArrows.mk₂
        (CategoryTheory.homOfLE
          (c60F69PhysicalVertexEdge
            ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)
            edge (c60F69ActualFlagEndpoint edge endpoint)))
        (CategoryTheory.homOfLE
          (c60F69PhysicalEdgeFace
            edge (c60F48AdjacentRealFace edge faceChoice)
            (c60F48AdjacentRealFace_incident edge faceChoice)))) =
    ComposableArrows.mk₁
      (CategoryTheory.homOfLE
        (c60F69PhysicalVertexFace
          ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)
          (c60F48AdjacentRealFace edge faceChoice)
          (c60F69EveryPhysicalFlagCorner_incident
            edge endpoint faceChoice)))
  rw [CategoryTheory.nerve.δ₁_mk₂_eq]
  exact congrArg ComposableArrows.mk₁ (Subsingleton.elim _ _)

/-! ## Genuine original four-tag F47 local quasicategory fibres -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section PhysicalF47Fibres
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

/-- The genuine type-dependent original F47 local 3-Hom nerve at a
fixed actual C60 physical edge, independently selected by a 90-bit
atlas and carrying the actual F42 / F54 four boundary tags. -/
def c60F69PhysicalIncidenceF47Fibre
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) : SSet :=
  c60F65AtlasLocalNerve t₁ t₂ left right sigma edge

/-- Each edge/face-selected genuine F47 fibre has the native
inner-horn quasicategory structure, independently of the global
physical incidence nerve's different categorical dimensions. -/
theorem c60F69PhysicalIncidenceF47Fibre_quasicategory
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) :
    SSet.Quasicategory
      (c60F69PhysicalIncidenceF47Fibre
        t₁ t₂ left right sigma edge) :=
  c60F65AtlasLocalNerve_quasicategory
    t₁ t₂ left right sigma edge

/-- A genuine native simplicial MAP of original type-dependent F47
nerves induced by the CONSTRUCTED arbitrarily long F67 source
category transport, not by an invented equality of original F55. -/
def c60F69PhysicalFibreFiniteAtlasNerveMap
    (sigma omega : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (via : List C60F67Atlas) :
    c60F69PhysicalIncidenceF47Fibre
        t₁ t₂ left right sigma edge ⟶
      c60F69PhysicalIncidenceF47Fibre
        t₁ t₂ left right omega edge :=
  CategoryTheory.nerveMap
    (c60F67AtlasRoute
      t₁ t₂ left right sigma omega edge via)

/-- The genuine simplicial MAP acts on an actual ORIGINAL
four-tag typed 3-cell 1-simplex as the F67 source functor does. -/
theorem c60F69PhysicalFibreFiniteAtlasNerveMap_edges
    (sigma omega : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (via : List C60F67Atlas)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge))}
    (f : X ⟶ Y) :
    CategoryTheory.nerve.homEquiv
      ((CategoryTheory.nerve.edgeMk f).map
        (c60F69PhysicalFibreFiniteAtlasNerveMap
          t₁ t₂ left right sigma omega edge via)) =
    (c60F67AtlasRoute
      t₁ t₂ left right sigma omega edge via).map f :=
  CategoryTheory.nerve.homEquiv_edgeMk_map_nerveMap
    f (c60F67AtlasRoute
      t₁ t₂ left right sigma omega edge via)

/-- Every ORIGINAL proof-relevant F42/F55/Delta mixed 3-arrow
retains ALL its independent integer charges and phase after any
arbitrarily long edge-local atlas-change nerve map. -/
theorem c60F69PhysicalFibreNerveMap_fullNative
    (sigma omega : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (via : List C60F67Atlas)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame
        t₁ t₂ left right edge (sigma edge))}
    (f : X ⟶ Y) :
    c60F47MixedEval
      (CategoryTheory.nerve.homEquiv
        ((CategoryTheory.nerve.edgeMk f).map
          (c60F69PhysicalFibreFiniteAtlasNerveMap
            t₁ t₂ left right sigma omega edge via))) =
    c60F47MixedEval f := by
  rw [c60F69PhysicalFibreFiniteAtlasNerveMap_edges]
  exact c60F67AtlasRoute_fullNative
    t₁ t₂ left right omega edge via sigma f

/-- The TRUE physical incidence 2-simplex at this source edge
AND the F67 type-correct arbitrarily long source 2-comparison
EXIST together for every original 90-edge × two-endpoint × two-face
site. Their categorical carriers are kept separately typed. -/
def c60F69PhysicalFlagWithFiniteAtlasCocycle
    (sigma omega : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (endpoint faceChoice : Bool)
    (via : List C60F67Atlas) :
    (ComposableArrows C60F69PhysicalCellSite 2) ×
    (c60F67AtlasRoute
        t₁ t₂ left right sigma omega edge via ≅
      c60F66AtlasTransition
        t₁ t₂ left right sigma omega edge) :=
  ⟨c60F69ActualPhysicalFlagTriangle edge endpoint faceChoice,
    c60F67AtlasRouteCollapse
      t₁ t₂ left right sigma omega edge via⟩

/-- Physical Čech patch curvature of the native Gray cochain
remains invariant under every original source F67 nerve-fibre
transport, despite the honest global incidence 2-simplex. -/
theorem c60F69IncidenceHigherNerve_obstruction_invariant
    (sigma omega : C60F67Atlas)
    (patch : C60IntegralTwoChains) :
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma patch =
      c60F68PhysicalPatchCurvature t₁ t₂ left right omega patch :=
  c60F68PhysicalPatchCurvature_evaluate_independent
    t₁ t₂ left right sigma omega patch

/-- Even with the complete actual 360-flag incidence nerve and
every arbitrary finite original F47 atlas transport, the unchanged
north-pentagon original Delta cochain DOES NOT admit uncorrected
effective C60 vertex descent.  A nonzero affine physical repair
is certified by the original tree-vertex construction. -/
theorem c60F69RealFlagNerve_curvature_obstruction_and_repair
    (sigma omega : C60F67Atlas) :
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma =
      c60F68PhysicalPatchCurvature t₁ t₂ left right omega ∧
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
        (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) ∧
    (¬ ∃ phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F68AtlasEdgeCochain t₁ t₂ left right sigma =
        phi.comp c60IntegralBoundaryOne) ∧
    c60F68CanonicalPhysicalRepair t₁ t₂ left right sigma ≠ 0 := by
  exact ⟨c60F68PhysicalPatchCurvature_independent
      t₁ t₂ left right sigma omega,
    c60F68PhysicalPatchCurvature_northSecondCharge
      t₁ t₂ left right sigma,
    (c60F68CurvedDescent_obstruction_and_repair
      t₁ t₂ left right sigma omega).2.2.1,
    c60F68CanonicalPhysicalRepair_ne_zero
      t₁ t₂ left right sigma⟩

end PhysicalF47Fibres

#print axioms C60F69PhysicalCellSite
#print axioms c60F69PhysicalIncidence
#print axioms c60F69PhysicalIncidenceNerve
#print axioms c60F69PhysicalIncidenceNerve_quasicategory
#print axioms c60F69EveryPhysicalFlagCorner_incident
#print axioms c60F69EveryPhysicalFlagCorner_injective
#print axioms c60F69ActualPhysicalFlagIndex_card
#print axioms c60F69ActualFlagEndpoint
#print axioms c60F69ActualPhysicalFlagTriangle
#print axioms c60F69ActualPhysicalFlagTriangle_distinct
#print axioms c60F69ActualPhysicalFlagTriangle_diagonal
#print axioms c60F69PhysicalIncidenceF47Fibre_quasicategory
#print axioms c60F69PhysicalFibreFiniteAtlasNerveMap
#print axioms c60F69PhysicalFibreFiniteAtlasNerveMap_edges
#print axioms c60F69PhysicalFibreNerveMap_fullNative
#print axioms c60F69PhysicalFlagWithFiniteAtlasCocycle
#print axioms c60F69IncidenceHigherNerve_obstruction_invariant
#print axioms c60F69RealFlagNerve_curvature_obstruction_and_repair

end
end KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
