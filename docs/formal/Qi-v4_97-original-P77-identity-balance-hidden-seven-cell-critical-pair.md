# Qi v4.97 — 三整数では見えない七セルcritical pairと第四の整数保存量

## 0. Canonical正本・exact-source証明記録

2026年11月7日 JST。唯一の正本は \`itakura-hidetoshi/KuuOS\` の \`main\`。
継承基点は統合済みQi v4.96、main \`78a2fb1d990e2bf02da7eb32d553b7e49b9f0ee5\`。
新規Leanファイルと公開集約importのみを追加し、既存の五セル元source、旧七セル構文、旧八セルpresentationを変更しない。

| 項目 | GitHub MCP検証記録 |
|---|---|
| 定理PR | [#3217](https://github.com/itakura-hidetoshi/KuuOS/pull/3217) — MERGED |
| 検証済みexact-source HEAD | \`bebaa45fda8c265d4d1a8b9729a95084a893bb6d\` |
| 定理squash／canonical main統合 | \`bb52d5fc464c673f8ee8a7ec2620acd83b7533f9\` |
| source／test-merge Git tree | \`570636f700bae543f38e182db3b7b2f5df0ef676\` — 一致 |
| exact-source CI | [#42273791864](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42273791864) — SUCCESS |
| Strict Lean | **10,296／10,296 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 追加宣言公理監査 | **25宣言、標準公理 \`propext\`／\`Classical.choice\`／\`Quot.sound\`のみ、\`sorryAx\`なし** |
| 変更Lean warning／error | **0／0** |
| 固定ピン | Lean \`v4.30.0-rc2\`、mathlib \`5450b53e5ddc75d46418fabb605edbf36bd0beb6\` |
| 公開構造 | \`KuuOSFormal\`、公開root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77IdentityBalanceHiddenCriticalPeaksV4_97.lean) ·
[前段Qi v4.96正式記録](Qi-v4_96-original-P77-three-charge-filtration-linear-rigidity.md)。

## 1. 元の生七セル履歴と新しい第四保存量

元v4.89の真正13構成子 \`SevenRewrite\` のraw Type値履歴を保持する。
Qi v4.96の3つの整数観測 \`T\`、\`J\`、\`K\` はそのまま使う。

新しい \`sevenIdentityBalance\` は \`inverseId\` に +1、\`inverseComp\` に −1、
その他の原始七セル操作に0を割り当てる。反転は符号反転、
履歴の縦合成と横合成は加法、逆語文脈は値をそのまま輸送する。

\[
\boxed{R(H)=N_{\mathrm{inverseId}}(H)-N_{\mathrm{inverseComp}}(H).}
\]

原始生成元の計数はraw七セルType上の指定構文に対する整数であり、
元六セル次数、元GK5CG五セル値、元七セルraw equality、選択された八セル商のEqとは区別する。

## 2. 最終八セル比較による普遍保存則

\`eightCell_preservesIdentityBalance\` は元v4.91の全22種類の八セル構成子を帰納し、
Rの不変性を証明した。新しい三角形v4.93および二重反転v4.94の
各比較構成子についても \`triangleEightCell_preservesIdentityBalance\` と
\`involutionEightCell_preservesIdentityBalance\` が同じ不変性を証明する。

重要な最終段は \`inverseCompEightCell_preservesIdentityBalance\` である。
v4.95新規の左右の逆元合成・単位重なりは、via側に
\`inverseComp\` 1回と \`inverseId\` 1回を含むため、Rの寄与は−1+1=0。
したがって**v4.95までに追加された全比較TypeでRが保存される**。

\`inverseCompHistoryClass_eq_preservesIdentityBalance\` は、
最終の選択された八セル履歴商で二つのclassが等しいならRも等しい
という必要条件を形式証明する。逆方向の完全性は主張しない。

## 3. 三整数値が一致する具体的な新しいcritical pair

同じ元六セル始終点を持つ、二つの新しい七セル履歴
\`sevenHiddenCriticalFirst\` と \`sevenHiddenCriticalSecond\` を構成した。

その構成は、三つの局所重なりの差が互いに補償するように選ぶ。

| 構成要素 | Route Aの寄与 \`(T,J,K;R)\` | Route Bの寄与 \`(T,J,K;R)\` |
|---|---|---|
| \`doubleInverse(refl)\` 対 2回の \`inverseId\` | \`(0,1,0;0)\` | \`(0,0,0;2)\` |
| 左二重反転・逆元消去 | 直接 \`(0,0,0;0)\` | via \`(1,1,0;0)\` |
| 三角形単位・結合 | via \`(1,0,0;0)\` | 直接 \`(0,0,0;0)\` |
| **合計** | **\`(1,1,0;0)\`** | **\`(1,1,0;2)\`** |

※ \`doubleInverse(refl)\` 自体がJ=1を持つので、単純に二つの経路の
残りの因子を一致させるのではない。T,Jの補償を計算した上で、
Rの差だけを残す。すべて真正の元六セルTypeの始終点を持つ履歴である。

Lean4定理 \`sevenHiddenCritical_threeChargeValues\` と
\`sevenHiddenCritical_balanceValues\` がこの全値を具体的に証明し、
その帰結として

\[
\boxed{
\mathbf Q(H_A)=\mathbf Q(H_B)=(1,1,0),
\quad R(H_A)=0,\quad R(H_B)=2
}
\]

が成立する。

## 4. 否定できる比較と非線形非因子化

\`sevenHiddenCritical_noComparison\` は、最終v4.95のType値
\`InverseCompEightCell(H_A,H_B)\` が存在すればRの保存と0≠2が矛盾するため、

\[
\boxed{\neg\operatorname{Nonempty}\bigl(\mathrm{InverseCompEightCell}(H_A,H_B)\bigr)}
\]

を直接証明する。また \`sevenHiddenCritical_notStrict\` はraw七セル履歴の
厳密Eqも成り立たないことを示し、
\`sevenHiddenCritical_distinctClasses\` は最終高次商のclass不一致へ輸送する。

\`sevenChargeTriple_notCompleteForInverseComp\` は、三整数値の一致から
最終八セル比較の存在が必ず従う、という一般命題を否定する。

さらに \`sevenIdentityBalance_notFactorThroughTriple\` は、
任意の（線形とは限らない）関数 \`F : (ℤ × ℤ × ℤ) → ℤ\` に対する
\`R(H)=F(\mathbf Q(H))\` の全七セル履歴での普遍成立を否定する。
二履歴の三整数値が同じでRだけ違う具体的反例であり、
前段v4.96の線形剛性とは独立に強い非因子化結果である。

## 5. 障害とは対照的な既存局所合流

\`sevenIdentityInterchangeFirst\`／\`sevenIdentityInterchangeSecond\` は、
二箇所に現れる独立した \`inverseId\` を異なる順で実行する二つの
実七セル履歴を構成する。\`sevenIdentityInterchange_joined\` は、
旧v4.91の \`EightCell.interchange\` を使って、これらにすでに八セル証拠がある
ことを確認した。単に三整数が一致したというだけで
すべてをobstructionとするのではなく、**既存規則で合流できる局所対と
証明された非合流対を分離**する。

## 6. 元GK5CGの真正source境界への輸送

\`pentagonActualThreeChargeIncompleteWithSourceObstruction\` は、
元P77の任意最終raw添字、真正五セル長短二端点上でも、
三整数一致が最終八セル比較を保証しないことを示す。
従来の \`PentagonAdjoinedSixCellEqualityInterpreter\` 不存在は同時に保存する。

元F55/P77/GK5CGのsource構成子を追加・上書きしない。
strict 空中心と独立Kuu=presentationを混同せず、
生の歴史Type、複数の独立八セルpresentation、選択商、
各不変量のdescent可否を異なるレイヤに保持する。

## 7. Lean4実装診断と修正履歴

- 初回CI [#42224920623](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42224920623) は親Lakeキャッシュの復元中断でcold buildとなり、75分制限で終了コード124。新モジュールの証明判定前だった。
- 次CI [#42271959509](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42271959509) で、新モジュール281行以降に \`long\`・\`short\` 等の暗黙引数未推論が連鎖。整数観測値に元Typeの端点が残らず、暗黙引数の再構成に失敗したことが構造的原因である。名前付き引数で各端点を明示。
- CI [#42273050387](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42273050387) では最後の1件、\`congrArg (fun s => ...)\` に生じたラムダ適用を \`rw\` が書換え対象として認識できない問題が残った。明示的 \`change\` で等式の型をβ簡約した形へ変更。
- 最終CI #42273791864 が全30ジョブ成功。変更Lean警告・エラー0。25宣言の \`#print axioms\` を全件収集して標準公理以外の混入がないことを確認。

## 8. 到達点と次の研究境界

Qi v4.97は、前段で整数線形不変量を尽くした最終選択presentationに対し、
**新しい第四の独立した整数障害が残っている**ことを、
元のType値履歴・具体的critical pair・各比較規則の帰納的保存則から構成した。

これらは「非線形のあらゆる不変量が存在しない」「すべての平行
七セル履歴が比較可能」「新しい八セルが自動でthinになる」等を
**証明していない**。次のQi v4.98候補は、今回の新たなcritical pairを
限定的に埋める別八セルpresentationと、その追加に伴う第四保存量の
非降下・旧商からの厳密粗化を検証することである。
新たな比較生成元を導入するときも、元の全sourceを変更しないことを前提とする。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
