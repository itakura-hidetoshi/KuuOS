# F112-P94D3GK5B — Genuine finite-tree rewrite paths and path-independent normalization

**Formal date:** 2026-11-01 JST  
**Theorem PR:** [#2899](https://github.com/itakura-hidetoshi/KuuOS/pull/2899) — MERGED  
**Theorem squash / canonical main at theorem merge:** `8a8abead7636024d50c748887336d27037d30cbf`  
**Final exact-source HEAD:** `afa157901a4cd9c3b6303a419f36055dad7c6ded`  
**GitHub test-merge commit:** `859461456c1fbda8b4b2520e411cec4daff1bccc`  
**Identical source/test-merge Git tree:** `0cef5f92477213381c90d5d069e5ea66f7738319`  
**Exact-source CI:** [#41306352193](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41306352193) — SUCCESS.

## Canonical formal Lean source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFiniteTreeRewritePathCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFiniteTreeRewritePathCoherence.lean)

Pinned Lean v4.30.0-rc2, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; append-only new Lean file, previous source untouched, public root 107 retained. GK5B imports the actual GK5A finite target-tree chosen-inverse comparison, which depends on GK4BZ and preceding typed Mathlib NatIso/target-NatTrans coherence. Strict 空 is central; independent Kuu remains one presentation. Copyright © 2026 Hidetoshi Itakura / 板倉英俊.

## Proof-relevant actual Mathlib rewrite system

For any fixed genuine Mathlib target category `T`, GK5A provided the finite binary tree `NativeGK5AFiniteTargetTree T` with unit, atom `R:T⥤T`, and paste constructors. GK5B introduces a new **proof-relevant typed step** `NativeGK5BRewriteStep T a b` with precisely these real Mathlib structural operations:

1. `assoc`: genuine `Functor.associator` for the reassociation `((a⋙b)⋙c) → (a⋙(b⋙c))`.
2. `leftUnit` and `rightUnit`: genuine `Functor.leftUnitor` and `Functor.rightUnitor`.
3. `whiskerRight` and `whiskerLeft`: genuine `Functor.isoWhiskerRight` and `Functor.isoWhiskerLeft`, applying a typed rewrite inside a larger finite tree.

A separate indexed `NativeGK5BRewritePath T a b` is proof-relevant syntax with `refl`, `basic`, `reverse`, and `trans`. Thus every finite path is a *concrete syntax tree of actual structural moves*; this is **not** a new raw original F54/F55/P92B 3-cell or a Gray structure.

`nativeGK5BStepIso` evaluates actual steps to full Mathlib NatIso. `nativeGK5BPathIso` evaluates whole paths by **real Iso composition** `≪≫`, inverse `.symm`, and identity.

## Main mathematical results

**1. Actual path NatIso = canonical whole-functor equality transport.**

`nativeGK5BStepEq` and `nativeGK5BPathEq` construct the whole Mathlib functor equalities arising from the corresponding genuine associator/unitor moves. `nativeGK5BStepIso_eqToIso` proves that each *actual* step NatIso equals `eqToIso` of that equality, including all left/right whiskering. It uses typed `Iso.ext` for Mathlib's genuine associator and unitors and exact equality transports for whiskering. Structural induction on entire paths yields

`nativeGK5BPathIso_eqToIso : pathIso(p) = eqToIso(pathEq(p))`.

This preserves the actual intermediate Mathlib NatIso objects in their constructors rather than assuming a missing higher source cell.

**2. Whole NatIso path independence.**

`nativeGK5BPath_independent` proves, for **ANY** two genuine rewrite paths `p q : NativeGK5BRewritePath T a b` with the same typed endpoints, the equality of **whole** NatIso values:

`nativeGK5BPathIso p = nativeGK5BPathIso q`.

This follows from the actual-pasting-to-equality-transport induction and proof irrelevance of the real whole-functor equality. The claim is **conditional on the two paths existing**; it does not assert all arbitrary tree pairs are connected by the rewrite generators.

**3. Ordered leaf-word preservation and normalization.**

Both `nativeGK5BStepLeaves` and `nativeGK5BPathLeaves` prove that every actual rewrite preserves the **ordered list of true non-unit target leaves**. GK5A already supplied the finite list fold `nativeGK5AListComposite` and tree-to-list whole-functor equality. GK5B constructs the concrete whole NatIso normalization `nativeGK5BTreeNormalization(t) = eqToIso(eval(t)=listComposite(leaves(t)))`. Its `nativeGK5BPath_normalization` theorem says:

`pathIso(p) ≪≫ normalize(b) ≪≫ eqToIso(listComposite(leaves(b)) = listComposite(leaves(a))) = normalize(a)`.

The last equality is the actual transport induced by `nativeGK5BPathLeaves p`; it is **not silently discarded**. This is exact typed path-compatibility with a canonical finite-word presentation.

**4. Chosen-inverse Q naturality and path independence.**

Using GK5A's genuine recursively pasted chosen-inverse `Θ_tree`, GK4BU's whole target-NatTrans modification, and the actual path NatIso, `nativeGK5BChosenInverse_rewritePath_square` proves the full natural-transformation equation

`(C_(pathIso(p).hom) ▷ Q_T) ≫ Θ_tree(b).hom = Θ_tree(a).hom ≫ (Q_T ◁ A_(pathIso(p).hom))`.

`nativeGK5BChosenInverse_twoPaths_agree` proves **both the left-hand and right-hand whole NatTrans pastings** are identical for any same-endpoint pair of actual rewrite paths. `nativeGK5BChosenInverse_rewritePath_transport` proves the true whole chosen-inverse NatIso equality with BOTH boundary `eqToIso` transports determined by `nativeGK5BPathEq`. In particular, the arbitrary chosen reverse `Q_T` remains distinct from the explicit GK4BP `P_T`, joined only by the existing genuine comparison `κ_T : Q_T ≅ P_T`.

**5. Nontrivial two-route demonstration.**

`nativeGK5BMiddleUnit_pathA` starts from `(((a ⋙ 𝟭) ⋙ b) ⋙ c)`, eliminates `𝟭` under two actual right whiskerings, then applies a real associator to reach `a ⋙ (b ⋙ c)`. `nativeGK5BMiddleUnit_pathB` instead applies the true associator first, then eliminates `𝟭` by a right-whiskered real right unitor. `nativeGK5BMiddleUnit_twoRoutes_coherent` proves the **whole Mathlib NatIso** of these two explicitly different intermediate paths is equal.

## Exact-source CI and structural error analysis

- Source HEAD `afa157901a4cd9c3b6303a419f36055dad7c6ded`, test-merge `859461456c1fbda8b4b2520e411cec4daff1bccc`, **identical Git tree `0cef5f92477213381c90d5d069e5ea66f7738319`**.
- [Strict Lean CI #41306352193](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41306352193): **3823/3823 SUCCESS**. Independent Kuu and retained public API **SUCCESS**, Workflow consolidation integrity **SUCCESS**, Governance terminal and exact-head completion receipt **SUCCESS**.
- **17 public definitions/theorems + 2 new indexed inductive types**. The 17 public declarations have **17 `#print axioms`**, and the exact-source job log lists **only** the standard `propext`, `Classical.choice`, `Quot.sound`; **sorryAx0**, changed Lean error/warning0/0.
- First CI run exposed a Lean4 **arrow/iso precedence parsing mistake**: `RewriteStep → A ≅ B` was not parsed as an arrow to a natural-isomorphism type; in the dependent recursive signatures it must be written `RewriteStep → (A ≅ B)`. The malformed signatures led to cascading synthetic `sorryAx` in a failed build. Full-source repair added both parentheses without weakening any statement.
- Second CI run confirmed every substantive proof, but the `nativeGK5BPath_independent` proof had a **redundant `rfl` after `rw` already closed the goal**, producing `No goals to be solved`. Removing only that redundant tactic fixed the final elaboration failure. The full changed source, dependent signatures and pinned Mathlib API were checked again. Final exact-source CI passed all jobs.

## Mathematical authority boundary and continuation

GK5B proves **equality of real Mathlib structural path NatIso for existing same-endpoint paths**, normalization compatibility and chosen-inverse target comparison in a **fixed genuine target endofunctor category**. It does not establish normalization termination/confluence for any arbitrary user-supplied raw rewrite system, reachability of arbitrary source terms, raw F54/F55/P92B Type-valued higher cells, unconditional faithfulness of original F45-dependent `S`, source-Q category laws, all integer matrices' attainability, global Gray coherence, or unlimited hyperdescent. No definitional equation `Q_T=P_T` is assumed.

A possible GK5C continuation is **proof-relevant normalization reachability**, explicitly constructing a rewrite path from every finite tree to the right-associated canonical leaf-word tree with true associators/unitors, and proving its whole NatIso equals GK5B's canonical normalization. This is an additional statement; GK5B only proves compatibility for already existing rewrite paths. Maintain append-only same-root107, protected validation-only PR #1558 Draft/OPEN/unmerged and separately synchronize README/ROADMAP by a docs-only PR with Strict Lean SKIPPED.
