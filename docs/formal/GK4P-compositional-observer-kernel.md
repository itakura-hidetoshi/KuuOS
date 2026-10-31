# F112-P94D3GK4P — 合成・文脈の観測則からkernel互換性へ

2026-10-31 JST。定理PR [#2765](https://github.com/itakura-hidetoshi/KuuOS/pull/2765) MERGED。

この文書は追加のみの研究記録である。README.md・ROADMAP.mdの既存本文は変更していないため、この記録を両ルート文書の同期完了と解釈しない。定理の正本はcanonical `main`上のLean宣言、その型・仮定・公理依存である。

## 1. 正本と検証記録

| 項目 | 確認結果 |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / `main` |
| 定理PR | #2765 MERGED |
| 定理squash SHA | `ffba5bbc8934c9e3d2a2a4a1367b2e5a9cc2419f` |
| 検証対象のPR source HEAD | `3478fa4a1b575908fe0ce00849c6d25e99b084c0` |
| Exact-source CI | [41161570573](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41161570573) |
| Strict Lean | **3721/3721 SUCCESS** |
| Governance | **5/5 required jobs completed SUCCESS** |
| 新規宣言 | 15 named declarations + 3 compiler-contract examples |
| 公理依存 | `propext`・`Classical.choice`・`Quot.sound`以内、`sorryAx`なし |
| 変更Lean warning/error | 0/0 |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

定理マージ直後、squash SHAとcanonical main HEADの完全一致をGitHub MCPで確認した。以後の文書コミットでmain HEADが進んでも、この定理squash SHAとexact-source CIの役割は区別する。

正本ソース：
[GK4PCompositionalObserverKernel](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4PCompositionalObserverKernel.lean)

初期コミット `7bc92a4800246aa5af8769860caf87ae946d345c` は、未実装のGK4P宣言を参照する3つのコンパイラ契約を先に置いた意図的な失敗記録であり、証明receiptではない。同じ3契約は最終実装内に保持され、上記の最終exact-source CIを通過した。

## 2. 三つの観測則から四つのkernel互換性を導出

GK4Oの観測関数族は、独立D/Eカテゴリー、四つのBlocks、二つのNat深さ、完全な元F45 source/targetを保持する。値は真正な元P92B証拠存在商から読む。

任意の値域型 `B`、二項演算 `combine : B → B → B`、実F45文脈Treeで添字付けた左右の値作用を指定する。必要な十分条件は次の三つである。

```text
O(trans u v)        = combine (O u) (O v)
O(leftContext r t)  = leftAction t (O r)
O(rightContext t r) = rightAction t (O r)
```

これらから、観測値の等しさが真正F54の前合成・後合成・左文脈・右文脈で保存されるという、GK4Oの四つのkernel互換性をすべて導出した。値域の演算に結合律・単位律・単射性・可逆性は仮定しない。

中心定理 `nativeGK4P_kernel_of_laws` は **公理に依存しない**。入力は明示的な三つの観測則であり、任意の観測が自動的にそれらを満たすという主張ではない。

導出したkernel互換性をGK4Oへ代入し、同じ十分条件の下で以下を証明した。

```text
全14の真正F54構造seam保存 ↔ 7つの基本seam保存
全境界でのGK4E構造商への降下 ↔ 7つの基本seam保存
```

ここで全境界とは、定義した観測関数族の元F45 source/target・Blocks・深さにわたる量化である。global strict nやhyperdescentの完成を意味しない。

## 3. BooleanとOption Natの具体的な対照

| 元P92B商上の実観測 | 合成の値演算 | 左右文脈の値作用 | 四つのkernel互換性 | 構造商への降下 |
| --- | --- | --- | --- | --- |
| GK4G Boolean grade | `Bool.and` | 恒等写像 | 証明済み | 証明済み |
| GK4K Option Nat | 既存`nativeGK4KAdd`（none吸収型加法） | 恒等写像 | 証明済み | 実F45 stageが存在すれば不成立 |

値作用が恒等であることは、生の文脈付き経路や元Type値証拠を同一視することではない。観測値だけについての法則である。

Option Natも真正F54の合成・左右文脈に整合し、四つのkernel互換性を満たす。しかし真正の左単位構造seamは、観測値が `some 2` と `some 1` になる経路を比較する。そのため7つの基本条件のうち単位条件を満たさず、GK4Eの独立構造商へ降下できない。

したがって、**kernel互換性だけでは構造商への降下に十分でない**ことを、真正な元P92B観測による具体的な反例として証明した。これは7つの基本条件の相互の論理的独立性や最小性を証明したという意味ではない。

真正C60北側六角形の元F45三重Treeでは、実P92B商の前合成がOption Nat観測の等しさを保存することと、同じ観測が構造商へ降下不能であることを同時に形式化した。可算性や人工的な経路空間への置換は用いない。

## 4. 主なLean宣言

- `nativeGK4P_kernel_of_laws`：三つの観測則から四kernel互換性。
- `nativeGK4P_factor_iff_seven_of_laws`：観測則の下で真正構造商降下と基本7条件が同値。
- `nativeGK4P_boolean_kernel_and_descent`：Booleanの互換性と降下。
- `nativeGK4P_option_kernel_without_descent`：Option Natの互換性と不降下。
- `nativeGK4P_kernel_not_sufficient`：kernel互換性だけから降下を導く一般命題の反例。
- `nativeGK4P_physical_north_kernel_vs_descent`：同一の真正C60文脈での対照。

## 5. 維持する境界と次段階

既存Leanファイル、公開root、Lean/mathlib pinは変更していない。strict空を中心とし、独立Kuuを一つのpresentationとして保持する。元Type値証拠、元P92B証拠存在商、独立F54構造比較商を区別する。Grayは再導入しない。保護PR #1558はDraft・OPEN・未マージを保持。

元P92B商の結合律、代替合成、歴史的完全型付き同型、真正14Dの無条件可算性、元19D filler、global strict n、hyperdescentは引き続き未証明。

**次のGK4Q（研究候補、未実装）**：kernel互換性から、元の型付き観測像に誘導される合成・文脈作用の存在と一意性を検討する。観測像上の作用と、全値域B上の作用を区別し、全射性なしに全値域の演算を捏造しない。

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
