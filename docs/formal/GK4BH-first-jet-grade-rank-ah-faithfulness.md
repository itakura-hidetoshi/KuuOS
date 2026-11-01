# F112-P94D3GK4BH — Genuine K_AI AH faithfulness from original F54 first jet and physical rank

2026-11-01 JST. **Two theorem PRs MERGED:** [#2858](https://github.com/itakura-hidetoshi/KuuOS/pull/2858) (ordered-history first jet), [#2859](https://github.com/itakura-hidetoshi/KuuOS/pull/2859) (Boolean grade and Hom faithfulness). This document records already formalized theorems, not a new axiom or new source equality.

## Canonical theorem sources

- [GK4BH first-jet recovery](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHFirstJetADRecovery.lean), source HEAD `d7aa7798a4a39e7450532dab02f0910c1c073adb`, squash `93db9b5f77c8554f9fc52a7c7f057188de1b83a0`.
- [GK4BH grade/rank faithfulness](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHGradeRankFaithfulness.lean), source HEAD `2c16bad8e8a893c66dda68c28da1625c82bf6f83`, squash `d4c435af91f4b4d9f605ee8739b6b758b79003d0`.
- Canonical `main` at completion: `d4c435af91f4b4d9f605ee8739b6b758b79003d0`. Canonical formal sources on main outrank this narrative.

## 1. Genuine first-jet recovery of ordered AD data

For every real original dependently typed F54 route `r`, the old polynomial matrix `P_r(X)` and old ordered `GK4AD` data obey the explicitly proven `nativeGK4BHJetLinked` constraints, including

```text
P_12.coeff 0 = charge + backwardCount
P_21.coeff 1 = backwardCount
P_11.coeff 1 = orderedMoment + triangular(backwardCount)
```

together with constant diagonal unit constraints and constant lower-left zero. Thus the old signed charge, true backward count and noncommutative ordered moment are recovered coefficient-by-coefficient from the **whole original matrix**. In particular, the first jet determines the old AD invariant. Combining this with GK4BA's formally proven original one-point determinacy at `t=4`, `nativeGK4BHRoute_AH_determines_AD` and `nativeGK4BHKernel_AH_determines_AD` show that equal old AH observations imply equal ordered AD data, both on original F54 routes with the same typed boundary and on the **existing** K_AI second-kernel Hom.

The induction covers the original `RotationEdge`, true `RotationChain`, and all five `DepthRotationRoute` constructors (casts, transitivity, left/right dependent contexts included). This is not a claim of raw F54 path equality.

## 2. Original physical rank closes the Boolean-grade gap

The original F54 backward count is bounded by its real primitive rotation count. Zero-rotation routes preserve original left-rank even through dependent casts and contexts. With the existing GK4AC forward-rank inequality, the actual Boolean grade obeys

```text
grade(r) = true  iff
  backwardCount(r) = 0 and rank(original source) = rank(original target).
```

See `nativeGK4BHRoute_backward_le_count`, `nativeGK4BHZeroRotation_rank_eq`, `nativeGK4BHRaw_grade_true_iff`, `nativeGK4BHKernel_grade_true_iff`, and `nativeGK4BHKernel_AH_determines_grade`.

Consequently AH equality determines *all* components of the existing K_AI kernel value: ordered AD, old AF (by GK4BG), Boolean grade, and AH itself. The central theorem is:

```lean
nativeGK4BHKernel_AH_injective
```

It gives `AH(u)=AH(v) → u=v` for all `u,v` in each genuine, typed Hom of **K_AI**, not in original unquotiented F54 or original Q and not in the independently presented S.

## 3. Actual image, not all integer matrices

`nativeGK4BHOldAHFunctor_injective_hom` proves Hom faithfulness of the existing Mathlib AH functor. The previously constructed GK4BF functor

```text
K_AI -> NativeGK4BFAttainedAHStage
```

is now Hom injective by `nativeGK4BHImageFunctor_injective_hom`, and Hom surjective by GK4BF; `nativeGK4BHImageFunctor_bijective_hom` combines both. Fixed actually attained AH fibers are subsingletons (`nativeGK4BHFixedAHFiber_subsingleton`), so GK4BG's residual AH collision is rigorously absent (`nativeGK4BHNoResidualAHCollision`).

This is a claim only about matrices **actually attained** from real original typed F54 paths and their K_AI classes, not about every ambient integer matrix.

## Exact-source validation receipts

| Evidence | First jet / #2858 | Grade-faithfulness / #2859 |
| --- | --- | --- |
| Final source HEAD | `d7aa7798a4a39e7450532dab02f0910c1c073adb` | `2c16bad8e8a893c66dda68c28da1625c82bf6f83` |
| Test-merge HEAD | `77fb5d2eefbc7fa1ae2c5d7b5e48ad990e092882` | `3ae76d2513ad9748ff111fafe3754f5717373bbd` |
| Git tree (source/test-merge) | `d1c3413213a8b8469cf8c8da93d71778035ae512` | `f87b3edba4497d24229339cd6c71685986c9e84e` |
| Strict Lean | 3802/3802 SUCCESS | 3803/3803 SUCCESS |
| Governance | terminal SUCCESS | terminal SUCCESS |
| New declarations | 12 | 12 |
| sorryAx | 0 | 0 |
| Merge squash | `93db9b5f77c8554f9fc52a7c7f057188de1b83a0` | `d4c435af91f4b4d9f605ee8739b6b758b79003d0` |

CI links: [#41260074882](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41260074882) and [#41260689362](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41260689362). All 24 new declarations have no axioms outside `propext`, `Classical.choice` and `Quot.sound`. Post-merge `main` Lean Formal Validation, Sharded Full Governance and Runtime Full Check were also reported SUCCESS. Do not infer the truth of theorems merely from check badges; consult their full Lean types and dependencies.

Pinned Lean: `v4.30.0-rc2`; mathlib: `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; public roots: 107. Protected validation-only [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) stays Draft/OPEN/unmerged.

## Next theorem: GK4BI

Formalize the already full and faithful, object-surjective actual-image functor as a **Mathlib category equivalence**, with explicit quasi-inverse on genuine attained Hom, functor laws and natural unit/counit isomorphisms:

```text
NativeGK4AIKernelStage ≌ NativeGK4BFAttainedAHStage
```

The source and target use their existing same original typed boundary presentation. **Not claimed:** equivalence with all integer matrices; source `S -> K_AI` faithfulness; original Q category axioms; raw Type-valued identity; unconditional 14D Countable; 19D fillers; global strictness or hyperdescent. Maintain strict 空 central, independent Kuu as a presentation, no Gray reintroduction and append-only/tighten-only/same-root.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
