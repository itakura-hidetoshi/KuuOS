# Qi v4.68 — 真正元P77の有限切断木の正規形と任意有限履歴の整合性

**2026年11月5日 JST**。strict 空を中心とし、独立Kuuを一つのpresentationとして扱う。元F55/P77/P94A、C60物理Gauge、北C60 CRTのauthorityを保持する。

| 項目 | exact-source確認 |
|---|---|
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / `main` |
| 継承元 | Qi v4.67 定理 [#3155](https://github.com/itakura-hidetoshi/KuuOS/pull/3155)、正式記録 [#3156](https://github.com/itakura-hidetoshi/KuuOS/pull/3156) MERGED |
| 基点main | `60c2c93d1681723e4b5d8dadcec04466bdfb964d` |
| 定理PR | [#3157](https://github.com/itakura-hidetoshi/KuuOS/pull/3157) **MERGED** |
| 検証済みHEAD | `7c2d8a5e02aa2e51c29e0d582c24ddfc100cf2bf` |
| 定理squash | `31b81adc1f5376796d054738db378b4a077ab4fd` |
| exact-source CI | [#42030101859](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42030101859) |
| Strict Lean | **10,265 / 10,265 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理検査 | **23件**、標準公理のみ、`sorryAx`なし |
| 変更Lean warning/error | **0 / 0** |
| source/test-merge Git tree | `d0d069f6fab8df4788c240329b5eefaa846d6d02`、完全一致 |
| 変更 | 新規Lean 550行、公開集約import 1行追加、既存定理本文の変更なし |
| 公開集約 / roots | `formal/KuuOSFormal.lean` / **107** |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR | [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)、Draft / OPEN / 未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FiniteCutTreeNormalCoherenceV4_68.lean)

## 1. 有限切断木と元パッチ列の正規形

`FivefoldP77RawPatchCutTree`は実際の`FivefoldPathVertex`を端点に持つ依存型である。葉はv4.65の任意有限長の`FivefoldP77RawPatchChain`、節は同じ中間頂点で接続する二つの部分木からなる。空鎖も葉にできる。したがって、任意の有限個の指定cut、入れ子のcut、任意深さの再括弧付けを記述できる。

`fivefoldP77RawPatchTreeFlatten`を $N(T)$ と書く。これは元の`Append`で葉を順序通りに連結した**元パッチ列そのもの**であり、各raw四セル族・index型・型付き中間端点を保持する。chargeや経路長だけで正規形を定めない。

## 2. 証拠付きTypeの明示的な正規化同値

`FivefoldP77RawPatchTreeWitness T`を $W_T$、元パッチ列の証拠付きTypeを $W(C)$ と書くと、

$$
W_T \simeq W(N(T))
$$

が`fivefoldP77RawPatchTreeNormalizeEquiv`で成立する。葉では恒等同値、節では`Equiv.prodCongr`とv4.67の本物の切断同値の逆を使う。各葉の元source経路と元P77商評価の証明を含むTypeから、元の列の証拠付きTypeへ移す具体的な関数と逆関数である。

各葉の互換条件は、従来の元GK5CG Type値五セルの存在と元source評価anchorを用いる。全葉でこの条件が満たされることと $W_T$ が存在することが必要十分になる。source経路証拠の一意性はv4.65の元P77 Faithful性から継承する。選ばれたraw四セル／五セルの証明履歴すべてを同一視する定理ではない。

## 3. 任意有限の切断・再括弧付け履歴

`FivefoldP77RawPatchCutRoute`は**Type値の有限履歴**であり、七つの構成子を持つ。

- 恒等履歴 `refl`
- 指定cutでの分割 `cut`
- 三部分木の括弧移動 `assoc`
- 逆履歴 `symm`
- 履歴の連結 `trans`
- 左部分木内への適用 `left`
- 右部分木内への適用 `right`

`fivefoldP77RawPatchTreeNormalizeRoute`は任意の木から`leaf (N(T))`への有限履歴を構造再帰で構成する。さらに、

$$
\operatorname{Nonempty}(\operatorname{CutRoute}(T,U))
\quad\Longleftrightarrow\quad N(T)=N(U)
$$

を`fivefoldP77RawPatchCutRoute_nonempty_iff`で証明する。比較条件は**元のrawパッチ列の厳密な等式**である。任意の同chargeパッチ列への置換を許していない。

正規化手順は木の構造に沿う有限な再帰である。`CutRoute`には逆操作・ループも残るため、任意に選んだ書換え戦略の停止性は今回の主張に含まれない。

## 4. 履歴が誘導する同値・source経路・P77部分Homの一致

`fivefoldP77RawPatchCutRouteEquiv`は各履歴を実際の証拠付きTypeの同値へ評価する。cutには既存の`CutWitnessEquiv`、assocには固定mathlibの`Equiv.prodAssoc`、文脈には`Equiv.prodCongr`を使う。

同じ始点・終点を持つ任意の有限履歴 $r_1,r_2:T\rightsquigarrow U$ について、

$$
E(r_1)=E(r_2)
$$

がLeanの`Equiv`そのものの等式として成立する。各履歴による同値は、$W_T\simeq W(N(T))\simeq W(N(U))\simeq W_U$ という正規形を経由した比較に等しい。証明には既証明の忠実性による元source経路証拠の一意性を用いる。**履歴 $r_1,r_2$ 自体は別のType値として保持する。**

任意の証拠 $w:W_T$ に対し、木の括り方に従って合成した元sourceの`Quiver.Path`は正規化した列の経路に厳密に等しい。有限履歴を通した場合も、

$$
\operatorname{path}_U(E(r)(w))=\operatorname{path}_T(w)
$$

が`fivefoldP77RawPatchCutRoute_path`で成立する。さらに`fivefoldP77RawPatchCutRoute_certified`は、元source到達性証明を備えた`FivefoldP77PartialDomain`そのものの一致を示す。`fivefoldP77RawPatchTreeCertified_recover`により、既存の部分復元はこの元source経路を正確に返す。

## 5. 局所obstructionの保持

`fivefoldP77RawPatchTreeObstructed`は、指定された葉のいずれかで元の互換条件が失敗することを再帰的に表す。これは全葉の互換性の否定と必要十分である。

`fivefoldP77RawPatchCutRoute_obstruction`は、その障害がある木からどの有限履歴を選んでも、移行先の証拠付きTypeは空であることを示す。切断順序・再括弧付けは、欠けた局所source証拠を生成しない。この結論は、同じ元パッチ列の指定因子別実現に限定される。別の全target因子分解への一般的な不可能性を導かない。

## 6. 検証と次段階

最終 [CI #42030101859](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42030101859) はworkflow・全32 jobs・Lean実行ステップ・依存manifest確認・終了receiptまで成功。Strict Leanは**10,265 / 10,265**、Governanceは**30 / 30**。新規23件の公理出力は`propext`／`Classical.choice`／`Quot.sound`の範囲で、`sorryAx`なし。変更Lean warning/errorは0/0、source/test-merge treeは完全一致した。

初回 [CI #42029005351](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42029005351) では、説明文中の `four-/five-cell` がブロックコメントを途中で閉じる字句上の問題と、依存経路移送補題の `rw` が等式引数 `heq` を未確定で残す問題が見つかった。前者は説明表記を修正し、後者は既証明の `CutRoute_flatten` と正規化した元witnessを補題へ明示した。定理文・仮定を変更せず、修正版HEADで全検証を完了した。[Leanのコメント構文](https://lean-lang.org/doc/reference/latest/Source-Files-and-Modules/#concrete-syntax-comments) と [命題のproof irrelevance](https://lean-lang.org/doc/reference/latest/The-Type-System/Propositions/) も照合した。

既存Lean本文、toolchain、mathlib manifest、公開root構成は保持し、新規モジュールと集約importのみを追加した。元の依存モジュールと新規ソースを照合し、数学設計の独立レビューと固定CIによる新規ソース全文の検証を行った。型付き空鎖、任意深さの左右文脈、逆履歴、有限合成、依存証拠輸送を一般定理の量化範囲に含める。

**次の候補Qi v4.69：** 元GK5CG Type値五セルで証明された局所パッチ族の表示変更・細分に対する比較と、今回の正規化との自然性を研究する。v4.68が扱う厳密に同じraw列から、実際の元比較証拠を持つ異なるraw族へ進む段階であり、全targetの無条件復元やchargeだけによる比較を導入しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
