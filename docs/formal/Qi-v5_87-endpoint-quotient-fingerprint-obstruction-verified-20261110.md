# Qi v5.87 — 真正17D商同一・元旧18D内部括弧同一でも依存型証拠総空間は非単射（Lean4認証）

2026年11月10日 JST。canonical正本：`itakura-hidetoshi/KuuOS` の `main`。元の17D／旧18D依存Type、元17Dの真正18D比較とその商、元旧19D・新19D比較を変更せず、型付き証拠を保った**総空間**でのobstructionを扱う。「空」「縁起」「二諦」「中道」と形式構造の対応は命名・解釈の層であり、宗教哲学的同一性をLeanが証明したものではない。

## 1．Canonical・形式認証・Git tree

- 基準main（Qi v5.86定理・公開import・正式記録3段階MERGED）`37a95bd6ab6212d8e3a6e3b3b5f8f40e256be21c`。
- [定理PR #3491](https://github.com/itakura-hidetoshi/KuuOS/pull/3491) **MERGED**。新規 `formal/KUOS/Architecture/QiWuxingGK5CHP77EndpointQuotientFingerprintObstructionV5_87.lean` 1ファイル・397行・21宣言・21件`#print axioms`。既存Leanファイル変更・削除なし。
- 定理認証source `6c379b23391a8af062a8adfbd2aa88a54cff0358`、squash後main `67c273926c51466476772cc1cfcc6dc492a3e7ba`。source／test-merge／squash Git tree `5f552956b1764c09a0da0f86f00b8a6111ab507d` は一致。
- [公開import PR #3492](https://github.com/itakura-hidetoshi/KuuOS/pull/3492) **MERGED**。`formal/KuuOSFormal.lean`へ`import KUOS.Architecture.QiWuxingGK5CHP77EndpointQuotientFingerprintObstructionV5_87`を1行追加のみ。既存の公開import・root107を保持。
- 公開認証source `c495a51504321dc883663988240f0f84d896231e`、squash後main `ae44b451ff0e38e736f11359c6fb18673a13c024`。source／test-merge／squash Git tree `21664c936d36e2bf6d58a1598463a3722fdeb4c0` は一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定、公開root107維持。保護validation-only PR #1558 はDraft／OPEN／未マージ。

## 2．元Typeを失わない総空間と観測の定義

同じ**16D親文脈**における真正17D端点Typeを `Seventeen(H,K)` とする。新しい総空間は元の型に基づく

`Σ J : Seventeen(H,K), Σ N : Seventeen(H,K), SelectedLocalEighteen W l r J N`

である。この`Sigma`は元raw17D端点`J,N`を証拠値とともに保持し、**単一の固定されたJ→N fiberではない**。

独立観測 `selectedV587TotalInnerBracket` は実際の旧18D証拠の内部括弧構文を読む。複合観測 `selectedV587TotalJoint` は

`(selectedEighteenClass l r J, selectedLocalEighteenInnerBracket l r M)`

と定義した。第一成分は**元17D端点の真正 selected18D quotient class**であり、元旧・新19D商とは別物である。第二成分はv5.73で認証済みの独立raw括弧観測。これを元の依存型証拠と同一視しない。

## 3．総空間における具体的衝突と正確な識別条件

任意の真正17D端点`J`について、`strict J : SelectedLocalEighteen W l r J J`を**実際の元証拠値**として総空間に埋め込む。その埋込はraw端点を保持するため単射である。全`J`について `innerBracket(strict J)=oldStrict`。

strict-loop像上では、**joint観測等号と元17D quotient class等号が同値**であることを独立定理で示した。従って、その像上のjoint観測単射性と、元17D quotient射影の単射性が同値。

v5.35の**実際に供給された**`before : SevenRewrite`、`F,G : ContextFrameEleven`、`C : SelectedContextualThirteen`、`after : SevenRewrite` について、

`J = selectedSeventeenUnitPrependLeft ...` と `N = selectedSeventeenUnitAppendLeft ...`

は元17D raw Type値として`J≠N`。一方、v5.36の元`SelectedLocalEighteen.unitLeft`比較により**本来の17D商**で`[J]18=[N]18`。その結果、二つの真正`strict J : J→J`と`strict N : N→N`は総空間において**異なる元証拠値**だが、共に`oldStrict`を観測し、元17D商クラスも同じ。従ってjoint観測の総空間上での非単射と、普遍的なraw総空間復元decoderの不存在を形式証明。

同じ主張を元の`unitRight`生成元からも**独立して**証明した。左右とも元の真正17D／旧18D証拠、元selected18商を使い、代理Typeの同一視ではない。

## 4．認証の範囲・obstructionを消さない

上の二つのstrict loopは**異なる元17D端点 fiber** `J→J` と `N→N` に属している。元の`J≠N`は明示的に保たれている。商クラス`[J]18=[N]18`は型付き証拠のraw端点の等号を与えない。これを口実に、二つの元旧18D証拠を同じfiberへ**cast**して比較していない。

したがって、Qi v5.86で条件とした「同一raw17D fiber上の`M≠L`かつ`innerBracket(M)=innerBracket(L)`」を**無条件に構成したという主張はしていない**。元旧5／新7 selected19 Type値比較も、異なるraw端点の間では直接形成しない。任意の`before,F,G,C,after`の居住性や接続証拠を無条件に仮定しない。総空間での局所観測衝突を、fixed-fiberでの大域的結論に昇格しない。

## 5．CI認証・公理監査

- [定理exact-source CI #42815901143](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42815901143)：terminal SUCCESS。Scoped Strict Lean **9,139/9,139**。Governance・独立Kuu Core 成功。初回の形式検証で型検査成功、修正による前提弱化なし。
- [公開exact-source CI #42816694373](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42816694373)：terminal SUCCESS。`KuuOSFormal` Strict Lean **10,400/10,400**、Governance選択ジョブ **30/30 SUCCESS**。
- 両CIで実際の21件`#print axioms`出力を確認：**21/21＝公理不要15／標準`Quot.sound`のみ6**。新規`sorryAx`なし、変更Lean warning/error 0/0。
- 定理／公開の各段階で、exact source、事前test-merge、最終squashのGit tree一致を独立照合済み。CI結果は**そのsourceとその定理の範囲**の認証であって、世界横断的権限を生じない。

## 6．次段 Qi v5.88 と未認証事項

次段は、同一**元raw17D exact fiber**の真の証拠衝突を可能にする具体的な依存型構成条件の追加探索、またはstrict-only fragmentなど成立不能範囲の形式証明。上の総空間衝突を同一fiberに勝手に移さない。

無条件の同一raw fiber衝突、任意の上位`SevenRewrite`／接続証拠の居住性、異なるraw17D端点の貼合、元旧新19D Typeの大域同値、WORLD／20D gluing、実行権限は**NO_DATA／未認証**。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
