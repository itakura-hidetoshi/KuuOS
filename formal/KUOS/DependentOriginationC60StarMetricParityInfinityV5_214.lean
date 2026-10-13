import Mathlib
import Mathlib.AlgebraicTopology.Quasicategory.Nerve
import Mathlib.CategoryTheory.Elements
import KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90
import KUOS.DependentOriginationFreeHistoryFunctorV0_6

namespace KUOS.DependentOriginationC60StarMetricParityInfinityV5_214

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationTruncatedIcosahedralRecursiveRefinementV3_90
open KUOS.DependentOriginationHistorySensitiveTransportV0_5
open KUOS.DependentOriginationFreeHistoryFunctorV0_6

set_option autoImplicit false
noncomputable section

/-!
# C60 pentagram/hexagram metrics, optional parity and the genuine context-state nerve

The existing v3.83–v3.90 files construct the ORIGINAL five- and six-vertex
recursive star incidences without claiming Euclidean metrics. This file adds
the exact numerical contraction constants for the *standard planar* regular
pentagram/hexagram conventions and proves their mismatch, as a first
obstruction to a single common metric scale across all 32 C60 faces.

The geometric identification of those constants with the actual intersection
coordinates of the old incidence carriers is NOT asserted; that requires
a separate faithful Euclidean realization. This is also NOT a theorem
that the isolated interior star faces glue to a new C60 sphere.

A chosen orientation-change ZMod 2 label is retained INDEPENDENTLY of scale.
Free finite histories define a genuine context-state functor and its
Mathlib category-of-elements nerve is a quasicategory. This 1-categorical
nerve does NOT yet realize nontrivial higher geometric homotopies, a global
(infinity,2) equivalence, or Cech hyperdescent.
-/

private theorem sqrt_five_bounds :
    (2 : ℝ) < Real.sqrt 5 ∧ Real.sqrt 5 < 3 := by
  have hsq : (Real.sqrt (5 : ℝ)) ^ 2 = 5 :=
    Real.sq_sqrt (by norm_num)
  have hnonneg : 0 ≤ Real.sqrt (5 : ℝ) :=
    Real.sqrt_nonneg _
  constructor <;> nlinarith

private theorem sqrt_three_bounds :
    (3 / 2 : ℝ) < Real.sqrt 3 ∧ Real.sqrt 3 < 3 := by
  have hsq : (Real.sqrt (3 : ℝ)) ^ 2 = 3 :=
    Real.sq_sqrt (by norm_num)
  have hnonneg : 0 ≤ Real.sqrt (3 : ℝ) :=
    Real.sqrt_nonneg _
  constructor <;> nlinarith

/-- Golden ratio, used only for the standard planar regular pentagram. -/
def goldenRatio : ℝ := (1 + Real.sqrt 5) / 2

/-- Central pentagon side length divided by the original pentagon side. -/
def pentagramContraction : ℝ := (3 - Real.sqrt 5) / 2

/-- Central hexagon side length divided by the original hexagon side
when two alternating equilateral triangles form the hexagram. -/
def hexagramContraction : ℝ := Real.sqrt 3 / 3

/-- Golden-ratio square law with an algebraic Mathlib proof. -/
theorem pentagramContraction_mul_goldenRatio_sq :
    pentagramContraction * goldenRatio ^ 2 = 1 := by
  have hsq : (Real.sqrt (5 : ℝ)) ^ 2 = 5 :=
    Real.sq_sqrt (by norm_num)
  have hphi : goldenRatio ^ 2 = (3 + Real.sqrt 5) / 2 := by
    dsimp [goldenRatio]
    nlinarith
  rw [hphi]
  dsimp [pentagramContraction]
  nlinarith

theorem goldenRatio_pos : 0 < goldenRatio := by
  dsimp [goldenRatio]
  have h := Real.sqrt_nonneg (5 : ℝ)
  linarith

/-- Exact pentagram shrink factor phi^(-2). -/
theorem pentagramContraction_eq_inv_phi_sq :
    pentagramContraction = 1 / goldenRatio ^ 2 := by
  have hne : goldenRatio ^ 2 ≠ 0 :=
    ne_of_gt (pow_pos goldenRatio_pos _)
  exact (eq_div_iff hne).2 pentagramContraction_mul_goldenRatio_sq

theorem pentagramContraction_pos : 0 < pentagramContraction := by
  dsimp [pentagramContraction]
  linarith [sqrt_five_bounds.2]

theorem pentagramContraction_lt_half :
    pentagramContraction < (1 / 2 : ℝ) := by
  dsimp [pentagramContraction]
  linarith [sqrt_five_bounds.1]

theorem hexagramContraction_gt_half :
    (1 / 2 : ℝ) < hexagramContraction := by
  dsimp [hexagramContraction]
  linarith [sqrt_three_bounds.1]

theorem hexagramContraction_lt_one : hexagramContraction < 1 := by
  dsimp [hexagramContraction]
  linarith [sqrt_three_bounds.2]

theorem pentagramContraction_lt_hexagramContraction :
    pentagramContraction < hexagramContraction :=
  lt_trans pentagramContraction_lt_half hexagramContraction_gt_half

/-- The contraction is genuinely face-type dependent. -/
def starFaceScale : TruncatedIcosahedralFaceKind → ℝ
  | .pentagon => pentagramContraction
  | .hexagon => hexagramContraction

theorem starFaceScale_pos (k : TruncatedIcosahedralFaceKind) :
    0 < starFaceScale k := by
  cases k
  · exact pentagramContraction_pos
  · exact lt_trans (by norm_num : (0 : ℝ) < 1 / 2)
      hexagramContraction_gt_half

theorem starFaceScale_lt_one (k : TruncatedIcosahedralFaceKind) :
    starFaceScale k < 1 := by
  cases k
  · exact lt_trans pentagramContraction_lt_half (by norm_num)
  · exact hexagramContraction_lt_one

/-- Even the numerical metric data rule out one shared uniform face scale. -/
theorem no_uniform_C60_star_scale
    (r : ℝ)
    (hall : ∀ k : TruncatedIcosahedralFaceKind, starFaceScale k = r) :
    False := by
  have h : pentagramContraction = hexagramContraction := by
    calc
      pentagramContraction = r := hall .pentagon
      _ = hexagramContraction := (hall .hexagon).symm
  exact (ne_of_lt pentagramContraction_lt_hexagramContraction) h

/-- Star recursion retains the face kind but does NOT assert boundary gluing. -/
theorem starFaceScale_recursion_stable
    (depth : Nat) (kind : TruncatedIcosahedralFaceKind) :
    starFaceScale (truncatedIcosahedralRecursiveFaceKind depth kind) =
      starFaceScale kind := by
  simp

/-- A star refinement event records a face kind AND a separately chosen parity
change. A geometric reflection is not silently inferred from drawing a star. -/
abbrev StarEvent := TruncatedIcosahedralFaceKind × ZMod 2

/-- Radius and chosen orientation bit; this is an observation state rather
than an a priori topological orientation of the actual 3D C60 surface. -/
abbrev StarState := ℝ × ZMod 2

/-- A single labeled refinement acts by its face-specific contraction and
its chosen parity update. -/
def starStep (e : StarEvent) (x : StarState) : StarState :=
  (starFaceScale e.1 * x.1, x.2 + e.2)

/-- Finite contextual histories are freely composable and need not be reversible. -/
def starHistoryTransport : HistoryTransport StarEvent StarState :=
  HistoryTransport.ofSingleEventTransport starStep

/-- Genuine original KuuOS parent functor from the free-history category. -/
def starHistoryContextualSystem :
    KUOS.DependentOriginationFunctorialTransportV0_1.FunctorialTransportSystem
      (FreeHistoryCategory StarEvent) :=
  starHistoryTransport.toFunctorialTransportSystem

/-- Finite histories obey the actual original compositional transport law. -/
theorem starHistoryTransport_append
    (left right : List StarEvent) (x : StarState) :
    starHistoryTransport.eval (left ++ right) x =
      starHistoryTransport.eval left
        (starHistoryTransport.eval right x) :=
  starHistoryTransport.eval_append left right x

/-- The nerve retains BOTH context and state, rather than merely its
one-object free-history category. -/
def starHistoryDependentNerve : SSet :=
  CategoryTheory.nerve starHistoryContextualSystem.state.Elements

/-- A genuine pinned-Mathlib quasicategory structure, via category of
elements and its strict Segal nerve. This remains 1-truncated.
Import Mathlib directly, so the historical v1.2 refinement proof is NOT a
spurious dependency of this independent new theorem. -/
theorem starHistoryDependentNerve_quasicategory :
    SSet.Quasicategory starHistoryDependentNerve :=
  SSet.StrictSegal.quasicategory
    (CategoryTheory.Nerve.strictSegal
      starHistoryContextualSystem.state.Elements)

/-- Hence the C60 parity-and-scale history model fills every inner horn
at the 1-categorical state-transport level; nontrivial higher geometric
fillers remain a distinct future task. -/
theorem starHistoryDependentNerve_innerHornFilling
    {n : Nat} {i : Fin (n + 1)}
    (h0 : 0 < i) (hn : i < Fin.last n)
    (σ0 : (Λ[n, i] : SSet) ⟶ starHistoryDependentNerve) :
    ∃ σ : Δ[n] ⟶ starHistoryDependentNerve,
      σ0 = Λ[n, i].ι ≫ σ := by
  letI : SSet.Quasicategory starHistoryDependentNerve :=
    starHistoryDependentNerve_quasicategory
  exact SSet.Quasicategory.hornFilling h0 hn σ0

#print axioms pentagramContraction_eq_inv_phi_sq
#print axioms pentagramContraction_lt_hexagramContraction
#print axioms no_uniform_C60_star_scale
#print axioms starFaceScale_recursion_stable
#print axioms starHistoryTransport_append
#print axioms starHistoryDependentNerve_quasicategory
#print axioms starHistoryDependentNerve_innerHornFilling

end
end KUOS.DependentOriginationC60StarMetricParityInfinityV5_214
