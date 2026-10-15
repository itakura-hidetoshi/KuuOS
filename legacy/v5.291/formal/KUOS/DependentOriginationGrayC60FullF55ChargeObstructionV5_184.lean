import KUOS.DependentOriginationGrayC60TypedF55LiftV5_183

namespace KUOS.DependentOriginationGrayC60FullF55ChargeObstructionV5_184

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
open KUOS.DependentOriginationGrayC60F55SharpRepairV5_168
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
open KUOS.DependentOriginationGrayC60BraidedFlatRepairV5_181
open KUOS.DependentOriginationGrayC60BraidedSharpSupportV5_182
open KUOS.DependentOriginationGrayC60TypedF55LiftV5_183
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F36 / v5.184 — NEW full nine-constructor original F55 source obstruction

F59-F35 proved a conditional lifting iff in terms of exact original
F58 charge realizability. This theorem unit derives a NONTAUTOLOGICAL
necessary condition on the original full nine-constructor source.

The FIRST generator charge (the genuine F55 pentagon count) of EVERY
original typed PresentedCell is determined completely by the
INTEGER difference of its source and target original F54 rotation
route lengths. Identity, pentagon (three rotations vs two), square
(two vs two), inverse, vertical composite and all FOUR contextual /
pre-post whiskerings are proved individually. No raw source cells
are quotient-identified, and no full ambient Gray 3-functor assumed.

Consequently any ORIGINAL F55 cell between the fixed genuine
left-first/right-first disjoint-square routes has first charge ZERO,
even if arbitrary pentagon, context and whiskering constructors
are allowed. This is stronger than the earlier square-only rigidity.

We then construct a TRUE C60 60-vertex potential: it adds precisely
one original F55 phase-compatible pentagon native generator at the
target dart of the original north-spoke zero cross edge. Its genuine
linear vertex coboundary added to the already-proved 27-edge
canonical repaired F55 field has ZERO oriented curvature on EACH
original 12 pentagon + 20 hexagon, and EACH original 90-edge
Gray 3-cell is in the source-compatible phase-locked subgroup.

But the ACTUAL north-spoke cross edge has FIRST charge ONE, so this
flat phase-locked field cannot lift to ANY of the FULL NINE original
F55 PresentedCell constructors between the same fixed genuine
left/right F54 square routes. This exhibits a concrete residual
TYPE-SENSITIVE F58 charge obstruction, independent of C60 H¹
flatness and the separate phase defect.

We also express the example as a correction of the original
independently braided B_ab field and carry it into the true
Mathlib Wang Bi 360-corner atlas; semantic readings, the old
Stage-II omega and a full Gray 3-functor remain distinct.
-/

/-! ## I. Universal full-nine-source F55 pentagon length charge -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section AllNineConstructors
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- The first integral F58 generator coordinate of an original
proof-relevant F55 cell is a BOUNDARY-COMPUTABLE signed rotation
count, including when the two original depth axes require casts. -/
theorem c60F36FullNinePentagonCharge_eq_rotationDifference
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (c60F55SourceNative cell).charge.1 =
      (r.rotationCount : ℤ) - (s.rotationCount : ℤ) := by
  induction cell with
  | ident route =>
      change (0 : ℤ) = (route.rotationCount : ℤ) - (route.rotationCount : ℤ)
      omega
  | pentagon t₁ t₂ t₃ t₄ =>
      change (1 : ℤ) =
        ((OriginalF45BracketTree.DepthRotationRoute.pentagonLong
          t₁ t₂ t₃ t₄).rotationCount : ℤ) -
        ((OriginalF45BracketTree.DepthRotationRoute.pentagonShort
          t₁ t₂ t₃ t₄).rotationCount : ℤ)
      rw [OriginalF45BracketTree.DepthRotationRoute.pentagonLong_rotationCount,
        OriginalF45BracketTree.DepthRotationRoute.pentagonShort_rotationCount]
      norm_num
  | disjointSquare left right =>
      change (0 : ℤ) =
        ((OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst
          left right).rotationCount : ℤ) -
        ((OriginalF45BracketTree.DepthRotationRoute.squareRightFirst
          left right).rotationCount : ℤ)
      rw [OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst_count,
        OriginalF45BracketTree.DepthRotationRoute.squareRightFirst_count]
      norm_num
  | symm cell ih =>
      change -(c60F55SourceNative cell).charge.1 =
        _ - _
      rw [ih]
      omega
  | trans left right ihLeft ihRight =>
      change (c60F55SourceNative left).charge.1 +
          (c60F55SourceNative right).charge.1 = _ - _
      rw [ihLeft, ihRight]
      omega
  | leftContext cell later ih =>
      change (c60F55SourceNative cell).charge.1 =
        _ - _
      simpa only [OriginalF45BracketTree.DepthRotationRoute.rotationCount] using ih
  | rightContext earlier cell ih =>
      change (c60F55SourceNative cell).charge.1 =
        _ - _
      simpa only [OriginalF45BracketTree.DepthRotationRoute.rotationCount] using ih
  | precompose priorRoute cell ih =>
      change (c60F55SourceNative cell).charge.1 =
        _ - _
      simp only [OriginalF45BracketTree.DepthRotationRoute.rotationCount,
        Nat.cast_add] at ih ⊢
      rw [ih]
      omega
  | postcompose cell suffix ih =>
      change (c60F55SourceNative cell).charge.1 =
        _ - _
      simp only [OriginalF45BracketTree.DepthRotationRoute.rotationCount,
        Nat.cast_add] at ih ⊢
      rw [ih]
      omega

/-- The pentagon-charge obstruction applies to every target cell
which is the genuine interpretation of an unrestricted original
F55 PresentedCell with the given EXACT indexed original routes. -/
theorem c60F36TypedSourceImage_requires_pentagonDifference
    (g : GradedThreeCell 0 0)
    (hlift : ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      c60F55SourceNative cell = g) :
    g.charge.1 = (r.rotationCount : ℤ) - (s.rotationCount : ℤ) := by
  obtain ⟨cell, hcell⟩ := hlift
  rw [← hcell]
  exact c60F36FullNinePentagonCharge_eq_rotationDifference cell

end AllNineConstructors

/-! ## II. Entire nine-constructor obstruction at genuine square routes -/

section AllNineFixedSquareRoutes
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

/-- Even with ALL original nine F55 constructors (including genuine
pentagons and four whiskerings), the independent pentagon charge
of a 3-cell between the TWO EXACT original F54 square orders is ZERO.
This is a source-dependent, NOT target-phase-only, theorem. -/
theorem c60F36AnyFullNineFixedSquareSource_pentagonCharge_zero
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)) :
    (c60F55SourceNative cell).charge.1 = 0 := by
  rw [c60F36FullNinePentagonCharge_eq_rotationDifference cell,
    OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst_count,
    OriginalF45BracketTree.DepthRotationRoute.squareRightFirst_count]
  norm_num

end AllNineFixedSquareRoutes

/-! ## III. A real C60 flat and phase-locked counterexample -/

/-- An ACTUAL dart of the original north-spoke zero cross edge. -/
def c60F36DistinguishedDart : IcosahedralDart :=
  .second (.northSpoke 0)

/-- An original target F55 pentagon-generator degree of freedom
at ONE of the existing sixty truncated-icosahedron vertices. -/
def c60F36PentagonVertexValue (d : IcosahedralDart) :
    GradedThreeCell 0 0 :=
  if d = c60F36DistinguishedDart then
    c60F55PentagonNativeGenerator
  else 0

/-- Extend actual C60 pointwise vertex values as a signed
integer-linear 0-cochain, not a new edge or face prescription. -/
def c60F36PentagonVertexGauge :
    C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  Finsupp.linearCombination ℤ c60F36PentagonVertexValue

/-- The fully repaired and independently pentagon-shifted 1-cochain:
the new term is an EXACT original vertex coboundary, with NO
braid-parity projection and no invented geometric cell. -/
def c60F36PentagonTwistCochain :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  c60F34RepairedF55EdgeCochain +
    c60F36PentagonVertexGauge.comp c60IntegralBoundaryOne

def c60F36PentagonTwistEdge
    (e : TruncatedIcosahedralEdge) : GradedThreeCell 0 0 :=
  c60F36PentagonTwistCochain (Finsupp.single e (1 : ℤ))

/-- The REAL integral endpoint boundary of each physical edge
produces exactly one difference of the two old sixty-vertex values. -/
theorem c60F36PentagonVertexGauge_edgeBoundary
    (e : TruncatedIcosahedralEdge) :
    c60F36PentagonVertexGauge
      (c60IntegralBoundaryOne (Finsupp.single e (1 : ℤ))) =
      c60F36PentagonVertexValue (truncatedIcosahedralEdgeEndpoints e).2 -
      c60F36PentagonVertexValue (truncatedIcosahedralEdgeEndpoints e).1 := by
  rw [c60IntegralBoundaryOne_singleEdge]
  simp [c60IntegralEdgeBoundaryChain, c60F36PentagonVertexGauge]

/-- The new target cochain changes the true 27-edge repaired F55
value by the real signed boundary of the new vertex potential. -/
theorem c60F36PentagonTwistEdge_formula
    (e : TruncatedIcosahedralEdge) :
    c60F36PentagonTwistEdge e =
      c60WangBiRepairedEdgeGrade e +
      (c60F36PentagonVertexValue (truncatedIcosahedralEdgeEndpoints e).2 -
       c60F36PentagonVertexValue (truncatedIcosahedralEdgeEndpoints e).1) := by
  change (c60F34RepairedF55EdgeCochain +
      c60F36PentagonVertexGauge.comp c60IntegralBoundaryOne)
      (Finsupp.single e (1 : ℤ)) = _
  rw [LinearMap.add_apply, LinearMap.comp_apply,
    c60F36PentagonVertexGauge_edgeBoundary]
  simp [c60F34RepairedF55EdgeCochain,
    c60F18GrayEdgeCochain]

/-- This is an EXACT C60 vertex descent, so the new source-incompatible
first charge is NOT a nonflatness artifact. -/
theorem c60F36PentagonTwist_exact_vertexDescent :
    c60F36PentagonTwistCochain =
      (c60F19TreeVertexGauge + c60F36PentagonVertexGauge).comp
        c60IntegralBoundaryOne := by
  apply LinearMap.ext
  intro x
  have hr := LinearMap.congr_fun c60WangBiRepairedGrade_exact_treeDescent x
  change c60F34RepairedF55EdgeCochain x =
    c60F19TreeVertexGauge (c60IntegralBoundaryOne x) at hr
  change c60F34RepairedF55EdgeCochain x +
      c60F36PentagonVertexGauge (c60IntegralBoundaryOne x) =
    (c60F19TreeVertexGauge + c60F36PentagonVertexGauge)
      (c60IntegralBoundaryOne x)
  rw [hr, LinearMap.add_apply]

/-- Flatness of the new physical integer-linear cochain on every
actual C60 pentagon and hexagon follows by REAL d₁ ∘ d₂ = 0. -/
theorem c60F36PentagonTwistCochain_all32_flat :
    c60F36PentagonTwistCochain.comp c60IntegralBoundaryTwo = 0 := by
  rw [c60F36PentagonTwist_exact_vertexDescent]
  exact c60F18Coboundary_squared_zero
    (c60F19TreeVertexGauge + c60F36PentagonVertexGauge)

/-- Basis reconstruction: original actual 90 edge generators retain
all three of the independent Gray 3-cell components. -/
theorem c60F36PentagonTwistGrade_realizes_cochain :
    c60F18GrayEdgeCochain c60F36PentagonTwistEdge =
      c60F36PentagonTwistCochain :=
  c60F33ReconstructActualEdgeCochain _

theorem c60F36PentagonTwist_all32_signedFaces_flat
    (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace c60F36PentagonTwistEdge face = 0 := by
  change c60F18SignedGrayFacePasting c60F36PentagonTwistEdge face = 0
  rw [c60F18SignedGrayFacePasting_eq,
    c60F36PentagonTwistGrade_realizes_cochain]
  have h := LinearMap.congr_fun c60F36PentagonTwistCochain_all32_flat
    (Finsupp.single face (1 : ℤ))
  change c60F36PentagonTwistCochain
    (c60IntegralBoundaryTwo (Finsupp.single face (1 : ℤ))) = 0 at h
  rw [c60IntegralBoundaryTwo_singleFace] at h
  exact h

/-- Every one of the original sixty C60 vertex values satisfies
the exact F55 phase/second-charge law. -/
theorem c60F36PentagonVertexValue_locked (d : IcosahedralDart) :
    c60F36PentagonVertexValue d ∈ c60F55PhaseLocked := by
  unfold c60F36PentagonVertexValue
  split_ifs
  · exact c60F55PentagonNativeGenerator_mem
  · exact c60F55PhaseLocked.zero_mem

/-- The entire new 90-edge flat physical field STILL retains
the target necessary original F55 phase-locked membership:
this condition does NOT imply actual typed-source lifting. -/
theorem c60F36PentagonTwist_all90_phaseLocked
    (e : TruncatedIcosahedralEdge) :
    c60F36PentagonTwistEdge e ∈ c60F55PhaseLocked := by
  rw [c60F36PentagonTwistEdge_formula]
  exact c60F55PhaseLocked.add_mem (c60F55RepairedGrade_mem e)
    (c60F55PhaseLocked.sub_mem
      (c60F36PentagonVertexValue_locked _)
      (c60F36PentagonVertexValue_locked _))

/-- A direct original EDGE-INCIDENCE calculation: the chosen north
cross edge has target value +pentagon and source value zero. -/
theorem c60F36NorthCrossGaugeValue :
    c60F36PentagonVertexValue
      (truncatedIcosahedralEdgeEndpoints (.cross (.northSpoke 0))).2 -
    c60F36PentagonVertexValue
      (truncatedIcosahedralEdgeEndpoints (.cross (.northSpoke 0))).1 =
      c60F55PentagonNativeGenerator := by
  simp [truncatedIcosahedralEdgeEndpoints,
    c60F36PentagonVertexValue, c60F36DistinguishedDart]

/-- The original physical north-spoke zero edge has INTRINSIC
pentagon charge +1 after the flat vertex twist. Its underlying
27-edge corrected F55 square label has first integer charge 0. -/
theorem c60F36NorthCrossPentagonCharge_one :
    (c60F36PentagonTwistEdge (.cross (.northSpoke 0))).charge.1 =
      (1 : ℤ) := by
  rw [c60F36PentagonTwistEdge_formula, c60F36NorthCrossGaugeValue,
    c60WangBiRepairedEdgeGrade_preserved _ (by decide)]
  rw [grayNeutral_add_charge]
  simp [c60F55PentagonNativeGenerator,
    originalF55BraidedSquareGenerator]

/-- A SINGLE original north cross edge rules out lifting to ANY
original full nine-constructor F55 PresentedCell between the
same fixed original F54 disjoint left/right square routes. -/
theorem c60F36NorthCross_noFullNineF55FixedSquareLift
    {a b : D} {x y : E}
    {n₁ n₂ m₁ m₂ : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
    {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
    (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F55SourceNative cell =
        c60F36PentagonTwistEdge (.cross (.northSpoke 0)) := by
  rintro ⟨cell, hcell⟩
  have hz := c60F36AnyFullNineFixedSquareSource_pentagonCharge_zero
    t₁ t₂ left right cell
  have hone := c60F36NorthCrossPentagonCharge_one
  have hc := congrArg
    (fun g : GradedThreeCell 0 0 => g.charge.1) hcell
  change (c60F55SourceNative cell).charge.1 =
    (c60F36PentagonTwistEdge (.cross (.northSpoke 0))).charge.1 at hc
  rw [hz, hone] at hc
  exact (by decide : (0 : ℤ) ≠ 1) hc

/-- Strong, full NINE-CONSTRUCTOR physical C60 counterexample:
all 32 actual faces are flat and ALL 90 target labels are
phase-locked, yet NO original F55 source-cell family for the fixed
genuine square routes exists. This no-lift theorem is NOT restricted
to the old square-only word fragment. -/
theorem c60F36FlatLocked_but_noFullNineFixedSquareSourceAtlas
    {a b : D} {x y : E}
    {n₁ n₂ m₁ m₂ : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
    {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
    (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter) :
    (∀ face : TruncatedIcosahedralSeedFace,
      c60WangBiSignedGrayFace c60F36PentagonTwistEdge face = 0) ∧
    (∀ e : TruncatedIcosahedralEdge,
      c60F36PentagonTwistEdge e ∈ c60F55PhaseLocked) ∧
    ¬ ∃ cells : TruncatedIcosahedralEdge →
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell
          (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
          (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      ∀ e : TruncatedIcosahedralEdge,
        c60F55SourceNative (cells e) = c60F36PentagonTwistEdge e := by
  refine ⟨c60F36PentagonTwist_all32_signedFaces_flat,
    c60F36PentagonTwist_all90_phaseLocked, ?_⟩
  rintro ⟨cells, hc⟩
  exact (c60F36NorthCross_noFullNineF55FixedSquareLift
    t₁ t₂ left right) ⟨cells (.cross (.northSpoke 0)),
      hc (.cross (.northSpoke 0))⟩

/-! ## IV. Source-image membership on every real C60 edge -/

section ArbitraryOriginalTypedRoutes
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}

/- An independently selected original typed F54 route pair on each C60 edge. -/
variable
  (r s : TruncatedIcosahedralEdge →
    OriginalF45BracketTree.DepthRotationRoute first last)

/-- ALL-NINE simultaneous original source lifting holds iff
EVERY physical edge has the genuine phase lock and a source
F58 charge witness with its exact local original typed routes. -/
theorem c60F36All90TypedSourceLift_iff_phaseAndOriginalF58
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∃ cells : ∀ e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
      ∀ e : TruncatedIcosahedralEdge,
        c60F55SourceNative (cells e) = grade e) ↔
      (∀ e : TruncatedIcosahedralEdge, grade e ∈ c60F55PhaseLocked) ∧
      (∀ e : TruncatedIcosahedralEdge,
        ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
          cell.interpret
            (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
              (D := D) (E := E)) = (grade e).charge) := by
  constructor
  · rintro ⟨cells, hcells⟩
    constructor
    · intro e
      have he := (c60F35TypedSourceLift_iff_phaseAndF58Realization
        (r := r e) (s := s e) (grade e)).mp ⟨cells e, hcells e⟩
      exact he.1
    · intro e
      exact ((c60F35TypedSourceLift_iff_phaseAndF58Realization
        (r := r e) (s := s e) (grade e)).mp ⟨cells e, hcells e⟩).2
  · rintro ⟨hlocked, hcharge⟩
    classical
    have h : ∀ e : TruncatedIcosahedralEdge,
        ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
          c60F55SourceNative cell = grade e := by
      intro e
      exact (c60F35TypedSourceLift_iff_phaseAndF58Realization
        (r := r e) (s := s e) (grade e)).mpr
          ⟨hlocked e, hcharge e⟩
    choose cells hcells using h
    exact ⟨cells, hcells⟩

/-- Full source-image lifting in genuine Wang Bi Mathlib natural
transformations at ALL 360 original C60 local corners.
The theorem uses grade-faithfulness; it does NOT equate different
raw PresentedCell witnesses with equal Gray interpretations. -/
theorem c60F36WangBiAll90TypedLift_iff_phaseAndOriginalF58
    (frame : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∃ cells : ∀ e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
      c60WangBiGlobalGradedAtlas side
        (fun e => c60F55SourceNative (cells e)) =
          c60WangBiGlobalGradedAtlas side grade) ↔
      (∀ e : TruncatedIcosahedralEdge, grade e ∈ c60F55PhaseLocked) ∧
      (∀ e : TruncatedIcosahedralEdge,
        ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
          cell.interpret
            (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
              (D := D) (E := E)) = (grade e).charge) := by
  rw [← c60F36All90TypedSourceLift_iff_phaseAndOriginalF58 r s grade]
  constructor
  · rintro ⟨cells, hAtlas⟩
    refine ⟨cells, ?_⟩
    have h := c60WangBiGlobalGradedAtlas_faithful frame side hAtlas
    exact congrFun h
  · rintro ⟨cells, hGrade⟩
    refine ⟨cells, ?_⟩
    have heq :
        (fun e => c60F55SourceNative (cells e)) = grade := by
      funext e
      exact hGrade e
    rw [heq]

/-- The precise remaining ORIGINAL source obstruction for
simultaneous C60 curvature flatness and full nine-constructor
typed lifting: real C60 affine correction + phase defect
cancellation + a genuine F58 source-charge witness at EACH
actual physical edge, with its original F54 endpoints. -/
theorem c60F36All90BraidedFlatTypedLift_iff
    (α β : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    ((∀ face : TruncatedIcosahedralSeedFace,
        c60WangBiSignedGrayFace (c60F33CorrectedEdgeGrade α β k) face = 0) ∧
     (∃ cells : ∀ e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
        ∀ e : TruncatedIcosahedralEdge,
          c60F55SourceNative (cells e) =
            c60F33CorrectedEdgeGrade α β k e)) ↔
      ((∃ phi : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
          k = phi.comp c60IntegralBoundaryOne -
            c60F33BraidedEdgeCochain α β) ∧
       (∀ e : TruncatedIcosahedralEdge,
          c60F29PhaseDefect (k (Finsupp.single e (1 : ℤ))) = -(α * β)) ∧
       (∀ e : TruncatedIcosahedralEdge,
        ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
          cell.interpret
            (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
              (D := D) (E := E)) =
                (c60F33CorrectedEdgeGrade α β k e).charge)) := by
  constructor
  · rintro ⟨hfaces, hlift⟩
    obtain ⟨hlocked, hcharge⟩ :=
      (c60F36All90TypedSourceLift_iff_phaseAndOriginalF58 r s
        (c60F33CorrectedEdgeGrade α β k)).mp hlift
    have h := (c60F34FlatAndSourcePhaseLocked_iff α β k).mp
      ⟨hfaces, hlocked⟩
    exact ⟨h.1, h.2, hcharge⟩
  · rintro ⟨hexact, hdefect, hcharge⟩
    have h := (c60F34FlatAndSourcePhaseLocked_iff α β k).mpr
      ⟨hexact, hdefect⟩
    exact ⟨h.1,
      (c60F36All90TypedSourceLift_iff_phaseAndOriginalF58 r s
        (c60F33CorrectedEdgeGrade α β k)).mpr ⟨h.2, hcharge⟩⟩

end ArbitraryOriginalTypedRoutes

#print axioms c60F36FullNinePentagonCharge_eq_rotationDifference
#print axioms c60F36TypedSourceImage_requires_pentagonDifference
#print axioms c60F36AnyFullNineFixedSquareSource_pentagonCharge_zero
#print axioms c60F36PentagonVertexGauge_edgeBoundary
#print axioms c60F36PentagonTwistEdge_formula
#print axioms c60F36PentagonTwist_exact_vertexDescent
#print axioms c60F36PentagonTwistCochain_all32_flat
#print axioms c60F36PentagonTwistGrade_realizes_cochain
#print axioms c60F36PentagonTwist_all32_signedFaces_flat
#print axioms c60F36PentagonVertexValue_locked
#print axioms c60F36PentagonTwist_all90_phaseLocked
#print axioms c60F36NorthCrossGaugeValue
#print axioms c60F36NorthCrossPentagonCharge_one
#print axioms c60F36NorthCross_noFullNineF55FixedSquareLift
#print axioms c60F36FlatLocked_but_noFullNineFixedSquareSourceAtlas
#print axioms c60F36All90TypedSourceLift_iff_phaseAndOriginalF58
#print axioms c60F36WangBiAll90TypedLift_iff_phaseAndOriginalF58
#print axioms c60F36All90BraidedFlatTypedLift_iff

end
end KUOS.DependentOriginationGrayC60FullF55ChargeObstructionV5_184
