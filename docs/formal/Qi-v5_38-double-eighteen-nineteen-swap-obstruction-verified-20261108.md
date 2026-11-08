# Qi v5.38 — 真正18D二重文脈輸送・選択19D商から観測swap商への降下・fine履歴保存輸送の障害

2026年11月8日 JST。Canonical repository: `itakura-hidetoshi/KuuOS`、branch: `main`。
前段Qi v5.37（定理 #3339、公開 #3340、正式記録 #3341）はすべてMERGED。v5.38では定理 #3342と公開 #3344まで検証・統合した。
元F55/P77/GK5CG、元6D〜14DのType値証拠、v5.23〜v5.37の独立selected presentationを上書きせず継承。
規律は **append-only／tighten-only／overwrite-forbidden／same-root**。

## 1. 唯一の正本とexact-source検証

| 項目 | GitHub MCP／exact-source CIで確認 |
|---|---|
| 定理PR | [#3342](https://github.com/itakura-hidetoshi/KuuOS/pull/3342) **MERGED** |
| 定理source HEAD | `d288d9259ab84c7807ba82c64f7796a1b1f3adf8` |
| 定理test-merge | `4f52f4dde4c36425ad9062b64b2e4a3b12eb2995` |
| 定理squash main | `0ef81341bde933e3de16bd3782719fd3792cdd40` |
| 定理source/test-merge/squash Git tree | **`48f7605ddeacac8668778cad8c4fb5318c559efa` 完全一致** |
| 定理exact-source CI | [#42469326230](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42469326230) **completed/SUCCESS** |
| Scoped Strict Lean | **9,090 / 9,090 SUCCESS** |
| 定理Governance | **5 / 5 SUCCESS** |
| 新規公理監査 | **16 / 16**、公理不要10件、標準公理のみ6件 |
| 新規sorryAx／追加公理 | **なし／なし** |
| 変更Lean error／warning | **0／0** |
| 新規定理差分 | Lean1ファイル、445行追加、削除0（既存名との衝突は新規ファイル内の3箇所を改名） |
| 公開集約PR | [#3344](https://github.com/itakura-hidetoshi/KuuOS/pull/3344) **MERGED** |
| 公開source HEAD | `028e19d1b9f02f5a0de827d6ba3b48990e416673` |
| 公開test-merge | `2ac02c03df46c772fad376963275c63378379ff8` |
| 公開squash main | `54ee7c3d2ffde6d0aecd827579b9df62e5f5a4f3` |
| 公開source/test-merge/squash Git tree | **`c202f6068c63f295d34c3e2bf151589dae55ad28` 完全一致** |
| 公開exact-source CI | [#42469855076](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42469855076) **completed/SUCCESS**、attempt 2 |
| KuuOSFormal全体Strict Lean | **10,351 / 10,351 SUCCESS** |
| 公開Governance | **30 / 30 SUCCESS** |
| 公開集約変更 | `formal/KuuOSFormal.lean`のimport1行のみ、削除0 |
| 公開root／保護PR | root107維持／#1558 Draft・OPEN・未マージ |
| 固定Lean／mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Lean4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77DoubleEighteenNineteenSwapV5_38.lean)。

定理CIは `lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77DoubleEighteenNineteenSwapV5_38` を実行し、ログに `Build completed successfully (9090 jobs)` を記録。
新規16件の`#print axioms`を独立照合した。10件は公理依存なし、残り6件の依存は`propext`／`Quot.sound`の標準公理に限る。
公開集約は独立に `Build completed successfully (10351 jobs)`。9,090と10,351は検証対象が異なり、混同しない。

## 2. 真正18D Type値証拠を保持した左右二重文脈輸送

`M : SelectedContextualEighteen W l r J N` を元の選択18DのType値証拠として保持する。
現行元`SevenRewrite`と`ContextFrameEleven`の厳密に一致した境界に限って、
`selectedEighteenLeftAfterRight` と `selectedEighteenRightAfterLeft` を真正型付きに構成する。

- `M_LR = whiskerLeft left ... (whiskerRight F G M right)`
- `M_RL = whiskerRight ... (whiskerLeft left F G M) right`

出力の17D始点・終点は一般に異なる依存fiberに属する。したがって比較は生raw Eqではなく、双方から共通`List Bool`へ送った観測値として行う。
`selectedEighteenMixedTraceValues`は次の**順序付き**履歴を証明する：

`Trace(M_LR) = false :: true :: Trace(M)`

`Trace(M_RL) = true :: false :: Trace(M)`

左右イベントの出現回数は等しいが、順序履歴自体は等しくない。

## 3. 各exact-fiber選択19D商から観測swap商への条件付き降下

v5.37の`selectedNineteenTraceOnQuotient`は、真正の選択19D証拠比較に関して完全順序付き18D履歴を`Quotient.lift`で降下させる。

これをv5.36の有限観測swap商と合成し、
`selectedNineteenSwapObservation`を**各17D fiberごとに別々に**定義する：

`[M]₁₉ ↦ [Trace(M)]_swap`。

`selectedNineteenSwapObservation_respectsNineteen`が実際の19D比較に対する互換性を証明する。
`selectedNineteenSwapCounts`は左右出現回数を別の商上観測へ降下させる。

`selectedDoubleEighteenNineteen_fineTraceDistinct`は左右二重輸送の**完全順序履歴が異なる**ことを証明。
一方、`selectedEighteenMixedOrder_swapClassEq`は観測swap商内でクラスが一致することを証明する。
`selectedEighteenMixedOrder_countsEq`は粗い左右計数も等しいことを、`selectedEighteenMixedOrder_prefixSwapClassEq`は任意の**共通有限prefix**を追加してもswap商互換が維持されることを示す。

異なる19D依存fiberの元証拠に、直接の比較セルや元のEqを導入したわけではない。

## 4. 完全fine履歴保存を要求する場合のno-go

`selectedEighteenMixedOrder_noFinePreservingTransport`は、左右の異なるexact-fiber19D商を結ぶ写像`f`について、

1. 全クラス`q`の完全順序履歴を保存する。
2. 指定した真正`[M_LR]₁₉`を`[M_RL]₁₉`へ送る。

という**二条件を同時に満たす写像は存在しない**と証明する。
これは証明済みの`false :: true :: h ≠ true :: false :: h`に帰着する。

この定理は**すべてのcross-fiber輸送を否定するわけではない**。完全履歴を変化させる輸送、または追加の型付き境界証拠を必要とする輸送については、別途構成と再検証が必要である。

## 5. 下位元証拠と高次障害を両立して保存

`SelectedMixedEighteenObservationPacket`には、既存の真正12D〜14D`SelectedMixedLowerHigherPacket`、両方の真正型付き18D文脈輸送、観測値の`SelectedOuterSwapClosure`、完全fine履歴の非等号、v5.34の`SelectedMixedTraceRespectingHigherGate`非空性否定を保持する。

`selectedMixedEighteenPacket_possible_strictGateImpossible`は、この正の観測レベルpacketの存在と、厳密順序履歴保存型高次gateの障害が同時に成立することを形式証明。

この新しいpacketは元のヘテロ型間19D交換セルではない。**観測互換性と証拠接合の権限を混同しない**。

## 6. HTTP 504障害の復旧経緯

- 旧Lean導入経路では定理CIのattempt 1〜6がElanまたはLean本体のダウンロードでHTTP 504となり、型検査前に停止した。これは数学的なエラーの証拠ではない。
- 独立したCI-only [PR #3343](https://github.com/itakura-hidetoshi/KuuOS/pull/3343)がMERGED。公式Lean v4.30.0-rc2配布物の既知のbyte sizeとSHA256を厳密照合するfail-closedな有限回リトライを導入。固定Lean/mathlibとすべての後続Scoped Strict Lean・Governance検査条件は変更していない。
- 新しいCIで定理 #3342は [#42469326230](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42469326230) SUCCESS。公開集約 #3344のCI [#42469855076](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42469855076)は初回の公式配布504後、**同じソースHEAD**で再実行してSUCCESS。
- 成功した受領書の範囲に限って定理と公開集約をmainへ統合した。旧failed CIを成功の根拠にしない。

## 7. authority境界・次段Qi v5.39

これまで得られたのは真正selected proof Typeの局所・文脈輸送と、独立観測商への`Quotient.lift`、正確な不可接合条件である。元のC60物理幾何の任意高次source同値、無制限cross-fiber19D/20D比較、全体Gray coherenceは主張しない。

次段Qi v5.39では、左右二重輸送の異なる17D依存端点を**型付きで比較するための境界証明書**を具体化し、必要なboundary transportと観測swap証明書の組合せを条件付きに接続する。元のType値履歴を保持し、条件が欠けるときは`NO_DATA`または明示的`obstruction`として残す。元raw Eqを前提に追加しない。

この文書はdocs-onlyであり、Lean定理・公開import・workflowを変更しない。
