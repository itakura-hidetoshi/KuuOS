# Qi v5.82 — 元18Dのpure strict/reverse/chain部分presentationにおける条件付き忠実性（Lean4形式証明・公理監査）

2026年11月10日 JST。対象は、元の依存型`SelectedContextualEighteen`から明示的に構成される**限定部分**、旧5構成子`SelectedLocalNineteen`と別Typeの新7構成子`SelectedRawCongruentNineteen`、それぞれの真正商である。「空」「縁起」との哲学的対応は命名・解釈層に属し、形式証明は与えられた型・構成子・比較・商の局所的主張に限る。

## 1．canonical正本と統合来歴

- Repository: `itakura-hidetoshi/KuuOS`、canonical `main`。研究起点Qi v5.81正式統合済み `376b22cb4e647dd72d6bb2170a2d04c92df230b0`。
- [定理PR #3476](https://github.com/itakura-hidetoshi/KuuOS/pull/3476) **MERGED**。新規Leanファイルは`formal/KUOS/Architecture/QiWuxingGK5CHP77PureStrictReverseFaithfulFragmentV5_82.lean`（385行、21宣言と21件の`#print axioms`）。既存定理・構成子・仮定への変更や削除なし。
- 定理認証source `e9ca0b3d2057c57c7e17a1245e959ba3c128843e`、test-merge `e6806e0ff2b924f4884339681ae2322f63f7ca93`、統合squash `801815134815cfb1274158696c534c6b38041c0a`のGit treeは `f6dd81bcd79086f54635080c41aa87d221ebac06`で一致。
- [公開import PR #3477](https://github.com/itakura-hidetoshi/KuuOS/pull/3477) **MERGED**。元の`formal/KuuOSFormal.lean`に`import KUOS.Architecture.QiWuxingGK5CHP77PureStrictReverseFaithfulFragmentV5_82`の**1行のみ追加**。従来689件のimport、公開root107を保持。
- 公開認証source `d61b5d87b170d9ca61e416dd0226fc18e96abeda`、test-merge `f6424d39d4d43af37959f33168d8daae2a3083d0`、統合squash `cefc10bbf9936d6d3e9ba62d0c1e949a57c8ea95`のGit treeは `d320d0f57dda95adff053515e3ba54386a2d360a`で一致。
- Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`を固定。validation-only [保護PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 2．元の依存18D Typeに埋め込む限定構文

`SelectedPureStrictReverseTree`は`strict`、`reversed`、`joined`からなる自由な非結合構文木である。真正に与えられた17D端点`N`ごとに、再帰的な`selectedPureStrictReverseEmbed N`でこれを元の真正`SelectedContextualEighteen W l r N N`の**元Type値**へ送る。

- `strict`は元の`strict N`。
- `reversed A`は元の`reverse (embed N A)`。
- `joined A B`は元の`chain (embed N A) (embed N B)`。

この限定presentationには`inherited`や左右whiskering構成子は現れない。したがって、旧19Dの本来の単位規則が消す「真正`inherited`葉に直接隣接したstrict」は存在せず、任意のraw strictを単位として消す新しい規則を仮定しない。任意の異端点`J→N`の居住性も仮定しない。

## 3．v5.81独立観測からの局所復元

別定義`selectedPureStrictReverseRawValue`は、自由なstrict/reversal/chainの樹形をv5.81の`SelectedWhiskerPlacementTree`へ読み取る。真正18D構成子への埋め込み後の実観測とこの値が一致することを元の依存Type上で形式証明した。

`selectedPureStrictReverseDecode`は全補助観測型上の関数として定義するが、その左逆性が証明されるのは**このpure部分の像上だけ**。他の`source`・`left`・`right`を含む全構文に対する忠実復元器とは主張しない。結果としてこの部分上では元18Dへの埋め込みも単射である。

## 4．旧5構成子と新7構成子の比較の一致範囲

指定した真正`N→N` fiberの純粋部分で、Lean4で次をそれぞれ証明した。

```text
[embed N A]_(old 19D) = [embed N B]_(old 19D)  ↔  A = B
[embed N A]_(new 19D) = [embed N B]_(new 19D)  ↔  A = B

Nonempty (SelectedLocalNineteen (embed N A) (embed N B))
  ↔ A = B

Nonempty (SelectedRawCongruentNineteen N N (embed N A) (embed N B))
  ↔ A = B
```

旧新の`Type`としての比較を同一視せず、**この制限された像上の比較可能性の必要十分条件が同じ**ことを証明した。旧・新商クラスの写像はそれぞれ単射で、旧→新射影もこの限定部分上では等号を反映する。全体商の一致や一般的な逆向き比較生成元の存在は主張していない。

## 5．v5.81完全観測を保つ局所的な忠実性

`SelectedFullV581QuotientObservationValue`は、それまでの`SelectedFullV580QuotientObservationValue`と、v5.81の独立して新商に降下済みのwhisker配置木との**直積**である。

`selectedRawCongruentFullV581QuotientObservation`を真正7構成子商からこの直積へ構成し、上記pure fragmentで

```text
FullV581([embed N A]) = FullV581([embed N B])  ↔  A = B
```

および合成写像の単射性を形式証明。従来の元九変量、二本の**全Nat→Nat無限塔**、ordered reversal run、元旧18D出典、strict-only枝観測などを減らすことなく、新観測を追加する構成である。

**境界**：v5.81で作ったwhiskered真正18D反例では、この新観測を含まないv5.80完全観測が非単射だった。本v5.82は**別の制限されたpure構文像**の単射性であるため、それと矛盾しない。

## 6．初回CIの修正履歴

- [初回CI #42763848078](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42763848078)の失敗：再帰定義の内部で`selectedPureStrictReverseEmbed l r N`と明示適用した結果、再帰方程式での暗黙引数の扱いと一致せず、型不一致と後続`rfl`・`change`失敗へ伝播。
- [修正後CI #42764426697](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42764426697)の失敗：再帰内外を区別せず全36箇所を`selectedPureStrictReverseEmbed N`にしたため、外部の明示引数`l r`が欠落。
- 実際に修正したのは**再帰方程式内の3箇所だけを`embed N`とし、定義外の33箇所は`embed l r N`とすること**。既存定理、固定Lean/mathlib、元仮定、全商の比較規則を変更しない。この構造原因を確認して3回目のexact-source CIで型検査成功。

## 7．機械的な認証と公理実監査

- [定理CI #42765067890](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42765067890)：**terminal SUCCESS**、Scoped Strict Lean **9,134/9,134**、選択Governance・Core Autonomy SUCCESS。独立exact-head completion receipt SUCCESS。
- [公開CI #42765607445](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42765607445)：**terminal SUCCESS**、KuuOSFormal Strict Lean **10,395/10,395**、Governance選択ジョブ**30/30 SUCCESS**、独立completion receipt SUCCESS。
- 新規21宣言の`#print axioms`実出力は、**公理不要7／`propext`・`Quot.sound`のみ14**。新規`sorryAx`なし、変更Lean error／warning 0／0。
- 定理と公開それぞれのsource／test-merge／squash Git treeの一致をGitHub Git dataで照合。CI成功と記録を、全商分類や哲学的命名層の証明へ不正に昇格させない。

## 8．未認証の範囲と次段

依然として任意の元18D証拠をpure部分へ簡約する定理、旧5構成子と新7構成子の大域的比較同値、全商の完全忠実分類、任意`J→N`の居住性、WORLD横断降下、20D gluing、行為権限は**未認証（NO_DATA）**である。

**Qi v5.83の候補**：元`inherited`葉またはwhiskeringを一つ以上含む部分presentationへ、どの補助履歴を保持すれば局所復元が拡張できるか、単位規則や元依存証拠の値を保存したまま探索する。対象部分の拡張と降下の証明条件を先に立て、未認証の全域化をしない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
