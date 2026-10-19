# KuuOS 五行群作用と型付き自由経路 v3.1

## 数学的目的

既存の `v2.6 → v2.7 → v2.8 → v2.9 → v3.0` の成果を保持する。
そのうえで、群作用と独立Kuuの自由経路圏を接続する。

五相は固定した物質でなく、関係的位相 `FivePhase = ZMod 5` である。

```text
木 0 → 火 1 → 土 2 → 金 3 → 水 4 → 木 0  (相生 +1)
木 0 → 土 2 → 水 4 → 火 1 → 金 3 → 木 0  (相剋 +2)
```

### 1. 五次巡回群の忠実かつ推移的な作用

```text
rotation δ (p) = p + δ  (mod 5)
rotation (a+b) = rotation a ; rotation b
rotation 0 = identity
rotation is injective
every phase q is reached from p via δ=q-p
```

相生 `S = rotation 1`、相剋 `K = rotation 2`。
位相写像として `K(p)=S(S(p))`。

### 2. 型付きの自由経路は同一視しない

独立Kuuの `Kuu.Presentation` とmathlib `Quiver.Path` を直接用いる。

- `Arrow.generation p : p → S p`
- `Arrow.control p : p → S (S p)`
- `directControlPath p` の長さは1
- `twoGenerationPath p` の長さは2

両者は同じ始点と終点を持つが、自由経路として異なる。

```text
source / target:      equal
group displacement:   equal
path length:          1 ≠ 2
free path:            distinct
```

単に作用先が等しいことを根拠に、2本の経路の等式を追加しない。
`Kuu.identityRelations` の下でも異なる経路の商像が異なることを証明する。

### 2b. イベント数が等しくても経路は異なる

同じ始点 `p` から、相生→相剋と相剋→相生の二つの経路を作る。

```text
p → S(p) → S³(p)           generationControlPath
p → S²(p) → S³(p)          controlGenerationPath
```

両経路は始点、終点、長さ2が一致する。しかし中間頂点は
`S(p) ≠ S²(p)` なので、mathlibの
`Quiver.Path.obj_eq_of_cons_eq_cons` により経路は等しくならない。

`pathShift` は両者を同じ `(+3, 2)` に写すため、
「位相・イベント数」観測は自由経路の順序を忘れる。
この区別も、`Kuu.identityRelations` の下で商に降りても保持される。

### 3. 忘却観測と合成の整合

各型付き経路 `path : Path p q` に

```text
pathShift(path) = (q-p, path.length) : ZMod 5 × Nat
```

を対応させる。

```text
pathShift(path.comp(next)) = pathShift(path) + pathShift(next)
rotation (pathShift(path)).1 p = q
```

この写像は合成に整合するが、一般には忠実でない。

### 4. 履歴の回数さえ、順序を完全には表さない

```text
[generation, control] ≠ [control, generation]
relationWordShift [generation, control]
  = relationWordShift [control, generation]
```

従来の `WuxingShift = FivePhase × Nat` は位相変位とイベント数を保持するが、
二つのイベントの非可換な順序そのものは保持しない。
順序の追跡には、関係語または自由経路を保持する必要がある。

これは `v2.7` の長さの異なる経路の区別とは独立の情報損失である。

## 既存理論・権限境界

- v2.6–v3.0の定理本文・名前・仮定は変更しない
- `formal/Kuu/Presentation.lean` の独立空商を使用し、Grayを基礎としない
- 射の同一視には、Kuuに指定された交代・置換関係が必要
- `Nat` を負の時間へ拡張しない
- 相乗は強度に関する別問題。相侮は `-2` 方向
- 群作用の整合は、病勢・臨床的効果・物理ゲージ理論の検証ではない
- 陰陽五行テンソルや臨床状態への写像は、別途定義・検証するadapterである

## Lean4 / mathlib

```sh
lake exe cache get
lake lean formal/KUOS/Architecture/QiWuxingCyclicGroupPathsV3_1.lean -- -DwarningAsError=true -DsorryAsError=true
lake build KuuOSFormal
```

標準公開入口は従来どおり `KuuOSFormal` 一つ。
増分チェックはその部分コンパイルであり、別の定理正本を作らない。


新モジュール：
`formal/KUOS/Architecture/QiWuxingCyclicGroupPathsV3_1.lean`

Copyright © 2026 Hidetoshi Itakura / 板倉英俊.
