# Qi v5.79 — strict-only枝の左右raw chain位置による追加識別障害（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は元の真正contextual18D依存Type値、旧selected19（5構成子）と独立な新raw congruence selected19（7構成子）の型付き比較、および同一端点fiberの真正商である。「空」「縁起」との対応は命名・解釈の層であり、形式的数学証明とは同一視しない。

## Canonical正本・Git来歴

- Repository `itakura-hidetoshi/KuuOS`、canonical `main`。Qi v5.78の定理・公開import・正式記録統合済みmain `eadcfeb3a6f09acf10fb5cd70691287f6da5b6c7`を起点とした。
- [定理PR #3467](https://github.com/itakura-hidetoshi/KuuOS/pull/3467) **MERGED**。新規Lean1ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77StrictBranchChainSideResidualV5_79.lean`、604行追加、既存Leanファイル変更・削除0。45宣言と全45件の明示`#print axioms`。
- 定理source `cc8bf4da45aeb543f9b36d8e1eb220417e5492b3`、test-merge `ceb0c901003c4aaac02a7e65be175b18fcf21c1a`、squash `89a31c0da8a4859a56bf7c3569b17eea11a3abae` のGit treeはすべて `8466fb8987b1c80fbd2f9fe245b18c824378241d` で一致。
- [公開import PR #3468](https://github.com/itakura-hidetoshi/KuuOS/pull/3468) **MERGED**。`formal/KuuOSFormal.lean` にv5.79定理import1行だけを追加、既存import削除なし。
- 公開source `b141d33e1319611ad89344d03e5c7ff6f892a32d`、test-merge `6bd1a1286ae087d35b27a0f5617bcd418c852f8a`、squash `6fecf722be20a546ec3341ccabfd0cdef80edc5e` のGit treeはすべて `362172f8105f2a9a5b9f6c2c196e586f87c17d98` で一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` は固定。公開root107不変更。保護validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 追加した観測：最大strict-only枝のraw chain左右経路

元の真正依存証拠 `SelectedContextualEighteen W l r J N` の上に、`SelectedStrictChainSide`（`left`／`right`）と、raw chainの外側から内側へ進む左右経路と最大非自明strict-only非結合木との対 `SelectedStrictBranchPath = List SelectedStrictChainSide × SelectedStrictOnlyChainTree` を独立に定義した。

`SelectedStrictBranchPathSummary` は次の二成分を保持する：

`pure : Option SelectedStrictOnlyChainTree`

`sites : List SelectedStrictBranchPath`

`chain`の左右が両方pureなときは一つの新たな最大joined枝を経路`[]`に記録する。それ以外では、左由来のすべての最大枝のアドレスに`left`、右由来には`right`を先頭に付し、列を順序付き連結する。`reverse`および元`whiskerLeft`／`whiskerRight`はpure根を終了させるが、raw chain左右経路自体は変更しない。旧18D継承葉やraw strict単体からは非自明pure鎖を作らない。

この観測の保存性を、**真正旧selected19の全5比較構成子**と、**新selectedRawCongruentNineteenの全7比較構成子**のそれぞれについて型付き証拠の帰納法で証明した。元の`unitPrepend`／`unitAppend`は真正`inherited`葉に隣接する単独strictの挿入・削除に過ぎず、strict-only鎖の左右位置の一般的同一視ではない。

旧5構成子商と新7構成子商へそれぞれ独立した`Quotient.lift`を実装し、旧→新商射影に関する因子化を証明した。旧・新比較Type自体を同一視していない。

## 真正18D証拠対：v5.78完全観測一致と新左右位置の相違

任意に与えられた真正17D端点`N`に対し、`S = strict N`として、元の真正18D構成子のみで同一`N→N` fiberの二証拠を定義した。

`A = chain (chain S S) (reverse S)`

`B = chain (reverse S) (chain S S)`

両者は元の九観測、二本の**完全なNat→Nat無限祖先塔・直接連続反転塔**、完全ordered reverse-run、v5.70単位簡約非結合括弧、旧18D継承証拠の葉数・ordered根タグ・完全内部構文リスト、v5.74反転site列`[0]`、v5.75イベント語`[rawReverse]`、v5.76継承葉保持括弧`reversed unit`、v5.77最大strict-only枝形`[joined leaf leaf]`、さらにv5.78深度付き枝形`[(0, joined leaf leaf)]`まで**すべて一致**する。無限塔は全次数の関数等式を`funext`で確かめ、有限サンプルへ弱めていない。

しかし新観測は次のとおり異なる：

`Path(A) = (none, [([left], joined leaf leaf)])`

`Path(B) = (none, [([right], joined leaf leaf)])`

新左右経路観測は真正新7構成子商に降下するため、**元の新19D商クラス不一致**、**二証拠を結ぶ真正新19D Type値比較不存在**が従う。これを使って、任意に供給された真正17D端点`N`の`N→N`商における**v5.78完全結合観測の非単射性**、新左右経路を復元するdecoder不存在、真正商クラスを復元するdecoder不存在を証明した。単なるraw構文文字列不一致を商比較不能性の根拠としていない。

## Exact-source Strict Lean・公理の実監査

- [定理CI #42751948688](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42751948688) **terminal SUCCESS**。Scoped Strict Lean **9,131/9,131**、選択Governance・Core Autonomy SUCCESS、変更Lean error／warning **0／0**。
- [公開CI #42752452653](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42752452653) **terminal SUCCESS**。KuuOSFormal Strict Lean **10,392/10,392**、選択Governance・Core Autonomy SUCCESS、変更Lean error／warning **0／0**。
- 新規45宣言の全`#print axioms`実出力を両exact-sourceログで照合。**公理不要17、標準`propext`／`Quot.sound`のみ28、新規`sorryAx`なし**。
- 定理・公開ともsource、test-merge、squashで同一Git tree。形式証明・CIの実ログと、説明文書の層を分ける。

## 証明範囲と次段Qi v5.80

証明対象は、実際に与えられた17D端点`N`により構成できる**同一`N→N` fiber**上の局所非単射性である。任意異端点`J→N` fiberの無条件非空性・非単射性、旧新商の大域的完全分類・完全忠実性、20D gluing、全WORLD横断降下、制度的実行権限はいずれも未認証（NO_DATA）。

次段Qi v5.80では左右raw chain経路を完全観測へ追加した後の識別力、経路・逆転深度・枝形の組が見落とす情報、および限定presentationでの条件付き忠実性を研究する。今回の証拠対は新左右経路値で区別されるので、次段の反例へそのまま流用しない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
