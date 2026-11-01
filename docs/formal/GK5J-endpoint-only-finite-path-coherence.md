# F112-P94D3GK5J — Genuine finite-path endpoint-only coherence obstruction

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2915](https://github.com/itakura-hidetoshi/KuuOS/pull/2915) — MERGED  
**Theorem squash/main HEAD at theorem merge:** `e7ad9bf2e9757bc8b722fc447c7ca7641bbe69d2`  
**Final theorem source HEAD:** `66ed8f1f54b06a133d7bc73a2be1d8ec17e4ee85`  
**Matching source/squash Git tree:** `aa036d080033ea2aac5f6efb4a9182a04b8f4828`  
**Exact-source CI:** [#41362213858](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41362213858) — ALL TERMINAL SUCCESS.

## Canonical Lean source

[PolygonNativeC60AQFullPentagonPhysicalNativeGK5JEndpointObstructionCanonicalization.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5JEndpointObstructionCanonicalization.lean)

GK5J is one new additive Lean file after GK5I, without historical file rewrites. Its actual primitives come from the already certified GK5D/GK5G/GK5H/GK5I chain. We keep true indexed Mathlib categories `C,D : I → Cat.{vC,uC}`, actual equivalences `e : ∀ i, C i ≌ D i`, both whole NatIso path interpretations, and recursive tree comparison isomorphisms `Φ_t`.

## Proven results

### 1. Proof-relevant path-choice invariance

For two actual GK5D paths `p,q : NativeGK5DTypedPath C a b` with the same dependently typed endpoint trees, `nativeGK5JPathSquare_iff_sameEndpoints` proves

`NativeGK5JPathSquare e p ↔ NativeGK5JPathSquare e q`.

The square is a WHOLE Mathlib NatIso equation

`PathIso(ChangePath(e,p)) ≪≫ Φ_b = Φ_a ≪≫ ChangeIso(e,PathIso(p))`.

This equivalence is **unconditional** even though each particular square may fail. The proof applies actual `nativeGK5DPath_independent` twice: once to `p,q` in the original categories C and independently once to `ChangePath(e,p),ChangePath(e,q)` in the changed categories D. No fictional filler, path truncation, new axiom, or equality between unrelated categories is inserted.

### 2. Constructive canonical endpoint criterion

GK5D constructs the actual normalization-and-reversal path

`N(a,b,h) := nativeGK5DPathBetweenOfSameLeaves a b h`

for an explicit equality `h : nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b` of ordered *dependently typed* leaf words. GK5J defines `NativeGK5JEndpointCompatible e` by testing exactly this canonical path for every such endpoint pair and proves

`NativeGK5HPathCompatible e ↔ NativeGK5JEndpointCompatible e`

in `nativeGK5JAllPaths_iff_endpoints`. Combining this with the GK5H local-to-global theorem gives the new exact three-way characterization

`PathCompatible e ↔ EndpointCompatible e ↔ StepCompatible e`

via `nativeGK5JEndpoints_iff_localSteps`.

The endpoint criterion still universally quantifies over compatible finite tree **pairs**. It is **not** a claim that only finitely many endpoint pairs must be checked or that all local generator obstructions vanish.

### 3. All actual paths at the three-atom associator endpoints

The already certified GK5I whole NatIso associator square is the witness for the single genuine three-atom basic step. The new theorem `nativeGK5JThreeAtoms_allPaths` proves the same whole NatIso square for **every** genuine finite typed rewrite path between the identical two three-atom associator endpoint trees, allowing any proof-relevant reversal or concatenation wherever type-correct. This uses the path-choice invariance, **not** a blanket assertion for arbitrary subtrees.

## Exact-source CI and axiom audit

- Source commit `66ed8f1f54b06a133d7bc73a2be1d8ec17e4ee85`.
- Squash commit `e7ad9bf2e9757bc8b722fc447c7ca7641bbe69d2`.
- Source and squash both have exact Git tree `aa036d080033ea2aac5f6efb4a9182a04b8f4828` (confirmed independently with GitHub MCP).
- [CI run #41362213858](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41362213858): **Strict Lean 3831/3831 SUCCESS**, **Independent Kuu core SUCCESS**, **Workflow integrity SUCCESS**, **Governance gate and audit summary SUCCESS**.
- **4/4 new public theorem `#print axioms`** outputs cite only `propext`, `Classical.choice`, `Quot.sound`. No `sorryAx`, no new axioms, changed source Lean errors/warnings 0/0.
- Fixed Lean `v4.30.0-rc2`, pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`, root107 unchanged, protected validation-only PR #1558 remains Draft/open/unmerged. Strict 空 centered; independent Kuu one presentation; original arbitrary chosen inverse Q and explicit inverse P remain distinguished by genuine κ comparison, not strictified.
- Initial submitted source compiled successfully; no diagnostic correction commits were needed.
- Documentation-only PR: Strict Lean should be SKIPPED under project CI policy, while its actual docs governance is verified separately.

## Open obstruction and next research GK5K

The equivalence of canonical endpoint conditions and all-path compatibility does **not** imply either side is true. General associator of arbitrary finite subtrees (with nontrivial `Φ_a,Φ_b,Φ_c`), left/right unitors and both contextual whiskering constructors remain open as *unconditional* generator compatibility theorems. Next investigate naturality of genuine middle `unitIso.symm` compositor with respect to the three subtree comparison NatIsos, then the associator/triangle/interchange coherence, without assuming the very square being proved. Only after all local generators are certified may GK5H/GK5J yield unconditional coherence for arbitrary finite paths. Unrestricted Gray/hyperdescent, raw source Type-valued high cells, source-Q category axioms and F45 faithfulness remain outside the proven scope.
