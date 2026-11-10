# Qi v5.89 — 元の真正旧18D依存型におけるunit-free条件の完全特徴付けと局所忠実性（Lean4形式証明）

2026年11月11日 JST。canonical正本：`itakura-hidetoshi/KuuOS` の `main`。対象は真正旧18D証拠型 `SelectedLocalEighteen` と、真正18Dへの `SelectedContextualEighteen.inherited`、独立した旧5構成子・新7構成子の選択19D商である。「空・縁起・二諦・中道」との対応は解釈／命名の層であり、Lean4が宗教哲学上の主張を証明したという意味ではない。

## 1．正本・独立CI・統合来歴

- **定理PR [#3497](https://github.com/itakura-hidetoshi/KuuOS/pull/3497) MERGED**。新規ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77OriginalUnitFreeExhaustionV5_89.lean`（GitHub差分314行追加、既存ファイルの編集・削除0）。
- 定理base `d8c448b04a3af38cf6e57adfdd3e20e4d139ac9a`（v5.88三段階統合後）。初回source `9cccdae52835ad62314a0b32582e0aa9338b1cfe`、修正・**認証source `93208030a6d33d8ce0909920d2b5e2b927cdf76c`**、統合後main `42f9d116408c56d3e75d5292d3eac6ee70b3c45e`。
- 定理のGit treeは source／test-merge／squash mainの3者で **`c3b0d7ceefbc58efae9ec6dd90a35e5fd92cb333` に一致**。GitHub Git commit objectで別個に再観測。
- **定理Exact-source CI [#42879791580](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42879791580)：terminal SUCCESS**。Scoped Strict Lean **9,141/9,141**、独立Kuu Core・Governance SUCCESS。固定 `lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77OriginalUnitFreeExhaustionV5_89`。
- **公開import PR [#3498](https://github.com/itakura-hidetoshi/KuuOS/pull/3498) MERGED**。`formal/KuuOSFormal.lean`に import **1行のみ**追加。公開source `198c8f09feb2179de3f75c2570b4092e1c4ac7b2`、統合後main `5d44145ad9e106017513b9642f65c50df82a6487`、source／test-merge／squash tree **`5a0d737a40c5f5cb8bfb30a3057ce8f31006949c`一致**。
- **公開CI [#42881124191](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42881124191)：terminal SUCCESS**。公開KuuOSFormal Strict Leanの依存閉包 **10,402件**、Governanceの選択分割チェックもSUCCESS。
- 定理・公開双方の実際の `#print axioms` **14/14**：**公理不要6件／残り8件は標準 `propext`・`Quot.sound` のみ**。新規 `sorryAx` はなく、対象変更Lean error／warningは0／0。
- Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**、公開root107維持。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 2．元の真正依存型に直接定義したunit-free条件

前段v5.88の `SelectedV588UnitFreeTerm` は補助構文であり、元旧18Dの「全zero-unit証拠がその像にある」とは未証明だった。今回は任意の元の依存証拠
`M : SelectedLocalEighteen W l r J N`
について、元の5構成子を**そのまま再帰**し、独立の `selectedV589OriginalUnitCount l r M : Nat` を定義した。

- `strict`では0。
- 実際の `unitLeft`／`unitRight` では各1。
- `reverse`は元の個数を保存。
- `chain`は内部2証拠の個数を加算し、**非結合の括弧構造を消さない**。

`selectedV589OriginalIsUnitFree l r M := selectedV589OriginalUnitCount l r M = 0` は**元の型付き証拠そのものに付した条件**であり、埋込像に属することを定義で仮定していない。

`selectedV589OriginalUnitCount_observed` は、この元証拠のunit個数と、v5.73の既存 `selectedLocalEighteenInnerBracket` に対するv5.88 `selectedV588InnerUnitCount` が一致することを元の5構成子について帰納的に証明する。これは観測の整合性であり、raw証拠と観測値の等号ではない。

## 3．真正raw17D端点を保持した全域性（新規中核定理）

`selectedV589OriginalFree_exhausted` は、任意の元証拠 `M : SelectedLocalEighteen W l r J N` に対して

```text
selectedV589OriginalIsUnitFree l r M
  → ∃ (h : J = N) (t : SelectedV588UnitFreeTerm),
      M = selectedV589CastFree l r h t
```

を証明した。`h : J=N` は真正依存添字の等号証明であって、異なる17D端点を勝手に同一視する仮定ではない。`reverse`と`chain`はその等号証拠で正当に輸送し、単位構成子の枝は元証拠unitCount=0に矛盾する。

従って**固定した同じ真正raw17D端点 `N→N`** では、元の任意の証拠 `M : SelectedLocalEighteen W l r N N` に対し、次の**必要十分条件**を証明：

```text
selectedV589OriginalIsUnitFree l r M
  ↔ ∃ t : SelectedV588UnitFreeTerm,
      M = selectedV588UnitFreeRawEmbed l r N t
```

これは `selectedV589OriginalLoopFree_iff_image`。v5.88の「明示的に構成した像上の忠実性」を、**元の真正旧18D型のzero-unit部分全体**へ拡張できる全域性の認証である。元旧18D全体への無条件拡張ではない。

## 4．拡張できる忠実性と、できない大域化

上の完全性から、同じN→N fiberの**両方が元のunit-free条件を満たす**真正旧18D証拠M,Lについて、次をそれぞれLeanで証明した。

1. `selectedV589OriginalLoopBracketFaithful`：元の内部括弧観測 `bracket(M)=bracket(L) ↔ M=L`。
2. `selectedV589OriginalLoopOldClassFaithful`：真正旧5生成元の独立selected19 quotientで `classOld(inherited M)=classOld(inherited L) ↔ M=L`。
3. `selectedV589OriginalLoopNewClassFaithful`：真正新7生成元の**別の**selected19 quotientで `classNew(inherited M)=classNew(inherited L) ↔ M=L`。

旧5と新7の比較**Type全体の同値や同一視**は作っていない。元の依存型の構成子・比較公理・仮定は変更していない。

## 5．初回Lean4エラーの全モジュール調査と修正経路

- 初回CI [#42879021485](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42879021485) はFAILURE。元v5.35の5構成子と依存添字署名、v5.73の再帰観測、v5.88の等号反映、今回の新規Leanファイル全体を照合した。
- 失敗は `selectedV589OriginalLoopBracketFaithful` にある**1件の型不一致**。v5.88の `selectedV588UnitFreeRawEq_iff` は補助構文の `selectedV588UnitFreeBracket t` の等号を使う。一方、今回の結論は元の `selectedLocalEighteenInnerBracket l r (embed N t)` の等号である。再帰観測は定義上の同一ではなく、**既に証明済みの観測等式を明示適用すべき**。
- 修正では、元の `selectedV588UnitFreeRaw_observed l r N t` と同じく `u` を `rw` で両辺に適用した後に、従前の等号反映定理を適用。**2行追記のみ**で、定理の条件・構成・型・既存証拠・比較規則の弱化は一切なし。
- 修正後の9,141件Strict Leanと上記14件の実公理出力で、当該 `sorryAx`／エラーが消えたことを確認。

## 6．保持すべき障害と次段

- 認証済みなのは、**元の真正旧18D依存型に直接付けたunitCount=0という条件の全域性**、及び同じN→N fiberのその部分に限る3種の忠実性。
- `unitLeft`／`unitRight`が一つでも含まれる場合の全域復元、同一raw fiber内の同指紋・異raw対の存在／不存在、正のunitCount領域における識別、元旧・新Type19Dの大域同値は**未認証（NO_DATA）**。
- v5.87の**異なるraw17D fiberにまたがる**total-space collisionは本成果と両立するが、同一fiberの衝突証明へ移し替えない。
- WORLD横断のdescent／gluing、実行・制度的権限、哲学上の「空」概念との数学的同一性についても何も証明していない。
- 次段候補Qi v5.90：**もし同一N→N fiberに同指紋・異raw証拠対が存在するなら、双方の元unitCountが正である**という必要条件を実際の型付き元証拠・独立の旧新商で形式化し、unit原子の個数だけで見落とす可能性のある元内部情報を検討する。存在の主張へ先走らない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
