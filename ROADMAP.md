# KuuOS / 空OS — Research ROADMAP

**研究地図（GitHub MCP観測：2026-11-27 JST）**

この文書は認証済み範囲、研究ブランチ上の成果、公開root、未解決obstruction、次の受入条件を同時に読むためのロードマップである。[README](README.md) は目的・利用方法・全体構造を案内する。

- 観測正本：[`main` @ `e1d754e8e0fc`](https://github.com/itakura-hidetoshi/KuuOS/commit/e1d754e8e0fc9382001a2e698751aa11d4272b84)（tree `bdf2e81fc2cf702481b80e7079e59b1b47836013`）
- 固定環境：Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。proof scope `2d9d0c313b6f7d8e4df0900fd0977324999a4200c1ed3c1adb178706370dbd6b`
- 保護：[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。変更禁止
- 旧版は[2026-11-22 README](docs/history/README-SNAPSHOT-20261122.md)・[ROADMAP](docs/history/ROADMAP-SNAPSHOT-20261122.md)・[2026-11-21以前のREADME](docs/history/README-THROUGH-20261121.md)・[ROADMAP](docs/history/ROADMAP-THROUGH-20261121.md)へ元blobのまま保存

## 0. 証拠と状態の読み方

| 状態 | 意味 |
| --- | --- |
| MERGED / canonical | 対象ソースがmainに採用された。以後の新規定理・実行権限を保証しない |
| LOCAL VERIFIED | 固定Leanでの直接検証・実Lean MCP成功。独立認証とは異なる |
| CI CERTIFIED (scoped) | 指定HEAD・指定宣言・指定環境の独立認証成功 |
| REUSE_EXISTING | 指定した完全型について証明項を構成・確認した範囲での再利用 |
| REFUTED_EXACT_TARGET | 指定命題Pに対する¬Pの実証明。別条件・別目標には移さない |
| HOLD / NO_DATA | 条件・証拠不足、探索miss、実行障害。数学的反証ではない |

`Preference ⇏ Descent ⇏ Authority`。候補の選好、局所貼合、形式証明、runtime妥当性、Memory昇格、行為権限、正本へのマージを別々に判定する。

## 1. canonical main：既に採用された基盤

| 領域 | 採用済み成果 | 次に必要な条件 |
| --- | --- | --- |
| Lean→Python | v0.60 [PR #3622](https://github.com/itakura-hidetoshi/KuuOS/pull/3622)、v0.61 adapter [PR #3626](https://github.com/itakura-hidetoshi/KuuOS/pull/3626)、候補Aの同一blob Lean 8宣言 [PR #3628](https://github.com/itakura-hidetoshi/KuuOS/pull/3628) | [PR #3629](https://github.com/itakura-hidetoshi/KuuOS/pull/3629) の公開rootと全体Strict Lean・Governance、元Pythonとの一般精密化 |
| CodeAI候補検証 | v0.61研究基盤 [PR #3623](https://github.com/itakura-hidetoshi/KuuOS/pull/3623)・[PR #3625](https://github.com/itakura-hidetoshi/KuuOS/pull/3625)・[PR #3626](https://github.com/itakura-hidetoshi/KuuOS/pull/3626)、`simpa` locator修正 [PR #3630](https://github.com/itakura-hidetoshi/KuuOS/pull/3630) | 4検証系統の独立受領書と同一candidate/source/contextの真正性、Memory昇格を別審査 |
| 既存証明検索 | [PR #3638](https://github.com/itakura-hidetoshi/KuuOS/pull/3638) 必須prior-proof gate、[PR #3639](https://github.com/itakura-hidetoshi/KuuOS/pull/3639) v0.3全ソース字句索引、[PR #3640](https://github.com/itakura-hidetoshi/KuuOS/pull/3640) v0.4、[PR #3641](https://github.com/itakura-hidetoshi/KuuOS/pull/3641) v0.5合計13既存宣言のカーネル記憶 | 未観測・推移依存の欠落を明示。新規性・実行権限に昇格させない |
| 共有Lean artifact | [PR #3643](https://github.com/itakura-hidetoshi/KuuOS/pull/3643)・[PR #3644](https://github.com/itakura-hidetoshi/KuuOS/pull/3644) の認証済み正本キャッシュ・別runner実再利用 | source・scope・pins・artifact digest・producer/verifierを照合し、missは既存Strict Leanへ戻す |
| Qi / C60 / F112 | [PR #3631](https://github.com/itakura-hidetoshi/KuuOS/pull/3631) Qi v5.99、[PR #3632](https://github.com/itakura-hidetoshi/KuuOS/pull/3632)・[PR #3633](https://github.com/itakura-hidetoshi/KuuOS/pull/3633) 真正物理gauge／五行／K5条件付き橋、[PR #3636](https://github.com/itakura-hidetoshi/KuuOS/pull/3636) 元F45五段階の構成 | [PR #3635](https://github.com/itakura-hidetoshi/KuuOS/pull/3635) 公開root、[PR #3637](https://github.com/itakura-hidetoshi/KuuOS/pull/3637) phase-sector同値の正式採用、異なるgaugeの同一性を仮定しない |

正本v0.5では13宣言の既存証明記憶を正本上で参照できるが、元[検証記録](docs/CodeAI/PRIOR_PROOF_KERNEL_MEMORY_v0_5.md)にあるproviderは決定的HOLDの試験用callbackであり、外部モデルによる新規証明生成は確認していない。従来の4系統独立検証器v0.2のHOLDを、この成功だけで解除しない。

## 2. Track A — 次世代CodeAI：検索・No-Go・再利用

### A1. 独立認証された研究成果（main未統合）

研究ブランチ：[`research/codeai-nogo-memory-v1-20261126`](https://github.com/itakura-hidetoshi/KuuOS/tree/research/codeai-nogo-memory-v1-20261126)。各段の成功は対応する研究HEADの範囲のみ。

| 段階 | 実装・認証内容 | 根拠 |
| --- | --- | --- |
| R7 | `.olean`カーネル型構造の分割収集・集約。全対象の未観測部分を保持 | [CI #45774874136](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45774874136) |
| R17–R19 | 再帰前提探索・二／三前提AND–OR・全索引由来の型構造選定と文脈限定No-Go | 後続R20のadmitted inventory |
| R20 R2 | 最上位定理名を指定せず、閉じた前提を型付きで選択 | [CI #45811079734](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45811079734) |
| R21–R22 R2 | 閉じた末端証明DAG、特殊化部分証明の共有 | [CI #45813837876](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45813837876)、[CI #45882835148](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45882835148) |
| R23 R2–R24 | 証明カプセルのコンパイル済みbyte移送、完全型・証明項・来歴固定の登録簿 | [CI #45893906832](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45893906832)、[CI #45895057363](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45895057363) |
| R25 | 新目標に対する完全型／定義的等価性照合。正・負4証明項、6宣言監査、HOLD2件 | [CI #45896476614](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45896476614) |
| R26 R2 | 再帰探索内カプセル再利用、No-Goによる経路単位の遮断、別経路の証明、17宣言監査 | [CI #45898216584](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45898216584) |
| R27 R2 | 正3・負2候補、7種類の目標型、完全型・公理・来歴を固定した比較メモ。24宣言監査、35再利用ヒット | [CI #45901313851](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45901313851) |

**R27 R2最終受領書：**

- research HEAD `4b3889aa3f5bb2c287721b772c4e9b580326cc5a`、tree `468beac80257b8b11a897d659c4b265bcc2ee34a`
- Direct digest `f6c1a4d1b1ef6548af45b86f8b12ea430a5a1cde1e655e3822cd1736d81a0750`
- MCP digest `da1c151e133d62a644eb3d3491ec21f90139cd6a1500e4dcebbefe614ac01c2f`
- inventory key `e8c2432768ea3dd062a0db14cf845e860f86335c19281e301294f8ec38ff905b`
- Sandbox job 140187492000／独立job 140189131473、artifact 15155193581／15156532332。両runner Direct digest一致、外部provider呼出し0、カプセル再構築0

[認証済みR27実装（固定HEAD）](https://github.com/itakura-hidetoshi/KuuOS/blob/4b3889aa3f5bb2c287721b772c4e9b580326cc5a/runtime/kuuos_codeai_olean_multi_typed_recall_v1_r2.py)・[検査スクリプト](https://github.com/itakura-hidetoshi/KuuOS/blob/4b3889aa3f5bb2c287721b772c4e9b580326cc5a/scripts/check_codeai_olean_multi_typed_recall_v1_r27_r2.py)。未観測モジュール695、意味探索の完全性はfalse。

### A2. 直近の研究 R28 — 実行間の版固定記憶

[研究HEAD `c05a986ecd57`](https://github.com/itakura-hidetoshi/KuuOS/commit/c05a986ecd571a1b00da255a7552ee8a54b4a709)、[CI #45902979815](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45902979815)。観測時点：Sandbox実行中、固定Leanと認証済み正本キャッシュの復元・scope照合成功、固定mathlib確認中。直接Lean・実Lean MCP・別runner独立CIは未確認。

[R28実装（未認証）](https://github.com/itakura-hidetoshi/KuuOS/blob/c05a986ecd571a1b00da255a7552ee8a54b4a709/runtime/kuuos_codeai_olean_portable_exact_recall_v1.py) は、R27の独立認証受領書から7件の完全型記憶を生成し、別runnerで新しい完全型の観測と照合する設計。既存記憶は証明候補の選択に使い、実際の証明項は新たにLean検証する。

| 検証条件 | 期待結果（未認証） |
| --- | --- |
| 過去に観測した閉じた完全型6件 | 正4・負2の型付き再適用 |
| 過去の検索miss | HOLD_HISTORICAL_NO_MATCH（¬Pではない） |
| 未観測の新規目標型 | HOLD_SEARCH_REQUIRED |
| 記憶改変・再ハッシュ | HOLD。自己計算したハッシュは認証受領書の代わりにならない |
| scope・登録簿・live型の変更 | HOLD／再認証 |
| 同一受領書・同一source | 新しい候補比較探索、最上位探索、カプセル再構築を不要にする範囲を測定 |

**受入条件**：認証済みR27受領書・artifact・正本・pinを照合し、正負の新規証明項を直接Lean／実Lean MCPで検査、別runnerでsandbox成果物を再観測。独立受領書とソースの一致を確認する。それまでは採用禁止。

### A3. その次の研究（計画・未着手として扱う）

1. R28の結果を確認後、永続化記憶をR26/R27の再帰探索途中へ接続する。型・文脈・scopeに合う部分だけを再利用し、未解決前提のみを探索する。
2. 同じ目標に複数の正の証明経路がある場合、候補と来歴を保持する。負の証明はその必要前提を持つ経路に限定し、代替を不正に排除しない。
3. 47,705件の型構造索引の完全型観測を拡張する。対象2,815モジュール中2,120観測、695 HOLD、完全型2,390件、否定構造候補5,558件。字句的No-Go候補6,380件は別の観測であり、数を足して反証の総数としない。
4. 候補生成・実修復・既存証明検索を単一の汎用経路に接続し、再利用・HOLD・反証・時間・計算量・依存変更・失敗再発率を検証する。
5. 研究ブランチの正式採用は別の統合PRで行う。元ソース・pins・scope、独立受領書、test-merge tree、既存回帰、公開root（該当時）、Governance、採用権限を確認する。全研究ブランチや失敗候補を一括で本番へ昇格させない。

**保留**：一般的な完全探索、任意の依存型・universeに対する自動証明、全No-Goの網羅、異なるLean版での互換性、外部モデルの実運用性能、4検証系統の真正な独立性、`verified_useful`昇格。検索候補数だけで有効な証明の数を評価しない。

## 3. Track B — 高次縁起・元Type値・降下

**[PR #3555](https://github.com/itakura-hidetoshi/KuuOS/pull/3555)：Draft／OPEN／未マージ。** 観測HEAD `a637438ceebdcb5b0247f30f14479b85b3bd0e1f`。同HEADで個別のv1.35 [CI #45343467773](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45343467773)、v1.70 [CI #45343469142](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45343469142) はSUCCESSだが、v1.73候補probe [CI #45343467763](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45343467763) はFAILURE。PR全体の認証を主張しない。[PR #3548](https://github.com/itakura-hidetoshi/KuuOS/pull/3548) のv1.111具体的4D type-(A)はvalidation-only、正式統合とは区別。

研究目標は型付きpresentation、元のType値、真正endpoint、型付き輸送、whiskering、coherence、Type-(A)/(B)/(C)のscaling・RLPを、元定義と仮定を保ったまま接続すること。

受入条件：対象Lean全文、imports、dependent signatures、固定mathlib API、elaboration failureの構造原因、独立CIと公理監査、公開root、Governanceを確認する。仮定弱化・空虚witness・新規公理・sorry・別presentationの無断同一化は禁止。

## 4. Track C — Qi／五行／C60／F112

### C1. 採用済みの数学

- Qi v5.99 [PR #3631](https://github.com/itakura-hidetoshi/KuuOS/pull/3631)：選択した五相shadowと真正C60 physical Slot/Dart/Edge、gauge共変性、元18D bracket・型付きpayloadの忠実なjoint observation、物理shadow単独の非忠実性。[Lean source](formal/KUOS/Architecture/QiWuxingGK5CHP77C60GaugeOriginalSourceBridgeV5_99.lean)には19個の公理監査対象がある。
- [PR #3632](https://github.com/itakura-hidetoshi/KuuOS/pull/3632) [north C60物理gaugeとK5境界](formal/Kuu/F112/PolygonNativeC60NorthK5GaugeBoundaryBridge.lean)：2定理。
- [PR #3633](https://github.com/itakura-hidetoshi/KuuOS/pull/3633) [五相＋物理gauge＋K5の条件付き橋](formal/Kuu/F112/PolygonNativeC60NorthWuxingK5TripleGaugeBridge.lean)：1定理。
- [PR #3636](https://github.com/itakura-hidetoshi/KuuOS/pull/3636) [元のF45五段階の構成と14個のK5括弧付け](formal/Kuu/F112/PolygonNativeC60NorthWuxingK5ActualFiveStageGauge.lean)：2定理。

異なる型付きgauge構造を単一の作用としない。五相shadowの選び方は明示したinterfaceであり、あらゆる元証拠がその商から復元できるという主張ではない。

### C2. 未統合・公開root

| 対象 | 現在の状態と次条件 |
| --- | --- |
| [PR #3635](https://github.com/itakura-hidetoshi/KuuOS/pull/3635) | Draft・OPEN、既存の二つのmodule importを公開rootへ追加する別PR。元ソース採用済みであることと公開rootの認証を区別する |
| [PR #3637](https://github.com/itakura-hidetoshi/KuuOS/pull/3637) | Draft・OPEN、phase↔sector同値の6宣言は [CI #45251598224](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45251598224) SUCCESS、旧HEADのGovernance [CI #45277272929](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45277272929) SUCCESS。現在のbase/test-merge tree・採用権限の確認が必要 |
| [PR #3634](https://github.com/itakura-hidetoshi/KuuOS/pull/3634) | validation-only。元PR #3631がマージされていても子PRの無条件マージは禁止 |
| 13/14-cell等 | 既存形式ソースと公開rootの範囲を尊重し、新規分割・heartbeat・timeoutは対象別に監査。局所結果を全高次coherenceへ昇格しない |

C60は一般縁起理論のテストベッドであって、一般理論はC60に還元しない。次の新規提案前にはQi・GK5・F112等の既存Lean宣言・型・仮定・依存・No-Goを横断照合する。

## 5. Track D — Lean→Python・各OSの接続

v0.60 Lean、v0.61 adapterと元候補Aの正式Leanファイルはmain採用済み。[PR #3629](https://github.com/itakura-hidetoshi/KuuOS/pull/3629) の公開rootはDraft・OPEN、[CI #44980424064](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44980424064) FAILURE、Public Proof Roots [CI #44980424086](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44980424086) SUCCESSを区別する。

| 接続 | 次の証明・試験条件 |
| --- | --- |
| MemoryOS / Plural / Wa → BeliefOS | 元観測、出典、文脈、型、履歴の保存。要約の一致を元証拠の一致にしない |
| DecisionOS → VerifyOS → PlanOS | 元Pythonの操作とLeanの型・仮定・保存量を個別に対応させる。6経路等の局所回帰を全体意味保存にしない |
| PlanOS → ActOS → ObserveOS | 計画・許可・実行・効果・独立再観測を分離 |
| LearnOS / CodeAI → MemoryOS | exact version／依存／subtask／独立受領書。旧v0.61の4系統不足のHOLDを維持 |

全OSのLean↔Python双方向意味保存、実WORLDと形式WORLDの同一性、外部行為の権限付与は未証明である。

## 6. Track E — 検証インフラ・運用

### E1. 実際に成功した認証済み共有キャッシュ

[PR #3643](https://github.com/itakura-hidetoshi/KuuOS/pull/3643)・[PR #3644](https://github.com/itakura-hidetoshi/KuuOS/pull/3644) MERGED。[producer/verifier](scripts/ci_verified_lean_project_cache_v1.py)は正本由来・固定proof scope・pins・source ancestry・artifact SHA-256/size・manifestを検証して安全に復元する。

| 実測 | 結果 |
| --- | --- |
| 正本publisher [CI #45615980980](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45615980980) | full Strict KuuOSFormal 10,433/10,433、artifact 15038487740（940,848,666 bytes） |
| 別runner [CI #45700676928](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45700676928) | 同一artifact復元、同一full Strict Lakeコマンド4.74秒、2,120 olean size/mtime保持 |
| #3644後の正本 | [CI #45711044342](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45711044342) Runtime full check SUCCESS、[CI #45711044643](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/45711044643) sharded Governance SUCCESS |

これは上記の観測範囲の実績であり、変更されたLean sourceの無検証再利用ではない。別PRの証明や期限切れartifactを正本扱いしない。未知・不一致は通常Strict Leanへ戻す。

### E2. 固定運用

1. GitHub MCPで対象HEAD・main・保護PRを固定し、既存形式成果物を検索する。
2. 認証済み完全型・証明カプセル・No-Goを再利用し、未解決部分だけ候補生成する。
3. GitHub隔離Sandboxで直接Lean、実Lean MCP、宣言公理監査を行う。GREEN前に独立CIを起動しない。可能な限り同じ作業単位内で修復から独立CI起動へ接続する。
4. 別runner独立CI、source／test-merge tree一致、必要時の公開root・Governance、採用権限を検査する。workflow/job/Lean stepの終了・実ログを確認する。
5. 失敗理由・scope・修復・再観測を版固定のappend-only記憶へ保存する。失敗候補を認証済みにしない。認証済み同一ソースを不要に再計算しない。

文書専用の更新には新規Lean定理の認証を要求しない。ただし、研究実験がexact canonical HEADを固定している場合、README等だけの正本変更でもそのHEAD照合を壊し得る。現行の実行を完了させ、旧観測HEAD・新HEAD・formal/lean subtree・固定proof scopeの関係を明示してから変更する。正本変更後も旧HEADの認証はその旧HEADに限定する。

## 7. 長期目標と残る境界

一般縁起の型付きpresentation間の必要十分なcompatibility・降下・obstructionを広げ、Lean形式化と元Python OSの対応、証明の再利用、独立再観測、権限ゲートを結ぶ。別正本[4d-mass-gap](https://github.com/itakura-hidetoshi/4d-mass-gap)への適用は研究実験として扱う。

**全KuuOSの完成、任意数学の自動証明、AIのハルシネーション消滅、仏教思想の形式証明、AIの無条件自律行為を宣言しない。** 現行ソース・形式成果物・実CIログが文書・記憶・モデル出力に優先する。

---

履歴：旧版の相対リンクを元の配置で開く場合は[観測正本の旧README](https://github.com/itakura-hidetoshi/KuuOS/blob/e1d754e8e0fc9382001a2e698751aa11d4272b84/README.md)・[旧ROADMAP](https://github.com/itakura-hidetoshi/KuuOS/blob/e1d754e8e0fc9382001a2e698751aa11d4272b84/ROADMAP.md)を使用する。各時点の「最新」「次段」「SUCCESS」は当時のHEADと範囲の記録として保持する。
