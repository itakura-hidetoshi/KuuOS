# Qi v4.87 — 高次六セル証明語の次数整合・商合成と条件付き観測descent

## 0. 正本・形式検証

2026年11月6日 JST。Repository：itakura-hidetoshi/KuuOS、canonical：main。

| 項目 | 検証済み状態 |
|---|---|
| 継承元 | Qi v4.86／canonical main `2ce04c4221c05a8c48a024e520897a7b35b495ec` |
| 定理PR | [#3197](https://github.com/itakura-hidetoshi/KuuOS/pull/3197) — MERGED |
| exact-source HEAD | `e5773d1890868b01be5bbfed66158c91581b9d3d` |
| squash／canonical theorem HEAD | `b7b3dae3f2c411f61b74f0b158fe06f4d0a7fdff` |
| source／test-merge／squash Git tree | `f7d2f2a35fe619734601420a463c3a7e45d7f456` — 完全一致 |
| exact-source CI | [#42192480627](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42192480627) — completed/SUCCESS |
| Strict Lean | **10,286／10,286 SUCCESS**（新モジュールとKuuOSFormalを含む） |
| Governance | **30／30 SUCCESS** |
| 公理監査 | 指定20宣言の `#print axioms` を実ログで確認。標準公理 `propext`／`Classical.choice`／`Quot.sound` の範囲 |
| `sorryAx`／変更Lean warning/error | なし／0・0 |
| 公開・保護 | `KuuOSFormal`、root107維持。#1558はDraft／OPEN／未マージ |
| pin | Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77SixCellWordCoherenceDescentV4_87.lean) · [v4.86正式証明記録](Qi-v4_86-original-P77-adjoined-six-cell-presentation-equality-descent-gate.md) · [真正GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 自由六セル証明語と新しい次数

元sourceの真正GK5CG保守的五セルTypeに、Qi v4.86が別presentationとして加えた `PentagonAdjoinedSixCell W long short` を継承する。構成子は `refl`、`symm`、`trans`、明示的な `pentagon`。元GK5CGへ六セルが存在したと主張しない。

新presentation内の任意の型付き六セル語cに、整数値の構文次数 `degree c` を再帰的に定義した。

\[
\deg(1_w)=0,\quad
\deg(p)=1,\quad
\deg(c^{-1})=-\deg(c),\quad
\deg(c\circ d)=\deg(c)+\deg(d).
\]

同じ端点を持つ語c,dについて `DegreeCoherent c d : Prop` は **\(\deg(c)=\deg(d)\)** と定義する。これは元五セル値の厳密等式でも、生の六セル証明語の等式でもない。次数による**選択した**整合関係である。

## 2. 六セル証明語の合成・逆元と商での群oid法則

`degreeCoherent_refl`、`degreeCoherent_symm`、`degreeCoherent_comp` によって、次数整合が反射・反転・合成に適合することを形式証明した。次に平行六セル語を次数整合で商化した `CoherentHom W long short w z` を構成し、`homId`、`homComp`、`homInv` を定義した。

商上で `hom_leftUnit`／`hom_rightUnit`／`hom_assoc`／`hom_inverseRight`／`hom_inverseLeft`／`hom_doubleInverse` を証明。

\[
\begin{aligned}
1\circ[c]&=[c]=[c]\circ1,\\
([c]\circ[d])\circ[e]&=[c]\circ([d]\circ[e]),\\
[c]\circ[c]^{-1}&=1,\qquad [c]^{-1}\circ[c]=1,\\
([c]^{-1})^{-1}&=[c].
\end{aligned}
\]

**構文上は同一視しない。** `raw_inverseCancellation_notStrict` は `trans pentagon (symm pentagon) ≠ refl` を原始構成子形状から証明する。真正元五セルを両端とする `pentagonActualSixCell_roundtrip_degreeCoherent` と `pentagonActualSixCell_roundtrip_notStrict` も両方形式証明した。新たな元sourceの7セルを証明したわけではない。

## 3. 観測descentの必要十分条件

任意のType Xと観測写像 O : W → X に対し、`observationDescent_iff` により

\[
\boxed{
\big(\forall w,z:W,\;
\mathrm{AdjoinedSixCell}(w,z)\to O(w)=O(z)\big)
\iff O(\mathrm{long})=O(\mathrm{short}).
}
\]

右辺から左辺へは六セル証明語の4構成子すべてについて帰納法で証明。反対向きは新生成元pentagonへの適用で導く。これは単なる十分条件ではなく**必要十分条件**である。

元の真正最終raw P77添字iと、真正元五セル値L₃(i),L₂(i)を代入した `pentagonActualSixCell_observationDescent_iff` も成立する。Qi v4.85の `pentagonOriginalFiveCell_words_ne` を再利用し、**Oが単射ならこのdescentは不可能**であると `pentagonActualSixCell_noInjectiveObservationDescent` で証明した。

この障害は元五セル語の厳密不一致に基づく。粗い観測を否定せず、すべての高次充填不可能性も主張しない。

## 4. 新endpoint商とfactorization

`EndpointQuot W long short` は **新しい**六セルの到達関係 `Nonempty (AdjoinedSixCell w z)` によるQuotであり、元sourceの厳密等号は変更しない。

`endpointGeneratorEq` でlongとshortの像の一致を証明し、`endpointMk_notInjective` では元値が異なるとき商写像が単射でないことを証明した。`endpointLift` は O(long)=O(short) を明示条件にして任意の観測 O をこの新endpoint商を介して因子化する。因子化の値保存は `endpointLift_mk` により示す。真正source値に関する `pentagonActualSixCell_endpointQuotEq` も証明済み。

## 5. ソースとauthorityの境界／CIと実装

新規Leanモジュール1件（約390行）＋ `formal/KuuOSFormal.lean` にimport1行。旧Lean定理・P77/F55/GK5CG元source・pin・manifest・workflow・保護PR・公開rootを変更しない。

初回に正本内の成功例と照合し、`Quot.liftOn₂` に必要な**左右独立の代表元不変性**の二証明を明示した。最新HEAD `e5773d1…` のexact-source CIは成功、Governance30件すべて成功、変更Leanのwarning/error0/0。新規指定20件の `#print axioms` は標準公理依存の範囲で `sorryAx` なし。検証済みheadを指定しsquashマージし、Git tree一致を再確認した。

## 6. 次候補 Qi v4.88

次数同値という現状の整合を、自由六セル語の端点ごとの正規形・完全性／忠実性へ進める。元GK5CGの五セル証拠履歴を残し、候補higher presentationの可換性を無条件の元source同一視に置換しない。構文上の`RawWord`、新商での`CoherentHom`、旧五セルType、観測値を区別する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
