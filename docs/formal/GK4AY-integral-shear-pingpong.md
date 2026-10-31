# GK4AY — actual original F54 generators and exact integral two-cone geometry

**2026-10-31 JST.** [Lean PR #2835](https://github.com/itakura-hidetoshi/KuuOS/pull/2835) **MERGED**, theorem squash `2218521799c635e627300b0434d9e57d40352d94`.

[Actual Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4AYShearPingPong.lean)

## Genuine generator connection, with no new source cells

GK4AV proves the real polynomial matrices of the original F54 dependent Type-valued route generator:
```text
C     = [[1, 1], [0, 1]]
F     = [[1,-1], [0, 1]] = C^{-1}
R(X)  = [[1, 0], [X, 1]]
R(4)  = [[1, 0], [4, 1]]
```

For the integer rescaling of coordinates `(u,v) -> (2u,v)`,
the exact original t=4 generator actions become
```text
U_n(x,y) = (x + 2*n*y, y)
L_n(x,y) = (x, y + 2*n*x)
```
where `U_1` corresponds to `C` and `L_1` to `R(4)`.
No irrational diagonal conjugacy is required. This is an algebraic observation **of the existing original generator images**, not creation of a new F54 path or a Type-valued 3-cell.

## Pinned-Lean proved geometry

Define two strict cones:
```text
H = {(x,y): |x| > |y|}
V = {(x,y): |y| > |x|}
```
Lean proves they are each nonempty and disjoint. For **every nonzero integer n**, including negative n,
```text
U_n(V) ⊆ H,
L_n(H) ⊆ V.
```
Both families satisfy `U_m ∘ U_n=U_(m+n)` and `L_m ∘ L_n=L_(m+n)`; both define actual integer permutations with inverses at exponent `-n`.

The core proof is entirely in `Int` using the triangle inequality, `0<|n|` for nonzero n, absolute-value product expansion, and `nlinarith`. The pinned import `Mathlib.GroupTheory.CoprodI` contains the actual ping-pong lemma to be applied in GK4AZ. It is NOT assumed as a new axiom.

## Exact-source proof validation

- Source `2a74c109ade0fa898c334b5f4a3e58a0e80ae3fb`, test-merge checkout `0dfcdde494bdaa3bfd253f3e72582a10f851f39e`.
- Same Git tree `4308276ef4434e69dfad7d1e952197b64982da6a`.
- [Run #41211527398](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41211527398): **Strict Lean 3788/3788 SUCCESS**, Governance **SUCCESS**.
- New Lean source 20 `#print axioms` declarations, standard `propext`, `Classical.choice`, `Quot.sound` at most; `sorryAx` zero; changed Lean warning/error 0/0.
- Pinned Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
- Original F54, F55/P92B, independent structural seams, GK4AV/AW/AX unchanged, public roots 107, strict 空 central, independent Kuu one presentation, Gray not reintroduced; protect #1558 Draft OPEN unmerged.

**Authority boundary:** Proved transvection and cone geometry alone does not imply a machine-checked free-product injection or a one-point original F54 polynomial injectivity theorem; free-product injection is established separately by GK4AZ.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
