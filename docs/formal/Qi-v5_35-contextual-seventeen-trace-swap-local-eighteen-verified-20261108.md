# Qi v5.35 — 選択17D真正文脈閉包・隣接交換の構成的証明書・局所選択18D比較

2026年11月8日 JST。Canonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
v5.34の定理 #3330、公開import #3331、正式記録 #3332 のMERGED正本を継承した。
元F55/P77/GK5CG、元6D〜14D生証拠Type値と、旧v5.23〜v5.34の各選択presentationを変更せず、新たな独立presentationを追加する。
運用原則：append-only／tighten-only／overwrite-forbidden／same-root。

## 1. 唯一の正本とexact-source CI

| 項目 | GitHub MCP・独立CI成果物で確認済み |
|---|---|
| 定理PR | [#3333](https://github.com/itakura-hidetoshi/KuuOS/pull/3333) **MERGED** |
| 定理source HEAD | `65e7c8a7565fce860e826357e6e0d15a2f5af0a0` |
| 定理test-merge | `093d5b53b879ddf2af56cf2a477670e93886d530` |
| 定理squash main | `e7fb555b8e6a8af8f116d57d96907a1c129445b9` |
| 定理source/test-merge/squash Git tree | **`9ea40dd4e8056e47e174bcbd3b8844fe20b6193d` 完全一致** |
| 定理exact-source CI | [#42458954011](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42458954011) **completed/SUCCESS** |
| Scoped Strict Lean | **9,087 / 9,087 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 新規宣言公理依存監査 | **31 / 31**：25件公理不要・6件標準公理のみ |
| 使用標準公理 | `propext`、`Quot.sound`のみ |
| `sorryAx`／新公理 | **なし／なし** |
| 変更Lean error／warning | **0／0** |
| 定理差分 | 新規Lean1ファイル、714行追加・削除0 |
| 公開集約PR | [#3334](https://github.com/itakura-hidetoshi/KuuOS/pull/3334) **MERGED** |
| 公開import source HEAD | `5c20057a052f50ac5db94bb48354737d3b764450` |
| 公開import test-merge | `5dd60d2c5f5ecc5878e45d3acdbfba105dc04443` |
| 公開import squash main | `7a1c3fd97bcbe6b6e95df20b3df0dc516c814718` |
| 公開import source/test-merge/squash Git tree | **`fefbfac9e4188317bba65f826ba38914dac54604` 完全一致** |
| 公開集約exact-source CI | [#42459369945](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42459369945) **completed/SUCCESS** |
| KuuOSFormal全体Strict Lean | **10,348 / 10,348 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開差分 | `formal/KuuOSFormal.lean`にimport1行追加、削除0 |
| 公開root／保護PR | root107維持／#1558 Draft・OPEN・未マージ |
| 固定Lean・mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Lean4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ContextualSeventeenTraceSwapV5_35.lean)。

定理CIの`lean-formal/receipt.json`は`status=passed`、`return_code=0`、
`git_sha=093d5b53b879ddf2af56cf2a477670e93886d530`を記録。
固定LeanとsorryAsError／warningAsErrorで実行した
`build KUOS.Architecture.QiWuxingGK5CHP77ContextualSeventeenTraceSwapV5_35`のログ末尾は
`Build completed successfully (9087 jobs)`。
31件の`#print axioms`を独立集計して25件公理不要・6件標準公理のみ。
`sorryAx`なし、変更Lean error／warning 0/0。
公開集約receiptも`status=passed`・`return_code=0`、
`git_sha=5dd60d2c5f5ecc5878e45d3acdbfba105dc04443`。
`build KuuOSFormal`のログは`Build completed successfully (10348 jobs)`。
9,087と10,348は独立の検証範囲である。

## 2. 選択17Dの独立真正文脈閉包と元証拠の単射保持

v5.33の元選択17D生証拠`SelectedLocalSeventeen W l r H K`を、
独立の`SelectedContextualSeventeen W l r H K`へ`inherited`でそのまま埋め込む。
`oldSeventeenToContextual_injective`は、この生の型付き証拠の埋込みが単射であることを証明した。

新規`whiskerLeft`・`whiskerRight`は、元の真正`SevenRewrite`と
`ContextFrameEleven`の六セル境界が適合するときだけ17D比較を16D始点・終点ともに輸送する。
`strict/reverse/chain`と併せ6種類の構成子を備え、
`selectedContextualSeventeen_leftStable/rightStable`により真正文脈下での局所安定性を証明。
旧17Dのraw Eqを導く新公理や構成子は追加しない。

`selectedContextualSeventeen_preservesSixteenTrace`は6構成子の帰納で
16D生証拠の**外側第七セルの順序付き`List Bool`履歴**を比較前後で保存する。
`selectedContextSeventeenSetoid`は、同一の真正15D端点を持つ平行16D生証拠について
選択17D比較の存在を同値関係として商を構成した。
`selectedContextSeventeenClass_eq_iff`は、商クラスEqと実際の17D比較の存在が同値と示す。
`selectedContextSeventeenTraceOnQuotient`は全順序履歴の真正`Quotient.lift`を与える。

一方、旧v5.33の真正17D局所単位比較では、raw16Dの単位前置・後置の先頭タグ3と0が異なるが商クラスは等しい。
`selectedContextSeventeen_noFirstTagDescent`で、生16D先頭タグを再現する商上写像の不存在を証明。
**文脈順序履歴は降下する／raw構成子タグは降下しない**。

## 3. 従来の不可能条件を保持したまま隣接交換を構成

v5.34で`SelectedMixedTraceRespectingHigherGate`の不成立が形式証明済み：

\[
\mathrm{Trace}(L(R(H)))\ne\mathrm{Trace}(R(L(H))).
\]

これは順序を**変更しない**高次gluing条件の障害である。
v5.35では新しい`SelectedOuterAdjacentSwap`を、共通観測先`List Bool`における
有限な隣接交換の証拠Typeとして構成した：

\[
[\mathrm{false},\mathrm{true}]\mathbin{+\!+}h
\quad\Rrightarrow{\mathrm{swap}}\quad
[\mathrm{true},\mathrm{false}]\mathbin{+\!+}h.
\]

`selectedMixedOuterAdjacentSwap`は真正元第七セルによるv5.33の二種16D文脈輸送から、
**実際の履歴観測に対してこの証拠を構成**する。
`selectedAdjacentSwap_changesTrace`は両観測が異なることを、
`selectedAdjacentSwap_preservesCounts`は左右の出現回数は同じことを証明する。

`SelectedMixedTraceChangingCertificate`は次の完全な局所資料を保持する：
元v5.18 double-whiskerに由来する12D始点・終点の真正橋、
v5.30の選択13D左右混合interchangerと選択14D自然性squareを含む
**元v5.33の真正`SelectedMixedLowerHigherPacket`**、
さらに上記の有限隣接swap Type値、左右出現回数の等号証明。

`selectedMixedTraceChangingCertificate`はこのパケットを旧証拠から構成し、
`selectedMixedTraceChange_possible_strictTraceImpossible`は**同じ文脈・元添字条件で**

\[
\boxed{
\operatorname{Nonempty}(\mathrm{TraceChangingCertificate})
\quad\land\quad
\neg\operatorname{Nonempty}(\mathrm{TraceRespectingHigherGate})
}
\]

を証明した。

これは「観測の隣接交換が可能」「観測を変えないgluingは不可能」の両立である。
隣接交換は**共通観測値でのType値証拠**であって、異なる依存15D/16Dの
raw証拠Eqでも、すべての高次交換を実現する18Dセルでもない。
trace変更型のより高次な元証拠輸送には、別の明示的な互換証拠が必要である。

## 4. 厳密な同一端点での局所選択18D

元v5.33の真正選択17D局所`unitLeft/unitRight`を独立の17D閉包へ含め、
その比較の前後それぞれに17D`strict`を貼り合わせた左右2系列の生17D経路を構成した。

`selectedSeventeenUnitPrependLeft/AppendLeft`と
`selectedSeventeenUnitPrependRight/AppendRight`は、
それぞれ完全に同じ16D始終点を持ち、先頭構成子観測は3／0。
`selectedSeventeenUnitLeft_rawDistinct/right_rawDistinct`は生17D値の非等号を証明する。

新しい独立`SelectedLocalEighteen`はこの**2系列だけ**を
`unitLeft/unitRight`という局所18D比較生成元として追加し、
`strict/reverse/chain`で閉包する。
`selectedLocalEighteen_leftWitness/rightWitness`は
選択18D比較の存在と生17D値の非等号を同時に証明。
`selectedLocalEighteen_noRawEqualityInterpreter`は、
選択18D比較を生17D Eqへ読み替える普遍解釈を否定する。

無条件の左右二重文脈18D交換、他の依存fiberへの全面的extension、
元証拠のstrictification、全体coherenceは証明していない。

## 5. 次の研究：Qi v5.36

1. 構成的な隣接交換`SelectedOuterAdjacentSwap`を、異なる依存15D/16D境界の
真正上位transportへ昇格させるために必要な**境界一致・上位比較の明示的証拠**を評価する。
2. 独立選択18Dからの17D商と、外側順序履歴の保存・非保存を形式証明する。
3. 順序を保つ降下・入れ替えを許す互換・阻害されるgluingのauthority境界を維持する。

append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
