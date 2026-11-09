# Qi v5.72 — 継承葉数まで観測しても残る旧18D根構成子の順序履歴（Lean4形式証明・公理監査）

2026年11月10日 JST。形式成果物は本来の依存Type値 `SelectedContextualEighteen`、原 `SelectedLocalEighteen`、元selected19の5構成子と独立した新raw congruenceの7構成子、同一exact 17D fiberの真正商に限定される。「空」「縁起」との対応は命名・解釈の層であり、Lean4による宗教哲学の証明ではない。

## 1. 唯一のcanonical正本と変更範囲

- Repository `itakura-hidetoshi/KuuOS`、canonical `main`。研究開始時Qi v5.71まで正式統合済みHEAD `9da7f51b91ea7c97b1b96fdd24548204372b4b03`。
- [定理PR #3446](https://github.com/itakura-hidetoshi/KuuOS/pull/3446) **MERGED**。新規Lean4ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77OrderedInheritedRootResidualV5_72.lean` **1件だけ追加**。既存Lean定義、型付き証拠、比較生成元、importはすべて不変。
- 定理認証source `386bde67318a0495d7a0dc3f24a69edf865a3da6`、test-merge `fe0611e13d553190309592d170f1fb18e3d4775e`、squash `2b9a61842a095ffdb631e3a134dfd0e2ab34085b` のGit treeは **`95f44b076df1f325c68a335df6ecb8701269a3a0`** で完全一致。
- [公開import PR #3447](https://github.com/itakura-hidetoshi/KuuOS/pull/3447) **MERGED**。公開 `formal/KuuOSFormal.lean` に該当importを **1行だけ**追記。既存import削除0、公開root **107維持**。
- 公開認証source `cd812bf75ad315149e2ecbf8be0e9fc2c27e058d`、test-merge `a9b49cc351ec920873e039cc780e439e76c2e762`、squash `48e1934c911f6086267fff891dd1df99c9f92f34` のGit treeは **`a6a0f44de1ae63ec9a7b9433da184e7bf121117f`** で一致。
- Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`** 固定。保護validation-only PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。

## 2. 証明した独立順序不変量

旧 `SelectedLocalEighteen` は `strict`・`unitLeft`・`unitRight`・`reverse`・`chain` の**5構成子**を持つ。新しい独立Enum `SelectedInheritedSourceRootTag` は、元の依存旧18D証拠 `M` を消去せず、その**最外構成子のラベルのみ**を読む。

`selectedContextEighteenInheritedRootList` は真正raw18D値を構造再帰する。元 `inherited(old18)` 葉にはold18のroot tagを1要素加え、raw `strict` は空列、raw `reverse` と原7D whiskeringは内側の列を保持し、raw `chain A B` は左右の列を **順序付き連結**する。元のraw18D `chain` の結合律は仮定していない。

この観測について：
- 旧 `SelectedLocalNineteen` の**5構成子**全部で保存性を形式証明。元の `unitPrepend`・`unitAppend` が消すのはraw strictであり、`inherited(old18)` 自体ではない。
- 独立新 `SelectedRawCongruentNineteen` の**7構成子**全部で保存性を形式証明。raw reverse、左右raw chainについて真の帰納仮定から整合性を証明。
- 旧商・新商へ別々に `Quotient.lift` で降下し、旧→新projectionによる因子化の可換性を証明。元Type値や元比較規則は変更なし。

## 3. 新しい真正18D Type値の反例

任意の元17D端点 `N` の真正 `N→N` fiberで、元 `SelectedLocalEighteen` の `strict N` と `chain (strict N) (strict N)` はどちらも本物のold18D証拠であり、同じ元端点を持つ。これらを原raw18D `reverse(inherited(_))` に持ち上げたものを `X`、`Y` とし：

```text
X := reverse (inherited (old18.strict N))
Y := reverse (inherited (old18.chain (strict N) (strict N)))
A := chain X Y
B := chain Y X
```

と構成した。二つの真正raw18D値について、**既存9変量、全 `Nat→Nat` 祖先塔、全 `Nat→Nat` 直接連続反転数塔、完全ordered raw reverse run list、v5.70非結合的単位簡約括弧構造、v5.71 inherited葉数（双方2）** がすべて一致することを証明。

一方、新しく独立に読んだ順序付き元証拠root listは：

```text
InheritedSourceRootList(A) = [strict, chain]
InheritedSourceRootList(B) = [chain, strict]
```

で相異なる。これは**単なる葉数差ではない**。新順序列が真正新7構成子商へ降下するため、A/Bは**異なる新商クラス**であり、両者の真正 `SelectedRawCongruentNineteen` Type値比較も存在しない。

さらに実際に提供された任意の元raw18D `M:J→N` に限り、`chain M A` と `chain M B` を同じexact fiber `J→N` で構成。すべての既存観測とinherited葉数は等しく、元証拠root listは共通prefixに対するリストの左消去則からなお相異なる。よって新結合商観測はそのfiberで非単射となり、root list decoder／全クラスdecoder不存在も得る。任意の指定 `J→J` には元 `strict J` で確かな具体例がある。

## 4. 実CI・修正履歴・公理監査

- 初回[定理CI #42706952322](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42706952322) はFAILURE。元 `SelectedLocalEighteen.unitLeft` と `unitRight` はそれぞれ**5つの明示引数**（before、F、G、C、after）を持つが、新root tag関数で当初4引数パターンを記述したため型不一致。そこから後続のroot tag計算と証明のdefinitional equality失敗、未認証source上の派生 `sorryAx` が生じた。
- 修正は元の5引数構成子とのパターン一致を正しく記載した**2行だけ**。前提、定理、元Type値、元比較、観測条件は不変。
- 修正版[定理exact-source CI #42707637446](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42707637446) **completed SUCCESS**：Scoped Strict Lean **9,124/9,124**、Governance **5/5 SUCCESS**、変更Lean error/warning **0/0**、新規sorryAxなし。
- [公開exact-source CI #42708720098](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42708720098) **completed SUCCESS**：KuuOSFormal Strict Lean **10,385/10,385**、Governance **30/30 SUCCESS**、変更Lean error/warning **0/0**、新規sorryAxなし。
- 新規**36宣言すべてに `#print axioms`** を置き、実ログを検証：**26宣言は公理なし**、残る**10宣言は標準 `propext` または `Quot.sound` のみ**。新規任意公理、証明穴はない。
- CI SUCCESSとGit tree同一性は固定Lean4の該当証明範囲での実検証であり、命名解釈や制度上のaction authorityの正当化ではない。

## 5. 境界と次段

- 新root tagは最外構成子**5値**の観測だけであり、同じ `chain` タグの二つの元old18D証拠や、その内部の入れ子構造を**同一視／分類したものではない**。現在の新結合観測へroot tag listまで加えたときの全商クラス識別性は**NO_DATA**。
- 次段Qi v5.73は、**同じ順序付きroot tag list**を持ちつつ相異なる元old18D証拠の内部構文を、真の旧新比較と整合する独立不変量として読めるかを調べる。v5.72の現在の証拠対はroot tag順序で区別されるため次段へそのまま流用しない。
- 任意異端点fiber非空性、元証拠値全体の無条件復元、20D gluing、全WORLD貼合、institutional authorityも未認証（NO_DATA）。
- append-only／tighten-only／overwrite-forbidden／same-root。元18D Type値、旧新19D比較の独立性、root107、固定Lean/mathlib、保護#1558 Draft／OPEN／未マージを維持。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
