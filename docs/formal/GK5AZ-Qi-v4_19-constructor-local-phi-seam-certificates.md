# F112-P94D3GK5AZ / Qi v4.19 — 元F55構成子別raw–φ seamと真正北C60の局所証明書

**研究継承日：2026年11月3日 JST。** Repository: [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)。
数学上のauthorityはstrict 空／独立Kuu→Qiであり、元F54双Nat・2圏・Blocks・F55 Type-valued証拠・元P89・選択P92B/P93C/P94Aを区別する。C60五行物理gaugeをsourceの高次証明書の代用にしない。公理追加、Gray再構築、無条件元P89 reflection／nonreflection、無条件全域seamの実在は主張しない。

## 1. 承認済み独立GK5AZ

- [独立定理PR #3025](https://github.com/itakura-hidetoshi/KuuOS/pull/3025) **MERGED**、main squash SHA `197a514e39cf72bd2e262e2699fbd1556a23dab1`。
- 最終検証対象ソースHEAD：`a75eb243375fc48d92e93c6b3c430c4f5fea3b98`。
- [exact-source Governance CI #41608786472](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41608786472)：**Strict Lean 9,256/9,256 SUCCESS、Governance 30/30 SUCCESS**。変更Leanファイルは0 error、32件の `#print axioms` 出力から `sorryAx` は見つからない。証明・構成定義は原則公理依存なし。選択による存在分岐と実在する北atomの計算・表示定義はLean標準の `propext`・`Classical.choice`・`Quot.sound` の範囲。
- [独立Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AZConstructorLocalSeamObstruction.lean) **655行**。公開 `KuuOSFormal` にimport追加。元source/APIは書き換えない。

## 2. 構成子別seamの数学

元F55 3-proof `f` の正確な依存型 `P92B.original(f)` と、GK5AIの9構成子再帰写像 `φ(f)` を結ぶ真正選択P94A 4-cellを

`SeamAt(f) := P94A(P92B.original(f), φ(f))`

と定義する。`SeamAt` は単なるraw証拠等式ではなく証拠をもつ型であり、任意の `f` でinhabitedと宣言しない。

| 真正元F55構成子 | 局所構成／必要なゲート |
| --- | --- |
| `pentagon` | 元atomで `original(f) = φ(f)` は定義的。真正 `P94A.refl` を無条件構成（任意のF54依存添字） |
| `disjointSquare` | 元atomで `original(f) = φ(f)` は定義的。真正 `P94A.refl` を無条件構成 |
| `ident` | raw `original(ident(r))` と選択 `refl(r)` は**証明項として不等**。4-cellは独立局所ゲートであり不存在を証明しない |
| `symm` | raw全体のsymm-wrapper解体と、P92Bの3-cell symmへの尊重4-cellの**2条件**を分ける。P94A 4-cellの `symm` をP92B 3-cellへの作用と混同しない |
| `trans` | raw全体wrapperをraw部分証拠の `trans` へ移す1つのshellと、既存2子の局所seamをP94Aの左右whiskeringで合成 |
| `leftContext` | 外側raw-wrapper-to-context shell＋実際の `P94A.leftContext` |
| `rightContext` | 外側raw-wrapper-to-context shell＋実際の `P94A.rightContext` |
| `precompose` | 元F54前合成を保つraw shell＋選択 `P94A.precompose` |
| `postcompose` | 元F54後合成を保つraw shell＋選択 `P94A.postcompose` |

合成の中心定義 `nativeGK5AZTrans_of_shell` は、型付きに

```
original(trans(f,g))
   -- raw trans shell --> trans(original f, original g)
   -- rightWhisker bridge(f) --> trans(phi f, original g)
   -- leftWhisker bridge(g) --> trans(phi f, phi g)
```

という真正4-cellを作る。`nativeGK5AZTrans_seam_or_shellHole` は、2つの子seamが実在した場合に親seamかraw shell欠損があるという**条件付き分岐**を形式化した。実際のshell欠損の存在は未証明。

## 3. GK5AX垂直primitive・GK5AW 8 contextの真正接続

- `nativeGK5AZRawP93_to_phi`：両端だけの局所seamと元のraw P93C証明書からP94A φ端点比較を構成。全域GK5AY seam不要。
- `nativeGK5AZPhi_to_raw`：選択φ端点比較をraw `original` 端点へ移す。元P89四セルを生成したこととは異なる。
- `nativeGK5AZRawLeftVerticalUnit`、`RawRightVerticalUnit`、`RawVerticalAssoc`：GK5AXの真正選択P94A 3 primitiveを2端点の局所seamでraw端点へ移す。
- `nativeGK5AZRawLeftUnit_from_local_gates` と `RawRightUnit_from_local_gates`：`ident`局所4-cell＋`trans`局所shell＋元F55子seamを正確に合成。
- `nativeGK5AZLeftContextIdentity_normalize` と `RightContextIdentity_normalize`：追加P94A contextUnit primitiveを使い、元identの条件付きraw正規化を構成。
- GK5AW全8の本来の元P89生成元：left/right whisker、left/right F45 context、pre/post F54 context、horizontal left/right。いずれも**実在するraw P93C比較＋2端点局所seam＋親BadPair**から、元F55子証拠ペアの真正GK5AQ BadPairを導出する。sourceのF54・Blocks添字を捨てず、P94Aの内部source-holeを無条件に消さない。

## 4. Qi v4.19 — 真正北C60 source-specific適用

[Qi v4.19 PR #3026](https://github.com/itakura-hidetoshi/KuuOS/pull/3026) **MERGED**。最終exact-source HEAD `94a15a33f2dd504e6523e8a1d7e5074c50523f09`、main squash `2c5528b534892c701022da1e80f223e48c7cfdb0`。[Governance #41609637738](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41609637738) は **Strict Lean 10,183/10,183、Governance 30/30 SUCCESS**、8宣言の公理監査で`sorryAx`はなく、通常のLean公理`propext`・`Classical.choice`・`Quot.sound`の範囲。 [Qi v4.19 Lean source](../../formal/KUOS/Architecture/QiWuxingGK5AZNorthConstructorLocalSeamsV4_19.lean) **248行**、公開`KuuOSFormal`へimport済み。

元北四段pentagon元F55 proof `p`、元F54短経路の元F55 `ident(s)` の真正合成 `c := trans(p, ident(s))` を対象に：

1. `SeamAt(p)` は元pentagon atomから無条件に構成。
2. raw `original(ident(s)) ≠ phi(ident(s))` を元Type値証拠の構成子相違として証明する。
3. **`SeamAt(ident(s))` と `P94A(original(c), trans(original(p), original(ident(s))))` の2局所ゲート**が実際に与えられれば、`SeamAt(c)` を真正P94A whiskeringで構成。
4. さらに選択P94A右単位を合成し、raw `original(c) → original(p)` の真正P94A 4-cellを構成。元P89四セルは依然として別障害。
5. 先行GK5AXの `BadPair(c,p) ↔ ¬ Nonempty(P89(c,p))`、第五around Dartの真正閉路・e04/e43物理向きを保持。五行gaugeは局所2ゲートを供給しない。

## 5. 継承境界と次の研究

公開root107維持、元F54双Nat/category/Blocks/historyを保存、固定Lean **v4.30.0-rc2**／mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**、保護PR **#1558 Draft/OPEN/未マージ**。append-only、no `sorry`/`admit`/`native_decide`/新公理。公理依存と元sourceの4-cell存在は区別する。

**次段階**：元F55の9構成子すべての局所shellの存在条件を、依存型再帰の1つのデータ構造に集約できるかを調べる。特に `ident`、`symm`、`trans` の3種類の高次obstructionが、非自明な北C60実例で満たされるか否かは未解決。存在条件を証明しないまま全域seamや元P89無条件faithfulness／nonfaithfulness、全P94A 19構成子の正規化を主張しない。
