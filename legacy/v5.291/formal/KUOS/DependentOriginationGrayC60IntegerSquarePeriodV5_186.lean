import KUOS.DependentOriginationGrayC60SquareLoopCosetV5_185
import Mathlib.GroupTheory.SpecificGroups.Cyclic.Basic
import Mathlib.Algebra.Group.Subgroup.ZPowers.Lemmas

namespace KUOS.DependentOriginationGrayC60IntegerSquarePeriodV5_186

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
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60BraidedFlatRepairV5_181
open KUOS.DependentOriginationGrayC60BraidedSharpSupportV5_182
open KUOS.DependentOriginationGrayC60TypedF55LiftV5_183
open KUOS.DependentOriginationGrayC60FullF55ChargeObstructionV5_184
open KUOS.DependentOriginationGrayC60SquareLoopCosetV5_185
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
# F59-F38 / v5.186 — the genuine original F55 square-loop group has an integral period

F59-F37 proved the *genuine, typed source-loop* square charges
form an additive subgroup H_r ≤ ℤ, preserved by actual F55
source transport. This theorem unit applies the independently
proved structure theorem for ALL additive subgroups of ℤ to obtain
a nonnegative period d_r and classify the EXACT original F55
realizable second charge by ORDINARY INTEGER DIVISIBILITY.

The period d_r is sourced from the genuine original nine-constructor
F55 loop subgroup; unlike assigning a new arbitrary charge, the
period itself is witnessed by a concrete genuine original F55
PresentedCell loop (possibly its identity when d_r=0).

  qS(original cell r⇒s) = z
  iff d_r divides z - qS(original source anchor r⇒s).

A neutral Gray coefficient g between the same source routes
therefore lifts iff:
  (i)   g.phase = (g.charge.2 : ZMod 2),
  (ii)  g.charge.1 = rotationCount(r) - rotationCount(s),
  (iii) (d_r : ℤ) ∣ (g.charge.2 - qS(anchor)).

All three conditions transfer to the original REAL C60 ninety
physical edges and the faithful Mathlib Wang Bi 360-corner atlas,
and combine with the original twelve pentagon / twenty hexagon
flatness and independent a*b braid-phase correction.

This gives a SHARP ARITHMETIC normalization of the source image
without guessing the NUMERICAL value of d_r. If d_r=0, the
original Gray interpretation is rigid on parallel F55 proof
witnesses. If d_r=1, all phase-locked Gray coefficients with
the correct source pentagon charge actually have source lifts.
More precise numerical determination of d_r would require
additional genuine F54/F55 source loop construction or rigidity.

No full ambient Gray 3-functor, historical Wang Bi semantics,
raw source quotient, or Stage-II omega identification is claimed.
-/

/-! ## I. A nonnegative integer period for every genuine subgroup of ℤ -/

/-- Mathlib's cyclicity of subgroups of ℤ, specialized to a
NONNEGATIVE generator. This is an actual discrete integer period,
not an invented source F55 3-cell. -/
theorem c60F38EveryIntegerAddSubgroup_hasNaturalPeriod
    (H : AddSubgroup ℤ) :
    ∃ d : ℕ, H = AddSubgroup.zmultiples (d : ℤ) := by
  have hle : H ≤ AddSubgroup.zmultiples (1 : ℤ) := by
    intro z _
    exact (Int.mem_zmultiples_iff).mpr (one_dvd z)
  obtain ⟨d, hd⟩ :=
    (AddSubgroup.le_zmultiples_iff (1 : ℤ) H).mp hle
  exact ⟨d, by simpa using hd⟩

/-- Canonically choose an integer subgroup's nonnegative period.
No computation of an original F55 loop is assumed at this stage. -/
noncomputable def c60F38IntegerAddSubgroupPeriod
    (H : AddSubgroup ℤ) : ℕ :=
  Classical.choose (c60F38EveryIntegerAddSubgroup_hasNaturalPeriod H)

theorem c60F38IntegerAddSubgroupPeriod_spec (H : AddSubgroup ℤ) :
    H = AddSubgroup.zmultiples
      ((c60F38IntegerAddSubgroupPeriod H : ℕ) : ℤ) :=
  Classical.choose_spec (c60F38EveryIntegerAddSubgroup_hasNaturalPeriod H)

/-- Membership in an arbitrary integer subgroup is reduced to
ordinary integer divisibility by its chosen nonnegative period. -/
theorem c60F38IntegerSubgroup_mem_iff_period_dvd
    (H : AddSubgroup ℤ) (z : ℤ) :
    z ∈ H ↔ ((c60F38IntegerAddSubgroupPeriod H : ℕ) : ℤ) ∣ z := by
  have heq : H = AddSubgroup.zmultiples
      ((c60F38IntegerAddSubgroupPeriod H : ℕ) : ℤ) :=
    c60F38IntegerAddSubgroupPeriod_spec H
  constructor
  · intro hz
    exact (Int.mem_zmultiples_iff).mp (heq ▸ hz)
  · intro hdiv
    exact heq.symm ▸ ((Int.mem_zmultiples_iff).mpr hdiv)

/-! ## II. Original fully typed F55 source-loop period -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalTypedSource
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Integer period of ALL original typed F55 loop-square charges
at the exact original F54 route. It is a canonical selection from
the *actual* source image subgroup, not an added source axiom. -/
noncomputable def c60F38F55SquarePeriod
    (route : OriginalF45BracketTree.DepthRotationRoute first last) : ℕ :=
  c60F38IntegerAddSubgroupPeriod
    (c60F37OriginalSquareLoopSubgroup route)

theorem c60F38F55SquareLoopSubgroup_eq_period
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    c60F37OriginalSquareLoopSubgroup route =
      AddSubgroup.zmultiples ((c60F38F55SquarePeriod route : ℕ) : ℤ) :=
  c60F38IntegerAddSubgroupPeriod_spec _

theorem c60F38F55SquareLoop_mem_iff_dvd
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (z : ℤ) :
    z ∈ c60F37OriginalSquareLoopSubgroup route ↔
      ((c60F38F55SquarePeriod route : ℕ) : ℤ) ∣ z :=
  c60F38IntegerSubgroup_mem_iff_period_dvd _ _

/-- The canonical period is ACTUALLY achieved by a genuine original
nine-constructor F55 proof-relevant closed cell at the original
F54 route. The existence witness cannot be an arbitrary target
Gray 3-cell or a fabricated edge. -/
theorem c60F38F55SquarePeriod_hasOriginalLoopWitness
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        route route,
      c60F37SquareCharge loop = (c60F38F55SquarePeriod route : ℤ) := by
  have hm : (c60F38F55SquarePeriod route : ℤ) ∈
      c60F37OriginalSquareLoopSubgroup route := by
    rw [c60F38F55SquareLoopSubgroup_eq_period route]
    exact AddSubgroup.mem_zmultiples _
  exact hm

/-- The chosen period is invariant under ACTUAL original typed
F55 higher transport (conjugation of real source loops). -/
theorem c60F38F55SquarePeriod_transport
    (anchor : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F38F55SquarePeriod r = c60F38F55SquarePeriod s := by
  change c60F38IntegerAddSubgroupPeriod
      (c60F37OriginalSquareLoopSubgroup r) =
    c60F38IntegerAddSubgroupPeriod
      (c60F37OriginalSquareLoopSubgroup s)
  rw [c60F37OriginalSquareLoopSubgroup_transport anchor]

/-- The exact original F55 source second-charge image now has a
simple DIVISIBILITY criterion. The previous source-dependent
affine coset subgroup condition has become an integer congruence
modulo the new canonical nonnegative F55 square-loop period. -/
theorem c60F38SquareCharge_realizable_iff_period_dvd
    (anchor : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (z : ℤ) :
    (∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      c60F37SquareCharge cell = z) ↔
      ((c60F38F55SquarePeriod r : ℕ) : ℤ) ∣
        (z - c60F37SquareCharge anchor) := by
  rw [c60F37SquareCharge_realizable_iff_affineCoset anchor z]
  exact c60F38F55SquareLoop_mem_iff_dvd r _

/-- Every pair of genuine original F55 typed paths between the
same exact F54 routes has square-charge difference divisible
by the route's canonical source-loop integer period. -/
theorem c60F38ParallelSourceSquareDifference_period_dvd
    (α β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    ((c60F38F55SquarePeriod r : ℕ) : ℤ) ∣
      (c60F37SquareCharge α - c60F37SquareCharge β) := by
  exact (c60F38SquareCharge_realizable_iff_period_dvd β
    (c60F37SquareCharge α)).mp ⟨α, rfl⟩

/-- COMPLETE original source lift arithmetic normal form:
independent F55 phase, exact original route pentagon length charge,
and period divisibility for actual original source square charges.
This is proved for ALL NINE original F55 constructors. -/
theorem c60F38TypedSourceLift_iff_phase_pentagon_periodDvd
    (anchor : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (g : GradedThreeCell 0 0) :
    (∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      c60F55SourceNative cell = g) ↔
      g ∈ c60F55PhaseLocked ∧
      g.charge.1 = (r.rotationCount : ℤ) - (s.rotationCount : ℤ) ∧
      ((c60F38F55SquarePeriod r : ℕ) : ℤ) ∣
        (g.charge.2 - c60F37SquareCharge anchor) := by
  rw [c60F37TypedSourceLift_iff_phase_pentagon_squareCoset anchor g]
  rw [c60F38F55SquareLoop_mem_iff_dvd]

/-- If the source-loop period is ZERO, independent raw original
PresentedCells with the same typed F54 boundaries have equal
neutral Gray 3-cell TARGET INTERPRETATIONS, not necessarily equal
raw F55 source syntax. -/
theorem c60F38ZeroPeriod_forces_targetRigidity
    (hzero : c60F38F55SquarePeriod r = 0)
    (α β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F55SourceNative α = c60F55SourceNative β := by
  have hd := c60F38ParallelSourceSquareDifference_period_dvd α β
  rw [hzero] at hd
  have hsq : c60F37SquareCharge α = c60F37SquareCharge β := by
    have hz : c60F37SquareCharge α - c60F37SquareCharge β = 0 :=
      (zero_dvd_iff).mp (by simpa using hd)
    exact sub_eq_zero.mp hz
  have hp : (c60F55SourceNative α).charge.1 =
      (c60F55SourceNative β).charge.1 := by
    rw [c60F36FullNinePentagonCharge_eq_rotationDifference α,
      c60F36FullNinePentagonCharge_eq_rotationDifference β]
  have hc : (c60F55SourceNative α).charge =
      (c60F55SourceNative β).charge := Prod.ext hp hsq
  have hα := c60F55SourceNative_mem α
  have hβ := c60F55SourceNative_mem β
  change (c60F55SourceNative α).phase =
    ((c60F55SourceNative α).charge.2 : ZMod 2) at hα
  change (c60F55SourceNative β).phase =
    ((c60F55SourceNative β).charge.2 : ZMod 2) at hβ
  apply GradedThreeCell.ext hc
  calc
    (c60F55SourceNative α).phase =
      ((c60F55SourceNative α).charge.2 : ZMod 2) := hα
    _ = ((c60F55SourceNative β).charge.2 : ZMod 2) := by rw [hc]
    _ = (c60F55SourceNative β).phase := hβ.symm

/-- If the source-loop period is ONE, the typed source F55 image
realizes EVERY F55 phase-locked neutral Gray coefficient with
the correct original rotation-count pentagon charge. -/
theorem c60F38UnitPeriod_allCompatibleTargetsLift
    (anchor : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (hone : c60F38F55SquarePeriod r = 1)
    (g : GradedThreeCell 0 0)
    (hlocked : g ∈ c60F55PhaseLocked)
    (hp : g.charge.1 = (r.rotationCount : ℤ) -
      (s.rotationCount : ℤ)) :
    ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      c60F55SourceNative cell = g := by
  apply (c60F38TypedSourceLift_iff_phase_pentagon_periodDvd
    anchor g).mpr
  refine ⟨hlocked, hp, ?_⟩
  simp [hone]

end OriginalTypedSource

/-! ## III. Fixed genuine original left/right square source routes -/

section OriginalPhysicalSquare
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

/-- EXACT physical original F55 all-nine square-source lift
now requires ordinary divisibility by the period of the genuine
left-first F54 route, without any unproved claim about its
numerical value. -/
theorem c60F38PhysicalSquareSourceLift_iff_periodDvd
    (g : GradedThreeCell 0 0) :
    (∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F55SourceNative cell = g) ↔
      g ∈ c60F55PhaseLocked ∧
      g.charge.1 = 0 ∧
      ((c60F38F55SquarePeriod
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right) : ℕ)
        : ℤ) ∣ (g.charge.2 - 1) := by
  rw [c60F37OriginalSquareAllNineLift_iff_coset t₁ t₂ left right g]
  rw [c60F38F55SquareLoop_mem_iff_dvd]

end OriginalPhysicalSquare

/-! ## IV. True original C60 ninety edges / 360 Wang Bi corners -/

section FullPhysicalC60
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable
  (r s : TruncatedIcosahedralEdge →
    OriginalF45BracketTree.DepthRotationRoute first last)
  (anchor : ∀ e : TruncatedIcosahedralEdge,
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e))

/-- Every real original C60 edge has independently supplied F54
typed route data, and its complete F55 source image criterion is
phase-lock + exact pentagon count + its own loop-period divisibility. -/
theorem c60F38All90TypedSourceLift_iff_periodDvd
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∃ cells : ∀ e : TruncatedIcosahedralEdge,
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
       ∀ e : TruncatedIcosahedralEdge,
         c60F55SourceNative (cells e) = grade e) ↔
      ∀ e : TruncatedIcosahedralEdge,
        grade e ∈ c60F55PhaseLocked ∧
        (grade e).charge.1 =
          ((r e).rotationCount : ℤ) - ((s e).rotationCount : ℤ) ∧
        ((c60F38F55SquarePeriod (r e) : ℕ) : ℤ) ∣
          ((grade e).charge.2 - c60F37SquareCharge (anchor e)) := by
  rw [c60F37All90TypedLift_iff_squareLoopCosets r s anchor grade]
  simp only [c60F38F55SquareLoop_mem_iff_dvd]

/-- Exact same integer-divisibility source-lift criterion in
native Mathlib Wang Bi NATURAL TRANSFORMATIONS over ALL 360 C60
physical edge-local corner flags. This relies on previously
proven faithfulness, not an invented chart morphism. -/
theorem c60F38WangBiAll90TypedLift_iff_periodDvd
    (frame : WangBiFrame) (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∃ cells : ∀ e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell (r e) (s e),
      c60WangBiGlobalGradedAtlas side
        (fun e => c60F55SourceNative (cells e)) =
          c60WangBiGlobalGradedAtlas side grade) ↔
      ∀ e : TruncatedIcosahedralEdge,
        grade e ∈ c60F55PhaseLocked ∧
        (grade e).charge.1 =
          ((r e).rotationCount : ℤ) - ((s e).rotationCount : ℤ) ∧
        ((c60F38F55SquarePeriod (r e) : ℕ) : ℤ) ∣
          ((grade e).charge.2 - c60F37SquareCharge (anchor e)) := by
  rw [c60F37WangBiAll90TypedLift_iff_squareLoopCosets
    r s anchor frame side grade]
  simp only [c60F38F55SquareLoop_mem_iff_dvd]

/-- Full actual C60 original braiding-target descent and source
lift, now expressed by the INTEGRAL F55 source-loop PERIOD at
each original edge. The phase-defect condition still measures
the independent nonprojected a*b Gray braiding. -/
theorem c60F38BraidedFlatTypedLift_iff_periodDvd
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
          (c60F33CorrectedEdgeGrade α β k e).charge.1 =
            ((r e).rotationCount : ℤ) - ((s e).rotationCount : ℤ)) ∧
       (∀ e : TruncatedIcosahedralEdge,
          ((c60F38F55SquarePeriod (r e) : ℕ) : ℤ) ∣
            ((c60F33CorrectedEdgeGrade α β k e).charge.2 -
              c60F37SquareCharge (anchor e)))) := by
  rw [c60F37BraidedFlatTypedLift_iff_squareLoopCosets r s anchor α β k]
  simp only [c60F38F55SquareLoop_mem_iff_dvd]

end FullPhysicalC60

#print axioms c60F38EveryIntegerAddSubgroup_hasNaturalPeriod
#print axioms c60F38IntegerAddSubgroupPeriod_spec
#print axioms c60F38IntegerSubgroup_mem_iff_period_dvd
#print axioms c60F38F55SquareLoopSubgroup_eq_period
#print axioms c60F38F55SquareLoop_mem_iff_dvd
#print axioms c60F38F55SquarePeriod_hasOriginalLoopWitness
#print axioms c60F38F55SquarePeriod_transport
#print axioms c60F38SquareCharge_realizable_iff_period_dvd
#print axioms c60F38ParallelSourceSquareDifference_period_dvd
#print axioms c60F38TypedSourceLift_iff_phase_pentagon_periodDvd
#print axioms c60F38ZeroPeriod_forces_targetRigidity
#print axioms c60F38UnitPeriod_allCompatibleTargetsLift
#print axioms c60F38PhysicalSquareSourceLift_iff_periodDvd
#print axioms c60F38All90TypedSourceLift_iff_periodDvd
#print axioms c60F38WangBiAll90TypedLift_iff_periodDvd
#print axioms c60F38BraidedFlatTypedLift_iff_periodDvd

end
end KUOS.DependentOriginationGrayC60IntegerSquarePeriodV5_186
