# Qi v5.34 — 選択17D商における16D順序履歴の降下と条件付き上位gluing障害

2026年11月8日 JST。Canonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
v5.33の定理 #3327・公開集約 #3328・正式記録 #3329 がMERGEDである正本を継承した。
元F55/P77/GK5CG、元6D〜14DのType値証拠、旧12D〜17Dの独立選択presentationを一切変更せず、
新しいLean4モジュールを追加した。append-only／tighten-only／overwrite-forbidden／same-root。

## 1. 正本・exact-source検証

| 項目 | GitHub MCPと独立CI成果物で確認済み |
|---|---|
| 定理PR | [#3330](https://github.com/itakura-hidetoshi/KuuOS/pull/3330) **MERGED** |
| source HEAD | `4ebdb5078d5c073b9d0a54bf58a58e3c76bca93f` |
| test-merge | `ca51a4bcc449481b71ecb2f410dccb8bbbe8047d` |
| theorem squash main | `12d8dc2bf608e5322bcbb0f26d5a5942f8edf6e7` |
| 上記source/test-merge/squash Git tree | **`749e66b02d2551d8cc7ea5795b6eea06a7878a2c` 完全一致** |
| 定理exact-source CI | [#42457030162](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42457030162) **completed/SUCCESS** |
| Scoped Strict Lean | **9,086 / 9,086 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 新規宣言の公理依存監査 | **21 / 21**：15件公理不要・6件標準公理のみ |
| 使用する標準公理 | `propext`、`Quot.sound`のみ |
| `sorryAx`／新公理 | **なし／なし** |
| 新規Lean error／warning | **0／0** |
| 定理変更 | 新規Lean1ファイル、482行追加、削除0 |
| 公開集約PR | [#3331](https://github.com/itakura-hidetoshi/KuuOS/pull/3331) **MERGED** |
| 公開集約source HEAD | `696832948227d46c3d9e4a5ef6b8e0efb23da8a5` |
| 公開集約test-merge | `ba0e87474b5817ff968c3dfdecfdf9fe3ec0a290` |
| 公開集約squash main | `ba98656ca1e8c2f88f8ab4408e11890c8d22e579` |
| 公開集約source/test-merge/squash Git tree | **`340c990135cad27285233b7839d27943a7ac4bea` 完全一致** |
| 公開集約exact-source CI | [#42457437150](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42457437150) **completed/SUCCESS** |
| KuuOSFormal全体Strict Lean | **10,347 / 10,347 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開集約差分 | `formal/KuuOSFormal.lean`へのimport 1行のみ追加・削除0 |
| 公開root・保護PR | root107維持、#1558 Draft／OPEN／未マージ |
| 固定Lean・mathlib | `v4.30.0-rc2`・`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Lean4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77SeventeenQuotientTraceGateV5_34.lean)。

定理CIの`lean-formal/receipt.json`は`status=passed`、`return_code=0`、
`git_sha=ca51a4bcc449481b71ecb2f410dccb8bbbe8047d`を記録。
`lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77SeventeenQuotientTraceGateV5_34`
の実ログ末尾は`Build completed successfully (9086 jobs)`。
新規21件の`#print axioms`結果をログから独立集計し、15件公理不要・6件は標準公理のみ・`sorryAx`なし。
公開集約のreceiptも`status=passed`、`return_code=0`、
`git_sha=ba0e87474b5817ff968c3dfdecfdf9fe3ec0a290`で
`lake ... build KuuOSFormal`が`Build completed successfully (10347 jobs)`。
Scoped 9,086と公開10,347は検証範囲が異なり、混同しない。

## 2. 選択17Dによる16D Type値証拠の商

v5.33の本物の選択17D証拠`SelectedLocalSeventeen W l r H K`を、
同じ真正15D始終点を持つ**平行な生16D証拠**`H,K`間で扱う。
`selectedSeventeenSetoid`は

```text
H ~17 K  iff  Nonempty (SelectedLocalSeventeen W l r H K)
```

を反射・対称・推移的な同値関係として構成。
`selectedSeventeenClass_eq_iff`は、
**商クラスの等号と型付き17D比較の存在の同値**を形式証明する。

旧証拠の生Eqや証明履歴の自動消去ではなく、新しい選択商の定義である。
`selectedSeventeenQuotientLift`は任意の観測`obs : Raw16D → A`が
**指定された全17D比較の前後で同値を保つ**場合に限り、
商への`Quotient.lift`を構成し、`selectedSeventeenQuotientLift_onClass`で
元観測値との可換性を証明した。

## 3. 降下できる順序履歴と、降下できない構成子タグ

`selectedSeventeen_preservesSixteenTrace`は17D構文の全5種
`strict/unitLeft/unitRight/reverse/chain`について、
v5.33の`selectedContextSixteenTrace`が選択17D比較を保存すると帰納的に証明した。
したがって`selectedSeventeenTraceOnQuotient`は
**外側第七セルの順序付き`List Bool`履歴を完全に保持する商上観測**であり、
`selectedSeventeenTrace_onClass`が元値との一致を証明する。
左右作用の個数`selectedFifteenTraceCounts`も
`selectedSeventeenCountsOnQuotient`として合成によって降下できる。
さらに、同一の厳密な15D fiber内では、
順序履歴の異なる生16D証拠の商クラスも異なると証明。

しかし、v5.33の真正局所17D`unitLeft`は
生16Dの単位前置`selectedSixteenUnitPrependLeft`（タグ3）と
単位後置`selectedSixteenUnitAppendLeft`（タグ0）を比較する。
両者は**生16D値として非等号**でも、`selectedSeventeenLeftUnit_classEq`によって
新17D商上は等しい。
`selectedSeventeenLeftUnit_projectionNotInjective`は商への射影が単射でないこと、
`selectedSeventeen_noFirstTagDescent`は
元の16D先頭構成子タグをそのまま再現する商上写像が存在しないことを形式証明した。
右側の局所生成元についても商クラス等号を構成済み。

「17D商で同一」「生16Dでは異なる」「順序履歴は保存される」
「生の構成子タグは保存されない」を分離している。

## 4. 異なる依存fiberの左右二重輸送

v5.33で実装された真正左右文脈の二重輸送

```text
L(R(H))  versus  R(L(H))
```

は、一般には**異なる生15D境界を添字に持つ別々の16D Type値**。
両者の生Eqを立てたり、共通のquotient Typeへ無理に写したりしない。

代わりに、それぞれの正しい依存fiberで生成した選択17D商クラスを、
共通の`List Bool`観測先へ送る。
`selectedSeventeenMixedOrder_traceObstruction`はその値が
`[false,true]++trace(H)`と`[true,false]++trace(H)`で異なることを証明。
`selectedSeventeenMixedOrder_countAgreement`は、
粗い左右出現回数が同じであることを証明する。
異なる商Typeの元自身をEq比較する主張ではない。

## 5. 高次gluingの必要な互換条件とobstruction

`SelectedMixedTraceRespectingHigherGate`は**限定した必要条件型**として、
(1) v5.33で既証明の真正下位12D境界・選択13D/14D比較を全て保持した
`SelectedMixedLowerHigherPacket`と、
(2) 上位16Dの左右二重輸送に関して**順序付き外側文脈traceが一致する**
という明示的な追加条件を同時に要求する。

`selectedMixedTraceRespectingHigherGate_empty`は、
(2) が元v5.33の有限順序obstructionと両立しないことを証明。
さらに`selectedMixedLowerCompatible_butHigherTraceObstructed`は

```text
Nonempty(real lower 12D–14D packet)
AND
NOT Nonempty(trace-respecting higher gluing gate)
```

を同じ真正元第六・第七セル文脈について同時に証明する。

この**厳密に定義したtrace保存型gluing条件**は不成立。
しかし、traceを変更する新たな上位presentationや別の高次mediatorの
存在まで否定していない。下位compatibilityは必要な構成要素でも、
これだけで全上位自然性やgluingは成立しない。

`selectedSeventeen_noRawEqualityInterpreter`も、
選択17D比較の存在を生16D Eqに読み替える普遍解釈がないことを証明する。

## 6. authority境界とQi v5.35

今回確立されたのは、**選択17Dで生成された商**の数学的性質と、
**順序履歴を保存する特定の高次gluing条件のobstruction**。
元の証拠履歴、旧14D/15D/16D raw等号、
異なる依存fiber間の無条件交換、グローバルcoherence、
全presentationのstrictificationは主張していない。

次段Qi v5.35では、異なる15D依存境界を比較可能にするための
**具体的な高次transport packetと、traceが変化する場合の条件付き障害の扱い**を研究する。
同時に新しい選択17D商の文脈作用と、局所18D比較が必要になる条件を検討する。

append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
