# Qi v5.78 — strict-only枝形が一致しても残るraw反転祖先深度の識別障害（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は真正な元contextual18D依存Type証拠、旧selected19（5構成子）と独立な新raw congruence selected19（7構成子）の実Type値比較、および固定端点の真正商である。数学的構成と「空」「縁起」の哲学的命名層は区別する。

## Canonical正本・検証の来歴

- Repository: `itakura-hidetoshi/KuuOS`、canonical `main`。起点はQi v5.77まで正式統合済みのmain `eb03843bc2bff45f2aae2e6e45b910ec912dc8e7`。
- [定理PR #3464](https://github.com/itakura-hidetoshi/KuuOS/pull/3464) **MERGED**。新規Lean1ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77StrictBranchReverseDepthResidualV5_78.lean` を560行追加。既存ファイル変更・削除0。41宣言と41件の明示`#print axioms`。
- 定理source `8b2045aa3dc18ac0f6a19eb17c742034843a5cc3`、test-merge `c9052ee92dc037aee407db56eb886b5d253d0352`、squash `7a12d1cd65cca79b0bdb214aa083e35d8b0d313b` はすべて同一Git tree `7fca8ce014fa01b1feee19e97bbaa3e11c959b21`。
- [公開import PR #3465](https://github.com/itakura-hidetoshi/KuuOS/pull/3465) **MERGED**。公開集約`formal/KuuOSFormal.lean`へ新定理importを1行だけ追加、従来import保持。
- 公開source `2cedca5350372c25f440a08cb6d9f7a59ac23190`、test-merge `360ce4f89c5294033a2b37739a01fa9f251b6cf2`、squash `5d07694e7e86105ffd00a8d1234b4c66a93de3ad` はすべて同一Git tree `c5a7ff7a10f5b0621c38514830de90b7dfd3cb56`。
- 固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107保持。保護validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。

## 新しい独立観測：最大strict-only枝のraw反転祖先深度

v5.77の`SelectedStrictOnlyBranchSummary`はpureなstrict-only非結合枝形の順序を保持するが、各枝の外側に存在するraw `reverse`の祖先個数は記録しない。v5.78では、元の真正依存`SelectedContextualEighteen`の構造再帰から、次の別の観測を定義した。

`SelectedStrictBranchDepthSummary`:
- `pure : Option SelectedStrictOnlyChainTree`
- `sites : List (Nat × SelectedStrictOnlyChainTree)`

`chain`は両子がpureなら一つの最大非自明joined枝と深度0を作り、それ以外では枝位置列を左右順に連結する。`reverse`はその内側の全枝の深度を1増す。`whiskerLeft`／`whiskerRight`はpure根を終えるがraw反転深度を増さない。`inherited(old18)`とraw `strict`単体は非自明strict-only枝を作らない。

本観測は**元旧selected19の全5構成子**、**独立新selectedRawCongruentNineteenの全7構成子**で保存されることを実Type値比較の帰納法で個別に形式証明した。旧単位規則`unitPrepend`／`unitAppend`が挿入するのは真正`inherited`葉に隣接するraw strict単体であり、非自明pure strict-only chainではない。

旧5構成子商と新7構成子商の**それぞれへ独立した`Quotient.lift`**を構成し、旧→新商射影に関する因子化も証明した。元18D証拠、旧新比較Typeそのものには変更を加えていない。

## v5.77全観測一致の新しい真正18D証拠対

任意に与えられた真正17D端点`N`に対し`S = strict N`と置き、同一`N→N`依存fiber内で以下を元の構成子のみから定義する。

- `A = chain (reverse (chain S S)) S`
- `B = chain (reverse S) (chain S S)`

両者のraw strict葉数は3、raw chain数は2、raw reverse数は1。元九観測、**両方の全無限Nat→Nat塔**、完全ordered reverse-run列、v5.70単位簡約括弧、旧18D継承葉数・根・内部構文列（空）、v5.74反転site列`[0]`、v5.75イベント語`[rawReverse]`、v5.76継承葉保持括弧`reversed unit`の値が全一致する。無限塔の同値性は各次数の証明と`funext`を使う。

さらにv5.77で追加した最大strict-only枝形summaryも**双方`(none, [joined leaf leaf])`で一致**する。従ってv5.77までの全商観測`selectedRawCongruentFullV577QuotientObservation`が一致することを、実商上で形式証明した。

しかし、新summaryの最大枝は次のように異なる。

- `Depth(A) = (none, [(1, joined leaf leaf)])`
- `Depth(B) = (none, [(0, joined leaf leaf)])`

左の枝はraw reverseの内側、右の枝はraw reverseの外側である。新summaryが新7構成子商へ真正に降下するため、**新商クラス不一致、真正新19D Type値比較の不存在**が従う。これを用い、任意の実在する`N`の`N→N`商上でのv5.77全観測の**非単射性**、新深度情報decoder・商クラスdecoderの**不存在**をLean4形式証明した。

単なるraw証拠文字列の差ではなく、独立に降下した商不変量によって比較不能性を示している。

## Exact-source CI・新規公理実監査

- [定理CI #42747612480](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42747612480)：**terminal SUCCESS**、Scoped Strict Lean **9,130/9,130**、選択Governance・Core Autonomy SUCCESS、変更Lean error/warning 0/0。
- [公開CI #42748192445](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42748192445)：**terminal SUCCESS**、KuuOSFormal Strict Lean **10,391/10,391**、選択Governance・Core Autonomy SUCCESS、変更Lean error/warning 0/0。公開側の関連チェックも成功。
- 新規41宣言の`#print axioms`出力を定理側・公開側の実Leanログで全件照合：**公理不要16、標準`propext`または`Quot.sound`のみ25**。新規`sorryAx`なし。
- 定理側／公開側で、source・test-merge・squashのGit treeはそれぞれ完全一致。文書側の形式記録は機械検証結果の記述であり証明の代替ではない。

## 有効範囲・未認証事項と次段

証明されたのは真正17D端点`N`が供給される**同一`N→N` fiber**での非単射性である。無条件の任意異端点`J→N` fiber非空性、全商クラスの分類、完全復元、20D gluing、WORLD横断降下、制度的・実行権限はいずれも未認証（NO_DATA）。

次段Qi v5.79では、新しい反転祖先深度を全観測へ追加した場合の識別力や、raw chainの左右位置・より深い構造が独立の商不変量として残るかを、あらためて真正型付き証拠上で検証する。v5.78のA/Bは新しい深度観測により区別されるため、次段反例には再使用しない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
