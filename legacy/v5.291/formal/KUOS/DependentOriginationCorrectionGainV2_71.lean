import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationCorrectionGainV2_71

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration

universe u v

/-!
# Exact-invariant correction gain v2.71

This layer separates an exact invariant from a residual defect and records
correction as a relation rather than a canonical function.  Only finite
iteration is constructed here; no infinite tower or convergence statement is
asserted.
-/

/-- A residual problem consists of an exact invariant and a defect-valued
readout. -/
structure ResidualProblem (State : Type u) (D : Type v) where
  invariant : State → Prop
  residual : State → D

/-- One admissible correction step raises certified obstruction order by `δ`
while preserving the exact invariant. -/
def HasCorrectionGain
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    (δ : ℕ) : Prop :=
  0 < δ ∧
    ∀ x n,
      P.invariant x →
      F.OrderAtLeast n (P.residual x) →
      ∃ y,
        Step x y ∧
        P.invariant y ∧
        F.OrderAtLeast (n + δ) (P.residual y)

/-- Correction gain is required to be strictly positive. -/
theorem correctionGain_pos
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop) {δ : ℕ}
    (h : HasCorrectionGain F P Step δ) : 0 < δ :=
  h.1

/-- A finite correction history retaining every chosen intermediate state
through its inductive proof data. -/
inductive FiniteCorrectionChain
    {State : Type u} (Step : State → State → Prop) :
    ℕ → State → State → Prop
  | nil (x : State) : FiniteCorrectionChain Step 0 x x
  | snoc {k : ℕ} {x y z : State}
      (hxy : FiniteCorrectionChain Step k x y)
      (hyz : Step y z) :
      FiniteCorrectionChain Step (k + 1) x z

/-- A one-step existential gain can be iterated for every prescribed finite
length without selecting or postulating an infinite correction history. -/
theorem exists_finiteCorrectionChain_of_gain
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    {δ n₀ : ℕ}
    (hgain : HasCorrectionGain F P Step δ)
    {x : State}
    (hxinv : P.invariant x)
    (hxord : F.OrderAtLeast n₀ (P.residual x))
    (k : ℕ) :
    ∃ y,
      FiniteCorrectionChain Step k x y ∧
      P.invariant y ∧
      F.OrderAtLeast (n₀ + k * δ) (P.residual y) := by
  induction k generalizing x n₀ with
  | zero =>
      refine ⟨x, FiniteCorrectionChain.nil x, hxinv, ?_⟩
      simpa using hxord
  | succ k ih =>
      obtain ⟨y, hchain, hyinv, hyord⟩ :=
        ih (x := x) (n₀ := n₀) hxinv hxord
      obtain ⟨z, hyz, hzinv, hzord⟩ :=
        hgain.2 y (n₀ + k * δ) hyinv hyord
      refine ⟨z, FiniteCorrectionChain.snoc hchain hyz, hzinv, ?_⟩
      simpa [Nat.succ_mul, Nat.add_assoc] using hzord

end KUOS.DependentOriginationCorrectionGainV2_71
