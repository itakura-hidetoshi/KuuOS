# Qi v5.58 — 七変量観測の残余raw反転祖先五重鎖障害（Lean4形式監査正本）

正式記録日：2026-11-09 UTC

## 1. Canonical正本・分離した検証・統合履歴

Repository：`itakura-hidetoshi/KuuOS`。Canonical branch：`main`。継承したQi v5.57完了HEADは `48194c223150739707c2e4ce241423628107d73b`、Git treeは `1a8c7fe99f9f6ca2e7bb542bdd7517db71ab9033`。

元の真正18D Type値証拠、元selected19比較、独立v5.50の新7構成子raw合同性、既存のすべての証明を変更しない独立モジュール：

[Qi v5.58 Lean4形式証明全文（認証済みexact source）](https://github.com/itakura-hidetoshi/KuuOS/blob/fa18260d5f6c110c27b64449154c39d3bbbdfecd/formal/KUOS/Architecture/QiWuxingGK5CHP77SevenObservationAncestorQuintupleV5_58.lean)

| 検証項目 | 定理 | 公開集約 |
| --- | --- | --- |
| PR | [#3404](https://github.com/itakura-hidetoshi/KuuOS/pull/3404) **MERGED** | [#3405](https://github.com/itakura-hidetoshi/KuuOS/pull/3405) **MERGED** |
| Exact-source CI | [#42573905069](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42573905069) **completed SUCCESS** | [#42574710291](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42574710291) **completed SUCCESS** |
| Strict Lean | Scoped **9,110 / 9,110 SUCCESS** | KuuOSFormal **10,371 / 10,371 SUCCESS** |
| Governanceを含む全job | **5 / 5 SUCCESS** | **32 / 32 SUCCESS** |
| 新規宣言の実公理監査 | **22 / 22** | **同じ22件を再確認** |
| 公理依存 | **14宣言なし、8宣言は標準のみ** | **定理段階の実結果と全件一致** |
| 新規sorryAx | **なし** | **なし** |
| 変更Lean error / warning | **0 / 0** | **0 / 0** |
| Source SHAのexact-head受領書 | **2件SUCCESS** | **2件SUCCESS** |
| 変更範囲 | 新規Lean 1ファイル・518行 | 公開import **+1行 / -0** |

公理監査の「標準のみ」は `propext` / `Quot.sound` を指す。全22件の個別結果は§5。公開CIは全公開集約を検証し、既存の公開証明とroot107を保持した。

**定理のGit来歴**

- 修正後source：`fa18260d5f6c110c27b64449154c39d3bbbdfecd`
- test-merge：`2ca9a79c9a81e54ed7b5b8ef94692b3acab8f72b`
- 統合squash：`ebc4ed0de39471d32841bf3e3f2150a8b656c59c`
- Source / test-merge / squash共通Git tree：`99875813b434f4aa4c9edd879379c2b9457a8a00`

**公開importのGit来歴**

- Source：`119c18031a95a15197954db6538fcb6fdef07b20`
- test-merge：`fb942ad384d1cee03afa65c8cf6feef1df29defe`
- 統合squash：`f5c79e811ebb798e67e33526fe2fd31c4c7ee577`
- Source / test-merge / squash共通Git tree：`ebfc62a4124257e6e8e6b420fdad195cd4e1ebcf`

二つの受領書はそれぞれ `chatgpt-ci-receipt/KuuOS Strict Lean formal validation` と `chatgpt-ci-receipt/KuuOS exact-head terminal`。実際の固定Lean checkの終了コードはいずれも0。定理checkは78.681秒、新moduleは62秒。公開checkは67.513秒。CIはtest-mergeで走るため、sourceとのGit tree一致を別途確認し、受領書が正しいsource SHAを指すことも確認した。

公開sourceの他9 workflowは8件SUCCESS、1件SKIPPED（既存のIndependent Kuu Foundationの選択結果）。未完了・FAILUREはない。定理squash後のmain pushに対するLean Formal Validation、Runtime Full Check、Sharded Full Governance AuditおよびCI Completion Reentryもcompleted SUCCESSを確認した。

この正式記録の作成基点は公開統合後のmain `f5c79e811ebb798e67e33526fe2fd31c4c7ee577`。正式記録・README・ROADMAPのdocs-only PRは独立に検証し、そのsource・CI・統合SHAは当該PRの受領書に残す。docs自身の統合後SHAを、この事前作成ファイルのSHAとして先取りしない。



## 2. 第8商不変量：反転祖先五重鎖数

既存の四重鎖計数を C₄、新しい五重鎖計数を C₅ とする。新規定義 `selectedContextEighteenReverseAncestorQuintupleCount` は、元の真正raw構成子について次を満たす。

```text
C₅(inherited old18) = 0
C₅(strict J) = 0
C₅(reverse M) = C₅(M) + C₄(M)
C₅(chain M L) = C₅(M) + C₅(L)
```

元Type値の内部を勝手に展開せず、inheritedを不透明な葉として観測する。これは元証拠の削除や同一視ではない。局所whiskeringでは再帰的に数を保持するが、異fiberの比較可能性を追加しない。

元selected19の5構成子と、新v5.50合同性比較の7構成子をそれぞれ構造帰納法で検証する。`rawReverse`では五重鎖計数の帰納法仮定に加え、既認証の `selectedRawCongruent_preservesReverseAncestorQuadruple` を使用する。元商と新商に別々の `Quotient.lift` を定義し、旧商→新商の射影に関する因子化も証明する。

## 3. v5.57の真正証拠を再利用した反例

v5.57の元の二つのsuffixを、そのまま次のように参照する。

```text
A = selectedSixQuadrupleSuffixLeft  N
B = selectedSixQuadrupleSuffixRight N
L = chain (reverse A) B
R = chain A (reverse B)
```

A、B、L、Rはいずれも、元の指定端点Nにおける真正 `SelectedContextualEighteen ... N N` の値である。従来のA/Bを作り替えず、外側に追加する一つのreverseの位置だけを変える。

| suffix観測 | L | R |
| --- | ---: | ---: |
| 完全ordered trace | `[]` | `[]` |
| 総raw反転数 | 15 | 15 |
| 隣接raw反転数 | 4 | 4 |
| 最外層raw反転フラグ | 0 | 0 |
| 反転祖先対数 | 31 | 31 |
| 反転祖先三重鎖数 | 32 | 32 |
| 反転祖先四重鎖数 | 18 | 18 |
| 反転祖先五重鎖数 | **4** | **6** |

`selectedSevenQuintuple_suffixSignature` が六種類の数値計数について左右それぞれの正確な値を証明する。完全ordered traceは両suffixで空、最外層はどちらもchainなのでフラグは0。既存の七変量の一致は、次の真正商観測の等式として個別に証明する。

元16D fiberと真正17D端点J,Nを固定し、**実在する元18D証拠 `M:J→N` が与えられたとき**、同じMに右合成した

```text
left(M)  = chain M L
right(M) = chain M R
```

は、同じ元のexact J→N fiberに属する。`selectedSevenQuintuple_sevenObservedEq` は新商上の実際の七変量写像 `selectedRawCongruentSixQuadrupleObservation` の一致を証明する。一方、

```text
C₅(right(M)) = C₅(left(M)) + 2
```

である。この正の差が新7比較構成子すべてで保存されるため、以下が成立する。

1. `newClass(left(M)) ≠ newClass(right(M))`。
2. この二点を結ぶ真正Type値 `SelectedRawCongruentNineteen` は存在しない。
3. 実在するMが与えられたexact fiberで、七変量観測は非単射。
4. 七変量からすべての新商クラスを復元する左逆decoderは存在しない。
5. 五重鎖数だけを七変量から復元するdecoderも存在しない。
6. 指定端点Jの真正 `strict J` を使えば、J→J fiberの非単射性を構成できる。
7. 五重鎖数を加えた第8観測は、この具体的な二点を区別する。

反例が生じる構造的理由は、外側のreverseが、ひとつ下の祖先鎖数を上位の計数に加えることにある。v5.57のA/Bは三重鎖まで一致し、四重鎖で2だけ異なる。そのA/Bのどちらに追加のreverseを置くかによって、今回のL/Rは四重鎖まで一致し、五重鎖で2だけ異なる。一般の任意次数に関する定理は、今回の22宣言には含まれない。

空OSの「一致した観測から元証拠の同一性を無条件に推論しない」という対応は解釈・命名層であり、Leanが認証する数学的命題とは分けて扱う。


## 4. 初回CIと証明記法の修正履歴

初回source `23902ca7049fda656a1a8ab4cf1a418755e28dcc` の [CI #42572151782](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42572151782) は **completed FAILURE**。新規ファイル378行のうち、`selectedSevenQuintuple_suffixSignature` の12個の連言をまとめた `rfl` と、`selectedSevenQuintuple_sevenObservedEq` の七変量全体の `rfl` が、どちらも `whnf` の400万heartbeats上限に到達した。新moduleのbuildingは501秒、Lean終了コードは1だった。初回ログの6宣言には直接・依存を通じて `sorryAx` が現れたため、このsourceを認証・統合していない。

変更Leanファイル全文、元のv5.37 raw構成子とtrace、v5.43反転計数、v5.47隣接計数、v5.50新比較、v5.53以降の商観測、v5.57の既証明signatureを照合した。Lean公式の[命題的等式](https://lean-lang.org/doc/reference/latest/Basic-Propositions/Propositional-Equality/)と[書き換え・合同性の説明](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference)も参照した。公式最新文書を固定pinの認証結果の代用にはせず、実際の固定Lean CIで再検証した。

修正source `fa18260d5f6c110c27b64449154c39d3bbbdfecd` は、次の**3つの証明本文のみ**を変更した。

1. `suffixSignature`：v5.57の認証済み10個の計数等式を取り出し、外側のchain/reverseだけを開いて書き換える。新しい五重鎖数は旧A/Bについて0と1を個別に確定する。
2. `sevenObservedEq`：`Prod.ext` で七成分に分け、数値成分にsignatureを再利用する。traceは両側で同一の `trace M ++ (trace A ++ trace B)` へ開き、最外層flagは外側のchainから0になる。
3. `countDiff`：新signatureの4と6を再利用し、元のMの計数に対する加算の等式を証明する。

22宣言のstatement、元のA/Bと新しいL/RのType値、入力M、仮定、imports、比較構成子、`maxHeartbeats 4000000`、固定Lean/mathlibは保持。既存ファイルは変更せず、新規モジュールは518行となった。

## 5. 新規22宣言の実公理監査

修正後の固定Leanの実ログから、全宣言を個別に確認した。

| 宣言 | `#print axioms` の実結果 |
| --- | --- |
| `selectedContextEighteenReverseAncestorQuintupleCount` | なし |
| `selectedLocalNineteen_preservesReverseAncestorQuintuple` | なし |
| `selectedRawCongruent_preservesReverseAncestorQuintuple` | なし |
| `selectedNineteenReverseAncestorQuintupleOnQuotient` | なし |
| `selectedRawCongruentReverseAncestorQuintupleOnQuotient` | なし |
| `selectedRawCongruentReverseAncestorQuintuple_onClass` | なし |
| `selectedRawCongruentReverseAncestorQuintuple_factorsOld` | `Quot.sound` |
| `selectedSevenQuintupleSuffixLeft` | なし |
| `selectedSevenQuintupleSuffixRight` | なし |
| `selectedSevenQuintuple_suffixSignature` | なし |
| `selectedSevenQuintupleLeft` | なし |
| `selectedSevenQuintupleRight` | なし |
| `selectedSevenQuintuple_sevenObservedEq` | なし |
| `selectedSevenQuintuple_countDiff` | なし |
| `selectedSevenQuintuple_classDistinct` | `propext, Quot.sound` |
| `selectedSevenQuintuple_noComparison` | `propext, Quot.sound` |
| `selectedRawCongruentSeven_notInjective` | `propext, Quot.sound` |
| `selectedRawCongruentSeven_noDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentSeven_noQuintupleDecoder` | `propext, Quot.sound` |
| `selectedRawCongruentSeven_endomorphismNotInjective` | `propext, Quot.sound` |
| `selectedRawCongruentSevenQuintupleObservation` | なし |
| `selectedRawCongruentEight_quintupleDistinguished` | `propext, Quot.sound` |

22件すべてを確認し、公理不要14宣言、標準 `propext` / `Quot.sound` のみ8宣言。新しい `sorryAx` は0、変更Lean error/warningは0/0。既存の全成果物まで同じ公理集合だけを使うとは主張しない。


## 6. 未認証領域と次段

**NO_DATA**：五重鎖数を加えた八変量による新商全体の分類・完全復元、任意の異17D端点J,Nのfiberの非空性、旧I6全成分の新商への降下、元16D fiberを超えるwhiskering比較、20D higher coherence/gluing、独立WORLDや物理C60との数学的同一視、制度的・実行上の権限。

次段 **Qi v5.59** の研究候補は、今回の「反転を付ける位置を移して差を一段上へ送る」構成を一般の祖先鎖次数へ拡張し、有限個の祖先鎖観測で残る障害を調べること。これは今回の形式証明から着想した研究方針であり、任意次数の定理や八変量の新しい反例が既に認証されたとは主張しない。

元sourceと既存のType値証拠、公開root107、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、保護PR #1558 Draft/OPEN/未マージを保持。append-only／tighten-only／overwrite-forbidden／same-root。正式記録・README・ROADMAPのPRはdocs-onlyで、Strict Leanを再実行しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
