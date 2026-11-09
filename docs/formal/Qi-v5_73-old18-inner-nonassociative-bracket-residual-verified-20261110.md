# Qi v5.73 — inherited旧18D内部の非結合的括弧構造が残す識別障害（Lean4形式証明・公理監査）

2026年11月10日 JST。以下の機械的結果は、真正の依存Type値 `SelectedLocalEighteen`、`SelectedContextualEighteen` と、独立した旧selected19・新7構成子raw合同性比較および同一exact fiberの商に限定する。「空」「縁起」との対応は命名・解釈の層であり、宗教哲学命題のLean証明ではない。

## 1. 正本と実際のGitHub認証来歴

- Repository `itakura-hidetoshi/KuuOS`。研究着手時のcanonical main HEADは、Qi v5.72まで正式統合済み `be6dc7025f8144588dce99061ee9f4bc28e1894f`。
- [定理PR #3449](https://github.com/itakura-hidetoshi/KuuOS/pull/3449) **MERGED**。新規 `formal/KUOS/Architecture/QiWuxingGK5CHP77OldInheritedInnerBracketResidualV5_73.lean` **1ファイル・545行追加、削除0**。既存Lean定義・元証拠Type・比較生成元を変更していない。
- 定理認証source HEAD `b1d9e06ad5873c4c8d060f798c3f2f0e03e37404`、test-merge `fbe73132797ef32f6ce935c075901e0f1339f5da`、squash `91c45faa19720b85d037ddd65fe671a18b6c311b`。三者のGit tree **`bd4a6351993e704cf078f1adcdfc4eab336aa0a8`** が完全一致。
- [公開import PR #3450](https://github.com/itakura-hidetoshi/KuuOS/pull/3450) **MERGED**。`formal/KuuOSFormal.lean` にv5.73をimportする**1行のみ追加**、既存import削除なし。公開root **107**を維持。
- 公開認証source `e544267a1433f1bb4d4e369a12a0185de9125ee9`、test-merge `a4b9254e75d854b648158e3f6011e1f1fd76a51c`、squash `96006113c177024ada877102900cef7ffd3c179b`。三者のGit tree **`3c452b87c77bcb535001125ffefabfdf058b5228`** が一致。
- 固定Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージを維持。

## 2. 真正旧18D証拠からの独立した非結合的内部構文観測

元の依存Type `SelectedLocalEighteen` は `strict`、`unitLeft`、`unitRight`、`reverse`、`chain` の5構成子を持つ。独立の `SelectedInheritedOldInnerBracket` は、これらをそれぞれ `oldStrict`、`oldUnitLeft`、`oldUnitRight`、単項 `oldReversed`、二項 `oldJoined` に写す、**結合則を課さない**構文木である。これは本来の依存Type値を同一視する商ではなく、本来の値の独立観測である。

新 `selectedContextEighteenInheritedInnerList` は、真正contextual18D raw証拠の `inherited(old18)` 葉で内側のold18D構文木を読み、順序付きListにする。raw `strict` は空列、raw `reverse`／whiskerは内側の列を保持し、raw `chain A B` は列を順序付き連結する。

- 元 `SelectedLocalNineteen` の**5構成子すべて**でこの列が保存される。特に元 `unitPrepend`／`unitAppend` はcontextual raw `strict` を除くだけで、継承された真のold18D証拠を変更しない。
- 独立 `SelectedRawCongruentNineteen` の**7構成子すべて**で保存。raw reverseと左右raw chainにおける型付き保存を帰納法で証明。
- 旧・新の別々の真正商へ `Quotient.lift` し、旧→新projectionを通じた因子化も証明した。比較生成元の増設や元Typeの書換えはない。

## 3. 既存全観測の一致と新障害の実例

任意の真正17D端点 `N` の元old18D `N→N` fiberで、次の実際のType値を構成する。

```text
s    := old18.strict N
Aold := old18.chain (old18.chain s s) s
Bold := old18.chain s (old18.chain s s)
A    := contextual18.reverse (contextual18.inherited Aold)
B    := contextual18.reverse (contextual18.inherited Bold)
```

`Aold`、`Bold` のold18D最外構成子はともに `chain`、内部の `strict` 原子はどちらも3個。しかし**非結合的old18D構文木は `((s∘s)∘s)` と `(s∘(s∘s))` で異なる**。

元の真正contextual18D `A`、`B` について、従来の**九観測・全自然数次数の祖先塔 `Nat→Nat`・全直接連続反転数塔 `Nat→Nat`・完全ordered raw逆転ラン列・raw18D単位簡約非結合括弧・inherited葉数（双方1）・その最外構成子の順序付き列（双方 `[chain]`）** が完全一致することを形式証明した。

その一方で、新しい真のold18D内部括弧リストは `[oldJoined (oldJoined s s) s]` 対 `[oldJoined s (oldJoined s s)]` と異なる。このリストは真正7構成子商へ降下するため、**真正新商クラスは相異なり、型付き新19D比較も存在しない**。

さらに実在する元 `M:J→N` を明示的に受け取った場合に限り、`chain M A`、`chain M B` を同じexact dependent fiberに構成し、全旧観測とv5.72根タグ列が一致したまま、新しいold18D内部括弧列は共通prefixのList消去によって異なるままと証明。よって、その実在するfiberにおける結合商観測の**非単射**、inner-bracket decoder不存在、全商クラスdecoder不存在、真正 `strict J` を与えるJ→J例を得た。異端点fiberの任意非空性は仮定しない。

## 4. Lean4・公理監査

- [定理exact-source CI #42713477509](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42713477509)：**completed SUCCESS**。Scoped Strict Lean **9,125/9,125**、Governance **5/5 SUCCESS**、変更Lean error/warning **0/0**。
- [公開exact-source CI #42714359073](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42714359073)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,386/10,386**、Governance **30/30 SUCCESS**、変更Lean error/warning **0/0**。
- 新規**41宣言すべて**に `#print axioms` を配置。双方の実Leanログで **31宣言は公理不要、残り10宣言は標準 `propext` または `Quot.sound` のみ**を確認。新規 `sorryAx`／任意公理なし。
- ソース・test-merge・squash Git tree一致は、それぞれのCIで型検査した対象が最終統合されたソースに一致することのGit上の検証であり、全WORLDの正当化へ自動的に拡張しない。

## 5. 論理境界と次段

`SelectedInheritedOldInnerBracket` は旧18D構成子の**内側の形状**を読むが、`unitLeft` や `unitRight` の依存添字・元の `before/F/G/C/after` 証拠値をそのまま復元するものではない。同じ自由構文木を持つ異なる元旧18D Type値の識別性、全新商クラスの分類、全証拠Type値の再構成は**NO_DATA**。

次段Qi v5.74では、この内部構文木まで追加した結合観測について、真正同一fiberの新たな識別障害または制限した構文クラスでの忠実性を検証する。今回の証拠対は内部構文木で区別されるため、そのまま次段の非単射反例に流用しない。

任意異端点fiber非空性、20D gluing、全WORLD descent、制度的・外部action authorityは未認証。append-only／tighten-only／overwrite-forbidden／same-root。元18D Type値・独立旧新19D比較・公開root107・固定Lean/mathlib・保護#1558 Draft／OPEN／未マージを保持。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
