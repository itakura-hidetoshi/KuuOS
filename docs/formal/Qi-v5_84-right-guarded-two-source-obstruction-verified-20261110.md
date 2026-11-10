# Qi v5.84 — 右whiskeringのguard付き局所忠実性と2源内部括弧obstruction（Lean4形式証明・公理監査）

2026年11月10日 JST。`itakura-hidetoshi/KuuOS` 正本 `main`。本書は元の真正依存`SelectedContextualEighteen`（18D Type値）、独立した旧5構成子`SelectedLocalNineteen`と新7構成子`SelectedRawCongruentNineteen`（19D比較Type）、真正商および追加の独立観測が**指定されたfiber内で**満たす形式定理の証跡である。「空」「縁起」への対応は解釈・命名層であり、数学定理から哲学的同一性を導いたものではない。

## 1. 正本・形式成果物・Git tree同一性

- 基準はQi v5.83正式統合main `8cd2f5329772444a789c64a8411f0e26edfba9b3`。
- [定理PR #3482](https://github.com/itakura-hidetoshi/KuuOS/pull/3482) **MERGED**。新規`formal/KUOS/Architecture/QiWuxingGK5CHP77RightGuardedTwoSourceObstructionV5_84.lean` **536行・25宣言・25件の独立`#print axioms`**。既存Leanファイルへの変更・削除なし。
- 定理exact-source `bf4c658bae71fb5727fc7bd4ac0a807aaa5ff4aa`、squash `ca1bfef33bd6c66e00f2ec4c4425bbf019541d30`。事前にsource/test-mergeのGit tree同一を独立確認し、マージ後squashとも`5d20be6c5ad94b1ee639c88620cfc81eaf8ee784`で一致。
- [公開import PR #3483](https://github.com/itakura-hidetoshi/KuuOS/pull/3483) **MERGED**。`formal/KuuOSFormal.lean`へ`import KUOS.Architecture.QiWuxingGK5CHP77RightGuardedTwoSourceObstructionV5_84`を**1行追加のみ**。公開root107、従前import・定理は不変更。
- 公開exact-source `98d7c6de366cb54a1fd69ae0a8e3b865ab5e891b`、test-merge、squash `73a7bca0cea8d29d5d6a02fa64917c99cf5f790d` のGit treeは`e3c90c36ba7e4e0dbf37c658bcd856ccb47e1825`で一致。
- 固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。validation-only保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 2. 元18D Type上の右側3枝と成立条件

真に供給された`F G : ContextFrameEleven W l r c d`、`after : SevenRewrite W l r d e`、元17D端点`N`を用いて、**右側のみ**`N' = whiskerRight F G N after`とする。さらに**別途実際に供給される**`M : SelectedLocalEighteen W l r N' N'`を必要条件とする。任意の`M`や`after`の存在を生成・推定しない。

新`SelectedV584RightGuardedFragment`から元の依存`SelectedContextualEighteen W l r N' N'`への埋め込みは、(1) v5.82自由pure strict/reverse/raw-chain部分の像、(2) `reverse (inherited M)`、(3) `reverse (whiskerRight F G (strict N) after)`の**3枝**のみを取る。左側v5.83のfiberと右側fiberを型として同一視しない。

独立`selectedContextEighteenWhiskerPlacement`観測は、それぞれ`selectedPureStrictReverseRawValue A`、`reversed (source (selectedLocalEighteenInnerBracket M))`、`reversed (right strict)`である。これらの排他性に基づく`selectedV584RawValue_injective`、元18D上の観測等式、埋め込みの単射性をLean4で証明。

## 3. 独立した旧新19D比較と完全観測

前節の指定3枝`A,B`に限り、**旧5構成子商と新7構成子商それぞれ**で`[embed A] = [embed B] ↔ A = B`を定理化。また元旧`SelectedLocalNineteen`と元新`SelectedRawCongruentNineteen`という**別々の比較Type**の`Nonempty`が、それぞれ`A = B`と同値であることを別証明し、この限定像上でのみ比較可能性の同値を得る。

`SelectedFullV581QuotientObservationValue`の旧v5.80全座標（元九観測・二本の**全Nat→Nat無限祖先／run塔**など）とv5.81配置木の直積を減らさず、当該3枝の真正新商クラス上で観測の等号反映を証明した。**全18D商全体の忠実性や、旧新19D比較Typeの同一性は未証明**。

## 4. 2つの元旧18D証拠の分離条件

同一の**右whiskered `N'→N'` fiber**に、別個の真正旧18D証拠`M,L`が**両方供給されたときに限り**、既に旧・新真正商へ別々に降下したv5.81配置観測を用いて次を証明。

- 旧5構成子商クラス`[inherited M] = [inherited L]`なら、`innerBracket(M) = innerBracket(L)`。
- 新7構成子商についても同じ必要条件。
- **対偶**：`innerBracket(M) ≠ innerBracket(L)`なら、旧・新両商クラスは不一致で、それぞれの元19D Type比較の`Nonempty`は成立しない。
- さらに、`reverse (inherited M)`と`reverse (inherited L)`を1回のraw反転でguardした真正新商クラスも不一致。

`innerBracket(M) = innerBracket(L)`から元Type値や商クラスの一致を導く**逆方向は未認証**。局所観測から無条件の大域貼合へ昇格させない。

## 5. 単位律による保存されたobstruction

元の`SelectedLocalNineteen.unitPrepend M`と`unitAppend M`を**変更せず**保存。右同一fiberでも、raw 18D構成子で異なる
`chain (strict N') (inherited M)`／`inherited M`、また`chain (inherited M) (strict N')`／`inherited M`は、元旧19D商および独立新19D商ではそれぞれ同一クラスになる。新しい`selectedV584Right_unguardedAppendOldNew`と`selectedV584Right_unguardedAppendRawDistinct`は、後者のraw不一致と商同一の両方を証明。

したがって未保護の`inherited`葉を自由追加した無制限の忠実な分類は、この構成からは得られない。これを障害として明示し、元の単位生成元や仮定を弱めていない。

## 6. CI失敗から形式認証までの変更履歴

- [初回定理CI #42771407042](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42771407042) **FAILURE**：新規Lean 378／398／470行で`cases ho`により`Dependent elimination failed: Failed to solve equation`。`source(innerBracket M) = source(innerBracket L)`等で、依存する元構成子内の引数等式を単に`cases`で消去しようとしたことが原因。
- [2回目CI #42771957162](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42771957162) **FAILURE**：構成子単射性へ置き換え、3件の依存消去障害を解消したが、2件の`injection ho with hbr`の直後に冗長な`exact hbr`が残り`No goals to be solved`。
- 最終修正source `bf4c658bae71fb5727fc7bd4ac0a807aaa5ff4aa`では上記2行のみ除去し、元Type／定理文／証明の仮定／既存の比較生成元は変更しなかった。**全文・依存構成子署名を照合し、エラー種別に対応した修正**として履歴を保存。
- [3回目定理CI #42772506829](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42772506829) **terminal SUCCESS**。Scoped Strict Lean **9,136/9,136**、Governance・独立Kuu Core選択ジョブSUCCESS。
- [公開CI #42773366817](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42773366817) **terminal SUCCESS**。`KuuOSFormal` Strict Lean **10,397/10,397**、Governance **30/30 SUCCESS**。
- 定理／公開の新規25件の`#print axioms`**実出力を照合**：**公理不要5／標準`propext`・`Quot.sound`のみ20**、変更Lean error/warning 0/0、新規`sorryAx`なし。対象25件の結果であり、全ライブラリの大域無公理性を主張しない。

## 7. 未認証項目とQi v5.85への境界

任意の元18D`M,L`や`SevenRewrite`の居住性、`innerBracket`観測一致からの逆方向、異なる左／右fiberの同一視・輸送、任意のraw結合・guard閉包、旧新19D Typeの大域同値、全商分類、WORLD横断降下、20D gluing、制度的／実行権限は**未認証（NO_DATA）**。

次段v5.85候補は、同一依存fiber内で**旧18D内部括弧観測が等しいが別の元Type証拠**の識別可能性／不足観測量の検討と、追加guard下の条件付き閉包。差分とcompatibilityを残し、全域化しない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
