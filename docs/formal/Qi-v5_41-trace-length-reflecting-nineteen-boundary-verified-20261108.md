# Qi v5.41 — 非定数・anchored 19D境界transportと外側履歴長の反映

2026年11月8日 JST。Canonical: `itakura-hidetoshi/KuuOS`、branch `main`。
前段Qi v5.40の定理PR #3349・公開PR #3350・正式記録PR #3351はMERGED。今回のv5.41は定理と公開集約を独立PRで認証した後に、本文書をdocs-onlyで記録する。元F55/P77/GK5CG、生6D〜19D Type値証拠、既存selected presentationと履歴、公開root 107、Lean/mathlib pin、保護Draft PR #1558を変更しない。append-only／tighten-only／overwrite-forbidden／same-root。

## 1. GitHub MCPによる正本・検証記録

| 対象 | 認証結果 |
|---|---|
| 新規定理 | [PR #3352](https://github.com/itakura-hidetoshi/KuuOS/pull/3352) MERGED |
| 定理source HEAD | `1979dd658a515a272c6b91b96cb39946e67cf935` |
| 定理test-merge HEAD | `479d6c5ad1487881417cf38ee94ea66cd642f497` |
| 定理squash main | `e2a1d29d06c895d4ac3c4eb76a9062a014cd6e0f` |
| 定理source／test-merge／squash Git tree | `f5cdf791ab419dcd69395683950a9eb341f63436` 完全一致 |
| 定理exact-source CI | [#42477185958](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42477185958) SUCCESS |
| Scoped Strict Lean | 9,093 / 9,093 SUCCESS |
| 定理Governance | 5 / 5 SUCCESS |
| 新規宣言の公理監査 | 15 / 15（公理不要3、標準公理のみ12） |
| `sorryAx`／変更Lean error／warning | なし／0／0 |
| 定理差分 | 新規Lean1ファイル334行、既存ファイル削除0 |
| 公開import | [PR #3353](https://github.com/itakura-hidetoshi/KuuOS/pull/3353) MERGED |
| 公開source HEAD | `dc3a836eb371508601e4a585932512ba16b09193` |
| 公開test-merge HEAD | `e6133c456e43651161a4eadef533ce8e33cdaa1c` |
| 公開squash main | `640b47193273dc333caa2d5794c1dafbc0c30d73` |
| 公開source／test-merge／squash Git tree | `c4e9223303d3866f26abc4b1a9060b46391b9d78` 完全一致 |
| 公開exact-source CI | [#42478757198](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42478757198) SUCCESS |
| 公開KuuOSFormal全体Strict Lean | 10,354 / 10,354 SUCCESS |
| 公開Governance | 30 / 30 SUCCESS |
| 公開差分 | `formal/KuuOSFormal.lean` にimport1行追加、削除0 |
| 固定Lean | `v4.30.0-rc2` |
| mathlib pin | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Lean4形式証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TraceLengthReflectingNineteenBoundaryV5_41.lean)。

## 2. 元の真正RL 18D証拠から作る非定数の証拠列

真正元18D証拠 `M` の左右二重輸送を、それぞれ異なる依存17D端点fiber内の
`X = selectedEighteenLeftAfterRight(M)`（LR）、
`R = selectedEighteenRightAfterLeft(M)`（RL）
として保存する。元の証拠値を同一視せず、RL fiberで旧`chain`・`reverse`構成子だけによって

```text
P_R(0)   = R
P_R(n+1) = chain (chain P_R(n) (reverse R)) R
```

を定義する（`selectedMixedRightTracePower`）。
`selectedMixedRightTracePower_length`が
`len(Trace(P_R(n))) = (2*n+1) * len(Trace(R))`
をLean4で証明する。RL真正二重輸送の履歴長は少なくとも2（`selectedMixedRightSeed_tracePositive`）なので、`n`の異なる証拠列は少なくとも履歴長で識別できる。これは元の異fiber証拠Eqではない。

## 3. 長さの単射符号化と実際の19D境界

指定LR証拠 `X` の履歴長を `base` として、
`selectedMixedLengthCode base n = if n = base then 0 else n + 1`
を定義し、`selectedMixedLengthCode_injective`で自然数上の単射性を証明する。

`selectedMixedLengthRawTransport M X'`は、LR source証拠 `X'` の外側履歴の**長さ**を符号化し、RLの真正証拠列 `P_R(code(length(Trace(X'))))`へ送る。指定LR証拠 `X` は指数0に送られるため、**像は元の真正RL証拠 `R` に一致する**（`selectedMixedLengthRawTransport_chosen`）。

`selectedMixedLengthBoundary`はv5.39の`SelectedMixedNineteenBoundary`の実際のinhabitantである。source側の真正`SelectedLocalNineteen`比較は全ordered traceを保存するため、sourceの長さ符号が一致し、像のraw値が一致する。これにより`localTransport`を**輸送先の真正`SelectedLocalNineteen.strict` Type値証拠**で構成できる。追加公理や無条件20D交換は使わない。

`selectedMixedLengthAnchored`は指定LR像とRL実証拠の間の真正19D比較も構成する。この局所的anchored比較から指定19D商クラス方程式と指定点のswap観測一致が得られる。ただし全sourceにわたるswap観測の自然性とは別である。

## 4. 厳密に証明できた反映と、未証明の忠実性

`selectedMixedLengthRaw_reflectTraceLength`：
輸送先で二つの像が真正19D比較を持てば、両sourceの**外側履歴長**は一致する。証明はRL証拠列の `(2*n+1)*len(Trace(R))`、正のRL種長、自然数上の単射符号化に依拠する。

`selectedMixedLengthDescend_reflectTraceLength`は、この反映を本物の`Quotient.lift`で作った異なる19D商間の写像へ降下させる。
`selectedMixedLengthDescend_separatesByTraceLength`は、sourceの長さが異なる任意の二商クラスを像で同一視できないことを証明する。

特に、指定LR真正証拠 `X` と元の`chain (chain X (reverse X)) X` は同一LR fiber内にあり、後者の外側履歴長は3倍。したがって
`selectedMixedLengthDescend_chosenVsRoundtrip`が、**実際に存在する二クラスの像の非等号**を証明する。v5.40の定数境界とは異なり、この境界は19D商上で非定数である。

**未認証（NO_DATA／obstruction）：** 同じ履歴長で内容が異なる元19D比較をすべて反映する`SelectedMixedNineteenFaithfulBoundary.reflectLocal`の具体的inhabitant、raw18D全証拠の単射、完全ordered trace全体の反映、全域のswap自然性、元の異依存fiber高次交換／20D gluing。長さの反映だけからこれらへ大域化しない。

## 5. CI失敗・修正の構造理由

最初の定理CI #42476709502では、sectionの暗黙の従属引数を含む再帰定義を明示的に再呼出しした際に、Lean4が`l : W`をRL raw18D証拠引数として扱う型不一致が発生した。これが長さ補題の基底・帰納ケースのdefinitional equalityに波及し、失敗した宣言の`sorryAx`診断も生じた。

旧sourceの定義や仮定を変えず、`selectedMixedRightTracePower`を同じ真正`chain/reverse/chain`証拠列を作る`Nat.rec`の式へ正規化した。基底ケースは`simp [selectedMixedRightTracePower]`で自然数の単位積を明示的に整理した。途中CI #42477098068はHEAD更新でキャンセルされ、認証根拠に採用しない。最新HEAD `1979dd65...`のCI #42477185958で全9,093ジョブ成功し、15宣言で`sorryAx`なしを確認した。公式Pinned Lean配布のHTTP 504があっても検証条件を弱めない。

## 6. 権威境界と次段

**Lean4で証明済み：** 非定数のanchored LR→RL境界transportの実在、元の真正19D Type値比較の保存、19D商降下、指定点でのswap観測一致、全商クラスに対する**履歴長**の反映、指定LR証拠と3倍roundtripの像の分離。

**未認証：** 同一長さ内の証拠区別をすべて保存する忠実性、全域swap自然性、元の異fiber20D交換セル。証明可能性の余地と既証明の不可能性を混同せず、obstructionを保持する。

**次段Qi v5.42：** この長さ符号化が潰す可能性のある同長異履歴のfiberを調べ、元19D比較反映を実際に構成できる条件と、全域swap観測の互換性を別々に探る。証明できない部分はNO_DATAのまま残す。

本PRはdocs-only正式記録・README・ROADMAP同期であり、Lean/import/workflow/依存pinは変更しない。docs-only GovernanceとCore AutonomyのみをCI確認し、Strict Leanを不要に起動しない。
