# Qi v5.83 — 真正継承旧18D証拠・左whiskeringを保護した局所忠実性（Lean4形式証明・公理監査）

2026年11月10日 JST。正本は`itakura-hidetoshi/KuuOS`、branch `main`。本記録は元の依存`SelectedContextualEighteen` Type、別々に定義された旧5構成子`SelectedLocalNineteen`と新7構成子`SelectedRawCongruentNineteen`、それぞれの真正商について、**指定された3枝の限定部分presentationのみ**を記録する。「空」「縁起」との対応は命名・解釈の層であり、Leanが哲学的同一性を証明した意味ではない。

## 1．正式統合された機械的成果物・来歴

- 研究基礎：Qi v5.82定理・公開・正式記録がMERGEDのmain `b547e993154f41a75d34100e1ac1667134cf8134`。
- [Lean定理PR #3479](https://github.com/itakura-hidetoshi/KuuOS/pull/3479) **MERGED**。新規`formal/KUOS/Architecture/QiWuxingGK5CHP77GuardedInheritedWhiskerFragmentV5_83.lean`、382行、18宣言、各宣言の独立した18件の`#print axioms`。既存Leanの変更・削除なし。
- 定理exact-source `659c2165f3e1d187dbfd36eadae8a0f84b2a4444`／test-merge `2d97ae382fdf90c0966152fa3e9e4250b1f428dc`／squash `014e65889df8ef0e0d261fcb540d37d258e3d4e8`。3者Git treeは`cfea0643c895e1ee786eab06ef5f87096ed379b5`に一致。
- [公開import PR #3480](https://github.com/itakura-hidetoshi/KuuOS/pull/3480) **MERGED**。`formal/KuuOSFormal.lean`に`import KUOS.Architecture.QiWuxingGK5CHP77GuardedInheritedWhiskerFragmentV5_83`を1行追加のみ。公開root107と従前のimportは不変更。
- 公開exact-source `9a53fdf6d8c0353b805cb645d2ca7e8c1e8927e9`／test-merge `f18c606d9468ccb51642455a3475a405a15a39c7`／squash `5c090513b4f96ca07294169223251e29f9604cd2`。3者Git tree`6d0eeec1629498175076fe90071649704a4167a7`一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定。validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 2．明示した供給条件と元の型付き3枝

真に与えられた`before : SevenRewrite W l r b c`、`F G : ContextFrameEleven W l r c d`、真正17D端点`N`を固定。実際の左whiskered端点を`N' = whiskerLeft before F G N`とする。さらに、**別途、真正の** `M : SelectedLocalEighteen W l r N' N'` が与えられた場合に限る。これらの入力の任意居住性は仮定も証明もしない。

新しい`SelectedV583GuardedFragment`には次の3種のみがある。

1. `pure A`：v5.82の自由strict/reverse/chain木`A`を元`SelectedContextualEighteen W l r N' N'`へ埋め込む。
2. `inheritedGuard`：元の真正旧18D値`M`を保った`reverse (inherited M)`。
3. `leftGuard`：真正`reverse (whiskerLeft before F G (strict N))`。

ここに未保護の任意`inherited`や任意`whiskerLeft`を自由構成子として付加したわけではない。両anchorは単一の元証拠と単一の左whiskering文脈に固定されており、右whiskeringや別fiberの無条件拡張もしていない。

## 3．独立観測、元18D・旧新19Dへの反映

既存v5.81の`selectedContextEighteenWhiskerPlacement`を**元の真正18D Type値で**直接評価すると、3枝は順に

```text
pure A          -> selectedPureStrictReverseRawValue A
inheritedGuard  -> reversed (source (selectedLocalEighteenInnerBracket M))
leftGuard       -> reversed (left strict)
```

となる。`selectedV583RawValue_injective`と`selectedV583Left_observed`を証明し、この限定枝の埋め込みが元の18D Type値において単射であることを示した。source/left/strictは区別して保持し、元旧18Dの内部証拠を消去・置換しない。

元旧5構成子商と別の新7構成子商**それぞれ**について、3枝の任意`A B`に対し`[embed A] = [embed B] ↔ A = B`。旧`SelectedLocalNineteen`と新`SelectedRawCongruentNineteen`の`Nonempty`比較も個別に`A = B`と同値であり、したがってこの像に限り比較可能性の条件が一致する。両比較Typeそのものの大域的同一視ではない。

`SelectedFullV581QuotientObservationValue`（v5.80の全座標・**2本の全Nat→Nat無限塔**を保つ直積とv5.81の新配置木）も、この同じ限定3枝の真正新商クラス上では`FullV581([embed A]) = FullV581([embed B]) ↔ A=B`を満たす。全18D商に対する単射性へ昇格させない。

## 4．保護しない場合の明示的obstruction

旧selected19が最初から保持する元の単位生成元`SelectedLocalNineteen.unitPrepend M`により、

```text
raw chain (strict N') (inherited M) != raw (inherited M)
old19 class(chain (strict N') (inherited M)) = old19 class(inherited M)
new19 class(chain (strict N') (inherited M)) = new19 class(inherited M)
```

が真正の依存型で証明された。前者は`selectedV583Left_unguardedRawDistinct`、後二者は`selectedV583Left_unguardedUnitOldNew`である。これはソース葉を保護せず自由に足した場合の忠実性の障害であり、既存の単位律を弱めたり、誤った自由分類を断定したりしないための保存された反例である。

## 5．Exact-source Strict Lean・実公理監査

- [定理CI #42768993880](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42768993880) **terminal SUCCESS**。Scoped Strict Lean **9,135/9,135**、選択Governance各ジョブSUCCESS。新規Leanは初回から型検査成功、修正を要するLeanエラーなし。
- [公開CI #42769590011](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42769590011) **terminal SUCCESS**。`KuuOSFormal` Strict Lean **10,396/10,396**、Governance選択**30/30 SUCCESS**。従前の公開importを保持。
- 新規**18/18宣言**の`#print axioms`実出力を両ログで照合：**公理不要4**、**標準`propext`／`Quot.sound`のみ14**。この範囲では新規`sorryAx`なし、変更Lean error／warning **0／0**。他のmathlib宣言まで公理不要という大域主張はしない。
- 定理・公開それぞれのsource／test-merge／squash Git treeをGitHubのGit-dataから独立照合し、一致を確認。CI成功の範囲を超える数学的命題や行為権限は生じない。

## 6．未認証と次段候補

任意の旧18D継承値`M`の居住性、別の`M`に対する識別可能性、任意のwhiskering文脈、右whiskering、自由なsource/reversal/chainの全閉包での忠実性、旧新Type19D比較の大域同値、異端点fiberの一般的居住性、全商分類、WORLD横断降下、20D gluing、制度的・実行権限は**未認証（NO_DATA）**。

**次段Qi v5.84候補**：固定old18D証拠の別sourceに変えた際の来歴識別条件、右whiskeringの正しい端点貼合とguarded closureの限界を、元の単位規則・obstructionを残したまま調べる。Preference ⇏ Descent ⇏ Authority。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
