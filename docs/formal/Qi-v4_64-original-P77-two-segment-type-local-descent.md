# Qi v4.64 — 真正元P77の二段Type値局所降下と経路合成証明

**2026年11月5日 JST**。strict 空中心、独立Kuu一presentation。append-only／same-root／旧定理上書き禁止、元F55/P77/P94AとC60物理Gauge・CRTを別authorityとして維持。

| 項目 | GitHub MCPで検証済み |
|---|---|
| Repository / branch | `itakura-hidetoshi/KuuOS` / `main` |
| 元定理 | Qi v4.63 [PR #3147](https://github.com/itakura-hidetoshi/KuuOS/pull/3147)／文書 [#3148](https://github.com/itakura-hidetoshi/KuuOS/pull/3148) MERGED |
| 新定理PR | [#3149](https://github.com/itakura-hidetoshi/KuuOS/pull/3149) **MERGED** |
| 定理正本基点 | `3b766d9297e8e01d8b763b169a65fa995af8d3b9` |
| exact-source HEAD | `b07cbe512047181c0d9aadb53e41e961efc40175` |
| 定理squash SHA | `eafe0036cd9a8433554fa93bff4ca0ea59a6239c` |
| Exact-source CI | [#42001754689](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42001754689) |
| Strict Lean | **10,261 / 10,261 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **10件**、標準`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| Source / test-merge Git tree | `457467cc1a37960b2be0096ea73d06659a0cfce2` 完全一致 |
| 定理Lean全文 | [Qi v4.64 module](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TwoSegmentLocalTypeDescentV4_64.lean) |
| 公開 | `formal/KuuOSFormal.lean`へ１import追記、公開root107維持 |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR | [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ |

## 1. 成立する真の局所Type値証拠

v4.63の同一Homの非空元F55/P77 raw四セルpatch族に対する`fivefoldP77LocalTypeDescent_iff`を、連続する**二つの異なる型付きHom** `u→v`／`v→w` へ接続した。`left : I → FivefoldP77LocalRaw u v`、`right : J → FivefoldP77LocalRaw v w` を非空添字族とする。元GK5CGのType値五セルの存在を `a ~ b` と表す。

```text
(∃ p : Quiver.Path u v, ∃ q : Quiver.Path v w,
   (∀ i : I, OriginalP77.map p = [left i]) ∧
   (∀ j : J, OriginalP77.map q = [right j]))
↔
(∀ i i' : I, left i ~ left i') ∧
(∃ i : I, ∃ p : Quiver.Path u v, EvalP77(p) ~ left i) ∧
(∀ j j' : J, right j ~ right j') ∧
(∃ j : J, ∃ q : Quiver.Path v w, EvalP77(q) ~ right j)
```

ここで `~` は整数charge等号でも一般的な数値比較でもなく、**元の真正GK5CG conservative Type値五セルの存在**である。元証拠へのsource有向経路anchorが各段につき少なくとも一つ必要。必要十分条件を`fivefoldP77TwoPatchLocalDescent_iff`で証明し、v4.63の局所降下一意性から経路ペア`(p,q)`が**一意**であることも`fivefoldP77TwoPatchLocalDescent_unique`で証明した。

## 2. 元P77垂直合成とsource型付き経路の可換性

上で証拠付けられた二つの元source有限経路`p : u→v`、`q : v→w`について、任意のパッチ対`(i,j)`で真正元P77保守的四セル商の実際の垂直合成を保持し、

```text
OriginalP77.map (p.comp q)
  = OriginalP77Compose [left i] [right j]
```

を`fivefoldP77TwoPatch_composition_evaluates`で証明した。新しい証拠付き依存Subtype上の真正部分Hom`fivefoldP77TwoPatchCertifiedComposite p q`を構成し、その元P77商値が各パッチ対の合成と正確に一致する定理と、**復元結果が元の型付きsource経路`p.comp q`に等しい**定理を追加した。

```text
PartialRecover(TwoPatchCertifiedComposite p q) = p.comp q
OriginalCharge((TwoPatchCertifiedComposite p q).val)
  = Int.ofNat ((p.comp q).length)
```

Chargeの等号はsource経路の真正Type値復元**後**の観測結果であり、chargeの数値一致を証拠の同一視に置換しない。

## 3. 降下失敗の正確な境界

`fivefoldP77TwoPatch_leftTypeGap_blocks_factorization`は、指定した左patchに任意の元source有限経路評価から到達するType値五セルが全く存在しなければ、指定の局所二段source経路ペアが存在しないことを証明した。また元の真正zero-charge逆`e01`＋五角形ループ（元P77 targetの端点1→0）が左patchに含まれるときは、そのchargeが`0`であっても**指定の二段局所降下を阻む**ことを元v4.59の未到達証明に接続した。

**証明していないこと：** 元P77全targetの任意合成から、それを構成した任意の指定中間Homの到達可能性を反射すること。二段合成が偶然source到達可能でも、各指定パッチが個別に復元できるとは無条件に主張しない。元P77全targetへの全域復元、非証拠的なchargeだけのgluing、任意siteのsheaf条件、新しい逆source辺、pentagonator、Grayは導入しない。

## 4. Lean4 exact-source と監査

固定Lean／mathlibにより [CI #42001754689](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42001754689) は、**10,261/10,261**モジュールSUCCESS、Governance **30/30** SUCCESS。新規10件`#print axioms`は標準公理`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`0。変更Lean warning/error 0/0、source/test-merge Git tree `457467cc1a37960b2be0096ea73d06659a0cfce2`完全一致。既存Leanファイルを上書きせず、独立新規モジュールと公開集約importだけを追加してsquashマージ済み。

**Qi v4.65以降の候補：** この「二つの証拠付きHomの合成降下」を、型付き有限列への帰納・patch間互換条件の可換性・局所的Type値障害の配列として一般化する。合成全体から各段の到達可能性を無条件に逆推論することは避け、独立Kuu・strict空、P77、C60のauthorityと型付き履歴を維持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
