# Qi v5.75 — 完全反転位置観測の先に残るraw反転／旧18D継承イベント順序の障害（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は真正の元contextual18D依存Type値と、同じ元17D端点fiberの元5構成子selected19比較・独立した新7構成子raw合同性比較による真正商である。空・縁起との対応は解釈・命名層であり、Lean4で哲学的同一性が証明されたという主張ではない。

## 唯一のcanonical正本と実装

- Repository: `itakura-hidetoshi/KuuOS`、canonical `main`。研究開始時のQi v5.74正式統合main `90b99181917b9f863b82409f6cfe15f7188f8192` を基礎とした。
- [定理PR #3455](https://github.com/itakura-hidetoshi/KuuOS/pull/3455) MERGED。新規Lean 1ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77ReverseInheritedEventInterleavingV5_75.lean`、475行追加、既存ファイルの削除・変更なし。
- 定理認証source `ee931bdc8926474a0735b0bdc4f75df2711b8a21`、test-merge `e1e70ee2227bbe1b78bd8271c9d8b4f1ccae0bcd`、squash `e467094284560cc7adaff1900d6668429f79ece4` のGit treeはすべて `36350419d633239e35af7875f78f2685c0423338` で一致。
- [公開import PR #3456](https://github.com/itakura-hidetoshi/KuuOS/pull/3456) MERGED。`formal/KuuOSFormal.lean` にv5.75 importを1行だけ追加、既存import削除0。
- 公開source `bd74323440d10e22d09962b8370979daa3a7580e`、test-merge `efb3d14aa4733e3b2cb6d640ada52d4876f65c7f`、squash `d2343a21b96e2146df201d14bd25f222c890f8f5` のGit treeはすべて `1967ba20725570b535bb1ab16f37aa44a00077b4` で一致。
- 固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107。保護validation-only [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ維持。

## 新しい独立観測E：真正rawイベントの交錯順序

真の `SelectedContextualEighteen W l r J N` 証拠に構造再帰し、`SelectedReverseInheritedEvent` という独立の二値構文を定義する。元Type値の同一視・型変更ではない。

```text
inherited old18      ↦ [inherited]
strict N             ↦ []
whiskerLeft/Right A  ↦ E(A)
reverse A            ↦ rawReverse :: E(A)
chain A B            ↦ E(A) ++ E(B)
```

旧selected19の全5構成子、新selectedRawCongruentNineteenの全7構成子で保存性を個別に形式証明。新rawReverseと両rawChainの文脈閉包にも整合し、**旧商・新商それぞれに独立にQuotient.liftで降下**する。両者が元旧→新projectionを通じて整合することを証明した。旧新19Dの比較Typeは相互に同一視しない。

## v5.74の完全観測一致と真正商の不一致

任意に実在する元17D端点`N`に対し、真正元contextual18Dの構成子で同じ`N→N` fiberの二証拠を作る。

```text
R = reverse (strict N)
I = inherited (SelectedLocalEighteen.strict N)
A = chain R I
B = chain I R
```

v5.73までの元九観測、**全Nat次数の祖先塔・全Nat次数の直接連続反転数塔**、完全ordered反転ラン列、単位簡約非結合raw括弧形、旧18D継承葉数1、旧18D根タグリスト`[strict]`、完全内部旧18D括弧リスト`[oldStrict]`がすべて一致する。さらに**v5.74のordered反転位置継承葉数リストも両者`[0]`で一致**する。

しかし、新しい独立観測は`E(A)=[rawReverse,inherited]`、`E(B)=[inherited,rawReverse]`で相異なる。Eは実際の新7構成子商に降下しているため、**両者の新商クラスは等しくなく、真正な新19D比較Typeも非空ではない**。前段全観測を新site列まで合わせた関数 `selectedRawCongruentDoubleBracketCountRootInnerSitesObservation` は、各真正`N→N`商で非単射。イベント列と商クラスの全域decoder不存在も証明した。

**証明範囲は真正同一端点`N→N`に限定**される。任意の`J→N`異端点fiberの非空性・同様の非単射性は今回の定理からは主張しない。元の証拠を破棄したり、raw構文の見かけ上の違いだけで商クラス不一致を推測したりしていない。

## 初回Lean4失敗と修正経路

初回exact-source CI [#42722358470](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42722358470) は`selectedReverseInherited_witnessRootInnerObservedEq`の`rfl`一箇所で失敗。全観測の2本の`Nat→Nat`関数を、raw鎖中のNat加算順が違うのに定義上同一としたことが原因だった。定理の仮定や元証拠には触れず、全次数の独立補題`selectedReverseInherited_witnessAncestorTowerEq`・`selectedReverseInherited_witnessRunTowerEq`を追加し、`funext`と`Prod.ext`により真の外延的等式へ修正した。

## exact-source Strict Leanと新公理の監査

- 修正後[定理CI #42723055504](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42723055504)：completed **SUCCESS**。Scoped Strict Lean **9,127/9,127**。選択Governance・Core Autonomy **SUCCESS**。
- [公開CI #42723805572](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42723805572)：completed **SUCCESS**。KuuOSFormal Strict Lean **10,388/10,388**。選択Governance・Core Autonomy **SUCCESS**。
- 両実ログで新規28宣言の**全28件`#print axioms`**を監査。**公理なし19、標準`propext`・`Quot.sound`のみ9**、新規`sorryAx`なし。変更Lean error/warning **0/0**。元18Dの実Type値、旧新独立Type19D、公開root107、固定Lean/mathlibを変更していない。
- Git tree同一性はそれぞれsource/test-merge/squashで検査済み。文書だけの正式記録は別PRで実施し、Strict Leanを意図的にSKIPPEDとする。

## 論理的境界と次段Qi v5.76

この結果はv5.74完全観測の**局所非単射性**であり、v5.75の新イベント語まで追加した後の全商クラス分類・単射性は未認証（NO_DATA）。元old18D内部のType値全体の完全な再構成も証明していない。次段では新イベント語まで一致する真正証拠対があるか、あるいは構文を制限した部分に条件付き忠実性が成立するかを調べる。

20D gluing、任意の異端点fiber、WORLDをまたぐ降下、哲学的同一性、制度的・実行上の権限もNO_DATA。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
