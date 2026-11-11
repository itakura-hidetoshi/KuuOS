# Qi v5.96 — 真正旧18Dの混合strict配置と型付きunit履歴の局所障害（Lean4形式認証）

2026年11月11日 JST。唯一のcanonical正本は `itakura-hidetoshi/KuuOS` の `main`。今回の形式対象は、元の本当の依存型 `SelectedLocalEighteen W l r J N`、元のraw17D始終端、v5.73非結合内部括弧観測、v5.89真正unit数、v5.92元unit葉の完全な型付きpayload履歴、v5.93未解決1-unit source collision Prop、v5.94・v5.95のstrict配置と等号反映である。哲学的な「空・縁起・二諦・中道」と形式構造の対応づけは解釈・命名層であり、Lean4が仏教哲学そのものを証明したとは主張しない。

## 1．GitHub正本と独立検証の来歴

- 基準main（Qi v5.95三段階統合）：`223e31c1c71656abb1eb576bee8ed0c71017c85a`。
- [新規Lean4定理PR #3518](https://github.com/itakura-hidetoshi/KuuOS/pull/3518) **MERGED**。新規ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77MixedStrictUnitProvenanceObstructionV5_96.lean` 1件、GitHub差分 **425行追加／既存行削除0**、実際の `#print axioms` **14件**。元17D/18D/19D Type・構成子・既存証明・元の旧5／新7選択19D比較を変更しない。
- 最終定理認証source `ea4300a5086aeddbaca64f771eadff5c5dd5d348`。[定理CI #42956722160](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42956722160) **completed／SUCCESS**、Scoped Strict Lean **9,148／9,148**、独立Kuu Core・Governance・workflow整合性すべてSUCCESS。変更Lean error/warning **0／0**、新規 `sorryAx` **なし**。
- 独立Lean実ログの公理監査 **14／14**：**公理不要4宣言**、残り**10宣言は `propext`／`Quot.sound` のみ**。定理squash後main `f24cfcd9a2151dc095fb9446a27b08025408313a`。source／test-merge／統合後main Git tree **`438e62a887f651dc2e9b261fef6ea3ef0f74930c`一致**。
- [公開import PR #3519](https://github.com/itakura-hidetoshi/KuuOS/pull/3519) **MERGED**。`formal/KuuOSFormal.lean` にv5.96 import**1行のみ**追加。source `06cc8abee94ddb1eab8180d5e30a684e6778d396`。[公開CI #42957409865](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42957409865) **completed／SUCCESS**：公開 `KuuOSFormal` 依存閉包 **10,409／10,409**、Governance **30／30 SUCCESS**、独立Kuu Core SUCCESS。公理監査14／14、変更Lean error/warning 0、新規sorryAxなし。
- 公開squash後main `580459c543fcb70dff6fd5c188fa10073e0948a8`。公開source／test-merge／統合後main Git tree **`cc7d6ab9066352b8ddc82d88d58a622cfe615ccc`一致**。
- 固定：Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**、公開root **107維持**、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) **Draft／OPEN／未マージ**。append-only／tighten-only／overwrite-forbidden／same-root。

## 2．本当の同一J→N fiberにおける混合配置の指紋剛性

`M,L : SelectedLocalEighteen W l r J N` は**同一の元raw17D J→N fiber**の真正証拠とする。元のv5.73内部括弧を `Bracket`、真正元v5.89 unit数を `UnitCount` と略す。

```text
hbase : Bracket(M) = Bracket(L)
hunit : 0 < UnitCount(M)
P_m(M) = v5.94 genuine original strict prefix of length m
S_n(L) = v5.94 genuine original strict suffix of length n
```

この**明示した条件の下で**次をLean4形式証明した。

```text
Bracket(P_m(M)) = Bracket(S_n(L))
  ↔ m = 0 ∧ n = 0

P_m(M) = S_n(L)
  ↔ m = 0 ∧ n = 0 ∧ M = L
```

証明は、v5.94の実strict葉数の加算式と`Bracket(M)=Bracket(L)`から`m=n`を導き、正の共通長ではprefixの最外左葉が`oldStrict`だがsuffixの最外左部分木には本当の元unit葉が残り、元unit数が0ではないことから括弧一致を排除する。元括弧一致・正unit数を外した全域の結論には一般化しない。

## 3．真正型付きunit payload履歴は同じでも括弧は別

任意の本当の`M:J→N`で`UnitCount(M)>0`なら、`m+n>0`を満たすすべての自然数対について、

```text
History(P_m(M)) = History(S_n(M))
Bracket(P_m(M)) ≠ Bracket(S_n(M))
P_m(M) ≠ S_n(M)
```

を証明した。ここで`History`は元v5.92の完全な型付きunit atom履歴であり、元`before/F/G/C/after`・元raw17D始終端・元の旧18D unit証拠自体を残す。履歴一致と元raw等号・括弧等号を混同しない。

さらに、もし元`M,L`の括弧と型付きunit履歴がともに一致し、UnitCount(M)=1、M≠Lの**証拠が本当に供給された場合**にも、非自明な混合paddingは履歴一致を維持する一方、括弧は一致しない。元源対の実在は仮定ではなく未解決の問題であり、条件付き定理がそれを構成するものではない。

## 4．制限された混合1-unit衝突像は厳密に分類可能

新`selectedV596MixedOneUnitCollisionExists l r J N m n`は、**元source同士の内部括弧が等しい**こと、`UnitCount(M)=1`、混合padding後の括弧等号・raw不等号を含む、限定された元旧18D依存型の存在`Prop`である。

```text
MixedOneUnitCollisionExists(m,n)
  ↔ m = 0 ∧ n = 0 ∧
    V593OneUnitSourceCollisionExists(J,N)
```

を形式証明。従って`m+n>0`では、この**限定された混合paddingによる1-unit衝突は不可能と証明された**。ただし元v5.93の0/0の源衝突の存在または不可能性を証明したわけではない。また、元source括弧一致を仮定しない他の構成法、全旧18D生証拠・商全域、異fiber貼合への不可能性も主張しない。

## 5．真正unitLeft／unitRightの元パラメータを保持

元v5.35の真正`unitLeft before F G C after`および独立の`unitRight before F G C after`のそれぞれについて、元v5.92の履歴が、対応する正しい`J,N`と**元の真のunit証拠**を含むsingleton Sigma payloadであることをLean4で確認した。

左右の元raw17D端点は一般には別の依存型であり、元生証拠同士の等号を捏造しない。一方、共通の内部括弧観測の値`oldUnitLeft`と`oldUnitRight`は区別される。さらに左右それぞれの本当の1-unit源について、任意の`m+n>0`で完全型付き履歴一致、括弧不一致、真正raw証拠不一致を元の同一fiber内で検証した。

## 6．Lean4失敗経路と修正

- [初回CI #42955657272](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42955657272) は4件の型不一致：最終の真正left/right具体例で、`selectedV596PositiveSameSourceMixedGap`に対して元sourceを重複して明示し、次の`decide`も誤った引数位置に現れた。元型と新規Lean全文を照合し、余分な明示source引数を左右で各1件削除。
- [第2回CI #42956118998](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42956118998) は残り2件：自由変数を含む`0 < OriginalUnitCount(unitLeft/right)`へ`decide`を直接適用したため、未簡約の依存式のDecidableを閉じられなかった。元unit構成子が真正にunit数1であることを`change 0 < (1 : Nat); decide`で明示して解決。
- [最終CI #42956722160](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42956722160) は**9,148／9,148 SUCCESS**。これらは新規ファイル内の証明手順だけの修正であり、**新規定理文、元依存型、比較規則、Lean/mathlib固定、既存ファイルは一切弱めていない**。失敗CIの公理出力は認証の根拠に採用しない。

## 7．障害（NO_DATA）とQi v5.97候補

**認証済み**：元の同一J→N fiber、元括弧一致・正のunit数という条件に限定した混合strict配置の括弧等号・raw等号の必要十分条件、完全型付きunit履歴不変のもとでの非自明混合配置の分離、限定混合1-unit衝突の正padding時不可能性、左右元unit源の独立型付きsingleton payload。

**未認証（NO_DATA）**：元旧18Dの同じJ→N fiberで`UnitCount(M)=1`かつ`Bracket(M)=Bracket(L)`かつ`M≠L`となる**元source対の実在・不可能性**。一つの制限付きmixed presentationの不可能性を全源空間の不可能性へ昇格しない。元旧5／新7選択19D比較の全域的同値、異fiber gluing、WORLD／20D降下、制度的行為権限も未認証。

**v5.97候補**：元内部括弧の`oldUnitLeft`／`oldUnitRight`の葉位置を固定した上で、元v5.92 Sigma型付きunit payloadの一致が真正元生証拠の等号を反映する局所断片を検証する。一般源への降下条件を別途示すまでは、局所結果を全域に拡張しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
