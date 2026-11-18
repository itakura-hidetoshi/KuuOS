import Mathlib
import KuuOSFormal.WaUpperClipV0_24

/-!
# Lean→Python v0.25 — finite weakest-positive / strongest-alert witnesses

The original Wa evaluator observes `min(samples)` on its seven positive
axes and `max(alert_samples)` on its alert axes. This file builds
an exact-rational **mathematical finite-list model**, proving its
range and selected-extremum properties. It does not assert general
CPython min()/max(), IEEE754, or source authenticity semantics.

Python supplies explicit observation equality and source identity
separately; no existing Lean theorem or Wa state is rewritten.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS
namespace DecisionOS
namespace WaFiniteExtremaV0_25

open WaRationalBridgeV0_19 WaUpperClipV0_24

/-- An exact bounded rational finite minimum, with a unit upper
    sentinel solely for the empty list. Original Wa axes are nonempty. -/
def rationalMin : List ℚ → ℚ
  | [] => 1
  | x :: xs => min x (rationalMin xs)

/-- An exact bounded rational finite maximum, with a zero lower
    sentinel solely for the empty list. Original Wa axes are nonempty. -/
def rationalMax : List ℚ → ℚ
  | [] => 0
  | x :: xs => max x (rationalMax xs)

/-- Every finite rational minimum of unit samples stays in [0,1]. -/
theorem rational_min_unit
    (xs : List ℚ) (h : ∀ x ∈ xs, 0 ≤ x ∧ x ≤ 1) :
    0 ≤ rationalMin xs ∧ rationalMin xs ≤ 1 := by
  induction xs with
  | nil =>
      norm_num [rationalMin]
  | cons x xs ih =>
      have hx : 0 ≤ x ∧ x ≤ 1 := h x (by simp)
      have hTail : ∀ y ∈ xs, 0 ≤ y ∧ y ≤ 1 := by
        intro y hy
        exact h y (by simp [hy])
      obtain ⟨hLo, hHi⟩ := ih hTail
      constructor
      · change 0 ≤ min x (rationalMin xs)
        exact (le_min_iff).2 ⟨hx.1, hLo⟩
      · change min x (rationalMin xs) ≤ 1
        exact le_trans (min_le_left _ _) hx.2

/-- Every finite rational maximum of unit samples stays in [0,1]. -/
theorem rational_max_unit
    (xs : List ℚ) (h : ∀ x ∈ xs, 0 ≤ x ∧ x ≤ 1) :
    0 ≤ rationalMax xs ∧ rationalMax xs ≤ 1 := by
  induction xs with
  | nil =>
      norm_num [rationalMax]
  | cons x xs ih =>
      have hx : 0 ≤ x ∧ x ≤ 1 := h x (by simp)
      have hTail : ∀ y ∈ xs, 0 ≤ y ∧ y ≤ 1 := by
        intro y hy
        exact h y (by simp [hy])
      obtain ⟨hLo, hHi⟩ := ih hTail
      constructor
      · change 0 ≤ max x (rationalMax xs)
        exact le_trans hx.1 (le_max_left _ _)
      · change max x (rationalMax xs) ≤ 1
        exact (max_le_iff).2 ⟨hx.2, hHi⟩

/-- The finite minimum cannot exceed any actual member, without
    selecting a numeric index or assuming a particular interpreter. -/
theorem rational_min_le_member (xs : List ℚ) (v : ℚ)
    (hMem : v ∈ xs) : rationalMin xs ≤ v := by
  induction xs with
  | nil =>
      simp at hMem
  | cons x xs ih =>
      simp only [List.mem_cons] at hMem
      rcases hMem with hEq | hTail
      · subst v
        change min x (rationalMin xs) ≤ x
        exact min_le_left _ _
      · change min x (rationalMin xs) ≤ v
        exact le_trans (min_le_right _ _) (ih hTail)

/-- Every actual member is below the finite maximum. -/
theorem rational_member_le_max (xs : List ℚ) (v : ℚ)
    (hMem : v ∈ xs) : v ≤ rationalMax xs := by
  induction xs with
  | nil =>
      simp at hMem
  | cons x xs ih =>
      simp only [List.mem_cons] at hMem
      rcases hMem with hEq | hTail
      · subst v
        change x ≤ max x (rationalMax xs)
        exact le_max_left _ _
      · change v ≤ max x (rationalMax xs)
        exact le_trans (ih hTail) (le_max_right _ _)

/-- The original mathematical Wa ideal is in [0,1] when its
    finite positive and alert sample lists satisfy their declared
    pointwise unit constraints and normalized weighted score is unit. -/
theorem rational_finite_extrema_wa_ideal_in_unit
    (beta normalized : ℚ) (positives alerts : List ℚ)
    (hBeta0 : 0 ≤ beta) (hBeta1 : beta ≤ 1)
    (hNorm0 : 0 ≤ normalized) (hNorm1 : normalized ≤ 1)
    (hPositives : ∀ x ∈ positives, 0 ≤ x ∧ x ≤ 1)
    (hAlerts : ∀ x ∈ alerts, 0 ≤ x ∧ x ≤ 1) :
    0 ≤ rationalIdeal beta normalized
      (rationalMin positives) (rationalMax alerts) ∧
    rationalIdeal beta normalized
      (rationalMin positives) (rationalMax alerts) ≤ 1 := by
  have hWeak := rational_min_unit positives hPositives
  have hAlert := rational_max_unit alerts hAlerts
  exact rational_normalized_wa_ideal_in_unit
    beta normalized (rationalMin positives) (rationalMax alerts)
    hBeta0 hBeta1 hNorm0 hNorm1
    hWeak.1 hWeak.2 hAlert.1 hAlert.2

/-- Gluing of separately *observed* weakest/alert equalities to
    the mathematical finite-list model. It does not prove the
    observation identities of an arbitrary Python runtime. -/
theorem observed_finite_extrema_ideal_identity
    (beta weighted weakest alert : ℚ)
    (positives alerts : List ℚ)
    (hWeak : weakest = rationalMin positives)
    (hAlert : alert = rationalMax alerts) :
    rationalIdeal beta weighted weakest alert =
      rationalIdeal beta weighted
        (rationalMin positives) (rationalMax alerts) := by
  rw [hWeak, hAlert]

#print axioms rational_min_unit
#print axioms rational_max_unit
#print axioms rational_min_le_member
#print axioms rational_member_le_max
#print axioms rational_finite_extrema_wa_ideal_in_unit
#print axioms observed_finite_extrema_ideal_identity

end WaFiniteExtremaV0_25
end DecisionOS
end KUOS
