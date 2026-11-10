# Qi v5.77 — 全v5.76観測が一致しても残るstrict-only非結合鎖の枝形障害（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は元の真正contextual18D依存Type値、元selected19（5構成子）と独立新raw congruence selected19（7構成子）の実Type値比較、同一の正確な17D端点fiberにおける真正商である。「空」「縁起」との哲学的対応は命名・解釈層に限り、Leanの数学的証明と同一視しない。

## Canonical正本と来歴

- Repository `itakura-hidetoshi/KuuOS`、canonical `main`。起点はQi v5.76まで正式統合済みのmain `179f835b5544b6ff578441ea8ef3726e5f442a2d`。
- [定理PR #3461](https://github.com/itakura-hidetoshi/KuuOS/pull/3461) MERGED。新規Lean1ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77StrictOnlyBranchShapeResidualV5_77.lean`、558行追加、既存ファイル変更・削除0。新規38宣言、全38件の明示`#print axioms`。
- 定理source `b38787d2f8952cd832215177aa5578ad65ba48fe`、test-merge `b51d71ff94b66accb4ae4607e5b0dc70e35fdf10`、squash `8a680c9741762be635c1b13e8ad4a5274752ab41` のGit treeはすべて `6ee06119ae8f3d219d5803a1f5a88072467bcbcc` で一致。
- [公開import PR #3462](https://github.com/itakura-hidetoshi/KuuOS/pull/3462) MERGED。`formal/KuuOSFormal.lean`にv5.77 importを一行追加、既存import削除なし。
- 公開source `ce02049027e86ddcf0dee15099c1f5eda6be3ad2`、test-merge `8f54d5e3a91c3335786f6ce8c83551c38203f7e2`、squash `169fd96dc4172cef9dab9bf70eb54b39125e2dec` のGit treeはすべて `5fd568d0810ab932dc15b34df67d1265bc42dfc4` で一致。
- 固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージを維持。

## 独立観測：strict-only鎖の最大非結合枝形

元の真正 `SelectedContextualEighteen W l r J N` Type値上で、`SelectedStrictOnlyChainTree`（`leaf`、`joined`）を独立の自由構文として導入した。`SelectedStrictOnlyBranchSummary` は次の二成分を持つ。

```text
pure : Option SelectedStrictOnlyChainTree
branches : List SelectedStrictOnlyChainTree
```

`pure`は証拠全体がraw strictとraw chainだけで構成されている場合の非結合構文木、`branches`は真のraw証拠の各位置に現れる**最大strict-only非自明鎖**を順序付きで保持する。純粋なstrict単体は枝イベントとして数えない。`chain`における二つのpure木の連結は一つの新たな最大`joined`木を作り、いずれかがpureでない場合は既存`branches`列を連結する。元の`reverse`・`whiskerLeft`・`whiskerRight`はpure根を終わらせるが、内部枝形は保持する。`inherited(old18)`は新しいstrict-only枝を作らない。

この定義が許される重要な理由は、元の旧selected19単位規則`unitPrepend`・`unitAppend`が、**真正継承葉の直前・直後のraw strict単体**だけを挿入／削除し、strict-onlyな`chain(strict,strict)`の結合形までは同一視しないことにある。旧selected19全5構成子、新selectedRawCongruentNineteen全7構成子に対する保存性を真正型付き比較証拠の帰納法で個別に証明した。新側の`rawReverse`・`rawChainRight`・`rawChainLeft`でもそれぞれのsummary変換との互換性を確認した。

**旧五構成子商・新七構成子商にそれぞれ独立した`Quotient.lift`を実装**し、旧→新商射影との因子化も証明した。元証拠Type・比較Typeの上書きや新公理追加はない。

## 全v5.76観測一致でも残る真正証拠対

実在する任意の17D端点`N`に対し、真正contextual18D Type値の構成子のみで`N→N`の二つの証拠を構成する。

```text
S = strict N
A = reverse (chain (chain S S) S)
B = reverse (chain S (chain S S))
```

両者で、**元九観測、二本の全無限`Nat→Nat`祖先塔・直接連続反転塔、完全ordered reverse-run列、v5.70単位簡約非結合raw括弧、旧18D継承葉数（0）、ordered旧18D根タグ列・完全内部構文リスト（ともに空列）、v5.74 reverse-site inherited count列（ともに`[0]`）、v5.75 orderedイベント語（ともに`[rawReverse]`）、v5.76継承葉保持括弧（ともに`reversed unit`）**のすべてが一致する。無限関数の一致には各`Nat`次数の等式と`funext`を実際に使っている。

一方、新しいstrict-only summaryは：

```text
Summary(A) = (none, [joined (joined leaf leaf) leaf])
Summary(B) = (none, [joined leaf (joined leaf leaf)])
```

という二つの異なる自由非結合木になる。これは元の真正新七構成子商上で保存される不変量なので、**商クラスが実際に異なり、両証拠を結ぶ真正新19D比較Type値は存在しない**。単なるraw文字列の違いを商の違いと取り違えていない。

従って、v5.76までの全観測をまとめた実新商観測`selectedRawCongruentFullV576QuotientObservation`は、真正に与えられた各17D端点`N→N`商上で非単射である。新summaryのdecoderと商クラス全体の逆decoderの存在も否定した。

## Lean4 exact-source / 公理実監査

- [定理CI #42741287136](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42741287136) は**terminal SUCCESS**：Scoped Strict Lean **9,129/9,129**、選択Governance・Core Autonomy SUCCESS、変更Lean error／warning **0/0**。
- [公開CI #42741965023](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42741965023) は**terminal SUCCESS**：KuuOSFormal Strict Lean **10,390/10,390**、選択Governance・Core Autonomy SUCCESS、変更Lean error／warning **0/0**。
- 新規38宣言すべての実`#print axioms`を両CIログで照合。**公理なし16、標準`propext`／`Quot.sound`のみ22、新規`sorryAx`なし**。
- 定理・公開の各source／test-merge／squash Git tree一致も再観測。文書のみの正式記録はこれら既存の機械検証を記述するものであり、Lean型検査の代替ではない。

## 証明の境界と次段 Qi v5.78

今回の非単射性は、真正17D端点`N`により構成された**同一端点`N→N`の元18D証拠fiber**に限る。異端点`J→N`fiberの任意の非空性や非単射性を無条件には主張しない。新strict-only枝形観測を加えた後の全商クラスの分類・完全復元・単射性も未認証（NO_DATA）。今回の二証拠は新観測で区別されるので、次段の反例に流用できない。

20D gluing、WORLD横断降下、哲学的同一性、制度的・実行権限はいずれも未認証。append-only／tighten-only／overwrite-forbidden／same-rootを維持する。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
