# Qi v4.65 — 真正元P77・任意有限段の型付きパッチ列とType値局所降下

**2026年11月5日 JST**。strict 空中心、独立Kuuは一presentation。append-only／same-root／既存定理上書き禁止。元F55/P77/P94A・実際のC60物理Gauge・北C60 CRTを別の証拠authorityとして保存する。

| 項目 | GitHub MCP・exact-source検証 |
|---|---|
| Repository | `itakura-hidetoshi/KuuOS`, canonical `main` |
| 継承元 | Qi v4.64 定理 [#3149](https://github.com/itakura-hidetoshi/KuuOS/pull/3149)、文書 [#3150](https://github.com/itakura-hidetoshi/KuuOS/pull/3150) MERGED |
| 正本基点 | `6de6137c5b2a8ef6a1b843a0ffce444c38c955f1` |
| 定理PR | [#3151](https://github.com/itakura-hidetoshi/KuuOS/pull/3151) **MERGED** |
| 最終exact-source HEAD | `5e489962eba30feacc64787c1ae68f8776cec0da` |
| 定理squash/main | `daae34e653d0e85052efde5ac79bdc60253e1062` |
| 定理CI | [#42007067524](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42007067524) |
| Strict Lean | **10,262 / 10,262 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 公理監査 | 新規**19件**、標準 `propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| source/test-merge Git tree | `4a0150635275fe386ccf83620ee16ce9986add97` **完全一致** |
| 新規Lean全文 | [Qi v4.65 Lean](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FiniteTypedPatchChainDescentV4_65.lean) |
| 公開集約 | `formal/KuuOSFormal.lean`へ新規import１行、公開root107保持 |
| 固定Lean/mathlib | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護 | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ |

## 1. 任意有限段の真の型付き証拠構造

`FivefoldP77RawPatchBlock f g h k u v` は、元の型付き端点 `u,v`、任意の添字型 `Index : Type`、`Nonempty Index`、そしてその添字から元F55/P77生四セルへ至る`raw`写像を保持する。**生四セルそのものを数値chargeへ置き換えず**、互換性をデータ定義の内部へ隠さない。

各ブロックの互換性 `fivefoldP77RawPatchBlockCompatible` は次の二条件の連言である。

- 任意の二つの元patch `raw i`・`raw j` 間に**本物のGK5CG保守的Type値五セル**が存在する。
- あるpatch `raw i` に対し、元の型付きsource有向自由経路の真正P77評価から到達する**本物のGK5CG保守的Type値五セル**が存在する。

`FivefoldP77RawPatchChain` は `nil` と `cons block tail` を持つ依存帰納型である。任意個のブロックについて中間頂点の型を保存するため、これは数値のリストや無型の辺列ではない。零段の空鎖と任意有限段の鎖の両方を扱う。

## 2. 全段のdescent必要十分条件と一意性

`FivefoldP77RawPatchChainWitness` は各段について「すべてのraw patchを元の保守的P77商へ厳密に評価する真正`Quiver.Path`」を保存する、**Type値の証拠付き有限経路列**である。

主定理 `fivefoldP77RawPatchChain_witness_iff` は任意の有限型付き鎖`C`に対して、

```text
Nonempty (FivefoldP77RawPatchChainWitness C)
  ↔ fivefoldP77RawPatchChainCompatible C
```

を数学的帰納法で証明する。右辺は全段における**真正元GK5CG Type値五セルのpatch間互換性と各段の少なくとも一つの真正source anchor**の連言である。元四セルのchargeの範囲内という数値条件だけではない。

`fivefoldP77RawPatchChain_witness_subsingleton` は元P77 Faithful関手から全段の復元証拠付き経路列が高々一つであることを導く。互換性が成立するとき `fivefoldP77RawPatchChain_witness_unique` は `∃!` により存在と一意性を与える。これは元のsource有限経路列の型としての一意性であり、chargeだけの一致ではない。

## 3. 全有限鎖の真正合成・復元整合性

`fivefoldP77RawPatchChainPath` は各段で復元された**元有向source経路**を端点を壊さず連結する。`fivefoldP77RawPatchChainTarget` は各段の元F55/P77四セル商クラスを、真正元P77の保守的垂直合成によって順序通りに結合する。

`fivefoldP77RawPatchChainPath_eval` が証明する可換性は、

```text
OriginalP77Functor.map (TypedPathOfChain C witness)
  = OriginalP77ConservativeCompositeOfRawPatches C
```

である。左辺は元source有限経路の本物のFunctor像、右辺は元GK5CG Type値五セルの関係で商にした**本物のP77四セル**の垂直合成である。ゼロ段では元の反射四セル、帰納段では`Functor.map_comp`と元source patchの評価証拠を使う。

さらに `fivefoldP77RawPatchChainCertified` は元の証拠付き依存Subtype `FivefoldP77PartialDomain` 上に真の合成クラスを構成し、

```text
CertifiedChain.val = OriginalP77ConservativeCompositeOfRawPatches
PartialRecover(CertifiedChain) = TypedPathOfChain C witness
OriginalP77Charge(CertifiedChain.val)
  = Int.ofNat (TypedPathOfChain C witness).length
```

をLean4で証明する。`charge`は**Type値復元後の観測量**であって、元四セルの証拠同一性や到達可能性を決める手段ではない。

## 4. 正確な障害境界

`fivefoldP77RawPatchChain_cons_typeGap`は、ある指定段のGK5CG保守的Type値五セル互換条件が失敗すると、その段を含む**指定された因子別経路列の**復元証拠は存在しないことを形式化する。

これは全targetにおける任意の別の合成因子分解の否定ではない。元P77全targetへの全域復元、合成全体から中間patchすべてへの無条件到達反射、逆向きsource辺の捏造、新pentagonator、Grayや一般siteでのsheaf降下を主張しない。

## 5. Lean4の修正根拠と再検証

初期CIでは、元patchブロックが任意の添字`Type`・元F55/P77の依存データを保持するため、通常の`Type`に結果を固定した帰納型`FivefoldP77RawPatchChain`の`cons`で**宇宙レベル不足**が発生した。後続のidentifier未解決はこの帰納型の宣言不成立に連鎖した。元の証拠や命題を減らさず、帰納型を適切な高い`Type`に置き、依存再帰定義の束縛パラメータ等を固定Lean4構文に合わせて修正した。初回の失敗を成功と混同しない。

最終のexact-source HEADは`5e489962eba30feacc64787c1ae68f8776cec0da`。CI #42007067524でStrict Lean **10,262/10,262** SUCCESS、Governance **30/30** SUCCESS。19件の`#print axioms`は`propext/Classical.choice/Quot.sound`のみ、`sorryAx`なし。変更Lean warning/error 0/0。source/test-merge Git tree `4a0150635275fe386ccf83620ee16ce9986add97`完全一致。

## 6. 次の研究候補 Qi v4.66

有限型付きパッチ鎖に対して、**連結の結合・分割操作と局所Type値証拠の保存**、分割方法から独立した真正元P77商評価、局所障害の正確な伝播・非反射条件を形式化する。元の五セル証拠の履歴を保持し、一般のsource回収を全targetへ偽って延長しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
