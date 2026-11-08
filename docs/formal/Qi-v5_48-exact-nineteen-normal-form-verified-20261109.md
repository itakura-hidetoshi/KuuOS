# Qi v5.48 — 真正19Dの型付き単位正規形と比較反映の条件

記録日：2026-11-09 JST

現行の `SelectedContextualEighteen` と `SelectedLocalNineteen` の定義を固定し、同じ厳密17D endpoint fiberの真正証拠値の範囲で認証する。空・縁起への対応づけは解釈であり、以下のLean4で証明した構造命題とは区別する。

## 1. 検証済み正本

- 定理PR [#3374](https://github.com/itakura-hidetoshi/KuuOS/pull/3374)：MERGED。新規Lean 271行、既存削除0。
- 公開import PR [#3375](https://github.com/itakura-hidetoshi/KuuOS/pull/3375)：MERGED。既存 `KuuOSFormal.lean` 全文を保持したimport 1行追加。
- [Lean形式証明全文](https://github.com/itakura-hidetoshi/KuuOS/blob/03d59e8cfa63e89baad79f644832f8735cc55006/formal/KUOS/Architecture/QiWuxingGK5CHP77ExactNineteenUnitNormalFormV5_48.lean)
- [公開Lean集約](https://github.com/itakura-hidetoshi/KuuOS/blob/098875873b7592ae1264b8ac921c274b4c3e9250/formal/KuuOSFormal.lean)

| 認証 | 定理単体 | 公開集約 |
| --- | --- | --- |
| exact-source CI | [#42528265204](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42528265204) SUCCESS | [#42528894967](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42528894967) SUCCESS |
| Strict Lean | 9,100 / 9,100 | 10,361 / 10,361 |
| Governance jobs | 5 / 5 SUCCESS | 32 / 32 SUCCESS |
| 新規公理監査 | 14 / 14 標準公理のみ | 定理を公開importして全体再検証 |
| `sorryAx` | なし | 公開Leanログ内なし |
| 変更Lean error / warning | 0 / 0 | 0 / 0 |

定理HEAD `095487b83c56ffe908f147fbddbd197fd3adbeea`、test-merge `1bc8e7b04ab5d79154ce4c0c826de81053a8865c`、squash/main統合 `03d59e8cfa63e89baad79f644832f8735cc55006` は共通tree `f4be6b4eeff7087d4e391645ce491cb6da732009` を持つ。

公開import HEAD `ff3a49c49514ff5c7c9eb8fc9b95fc8ff50a197f`、test-merge `879506a4638801eb4a0664529f7616fa58308814`、squash/main統合 `098875873b7592ae1264b8ac921c274b4c3e9250` は共通tree `2c4a5f1f8825b07e3f6c03297a986a65f91124db` を持つ。

初回定理CI [#42527953347](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42527953347)は `selectedNineteenNormal_rawCertified` を `theorem` と宣言したため失敗した。真正 `SelectedLocalNineteen` はPropでなくType値であり、Leanでは `theorem` の結論はPropに限る。修正はこの宣言を `def` に変更する1箇所だけで、証拠をProp化せず元の型を維持した。修正後、変更全文271行・依存定義・14件の公理出力を再照合し、上記exact-source CIに成功した。

## 2. 元selected19比較の範囲

既存 `SelectedLocalNineteen` の構成子は `strict`（反射）、`unitPrepend`、`unitAppend`、`reverse`（対称）、`chain`（推移）の5種。二つの単位生成元は真の旧18D `inherited M` に直結する `chain (strict J) (inherited M)` と `chain (inherited M) (strict N)` だけを比較する。raw18D `reverse`、`chain`、whiskeringを含む任意の構文文脈へその比較を拡張する生成元はない。

## 3. Type値の正規代表と必要十分な比較条件

`selectedNineteenNormalCertified` は各元raw18D証拠 `M : J → N` から、同じ厳密fiberの元raw証拠 `K` と真正 `SelectedLocalNineteen M K` のSigmaペアを構成する。上記二つの直接単位挿入だけを元 `inherited M` に縮約し、その他の構文は元のまま保持する。新しい比較公理、証拠値の数値への置換、異なるfiberの同一視は導入していない。

厳密なLean定理 `selectedNineteenNormal_eq_iff_local` は次である。

```text
Normal(M) = Normal(L)
  ↔ Nonempty (SelectedLocalNineteen W l r M L)
```

`selectedNineteenNormal_eq_iff_class` により、上の両条件は `selectedNineteenClass M = selectedNineteenClass L` とも同値になる。逆方向の比較証拠は、二つの元Type値正規化証拠を `reverse` と `chain` で貼り合わせて実際に構成する。`Normal(Normal(M)) = Normal(M)` も証明した。

同一厳密fiberの商から元raw Type値へ `selectedNineteenNormalOnQuotient` を構成し、`selectedNineteenClass (NormalOnQuotient(q)) = q`（section）と正規代表の単射性を証明した。これはraw証拠をすべて等号に潰すことではなく、商の各クラスに元の型を持つ代表を与えること。任意のWやfiberにおける正規代表の等号判定が計算可能・決定可能という主張はしていない。

## 4. 残存障害と境界のfaithfulness

v5.47で構成した `AdjacentReverseLeft M` と `AdjacentReverseRight M` は、与えられた元証拠Mの同一J→N fiberで完全ordered traceと六変量が一致する。しかし `AdjacentReverseCount` の差により真正19D商クラスが異なる。v5.48の `selectedNineteenNormal_separatesAdjacentReverse` はその正規代表も異なることを証明した。

任意に与えられた型付きLR→RL境界Bについて、`selectedMixedBoundary_reflection_iff_injective` は次を証明する。

```text
Nonempty (∀ {X Y}, SelectedLocalNineteen (B.rawTransport X)
                   (B.rawTransport Y) → SelectedLocalNineteen X Y)
  ↔ Function.Injective (selectedMixedBoundaryDescend B)
```

さらに `selectedMixedBoundary_normalReflection_iff_injective` は、輸送先の正規形の一致から元の正規形の一致を反映する条件とも同値であることを証明する。すべて厳密な各LR/RL endpoint fiber内での等号・比較であり、heterogeneous raw equalityは使わない。逆方向で元Type値の比較を取り出す際の `Classical.choice` は標準公理監査に現れる。

これは**与えられた境界に対する必要十分条件**である。一般の忠実LR→RL境界の存在・不存在、無条件20D交換・gluing、全fiber居住性、全域swap自然性、あらゆる文脈の正規化は未認証のまま保持する。

## 5. 全14宣言の公理監査

修正後の固定Lean `#print axioms` 出力を全件照合した。公理不要0件、標準公理のみ14件、`sorryAx`なし。各宣言に現れた公理依存は次のとおり。

| 宣言 | 公理依存 |
| --- | --- |
| `selectedNineteenNormalCertified` | `propext` |
| `selectedNineteenNormal` | `propext` |
| `selectedNineteenNormal_rawCertified` | `propext` |
| `selectedNineteenNormal_respects` | `propext` |
| `selectedNineteenNormal_eq_iff_local` | `propext` |
| `selectedNineteenNormal_eq_iff_class` | `propext, Quot.sound` |
| `selectedNineteenNormal_idempotent` | `propext` |
| `selectedNineteenNormalOnQuotient` | `propext` |
| `selectedNineteenNormalOnQuotient_onClass` | `propext` |
| `selectedNineteenNormalOnQuotient_section` | `propext, Quot.sound` |
| `selectedNineteenNormalOnQuotient_injective` | `propext, Quot.sound` |
| `selectedNineteenNormal_separatesAdjacentReverse` | `propext, Quot.sound` |
| `selectedMixedBoundary_reflection_iff_injective` | `propext, Classical.choice, Quot.sound` |
| `selectedMixedBoundary_normalReflection_iff_injective` | `propext, Quot.sound` |

## 6. 保存条件・次段

公開root107、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、元F55/P77/GK5CGと6D–19D全元証拠、保護PR #1558のDraft／OPEN／未マージを維持。運用はappend-only／tighten-only／overwrite-forbidden／same-root。

次段Qi v5.49の研究候補は、得られた厳密正規代表について直接単位クラスの形をさらに分類し、型付き文脈内操作の保存条件と反例を明確にすること。正規化された値の数値化や、未証明の文脈合同性を追加してはならない。

本記録とREADME・ROADMAPの追記はdocs-onlyで行い、Leanは変更しない。docs-only CIのStrict LeanはSKIPPEDとして独立判定する。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
