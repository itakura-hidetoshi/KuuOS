# Constructive Dependent Origination v2.74-v2.80 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Extend the green v2.70-v2.73 filtered-obstruction stack with explicit correction images, ordered correction sectors, bounded-loss filtration calculus, cofinal schedules, explicit tower realization, residual-stability transfer, relative correction, and generated-holonomy correctability while preserving the invariant non-flat != uncorrectable.

**Architecture:** Implement seven additive Lean layers in strict dependency order. Each layer owns one authority boundary: correction-image evidence, ordered finite correction, fixed-loss stability, cofinal stage selection, realization versus residual transfer, relative preservation/descent, and generated-holonomy specialization. Every mathematical unit is validated on its exact head before the next layer is stacked.

**Tech Stack:** Lean leanprover/lean4:v4.30.0-rc2; Mathlib exact revision 5450b53e5ddc75d46418fabb605edbf36bd0beb6; Lake; GitHub exact-head CI.

**Spec:** docs/superpowers/specs/2026-09-20-constructive-dependent-origination-v274-v280-design.md

## Global Constraints

- Design authority is ec54fac27d35b665485e99c1377269ee57c84711.
- Mathematical base at design start is green v2.73 head b9a860de89b6abc7b867a4ef40b8013e25b9b16a.
- Fresh-observe the actual base before every implementation unit; do not rely on a stale or synthetic merge SHA.
- Lean toolchain stays exactly v4.30.0-rc2 and Mathlib stays exactly 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
- Additive/tighten-only: do not weaken or reinterpret v2.70-v2.73.
- No sorry, admit, new axiom, hidden canonical correction, hidden topology, or hidden completeness.
- non-flat must never be identified with uncorrectable.
- Finite correction gain must not imply an infinite tower.
- A formal tower must not imply a realized limit.
- A realized limit must not inherit flat residual without explicit residual-stability transfer.
- Flatness must not imply equality without SeparatedAt.
- Every bounded loss is explicit.
- Relative correction preserves exterior exactness only through explicit hypotheses.
- Generated-holonomy nontriviality must not imply hard obstruction without independent uncorrectability evidence.
- Do not edit README, ROADMAP, lakefile.toml, lean-toolchain, v2.69, or existing v2.70-v2.73 theorem files in these units.

## Review Focus

1. Correctable but non-flat defects remain possible.
2. A cofinal schedule may be unbounded without being eventually monotone.
3. Robust-margin weakening goes from stronger margin to weaker margin only.
4. Later sector corrections preserve earlier sectors at their already-raised order.
5. Nontrivial or non-flat holonomy is not hard until explicit uncorrectability evidence exists.

## File Structure

Create:

- formal/KUOS/DependentOriginationCorrectionRealizationV2_74.lean
- formal/KUOS/DependentOriginationOrderedSectorCorrectionV2_75.lean
- formal/KUOS/DependentOriginationBoundedLossFiltrationV2_76.lean
- formal/KUOS/DependentOriginationCofinalCorrectionV2_77.lean
- formal/KUOS/DependentOriginationTowerRealizationV2_78.lean
- formal/KUOS/DependentOriginationResidualStabilityV2_78.lean
- formal/KUOS/DependentOriginationRelativeCorrectionV2_79.lean
- formal/KUOS/DependentOriginationGeneratedHolonomyCorrectabilityV2_80.lean

Temporary compile probes live under /tmp and are not committed.

---

### Task 1: v2.74 Explicit Correction Realization

**Files:**
- Create formal/KUOS/DependentOriginationCorrectionRealizationV2_74.lean
- Test /tmp/CorrectionRealizationV274Probe.lean

**Interfaces:**
- Produces CorrectionRealization, CorrectableAt, HardObstructionAt, RobustCorrectionData, correctableAt, weaken_margin.

- [ ] **Step 1: Write the failing truth-test probe**

The probe must include a Boolean defect carrier with a filtration whose only flat value is true, and an explicit correction realization that can realize false. It must prove both:

~~~lean
example : boolCorrection.CorrectableAt () false := by
  exact ⟨false, trivial, rfl⟩

example : boolCorrection.CorrectableAt () false ∧ ¬ boolFiltration.Flat false := by
  constructor
  · exact ⟨false, trivial, rfl⟩
  · intro h
    have h0 := h 0
    simp [boolFiltration] at h0
~~~

Run:

~~~bash
lake env lean /tmp/CorrectionRealizationV274Probe.lean
~~~

Expected: module-not-found failure before implementation.

- [ ] **Step 2: Implement the v2.74 API**

~~~lean
import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationCorrectionRealizationV2_74

universe u v w m

structure CorrectionRealization
    (State : Type u) (Param : Type v) (D : Type w) where
  admissible : State → Param → Prop
  effect : State → Param → D

namespace CorrectionRealization

variable {State : Type u} {Param : Type v} {D : Type w}

def CorrectableAt
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) : Prop :=
  ∃ p, C.admissible x p ∧ C.effect x p = d

def HardObstructionAt
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) : Prop :=
  ¬ C.CorrectableAt x d

end CorrectionRealization

structure RobustCorrectionData
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D)
    (Margin : Type m) [Preorder Margin] where
  robustAt : Margin → State → D → Prop
  robust_implies_correctable :
    ∀ mu x d, robustAt mu x d → C.CorrectableAt x d
  robust_monotone :
    ∀ {mu1 mu2 x d}, mu2 ≤ mu1 → robustAt mu1 x d → robustAt mu2 x d

namespace RobustCorrectionData

variable
    {State : Type u} {Param : Type v} {D : Type w}
    {C : CorrectionRealization State Param D}
    {Margin : Type m} [Preorder Margin]

theorem correctableAt
    (R : RobustCorrectionData C Margin)
    {mu : Margin} {x : State} {d : D}
    (h : R.robustAt mu x d) :
    C.CorrectableAt x d :=
  R.robust_implies_correctable mu x d h

theorem weaken_margin
    (R : RobustCorrectionData C Margin)
    {mu1 mu2 : Margin} {x : State} {d : D}
    (hmu : mu2 ≤ mu1)
    (h : R.robustAt mu1 x d) :
    R.robustAt mu2 x d :=
  R.robust_monotone hmu h

end RobustCorrectionData
end KUOS.DependentOriginationCorrectionRealizationV2_74
~~~

- [ ] **Step 3: Strict compile, probe, scan, and commit**

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationCorrectionRealizationV2_74.lean
lake env lean /tmp/CorrectionRealizationV274Probe.lean
if grep -nE '\b(sorry|admit|axiom)\b'   formal/KUOS/DependentOriginationCorrectionRealizationV2_74.lean; then
  exit 1
fi
git add formal/KUOS/DependentOriginationCorrectionRealizationV2_74.lean
git commit -m "Formalize explicit correction realization v2.74"
~~~

- [ ] **Step 4: Open a Draft stacked PR**

Branch: formal/dependent-origination-correction-realization-v274

Base: fresh head of design/constructive-dependent-origination-v274-v280

Require exact-head Strict Lean and governance success before v2.75.

---

### Task 2: v2.75 Ordered Sector Correction

**Files:**
- Create formal/KUOS/DependentOriginationOrderedSectorCorrectionV2_75.lean
- Test /tmp/OrderedSectorCorrectionV275Probe.lean

**Interfaces:**
- Produces SectorOrderData, OrderedSectorCorrector, runSchedule, runSchedule_invariant, runSchedule_preserves_not_mem, runSchedule_gain_of_mem, runFullCycle_order.

The selected correct function is explicit data; it is not inferred canonically from existential correctability.

- [ ] **Step 1: Implement the sector and selected-corrector core**

~~~lean
import KUOS.DependentOriginationCorrectionRealizationV2_74

namespace KUOS.DependentOriginationOrderedSectorCorrectionV2_75

universe u

structure SectorOrderData (State : Type u) (r : ℕ) where
  good : Fin r → ℕ → State → Prop
  weaken :
    ∀ i {m n : ℕ} {x : State},
      m ≤ n → good i n x → good i m x

structure OrderedSectorCorrector
    {State : Type u} {r : ℕ}
    (S : SectorOrderData State r)
    (Invariant : State → Prop)
    (Step : Fin r → State → State → Prop)
    (delta : ℕ) where
  correct : Fin r → State → State
  step : ∀ i x, Step i x (correct i x)
  invariant :
    ∀ i x, Invariant x → Invariant (correct i x)
  gain :
    ∀ i x n,
      Invariant x →
      S.good i n x →
      S.good i (n + delta) (correct i x)
  preserve_other :
    ∀ i j m x,
      j ≠ i →
      S.good j m x →
      S.good j m (correct i x)

namespace OrderedSectorCorrector

variable
    {State : Type u} {r delta : ℕ}
    {S : SectorOrderData State r}
    {Invariant : State → Prop}
    {Step : Fin r → State → State → Prop}

def runSchedule
    (C : OrderedSectorCorrector S Invariant Step delta) :
    List (Fin r) → State → State
  | [], x => x
  | i :: is, x => runSchedule C is (C.correct i x)

theorem runSchedule_invariant
    (C : OrderedSectorCorrector S Invariant Step delta)
    (schedule : List (Fin r)) {x : State}
    (hx : Invariant x) :
    Invariant (C.runSchedule schedule x) := by
  induction schedule generalizing x with
  | nil =>
      simpa [runSchedule] using hx
  | cons i is ih =>
      simp only [runSchedule]
      exact ih (C.invariant i x hx)

theorem runSchedule_preserves_not_mem
    (C : OrderedSectorCorrector S Invariant Step delta)
    (schedule : List (Fin r))
    {j : Fin r} {m : ℕ} {x : State}
    (hj : j ∉ schedule)
    (hgood : S.good j m x) :
    S.good j m (C.runSchedule schedule x) := by
  induction schedule generalizing x with
  | nil =>
      simpa [runSchedule] using hgood
  | cons i is ih =>
      have hji : j ≠ i := by
        intro h
        subst i
        exact hj (by simp)
      have hjtail : j ∉ is := by
        intro h
        exact hj (by simp [h])
      simp only [runSchedule]
      exact ih hjtail (C.preserve_other i j m x hji hgood)

end OrderedSectorCorrector
end KUOS.DependentOriginationOrderedSectorCorrectionV2_75
~~~

- [ ] **Step 2: Add schedule gain and full-cycle order**

Reopen namespace OrderedSectorCorrector and add:

~~~lean
theorem runSchedule_gain_of_mem
    (C : OrderedSectorCorrector S Invariant Step delta)
    (schedule : List (Fin r))
    (hnodup : schedule.Nodup)
    {x : State} {n : ℕ}
    (hxinv : Invariant x)
    (hxbase : ∀ j, S.good j n x)
    {j : Fin r}
    (hj : j ∈ schedule) :
    S.good j (n + delta) (C.runSchedule schedule x) := by
  induction schedule generalizing x with
  | nil =>
      simp at hj
  | cons i is ih =>
      have hitail : i ∉ is := (List.nodup_cons.mp hnodup).1
      have htailnodup : is.Nodup := (List.nodup_cons.mp hnodup).2
      have hx1inv : Invariant (C.correct i x) :=
        C.invariant i x hxinv
      have hx1base : ∀ k, S.good k n (C.correct i x) := by
        intro k
        by_cases hki : k = i
        · subst k
          exact S.weaken i (Nat.le_add_right n delta)
            (C.gain i x n hxinv (hxbase i))
        · exact C.preserve_other i k n x hki (hxbase k)
      simp only [runSchedule]
      rcases List.mem_cons.mp hj with hji | hjtail
      · subst j
        exact C.runSchedule_preserves_not_mem is hitail
          (C.gain i x n hxinv (hxbase i))
      · exact ih htailnodup hx1inv hx1base hjtail

theorem runFullCycle_order
    (C : OrderedSectorCorrector S Invariant Step delta)
    (schedule : List (Fin r))
    (hnodup : schedule.Nodup)
    {x : State} {n : ℕ}
    (hxinv : Invariant x)
    (hcover : ∀ j, j ∈ schedule)
    (hxbase : ∀ j, S.good j n x) :
    ∀ j, S.good j (n + delta) (C.runSchedule schedule x) := by
  intro j
  exact C.runSchedule_gain_of_mem schedule hnodup hxinv hxbase (hcover j)
~~~

- [ ] **Step 3: Truth-test two sectors**

Use State = Nat × Nat. Sector 0 is certified by the first coordinate, sector 1 by the second. Schedule [0,1]. Each selected correction increments only its active coordinate. Prove both sectors have order 1 at the end. This specifically catches regression of an earlier sector.

- [ ] **Step 4: Strict compile, probe, commit, exact-head validate**

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationOrderedSectorCorrectionV2_75.lean
lake env lean /tmp/OrderedSectorCorrectionV275Probe.lean
git add formal/KUOS/DependentOriginationOrderedSectorCorrectionV2_75.lean
git commit -m "Formalize ordered sector correction v2.75"
~~~

Branch: formal/dependent-origination-ordered-sector-correction-v275

Base: exact green v2.74 head.

---

### Task 3: v2.76 Bounded-Loss Filtration Algebra

**Files:**
- Create formal/KUOS/DependentOriginationBoundedLossFiltrationV2_76.lean
- Test /tmp/BoundedLossFiltrationV276Probe.lean

**Interfaces:**
- Produces LossyUnaryOperation, LossyBinaryOperation, flat_map, flat_iterate.

- [ ] **Step 1: Implement explicit fixed-loss operations**

~~~lean
import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationBoundedLossFiltrationV2_76

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration

universe u

structure LossyUnaryOperation
    {D : Type u} (F : ObstructionFiltration D) where
  op : D → D
  loss : ℕ
  map_order :
    ∀ n d,
      F.OrderAtLeast (n + loss) d →
      F.OrderAtLeast n (op d)

structure LossyBinaryOperation
    {D : Type u} (F : ObstructionFiltration D) where
  op : D → D → D
  loss : ℕ
  map_order :
    ∀ n a b,
      F.OrderAtLeast (n + loss) a →
      F.OrderAtLeast (n + loss) b →
      F.OrderAtLeast n (op a b)

namespace LossyUnaryOperation

variable {D : Type u} {F : ObstructionFiltration D}

theorem flat_map
    (O : LossyUnaryOperation F) {d : D}
    (hd : F.Flat d) :
    F.Flat (O.op d) := by
  intro n
  exact O.map_order n d (hd (n + O.loss))

theorem flat_iterate
    (O : LossyUnaryOperation F) {d : D}
    (hd : F.Flat d) (k : ℕ) :
    F.Flat ((O.op^[k]) d) := by
  induction k with
  | zero =>
      simpa using hd
  | succ k ih =>
      simpa [Function.iterate_succ_apply] using O.flat_map ih

end LossyUnaryOperation

namespace LossyBinaryOperation

variable {D : Type u} {F : ObstructionFiltration D}

theorem flat_map
    (O : LossyBinaryOperation F) {a b : D}
    (ha : F.Flat a) (hb : F.Flat b) :
    F.Flat (O.op a b) := by
  intro n
  exact O.map_order n a b
    (ha (n + O.loss))
    (hb (n + O.loss))

end LossyBinaryOperation
end KUOS.DependentOriginationBoundedLossFiltrationV2_76
~~~

- [ ] **Step 2: Probe arbitrary finite iteration and a nonzero loss**

Verify flatness survives one unary operation, one binary operation, and k unary iterations. Every proof must request the source at n + loss.

- [ ] **Step 3: Strict compile, scan, commit**

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationBoundedLossFiltrationV2_76.lean
lake env lean /tmp/BoundedLossFiltrationV276Probe.lean
if grep -nE '\b(sorry|admit|axiom)\b'   formal/KUOS/DependentOriginationBoundedLossFiltrationV2_76.lean; then
  exit 1
fi
git add formal/KUOS/DependentOriginationBoundedLossFiltrationV2_76.lean
git commit -m "Formalize bounded-loss filtration algebra v2.76"
~~~

Branch: formal/dependent-origination-bounded-loss-filtration-v276

Base: exact green v2.75 head.

---

### Task 4: v2.77 Cofinal Correction Schedules

**Files:**
- Create formal/KUOS/DependentOriginationCofinalCorrectionV2_77.lean
- Test /tmp/CofinalCorrectionV277Probe.lean

**Interfaces:**
- Produces CofinalOrderSchedule, cofinalOrderSchedule_add_loss, CofinalCorrectionTower, exists_stage_orderAtLeast, exists_stage_orderAtLeast_with_loss.

- [ ] **Step 1: Implement unbounded cofinality and explicit tower data**

~~~lean
import KUOS.DependentOriginationCorrectionGainV2_71

namespace KUOS.DependentOriginationCofinalCorrectionV2_77

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationCorrectionGainV2_71

universe u v

def CofinalOrderSchedule (g : ℕ → ℕ) : Prop :=
  ∀ N, ∃ j, N ≤ g j

theorem cofinalOrderSchedule_add_loss
    {g : ℕ → ℕ}
    (hg : CofinalOrderSchedule g)
    (loss N : ℕ) :
    ∃ j, N + loss ≤ g j :=
  hg (N + loss)

structure CofinalCorrectionTower
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    (Step : State → State → Prop)
    (g : ℕ → ℕ) where
  state : ℕ → State
  invariant : ∀ j, P.invariant (state j)
  step : ∀ j, Step (state j) (state (j + 1))
  order : ∀ j, F.OrderAtLeast (g j) (P.residual (state j))
  cofinal : CofinalOrderSchedule g

namespace CofinalCorrectionTower

theorem exists_stage_orderAtLeast
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (N : ℕ) :
    ∃ j, F.OrderAtLeast N (P.residual (T.state j)) := by
  obtain ⟨j, hj⟩ := T.cofinal N
  exact ⟨j, F.orderAtLeast_mono hj (T.order j)⟩

theorem exists_stage_orderAtLeast_with_loss
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (loss N : ℕ) :
    ∃ j,
      N + loss ≤ g j ∧
      F.OrderAtLeast (g j) (P.residual (T.state j)) := by
  obtain ⟨j, hj⟩ := cofinalOrderSchedule_add_loss T.cofinal loss N
  exact ⟨j, hj, T.order j⟩

end CofinalCorrectionTower
end KUOS.DependentOriginationCofinalCorrectionV2_77
~~~

- [ ] **Step 2: Truth-test non-monotone cofinal semantics**

Use a schedule with arbitrarily high even-index values and repeated return to zero at odd indices. Prove CofinalOrderSchedule. Do not add an eventual-order theorem.

- [ ] **Step 3: Strict compile, commit, exact-head validate**

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationCofinalCorrectionV2_77.lean
lake env lean /tmp/CofinalCorrectionV277Probe.lean
git add formal/KUOS/DependentOriginationCofinalCorrectionV2_77.lean
git commit -m "Formalize cofinal correction schedules v2.77"
~~~

Branch: formal/dependent-origination-cofinal-correction-v277

Base: exact green v2.76 head.

---

### Task 5: v2.78 Tower Realization and Residual Stability

**Files:**
- Create formal/KUOS/DependentOriginationTowerRealizationV2_78.lean
- Create formal/KUOS/DependentOriginationResidualStabilityV2_78.lean
- Test /tmp/TowerRealizationV278Probe.lean

**Interfaces:**
- Produces TowerRealization, ResidualStabilityTransfer, realized_invariant_and_flat, realized_residual_eq_of_separatedAt.

- [ ] **Step 1: Implement realization data only**

~~~lean
import KUOS.DependentOriginationCofinalCorrectionV2_77

namespace KUOS.DependentOriginationTowerRealizationV2_78

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationCorrectionGainV2_71
open KUOS.DependentOriginationCofinalCorrectionV2_77

universe u v

structure TowerRealization
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop) where
  limitState : State
  invariant_limit : P.invariant limitState
  approximation :
    ∀ j, Approx (g j) (T.state j) limitState

end KUOS.DependentOriginationTowerRealizationV2_78
~~~

Directly compile this file. It must expose no flatness theorem.

- [ ] **Step 2: Implement fixed-loss residual transfer**

~~~lean
import KUOS.DependentOriginationTowerRealizationV2_78

namespace KUOS.DependentOriginationResidualStabilityV2_78

open KUOS.DependentOriginationFilteredObstructionCoreV2_70
open KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration
open KUOS.DependentOriginationCorrectionGainV2_71
open KUOS.DependentOriginationCofinalCorrectionV2_77
open KUOS.DependentOriginationTowerRealizationV2_78

universe u v

structure ResidualStabilityTransfer
    {State : Type u} {D : Type v}
    {F : ObstructionFiltration D}
    {P : ResidualProblem State D}
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop)
    (L : TowerRealization T Approx) where
  loss : ℕ
  transfer :
    ∀ n j,
      n + loss ≤ g j →
      F.OrderAtLeast (g j) (P.residual (T.state j)) →
      Approx (g j) (T.state j) L.limitState →
      F.OrderAtLeast n (P.residual L.limitState)

theorem realized_invariant_and_flat
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop)
    (L : TowerRealization T Approx)
    (S : ResidualStabilityTransfer T Approx L) :
    P.invariant L.limitState ∧
      F.Flat (P.residual L.limitState) := by
  refine ⟨L.invariant_limit, ?_⟩
  intro n
  obtain ⟨j, hj⟩ := cofinalOrderSchedule_add_loss T.cofinal S.loss n
  exact S.transfer n j hj (T.order j) (L.approximation j)

theorem realized_residual_eq_of_separatedAt
    {State : Type u} {D : Type v}
    (F : ObstructionFiltration D)
    (P : ResidualProblem State D)
    {Step : State → State → Prop}
    {g : ℕ → ℕ}
    (T : CofinalCorrectionTower F P Step g)
    (Approx : ℕ → State → State → Prop)
    (L : TowerRealization T Approx)
    (S : ResidualStabilityTransfer T Approx L)
    {e : D}
    (hsep : F.SeparatedAt e) :
    P.residual L.limitState = e := by
  exact F.flat_eq_of_separatedAt hsep
    (realized_invariant_and_flat F P T Approx L S).2

end KUOS.DependentOriginationResidualStabilityV2_78
~~~

- [ ] **Step 3: Probe the authority separation**

The probe assumes T, Approx, and L. It must be unable to state a generic flatness result from L alone; the successful theorem invocation must additionally take S : ResidualStabilityTransfer T Approx L.

- [ ] **Step 4: Strict compile, commit both files**

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationTowerRealizationV2_78.lean
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationResidualStabilityV2_78.lean
lake env lean /tmp/TowerRealizationV278Probe.lean
git add   formal/KUOS/DependentOriginationTowerRealizationV2_78.lean   formal/KUOS/DependentOriginationResidualStabilityV2_78.lean
git commit -m "Separate tower realization and residual stability v2.78"
~~~

Branch: formal/dependent-origination-tower-realization-v278

Base: exact green v2.77 head.

---

### Task 6: v2.79 Relative Correction and Corrective Descent

**Files:**
- Create formal/KUOS/DependentOriginationRelativeCorrectionV2_79.lean
- Test /tmp/RelativeCorrectionV279Probe.lean

**Interfaces:**
- Produces RelativeCorrectionProblem, ExteriorExact, RelativeStep, exteriorExact_of_relativeStep, CorrectiveDescentData, globalRealizable_of_correctiveDescent.

- [ ] **Step 1: Implement region-relative preservation**

~~~lean
import KUOS.DependentOriginationResidualStabilityV2_78

namespace KUOS.DependentOriginationRelativeCorrectionV2_79

universe u r

structure RelativeCorrectionProblem
    (State : Type u) (Region : Type r) where
  active : Region → Prop
  exactAt : Region → State → Prop
  compatible : State → Prop

namespace RelativeCorrectionProblem

variable {State : Type u} {Region : Type r}

def ExteriorExact
    (P : RelativeCorrectionProblem State Region)
    (x : State) : Prop :=
  ∀ region, ¬ P.active region → P.exactAt region x

end RelativeCorrectionProblem

def RelativeStep
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region)
    (Step : State → State → Prop)
    (x y : State) : Prop :=
  Step x y ∧
  (∀ region,
    ¬ P.active region →
    P.exactAt region x →
    P.exactAt region y) ∧
  (P.compatible x → P.compatible y)

theorem exteriorExact_of_relativeStep
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region)
    (Step : State → State → Prop)
    {x y : State}
    (hx : P.ExteriorExact x)
    (hxy : RelativeStep P Step x y) :
    P.ExteriorExact y := by
  intro region houtside
  exact hxy.2.1 region houtside (hx region houtside)

structure CorrectiveDescentData
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region) where
  globalRealizable : State → Prop
  descend :
    ∀ x,
      P.ExteriorExact x →
      P.compatible x →
      globalRealizable x

theorem globalRealizable_of_correctiveDescent
    {State : Type u} {Region : Type r}
    (P : RelativeCorrectionProblem State Region)
    (D : CorrectiveDescentData P)
    {x : State}
    (hexterior : P.ExteriorExact x)
    (hcompat : P.compatible x) :
    D.globalRealizable x :=
  D.descend x hexterior hcompat

end KUOS.DependentOriginationRelativeCorrectionV2_79
~~~

- [ ] **Step 2: Probe conditional exterior preservation**

Use two regions, one active and one exterior. The successful proof must require RelativeStep; bare Step must not suffice.

- [ ] **Step 3: Strict compile, commit, validate**

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationRelativeCorrectionV2_79.lean
lake env lean /tmp/RelativeCorrectionV279Probe.lean
git add formal/KUOS/DependentOriginationRelativeCorrectionV2_79.lean
git commit -m "Formalize relative corrective descent v2.79"
~~~

Branch: formal/dependent-origination-relative-correction-v279

Base: exact green v2.78 head.

---

### Task 7: v2.80 Generated-Holonomy Correctability

**Files:**
- Create formal/KUOS/DependentOriginationGeneratedHolonomyCorrectabilityV2_80.lean
- Test /tmp/GeneratedHolonomyCorrectabilityV280Probe.lean

**Interfaces:**
- Consumes v2.74 correction realization and v2.73 filtered generated holonomy.
- Produces GeneratedHolonomyCorrectable, GeneratedHolonomyRobustlyCorrectable, GeneratedHolonomyHardObstruction, generatedHolonomy_correctable_of_robust, generatedHolonomy_not_flat_of_ne_of_separatedAt, generatedHolonomy_hard_of_uncorrectable.

- [ ] **Step 1: Define the three distinct predicates**

Use the exact current universe style:

~~~lean
(R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))
~~~

For the automorphism carrier use:

~~~lean
((freePathEvaluator W R D).map p ≅
  (freePathEvaluator W R D).map p)
~~~

Define:

~~~lean
GeneratedHolonomyCorrectable
GeneratedHolonomyRobustlyCorrectable
GeneratedHolonomyHardObstruction
~~~

as direct specializations of CorrectableAt, RobustCorrectionData.robustAt, and HardObstructionAt to generatedHolonomy W R D gamma.

- [ ] **Step 2: Add only one-way theorems**

Required conclusions:

~~~lean
robust generated holonomy
  -> GeneratedHolonomyCorrectable

generatedHolonomy W R D gamma != Iso.refl _
+ F.SeparatedAt (Iso.refl _)
  -> not FilteredGeneratedHolonomyFlat W R D F gamma

not GeneratedHolonomyCorrectable
  -> GeneratedHolonomyHardObstruction
~~~

Forbidden conclusions:

~~~text
generatedHolonomy != refl -> GeneratedHolonomyHardObstruction
not FilteredGeneratedHolonomyFlat -> GeneratedHolonomyHardObstruction
~~~

- [ ] **Step 3: Probe the logical separation**

The probe separately invokes the non-flat theorem from nontriviality + separatedness and the hard-obstruction theorem from explicit uncorrectability. It must contain no theorem connecting those premises.

- [ ] **Step 4: Strict compile, scan, commit**

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true   env lean formal/KUOS/DependentOriginationGeneratedHolonomyCorrectabilityV2_80.lean
lake env lean /tmp/GeneratedHolonomyCorrectabilityV280Probe.lean
if grep -nE '\b(sorry|admit|axiom)\b'   formal/KUOS/DependentOriginationGeneratedHolonomyCorrectabilityV2_80.lean; then
  exit 1
fi
git add formal/KUOS/DependentOriginationGeneratedHolonomyCorrectabilityV2_80.lean
git commit -m "Classify generated-holonomy correctability v2.80"
~~~

Branch: formal/dependent-origination-generated-holonomy-correctability-v280

Base: exact green v2.79 head.

---

### Task 8: Whole-Stack Verification and Promotion

**Files:**
- Verify all eight new production files.
- Test /tmp/ConstructiveDependentOriginationAxiomsV280.lean

- [ ] **Step 1: Create an axiom-footprint probe**

Print axioms for:

~~~text
RobustCorrectionData.correctableAt
OrderedSectorCorrector.runFullCycle_order
LossyUnaryOperation.flat_map
CofinalCorrectionTower.exists_stage_orderAtLeast_with_loss
realized_invariant_and_flat
exteriorExact_of_relativeStep
generatedHolonomy_not_flat_of_ne_of_separatedAt
~~~

Unexpected project-specific axioms are blockers.

- [ ] **Step 2: Strict-build every new module**

~~~bash
for file in   formal/KUOS/DependentOriginationCorrectionRealizationV2_74.lean   formal/KUOS/DependentOriginationOrderedSectorCorrectionV2_75.lean   formal/KUOS/DependentOriginationBoundedLossFiltrationV2_76.lean   formal/KUOS/DependentOriginationCofinalCorrectionV2_77.lean   formal/KUOS/DependentOriginationTowerRealizationV2_78.lean   formal/KUOS/DependentOriginationResidualStabilityV2_78.lean   formal/KUOS/DependentOriginationRelativeCorrectionV2_79.lean   formal/KUOS/DependentOriginationGeneratedHolonomyCorrectabilityV2_80.lean
do
  lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true env lean "$file" || exit 1
done
~~~

- [ ] **Step 3: Forbidden-token scan and full formal build**

~~~bash
if grep -nE '\b(sorry|admit|axiom)\b'   formal/KUOS/DependentOriginationCorrectionRealizationV2_74.lean   formal/KUOS/DependentOriginationOrderedSectorCorrectionV2_75.lean   formal/KUOS/DependentOriginationBoundedLossFiltrationV2_76.lean   formal/KUOS/DependentOriginationCofinalCorrectionV2_77.lean   formal/KUOS/DependentOriginationTowerRealizationV2_78.lean   formal/KUOS/DependentOriginationResidualStabilityV2_78.lean   formal/KUOS/DependentOriginationRelativeCorrectionV2_79.lean   formal/KUOS/DependentOriginationGeneratedHolonomyCorrectabilityV2_80.lean
then
  exit 1
fi

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
~~~

Expected: PASS.

- [ ] **Step 4: Exact-head governance for every stacked PR**

For each v2.74-v2.80 unit require:

~~~text
behind_by = 0
merge base = fresh base SHA
changed files = only the mathematical unit
PR remains Draft during validation
Strict Lean formal validation = completed/success
final governance summary = completed/success
~~~

If a base branch moved, integrate the fresh base and rerun direct Lean plus exact-head CI. Never reuse green evidence from an older head.

- [ ] **Step 5: Promote complete units in order**

Promotion order:

~~~text
v2.74 correction realization
v2.75 ordered sector correction
v2.76 bounded-loss filtration
v2.77 cofinal correction
v2.78 realization + residual stability
v2.79 relative correction
v2.80 generated-holonomy correctability
~~~

At each boundary fresh-observe base/head and diff scope before marking ready or merging.

- [ ] **Step 6: Keep README/ROADMAP promotion separate**

Only after v2.80 is merged into the selected theorem line may a docs-only unit describe:

~~~text
Constructive Dependent Origination =
explicit relation
+ obstruction
+ correctability
+ ordered correction
+ bounded loss
+ cofinal iteration
+ realization
+ relative descent
~~~

The docs must retain:

~~~text
non-flat != uncorrectable
formal mathematical presentation != historical-philosophical identity
~~~

## Self-Review Result

- Spec coverage: v2.74 through v2.80 map one-to-one to Tasks 1-7; governance is Task 8.
- Authority boundaries remain separate: correction image, finite selected correction, cofinal tower, realized limit, residual transfer, flatness, exactness, hard obstruction.
- v2.74 explicitly demonstrates correctable + non-flat.
- v2.75 preserves already-improved sectors at their stronger order.
- v2.77 uses unbounded cofinality, not eventual domination.
- v2.78 does not obtain flatness from realization alone.
- v2.79 requires explicit exterior preservation and descent data.
- v2.80 has no converse from nontrivial/non-flat to hard obstruction.
- All five Review Focus risks have a named test or theorem gate.
- No unfinished implementation marker or unspecified theorem body remains.
