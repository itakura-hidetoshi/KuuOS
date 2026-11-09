# Qi v5.65 — 全無限祖先塔と隣接反転数の独立性：形式証明・公理監査

2026年11月9日 JST。**認証済みの対象は、全自然数次数の反転祖先数塔＋完全ordered raw trace＋最上位反転flagから、隣接反転数を復元できないこと**である。隣接反転数を含む既存九観測の完全分類・非単射性をこの具体的対から推測しない。

## canonical正本と形式証明の来歴

- Repository `itakura-hidetoshi/KuuOS`、canonical `main`。出発元Qi v5.64 main HEAD `1f864d6e817efc4397a0380bfb2ecfe8ccc5408c`。
- 定理 [PR #3425](https://github.com/itakura-hidetoshi/KuuOS/pull/3425) **MERGED**。新規 `formal/KUOS/Architecture/QiWuxingGK5CHP77FullAncestorTowerAdjacencyIndependenceV5_65.lean`、**462行追加・削除0**、元のLean source、旧selected19比較、新7構成子比較、18D型付き値・依存端点・既存import・workflowは変更なし。
- 定理exact-source HEAD `11ea98d12af2f71bdb58623d48cefeef99aa4786`、squash `9c6172a70bccd22d7b6832f9a2f8df39a02460b1`。source／test-merge／squash Git tree `fff4ce1ce15dc10a1275d8f2584302b7787a14db` 完全一致。
- [定理CI #42613890666](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42613890666) **completed SUCCESS**。Scoped Strict Lean **9,117/9,117**、Governance **5/5**、29新規宣言の実公理監査、exact-head受領書 **2件SUCCESS**、変更Lean error/warning **0/0**。
- 公開 [PR #3426](https://github.com/itakura-hidetoshi/KuuOS/pull/3426) **MERGED**。公開集約`formal/KuuOSFormal.lean`へ**import 1行のみ追加・削除0**。source HEAD `e99856b27941a1c8c286ad41c3412b7353c61699`、squash `216369bfaf407b5d825cce5bdbb2c0e08bb6e6db`。source／test-merge／squash Git tree `60dd5b20d8ce5575248fd54fa50140a96bd329d5` 一致。
- [公開CI #42614676906](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42614676906) **completed SUCCESS**。全KuuOSFormal Strict Lean **10,378/10,378**、Governance **30/30**、29宣言の公理結果一致、変更Lean error/warning **0/0**、exact-head受領書 **2件SUCCESS**。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` pin、公開root **107**を維持。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) は Draft／OPEN／未マージ。

## 真正18D raw証拠対

元の依存型`SelectedContextualEighteen W l r N N`を維持し、与えられた真正17D端点`N`で、次の構成子だけで作る。

```text
S := strict N
R := reverse S
A := chain (reverse (chain R S)) S
B := chain (reverse R) S
```

元の`selectedAncestorTowerByProof`は、C₀=1という形式的seedを持ち、raw reverseは一段下の計数を加え、raw chainは正の次数を和として保持する。ここで`chain R S`と`R`のCₙが**全nで一致**することを、n=0とn+1に分けて証明する。raw reverseとraw right strict-chainによるこの等式の保存も別々に証明した。結果：

[
\boxed{\forall n\in\mathbb N,\quad C_n(A)=C_n(B)}
]

元の完全ordered raw traceも一致（両方空列）、最上位raw reverse flagも一致（両方chainなので0）。

一方で、既にv5.53で**独立した新商不変量**であることを確認した`selectedContextEighteenAdjacentReverseCount`は、この具体的元証拠対について

[
\operatorname{Adjacent}(A)=0,\qquad
\operatorname{Adjacent}(B)=1
]

と厳密に異なる。Aでは二つのraw reverse間にchainが挟まって直接隣接しないが、Bでは二つのreverseが直接入れ子になるためである。この観測はv5.50の**7比較構成子全部で保存済み**のため、AとBの真正新商クラスは異なり、Type値の新19D比較も存在しない。

## 元の実在する任意fiberへの局所輸送

実際の`M : SelectedContextualEighteen W l r J N`が**与えられたときのみ**、`chain M A`と`chain M B`を元の同一J→N fiberに構成する。全Cₙの一致、ordered traceの一致、top reverse flagの一致は右連結で保存される一方、隣接反転数の右左差は正確に+1のまま残る。

ここで、実在する新7構成子商上に

[
\mathrm{Obs}_{\infty}(q)=
\left(
\mathrm{Trace}(q),\mathrm{TopReverse}(q),
(n\mapsto C_n(q))
\right)
]

を定義した。このcodomainは`(List Bool × Nat) × (Nat → Nat)`であり、有限近似ではなく**本当に無限関数型の全塔観測**である。型付き商クラス対が同じ`Obs_∞`を持ち、Adjacentだけで区別されることを形式証明した。

その結果、与えられたMのある各元fiberで、`Obs_∞`の非単射性、Adjacentを復元する全域関数の不存在、全クラスdecoderの不存在を証明。指定`J`の`J→J` fiberには真正`strict J`があるため、特別なinhabitance仮定なく非単射性が成立する。

## 機械的公理監査

新モジュールの29宣言全部へ`#print axioms`を設け、定理CIと公開CIの実ログを照合した。

- **公理不要20宣言**：元raw証拠4定義、全Cₙ保存の型付き補題、trace/top/adjacentの具体計算、真のJ→N輸送の計算補題、全塔・複合観測の定義など。
- **標準公理のみ9宣言**：商クラス分離、比較不存在、商観測の等式、非単射性、Adjacent/class decoder不存在など。実ログの依存は`propext`と`Quot.sound`のみ。
- 新規sorryAxや新規公理なし、変更Lean error/warning **0/0**。Build成功件数は定理 **9,117**、公開 **10,378**。

## 証明範囲と残る障害

**証明済み**：全自然数次数の祖先塔と、完全ordered raw trace・最上位reverse flagを同時に観測しても、新商の独立した隣接反転数は復元できない。これは有限サンプリングではなく**全無限塔**に対する具体的障害。

**NO_DATA／未認証**：既存九観測（隣接反転数を含む）と全無限祖先塔を合わせた観測の単射性・完全分類、その他の独立不変量との結合分類、任意異端点fiberの存在、異fiber whiskering、20D gluing、全WORLDへの貼合、制度的実行権限。

v5.51で既証明の旧`LeftNestedCount`等の新商非降下障害と、旧selected19商／新7構成子商の区別を保持する。命名層の「空」「縁起」の対応付けは解釈であり、このLean定理だけから哲学的同一性は証明されない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
