# F112-P94D3GK5E — Heterogeneous finite-tree chosen-inverse coherence, path naturality and two-end transport

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2905](https://github.com/itakura-hidetoshi/KuuOS/pull/2905) — MERGED  
**Theorem squash / canonical main HEAD at theorem merge:** `25476845f43750450ef36ace772244a222c5fec6`  
**Final theorem source HEAD:** `df2160c0eac86dd51593c969b039a251f89213f8`  
**Test-merge SHA:** `9518d0a823d9541e73cc721bb758bec9ef58ad2a`  
**Identical source/test-merge Git tree:** `716543f2fad563767b598a464730165f7641daca`  
**Exact-source CI:** [#41341736451](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41341736451) — SUCCESS.

## Canonical Lean source and inherited boundaries

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5EHeterogeneousChosenInverseCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5EHeterogeneousChosenInverseCoherence.lean)

The new proof imports GK5D's already verified typed many-category finite trees and retains GK4BM's *genuine arbitrary choice-based inverse* `Q_T`, GK4BP's distinct explicit inverse `P_T`, the GK4BQ genuine natural-isomorphism comparison `κ_T : Q_T ≅ P_T`, GK4BT's whole chosen-inverse target comparison `Θ_R`, GK4BU's whole target NatTrans square, GK4BV's binary-composition coherence, and GK4BW's REAL binary pasting of two whole NatIso values. `Q_T` and `P_T` are **not definitionally identified**.

The original F45 source, genuinely attained old-AH target `A_att`, compatible kernel-defined full subcategory `Comp_T`, and all previous theorem source files remain untouched. The only theorem-file change is one *new* Lean file. Lean is pinned to **v4.30.0-rc2** and mathlib to `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public root count **107** remains unchanged. Protected PR #1558 is Draft/OPEN/unmerged.

## Main mathematics

Let `I` be any index type and `C : I → Cat.{vC,uC}` a family of genuine Mathlib categories, all bundled at one fixed universe pair. For any indices `i,j : I`, GK5D defines real dependent finite functor trees `NativeGK5DTypedTree C i j`, their whole Mathlib functor composite `R_t : C i ⥤ C j`, and real associator/unitor/whiskering rewrite paths between same-typed endpoints.

### 1. Recursive whole NatIso, arbitrary depths and genuinely different categories

`nativeGK5EChosenInverse_treeIso` assigns to EACH finite typed tree `t` a genuine whole Mathlib NatIso

`Θ_t : R_{t,*}^Comp ⋙ Q_{C j} ≅ Q_{C i} ⋙ R_{t,*}^Att`.

The `unit` and `atom` cases use GK4BT's original actual whole `Θ_R`. The `paste left right` case uses **GK4BW's genuine binary NatIso pasting**, complete with the real associator, whiskering, target-composition equality and both source/target transports, over the genuinely matched intermediate category.

The main structural-induction theorem `nativeGK5EChosenInverse_treeIso_eq_direct` proves EXACT equality of whole actual Mathlib natural isomorphisms

`Θ_recursive(t) = Θ_direct(R_t)`.

In the `paste` case, the proof uses both induction hypotheses, GK4BW's theorem identifying binary pasting of the actual Theta factors with GK4BV's concrete comparison, and GK4BV's full composition-coherence theorem. There is no newly postulated higher-dimensional cell and no assumption of strict chosen-inverse target commutation.

### 2. Whole target NatTrans naturality for heterogeneous trees

`nativeGK5EChosenInverse_treeNat_square` applies to ANY genuine target natural transformation `ρ : R_left ⟶ R_right` for two trees with identical typed category endpoints. It proves the full square

`(ρ_*^Comp ▷ Q_{C j}) ≫ Θ_right.hom = Θ_left.hom ≫ (Q_{C i} ◁ ρ_*^Att)`

as equality of **whole Mathlib NatTrans** values. This follows from exact recursive-vs-direct equality and GK4BU's previously proven native target NatTrans square. Both choices of target category may be different.

`nativeGK5EChosenInverse_rewritePath_square` instantiates the square with the **hom** of an actual GK5D path's genuine whole Mathlib NatIso, retaining real associator/unitor/whiskering evidence.

### 3. Path-independent whole chosen-inverse modifications

`nativeGK5EChosenInverse_twoPaths_agree` establishes equality of BOTH fully pasted left and right whole NatTrans expressions for ANY two actual GK5D rewrite paths between the same typed trees. Its proof uses GK5D's **whole NatIso** path-independence, not mere equality of route labels or objectwise components.

### 4. BOTH genuine eqToIso boundaries

`nativeGK5EChosenInverse_eqTransport` treats ANY whole-functor equality `h : F = G` in `C i ⥤ C j` and proves exact equality of entire chosen-inverse comparison NatIso values after (1) the left `eqToIso(congrArg ... h)` and (2) the right `eqToIso(congrArg ... h.symm)`.

`nativeGK5EChosenInverse_rewritePath_transport` applies that generic proof to `nativeGK5DPathEq path` along a real finite rewrite route, then replaces direct Theta with the actually recursively pasted `Θ_t` at BOTH endpoints.

`nativeGK5EChosenInverse_normalization_square` and `nativeGK5EChosenInverse_normalization_transport` strengthen the result to the specifically **constructed GK5D normalizing path** from EVERY finite tree to its right-associated ordered typed leaf-word canonical tree. The latter is an equality of complete NatIso values, including both actual boundary equality transports.

### 5. Nonvacuous existence from equal ordered typed leaves

Given `h : TreeLeaves left = TreeLeaves right`, GK5D supplies `nativeGK5DPathBetweenOfSameLeaves left right h`, a CONCRETE actual path built by normalizing, transporting leaf equality, and reversing the second normalization. `nativeGK5EChosenInverse_sameLeaves_canonical_square` proves the full chosen-inverse target NatTrans square for this specific, not merely existential, path.

`nativeGK5EChosenInverse_sameLeaves_transport` also transports the two recursively pasted NatIso values along the **whole-functor equality** `nativeGK5DTreeComposite_eq_of_leaves`, with both genuine boundary `eqToIso` morphisms. Equality of typed leaf words is a syntactic/presentation equality; it is NOT claimed to characterize all semantic functor equalities.

### 6. Concrete three-stage heterogeneous associator

`nativeGK5EChosenInverse_threeStage_associator_square` exhibits the actual, nontrivial whole NatTrans square associated to the true Mathlib associator between `(F ⋙ G) ⋙ H` and `F ⋙ (G ⋙ H)` for `F : C i ⥤ C j`, `G : C j ⥤ C k`, `H : C k ⥤ C l`. Its proof applies the arbitrary-path theorem to the constructed `basic (assoc ...)` route.

## Lean4 elaboration issue, repair, and exact-source certificate

The initial exact-source CI found one error in the final concrete associator example. Its goal used `nativeGK5DStepIso (assoc ...)`; the applied general rewrite-path theorem produced `nativeGK5DPathIso (basic (assoc ...))`. Those genuine NatIso terms agree via the *dependent path definition equations*, but Lean's elaborator did not automatically reduce the indexed `basic` constructor in this context.

The only repair replaced the last proof with `simpa only [nativeGK5DPathIso] using (...)`, using the fixed pinned Mathlib API and GK5D's already validated indexed path semantics. No theorem target, hypothesis, old proof file or axiom was changed.

**Final source HEAD:** `df2160c0eac86dd51593c969b039a251f89213f8`  
**GitHub test-merge HEAD:** `9518d0a823d9541e73cc721bb758bec9ef58ad2a`  
**Independently fetched Git object trees for both:** `716543f2fad563767b598a464730165f7641daca` — exact match.  
**Exact-source run:** [#41341736451](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41341736451): **Strict Lean 3826/3826 SUCCESS**, **Independent Kuu SUCCESS**, **Workflow integrity SUCCESS**, **Governance terminal SUCCESS**.  
**12 public `#print axioms` checks / 12 declarations:** only `propext`, `Classical.choice`, and `Quot.sound`; **sorryAx = 0**, no new axioms, changed Lean error/warning **0/0**.  
**Theorem squash / main HEAD at theorem merge:** `25476845f43750450ef36ace772244a222c5fec6`.

This proof receipt is a docs-only follow-up and must not trigger strict Lean again; its own CI is expected to report **Strict Lean SKIPPED**.

## Scope, obstructions, next GK5F

GK5E proves chosen-inverse coherence for arbitrary **finite** many-category typed Mathlib functor trees with a fixed universe pair, and their actual GK5D structural rewrite paths. It does not prove coherence for category universes varying along a chain, arbitrary unbounded high-descent systems, raw source F54/F55/P92B Type-valued higher cells, original F45 unconditional source faithfulness, original source-Q category axioms, reachability of arbitrary integer matrices, or a global Gray category.

A separately typed GK5F may address the **functoriality in the category family itself** (change-of-index/presentation transport), or naturality under genuine family morphisms, while preserving the type and authority boundaries. Neither is established by GK5E.

Strict 空 remains the organizing center; independent Kuu is one presentation. All KuuOS standard governance and append-only rules remain unchanged.

Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
