# GK5CE／Qi v4.49 — 4区間5括弧付けの型可変RingHom Pentagon境界と真正CRT自然性

2026年11月5日 JST ／ F112-P94D3GK5CE・Qi v4.49 ／ **独立・Qi両定理MERGED**

## 1. 唯一の正本・exact-source検証

| 項目 | 独立GK5CE | Qi v4.49 |
|---|---|---|
| 定理PR | [#3116](https://github.com/itakura-hidetoshi/KuuOS/pull/3116) MERGED | [#3117](https://github.com/itakura-hidetoshi/KuuOS/pull/3117) MERGED |
| exact-source HEAD | `f5337045a120b5bd51d0809223fb24ee3ade09a1` | `c6b05f5bc1866327c2f91e0c08591679c7d1aef2` |
| squash SHA | `fa16ef40c37419b33da94b0e1a43f1a52f34f5c5` | `94fd315eeae36f23f08cc3df9a91a51f958d1845` |
| source/test-merge/squash Git tree | `bba77ca72145a07b1d1a993996f8fa53a28fcdab` | `c4940dbdd020a094c43a7cf3308d9552f702c3ab` |
| exact-source CI | [#41919563732](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41919563732) | [#41920712069](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41920712069) |
| Strict Lean | **9,317／9,317 SUCCESS** | **10,244／10,244 SUCCESS** |
| Governance | **SUCCESS** | **SUCCESS** |
| 公理監査 | **14定理、sorryAxなし** | **14定理、sorryAxなし** |
| 新規Leanソース | **342行** | **423行** |

- [独立GK5CE形式証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CEFourSegmentPentagonCRT.lean)
- [Qi v4.49形式証明](../../formal/KUOS/Architecture/QiWuxingGK5CENorthFourPentagonCRTV4_49.lean)
- [公開集約KuuOSFormal](../../formal/KuuOSFormal.lean)

Qi v4.49をマージしたmain SHA：`94fd315eeae36f23f08cc3df9a91a51f958d1845`。各定理は元の固定Lean `v4.30.0-rc2`・mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` で検証した。既存Lean定理ソースは変更せず、新規モジュールと公開集約へのimportのみ追加。公開root107維持、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 2. 独立GK5CE — 五つの実在するRingHomとPentagon境界

元GK5CCの型付き有限多項式鎖`T(start,n)`とGK5CDの任意位置分割`RingHom`から、4区間長`a,b,c,d`に対して五つの括弧付け
```text
(((a+b)+c)+d)
((a+(b+c))+d)
((a+b)+(c+d))
(a+((b+c)+d))
(a+(b+(c+d)))
```
を実際の二分割合成として構成し、`Nat.add_assoc`に沿う`congrArg (fun n => start+n)`の**型付きtransport**で終端を一致させた。各`RingHom`が同一の`T(start,a+(b+(c+d)))`へ正規化されると証明し、その五つの境界比較を同時にLeanで証明。

さらに大域`ZMod L_s`、gcd互換局所Subring`R_s`への多変数整数評価`RingHom`、CRT環同型`Φ_s`、被覆制限`q_{s,t}`／`ρ_{s,t}`、三段`u⊆t⊆s`のCRT自然性を同一の型付きRingHom構成で証明した。法0、空被覆、非互いに素、変数型変動、負係数、区間長0を排除しない。

**数学的境界：** 今回のPentagon形は`RingHom`等式の五角形であり、圏論のassociator自然同型・2-cell・P94Aの高次四セルの存在を証明するものではない。高次cellの出典・型証拠は別authorityとする。

## 3. Qi v4.49 — 真正北C60 original signed numeratorとの接続

各段で`Fin (arity i)`の変数型を保ったまま、五つの括弧付けを独立GK5CEの正規化`RingHom`として移送。終端の`fivefoldGK5CENorthFourTerminalSigned`は、元GK5BQの**真正符号付き整数分子**`nativeGK5BQClearedNumerator depth (indices v) values`そのものである。`natAbs`や新しい元F55 Type sourceは作らない。

同一の元符号付き値で多変数整数多項式を評価することと、真の大域`ZMod L_s`・局所互換Subringへ先に移すことの可換性を、真正CRT環同型と被覆一段／三段自然性を含めて形式証明。**元F55 primitive P=1とdouble inverse＋右単位P=X²のoriginal→phi seam存在／不存在は、先行の別型付き定理に依拠する区別として保持**する。今回の数値的Pentagon整合性が元F55 Type源、P77類、P89無条件反射、P94A高次セル、普遍GK5AY seam、W=1→seamを再構築したとは主張しない。既存の条件付き整数深度多項式CRT零を任意外側多項式の零へ拡張しない。

## 4. 検証・継承境界

両PRとも初回exact-source CIで新規Leanモジュールと公開集約`KuuOSFormal`のビルド成功。公理監査はそれぞれ14定理、`sorryAx`なし。source/test-merge/squash Git treeが各定理PRで一致。定理命題・前提の弱化や既存Lean定理の書換えなし。strict 空／独立Kuu→Qi、元F54二Nat・二圏・Blocks、F55 Type履歴、真正北C60 gauge・条件付きP89 BadPairを別authorityとして保持。追加公理／sorry／admit／native_decide／Gray／GK5BA kitなし。

**次GK5CF（研究計画、未形式化）：** このRingHom等号Pentagonと、元original／phiのpresentationや構造的Type seamにおける高次coherenceとの比較を、必要な型・自然変換・障害条件を明示して進める。数値的coherenceを無条件に高次Type証拠へ昇格しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
