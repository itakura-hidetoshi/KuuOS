# Qi v5.50 — 型付きraw文脈合同性の自由閉包と旧19D商の厳密な情報損失

検証記録日：2026-11-09 JST

## 1. 根拠（正本・機械検証）

正本：`itakura-hidetoshi/KuuOS`、canonical `main`。定理・公開集約は別PRで実際にMERGED済み。

- [Qi v5.50 Lean4定理PR #3380](https://github.com/itakura-hidetoshi/KuuOS/pull/3380) MERGED：`d4a85788b5c6c724d3a45f356b3eb82e2db82632`。
- [公開import PR #3381](https://github.com/itakura-hidetoshi/KuuOS/pull/3381) MERGED：`889c10fa66ba2531854153a2d3d5ce266464290e`。
- [形式証明Lean全文](https://github.com/itakura-hidetoshi/KuuOS/blob/d4a85788b5c6c724d3a45f356b3eb82e2db82632/formal/KUOS/Architecture/QiWuxingGK5CHP77TypedRawCongruenceCompletionV5_50.lean)、新規1ファイル421行、元のLeanソース・比較構成子・Type値証拠は変更なし。

## 2. 元のselected19 presentationから独立した型付き閉包

元の19D比較`SelectedLocalNineteen`は、`strict`・`unitPrepend`・`unitAppend`・比較証拠の`reverse`・比較証拠の`chain`だけからなる。Qi v5.49はこれがraw18D `reverse` および raw18D `chain` の合同性を持たないことを形式証明している。

本研究では、元定義を変更せず、**別名で独立した新presentation**`SelectedRawCongruentNineteen W l r J N M L : Type`を構成。ここで`J,N`は元の同一16D fiber上の真正17D証拠端点。

新Type値比較の生成元は7種類：

1. `inherited`：元の真正`SelectedLocalNineteen` Type値証拠をそのまま埋め込む。
2. `strict`：同一raw証拠の反射。
3. `reverse`：**比較証拠**の対称。
4. `chain`：**比較証拠**の推移。
5. `rawReverse`：`J→N`で比較可能なraw証拠にraw反転を適用し、**逆endpoint `N→J`**で比較証拠を構成。
6. `rawChainRight`：`J→N`の比較を、指定された真正raw `X:N→S`との右合成`J→S`へ輸送。
7. `rawChainLeft`：指定された真正raw `X:J→N`と`N→S`の比較を左合成`J→S`へ輸送。

これらは元の比較公理を改変したものではない。新しい比較閉包が識別を追加することを、旧商と新商を別々の型として保持することで明示する。raw whiskerLeft/whiskerRight、異なる16D fiber間交換・20D gluing生成元は追加していない。

## 3. 最小性（全ての閉包関係への普遍的証明）

定理`selectedRawCongruent_minimal`は、厳密な端点添字を持つ任意のProp値関係

```text
R(J,N) : Raw(J,N) → Raw(J,N) → Prop
```

が、元19D比較の包含、反射・対称・推移、raw reverse、raw右・左chainの合同性を満たすなら、新presentationの**任意の真正Type値証拠**`A : SelectedRawCongruentNineteen ... M L`から`R(J,N)(M,L)`が従うことを構造帰納法で証明する。これが指定7生成元に関する最小性であり、それ以上の大域的比較や自由な元証拠の消去を主張しない。

## 4. 新しい商と降下

新Type値比較の`Nonempty`を同一fiberの同値関係として`selectedRawCongruentSetoid`を構成。商クラス一致と真正比較の存在の同値を証明した。

```text
[M]_new = [L]_new ↔ Nonempty(SelectedRawCongruentNineteen ... M L)
```

従来のselected19商から新商への射`π : Quot_old(J,N) → Quot_new(J,N)`を、元19D比較証拠を`inherited`で保存することで`Quotient.lift`により構成。任意の指定厳密fiberで**πは全射**と証明した（空fiberでは空性の範囲で成立）。

新商上では、元raw反転

```text
Reverse_new : Quot_new(J,N) → Quot_new(N,J)
```

および真正raw `chain` の二変数合成

```text
Chain_new : Quot_new(J,N) → Quot_new(N,S) → Quot_new(J,S)
```

をそれぞれ実際に構成し、rawクラス上で期待される作用の等式を証明した。これらは**新商だけ**の降下であり、旧商に元raw操作が降下したという主張ではない。

## 5. 旧障害を保持した情報損失の定理

Qi v5.49の与えられた元旧18D証拠`M:J→N`を用い、旧商では比較不可能と形式証明済みの三つの組を新Type値比較で結んだ。

- `reverse(prepend(M))` と `reverse(inherited(M))`。
- `chain(prepend(M), strict N)` と `chain(inherited(M), strict N)`。
- `chain(strict J, prepend(M))` と `chain(strict J, inherited(M))`。

新比較のType値証拠はそれぞれ`rawReverse`、`rawChainRight`、`rawChainLeft`から直接構成。新商がこれらを同一視する一方、旧商では異なることから、次の非単射定理を証明した。

```text
¬ Injective (π_(N,J))     -- raw reverse を用いる場合
¬ Injective (π_(J,N))     -- strict right raw chain を用いる場合
¬ Injective (π_(J,N))     -- strict left raw chain を用いる場合
```

いずれも**当該`M`が実際に与えられた厳密fiberの範囲**に限る。全fiberの非空・非単射や、新しいpresentationによる忠実比較反映は主張しない。むしろ元商との差は具体的なobstructionとして記録される。

## 6. exact-source CIとGit tree受領書

| 段階 | 認証済みの結果 |
| --- | --- |
| 新規定理CI | [#42535577314](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42535577314) SUCCESS |
| 定理Scoped Strict Lean | **9,102 / 9,102 SUCCESS** |
| 定理Governance | **5 / 5 SUCCESS** |
| 新規19宣言の公理監査 | **8件公理なし・11件標準公理のみ**、`sorryAx`なし |
| 変更Lean warning / error | **0 / 0** |
| 公開import CI | [#42536059534](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42536059534) SUCCESS |
| 公開KuuOSFormal | **10,363 / 10,363 SUCCESS** |
| 公開Governance | **32 / 32 SUCCESS** |

定理source HEAD `905c33cb3b610c4e92957cdd1c90776b61bb1db4`、test-merge `3b8d31e7dc0fa2c633b10a54ab3d81a96eb05652`、squash/main `d4a85788b5c6c724d3a45f356b3eb82e2db82632` の共通tree `7101b94d83659ee32b934551dd62ba0559900151`。

公開source HEAD `637e90ce79150a70aca27c52a12854a6ab9c63d6`、test-merge `efc5e7a894de52ca9f28b8d3688e74a8134c5316`、squash/main `889c10fa66ba2531854153a2d3d5ce266464290e` の共通tree `07986095e9727e8c3412212d3f5e1dd63e789f53`。

## 7. 新規19宣言の公理監査全文

最終CIに表示された各宣言の`#print axioms`を照合。標準依存は`propext`、`Quot.sound`に限定。`Classical.choice`も`Lean.ofReduceBool`も新規公理として要求されず、`sorryAx`は出現しない。

| 宣言 | 使用公理 |
| --- | --- |
| `SelectedRawCongruentNineteen` | なし |
| `selectedRawCongruent_inherit` | なし |
| `selectedRawCongruent_minimal` | なし |
| `selectedRawCongruentSetoid` | なし |
| `selectedRawCongruentClass` | なし |
| `selectedRawCongruentClass_eq_iff` | `propext, Quot.sound` |
| `selectedRawCongruentProject` | `Quot.sound` |
| `selectedRawCongruentProject_onClass` | `Quot.sound` |
| `selectedRawCongruentProject_surjective` | `Quot.sound` |
| `selectedRawCongruentReverse` | `Quot.sound` |
| `selectedRawCongruentReverse_onClass` | `Quot.sound` |
| `selectedRawCongruentChain` | `Quot.sound` |
| `selectedRawCongruentChain_onClass` | `Quot.sound` |
| `selectedRawCongruent_reverseUnitComparison` | なし |
| `selectedRawCongruent_rightStrictUnitComparison` | なし |
| `selectedRawCongruent_leftStrictUnitComparison` | なし |
| `selectedRawCongruentProject_noninjective_reverse` | `propext, Quot.sound` |
| `selectedRawCongruentProject_noninjective_right` | `propext, Quot.sound` |
| `selectedRawCongruentProject_noninjective_left` | `propext, Quot.sound` |

## 8. 保存条件・研究の限界と次段

元F55/P77/GK5CGから元selected19までのType値証拠、証明履歴、独立presentations、公開root107を保持。Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`を固定し、保護#1558はDraft／OPEN／未マージ。append-only／tighten-only／overwrite-forbidden／same-root。

新presentationの**全射は忠実性ではない**。今回、与えられた元18D証拠のあるfiberで非単射も証明した。数値観測の一致をraw証拠の同一性に昇格させない。別の16D fiberにまたがる文脈合同性、7D whiskeringへの自然性、20D coherenceやgluingは未認証のまま維持する。

**次段Qi v5.51の研究候補：** 新商でも保存される元18D ordered traceやその他の不変量を、7構成子全ての保存証明によって商へ降下させる。文脈合同性の拡張で残るobstructionを具体的に観測し、局所性から大域性への不正な昇格を避ける。

本正式記録はdocs-onlyであり、Lean定理・workflow・pinには変更を加えない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
