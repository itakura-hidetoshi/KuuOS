# Qi v4.67 — 真正元P77の証拠付き有限鎖の切断同値・三段結合整合性

**2026年11月5日 JST**。KuuOS strict 空中心、独立Kuuは一つのpresentation。append-only／same-root／旧定理上書き禁止、元F55/P77/P94Aの証拠・元C60物理Gauge・北C60 CRTのauthorityを区別して維持する。

| 項目 | GitHub MCP exact-source検証 |
|---|---|
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / `main` |
| 継承元 | Qi v4.66 定理 [#3153](https://github.com/itakura-hidetoshi/KuuOS/pull/3153)、正式記録 [#3154](https://github.com/itakura-hidetoshi/KuuOS/pull/3154) MERGED |
| 基点main | `ec96ff9e72bb199732298e6b0aba450af798a8ea` |
| 新定理PR | [#3155](https://github.com/itakura-hidetoshi/KuuOS/pull/3155) **MERGED** |
| exact-source HEAD | `7464aee9db5197d4696d18030cdee0c64da30c51` |
| 定理squash/main | `ef6aa75440849f6af59aa5fa082d8e87e84e4ab5` |
| CI | [#42025070757](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42025070757) |
| Strict Lean | **10,264 / 10,264 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 公理監査 | 新規**11件**、`propext`／`Classical.choice`／`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| source/test-merge Git tree | `b7e50f71d038355a92afcf4864a0519ebca996db` **完全一致** |
| 新規Lean全文 | [Qi v4.67](../../formal/KUOS/Architecture/QiWuxingGK5CHP77WitnessCutTripleCoherenceV4_67.lean) |
| 公開集約 | `formal/KuuOSFormal.lean` に新規import１行追記、公開root107維持 |
| Lean / mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護 | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ |

## 1. 前段の形式正本と今回の切断

Qi v4.65の`FivefoldP77RawPatchChain`は任意有限段の元F55/P77生四セルの**型付き**patch族を保持し、`FivefoldP77RawPatchChainWitness`は各段の真正source有限経路とその元P77保守的商評価の証拠を保存する。Qi v4.66は途中の真正`FivefoldPathVertex`を切断点として、元Type値GK5CG保守的五セルの互換条件を壊さずに左右の鎖を連結する。

今回`fivefoldP77RawPatchChainSplitWitness`を追加し、**任意の指定cut**のもとで連結済み証拠付きsource経路列を左部分・右部分の真正証拠付きTypeへ分解した。これは元の型付き端点と四セルを失わず、数値chargeや新しい逆source辺を用いない。

## 2. 真正Type-level cut Equiv

`W(C)`を元F55/P77 patch鎖`C`の真正source経路列の証拠付きType、`L ++ R`をv4.66の本物の依存鎖連結とする。

```text
W(L ++ R) ≃ (W(L) × W(R))
```

`fivefoldP77RawPatchChainCutWitnessEquiv`はこの型同値を実装する。前向きは元依存鎖からの`SplitWitness`、逆向きは既証明の`AppendWitness`である。両側の真の逆法則はv4.65で証明済みの元P77 Faithful性からの`Subsingleton`を用いる。旧証拠の型を数値の同値へ置換したわけではなく、Leanの`Equiv`という完全なType値である。

`fivefoldP77RawPatchChainCutWitness_nonempty_iff`はこれを証拠存在の必要十分条件へ接続する。`fivefoldP77RawPatchChainSplit_path`は、分割した元source経路を合成した結果が、元の連結鎖を一度に復元した**真正source`Quiver.Path`そのもの**に一致することを形式証明する。

## 3. 三段型付き鎖の結合順序独立性

連続する三つの型付き元patch鎖`L : u→v`、`M : v→w`、`R : w→t`について、`(L ++ M) ++ R`および`L ++ (M ++ R)`それぞれの真正source証拠付きTypeを`fivefoldP77RawPatchChainTripleLeftWitness`／`TripleRightWitness`で明示構成する。

- `fivefoldP77RawPatchChainTriple_witness_transport`：v4.66の実際の依存鎖結合等式に沿って左側の元Type値証拠を輸送すると、右側の証拠に**厳密に一致**する。
- `fivefoldP77RawPatchChainTriple_path_coherence`：元sourceの型付き有限経路がどちらの括り方でも完全に同一となる。使用する結合律は固定mathlibの`Quiver.Path.comp_assoc`であり、新しい高次生成元を仮定しない。
- `fivefoldP77RawPatchChainTriple_target_coherence`：元GK5CG Type値五セルで構成した**真正元P77保守的四セル商**の最終値が括り方に依存しない。
- `fivefoldP77RawPatchChainTriple_certified_coherence`：さらに元source到達性証拠を備えた`FivefoldP77PartialDomain`のクラスも、`Subtype.ext`によって厳密に一致する。

これは三段有限鎖の具体的な結合整合性であり、新しいpentagonatorを付与したものでも、任意の高次圏構造を仮定したものでもない。

## 4. 因子別障害とauthority境界

`fivefoldP77RawPatchChainTriple_middle_obstruction`は、中間鎖の元GK5CG保守的Type値五セルによる局所互換条件が失敗すれば、**指定された三段因子別連結**が失敗することを示す。全元P77 targetの任意合成から中間Homへ無条件に原像を復元するとは主張しない。

元F55/P77/P94A、独立Kuu、北C60物理GaugeとCRTは別authorityであり、元四セル・元五セル・charge整数・物理リンクを同一のTypeにしない。全targetへの全域逆関手、一般sheaf descent、逆向きsource辺の捏造、Gray圏復元、新pentagonatorは禁止・未証明のまま保持する。

## 5. 監査と次段階

最終exact-source CI #42025070757 で全**10,264/10,264** Lean jobs成功、Governance **30/30**成功。新規11件の`#print axioms`は`propext/Classical.choice/Quot.sound`の範囲に留まり`sorryAx`0、変更Lean warning/error 0/0、source/test-merge Git tree `b7e50f71d038355a92afcf4864a0519ebca996db`一致。既存証明やtoolchain pinは変更せず、新規Leanファイルと公開集約importだけを追加してマージした。

**次のQi v4.68候補：** 任意有限個の指定cutに対する再括弧付けを、既存のstrictな型付き結合律と元P77証拠付きsource経路の一意性から一般化する。局所因子分解のための必要十分Type値条件を維持し、元P77全targetへの不正な復元や新たなpentagonatorを導入しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
