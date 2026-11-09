# Qi v5.67 — 既存九変量＋全無限祖先塔＋三連続反転数でも残る四連続反転障害（Lean4形式証明・公理監査）

2026年11月9日 JST。**数学的主張の対象は元の依存型18D raw証拠と、旧selected19とは別に定義された新7構成子19D比較から形成した真正商の同一fiberである。** 形式定理を「空」「縁起」と関連づけることは解釈（命名層）であり、Leanがその哲学的同一性を証明するわけではない。

## 唯一の正本・変更来歴

- Repository: `itakura-hidetoshi/KuuOS`。canonical branch: `main`。開始時のQi v5.66統合済みHEAD `f25d20fba5352c13bdfffb51f67e66a7f8b359de`。
- [定理PR #3431](https://github.com/itakura-hidetoshi/KuuOS/pull/3431) **MERGED**。追加ファイルは `formal/KUOS/Architecture/QiWuxingGK5CHP77NineFullTowerTripleQuadrupleResidualV5_67.lean` の1件のみ（最終654行追加、既存ファイル削除0）。修正後HEAD `0b9acdcb82ea0275954115eb7c1057a3ce0ca4bf`、squash commit `3dea29947a3c3a4c9a02da56440c84753fc07a3b`。
- 定理[exact-source CI #42632280137](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42632280137)：**completed SUCCESS**。Scoped Strict Lean **9,119/9,119**、Governance **5/5**、39宣言の実公理監査、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source/test-merge/squash Git treeは `3cded91226bd5e1442510194ca0f63d4b330bb1a` で一致。
- [公開import PR #3432](https://github.com/itakura-hidetoshi/KuuOS/pull/3432) **MERGED**。`formal/KuuOSFormal.lean`へのimport **1行のみ追加**、削除0。source HEAD `aeb60cc7d31e5b352ae3dced4cfc3f34c78d6612`、squash commit `e0faa4e4e0b338944a86f7f0e778f4be3caebe3f`。
- 公開[exact-source CI #42633542689](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42633542689)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,380/10,380**、Governance **30/30**、39宣言の公理監査が定理CIと一致、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source/test-merge/squash Git treeは `1617ee4b6c00933c2972d8b6acfb41949a3c4bb7` で一致。
- 固定：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root **107**。保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージのまま。

## 真正18D証拠と同一観測・異なる四連続反転数

前段Qi v5.66で得た3連続反転数は、新7構成子商で独立に保存される。今回の新反例は、その数までも一致させている。真正17D端点`N`について元の`SelectedContextualEighteen W l r N N`の本来の`strict`、`reverse`、`chain`だけを使い、

```text
S := strict N
D := reverse (reverse S)
T := reverse D
gap(X) := chain X S
A := reverse (reverse (reverse (reverse (gap D))))
B := reverse (reverse (reverse (gap T)))
```

と定義した。Aは外から**4連続＋gap＋2連続**、Bは**3連続＋gap＋3連続**という構文上の異なる履歴であり、双方ともraw reverse節は計6個。次を元Type値で証明した。

```text
∀ n : Nat, C_n(A) = C_n(B)
Trace(A) = Trace(B)
TopReverseFlag(A) = TopReverseFlag(B)
AdjacentReverseCount(A) = AdjacentReverseCount(B) = 4
ConsecutiveTripleCount(A) = ConsecutiveTripleCount(B) = 2
ConsecutiveQuadrupleCount(A) = 1
ConsecutiveQuadrupleCount(B) = 0
```

`gap`はstrict identityをchainで入れるが全次数`C_n`を変えない。gapの位置をraw reverse一個だけ移すときも全自然数次数の等式を維持することを証明し、その外側に三つのraw reverseを重ねてA/Bの全塔一致を導出した。したがって、有限個の祖先サンプルから無限への推測ではない。v5.60のC₁〜C₅橋渡しから、元の8観測の一致と第9のC₆一致を導き、完全ordered traceとtop flag、隣接反転、三連続反転も一致させた。

## 独立した四連続反転数と商への降下

新たに元18D証拠へ`selectedContextEighteenTopTripleReverseFlag`と`selectedContextEighteenConsecutiveQuadrupleCount`を追加定義。後者はraw reverseの子が最上位に三つの即時reverseを持つ場合のみ1を加え、`chain`では左右の部分木の数を加算し、`whiskerLeft`／`whiskerRight`では内側の数を保持する。元selected19の全5構成子と、新raw congruenceの全7構成子における保存を**別々に構造帰納法で証明**した（rawReverseは別途保存したtop-triple flagを使用）。

元商・新商それぞれで`Quotient.lift`による真の商不変量を定義し、旧商から新商へのprojectionで因子化することも証明。四連続数の**1対0**から、A/Bの新商クラスは相異なり、型付き新19D比較値は存在しない。比較生成元を付け足して結論を得たのではなく、既存の7構成子を保持した。

## 真正の同一fiberへの輸送と10番目を越える障害

実際に`M : SelectedContextualEighteen W l r J N`が**与えられた場合に限り**、`chain M A`と`chain M B`を元と同一のJ→N fiberへ構成する。九観測、全`Nat→Nat`祖先塔、三連続反転数はなお一致し、四連続反転数の差1が残る。

既存の真の商写像`selectedRawCongruentNineFullTowerObservation`と、新商の独立した三連続計数を組み合わせ、

```text
Obs_(9+infinity+triple)(q) =
  (selectedRawCongruentNineFullTowerObservation(q),
   selectedRawCongruentConsecutiveTripleOnQuotient(q))
```

を定義。実際のMを供給したfiberでこの**商観測は非単射**、四連続数decoderと全商クラスdecoderは存在せず、J→Jのstrict raw証拠による明示例も存在する。前段v5.66の反例を流用せず、三連続計数まで一致する新証拠対を構成している。

## 39宣言の公理監査・修正経路

- 新規**39宣言**全件に`#print axioms`。修正後定理CIと公開CIを実ログで照合し、**14宣言は公理不要**、**25宣言は標準`propext`／`Quot.sound`のみ**。`Classical.choice`、新規公理、`sorryAx`は追加されない。
- 初回定理CI #42631537301 は`selectedQuadrupleWitnessFiber_quadGap`の末尾で`rw`がゴールを閉じた後にさらに`omega`を適用し`No goals to be solved`でFAILURE。変更ファイル全文と依存するv5.65／v5.66のsignatureを点検し、**余分な`omega`1行だけ削除**した。仮定・定理文・元証拠・既存比較は不変。修正後CI #42632280137で9,119/9,119成功。
- 両認証段階でexact-head受領書が2件ずつSUCCESS、真正Git treeのsource/test-merge/squash一致を確認。これは**当該形式証明の機械検証**であり、全WORLDへ無条件に降下したことや実行権限を与えるものではない。

## 未認証境界と次段の検討

この定理から、**新たに四連続反転数を観測へ追加したときの完全識別性は導けない**。その段階は未認証（NO_DATA）。次段では反転連続長一般`k`の不変量について構造再帰・商保存と、`[k,k−2]`対`[k−1,k−1]`（k≧4）の同型の障害が本当に成立するかを具体的に検証できるが、現段階で全kの定理を主張しない。

任意の異端点fiberの非空性、異fiber whiskering、20D gluing、全WORLDの大域貼合、全商の完全分類、制度的な行為権限は未認証。元18Dの真正依存Type値、旧selected19と新7構成子商の区別、root107、固定Lean/mathlib、保護#1558 Draft/OPEN/未マージを維持。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
