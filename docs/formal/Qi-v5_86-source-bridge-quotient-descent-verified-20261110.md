# Qi v5.86 — 真正旧18D証拠の型付き橋渡しによる条件付き同指紋対・旧5／新7生成元の商降下判定（Lean4形式証明）

2026年11月10日 JST。canonical正本は `itakura-hidetoshi/KuuOS` の `main`。形式証明対象は元の真正依存 `SelectedLocalEighteen`（旧18D証拠Type）、`SelectedContextualEighteen`（真正18D証拠Type）、元の `SelectedLocalNineteen`（旧5構成子）と、これとは**別の** `SelectedRawCongruentNineteen`（新7構成子）の独立した19D比較Typeと各真正商。空・縁起・二諦・中道との対応は命名・解釈層であり、Leanの型検査は哲学的な同一性を形式証明したものではない。

## 1．正本と厳格なGit来歴

- Qi v5.85三段階正式統合後の基準main：`933458acbe227145fa5d008b98655716e0b1ffc8`。
- [定理PR #3488](https://github.com/itakura-hidetoshi/KuuOS/pull/3488) **MERGED**。新規 `formal/KUOS/Architecture/QiWuxingGK5CHP77SourceBridgeDescentCriterionV5_86.lean` **1ファイル501行・22定義／定理・独立の`#print axioms`22件**を追加。元のLeanファイル変更・削除なし。
- 定理認証source `8d308ee841c84224c0aee3c7da9119eacbeb9dd2`、squash main `e05ece475ff0b796e1f16df51069b92a89af212e`。source／事前test-merge／squash Git treeは `6acf17b188635d8b33f158ba70f3208970f85ba6` で一致。
- [公開import PR #3489](https://github.com/itakura-hidetoshi/KuuOS/pull/3489) **MERGED**。`formal/KuuOSFormal.lean`に `import KUOS.Architecture.QiWuxingGK5CHP77SourceBridgeDescentCriterionV5_86` **1行追加のみ**。既存import・公開root107・元比較Typeの不変更。
- 公開認証source `d9e4aadbbd492c70ec993a1bf2a9786b671af39b`、squash main `36fc17adaa27143a54da669c4b5f304fa77f1ee2`。source／test-merge／squash Git treeは `55ed4e71eb36c848f3cd63506e3f94d3ccd69b11` で一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定。保護validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージを維持。

## 2．元の依存型のまま構成した右whisker正確fiberの条件付き衝突

真正 `F,G : ContextFrameEleven` と `after : SevenRewrite`、元16D端点 `H,K` および元17D端点 `N : SelectedContextualSeventeen H K` を**供給する**。右whiskeringによって親16Dの添字自体が `H'=whiskerRight F G H after`、`K'=whiskerRight F G K after` へ移ることを保つ。右17D端点 `R=whiskerRight F G N after` は正確に `SelectedContextualSeventeen H' K'` に属する。

さらに、**同じwhisker後16D親添字**の真正17D端点 `A,B : SelectedContextualSeventeen H' K'` と、以下の真正旧18D証拠値を別途与える。

`pre : SelectedLocalEighteen R A`、`M,L : SelectedLocalEighteen A B`、`post : SelectedLocalEighteen B R`。

仮定は `innerBracket(M)=innerBracket(L)` かつ**元のraw旧18D Type値として** `M ≠ L`。Lean4は次の二つの**実際の** `R→R`旧18D証拠を構成する。

`X=chain (chain pre M) post`、`Y=chain (chain pre L) post`。

`X≠Y`、`innerBracket(X)=innerBracket(Y)`を証明し、既存v5.85の配置木からの同時raw復元器不存在へ正しく接続する。衝突の**十分条件と具体的構成関数**の証明であり、`M,L,pre,post,F,G,after`等を無条件に作ったわけではない。異なる未接続16D親文脈をキャストして貼り合わせてはいない。指紋一致から元旧・新19D商クラスの一致／不一致は導いていない。

## 3．本来の旧5／新7生成元に対する独立の商降下必要十分条件

任意の同一16D文脈における真正18D観測族 `obs : ∀ {J N}, SelectedContextualEighteen J N → α` を取る。

- **旧5構成子**：元の `SelectedLocalNineteen` が識別するすべての証拠対で `obs` が等しいことと、`selectedNineteenSetoid` の真正Quotientへの観測の因子化は**同値**。具体的には `unitPrepend`・`unitAppend`保存の二条件から、反射・対称・推移生成元を含む旧5全体の保存を構成。
- **新7構成子**：元の `SelectedRawCongruentNineteen` を保存することと、別の `selectedRawCongruentSetoid` の真正Quotientへの観測の因子化は**別に同値**。旧5保存に加えて、raw reverse、右raw chain、左raw chainに沿う「観測等号の合同性」を明示的に要する十分条件を証明。旧商保存だけでは新商保存を宣言しない。
- **比較の方向性**：新7保存は旧5保存を含意する。既存の旧商→新商射影に沿う観測因子化の可換性を真正 `Quotient`上で証明。旧・新の異なる19D Typeを同一視しない。
- **降下可能な具体的追加観測**：元のv5.81 whisker配置木とv5.73の順序付き旧継承内部括弧列の**直積**は、旧5・新7双方の比較を保存する。従って双方の真正商に降下し、旧→新の図式が可換となる。ただし全商の完全不変量・全域忠実性を主張しない。
- **非降下の明示例**：真正18D raw先頭が `chain` かどうかの `Bool` は、真正に供給された `M`について `chain (strict J) (inherited M)` と `inherited M`を区別する。一方、元の旧 `unitPrepend`（新7にも継承）がその二値を同一クラスとするため、このraw先頭観測は**旧商・新商のどちらにも降下できない**。obstructionを消さない。

## 4．Lean4失敗・修正・最終成功の経路

証明・条件の弱化、元Lean定義の編集、既存公理追加はいずれも行っていない。変更Lean**全文**、imports、dependent constructors、固定Leanのelaborationを読み、失敗原因を次のように修正。

1. [初回 CI #42806887777](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42806887777) FAILURE：右whiskerで16D親添字が変わるのに未whisker `H,K`の17D端点を置いた不一致。未固定の高階暗黙添字、raw先頭の`decide`、未展開の`injection`等も失敗。証拠の親添字を正確なwhiskered `H',K'`に修正。
2. [2回目 CI #42807780457](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42807780457) FAILURE：定理**ヘッダー**の`H,K`が推定未解決、再帰的な`simp`で`whnf`timeout、多数の依存引数を持つコンストラクタで誤った等式を取得。`(H := H) (K := K)`を明示、括弧保存を`congrArg`へ、構成子式を明示化。
3. [3回目 CI #42808730307](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42808730307) FAILURE：必要な内側の `pre.chain M = pre.chain L` は既に生成されていたが、`injections; assumption`だけでは最終の`M=L`へ至らず。内側の等式を名前付きで取得し、次の`injection`へ伝達。
4. [4回目 CI #42809373251](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42809373251) FAILURE：`injection hchain`が証明を閉じた**後**に残った`assumption`の「No goals to be solved」1件。余分な戦術1行のみ削除。
5. [最終定理 CI #42810096603](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42810096603) **terminal SUCCESS**：Scoped Strict Lean **9,138/9,138**、選択Governance・独立Kuu Core SUCCESS、source/test-merge/squash tree一致。
6. [公開 CI #42810976263](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42810976263) **terminal SUCCESS**：公開 `KuuOSFormal` Strict Lean **10,399/10,399**、Governance **30/30 SUCCESS**、source/test-merge/squash tree一致。

定理側・公開側の**実際の公理出力22/22**：**公理不要11、標準 `propext`／`Quot.sound`のみ11**、新規`sorryAx`なし、変更Lean error/warning 0/0。これはv5.86の対象22宣言についての監査であり、外部全体や哲学的意味の認証ではない。

## 5．未認証の境界・次段

等しい内部括弧指紋を持ちながら元raw旧18D Type値が異なる`M,L`の**無条件の具体的存在**、任意`pre/post`や`SevenRewrite`の居住性、任意の16D親添字の間の型消去・転送、同指紋から旧／新真正商クラスの比較可能性、全商完全分類、元旧／新19D Typeの大域同値、WORLD横断降下／20D gluing、行為・ガバナンス権限は**NO_DATA／未認証**。選好は降下を、降下は権限を意味しない。

次段Qi v5.87では、衝突対を元の依存Type内で実際に居住させ得る具体的な生成条件（または成立障害）を探し、観測の合同性を忘れずに新旧商に対する識別能力の限界を調べる。

運用原則：append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
