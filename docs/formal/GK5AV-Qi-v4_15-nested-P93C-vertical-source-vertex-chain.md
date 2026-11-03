# F112-P94D3GK5AV / Qi v4.15 — P93C-in-P94A内部二段証拠の真正source-vertex鎖

**正式証明記録／2026-11-03 JST。** 正本リポジトリ：\`itakura-hidetoshi/KuuOS\`、canonical \`main\`、権限方向 **独立Kuu → Qi**。strict 空と選択presentation・証拠型・C60 shadow・物理gaugeを無条件に同一視しない。元F54/F55/P89、選択P92B/P93C/P94Aの既存定義は一切変更せず、新規Leanモジュールと公開importのみを追加。公開root **107**、保護PR **#1558 Draft／OPEN／未マージ**を保持。Lean **v4.30.0-rc2**、mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6** を固定。

## 1. Exact-source CI と正式マージの確定記録

| 項目 | 確定結果 |
| --- | --- |
| GK5AV独立定理 | [PR #3013](https://github.com/itakura-hidetoshi/KuuOS/pull/3013) — MERGED |
| GK5AV検証対象HEAD | \`abe22d081513c94091cf8f9530922065faab3cd6\` |
| GK5AV squash SHA | \`1b27258c33d7f823836d021d72395a01ecbe1e54\` |
| GK5AV exact-source CI | [Governance #41579826031](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41579826031) **30/30 SUCCESS** |
| GK5AV Strict Lean | **9,248 / 9,248 SUCCESS** |
| GK5AV公理監査 | **10件**、\`sorryAx\`なし。標準 \`propext\`・\`Classical.choice\`・\`Quot.sound\` または公理依存なし |
| Qi v4.15物理統合 | [PR #3014](https://github.com/itakura-hidetoshi/KuuOS/pull/3014) — MERGED |
| Qi v4.15検証対象HEAD | \`bd1a88b6be9b40fc7891bdf0bd03245eea9b4187\` |
| Qi v4.15 squash SHA | \`2b06b3c9608a9a6618d7a303b29e552877fbca69\` |
| Qi exact-source CI | [Governance #41580343195](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41580343195) **30/30 SUCCESS** |
| Qi Strict Lean | **10,175 / 10,175 SUCCESS** |
| Qi公理監査 | **3件**、許容標準公理のみ、\`sorryAx\`なし |

最終ソースにLean compiler error/warningはなく、新規公理・\`sorry\`・\`admit\`・\`native_decide\`・Gray復元・無条件gluingはない。

## 2. P93C内部の真正P92B中間証拠を元F55へ反射

GK5AUはP94A**全19**構成子および内包P93C**全16**構成子の、真正Type値付きP92B証拠に対するsource-holeを再帰的に検査した。GK5AVはその監査を保ったまま、**P93Cの垂直二段合成**の内部で実際に元F55を復元する新しい段階である。

真のP93C四セル \`left : P93C(f,q)\` および \`right : P93C(q,g)\` について、\`P93C.trans left right\` がsource-holeを持たなければ、P92B中間証拠 \`q\` に対する真正依存型元F55 fiber \`{m : OriginalF55 // φ(m)=q}\` は非空である。定理は \`nativeGK5AVP93C_clean_trans_middle_fiber\`。

さらに真正P94A構成子 \`P94A.old (P93C.trans left right)\` のsource-saturationからも全く同じ元F55 fiberを導く（\`nativeGK5AVP94OldP93C_clean_trans_middle_fiber\`）。P94Aの \`old\` で包まれてもP93C内部の元証拠復元条件は消えない。P93C全16構成子の左右端点証拠がφ像外ならsource-holeとなる補題も新たに形式証明済み。

重要なのは、\`P93C.old\` が受け取る選択証拠 \`P92B.original(f)\` を、元F55全9構成子を再帰的に解釈する真正構造写像 \`φ(f)\` と自動的に同一視しないことである。shadow・商等式・左右偶奇から元F55証拠を捏造しない。

## 3. 元F55 source-vertexの真正二辺鎖と条件付きP89降下

真の元F55 Type証拠 \`f,g\`、選択中間P92B証拠 \`q\`、実在する真正P94A四セル \`left : P94A(φ(f),q)\` と \`right : P94A(q,φ(g))\` を取る。中間 \`m : OriginalF55\` が \`φ(m)=q\` を満たすなら、GK5AVの新しい \`nativeGK5AVTwoStepSourceChain\` は、**元F55の三節点 f→m→g を持つ実際の二辺鎖** \`NativeGK5ASSourceVertexChain f g\` を構成する。

その二辺の選択P94A証拠は、与えられた \`left/right\` を正確な依存型等式 \`φ(m)=q\` によって移送したものである。数値shadowや元証拠のない任意のグラフではない。GK5AVの \`nativeGK5AVP94CleanTrans_sourceChain_reflect_or_bad\` は、GK5AUのsource-saturationから実際の中間 \`m\` を得てこの鎖を構成し、元P89四セル \`P89(f,g)\` が存在するか、当該鎖に \`HasBadStep\` が存在することを証明する。

\`nativeGK5AVP93CInsideP94_sourceChain_reflect_or_bad\` は同じ議論を、**P94A.oldの中の真正P93C trans**に対して証明する。\`nativeGK5AVP93CInsideP94_descends_of_noBad\` は、指定された二辺鎖に局所BadStepがない場合に元P89四セルの存在を形式化した。

これは元F55の局所比較と非反射障害の型付き分離である。**選択P94A raw証明項全体とsource-chain.toSelectedがType値として同一**であるとは証明していない。また、任意のP94Aの文脈・whisker・水平interchange・独立単位生成元の内部をすべてこの二辺鎖へ無条件正規化したわけでもない。全構成子のsource-hole検査と、垂直二段のconstructive descentを混同しない。

## 4. 真正北C60のP93C二重反射、偶奇0の限界

北C60第1〜3の真正F45単位経路に対して新しく選択されたP92B \`assocNaturality\` 証拠を \`q_N\` とする。元F55の対応する証拠型は空であり、GK5AVは実際の証明項 \`w_N = P94A.old (P93C.trans (P93C.refl q_N) (P93C.refl q_N))\` を構成した。

\`nativeGK5AVNorthNestedP93CDoubleRefl_obstruction_zeroGrade\` が示すのは、**この内部P93C二段合成の元F55 φ-fiberが空、P94A source-saturationが不成立、しかし左右文脈単位回数はそれぞれ \`0 mod 2\`**という同時事実である。元F55の2証拠が存在しないこの例を、元P89→P94Aの非単射性を示すGK5AQ BadPairとは主張しない。

## 5. Qi v4.15 北C60物理境界との接続

Qiの新規3定理は、元の北四段pentagon長短の**二Nat・F54/F55・二圏Blocksを保持**したままGK5AVの独立証明を特殊化する。

- \`fivefoldGK5AVNorthP93CInsideP94_sourceChain_reflect_or_bad\`：P94A内の真正P93C二段証明から元F55中間証拠と二辺source-vertex鎖を構成。元P89反射または実際の局所BadStepを確定。
- \`fivefoldGK5AVNorthP93CInsideP94_descends_of_noBad\`：その真正二辺鎖で局所BadStepがなければ、元P89四セルに降下する。
- \`fivefoldGK5AVNorthPhysicalNestedP93CDoubleReflSourceGate\`：内部元F55 φ像欠損と偶奇\`(0,0)\`を保ち、**第五around Dart閉路**、**04・43の物理方向と圏論方向の相違**、Qi v4.10の**条件付き非単射性 iff 元GK5AQ反射障害**を一つの定理で保持する。

物理的Dart frameの存在は、欠けた元F55証拠を供給しない。元P89→P94Aの無条件単射性・非単射性はいずれも未証明である。

## 6. Lean4記法エラーの根本原因と修正履歴

GK5AV最初の [CI #41579422093](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41579422093) では、P93C全16構成子のsource-hole端点補題に使った \`cases w <;> simp [nativeGK5AUP93CSourceHole, missing]\` が、依存型recursorを過度に展開し、\`whnf\` deterministic heartbeat上限に達した。数学的仮定不足でも他の構成子の型不一致でもない。

修正HEAD \`abe22d081513c94091cf8f9530922065faab3cd6\` は、**同じ全16構成子のcase splitを保持**し、端点の選言を \`cases w <;> exact Or.inr (Or.inl missing)\` または \`Or.inl missing\` で直接組み立てた。タイムアウト閾値や定理仮定を弱めず、最終CI・公理監査に成功した。旧Leanソースの上書きはない。

## 7. 次の研究境界：GK5AW（仮称）

GK5AVは **全構成子source-hole監査 → P93C内包の垂直二段source-vertex構成**を実現した。次はP93C/P94Aの各primitive（whisker・左右context・pre/postcompose・horizontal/interchange・新unit）の、元P89反射に本当に必要な**generator-indexed local 4-cell reflection certificate**を別途定式化し、複数の依存型履歴へ合成する条件付き局所・大域ゲートを目指す。source-holeがないというだけで元P89の高次証拠が自動生成するとはしない。

**Leanソース：** [GK5AV独立定理](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AVNestedVerticalSourceChain.lean)、[Qi v4.15](../../formal/KUOS/Architecture/QiWuxingGK5AVNorthNestedSourceVertexChainV4_15.lean)、[GK5AU／Qi v4.14正式記録](GK5AU-Qi-v4_14-p94-p93-internal-source-history-saturation.md)。
