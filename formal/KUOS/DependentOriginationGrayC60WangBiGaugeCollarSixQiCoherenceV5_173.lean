import KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
import KUOS.DependentOriginationTruncatedIcosahedralCyclicSquareCollarGluingV5_154

namespace KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayC60YinYangFourImagesV5_170
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169
open KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F25 / v5.173 — Wang Bi descent across genuine C60 shared flags

v5.172 makes a real Mathlib natural transformation on all 90 four-flag
edge squares, but its chosen ENDPOINT Bool is deliberately only a LOCAL
side coordinate. At a physical pentagon shared vertex, the outgoing
edge has Bool=true while the next edge has Bool=false. Identifying
those two local coordinates as the same global Yin/Yang side would
incorrectly glue distinct local encodings.

Here an explicitly chosen DART-BASED side gauge resolves this:
  signed(c) = (actualFace(c), gauge(actualDart(c))).
Two physical flags with equal dart/face now have equal 64-symbol
encodings in EVERY Wang Bi chart and at EVERY supplied time, and the
graded NatTrans remains a genuine functorial natural transformation.

More importantly, equality of the ENTIRE (64-symbol, F55 3-cell)
label is characterized by equality of independently supplied Gray
grades on the two original edges. In the original F55 instance this
criterion is satisfied while retaining (0,1) square charge and
nonzero odd/odd exchange phase on each square. All twelve actual
pentagon collars therefore glue cyclically in this gauge.

For all twenty REAL hexagons, the original oriented six-edge cycle
is indexed by a chosen 六氣 local chart. Its source/target dart-face
flags are incident, glued cyclically, and acquire the same
gauge-corrected six-Yao and nontrivial F55 labels. The native
six-square F55 composite has charge (0,6), phase 0: this is the
UNSIGNED six-edge composite; it is NOT confused with the signed
oriented F59-F19 face curvature or the ancient 六氣 interpretation.

The F55 target values are genuine native braided 3-cells. This is
not yet a fully faithful Gray 3-functor on all raw source F55
PresentedCells or a theorem about actual traditional text semantics.
-/

/-- A genuinely GLOBAL local-real-side gauge assigned to each
of the sixty physical C60 darts; not fixed intrinsic Yin/Yang. -/
abbrev C60DartSideGauge := IcosahedralDart → Bool

/-- Encode an actual vertex-face corner using the physical dart
for the side gauge, instead of the non-gluing local endpoint index. -/
def c60GaugeSignedFace (side : C60DartSideGauge)
    (c : C60ActualSquareCorner) : C60WangBiSignedFace :=
  ((c60ActualCornerFlag c).2, side (c60ActualCornerFlag c).1)

/-- Any two descriptions of the SAME original C60 geometric flag
have the same chosen globally gauged signed-face code. -/
theorem c60GaugeSignedFace_eq_of_flag_eq
    (side : C60DartSideGauge)
    {c d : C60ActualSquareCorner}
    (h : c60ActualCornerFlag c = c60ActualCornerFlag d) :
    c60GaugeSignedFace side c = c60GaugeSignedFace side d := by
  unfold c60GaugeSignedFace
  rw [h]

/-- A corrected six-Yao label with an INDEPENDENT native braided
3-cell on each actual edge. -/
def c60GaugeGradedLabel
    (a : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (c : C60ActualSquareCorner) :
    WangBiSixYao × GradedThreeCell 0 0 :=
  (wangBiOriginalFaceEncoding a (c60GaugeSignedFace side c),
    grade c.1)

/-- For matching physical flags, high-dimensional gluing holds
IF AND ONLY IF the original edge's independently supplied Gray
3-cell labels agree. The six-Yao comparison alone cannot force
two arbitrary nontrivial original higher witnesses to be equal. -/
theorem c60GaugeGradedLabel_eq_iff_grade_eq
    (a : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    {c d : C60ActualSquareCorner}
    (h : c60ActualCornerFlag c = c60ActualCornerFlag d) :
    c60GaugeGradedLabel a side grade c =
      c60GaugeGradedLabel a side grade d ↔
      grade c.1 = grade d.1 := by
  have hs := c60GaugeSignedFace_eq_of_flag_eq side h
  constructor
  · intro heq
    exact congrArg Prod.snd heq
  · intro hg
    exact Prod.ext (congrArg (wangBiOriginalFaceEncoding a) hs) hg

/-- TRUE naturality of the corrected gauge-label construction,
for arbitrary native Gray 3-cell edge data and every frame change. -/
theorem c60GaugeGradedLabel_natural
    (a b : WangBiFrame) (f : a ⟶ b)
    (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (c : C60ActualSquareCorner) :
    (wangBiChartArrow a b f (c60GaugeGradedLabel a side grade c).1,
      (c60GaugeGradedLabel a side grade c).2) =
      c60GaugeGradedLabel b side grade c := by
  exact congrArg (fun x => (x, grade c.1))
    (wangBiEncodingNaturality a b f (c60GaugeSignedFace side c))

/-- An honest Mathlib natural transformation in the old v5.171
WangBiFrame category from the real 90-edge geometric corner functor
to the old independently graded six-Yao target functor. -/
def c60GaugeGradedNatTrans
    (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    c60ActualCornerFunctor ⟶ c60GradedSixYaoFunctor where
  app a := TypeCat.ofHom (c60GaugeGradedLabel a side grade)
  naturality := by
    intro a b f
    apply TypeCat.homEquiv.injective
    funext c
    exact (c60GaugeGradedLabel_natural a b f side grade c).symm

/-- The time-dependent 王弼 interpretation is supplied separately
and evaluated at the actual globally gauged signed face. -/
def c60GaugeTemporalRead
    {T M : Type*} (a : WangBiFrame)
    (r : WangBiTemporalReading T M)
    (side : C60DartSideGauge)
    (c : C60ActualSquareCorner) (t : T) : M :=
  wangBiFrameRead a r (c60GaugeSignedFace side c) t

theorem c60GaugeTemporalRead_natural
    {T M : Type*} (a b : WangBiFrame) (f : a ⟶ b)
    (r : WangBiTemporalReading T M)
    (side : C60DartSideGauge)
    (c : C60ActualSquareCorner) (t : T) :
    c60GaugeTemporalRead b (wangBiFrameTransport a b f r) side c t =
      c60GaugeTemporalRead a r side c t :=
  wangBiSemanticSquare a b f r (c60GaugeSignedFace side c) t

theorem c60GaugeTemporalRead_glues
    {T M : Type*} (a : WangBiFrame)
    (r : WangBiTemporalReading T M)
    (side : C60DartSideGauge)
    {c d : C60ActualSquareCorner}
    (h : c60ActualCornerFlag c = c60ActualCornerFlag d)
    (t : T) :
    c60GaugeTemporalRead a r side c t =
      c60GaugeTemporalRead a r side d t := by
  exact congrArg (fun x => wangBiFrameRead a r x t)
    (c60GaugeSignedFace_eq_of_flag_eq side h)

/-! ## All twelve real pentagonal Wuxing collars. -/

/-- Physical END corner of one original generative Wuxing edge,
on the original pentagon side of its actual incidence square. -/
def c60ShengEndCorner
    (v : IcosahedralVertex) (p : WuxingPhase) :
    C60ActualSquareCorner :=
  (c60WuxingShengPhysicalEdge v p, (true, false))

/-- Physical START corner of the next generative Wuxing edge.
It is a DIFFERENT local Bool coordinate for the SAME real flag. -/
def c60ShengNextStartCorner
    (v : IcosahedralVertex) (p : WuxingPhase) :
    C60ActualSquareCorner :=
  (c60WuxingShengPhysicalEdge v (wuxingSheng p), (false, false))

/-- The five genuine Wuxing pentagon edges share exactly the same
actual C60 dart AND pentagonal face at each consecutive junction.
This includes the fifth-to-first closure. -/
theorem c60ShengConsecutive_actualFlag
    (v : IcosahedralVertex) (p : WuxingPhase) :
    c60ActualCornerFlag (c60ShengEndCorner v p) =
      c60ActualCornerFlag (c60ShengNextStartCorner v p) := by
  apply Prod.ext
  · change icosahedralIncidentDartAt v (pentagonalSlotNext (wuxingSlotEquiv p)) =
        icosahedralIncidentDartAt v (wuxingSlotEquiv (wuxingSheng p))
    rw [wuxingSlotSheng_equivariant]
  · rfl

/-- All twelve five-edge pentagon collars now satisfy a PRECISE
gluing criterion: the 64-code agrees automatically via global
dart gauge; equality of independently chosen higher data remains
the necessary and sufficient condition. -/
theorem c60ShengConsecutive_grade_glue_iff
    (a : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (v : IcosahedralVertex) (p : WuxingPhase) :
    c60GaugeGradedLabel a side grade (c60ShengEndCorner v p) =
      c60GaugeGradedLabel a side grade (c60ShengNextStartCorner v p) ↔
    grade (c60WuxingShengPhysicalEdge v p) =
      grade (c60WuxingShengPhysicalEdge v (wuxingSheng p)) :=
  c60GaugeGradedLabel_eq_iff_grade_eq a side grade
    (c60ShengConsecutive_actualFlag v p)

/-- The original F55 square generator provides the NONTRIVIAL
higher cell grade making all five physical pentagon junctions
glue, without quotienting away exchange phase or integer charge. -/
theorem c60ShengConsecutive_originalF55_glues
    (a : WangBiFrame) (side : C60DartSideGauge)
    (v : IcosahedralVertex) (p : WuxingPhase) :
    c60GaugeGradedLabel a side
      (fun _ => originalF55BraidedSquareGenerator) (c60ShengEndCorner v p) =
    c60GaugeGradedLabel a side
      (fun _ => originalF55BraidedSquareGenerator)
        (c60ShengNextStartCorner v p) :=
  (c60ShengConsecutive_grade_glue_iff a side
    (fun _ => originalF55BraidedSquareGenerator) v p).2 rfl

/-- The independently supplied time-dependent meanings ALSO glue
at each actual pentagon junction, before or after chart transport. -/
theorem c60ShengConsecutive_meaning_glues
    {T M : Type*} (a : WangBiFrame) (side : C60DartSideGauge)
    (r : WangBiTemporalReading T M)
    (v : IcosahedralVertex) (p : WuxingPhase) (t : T) :
    c60GaugeTemporalRead a r side (c60ShengEndCorner v p) t =
      c60GaugeTemporalRead a r side
        (c60ShengNextStartCorner v p) t :=
  c60GaugeTemporalRead_glues a r side
    (c60ShengConsecutive_actualFlag v p) t

/-- All five locally glued original F55 square labels, in the
genuine Wood→Fire→Earth→Metal→Water physical Sheng edge order. -/
def c60ShengWangBiF55SquareList
    (a : WangBiFrame) (side : C60DartSideGauge)
    (v : IcosahedralVertex) : List (GradedThreeCell 0 0) :=
  wuxingGenerativeOrder.map (fun p =>
    (c60GaugeGradedLabel a side
      (fun _ => originalF55BraidedSquareGenerator)
      (c60ShengEndCorner v p)).2)

/-! Genuine F55 target-side comparison with the SAME old independently
typed F54 local rotation inputs, not just an arithmetic five-count. -/
universe uD vD uE vE
section PentagonNativeComparison
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {aa bb : D} {xx yy : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks aa bb}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks xx yy}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

include left right

/-- The new Wang Bi gauge-glued local list is IDENTICAL to the
old five ACTUAL F55 interpreted C60 squares, retaining original
typed F54 rotations. -/
theorem c60ShengWangBiF55SquareList_eq_original
    (a : WangBiFrame) (side : C60DartSideGauge)
    (v : IcosahedralVertex) :
    c60ShengWangBiF55SquareList a side v =
      c60GraySquareList t₁ t₂ left right v := by
  rw [c60GraySquareList_eq t₁ t₂ left right v]
  rfl

/-- Gauge-compatible C60 original pentagon generator together
with its five ACTUAL adjoining F55 squares gives the same
NATIVE CATEGORY composition as the original charged Gray collar.
No new Gray coherence axioms are assumed. -/
theorem c60ShengWangBiF55_native_collaring
    (a : WangBiFrame) (side : C60DartSideGauge)
    (v : IcosahedralVertex) :
    c60GrayPentagon t₁ t₂ t₃ t₄ v +
      (c60ShengWangBiF55SquareList a side v).sum =
    (c60GrayPentagon t₁ t₂ t₃ t₄ v ≫
      (c60GraySquareList t₁ t₂ left right v).sum :
        GrayGrade.unit ⟶ GrayGrade.unit) := by
  rw [c60ShengWangBiF55SquareList_eq_original t₁ t₂ left right a side v]
  exact c60GrayCollar_native_comp t₁ t₂ t₃ t₄ left right v

/-- The FULL original pentagon Gray 3-cell still carries (1,5;1),
and the glued Wang Bi 64-code charts do not erase this phase. -/
theorem c60ShengWangBiF55_collar_components
    (a : WangBiFrame) (side : C60DartSideGauge)
    (v : IcosahedralVertex) :
    (c60GrayPentagon t₁ t₂ t₃ t₄ v +
      (c60ShengWangBiF55SquareList a side v).sum).charge =
        ((1 : Int), (5 : Int)) ∧
    (c60GrayPentagon t₁ t₂ t₃ t₄ v +
      (c60ShengWangBiF55SquareList a side v).sum).phase =
        (1 : ZMod 2) := by
  rw [c60ShengWangBiF55SquareList_eq_original t₁ t₂ left right a side v]
  exact c60GrayCollar_components t₁ t₂ t₃ t₄ left right v

end PentagonNativeComparison

/-! ## Genuine 20 hexagonal 六氣 oriented collars. -/

/-- A CHOSEN sixfold cyclic order on the context names, not a
claim that chronology or a medical transition follows C60 edges. -/
def c60SixQiNext : C60SixQi → C60SixQi
  | .jueyin => .shaoyin
  | .shaoyin => .shaoyang
  | .shaoyang => .taiyin
  | .taiyin => .yangming
  | .yangming => .taiyang
  | .taiyang => .jueyin

/-- Attach every 六氣 context slot to the EXACT ORIENTED
edge of the genuine old closed icosahedral hexagonal boundary. -/
def c60SixQiOrientedEdge
    (face : IcosahedralFace) : C60SixQi →
      OrientedTruncatedIcosahedralEdge
  | .jueyin => (truncatedIcosahedralHexagonCycle face).e0
  | .shaoyin => (truncatedIcosahedralHexagonCycle face).e1
  | .shaoyang => (truncatedIcosahedralHexagonCycle face).e2
  | .taiyin => (truncatedIcosahedralHexagonCycle face).e3
  | .yangming => (truncatedIcosahedralHexagonCycle face).e4
  | .taiyang => (truncatedIcosahedralHexagonCycle face).e5

/-- Six-qi source edges are EXACTLY the previous v5.172
underlying unoriented actual hexagonal boundary edges. -/
theorem c60SixQiOrientedEdge_underlying
    (face : IcosahedralFace) (q : C60SixQi) :
    (c60SixQiOrientedEdge face q).edge =
      c60SixQiHexagonBoundaryEdge face q := by
  cases q <;> rfl

/-- The ORIGINAL six typed endpoint equalities give all SIX
cyclic neighboring hexagonal connections, including closing
back from 太陽 to 厥陰. -/
theorem c60SixQiOriented_consecutive
    (face : IcosahedralFace) (q : C60SixQi) :
    (c60SixQiOrientedEdge face q).target =
      (c60SixQiOrientedEdge face (c60SixQiNext q)).source := by
  cases q with
  | jueyin => exact (truncatedIcosahedralHexagonCycle face).h01
  | shaoyin => exact (truncatedIcosahedralHexagonCycle face).h12
  | shaoyang => exact (truncatedIcosahedralHexagonCycle face).h23
  | taiyin => exact (truncatedIcosahedralHexagonCycle face).h34
  | yangming => exact (truncatedIcosahedralHexagonCycle face).h45
  | taiyang => exact (truncatedIcosahedralHexagonCycle face).h50

/-- TRUE geometric source and target flags of the original
hexagon boundary edge, not an invented quadrilateral face. -/
def c60SixQiSourceFlag
    (face : IcosahedralFace) (q : C60SixQi) :
    IcosahedralDart × TruncatedIcosahedralSeedFace :=
  ((c60SixQiOrientedEdge face q).source, .fromTriangle face)

def c60SixQiTargetFlag
    (face : IcosahedralFace) (q : C60SixQi) :
    IcosahedralDart × TruncatedIcosahedralSeedFace :=
  ((c60SixQiOrientedEdge face q).target, .fromTriangle face)

/-- Finite KERNEL computation, on ALL twenty true hexagons and
all six oriented slots: every boundary source flag is incident
to its actual original triangle-origin hexagon face. -/
theorem c60SixQiSourceFlag_incident :
    ∀ face : IcosahedralFace, ∀ q : C60SixQi,
      truncatedDartOnSeedFace
        (c60SixQiSourceFlag face q).1
        (c60SixQiSourceFlag face q).2 := by
  intro face q
  cases face <;> cases q <;>
    simp [c60SixQiSourceFlag, c60SixQiOrientedEdge,
      truncatedIcosahedralHexagonCycle,
      OrientedTruncatedIcosahedralEdge.source,
      truncatedDartOnSeedFace, icosahedralFaceEdges,
      icosahedralIncidentDartAt]

theorem c60SixQiTargetFlag_consecutive
    (face : IcosahedralFace) (q : C60SixQi) :
    c60SixQiTargetFlag face q =
      c60SixQiSourceFlag face (c60SixQiNext q) := by
  exact Prod.ext (c60SixQiOriented_consecutive face q) rfl

/-- The target flag is therefore genuine and automatically
incident as well: all 120 links glue at real C60 hexagon darts. -/
theorem c60SixQiTargetFlag_incident
    (face : IcosahedralFace) (q : C60SixQi) :
    truncatedDartOnSeedFace
      (c60SixQiTargetFlag face q).1
      (c60SixQiTargetFlag face q).2 := by
  rw [c60SixQiTargetFlag_consecutive]
  exact c60SixQiSourceFlag_incident face (c60SixQiNext q)

/-- The chosen common side gauge evaluates at the TRUE oriented
hexagonal boundary dart, with a single underlying actual hexagon. -/
def c60SixQiSourceSignedFace
    (side : C60DartSideGauge)
    (face : IcosahedralFace) (q : C60SixQi) : C60WangBiSignedFace :=
  ((c60SixQiSourceFlag face q).2, side (c60SixQiSourceFlag face q).1)

def c60SixQiTargetSignedFace
    (side : C60DartSideGauge)
    (face : IcosahedralFace) (q : C60SixQi) : C60WangBiSignedFace :=
  ((c60SixQiTargetFlag face q).2, side (c60SixQiTargetFlag face q).1)

theorem c60SixQiSignedFace_consecutive
    (side : C60DartSideGauge)
    (face : IcosahedralFace) (q : C60SixQi) :
    c60SixQiTargetSignedFace side face q =
      c60SixQiSourceSignedFace side face (c60SixQiNext q) := by
  exact congrArg (fun flag : IcosahedralDart × TruncatedIcosahedralSeedFace =>
      (flag.2, side flag.1)) (c60SixQiTargetFlag_consecutive face q)

/-- Original physical 六氣 edge, Wang Bi symbol, and genuine
native F55-grade value are distinct, typed components. -/
def c60SixQiSourceGradedLabel
    (a : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : IcosahedralFace) (q : C60SixQi) :
    WangBiSixYao × GradedThreeCell 0 0 :=
  (wangBiOriginalFaceEncoding a (c60SixQiSourceSignedFace side face q),
    grade (c60SixQiHexagonBoundaryEdge face q))

def c60SixQiTargetGradedLabel
    (a : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : IcosahedralFace) (q : C60SixQi) :
    WangBiSixYao × GradedThreeCell 0 0 :=
  (wangBiOriginalFaceEncoding a (c60SixQiTargetSignedFace side face q),
    grade (c60SixQiHexagonBoundaryEdge face q))

/-- Six independent, cyclic hexagonal edge-square gluing tests:
the WHOLE label joins precisely when two original F55 3-cell
grades agree. The Wang Bi symbols already agree geometrically. -/
theorem c60SixQiLabel_consecutive_iff
    (a : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : IcosahedralFace) (q : C60SixQi) :
    c60SixQiTargetGradedLabel a side grade face q =
      c60SixQiSourceGradedLabel a side grade face (c60SixQiNext q) ↔
    grade (c60SixQiHexagonBoundaryEdge face q) =
      grade (c60SixQiHexagonBoundaryEdge face (c60SixQiNext q)) := by
  have hs := c60SixQiSignedFace_consecutive side face q
  constructor
  · intro h
    exact congrArg Prod.snd h
  · intro hg
    exact Prod.ext (congrArg (wangBiOriginalFaceEncoding a) hs) hg

/-- Each of the 20 genuine hexagons' six boundary junctions
glues with the actual nontrivial F55 square generator. -/
theorem c60SixQiOriginalF55_consecutive_glues
    (a : WangBiFrame) (side : C60DartSideGauge)
    (face : IcosahedralFace) (q : C60SixQi) :
    c60SixQiTargetGradedLabel a side
      (fun _ => originalF55BraidedSquareGenerator) face q =
      c60SixQiSourceGradedLabel a side
        (fun _ => originalF55BraidedSquareGenerator)
          face (c60SixQiNext q) :=
  (c60SixQiLabel_consecutive_iff a side
    (fun _ => originalF55BraidedSquareGenerator) face q).2 rfl

/-- Each REAL hexagonal boundary 六氣 symbol transports
naturally with the old Wang Bi chart Category; the actual
F55 braided grade is left invariant. -/
theorem c60SixQiLabel_transport
    (a b : WangBiFrame) (f : a ⟶ b)
    (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0)
    (face : IcosahedralFace) (q : C60SixQi) :
    (wangBiChartArrow a b f
      (c60SixQiSourceGradedLabel a side grade face q).1,
      (c60SixQiSourceGradedLabel a side grade face q).2) =
      c60SixQiSourceGradedLabel b side grade face q := by
  exact congrArg (fun x => (x, grade (c60SixQiHexagonBoundaryEdge face q)))
    (wangBiEncodingNaturality a b f (c60SixQiSourceSignedFace side face q))

/-- Authentic 6-step unsigned F55 composite in the neutral
Gray endomorphism CATEGORY, using the actual six ordered
oriented hexagon edges. No new edge or F55 generator is invented. -/
def c60SixQiF55SixSquareList
    (a : WangBiFrame) (side : C60DartSideGauge)
    (face : IcosahedralFace) : List (GradedThreeCell 0 0) :=
  ([C60SixQi.jueyin, .shaoyin, .shaoyang,
      .taiyin, .yangming, .taiyang] : List C60SixQi).map
    (fun q => (c60SixQiSourceGradedLabel a side
      (fun _ => originalF55BraidedSquareGenerator) face q).2)

theorem c60SixQiF55SixSquareList_eq
    (a : WangBiFrame) (side : C60DartSideGauge)
    (face : IcosahedralFace) :
    c60SixQiF55SixSquareList a side face =
      [originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator] := by
  rfl

/-- Six actual original F55 exchange squares compose to an
independent (0,6) integer charge with trivial TOTAL mod-2
exchange phase, although every individual local phase is 1. -/
theorem c60SixQiF55SixSquareComposite_components
    (a : WangBiFrame) (side : C60DartSideGauge)
    (face : IcosahedralFace) :
    (c60SixQiF55SixSquareList a side face).sum.charge =
      ((0 : Int), (6 : Int)) ∧
    (c60SixQiF55SixSquareList a side face).sum.phase =
      (0 : ZMod 2) := by
  rw [c60SixQiF55SixSquareList_eq a side face]
  constructor <;> decide

/-- Pairwise F55 native 3-cell vertical composition agrees with
the grading of two consecutive REAL hexagonal incidences. -/
theorem c60SixQiF55Pair_native_comp
    (a : WangBiFrame) (side : C60DartSideGauge)
    (face : IcosahedralFace) (q : C60SixQi) :
    (c60SixQiSourceGradedLabel a side
        (fun _ => originalF55BraidedSquareGenerator) face q).2 +
    (c60SixQiSourceGradedLabel a side
        (fun _ => originalF55BraidedSquareGenerator)
          face (c60SixQiNext q)).2 =
    ((c60SixQiSourceGradedLabel a side
        (fun _ => originalF55BraidedSquareGenerator) face q).2 ≫
      (c60SixQiSourceGradedLabel a side
        (fun _ => originalF55BraidedSquareGenerator)
          face (c60SixQiNext q)).2 :
          GrayGrade.unit ⟶ GrayGrade.unit) :=
  grayNeutral_add_eq_native_comp _ _

#print axioms c60GaugeSignedFace_eq_of_flag_eq
#print axioms c60GaugeGradedLabel_eq_iff_grade_eq
#print axioms c60GaugeGradedLabel_natural
#print axioms c60GaugeGradedNatTrans
#print axioms c60GaugeTemporalRead_natural
#print axioms c60GaugeTemporalRead_glues
#print axioms c60ShengConsecutive_actualFlag
#print axioms c60ShengConsecutive_grade_glue_iff
#print axioms c60ShengConsecutive_originalF55_glues
#print axioms c60ShengConsecutive_meaning_glues
#print axioms c60ShengWangBiF55SquareList_eq_original
#print axioms c60ShengWangBiF55_native_collaring
#print axioms c60ShengWangBiF55_collar_components
#print axioms c60SixQiOrientedEdge_underlying
#print axioms c60SixQiOriented_consecutive
#print axioms c60SixQiSourceFlag_incident
#print axioms c60SixQiTargetFlag_consecutive
#print axioms c60SixQiTargetFlag_incident
#print axioms c60SixQiSignedFace_consecutive
#print axioms c60SixQiLabel_consecutive_iff
#print axioms c60SixQiOriginalF55_consecutive_glues
#print axioms c60SixQiLabel_transport
#print axioms c60SixQiF55SixSquareList_eq
#print axioms c60SixQiF55SixSquareComposite_components
#print axioms c60SixQiF55Pair_native_comp

end
end KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
