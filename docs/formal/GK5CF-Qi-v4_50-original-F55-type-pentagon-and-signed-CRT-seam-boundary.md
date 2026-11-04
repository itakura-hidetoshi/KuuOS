# GK5CF／Qi v4.50 — 真正元F55 Type値PentagonとRingHom／高次seamの比較

2026年11月5日 JST ／ **F112-P94D3GK5CF・Qi v4.50 — MERGED**

## 1. 唯一の正本とexact-source検証

| 項目 | 独立GK5CF | Qi v4.50 |
|---|---|---|
| 定理PR | [#3119](https://github.com/itakura-hidetoshi/KuuOS/pull/3119) **MERGED** | [#3120](https://github.com/itakura-hidetoshi/KuuOS/pull/3120) **MERGED** |
| exact-source HEAD | `1b09a080b9d000bdd873020901cc98d23c3f5687` | `12f5105dc981528c5855820217643cedaa791096` |
| squash SHA | `ef802ecf6ce56fd11416e1d48b35ddb09ce6bf13` | `21e51c50de09c73a7addf6a586e6a050c3017bac` |
| source/test-merge/squash Git tree | `564ba61fcafef1e724c420072fe28e8e2b9e380c` | `a574a66f4234546bd131079fa06f9b91b326f4ca` |
| exact-source CI | [#41924042634](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41924042634) | [#41925498016](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41925498016) |
| Strict Lean | **9,319／9,319 SUCCESS** | **10,246／10,246 SUCCESS** |
| Governance | **30／30 SUCCESS** | **30／30 SUCCESS** |
| 新規公理監査 | **25宣言、sorryAxなし** | **15宣言、sorryAxなし** |
| 変更Leanコンパイルエラー | **0** | **0** |

- [独立GK5CF形式証明](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CFOriginalPhiTypedPentagonComparison.lean)
- [Qi v4.50形式証明](../../formal/KUOS/Architecture/QiWuxingGK5CFNorthSourcePentagonSeamCRTV4_50.lean)
- [公開Lean集約](../../formal/KuuOSFormal.lean)

**確定正本：** `itakura-hidetoshi/KuuOS` の`main`、Qi v4.50までの最新マージ済みHEAD `21e51c50de09c73a7addf6a586e6a050c3017bac`。Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。既存定理ファイルを変更せず新規Leanモジュール＋公開aggregate importのみ。公開root107維持、保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ。

## 2. 独立GK5CF — 真正元F55の高次Pentagon境界

GK5CEの5種の型可変多項式代入RingHom等式とは**独立**に、真正元F55の4つの合成可能なType値付き証拠`f,g,h,k`を、その元F54依存型始終端のまま次の5括弧付けとして構成する：

```text
(((f·g)·h)·k)
((f·(g·h))·k)
((f·g)·(h·k))
(f·((g·h)·k))
(f·(g·(h·k)))
```

元P77の真正結合律四セル、左whiskering、右whiskering、逆転で五角形の**5本のType値付き四セル**を構成。上側3辺と下側2辺を別々の本物のP77四セル鎖として得て、それぞれ歴史的な7段old埋め込みで元raw-wrapper端点のP94A四セルへ移送した。

**正確な境界：** 上下2本の四セル証拠は**存在する**が、その証明項同士の等式、pentagonatorの五セル、自然同型の無条件高次同一視は証明していない。元P77で得た5辺に沿って`Nonempty(SeamAt(f))`を移送でき、5頂点の局所original→再帰φ seam存在性が同値になる。全元F55証拠に一様に存在するGK5AY seamはGK5BBのno-goにより依然として不可能。

GK5CEの数値`RingHom` Pentagonを、5等式からなる**Prop** `nativeGK5CFNumericalPentagonBoundary`として明示し、実際の証明項`nativeGK5CEFourPentagon_boundary`と区別した。高次比較条件`nativeGK5CFPentagonHigherComparison`は、この数値Propと**真正P94A local seamの存在**の連言であり、数値Propが常に成り立つため、高次比較成立とlocal seam存在が必要十分。数値等式単独から元F55の証拠は復元できない。

**北C60の反例：** 真正元pentagon primitive`p`は局所seamが実在する。一方同じ元F54 long→short Homの元F55`symm(symm(p))`は、選択φの元wrapper数`N=1`、符号付き個数`S=1`をprimitiveと共有しても、反転深度重み`W=4`対raw`W=1`の障害によりlocal seamは存在しない。両者の数値RingHom Pentagonが無条件に整合しても、高次Type証拠存在性は異なる。

## 3. Qi v4.50 — 元符号付き北C60 signed CRTと実在する元F55五角形

元GK5BQの`nativeGK5BQClearedNumerator`に評価する4区間型可変多項式代入を用い、真の有限非互いに素CRT環同型・大域ZMod・局所gcd互換Subring・全被覆制限・三段塔の`RingHom`自然性を保持した。

実際のsigned CRT RingHom等式を別の**Prop** `fivefoldGK5CFNorthSignedCRTRingHomBoundary`として定義。その数値条件に独立GK5CFの真正元F55 local seam条件を重ね、元北source`src`に対して

```text
SignedCRT ∧ HigherOriginalPhiPentagon(src)
    ↔ Nonempty(SeamAt(src))
```

を、独立したLean証明として成立させた。

さらに、**元F55 primitiveまたはdouble inverse ＋ 元F55の本物の右identityを3回**という4要素の五角形を実際に作った。primitive側はP77/P94A右単位の真正四セル輸送によって5頂点すべてに個別seamを構成。double inverse側は同じく元F55/P77型付き証拠で移送を逆向きに適用し、5頂点全部のseamが成立することは不可能と証明。**元P77五角形の存在そのものは両側で成立**し、失われるのはoriginal→選択φの局所高次seamである。

真正北C60の**三段CRT環同型/被覆制限の等式が成立**することと、double inverseの局所高次seam**不存在**が同時に証明された。数値CRTのdescentと元Type証拠のdescentは別のauthority・obstructionを持つ。

## 4. Lean4修正記録と今後の課題

GK5CF初回CIでは、`nativeGK5CEFourPentagon_boundary ...`という**定理の証明項**を`∧`の命題位置に置いたためLean4で型不一致を生じた。5辺のRingHom等式を別`Prop`として完全に定義し、元定理を証明項として使うよう修正。**命題の弱化なし**。変更Leanファイル全文・imports・依存定義・固定mathlib API照合後、再CI `9,319／9,319`で成功。Qi v4.50も同じ区別を継承し初回exact-source CIで`10,246／10,246`成功。

**次GK5CG（研究課題）：** 2経路の元P77四セルを証明項として保持したまま、どの追加の型付き五セル／高次比較証拠でpentagonatorが存在するかを検討する。元P94Aの19構成子に対する全域正規化、元P89 class mapの無条件反射、逆向きQi→独立Kuu、原始元F55証拠の数値CRTからの無条件復元は主張しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
