# Qi v5.61 — 真正八変量観測の識別限界と第九C₆による残余分離（Lean4形式認証）

記録日：2026-11-09 JST

## 正本と実際の認証

- Repository: `itakura-hidetoshi/KuuOS`、正本 `main`。出発時のQi v5.60 main HEAD `6f30b2f6bed2cae517cd910c2ca939e5c3e0f0b4`、Git tree `78e5b2c5d8ca7bc3ee0ffa100476d009f770357d`。
- [定理PR #3413](https://github.com/itakura-hidetoshi/KuuOS/pull/3413) **MERGED**。新規Leanファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77EightObservationSixthAncestorResidualV5_61.lean`、**398行追加・削除0**、他のLean source変更なし。
- 認証済みsource HEAD `f300b33e8930ae96e9e0003c0595f031021698b7`、定理squash `579e3418d092473303e73de2de3223a4fbc6db9a`。source／test-merge／squash Git tree `701153c368fb4a08e38e58ad5a2fd4fa53be57d0`、完全一致。
- [定理exact-source CI #42598568166](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42598568166) **completed SUCCESS**。Scoped Strict Lean **9,113 / 9,113**、Governance **5 / 5**、変更Lean error/warning **0 / 0**、exact-head source／terminal受領書 **2件SUCCESS**。16宣言実公理監査は公理不要7・標準のみ9・sorryAxなし。
- [公開import PR #3414](https://github.com/itakura-hidetoshi/KuuOS/pull/3414) **MERGED**。新規importのみ **+1/-0**、source `d9e1fc43d5a36343230673d4ccca2209b5db53f9`、squash `a38d2447db9ee02d629a4878f5c739a9ba5c139e`、source／test-merge／squash Git tree `c9a4c6ed51bad36dc8807b66b4165e147c29cfd4`、完全一致。
- [公開exact-source CI #42599309789](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42599309789) **completed SUCCESS**。全公開KuuOSFormal Strict Lean **10,374 / 10,374**、Governance **30 / 30**、新規16宣言の公理結果一致、sorryAxなし、変更Lean error/warning **0 / 0**、exact-head受領書 **2件SUCCESS**。
- docs-only記録PRの検証・統合とその後のmain push CIは、実際に取得した独立受領書に従って後から判定する。

## 元Type値を変えない八変量の識別限界

今回の比較の対象は**独立して新設した7構成子の `SelectedRawCongruentNineteen` 商**。旧selected19の商、旧18D真正Type値、16D fiberと17D端点の元証拠は一切変更しない。

v5.58で得た真正N→Nの原証拠をAとBとする。v5.60では `(C₁,C₂,C₃,C₄,C₅)(A)=(15,31,32,18,4)`、`(C₁,C₂,C₃,C₄,C₅)(B)=(15,31,32,18,6)` を元の証明書から形式認証した。同じ真正17D端点Nで次を構成する。

```text
L₆ := chain (reverse A) B
R₆ := chain A (reverse B)
```

v5.60で証明済み：`∀ k ≤ 5, Cₖ(L₆)=Cₖ(R₆)`、`C₆(R₆)=C₆(L₆)+2`、真正 `SelectedRawCongruentNineteen` 比較の不存在。今回はこれに加え、**独立の旧八変量の残る観測**を追加認証した。

| 従来の商観測 | L₆／R₆ | 数理・形式根拠 |
|---|---|---|
| 完全ordered raw trace | 一致 | raw reverseはtraceを変えず、chainは両者で同順に連結 |
| raw reverse総数 | 一致 | C₁との元証拠点ごとの同値、C₁の一致 |
| adjacent raw reverse数 | 一致 | source A/Bはともに最上位chainで、両者top-reverse flag=0 |
| 最上位raw reverse flag | 一致（ともに0） | L₆とR₆の最上位構成子は共にchain |
| 反転祖先ペア数 | 一致 | C₂との旧定義の同値 |
| 反転祖先三重鎖数 | 一致 | C₃との旧定義の同値 |
| 反転祖先四重鎖数 | 一致 | C₄との旧定義の同値 |
| 反転祖先五重鎖数 | 一致 | C₅との旧定義の同値 |
| **第九候補・反転祖先六重鎖C₆** | **差はちょうど2** | v5.60の元証拠を用いた真正加法式 |

ここで八変量を、最もありそうな指標で代表させたり、旧I6の未降下成分を混ぜたりしていない。各観測の型は、既に七構成子すべてで不変と証明されてきた商観測そのものである。

## 実装した16宣言と証明の経路

- `selectedRawEightSignature`：同一fiberの真正18D証拠2値に対する8成分の具体的な原データ等式。
- `selectedRawEightSignature_toObservation`：各raw成分等式から既存の**実際の8成分商観測の等式**を構成。
- `selectedAncestorShift_traceEq`：任意の真正A,Bで反転を左右へ配置してもordered traceの同一性を証明。
- `selectedAncestorShift_bothTopZero`：逆配置後の最上位がchainであることから双方のtop flag=0を証明。
- `selectedAncestorShift_adjacentIfTopEq`：**実際のA/B top flagが等しいという条件下でのみ**隣接反転数が保存される一般定理。
- `selectedSevenQuintuple_sourcesTopZero`：v5.58の固有A/Bはchain最上位ゆえ、この条件を満たすことを形式認証。
- `selectedEightTowerShift_eightSignature`：認証済みC₀〜C₅を旧C₁〜C₅の等式に接続し、trace/adjacent/topとともに八変量の完全一致を構成。
- `selectedRawEightSignature_rightChain`：実際の元18D値M:J→Nを右連結した際の原八変量の保存を証明。旧Type値と同一の元fiberを保持。
- `selectedEightTowerFiber_eightSignature`、`selectedEightTowerFiber_eightObservedEq`：Mの実在を仮定したときに、新商で実際の八観測が等しいことを証明。
- `selectedRawCongruentEight_notInjective`：八変量観測写像の非単射性を、前段の同一fiberでの**真正C₆商クラス不一致**と接続して証明。
- `selectedRawCongruentEight_noDecoder`：八観測から全新商クラスへの完全復元関数が存在しないことを証明。
- `selectedRawCongruentEight_noSixthDecoder`：八観測から新商上のC₆数値を復元できないことを証明。
- `selectedRawCongruentEight_endomorphismNotInjective`：任意の指定されたJに対し、実在する`strict J`を使ってJ→Jで非単射性を証明。任意の異端点fiber非空性は主張しない。
- `selectedRawCongruentNineObservation`：独立な第九商観測C₆を追加する定義。全商分類の仮定を含めない。
- `selectedRawCongruentNine_sixthDistinguished`：この**特定の真正商クラス対**が第九観測で区別されることのみを証明。

証明では、元v5.58の巨大なraw suffix構文全体を直接正規化していない。一般の型付きA/Bを対象に、trace、adjacent、top、right-chainとの局所互換を別々に証明してから、既存の数値証明書とC₆残余証明を貼り合わせた。

## 新規公理監査（Lean実ログ）

16宣言すべてに`#print axioms`を付与し、定理CIと公開CIで実際の証拠ログを照合。

- 公理不要7：`selectedRawEightSignature`、`selectedRawEightSignature_toObservation`、`selectedAncestorShift_traceEq`、`selectedAncestorShift_bothTopZero`、`selectedSevenQuintuple_sourcesTopZero`、`selectedRawEightSignature_rightChain`、`selectedRawCongruentNineObservation`。
- 標準公理のみ9：その他の9宣言。出現するのは`propext`と`Quot.sound`のみ。
- 新規sorryAx：**なし**。変更Lean error／warning：**0 / 0**。

この実公理監査の対象は今回の新規宣言であり、過去の全宣言や数学的な命名層の自動認証を意味しない。

## 障害・次段 Qi v5.62（未認証）

**今回の証明で解消した障害**：v5.60のC₀〜C₅一致だけからは確定できなかったtrace／adjacent／topの三条件を、実際の構成子について検証した。これにより八変量の同時一致と新商のクラス不一致が**同じ真正証拠対**において成立する。

**依然NO_DATA**：九変量観測による**全新商クラス**の分類・完全復元、すべての自然数次数について実際の有限prefixをすり抜ける証拠対の一様構成とその非単射性、任意異端点fiberの非空性、異fiber whiskering／20D gluing／全WORLD貼り合わせ、制度的な実行権限。v5.51で既証明の旧LeftNestedCount／元19D正規代表の非降下障害は依然有効。

**次段Qi v5.62候補**：先の真正A/Bの反転位置交換を任意回数反復する実際の同一fiber Type値列を定義。各反復で全raw trace、adjacency、top reverse flagと既存の有限塔prefixの互換を形式証明し、有限prefixの任意次数に対する具体的クラス分離を検討する。単に `∀ n` の条件付き定理があることを `∀ n, ∃ witness` へ無断で昇格しない。

維持：公開root107、Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、保護PR #1558 Draft/OPEN/未マージ。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
