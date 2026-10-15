import KUOS.DependentOriginationGrayC60BraidedSharpSupportV5_182
import KUOS.DependentOriginationGrayC60F55SourceSquareRigidityV5_168

namespace KUOS.DependentOriginationGrayC60TypedF55LiftV5_183

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
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
open KUOS.DependentOriginationGrayC60F55SharpRepairV5_168
open KUOS.DependentOriginationGrayC60F55SourceSquareRigidityV5_168
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60BraidedFlatRepairV5_181
open KUOS.DependentOriginationGrayC60BraidedSharpSupportV5_182
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
# F59-F35 / v5.183 — precisely typed F55 lifting from C60 Gray target data

F59-F34 showed that making all 90 edges compatible with the original
F55 phase law is NOT the same as 24-edge target Gray flat repair.

We now distinguish two actual, genuinely TYPED source-lift problems.

(A) For arbitrary original F55 PresentedCells between any FIXED
parallel original F54 routes r,s, a Gray 3-cell g lifts iff:
  (i) its exchange phase is F55-compatible; AND
  (ii) its genuine F58 integer charge is realized by an original
       PresentedCell having EXACTLY those typed endpoints.
This is an honest iff theorem; it does not assume (ii) from (i).

(B) For the ORIGINAL particular disjoint-square left-first and
right-first routes, consider the complete square-only grammar
(ident, square, inverse, trans) already embedded into the original
proof-relevant F55 syntax by F59-F20. Every source word from left
to right evaluates to the SAME square generator, so an assignment
of such words to ALL ORIGINAL ninety edges realizes an edge field
iff that field is UNIFORMLY the original F55 generator.

Applied to arbitrary Gray cochain corrections of B_ab, there is
EXACTLY ONE resulting correction allowing this fixed-square source
fragment: K_fixed = F55-original - B_ab. This correction is NOT
locally flat (already at an actual C60 north pentagon), even though
its full Gray output is source-typed. Thus no correction can be both
globally flat and liftable to this fixed-boundary square-word class.

Conversely F59-F34's canonical flat, phase-compatible repair is
NOT liftable to these fixed source routes. We also exhibit the
actual north pentagon closing physical edge as a single explicit
locked-but-unliftable counterexample. Full unrestricted
PresentedCell source-image existence remains indexed by F58 charge
realizability; higher contextual/pentagon source constructions are
not falsely ruled out. Stage-II omega and historic semantics are
not identified.
-/

/-! ## I. Arbitrary original fully typed F55 PresentedCell targets -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GeneralTypedRoutes
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- ACTUAL F55 type-sensitive lifting: original nine-constructor
source syntax realizes a neutral Gray 3-cell at the exact fixed
F54 endpoints if and only if its phase is compatible AND the same
integer generator charge has a genuine source witness.

The second clause is not erased, inferred, or replaced by a
numerical existence postulate. -/
theorem c60F35TypedSourceLift_iff_phaseAndF58Realization
    (g : GradedThreeCell 0 0) :
    (∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
        c60F55SourceNative cell = g) ↔
      g ∈ c60F55PhaseLocked ∧
      ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
        cell.interpret
          (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
            (D := D) (E := E)) = g.charge := by
  constructor
  · rintro ⟨cell, hcell⟩
    have hmem := c60F55SourceNative_mem cell
    have hc :=
      KUOS.DependentOriginationGrayF55PhaseRealizationV5_156.OriginalF45BracketTree.DepthRotationRoute.PresentedCell.braidedPhase_charge_eq_F58 cell
    refine ⟨?_, ⟨cell, ?_⟩⟩
    · rw [← hcell]
      exact hmem
    · calc
        cell.interpret
          (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
            (D := D) (E := E)) =
          (c60F55SourceNative cell).charge := hc.symm
        _ = g.charge := congrArg GradedThreeCell.charge hcell
  · rintro ⟨hmem, ⟨cell, hcharge⟩⟩
    have hc : (c60F55SourceNative cell).charge = g.charge :=
      (KUOS.DependentOriginationGrayF55PhaseRealizationV5_156.OriginalF45BracketTree.DepthRotationRoute.PresentedCell.braidedPhase_charge_eq_F58 cell).trans hcharge
    have hsource := c60F55SourceNative_mem cell
    change (c60F55SourceNative cell).phase =
      ((c60F55SourceNative cell).charge.2 : ZMod 2) at hsource
    change g.phase = (g.charge.2 : ZMod 2) at hmem
    refine ⟨cell, GradedThreeCell.ext hc ?_⟩
    calc
      (c60F55SourceNative cell).phase =
          ((c60F55SourceNative cell).charge.2 : ZMod 2) := hsource
      _ = (g.charge.2 : ZMod 2) := by rw [hc]
      _ = g.phase := hmem.symm

end GeneralTypedRoutes

/-! ## II. Original fixed-boundary F55 square-source fragment -/

/-- The sole source-field correction that makes all corrected
C60 Gray labels equal to the ACTUAL ORIGINAL (0,1;1) F55
disjoint-square value; it is NOT the parity projection functor. -/
def c60F35FixedSquareCorrection (a b : ZMod 2) :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  c60F19OriginalF55EdgeCochain - c60F33BraidedEdgeCochain a b

theorem c60F35FixedSquareCorrection_returns_original (a b : ZMod 2) :
    c60F33BraidedEdgeCochain a b + c60F35FixedSquareCorrection a b =
      c60F19OriginalF55EdgeCochain := by
  unfold c60F35FixedSquareCorrection
  abel

/-- The only correction compatible with the actual original
fixed square-word grammar is necessarily NONFLAT on C60:
the old signed physical north-pentagon F55 curvature returns. -/
theorem c60F35FixedSquareCorrection_notFlat (a b : ZMod 2) :
    (c60F33BraidedEdgeCochain a b +
      c60F35FixedSquareCorrection a b).comp
        c60IntegralBoundaryTwo ≠ 0 := by
  rw [c60F35FixedSquareCorrection_returns_original]
  intro hflat
  obtain ⟨phi, hphi⟩ :=
    (c60F18ClosedEdgeIffVertexPotential
      c60F19OriginalF55EdgeCochain).mp hflat
  exact c60F19OriginalF55EdgeCochain_no_vertexGauge ⟨phi, hphi⟩

/-- The original square-only fixed-route value is phase-locked,
but this source property never forces flatness of its C60 atlas. -/
theorem c60F35FixedSquareCorrection_all90_locked (a b : ZMod 2)
    (e : TruncatedIcosahedralEdge) :
    c60F33CorrectedEdgeGrade a b (c60F35FixedSquareCorrection a b) e ∈
      c60F55PhaseLocked := by
  have hvalue :
      c60F33CorrectedEdgeGrade a b
        (c60F35FixedSquareCorrection a b) e =
        originalF55BraidedSquareGenerator := by
    change (c60F33BraidedEdgeCochain a b +
      c60F35FixedSquareCorrection a b)
        (Finsupp.single e (1 : ℤ)) = _
    rw [c60F35FixedSquareCorrection_returns_original]
    exact c60F20OriginalF55SingleEdge e
  rw [hvalue]
  exact c60F55SquareNativeGenerator_mem

/-- In odd/odd braiding the unique uniform source-square correction
really modifies ALL 90 physical edges; source-compatibility does
NOT reduce this number to the 24 used by the flat target repair. -/
theorem c60F35OddOddFixedSquareCorrection_support90 :
    (c60F34CorrectionSupport (c60F35FixedSquareCorrection 1 1)).card =
      90 := by
  apply c60F34OddOddLockedCorrectionSupport_card_eq90
  exact c60F35FixedSquareCorrection_all90_locked 1 1

section FixedSquareRoutes
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

/-- Source-classified Gray target of an ACTUAL original typed F55
square-only word, with its exact unchanged F54 endpoints. -/
def c60F35FixedSquareWordGrade (word : C60F55SquareWord false true) :
    GradedThreeCell 0 0 :=
  (word.toOriginalF55 t₁ t₂ left right).interpret
    (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.braidedPhase
      (D := D) (E := E))

theorem c60F35FixedSquareWordGrade_eq_original
    (word : C60F55SquareWord false true) :
    c60F35FixedSquareWordGrade t₁ t₂ left right word =
      originalF55BraidedSquareGenerator :=
  word.fixedBoundary_braidedRigidity t₁ t₂ left right

/-- A full 90-edge field has a bona fide ORIGINAL F55
fixed-left-right-square WORD at EVERY real physical edge iff
every one of its labels is the unmodified native square generator.
Here WORD is a genuinely typed original PresentedCell fragment,
not a free target coefficient added by hand. -/
theorem c60F35FixedSquareWordAtlasLift_iff_uniform
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∃ words : TruncatedIcosahedralEdge → C60F55SquareWord false true,
      ∀ e : TruncatedIcosahedralEdge,
        grade e = c60F35FixedSquareWordGrade t₁ t₂ left right (words e)) ↔
      grade = c60F19UniformF55EdgeLabels := by
  constructor
  · rintro ⟨words, hwords⟩
    funext e
    rw [hwords e, c60F35FixedSquareWordGrade_eq_original]
    rfl
  · intro hgrade
    refine ⟨fun _ => .square, ?_⟩
    intro e
    rw [hgrade]
    exact (c60F35FixedSquareWordGrade_eq_original t₁ t₂ left right
      (C60F55SquareWord.square)).symm

/-- EXACT necessary/sufficient classification of all C60 Gray
cochain corrections admitting arbitrary original fixed-route
square-only F55 words on all 90 actual edges: there is precisely
one such correction, K_fixed=Original_F55-B_ab. -/
theorem c60F35CorrectedAtlas_hasFixedSource_iff_correction
    (α β : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    (∃ words : TruncatedIcosahedralEdge → C60F55SquareWord false true,
      ∀ e : TruncatedIcosahedralEdge,
        c60F33CorrectedEdgeGrade α β k e =
          c60F35FixedSquareWordGrade t₁ t₂ left right (words e)) ↔
      k = c60F35FixedSquareCorrection α β := by
  rw [c60F35FixedSquareWordAtlasLift_iff_uniform t₁ t₂ left right]
  constructor
  · intro hgrade
    have hco :
        c60F33BraidedEdgeCochain α β + k =
          c60F19OriginalF55EdgeCochain := by
      calc
        c60F33BraidedEdgeCochain α β + k =
          c60F18GrayEdgeCochain (c60F33CorrectedEdgeGrade α β k) :=
            (c60F33CorrectedGrade_realizes_cochain α β k).symm
        _ = c60F18GrayEdgeCochain c60F19UniformF55EdgeLabels := by
          rw [hgrade]
        _ = c60F19OriginalF55EdgeCochain := rfl
    unfold c60F35FixedSquareCorrection
    calc
      k = (c60F33BraidedEdgeCochain α β + k) -
          c60F33BraidedEdgeCochain α β := by abel
      _ = c60F19OriginalF55EdgeCochain -
          c60F33BraidedEdgeCochain α β := by rw [hco]
  · intro hk
    rw [hk]
    funext e
    change (c60F33BraidedEdgeCochain α β +
      c60F35FixedSquareCorrection α β)
        (Finsupp.single e (1 : ℤ)) =
      c60F19UniformF55EdgeLabels e
    rw [c60F35FixedSquareCorrection_returns_original]
    exact c60F20OriginalF55SingleEdge e

/-- The actual F55 fixed-square-word fragment can NEVER realize
a corrected field that is flat on all original twelve pentagons
and twenty hexagons, even if its independent Gray target
correction is arbitrary and all charge/phase data are retained. -/
theorem c60F35NoFlatFixedSquareSourceLift (α β : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0)
    (hflat : ∀ face : TruncatedIcosahedralSeedFace,
      c60WangBiSignedGrayFace (c60F33CorrectedEdgeGrade α β k) face = 0) :
    ¬ ∃ words : TruncatedIcosahedralEdge → C60F55SquareWord false true,
      ∀ e : TruncatedIcosahedralEdge,
        c60F33CorrectedEdgeGrade α β k e =
          c60F35FixedSquareWordGrade t₁ t₂ left right (words e) := by
  intro hwords
  have hk := (c60F35CorrectedAtlas_hasFixedSource_iff_correction
    t₁ t₂ left right α β k).mp hwords
  have hco := (c60F33CompleteFlatCorrectionClassification α β k).mpr
    ((c60F33All32Flat_iff_completeCorrection α β k).mp hflat)
  rw [hk] at hco
  exact c60F35FixedSquareCorrection_notFlat α β hco

/-- The F59-F34 constructed genuinely flat and phase-locked Gray
C60 atlas still has NO uniform lift to the original fixed-route
typed source square fragment, for ANY braided pair α,β. -/
theorem c60F35FlatLockedButNoFixedSquareSourceLift
    (α β : ZMod 2) :
    (∀ face : TruncatedIcosahedralSeedFace,
      c60WangBiSignedGrayFace
        (c60F33CorrectedEdgeGrade α β
          (c60F34PhaseCompatibleCorrection α β)) face = 0) ∧
    (∀ e : TruncatedIcosahedralEdge,
      c60F33CorrectedEdgeGrade α β
        (c60F34PhaseCompatibleCorrection α β) e ∈
          c60F55PhaseLocked) ∧
    ¬ ∃ words : TruncatedIcosahedralEdge → C60F55SquareWord false true,
      ∀ e : TruncatedIcosahedralEdge,
        c60F33CorrectedEdgeGrade α β
          (c60F34PhaseCompatibleCorrection α β) e =
          c60F35FixedSquareWordGrade t₁ t₂ left right (words e) := by
  have h := c60F34PhaseCompatibleCorrection_flatAndLocked α β
  exact ⟨h.1, h.2, c60F35NoFlatFixedSquareSourceLift t₁ t₂
    left right α β (c60F34PhaseCompatibleCorrection α β) h.1⟩

/-- Explicit LOCAL source-image obstruction: the original north
pentagon closing edge is phase-locked after genuine target repair,
but can NOT be represented by any original typed square word
between the SAME pair of F54 left/right routes. -/
theorem c60F35NorthClosingEdge_locked_but_notFixedSquareLift :
    c60WangBiRepairedEdgeGrade (.around ⟨.north, .s4⟩) ∈
        c60F55PhaseLocked ∧
    ∀ word : C60F55SquareWord false true,
      c60WangBiRepairedEdgeGrade (.around ⟨.north, .s4⟩) ≠
        c60F35FixedSquareWordGrade t₁ t₂ left right word := by
  refine ⟨c60F55RepairedGrade_mem _, ?_⟩
  intro word hword
  have hchanged :
      c60WangBiRepairedEdgeGrade (.around ⟨.north, .s4⟩) ≠
        originalF55BraidedSquareGenerator :=
    (c60WangBiRepairedEdgeGrade_changed_iff _).mpr (by decide)
  exact hchanged (hword.trans
    (c60F35FixedSquareWordGrade_eq_original t₁ t₂ left right word))

/-- The Wang Bi NATURAL TRANSFORMATION on all 360 original C60
flags detects exactly the same original fixed-square word
liftability, by its already-proved grade faithfulness. An atlas
equality does NOT identify distinct raw proof-relevant words. -/
theorem c60F35WangBiAtlas_eq_iff_fixedSquareSourceLift
    (α β : ZMod 2)
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0)
    (frame : WangBiFrame) (side : C60DartSideGauge) :
    (c60WangBiGlobalGradedAtlas side (c60F33CorrectedEdgeGrade α β k) =
        c60WangBiGlobalGradedAtlas side c60F19UniformF55EdgeLabels) ↔
      ∃ words : TruncatedIcosahedralEdge → C60F55SquareWord false true,
        ∀ e : TruncatedIcosahedralEdge,
          c60F33CorrectedEdgeGrade α β k e =
            c60F35FixedSquareWordGrade t₁ t₂ left right (words e) := by
  rw [c60F35FixedSquareWordAtlasLift_iff_uniform t₁ t₂ left right]
  constructor
  · intro h
    exact c60WangBiGlobalGradedAtlas_faithful frame side h
  · intro h
    rw [h]

#print axioms c60F35WangBiAtlas_eq_iff_fixedSquareSourceLift
#print axioms c60F35CorrectedAtlas_hasFixedSource_iff_correction
#print axioms c60F35NoFlatFixedSquareSourceLift
#print axioms c60F35FlatLockedButNoFixedSquareSourceLift
#print axioms c60F35NorthClosingEdge_locked_but_notFixedSquareLift
#print axioms c60F35FixedSquareWordGrade_eq_original

end FixedSquareRoutes

#print axioms c60F35TypedSourceLift_iff_phaseAndF58Realization
#print axioms c60F35FixedSquareCorrection_returns_original
#print axioms c60F35FixedSquareCorrection_notFlat
#print axioms c60F35FixedSquareCorrection_all90_locked
#print axioms c60F35OddOddFixedSquareCorrection_support90

end
end KUOS.DependentOriginationGrayC60TypedF55LiftV5_183
