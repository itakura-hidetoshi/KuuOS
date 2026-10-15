# KuuOS / 空OS

[![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml)
[![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml)
[![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml)

**KuuOS（空OS）** は、**空・縁起・関係・文脈・表現の交代可能性・高次圏論・obstruction-aware descent** を数学的に扱う研究体系です。Lean 4による形式化と、別途検証が必要なAI推論ランタイム研究の双方を含みます。

**研究・著作権者 / Founder and copyright holder:** **板倉英俊 / Hidetoshi Itakura**。ソースコード・文書のライセンスは [Apache License 2.0](LICENSE)（`Apache-2.0`）。[NOTICE](NOTICE)・[COPYRIGHT.md](COPYRIGHT.md)を参照してください。

> **空は、異なる原表示を無条件に同一視することではない。** 文脈と保存量を明確にしたうえで、交換可能な表現を証明し、合成・輸送・貼り合わせが不整合ならその障害を残す。

English: KuuOS is a research architecture for dependent origination, context-dependent presentations, exact categorical quotients, presentation replaceability, compositional coherence, and obstruction-preserving descent. The mathematical results are versioned Lean declarations; runtime use and empirical validity require independent evidence.

## Verified formal frontier / Lean4の現在の正本

**2026-10-16 JST GitHub MCP再確認：`v5.289 / F112` 第17段階までLean4で統合済み。** F112第6段階（v5.278）で真正F69/F106物理交差証人を保持する任意有限長の経路圏、原F42/F43/F54/F55四境界F47ソースCat値図式・Grothendieck総圏を構成し、第7段階（v5.279）で元のF69頂点・辺・面の**真正前向き入射射と形式的な逆向き射**を別圏の自由zigzagへ配置しました。第8段階（v5.280）では、**異なる実C60物理辺の共通F69サイトを保存した証人の反転**、任意有限長の物理交差経路の逆順・連結反転則・二重反転恒等性、および元F69入射zigzagの正確な**形式的逆向き経路**を実装。**元の証人付き自由経路は往復しても空経路にならない**一方、完全な二整数荷電と独立ZMod2位相を保存する原F47ソース圏の輸送は**両向きの往復で厳密な恒等関手**となり、全Homに型付き`HEq`を与えます。これは元F69入射射に真の逆射を追加したことでも、元のF42/F54原語を同一視したことでもありません。F55比較補正射`Δ=(0,1;phase0)`の九生成子non-lift、F110位相のF77からの非復元、F68北五角形第2荷電`−5`の曲率障害は残り、原F42/F54/F55の完全な大域的実効3-descentは未証明です。

**v5.282／F112第10段階（[数学PR #2318](https://github.com/itakura-hidetoshi/KuuOS/pull/2318)）**では、元F69半順序圏の`FreeGroupoid`とGabriel–Zisman局所化が普遍性によって圏同値となることを証明。原F69の前向き真正入射と形式的後向きにより生成された**F113のraw自由zigzagの局所化核**を`Functor.homRel`として定義し、mathlibの真の`Quotient`圏、厳密で一意な因子化、核の等式を忠実に保持する表現を構成しました。rawの二脚往復は非空ですが、この**指定した核商で初めて恒等**になります。

**v5.283／F112第11段階（[数学PR #2319](https://github.com/itakura-hidetoshi/KuuOS/pull/2319)）**では、固定mathlibの**実際の局所化生成子**（真正F69前向き射・その形式的逆向き射）からF113のraw zigzagへ復号する`Prefunctor`と`Paths.lift`を構成し、局所化の全Homが元の有限zigzagの像になる**充満性**を証明しました。さらに**本質的全射性**と第10段階の**忠実性**から、\(\operatorname{Zigzag}_{\mathrm{raw}}(F69)/\ker L\simeq F69[W^{-1}]\simeq\operatorname{FreeGroupoid}(F69)\) を**真の圏同値**としてLean4で証明。**元のraw zigzagそのものは同値と主張せず**、原F69入射圏を改変しません。F55 Δ non-lift、F110位相非復元、F68北五角形第2荷電`−5`、F42/F54/F55全ソース実効descent未証明を引き続き保持します。

**v5.284／F112第12段階（[数学PR #2321](https://github.com/itakura-hidetoshi/KuuOS/pull/2321)）**では、元F69で既存の**真正360個の頂点–辺–面入射二単体**と、元の前向き入射射で構成したF113 raw二脚zigzagを接続しました。実際の中間辺サイトを保持した**raw二脚経路と原直接対角射のraw一脚経路は長さ2と1で非同一**、しかし正確なF69 Gabriel–Zisman局所化とv5.283の忠実充満な**局所化核商**ではそれらの像が同じ射になることを証明。任意の**真正**F69中間サイトによる平行二脚spanも、局所化・核商で厳密整合します。これは**F69入射1圏／そのnerveの二単体関係**であり、元F42/F54/F55の真正Gray 2/3-cellのBeck–Chevalley整合性・大域実効descentを自動的に証明するものではありません。原F55 Δ non-lift、F110のF77位相非復元、F68北五角形の原第2荷電`−5`も残存します。

**v5.285／F112第13段階（[数学PR #2323](https://github.com/itakura-hidetoshi/KuuOS/pull/2323)）**では、全90実物理辺の各々において元の二つの異なる五／六角形面サイトを使うF108源文脈を構成し、元C60実Quiver.Pathで360物理フラグ頂点と辺端点を接続。独立した奇次数**原F42面2-cell**の二表示を比較する**原F47四境界ソース関手**を作り、旧F54/F55回転木を保持した**左・右Beck–Chevalley NatIso**と、**全F47三射の自然性**を証明しました。特に原F43面交換3-Hom／原F54/F55回転境界3-Homで自然性を個別検証し、二整数荷電と独立ZMod2位相を完全に保存。F69の全360真正入射二単体の局所化kernel等号と元raw経路の非同一、原F51位相1、元F55九生成子Deltaの**non-lift**、F68北五角形原荷電`−5`が**同時に保持**されることを証明しました。**境界：これは各真正F69フラグの同一物理辺に局所化された原F47ソースBCであり、全元F69頂点・面にF47繊維を与える大域図式や元F42/F54/F55有効3-descentは未証明**です。

**v5.286／F112第14段階（[数学PR #2325](https://github.com/itakura-hidetoshi/KuuOS/pull/2325)）**では、**相異なる真正C60物理辺**の交差証人`W : C60F112DistinctEdgeOverlap C i j`を必須とし、辺iで独立した原F42二面表示を変更後に実交差を越える経路と、実交差後に辺jで独立した原F42二面表示を変更する経路を、それぞれ**原F43/F54/F55由来の四境界付きF47ソース関手**として構成。**全F47三射で二整数荷電と独立ZMod2位相の完全保存**を証明し、二つの順序で得られるF47ソース関手の**厳密等式**、したがって関手圏の**Beck–Chevalley NatIso**を形式化しました。依存Homの`eqToHom`輸送を明示して等式を証明し、**全Hom自然性、原F43面交換射・元F54/F55回転射の自然性、混合四境界平方の保存**も証明。両方の原F42奇次数交換位相1、両辺の原F55九生成子Delta non-lift、F68北五角形の非ゼロ曲率荷電`−5`は同時に保持。**この二セルは真正F69交差でガードされた原F47混合ソース圏の関手圏2セル**です。全F69頂点／面の大域Cat値原F47繊維や元F42/F54/F55実効3-descent、F77からの原位相復元は主張しません。

**v5.287／F112第15段階（[数学PR #2327](https://github.com/itakura-hidetoshi/KuuOS/pull/2327)）**では、F278で構成した**真正F69物理交差証人付き任意有限長経路圏**の同一実C60文脈`C`上、各物理辺に独立に選んだ原奇次数F42二面ソース表示族`P,Q`について**完全Int×Int荷電＋独立ZMod2位相を保存する原F47四境界ソース変更関手**を構成。第14段階の真正異辺交差にガードされたCat Beck–Chevalley等式を各一歩で用い、経路帰納法により**任意有限長pathについて`L_i ⋙ T_Q(path) = T_P(path) ⋙ L_j`**を証明しました。これにより、二つの原F47 Cat値図式間の**真の自然変換**を構成し、任意経路連結との整合性を保証。さらに三つの独立表示族`P,Q,R`について、**全自然変換の厳密Čech三重cocycle、自己表示変更が恒等自然変換であること**をLean4で証明し、逆向き表示変更を明示した**Cat値図式全体の自然同型**`c60F121WitnessedF47DiagramSourceNatIso`へ到達しました。**この自然同型は証人付き交差経路圏の原F47混合商ソース図式の間に限る**もので、元F69全頂点・面の原F47繊維や、原F42/F54/F55 raw構文の同一化、無条件の大域実効3-descentを意味しません。元F55 Delta九生成子non-lift、F110位相非復元とF68北五角形原第2荷電`−5`は保持します。

**v5.288／F112第16段階（[数学PR #2329](https://github.com/itakura-hidetoshi/KuuOS/pull/2329)）**では、F278真正物理交差証人付き任意有限長経路圏上の原F47混合ソースCat値図式について、F121の**二つの独立した原F42面表示family間の自然同型**を固定mathlib `Grothendieck.map`で**真正な総圏関手**に持ち上げました。総圏の**全対象と全Homの実物理交差経路baseをそのまま保存**し、`Grothendieck.forget`との**厳密可換性**、同一表示の恒等functor、独立三表示`P,Q,R`間の**総圏全体の厳密Čech cocycle**を証明。逆表示変更と左右三角恒等式から**総圏のCat同型**と`Cat.equivOfIso`による**圏同値**をLeanで構成しました。元F47繊維でのInt×Int荷電と独立ZMod2位相を保持しつつ、**両表示における旧F55九生成子Delta non-lift、原F68北五角形第2荷電`−5`と非ゼロ曲率、未修復vertex gauge不能**を同時に証明。これは**真正な証人付き物理交差経路圏上の原F47混合商ソース総圏**についての結果であり、元F69全頂点・面の大域原F42/F54/F55三次stack／実効descentや元F113・原F42/F54 raw構文同一化を主張しません。

**v5.289／F112第17段階（[数学PR #2331](https://github.com/itakura-hidetoshi/KuuOS/pull/2331)）**では、既存F281で検証した**真正F69物理交差証人付き経路圏のmathlib Gabriel–Zisman局所化**と、v5.287で得た任意有限長の原F47表示変更**Cat値図式自然同型**を接続しました。F281の二つの原F47図式の**厳密局所化因子化**から必要な`Localization.Lifting`を型付きで構成し、固定mathlib `Localization.liftNatIso`によって二つの局所化後原F47図式間の**真の自然同型**を構成。これを`Grothendieck.map`で**局所化後の原F47混合ソース総圏**へ持ち上げ、**総圏の全対象と全Homの局所化済み物理経路baseが厳密に不変**、`Grothendieck.forget`と射影が厳密可換であることを証明しました。さらに`Grothendieck.pre_comp_map`を用い、元の**真正経路圏から局所化圏へのbase変更**と原F47表示変更が厳密に交換する定理を証明し、局所化総圏の**Cat同型と圏同値**を構成しました。原F55九生成子Δ non-lift、F110/F77位相非復元、F68北五角形の原第2荷電`−5`・非ゼロ曲率・未修復vertex gauge障害は保持されます。**元のF69入射半順序圏自体とは別の局所化**であり、原F69全頂点・面のF42/F54/F55大域3-stackやraw原構文実効descentを証明したものではありません。








**v5.281／F112第9段階（[数学PR #2316](https://github.com/itakura-hidetoshi/KuuOS/pull/2316)）**は、元のF69入射半順序圏そのものを変更せず、mathlibのGabriel–Zisman局所化 \(C_{F69}[W^{-1}]\) を構成して普遍因子化・一意性を証明しました。第7段階の真正F69前向き不等式／形式的逆向きによる**自由zigzagをこの局所化へ型付き関手で写し**、rawの反射的一歩が局所化後には恒等射に写ることを区別します。また、真正C60物理交差の**証人付き経路圏の別の局所化**において、完全なInt×Int整数荷電・独立ZMod2位相を保持する原F47 Cat値図式が全経路を同型に送ることと、その**厳密で一意な因子化**を証明。**自由zigzag自体が局所化と圏同値であること、F69全サイト上の原F47図式、原F42/F54/F55の大域実効descentは未主張**であり、F55 Δ non-lift、F110位相非復元、F68北五角形の第2荷電\(-5\)は保持します。

| 検証項目 | 最新の確認済み権威 |
| --- | --- |
| Repository / canonical branch | [`itakura-hidetoshi/KuuOS`](https://github.com/itakura-hidetoshi/KuuOS) / `main` |
| **最新 theorem-bearing PR** | **[PR #2331 — v5.289 F112第17段階, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2331)** |
| **Theorem-bearing merge SHA** | **`2bbaafaa58af64f939ee1d01db3b489e1cc897cd`**（PR #2331数学squashマージSHA、マージ直後canonical `main`との一致をGitHub MCPで確認済み） |
| Exact tested source HEAD | `a254bae035ccfc9660fd98317d02df41fe007318` |
| Exact-head proof CI | [GitHub Actions #38778674715](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38778674715) — **completed SUCCESS** |
| Strict Lean target | `KUOS.DependentOriginationC60KuuLocalizedWitnessedTotalSourceEquivalenceV5_289` — **9101/9101 jobs SUCCESS** |
| Governance / MCP | Strict Lean・Governance・MCP Lean completion・MCP CI completion **全SUCCESS** |
| Changed-file audit | **warning/error 0/0**、**10 `#print axioms`**、**`sorryAx`なし**（既存C60有限幾何`native_decide`依存は継承） |
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
| F75–F83、F94–F112（第11段階） | 実C60原F42/F51二面関手とF77商圏、全90物理辺での実有限交差上Čech自然同型、**物理交差の任意長履歴の厳密な経路独立性・閉路恒等性・制限前後の観測関手／自然変換成分の整合性**。F110の原位相非復元・原F68非平坦曲率の障害も保持 | F77観測後の整合性を原F42/F54/F55の無条件大域貼り合わせや原位相復元、非ゼロ原物理曲率の消去とみなすこと |
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
| **[F108 第4段階 / v5.265 / #2288](https://github.com/itakura-hidetoshi/KuuOS/pull/2288)** | 物理辺を挟む**異なる二つの実多角形面**の原F42生成子を、基点間の真正C60経路で共通開経路へ接続。両面を含む二つの水平合成語間の原F43/F51交換射は`charge=(0,0), phase=1`。全90物理辺の局所スター関手と両側の実入射三角形を構成。各面サイトへの独立F42対象割当ては未証明 |
| **[F109 第1段階 / v5.266 / #2289](https://github.com/itakura-hidetoshi/KuuOS/pull/2289)** | 二面原F51スター関手の**全Hom上の整数荷電ゼロ**と、任意の真正有限物理交差上の**二成分荷電差ゼロ**を証明。独立位相1は原構文に保持。二面F42合成の次数0を証明 |
| **[F109 第2段階 / v5.267 / #2290](https://github.com/itakura-hidetoshi/KuuOS/pull/2290)** | 上記のF42次数0から、全物理重なりでF77観測対象が同一の中性商対象になることを証明。F106の対象・荷電条件を実際に満たし、**真のNatIsoおよび厳密な3パッチČech cocycle**を構成（この特定の二面意味論について） |
| **[F110 第1段階 / v5.268 / #2292](https://github.com/itakura-hidetoshi/KuuOS/pull/2292)** | 実物理頂点→辺原F51射の位相1がF77観測後の**等式輸送射**に写ることを形式化。F109の真正F77物理Čech自然同型の追加荷電ゼロと、F68北五角形の原第2荷電`−5`・物理曲率非ゼロ・無補正頂点ゲージ不存在・必要な非ゼロ修復を同時に証明 |
| **[F110 第2段階 / v5.269 / #2293](https://github.com/itakura-hidetoshi/KuuOS/pull/2293)** | 原Gray圏の位相1生成子と恒等射は異なるがF77商では同じ。F77射から全原位相を回復する関数は存在せず、**`F77→GrayGrade`の左逆関手による完全な原Gray復元も不可能**。ただし追加ソースデータによる局所リフトは否定しない |
| **[F111 第1段階 / v5.270 / #2295](https://github.com/itakura-hidetoshi/KuuOS/pull/2295)** | パッチの真正有限物理交差への所属証明を持つ型付き中間履歴を導入し、**任意長のČech自然変換の経路独立性・閉路恒等性・追加整数荷電ゼロ・自然性・連結／分割整合性**を証明。全90辺の実C60へ特殊化 |
| **[F111 第2段階 / v5.271 / #2296](https://github.com/itakura-hidetoshi/KuuOS/pull/2296)** | F106の真正幾何学的制限(J⊆I)に対する**F77観測関手の対象／射／関手全体の一致**を証明。F109自然同型の成分と**異なる長さ・中間パッチ履歴の成分**が制限前後で一致し、追加荷電ゼロを保存。全90辺へ特殊化 |
| **[F111 第3段階 / v5.272 / #2297](https://github.com/itakura-hidetoshi/KuuOS/pull/2297)** | 真正C60有限物理交差の二段階包含`K⊆J⊆I`について、F106制限の対象・全Homの直接制限との一致、F109自然同型成分の二段階整合性、三つの集合で**それぞれ異なる任意長Čech履歴の二つの比較等式**、追加荷電ゼロを構成。全90実物理辺に特殊化。F77観測後の有限交差に限る |
| **[F112 第1段階 / v5.273 / #2300](https://github.com/itakura-hidetoshi/KuuOS/pull/2300)** | **任意有限長の型付き真正C60物理交差制限列**を帰納型として実装。原F106制限関手の全対象・射での端点直接制限への一致、列の連結、独立な二列・異なる任意長Čech履歴のF77観測射の異種等式`HEq`、高次cocycleと追加荷電ゼロ、全90実物理辺をLeanで確認。F110位相非復元を保存し、原F68北五角形荷電`−5`は独立のobstructionとして保持 |
| **[F112 第2段階 / v5.274 / #2302](https://github.com/itakura-hidetoshi/KuuOS/pull/2302)** | **二つの別々の実C60面サイトの独立した原F42境界型と奇次数を保存**。原F43/F51交換射の荷電`(0,0)`・位相`1`・非恒等性を示し、F77商ではじめて恒等射に潰れることを証明。別の原F54/F55回転境界付き物理旗標射の実現、任意長F112制限列の観測後整合性、原F68北五角形の第2荷電`−5`と無補正ゲージ不存在を同時に保持。ソース側全大域descentは未主張 |
| **[F112 第3段階 / v5.275 / #2304](https://github.com/itakura-hidetoshi/KuuOS/pull/2304)** | 二つの独立した実面サイトの任意の奇次数原F42二射と本物のF43交換射から、原F54回転境界・原F55物理旗標射を保持した**真正のF47四境界ソース枠**を構成。元のF43/F51完全Gray像の一致、F47混合圏の**可換四角形**、補正受信射`Δ=(0,1; phase 0)`の一意性、および元の九生成子F55の正確な型付き境界における**non-lift定理**を証明。全90物理辺へ特殊化。追加F47射を原F55に偽装せず、F68曲率`−5`は未解消 |
| **[F112 第4段階 / v5.276 / #2306](https://github.com/itakura-hidetoshi/KuuOS/pull/2306)** | 同一真正物理辺の独立原F42表示間で、原F43/F44・F54/F55完全Gray像の一致を供給し、原F47四境界**ソース表示変更関手**、全Hom二整数荷電＋位相保存・忠実性、三表示の`HEq` Čech整合性と原F42/F54左右Beck–Chevalley自然同型、F55 non-liftの継承を証明 |
| **[F112 第5段階 / v5.277 / #2308](https://github.com/itakura-hidetoshi/KuuOS/pull/2308)** | **異なる実C60物理辺の真正F69入射スター交差**を共有頂点・元五／六角形面の証人から構成。全Hom二整数荷電＋ZMod2位相を保存する**交差証人付き局所F47表示変更関手**・忠実性・可換四角形保存、三辺の実共通入射サイト上の`HEq` Čech整合性、元F55九生成子non-lift、F68北五角形原第2荷電`−5`を証明。大域F69→F47関手や実効ソースdescentは未証明 |
| **[F112 第6段階 / v5.278 / #2310](https://github.com/itakura-hidetoshi/KuuOS/pull/2310)** | **実F69入射交差証人付き任意有限長の真正C60物理辺の経路**を帰納型・Mathlib圏として構成。原F42/F54/F55混合四境界F47圏の全Hom荷電＋位相保存・忠実な輸送と、経路連結＝関手合成、任意二経路の**完全F47関手の一致**とHomの`HEq`をLeanで証明。Cat値経路図式・Grothendieck総圏を構成する一方、辺位置を保存して元F69入射圏に投影する関手の**NO-GO**を証明。原F55補正射non-liftとF68北五角形第2荷電`−5`は残存 |
| **[F112 第7段階 / v5.279 / #2312](https://github.com/itakura-hidetoshi/KuuOS/pull/2312)** | 元F69頂点・辺・面の**実在する向き付き入射射／形式的逆向き射**で生成した**別個の自由zigzag圏**を構成。真正F69/F106の二辺交差サイトを証人として**二脚zigzag**を作り、任意長の実交差証人付き経路から幾何学的zigzag圏への**Mathlib関手**を証明。原F47四境界ソースGrothendieck総圏をこの幾何学と関手で接続し、二整数荷電・位相保存を保持。元F69各サイトを固定するzigzag→元F69関手の**NO-GO**を証明。形式的逆向き射を元のF69射に捏造せず、原F55 non-lift／F68第2荷電`−5`／大域実効descent未証明を保持 |
| **[F112 第8段階 / v5.280 / #2314](https://github.com/itakura-hidetoshi/KuuOS/pull/2314)** | **異なる真正C60物理辺の実F69共通サイトを保持する交差証人の反転**と任意有限長の証人付き経路の反転・連結逆順・二重反転をLeanで構成。別の自由F69ジグザグの形式的逆向き操作も実装。**自由物理経路の往復は原証人を消去せず非空**だが、原F47四境界ソース関手の往復は左右とも**厳密な恒等関手**となり、全Homで`HEq`を証明。元F69への逆射追加・元F42/F54原語の等置・F68曲率の平坦化は未主張 |
| **[F112 第9段階 / v5.281 / #2316](https://github.com/itakura-hidetoshi/KuuOS/pull/2316)** | 元のF69入射圏の**真正なmathlib局所化**と局所化普遍性、自由F69 zigzagから局所化への型付き関手、自由原反射的一歩のnontrivial raw／局所化後恒等性を証明。独立した真正C60証人付き経路圏の全射を原F47 Cat図式が同型に送ることをF114左右逆で証明し、**一意な原F47 Cat因子化**を構成。完全二整数荷電とZMod2位相を保持する一方、raw構文同一化、全F69 Cat source gluing、F55 non-lift解除、F68曲率平坦化は未主張 |
| **[F112 第10段階 / v5.282 / #2318](https://github.com/itakura-hidetoshi/KuuOS/pull/2318)** | 元のF69の自由groupoid完成と真正局所化の**圏同値**、元F113 raw zigzagから局所化への表現関手の**厳密核`Functor.homRel`**によるmathlib商圏、厳密な普遍因子化・一意性・忠実性、真正元F69前向き射と形式的逆向き射のraw非空往復／核商後恒等性を証明。元raw構文は変更しない |
| **[F112 第11段階 / v5.283 / #2319](https://github.com/itakura-hidetoshi/KuuOS/pull/2319)** | mathlib元F69局所化の**全真正generator**からF113 raw zigzagへ復号する`Prefunctor`＋`Paths.lift`を構成。型付き局所化パス全体の関手恒等性、**Full／EssSurj**を証明し、F116で確立した忠実性と合わせて**raw自由zigzagの局所化核商と元F69局所化・元F69自由groupoid完成の圏同値**に到達。元rawの直接圏同値、原F42/F54/F55の全域Cat値実効descent、F68曲率の平坦化は未主張 |
| **[F112 第12段階 / v5.284 / #2321](https://github.com/itakura-hidetoshi/KuuOS/pull/2321)** | 元の360真正F69頂点→辺→面二単体を、F113のraw二脚経路と原対角一脚経路で具体化し、**raw二脚≠raw対角**（長さ2対1）、しかし**元F69局所化とv5.283の正確な局所化核商では両者一致**を証明。任意の実F69始終点を共有する並行二脚spanも局所化・核商で整合。元F69前向き射を改変せず、元F42/F54/F55高次Beck–ChevalleyやF68曲率消去は未主張 |
| **[F112 第13段階 / v5.285 / #2323](https://github.com/itakura-hidetoshi/KuuOS/pull/2323)** | すべての真正C60物理辺に実在する二つの原多角形面F42ソースを保持して、元の実Quiver.Pathを各360物理フラグ頂点へ接続。独立原F42奇次数面セルの間の原F47四境界比較関手で**左・右F58原F42/F54/F55 Beck–Chevalley NatIso**を実装し、全F47三射、原F43面交換、原F54/F55回転Homで自然性と完全Int×Int＋ZMod2保存を証明。全360入射二単体の核商整合とF51位相1、F55 Delta非lift、F68原曲率−5が同時に存在。**辺局所**であり、F69全サイトの大域原ソース3-descentは未主張 |
| **[F112 第14段階 / v5.286 / #2325](https://github.com/itakura-hidetoshi/KuuOS/pull/2325)** | **二つの相異なる実物理辺間の真正F69交差証人**をガードとし、原F42二面表示の辺内変更と原F47ソースの交差辺輸送の**二順序が厳密に同じF47ソース関手**になることを証明。Catの**Beck–Chevalley NatIso**、全原F47三射／元F43面交換／原F54/F55回転射の自然性、混合四境界図式保存、完全Int×Int＋ZMod2保存を形式化。両辺の旧F55 Delta non-lift・F68北荷電`−5`を保持。**交差ガードされたF47ソース関手圏2セルであり、原F69全域のF42/F54/F55大域実効descentではない** |
| **[F112 第15段階 / v5.287 / #2327](https://github.com/itakura-hidetoshi/KuuOS/pull/2327)** | F278の**真の物理交差証人付き任意有限経路圏**上、各辺の独立原F42二面表示族`P,Q`の間で完全Int×Int＋独立ZMod2位相付きF47ソース変更関手を構成。v5.286の各ステップ真正異辺交差BCから**任意有限長の経路に対する自然性と全Cat値F47図式間NatTrans**、経路連結との整合性を帰納法で証明。三表示族`P,Q,R`の**自然変換全体の厳密Čech cocycle、自己表示変更の単位則・明示的逆向き表示変更**から**F47ソース図式全体のNatIso**を構成。元F69入射全サイトの大域Cat値原F47図式や原F42/F54/F55実効3-descentは未主張 |
| **[F112 第16段階 / v5.288 / #2329](https://github.com/itakura-hidetoshi/KuuOS/pull/2329)** | 真正F69交差証人付き任意有限経路圏上の二つの原F47混合ソースCat図式間NatIsoを、mathlib Grothendieck.mapに通して**全対象・全Homの原物理経路base保存、projectionとの厳密可換性、総圏Functorsのself恒等／三表示Čech cocycle**を証明。さらに**二つの真正Grothendieck総圏のCat同型・圏同値**を構成。元F55 Delta non-lift（両表示）・F68曲率−5／未修復vertex gauge不能は継続。**F69全サイトを対象とする大域原F42/F54/F55実効3-descentは未主張** |
| **[F112 第17段階 / v5.289 / #2331](https://github.com/itakura-hidetoshi/KuuOS/pull/2331)** | 元F69入射圏と別の**真正証人付き経路圏の局所化**において、原F47図式の厳密因子化を用い、独立原F42表示族間のF121 NatIsoをmathlib **Localization.liftNatIso**で局所化後へ持ち上げた。原F47 Grothendieck**局所化総圏の対象・Homの局所化base保存と厳密射影可換性**、mathlib**Grothendieck.pre_comp_mapによる局所化前後のbase変更／原ソース表示変更の厳密可換性**、局所化総圏の**Cat同型・圏同値**を証明。原F55 Delta non-lift、F68原曲率−5・未修復vertex gauge不能は保持。元F69全頂点/面の原F42/F54/F55実効3-descentは未主張 |

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
- **[F108 第4段階 — 二つの実隣接面の原F42/F51交換](formal/KUOS/DependentOriginationC60KuuTwoActualFaceInterchangeV5_265.lean)**
- **[F109 第1段階 — 真正C60物理重なりの整数荷電差ゼロ](formal/KUOS/DependentOriginationC60KuuTwoFacePhysicalOverlapCompatibilityV5_266.lean)**
- **[F109 第2段階 — F77観測対象の一致とČech整合性](formal/KUOS/DependentOriginationC60KuuTwoFaceObservedObjectCechV5_267.lean)**
- **[F110 第1段階 — F77入射射・原F51位相・F68非平坦曲率の同時証明](formal/KUOS/DependentOriginationC60KuuObservedGluingOriginalPhaseCurvatureV5_268.lean)**
- **[F110 第2段階 — F77からの完全位相復元関手の不存在](formal/KUOS/DependentOriginationC60KuuPhaseReconstructionObstructionV5_269.lean)**
- **[F111 第1段階 — 真正物理交差の任意長Čech歴史と閉路恒等性](formal/KUOS/DependentOriginationC60KuuActualPhysicalFiniteCechHistoriesV5_270.lean)**
- **[F111 第2段階 — 物理交差制限に沿った観測関手・Čech歴史の整合性](formal/KUOS/DependentOriginationC60KuuActualPhysicalRefinementCechV5_271.lean)**
- **[F111 第3段階 — 二段階物理制限と任意長Čech歴史の高次整合性](formal/KUOS/DependentOriginationC60KuuDoublePhysicalRefinementCechV5_272.lean)**
- **[F112 第1段階 — 任意有限長の真正C60物理制限列と高次Čech輸送](formal/KUOS/DependentOriginationC60KuuArbitraryPhysicalRefinementTowersV5_273.lean)**
- **[F112 第2段階 — 原F42別々の実面サイト・F51位相・F54/F55物理境界の同時保持](formal/KUOS/DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274.lean)**
- **[F112 第3段階 — 独立F42面ソースから型付きF47四境界混合圏への実構成・一意補正とnon-lift](formal/KUOS/DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275.lean)**
- **[F112 第4段階 — 同一C60実物理辺の原F47ソース表示変更・全Hom Čech異種等式・左右Beck–Chevalley](formal/KUOS/DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276.lean)**
- **[F112 第5段階 — 異なる実C60物理辺のF69交差証人・原F47局所表示変更・三辺共通サイトČech](formal/KUOS/DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277.lean)**
- **[F112 第6段階 — 実交差証人付き任意有限経路圏・原F47 Cat値関手とGrothendieck総圏](formal/KUOS/DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278.lean)**
- **[F112 第7段階 — 真正F69入射zigzag圏・二脚実交差構成・F47 Grothendieckとの幾何学的接続](formal/KUOS/DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279.lean)**
- **[F112 第8段階 — 真正C60交差経路反転・元F69自由zigzag形式逆・完全位相付き原F47往復恒等性](formal/KUOS/DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280.lean)**
- **[F112 第9段階 — 元F69入射の真正局所化普遍性・自由zigzagの型付き解釈・完全位相付きF47 Cat図式の一意な局所化因子化](formal/KUOS/DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281.lean)**
- **[F112 第10段階 — 元F69自由groupoid完成の普遍同値・F113生zigzag局所化核の正確なmathlib商圏](formal/KUOS/DependentOriginationC60KuuF69ZigzagKernelQuotientFreeGroupoidV5_282.lean)**
- **[F112 第11段階 — 実局所化生成子の復号・raw zigzagの充満性／本質的全射性・核商≃局所化≃自由groupoid圏同値](formal/KUOS/DependentOriginationC60KuuF69RawZigzagQuotientLocalizationEquivalenceV5_283.lean)**
- **[F112 第12段階 — 真正C60/F69の全360非退化入射二単体、raw二脚と原対角の非同一、局所化・核商での二単体/平行span整合性](formal/KUOS/DependentOriginationC60KuuOriginalFlagTwoSimplexZigzagDescentV5_284.lean)**
- **[F112 第13段階 — 真正C60物理フラグに固定した独立原F42/F54/F55四境界ソース、左右F58 Beck–Chevalley自然同型と全三射自然性・非lift／曲率障害](formal/KUOS/DependentOriginationC60KuuPhysicalFlagOriginalSourceBeckChevalleyV5_285.lean)**
- **[F112 第14段階 — 真正異辺物理交差にガードされた原F42表示変更と原F47輸送の厳密可換性・Cat Beck–Chevalley自然同型・混合四境界／曲率障害](formal/KUOS/DependentOriginationC60KuuCrossEdgeOriginalSourceBeckChevalleyV5_286.lean)**
- **[F112 第15段階 — 任意有限長の真正F69交差経路上の原F47図式間自然性・三重Čech cocycleと完全位相付きCat値図式自然同型](formal/KUOS/DependentOriginationC60KuuWitnessedSourceDiagramBeckChevalleyV5_287.lean)**
- **[F112 第16段階 — 真正物理交差経路上の独立原F42表示間Grothendieck総圏同型・圏同値、射影可換性・全経路保持・三重Čech cocycle・F55／F68障害](formal/KUOS/DependentOriginationC60KuuWitnessedGrothendieckSourceEquivalenceV5_288.lean)**
- **[F112 第17段階 — 真正F69物理交差経路のGabriel–Zisman局所化へ原F47ソース自然同型を持ち上げ、総圏のCat同型／圏同値・局所化base射影・base変更Beck–Chevalley可換性を検証](formal/KUOS/DependentOriginationC60KuuLocalizedWitnessedTotalSourceEquivalenceV5_289.lean)**

詳細な歴史・公理・未解決課題は **[ROADMAP.md](ROADMAP.md)** を参照してください。

## What remains open / 次の数学的課題

**F108第1〜第4段階、F109第1〜第2段階、F110第1〜第2段階、F111第1〜第3段階、F112第1〜第17段階をLean4で証明・マージ済みです。** F112第6段階で真正C60物理交差証人付きの任意有限長経路圏と完全Gray値を保存するF47四境界ソースGrothendieck総圏、第7段階で元F69実入射に沿った別の自由zigzag圏への幾何学的関手を構成しました。**第8段階は経路反転を幾何学の証人レベルまで構成し、経路往復が自由経路の等式としては非自明な一方、原F47ソース圏の完全荷電＋位相付き関手としては厳密に恒等になる**ことを証明。元F69の逆射を捏造しておらず、元F55 non-lift・F68北五角形の第2荷電`−5`は保存されています。大域的原F42/F54/F55実効descentは未証明です。 **第9段階v5.281は二つの局所化を分け、元F69入射射を反転させる局所化の普遍性と、元F47 Cat図式が証人付き経路圏の局所化を通る一意因子化を証明しました。** **第10〜11段階v5.282〜283では、真のF69局所化と元F69自由groupoidの普遍同値、F113のraw入射zigzagの正確な局所化核商、その局所化との充満・忠実・本質的全射を満たす圏同値を統合しました。** **第12段階v5.284では全360真正F69物理入射二単体のraw経路非同一と局所化・核商後の厳密二単体／平行span整合性を証明しました。** **第13段階v5.285では各360真正物理フラグに固定された原F47ソースの左右Beck–Chevalley自然同型を原F43/F55も含む全Homで検証しました。** **第14段階v5.286は、原F47辺内表示変更と真正異辺物理交差による再索引の二順序について完全位相付き関手等式・自然同型を証明しました。** **第15段階v5.287では、真正物理交差証人付き任意有限長経路圏の原F47 Cat値図式間で、表示変更の自然変換・三重cocycle・明示的逆向きによる自然同型まで証明しました。** **第16段階v5.288では完全位相付き原F47表示変更の自然同型を、同じ実物理経路baseを保存するGrothendieck総圏の圏同値へ昇格しました。** **第17段階v5.289では、証人付き物理交差圏の局所化にF47図式自然同型を持ち上げ、その局所化総圏のCat同型・圏同値とbase変更の厳密可換性を証明しました。**

**次の未解決研究軸は、F112第18段階以降の**F69全60頂点・90辺・32原面へ原F42/F54/F55の実際の繊維と制限関手を与える場合の**条件付き**源descent、原F68非ゼロ曲率に整合する補正cochainと有効貼り合わせの必要十分条件**です。v5.289の局所化baseは**元のF69入射半順序圏ではなく、実F69サイトの交差証人付き経路圏**です。局所化後の原F47 mixed native-kernel総圏同値から、元raw F42/F54/F55の高次3-stack実効性や各物理面・頂点への大域繊維を推論することはできません。F113 raw往復の非空、F55 Delta九生成子non-lift、F77原位相非復元、F68北原第2荷電`−5`と未修復vertex gauge不能は独立障害として維持します。

**Old Grayを復元することは本研究ルートの前提ではありません。** 元のGray位相はソース診断として保存し、空による交代可能性は**指定された商圏と正確な保存量**について証明します。

## Reasoning route and runtime boundary / 推論OSとの関係

`observation → context/presentation → multiple inference paths → typed transport → 2-/3-cell comparison → compatibility check → descent or obstruction → authority check → minimal action → re-observation`

研究上のランタイム構成案は **`LLM + KuuOS reasoning runtime + formal authority layer`** です。Leanの定理が正しいことは、モデルの重み・対話システム・バックグラウンドエージェントの挙動が変わったこと、全リポジトリが実際に取り込まれたこと、臨床的・物理的・倫理的正当性が検証されたことを意味しません。結合実装は、正本SHAへの固定、明示的な権限・同意境界、観測と推測の区別、継続的な実測・再検証を別途必要とします。

## Reproduce the F112 v5.289 theorem-bearing result / 形式証明の再現

```bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git
cd KuuOS
git checkout 2bbaafaa58af64f939ee1d01db3b489e1cc897cd
cat lean-toolchain
lake exe cache get  # 必要な場合のみ、固定mathlibに対応するキャッシュを取得
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationC60KuuLocalizedWitnessedTotalSourceEquivalenceV5_289
```

[PR #2331のexact-source-head CI #38778674715](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38778674715) は **9101/9101 SUCCESS**。変更Leanファイルwarning/error 0/0、10件の`#print axioms`に`sorryAx`なし。Strict Lean・Governance・MCP Lean/CI完了証跡は全SUCCESS。検証済みsource HEAD `a254bae035ccfc9660fd98317d02df41fe007318`、数学squashマージSHA `2bbaafaa58af64f939ee1d01db3b489e1cc897cd`。前段階第16段階[PR #2329](https://github.com/itakura-hidetoshi/KuuOS/pull/2329)の[CI #38747866204](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38747866204)も**9100/9100 SUCCESS**、9件の`#print axioms`で`sorryAx`なし。F112第1〜16段階の定理はexact-head GREEN・マージ済みです。

別の検証範囲である全形式化ターゲットや推論ランタイムを調べる場合は、それぞれ独立に実行してください（上記CIによる成功の保証はありません）。

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

参照 / References: [ROADMAP](ROADMAP.md) · [GOVERNANCE](GOVERNANCE.md) · [CITATION](CITATION.cff) · [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md)。

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
