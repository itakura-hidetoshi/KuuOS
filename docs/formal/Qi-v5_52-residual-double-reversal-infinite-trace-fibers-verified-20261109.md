# Qi v5.52 — 独立raw合同性商に残る二重反転障害と等trace fiberの無限性（Lean4形式監査記録）

記録日：2026-11-09 JST。証拠の権威はLeanソース、固定依存、completed CI、Git treeで判断する。研究上の「空・縁起」の対応づけは命名・解釈であり、Leanの定理として証明されたものとは区別する。

## 1. 正本・不変条件

- Repository: `itakura-hidetoshi/KuuOS`。canonical `main`。
- 定理PR [#3386](https://github.com/itakura-hidetoshi/KuuOS/pull/3386) **MERGED**。
- 定理source HEAD `53e7574671c9e576d7d317e10b7bbfdcd2b3b4c1`、test-merge `66a6ba82d59ffefd8640e897258ca6ec4ef760fc`、main squash `ab0bb48f73ef532d728c92a51f57008406405571`。三者共通の実Git tree `a0ca7f5f10a1ccd4a8d531a7554fa0952f547c07`（GitHub MCPで各Git commitを再取得した値）。
- 新規Leanファイル：`formal/KUOS/Architecture/QiWuxingGK5CHP77RawCongruenceDoubleReverseObstructionV5_52.lean`、294行追加、削除0。
- 公開import：[#3387](https://github.com/itakura-hidetoshi/KuuOS/pull/3387) は別PR。定理の認証と公開集約の認証を混同せず、下記の公開CI欄は検証完了後に確定する。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root 107、保護PR #1558 Draft/OPEN/未マージ。
- append-only／tighten-only／overwrite-forbidden／same-root。元18D/19D Type値証拠、旧19D比較、新7構成子比較presentation、元F55/P77/GK5CG sourceはいずれも不変更。

## 2. 証明された内容（同一の依存型fiber内）

新合同性商 `SelectedRawCongruentNineteen` において：

1. raw反転は完全ordered `List Bool` traceを保持し、raw reverse-countを厳密に1増加させる。
2. 二変数raw chainは左右のraw reverse-countを加算する。
3. 既存v5.43の`selectedContextEighteenDoubleReverse`はordered traceを保持し、raw反転回数を2増やすため、新商でも二重反転後のクラスは元のクラスと異なる。
4. したがって二重反転を消去する`SelectedRawCongruentNineteen`の真正Type値比較は存在しない。新商上の二重反転写像も、与えられた点では固定点を持たない。
5. raw反転はこの特定のraw chainとstrict identityに対する右逆元ではない。raw syntax上の反転を、群oidの逆射と同一視しない。
6. 任意の実際に与えられた18D証拠`M`について、二重反転を`n`回繰り返す。依存型始終点は保存され、`Trace(M_n)=Trace(M)`、`ReverseCount(M_n)=ReverseCount(M)+2*n` を証明した。
7. 同じ族について新商クラス`[M_n]`は`Nat`から単射であり、この族の真正比較が存在するのは`m=n`の時、かつその時に限る。
8. その証拠のordered trace値が固定されたfiberに`Nat ↪ {q // Trace(q)=Trace(M)}`を構成。指定`J`のstrict identityが与えられれば、`J→J`の空trace fiberにも`Nat`を埋め込める。
9. 完全ordered trace観測は新商で一般には忠実でなく、与えられたinhabited fiberに全クラスを戻すtrace decoderは存在しない。

## 3. Lean宣言と保存された退行検査

新規16宣言：

`selectedRawCongruentReverse_trace`; `selectedRawCongruentReverse_count`; `selectedRawCongruentChain_count`; `selectedRawCongruent_doubleReverse_classDistinct`; `selectedRawCongruent_doubleReverse_noComparison`; `selectedRawCongruent_doubleReverse_noFixedPoint`; `selectedRawCongruent_rawRightInverse_obstruction`; `selectedRawCongruentDoubleReverseIter`; `selectedRawCongruentDoubleReverseIter_trace`; `selectedRawCongruentDoubleReverseIter_count`; `selectedRawCongruentDoubleReverseIter_classInjective`; `selectedRawCongruentDoubleReverseIter_comparison_iff`; `selectedRawCongruentTraceFiberEmbedding`; `selectedRawCongruentEmptyTraceEmbedding`; `selectedRawCongruentTrace_notInjective`; `selectedRawCongruentTrace_noClassDecoder`。

初回regression-first commitで未実装名2件が検出された。その同一の退行検査命題2件を保存したまま、後続commitで真正Lean証明を追加して解消した。`sorry`、`admit`、公理の追加、原仮定の弱化、旧比較の上書きは行っていない。

## 4. 定理exact-source CI（完了・認証済み）

- [#42541517446](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42541517446) **completed SUCCESS**。変更source HEAD `53e7574671c9e576d7d317e10b7bbfdcd2b3b4c1`。
- Scoped Strict Lean：**9,104 / 9,104 SUCCESS**。Governance：**5 / 5 SUCCESS**。
- 新規宣言公理監査：**16 / 16**。公理不要3件、`Quot.sound`のみ13件。新公理0、`sorryAx`なし。変更Lean error／warning：**0 / 0**。
- source／test-merge／main squashの Git tree は上記 `a0ca7f5f10a1ccd4a8d531a7554fa0952f547c07` と一致する。以前PR本文に一時記載された異なるtree値を使用しない（PR #3386へ訂正コメントを追記済み）。
- 公開import検証：**未認証／別途要確認**。公開集約を定理のScoped CIのみで認証したと扱わない。

## 5. 障害として保持するもの（NO_DATA）

全16D／17D fiberのinhabitance、全fiberでの非自明性、一意な元Type値証拠の完全復元、raw構文の群oid化、元の旧5/6変量すべての新商降下、全新商の可算性・分類、異なるfiber間のwhiskering、無条件20D gluing、KuuOS全体の大域的一致は証明していない。

本結果は**与えられた同一依存型fiber内**の具体的無限部分族と、局所的な非降下を認証する。trace一致を新商上の同一性と誤認してはならない（Preference ⇏ Descent ⇏ Authority）。

## 6. 次の形式化対象

v5.53では、新商の二つの保存観測 `(orderedTrace, reverseCount)` の**共同fiber**が何を区別でき、何を識別できないかを、具体的に構成可能な証拠対に限定して検討する。v5.52はその全分類を主張しない。別候補として既存v5.47の他の各旧計数について新商降下の可否を1個ずつ形式化する。

この記録とREADME/ROADMAP追記はdocs-onlyであり、Lean、import、workflow、pinned dependenciesは変更しない。docs-only CIではStrict Leanを起動しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
