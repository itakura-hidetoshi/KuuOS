# Qi v4.55 — 真正五行有向五角形の有限経路一意性・元P77保守的5-cell商関手の無条件faithfulness

**2026-11-05 JST**

| 項目 | 正本・検証結果 |
|---|---|
| 定理PR | [#3130](https://github.com/itakura-hidetoshi/KuuOS/pull/3130) **MERGED** |
| exact-source 検証HEAD | `523e081a02c712984274e3d0580ec1eb20e969c9` |
| 定理squash main SHA | `e8066445cf6be08e7ea59cf5155fc91c586054b3` |
| source/test-merge Git tree | `a2d7282bb22982250dc5ae0bfa01be1367731a38` 完全一致 |
| exact-source CI | [#41947668879](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41947668879) |
| Strict Lean | **10,252 / 10,252 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **18 / 18**, `propext`・`Classical.choice`・`Quot.sound` 以内、`sorryAx` なし |
| 変更 | [新規Lean1ファイル](../../formal/KUOS/Architecture/QiWuxingGK5CHFivefoldFinitePathFaithfulV4_55.lean)＋`KuuOSFormal` import 1行のみ |

**Pinned:** Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107維持、#1558 validation-only Draft/open/unmerged維持。strict空を中心とし、独立Kuuは別presentation。歴史的証拠と定理の変更・削除なし。

## 1. 元FivefoldEdgeの有限有向構造

Qi v3.5/v4.52の**唯一の** `FivefoldIndex = FivePhase = ZMod 5` と実際の `FivefoldEdge` を使用。エッジは以下の5本で、Qi v3.1の相生／相剋 Quiver と混同しない。

```text
0 --e01--> 1 --e12--> 2 --e23--> 3
 \                               ^
  \--e04--> 4 --e43-------------/
```

生成辺の始終点の完全な一致から生成辺値が等しいことを、有限 `decide` による真正Lean検査で証明。`fivefoldPathArrow_subsingleton` は各型付き端点に対して生成Homが高々1個であることを示す。生成元の上流 `FivefoldEdge` や元P77四証拠を互いに潰したわけではない。

`fivefoldTwoEdgeWord_unique` により、2辺の合成可能な真正語は固定始終点で一意：`e01;e12`、`e12;e23`、`e04;e43`。3辺の合成可能な真正語は `e01;e12;e23` のみ（`fivefoldThreeEdgeWord_unique`）。4辺連続する有向語は**存在しない**（`fivefoldFourEdgeWord_impossible`）。これはこの有向五角形の具体的事実であり、抽象的な任意クィバーで成立するものではない。

## 2. 依存型Quiver.Pathの全有限経路を分類

元のMathlib `Quiver.Path` を、`nil/cons` 構成子の完全な型付きケース分解で扱う。`fivefoldFreePath_length_le_three` により、

```text
∀ (u v : FivefoldPathVertex) (path : Quiver.Path u v), path.length ≤ 3
```

を無条件に形式証明した。経路構文は任意有限長を許すが、**この具体的クィバー上で実在する経路は長さ0～3のみ**。

長さ1／2／3の各経路を真正 `FivefoldPathArrow` のネストした `nil.cons` 型に分解する `fivefoldFreePath_one_decomp`／`two_decomp`／`three_decomp` を証明。合成可能な有限辺の始終点検査から、各長さに対し始終点が共通なら**生の自由経路そのものが同じ値**であると証明した（`one_unique`／`two_unique`／`three_unique`）。

さらに長さ0の場合は固定mathlibの `Path.eq_nil_of_length_zero` を用いる。`fivefoldFreePath_length_injective` が全てを統合し、全original型付きHom `u→v` に対して

```text
Function.Injective
  (fun path : Quiver.Path u v => path.length)
```

が**無条件**に成立する。異なる元証拠間の不正な型消去は使わない。

## 3. 元P77証拠評価の単射性

Qi v4.53 `fivefoldEvaluateP77` は、各真正自由経路を上流 `NativeF55RawVerticalFourCell` の生の依存型四証拠へ `Quiver.Path.rec` で評価する。先行v4.53の条件付き単射定理 `fivefoldEvaluateP77_injective_of_length` に、今回成立した全Homの `fivefoldFreePath_length_injective` を適用した。

`fivefoldEvaluateP77_injective_genuine` は元P77**生の四証拠値**への評価が各Homで無条件に単射であることを示す。旧P77の合成・反転・whiskeringや元F54の二カテゴリー／二Nat深さ／Blocks証拠を変更せず、上流Type証拠を数値長やC60物理Edgeへ置換しない。

## 4. 元P77保守的5-cell商への関手の無条件faithfulness

Qi v4.54で構成済みの**真正Mathlib Functor**

```text
fivefoldP77ConservativeFunctor f g h k :
  FivefoldFreePathCategory ⥤ FivefoldP77ConservativePoint f g h k
```

について、`fivefoldP77ConservativeFunctor_faithful_genuine` が全元F55四項組で無条件に `F.Faithful` を証明した。

証明は次の2つの独立した以前の形式定理を合成している。

1. **GK5CG/Qi v4.54:** 本物の保守的5-cellが生成する商でchargeは保存され、`charge(F.map w)=(w.length:ℤ)`。したがって`F.map a=F.map b`は`length(a)=length(b)`を強制。
2. **Qi v4.55:** この元の5辺有向クィバーの同じ始終点に対して、`length(a)=length(b)⇒a=b`。

従って、sourceが等しいことを必要十分条件とするfaithfulnessを**数学的仮定なし**で構成。一般クィバーのfull/faithful性を不正に一般化せず、元の五角形でのみ結論する。

## 5. 真正保守的5-cellのexact kernel反映

`fivefoldEvaluateP77_conservativeFiveCell_iff_path_eq`：

```text
Nonempty (NativeGK5CGConservativeFiveCell first last
  (fivefoldEvaluateP77 f g h k A)
  (fivefoldEvaluateP77 f g h k B))
  ↔ A = B
```

これは同じ型付き始終点の全経路 `A,B` について成立。**保守的5-cellが存在すること**と、**元自由経路が等しいこと**を、元P77四証拠から商へ写した関手のfaithfulnessを通じて接続する。等号をcharge等号や数値CRTから作ることはしていない。`fivefoldEvaluateP77_noConservativeFiveCell_of_ne` は異なる経路の保守的5-cell不在を任意長の形式で導く。

五角形上側3辺 `e01;e12;e23` と下側2辺 `e04;e43` は依然異なり、元P77 chargeが3と2、保守的target射も異なる。旧GK5CGの別の新規adjoined presentationに宣言したpentagonatorは、この**保守的な旧P77**へ復元した証拠ではない。

## 6. exact-source Lean4学習・修正履歴

初回HEAD `0e7516e54255653ee30ae8aa824383be31dc6bb7` のCIではStrict LeanのLakeキャッシュ復元ジョブが環境的に失敗したため、失敗ジョブのみGitHub MCPで再実行。その後に得た真正Lean出力では、新規 `fivefoldFreePath_length_injective` 定理の`omega`呼出3箇所のみエラー：`Function.Injective` で導入した仮定が `(fun path => path.length) p = (fun path => path.length) q` の形に残り、`omega` への線形整数制約として正規化されていなかったことが原因。

**修正:** 同定理の`intro p q heq`直後に `change p.length = q.length at heq` を1行加え、固定Lean4のdefinitional equalityを使って正しい数値等号を明示。ソース・仮定・帰結、既存依存定理に変更なし。最終HEAD `523e081a...` の[CI #41947668879](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41947668879)で**10,252/10,252 SUCCESS**、`#print axioms` 18件は標準3公理以内で `sorryAx` なし。変更ソースのwarning/errorなし。source/test-merge Git treeは`a2d7282...`完全一致、Governanceは30/30、独立Kuu公開API成功。検証済みHEADを指定したsquash MERGED済み。

## 7. 証明の数学的範囲と次の研究

- **確定したもの：** この5本の実元FivefoldEdgeに関する完全な自由経路長分類、元P77四証拠評価の無条件単射性、源の保守的5-cell商への真正Functorの無条件 `Faithful`、全経路のexact kernel反映。
- **未確定：** `F.Full`（任意の元P77保守的クラスがFivefoldEdge経路の評価像に属するか）、全高次P94Aへのfaithfulness反映、無条件original→φ seam、数値CRTから元証拠の復元、物理C60 Edge historyとP77四セルの型同一視、global strict高次圏。
- **次Qi v4.56候補：** `F.Full`の必要十分条件を真正target Homごとの到達可能性として明示し、元P77生構文のコンストラクタと本5辺経路評価の間に存在するextra Hom obstructionを検討する。既存faithfulness定理はそのまま保存し、fully faithfulを無断主張しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
