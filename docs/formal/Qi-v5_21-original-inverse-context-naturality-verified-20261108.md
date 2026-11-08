# Qi v5.21 — 真正inverseContextの第八〜第十二セル自然性とwhiskering履歴障害

## 0. 唯一の正本とexact-source検証

2026年11月8日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical `main`。
Qi v5.20の定理#3292／正式記録#3293をともにMERGEDの
`92b80e84ad234020f90b8e95b96f11c4cd6f957c`から継承した。
元F55/P77/GK5CGと独立6D〜12Dのすべてのraw Type値・証拠履歴は無変更。
新規Lean単独モジュールと公開集約import一行だけを追加した。

| 項目 | exact-source独立再観測 |
|---|---|
| 定理PR | [#3294](https://github.com/itakura-hidetoshi/KuuOS/pull/3294) MERGED |
| source HEAD | `7bab61b4ab0b0600029c0cd785a66b2fc6ee061c` |
| test-merge HEAD | `e48732536aa6c967553198e5e6e1bdaa12d4ba88` |
| squash/main | `eb2593774a609798243b0a7bb588a47ec834e11a` |
| source/test-merge/squash Git tree | **`5bfe455f006da318befafc5e12248eebc339c0ec` 完全一致** |
| exact-source CI | [#42431492263](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42431492263) SUCCESS |
| Strict Lean | **10,334 / 10,334 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| `#print axioms` | **17 / 17**、公理不要11、標準公理のみ6 |
| 標準公理 | 非無公理宣言は`propext`、必要な箇所のみ`Quot.sound` |
| 新規非標準公理、`sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0**（`warningAsError`、`sorryAsError`） |
| 改変範囲 | 新規Lean306追加行、`formal/KuuOSFormal.lean`にimport1行、削除0 |
| 既存公開root | 107維持 |
| 固定環境 | Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft／OPEN／未マージ維持 |

[形式証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77InverseContextNaturalityV5_21.lean)。

## 1. 真正inverseContextは別fiberへの型付き作用

v5.20の`TraceFaithfulHigherTower`は**固定された元の六セル添字**
`c,d`に対し、元第八セルcompatibleに追加して全上位証拠Typeへの
依存関数と第十セル順序履歴保存を要求する。

Qi v5.21では、新たに元の`FramedEleven`に直接作用する

`inverseContextTransportFrame : FramedEleven W l r → FramedEleven W l r`

を構成。内部では実際に既存の元構成子を使用する。

| 次元 | 入力 → 出力 |
|---|---|
| 六セル | `c : w→z` → `SixCell.symm c : z→w` |
| 七セル | `s` → `SevenRewrite.congrInv s` |
| 八セル | `q` → `PentagonAssocEightCell.inverseContext q` |
| 九セル | `alpha` → `MixedCancelNineCell.inverseContext alpha` |
| 十セル | `xi` → `MixedUnitAssocTenCell.inverseContext xi` |
| 十一セル | `H` → `MixedExchangeUnitElevenCell.inverseContext H` |
| 十二セル | `T` → `MixedExchangeInverseTwelveCell.inverseContext T` |

すべて原型のType値のまま構成・添字付けされ、
偽の元六セル等号、`EightCell(s, congrInv s)`、
商の強制的復元のいずれも仮定しない。
`inverseContextTransportFrame_onRaw`は旧十一セル値を再パックした結果を、
本物の元十一セルinverseContextと**定義上の等号**で結ぶ。

## 2. 履歴保存と逆文脈の二段反復

元第十セルの完全ordered witness traceについて

\[
\boxed{
\mathrm{Trace}_{10}(\mathrm{inverseContext}(\xi))
 =\mathrm{Trace}_{10}(\xi)
}
\]

を証明した（`inverseContextTransportFrame_preservesTrace`）。
二回適用した場合の履歴保存も
`inverseContextTransportFrame_twice_preservesTrace`で証明。

ただし、自由六セルにおける`symm (symm c)`を
`c`と**生の厳密な等号で同一視していない**。
反転操作の意味と、元raw構文の強制的簡約は別である。

## 3. 旧第十二セル証拠の自然性と比較の降下

`inverseContextOldTwelfth`は実在する旧
`MixedExchangeInverseTwelveCell H K`の証拠値を
既存原始`inverseContext T`で輸送し、新しい下位fiberで
`FramedInheritedTwelfth`を構成する。

`inverseContextInheritedTwelfth`は、
その`strict / previous / reverse / chain`の
**全4構成子**に関する帰納法で閉じる。よって旧比較の存在は
inverseContextで保たれ、`inverseContextInheritedTwelfth_toFull`により
元v5.18 framed第十二セルへ**追加の商同一視なしに**埋め込まれる。

これは旧比較のみの自然性である。v5.18で追加した
`doubleWhisker`原始の全体に対する任意context自然性を
新しい公理として仮定したり、一般的に証明したりはしていない。

## 4. 生の非恒等性と固定fiber towerのauthority障害

`originalReflexiveElevenFrame`は任意の元値`w : W`について、
元の六セル`refl w`、七セル`refl`、
真正の八・九・十・十一セル反射の**既存原始だけ**から作られる
実際にinhabitedな型付き証拠値である。

入力と輸送後は、元六セルのsourceの最外コンストラクタが

\[
\boxed{
\mathrm{refl}(w)\quad\text{対}\quad
\mathrm{symm}(\mathrm{refl}(w))
}
\]

と異なる。この差を`frameSourceSixInverseTag`で
依存型を壊さず観測し、次を証明：

- `inverseContextFrame_nonidentityAtRefl`：任意の元反射六セル添字上の実十一セル証拠について、raw framed packetは厳密に異なる。
- `originalReflexive_inverseContext_nonidentity`：**実在する具体的反射十一セル**で、非同一性と旧第十セル順序履歴の同一性を同時に証明。
- `inverseContextFrame_notFixedSixTower`：v5.20の**固定六セル添字**を保つ任意towerからは、この逆contextの生packetを出力できない。

この不可能性は歴史の長さだけでなく**元六セルsource添字**に由来する。
新しいcontextの輸送は実在するが、既存の固定fiber塔に
無条件に取り込めるものではない。

## 5. 左右whiskeringとの厳密な対照

`originalLeftWhisker_tracePrefix`、
`originalRightWhisker_tracePrefix`が元の十セルコンストラクタについて

\[
\begin{aligned}
\operatorname{Trace}_{10}(\operatorname{whiskerLeft}(\xi))
  &=\mathrm{false}::\operatorname{Trace}_{10}(\xi),\\
\operatorname{Trace}_{10}(\operatorname{whiskerRight}(\xi))
  &=\mathrm{true}::\operatorname{Trace}_{10}(\xi).
\end{aligned}
\]

を**定義上の等号**で証明。
有限リストの長さの差より、いずれも元の順序履歴には
等しくならない（`originalLeftWhisker_traceObstruction`／
`originalRightWhisker_traceObstruction`）。
これは商や任意補助traceを使った仮定ではなく、
元コンストラクタの真正構文に対する結論である。

従って`inverseContext`は履歴を保つ**非恒等境界作用**、
左右whiskeringは履歴に新しい構造を追加する**非保存文脈作用**
として区別される。

## 6. authority・研究frontier

元source／witnessを別のpresentationへ移すことと、
その元sourceのstrict Eqを証明すること、
異なる文脈間の新しい高次interchangerを存在証明することは
別の数学的義務である。

今後のQi v5.22では、真正の両側whiskeringを伴う
新しい**trace-defect付きtransport**の条件付き合成と、
元第十二セルを保つ独立naturalityの可能性を検討する。
第八セルの比較証拠を元のraw source Eqに昇格させず、
選択商・source authority・残存obstructionを独立に扱う。

append-only／tighten-only／overwrite-forbidden／same-root。
元F55/P77/GK5CG、全6D〜12D witness、独立KuuOSStrict、root107、
Lean/mathlib pin、#1558の保護を維持。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
