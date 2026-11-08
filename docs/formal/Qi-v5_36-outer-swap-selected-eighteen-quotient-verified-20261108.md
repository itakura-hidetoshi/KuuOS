# Qi v5.36 — 有限隣接交換の観測商・選択18D証拠商と粗密観測の区別

2026年11月8日 JST。Canonical repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.35の定理PR #3333、公開import #3334、正式記録 #3335はすべてMERGED。
元F55/P77/GK5CG、元6D〜14Dの型付き証拠、v5.23〜v5.35の独立選択presentationを変更せず、新しいLean 4モジュールを追加した。
運用：append-only／tighten-only／overwrite-forbidden／same-root。

## 1. Exact-source CIとcanonical正本

| 項目 | GitHub MCP・GitHub Actions成果物で確認 |
|---|---|
| 定理PR | [#3336](https://github.com/itakura-hidetoshi/KuuOS/pull/3336) **MERGED** |
| 初回source | `85870a7c0c3e9f6a991df4370cadbe41bb04df42` |
| 初回exact-source CI | [#42460887123](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42460887123) FAILURE（Lean構文エラー） |
| 修正後source HEAD | `a120d2887dd2a516a548a9b7ba69113c0e415452` |
| 修正後test-merge | `220d1fae1288838956bea0957dfdb4c8a9b87772` |
| 定理squash main | `7250941e32332863210e8cef13a9a340fed21d00` |
| 修正後source／test-merge／squash Git tree | **`72fb06733f32283f996267d9a3e17e10d2a6b9f2` 完全一致** |
| 修正後exact-source CI | [#42461130767](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42461130767) **completed/SUCCESS** |
| Scoped Strict Lean | **9,088 / 9,088 SUCCESS** |
| Governance | **5 / 5 SUCCESS** |
| 変更Lean error／warning | **0／0** |
| 新規宣言公理監査 | **30 / 30**：13件公理不要・17件標準公理のみ |
| 公理依存 | `propext`、`Quot.sound`のみ、`sorryAx`なし |
| 定理差分 | 新規Lean 1件・633行追加・削除0 |
| 公開import PR | [#3337](https://github.com/itakura-hidetoshi/KuuOS/pull/3337) **MERGED** |
| 公開import source | `3da7d8df2274af9ae5c19fe04d0fd70290ac1228` |
| 公開import test-merge | `e97295e30b91f241945cb5a49be8626076a553ac` |
| 公開import squash main | `920df2b6a5f5c028c3e4225b51e89151650110d4` |
| 公開import source／test-merge／squash Git tree | **`b39d3c6f583780b42c56821816cb1aa611cda1a4` 完全一致** |
| 公開import exact-source CI | [#42461901631](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42461901631) **completed/SUCCESS** |
| KuuOSFormal全体Strict Lean | **10,349 / 10,349 SUCCESS** |
| 公開Governance | **30 / 30 SUCCESS** |
| 公開集約差分 | `formal/KuuOSFormal.lean`へimport 1行のみ追加・削除0 |
| 公開root・保護PR | root107維持、#1558 Draft／OPEN／未マージ |
| 固定Lean／mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[新規Lean 4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77OuterSwapEighteenQuotientV5_36.lean)。

修正後Lean artifactの`lean-formal/receipt.json`は`status=passed`、`return_code=0`、
`git_sha=220d1fae1288838956bea0957dfdb4c8a9b87772`、`run_id=42461130767`。
`lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77OuterSwapEighteenQuotientV5_36`
のログ末尾は`Build completed successfully (9088 jobs)`。
新規30宣言の`#print axioms`結果を再集計して13件公理不要、17件標準公理のみ、`sorryAx`なし、error/warning0。
公開側artifactも`status=passed`、`return_code=0`、`git_sha=e97295e30b91f241945cb5a49be8626076a553ac`、
`build KuuOSFormal`は`Build completed successfully (10349 jobs)`。9,088と10,349は異なる対象範囲。

### 初回Leanエラーの構造的原因と最小修正

初回CIでは、`SelectedOuterSwapClosure`の帰納法で使用した生成元名`prefix`をLean 4の構文解析器が通常の未引用識別子として受理せず、
`unexpected token 'prefix'; expected '_' or identifier`および帰納法の`Missing alternative name`が連鎖発生した。
この問題は数学的な境界整合性エラーではなく、**Lean 4の構文識別子の衝突**である。

修正は同一新規Leanファイル内の3箇所を`prefix`から`prepend`に改名しただけ
（生成元の宣言、帰納法のcase、生成元の使用）。
既存の数学的仮定・元証拠・import・依存署名は変更せず、2回目のexact-source CIは完全成功。
初回失敗時ログに一時的に現れた`sorryAx`診断も構文パース不全の連鎖であり、修正後の最終結果には存在しない。

## 2. 有限観測だけに作用する隣接交換の商

v5.35の真正元第七セル由来の**観測上の**`SelectedOuterAdjacentSwap`を継承し、
`SelectedOuterSwapClosure`で反射`strict`、実在する隣接交換`observed`、
同じ外側イベントの追加`prepend`、反転`reverse`、結合`chain`の有限構文を構成した。

`selectedOuterSwapClosure_preservesCounts`は、すべての選択生成元が左右（false/true）出現回数を保存することを形式証明。
`selectedOuterSwapSetoid`はこの**共通の観測値型 `List Bool` 上だけ**の同値関係。
`selectedOuterSwapClass_eq_iff`はクラスEqと具体的な選択swap履歴の存在を同値にする。

```text
[false, true] ++ h   ~swap   [true, false] ++ h
```

この商では`selectedOuterSwap_headClassEq`により上記二つのリストのクラスは等しくなるが、
生のリスト自体は非等。`selectedOuterSwap_projectionNotInjective`が射影の非単射性、
`selectedOuterSwap_noRawTraceDescent`が**生の順序付きリストを復元する商上関数の不存在**を証明する。
一方、左右の出現回数は`selectedOuterSwapCountsOnQuotient`として正しく降下。
`selectedOuterSwap_prefixClassEq`は共通外側イベント付加後も商クラスEqを保存する。

v5.33の真正12D〜選択14Dの比較証拠パケットと、
v5.35の隣接観測swapを組み合わせた`selectedMixedTraceChange_swapClassEq`は、
別々に型付けされた上位輸送の**共通観測先の商クラス**が一致することを証明。
`selectedMixedSwapCoarseCompatible_strictGateImpossible`は同じ真正文脈で
下位比較パケットの存在・観測swap商での同一性・v5.34の厳密な順序履歴一致を要求する上位gluing gateの不存在を同時に主張する。

観測swapは依存型を跨ぐ元18Dの交換セルではなく、**観測側で選んだ表示の商**である。

## 3. 真正18D比較による別の17D証拠商

同じ真正16D始終点を持つ平行17D生証拠`J,N`に、
v5.35で構成した独立`SelectedLocalEighteen`の型付き比較が存在することを
同値関係`selectedEighteenSetoid`として形式化し、別の選択18D商を構成。

`selectedEighteen_preservesSeventeenTrace`は本物の選択18Dの5つの構成子
`strict/unitLeft/unitRight/reverse/chain`について、
16Dの外側文脈を伝える17D生証拠の全順序付き`List Bool`履歴が保存されることを証明。
したがって`selectedEighteenTraceOnQuotient`が本物の`Quotient.lift`となり、
`selectedEighteenTrace_onClass`が元値の再現を保証する。

一方、本物の18D局所単位比較は、17Dの前置`UnitPrepend`と後置`UnitAppend`を
**生値非等号のまま同じ18D商クラスへ写す**。
`selectedEighteen_projectionNotInjective`は商射影の非単射性を、
`selectedEighteen_noFirstTagDescent`は先頭の生17D構成子タグ3／0を保った商上観測の不存在を証明する。

この18D商では、生17Dの外側順序traceは**保存・降下できる**。
上記の有限`List Bool` swap商では、生の順序traceは**同一視されて降下できない**。
両者は**別の集合に置く別の同値関係**であり、矛盾ではない。

## 4. 左右二重輸送：共通観測へ写した粗密比較

元第六セル境界が適合する真正外側第七セル`left,right`の作用で
17Dの`L(R(J))`と`R(L(J))`をそれぞれの正確な依存型で構成。
16D/17Dの添字は一般に異なるため、両生値をraw Eqで同一視しない。

`selectedEighteenMixedOrder_fineTraceDistinct`は二つの18D商クラスから
**共通の`List Bool`観測先**に写した値が
`[false,true]++trace(J)`と`[true,false]++trace(J)`で異なることを証明。

`selectedEighteenMixedOrder_swapObservationsAgree`は、その別々の順序traceを
さらに**観測swap商**へ送ると値が一致することを証明する。
`selectedEighteenMixedOrder_coarseCountsAgree`は、左右出現数が等しいことを証明。
これは上位証拠のEqではなく、独立の選択商と共通の観測空間を通る可換性である。

## 5. authority境界・次のQi v5.37

本研究の確定範囲は
（1）有限観測swapのproof-relevantな商、
（2）厳密同一始終点の局所18D比較による17D証拠商、
（3）それぞれの商で保存される観測の違い、
（4）真正下位比較の存在と厳密trace保存型上位gluing障害の両立。

元F55/P77/GK5CGの高次Type値・旧証拠履歴は不変であり、
異なる依存fiber間の自動18D交換、元sourceの厳密Eq、全体的coherence、
任意上位transportの成立や全面的strictificationは主張していない。

次段Qi v5.37では、選択18Dの真正七セル文脈閉包と、
18D商から観測swap商への合成写像、
外側文脈作用と有限隣接swapのcompatibility、
局所19D単位critical pairの条件付き構成可能性を研究する。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
