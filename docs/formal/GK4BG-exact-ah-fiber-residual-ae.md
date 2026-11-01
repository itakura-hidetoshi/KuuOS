# F112-P94D3GK4BG — 真正K_AIの固定AHファイバーと残余AE観測の厳密分類

2026-11-01 JST。canonical main。[GK4BG定理PR #2856](https://github.com/itakura-hidetoshi/KuuOS/pull/2856) **MERGED**。

## 数学的成果

GK4BA〜GK4BEの本来の元F54依存型ルートと実際の第二kernel K_AIを使う。旧AH行列が等しければ、元F54の整数多項式行列全体が等しく、そのt=1特殊化である旧AF行列も等しい。したがって同じ型付きHomに属する二つのK_AI類 u,v について：

```text
M_AH(u) = M_AH(v) ならば
  u = v  ↔  O_AE(u) = O_AE(v)
```

旧AE観測はBoolean gradeおよび旧GK4ADの非可換順序付き三成分 `((charge, backwardCount), orderedMoment)` である。**AHが等しい場合、AFは独立した残余障害ではない。**

任意の整数行列 A を指定し、元F54の完全依存型Homを保存して `NativeGK4BGFixedAHFiber first last A` を構成する。Aが到達不可能ならこの型は空。さらに固定A上で**実際に到達するAE値だけ**から `NativeGK4BGAttainedResidualAE first last A` を構成し、

```text
NativeGK4BGFixedAHFiber first last A
  ≃ NativeGK4BGAttainedResidualAE first last A
```

を本物のLean `Equiv.ofBijective` により証明した。よって固定AHファイバーが二つの異なる類を含むことと、同じファイバーで異なる実到達AE値が二つ存在することは必要十分。

**重要な境界：** 本定理はどちらかの存在を仮定・断言しない。元P92B商Qの結合律・単位律や元Type値3-cellを付け加えていない。

## 真正自己Homにおける物理的制約

GK4ACの既証明によって、元F54の完全型付き自己Homで後退物理回転数が0なら全物理回転数も0。そのためBoolean gradeは必ず `true` になる。

これを第二kernel K_AIのAH観測と旧ADの実成分に沿って形式化し、両類の後退数0かつAH一致を仮定すると

```text
u ≠ v  ↔  ordered_AD(u) ≠ ordered_AD(v)
```

を証明。これも**非忠実性の反例の実在を証明するものではない**。真正型付きの経路を構成できない単なる記号積 `C·F=I` は根拠として採用しない。

## 形式化12宣言

[正式Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BGResidualAEFiber.lean)。

- `nativeGK4BGKernelAF_eval_one`: AFは実多項式のt=1成分。
- `nativeGK4BGKernelAH_eq_implies_AF_eq`: AH一致からAF一致。
- `nativeGK4BGKernelAH_eq_class_iff_AE_eq`: AH固定時の元類一致とAE一致の同値。
- `NativeGK4BGFixedAHFiber`: 真のAH固定ファイバー。高次宇宙を保持。
- `NativeGK4BGAttainedResidualAE`: 真の固定AH上の到達AE像。
- `nativeGK4BGFixedAHToResidualAE`: 固定ファイバーから残余像への写像。
- `nativeGK4BGFixedAHToResidualAE_injective` と `_surjective`: 単射性・全射性。
- `nativeGK4BGFixedAHFiberEquivResidualAE`: 実際の全単射。
- `nativeGK4BGFixedAH_nontrivial_iff_residual`: 非自明ファイバー存在の必要十分条件。
- `nativeGK4BGSelf_zeroBackward_grade_true`: 後退回転0自己Homのgrade true。
- `nativeGK4BGSelf_zeroBackward_collision_iff_AD`: その範囲でADだけが障害になり得ることの条件付き同値。

## exact-source Lean4 / CI と修正理由

| 項目 | GitHub MCP確認 |
|---|---|
| 定理PR | [#2856](https://github.com/itakura-hidetoshi/KuuOS/pull/2856) MERGED |
| 最終source HEAD | `1375b66b29c2dc13d92abb42305c610abf17f5cf` |
| 最終test-merge HEAD | `db1160da9054d99c702944694b693f7eea4e3496` |
| 共通Git tree | `139e402b8f21d16ab3da577379eb840bf6246e26` 完全一致 |
| [exact-source CI #41258432374](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41258432374) | **Strict Lean 3801/3801 SUCCESS・Governance terminal SUCCESS** |
| 全12宣言公理依存 | `propext`、`Classical.choice`、`Quot.sound` の標準3以内 |
| sorryAx | 0 |
| 定理squash（マージ時canonical main） | `b7c172c39a3e55ee18dfb7215b6c4237fff00c5d` |

初回のLean失敗は、`NativeGK4BGFixedAHFiber` を単純な小さい `Type` と宣言したため、元F54の依存型K_AI Homが持つ大きな宇宙レベルと一致しなかったこと。初回はそのエラーから複数の見かけ上の型不一致および `sorryAx` 表示が派生した。定義の帰属宇宙を `Type (max (max uD uE) (max vD vE))` に修正し、**新しい正本source HEADで全文を再コンパイルした**。同じ12宣言で標準公理のみを独立確認済み。

## authority と次の研究課題

固定Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、strict空中心・独立Kuu一presentation、Gray非再導入、保護PR #1558 Draft／OPEN／未マージを維持。

未証明なのは、固定AHファイバーの実際の非自明性、またはその不可能性によるAH functorの忠実性。さらに元Q自身の圏公理、元Type値完全同値、固定単一旧類ファイバー無限性、算術slice全域到達、真正14D無条件Countable、19D filler、global strict、hyperdescentは未解決。

次候補GK4BHは、GK4BAの自由積語決定性からGK4AD順序付き履歴まで決定できるかを数学的に解析し、型付き本物のF54証拠でAH観測の忠実性または非忠実性を決着させる。未検証結論を既証明として扱わない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
