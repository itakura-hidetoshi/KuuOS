# F112-P94D3GK4AX — genuine finite-evaluation determinacy and two-observation degree obstruction

2026-10-31 JST · canonical `main` · [Lean theorem PR #2833](https://github.com/itakura-hidetoshi/KuuOS/pull/2833) **MERGED** · exact-source CI [#41208604553](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41208604553) **SUCCESS**.

## 1. Authoritative source and dependency boundary

- [New, append-only Lean proof](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AXFiniteEvaluationDeterminacy.lean).
- Canonical pre-theorem main: `cec732dee9914fff6d63dc4a9cf98fb2890a9dd0`.
- Exact theorem PR head: `0dcf281ee6433674f30a7f56be337061eecf6a72`.
- Exact test-merge checkout: `f4033c6fc438b5f54f29b56d79bbec0d750a3ce1`.
- **Identical source and test-merge Git tree:** `2f7a50aaa539b01b717df841e6580289f1847f25`.
- Theorem squash merge: `222a7d003312ac1274211292d301897e62f2032e`.
- Pinned Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; existing public roots **107**.
- Original GK4AV `nativeGK4AVRoute_degree`, `nativeGK4AVP92_degree`, `nativeGK4AVStructural_degree` are reused unchanged.
- Crucial pinned mathlib theorem: `Polynomial.eq_of_natDegree_lt_card_of_eval_eq` in `Mathlib/Algebra/Polynomial/Roots.lean`. It explicitly requires pairwise distinct sample parameters, equality at all samples, and degree strictly below sample count.

## 2. Mathematics proved in Lean

The original fully typed F54 path has a polynomial matrix
`P_r(X) ∈ Mat₂(ℤ[X])` with each entry's `natDegree ≤ β(r)`,
where `β(r)` is the **actual GK4AD original backwardCount**.

For any pair `u,v` with identical original typed source and target,
any finite set of **N distinct integers** `t₁,...,t_N` with

```text
N > max(β(u), β(v))
P_u(t_i) = P_v(t_i)   for all i
```

implies

```text
P_u(X) = P_v(X) in Mat₂(ℤ[X]).
```

This is an unconditional *bounded evaluation-determinacy theorem*, **not** an injectivity claim for all source Type-valued paths.

The Lean declarations are:
- `nativeGK4AXEntry_eq_of_samples` and `nativeGK4AXMatrix_eq_of_samples`: arbitrary finite injective integer samples and full four-entry matrix.
- `nativeGK4AXRoute_eq_of_samples`: genuine original fully dependent F54 paths.
- `nativeGK4AXP92_eq_of_samples`: independently descended original P92B witness-existence quotient `Q`.
- `nativeGK4AXStructural_eq_of_samples`: independently descended original structural comparison quotient `S`.

The `Q` and `S` results are **separate**, based on their own previously verified descents. Neither is created by observer equalities.

## 3. The two OLD matrix observations at parameters 1 and 4

The original AF matrix is exactly `P_r(1)`; AH is exactly `P_r(4)`.
The two integers are different, so they form an injectively indexed
`Fin 2 → Int` sample. With `max(β(u),β(v)) < 2`, the pinned
polynomial uniqueness lemma yields:

```text
β(u) ≤ 1, β(v) ≤ 1,
AF(u) = AF(v), AH(u) = AH(v)
   ==> P_u(X) = P_v(X).
```

This is proved separately for original F54 routes, P92B `Q`, and
structural `S` by
`nativeGK4AXRoute_twoEval_determines`,
`nativeGK4AXP92_twoEval_determines`,
and `nativeGK4AXStructural_twoEval_determines`.

A further proved obstruction on actual F54 Type-valued paths is:

```text
AF(u) = AF(v), AH(u) = AH(v), P_u(X) ≠ P_v(X)
   ==> 2 ≤ max(β(u),β(v)).
```

Lean: `nativeGK4AXRoute_collision_requires_two`.
**This is only a necessary condition; it DOES NOT assert that a
collision satisfying the premises actually exists.**

## 4. Stronger single-evaluation question and Sanov boundary

The central **unproved-in-KuuOS** question is whether

```text
P_u(4) = P_v(4) ==> P_u(X) = P_v(X)
```

holds for arbitrary original F54 typed source histories, without
a backwardCount restriction.

At the mathematical group level, let
`C = [[1,1],[0,1]]`, `F=C⁻¹`, and
`R(X) = [[1,0],[X,1]]`. Under the real diagonal conjugacy
`D = diag(√2, 1/√2)`, one has

```text
D C D⁻¹    = [[1,2],[0,1]]
D R(4) D⁻¹ = [[1,0],[2,1]].
```

These are the classical Sanov free-group generators. In standard
group theory, their freeness suggests the stronger t=4 statement:
equal t=4 matrices correspond to the same reduced free-group word,
hence produce equal polynomial matrices at the formal variable X.
However **the required KuuOS Lean proof is not yet present**:
it must exhibit the genuine source-to-word map, establish a
machine-checked Sanov/ping-pong injectivity theorem for the pinned
representation, and transfer the result through all actual typed
F54 constructors. Do NOT add a Sanov conclusion as a new axiom or
assume a missing Type-valued 3-cell.

Consequently, the earlier *candidate* of different full
polynomials with equal old AF and AH must NOT be asserted as an
existing witness. If the full Sanov-to-F54 proof succeeds, that
candidate will instead be ruled out.

## 5. Exact-head validation

- [GitHub Actions #41208604553](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41208604553) terminal **SUCCESS**, scoped pinned Strict Lean **3785/3785**.
- Independent core and workflow integrity **SUCCESS**, Governance gate **SUCCESS**.
- **12 new `#print axioms` declarations**, dependencies only in `propext`, `Classical.choice`, `Quot.sound`.
- `sorryAx`: **0**; compilation errors/warnings in changed Lean: **0/0**.
- Original two Lean files GK4AV, GK4AW and their dependent declarations/imports untouched; exact source and test-merge Git trees independently matched.

## 6. Remaining obligations / authority boundaries

Still **unproved**: general one-point `t=4` determinacy in pinned Lean,
whole-family polynomial descent through existing `K_AI`, single
fixed old-class fiber infinitude, full arithmetic-slice attainability,
original `Q` associativity/unit laws, historical full typed
equivalence, unconditional genuine 14D Countable, 19D filler, global
strict and hyperdescent.

Strict 空 remains central; independent Kuu is one presentation.
Append-only / tighten-only / overwrite-forbidden / same public
roots107; no Gray reintroduction. Protected PR #1558 must remain
Draft/OPEN/unmerged.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
