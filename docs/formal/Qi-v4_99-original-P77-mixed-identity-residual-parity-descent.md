# Qi v4.99 — 混合identity／inverseComp重なりと第四整数の残余偶奇降下

## 0. Canonical正本・exact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、正本branch `main`。
基点はQi v4.98まで統合したmain `a85a06f6165421152e71b72ca7bdb3be03771d24`。
元GK5CG五セルsource、七セル生構文、旧八セルpresentation、選択商は上書きせず、
新Leanモジュールと公開集約importだけをappend-only追加。

| 項目 | GitHub MCPでの検証結果 |
|---|---|
| 定理PR | [#3221](https://github.com/itakura-hidetoshi/KuuOS/pull/3221) — MERGED |
| 検証済みexact-source HEAD | `3945508195be51931161ef372e18de49765cf2e3` |
| 定理squash／定理正本HEAD | `dbc8f810625ea677f61d6c2c419aa03af6b440c6` |
| source／test-merge Git tree | `8df1365b08fc890ef21fdc33f39a0d5525979018` — 完全一致 |
| exact-source CI | [#42299218011](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42299218011) — SUCCESS |
| Strict Lean | **10,298／10,298 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 新規公理監査 | **32宣言**、`propext`／`Classical.choice`／`Quot.sound` のみ |
| `sorryAx` | **なし** |
| 変更Lean warning／error | **0／0** |
| Lean／mathlib pin | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開構造 | `KuuOSFormal`、root107維持 |
| 保護PR #1558 | Draft／OPEN／未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedIdentityParityDescentV4_99.lean) ·
[前段Qi v4.98](Qi-v4_98-original-P77-identity-double-higher-local-completion.md)

## 1. 第四整数の非降下から残余偶奇の降下へ

Qi v4.97の `sevenIdentityBalance` を `R(H)` とする。
元七セル13構成子に対し、`inverseId` は+1、`inverseComp` は−1、
反転は符号反転、縦横合成は加法となる。

Qi v4.98で導入した別presentation `IdentityEightCell` では、
`identityDouble` による具体的二経路のRが0と2で異なるため、
Rは新八セル商の整数値保存量ではなくなる。

しかし、**その差は2の倍数**である。
Qi v4.99では元のraw履歴に対して

\[
\boxed{\bar R(H)=R(H)\bmod 2}
\]

を `sevenIdentityParity` として定義し、元v4.95比較規則
と新v4.98比較規則の**全構成子**に対する合同保存を形式証明した。
`identityEightCell_preservesParity` の帰納法は、
旧比較の整数R保存、新`identityDouble`の偶数差、
reverse・chain・whisker・inverseContext・compositeContextでの
合同関係の移送をすべて扱う。

`identityHistoryClass_eq_preservesParity` は選択された
新八セル履歴商のEqから偶奇一致を導く。
さらに `identityHistoryParity` は `Quotient.lift` により
**商の上で定義された真正Bool観測値**を構成し、
`identityHistoryParity_onClass` が代表元に対する計算法を示す。

`identityParity_survivesIntegerFailure` は
**偶奇は降下するが、整数値Rは降下しない**という二命題を同時に提示する。
これは単にRを0と置き換えた主張でも、生の七セル履歴を同一視する操作でもない。

## 2. 三種類の真正混合critical pair

旧v4.95で比較可能な `inverseComp` 左右重なりと、
旧v4.94の `doubleInverse`／逆元消去重なりを、
v4.98の新 `identityDouble` と同じ型付き六セル文脈に配置する。

| 混合pair | 新identityDoubleと貼り合わせる旧比較 |
|---|---|
| `mixedIdentityInvCompLeft` | 左 `inverseComp`・単位則重なり |
| `mixedIdentityInvCompRight` | 右 `inverseComp`・単位則重なり |
| `mixedIdentityInvolutionLeft` | 左二重反転・逆元消去重なり |

全て、二つの真正raw七セル履歴について元六セルの始終点が一致し、
新規の整数Rの差は

\[
\boxed{R(H_{\mathrm{direct}})=0,\qquad
R(H_{\mathrm{via}})=2}
\]

である。
`mixedIdentity..._balanceGap` の3定理が具体的に計算する。

各pairの新八セル証拠は、
`IdentityEightCell.compositeContext` に
`identityDouble` と既存の `InverseCompEightCell.leftOverlap`／
`rightOverlap` または旧 `InvolutionEightCell.leftOverlap`
を与えて構成する。
**混合pair専用の新しい原始八セル生成元は追加していない**。

## 3. 旧比較の厳密障害と新比較の局所合流

`mixedIdentityInvCompLeft_noPrevious`、
`mixedIdentityInvCompRight_noPrevious`、
`mixedIdentityInvolutionLeft_noPrevious` は、
旧 `InverseCompEightCell` の全構成子でRが保存されることを利用する。
旧比較が存在すれば0=2となるため矛盾する。未発見ではなく、
旧presentationについての**形式的な不存在定理**である。

これに対し、新八セルについては
`mixedIdentityInvCompLeft_fill`、
`mixedIdentityInvCompRight_fill`、
`mixedIdentityInvolutionLeft_fill` が、実際のType値証拠を構成する。

3つの `mixedIdentity..._newVsOld` 定理では、
新比較の存在、旧比較の不存在、新比較下での偶奇一致を一体で保証する。
したがって旧障害を忘れて上書きしたのではなく、
**異なるpresentationでの局所可比較性の変化**を比較可能な形で記録した。

## 4. 限定混合critical peak族と新商への降下

`MixedIdentityCriticalPeak` は3種の混合pairと
reverse・chain・左右whisker・inverseContext・compositeContext
という元の型付き閉包のみからなる。

`mixedIdentityCriticalPeak_fill` は構造帰納法により、
この指定族の**全構成子**の新八セル証拠を構築する。
`mixedIdentityCriticalPeak_joinable` はNonemptyを、
`mixedIdentityCriticalPeak_classEq` は新商でのEqを導く。

`mixedIdentityInvCompLeft_strictClasses` は、
新商では一致するが旧v4.95商では一致しない、
具体的混合履歴対を与える。
全七セル平行履歴の比較可能性や、さらに高次のthin性は主張しない。

## 5. 元GK5CGへの輸送とauthority境界

`pentagonActualMixedIdentityParityWithSourceObstruction` は、
任意の真正P77最終raw添字について、元の五セル長短二端点から
元六セル生成元を取り、その混合左 `inverseComp`／identityDouble
履歴pairに対して以下を同時に証明する。

- 新 `IdentityEightCell` では比較が存在する
- 旧 `InverseCompEightCell` では比較が存在しない
- 元 `PentagonAdjoinedSixCellEqualityInterpreter` の不可能性は維持される

元GK5CG五セルTypeを改変せず、strict 空中心と独立Kuu=presentation、
元sourceの履歴・選択比較・商・観測値のauthority境界を保持する。

## 6. 数学的到達点と研究境界

Qi v4.99は、v4.98の新比較が作る「整数Rの降下不能」を
「偶奇という残余の降下可能性」に分解し、
3つの具体的なmixed higher critical pairで
既存証拠の貼り合わせによる局所合流を構成した。

ただし「R mod 2が全ての高次不変量を分類する」
「大域的に任意の七セル履歴が比較可能」
「任意の九セルcoherenceが存在する」
などは証明していない。

次のQi v5.00候補では、偶奇以外の新保存量・Type値障害を探索し、
混合文脈のさらなる重なりを調べる。
高次証拠のhistoryを保持し、未証明の大域thin性を仮定しない。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
