# 真正C60のグラフ主体の表示からゲージ表示への移行

**研究レーン:** F112 C60 gauge-first / Qi v3.4 / K₅非可換高次境界  
**基点:** canonical `main` の `e7fc499381cdf7a53442b293fd742ff61ff3ee53`（F112-P94D3I）  
**実装PR:** [#2510](https://github.com/itakura-hidetoshi/KuuOS/pull/2510)（検証中の差分はマージ前の定理正本ではない）

## 目的と厳密な置換境界

C60の研究で**グラフの接続性・隣接や図の一致だけをcoherence、descent、Type値高次セルの根拠として用いる経路を退ける**。代わりに、真正のC60入射・F45/F54/F55のType値証拠を保つゲージ接続・ゲージ変換・曲率・非零障害を証明して使う。

これは「グラフとして正しく証明されていた数学を削除する」指示とは区別する。原幾何の有限入射、歴史的Quiver、Catalan型のK₅有限形状、raw no-goやH₁・H₂計算は、それぞれ独立の定理として有効であり、削除すると現在の107公開rootや既存の真正性証明を破壊する。**現行の前向きの意味付け・ゲージでの比較先を切り替える**ことを対象とし、有限入射や証明履歴をなかったことにしない。

| 以前のグラフ・Quiver表示 | 以後のゲージ表示の正本入口 | 物理的・数学的に残すもの |
| --- | --- | --- |
| C60の原60 Dart／90 Edge／32 Polygon、182入射サイトと360旗の入射経路 | [Native C60 site gauge](../formal/Kuu/F112/PolygonNativeC60PhysicalGaugeAtlas.lean) — 加法ゲージ接続、実際のF69 `Zigzag` に沿う積分、局所ゲージ・軌道・非零曲率 | 全真正幾何、実際の入射、raw経路とその異同、五角形・六角形、整数鎖複体 |
| K₅の14括弧付け／21回転／9面のグラフシェリング（F112-P94D1–D3I） | [Native K5 typed gauge](../formal/Kuu/F112/PolygonNativeC60K5TypedGaugeCoherence.lean) — 真正型付き9面の順序付き非可換語、共役ゲージ、自然性数とF55 shadow、4-cellへの非降下 | 14/21/9の有限計算と真正F54型付き21辺、9つのF55/P92B型付き面、自然性数+1、既存no-go |
| 五行の五芒星Quiver（歴史的v5.169） | [Qi v3.4 actual C60 phase gauge](../formal/KUOS/Architecture/QiWuxingNativeC60GaugeV3_4.lean) — 群 \(\mathbb{Z}/5\mathbb{Z}\) の局所位相枠、12真正五角形の5スロットとDart、相生1・相剋2の群作用 | 旧五行型付き自由路、相生と相剋の異なる元の生成史、旧Quiver定理（歴史的証拠として保持） |
| C60の入射グラフ接続を用いた歴史的F109・鎖ホモトピーや観測 | 上記物理ゲージの`Zigzag`積分・閉路ホロノミーと、必要なら真正Type値transportへの比較を追加 | 実際の接続証拠、原H₀／H₁／H₂の定理。GraphRAGやruntimeの汎用グラフ機能には手を触れない |

## C60入射接続のゲージ変換

真正サイトの入射 \(s\le t\) 上の値を \(A(s,t)\in G\)、真正サイトごとに選択するゲージを \(\phi(s)\in G\) とする（このPRでは任意の **可換加法群** \(G\) を選ぶ）。実際の入射以外には、ゲージ辺を構成しない。

\[
 A^{\phi}(s,t)=A(s,t)+\phi(t)-\phi(s).
\]

元の真正raw F69 zigzag \(z:s\rightsquigarrow t\) に対して、前向き脚を正、逆脚を負として計算する（raw脚を消去しない）。

\[
 \operatorname{Hol}_{A^\phi}(z)
 =
 \operatorname{Hol}_{A}(z)+\phi(t)-\phi(s).
\]

この式をraw `Zigzag` の全生成構文についての帰納法で証明する。したがって閉路 \(z:s\rightsquigarrow s\) のホロノミーはゲージ不変。原360旗の二段経路と斜辺の差、および原32面の10／12脚の境界積分の曲率も不変。

この新ゲージ場は**別途選択する独立した加法接続**である。歴史的F55やF68で構成された各曲率（例：北面で非零）との同一性は、元の証拠・荷電を接続へ運ぶ比較定理がない限り主張しない。どのゲージも元の非零曲率を勝手に零にしない。

## K₅のゲージと障害

K₅の真正原F55/P92Bの9面を、**向きと非可換順序を固定**した
`pentagon7, square0, pentagon5, pentagon8, square1, pentagon3, pentagon6, square2, pentagon4` の順序で読む。数値shadowから3-cellを捏造しない。

群語 (W) に対してゲージ枠 (g) による変更は \(W\mapsto g+W-g\)（`FreeAddGroup` の非可換加法記法）とする。新自然性数と完全旧F55 shadowはそれぞれ共役に不変であり、

\[
  \nu_N(W)=1, \qquad \chi_{F55}(W)=0.
\]

既存の全真正P94A Type値4-cellが生成する正規核 \(R_{\mathrm{typed}}\) は \(\ker\nu_N\) に含まれるため、任意の \(g\) について \(g+W-g\notin R_{\mathrm{typed}}\)。よって**ゲージ変更自体は、既存P94A/P94C2では作れない4-cellを生成しない**。

ただし (W) は9個の**個々には真正Type値の面証拠**から作る形式的群語であり、それらの間の全F54経路transportと全球面3-cell貼り合わせが構成されたわけではない。独立4次元pentagonatorのcoherenceも未証明。

## 五行の局所ゲージ

\(\mathrm{FivePhase}=\mathbb{Z}/5\mathbb{Z}\)、実際の12個のC60五角形上のframe \(g(v)\) を選ぶ。真正な五辺スロットのラベルは \(\mathrm{ringSlot}(p+g(v))\)。相生は変位1、相剋は変位2であり、チャート変更に対して両方の移動は可換である。一方、**一つの相剋arrowと二つの相生arrowというType値生成履歴は異なる**ことを、既存Qi v3.1の証明とともに保つ。

## 未解決事項と禁止

- 9面の全真正F54経路への共通transport、P92B seamのType値証拠、全球面3-cellの構成。
- 4次元pentagonatorとPeiffer/horizontal/vertical高次coherence。
- 完全な局所・大域strict 3/n圏と\((\infty,3)\)-hyperdescent。
- 旧Grayの再導入、グラフの隣接からの4-cell捏造、shadow一致による充填の仮定、旧no-go／107公開root／歴史的成果の削除を行わない。

**研究方針:** 物理入射は土台のまま、ゲージは選択可能なpresentationとして扱う。独立Kuuを唯一の空とせず、一般の縁起の理論と輸送・descent・obstructionを相互に検証する。
