# KuuOS / 空OS

[![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml)
[![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml)
[![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml)

**KuuOS（空OS）** は、**空・縁起・関係・文脈・表現の交代可能性・高次圏論・obstruction-aware descent** を数学的に扱う研究体系です。Lean 4による形式化と、別途検証が必要なAI推論ランタイム研究の双方を含みます。

**研究・著作権者 / Founder and copyright holder:** **板倉英俊 / Hidetoshi Itakura**。ソースコード・文書のライセンスは [Apache License 2.0](LICENSE)（`Apache-2.0`）。[NOTICE](NOTICE)・[COPYRIGHT.md](COPYRIGHT.md)を参照してください。

> **空は、異なる原表示を無条件に同一視することではない。** 文脈と保存量を明確にしたうえで、交換可能な表現を証明し、合成・輸送・貼り合わせが不整合ならその障害を残す。

English: KuuOS is a research architecture for dependent origination, context-dependent presentations, exact categorical quotients, presentation replaceability, compositional coherence, and obstruction-preserving descent. The mathematical results are versioned Lean declarations; runtime use and empirical validity require independent evidence.

## Verified formal frontier / Lean4の現在の正本

**2026-10-15 JST 再確認：`v5.264 / F108` 第3段階まで統合済み。真正C60全スターへの非恒等原F51関手を構成済み。二つの隣接面を独立に保持する原F42/F55比較はOPEN。**

| 検証項目 | 最新の確認済み権威 |
| --- | --- |
| Repository / canonical branch | [`itakura-hidetoshi/KuuOS`](https://github.com/itakura-hidetoshi/KuuOS) / `main` |
| **最新 theorem-bearing PR** | **[PR #2286 — v5.264 F108第3段階, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2286)** |
| **Theorem-bearing merge SHA** | **`aefcb17f23c7f8f0e6627c49150001858f513d4f`**（PR #2286のマージ後に`main`と一致を確認） |
| Exact tested source HEAD | `92d6541eb0682394dd4c9b5e6050510af224a9a5` |
| Exact-head proof CI | [GitHub Actions #38642525139](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38642525139) — **completed SUCCESS** |
| Strict Lean target | `KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264` — **9076/9076 jobs SUCCESS** |
| Governance / MCP | Strict Lean・Governance・MCP Lean completion・MCP CI completion **全SUCCESS** |
| Changed-file audit | **warning/error 0/0**、**10 `#print axioms`**、**`sorryAx`なし** |
| Pinned versions | [Lean `v4.30.0-rc2`](lean-toolchain)、[mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`](lake-manifest.json) |
| Separate verification only | [PR #1558 — Lean 4.31](https://github.com/itakura-hidetoshi/KuuOS/pull/1558): **OPEN / DRAFT / NOT MERGED**。正本へマージしない |

**Authority rule:** その時点の実`main` HEAD → 正確なLean定理・依存ファイル → 文書 → 同じsource HEADのCI・証跡 → 履歴、の順に確認してください。README・ROADMAPだけの更新でも`main` SHAは動きますが、**数学的theorem-bearing SHAは変わりません**。選択したLeanモジュールのCI成功は、リポジトリ全体・実行環境・AIモデルの検証を意味しません。`#print axioms`には通常の`propext`、`Classical.choice`、`Quot.sound`のほか、初期C60有限幾何に由来する`native_decide`の公理依存が含まれる場合があります。これらを`sorryAx`や新しく導入した未審査公理と混同しないでください。

## 空＝型付きの表現交代可能性 / Mathematical core

F94–F95では、真正のC60経路`p,q`に沿う**平行な原F51の3射**`f,g`について、意図的に構成されたF77商圏への観測`Q`が

\[
\boxed{
f\sim_{\mathrm{kuu}}g
\iff Q(f)=Q(g)
\iff \operatorname{charge}(f)=\operatorname{charge}(g)
\in\mathbb{Z}\times\mathbb{Z}
}
\]

を満たします。**二つの独立した整数荷電は消去されません。** 元の交換位相（`ZMod 2`）は**この明示的な商圏に写した後にだけ**忘却されます。異なる原F42/F43やF54/F55の証明項が元の型で同じになるわけではありません。

また各経路対に対するF95の真正の圏商`Q_{p,q}: \mathcal P(p,q)\to\mathcal K(p,q)`は、F94の交代可能性を保存する観測関手に対して**一意の因子化**を持ちます。

\[
F=\overline F\circ Q_{p,q},\qquad \exists!\,\overline F
\quad\text{（`F`が交代可能性を保存する場合）}.
\]

この仮定は本質的です。局所的な一意因子化だけから、異なる物理パッチ間の無条件な大域貼り合わせは導けません。

### 証明対象の区別 / Do not collapse the layers

| 層 | 証明・操作できること | 誤って主張しないこと |
| --- | --- | --- |
| 原C60幾何 | **60頂点、90物理辺、32実多角形面（12五角形、20六角形）**、360入射旗標、真正の有向`Quiver.Path` | 入射旗標の`K₂,₂`四角形を新たなC60表面の正方形面とみなすこと |
| 原F42/F43/F51/F54/F55 | 型付き2射・3射の原表示と独立した位相・荷電・曲率 | 異なる原構文を無条件に等置すること、既存のF43に無かったF51の追加生成子を過去に遡って同一視すること |
| F75–F83、F94–F108（第3段階） | 二成分荷電の真正`CategoryTheory.Quotient`、F95局所商圏、条件付きdescent、原C60経路からの非恒等F42面ラベル・局所F95関手、**全90物理辺スターで位相1の非恒等原F51関手** | F77の一致を元の全F42/F55位相保存同値や無条件の物理的hyperdescentとみなすこと |
| 実物理曲率 | F68の符号付き2-cochain、局所非平坦性、必要な非ゼロ修復 | 全32面の有向和がゼロであることから個々の五角形・六角形が平坦だと推論すること |

**明示的なobstruction:** 元の北五角形の第2整数荷電は**`−5`**です。F77観測後の比較射が追加荷電ゼロでも、この原F55物理曲率は消えません。修復を使うならF68の非ゼロ補正を明示的に扱う必要があります。

## Formal milestones / 証明済みの主要段階

| 範囲 / PR | Lean4で証明した到達点（その型と仮定の範囲内） |
| --- | --- |
| v4.00–v5.101 | presentation-sensitiveな局所化と障害、原`F/G/η/ε`、独立したforward/reverse swallowtail、[v5.101 coherent biadjunction](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) |
| v5.102–v5.154 | Native mates/adjunction、独立したF19/F28軸、有限合成・原F45/F54/F55の構成 |
| v5.155–v5.228 | 真正のC60幾何・F42/F51/F55入射と曲率、有限アトラス・Čech・nerveの条件付き結果 |
| [F75–F93 / #2248–#2266](https://github.com/itakura-hidetoshi/KuuOS/pull/2266) | 独立位相を忘却するF77圏商、F78 globular certificate、F80の商Hom tensor、モノイダル整合性、F93の比較tensorator等式 |
| [F94–F95 / #2267–#2268](https://github.com/itakura-hidetoshi/KuuOS/pull/2268) | 正しい原F51境界上の荷電による交代可能性、真正の局所`CategoryTheory.Quotient`と普遍因子化 |
| [F96–F99 / #2269–#2272](https://github.com/itakura-hidetoshi/KuuOS/pull/2272) | F95水平・垂直双関手、4入力F98観測交換`NatIso`、F99左右`whiskering`関手の局所商圏へのdescent |
| [F100 / #2274](https://github.com/itakura-hidetoshi/KuuOS/pull/2274) | 左→右と右→左の実C60文脈順序をF77観測後に`NatIso`で比較。原F42の異なる括弧は同一視しない |
| [F101 / #2275](https://github.com/itakura-hidetoshi/KuuOS/pull/2275) | 4入力の文脈化された水平／垂直交換`NatIso`の可換四角形を自然変換の等式として証明 |
| [F102 / #2276](https://github.com/itakura-hidetoshi/KuuOS/pull/2276) | 4入力の二重文脈順序LR/RLと水平／垂直HV/VHによる比較四角形の高次整合性 |
| [F103 / #2277](https://github.com/itakura-hidetoshi/KuuOS/pull/2277) | 4経路の**観測後五角形整合性**、ゼロ追加荷電自然変換の一意性、F102比較経路の高次一意性 |
| [F104 / #2278](https://github.com/itakura-hidetoshi/KuuOS/pull/2278) | **同一原経路対上**の有限左右文脈アトラスで厳密Čech 1-cocycle、任意長経路独立性、基準観測への比較と追加荷電障害 |
| [F105 / #2279](https://github.com/itakura-hidetoshi/KuuOS/pull/2279) | **異なる実C60物理辺**のF95局所圏を**与えられた重なり圏・制限関手**で比較。`Int × Int`差のcocycle、条件付き貼り合わせと非ゼロ障害、北五角形曲率の保持 |
| [F106 / #2280](https://github.com/itakura-hidetoshi/KuuOS/pull/2280) | F69の真正の**入射スター有限交差圏**、部分集合による制限関手、共有頂点・共有実多角形面の存在証明。F95意味論は明示的な追加データ |
| **[F107 / #2281](https://github.com/itakura-hidetoshi/KuuOS/pull/2281)** | 原F42の対象ラベル・型付き原F51の射語を与え、**二成分荷電の単位律・合成律からF95意味論関手を構成**。原F51への持ち上げには別途`ZMod 2`位相整合性を要求し、原F42境界次数と位相合成の障害を証明 |
| **[F108 第1段階 / v5.262 / #2283](https://github.com/itakura-hidetoshi/KuuOS/pull/2283)** | 実際の五角形・六角形面と型付き前後`Quiver.Path`から**次数1の原F42面ラベル**と原F51恒等語による局所F95/F51関手を構成。別途、原F43交換射の前後文脈化により`charge=(0,0), phase=1`の**非恒等F51射**を真正F69入射三角形の比較とともに構成（文脈経路の存在は入力） |
| **[F108 第2段階 / v5.263 / #2284](https://github.com/itakura-hidetoshi/KuuOS/pull/2284)** | 原C60正逆90辺から北基点→全60頂点、任意2頂点間の真正`Quiver.Path`を構成。F108の前後文脈経路の存在を証明して**全90物理辺**のF42/F95意味論を構成。保守的な原F51恒等語のスター全体への拡張と、独立した非恒等交換射の存在を区別 |
| **[F108 第3段階 / v5.264 / #2286](https://github.com/itakura-hidetoshi/KuuOS/pull/2286)** | 真正F69入射半順序の頂点層→辺・面層の単調関手と`Bool` walking-arrowから、**全スターHomに定義される非恒等の原F51関手**を構成。実頂点→物理辺射が`charge=(0,0), phase=1`の原F43/F51交換3射へ写ることを証明。両上位面は選んだ一方の面由来の二つのF42水平合成表示を使う（面別F42は次段階） |

特に最近のtheorem-bearingファイルは次のとおりです（各リンクは実際のLeanソース）。

- [F100 — 二方向の観測順序](formal/KUOS/DependentOriginationC60KuuTwoSidedContextCoherenceV5_254.lean)
- [F101 — 文脈化4入力交換](formal/KUOS/DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255.lean)
- [F102 — 二重文脈と交換の四角形](formal/KUOS/DependentOriginationC60KuuFourInputDoubleContextCoherenceV5_256.lean)
- [F103 — 観測五角形と一意性](formal/KUOS/DependentOriginationC60KuuObservedContextPentagonV5_257.lean)
- [F104 — 有限文脈Čech](formal/KUOS/DependentOriginationC60KuuFiniteContextCechDescentV5_258.lean)
- [F105 — 異なる物理パッチ間の荷電障害](formal/KUOS/DependentOriginationC60KuuPhysicalOverlapObstructionV5_259.lean)
- [F106 — 真正C60入射重なりと制限](formal/KUOS/DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260.lean)
- **[F107 — 原F42/F51の型付き語からのKuu意味論](formal/KUOS/DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261.lean)**
- **[F108 第1段階 — 物理面F42/F51文脈と非ゼロ位相](formal/KUOS/DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262.lean)**
- **[F108 第2段階 — 全60頂点の原Quiver.Pathと90物理辺の文脈](formal/KUOS/DependentOriginationC60KuuAllPhysicalSourcePathsV5_263.lean)**
- **[F108 第3段階 — 原F51非恒等3射による真正C60入射スター関手](formal/KUOS/DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264.lean)**

詳細な歴史・公理・未解決課題は **[ROADMAP.md](ROADMAP.md)** を参照してください。

## What remains open / 次の数学的課題

**F108第1〜第3段階は証明・統合済みで、面別の原構文整合性とF109以降はOPENです。** 第1段階では次数1の多角形面F42ラベルと元F43交換射由来の位相1の原F51射、第2段階では全60頂点間の原Quiver.Pathと90辺の文脈経路を構成しました。第3段階では、入射スターの**全Hom**上に、元F43交換射を実際に含む非恒等原F51関手を構成しました。ただし上位二面は選択した**一方の多角形面**由来の別々のF42水平合成表示を使います。両方の独立した隣接実多角形面を**各々の原F42境界で**保持し、その間の原F51/F55輸送や大域貼り合わせを実現する定理は未証明です。

次の研究軸は、各辺に実在する**二つの異なる隣接五角形・六角形面**から、それぞれの原F42閉路を正しく共通の開いた経路対へ輸送し、面ごとに異なる原F42ラベルと原F51交換3射を同時に整合させることです。その後に別物理パッチ間の荷電・位相・F55境界条件を比較します。成立しない場合は、次数不一致・位相・符号付きF55曲率をobstructionとして記録します。**全C60物理表面の無条件global glue、原F55の一般的な高次同値、無条件hyperdescentは未証明です。**

**Old Grayを復元することは本研究ルートの前提ではありません。** 元のGray位相はソース診断として保存し、空による交代可能性は**指定された商圏と正確な保存量**について証明します。

## Reasoning route and runtime boundary / 推論OSとの関係

`observation → context/presentation → multiple inference paths → typed transport → 2-/3-cell comparison → compatibility check → descent or obstruction → authority check → minimal action → re-observation`

研究上のランタイム構成案は **`LLM + KuuOS reasoning runtime + formal authority layer`** です。Leanの定理が正しいことは、モデルの重み・対話システム・バックグラウンドエージェントの挙動が変わったこと、全リポジトリが実際に取り込まれたこと、臨床的・物理的・倫理的正当性が検証されたことを意味しません。結合実装は、正本SHAへの固定、明示的な権限・同意境界、観測と推測の区別、継続的な実測・再検証を別途必要とします。

## Reproduce the F108 v5.264 theorem-bearing result / 形式証明の再現

```bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git
cd KuuOS
git checkout aefcb17f23c7f8f0e6627c49150001858f513d4f
cat lean-toolchain
lake exe cache get  # 必要な場合のみ、固定mathlibに対応するキャッシュを取得
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264
```

[PR #2286のexact-source-head CI #38642525139](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38642525139) は **9076/9076 SUCCESS**。追加ファイルのwarning/error 0/0、10件の`#print axioms`に`sorryAx`なし。Strict Lean・Governance・MCP Lean/CI完了証跡はすべて成功しました。第2段階の[PR #2284 / CI #38581217277](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38581217277)も**9075/9075 SUCCESS**、12件の公理監査済みです。

別の検証範囲である全形式化ターゲットや推論ランタイムを調べる場合は、それぞれ独立に実行してください（上記CIによる成功の保証はありません）。

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

参照 / References: [ROADMAP](ROADMAP.md) · [GOVERNANCE](GOVERNANCE.md) · [CITATION](CITATION.cff) · [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md)。

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
