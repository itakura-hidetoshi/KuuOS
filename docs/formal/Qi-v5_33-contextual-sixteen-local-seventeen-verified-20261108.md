# Qi v5.33 — 真正12D〜選択14D混合証拠パケット、16D文脈閉包と局所選択17D比較

2026年11月8日 JST。唯一のcanonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.32（定理 #3324、公開集約 #3325、正式記録 #3326）までのMERGED正本を継承。
元F55/P77/GK5CG、元6D〜14D証拠、v5.32以前の選択presentationをすべて保存し、新しい独立presentationを追加する。

## 1. 唯一の正本とexact-source検証

| 項目 | GitHub MCP・CI原本で確定した結果 |
|---|---|
| 定理PR | [#3327](https://github.com/itakura-hidetoshi/KuuOS/pull/3327) **MERGED** |
| 定理source HEAD | `6cd923d575724ca8137aa32380659ef969080dff` |
| 定理test-merge | `1412303413c78c9f116d2b51f93644f1963a4443` |
| 定理squash main | `a236bc2e782c4b9f3ceff7b96edadafd34c8ac82` |
| 上記3コミットのGit tree | **`04daf15268537fb5c0033778c59535d1d0660754` 完全一致** |
| 定理exact-source CI | [#42454364715](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42454364715) **completed/SUCCESS** |
| Scoped Strict Lean | **9,085 / 9,085 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 新規宣言の公理依存監査 | **33 / 33**：29件公理不要、4件標準公理のみ |
| 使用した標準公理 | `propext`、`Quot.sound`のみ |
| `sorryAx`／新公理 | **なし／なし** |
| 新規Lean error／warning | **0／0** |
| 定理変更 | 新規Lean1ファイル、757行追加、削除0 |
| 公開集約PR | [#3328](https://github.com/itakura-hidetoshi/KuuOS/pull/3328) **MERGED** |
| 公開集約source HEAD | `dee9bbf224f048928ca0b6237e8c73bf9882dc89` |
| 公開集約test-merge | `ac877661d16707da9ef6aecd4c70f66a0c775361` |
| 公開集約squash main | `a2fe713c9efe5cdd4fe34b09db7000352a0f35f6` |
| 公開集約3コミットのGit tree | **`81f1ad3f987cf97bdf0ac73b4f63e249f5bd4b66` 完全一致** |
| 公開集約CI | [#42454714135](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42454714135) **completed/SUCCESS** |
| KuuOSFormal全体Strict Lean | **10,346 / 10,346 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開集約変更 | `formal/KuuOSFormal.lean`のimport1行追加、既存import削除0 |
| 固定Lean／mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root／保護PR | root107維持、#1558 Draft／OPEN／未マージ |

[Lean 4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ContextualSixteenSeventeenV5_33.lean)。

定理CI成果物`lean-formal/receipt.json`には`status=passed`、
`return_code=0`、`git_sha=1412303413c78c9f116d2b51f93644f1963a4443`、
`build KUOS.Architecture.QiWuxingGK5CHP77ContextualSixteenSeventeenV5_33`が記録され、
Leanログ末尾は`Build completed successfully (9085 jobs)`。
新規33宣言の`#print axioms`全文を照合し、29件公理不要、4件は標準`propext`/`Quot.sound`のみ。
公開集約receiptも`status=passed`、`return_code=0`、
`git_sha=ac877661d16707da9ef6aecd4c70f66a0c775361`、
`build KuuOSFormal`で`Build completed successfully (10346 jobs)`。
9,085と10,346は異なる検証対象であり混同しない。

## 2. 元の12D境界から選択14Dまでの真正パケット

`SelectedMixedLowerHigherPacket`は、元の六セル境界が厳密に整合する第七セル`left/right`、
第十一セル`F,G`、選択第十二セル`P,Q`、元v5.29の型付き第十三セル`C:P⇒Q`を保持する。
内容は次の**すべて実装済み**の証拠値から成る。

- 元v5.18の真正`doubleWhisker`を二段`previous`で保持した、始点・終点の**2本の選択12D境界橋**。
- 元v5.30の`SelectedMixedInterchangerThirteen.mixed`から、`P`と`Q`それぞれにおける**選択13D interchanger**。
- 元v5.30の`SelectedMixedNaturalityFourteen.criticalMixed`による、真正`C`に対する**選択14D局所自然性比較**。

`selectedMixedLowerHigherPacket`で構成、`selectedMixedLowerHigherPacket_witness`でパケットの存在と比較対象13D生経路の非等号を証明した。
このパケットは**下位の段階別互換性証明書**であり、v5.31の`L(R(T))`と`R(L(T))`に現れる異なる14D依存境界を強制的に同一視せず、一般の16D交換も導かない。

## 3. 旧16Dの単射保持と真正第七セルによる文脈閉包

新しい独立`SelectedContextualSixteen`は、v5.32の`SelectedLocalSixteen`の生証拠をすべて`inherited`として保存する。
`oldSixteenToContextual_injective`は元の16D生証拠埋込みの単射を証明する。
新しい`whiskerLeft/whiskerRight`は、元の`SevenRewrite`と正確な六セル始終点が整合する第十一セルpacketのもとでのみ、16D比較の**15D端点を双方とも**輸送する。
`strict/reverse/chain`も型付きで構成し、`selectedContextualSixteen_leftStable/rightStable`で左右独立の存在を確認した。
元の生15D・16D証拠Eqを仮定しない。

## 4. 文脈閉包16Dによる新しい15D商と選択的降下

`selectedContextualSixteen_preservesTrace`は新しい16D文法の**全6構成子**で、元v5.31の`selectedContextFifteenTrace`が比較の前後で同じ`List Bool`値をとることを帰納的に証明。
`selectedContextSixteenSetoid`は同じ真正14D端点の平行15D証拠を、型付き選択16D比較の存在によって商とする。
`selectedContextSixteenClass_eq_iff`は商クラス等号と16D比較存在を同値にする。
`selectedContextSixteenTraceOnQuotient`は元の**順序付き外側文脈履歴**をその商へ本物の`Quotient.lift`で降下させる。

一方、元v5.32の実在する局所16D単位証拠は、raw15D往復ループ（先頭構成子タグ0）とraw15D反射（タグ3）を比較するため、
新しい16D商における両クラスは同一でも、構成子タグを保つ商上関数は存在しない。
`selectedContextSixteen_noFirstTagDescent`がこの**非降下obstruction**を形式証明。
「証拠の商での同一性」と「raw証拠の等号」と「観測の降下可能性」を区別する。

## 5. 左右二重16D輸送の有限順序履歴

`selectedSixteenLeftAfterRight`および`selectedSixteenRightAfterLeft`は、
境界適合する真正第七セルの外側文脈で16D証拠を二つの異なる順序に輸送する。
一般に15D生の始終点型が異なるのでraw16DのEqは主張しない。

別の有限観測`selectedContextSixteenTrace`は
`whiskerLeft↦false`、`whiskerRight↦true`を外側の順序付きリストとして記録する。
`selectedSixteenMixedTraceValues`と`selectedSixteenMixedTrace_obstruction`は

\[
\begin{aligned}
\operatorname{Trace}(L(R(H)))&=[\mathrm{false},\mathrm{true}]\mathbin{+\!+}\operatorname{Trace}(H),\\
\operatorname{Trace}(R(L(H)))&=[\mathrm{true},\mathrm{false}]\mathbin{+\!+}\operatorname{Trace}(H)
\end{aligned}
\]

の非等号を証明。一方`selectedSixteenMixedTrace_lengthEqual`は長さの一致を証明した。
これは**共通観測先での比較**であり、異なる依存型に属する生16D値を同一視したものではない。

## 6. 局所選択17Dの完成範囲

v5.32で実装済みの真正16D`unitRoundtripLeft/right`の両端に、
16D反射`strict`を**前後別々に貼り合わせた**4本の実在する16D生経路
`selectedSixteenUnitPrependLeft/AppendLeft/PrependRight/AppendRight`を構成した。

左右各々の二経路は15D始終点が厳密に一致する一方、
`selectedContextSixteenFirstAtomTag`の先頭タグは3（反射前置）と0（旧16D包含前置）で異なる。
`selectedSixteenUnitLeft_rawDistinct`／`selectedSixteenUnitRight_rawDistinct`がraw16D非等号を証明。

新しい独立`SelectedLocalSeventeen`は、この**2系列の真正局所critical pairだけ**に選択17D生成元を追加し、
`strict/reverse/chain`で閉包する。
`selectedLocalSeventeen_leftWitness/rightWitness`は、局所17D比較の存在と生16D非等号を同時に証明。
`selectedLocalSeventeen_noRawEqualityInterpreter`は、選択17Dの比較がraw16D Eqを意味するという普遍解釈を否定する。

今回の17D比較は元16Dの単位貼り合わせという**厳密同一端点**に限る。異なる依存15D端点の左右二重16D輸送を結ぶ任意17D交換は生成しておらず、全体的な高次coherenceを主張しない。

## 7. 次の研究：Qi v5.34

まず今回の下位12D〜14Dパケットの上に、左右二重輸送の依存14D/15D境界をさらに比較する**実際の型付き輸送証拠**を得られる条件を探索する。
同時に17Dの局所選択商・順序観測の降下条件と、残存するobstructionを調べる。
旧raw Eq・無条件のgluing・全体的strictificationを仮定しない。

append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
