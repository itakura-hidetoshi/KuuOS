import KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
import KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
import KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169

namespace KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157
open KUOS.DependentOriginationGrayC60YinYangFourImagesV5_170
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169
open KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F24 / v5.172 — native Wang Bi descent on all real C60 four-flags

The v5.171 native chart Category and six-Yao Functor are extended to:
* all 90 original C60 edges and their 4 genuine vertex/face flags;
* all 12 pentagons, with genuinely PHYSICAL Sheng edges (Ke chords
  remain virtual quiver decorations, not new C60 edges);
* all 20 original closed hexagons, each with six ordered and
  alternating physical boundary edges, supplied a CHOSEN 六氣 chart;
* the original independently charged F55 square 3-cell target.

A genuine Mathlib natural transformation intertwines the constant
physical four-flag functor with a chart-changing (six-Yao × F55-grade)
functor. The first coordinate is transported via the v5.171 chart
equivalence; the independent Int×Int charge and ZMod 2 exchange phase
are NOT discarded. The construction requires no equation of distinct
geometric square faces or identification of all native Gray 3-cells.

A C60 'square' here is the proven K2,2 INCIDENCE square around a real
edge, never a nonexistent quadrilateral polygon of C60. The local
endpoint Bool is an explicitly CHOSEN chart-relative side code.
六氣/三陰三陽 labels on the six boundary positions are a local
combinatorial context, not a clinical assertion or a canonical
classical correspondence forced by the topology.
-/

/-- The 60 around-pentagon and 30 cross-hexagon edges are assigned
their separately PROVED original four-incidence-flag squares. -/
noncomputable def c60ChosenGeometricSquare :
    (e : TruncatedIcosahedralEdge) → TruncatedEdgeFlagSquare e
  | .around a => aroundPentagonHexagonSquare a
  | .cross e => crossHexagonHexagonSquare e

/-- One of the four real flags over one of the 90 real C60 edges.
The two Bool coordinates choose an endpoint and an incident face. -/
abbrev C60ActualSquareCorner :=
  TruncatedIcosahedralEdge × (Bool × Bool)

/-- The actual dart and actual face at the selected corner. -/
def c60ActualCornerFlag
    (c : C60ActualSquareCorner) :
    IcosahedralDart × TruncatedIcosahedralSeedFace :=
  ((c60ChosenGeometricSquare c.1).vertex c.2.1,
    (c60ChosenGeometricSquare c.1).face c.2.2)

/-- Every corner denotes a TRUE incidence of the existing original
truncated-icosahedral 60/90/32 cellular structure. -/
theorem c60ActualCornerFlag_incident
    (c : C60ActualSquareCorner) :
    truncatedDartOnSeedFace
      (c60ActualCornerFlag c).1 (c60ActualCornerFlag c).2 := by
  exact (c60ChosenGeometricSquare c.1).corner_incident c.2.1 c.2.2

/-- Four distinct actual flags above EACH physical C60 edge. -/
theorem c60ActualCornerFlag_injective_on_edge
    (e : TruncatedIcosahedralEdge) :
    Function.Injective (fun ij : Bool × Bool =>
      c60ActualCornerFlag (e, ij)) := by
  exact (c60ChosenGeometricSquare e).corner_injective

/-- The two successive flags are EXACTLY the pre-existing four
images; no extra square face is inserted into the C60 CW complex. -/
def c60ActualCornerFourImage
    (c : C60ActualSquareCorner) : C60FourImage :=
  c60FourImageOfFlags c.2

theorem c60ActualCornerFourImage_bijective_on_edge
    (e : TruncatedIcosahedralEdge) :
    Function.Bijective (fun ij : Bool × Bool =>
      c60ActualCornerFourImage (e, ij)) := by
  exact c60FourImageOfFlags_bijective

/-- The old genuine ninety-edge count yields exactly 360 local flags,
not 360 additional edges or C60 polygonal faces. -/
theorem c60ActualSquareCorner_card :
    Fintype.card C60ActualSquareCorner = 360 := by
  simp [C60ActualSquareCorner, Fintype.card_prod,
    allOriginalTruncatedEdge_card_kernel]

/-- Locally chosen endpoint side plus a genuinely incident face
is one of the 64 *existing* C60 signed-face symbols. Adjacent edge
charts need not assign the same local side without a further gauge. -/
def c60ActualCornerSignedFace
    (c : C60ActualSquareCorner) : C60WangBiSignedFace :=
  ((c60ActualCornerFlag c).2, c.2.1)

/-- The constant chart-independent geometric corner category
representation, on the very SAME WangBiFrame source category. -/
def c60ActualCornerFunctor : WangBiFrame ⥤ Type 0 where
  obj _ := C60ActualSquareCorner
  map := fun {_ _} _ => TypeCat.ofHom (id : C60ActualSquareCorner → C60ActualSquareCorner)
  map_id := by intro _; rfl
  map_comp := by intros; rfl

/-- Physical six-Yao codes paired with an INDEPENDENT braided F55
3-cell grade. Chart change acts ONLY on the six-Yao coordinate.
This is an actual native Mathlib Functor, not a pseudofunctor claim. -/
def c60GradedSixYaoFunctor : WangBiFrame ⥤ Type 0 where
  obj _ := WangBiSixYao × GradedThreeCell 0 0
  map := fun {a b} f =>
    TypeCat.ofHom (fun x : WangBiSixYao × GradedThreeCell 0 0 =>
      (wangBiChartArrow a b f x.1, x.2))
  map_id := by
    intro a
    apply TypeCat.homEquiv.injective
    funext x
    rcases x with ⟨code, grade⟩
    exact congrArg (fun y => (y, grade)) (wangBiChartArrow_id a code)
  map_comp := by
    intro a b c f g
    apply TypeCat.homEquiv.injective
    funext x
    rcases x with ⟨code, grade⟩
    exact congrArg (fun y => (y, grade))
      (wangBiChartArrow_comp a b c f g code)

/-- A local square chart with a separately supplied authentic
braided grade. The grade depends on the PHYSICAL edge, never on
arbitrary six-Yao face enumeration. -/
def c60CornerGradedLabel
    (a : WangBiFrame) (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (c : C60ActualSquareCorner) : WangBiSixYao × GradedThreeCell 0 0 :=
  (wangBiOriginalFaceEncoding a (c60ActualCornerSignedFace c),
    grade c.1)

/-- This is the formal LOCAL-TO-LOCAL coherence square, preserved for
every original geometric corner and EVERY independently given grade. -/
theorem c60CornerGradedLabel_naturality
    (a b : WangBiFrame) (f : a ⟶ b)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (c : C60ActualSquareCorner) :
    (wangBiChartArrow a b f (c60CornerGradedLabel a grade c).1,
      (c60CornerGradedLabel a grade c).2) =
      c60CornerGradedLabel b grade c := by
  exact congrArg (fun code => (code, grade c.1))
    (wangBiEncodingNaturality a b f (c60ActualCornerSignedFace c))

/-- An ACTUAL natural transformation between two Mathlib functors
on WangBiFrame; this is stronger than 360 unrelated equations. -/
def c60CornerGradedNaturalTransformation
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor where
  app a := TypeCat.ofHom (c60CornerGradedLabel a grade)
  naturality := by
    intro a b f
    apply TypeCat.homEquiv.injective
    funext c
    exact (c60CornerGradedLabel_naturality a b f grade c).symm

/-- Time-dependent semantic meanings are also invariant on ALL
real C60 corners under the supplied Wang Bi chart change. -/
def c60CornerTemporalRead
    {T M : Type*} (a : WangBiFrame) (r : WangBiTemporalReading T M)
    (c : C60ActualSquareCorner) (t : T) : M :=
  wangBiFrameRead a r (c60ActualCornerSignedFace c) t

theorem c60CornerTemporalRead_transport
    {T M : Type*} (a b : WangBiFrame) (f : a ⟶ b)
    (r : WangBiTemporalReading T M)
    (c : C60ActualSquareCorner) (t : T) :
    c60CornerTemporalRead b (wangBiFrameTransport a b f r) c t =
      c60CornerTemporalRead a r c t :=
  wangBiSemanticSquare a b f r (c60ActualCornerSignedFace c) t

/-- Place a true Wuxing generative arrow on a real C60 pentagon
edge and then select one of its four square flags. -/
def c60PentagonShengCorner
    (v : IcosahedralVertex) (p : WuxingPhase)
    (ij : Bool × Bool) : C60ActualSquareCorner :=
  (c60WuxingShengPhysicalEdge v p, ij)

/-- The Sheng square's first face is literally the original pentagon,
not its virtual two-step controlling diagonal. -/
theorem c60PentagonShengCorner_firstFace
    (v : IcosahedralVertex) (p : WuxingPhase) (i : Bool) :
    (c60ActualCornerFlag
      (c60PentagonShengCorner v p (i, false))).2 =
        .aroundVertex v := by
  rfl

/-- A 12×5 family of actual physical generative edges, with
chart-transported Wang Bi meanings for every time and side. -/
theorem c60PentagonShengMeaning_transport
    {T M : Type*} (a b : WangBiFrame) (f : a ⟶ b)
    (r : WangBiTemporalReading T M)
    (v : IcosahedralVertex) (p : WuxingPhase)
    (ij : Bool × Bool) (t : T) :
    c60CornerTemporalRead b (wangBiFrameTransport a b f r)
      (c60PentagonShengCorner v p ij) t =
    c60CornerTemporalRead a r (c60PentagonShengCorner v p ij) t :=
  c60CornerTemporalRead_transport a b f r _ t

/-- A CHOSEN local ordering of the traditional 六氣 terms with
three 陰 and three 陽 designations. The six labels are separate
from a physical temperature or a medical diagnostic finding. -/
inductive C60SixQi
  | jueyin | shaoyin | shaoyang | taiyin | yangming | taiyang
  deriving DecidableEq, Repr, Fintype

def C60SixQi.isYin : C60SixQi → Bool
  | .jueyin | .shaoyin | .taiyin => true
  | .shaoyang | .yangming | .taiyang => false

theorem c60SixQi_threeYin :
    (Finset.univ.filter (fun q : C60SixQi => q.isYin = true)).card = 3 := by
  decide

theorem c60SixQi_threeYang :
    (Finset.univ.filter (fun q : C60SixQi => q.isYin = false)).card = 3 := by
  decide

/-- The traditional names decorate, IN ORDER, the six actual
oriented edges of each of the twenty existing hexagonal cycles.
The geometrical cyclic order is supplied by v3.86. -/
def c60SixQiHexagonBoundaryEdge
    (face : IcosahedralFace) : C60SixQi → TruncatedIcosahedralEdge
  | .jueyin  => (truncatedIcosahedralHexagonCycle face).e0.edge
  | .shaoyin => (truncatedIcosahedralHexagonCycle face).e1.edge
  | .shaoyang => (truncatedIcosahedralHexagonCycle face).e2.edge
  | .taiyin => (truncatedIcosahedralHexagonCycle face).e3.edge
  | .yangming => (truncatedIcosahedralHexagonCycle face).e4.edge
  | .taiyang => (truncatedIcosahedralHexagonCycle face).e5.edge

/-- These six labels really follow the original alternating
around/cross boundary, rather than generating six new edges. -/
theorem c60SixQiHexagonBoundary_family_pattern
    (face : IcosahedralFace) :
    (truncatedIcosahedralEdgeFamily (c60SixQiHexagonBoundaryEdge face .jueyin),
      truncatedIcosahedralEdgeFamily (c60SixQiHexagonBoundaryEdge face .shaoyin),
      truncatedIcosahedralEdgeFamily (c60SixQiHexagonBoundaryEdge face .shaoyang),
      truncatedIcosahedralEdgeFamily (c60SixQiHexagonBoundaryEdge face .taiyin),
      truncatedIcosahedralEdgeFamily (c60SixQiHexagonBoundaryEdge face .yangming),
      truncatedIcosahedralEdgeFamily (c60SixQiHexagonBoundaryEdge face .taiyang)) =
      (.around, .cross, .around, .cross, .around, .cross) := by
  exact truncatedIcosahedralHexagonCycle_family_pattern face

/-- Actual source geometry closes after these exact six oriented
edge positions: no artificial hexagon cycle is added. -/
theorem c60SixQiHexagonBoundary_closed (face : IcosahedralFace) :
    (truncatedIcosahedralHexagonCycle face).e5.target =
      (truncatedIcosahedralHexagonCycle face).e0.source :=
  (truncatedIcosahedralHexagonCycle face).h50

/-- Place each 六氣 slot back on a real physical four-flag square. -/
def c60SixQiHexagonCorner
    (face : IcosahedralFace) (q : C60SixQi)
    (ij : Bool × Bool) : C60ActualSquareCorner :=
  (c60SixQiHexagonBoundaryEdge face q, ij)

/-- The 20 genuine hexagons × six labelled edges = 120 original
boundary incidences, NOT 120 new C60 edges. -/
theorem c60SixQiHexagonSlots_card :
    Fintype.card (IcosahedralFace × C60SixQi) = 120 := by
  decide

/-- All twenty true hexagons inherit the SAME higher naturality,
with each of their six actual edge-square corners. -/
theorem c60SixQiMeaning_transport
    {T M : Type*} (a b : WangBiFrame) (f : a ⟶ b)
    (r : WangBiTemporalReading T M)
    (face : IcosahedralFace) (q : C60SixQi)
    (ij : Bool × Bool) (t : T) :
    c60CornerTemporalRead b (wangBiFrameTransport a b f r)
      (c60SixQiHexagonCorner face q ij) t =
    c60CornerTemporalRead a r (c60SixQiHexagonCorner face q ij) t :=
  c60CornerTemporalRead_transport a b f r _ t

/-- The concrete F55-braided grade is the already-proved, NONTRIVIAL
independent original square generator with its exact charges. -/
def c60OriginalF55GradedNaturality :
    c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor :=
  c60CornerGradedNaturalTransformation
    (fun _ => originalF55BraidedSquareGenerator)

/-- At each of the ninety true C60 edges, and all four flags,
the natural transformation carries the nonzero original F55
exchange phase AND its independent integer square charge. -/
theorem c60OriginalF55EveryCorner_components
    (a : WangBiFrame) (c : C60ActualSquareCorner) :
    (c60CornerGradedLabel a (fun _ => originalF55BraidedSquareGenerator) c).2.charge =
        ((0 : Int), (1 : Int)) ∧
    (c60CornerGradedLabel a (fun _ => originalF55BraidedSquareGenerator) c).2.phase =
        (1 : ZMod 2) :=
  originalF55BraidedSquareGenerator_complete

/-! Cross-check against the already implemented genuine F55-labeled
90-edge geometry. This identifies the new graded chart functor's
edge labels with those obtained by interpreting actually supplied
F54 source rotations, not with freely invented extra generators. -/
universe uD vD uE vE
section OriginalF55Agreement
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b}
variable {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- With the original F54 input rotations explicitly supplied,
the old physical F55 edge generator and the new enriched natural
transformation agree, FOR ALL NINETY ACTUAL C60 EDGES. -/
theorem c60CornerGrade_matches_originalPhysicalF55
    (aFrame : WangBiFrame) (c : C60ActualSquareCorner) :
    (c60CornerGradedLabel aFrame
      (fun _ => originalF55BraidedSquareGenerator) c).2 =
      c60AllNinetyGrayCell t₁ t₂ left right c.1 := by
  exact (c60AllNinetyGrayCell_eq t₁ t₂ left right c.1).symm

end OriginalF55Agreement

#print axioms c60ActualCornerFlag_incident
#print axioms c60ActualCornerFlag_injective_on_edge
#print axioms c60ActualCornerFourImage_bijective_on_edge
#print axioms c60ActualSquareCorner_card
#print axioms c60ActualCornerFunctor
#print axioms c60GradedSixYaoFunctor
#print axioms c60CornerGradedLabel_naturality
#print axioms c60CornerGradedNaturalTransformation
#print axioms c60CornerTemporalRead_transport
#print axioms c60PentagonShengCorner_firstFace
#print axioms c60PentagonShengMeaning_transport
#print axioms c60SixQi_threeYin
#print axioms c60SixQi_threeYang
#print axioms c60SixQiHexagonBoundary_family_pattern
#print axioms c60SixQiHexagonBoundary_closed
#print axioms c60SixQiHexagonSlots_card
#print axioms c60SixQiMeaning_transport
#print axioms c60OriginalF55GradedNaturality
#print axioms c60OriginalF55EveryCorner_components
#print axioms c60CornerGrade_matches_originalPhysicalF55

end
end KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
