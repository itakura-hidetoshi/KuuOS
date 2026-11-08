# Qi v5.31 — 選択第十五セルの真正文脈閉包・第十四セル商の条件付き降下・順序履歴obstruction

2026年11月8日 JST。canonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.30定理PR #3318、公開集約PR #3319、正式記録PR #3320のMERGED正本を継承。
元F55/P77/GK5CG、元6D〜14Dの生証拠Type値、選択v5.23〜v5.30の全証拠型を変更しない。
独立した新選択presentationの追加のみで実装した。

## 1. 唯一の正本とexact-source形式証明

| 項目 | GitHub MCPと検証成果物で確認した値 |
|---|---|
| 定理PR | [#3321](https://github.com/itakura-hidetoshi/KuuOS/pull/3321) **MERGED** |
| 定理source HEAD | `ed4feb4af9e121f807e93b8fa54cd0a4f8d2e87c` |
| 定理test-merge | `867bdfb107cedcf34b1ba82d590f8006ab096767` |
| 定理squash main | `0e7e17c940749ea177ec25e4d29cf3c374bc4981` |
| 上記source/test-merge/squash Git tree | **`b87b6f3bcec9ba31bdb54f95533f53566c2319b3` 完全一致** |
| 定理exact-source CI | [#42450986078](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42450986078) **completed/SUCCESS** |
| Scoped Strict Lean | **9,083 / 9,083 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 新規宣言の公理依存監査 | **21 / 21**：公理不要17件、標準公理のみ4件 |
| 標準公理 | `propext`、`Quot.sound`のみ |
| `sorryAx`／新公理 | **なし／なし** |
| 変更Lean error／warning | **0／0** |
| 定理差分 | 新規Lean1ファイル、492行追加・削除0 |
| 公開集約PR | [#3322](https://github.com/itakura-hidetoshi/KuuOS/pull/3322) **MERGED** |
| 公開集約source HEAD | `39971333e5ad06854d9d2367017dbf656596cc05` |
| 公開集約test-merge | `6c92f0311a44d1aa07bfde35500c8ebc9f74aa04` |
| 公開集約squash main | `a06ccf594123f21814e737f4a340fe129c081773` |
| 公開集約source/test-merge/squash tree | **`310094e1fecd7d2c1e7013647eab899daeeb4923` 完全一致** |
| 公開集約exact-source CI | [#42451246378](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42451246378) **completed/SUCCESS** |
| KuuOSFormal全体Strict Lean | **10,344 / 10,344 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開集約変更 | `formal/KuuOSFormal.lean` import1行追加、旧import削除0 |
| 公開root／保護PR | root107維持、#1558 Draft／OPEN／未マージ |
| Lean／mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[新規Lean 4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ContextualFifteenDescentV5_31.lean)。

定理exact-sourceの`lean-formal/receipt.json`は`status=passed`、
`return_code=0`、`git_sha=867bdfb107cedcf34b1ba82d590f8006ab096767`、
`lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77ContextualFifteenDescentV5_31`
を記録。ログ末尾は`Build completed successfully (9083 jobs)`。
公開集約のreceiptは`status=passed`、`return_code=0`、
`git_sha=6c92f0311a44d1aa07bfde35500c8ebc9f74aa04`、
`build KuuOSFormal`、`Build completed successfully (10344 jobs)`。
対象限定9,083と公開集約10,344は異なる検証範囲であり混同しない。

## 2. 元第十五セル証拠を保存する独立の文脈閉包

v5.30の真正選択15D証拠`SelectedMixedCoherenceFifteen W l r V X`を、
新しく独立に定義した`SelectedContextualFifteen W l r V X`へ
`inherited`でそのまま埋め込み、`oldFifteenToContextual_injective`で
**生証拠埋込みの単射性**を証明した。

新しい生成元`whiskerLeft`と`whiskerRight`は、
真正の元第七セル`SevenRewrite`および元第六セル境界に整合する
`ContextFrameEleven`を引数として要求する。
両方の第十四セル境界が正確に輸送される場合に限り、第十五セル比較が得られる。
`selectedFifteen_leftStable/rightStable`で存在を証明。
`strict/reverse/chain`の構文閉包と実際の15D往復証拠
`selectedFifteenUnitRoundtrip`を構成するが、戻り道がrawで単位証拠と
等しいという消去法則を追加していない。

## 3. 14D比較を保存する選択15Dによる商

同じ真正13D始終点を持つ並行14D証拠`V,X`上の関係を

\[
V\sim_{15}X
\quad\Longleftrightarrow\quad
\operatorname{Nonempty}
(\operatorname{SelectedContextualFifteen}(V,X))
\]

として`selectedContextFifteenSetoid`で構成した。
`strict/reverse/chain`から反射・対称・推移性を証明。
`selectedContextFifteenClass_eq_iff`は、商上の二つの14Dクラスが
等しいことと、型付きの選択15D比較が存在することを同値にする。

`selectedContextFifteenQuotientLift`は、14D生証拠の観測
`obs : Fourteen → A`が**すべての指定15D比較を保存する**場合に限り、
観測がこの商へ降下するための実際の`Quotient.lift`を構成する。
`selectedContextFifteenQuotientLift_onClass`で元の観測値との可換性を証明した。

## 4. raw第十四セル構成子タグの非降下という実際のobstruction

v5.30の真正局所15D単位比較

\[
\mathrm{criticalUnit}:
\mathrm{UnitPrepend}_{14}
\Rrightarrow_{15}
\mathrm{UnitAppend}_{14}
\]

を`selectedFifteenContextualUnit`として保存し、
`selectedContextFifteen_unitClassEq`で

\[
[\mathrm{UnitPrepend}_{14}]_{15}
=
[\mathrm{UnitAppend}_{14}]_{15}
\]

を証明した。

しかし旧v5.30の生14D先頭構成子観測
`selectedMixedFourteenFirstAtomTag`は、
前者を2、後者を1へ送る。したがって両者の商クラスが等しいまま
生観測タグを保つ写像は存在できない。
`selectedContextFifteen_noFirstTagDescent`はこれを明示的な否定存在定理として証明。

つまり「商上は同一」「生証拠は異なる」「その生観測は商に降下不能」が
同時に成立する。これはauthorityを越えた無条件のstrict化ではなく、
**局所生成された同値関係と情報損失の厳密な証明**である。

## 5. 真正左右文脈の多重輸送と順序履歴

任意の適合する真正元第七セル`left`、`right`、
元第六セル境界に整合する第十四セル証拠とその選択15D比較`T`から、
二つの本物の15D輸送を構成した：

\[
L_{\mathrm{left}}(R_{\mathrm{right}}(T)),
\qquad
R_{\mathrm{right}}(L_{\mathrm{left}}(T)).
\]

両者の14D端点は**一般には別の依存Type値**であり、
raw Eqを作るために無理な同一視をしていない。

新15D構文の`whiskerLeft`をfalse、`whiskerRight`をtrueとして
原子の順序を保持するraw観測`selectedContextFifteenTrace`を導入した。
`selectedFifteenMixedTraceValues`は

\[
\begin{aligned}
\mathrm{Trace}(L(R(T)))&=[\mathrm{false},\mathrm{true}]\mathbin{+\!+}\mathrm{Trace}(T),\\
\mathrm{Trace}(R(L(T)))&=[\mathrm{true},\mathrm{false}]\mathbin{+\!+}\mathrm{Trace}(T)
\end{aligned}
\]

を証明し、`selectedFifteenMixedTrace_obstruction`で両有限値の非等号、
`selectedFifteenMixedTrace_lengthEqual`で長さの一致を証明する。

これらは同一Type値のraw比較ではなく、**異なる文脈輸送から
得られる有限な履歴観測の比較**である。
第十五セルが存在すれば第十四セルの生証拠も等しい、という
普遍解釈が成立しないことは`selectedFifteen_noRawEqualityInterpreter`で再確認した。

## 6. 境界と次のQi v5.32

今回の定理は独立の選択15D文脈閉包と特定14D商の証明である。
元15D証拠のraw Eq、異なる依存14D境界間の自動的な交換16D比較、
任意多重文脈の全面的なcoherence、元の証拠Typeへの無条件descentは主張していない。

次のQi v5.32では、左右二重輸送の各14D境界を結ぶ
**実在する比較橋・十分なcompatibility条件**がある場合に限った
選択16Dの局所完成、traceを保存する観測量の候補、
商を越えて残る順序obstructionを検討する。

append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
