# Qi v5.76 — 全イベント語一致後の継承葉を保持する非結合括弧障害（Lean4形式証明・公理実監査）

2026年11月10日 JST。対象は真正の元`SelectedContextualEighteen`依存Type値と、元の旧5構成子`SelectedLocalNineteen`・独立した新7構成子`SelectedRawCongruentNineteen`による同一exact fiberの真正商。哲学上の「空」「縁起」との対応は命名・解釈の層であり、Leanが哲学的同一性を証明したものではない。

## Canonical正本・source・認証来歴

- Repository: `itakura-hidetoshi/KuuOS`、canonical `main`。研究開始時のQi v5.75正式統合main HEAD `62f3af1042d41a9fa5700c83c5288c8a3736c140` が唯一の基礎正本。
- [定理PR #3458](https://github.com/itakura-hidetoshi/KuuOS/pull/3458) **MERGED**。新規Lean 1ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77InheritedSensitiveBracketResidualV5_76.lean`、552行追加、既存ソース変更・削除0。新規34宣言すべてに実`#print axioms`を追加。
- 定理認証source `8d5aa73fd08d44d6032c42d79f79423c645c631e`、test-merge `f85e244d7c94d001e0f2962f6650a7b7e5bbd9c7`、squash `2ee42486b517b132c728d871f823512d78f9dac9` のGit treeはすべて **`66d019654100fa87fa58332bfb1d197fc1cd84a9` で一致**。
- [公開import PR #3459](https://github.com/itakura-hidetoshi/KuuOS/pull/3459) **MERGED**。`formal/KuuOSFormal.lean`へv5.76 importを1行だけ追加。既存import・公開root・旧ソースは不変更。
- 公開認証source `a257537e0f25f71c51979af4fcd83a908b8fd65a`、test-merge `4078a3d033013283a3de1a2495102e6955ae299c`、squash `f02e757e5da7861f31fd6b7c9852450001ec994c` のGit treeはすべて **`9a6da30099960550816bbbc488e2e6a679366825` で一致**。
- 固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107。保護validation-only [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 真正継承葉を消去しない非結合構文

v5.70の従来raw単位簡約括弧は、元の`inherited(old18)`葉も単位として消去する。この情報損失を分離する独立観測`SelectedInheritedSensitiveRawBracket`を元の真正Type値上に構造再帰で定義した。

```text
inherited old18       ↦ source
strict N              ↦ unit
whiskerLeft/Right A   ↦ B(A)
reverse A             ↦ reversed (B(A))
chain A C             ↦ join (B(A)) (B(C))
join unit t           ↦ t
join t unit           ↦ t
join s t (otherwise)  ↦ joined s t
```

`source`は、任意の旧18D依存Type証拠の等式ではなく、継承葉が存在したという新しい独立構文原子。非単位元同士の`joined`には一般の結合則を課さない。実際の旧selected19の**5構成子すべて**、独立した新raw合同性の**7構成子すべて**で保存性を形式証明。特に旧`unitPrepend`／`unitAppend`はraw strict単位を挿入・除去するにすぎず、一般のraw`chain`結合則を与えない。新`rawReverse`・`rawChainLeft`・`rawChainRight`でも帰納仮定と構文変換の互換性を確認した。

旧商と新商には別々の`Quotient.lift`で降下し、元の旧→新商projectionへの因子化を証明した。元Type18Dと独立旧・新Type19Dは変更も同一視もしていない。

## 全v5.75観測一致と新しい商障害

任意に実在する元17D端点`N`について、真正元`SelectedContextualEighteen`の厳密な構成子で同一`N→N`の二証拠を作る。

```text
I = inherited (SelectedLocalEighteen.strict N)
R = reverse (strict N)
A = chain (chain I R) I
B = chain I (chain R I)
```

両者は旧九観測、**全次数の祖先塔`Nat→Nat`と全次数の直接連続反転数塔`Nat→Nat`**、完全ordered反転ラン列、v5.70の非結合単位簡約raw括弧、継承葉数（両方2）、元old18D根タグのordered列（両方`[strict,strict]`）、元old18Dの完全内部非結合構文リスト（両方`[oldStrict,oldStrict]`）、v5.74のordered反転位置葉数列（両方`[0]`）、v5.75の**完全イベント語（両方`[inherited,rawReverse,inherited]`）**まで一致する。無限塔の関数等式は`funext`、次数別`Nat.add_assoc`、`Prod.ext`により証明した。**Natの加算の結合則から元証拠のchain結合則は推論していない**。

新観測の値だけは以下で異なる。

```text
B(A) = joined (joined source (reversed unit)) source
B(B) = joined source (joined (reversed unit) source)
```

二つの自由な非結合値は`DecidableEq`で異なり、新観測は実際の新7構成子商へ独立に降下する。従って**真正の新商クラスが異なり、両証拠間の新19D Type値比較は存在しない**。v5.75の全観測を新イベント語まで含めた結合商観測は、この真正同一端点`N→N`商上で非単射。新括弧と商クラスをその観測から復号する全域decoderも存在しない。

## Exact-source型検査・公理・source tree監査

- [定理exact-source CI #42725948603](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42725948603)：**completed SUCCESS**。Scoped Strict Lean **9,128/9,128**、選択Governance・Core Autonomy **SUCCESS**。
- [公開exact-source CI #42726543992](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42726543992)：**completed SUCCESS**。KuuOSFormal Strict Lean **10,389/10,389**、選択Governance・Core Autonomy **SUCCESS**。
- 新規34宣言の`#print axioms`を**両方の実ログですべて照合**。**公理なし14、標準`propext`／`Quot.sound`のみ20、`Classical.choice`なし、新規`sorryAx`なし**。変更Lean error／warning **0／0**。source/test-merge/squashのGit treeは各段階で一致。
- 文書のみの正式記録PRではStrict Leanを意図的に`SKIPPED`とし、選択Governance・Core Autonomyを検査する。記録自体は証明の代用にならない。

## 認証境界と次段Qi v5.77

証明は**元の真正17D端点Nが与えられた`N→N`fiber**における局所非単射性である。任意の異端点`J→N`fiberの非空性・同様の非単射性は主張しない。新しい継承葉保持括弧まで観測に加えた後、すべての実際の商クラスを完全に復元できるかも**未認証（NO_DATA）**。今回の二証拠は新括弧観測で区別されるので次段の反例に流用できない。

20D gluing、WORLD横断降下、哲学的同一性、制度的・実行権限は未認証。append-only／tighten-only／overwrite-forbidden／same-rootを維持する。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
