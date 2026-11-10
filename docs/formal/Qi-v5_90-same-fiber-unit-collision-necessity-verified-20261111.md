# Qi v5.90 — 真正旧18D同一exact fiberの指紋衝突には両側のunit構成子が必要（Lean4形式証明）

2026年11月11日 JST。canonical正本：`itakura-hidetoshi/KuuOS`／`main`。元の真正17D依存端点を固定した旧18D `SelectedLocalEighteen W l r N N`、その元内部括弧観測、元の旧5／別の新7選択19D商およびそれぞれの型付き19D比較を対象にする。以下の必要条件は**衝突の存在証明でも十分条件でもない**。「空・縁起・二諦・中道」との対応は解釈／命名の層で、Lean4が哲学的概念を証明した意味ではない。

## 1．Git正本と独立CIの来歴

- 前段Qi v5.89の定理・公開import・正式記録がすべてMERGED。v5.90のbase main `3601e183b54aa8f9a6c46b0076ecb71879b6fe33`。
- **定理PR [#3500](https://github.com/itakura-hidetoshi/KuuOS/pull/3500) MERGED**。新規 `formal/KUOS/Architecture/QiWuxingGK5CHP77SameFiberUnitCollisionNecessityV5_90.lean` 1ファイル、最終GitHub差分271行追加／削除0。歴史的Leanファイルを改変しない。
- 初回source `6fb4fa4ec5c590c6dd3ffc4b1f07c35cf2d32e67`、修正後認証source `df651060f6ed9b314d2a79458fff863a8df0dd70`、定理squash後main `abea76ed59d5986d808e368e7458b1d4139dcfba`。source／test-merge／squash後Git treeは**`e7dc418e230ea86adaf9ebce33a2cc1bfa6ce682`で完全一致**。
- 定理exact-source CI [#42898281779](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42898281779)：**terminal SUCCESS**、Scoped Strict Lean **9,142/9,142**、Governance／独立Kuu Core SUCCESS。
- **公開import PR [#3501](https://github.com/itakura-hidetoshi/KuuOS/pull/3501) MERGED**。元の `formal/KuuOSFormal.lean` に**新規import1行のみ**。公開source `bf3167b519c1116872ab38d96d6329e1c832cee2`、squash後main `eda299ba4013fd46a0e3e161cb7de0eef1caa913`。source／test-merge／squash後Git treeは **`2f578b0f7aae24015824407086403a3b593bc924`で一致**。
- 公開CI [#42899043239](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42899043239)：**terminal SUCCESS**、公開 `KuuOSFormal` のLean依存閉包 **10,403件**、Governanceの30ジョブすべてcompleted／失敗0。
- 両独立Lean実ログの新規 `#print axioms`は**12/12**。**公理不要3件、残り9件は`propext`・`Quot.sound`のみ**。新規 `sorryAx`、対象Lean error／warningなし。
- Lean固定版 **v4.30.0-rc2**、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107維持。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 2．観測と元の証拠値の区別

前段v5.89で、元旧18Dの実際の5構成子に直接 `selectedV589OriginalUnitCount` を再帰定義し、**unitCount=0の場合に限り**元証拠がv5.88の忠実なunit-free構文像で尽くされることを証明済み。

Qi v5.90は元の真正旧18D `M,L : SelectedLocalEighteen W l r J N` の**同じ依存添字**を保持し、
`selectedLocalEighteenInnerBracket l r M = selectedLocalEighteenInnerBracket l r L`
から
`selectedV589OriginalUnitCount l r M = selectedV589OriginalUnitCount l r L`
を証明（`selectedV590BracketEq_originalCountEq`）。これはv5.89の証明済み`OriginalUnitCount_observed`を両側に使った観測整合性であり、`M=L`を無条件に主張しない。

## 3．同一N→N exact fiberで証明された必要条件

真正同一raw17D端点 `N` について

```text
M L : SelectedLocalEighteen W l r N N
bracket(M) = bracket(L)
M ≠ L
--------------------------------
0 < OriginalUnitCount(M) ∧ 0 < OriginalUnitCount(L)
```

を `selectedV590BracketCollision_requiresPositiveUnits` として形式証明。

その反対方向は主張していない。証明の中心は、`bracket(M)=bracket(L)`で一方の元unitCountが0なら、まずunitCountの一致によりもう一方も0と判明し、v5.89の**元依存型の全zero-unit像の忠実性**から真正raw旧18D証拠が`M=L`になる、という論理である。

`selectedV590BracketEq_leftFreeReflect`と`selectedV590BracketEq_eitherFreeReflect` は「一方がunit-free」という**片側条件だけ**からraw等号を反映する。前提を弱化したのではなく、他方のunit-free性を既証明の観測保存則で導いたもの。

## 4．旧5商・新7商・元の型付き19D比較の独立した必要条件

同じN→N fiber上の元旧18D証拠`M,L`を真正18Dの`.inherited M`、`.inherited L`として埋め込む。v5.73で証明済みの**本来の**継承内括弧列観測に対する降下定理を、それぞれ本来の旧5商と本来の新7商へ別々に適用し、商クラス等号から元内部括弧観測等号を得る。

- `selectedV590OldClassEq_impliesBracketEq`／`selectedV590NewClassEq_impliesBracketEq`：各々の真正商で同一クラスなら元旧18Dのsource-inner bracketが一致する。
- `selectedV590OldClassEq_leftFreeReflect`／`selectedV590NewClassEq_leftFreeReflect`：各々の真正商で同一クラス、かつ元の一方のunitCountが0なら、本当の元旧18D raw証拠は等しい。
- `selectedV590OldClassCollision_requiresPositiveUnits`／`selectedV590NewClassCollision_requiresPositiveUnits`：各々の真正商で同一クラスでも元のraw証拠が異なる**仮定**の下では、両側で元unitCountが正。
- `selectedV590OldTypedCollision_requiresPositiveUnits`／`selectedV590NewTypedCollision_requiresPositiveUnits`：元の**別々の型**の選択19D比較が実際に存在して、raw元証拠が異なると仮定したときにも、同じ必要条件が成り立つ。

これらは `Nonempty` の証拠が与えられた場合の含意であり、どちらのType19D比較の居住性も新たに生成していない。旧5商と新7商の大域同値も宣言していない。

## 5．初回Lean4失敗の構造原因と最小修正

初回CI [#42897496450](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42897496450) はFAILURE。実ログは新規ファイル147・165行の**2件の `No goals to be solved`**。これは旧5商・新7商の各証明でリスト単一要素等号に `injection ho with hbr` を実行した時点で目標が完成していたのに、続く `exact hbr` を実行していたためである。

変更Leanファイル全文、元v5.35の依存構成子、v5.73の元継承内括弧降下、v5.88の元商観測書換え、v5.89のunit-free全域性を確認。**未マージ新規ファイルの余分な`exact hbr`2行だけを削除**。元の定理の型・仮定・比較規則、ピンしたLean/mathlib、歴史的ファイルは不変更。修正後の9,142件Strict Leanと12件の実公理監査でエラー解消を確認した。

## 6．未認証障害・次段候補

**認証済み**：同じ真正raw17D N→N fiber内で、同指紋だが異なる元raw旧18D証拠の存在を**仮定したなら**、どちらもunit構成子を一つ以上持つ。元旧5・新7真正商のクラス等号、別々の元Type19D比較が仮に異raw値を結ぶ場合にも同じ必要条件。

**NO_DATA**：unit構成子を含む同一fiberの同指紋・異raw証拠対が実際に存在するか、正のunitCountが衝突の十分条件になるか、元のunitLeft／unitRightパラメータから型付き衝突を構成できるか、全旧18D分類、旧新19D比較の大域同値、異fiber transport／WORLD／20D降下、実行・制度的権限。前段v5.87の**異なるraw17D fiberを跨ぐ**total-space collisionをここに移し替えない。

**Qi v5.91候補**：元のunitLeft／unitRightを含む正のunitCount領域で、同一真正raw17D fiberの居住性・中間端点整合・source-inner-bracketの単位原子以外のパラメータ情報を調べる。衝突の存在を結論へ先取りせず、実際の型付き証拠構成が成立した場合にのみ局所認証を拡張する。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
