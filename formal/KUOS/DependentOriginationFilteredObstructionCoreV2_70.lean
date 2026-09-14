import Mathlib

namespace KUOS.DependentOriginationFilteredObstructionCoreV2_70

open Set

universe u

/-!
# Filtered obstruction core v2.70

This file introduces the minimal decreasing-filtration layer used by the
filtered residual hyperdescent program. It is deliberately independent of the
higher-localization and generated-holonomy modules.

`Flat` means membership in every filtration level. It is not identified with
an exact defect until `SeparatedAt` is supplied explicitly.
-/

/-- A decreasing natural-number filtration of an obstruction carrier.
Higher indices represent stronger vanishing/order requirements. -/
structure ObstructionFiltration (D : Type u) where
  level : ℕ → Set D
  antitone_level : Antitone level

namespace ObstructionFiltration

variable {D : Type u}

/-- The defect `d` has filtration order at least `n`. -/
def OrderAtLeast (F : ObstructionFiltration D) (n : ℕ) (d : D) : Prop :=
  d ∈ F.level n

/-- The defect lies in every filtration level. This is not equality to an
exact defect unless separatedness is supplied separately. -/
def Flat (F : ObstructionFiltration D) (d : D) : Prop :=
  ∀ n, d ∈ F.level n

/-- Stronger filtration order implies every weaker filtration order. -/
theorem orderAtLeast_mono
    (F : ObstructionFiltration D) {m n : ℕ} {d : D}
    (hmn : m ≤ n) (hd : F.OrderAtLeast n d) :
    F.OrderAtLeast m d := by
  exact F.antitone_level hmn hd

/-- A flat defect has every finite filtration order. -/
theorem flat_orderAtLeast
    (F : ObstructionFiltration D) {d : D}
    (hd : F.Flat d) (n : ℕ) : F.OrderAtLeast n d := by
  exact hd n

/-- The distinguished exact defect `e` is itself flat and is the unique flat
defect. Requiring `F.Flat e` prevents vacuous separatedness. -/
def SeparatedAt (F : ObstructionFiltration D) (e : D) : Prop :=
  F.Flat e ∧ ∀ d, F.Flat d → d = e

/-- The distinguished exact defect is flat in every separated filtration. -/
theorem separatedAt_exact_flat
    (F : ObstructionFiltration D) {e : D}
    (hsep : F.SeparatedAt e) : F.Flat e := by
  exact hsep.1

/-- In a filtration separated at `e`, every flat defect equals `e`. -/
theorem flat_eq_of_separatedAt
    (F : ObstructionFiltration D) {d e : D}
    (hsep : F.SeparatedAt e) (hd : F.Flat d) : d = e := by
  exact hsep.2 d hd

/-- A defect known to differ from the exact defect cannot be flat in a
filtration separated at that exact defect. -/
theorem not_flat_of_ne_of_separatedAt
    (F : ObstructionFiltration D) {d e : D}
    (hsep : F.SeparatedAt e) (hne : d ≠ e) : ¬ F.Flat d := by
  intro hd
  exact hne (hsep.2 d hd)

end ObstructionFiltration
end KUOS.DependentOriginationFilteredObstructionCoreV2_70
