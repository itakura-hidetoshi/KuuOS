# Qi v5.32 — 真正左右混合の下位境界証明書・局所選択16Dと15D順序履歴の選択的降下

2026年11月8日 JST。Canonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.31までの定理・公開集約・正式記録はMERGED。元F55/P77/GK5CG、元6D〜14D証拠Type、既存のすべての選択presentationを変更せず、新しい独立選択presentationを追加した。

## 1. 正本・exact-source形式検証

| 対象 | 最終検証済みの事実 |
|---|---|
| 定理PR | [#3324](https://github.com/itakura-hidetoshi/KuuOS/pull/3324) **MERGED** |
| 定理source HEAD | `30c573c519818e9cf0e2569ceeecf2c1a8cb33c6` |
| 定理test-merge | `d1ac71b51413dd98faa670e8a0cc85185bd91c5c` |
| 定理squash main | `dce614b8d96dfd27fb4a338855e3e6a7843269db` |
| 上記3コミットのGit tree | **`c5dcb90ac290f8fe0cba25b3ce33525ed4fcb1bb` 完全一致** |
| 定理exact-source CI | [#42452960112](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42452960112) **completed/SUCCESS** |
| Scoped Strict Lean | **9,084 / 9,084 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 新規宣言公理依存監査 | **27 / 27**：17件公理不要、10件標準公理のみ |
| 標準公理 | `propext`、`Quot.sound`のみ |
| `sorryAx`／新公理 | **なし／なし** |
| 変更Lean error／warning | **0／0** |
| 定理差分 | 新規Lean1ファイル、616行追加・削除0 |
| 公開集約PR | [#3325](https://github.com/itakura-hidetoshi/KuuOS/pull/3325) **MERGED** |
| 公開集約source HEAD | `54eabc55e06330f3e87e7b7dd73d37b38cf8f46f` |
| 公開集約test-merge | `b6dcd390b27e444211bc7e777eb4d6f432762d59` |
| 公開集約squash main | `d8b01f0bf85b3c2220afd067437ce977aad85b8f` |
| 公開集約の3コミットのGit tree | **`4a00fa91556f5bc28ef95c36f46014007ccfc16a` 完全一致** |
| 公開集約CI | [#42453327889](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42453327889) **completed/SUCCESS** |
| KuuOSFormal全体Strict Lean | **10,345 / 10,345 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開差分 | `formal/KuuOSFormal.lean`のimport1行追加／削除0 |
| 固定Lean/mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root／保護PR | root107維持、#1558 Draft／OPEN／未マージ |

[Lean4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedBoundarySixteenV5_32.lean)。

定理のLean receiptは`status=passed`、`return_code=0`、
`git_sha=d1ac71b51413dd98faa670e8a0cc85185bd91c5c`を記録。
`lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77MixedBoundarySixteenV5_32`
は`Build completed successfully (9084 jobs)`で完了。
27件の`#print axioms`を独立して集計した。
公開集約receiptも`status=passed`・`return_code=0`であり、
`build KuuOSFormal`は`Build completed successfully (10345 jobs)`。
対象限定9,084と公開全体10,345は別の検証対象である。

## 2. 真正double-whiskerの二端点境界証明書

v5.31の二つの15D輸送`L(R(T))`／`R(L(T))`は元の14D境界の依存型が一般に異なる。
したがって未証明の同一視を避け、元v5.18の`doubleWhisker`から、
v5.27選択12Dへの二段`previous`を経て構成可能な
`SelectedMixedLowerBoundaryPacket`を追加した。

これは元第六セル境界が厳密に整合する真正第七セル`left,right`と
元第十一セル証拠`F,G`を引数とし、
11D始点・終点の両方に対して実際の12D境界橋を保持する。
`selectedMixedLowerBoundaryQuotients`は両端での選択12D商クラスの一致を証明する。

**重要な境界：** この証明書は真正な下位11D端点の互換性を保証するが、
異なる依存14D境界を同一視する証拠でも、二つの15D混合輸送の
任意16D比較でもない。必要な上位coherenceは未証明のまま明示する。

## 3. 左右二重輸送の順序履歴と粗い計数

元v5.31の順序付き15D外側文脈観測を保存し、新しい
`selectedFifteenTraceCounts : List Bool → Nat × Nat`を定義。
これはfalse（左）とtrue（右）の各出現回数のみを記録する。

任意の元六セル境界適合15D証拠`T`と真正外側左右七セルについて、

\[
\begin{aligned}
\mathrm{Trace}(L(R(T)))&=[\mathrm{false},\mathrm{true}]\mathbin{+\!+}\mathrm{Trace}(T),\\
\mathrm{Trace}(R(L(T)))&=[\mathrm{true},\mathrm{false}]\mathbin{+\!+}\mathrm{Trace}(T)
\end{aligned}
\]

は等しくない。一方、左右の出現回数は双方とも1ずつ増え、
`selectedFifteenMixedCountsEqual`が粗い計数の一致を形式証明。
`selectedFifteenMixedCoarseFineSeparation`は**同一計数／異なる順序履歴**
を一つの定理に統合した。両15D証拠自体のEqは依存型が異なるため主張しない。

## 4. 真正な局所第十六セル生成元

旧v5.30の本物の15D局所単位比較を用い、往復・逆往復の15Dループを構成した。
それぞれ`strict`と**厳密に同じ14D始終点**を持つが、
新しい`selectedFifteenFirstAtomTag`で
前者はタグ0、逆往復は4、反射は3と識別され、
`selectedFifteenUnitRoundtrip_rawDistinct`／
`selectedFifteenReverseRoundtrip_rawDistinct`がraw非等号を証明した。

独立した`SelectedLocalSixteen`では、真正に型付きの
`unitRoundtripLeft`と`unitRoundtripRight`のみを新規非自明生成元として選択し、
`strict/reverse/chain`によって閉包した。

\[
\boxed{
\mathrm{Roundtrip}_{15}
\xRrightarrow{\mathrm{selected\ 16D}}
\mathrm{Strict}_{15}
}
\]

これは明示的に選択した局所16D comparisonであり、
旧15Dのraw Eqでも、左右二重輸送の全面的16D exchangeでもない。

## 5. 第十五セル商での選択的降下と非降下

`selectedSixteenSetoid`は、全く同じ14D始終点を持つ15D raw証拠上に
「選択16D比較が存在する」という同値関係を定義した。
`selectedSixteenClass_eq_iff`は15Dの商クラス等号と
型付き16D比較の存在との同値を証明する。
局所16D生成元から15Dループと反射がこの商で一致する。

`selectedSixteen_preservesTrace`は新しい16D構成子の全体について
**元v5.31の外側順序付きList Bool履歴が保存される**ことを証明。
そのため`selectedSixteenTraceOnQuotient`は真正な`Quotient.lift`となり、
`selectedSixteenTrace_onClass`で元値を再現する。

一方、局所16D比較がタグ0の15Dループをタグ3の反射へ接続するため、
`selectedSixteen_noFirstTagDescent`は
raw15D先頭構成子タグの商への降下が不可能なことを否定存在定理として証明。
ここでは**順序付き外側履歴は降下可能、先頭構成子タグは降下不能**という
二種類の観測のauthority境界が数学的に確定した。

さらに`selectedSixteenMixedOrderTraceObstruction`は、
異なる14D依存型に属する左右二重輸送の16D商クラスに対して
共通の`List Bool`値として観測した順序差が残ることを証明。
`selectedSixteenMixedOrderCountAgreement`は
その粗い左右計数が等しいことを別途証明する。
異なる商クラス自体を同一Type値として比較する主張はしない。

## 6. 既存authorityの保存とQi v5.33

元F55/P77/GK5CG、旧6D〜14D証拠、v5.32以前の選択型・元の厳密Eqは不変。
今回は「下位11D互換性の真正証明書」「局所16D単位比較」
「15D商への順序履歴の降下」「rawタグの非降下」を結合した成果である。
任意の二重文脈15D輸送の16D自然同型、上位境界の全面的なgluing、
元sourceへの自動descentは未証明。

次段Qi v5.33：左右二重15Dの**異なる14D依存境界を接続できる
実際の13D/14D comparison packet**の存在可能性を検査。
橋が構成できない場合は、新生成元で強引に埋めず、
必要条件とobstructionを別々に形式証明する。
併せて16Dの局所比較を再文脈化したときに保存される観測と
新たな17D coherenceの必要性を評価する。

append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
