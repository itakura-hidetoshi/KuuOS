# Qi v5.39 — 型付き19D境界transport条件・条件付き異fiber商降下・fine履歴障害

2026年11月8日 JST。Canonical repository: itakura-hidetoshi/KuuOS、branch: main。
前段 Qi v5.38（定理 #3342、CI修正 #3343、公開 #3344、正式記録 #3345）はすべて統合済み。
既存 F55/P77/GK5CG、真正6D〜19DのType値証拠、旧selected presentationとその全履歴を変更せず継承する。
規律：append-only／tighten-only／overwrite-forbidden／same-root。

## 1. 認証範囲とGitHub MCP再観測

| 項目 | 実証結果 |
|---|---|
| 定理PR | [#3346](https://github.com/itakura-hidetoshi/KuuOS/pull/3346) MERGED |
| 定理source HEAD | c680984a69f3ee195ed13e741b95993e60667853 |
| 定理test-merge HEAD | cf05d889cc4710e456bddf490bf17bef99120e00 |
| 定理squash main HEAD | 534e856442c9a7b8084b5e876fceda089e68876c |
| 定理source/test-merge/squash Git tree | 981d53614abcb65f928c852d06c98d80c42885f7 完全一致 |
| 定理exact-source CI | [#42471675817](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42471675817) SUCCESS |
| Scoped Strict Lean | 9,091 / 9,091 SUCCESS |
| 定理Governance | 5 / 5 SUCCESS |
| 新規公理監査 | 18 / 18（公理不要9件・標準公理のみ9件） |
| 新規 sorryAx／非標準公理 | なし／なし |
| 変更Lean error／warning | 0／0 |
| 新規変更 | Lean1ファイル・309行追加・削除0 |
| 公開集約PR | [#3347](https://github.com/itakura-hidetoshi/KuuOS/pull/3347) MERGED |
| 公開source HEAD | 32693d35355ae161f2b09e08eb0b0cd8335d41a5 |
| 公開test-merge HEAD | d79be2f28a30abb41a7e7620755749008eec0bc9 |
| 公開squash main HEAD | eeb14764dfe8109fd6266c3bfdfefe04a75a9e57 |
| 公開source/test-merge/squash Git tree | 6110138541a82835e01b2bf377537b7ccd123b7d 完全一致 |
| 公開exact-source CI | [#42472134706](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42472134706) SUCCESS |
| KuuOSFormal全体Strict Lean | 10,352 / 10,352 SUCCESS |
| 公開Governance | 30 / 30 SUCCESS |
| 公開変更 | KuuOSFormal import 1行のみ・削除0 |
| 固定バージョン | Lean v4.30.0-rc2、mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| 公開root・保護PR | root107維持、#1558はDraft／OPEN／未マージ |

[Lean4定理全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TypedNineteenBoundaryTransportV5_39.lean)。

以上の数値は2026年11月8日のGitHub MCPと成功したexact-head CIログによる。定理単体の9,091と公開全体の10,352は異なる検証対象である。どちらも受領書がSUCCESSで、Git treeを独立照合した。文書だけの変更にはStrict Leanを要求しない。

## 2. 異なる依存17D端点のraw18D型を保持

v5.38の元第七セル左右二重文脈輸送を、独立の18D型
- selectedMixedLeftNineteenRaw（LR側）
- selectedMixedRightNineteenRaw（RL側）
に保持する。それぞれ異なる17D端点を持つSelectedContextualEighteenのType値であり、生Eqを導入しない。

さらにselectedMixedLeftNineteenQuot／selectedMixedRightNineteenQuotは、各々のselectedNineteenSetoidによる別々の商型を示す。観測商と元19D証拠商を同一視しない。

## 3. 必要な追加境界データと条件付き降下

SelectedMixedNineteenBoundary は次の二種類の証拠を明示的に要求する：

1. rawTransport : LRの真正18D証拠値 → RLの真正18D証拠値、という型付き写像。
2. localTransport : 任意のLR側SelectedLocalNineteen X Yという**Type値比較**から、輸送先のSelectedLocalNineteen (rawTransport X) (rawTransport Y)というType値比較を構成する作用。

これは構造体の**必要なフィールド仕様**であり、すべての元境界で構造体がinhabitedだと証明したものではない。

これらが与えられれば、selectedMixedBoundaryDescend は真正19D setoid比較を利用するQuotient.liftにより、LR商から別のRL商への関数を構成する。
selectedMixedBoundaryDescend_onClass が元18Dクラス上の計算則を証明した。

## 4. 粗い観測との自然性は独立条件

SelectedMixedBoundaryCoarseCompatible は、元のraw18D証拠すべてについて、輸送前後の共通有限swap観測クラスが一致する条件を定義する。

この追加条件を与えた時に限り、
- selectedMixedBoundaryDescend_swapNatural：19D商輸送と有限swap観測が可換。
- selectedMixedBoundaryDescend_countsNatural：左右イベント計数が対応。

を形式証明する。局所19D比較の保存だけからグローバル観測自然性が自動的に従うとは言わない。

## 5. 指定LR→RL境界と履歴変更の不可避性

SelectedMixedNineteenAnchored は上記境界データに加えて、元v5.38の真正LR証拠を輸送した結果と、真正RL証拠の間の**輸送先のType値SelectedLocalNineteen**比較chosenComparisonを持つ。

この指定比較がある場合に限り：
- selectedMixedAnchoredDescend_chosenClass：指定LR商クラスをRL商クラスに写す。
- selectedMixedAnchored_chosenSwap／chosenCounts：指定クラスの有限swap観測と左右計数が一致する。
- selectedMixedAnchored_fineTraceChanges：輸送されたLR証拠と元LR証拠の完全順序履歴は異なる。
- selectedMixedAnchored_noFinePreservation：その輸送はすべてのraw18D履歴を完全保存できない。
- selectedMixedAnchored_noFineQuotientTransport：19D商上の全クラスでも完全順序履歴保存は不可能。

証明の障害はv5.38の具体例 Trace(M_LR) = false :: true :: h、Trace(M_RL) = true :: false :: h の非等号に由来する。
真正の局所19D証拠は同一RL fiber内ではfine履歴を保存するので、指定LR→RL比較を実現する輸送そのものが順序履歴を変える必要がある。

## 6. 未認証範囲・次段

**未構成：** SelectedMixedNineteenBoundary／SelectedMixedNineteenAnchored の任意の境界での具体的inhabitant、無条件のcross-fiber19D/20D交換、異なる元Type値のEq、global coherence、任意の元C60 sourceへの大域化。
これらはNO_DATA／obstructionとして残す。観測swap商の一致は元のType値同一性を意味しない。

**Qi v5.40の研究候補：** 真正の第七セル境界が特に単純な指定クラスにおいて、rawTransportとlocalTransportを実際の既存構成子から組み立てられるかを調べる。できなければ具体的に欠けるtransport／comparisonの型と障害を証明する。追加仮定の無検証導入や形式的な存在断定は行わない。

本書はdocs-only正式記録であり、証明ソース、公開import、workflow、バージョンpinを変更しない。
