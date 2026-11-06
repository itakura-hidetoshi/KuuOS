# Qi v5.00 — 単位則ダイヤモンドの四剰余障害と残余偶奇の不完全性

## 0. 正本・Lean4 exact-source検証

2026年11月7日 JST。Repository: \`itakura-hidetoshi/KuuOS\`、canonical branch: \`main\`。
継承基点: Qi v4.99の統合済み正本 \`d70a3efc88c34b8344af10f6ca024350e533fc8b\`。
定理PR: [#3223](https://github.com/itakura-hidetoshi/KuuOS/pull/3223) **MERGED**。
定理squash commit: \`7c3c0ae4b3f4e2e2872e6dce9a6d7f71aa0c9b84\`。

- exact-source CI: [#42302613120](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42302613120) — **SUCCESS**。Strict Lean **10,299/10,299**。Governance **30/30 SUCCESS**。
- 検証済みPR source HEAD: \`aa0c6f7cda18848035a3a04f49b973110d593f02\`。
- exact-source test-merge commit: \`3cf015658416cc711d61a412b2c36eaee086a0bd\`。
- PR source/test-merge Git tree: \`79042e9bb6a687a62b44cb4affa0eaad9e9a2773\`。**完全一致**。
- 新規25宣言の\`#print axioms\`は\`propext\`、\`Classical.choice\`、\`Quot.sound\`の標準公理または空。**sorryAxなし**。
- 新規Lean warning/error **0/0**。\`-DwarningAsError=true\`と\`-DsorryAsError=true\`でビルド。
- Lean \`v4.30.0-rc2\`、mathlib \`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`。
- 公開集約 \`KuuOSFormal\`、公開root **107維持**。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) は Draft／OPEN／未マージ維持。

[Qi v5.00 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77UnitDiamondFourTorsionObstructionV5_00.lean) ·
[Qi v4.99正式記録](Qi-v4_99-original-P77-mixed-identity-residual-parity-descent.md)

## 1. 問題設定と観測・推測の分離

Qi v4.99では、真の七セル履歴上の第四整数\`R(H)=sevenIdentityBalance H\`が、
独立\`IdentityEightCell\`商へ整数のままでは降下しないにもかかわらず、
\`R(H)%2\`は全高次比較構成子で保存され、
\`Quotient.lift\`によるBool値観測量\`identityHistoryParity\`が得られた。

未解決だった問いは、
**同じ生の六セル始終点を持つ二つの七セル履歴で、Rの偶奇が等しくても、
既存の\`IdentityEightCell\`構成子のいかなる合成でも比較できない具体例があるか**、
というものである。

本段階はその具体的反例を形式証明する。
一般の七セル平行履歴の大域的分類や、選択商のthin性までは主張しない。

## 2. 四剰余観測量の定義

不変量のもとになる\`sevenUnitTorsionWeight(H): ℤ\`は、元の13構成子を持つ自由\`SevenRewrite\` Typeから再帰的に定義する。
基本生成元の重みは以下のとおり。

| 七セル生成元 | 重み |
|---|---:|
| \`refl\`, \`leftUnit\`, \`assoc\`, \`inverseRight\` | 0 |
| \`inverseId\`, \`inverseComp\` | 1 |
| \`rightUnit\`, \`inverseLeft\`, \`doubleInverse\` | 2 |

\`symm H\`では符号を反転する。\`trans H K\`と\`congrComp H K\`では加算し、
\`congrInv H\`では同じ重みを保つ。

\[
S(H):=\operatorname{sevenUnitTorsionResidue}(H)
=\operatorname{sevenUnitTorsionWeight}(H)\bmod 4.
\]

Lean実装では\`S(H): ℤ\`を0から3の剰余代表として保持し、\`ZMod 4\`との暗黙の型同一視はしない。

\`S\`は既存の第四整数\`R\`とは異なる。\`R\`は\`identityDouble\`で2だけ変化し、
\`S\`はこれも含む全比較で不変となる。

構成子の重みを法2に落とすと\`S(H) % 2 = R(H) % 2\`となる。
これは今回採用した重みからの代数的解釈であり、独立したLean定理としての等式追加は次段に残す。

## 3. 全高次比較構成子への保存証明

\`EightCell\`には元の22種類の比較構成子があり、
その全構成子の帰納法で\`S\`の保存を証明した。
\`zigzagDiamond\`の両辺の整数重みは0と4になり得るため、
必要なのは整数の等式でなく**法4での等式**である。

次に\`TriangleEightCell\`、\`InvolutionEightCell\`、
\`InverseCompEightCell\`の追加構成子それぞれについて保存を証明。
最後に\`IdentityEightCell.identityDouble\`を含む全部の構成子と
左右whiskering、逆元文脈、合成文脈を証明する。

中心定理は次の形式を持つ。

\`\`\`lean
theorem identityEightCell_preservesUnitTorsionResidue
    {s t : SevenRewrite W long short c d}
    (q : IdentityEightCell W long short s t) :
    sevenUnitTorsionResidue s = sevenUnitTorsionResidue t
\`\`\`

\`Quotient.lift\`を使い、新しい選択商上の真正観測量
\`identityHistoryUnitTorsion\`を構成した。これは七セルraw構文そのものの
等式を意味せず、別presentationの証拠履歴を上書きしない。

## 4. 真正な「単位則ダイヤモンド」反例

任意の\`w : W\`について、共通のraw六セル始終点は

\[
(\operatorname{refl}(w);\operatorname{refl}(w))
\;\longrightarrow\; \operatorname{refl}(w).
\]

二つの**元の\`SevenRewrite\`原始生成元**を使う。

\[
H_L:=\operatorname{leftUnit}(\operatorname{refl}(w)),\qquad
H_R:=\operatorname{rightUnit}(\operatorname{refl}(w)).
\]

Leanで、三整数組と残余偶奇が一致することを直接証明した。

\[
\mathbf Q(H_L)=\mathbf Q(H_R),\qquad
\bar R(H_L)=\bar R(H_R)=0.
\]

一方、新しい保存量では

\[
\boxed{S(H_L)=0,\qquad S(H_R)=2\pmod 4.}
\]

したがって全構成子保存定理と矛盾するため

\[
\boxed{\neg\operatorname{Nonempty}
\bigl(\operatorname{IdentityEightCell}(H_L,H_R)\bigr).}
\]

これは単なる比較証拠の未発見ではない。
現行の全\`IdentityEightCell\`構文では比較不可能という構成的証明である。
よって\`identityHistoryClass\`でも両者は異なる。
\`sevenIdentityParity_notCompleteForIdentity\`では、
**偶奇一致⇒比較存在という無条件の主張を反証**し、
\`sevenUnitTorsion_notFactorThroughParity\`では、
法4観測量が偶奇値の任意の非線形関数からも復元できないことを証明する。

この\`unit diamond\`は既存のv4.99混合critical pairとは異なり、
既存の比較構成子の貼合せで埋まるものではない。

## 5. 元P77 raw添字への型付き輸送とauthority境界

二つの単位則履歴に同じ真正六セルsource生成元\`c\`を横合成し、
\`sevenUnitDiamondCompositeLeft c\`と
\`sevenUnitDiamondCompositeRight c\`を作る。

両者は同じ六セル始終点を持ち、\`R\bmod2\`は等しいが、
\`S\`は0対2なので比較できない。
\`pentagonActualUnitDiamondFourTorsionWithSourceObstruction\`は
**任意の真正P77最終raw添字**に対し
\`pentagonAdjoinedSixCell_generator\`を使ってその事実を輸送し、
\`¬ PentagonAdjoinedSixCellEqualityInterpreter\`も同時に証明する。

元F55/P77/GK5CGのsource Type値証拠・証拠履歴・strict Eq、
独立Kuuの高次presentation、各段階の商は互いに別である。
新しい選択商の等式を元sourceのstrict Eqへ昇格させない。

## 6. Lean4全文点検とCI修正

初回PR HEAD \`4c04f6fabc877ecaf00268a041c935d650e415f5\`では、
\`EightCell.inverseCongruenceChain\`の場合の\`simp only\`が
目標をすでに消去しているにもかかわらず、直後に\`omega\`を書いたため
Lean4が\`No goals to be solved\`と報告した。
型付け不能に伴う下流の\`sorryAx\`診断は実際の追加公理ではなかった。

新モジュール全文、import関係、元SevenRewriteと全比較grammarを照合し、
余分な\`omega\`1行だけを削除した修正版HEAD
\`aa0c6f7cda18848035a3a04f49b973110d593f02\`で
exact-source Strict Leanが成功した。
既存Leanファイル、mathlib pin、workflow、元のpresentationには手を加えていない。

## 7. 今回証明していない事項

- 任意の平行七セル履歴について\`S\`の一致が比較可能性を保証すること
- \`S\`が全ての高次障害を分類すること
- 任意の比較Typeがthinまたはcontractibleであること
- 最終八セル・九セルの大域的thin性
- 元F55/P77/GK5CG sourceのstrict Eqと選択商Eqの同一視
- \`unitDiamond\`を充填する新八セル生成元の追加（今回は**障害の証明まで**）

## 8. 次段 Qi v5.01

今回形式証明した真正\`unitDiamond\`障害に限り、
必要な場合は一つの原始比較\`unitDiamond\`を**別の独立presentation**へ最小追加し、
従来の\`IdentityEightCell\`および全sourceを変更しない。
その後、残余四剰余がどの商まで降下するか、
新しい混合critical pairが既存証拠で埋まるかを判定する。

append-only／tighten-only／overwrite-forbidden／same-root。
厳密なauthority境界と元Type値証拠履歴を維持する。
