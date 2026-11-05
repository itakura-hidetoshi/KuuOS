# Qi v4.61 — 元P77証拠付き像の準逆Functor自然同型と五角形上下経路の真正正規形

**2026年11月5日 JST**。strict 空中心／独立Kuu一presentation。append-only・same-root・overwrite forbidden。

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#3143](https://github.com/itakura-hidetoshi/KuuOS/pull/3143) **MERGED** |
| 継承元 | Qi v4.60 定理 #3141／正式記録 #3142 MERGED |
| 定理exact-source HEAD | `fde458fb8e42b35231e5c408b419a64283905ff7` |
| 定理squash/main | `e46c5d74d2a191bc3414425f09a5025d6e9988ae` |
| source/test-merge Git tree | `2827f2dce780e392deb3c5dd08ea8c8bce56e680` **一致** |
| exact-source CI | [#41984530648](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41984530648) |
| Strict Lean | **10,258 / 10,258 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 公理監査 | 新規14件、`propext`／`Classical.choice`／`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| 変更 | [新規Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77InverseUniquenessPentagonNormalFormsV4_61.lean)＋`formal/KuuOSFormal.lean`へのimport 1行 |
| 環境 | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護 | 公開root107、PR #1558 Draft／OPEN／未マージ |

## 1. 正本と三つのauthority

Qi v4.53で元FivefoldEdgeの5本の有向辺 `e01,e12,e23,e04,e43` から真正自由経路圏を構成。Qi v4.54は元F55/P77の依存型四セルを元GK5CGの保守的**Type値5-cellの存在証拠**で商にしたtarget圏を持つ。Qi v4.57の`FivefoldP77ImagePoint`は、元target商クラスと本物の有限元経路による到達可能性の証拠を備えた**別の像圏**である。

Qi v4.58の`fivefoldP77ImageEquivalence`は、真正source圏から像圏へのMathlibカテゴリー同値を構成し、準逆`fivefoldP77ImageQuasiInverse`を与えた。Qi v4.60は到達証拠から唯一の元`Quiver.Path`を復元する独立の`fivefoldP77ImageRecoveryFunctor`を構成した。

元P77全targetは、v4.59で証明したchargeゼロでも到達不能な真正四セルを保持している。したがって、今回の比較は**像圏上の二つの準逆Functor**の比較であって、全targetへの回収や元証拠の数値化を主張しない。

## 2. 真正のNatIsoによる二つの準逆の比較

\[
Q:=\text{fivefoldP77ImageQuasiInverse},\qquad
R:=\text{fivefoldP77ImageRecoveryFunctor}.
\]

v4.58の真正カテゴリー同値`E`の`counitIso.app X`は、元の証拠付き像圏における真正同型である。これをv4.60の復元Functor`R.mapIso`で移送し、各像対象`X`で

\[
\theta_X:Q(X)\overset{\cong}{\longrightarrow}R(X)
\]

を構成した。`fivefoldP77InverseRecoveryComponent`がこの**Mathlib Isoデータ**である。

`fivefoldP77InverseRecoveryComponent_natural`は元counit自然性をFunctor`R`で写し、v4.60で既に形式化された厳密な元経路の回収則を使って、全ての真正像Hom`A:X⟶Y`に対し

\[
Q(A)\,\circ\,\theta_Y
=\theta_X\,\circ\,R(A)
\]

（Leanの`≫`順で`Q.map A ≫ θ_Y.hom = θ_X.hom ≫ R.map A`）を証明する。これから固定mathlibの`NatIso.ofComponents`を使い、

\[
\boxed{Q\cong R}
\]

という実際の**Natural Isomorphism**を`fivefoldP77QuasiInverseRecoveryNatIso`で得た。

これはchoiceに依存するv4.58準逆とv4.60経路復元が「定義的に同じ」という主張ではなく、自然同型で比較可能である、という正確な形式命題である。

## 3. 真正元P77上下五角形経路の正規形

元の上経路 `U : 0→3` は `e01 ; e12 ; e23` の3辺、下経路 `L : 0→3` は `e04 ; e43` の2辺である。

`fivefoldP77CertifiedUpper`と`fivefoldP77CertifiedLower`は、これらの真正元有向自由経路を**元F55/P77 conservative 5-cell商クラス＋元経路到達証拠**として像圏に移したもの。

`fivefoldP77CertifiedUpper_recover`／`fivefoldP77CertifiedLower_recover`により、復元したType値経路は上・下ともに元の構文と**厳密に一致**する：

\[
R(F(U))=U,\qquad R(F(L))=L.
\]

元GK5CGの整数chargeと正規経路長の一致から

\[
Q_{\mathrm{P77}}(F(U))=3,\qquad
Q_{\mathrm{P77}}(F(L))=2
\]

を証明。 `fivefoldP77CertifiedUpper_ne_lower`で、元P77の**真正証拠付き像Homは異なる**と確認した。実際の原P77五セルや新pentagonatorを追加して等しくする処理は一切行わない。

さらに`fivefoldP77QuasiInverse_upper_naturality`と`fivefoldP77QuasiInverse_lower_naturality`は、上／下の各元P77像Homで、比較自然同型の可換四角形が**復元済みの具体的元経路**と一致することを証明している。

## 4. 初回CI修正の構造理由

初回CIでは、counit自然性を`calc`へ持ち込む際のEq中間型接続が合致せず、また`congrArg`由来のlambda式のbeta簡約前のままcharge書換えを試みた。さらにNatTrans自然性からの具体的上／下経路への`rw`は、関手Homの展開段階でパターンが一致しなかった。

元P77・v4.58〜v4.60のLean定義と固定mathlibの`NatIso.ofComponents`、`Equivalence.counitIso`、`Functor.mapIso`を照合し、counit自然性を`congrArg (R.map)`で移送する直接証明、chargeの`change`によるbeta正規化、上下経路への`congrArg`等式輸送に置換した。

**新規定理は削除せず、仮定も弱めず**、2回目のexact-source CIで10,258/10,258全ビルド成功。14件の公理監査は標準三公理のみで、`sorryAx`なし。source/test-merge Git treeも完全一致した。

## 5. 次の研究境界

**確定**：元P77証拠付き像圏上の二つの真の逆関手は自然同型で比較できる。元P77上経路3辺と下経路2辺は、元のType値証拠・到達履歴を保持したまま相異なる正規形へ復元される。

**未主張**：元P77全targetとのこの関手による圏同値、未知のoriginal→phi seam、元P77の上下差を消す新pentagonator、数値CRTから元F55証拠を復元すること、C60物理辺とP77四セルの型同一視、Gray圏復元。

**次 Qi v4.62 候補**：準逆比較の一意性・三角恒等式への証拠付き接続、原P77全targetに対する「到達可能性を保つ部分的回収」と不可能なHomの境界のさらに精密な分類。元F55/P77/P94Aと実際のC60 gaugeのauthority境界を維持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
