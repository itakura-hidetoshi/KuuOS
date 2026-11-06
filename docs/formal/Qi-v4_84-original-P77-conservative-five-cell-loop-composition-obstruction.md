# Qi v4.84 — 元P77真正GK5CG保守的五セルloop合成と高次整合性の境界

## 0. canonical正本と検証

2026年11月6日 JST。Repository: itakura-hidetoshi/KuuOS、canonical branch: main。

| 項目 | 確定結果 |
|---|---|
| 継承基点 | Qi v4.83、main 720ef6ce840c1623ac2f31c7cc9a3659a1ec0200 |
| 定理PR | [#3191](https://github.com/itakura-hidetoshi/KuuOS/pull/3191) — MERGED |
| exact-source HEAD | 0bae7a58473167efad5673937844847c48ad7d0a |
| 定理squash | 39484e1733703175c883a67aeadca97dd5210c4d |
| source/test-merge/squash Git tree | bd5cdb35b34eeab9ccf5c131e9d543210c1274b7、完全一致 |
| exact-source CI | [#42175713203](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42175713203) — completed/SUCCESS |
| Strict Lean | **10,283 / 10,283 SUCCESS** |
| Strict Lean job | 127753683870、実Lean step 14 completed/success |
| Governance | **30 / 30 jobs SUCCESS** |
| 新規公理監査 | **17 / 17**、propext・Classical.choice・Quot.soundのみ |
| sorryAx／変更Lean warning/error | **なし／0/0** |
| 固定pin | Lean v4.30.0-rc2／mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| 公開・保護 | KuuOSFormal、root107、保護PR #1558 Draft／OPEN／未マージ |

[Leanソース全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77OriginalFiveCellLoopObstructionV4_84.lean) · [Qi v4.83正式記録](Qi-v4_83-original-P77-actual-typed-pentagon-observation.md) · [独立GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 五角5辺の元五セルが持つ真正の型

v4.83では5辺のpentagonEdge01/12/23/04/43_rawLoopをそれぞれ元のNativeGK5CGConservativeFiveCell Type値として構成済み。どのloopも、共通最終因子木とraw添字iに対応する真正P77 raw四セル w_i 上の自己五セルである。

pentagonFinalConservativeLoop はこの既存の元Typeのabbrevであり、新しい五セル文法ではない。任意の辺間でsource/target四セル w_i が同じであるため、合成に余分なcast、商、元source証拠のsubsingleton性は不要である。

## 2. 真正GK5CGの既存構成子だけで二経路を合成

次の構成を元の .trans と .symm だけでLean4に実装した。

- 長経路 L₃(i) = Loop₀₁(i) ⬝ (Loop₁₂(i) ⬝ Loop₂₃(i))。
- 短経路 L₂(i) = Loop₀₄(i) ⬝ Loop₄₃(i)。
- 差分 Δ(i) = L₃(i) ⬝ symm(L₂(i))。
- 反対向きの差分 Δrev(i) = L₂(i) ⬝ symm(L₃(i))。

実装名は pentagonLongConservativeFiveCell、pentagonShortConservativeFiveCell、pentagonDifferenceConservativeFiveCell、pentagonReverseDifferenceConservativeFiveCell。いずれも実際の元GK5CG型 Cell(w_i,w_i) に属する。長短それぞれの値のNonemptyを証明し、任意の部分状態の空木で回帰検証した。

**Δは真正の五セル自己ループであり、それを消去・充填する六セルではない。** L₃=L₂、Δ=refl、loop自明性、高次pentagonatorの存在を証明していない。

## 3. 厳密な証明語一致の障害条件

PentagonStrictFiveCellCoherence は、全raw添字iについて選択された元五セル構成子語 L₃(i)=L₂(i) が成り立つという命題。PentagonStrictFiveCellObstruction は、L₃(i)≠L₂(i) となるiが存在するという命題。

pentagonStrictFiveCellObstruction_iff は次をLean4で証明した。

\[
(\exists i,\ L_3(i)\neq L_2(i))
\quad\Longleftrightarrow\quad
\neg(\forall i,\ L_3(i)=L_2(i)).
\]

これは**元Type値の厳密な構成子語一致の境界**であり、真偽どちらかの判定はしない。さらに高次の六セル充填可能性をこの構成子語の等号と同一視しない。

## 4. 独立F112/GK5CGの元source no-goの保存

真正元F55/P77四セルの上側と下側には、既証明の符号付きassociator電荷

\[
Q_{\rm upper}=3,\quad Q_{\rm lower}=2,\quad Q_{\rm upper}-Q_{\rm lower}=1
\]

が成立する。独立GK5CGの保守的五セルはこの電荷を保存するため、**これら二つの異なる元P77四セル証明書を結ぶ保守的五セルの存在は否定される**。

v4.84の pentagonSourceChargeGap_exact と pentagonOriginalSource_noConservativePentagonator は、元の独立定理を一切変更せず継承する。pentagonLoopComposition_withSourceObstruction は、Qi側の最終raw四セル上の自己五セルの存在と、別の元F55/P77上側・下側四セル間の+1電荷差とno-goを同時に保持する。**両問題は四セルのsource/targetが異なる**ため、Qi自己loopの合成可能性から元上側／下側を結ぶ五セルの存在は導かれない。

pentagonLongConservativeFiveCell_charge_sound、pentagonShortConservativeFiveCell_charge_sound、pentagonDifferenceConservativeFiveCell_charge_sound は、新しい元五セル値に対し既証明の電荷保存定理を適用する。差分のゼロ性・非自明性を判定するものではない。

## 5. CIの失敗理由とLean4修正

初回exact-source CI [#42174764243](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42174764243) は、6定理で Unknown identifier A/B/C/D₄。Lean4ではsection変数をproof本文で参照するだけでは定理引数に導入されない。

2回目CI [#42175253681](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42175253681) は、ドキュメントコメントと定理の間に置いた局所 include 命令について unexpected token include; expected lemma の構文エラー。いずれも実ログ・Lean4公式section変数規則・依存型・新規ソース全文を照合した。

修正では6定理の宣言に元の真正部分木 A/B/C/D₄ の依存型binderを明示。既存証明・original source・charge定理・結論を弱めず、proof placeholder、追加公理、warning抑制、toolchain変更はしなかった。

最終HEAD 0bae7a58473167efad5673937844847c48ad7d0aの[CI #42175713203](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42175713203) でStrict Lean 10,283/10,283、Governance30/30、17宣言の標準公理のみ、sorryAxなし、変更Lean warning/error0/0、source/test-merge/squash Git tree一致を確認。検証済みHEADを指定して定理PR #3191をsquashマージした。

## 6. 次段階：Qi v4.85

真正元五セルloopの構成子的等式と、さらに一段高い充填証明書（必要なsource/targetの型・高次生成元・元sourceへの戻り写像）を明確に分離して研究する。F112の元四セル電荷+1によるno-goを、Qi側の異なる自己loop合成で覆すことはない。

strict 空中心、独立Kuu＝presentation、元Type値・source証拠・authority・obstruction、append-only／tighten-only／same-rootを維持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
