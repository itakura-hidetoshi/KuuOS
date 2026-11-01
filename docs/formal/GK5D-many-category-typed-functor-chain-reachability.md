# F112-P94D3GK5D — Genuine typed many-category finite functor chains, normalization and exact reachability

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2903](https://github.com/itakura-hidetoshi/KuuOS/pull/2903) — MERGED  
**Theorem squash / canonical main HEAD at theorem merge:** `cedb7970477393d625f00fc4e4cd5941c4e824f1`  
**Final theorem source HEAD:** `143c4e379c7dc4b41533411f510ef25c4ccad2aa`  
**Test-merge SHA:** `70db965347e98854e3a4eee591e647a980b13aca`  
**Matching source/test-merge Git tree:** `08b422bbd30ed335858eaf07f9753e67687b9f4f`  
**Exact-source CI:** [#41330331080](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41330331080) — SUCCESS (Strict Lean 3825/3825, Independent Kuu, Workflow integrity, Governance terminal).

## Canonical Lean source and technical scope

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5DTypedManyCategoryFunctorChains.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5DTypedManyCategoryFunctorChains.lean)

Pinned **Lean v4.30.0-rc2**, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Exactly one additive theorem source; previously merged GK5A/GK5B/GK5C proof files, original F45/AH witness structures, public **107 roots**, and all pinned dependency files remain unchanged. No Gray reconstruction. Protected Lean-4.31 validation-only PR #1558 remains Draft/open/unmerged.

## From a fixed endofunctor category to many different categories

GK5A/GK5B/GK5C treated genuine endofunctor trees `T ⥤ T` over one fixed `T`. GK5D instead fixes an **index type** `I` and a family of genuinely bundled Mathlib categories

`C : I → Cat.{vT,uT}`

and introduces two *source-and-target-indexed* inductive presentations:

- `NativeGK5DTypedWord C i j`: a dependently typed finite ordered word of composable genuine functors, with `empty i` and `cons (F : C i ⥤ C j) (rest : Word C j k)`.
- `NativeGK5DTypedTree C i j`: the typed binary presentation, with `unit i`, `atom (F : C i ⥤ C j)`, and `paste : Tree C i j → Tree C j k → Tree C i k`.

The intermediate category is checked by Lean's type system, not by a separate unproved well-formedness predicate. `Cat` packages the categories, but the denotations of nodes are the underlying **actual Mathlib functors** and **whole Mathlib NatIso** values. The theorem does not identify unrelated categories by definition.

### 1. Typed ordered words and canonical evaluation

`nativeGK5DWordAppend`, `nativeGK5DWordComposite`, `nativeGK5DTreeComposite`, `nativeGK5DTreeLeaves`, and `nativeGK5DTreeOfWord` give real type-preserving functor composition, ordered-leaf extraction, and canonical right-associated tree construction.

Theorems include

- `nativeGK5DWordAppend_assoc` and `nativeGK5DWordAppend_empty`;
- `nativeGK5DWordComposite_append`;
- `nativeGK5DTreeComposite_eq_word`: the *whole composite* functor equals the canonical typed word composite;
- `nativeGK5DTreeComposite_eq_of_leaves`: equal actual typed words imply equal whole functors, **not conversely**;
- `nativeGK5DTreeOfWord_leaves` and `nativeGK5DTreeOfWord_eval`.

The exact category boundary and every non-identity leaf functor remain in the dependently typed word.

### 2. Actual heterogeneous associator/unitor rewrite steps

`NativeGK5DTypedStep` has constructors for the true Mathlib `Functor.associator`, `Functor.leftUnitor`, `Functor.rightUnitor`, and left/right whiskering; `NativeGK5DTypedPath` keeps finite step evidence, identities, inverses and composition.

`nativeGK5DStepIso` and `nativeGK5DPathIso` interpret each proof-relevant path by actual whole Mathlib natural isomorphisms. The whole-functor equality witnesses `nativeGK5DStepEq` and `nativeGK5DPathEq` are separately retained.

`nativeGK5DStepIso_eqToIso` and `nativeGK5DPathIso_eqToIso` prove that **the true constructed whole NatIso equals the canonical eqToIso of the actual whole-functor equality**. Consequently, `nativeGK5DPath_independent` proves equality of the entire actual NatIso values of arbitrary two same-typed-endpoint paths.

The three-stage `nativeGK5DThreeStage_associator` verifies the genuine Mathlib NatIso even when the successive categories are distinct.

### 3. Constructive arbitrary-finite-depth typed normalization

`nativeGK5DPathWhiskerLeft` and `nativeGK5DPathWhiskerRight` lift whole rewrite paths under typed outer contexts. The recursive `nativeGK5DAppendPath` uses the true left unitor for an empty first word, and a real associator plus genuine left whiskering at the nonempty recursive step.

`nativeGK5DNormalizePath` constructs, **for every** `t : NativeGK5DTypedTree C i j`, a genuine finite sequence of actual Mathlib structural steps from `t` to the canonical `TreeOfWord (TreeLeaves t)`. It uses identity paths for units, the inverse real right unitor for atoms, and two recursive whiskerings followed by canonical append for a paste node.

`nativeGK5DNormalizePath_iso_eq_canonical` identifies the constructed normalization NatIso with the canonical whole-functor equality **after genuine terminal eqToIso transport**.

### 4. Exact typed reachability and nonvacuous coherence

The main result, `nativeGK5DReachable_iff_sameLeaves`, proves for **any same-typed endpoints** `a b : Tree C i j`

`Nonempty (NativeGK5DTypedPath C a b) ↔ TreeLeaves a = TreeLeaves b`.

Forward direction uses `nativeGK5DStepLeaves` and `nativeGK5DPathLeaves`, preservation of the entire ordered typed word by each genuine step and path. Reverse direction uses the *constructed* normalizations of both trees, the given word equality as endpoint transport, and the reversed second path to produce a real proof-relevant path `a → b`.

`nativeGK5DPath_eq_canonical_of_path` proves every real path agrees with this *specific constructed normal-form comparison path* as an actual whole NatIso. No arbitrary higher cell is postulated.

### 5. Lean4 dependent-elaboration errors and exact repair

The initial proof of `nativeGK5DPathIso_eqToIso` using tactic `induction p` left dependent source/target tree indices opaque in the `refl` and `basic` cases. Changing to `induction p generalizing a b` is invalid because the induction target itself depends on those indices. The successful Lean4-compatible repair used **constructor-pattern recursion over the complete indexed motive**, and then explicitly simplified the definitional equation lemmas for `nativeGK5DPathIso` and `nativeGK5DPathEq` in the base cases. All dependent signatures, target statements and axioms were retained unchanged.

## Exact-source proof certificate

- **Final source**: `143c4e379c7dc4b41533411f510ef25c4ccad2aa`.
- **GitHub test-merge**: `70db965347e98854e3a4eee591e647a980b13aca`.
- **Independent Git object verification**: both commits have identical tree `08b422bbd30ed335858eaf07f9753e67687b9f4f`.
- [CI #41330331080](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41330331080): **Strict Lean 3825/3825 SUCCESS; Independent Kuu SUCCESS; Workflow integrity SUCCESS; Governance terminal SUCCESS**.
- **16 public audited declarations, 16 `#print axioms` checks**: only standard `propext`, `Classical.choice`, `Quot.sound`; **sorryAx = 0**; changed Lean error/warning **0/0**.
- The merged theorem squash is `cedb7970477393d625f00fc4e4cd5941c4e824f1`. This separate documentation follow-up is docs-only; Strict Lean should be **SKIPPED** rather than rerun.

## Exact obstruction boundary and possible next GK5E

The theorem concerns **arbitrary finite** trees of *composable functors between a family of different categories that share a fixed universe pair* `(vT,uT)`. It does not cover different universe levels varying along a chain, arbitrary dependent source schemas, or semantic equivalence between distinct typed leaf words.

In particular, it does NOT establish unconditional original F45 source-category faithfulness, source-Q category axioms, raw F54/F55/P92B Type-valued higher-cell constructors, attainability of arbitrary integer matrices, a global Gray category, or unbounded higher hyperdescent. GK4BM's arbitrary chosen inverse `Q_T` and GK4BP's explicit `P_T` remain different presentations connected only by GK4BQ's genuine NatIso `κ_T`; cross-category GK4BM/GK4BU chosen-inverse naturality is NOT a GK5D theorem.

A next, separately typed GK5E could study naturality of chosen-inverse comparisons under heterogeneous target functors, subject to explicit source/target compatibility assumptions and true two-endpoint eqToIso transports. The existing user-requested strict 空 center and independent Kuu presentation boundaries remain unchanged.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
