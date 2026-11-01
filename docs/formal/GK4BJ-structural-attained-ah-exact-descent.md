# F112-P94D3GK4BJ — exact descent of the independent structural category to the actually attained old-AH image

2026-11-01 JST. **[Theorem PR #2863](https://github.com/itakura-hidetoshi/KuuOS/pull/2863) — MERGED.** This document is a historical validation record; the authoritative theorem is in the canonical main Lean source.

## Exact theorem carrier

- [GK4BJ full Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BJStructuralAttainedAHDescent.lean), one new file containing ten declarations.
- Final source HEAD: `84b6480c102bd4a27d597eb5c38602b9fac25594`.
- Final test-merge HEAD: `b0ca6b57911c7032a807756eb0434f44e6d687ce`.
- Exact **identical source and test-merge Git tree**: `5e949087e6a3dd85a623b1d5e3285622f2089d4e`.
- Successful squash and canonical main at integration: `70ca44e911b59ef0a51f27318a3e5b7d2f099c09`.
- [Exact-source CI #41264909942](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41264909942): **Strict Lean 3805/3805 SUCCESS**; **Governance terminal SUCCESS**; independent Kuu core and workflow integrity checks SUCCESS. All ten `#print axioms` declarations have dependencies within `propext`, `Classical.choice`, `Quot.sound`, with `sorryAx` absent and changed-file Lean errors/warnings 0/0.

## Actual source-comparison geometry

Let `S` denote the EXISTING, independent structural F54/F55 witness-existence quotient Mathlib category `NativeGK4IStage`. Let `K_AI` denote the already established second-kernel category, and `A_AH^att` denote the genuine category of old-AH matrices **actually attained** on the original dependent F45-typed Homs.

GK4AI provides the genuine fully typed functor `S -> K_AI`, proved surjective on each Hom; GK4BI provides the genuine Mathlib equivalence `K_AI ≌ A_AH^att` whose forward functor is GK4BF's old-AH image map. GK4BJ defines the real composite, without replacing or modifying those categories:

```text
nativeGK4BJStructuralAHFunctor :
  NativeGK4IStage ⥤ NativeGK4BFAttainedAHStage
  := nativeGK4AIComparisonFunctor ⋙ nativeGK4BFImageFunctor
```

The exact original dependent F45 boundary objects remain unchanged. `nativeGK4BJStructuralAH_obj` shows the object map agrees with the genuine wrapper. `nativeGK4BJStructuralAH_surjective_obj` and `nativeGK4BJStructuralAH_surjective_hom` prove literal object and local Hom surjectivity. `nativeGK4BJStructuralAH_full` and `nativeGK4BJStructuralAH_essSurj` package these in pinned Mathlib `Functor.Full` and `Functor.EssSurj`.

## Exact equality kernel — the remaining true obstruction

`nativeGK4BJStructuralAH_value` identifies the underlying integer matrix of the composite functor's actual image with the original structural AH observer `nativeGK4AHStructuralValue`. Hence for any two independent structural S Hom classes `u,v` with **the same actual typed endpoints**:

```text
nativeGK4BJStructuralAHFunctor.map u
  = nativeGK4BJStructuralAHFunctor.map v
    ↔ nativeGK4AHStructuralValue u
      = nativeGK4AHStructuralValue v
```

This is **`nativeGK4BJStructuralAH_eq_iff`** and directly yields **`nativeGK4BJStructuralAH_injective_iff`**.

Finally, **`nativeGK4BJStructuralAH_isEquivalence_iff`** proves the exact categorical criterion:

```text
The composite S -> A_AH^att is a Mathlib IsEquivalence
  ↔ the genuine original structural S-side old-AH observer
     is injective on every dependent source/target Hom.
```

The forward composite is already FULL and ESSENTIALLY SURJECTIVE **without conditions**. It is NOT assumed faithful; the right side above is **not proven unconditionally**. A categorical equivalence of `K_AI` with attained AH does not imply a categorical equivalence of independent `S` with attained AH.

## Lean4 correction and scope

The initial [CI #41264712763](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41264712763) exposed a rewrite elaboration failure: a surjectivity witness had the normal form `(fun f => F.map f) s = q`, while the dependent Hom goal contained `F.map s`. The original `rw [hs]` could not match this syntactic wrapper, so the unfinished declaration showed `sorryAx` in its nonfinal axiom output. The only repair was to normalize the equality using `change F.map s = q at hs` before rewriting. The complete file and all imports/dependent declarations were rechecked at the pinned versions; the subsequent exact-source run #41264909942 compiled successfully with no `sorryAx` or warnings/errors.

**Not proved by GK4BJ:** unconditional faithfulness of `S -> K_AI`; equality of raw original Type-valued F54 paths or original unfilled comparison slots; original Q category laws; essential or full surjectivity onto **all** ambient integer matrices; original 14D unconditional Countable; 19D fillers; global strict n-category or hyperdescent. The categorical result is a true, limited, **ordinary 1-category observer descent**, not a high-degree hyperdescent assertion.

## Next: GK4BK

Use the proven exact Hom kernel and full/object-surjective source functor to formulate and prove its **categorical universal factorization property**: a genuine functor out of the independent structural category that identifies every pair of structurally equal old-AH observations should factor through the ACTUALLY attained AH category, with an explicit functor, unit and composition verification, and uniqueness subject to precise dependent object transport. Keep original source witnesses and all authority boundaries.

Lean v4.30.0-rc2; pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public roots 107; protected #1558 Draft/OPEN/unmerged. Strict 空 central; independent Kuu is one presentation; Gray not reintroduced; append-only/tighten-only/overwrite-forbidden/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
