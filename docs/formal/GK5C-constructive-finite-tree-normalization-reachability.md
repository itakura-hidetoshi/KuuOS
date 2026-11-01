# F112-P94D3GK5C — Constructive finite-tree normalization reachability and chosen-inverse coherence

**Date:** 2026-11-01 JST  
**Theorem PR:** [#2901](https://github.com/itakura-hidetoshi/KuuOS/pull/2901) — MERGED  
**Theorem squash / canonical main HEAD at theorem merge:** `73ea3ac3e6f6c86d8ec7a21dff011a6a34d6d46f`  
**Final theorem source HEAD:** `502c1e0f7d2d4e2adc68e6a55fd6d2018b626de1`  
**Test-merge commit:** `e464e79ac0302db61f8ab74e71533b39fbd5f0e5`  
**Matching source/test-merge Git tree:** `1e20f44546642bf3ceb3f834b8d05eff28269ded`  
**Exact-source CI:** [#41307401462](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41307401462) — SUCCESS.

## Canonical Lean source and original boundaries

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5CFiniteTreeNormalizationReachability.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CFiniteTreeNormalizationReachability.lean)

Pinned **Lean v4.30.0-rc2**, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Exactly one append-only Lean file following GK5B, retaining its entire source unchanged. The repository's existing **107 public roots** are unchanged. The original typed F45 structural source, actually attained old-AH image, genuine AH-kernel-compatible full subcategory, arbitrary GK4BM chosen inverse `Q_T`, GK4BP explicit inverse `P_T`, and their GK4BQ natural-isomorphism comparison remain fixed. `Q_T` is not definitionally equal to `P_T`.

## The previously open problem: does an actual path exist?

GK5B built **proof-relevant, genuinely typed** `NativeGK5BRewriteStep` and `NativeGK5BRewritePath` using actual pinned Mathlib `Functor.associator`, `Functor.leftUnitor`, `Functor.rightUnitor`, and real iso-whiskering, and proved that any two existing same-endpoint paths evaluate to the same whole Mathlib NatIso.

**GK5B did NOT yet construct a path between arbitrary finite presentations with equal ordered leaf lists. GK5C now does so**, by defining true finite normalization witnesses, not postulating accessibility or fictitious raw higher cells.

### 1. Path-level genuine whiskering

`nativeGK5CPathWhiskerLeft` and `nativeGK5CPathWhiskerRight` recursively lift every constructor of a genuine GK5B path—including identity, step, reversal, and concatenation—through fixed outer left/right binary tree contexts. Each lifted basic step uses GK5B's actual `whiskerLeft`/`whiskerRight` constructor and hence actual Mathlib iso-whiskering. These are finite, proof-relevant paths with correctly typed intermediate trees.

### 2. True canonical list append path

`nativeGK5CAppendPath(xs,ys)` constructs a real typed path

`paste(treeOfList xs,treeOfList ys) → treeOfList(xs ++ ys)`.

The empty-left-word base **really applies** the left unitor to the canonical tree `treeOfList ys`; in the nonempty case `R :: xs`, the path first applies a real associator to

`paste(paste(atom R, treeOfList xs), treeOfList ys)`

and then applies the inductive append path under a **real left-whisker** by `atom R`. The construction retains the actual intermediate structural moves.

### 3. Constructive normalization of EVERY finite tree

`nativeGK5CNormalizePath t` gives a concrete term of

`NativeGK5BRewritePath T t (nativeGK5ATreeOfList (nativeGK5ATreeLeaves t))`

for **every** `t : NativeGK5AFiniteTargetTree T`.

The `unit` case uses a real identity path. The `atom R` case uses the **inverse of the real right-unitor** to expand the atom into the canonical `paste(atom R, unit)`. The `paste left right` case concatenates:

1. Right-whiskering of the recursively constructed normalization path of `left`;
2. Left-whiskering of the recursively constructed normalization path of `right`;
3. The genuine canonical-list append path from step 2.

This is a genuine **termination-by-structural-recursion construction of normalization reachability** for all finite trees, not an assumed path, not a new raw F54/F55/P92B higher filler.

`nativeGK5CTreeOfList_leaves` proves the canonical tree's leaf list equals exactly the supplied finite list; `nativeGK5CNormalizePath_leaves` proves every constructed normalization path preserves the original ordered leaves.

### 4. Equality of actual normalization NatIso and GK5B canonical comparison

`nativeGK5CNormalizePath_iso_eq_canonical` proves the true whole Mathlib NatIso equality

`pathIso(normalizePath t) ≪≫ eqToIso(treeOfList_eval(leaves t)) = treeNormalization(t)`.

The appended `eqToIso` matters: the evaluated right-associated canonical tree and GK5A's finite list composite agree **as whole functors by an existing theorem**, not by an unchecked implicit coercion of dependent Iso types. GK5B's `nativeGK5BPathIso_eqToIso` and pinned Mathlib `eqToIso_trans` establish the exact boundary transport.

### 5. NECESSARY AND SUFFICIENT reachability

The strongest new GK5C theorem,

`nativeGK5CReachable_iff_sameLeaves`,

states **for any two finite actual target trees** `a,b`:

`Nonempty (NativeGK5BRewritePath T a b) ↔ nativeGK5ATreeLeaves a = nativeGK5ATreeLeaves b`.

**Forward implication:** GK5B's already proved `nativeGK5BPathLeaves` gives preservation of the complete ordered list of genuine target leaves under each actual structural rewrite.

**Reverse implication:** `nativeGK5CPathBetweenOfSameLeaves` constructs the actual path by normalizing `a` to its canonical leaf-word tree, transporting the given leaf-list equality to the canonical normalization target of `b`, and reversing the actual normalization path of `b`. No extra assumption of path existence is made.

`nativeGK5CPath_eq_canonical_of_path` then combines existence with GK5B's whole NatIso path independence: **every actual path `a→b` agrees with this specifically constructed normalization/reverse-normalization path as a whole NatIso.**

### 6. Chosen-inverse target-NatTrans and actual boundary transport

`nativeGK5CChosenInverse_normalization_square` proves the GK4BU/GK5A **whole NatTrans modification square** along the concrete, recursively generated `normalizePath(t)`. `nativeGK5CChosenInverse_normalization_transport` proves GK5A's chosen-inverse comparison agrees after both boundary `eqToIso` transports induced by the normalization path's whole-target-functor equality.

`nativeGK5CChosenInverse_sameLeaves_canonical_square` handles **any equal-leaf pair** along the explicitly constructed complete-reachability path. This is a genuine whole NatTrans square over the existing actual compatible and attained-AH categories, not a new raw higher-dimensional source cell.

## Exact-source CI, 13 declaration axiom audit

- **Source HEAD** `502c1e0f7d2d4e2adc68e6a55fd6d2018b626de1`.
- **Test-merge SHA** `e464e79ac0302db61f8ab74e71533b39fbd5f0e5`.
- **Matching Git tree** `1e20f44546642bf3ceb3f834b8d05eff28269ded`.
- [GitHub Actions #41307401462](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41307401462): **Strict Lean 3824/3824 SUCCESS**, **Independent Kuu SUCCESS**, **Workflow integrity SUCCESS**, **Governance terminal SUCCESS**, exact-head completion receipts published.
- **13 public definitions/theorems, 13 `#print axioms`**. Independently extracted exact-head Lean logs show only `propext`, `Classical.choice`, `Quot.sound`; **sorryAx = 0**; changed Lean errors/warnings **0/0**.
- The theorem source adds one file, with no edits/deletions of earlier proof sources. No additional axioms, weakenings or strictness assumptions were introduced. The separate documentation follow-up should be docs-only with Strict Lean **SKIPPED**.

## Mathematical scope and next boundary

The proved iff reachability and path-independence concern finite binary trees whose leaves are **endofunctors `T ⥤ T` of one fixed genuine Mathlib target category**. Ordered leaves are compared literally as lists of whole functors. Arbitrary unbounded chains through DIFFERENT target categories, semantic equivalence under unequal leaf sequences, original F45 source unconditional faithfulness, source-Q category laws, raw F54/F55/P92B Type-valued higher cells, all integer matrices' attainability, global Gray, and unlimited hyperdescent are **not** established. Strict 空 is central, and independent Kuu is one presentation.

**Next possible GK5D:** abstract this normalization and reachability as a universal property of an explicit typed rewrite presentation, or extend the construction to heterogeneous composable target-category chains without definitional strictification of `Q_T`. Neither extension is a GK5C theorem.
