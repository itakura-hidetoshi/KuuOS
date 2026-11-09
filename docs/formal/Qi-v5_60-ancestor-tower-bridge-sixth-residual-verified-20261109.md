# Qi v5.60 — 旧五計数と自然数次数塔の同一性・真正六重鎖残余のLean4形式証明記録

正式記録日：2026-11-09 JST

## 1. 正本・認証の強さと来歴

- Repository: `itakura-hidetoshi/KuuOS`、canonical branch: `main`。継承元Qi v5.59正本 `43a4f6b77e2398ae50fe530267dba48bd1beea52`、tree `61854d513a57b0aa252d731d16152c5e451e06a0`。
- [定理PR #3410](https://github.com/itakura-hidetoshi/KuuOS/pull/3410) **MERGED**。新規Leanモジュール `formal/KUOS/Architecture/QiWuxingGK5CHP77AncestorTowerBridgeSixthWitnessV5_60.lean`、**401行追加・削除0**。変更前の既存Lean定義はすべて保持。
- 定理認証済みsource HEAD: `1a1e44a0424c0acaa630fc5e9ab375408c8c0293`、squash統合 `59cb416c621b46793728cd62b8c773b0e3e014dd`、source/test-merge/squash tree `1be1c70ba83f95b9bb4539ee59890d7cc8f5b1a6`（完全一致）。
- [定理exact-source CI #42582641821](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42582641821) **completed SUCCESS**：Scoped Strict Lean **9,112/9,112**、Governance **5/5**、変更Lean error/warning **0/0**、source-SHAに対するexact-head受領書 **2件SUCCESS**。
- [公開import PR #3411](https://github.com/itakura-hidetoshi/KuuOS/pull/3411) **MERGED**。`formal/KuuOSFormal.lean`にimport **1行追加・削除0**。source `c21b37341187b2f626d8cf30af5c5ae556095928`、squash `c019287f13db1d6a6456ee174944ea45500318a4`、source/test-merge/squash tree `072f030cfb5791a8f49a78bb34b28fb5f31f562a`。
- [公開exact-source CI #42583422934](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42583422934) **completed SUCCESS**：全公開KuuOSFormal Strict Lean **10,373/10,373**、Governance **30/30**、変更Lean error/warning **0/0**、exact-head受領書 **2件SUCCESS**。関連workflowは8件SUCCESS・1件SKIPPED（Independent Kuu Foundation）。
- 本文書・README・ROADMAPのdocs-only PR自身の検証結果や統合後mainは、当該PRの実際の終了受領書で別に判定する。未取得の未来の結果をここでSUCCESSと仮定しない。

## 2. 五つの旧計数とC1〜C5の真正raw全証拠での等式

前段Qi v5.59の `selectedAncestorTowerCount l r n M` の `C₀(M)=1` は形式的seedであり、反転回数ではない。**次の五本は今回、全て元18Dの真の依存型証拠Mを用いてLean4で証明**した。

| 現行の塔 | 既存のcertified定義 | 新規Lean定理 |
|---|---|---|
| C₁(M) | `selectedContextEighteenReverseCount` | `selectedAncestorTower_eqReverseCount` |
| C₂(M) | `selectedContextEighteenReverseAncestryCount` | `selectedAncestorTower_eqAncestryCount` |
| C₃(M) | `selectedContextEighteenReverseAncestorTripleCount` | `selectedAncestorTower_eqAncestorTripleCount` |
| C₄(M) | `selectedContextEighteenReverseAncestorQuadrupleCount` | `selectedAncestorTower_eqAncestorQuadrupleCount` |
| C₅(M) | `selectedContextEighteenReverseAncestorQuintupleCount` | `selectedAncestorTower_eqAncestorQuintupleCount` |

各等式の帰納対象は、真正 `SelectedContextualEighteen` の **inherited／whiskerLeft／whiskerRight／strict／reverse／chain** の6構成子すべて。新しいMを数値データへ置換して同じだと命名したのではない。二つの文脈whiskeringで内部のframed／16D添字が変わる事実を含めた型付き帰納法である。旧18D／19D sourceと新v5.50七構成子比較は不変。

`selectedAncestorTower_v558NewQuotientBridge` と `selectedAncestorTower_v558OldQuotientBridge` で、それぞれ新7構成子商と元selected19商について独立した `Quotient.inductionOn` を通じて、C₅商観測とv5.58の五重鎖商観測が一致することを形式証明した。二つの商を勝手に同一視していない。

## 3. 五重鎖4対6を接続した真正証拠対

v5.58で証明済みの、真正固定17D端点 N を持つN→N raw suffix `A=selectedSevenQuintupleSuffixLeft l r N` と `B=selectedSevenQuintupleSuffixRight l r N` を元のType値のまま保持する。

```text
       C₁   C₂   C₃   C₄   C₅
A      15   31   32   18    4
B      15   31   32   18    6
```

`selectedSevenQuintuple_towerSuffixSignature` はこの表を新塔で実際に証明した。`selectedSevenQuintuple_towerFirstGap` は `∀ k<5, Cₖ(A)=Cₖ(B)` と `C₅(A)≠C₅(B)` の両方をcertifyする。各証拠は実在する元18D構成子から作成されており、商クラス値を直接捏造していない。

```text
L₆ := chain (reverse A) B
R₆ := chain A (reverse B)
```

`selectedEightTowerShiftLeft` と `selectedEightTowerShiftRight` は真正N→N型を持つ。この型付き対について、

1. `selectedEightTowerShift_residualGate`：全ての `k≤5` で `Cₖ(L₆)=Cₖ(R₆)`、かつ両者の真正 `SelectedRawCongruentNineteen` Type値比較の `Nonempty` は偽。
2. `selectedAncestorShift_sixthGapIfFifth`：任意の実在するA,Bに `C₅(B)=C₅(A)+2` が与えられる条件で、`C₆(shiftRight)=C₆(shiftLeft)+2` を証明する、抽象的だが真正型付きの算術輸送。
3. `selectedEightTowerShift_sixthGap`：元の真正v5.58証拠対に適用して **`C₆(R₆)=C₆(L₆)+2`** を確定。
4. `selectedEightTowerFiberLeft/Right`：**実際に供給された**`M:J→N`の右にL₆/R₆を連結し、元のJ→N exact fiberを維持する。`selectedEightTowerFiber_sixthGap` でC₆の差+2を保存し、`selectedEightTowerFiber_classDistinct` で独立新商クラスの不一致を証明する。

**降下の範囲**：C₀〜C₅の一致からC₆を含む完全分類は導けない。今回の証明は、真正A/Bを持つ固定Nおよび明示的にMが供給されたJ→N fiberで成立する。異端点の任意fiberが非空という主張にはならない。

## 4. 初回Lean失敗と構造修正

初回source HEAD `eeb6305a3d1c5737aa05eb7f446b40dfcc1e302e`、[初回CI #42581448347](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42581448347) **FAILURE**。初稿378行・17宣言のline305 `change` で、巨大な具体的な元18D suffixの`C₆`をwhnfまで展開し、固定の4,000,000 heartbeatsの決定的上限を超えた。残りのsourceに対する別種の構文エラーはログで確認されなかった。

修正ではmaxHeartbeatsを増やさず、**具体的suffixを展開する直前に任意の真正A/Bを対象とする `selectedAncestorShift_sixthGapIfFifth` を独立に証明**。加法式と`omega`で次数の差を処理し、具体値は既存signatureの証明から代入した。元証拠のconstructor、前提、旧新比較、五同値定理、従来の証明書、最終結論、Lean/mathlib pinは不変。修正後401行・18宣言は全て型検査成功。失敗した初稿は認証・統合していない。

## 5. 全18宣言の新規実公理監査

`#print axioms` を18宣言すべてに付けてexact-sourceと公開集約で実際のログを確認した。

- **公理不要：12宣言**。
- **標準公理のみ：6宣言**。出現するのは`propext`と`Quot.sound`だけ。
- **新規sorryAx：なし**。
- **変更Lean error/warning：0/0**。

上記は今回追加した宣言に対する監査であり、過去の全Lean宣言を追加検査したことの代用にはしない。変更file全文・import関係・真の依存型と元source署名・固定Leanログ・source/test-merge/squash treeを照合した。

## 6. NO_DATAと次段Qi v5.61

認証済みは**塔C₁〜C₅と旧計数の一致、五重鎖4対6の真正証拠対、shift後のC₀〜C₅一致とC₆差2、真正Type値比較の不存在、任意に供給されたMでの商クラス分離**である。

**NO_DATA（依然未認証）**：shift後L₆/R₆で既存の全八変量 `(ordered trace, raw reverse total, adjacent reverse count, top reverse flag, ancestor pair, triple, quadruple, quintuple)` が等しいという完全な共同観測のLean4証明。それに依拠する「八変量観測の非単射性」「九番目のC₆を加えた完全復元可能性／不可能性」の主張。一般の `∀n∃` witness、任意のJ→N fiber非空性、異fiber whiskering、20D gluing、authority。

**次段Qi v5.61（研究候補）**：同じ真正L₆/R₆に対するTrace、adjacent reverse、top reverse flagの各保存を独立に証明し、既存C₁〜C₅の証明と結合。八変量が真に一致すれば、元v5.58八成分商観測の非単射性と真正九番目C₆による明示的分離を形式証明する。未認証の段階で「八変量の反例を証明した」と記載しない。

Qi v5.51で既証明の元LeftNestedCount／19D正規代表の非降下障害も保持し、旧I6全成分を新商の観測に無条件昇格させない。

公開root107、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、保護PR #1558 Draft/OPEN/未マージを維持。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
