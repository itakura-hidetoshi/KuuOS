# F112-P94D3GK4BC — 既存 K_AI 上の多項式行列関手

2026-11-01 JST。canonical `main` / [定理PR #2847](https://github.com/itakura-hidetoshi/KuuOS/pull/2847) **MERGED**。

## 1. 数学的結論

GK4BB の真正多項式行列降下 `P̄:K_AI→Mat₂(ℤ[X])` は、既存の K_AI 合成と単位を保存する：

```text
P̄(nativeGK4AIKernelCompose t₁ t₂ t₃ u v)
  = nativeGK4AVMul (P̄ u) (P̄ v)
P̄(nativeGK4AIKernelUnit t₁) = nativeGK4AVOne
```

これは **元P92B商Qの合成の結合律・左右単位を仮定しない**。元F54依存型経路の非可換行列積と、そのP92B観測値保存を実証明した後、真の第二kernel商の代表元について `Quotient.inductionOn₂` で降下する。既存の K_AI 圏公理のみを使用する。

任意の整数 `t` で `eval_t(P̄(u∘v)) = eval_t(P̄u) · eval_t(P̄v)`。とくに `t=4` は、GK4BB が厳密に回収した旧AH行列成分の乗法と可換である。

## 2. 新規Lean4ファイルと9宣言

[証明全文](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BCPolynomialFunctorAI.lean)

1. `nativeGK4BCP92Polynomial_compose`：真正元Q上の多項式**観測**の積保存。
2. `nativeGK4BCP92Polynomial_unit`：元Qゼロ経路の多項式観測が単位行列。
3. `nativeGK4BCPolynomialOnAI_compose`：既存K_AI第二商の合成保存。
4. `nativeGK4BCPolynomialOnAI_unit`：既存K_AI第二商の単位保存。
5. `nativeGK4BCPolynomialOnAI_eval_compose`：任意整数評価の積保存。
6. `nativeGK4BCPolynomialOnAI_eval_four_compose`：`t=4`旧AH成分の積回収。
7. `nativeGK4BCPolynomialValueCategory`：非可換多項式2×2行列値の一対象圏。
8. `nativeGK4BCPolynomialValueFunctor`：真正K_AI圏から多項式行列値圏へのMathlib関手。
9. `nativeGK4BCPolynomialValueFunctor_structural`：独立構造商S→K_AI→多項式値と従来のS上多項式観測の可換性。

元F54のcast、forward、backward、RotationChain、DepthRotationRouteと二つの型付き文脈を保持。既存第二商への降下だけを使用し、元Type値の新たな3-cell、Gray圏、元Qの未証明圏公理を作らない。

## 3. exact-source CI

| 項目 | GitHub MCPで確認した値 |
|---|---|
| 定理PR | [#2847](https://github.com/itakura-hidetoshi/KuuOS/pull/2847) MERGED |
| source HEAD | `f93b85e7a8759e6f32760ab975f6728483e1df8e` |
| test-merge HEAD | `d2d061ef95a5c5bb68111af7cf2708d54d3ea639` |
| source/test-merge tree | `7b944c445e213662db7355e68989d29d774dca93`（完全一致） |
| [Strict Lean / Governance #41253944040](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41253944040) | **3797/3797 SUCCESS / Governance SUCCESS** |
| 変更 | 新規Lean1ファイル・215行追記 |
| 公理依存 | 9宣言すべて `propext`, `Classical.choice`, `Quot.sound` の標準3以内 |
| sorryAx | 0 |
| 定理squash = マージ時main HEAD | `b9ae3569a167c89b9b04d83ab53aceaf58412050` |

Lean v4.30.0-rc2、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107維持、保護PR #1558 Draft/OPEN/未マージ。

## 4. Authority／未証明事項

これは既存K_AIの多項式観測が関手として整合的であるという定理であり、多項式値Functorのfaithfulness、元QとSの同一性、元Q自身の圏公理、元Type値経路・3-cellの一致を意味しない。旧AH一点評価の多項式決定性（GK4BA）と、本K_AI商の識別能力は異なる問いである。

単一固定旧類ファイバーの無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは未証明のまま。

strict空中心・独立Kuuは一つのpresentation。append-only/tighten-only/overwrite-forbidden/same-root107、Gray非再導入。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
