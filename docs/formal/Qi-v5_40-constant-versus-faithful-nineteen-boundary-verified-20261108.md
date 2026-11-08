# Qi v5.40 — 具体的定数19D境界transport・忠実性不成立・比較反映条件

2026年11月8日 JST。Canonical repository: itakura-hidetoshi/KuuOS、branch: main。
前段Qi v5.39の定理 #3346、公開 #3347、正式記録 #3348は統合済み。
元F55/P77/GK5CG、元6D〜19DのType値と旧selected presentation、公開root107、固定Lean/mathlibを変更せず継承した。
append-only／tighten-only／overwrite-forbidden／same-root。保護PR #1558はDraft／OPEN／未マージ。

## 1. GitHub MCP・exact-source CIの認証範囲

| 項目 | 確認 |
|---|---|
| 定理PR | [#3349](https://github.com/itakura-hidetoshi/KuuOS/pull/3349) MERGED |
| 定理source HEAD | c40e2cc018be02b2cf3a8e332e8726326136773f |
| 定理test-merge HEAD | 4a3e9933d12ed6f315c61a0cca998105c53675e6 |
| 定理squash main | 59215055197d344f9eb6ba8025529bb8e75106cd |
| 定理source／test-merge／squash Git tree | 910132e2bfe6ac9e59b4b785d6cd2428b226c213 一致 |
| 定理exact-source CI | [#42474198094](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42474198094) SUCCESS |
| Scoped Strict Lean | 9,092 / 9,092 SUCCESS |
| 定理Governance | 5 / 5 SUCCESS |
| 新規宣言 #print axioms | 13 / 13（公理不要5件、標準公理のみ8件） |
| sorryAx・追加公理・変更Lean error／warning | なし／なし／0／0 |
| 追加変更 | 新規Lean1ファイル269行、削除0 |
| 公開PR | [#3350](https://github.com/itakura-hidetoshi/KuuOS/pull/3350) MERGED |
| 公開source HEAD | db7610f51a75507e667fa0e4c7f0edeb6bb62d2b |
| 公開test-merge HEAD | 1a3436166a5869cb1e3bfb0d578e29d308afedb8 |
| 公開squash main | 9075700ca0a2cee15ad0e684d889adbac36b84be |
| 公開source／test-merge／squash Git tree | d15b9ae954223fceb3b1ab6b0a7d7c45faada689 一致 |
| 公開exact-source CI | [#42474728586](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42474728586) SUCCESS |
| KuuOSFormal全体Strict Lean | 10,353 / 10,353 SUCCESS |
| 公開Governance | 30 / 30 SUCCESS |
| 公開変更 | KuuOSFormal import1行、削除0 |
| 固定Lean | v4.30.0-rc2 |
| mathlib | 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |

[Lean4形式証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FaithfulNineteenBoundaryObstructionV5_40.lean)。

## 2. v5.39からの更新：証明書の存在と忠実性は別問題

v5.39のSelectedMixedNineteenBoundaryは、異なる依存17D端点を持つLR／RL raw18D型間のrawTransportと、厳密同一source fiberの選択19D比較の輸送localTransportを別々に要求する。v5.39時点ではその一般的inhabitantは構成しなかった。

v5.40のselectedMixedConstantBoundaryは、任意の真正元Mについて、すべてのLR source raw18D値を、既存の真正RL値selectedEighteenRightAfterLeft(M)へ写す**定数関数**を具体的に構成する。localTransportは既存SelectedLocalNineteen.strictによる本物のType値比較なので、新しい仮定や公理を必要としない。

selectedMixedConstantAnchoredでは、指定LR→RL終点のchosenComparisonも同じ真正strict構成子で与える。
selectedMixedConstantAnchored_nonemptyにより、**指定Mに対するanchored境界証明書が定数輸送という退化的な意味では実際に非空**と証明した。

これはv5.39の「未構成」の部分的な更新であるが、忠実な境界transportの存在や、元の高次交換が実現したことを意味しない。意味の異なる二つの結論を混ぜない。

## 3. 真正同一LR source fiber内での二つの非同値19D商クラス

任意の元の真正18D Mに対し、LRの二重文脈輸送X=selectedEighteenLeftAfterRight(M)は元7D文脈からの順序付き2イベントを持つ。
同じ17D始終点fiber内に、既存のchainとreverseだけから
Y = chain (chain X (reverse X)) X
を構成する（selectedMixedLeftRoundtripAmplify）。

selectedMixedLeftRoundtrip_traceLengthは元raw18Dの順序履歴について
len(Trace(Y)) = 3 * len(Trace(X))
を証明する。Trace(X)の長さは少なくとも2なので、完全順序履歴が異なることをselectedMixedLeftRoundtrip_traceDistinctで証明した。

既存v5.37のSelectedLocalNineteenは順序付き完全traceを保存する。そのため同一LR fiberの選択19D商上でも、selectedMixedLeftRoundtrip_classDistinctが [X]₁₉ ≠ [Y]₁₉ を証明する。

## 4. 定数輸送の非忠実性と新しい忠実条件

selectedMixedConstantDescend_allでは、v5.39の本物のQuotient.liftを用いて構成した写像が**全ソースクラスを同じRL商クラスへ写す**ことを証明する。

したがって、すでに[X]₁₉ ≠ [Y]₁₉と確定した2つのソースクラスを同一視する。selectedMixedConstantDescend_notInjectiveが商関数の非単射性を形式証明した。

新しいSelectedMixedNineteenFaithfulBoundaryは、旧boundaryに追加して、輸送先で成立したすべての真正選択19D Type値比較から、元LR fiber側の真正比較を復元するreflectLocalを要求する。
これは保存localTransportの逆向きであり、一般には存在が保証されない。

selectedMixedFaithfulDescend_injectiveは、**追加のType値比較反映証明書が与えられる場合に限り**、異なるfiber間の19D商降下写像が単射になることを証明する。
selectedMixedConstantBoundary_noReflectionは具体的な定数輸送ではreflectLocalのType値関数が非空でないと証明する。
selectedMixedFaithful_notConstantは、反映可能な境界が実装済み定数境界と等しくなることを否定する。

「比較保存 ⇒ 商降下」と「比較反映 ⇒ 商単射」は異なる強さの定理であり、どちらもraw18Dの生Eqへ大域化しない。

## 5. 初回失敗と修正の構造理由

定理PRの初回exact-source CI #42473837670は、Lean本体の導入ではなく新定理の型検査でエラー3件を検出した。

- 長さ補題で再帰的trace関数全体をsimp展開した結果、whnfの心拍数制限に達した。Tripleの局所的な定義上の等式にchangeし、List.length_appendのみに限定して正規化。
- Type uSixに属する「すべての元比較を反映するType値関数」を直接 ¬ P と書いたため、Notが要求するPropとの不一致が生じた。¬ Nonempty(...)に訂正。
- そのType不一致に連鎖した明示添字不足を、LR側の二つの真正証拠X/Yを指定して解決。

元Type値証拠、定理の仮定、標準公理監査、import、固定Lean/mathlibはいずれも弱化していない。修正HEAD c40e2cc...のCIは全検査SUCCESS。初回失敗を成功の根拠に使わない。

## 6. 権威境界と次段Qi v5.41

**証明済み：** 元の真正第七セル文脈と18D証拠から、定数のanchored境界は実際に存在する。ただしその19D商写像は非単射。比較反映を追加した忠実境界なら商単射、実装済み定数境界はその条件に適合しない。

**未認証：** 忠実なcross-fiber境界証明書の一般的inhabitant、全source raw18Dに対するswap観測自然性、元のヘテロ19D/20D交換セル、非退化なhigher coherence、任意C60物理幾何への拡張。NO_DATAとして保持する。

**Qi v5.41の研究課題：** 元のselected 18D構成子とv5.37の19D単位生成元の局所compatibilityを調べ、定数以外の型付き境界transportを実際に構成できる限定的なsource presentationを探索する。比較保存・反映・swap観測自然性のどれが満たされるかを別々に示す。未構成のType値比較を存在証明に置き換えない。

本書はdocs-only正式記録であり、Lean形式証明・公開import・workflow・固定バージョンは変更しない。文書専用のGovernanceとCore Autonomyだけを検証する。
