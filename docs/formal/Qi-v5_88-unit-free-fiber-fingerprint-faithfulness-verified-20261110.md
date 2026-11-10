# Qi v5.88 — 真正raw旧18D同一fiber内のunit-free部分における内部括弧観測の忠実性（Lean4形式証明）

2026年11月10日 JST。唯一のcanonical正本は `itakura-hidetoshi/KuuOS` の `main`。対象は元の依存型 `SelectedLocalEighteen`（真正旧18D証拠）と `SelectedContextualEighteen`（真正18D証拠）に実際に埋め込まれた**限定unit-free部分**、元の旧5構成子 `SelectedLocalNineteen` と別型の新7構成子 `SelectedRawCongruentNineteen`（真正19D比較）および各真正商である。構文観測と「空・縁起・二諦・中道」の対応は命名・解釈の層であり、Lean4が宗教哲学を証明した意味ではない。

## 1．Git正本・Lean環境・独立認証

- 前段v5.87三段階統合済みmain：`f70d9a8444c7a49c3615af39fc89516c6eb59d96`。
- [定理PR #3494](https://github.com/itakura-hidetoshi/KuuOS/pull/3494) **MERGED**。新規 `formal/KUOS/Architecture/QiWuxingGK5CHP77UnitFreeFingerprintFaithfulnessV5_88.lean` 1ファイル**513行・26宣言・独立`#print axioms`26件**。歴史的Leanファイルは変更・削除0。
- 定理認証source `1b9f62bd0d3e8aef4a71c52bdbd92e1922158fcd`、squash後main `946f82b81e6602ee204d73fd5d26a00a6d63df3a`、source／事前test-merge／squash Git tree `f1ccac880116ca90b78bebae6971f2139199c5eb` は完全一致。
- [公開import PR #3495](https://github.com/itakura-hidetoshi/KuuOS/pull/3495) **MERGED**。`formal/KuuOSFormal.lean`に`import KUOS.Architecture.QiWuxingGK5CHP77UnitFreeFingerprintFaithfulnessV5_88`を1行追加のみ。既存公開importと公開root107は変更なし。
- 公開認証source `d790ed0fef1e85f414637eb4079f40ee036d6b6a`、squash後main `925a31d92f76c3b32288657fd6fba9ce78c1c318`、source／test-merge／squash Git tree `e1aec4b5ea31794ce053a3676d044bf35d097edd` 完全一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`を固定。保護validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージを維持。

## 2．真正旧18Dの同一exact N→N fiberに入るunit-free部分

元の16D親文脈で真正17D証拠端点 `N : SelectedContextualSeventeen W l r H K`を固定する。独立補助構文 `SelectedV588UnitFreeTerm`は`strict`・raw `reversed`・非結合二分木`joined`のみを持つ。**新しい同値関係・代理旧18D証拠Typeを定義したものではない**。

`selectedV588UnitFreeRawEmbed l r N`は、この部分構文の各値を元の `SelectedLocalEighteen W l r N N` に、元の `.strict N`・`.reverse`・`.chain`構成子だけで埋め込む。各分枝は同一の真正raw17D端点`N→N`にとどまる。後段の忠実性は**この実際に構成された像上のみ**の主張であり、任意の元旧18D証拠に対する大域主張ではない。

## 3．内部括弧観測の構文復元と元raw証拠値の識別

元のv5.73独立構文 `SelectedInheritedOldInnerBracket`を変えず、unit-free構文の独立読取り`selectedV588UnitFreeBracket`と部分パーサ`selectedV588UnitFreeParse`を定義した。元の`oldUnitLeft`・`oldUnitRight`はparserの値`none`に明示的に残す。

`parse (bracket t)=some t`を全unit-free項`t`についてLean4で証明。従って`bracket`は単射で、**元の型付き旧18D証拠上**の観測定理

`selectedLocalEighteenInnerBracket l r (selectedV588UnitFreeRawEmbed l r N t)=selectedV588UnitFreeBracket t`

と合わせて、`embed(N,t)=embed(N,u) ↔ bracket(t)=bracket(u)`を得る。実際の`embed(N,-)`も単射。等号反映は元raw旧18D Type値の等号であって、観測値を元証拠に代入したり、元証拠構成子を上書きしていない。

## 4．独立した元旧5／新7真正商とType19D比較の限定忠実性

`inherited (embed(N,t))`という元の真正18D証拠を使用し、元のv5.73「継承内部括弧列の旧5・新7商への独立降下」定理と接続して、次を**別々に**形式証明した。

- 元旧5構成子`selectedNineteenClass`：`[inherited(embed t)]old=[inherited(embed u)]old ↔ t=u`。
- 独立新7構成子`selectedRawCongruentClass`：`[inherited(embed t)]new=[inherited(embed u)]new ↔ t=u`。
- 真正新7商で**1回raw反転guardを付けた** `reverse(inherited(embed t))` の像でも新商等号`↔ t=u`。
- 元旧`SelectedLocalNineteen`および別の元新`SelectedRawCongruentNineteen`の**各型付き比較Typeの`Nonempty`**が個別に`t=u`と同値であり、両比較の居住性が一致するのは**この限定像のみ**。
- 元の同一`N→N` fiberに実際に構成される`strict N`と`reverse(reverse(strict N))`はraw旧18D値として相異なり、旧新真正商でも別クラス。raw二重反転を勝手な群oid逆射と同一視していない。

## 5．unitLeft・unitRightによる観測範囲の境界

独立の`selectedV588InnerUnitCount`を内部括弧木に定義した。unit-freeの**すべての深さ・入れ子**の木についてその値は0である。unit原子が一つでもある任意の観測値はunit-free構文像に属さない。

元の**真正型付き旧18D** `SelectedLocalEighteen.unitLeft before F G C after`と`.unitRight before F G C after`は、それぞれ元v5.73の`oldUnitLeft`・`oldUnitRight`を観測する。いずれもunit-free像に属さず、両観測原子も別である。

この「部分parserが適用できない」ことは**元旧18Dの全体に同指紋・異raw証拠対があるという存在証明ではない**。真正unit生成元を含む任意の元旧18D証拠を、上のunit-free復元器で復元できるとは主張しない。とくにv5.87の**異なるraw17D fiber間の総空間衝突**を同一fiber衝突に言い換えない。

## 6．Lean4エラーの構造分析・厳格なexact-source受領書

- 初回[定理CI #42819515133](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42819515133) FAILURE：変更Lean全文・元v5.35依存構成子・v5.73元観測降下・v5.86/v5.87定義を確認。具体的には再帰的な`simpa`による`whnf`ハートビート上限2件、未証明の再帰観測等式をdefinitional equalityとして`change`した失敗3件、raw単位証拠を未展開のまま`decide`した自由変数の失敗1件。すべて定理の前提・元ソース・元19D比較を弱めず修正。
- 修正は、元旧18Dコンストラクタの直接形を`change`で固定し`congrArg`／`congrArg₂`で等式を移す、元商から取り出した**実際の**元旧18D継承括弧列の等式を書き出した後で既存の観測定理を`rw`する、元単位観測を`oldUnitLeft ≠ oldUnitRight`へ正規化して`decide`すること。
- [最終定理CI #42820232955](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42820232955)：terminal SUCCESS、Scoped Strict Lean **9,140/9,140**、選択Governance・独立Kuu Core SUCCESS。
- [公開CI #42821087371](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42821087371)：terminal SUCCESS、`KuuOSFormal` Strict Lean **10,401/10,401**、Governance **30/30**。
- 両CIの**実公理監査26/26**：**公理不要7、標準`propext`・`Quot.sound`のみ19**。新規`sorryAx`なし、変更Lean error／warning 0／0。定理・公開の各exact source／test-merge／最終squash Git treeも一致。CI成功は**その定理の条件付き範囲でのみ**認証を与える。

## 7．未認証の障害と次段

証明済み：この**特定のunit-free同一raw17D exact fiber埋込像**は、元の内部括弧観測・旧5／新7真正商・独立元Type19D比較において局所忠実。

未認証（NO_DATA）：任意の元旧18D raw sourceがこのfragmentに属するとの主張、unitLeft／unitRightを含む部分での全域復元、同一raw17D exact fiber内の**同指紋で異なる元旧18D証拠対の存在または不存在**、任意上位`SevenRewrite`／橋の居住性、元旧・新Type19Dの大域同値、WORLD横断／20D gluing、制度的権限。追加観測の一意性も証明していない。

次段Qi v5.89候補：元旧18Dのunit-free条件を**元の依存証拠値に直接**付し、上記埋込像がその条件を尽くすか検証する。さらにunit生成元を含む同一raw fiberの情報消失が実際に衝突を作るための必要条件を調べる。部分忠実性を無条件全域に降下させない。

運用原則：append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
