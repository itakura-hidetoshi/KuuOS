# Qi v5.26 — 元whiskering履歴長と型付き文脈作用の単位・同側合成障害

## 0. 正本・exact-source検証

2026年11月8日 JST。唯一のcanonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.25の定理#3302・正式記録#3303、公開集約追加#3304およびREADME/ROADMAP同期#3306を継承した。
従来の真正元F55/P77/GK5CG、元6D〜14Dの全Type値証拠、v5.25の文脈閉包presentationを改変していない。

| 項目 | 正式確認 |
|---|---|
| 定理PR | [#3305](https://github.com/itakura-hidetoshi/KuuOS/pull/3305) **MERGED** |
| 独立source初回HEAD | `d0f2880f4d1dc1ec322350406ae0320415a03ad2` |
| canonical mainを継承したsource HEAD | `8a7f38b6fae1efc37b002ae59d023b55942842ed` |
| source対応test-merge | `609f97366d7577eeb86aa7b24e953f475034bf17` |
| 定理squash main | `02c5db8462ba363aef46180845818e249e3e12b7` |
| 上記最終source/test-merge/squash Git tree | **`7f3ee65e2abf5e96f3190ed00e36e5e99c1859f2` 完全一致** |
| 最終exact-source CI | [#42443161009](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42443161009) **SUCCESS** |
| Scoped Strict Lean | **9,078 / 9,078 SUCCESS** |
| Governance | **選択5 / 5ジョブ SUCCESS** |
| 新規宣言の公理監査 | **17 / 17**：8件公理不要、9件標準公理のみ |
| `sorryAx`／新公理／変更Lean error・warning | **なし／なし／0・0** |
| 定理差分 | 独立新規Leanファイル1件、245行追加・削除0 |
| 公開集約PR | [#3307](https://github.com/itakura-hidetoshi/KuuOS/pull/3307) **MERGED**、import追加1行のみ |
| 公開集約exact-source CI | [#42443549738](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42443549738) **SUCCESS** |
| KuuOSFormal Strict Lean／Governance | **10,339 / 10,339 SUCCESS／30 / 30 SUCCESS** |
| 公開集約source/test-merge/squash Git tree | **`7cbd0b542270950a8627f0bf8bcb6d57bef24dd1` 完全一致** |
| 公開集約squash main | `397b62e5ce6050fcb3fb825794eb13559dac10da` |
| Lean/mathlib | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root／保護PR | root107維持、#1558 Draft・OPEN・未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ContextActionLengthObstructionV5_26.lean)。

## 1. 旧商と文脈閉包後の新商に残る「履歴長」

元の第十セルwhiskering構文履歴`framedWhiskerRawTrace`から

\[
\boxed{\ell(F):=\left|\operatorname{Trace}_{10}(F)\right|\in\mathbb N}
\]

を定める。`framedDoubleWhisker_preservesTraceLength`は旧full framed12Dの全構成子を帰納し、比較があるときの長さ保存を証明する。
さらに`contextClosed_preservesTraceLength`は**v5.25の全6構成子**（旧比較の包含、反射・反転・連結、左右の真正文脈閉包）で長さの保存を証明：

\[
\boxed{T:\mathrm{ContextClosed12}(F,G)\Longrightarrow\ell(F)=\ell(G).}
\]

左右の新構成子は、両端の生履歴に同じBool値を1項だけ先頭追加する。従って順序を捨てずに元証拠を保持しながら、長さだけは比較不変になる。

`contextClosedTraceLength`、`originalFramedTraceLength`は各商から`Nat`への`Quotient.lift`。
`contextClosedTraceLength_factorsOld`は、旧→新商写像`oldToContextClosedQuotient`に沿って長さ観測が一致すると証明する。

v5.24の**末尾列**`drop 2`はv5.25の新商で失われたが、**総長さ**は残る。観測可能な情報の階層が変化したのであり、raw証拠自体は削除されていない。

## 2. 元の六セル境界に沿った左右作用は長さを1増やす

`contextBoundaryTraceLength`は真正元6Dの両端`c,d`を添字に持つpacket商`Q(c,d)`へ観測を降下する。

実在する元第七セル文脈`before:b→c`、`after:d→e`からv5.25の

\[
L_{before}:Q(c,d)\to Q(b,d),
\qquad
R_{after}:Q(c,d)\to Q(c,e)
\]

を用いる。`contextLeftAction_traceLength`と`contextRightAction_traceLength`は、すべての商の元`x`について

\[
\boxed{\begin{aligned}
\ell(L_{before}(x))&=\ell(x)+1,\\
\ell(R_{after}(x))&=\ell(x)+1
\end{aligned}}
\]

を証明した。両辺の型が異なる境界を持つ場合でも、`Nat`観測なので比較できる。元の第七セルの文脈が反射証拠である場合にもこの増分は消えない。

## 3. 反射第七セルの形式的文脈は恒等作用ではない

任意の実在する`F : ContextFrameEleven W l r c d`について、新商の類`[F]`に反射第七セル文脈を付けると

\[
\ell(L_{\mathrm{refl}}([F]))=\ell([F])+1,
\qquad
\ell(R_{\mathrm{refl}}([F]))=\ell([F])+1
\]

となる。自然数に`n+1=n`は成立しないため、

\[
\boxed{L_{\mathrm{refl}}([F])\ne[F],
\qquad R_{\mathrm{refl}}([F])\ne[F].}
\]

`contextLeftReflexive_notIdentity`・`contextRightReflexive_notIdentity`が実際の型付き入力ごとにこの差を証明。
`contextLeftAction_noUniversalUnit`・`contextRightAction_noUniversalUnit`は、inhabitedな各原fiberでの万能な恒等作用法則を否定する。

ここで`SevenRewrite.refl`は元第七セルの**生の構成子**であり、その上の作用が商で自動的に恒等となると取り違えない。

## 4. 同じ側の二重作用と一回の合成文脈は一致しない

元の第七セル`before:a→b`、`after:b→c`を与える。v5.25の境界商に対し、

\[
\begin{aligned}
\ell(L_{before}(L_{after}([F])))&=\ell([F])+2,\\
\ell(L_{before\cdot after}([F]))&=\ell([F])+1
\end{aligned}
\]

であるから

\[
\boxed{L_{before}(L_{after}([F]))\ne L_{before\cdot after}([F])}
\]

を`contextLeftAction_compositionGap`として証明する。
右についても合成可能な二つの元第七セル文脈から`contextRightAction_compositionGap`を証明した。

これはv5.25の`contextClosedActions_commute`と矛盾しない。後者は**反対側**の左右作用について、いずれも合計2イベントを生むことを前提とした型付き比較である。一方、今回の問題は**同じ側**の二文脈を一つの元第七セル合成構文にした場合であり、履歴長が異なる。

## 5. authority境界と次段階Qi v5.27

Qi v5.26は**既存のv5.25文脈閉包商に対して**単位則・同側合成則が厳密には成立しないことを証明した。新たな比較生成元も公理も追加していない。将来別のunital/compositional completionを作ることが不可能だとは述べない。

次の研究候補は、元の文脈が反射または合成であることを明示する独立の選択12D比較を追加し、単位則・同側合成則を成立させる必要最小の商を構成すること。
ただし、この新商では上記の`\ell`はもはや降下できないはずであり、これは**新しい定理として要証明**である。v5.25で保存した元3計数が引き続き降下するかも、全新構成子について厳密に検証する。

元F55/P77/GK5CGの証拠、旧6D〜14Dの真正Type、v5.23選択13D/14D、独立Kuuのauthority、公開root107は変更しない。
append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
