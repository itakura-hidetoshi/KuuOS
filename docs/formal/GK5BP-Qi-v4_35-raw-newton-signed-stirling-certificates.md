# GK5BP／Qi v4.35 — 生観測値・Newton補間・符号付きStirling係数判定の正式Lean4証明記録

2026年11月4日 JST ／ F112-P94D3GK5BP ／ Qi v4.35 ／ 独立・Qiとも **MERGED**

## 1. 検証済みexact-source正本

| 項目 | 独立GK5BP | Qi v4.35 |
|---|---|---|
| PR | [#3073](https://github.com/itakura-hidetoshi/KuuOS/pull/3073) MERGED | [#3074](https://github.com/itakura-hidetoshi/KuuOS/pull/3074) MERGED |
| exact-source HEAD | `42a0fd10d4c0179f370fec9265b0d3e480954e1f` | `cdb2eac4f9668297972e882168b0fb87cc2549fc` |
| test-merge SHA | `1ebad306e340c7f70fd7e677995083d220bacc64` | `56f22c5b6c6c0776647e9279184e6041d7ab3ac3` |
| squash SHA | `b5520efd3c0b03d489e1b299f4cc12fbb08a91e9` | `407bab8643ccece147b22ed4a74e995890ae6e65` |
| source/test-merge/squash Git tree | `53175a0b80c64eec58ba0a5f191404342758f602` | `d95397f7a6ae7d643f71cfb955616577d0ab2dd5` |
| exact-source CI | [#41752699168](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41752699168) | [#41753489564](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41753489564) |
| Strict Lean | **9,288/9,288 SUCCESS** | **10,215/10,215 SUCCESS** |
| Governance | **30/30 SUCCESS** | **30/30 SUCCESS** |
| 新規公理監査 | 10定理、`sorryAx`なし | 9定理、`sorryAx`なし |
| 変更Lean warning/error | 0/0 | 0/0 |

- [独立GK5BP Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BPRawNewtonStirling.lean)：新規291行、3定義と10件の監査付き定理
- [Qi v4.35 Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BPNorthRawStirlingV4_35.lean)：新規228行、北C60統合定義・9件監査付き定理
- [公開集約](../../formal/KuuOSFormal.lean)：各段階で1 importをappend、新規公開rootの追加はない（107維持）。既存Lean定理の命題・仮定・F55 Type値履歴は上書きしない。

固定Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。保護PR #1558はDraft／OPEN／未マージ。

## 2. 独立GK5BP：観測値だけからの構成的再構成

任意の生観測関数 `v : Nat → Rat` と有限観測上限 `d` に対し、真のmathlib `fwdDiff (1:Nat)` を使って `Δ^k v(0)` を定義した。これを交代符号付き二項和

```text
Δ^k v(0) = ∑_{j=0}^k (-1)^(k-j) * choose(k,j) * v(j)
```

として表し、元多項式の係数を入力せずに**有理Newton多項式そのものを構成**：

```text
N_d(v) = ∑_{k=0}^d (Δ^k v(0) / k!) · descPochhammer(Rat,k).
```

実際の`descPochhammer(Rat,k)`は下降階乗 `X(X−1)…(X−k+1)`。その整数多項式係数を `s(k,j):=coeff(descPochhammer(Int,k),j)` と定義し、Ratへの真のcastとの整合性をLeanで証明した。この `s(k,j)` は**符号付き第一種Stirling係数の下降階乗係数表示**である。

任意の自然数`n≤d`で`N_d(v).eval(n:Rat)=v(n)`、`natDegree N_d(v)≤d`が成立し、元GK5BLの真正有理Lagrange補間と同一の多項式であることをLeanで証明した。

係数の完全な有限変換：

```text
coeff(N_d(v), j)
    = ∑_{k=0}^d (Δ^k v(0)/k!) · cast(s(k,j)).
```

この結果とGK5BMの有限support構成から、次の**必要十分条件**を構成した。

```text
∃ P : Int[X], P.map(Int.castRingHom Rat) = N_d(v)
 ↔
∀ j ∈ range(d+1), ∃ z : Int,
    (z:Rat) = ∑_{k=0}^d (Δ^k v(0)/k!) · cast(s(k,j)).
```

同値条件は元のGK5BL Lagrange補間にも成立し、`v:Nat→Int` の整数観測に特化した定理もある。整数観測のみでmonomial整数係数性が従うという誤った十分性は一切仮定しない。

**残る明示的境界**：今回のsigned`s(k,j)`は降下階乗のInt多項式係数として証明済みであるが、Mathlibの自然数値`Nat.stirlingFirst k j`との直接の符号付き閉形式`s(k,j)=(-1)^(k-j)Nat.stirlingFirst k j`そのものは今回の監査対象定理として追加していない。これを次段階の独立数学的補題候補として区別する。

## 3. Qi v4.35：真正北C60の生観測へ移送

任意の真正original北F55証拠`f`、また真正元F55/P77 source quotient`q`が与える**既存の降下済み整数多項式値**を入力し、0からdまでの本物の整数評価からStirling係数証明書を導いた。まず一般の真正`P:Int[X]`に対して、`natDegree P≤d`を仮定すると生観測`P.eval(n:Int)`のNewton／Lagrange再構成が元`P.map`に一致することを利用した。無条件の生観測整係数性ではない。

真正北C60：元primitive`P=1`と元double inverse＋実際のF55右単位`P=X²`は`{0,1,2}`の3観測点、元選択P92B endo-loop`A=X³+2`と`B=2X²+X`は**新しい**`{0,1,2,3}`の4観測点を使用。旧`{-1,0,1,2}`の補間集合と区別する。両loopを元original→phi seam反例へ昇格しない。

元F55 Type値証明の逆向き実現可能性、元P77商類の一致、P94A四セルの生成、局所seamの十分性は結論していない。真正北C60第五Dart物理閉路、既存のpositive/negative local seams、元P89 source-map BadPair**条件付き**反射は別の定理として保持する。Gray圏・GK5BA kit・GK5AY全域seam・W=1→seamの無条件十分性を主張しない。

## 4. Lean elaboration修正・次段階

独立GK5BP初回CI #41752329856では、`descPochhammer_natDegree`による`k≤k`書換えでゴールが既に閉じた後に追加の`omega`が残り`No goals to be solved`となった。全新規Leanファイル・依存GK5BO・固定mathlibの次数APIを照合して、`natDegree≤k`を明示命名して`natDegree_le_iff_coeff_eq_zero`へ渡す形に変更。定理・仮定の弱化なし。修正後、新規10宣言すべての公理監査で`propext`・`Classical.choice`・`Quot.sound`のみ。Qi v4.35は初回から全Lean検証SUCCESS。

**次GK5BQ（仮称）：** 真正下降階乗係数の符号付き第一種Stirling閉形式と固定mathlib `Nat.stirlingFirst` 再帰の一致、観測列に対する共通分母・整数整除条件の明示化、効率的に検査できる有限係数証明書へ進む。元Type値証拠のdescent可能性は別obstructionとする。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
