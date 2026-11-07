# Qi v5.06 — 三整数・二偶奇では不可視な混合逆元消去の法4障害

## 0. Canonical正本・exact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.05統合済み正本 `b1c0579cdb254111ee76362b06801b4eaddfadbe` から継承した。

| 項目 | 確認結果 |
|---|---|
| 定理PR | [#3235](https://github.com/itakura-hidetoshi/KuuOS/pull/3235) **MERGED** |
| 定理squash | `31d12d464121206bba9b8a1711bef476bd9ae52f` |
| exact-source CI | [#42319414530](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42319414530) **SUCCESS** |
| Strict Lean | **10,305 / 10,305 SUCCESS** |
| Governance | **SUCCESS**：30 job、失敗なし |
| 新規宣言公理監査 | **26宣言**：標準公理 `propext`、`Classical.choice`、`Quot.sound`、または依存なし |
| `sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0** |
| 検証source HEAD | `5520d5141d4a5c9fccfb8f2d484bb1171ba3bfc6` |
| exact-source test-merge HEAD | `27aad008436fbe1ca510befc03ae46223af568c5` |
| source/test-merge Git tree | **`613d4cd02a2b3d07ee023ba23d6967e77ed7623d` 完全一致** |
| 固定Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR #1558 | Draft／OPEN／未マージ（維持） |

[Qi v5.06 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedInverseCompResidueObstructionV5_06.lean) ·
[前段Qi v5.05正式記録](Qi-v5_05-original-P77-double-composite-minimal-higher-completion.md)

## 1. v5.05からの数学的問題

Qi v5.05では、独立`DoubleCompositeEightCell`に最小の比較生成元を1種類追加した。
その完全な構成子と型付き文脈について、元整数Vの法4剰余

```lean
sevenTotalReductionResidue s = sevenTotalReductionCharge s % 4
```

を保存することが証明された。旧第四整数Rと元単位則カウントUの偶奇も降下した。
これらの値が等しいだけで任意の平行履歴に比較があるという十分性は、
**証明していない**。今回は具体的な新たな比較不能性を形式構成する。

## 2. 元の2種類の七セルcritical pairの混合

真正な第一因子はQi v5.04の`sevenCompositeInverseCancelDirect/Via`である。
同じraw六セル始終点に対し、直接逆元消去と逆元分配・再結合・逐次消去を比較する。

真正な第二因子はQi v5.02の
`sevenInverseUnitRightDirect/Via`である。
元`inverseRight(refl(w))`と
`inverseId`を適用した後の`rightUnit`を、同じ元六セル始終点上で比較する。

これらを`SevenRewrite.congrComp`で横合成したものが

```lean
sevenMixedCancellationFirst w
sevenMixedCancellationSecond w
```

である。元の六セル生構文を保存したまま、次が成立する。

```text
観測量                     First       Second
旧 T                       2           2
旧 J                       0           0
旧 K                       0           1
R mod 2                     0           0
U mod 2                     0           0
整数 V                      2           4
V mod 4                     2           0
raw六セル始終点             同一        同一
```

RとUの偶奇差は二つの因子の間で相殺されるが、
Vの差2は残る。ただし**旧K値には1の差がある**ので、
この二因子前駆例を三整数まで不可視なものとは呼ばない。
その差を次段で真正な旧critical pairにより相殺する。

## 3. 元v4.95の真正inverseComp左critical pairによるK相殺

第三因子は以前から定義されている

```lean
sevenInvCompLeftDirect (.refl w)
sevenInvCompLeftVia (.refl w)
```

である。directは旧Kが0、viaは旧Kが1。
二つは同じraw六セル始終点を持ち、
元`InverseCompEightCell.leftOverlap`という
既証明の旧八セル比較により局所的に比較できる。

第三因子を**第一経路へvia、第二経路へdirect**として
横合成し、次の元自由七セル履歴を構成する。

```lean
sevenMixedResidueFirst w
sevenMixedResidueSecond w
```

Leanでは元六セルraw始終点`mixedResidueSource/Target`を明示した。
これにより元三整数Kの差は厳密に相殺される。
二つの七セル履歴は同じ元六セル始終点と独立の元Type値証拠履歴を保持する。

```text
観測量                     First       Second
元三整数 (T,J,K)           (2,0,1)     (2,0,1)
旧 R mod 2                 0           0
旧 U mod 2                 1           1
整数 V                     3           5
新 V mod 4                 3           1
raw六セル始終点             同一        同一
```

元三整数の一致、二つの旧偶奇の一致、そして法4値の相違を
それぞれLean定理`sevenMixedResidue_tripleValues`、
`sevenMixedResidue_parityValues`、
`sevenMixedResidue_totalValues`、
`sevenMixedResidue_residueValues`として証明した。

## 4. 現行独立八セルpresentationの比較不能性

Qi v5.05の`doubleCompositeEightCell_preservesTotalReductionResidue`は
旧全比較生成元と新`doubleComposite`を含む**完全な選択grammar**で
法4保存を保証する。

もし二つの強い三因子履歴に
`DoubleCompositeEightCell`比較が存在すれば、
その保存則から整数等式`3=1`が従って矛盾する。

```lean
sevenMixedResidue_noDoubleCompositeComparison
sevenMixedResidue_distinctDoubleCompositeClasses
sevenTripleAndParities_notCompleteAfterDoubleComposite
```

このため旧三整数と両偶奇が一致しても、
現行選択八セルで比較できるという主張は**偽**である。
これは比較を未発見という報告ではなく、構成子保存則を用いた非存在証明である。

さらに`sevenTotalReductionResidue_notFactorThroughOldObservations`により
V mod 4は、元三整数と旧二偶奇の組に対する
**任意の非線形関数**としても普遍的に復元できないことを示した。

ただしV mod4の値が一致したときの比較の十分性、
障害の完全分類、大域的thin性は主張しない。

## 5. 真正P77/GK5CG sourceへの輸送

元の`pentagonAdjoinedSixCell_generator`を使用し、
同一の元source六セルを`congrComp`で貼る。

```lean
sevenMixedResidueCompositeFirst c
sevenMixedResidueCompositeSecond c
```

これらに対する`sevenMixedResidueComposite_values`は
旧三整数と二偶奇の一致、V mod 4の3対1の差を保持する。
`sevenMixedResidueComposite_noDoubleCompositeComparison`で
貼り合わせ後にも比較不能であることを形式証明した。

`pentagonActualMixedResidueWithSourceObstruction`は
**任意の真正P77最終raw添字**で、元GK5CG Type値sourceを持つ
これらの二履歴と旧観測量の一致、比較不能性、
`¬ PentagonAdjoinedSixCellEqualityInterpreter`の維持を同時に保証する。

これは元F55/P77/GK5CG sourceのstrict Eqと
高次商のEqを同一視するものではない。

## 6. 検証履歴と変更境界

新規Leanモジュール1件（482追加行）と、
公開集約`formal/KuuOSFormal.lean`へのimport1行だけを追加した。
元の自由七セル／八セル／高次商／source証拠ファイルは変更していない。

初回のexact-source CI #42319414530はSUCCESS。
固定Lean・mathlibでの`lake build KuuOSFormal`と新モジュールのチェックが
**10,305/10,305 SUCCESS**、
新26宣言の公理は標準公理のみ・`sorryAx`なし、
変更warning/error0/0だった。
同一Git treeでのsource/test-merge検証と
Governanceの完了成功を確認してから定理PRをsquashマージした。

## 7. 未証明事項・次のQi v5.07

今段階では次を証明していない。

- 任意の平行七セル履歴の比較可能性
- V mod 4の一致からの比較存在という十分性
- 旧観測量と新観測量の大域的な完全分類
- 元source strict Eqと高次商Eqの同一視
- 九セル以上の大域thin性

Qi v5.07候補では、今回証明済みの強い三因子障害に対して
既存構成子の局所閉包を先に精査する。
必要な場合に限り、元sourceを変更せず
**独立した次の高次presentationに新比較生成元を一種類だけ追加**
することを検討する。
新しい比較を追加した場合にはV mod4の非降下と
より粗い残余観測量の降下境界を再検証する。

append-only／tighten-only／overwrite-forbidden／same-root。
公開root107、保護PR #1558 Draft／OPEN／未マージを維持する。
