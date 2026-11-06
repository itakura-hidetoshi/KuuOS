# Qi v5.01 — 単位則ダイヤモンドの独立八セル最小局所補完・残余偶奇の降下

## 0. Canonical正本・exact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
継承元はQi v5.00までMERGEDの`c10b976b845815deedefeaf3fab816cca42cd1db`。

| 検証項目 | 実測結果 |
|---|---|
| Qi v5.01定理PR | [#3225](https://github.com/itakura-hidetoshi/KuuOS/pull/3225) MERGED |
| 定理squash SHA | `f26f19d2f4cb1ed1e561904ba7f5167aa58fe3ae` |
| exact-source CI | [#42305483543](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42305483543) SUCCESS |
| Strict Lean | **10,300 / 10,300 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規定理・宣言公理監査 | **45宣言**、`propext`／`Classical.choice`／`Quot.sound`または公理依存なし |
| sorryAx | **なし** |
| 変更Lean warning/error | **0 / 0** |
| 検証source HEAD | `1cb34c5524d956b06a06bc16ea266997cb94292e` |
| test-merge HEAD | `251fd8558c57dc26b89c97688681fc232f4a2daf` |
| source/test-merge Git tree | **`bfa6690da3775a293f2e820293073f9564fd19fd` 完全一致** |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・公開root | `KuuOSFormal` / **107維持** |
| 保護PR #1558 | Draft／OPEN／未マージ（維持） |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77UnitDiamondMinimalHigherCompletionV5_01.lean) ・
[前段Qi v5.00正式記録](Qi-v5_00-original-P77-unit-diamond-four-torsion-obstruction.md)

## 1. 前段で確定した障害と最小介入

Qi v5.00では、**同じraw六セル始終点**をもつ、元の七セル自由構文の真正履歴

```lean
sevenUnitDiamondLeft w  = SevenRewrite.leftUnit  (PentagonAdjoinedSixCell.refl w)
sevenUnitDiamondRight w = SevenRewrite.rightUnit (PentagonAdjoinedSixCell.refl w)
```

について、第四整数Rの残余偶奇がともに0であるにもかかわらず、
四剰余Sが0と2に分離することを、全旧`IdentityEightCell`比較構成子の
法4保存定理から証明した。

```lean
¬ Nonempty (IdentityEightCell W long short
  (sevenUnitDiamondLeft w) (sevenUnitDiamondRight w))
```

よって「まだ見つかっていない」のでなく、**旧presentationでは不存在**である。
本段階ではその真正な障害に限り、必要最小の一つの新比較を加える。

## 2. 独立八セルpresentationの最小構成

新しい`UnitDiamondEightCell`は、元`IdentityEightCell`を一切改変せず、
次の生成元と構造的閉包だけから構成する。

- `previous`：既存`IdentityEightCell` Type値証拠を型付きで包含
- `unitDiamond w`：今回の**唯一の新原始八セル生成元**
- `reverse`、`chain`：対称・推移の比較
- `whiskerLeft`、`whiskerRight`：七セル縦文脈への貼り合わせ
- `inverseContext`、`compositeContext`：型付き六セル逆・横合成文脈

`unitDiamondEightCell_refl`は旧最初期の`EightCell.reflexive`を
段階的な`previous`により保守的に持ち上げる。
旧source Type、七セル構文と旧高次商を同一視・置換しない。
`unitDiamondEightCell_noPreviousInterpreter`により全新八セルを旧八セルへ
解釈する普遍写像は存在しない。`unitDiamondEightCell_noStrictInterpreter`により、
新八セルの存在から元の自由七セル生構文の厳密なEqは導けない。

## 3. 商の厳密な粗化と降下境界

新しい商は

```lean
unitDiamondHistorySetoid
unitDiamondHistoryClass
unitDiamondHistoryClass_eq_iff
```

で構成し、旧商のclass一致は新商のclass一致へ一方向に降下する。

[
[H_L]_{mathrm{unit}}=[H_R]_{mathrm{unit}},
qquad
[H_L]_{mathrm{identity}}
e[H_R]_{mathrm{identity}}.
]

両者の区別はv5.00のS=0対2によって保証される。
これが新商が旧商より**真に粗い**ことの具体的証明であり、
`unitDiamondHistoryClass_noPreviousReturn`も証明した。

一方、今回追加した`unitDiamond w`で四剰余Sは変化するので、

[
oxed{
S(H_L)=0,quad S(H_R)=2,quad
S 	ext{は新商へ降下しない}.
}
]

新しい比較はv4.99の第四整数Rの偶奇を変えない。
全`UnitDiamondEightCell`構成子の帰納法から

[
oxed{
ar R(H_L)=ar R(H_R),qquad
ar R 	ext{は新商へ降下する}.
}
]

さらに`Quotient.lift`で新商上のBool値観測量
`unitDiamondHistoryParity`を構成した。

**重要：** この結果は選択した独立八セルpresentationに対する
必要条件と具体的な局所補完を与えるだけで、偶奇一致による
**任意の平行履歴の比較存在**を主張しない。

## 4. 新生成元と旧規則の混合critical pair

今回は次の3種類の実際の型付き七セル平行履歴を作った。

1. `unitDiamond × identityDouble`（第四整数R=0対2の旧比較と横合成）
2. `unitDiamond × 左inverseComp／単位則`
3. `unitDiamond × 左doubleInverse／逆元消去`

各pairは**旧`IdentityEightCell`で比較不能**である。
最初と第三のpairは旧Sが2対0、第二のpairは0対2であり、
旧全構成子保存定理と矛盾する。

他方、新しい`UnitDiamondEightCell`では
`compositeContext`と、唯一の新`unitDiamond`および既存の
`identityDouble`／`leftOverlap`証拠だけで比較が構成できる。
さらに、その比較がRの偶奇を保存することを示した。

`UnitDiamondCriticalPeak`は旧v4.98／v4.99の選択critical family、
今回の3種類、新`unitDiamond`と型付き文脈閉包を含む**限定族**である。
`unitDiamondCriticalPeak_fill`は**この限定族の全構成子**について
真正Type値合流証拠を構造帰納法により構成し、
`unitDiamondCriticalPeak_classEq`で新商のclass一致まで降下する。

## 5. 元P77 raw最終添字・GK5CG sourceへの輸送

真正`pentagonAdjoinedSixCell_generator`を同じ左文脈へ貼る
`unitDiamondComposite_fill c`を構成した。
`pentagonActualUnitDiamondCompletionWithSourceObstruction`は
**任意の元P77 raw最終添字**に対し、次を同時に保証する。

1. 元GK5CGの真正Type値sourceを持つ、新`UnitDiamondEightCell`の比較証拠が存在する。
2. 同じ七セル二端点に対する旧`IdentityEightCell`は存在しない。
3. 元sourceの`PentagonAdjoinedSixCellEqualityInterpreter`は存在しない。

これにより、sourceのstrict空、独立Kuuのpresentationと
型付き証拠履歴のauthority境界は保存される。
**元source strict Eqと高次商Eqは同一視しない。**

## 6. CIエラー全文点検と構文修正

初回PR HEAD `1d1c8a74496e90648c4553820ee5afa3d11947cb`の
exact-source CIは、新規Leanファイルの

- `unitDiamondEightCell_strictlyNew`：型宣言の閉じ括弧が一つ不足
- `mixedUnitIdentityDouble_newVsOld`：裸の`w : W`からは
  `long`・`short`の暗黙パラメータを一意に復元できない

という2つの独立した構文／elaboration問題で失敗した。
後続の`Unknown constant`と`sorryAx`はその型付け失敗から連鎖した診断だった。

修正版では型宣言の括弧を閉じ、
`(long := long) (short := short)`を明示した。
新Lean全文・全imports・旧`IdentityEightCell`と
`SevenRewrite`の全型付き構成子・固定mathlibを照合し、
修正版HEAD `1cb34c5524d956b06a06bc16ea266997cb94292e`で
Strict Lean **10,300/10,300 SUCCESS**、
宣言公理監査 **45件・標準公理のみ**、
`sorryAx`なし、変更warning/error 0/0を検証した。

## 7. 未証明事項を保持

- 全ての平行七セル履歴の比較可能性
- 法2偶奇の一致から新八セル比較が必ず存在すること
- 高次障害の完全分類、九セルの大域thin性
- 原始八セル比較の追加以外の新関係によるcomplete rewriting
- 元F55/P77/GK5CG strict Eqと新高次商Eqの同一視

## 8. 次段階 Qi v5.02

局所補完後にも残る**法2では区別不能な平行七セルのobstruction**
を探索する。まず既存の全型付き比較構成子に基づく合流を確かめ、
条件を弱めず、具体的な新不変量と新比較不能性の証明が得られたときに
限り、別の独立presentationへの最小追加を検討する。

append-only／tighten-only／overwrite-forbidden／same-root。
公開root107、保護PR #1558 Draft/open/unmergedを維持。
