# Qi v5.80 — inherited-guarded raw strict単位配置の新しい識別障害（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は元の真正contextual18D依存Type証拠、元selected19（5構成子）と独立新raw congruence selected19（7構成子）の真正Type値比較、および指定した同一端点fiberの真正商である。「空」「縁起」への哲学的対応は命名・解釈の層であり、形式的数学証明の内容とは同一視しない。

## canonical正本・source・test-merge・統合の来歴

- Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。起点はQi v5.79まで正式統合済みmain `84b2dc2dfcf109d160809137e52e44a434c0385b`。
- [定理PR #3470](https://github.com/itakura-hidetoshi/KuuOS/pull/3470) **MERGED**。新規Lean1ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77InheritedGuardedStrictReverseUnitResidualV5_80.lean`、637行追加。既存Leanファイル変更／削除0。49宣言と49件の明示`#print axioms`。
- 定理source `3ea155f4270b120e652aca9945aa0e38fe074b01`、test-merge `155275e88966c3fc6f6263c1ee650d8300884311`、squash `b773ce6e87b6e752e956e238f4547221a8e890fe` のGit treeはすべて `fcc11b31bf3f10430aeb77b0734a1202e591c447`。
- [公開import PR #3471](https://github.com/itakura-hidetoshi/KuuOS/pull/3471) **MERGED**。`formal/KuuOSFormal.lean`へv5.80定理importを1行だけ追加、既存import削除なし。
- 公開source `18d84241426ff7592e12e705ae74969b95b339ad`、test-merge `59ad2a8db6706d28dec56d50c35d645adfe71e61`、squash `cf68396b064cb4d86ebbc69f6f1be2f3766c4fb9` のGit treeはすべて `c5f7cdbff33232f25960e8b90daf7223bce939e1`。
- 固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107を保持。保護validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージを維持。

## 旧selected19の単位規則の正確な境界

元`SelectedLocalNineteen`の`unitPrepend`／`unitAppend`は、真正な旧18D Type値`M`を継承した`inherited M`の直前・直後へraw `strict`を一つ置く操作に対してのみ、比較証拠を与える。

この事実は、任意のraw `reverse`やraw `chain`の左右でstrictを自由に消去できるという一般単位律ではない。本研究ではこの区別を消さず、元の比較関係に新しい構成子を追加していない。

新たな独立`SelectedInheritedGuardedRawTree`は、`inherited`・`strict`・`reversed`・`joined`の自由な非結合構文木である。`selectedInheritedGuardedRawJoin`が直接簡約するのは次の2式だけ：

`join(strict, inherited) = inherited`

`join(inherited, strict) = inherited`

他のraw joinを勝手に同一視しない。元の真正依存contextual18D証拠の六構成子を構造再帰でこの補助構文木に写す。元Type値自体は上書きしない。`whiskerLeft`／`whiskerRight`は内部観測を維持する。

## 真正型付き比較の保存と両商への独立降下

- 元の旧selected19全5構成子で新観測が保存されることを、真正比較証拠に関する帰納法で証明。特に`unitPrepend`と`unitAppend`は上記2つの正確な式を使う。
- 新`SelectedRawCongruentNineteen`の全7構成子でも保存。raw `reverse`、左右raw `chain`の合同性を構造的に証明。
- 元5構成子商`selectedNineteenSetoid`、新7構成子商`selectedRawCongruentSetoid`それぞれへ独立した`Quotient.lift`を構成。旧→新商射影との因子化を証明。旧新Type値比較そのものを同一視しない。

## v5.79全観測が一致する真正18D証拠対

任意に与えられた真正17D端点`N`に対し`S = strict N`として、同一真正`N→N` fiberで元18D構成子だけから次を作る。

`A = chain (reverse S) S`

`B = chain S (reverse S)`

両者の元九観測、二本の**全Nat→Nat無限塔**、ordered反転run、v5.70単位簡約非結合raw括弧、旧18D継承葉数・ordered根タグ・完全内部構文、v5.74 reverse site列`[0]`、v5.75イベント語`[rawReverse]`、v5.76継承葉保持括弧`reversed unit`は一致する。無限塔は全次数の等式と`funext`で証明した。

さらにraw chainの一方の子がreverseであるため、最大の**非自明strict-only鎖は存在しない**。従ってv5.77枝形summary、v5.78反転祖先深度summary、v5.79左右経路summaryはそれぞれ両者で`(none, [])`に一致する。以前の完全観測を捨てたり有限サンプルへ弱めたりせず、真正新商上の`selectedRawCongruentFullV579QuotientObservation`全体が等しいことを証明している。

対して新`SelectedInheritedGuardedRawTree`観測では：

`G(A) = joined (reversed strict) strict`

`G(B) = joined strict (reversed strict)`

となり、自由補助構文木の値は異なる。新観測の真正新商への独立降下を使い、**新7構成子商クラスの不一致**、**真正新19D型付き比較の不存在**、指定した`N→N`商での**v5.79全観測非単射**、新guarded treeおよび商クラスのdecoder不存在をLean4で形式証明した。証拠のraw文字列が違うというだけでは商の非同一性を主張していない。

## exact-source Lean4 CI／公理の実監査

- [定理CI #42754490773](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42754490773) **terminal SUCCESS**：Scoped Strict Lean **9,132/9,132**、Governance・Core Autonomy SUCCESS、変更Lean error/warning **0/0**。
- [公開CI #42755012580](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42755012580) **terminal SUCCESS**：KuuOSFormal Strict Lean **10,393/10,393**、関連選択Governance・Core Autonomy SUCCESS、変更Lean error/warning **0/0**。
- 新規49宣言全件の`#print axioms`実出力を定理・公開側ログで再照合：**公理なし15宣言**、標準`propext`／`Quot.sound`のみ**34宣言**。新規`sorryAx`なし。
- 定理側と公開側のsource／test-merge／squash Git treeはそれぞれ完全一致。文書の記述は実CIとLean形式成果物の代替ではない。

## 証明の範囲・次段Qi v5.81

証明したのは、実際に与えられた17D端点`N`が作る**同一`N→N` fiber**での局所非単射性である。任意の異端点`J→N` fiberの無条件非空性、旧新商の大域完全分類や完全忠実性、20D gluing、WORLD横断降下、制度的・実行権限は未認証（NO_DATA）として保持する。

次段Qi v5.81では、今回の正確な継承証拠保護付きraw構文観測まで加えた後の識別限界、whisker層に残る履歴、あるいは特定部分presentationでの条件付き忠実性を独立して検証する。今回のA/Bは新guarded tree値で区別されるため、次段の非単射反例にそのまま流用しない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
