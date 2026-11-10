# Qi v5.92 — 真正旧18Dの依存型unitパラメータ履歴と括弧残差（Lean4形式証明）

2026年11月11日 JST。唯一のcanonical正本：`itakura-hidetoshi/KuuOS`／`main`。対象は元の真正依存型`SelectedLocalEighteen`、元のraw17D端点、v5.73の非結合的内部括弧観測、v5.89の元unit数、v5.91の2-unit真正閉路である。空・縁起・二諦・中道との対応は命名／解釈層であり、Lean4の証明が哲学的同一性を証明したものではない。

## 1．認証済みGit来歴

- 基準：Qi v5.91三段階統合後main `33236cc9490bc6982030c73f5c235ea8de842851`。
- [定理PR #3506](https://github.com/itakura-hidetoshi/KuuOS/pull/3506) **MERGED**。元のLean4ファイルを一切変更・削除せず、新規`formal/KUOS/Architecture/QiWuxingGK5CHP77OriginalUnitParameterHistoryV5_92.lean`のみ**349行追加**（修正後）。15宣言／実`#print axioms`15件。
- 定理認証source `de04d1703149756c54992ba718f598c1e70d218e`。定理統合後main `1cc11462ec22de4e155e2da6e5efe78b241218e5`。source／test-merge／squash後mainのGit tree `076579c23f0786bb03c5a49b5592be90ffd3a57d`完全一致。
- [修正後定理CI #42908182854](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42908182854) **completed/SUCCESS**。Scoped Strict Lean **9,144/9,144**、Governance・独立Kuu Core・整合性検証すべてSUCCESS。
- [公開import PR #3507](https://github.com/itakura-hidetoshi/KuuOS/pull/3507) **MERGED**。`formal/KuuOSFormal.lean`に新規import**1行のみ**追加。公開認証source `0db6cde12170fc0b2ec17e47bddd52d16c254f74`、公開統合後main `b59660117f6049a89b6ee5e51b1031a01bdcf31f`。source／test-merge／squash main Git tree `79d6ed58a3618884f59957c1c7c719940b4858e7`完全一致。
- [公開CI #42909417088](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42909417088) **completed/SUCCESS**。公開`KuuOSFormal`依存閉包Strict Lean **10,405/10,405**、Governance **30/30 SUCCESS**。
- 両独立CIで実公理監査15/15：**公理不要9**、**標準公理のみ6**（`propext`だけ5件、`propext`・`Quot.sound`1件）。新規`sorryAx`なし、変更Lean error/warning **0/0**。
- 固定環境はLean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**。公開root107維持、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 2．元の依存型unitパラメータの観測

`SelectedV592OriginalUnitAtom`は、同じ上位16D文脈のもとで

```text
Σ J : genuine raw17D endpoint,
  Σ N : genuine raw17D endpoint,
    SelectedLocalEighteen W l r J N
```

という**元の型付き証拠そのもの**を収納する。新しい19D比較や等号を構成しない。

`selectedV592OriginalUnitHistory`は、元の5構成子を直接再帰して、真正`unitLeft before F G C after`／`unitRight before F G C after`の葉を元証拠・本来の17D始終端・付加パラメータごと順序付きリストに記録する。`strict`は空列、`reverse`は葉の元payloadを保持し、`chain`は左右リストを順序付き連結する。これは**payload-only履歴**であり、反転の外側の位置や`strict`の位置・raw括弧木は意図的に別の観測量へ残す。

`selectedV592OriginalUnitHistory_length`は**任意の元旧18D依存型証拠**Mに対して

```text
History(M).length = OriginalUnitCount(M)
```

を証明した。これはrestricted fragmentの定義にunitCountが一致するという条件付き主張ではない。

## 3．2-unit往復閉路：履歴の一致は異fiberの等号ではない

v5.91の真の元証拠`U:J→N`から

```text
Forward(U)  = chain U (reverse U)  : J→J
Backward(U) = chain (reverse U) U  : N→N
```

を元Typeのまま構成する。v5.92は両方向で`History = History(U) ++ History(U)`を証明し、元のunit数1なら歴史リスト長は双方2と証明した。

ただし、元unitLeft・unitRightの`J≠N`はv5.91によって証明済みであり、この二つの閉路は**異なる真正raw17D fiber**に属する。歴史リストが等しくても、raw旧18D証拠の異fiber等号・比較居住性は得られない。

## 4．同一真正fiberでの「履歴一致・括弧不一致」実例

元unitLeftまたはunitRightの真正付加パラメータ`before/F/G/C/after`を固定し、その元証拠を`U:J→N`、真正往復閉路を`R = chain U (reverse U):J→J`とする。実際の同一`J→J`fiberで、

```text
A = chain (strict J) R : J→J
B = chain R (strict J) : J→J
```

を構成する。元旧18Dの`strict`は元unit数0、元unit payload履歴は空。そこで`selectedV592ActualLeftTwoUnitSameFiberHistoryGap`と独立の`...Right...`が次をそれぞれ証明する。

```text
History(A) = History(B)
Bracket(A) ≠ Bracket(B)
OriginalUnitCount(A) = 2
OriginalUnitCount(B) = 2
A ≠ B   (ACTUAL original typed old18D equality)
```

括弧はそれぞれ`oldJoined oldStrict (oldJoined oldUnitLeft (oldReversed oldUnitLeft))`と`oldJoined (oldJoined oldUnitLeft (oldReversed oldUnitLeft)) oldStrict`（右unitも対応）であり、元の`chain`への結合律や単位律は追加していない。括弧が異なることを使って元raw証拠が異なると証明するため、**履歴の非単射の実例**だが、**同じ内部括弧指紋の衝突ではない**。

## 5．Lean4エラー修正の型構造上の原因

初回定理source `0acbf85b0a4551f894d7d108b4ef4ec3875f4ff2`の[CI #42907366988](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42907366988)は、新規ファイルの**6件**の`Expected type must not contain free variables`によりFAILURE。元の5構成子、v5.73内部括弧観測、v5.89 count、v5.91元往復閉路、新規Lean全文を照合した。

発生理由は、`l,r,before,F,G,C,after`等の自由変数を式の内部に残したまま閉じた命題を判定する`decide`を直接使ったこと。左／右の非等号各1件は、実際に定義計算で得られる**閉じた非結合括弧木**へ`change`してから`decide`を使用。元unit数の等式各2件は実際の定義計算に従って`rfl`へ変更した。合計6箇所であり、定理の前提／結論、元のLeanファイル、固定Lean/mathlibは変更していない。修正後CIと公開CIは独立にSUCCESS。

## 6．障害の保持／次段v5.93

**認証済み**：元依存型のunit葉payload履歴、歴史長＝元unit数、真正2-unit往復閉路の歴史、同一fiberの2-unit**履歴一致だが内部括弧不一致**の実例。

**NO_DATA**：同一真正raw17D exact fiberで、**内部括弧指紋まで等しく、元旧18D raw証拠が異なる**対の実在。v5.91の元unitCount≥2はその仮説的衝突の**必要条件**であって十分条件ではない。元旧5／新7の選択19D比較の一般的な居住性・両Typeの大域同値、異fiber gluing、WORLD／20Dの降下、実行・制度的権限も未認証。

**次段Qi v5.93候補**：真正同一17D fiber内で2-unit旧18D証拠の**内部括弧等号そのもの**を仮定／構成可能な条件を切り分け、元unit付加パラメータの一致／不一致を証明可能な範囲で復元する。勝手なfiber貼合を行わず、形式証明できない条件はobstructionとして保持する。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
