# Qi v5.37 — 真正18D文脈閉包・局所19D単位coherence・証拠商の履歴降下と非降下

2026年11月8日 JST。Canonical repository: `itakura-hidetoshi/KuuOS`、branch: `main`。
前段Qi v5.36の定理 #3336、公開集約 #3337、正式記録 #3338（全MERGED）を正本として継承。
元F55/P77/GK5CG、元6D〜14Dの各Type値証拠、v5.23〜v5.36までの独立選択presentationは一切変更していない。
運用原則：**append-only／tighten-only／overwrite-forbidden／same-root**。

## 1. 唯一の正本とexact-source CI

| 項目 | GitHub MCP／独立CI結果 |
|---|---|
| 定理PR | [#3339](https://github.com/itakura-hidetoshi/KuuOS/pull/3339) **MERGED** |
| 定理source HEAD | `ea8cc04e6c3737030778fb1c06eeaecd02850193` |
| 定理test-merge | `7601d660367aa29cf0d95db1fbc7cbf769fa93c4` |
| 定理squash main | `1b2f0d249e352038cd9e53ada405b1de12d32916` |
| source／test-merge／squash Git tree | **`49e35ae074016c53f7c1e54f4629ebdde00e7b15` 完全一致** |
| 定理exact-source CI | [#42463381138](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42463381138) **completed/SUCCESS** |
| Scoped Strict Lean | **9,089 / 9,089 SUCCESS** |
| 定理Governance | **5 / 5 SUCCESS** |
| 新規宣言の公理監査 | **25 / 25**：20件公理不要、5件標準公理のみ |
| 標準公理 | `propext`、`Quot.sound` のみ |
| 新規`sorryAx`／追加公理 | **なし／なし** |
| 変更Lean error／warning | **0／0** |
| 定理差分 | 新規Lean 1ファイル、628行追加、削除0 |
| 公開集約PR | [#3340](https://github.com/itakura-hidetoshi/KuuOS/pull/3340) **MERGED** |
| 公開import source HEAD | `92d639748eae79407704eebdbd9e36cb7580de27` |
| 公開import test-merge | `45639972622fc9ae31c431494455adfb526d5438` |
| 公開import squash main | `a19c5cd5b3e38f3a9f52acbdec6c9aa662544518` |
| 公開source／test-merge／squash Git tree | **`32c48c8abc82d2b51a84659c7aad92c3a1a148e2` 完全一致** |
| 公開exact-source CI | [#42463751124](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42463751124) **completed/SUCCESS** |
| KuuOSFormal全体Strict Lean | **10,350 / 10,350 SUCCESS** |
| 公開Governance | **30 / 30 SUCCESS** |
| 公開変更 | `formal/KuuOSFormal.lean`へのimport 1行、削除0 |
| 公開root／保護PR | root107維持／#1558 Draft・OPEN・未マージ |
| 固定Lean／mathlib | `v4.30.0-rc2`／`5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

[Lean4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ContextualEighteenNineteenV5_37.lean)。

独立のCIログは `lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77ContextualEighteenNineteenV5_37` について
`Build completed successfully (9089 jobs)` を明示。
25件の`#print axioms`を確認し、20件に公理依存がなく、残り5件も標準`propext`／`Quot.sound`のみ。
公開集約CIは独立して `Build completed successfully (10350 jobs)` を記録した。

## 2. 真正18Dの独立文脈閉包

新規`SelectedContextualEighteen`は、v5.35の元`SelectedLocalEighteen`のType値証拠を
`inherited`構成子として保存する。
`oldEighteenToContextual_injective`はこの埋込みの**単射性**をLean4で証明している。

残る`whiskerLeft`、`whiskerRight`は真正`SevenRewrite`と`ContextFrameEleven`の
依存添字が一致する場合にだけ許される。`strict`／`reverse`／`chain`を併せた
**6構成子すべて**について、

```lean
selectedContextSeventeenTrace l r J =
  selectedContextSeventeenTrace l r N
```

を`selectedContextualEighteen_preservesSeventeenTrace`で証明した。
これは粗いイベント計数ではなく、`List Bool`の**順序付き完全履歴**である。

新しい`selectedContextEighteenSetoid`は、厳密同じ16D端点を共有する
平行17D生証拠を、選択18Dの具体的な比較Typeの`Nonempty`で商とする。
`selectedContextEighteenClass_eq_iff`は商クラスの等号と実際の18D比較の存在を同値にし、
`selectedContextEighteenTraceOnQuotient`は`Quotient.lift`で完全な履歴を商へ降下させる。
これはv5.36の局所18D商とは**別の選択商**であり、同じ元証拠のraw Eqを主張しない。

## 3. 真正型付き局所19D単位比較

`SelectedContextEighteenTrace`ではなく、正確な定数名
`selectedContextEighteenTrace`で**生18D証拠自体**の外側文脈履歴を観測する。
`inherited`／`strict`は空履歴、左右whiskeringは順序付き`false`／`true`を前置し、
`reverse`は履歴を保存、`chain`は履歴リストを連結する。

新しい独立`SelectedLocalNineteen`は以下の5種類の構成子のみを持つ：

- `strict`：同一の真正raw18D証拠の反射。
- `unitPrepend`：任意の真正旧18D証拠 `M : SelectedLocalEighteen W l r J N` に対して
  `chain (strict J) (inherited M)` と `inherited M` を、同一17D端点内で比較する。
- `unitAppend`：`chain (inherited M) (strict N)` と `inherited M` の同型の局所比較。
- `reverse`／`chain`：その型付き局所比較だけの反転・合成。

`selectedLocalNineteen_preservesEighteenTrace`は上記5構成子の構造帰納により、
始終点の**完全な順序付きraw18D外側履歴**が等しいことを証明する。
`selectedNineteenSetoid`・`selectedNineteenClass_eq_iff`で真正同一17D fiberの
19D証拠商を定義し、`selectedNineteenTraceOnQuotient`で完全履歴を
`Quotient.lift`として降下させた。

## 4. 局所19D商でのrawタグ非降下

左側の具体的critical pair
`A = chain (strict J) (inherited M)`、`B = inherited M`は
**新しい選択19D比較Typeで比較可能**なので `[A]₁₉=[B]₁₉` である。
しかし生の18D構文先頭タグは

```
selectedContextEighteenTopTag l r A = 5
selectedContextEighteenTopTag l r B = 0
```

となる。
`selectedNineteenUnitPrepend_rawDistinct`は `A ≠ B` を、
`selectedNineteen_noRawEqualityInterpreter`は選択19D比較をraw Eqへ解釈できないことを、
`selectedNineteen_noTopTagDescent`は**生の先頭タグを忠実に再現する商上関数が存在しない**ことを形式証明した。

したがって同じ局所19D商で、

- 順序付きの外側文脈履歴は降下可能。
- 生18Dのトップ構成子タグは降下不能。

この両立が数学的に確定している。

## 5. authority境界・限界

- v5.36の`SelectedOuterSwapClosure`は共通`List Bool`**観測空間上**の隣接交換商であり、今回の18D/19D証拠商とは別の同値関係。
- 観測swapでLR/RLが一致しても、依存型の異なるraw17D/18D証拠の同一視には**ならない**。
- 真正下位12D〜14D比較パケットだけでは異なる高次fiberの端点同一性は導けず、v5.34のtrace保存型高次gluing gate障害も解除されていない。
- 新しい19D単位比較は厳密同一17D端点の局所生成元であり、任意の混合19D交換・全面的Gray coherenceを主張しない。
- 元証拠、旧定理の仮定、Lean/mathlib pin、public root107、保護#1558は不変。

## 6. 次段Qi v5.38

- 真正18D左右文脈の二重transportを**別々の依存fiberに保持**して構成する。
- 各fiberの19D商から共通観測`List Bool`および有限swap商への写像を、元の証拠の履歴を失わずに接続する。
- source-level比較へ進むための**追加の境界同一性／transport証拠**を必要十分条件として検討し、不足時には具体的obstructionを提示する。
- 元raw Eq、異種依存fiberの無条件接合、弱い仮定への置換をしない。

すべてappend-only、exact-source CIで独立再観測し、定理・公開集約・正式記録を段階的に検証する。
