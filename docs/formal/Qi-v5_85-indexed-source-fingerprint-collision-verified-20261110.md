# Qi v5.85 — 添字付き旧18D証拠族の条件付き忠実性と同指紋raw観測の復元障害（Lean4形式証明）

2026年11月10日 JST。唯一の正本は`itakura-hidetoshi/KuuOS`、branch `main`。対象は元の真正依存`SelectedContextualEighteen`（18D Type値）と、互いに独立した旧5構成子`SelectedLocalNineteen`・新7構成子`SelectedRawCongruentNineteen`（19D比較Type）、両真正商および別定義のwhisker配置観測である。空・縁起との対応は命名・解釈の層であり、Leanが哲学的同一性を証明した意味ではない。

## 1．正本・機械的証明・Git tree来歴

- 前段Qi v5.84正式統合後の基準main：`912f543e83514ebb8e6bdaa89a21271f28dde249`。
- [定理PR #3485](https://github.com/itakura-hidetoshi/KuuOS/pull/3485) **MERGED**。追加は新規`formal/KUOS/Architecture/QiWuxingGK5CHP77IndexedSourceFingerprintCollisionV5_85.lean`（382行・14宣言・14件の独立`#print axioms`）のみ。既存Leanファイルの変更・削除はない。
- 定理認証source `970ac38081b50081b7ded5f140a7e13d525ead16`、統合squash `78100f357db2e89ea7357dda7d5663863f2e0340`。source／事前test-merge／squash Git tree`c57e72034d15357982654132817682597baf19b5`が一致。
- [公開import PR #3486](https://github.com/itakura-hidetoshi/KuuOS/pull/3486) **MERGED**。`formal/KuuOSFormal.lean`へ`import KUOS.Architecture.QiWuxingGK5CHP77IndexedSourceFingerprintCollisionV5_85`を1行追加のみ。公開root107と既存importは変更なし。
- 公開認証source `3a43431f5bfbd7746bfcf23812080636ca2642a9`、統合squash `99ae3a1311b69177146414c57e007c09cd3ba0a2`。source／test-merge／squash Git tree`03ed3524fb092d906e9e7d5edbf0dff61a7d55c9`は一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定。validation-only [保護PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 2．実際に与えられた添字付き旧18D証拠族

真正の右`ContextFrameEleven F G`、`after : SevenRewrite`と元17D端点`N`を**与え**、実際の右whiskered端点を`N' = whiskerRight F G N after`とする。添字Type`ι`について、**別途与えられた真正元旧18D証拠族**
`sources : ι → SelectedLocalEighteen W l r N' N'`
を用いる。次の仮定は**追加条件**であって全源についての主張ではない。

`Function.Injective (fun i : ι => selectedLocalEighteenInnerBracket l r (sources i))`

この`innerBracket`指紋の単射性は、与えられた族の条件であり、任意`ι`や`Fin n`に対応する証拠の居住性を自動的に作るものではない。

## 3．局所的忠実性の形式認証

上の**明示した単射性条件**のもと、元の`inherited (sources i)`を**元18D Type値のまま**使用し、次をLean4で証明。

- 旧5構成子の真正selected19商クラスの`i ↦ [inherited (sources i)]_old`は単射。
- 新7構成子の**別の**真正selected19商クラスの同写像も単射。
- `reverse (inherited (sources i))`の**実際の新7構成子商クラス**も単射。
- 元旧・元新の別々の19D Type値比較の`Nonempty`はそれぞれ`i = j`と同値。**比較Type同士の同一視ではない**。
- 全旧v5.80観測（元九観測、二本の**全Nat→Nat無限塔**、その他の確認済み座標）と独立v5.81配置木の直積`SelectedFullV581QuotientObservationValue`は、**反転guard付きの当該像上**で指紋の単射性を反映する。
- 添字`Fin n`での3種類の単射性を、任意に**供給された**有限族について別定理として構成した。`n`個の異なる旧18D証拠の無条件存在は主張していない。

各主張は同一の真正右whiskered`N'→N'` fiberに限定され、左・右fiberの無条件輸送や全19D商の完全分類には拡張しない。

## 4．同じ`innerBracket`指紋を持つ2源の条件付き障害

同じ右fiberに真正に**別々に与えられた**`M,L : SelectedLocalEighteen W l r N' N'`について、v5.81の**配置木だけ**なら

`obs(inherited M) = obs(inherited L) ↔ innerBracket(M) = innerBracket(L)`

と、1回のraw反転guard後の同様の必要十分条件を形式証明した。

さらに**追加で**`innerBracket(M)=innerBracket(L)`かつ元旧18D Type値として`M≠L`が実際に成立するなら、配置木から**この2つのraw元旧18D証拠値を同時に復元するdecoderは存在しない**。したがって、そのfiber全体に対するこの配置観測だけからの元raw旧18D復元器も存在しない。

重要な境界：この条件を満たす具体的`M,L`が無条件に存在するとは証明していない。**配置木の観測一致から、真正旧・新19D商クラスが一致する／しないとは推論していない**。また、完全`FullV581`観測全体が衝突したとも主張していない。局所観測の不足を全商の結論へ昇格させず、obstructionを条件付きで保存する。

## 5．Exact-source CI・公理監査

- [定理CI #42781220874](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42781220874)：**terminal SUCCESS**。Scoped Strict Lean **9,137/9,137**、選択Governance・独立Kuu Core SUCCESS。新規ファイルは初回のLean型検査で成功、定理の弱化・既存ソース変更を伴う修正なし。
- [公開CI #42781789198](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42781789198)：**terminal SUCCESS**。公開`KuuOSFormal` Strict Lean **10,398/10,398**、選択Governance **30/30 SUCCESS**。
- 両CIの新規`#print axioms` **14/14出力**を確認：**公理不要0／標準`propext`・`Quot.sound`のみ14**。新規`sorryAx`なし、変更Lean error／warning 0／0。これは対象14宣言に限る公理監査であり、全mathlib等に対する大域主張ではない。
- 定理・公開それぞれでsource/test-merge/squash Git treeが一致していることをGitHub Git dataから再照合した。実行ログと本記録は、元の証明が示す範囲を超える権限を与えない。

## 6．未認証の境界と次段Qi v5.86

任意の`ι`／`Fin n`での証拠族の無条件居住性、全証拠の指紋単射性、等しい指紋で異なる元旧18D Type値の具体的証拠対の無条件構成、同指紋からの旧新商クラス比較、完全`FullV581`観測全体の非単射性、任意fiberの完全分類、旧・新Type19Dの大域同値、WORLD横断降下、20D gluing、実行権限は**NO_DATA／未認証**。

次段v5.86候補：同じ内部括弧観測をもつ元証拠の存在条件を**元依存Type内で**検討し、追加独立観測とその旧5／新7生成元での保存条件を確かめる。観測だけで全源復元や全商貼合を仮定しない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
