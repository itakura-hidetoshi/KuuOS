# Qi v5.70 — 全二重無限観測＋順序付き反転ランでも残る非結合的括弧構造の障害（形式証明・公理監査）

2026年11月10日 JST。**形式成果物の対象は、元の依存Type値18D raw証拠と、独立した新7構成子19D比較による真正商の同一fiberに限る。**「空」「縁起」とこの形式構造の対応は命名・解釈の層であり、Lean4による哲学命題の証明ではない。

## 唯一の正本・コードとCIの来歴

- Repository `itakura-hidetoshi/KuuOS`、canonical `main`。研究開始時に正式統合済みのQi v5.69 main HEAD `171d2c148300ba7a818f1858c61bd8054454e77d`。
- [定理PR #3440](https://github.com/itakura-hidetoshi/KuuOS/pull/3440) **MERGED**。新規Leanファイル`formal/KUOS/Architecture/QiWuxingGK5CHP77UnitReducedBracketShapeResidualV5_70.lean` 1件（700行追加・削除0）。認証source HEAD `6b10638d5d950b42dead986c92039bb7c8a5b634`、squash `3d44e2eecbebb01a66781aeee1c66b7aeae9c35d`。
- 定理[exact-source CI #42692161306](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42692161306) **completed SUCCESS**：Scoped Strict Lean **9,122/9,122**、Governance **5/5**、全45新宣言の公理監査、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source／test-merge／squash Git tree `3bebb711afd6466e8864b8589d841d718de2ce16` 完全一致。
- [公開import PR #3441](https://github.com/itakura-hidetoshi/KuuOS/pull/3441) **MERGED**。`formal/KuuOSFormal.lean`にimport **1行だけ追加**・既存削除0。認証source HEAD `8bafe9b2d2e5de72dac3cc7c3c7e9c8e5d560bec`、squash `c0ce3f5e5fe145038b2fc4dc357f1b687b84482b`。
- 公開[exact-source CI #42692984615](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42692984615) **completed SUCCESS**：KuuOSFormal Strict Lean **10,383/10,383**、Governance **30/30**、同じ全45公理監査、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source／test-merge／squash Git tree `5adf72e3fd40529800dba907ff9022e44047c058` 完全一致。
- 固定：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root **107**。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージを維持。

## 新しい証明済みの非結合的単位簡約括弧構造

真正17D端点`N`の同一N→N dependent fiberで、本来の`SelectedContextualEighteen`のstrict、reverse、chainだけを用いて、

```text
R := reverse (strict N)
A := chain (chain R R) R
B := chain R (chain R R)
```

を構成した。両方とも真正元18D Type値であり、別の観測用proxyの構文木に置き換えて元の証拠を消したものではない。

元証拠から独立して読む`SelectedRawUnitReducedBracket`は`unit`、単項`reversed`、二項`joined`の自由な非結合構文である。`selectedContextEighteenUnitReducedBracket`は元18D上の構造再帰で、strict／inheritedをunitへ、whiskerを内側の値へ、raw reverseをreversedへ、raw chainを単位簡約付き二項joinedへ写す。**単位は消去するが結合則を付け足さない**ため、

```text
bracket(A) = joined (joined (rev unit) (rev unit)) (rev unit)
bracket(B) = joined (rev unit) (joined (rev unit) (rev unit))
bracket(A) ≠ bracket(B)
```

が元証拠の異なる括弧構造を識別する。

この新しい観測の保存性を旧`SelectedLocalNineteen`の**5構成子**すべて、新`SelectedRawCongruentNineteen`の**7構成子**すべてに対して構造帰納法で証明した。旧unitPrepend/unitAppendで元inheritedとstrictの単位簡約が合い、新rawReverseとrawChainRight/rawChainLeftで実際の帰納仮定と構文木関数の互換性が成立する。独立する旧商・新商のそれぞれへ`Quotient.lift`で降下し、既存の旧→新projectionを通じて因子化することも証明済み。**元18D Type値、旧19D比較、新7構成子19D比較のいずれも変更していない。**

## すべての既存観測が一致する真正証拠対

AとBは、raw合成の括弧構造だけが異なり、元Type値上で以下を機械的に証明した。

```text
∀ n : Nat, AncestorTower_n(A) = AncestorTower_n(B)
∀ n : Nat, ConsecutiveRunCount_n(A) = ConsecutiveRunCount_n(B)
OrderedRunList(A) = OrderedRunList(B) = [1,1,1]
Trace(A) = Trace(B)
TopReverseFlag(A) = TopReverseFlag(B)
AdjacentReverseCount(A) = AdjacentReverseCount(B)
NineObservation(A) = NineObservation(B)
```

祖先塔・全連続反転計数の等式に使うのは、元raw chainにおける**数値計算のNat.add_assoc**であって、元18Dのraw chain自体を結合的と仮定する証明ではない。反転ランの順序付きリストも完全に一致する。別に構成した単位簡約括弧不変量が異なるため、**新7構成子商の二つのクラスは異なり、真正新19D Type値比較も存在しない。**

## 正確な同一fiberへの輸送と完全観測の非単射性

元18Dの実在する`M : SelectedContextualEighteen W l r J N`が**与えられた場合に限って**、`chain M A`・`chain M B`を同じJ→N exact dependent fiberへ構成する。既存の全祖先塔、全run-count塔、ordered-run list、九観測は一致したままである。一方で、新しい構文木上は、共通する`bracket(M)`との単位簡約付き二項joinedを経ても、**右側の異なる括弧構造が残る**ことを証明した。従って真正新商の各クラスも不一致。

結合観測を

```text
Obs_(double∞+ordered)(q)
 = (NineFullTower(q), AllConsecutiveRunCountTower(q), OrderedRunList(q))
```

として実際の新商上に定義し、供給されたMのある同一fiberで**非単射**、新たな括弧不変量の全域decoder不存在、および全商クラスdecoder不存在を証明した。任意に指定されたJ→Jには真正`strict J`があるので、その実在する証拠を使用したendomorphism版も得た。異端点fiberの勝手な非空仮定は導入していない。

## 公理監査と論理境界

- 新規**45宣言**に実際の`#print axioms`を付与。定理CI・公開CIで実ログを読み照合し、**公理不要14**、残る**31宣言は標準`propext`、`Quot.sound`、`Classical.choice`の範囲のみ**。新規axiom／sorryAxなし。変更Lean error/warning **0/0**。
- このCI SUCCESSは固定Lean/mathlib依存閉包と当該ソースに対する形式認証であり、**すべてのWORLD・全証拠の分類・制度的な行為権限**に自動的に降下するものではない。特に新しい括弧構造まで観測へ追加した場合の完全識別性は未認証（NO_DATA）。
- raw合成の結合則を**証明したのではなく**、結合則が与えられていない現行比較presentationの下で異なる括弧を保持することを証明した。

## 次段Qi v5.71（未認証）

新しい括弧形まで加えた観測の単射性を断定しない。次段では、単位簡約の仕方自体が失う原証拠の情報、あるいは異なる元Type値から同一括弧形への真のfiber、旧新商への保存条件を具体的に調べる。今回のA/Bは新括弧形で区別されるので、そのまま次段の反例にはならない。

任意異端点fiber非空性、20D gluing、異fiber whiskering、全WORLD大域貼合、制度的権限は引き続きNO_DATA。公開root107、固定Lean/mathlib、元Type値、独立旧新商と保護#1558 Draft／OPEN／未マージを維持。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
