# Filtered Obstruction Core v2.70 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the minimal theorem-backed decreasing-filtration core that distinguishes finite obstruction order, flatness, and separated exactness without importing higher-localization or PDE-specific structure.

**Architecture:** Create one independent Lean module under `formal/KUOS/`. The module depends only on Mathlib, defines a decreasing `ℕ`-indexed family of subsets, and proves the exact monotonicity/separatedness lemmas needed by v2.71–v2.73. It does not modify v2.69, does not add an umbrella import, and does not introduce convergence, group, topology, or completion assumptions.

**Tech Stack:** Lean `leanprover/lean4:v4.30.0-rc2`; Mathlib exact revision `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; Lake; GitHub exact-head CI.

**Spec:** `docs/superpowers/specs/2026-09-15-filtered-residual-hyperdescent-design.md`

## Global Constraints

- Stack from the reviewed design branch, which itself is stacked on v2.69 exact proof head `940c3b8f164ac35e49e6fcf2532aef9bba3c2eff`.
- Keep PR #1651 / v2.69 files unchanged.
- Lean toolchain is exactly `leanprover/lean4:v4.30.0-rc2`.
- Mathlib revision is exactly `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
- Additive/tighten-only: no weakening or reinterpretation of existing theorems.
- No `sorry`, `admit`, new `axiom`, placeholder theorem authority, or hidden convergence assumption.
- `Flat` must not imply equality without an explicit `SeparatedAt` hypothesis.
- `SeparatedAt F e` must include that `e` itself is flat.
- v2.70 must not require `Group`, `Monoid`, `TopologicalSpace`, `MetricSpace`, completeness, or generated-holonomy imports.
- Do not modify `formal/KuuOSFormalV0_69.lean`; umbrella/version changes are outside this unit.

---

## File Structure

- Create `formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean`
  - Owns the generic filtration structure and all v2.70 predicates/theorems.
- No persistent test file is added. TDD compile probes are written to `/tmp` and import the final module.
- No README, ROADMAP, v2.68, or v2.69 file is changed in this unit.

---

### Task 1: Establish the decreasing-filtration API and order monotonicity

**Files:**
- Create: `formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean`
- Test: `/tmp/FilteredObstructionCoreV270Probe.lean` (temporary, not committed)

**Interfaces:**
- Consumes: Mathlib `Set`, `Antitone`, `ℕ`, and ordinary proposition logic.
- Produces:
  - `KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration`
  - `ObstructionFiltration.OrderAtLeast`
  - `ObstructionFiltration.Flat`
  - `ObstructionFiltration.orderAtLeast_mono`
  - `ObstructionFiltration.flat_orderAtLeast`

- [ ] **Step 1: Write the failing compile probe before the module exists**

Create `/tmp/FilteredObstructionCoreV270Probe.lean` with:

```lean
import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationFilteredObstructionCoreV2_70

open Set

universe u

namespace ObstructionFiltration

variable {D : Type u}

example (F : ObstructionFiltration D) {m n : ℕ} {d : D}
    (hmn : m ≤ n) (hd : F.OrderAtLeast n d) :
    F.OrderAtLeast m d := by
  exact orderAtLeast_mono F hmn hd

example (F : ObstructionFiltration D) {d : D}
    (hd : F.Flat d) (n : ℕ) : F.OrderAtLeast n d := by
  exact flat_orderAtLeast F hd n

end ObstructionFiltration
end KUOS.DependentOriginationFilteredObstructionCoreV2_70
```

- [ ] **Step 2: Run the probe and verify it fails for the intended reason**

Run:

```bash
lake env lean /tmp/FilteredObstructionCoreV270Probe.lean
```

Expected: failure because module `KUOS.DependentOriginationFilteredObstructionCoreV2_70` does not yet exist. Do not proceed if the failure is instead a toolchain or dependency-resolution error.

- [ ] **Step 3: Implement the minimal structure and first two predicates/theorems**

Create `formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean` with this exact initial content:

```lean
import Mathlib

namespace KUOS.DependentOriginationFilteredObstructionCoreV2_70

open Set

universe u

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

/-- The defect lies in every filtration level.  This is not equality to an
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

end ObstructionFiltration
end KUOS.DependentOriginationFilteredObstructionCoreV2_70
```

- [ ] **Step 4: Compile the module directly**

Run:

```bash
lake env lean formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean
```

Expected: PASS with no errors and no warnings promoted by the repository toolchain.

- [ ] **Step 5: Re-run the probe**

Run:

```bash
lake env lean /tmp/FilteredObstructionCoreV270Probe.lean
```

Expected: PASS.

- [ ] **Step 6: Commit the independently useful core**

```bash
git add formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean
git commit -m "Formalize filtered obstruction order core v2.70"
```

---

### Task 2: Add separatedness and the hard-obstruction implication

**Files:**
- Modify: `formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean`
- Test: `/tmp/FilteredObstructionSeparatedV270Probe.lean` (temporary, not committed)

**Interfaces:**
- Consumes:
  - `ObstructionFiltration.Flat`
  - exact defect `e : D`
- Produces:
  - `ObstructionFiltration.SeparatedAt`
  - `ObstructionFiltration.separatedAt_exact_flat`
  - `ObstructionFiltration.flat_eq_of_separatedAt`
  - `ObstructionFiltration.not_flat_of_ne_of_separatedAt`

- [ ] **Step 1: Write the failing separatedness probe**

Create `/tmp/FilteredObstructionSeparatedV270Probe.lean` with:

```lean
import KUOS.DependentOriginationFilteredObstructionCoreV2_70

namespace KUOS.DependentOriginationFilteredObstructionCoreV2_70

universe u

namespace ObstructionFiltration

variable {D : Type u}

example (F : ObstructionFiltration D) {e : D}
    (hsep : F.SeparatedAt e) : F.Flat e := by
  exact separatedAt_exact_flat F hsep

example (F : ObstructionFiltration D) {d e : D}
    (hsep : F.SeparatedAt e) (hd : F.Flat d) : d = e := by
  exact flat_eq_of_separatedAt F hsep hd

example (F : ObstructionFiltration D) {d e : D}
    (hsep : F.SeparatedAt e) (hne : d ≠ e) : ¬ F.Flat d := by
  exact not_flat_of_ne_of_separatedAt F hsep hne

end ObstructionFiltration
end KUOS.DependentOriginationFilteredObstructionCoreV2_70
```

- [ ] **Step 2: Verify the new probe fails because the separatedness API is absent**

Run:

```bash
lake env lean /tmp/FilteredObstructionSeparatedV270Probe.lean
```

Expected: failure on unknown `SeparatedAt` / separatedness theorem names, while the imported v2.70 module itself resolves successfully.

- [ ] **Step 3: Add the exact separatedness definition and theorems**

Append inside `namespace ObstructionFiltration`, before its closing `end`:

```lean
/-- The distinguished exact defect `e` is itself flat and is the unique flat
defect.  Requiring `F.Flat e` prevents vacuous separatedness. -/
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
```

- [ ] **Step 4: Compile the module and separatedness probe**

Run:

```bash
lake env lean formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean
lake env lean /tmp/FilteredObstructionSeparatedV270Probe.lean
```

Expected: both PASS.

- [ ] **Step 5: Commit the separatedness theorem boundary**

```bash
git add formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean
git commit -m "Prove separated flat obstruction criterion v2.70"
```

---

### Task 3: Verify theorem authority, forbidden tokens, and repository build

**Files:**
- Verify only: `formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean`
- Test: `/tmp/FilteredObstructionAxiomsV270.lean` (temporary, not committed)

**Interfaces:**
- Consumes: all Task 1–2 declarations.
- Produces: exact-head compile/build evidence; no new theorem API.

- [ ] **Step 1: Create an axiom-footprint probe**

Create `/tmp/FilteredObstructionAxiomsV270.lean`:

```lean
import KUOS.DependentOriginationFilteredObstructionCoreV2_70

#print axioms KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration.orderAtLeast_mono
#print axioms KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration.flat_orderAtLeast
#print axioms KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration.separatedAt_exact_flat
#print axioms KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration.flat_eq_of_separatedAt
#print axioms KUOS.DependentOriginationFilteredObstructionCoreV2_70.ObstructionFiltration.not_flat_of_ne_of_separatedAt
```

- [ ] **Step 2: Run direct strict compilation**

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  env lean formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean
```

Expected: PASS.

- [ ] **Step 3: Check the theorem axiom footprint**

```bash
lake env lean /tmp/FilteredObstructionAxiomsV270.lean
```

Expected: no new/custom axiom dependency. These elementary theorems should require no nonstandard axioms; any unexpected project-specific axiom is a blocker.

- [ ] **Step 4: Scan the new theorem file for forbidden proof tokens**

```bash
if grep -nE '\b(sorry|admit|axiom)\b' \
  formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean; then
  echo "forbidden proof token found"
  exit 1
fi
```

Expected: exit 0 with no matches.

- [ ] **Step 5: Build the Lean library with warnings and sorry promoted to errors**

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

Expected: PASS.

- [ ] **Step 6: Confirm the implementation diff is isolated**

```bash
git diff --name-only design/filtered-residual-hyperdescent-v270-v273...HEAD
```

Expected exactly:

```text
formal/KUOS/DependentOriginationFilteredObstructionCoreV2_70.lean
```

If any v2.68/v2.69 or umbrella file appears, stop and remove that unrelated change.

- [ ] **Step 7: Push the exact implementation head and open a Draft stacked PR**

Use branch:

```text
formal/dependent-origination-filtered-obstruction-core-v270
```

with PR base:

```text
design/filtered-residual-hyperdescent-v270-v273
```

PR title:

```text
Formalize filtered obstruction core v2.70
```

PR body must state:

```text
Mathematical unit:
- generic decreasing obstruction filtration
- finite order and flatness predicates
- separated exact-defect criterion
- nontrivial defect in a separated filtration is not flat

Boundaries:
- no v2.69 changes
- no convergence/completion claims
- no algebraic/topological assumptions
- no generated-holonomy bridge yet
- no umbrella/version promotion
```

- [ ] **Step 8: Require exact-head CI before any promotion**

Read the PR head SHA after push, then inspect GitHub Actions for that exact SHA. Promotion criteria are all of:

```text
PR remains Draft during validation
head SHA observed exactly
KuuOS PR Governance Gate completed
conclusion = success
no unexpected changed files
```

Do not mark ready or merge in this task. v2.70 remains stacked/non-authoritative until upstream design and v2.69 authority are resolved.

---

## Self-Review Result

- **Spec coverage:** v2.70 Sections 4.1–4.4 are fully covered. v2.71–v2.73 are intentionally excluded and receive separate plans.
- **Authority boundary:** no theorem from v2.69 is modified or weakened; no umbrella promotion occurs.
- **Flat/trivial distinction:** encoded explicitly by requiring `SeparatedAt` for equality.
- **Vacuity check:** `SeparatedAt F e` includes `F.Flat e`.
- **Type consistency:** every probe uses exactly the declaration names and argument order produced by the implementation steps.
- **Placeholder scan:** no implementation placeholder is permitted; temporary probe failures are deliberate TDD steps, not theorem placeholders.
