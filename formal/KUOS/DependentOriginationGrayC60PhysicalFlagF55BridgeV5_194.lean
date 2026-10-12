import KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
import KUOS.DependentOriginationGrayC60BraidedThreeSectorV5_188
import KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157

namespace KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60BraidedThreeSectorV5_188
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F46 / v5.194 — actual C60 geometric four-flag / original F55 source bridge

The actual ORIGINAL C60 has precisely 60 darts, 90 physical edges,
32 genuinely pentagonal or hexagonal faces, and 360 *incidence*
flags. Each physical edge has a real K₂,₂ four-flag square
(two distinct physical endpoints × two distinct incident
polygonal faces), WITHOUT introducing a fictitious square face.

The existing F54/F55 independently selected original local
bracket-tree rotations provide the two exact F54 route boundaries
of an ORIGINAL F55 square 3-morphism on each of those same ninety
geometric incidence squares. The F59-F44 genuine 3-Hom CATEGORY
realizes the source F55 3-morphism, carrying *both* integer F58
charges and its independent braided Gray exchange phase.

Here we form a real nonconstant, SITE-SELECTIVE Mathlib FUNCTOR
from each original F54/F55 route 3-Hom category to the 182-site
C60 GrayGrade product category from F59-F40. The functor acts
by the COMPLETE original native F55 3-Hom map at ONE chosen
actual C60 edge, and by TRUE native identity on ALL other
89 original edges, 60 physical vertices and 32 original faces.
It preserves original categorical identity/composition,
is FAITHFUL at its chosen physical edge, and does NOT erase
either integer generator charge or the independent phase.

Genuine original source F55 square cells can therefore be
localized canonically to each real four-flag C60 incidence
carrier WITH exactly typed left-first/right-first original F54
boundaries, producing an actual nontrivial categorical 3-cell
at the physical square. We prove this for ALL ninety original
edges and the exact locally adjacent pentagon/hexagon or
hexagon/hexagon face carrier.

This is an honest, constructive LOCAL 3-Hom-to-C60-site bridge,
not a global dimension-preserving nondegenerate Gray 3-functor.
In particular, a physical K₂,₂ flag square is NOT an extra C60
surface face, and the independent F54 rotation 2-cell boundaries
are NOT silently made equal to the F42 polygonal face 2-cells.
Those require explicit further source boundary comparison.
-/

/-! ## I. All actual 90 physical four-flag incidence squares -/

/-- The EXACT original geometric four-flag square in the
pentagon/hexagon or hexagon/hexagon family, with all genuine
original C60 finite endpoint and neighboring face incidences. -/
noncomputable def c60F46PhysicalFourFlagSquare
    (edge : TruncatedIcosahedralEdge) :
    TruncatedEdgeFlagSquare edge :=
  match edge with
  | .around a => aroundPentagonHexagonSquare a
  | .cross e => crossHexagonHexagonSquare e

theorem c60F46PhysicalFourFlagSquare_allFourIncidences
    (edge : TruncatedIcosahedralEdge)
    (i j : Bool) :
    truncatedDartOnSeedFace
      ((c60F46PhysicalFourFlagSquare edge).vertex i)
      ((c60F46PhysicalFourFlagSquare edge).face j) :=
  (c60F46PhysicalFourFlagSquare edge).corner_incident i j

theorem c60F46PhysicalFourFlagSquare_fourDistinct
    (edge : TruncatedIcosahedralEdge) :
    Function.Injective
      (fun ij : Bool × Bool =>
        ((c60F46PhysicalFourFlagSquare edge).vertex ij.1,
         (c60F46PhysicalFourFlagSquare edge).face ij.2)) :=
  (c60F46PhysicalFourFlagSquare edge).corner_injective

/-- Every real around-edge square's FIRST incident face is the
original vertex-centered PENTAGON; the second is hexagonal. -/
theorem c60F46AroundFlag_firstRealPentagon
    (a : TruncatedIcosahedralAroundEdge) :
    (c60F46PhysicalFourFlagSquare (.around a)).firstFace =
      (.aroundVertex a.center) := rfl

/-- Every genuine cross-edge incidence square is between the
exact two original neighboring HEXAGONS. -/
theorem c60F46CrossFlag_firstHexagon
    (e : IcosahedralEdge) :
    (c60F46PhysicalFourFlagSquare (.cross e)).firstFace =
      (.fromTriangle (icosahedralEdgeIncidentFaces e).1) := rfl

theorem c60F46CrossFlag_secondHexagon
    (e : IcosahedralEdge) :
    (c60F46PhysicalFourFlagSquare (.cross e)).secondFace =
      (.fromTriangle (icosahedralEdgeIncidentFaces e).2) := rfl

/-! ## II. Genuine ORIGINAL F54/F55 square 3-cells on all 90 flags -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineOriginalF55
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

/-- An ACTUAL, fully ORIGINAL proof-relevant F55 source cell on
each original geometric C60 K₂,₂ flag square. It retains its
two distinct typed original F54 rotation route boundaries. -/
def c60F46PhysicalFlagOriginalF55Cell
    (edge : TruncatedIcosahedralEdge) :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right) :=
  match edge with
  | .around a =>
      (OriginalC60FlagSquareWithF55Generator.canonical a left right).squareCell
  | .cross e =>
      (OriginalC60CrossHexagonSquareWithF55Generator.canonical e left right).squareCell

/-- The same proof-relevant original F55 3-morphism, now a TRUE
categorical morphism of the F59-F44 original source 3-Hom
category, and not merely a free syntactic 3-cell. -/
def c60F46PhysicalFlagOriginalF55Arrow
    (edge : TruncatedIcosahedralEdge) :
    (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right) ⟶
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right) :=
  c60F44OriginalF55Of
    (c60F46PhysicalFlagOriginalF55Cell t₁ t₂ left right edge)

/-- Complete original real C60 ninety-edge SOURCE realization:
each categorical higher arrow has the genuine F55 generator
degree (0,1) and nonzero exchange phase ONE. -/
theorem c60F46PhysicalFlagOriginalF55Arrow_fullNative
    (edge : TruncatedIcosahedralEdge) :
    c60F44OriginalF55GrayFunctor.map
      (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right edge) =
        c60AllNinetyGrayCell t₁ t₂ left right edge := by
  cases edge <;> rfl

end GenuineOriginalF55

/-! ## III. The C60 edge-site-localized original 3-Hom FUNCTOR -/

section LocalizedCategoricalSource
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}

/-- Genuine nonconstant Mathlib FUNCTOR from the full original
F54/F55 typed 3-Hom category to the 182-site C60 native
GrayGrade category. It acts as the ACTUAL original F55 Gray
functor at exactly one physical edge, and as identity on all
other actual C60 sites, never assigning additional fake edges. -/
def c60F46EdgeLocalizedF55Functor
    (edge : TruncatedIcosahedralEdge) :
    (OriginalF45BracketTree.DepthRotationRoute first last) ⥤
      C60GrayIndexedTwoThreeCategory where
  obj _ := c60GrayPhysicalUnit
  map := fun {_ _} f site =>
    if site = C60GrayPhysicalSite.edge edge then
      c60F44OriginalF55GrayFunctor.map f
    else
      (𝟙 GrayGrade.unit)
  map_id := by
    intro route
    funext site
    by_cases hsite : site = C60GrayPhysicalSite.edge edge
    · subst site
      simp only [CategoryTheory.Pi.id_apply]
      exact c60F44OriginalF55GrayFunctor.map_id route
    · simp only [CategoryTheory.Pi.id_apply, if_neg hsite]
      rfl
  map_comp := by
    intro r s t f g
    funext site
    by_cases hsite : site = C60GrayPhysicalSite.edge edge
    · subst site
      simp only [CategoryTheory.Pi.comp_apply]
      exact c60F44OriginalF55GrayFunctor.map_comp f g
    · simp only [CategoryTheory.Pi.comp_apply, if_neg hsite]
      exact (Category.id_comp (𝟙 GrayGrade.unit)).symm

theorem c60F46EdgeLocalizedF55_atOriginalEdge
    (edge : TruncatedIcosahedralEdge)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (f : r ⟶ s) :
    ((c60F46EdgeLocalizedF55Functor edge).map f)
      (.edge edge) = c60F44OriginalF55GrayFunctor.map f := by
  simp [c60F46EdgeLocalizedF55Functor]

/-- All actual original C60 vertex positions receive only
the categorical IDENTITY on the localized F55 3-Hom image. -/
theorem c60F46EdgeLocalizedF55_atOriginalVertex
    (edge : TruncatedIcosahedralEdge)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (f : r ⟶ s) (dart : IcosahedralDart) :
    ((c60F46EdgeLocalizedF55Functor edge).map f)
      (.dart dart) = (𝟙 GrayGrade.unit) := by
  simp [c60F46EdgeLocalizedF55Functor]

/-- All 32 actual original C60 pentagon/hexagon FACE sites
remain separate, and are unchanged by edge-only F55 maps. -/
theorem c60F46EdgeLocalizedF55_atOriginalFace
    (edge : TruncatedIcosahedralEdge)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (f : r ⟶ s) (face : TruncatedIcosahedralSeedFace) :
    ((c60F46EdgeLocalizedF55Functor edge).map f)
      (.face face) = (𝟙 GrayGrade.unit) := by
  simp [c60F46EdgeLocalizedF55Functor]

/-- Original full F58 integer and F59 phase source-image
FAITHFULNESS survives C60-localization at a chosen real edge:
the actual selected 3-cell component recovers the entire
original F54/F55 categorical arrow (after its honest kernel
quotient) with no phase or generator-charge projection. -/
theorem c60F46EdgeLocalizedF55_faithful
    (edge : TruncatedIcosahedralEdge)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    {f g : r ⟶ s}
    (h : (c60F46EdgeLocalizedF55Functor edge).map f =
      (c60F46EdgeLocalizedF55Functor edge).map g) : f = g := by
  have hh := congrArg
    (fun z : (c60F46EdgeLocalizedF55Functor edge).obj r ⟶
      (c60F46EdgeLocalizedF55Functor edge).obj s =>
        z (.edge edge)) h
  change ((c60F46EdgeLocalizedF55Functor edge).map f) (.edge edge) =
    ((c60F46EdgeLocalizedF55Functor edge).map g) (.edge edge) at hh
  rw [c60F46EdgeLocalizedF55_atOriginalEdge,
      c60F46EdgeLocalizedF55_atOriginalEdge] at hh
  exact c60F44OriginalF55GrayFunctor_faithful hh

end LocalizedCategoricalSource

/-! ## IV. Actual ninety physical typed F55 3-Hom localizations -/

section AllNinety
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

/-- ACTUAL localized Gray target image of the original true
F55 square source 3-morphism ON ITS OWN real C60 incidence
edge, carrying (0,1;phase1) at exactly the correct site. -/
theorem c60F46EveryActualFlagSquare_localizedF55
    (edge : TruncatedIcosahedralEdge) :
    ((c60F46EdgeLocalizedF55Functor edge).map
      (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right edge))
        (.edge edge) =
      c60AllNinetyGrayCell t₁ t₂ left right edge := by
  rw [c60F46EdgeLocalizedF55_atOriginalEdge]
  exact c60F46PhysicalFlagOriginalF55Arrow_fullNative
    t₁ t₂ left right edge

/-- TRUE physical original ninety-edge indexed target field,
built at EVERY original edge from a genuine original F55
categorical SOURCE witness, identity at all 60 original
C60 vertices and 32 genuine pentagonal/hexagonal faces.
This is an honest morphism of the F59-F40 182-site CATEGORY. -/
def c60F46AllNinetyAuthenticSourceFlagField :
    c60GrayPhysicalUnit ⟶ c60GrayPhysicalUnit :=
  fun site =>
    match site with
    | .edge edge =>
        ((c60F46EdgeLocalizedF55Functor edge).map
          (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right edge))
            (.edge edge)
    | .dart _ => 𝟙 GrayGrade.unit
    | .face _ => 𝟙 GrayGrade.unit

theorem c60F46AllNinetyAuthenticSourceFlagField_edge
    (edge : TruncatedIcosahedralEdge) :
    c60F46AllNinetyAuthenticSourceFlagField t₁ t₂ left right
      (.edge edge) =
      c60AllNinetyGrayCell t₁ t₂ left right edge :=
  c60F46EveryActualFlagSquare_localizedF55 t₁ t₂ left right edge

/-- The authentic F55 source-interpreted categorical 3-cell
field on all 90 actual C60 edges is NONFLAT on the TRUE
north pentagon of the original C60 surface, as already
proved in the independent physical signed face-curvature
theorem.  This is not a claim that the real K₂,₂ flag
squares are surface quadrilateral faces. -/
theorem c60F46AllNinetyAuthenticSourceFlagField_northCurved :
    c60WangBiSignedGrayFace
      (fun edge => c60F46AllNinetyAuthenticSourceFlagField
          t₁ t₂ left right (.edge edge))
      (.aroundVertex .north) ≠ 0 := by
  have hfield :
      (fun edge => c60F46AllNinetyAuthenticSourceFlagField
        t₁ t₂ left right (.edge edge)) =
      c60F19UniformF55EdgeLabels := by
    funext edge
    rw [c60F46AllNinetyAuthenticSourceFlagField_edge,
      c60AllNinetyGrayCell_eq]
    rfl
  rw [hfield]
  exact c60WangBiOriginalF55NorthFace_nonflat

#print axioms c60F46EveryActualFlagSquare_localizedF55
#print axioms c60F46AllNinetyAuthenticSourceFlagField_edge
#print axioms c60F46AllNinetyAuthenticSourceFlagField_northCurved

end AllNinety

#print axioms c60F46PhysicalFourFlagSquare_allFourIncidences
#print axioms c60F46PhysicalFourFlagSquare_fourDistinct
#print axioms c60F46AroundFlag_firstRealPentagon
#print axioms c60F46CrossFlag_firstHexagon
#print axioms c60F46CrossFlag_secondHexagon
#print axioms c60F46PhysicalFlagOriginalF55Cell
#print axioms c60F46PhysicalFlagOriginalF55Arrow_fullNative
#print axioms c60F46EdgeLocalizedF55Functor
#print axioms c60F46EdgeLocalizedF55_atOriginalEdge
#print axioms c60F46EdgeLocalizedF55_atOriginalVertex
#print axioms c60F46EdgeLocalizedF55_atOriginalFace
#print axioms c60F46EdgeLocalizedF55_faithful

end
end KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
