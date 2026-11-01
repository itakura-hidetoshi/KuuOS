# F112-P94D3GK5F — Typed category-index relabeling, genuine rewrite-path NatIso transport and chosen-inverse coherence

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2907](https://github.com/itakura-hidetoshi/KuuOS/pull/2907) — MERGED  
**Theorem squash / canonical main HEAD at theorem merge:** `aa689ddac8c5f9036fe2a4185eb537882b9c44fb`  
**Final theorem source HEAD:** `994efa8b163cb621c07c4ec4a11e3d0639ee6b72`  
**Test-merge SHA:** `30acfe41a36d70b9a6dee86bdccfd4cc034d8b2b`  
**Identical source/test-merge Git tree:** `6373e48c6f2bdce6d367b1d916130ca100db3767`  
**Exact-source CI:** [#41347640760](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41347640760) — SUCCESS.

## One additive Lean source, unchanged originals

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5FIndexRelabelingCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5FIndexRelabelingCoherence.lean)

GK5D's dependent genuine category-indexed words/trees/structural paths and GK5E's arbitrary-choice inverse comparison are used with their original FULL signatures and assumptions. Only a new GK5F Lean source is added. Existing source-Q, original F45, attained-AH, compatible kernel subcategory, GK4BM arbitrary `Q_T`, GK4BP explicit `P_T`, GK4BQ's `κ_T : Q_T ≅ P_T`, GK4BT through GK5E, and all historical proofs are unchanged. In particular **`Q_T` is not identified definitionally with `P_T`**.

Pinned Lean **v4.30.0-rc2**, pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, original **107 public roots**, protected PR #1558 Draft/OPEN/unmerged, append-only / tighten-only / overwrite-forbidden / same-root.

## 1. Genuine typed index reclassification

For arbitrary index types `I`, `J`, an arbitrary function `f : I → J`, and a genuine fixed-universe-pair Mathlib category family `C : J → Cat.{vC,uC}`, define the actual pullback family

`f* C : I → Cat.{vC,uC}`, `(f* C)(i) = C(f(i))`.

This **relabels the category indices; it does NOT replace the actual underlying category at any position by an unrelated category**. There is no arbitrary categorical equivalence postulated between different category values, and `f` need not be injective or surjective.

`nativeGK5FWordReindex` constructs the complete typed finite word in `C` corresponding to one in `f* C`, changing every endpoint to `f(i)` while retaining each original genuine Mathlib atom functor. `nativeGK5FTreeReindex` constructs the analogous real binary tree, applying `f` to every source/intermediate/target index.

## 2. Exact whole-functor and normalization compatibility

The following whole dependent-typed equalities are proved for **all finite lengths/depths**:

- `nativeGK5FWordReindex_append`: reclassification preserves the genuine typed word concatenation.
- `nativeGK5FWordComposite_reindex`: the entire original and reclassified word evaluate to equal **whole Mathlib functors**.
- `nativeGK5FTreeComposite_reindex`: the complete binary-tree composite is exactly unchanged.
- `nativeGK5FTreeLeaves_reindex`: the entire **ordered dependent typed leaf word** is preserved.
- `nativeGK5FTreeOfWord_reindex`: right-associated canonical typed trees agree with reclassification.
- `nativeGK5FWordReindex_id` and `nativeGK5FTreeReindex_id`: reclassification by the identity map is the strict identity on dependent words and trees.
- `nativeGK5FWordReindex_comp` and `nativeGK5FTreeReindex_comp`: two successive reclassifications `I → J → K` agree, as literal typed source objects, with their composed reclassification.

These are literal Lean equalities in the respective well-typed dependent families. They are not equivalences of arbitrary unrelated category families.

## 3. Relabeling ACTUAL proof-relevant rewrite paths

`nativeGK5FStepReindex` transforms every genuine GK5D structural step: Mathlib associator, left/right unitor, left/right whiskering. `nativeGK5FPathReindex` transforms each proof-relevant finite path, retaining basic steps, identity, reverse and path concatenation.

The real WHOLE Mathlib NatIso denotations are transported at **both endpoints** by original, verified whole-functor equalities. Specifically, `nativeGK5FStepIso_reindex_transport` and `nativeGK5FPathIso_reindex_transport` prove that

`eqToIso(h_left.symm) ≪≫ Iso(reindex(path)) ≪≫ eqToIso(h_right) = Iso(path)`,

where `h_left` and `h_right` are the true whole-functor equalities `TreeComposite(reindex t) = TreeComposite(t)`. This is equality of **whole actual Mathlib NatIso values**, not of route labels or a fabricated higher cell.

The proof uses GK5D's already audited `StepIso_eqToIso`/`PathIso_eqToIso` and the actual pinned Mathlib `eqToIso_trans`. `nativeGK5FPath_reachable_reindex` transports actual path **evidence**, not just a proposition that one exists; `nativeGK5FSameLeaves_reachable_reindex` invokes GK5D's genuinely constructed normalization/reverse-normalization route before relabeling to give a nonvacuous actual path.

## 4. Whole chosen-inverse NatIso and whole NatTrans transport

`nativeGK5FChosenInverse_reindex_transport` states that GK5E's **recursively pasted** chosen-inverse whole NatIso for the reindexed tree and that for the original typed tree agree **after the two actual endpoint eqToIso transports**. It is an instance of the already validated GK5E whole equality-transport theorem with `h : TreeComposite(t) = TreeComposite(reindex(t))`.

Thus the arbitrary GK4BM chosen inverse `Q_{C(f i)}` and the separate GK4BP explicit `P_{C(f i)}` remain different presentations compared through the true GK4BQ `κ`; no definitional strictness is introduced.

`nativeGK5FChosenInverse_reindexedPath_square` proves the true GK5E chosen-inverse target NatTrans naturality square along **the actual reclassified finite rewrite path**, with source and target categories and whole transformations retained. It follows from the existing GK5E theorem applied to `nativeGK5FPathReindex` rather than from a hypothesized new high cell.

## 5. Exact Lean4 CI error diagnosis and repair

The initial version had **four Lean elaboration/tactic failures**:

1. In the `cons` case of the whole-word-composite induction, Lean inferred the TARGET category-index universe from another instance of `nativeGK5DWordComposite` and attempted to apply the target-family evaluator (indexed by `J`) to `xs` from the pullback family (indexed by `I`). An explicit named argument `(C := fun z : I => C (f z))` fixes the correct source indexed family while leaving the mathematical statement unchanged.
2. In the binary-tree-composite induction, the same `I` vs `J` index-universe ambiguity affected the right subtree. Explicit source-family arguments to both original-tree evaluators preserve the full source signatures.
3. After rewriting by the induction hypothesis in identity reclassification for words, a reflexive dependent constructor equality remained. It was closed with `rfl`.
4. The same residual reflexive constructor equality remained after rewriting in identity reclassification for trees, also closed with `rfl`.

No assumptions, theorem statements, earlier files or axioms were modified. No use of `sorry`. The final 19 audited declarations have no `sorryAx` dependencies.

## 6. Verified completion receipt

- Final exact-source HEAD `994efa8b163cb621c07c4ec4a11e3d0639ee6b72`.
- GitHub test-merge commit `30acfe41a36d70b9a6dee86bdccfd4cc034d8b2b`.
- Independently fetched, **matching** source and test-merge Git tree `6373e48c6f2bdce6d367b1d916130ca100db3767`.
- [CI run #41347640760](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41347640760): **Strict Lean 3827/3827 SUCCESS**; **Independent Kuu SUCCESS**; **Workflow integrity SUCCESS**; **Governance terminal SUCCESS**.
- **19 new audited declarations / 19 `#print axioms` results**: only standard `propext`, `Classical.choice`, `Quot.sound` when an axiom appears. **sorryAx0**, no new axioms, changed Lean errors/warnings **0/0**.
- Theorem squash and then-main HEAD `aa689ddac8c5f9036fe2a4185eb537882b9c44fb`.
- This is a **docs-only follow-up**; its Strict Lean should be **SKIPPED**, rather than rerunning all mathlib checks.

## 7. Exact obstruction boundary and possible GK5G

This result proves genuine reindexing along an arbitrary map `f` for the *same actual family pulled back along f*. It does **not** prove that relabeling by a noninjective `f` reflects literal equality of distinct original indexed words, or supply a canonical comparison between unrelated category families `D : I → Cat` and `C ∘ f` without explicit compatibility equivalences.

A possible GK5G will study **genuine changes of category family / presentation** along specified pointwise category equivalences or transport functors, keeping variance, coherence, chosen quasi-inverses and obstruction boundaries explicit. This is not a GK5F theorem.

As in the previous KuuOS lineage: no unconditional original F45 source faithfulness, source-Q category axioms, raw F54/F55/P92B Type-valued higher cells, arbitrary integer matrix reachability, global Gray reconstruction, unrestricted changing universe levels or unbounded hyperdescent. Strict 空 is central; independent Kuu remains one presentation.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
