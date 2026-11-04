# GK5CD／Qi v4.48 — 任意分割の型可変多変数多項式代入鎖・真正CRT自然性

2026年11月5日 JST ／ F112-P94D3GK5CD・Qi v4.48 ／ **独立・Qi両定理MERGED**

## 1. 正本・exact-source CI・Git tree監査

| 項目 | 独立GK5CD | Qi v4.48 |
|---|---|---|
| 定理PR | [#3113](https://github.com/itakura-hidetoshi/KuuOS/pull/3113) MERGED | [#3114](https://github.com/itakura-hidetoshi/KuuOS/pull/3114) MERGED |
| exact-source HEAD | `290a8c05414e09c17e0509be7db648575cc9763f` | `64001bcab126f0cde747d1a2e8e629049d871cc5` |
| squash SHA | `eef2791a1c0e72b8bad54f6df33e3c9a8afc3b29` | `bb4e704a40314e248373a6d18c01c0afb2155fb3` |
| source/test-merge/squash Git tree | `4c000f047dc8b36d54d8b2ad96225a7a8b0b0812` | `b91c512e17466e31ed08bf2cfe3fc7787abfd45d` |
| exact-source CI | [#41899977266](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41899977266) | [#41901034054](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41901034054) |
| Strict Lean | **10,241／10,241 SUCCESS** | **10,242／10,242 SUCCESS** |
| Governance gate | **SUCCESS** | **SUCCESS** |
| 新規公理監査 | **13定理、sorryAxなし** | **10定理、sorryAxなし** |

- [独立GK5CD形式証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CDTypedChainSplitCRT.lean)
- [Qi v4.48形式証明](../../formal/KUOS/Architecture/QiWuxingGK5CDNorthSplitCRTV4_48.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)

canonical main HEADはQi定理squash後 `bb4e704a40314e248373a6d18c01c0afb2155fb3`。固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。既存Lean定理ソースは変更せず、独立とQiの新規モジュールと公開aggregate importのみを追記した。

## 2. 独立GK5CD — 依存型の連結とCRT RingHom自然性

前段GK5CCの真正型可変代入鎖 `T(start,length)` は、各段 `α i → MvPolynomial (α (i+1)) Int` を実在する`RingHom`へ移し、その有限長の型付き合成を作る。GK5CDは任意`start,left,right`について、前半`T(start,left)`と後半`T(start+left,right)`の合成に`Nat.add_assoc`の型移送を施し、単一鎖`T(start,left+right)`と**厳密なRingHom等式**で等しいことを証明した。

型付き等式：
`transport(Nat.add_assoc start left right, T(start+left,right) ∘ T(start,left)) = T(start,left+right)`。

長さ0の左右分割でも同一値を保持する。左側が0のとき終端添字`start+(0+right)`と`start+right`は定理的には等しいが、依存型としては無断同一視しないため、補題内で`0+right`を明示的に保持する。

この結果を大域`ZMod L_s`・元のgcd互換局所Subring`R_s`で評価する`RingHom`へ接続。実際のGK5BW CRT RingEquiv、GK5BX被覆制限、三段`u⊆t⊆s`でのCRT可換性、任意非単射初期変数再分類、元signed`Int`評価後の剰余一致を導出。法0・空被覆・負係数・非互いに素法・変数型変動を排除しない。

## 3. Leanエラーの構造理由と修正

初回CI #41878040482では、連結定理の後続ステップで`Nat.add_assoc`の依存型輸送と`RingHom.comp`の交換が未解消であり、左区間0の補題において`α(start+right)`と`α(start+(0+right))`を暗黙に同一視した型不一致も検出された。

新規ソース全文・依存元GK5CCの再帰的型付き`RingHom`・Lean4のtransportを照合し、`nativeGK5CDTransportStep`を等式帰納法`cases h; rfl`で証明。後続の合成に明示的に使用し、左零区間は型添字を`0+right`と記述して正確性を保持した。中間CIでは連結本体の公理監査からsorryAxが消え、最後に全13定理のexact-source Leanと公理監査が成功した。数学的連結主張の仮定や射の等式を弱めていない。

## 4. Qi v4.48 — 真正北C60 signed numeratorとType authority境界

元`fivefoldGK5CCNorthFiniteChainHom arity steps start length`の各段は実際の`Fin (arity i)`多変数整数多項式を変数として扱う。Qi v4.48は任意分割の真正代入鎖をそのままRingHomにし、終端変数へ**元GK5BQ符号付き`nativeGK5BQClearedNumerator`**を代入。大域`ZMod L_s`、真正compatible-local Subring、CRT RingEquiv、被覆一段／三段塔、元整数評価の可換性を10定理で証明した。

**境界：** 元F55のprimitive原Type証拠`P=1`とdouble inverse＋右F55単位`P=X²`について、original→phi seamの存在／不存在が異なることは**先行の独立・Qi形式証明で確立された別authority**。Qi v4.48で新たに別のF55 sourceやhigher cellを構築したという主張ではない。数値合同やCRT gluingから元F55 Type、P77等号、P89無条件反射、P94A四セル、普遍GK5AY seam、`W=1→seam`は導かない。既存`2≤d`・`L_s∣d!`で保証された零証明は元の整数深度多項式だけであり、任意外側代入多項式が零になるとは主張しない。

## 5. 継承境界

strict 空／独立Kuu→Qi、元F54二Nat・二圏・Blocks、元F55 Type履歴、真正北C60物理gauge、P89条件付きBadPair、公開root107、保護PR #1558 Draft/open/unmergedを保持。追加公理、sorry、admit、native_decide、Gray／GK5BA kitなし。次GK5CE（未形式化）では任意3区間以上の括弧付けとPentagon coherenceを型付きRingHom／CRT自然性へ拡張する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
