# F112-P94D3GK4BB — 既存 K_AI への真正F54全多項式行列の降下

2026-11-01 JST。canonical `main` / [定理PR #2845](https://github.com/itakura-hidetoshi/KuuOS/pull/2845) **MERGED**。

## 1. 中心定理

GK4AVにより、元F54完全依存型経路の整数多項式行列`P_r(X) ∈ Mat₂(ℤ[X])`は、元F55全9、P92B全9、構造比較seam全14および拡張3構成子で保存され、元P92B存在商`Q`と独立構造商`S`へ別々に降下していた。GK4BAにより旧AH行列一つ、すなわち`P_r(4)`の一致が多項式行列全体の一致と同値であることもLean4で証明済み。

既存の第二kernel商`K_AI`の観測値は`O_AI=(O_AE,M_AF,M_AH)`であり、その最後の**実成分**は`M_AH=P(4)`である。したがって既存観測の等式から、元`Q`の多項式全体が代表元に依存せず一致する。これを固定mathlibの本当の`Quotient.lift`で定義した。

```text
NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last
    →  NativeGK4AVValue
```

定理`nativeGK4BBPolynomialOnAI`は、新しい商を導入せず**既存K_AIに全多項式族を降下**させる。

## 2. Lean4で証明した6宣言

[正式Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4BBPolynomialDescentAI.lean)。

1. `nativeGK4BBPolynomialOnAI`：元P92Bの真の商同値を保持した明示的`Quotient.lift`。
2. `nativeGK4BBPolynomialOnAI_class`：すべての元Q類の像が元`nativeGK4AVP92Value`と厳密に一致。
3. `nativeGK4BBPolynomialOnAI_eval_four`：任意`z ∈ K_AI`で、降下した多項式行列の`X=4`評価が`nativeGK4AIKernelValue z`の旧AH成分と一致。
4. `nativeGK4BBPolynomialOnAI_eq_iff_AH`：**K_AI上の多項式値の一致**が、その旧AH成分の一致と同値。これは`K_AI`のクラス`u=v`が旧AH一致と同値、という主張ではない。
5. `nativeGK4BBPolynomialOnAI_unique`：元Qの全代表元について元多項式値を復元する降下関数は一意。
6. `nativeGK4BBPolynomialOnAI_structural`：独立構造商S→既存K_AIの実比較写像と、既存のS側多項式降下との正確な可換三角形。

この結果は**元Q自身の未証明圏公理も、元Type値の新しい3-cellも必要としない**。独立構造商S、元Q、既存K_AIを同一視せず、その比較・出典・Type値境界を保持している。

## 3. exact-source 検証

| 項目 | 事実 |
|---|---|
| 正本定理PR | [#2845](https://github.com/itakura-hidetoshi/KuuOS/pull/2845) MERGED |
| source HEAD | `9617a45e331a52abd22ad2586be5216bc3360b7d` |
| CI test-merge checkout | `67840fc1e5404a453d360c3cdfd22e96a66d67e9` |
| 両Git tree | `579a1630f3226a98bf2d4ec3a0de979f6dc426f1` 完全一致 |
| [GitHub Actions #41253344455](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41253344455) | **Strict Lean 3796/3796 SUCCESS / Governance SUCCESS** |
| 新規Lean | 1ファイル、`#print axioms`6宣言 |
| 公理依存 | `propext`, `Classical.choice`, `Quot.sound` の標準3以内 |
| sorryAx・変更Lean warning/error | 0・0/0 |
| 定理squash = 当時canonical main HEAD | `2db3201782457854f7b5fdaeeeba4b086a273228` |

Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定。追加のみの拡張で公開root107を維持。保護PR #1558はDraft/OPEN/未マージ。

## 4. 数学的・authority境界

GK4BAで否定した「旧AH評価が同じなのに多項式が違う」という候補が、ここでは既存K_AIの普遍的な降下可能性へつながった。新しい多項式観測は、**既存K_AIが保存する情報以上に元Q/S類を分離できない**。これは多項式の全成分・全次数を同時に扱う定理であり、次数上界だけではない。

一方、K_AIの値には元四成分や別の旧AF行列も含まれるため、**多項式降下が忠実である、あるいはK_AIの元クラスが旧AHだけで一意になるとは主張しない**。K_AIから元Qや独立Sへの逆向き忠実性、真正14D無条件Countable、固定単一旧類ファイバー無限性、算術slice全域到達、19D filler、global strict、hyperdescentはなお未証明。

strict空中心、独立Kuuは空の一つのpresentation。Gray再導入なし。append-only／tighten-only／overwrite-forbidden／same-root107。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
