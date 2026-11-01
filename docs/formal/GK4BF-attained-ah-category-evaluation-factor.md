# F112-P94D3GK4BF — 真正K_AIのAH到達像の圏構造と整数評価の関手因子化

2026-11-01 JST。canonical `main`、[定理PR #2854](https://github.com/itakura-hidetoshi/KuuOS/pull/2854) **MERGED**。

## 1. 数学的中心成果

GK4BEで、元F54完全依存型経路に由来する既存二次kernel圏 `K_AI` の各真の型付きHomに対して、実際に到達する旧AH行列だけのSubtype `NativeGK4BEAttainedAH first last` を作った。GK4BFはこれを**新しい真のMathlib Category** `NativeGK4BFAttainedAHStage`のHomとして構成する。

元の物理F54型付き境界と真のK_AI代表射を保持し、旧AH行列の非可換積で合成、旧K_AIの元ゼロ射から単位を得た。合成値の到達証拠は、元Qの圏公理を仮定せず、すでに証明されたK_AIの合成を使って実際の代表射を構成する。圏の結合律・左右単位は既存の整数行列積の数学的法則からLeanで証明した。

```text
      π_AH                    ι
 K_AI ------> AH_attained ------> Mat₂(ℤ)
    \\__________ F_AH __________/
```

- `nativeGK4BFImageFunctor`: 既存の真正K_AIから到達AH圏への関手。**各Hom上で全射**。忠実性を仮定・主張しない。
- `nativeGK4BFInclusionFunctor`: 到達AH圏から全整数行列一対象圏への関手。Subtypeの値をとるだけなので、**各Hom上で単射（faithful）**。全整数行列への全射ではない。
- `nativeGK4BFInclusion_factor_functor`: 両関手の合成が、既存`nativeGK4BDOldAHFunctor`と**Functor全体の等式として一致**する。

元K_AI→AH到達像のHom単射性が成り立つための必要十分条件は、「同じ型付きHomの任意の2類について旧AH観測値一致から類自体の等式を復元できること」。`nativeGK4BFImageFunctor_injective_hom_iff`がこの条件を証明する。**この条件が実際に成立するとは断言していない**。

## 2. GK4BEの一意因子化を実際のFunctorへ

GK4BEは各Homの到達AH値に対し任意整数tで評価値を一意に定めていた。GK4BFはこれを`nativeGK4BFAttainedEvaluationFunctor`という本物のMathlib Functorへ昇格させた。

```text
K_AI --π_AH--> AH_attained --Eval_t--> Mat₂(ℤ)
 |                                        ^
 |________________ F_t __________________|
```

全ての整数 `t` で上記は**Functor等式として可換**し、`t=4` では `Eval_4 = ι`、すなわち実際の旧AH値の包含そのものになる。整数行列演算は非可換のまま保持し、源の任意の行列値が実際に到達すると仮定していない。

## 3. Lean4新規16宣言

[新規Lean全文](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BFAttainedAHCategory.lean)。

- `nativeGK4BFAHUnit`・`nativeGK4BFAHUnit_val`・`nativeGK4BFAHCompose`・`nativeGK4BFAHCompose_class`: 真正K_AI射を証拠にした単位・合成・代表元計算。
- `nativeGK4BFAttainedAHCategory`: 元の型付き境界上のAH到達像Category。
- `nativeGK4BFImageFunctor`・`nativeGK4BFImageFunctor_surjective_hom`: K_AIからのHom全射関手。
- `nativeGK4BFInclusionFunctor`・`nativeGK4BFInclusionFunctor_injective_hom`: 整数行列値へのHom単射関手。
- `nativeGK4BFInclusion_factor_map`・`nativeGK4BFInclusion_factor_functor`: 旧AH関手の厳密因子化。
- `nativeGK4BFImageFunctor_injective_hom_iff`: faithfulnessを勝手に仮定せず、Hom単射性の正確な条件を形式化。
- `nativeGK4BFAttainedEvaluationFunctor`・`nativeGK4BFAttainedEvaluation_four`・`nativeGK4BFAttainedEvaluation_factor_map`・`nativeGK4BFAttainedEvaluation_factor_functor`: 任意整数評価の真のFunctorと可換性。

## 4. exact-source CI・authority

| 項目 | GitHub MCPで検証した事実 |
|---|---|
| 定理PR | [#2854](https://github.com/itakura-hidetoshi/KuuOS/pull/2854) MERGED |
| source HEAD | `a52a701341cc369b2211ea8111c83441b156b9ac` |
| test-merge HEAD | `5875ff8652c124de7964568cdc79f05462335070` |
| 両Git tree | `78971c18d8a155fc4498fa402945826fec1d3565` 完全一致 |
| [GitHub Actions #41256478785](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41256478785) | **Strict Lean 3800/3800 SUCCESS・Governance terminal SUCCESS** |
| Lean新規宣言 | 16宣言、全て`propext`、`Classical.choice`、`Quot.sound`の標準3公理以内 |
| sorryAx | 0 |
| theorem squash SHA（マージ時のmain） | `8c41653a55c28439bd4b1ec0ade255d34d41ef20` |

Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` 固定。公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft・OPEN・未マージ。

## 5. 未証明・obstruction

AH到達圏へのHom全射は、元K_AIのfaithfulness／元Type値経路・3-cellの一致を意味しない。元Q自身の結合律・左右単位も証明していない。固定旧類ファイバーの単一類無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは継続して未証明。今後は`ker(π_AH)`がどの程度厳密に非自明か、実在する元F54型付き射の衝突・obstructionを構成する問題が残る。

append-only／tighten-only／overwrite-forbidden／same-root107。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
