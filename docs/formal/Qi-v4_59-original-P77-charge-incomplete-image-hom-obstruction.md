# Qi v4.59 — 元P77のcharge不完全性と真正証拠付き像Homの到達障害

**2026-11-05 JST** — append-only、strict 空中心、独立Kuuは一presentation。

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#3139](https://github.com/itakura-hidetoshi/KuuOS/pull/3139) **MERGED** |
| 継承元 | Qi v4.58 [#3136](https://github.com/itakura-hidetoshi/KuuOS/pull/3136)・正式記録[#3138](https://github.com/itakura-hidetoshi/KuuOS/pull/3138) MERGED |
| 定理exact-source HEAD | `a9ec1f808c703ea138ca99b2d4382fbb18e84356` |
| 定理squash/main | `17d07420fb4c1c2a6f85b73d067ec355a34a72a7` |
| Git tree (source = test-merge) | `ca96ea96a50bbaa70c5338bf4b125837ff32ae3f` 完全一致 |
| exact-source CI | [#41973142130](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41973142130) |
| Strict Lean | **10,256 / 10,256 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **15件**、`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| 新規証明ソース | [Qi v4.59 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ChargeIncompleteImageObstructionV4_59.lean) + `formal/KuuOSFormal.lean` import 1行 |
| 固定環境 | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護条件 | public root107、#1558 Draft/open/unmerged、既存定理変更なし |

## 1. 三つの独立したauthority

1. 元Qi v4.53の5本の有向`FivefoldEdge`からなる真正の型付き自由経路圏 `FivefoldFreePathCategory`。
2. 元F55/P77四セルの商クラスに、元経路と元GK5CGのType-valued conservative five-cell到達証拠を付した`FivefoldP77ImagePoint`。Qi v4.58は真正`CategoryTheory.Equivalence`を確定した。
3. 元のすべてのP77保守的四セル商からなる`FivefoldP77ConservativePoint`。逆向きP77四セルを持つため、像の包含はFaithfulだがFullではない。

chargeは元GK5CG構造の数値観測であって、元の証拠クラスの定義や証拠復元関手ではない。元P94A、独立Kuu、C60物理Edge、数値CRTも同一視しない。

## 2. 像所属を決めるのは真正Source Type証拠

`fivefoldP77Image_lift_iff_reachable` と `fivefoldP77ImageInclusion_map_iff_reachable` は、元P77クラスが像Homにliftできることと、元有向有限経路の真正原像の存在を同値とする。

`fivefoldP77OriginalClass_unreachable_iff_noSourceFiveCell` は、任意の元P77四セル `w` について、像に属さないことと「**どの元型付き有限経路についても、その評価とwをつなぐ真正元GK5CG conservative five-cellのType値証拠が存在しない**」ことを厳密な必要十分条件とした。

## 3. chargeの検出範囲と単射性の限界

元5辺有向グラフの有限経路は長さ最大3である。よって到達可能な像クラス`z`には

\[
0\le Q(z)\le3.
\]

`fivefoldP77_reachable_charge_range` と `fivefoldP77_charge_out_of_range_not_reachable` がこれを与える。また`fivefoldP77_reachable_charge_injective`は、**始終点が同じ、かつ両方とも既に到達可能と証明された**元P77商クラスに限り、charge等号がクラス等号を導くことを証明する。像Category上では`fivefoldP77Image_charge_injective`となる。

この主張は元P77の全Homでchargeが単射であることも、`0\le Q\le3`だけで像所属を判定できることも意味しない。

## 4. chargeがゼロでも未到達の真正P77証拠

元P77の真正構成子`symm`と`trans`、既存の上／下五角形有限経路`U:0→3`（3辺）、`L:0→3`（2辺）を使う。

\[
z_0 := e_{01}^{-1}\circ U\circ L^{-1}:1\longrightarrow0,
\qquad Q(z_0)=-1+3-2=0.
\]

`fivefoldP77OriginalZeroChargeReverse01`は元F55/P77四セルを構成し、`fivefoldP77OriginalZeroChargeReverse01_charge`は商の真正charge 0を証明する。

元有向自由経路でcharge 0なら`length=0`、従って元の始終点は一致する。しかし`z_0`は真正`1→0`なので、そのような元経路は存在しない。`fivefoldP77OriginalZeroChargeReverse01_not_reachable`と`fivefoldP77Image_zeroCharge_missing`がこれを証明する。

この反例はv4.56の逆向き`e01^{-1}`（charge -1）とは**別の元P77商クラス**であり、`fivefoldP77OriginalZeroReverse_ne_negativeReverse`で証明した。よって`fivefoldP77_charge_range_not_sufficient_for_reachability`は、charge範囲条件だけでは未到達性を見逃すことを実際のType値証拠で示す。

## 5. 拡張presentationへの必要条件

`fivefoldP77FullExtension_requires_reverse_and_zeroCharge`は、将来の拡張源圏`S`から全元P77ターゲットへの関手がFullで、元位相1/0を対象として覆うなら、少なくとも**元逆向きe01クラス（charge -1）**と**その逆向き+五角形ループのクラス（charge 0）**の両方に真正Hom原像が必要であることを証明する。

これは必要条件であり、拡張presentation自体の構成、元P77全targetとの圏同値、新pentagonator、旧GK5CG保守的5-cellの書換えは一切主張しない。

## 6. Strict Lean・運用記録

初回のv4.57基点の試行[#3137](https://github.com/itakura-hidetoshi/KuuOS/pull/3137)では、新規Leanの等式書換え3箇所・ゼロcharge証明の書換え・Subtypeの依存型推論の計5箇所が失敗した。Leanログと新規Lean全文・v4.53〜v4.58の定義を照合し、既存`fivefoldP77ConservativeFunctor_charge_length`の**明示的calc等式連鎖**、`congrArg`、`Subtype.property`の直接運搬で修復した。数学的仮定や定理主張は弱めていない。

その後に別作業のQi v4.58 #3136/#3138 がmainへマージされたため、旧Draft #3137は履歴を残して未マージ・クローズ。最新main基点の新規Qi v4.59 #3139で固定Lean全体 **10,256/10,256** 成功、15件の公理依存は標準のみ。source/test-mergeは同一Git treeで、検証済みHEADを指定してsquashマージ済み。

## 7. 次の研究境界

**証明済み**：元5辺自由経路圏と証拠付き像圏はv4.58で真正圏同値であり、全元P77商ターゲットへの包含は非Full。Qi v4.59で、chargeは像上で識別子になっても像への所属を決める十分条件ではない、とType値の具体例で確定した。

**次の焦点**：像圏の準逆による型付き経路復元と`charge=length`の関手的自然性、充足可能な拡張presentationの生成元・関係の最小条件、構造5-cell obstructionを保持したdescent/gluing。元の四セル・五セル履歴を消去せず、strict 空を中心とする独立Kuu一presentationを維持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
