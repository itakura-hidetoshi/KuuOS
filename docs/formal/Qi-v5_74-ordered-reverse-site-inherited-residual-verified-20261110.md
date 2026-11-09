# Qi v5.74 — 旧18D内部構文まで一致しても残るraw反転位置の継承証拠順序（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は**真正の元18D依存Type値**と、元の旧5構成子selected19比較・独立した新7構成子raw合同性比較による同一exact fiber上の真正商である。「空」「縁起」の命名・哲学的対応は解釈の層であり、Lean4によって証明されたものではない。

## 唯一の正本・コード・CI認証来歴

- Repository `itakura-hidetoshi/KuuOS`、canonical `main`。研究開始時のQi v5.73正式統合main HEAD `cd92a67918e4f1471cd559637338567f537984c8` を基礎にする。
- [定理PR #3452](https://github.com/itakura-hidetoshi/KuuOS/pull/3452) **MERGED**。追加したLeanソースは `formal/KUOS/Architecture/QiWuxingGK5CHP77ReverseSiteInheritedOrderResidualV5_74.lean` の**新規1ファイル、460行追加・削除0**。既存Leanファイル、元の証拠Type、旧新19D比較、固定pin・root107は不変。
- 定理認証source `d29c6b2ebd9e688b0e6cb25189a57adec1227d63`、test-merge `7454d497b7d515807308709228c2602e3a9544c8`、squash `ccae1e95c338119c9801c5f144322368056d7d86` のGit treeは**すべて `60f835f657741181ce9b7b90e4b2171d7063cf42` で一致**した。
- [公開import PR #3453](https://github.com/itakura-hidetoshi/KuuOS/pull/3453) **MERGED**。`formal/KuuOSFormal.lean` にv5.74 importを**1行だけ追加**、既存import削除0、公開root107維持。
- 公開認証source `0afdd1096cbbf4b84290e993abc496e8579658ff`、test-merge `c550741b1d4887e70bd7a95b82370df8389c9aa6`、squash `d5bd49df54587a79ce14863c263ad45931c456e1` のGit treeは**すべて `d4bcc05d64e61baa880f658fdff757cfd777f461` で一致**。
- 固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root **107**。保護validation-only [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。

## 新しい独立観測と保存性

真正 `M : SelectedContextualEighteen W l r J N` のraw構成子に構造再帰し、各 `reverse A` の**直下の元証拠 `A` に存在する真正 `inherited(old18)` 葉の個数**を記録する。新定義は `selectedContextEighteenReverseSiteInheritedCounts`。その動作は：

```text
inherited old18    ↦ []
strict N           ↦ []
whiskerLeft/Right A↦ SiteList(A)
reverse A          ↦ InheritedLeafCount(A) :: SiteList(A)
chain A B          ↦ SiteList(A) ++ SiteList(B)
```

単に反転総数や継承葉総数を読むのではなく、**raw反転の位置ごとの条件付き継承数を順序付きで保存**する。新しい値は旧18D本体の代用や元Type値の同一視ではない。

- 元の `SelectedLocalNineteen` **5構成子すべて**で保存を形式証明した。特に旧 `unitPrepend`・`unitAppend` はraw strictの挿入・削除のみで反転位置列に影響しない。
- 独立 `SelectedRawCongruentNineteen` **7構成子すべて**で保存を形式証明。新 `rawReverse` に対しては**既存v5.71の継承葉数保存**と再帰的な反転位置列の保存を両方使用し、元の型付き比較を忠実に追った。左右の `rawChainRight`／`rawChainLeft` も順序付きリスト連結と互換。
- **旧商・新商に独立して `Quotient.lift`** で降下し、元の旧→新projectionへの因子化を証明。比較規則の上書きや追加公理は行っていない。

## 真正同一fiberでの全旧観測一致と新しい障害

任意の真正17D端点 `N` について、元 `SelectedContextualEighteen` の厳密な依存構成子だけで以下を作る。

```text
R = reverse (strict N)
I = reverse (inherited (SelectedLocalEighteen.strict N))
A = chain R I
B = chain I R
```

両者は真正 `N→N` の元raw18D Type値である。既存**九観測、全次数の祖先塔 `Nat→Nat`、全次数の直接連続反転数塔 `Nat→Nat`、完全ordered raw反転ラン列、単位簡約したraw18D非結合括弧構造、inherited葉数（両方1）、順序付き旧18D根タグ列（両方 `[strict]`）、さらに**v5.73で加えた完全ordered内部旧18D非結合構文リスト（両方 `[oldStrict]`）**まで一致する。

新たな反転位置列だけは `S(A)=[0,1]`、`S(B)=[1,0]` で異なる。この列は真正新商へ降下するため、**実際の新7構成子商クラスが相異なり、両者の真正Type値新19D比較も存在しない**。単なるraw構文の文字列不一致を商不一致と取り違えていない。

さらに、元の真正 `M:J→N` が**実際に供給された場合だけ**、`chain M A` と `chain M B` を**同じexact dependent fiber `J→N`** に構成する。全従来観測は一致し、新反転位置列の相違は同じprefixのList消去則によって残る。よって拡張前のv5.73結合商観測はそのfiberで非単射、反転位置列のdecoderおよび商クラス全体のdecoderは存在しない。指定 `J→J` に対しては真正 `strict J` を使った具体例も得た。勝手に異端点fiberを非空と仮定していない。

## Lean4形式検証・公理実監査

- [定理exact-source CI #42717175261](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42717175261)：**completed SUCCESS**。Scoped Strict Lean **9,126/9,126**、Governance **5/5 SUCCESS**、変更Lean error／warning **0/0**。
- [公開exact-source CI #42718023314](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42718023314)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,387/10,387**、Governance **30/30 SUCCESS**、変更Lean error／warning **0/0**。
- **新規29宣言すべて**に `#print axioms` を付けて実ログを照合。**19宣言は公理不要、10宣言は標準 `Quot.sound` または `propext` のみ**。新規 `sorryAx` なし。実CIの固定依存閉包とGit treeの一致を機械的検証の範囲とする。

## 論理的な境界・次段

新しい列を追加しても、全商クラスの一般分類・完全復元は証明していない。今回の反例対は**新反転位置列そのもので区別される**ため、その新観測を加えた場合の非単射性の証明に流用できない。

次段Qi v5.75の研究候補は、この反転位置列まで同時観測してもなお残るsource来歴の独立不変量、または限定した構文／fiberにおける条件付き識別性である。現時点ではいずれも**未認証（NO_DATA）**。

任意異端点fiber非空性、旧18D依存Type値全体の復元、20D gluing、全WORLD貼合、制度的実行権限も未認証。append-only／tighten-only／overwrite-forbidden／same-root。元18D Type値と独立旧新19D比較、公開root107、固定Lean/mathlib、保護#1558 Draft／OPEN／未マージを維持。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
