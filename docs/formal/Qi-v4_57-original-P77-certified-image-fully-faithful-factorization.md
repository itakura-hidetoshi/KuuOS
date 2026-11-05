# Qi v4.57 — 真正元P77保守的5-cell商の到達可能像・完全忠実因子分解

**2026-11-05 JST**

| 項目 | 検証済み正本 |
|---|---|
| 定理PR | [#3134](https://github.com/itakura-hidetoshi/KuuOS/pull/3134) **MERGED** |
| 最終exact-source HEAD | `a969305068fa99950435aaff31b4522810cf1bfa` |
| 定理squash/main | `94f43a1e34fa20ec1f3385f4fdecde6675f0cfd6` |
| source/test-merge Git tree | `57ccc9ba1d98736e84a2bddfb192d62d54f255ff` 完全一致 |
| exact-source CI | [#41957621160](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41957621160) |
| Strict Lean | **10,254 / 10,254 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 公理監査 | **17 / 17**、標準 `propext`／`Classical.choice`／`Quot.sound` のみ、`sorryAx` なし |
| Lean全文 | [QiWuxingGK5CHP77CertifiedImageFactorizationV4_57.lean](../../formal/KUOS/Architecture/QiWuxingGK5CHP77CertifiedImageFactorizationV4_57.lean) |
| 変更 | 新規Leanファイル1件、`KuuOSFormal` import 1行。既存原証明不変更 |

固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root107、保護PR #1558 Draft/open/unmerged。strict 空中心・独立Kuuは一presentation。元F54/F55/P77/P94Aの依存型履歴と真正C60物理Edge、Qiの符号付きCRTは別authorityのまま保存。

## 1. Qi v4.53–v4.56からの正確な継承

元の真正`FivefoldEdge` 5本（`e01,e12,e23,e04,e43`）をもつ有向自由経路圏`FivefoldFreePathCategory`から、元F55/P77の真正Type値付き四セルをGK5CG**保守的5-cell証拠が存在する場合のみ**同一視したtarget Categoryへの関手

```text
F : FivefoldFreePathCategory ⥤ FivefoldP77ConservativePoint f g h k
```

を継承。Qi v4.55では `F.Faithful` が無条件に成立し、Qi v4.56では真正P77 `e01` の`symm`から生じる逆向き四セル1→0、charge `-1` により `¬F.Full` が形式証明された。証明の定義や仮定を変更せず、両方を保持する。

## 2. source-certified image Homの真正構成

新しい`FivefoldP77ImagePoint f g h k`は元の`FivefoldPathVertex`を独立ラッパーとして格納し、既存Qi・P77のCategory instance衝突を回避する。

```text
FivefoldP77ImageHom X Y :=
  { z : FivefoldP77ConservativeClasses f g h k X.vertex Y.vertex //
    fivefoldP77ConservativeReachable f g h k z }
```

このHomの値`z`は、あくまで**元P77四セルの真正保守的5-cell商クラス**。追加成分は、そのクラスが元の型付き有限経路評価`F.map path`から得られるという`Prop`証拠であり、数値charge値でも物理Edge列でもない。到達可能性はQi v4.56の真正型付き5-cell証拠への必要十分条件と整合。

恒等射`fivefoldP77ImageId`の到達可能性は真の空経路で証明。像の合成`fivefoldP77ImageComp`は元targetの真正商合成を用い、2つの元経路`pathA, pathB`の`Quiver.Path.comp`を証拠として、既証明の関手合成律から閉性を示す。

その上で`fivefoldP77ImageCategory`がMathlib `Category`を構成し、left/right unit・associativityを**元GK5CG保守的5-cellの実際のunit/assoc witness**から示す。`fivefoldP77ImageId_val`と`fivefoldP77ImageComp_val`は値成分と元targetの完全一致を厳密に記述する。

## 3. 二つの真正関手と正確な因子分解

```text
A = FivefoldFreePathCategory
I = FivefoldP77ImagePoint f g h k
C = FivefoldP77ConservativePoint f g h k

A --fivefoldP77ImageFactor--> I --fivefoldP77ImageInclusion--> C
```

`fivefoldP77ImageFactor`は自由経路をその元P77商評価クラスと**同じ経路による到達可能性の証拠**の組へ移す。包含関手`fivefoldP77ImageInclusion`はクラスを変形せず`Subtype.val`で元targetへ戻す。双方は真正Mathlib Functorであり、

```text
fivefoldP77ImageFactor f g h k ⋙
  fivefoldP77ImageInclusion f g h k
= fivefoldP77ConservativeFunctor f g h k
```

を`fivefoldP77Image_factorization`として**関手等号**で形式証明。

## 4. 完全忠実な因子と非Fullな包含を分離

`fivefoldP77ImageFactor_full`：像Homの到達可能性証拠を取り出すだけで、真正元自由経路のpreimageが存在する。`fivefoldP77ImageFactor_faithful`：元targetへの包含による商クラスの等号からQi v4.55の真正関手の単射性を使用する。

`fivefoldP77ImageFactor_fullyFaithful`はMathlibの**`Functor.FullyFaithful`データ付き構造**を構成する（`Prop`ではなく`Type`）。最終命題では`Nonempty`で包んで存在を表す。

包含関手は`fivefoldP77ImageInclusion_faithful`により忠実。ただし、元P77の真の逆向き`e01`四セルはcharge `-1` のため到達可能でなく、`fivefoldP77ImageInclusion_not_full`が**非Full**を形式証明。元の保守的target自体を縮小せず、逆向きP77証拠も保持。

したがって中心定理`fivefoldP77Image_exact_factorization_split`：

```text
Nonempty (ImageFactor f g h k).FullyFaithful
∧ (ImageInclusion f g h k).Faithful
∧ ¬ (ImageInclusion f g h k).Full
∧ (ImageFactor f g h k ⋙ ImageInclusion f g h k = OriginalP77Functor)
```

を全ての真正元F54/F55四項組で証明。

## 5. Lean記載法の学習・修正と検証境界

初回CIは次の構造的型問題を検出し、定理の仮定を弱化せずに修正した。

- `Exists`による到達可能性は`Prop`なので、`Type`値の構成前に`rcases`で消去せず、像の値を先に与え、その後で`Prop`内の到達証拠を取り出す。
- `Category.id_comp`等の型推論で元targetの局所`Category` instanceが解決されないため、像の`Subtype.val`へ射影し、真正元P77保守的5-cellの左右単位・結合証拠を明示して証明する。
- `Subtype.ext`を用い、像のHom同士の等式を元target Homの値成分の等式へ正確に還元する。合成射影は`fivefoldP77ImageComp_val`等で簡約する。
- `Functor.FullyFaithful`は`Prop`ではなく**preimageを持つType-valued structure**。定理ではなく`def`として構成し、命題の連言へ含める場合は`Nonempty`を使う。

最終HEAD `a9693050...` のexact-source CI [#41957621160](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41957621160) はStrict Lean **10,254/10,254 SUCCESS**、変更Leanモジュールの`#print axioms` **17件が標準公理内**、`sorryAx`なし、Governance30/30 SUCCESS。GitHub MCPでsourceとtest-mergeのGit tree `57ccc9ba...`一致およびsquash main `94f43a...`を再確認。

## 6. 数学的限界と次の焦点

この研究で**確定**したのは、元P77保守的商Categoryのsource到達像を、元の商クラスと型付きpreimage証拠を保持する真正Mathlib Categoryとして構成し、そこへの完全忠実因子分解と元targetへの非Fullな包含を分離できたこと。

**未主張：** 元の保守的targetへのFull・Equivalence、元P77生の四セルを型等号でstrict化すること、無条件original→phi seam、元P94A全域証拠復元、C60物理辺とP77四セルの型同一視、Gray等のglobal strict高次圏。

**次Qi v4.58：** `FivefoldFreePathCategory`とsource-certified image Categoryの間について、今回証明された完全忠実性に加え、対象の実際の対応を使った**真正カテゴリー同値（あるいは明示的inverse functor）**を形式化する。像から元のFull targetに戻る包含はNonFullという障害を保存する。任意のsource外生成元を歴史的証拠として追加したと主張しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
