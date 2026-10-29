# KuuOS / 空OS — Formal Research Roadmap

**更新：2026-10-29 JST。最新のLean統合段階は F112-P94D3FQ / [PR #2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692) MERGED。** 定理squash SHA `09c3150dbfb59f92167e8840575f0053c3dae71c`（当時のcanonical main HEAD）。exact-source-head [Strict Lean #40872152257](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40872152257) **9033 scoped jobs SUCCESS**、Governance **30/30 completed・失敗0**。FQで監査した13宣言の依存公理は`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし。FO [#2689](https://github.com/itakura-hidetoshi/KuuOS/pull/2689)は全コード衝突差語の正規閉包＝全核、FP [#2690](https://github.com/itakura-hidetoshi/KuuOS/pull/2690)は正規商≃実輸送像と受信器の像上の一意因子化。FQは全衝突生成族を**同一受信コードファイバーの1代表元への根付き関係族**に縮約し、真正18D完全コード衝突を**元のassoc/post/pre構成子の同種セクター3族**へ分解、原の非可換群で全核＝3族和集合の正規閉包、各セクター内の受信器一致 iff 像上の一意因子化を証明。非全射・空ソースにも汎用根付き定理は成立。有限・最小正規生成や単一FJ欠損による全核生成、真正19D幾何充填は未証明。旧FJ非忠実性とFK–FM別presentation忠実性、DS、107公開root、独立Kuu/strict空、Gray非再導入を保持。次はF112-P94D3FR（仮称）。

<details>
<summary>旧更新記録：2026-10-23 / F112-P91B（歴史的な検証receipt。現在の最終段階ではない）</summary>

**更新：2026-10-23 JST。F112-P91B [#2482](https://github.com/itakura-hidetoshi/KuuOS/pull/2482)までmain統合済み。P91Aで元F55全九構成子のF54原始回転数差＝五角形電荷を証明し、P90自然性比較証拠が存在する場合の五角形電荷0と奇位相parityを必要条件として確定。P91Bで原F55証拠存在exact kernelの別F54経路商、旧P67 square-only商からの全射、五角形3対2回転の同一視による回転数非降下を証明。**P90自然性比較slotのinhabitantと水平結合律・higher coherenceは未証明**。C60以前の縁起一般理論、107公開root、旧P87/P88 no-go、新P89 interchange、C60 odd phaseを保持。**

</details>

> **一般理論 → C60による具体的検証 → 一般理論の改善・strict高次化 → (∞,3)-hyperdescent。**
> 
> C60は縁起の一般化の起点ではない。独立Kuuも一つのpresentationであり、strict 3圏を証明できたとしても唯一の「空」ではない。定理の型・仮定・obstructionを失わず、一般化の数学的根拠を段階的に増やす。

この文書は[README](README.md)を補い、**検証済みの一般的定理／後から導入したC60の個別定理／条件付きの帰結／未証明の到達目標**を分離します。過去の定理を「C60研究の前準備」として書き換えたり、Gray非依存化のために既存成果を廃止したりしません。

## 0. 正本・依存・証明の判定

| 区分 | 正確な位置づけ |
| --- | --- |
| 公開統合正本 | [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。歴史的`formal/KUOS/`と現行`formal/Kuu/`、Qiを**同一Leanパッケージ**に含む。 |
| 独立Kuu F112研究 | [親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)は**MERGED**。かつての`formal/v5-293-f112-independent-total-change`は移行作業の履歴であり、現在の正本はmain。 |
| 現在のF112検証範囲（2026-10-29） | **P94D3FQ [#2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692)までmain統合済み。** 定理SHA `09c3150dbfb59f92167e8840575f0053c3dae71c`、Strict Lean **9033 scoped jobs SUCCESS**、Governance **30/30 jobs completed・失敗0**、FQ新規13宣言は標準3公理のみ／`sorryAx`なし。元完全18D輸送の全核は、全コード衝突差語（FO）・その根付き差語（FQ）・3セクター内衝突差語の和集合（FQ）のいずれでも厳密に正規生成され、商≃実輸送像・像上受信器一意性（FP/FQ）を保つ。FJ旧輸送は非空有限文脈非単射、FK–FM別輸送は全有限文脈単射。 |
| F112以前の確認範囲（2026-10-23時点の履歴） | **P91Bまでmain統合済み（当時）**。P89B：9702/9702・13/13公理監査、P90A：9703/9703・7/7、P90B：9704/9704・7/7、**P91A：9705/9705・4/4**、**P91B：9706/9706・13/13**。新規`sorryAx`なし、変更ファイルLeanエラー/警告0、107公開root保全、exact-head Governanceとcompletion receipts 2/2 SUCCESS。P91A統合SHA `153361ebc9bf4303ed9c79e931c768fc99a885af`、P91B統合SHA `8fd61aad78943f6c9c630a585450eac2b5246f90`。唯一の公開入口`KuuOSFormal`に両モジュールを直接import。 |
| 既存定理の証拠 | 実際のLean宣言・型と仮定・`#print axioms`・対応するexact-head CI。`sorryAx`、`sorry`、`admit`、新たな未証明公理による補完は禁止。 |
| 数学的区別 | raw Type-valued証拠、Prop証明、選択した商、観測、物理的解釈は互いに無条件には同一視しない。 |
| 公開入口・toolchain | `lake build KuuOSFormal`（`lake build`も同じ）。既存107公開rootは維持。Lean `v4.30.0-rc2`、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。 |
| 別レーン | PR #1558（Lean 4.31）はvalidation-only、Draft・未マージ。Lean/mathlibの正式な固定環境は上記のまま。 |

GitHub正本・Lean成果・README/ROADMAP・CI・歴史的スナップショットには異なる役割がある。**P94D3FQまでのmain統合はGitHub上のMERGED commitで、当該Lean定理のPR exact-source-head CIを独立確認済み**。FP（9032 scoped jobs）、FO（9956/9956）、FN（9955/9955）およびP91B・FI–FMの数値は各時点の独立receiptとして保持。文書はLean定理の代替ではなく、C60以前の縁起一般化成果も維持する。

## 0A. 2026-10-29現在の証明フロンティア：EX–FQ

**研究の主題：** 元の14D–18D依存型・非可換証拠を保存し、実際のC60有限AQ文脈での17D輸送 `C_w`、完全18Dコード写像 `f_w`、非可換自由群準同型 `τ_w` の**単射性・核・obstruction・相対商への降下**を区別して形式化する。C60は縁起の一般理論を取り替える唯一のモデルではない。現段階の18D生成子・19D候補は、元の幾何的19D充填や大域strict 3圏の完成証明ではない。

### 0A.1 検証済みの成果（すべてcanonical mainにMERGED）

| F112段階 / PR | 主要なLean証明・構成 | 未証明の境界または必要な仮定 |
| --- | --- | --- |
| EX / [#2663](https://github.com/itakura-hidetoshi/KuuOS/pull/2663) | 完全18D非可換pentagon欠損の前置・符号付き生成子・後置への順序保持因子化 | 未定義の幾何的19D fillerへ飛躍しない |
| EY / [#2664](https://github.com/itakura-hidetoshi/KuuOS/pull/2664) | 有限符号付き19D**候補**経路の全欠損積、正規閉包、相対商への降下 | 全体欠損の商零化と生成子ごとの零化は別条件 |
| EZ / [#2665](https://github.com/itakura-hidetoshi/KuuOS/pull/2665) | 非可換ゲージ共役での正規閉包不変性、文脈拡張、降下条件 | 商による正規化を元のType値証拠の同一視としない |
| FA / [#2666](https://github.com/itakura-hidetoshi/KuuOS/pull/2666) | 実際のDV完全18D文脈輸送と19D候補経路の生成子別障害 | 形式的な候補を元のC60で存在する19D証拠としない |
| FB / [#2667](https://github.com/itakura-hidetoshi/KuuOS/pull/2667) | 真正pentagon完全自由群証拠はDV輸送後も非自明。明示的に選んだDX相対商では像が零 | 元の非零と選択商での零を混同しない |
| FC / [#2668](https://github.com/itakura-hidetoshi/KuuOS/pull/2668) | 完全依存型コード写像の単射性と自由群輸送の単射性の同値。非自明自由群核と異なる元コードの同一輸送像との同値 | DV全体の無条件単射性を主張しない |
| FD / [#2669](https://github.com/itakura-hidetoshi/KuuOS/pull/2669) | 異なる元17D対象が同じ実文脈像を持てば、元の反射的18D associatorコード衝突と非自明な2文字核を構成 | 任意のC60 frameに衝突があるとは仮定しない |
| FE / [#2670](https://github.com/itakura-hidetoshi/KuuOS/pull/2670) | 反射的associatorコード族の衝突と17D文脈対象衝突の必要十分条件。任意有限文脈対象作用の単射性は2つの単独frameの`mapTotal`単射性と同値。`onObj`・依存型`onCell`単射性はその十分条件 | 2つのframeが実際に単射であることは未証明 |
| FF / [#2671](https://github.com/itakura-hidetoshi/KuuOS/pull/2671) | 実17D文脈対象作用の単射性を仮定すると、原raw17Dのatom/refl/symm/trans全構成子の等式反映、元18D対象の両端点・raw17D履歴を含む単射性。空文脈の18D対象単射性は無条件 | 18D**対象**から18D**生成子**全体の単射性は従わない |
| FG / [#2672](https://github.com/itakura-hidetoshi/KuuOS/pull/2672) | 実DV輸送は18Dの`assoc/post/pre`構成子タグを無条件に保存。異セクター間の完全コード衝突と2文字核を排除。全コード・非可換自由群輸送の単射性は3セクター各々の忠実性と同値。17D文脈作用の単射性を仮定すると、元`assoc`3経路と、固定内側生成子の`pre/post`経路引数の単射性を証明 | 変動する内側18D生成子の再帰的反映と各セクターの忠実性成立は未証明 |
| FH / [#2674](https://github.com/itakura-hidetoshi/KuuOS/pull/2674) | 元のraw17D外側`pre/post`経路と可変内側18D生成子を同時に扱い、17D文脈対象作用と元の固定内側ファイバーの単射性を仮定した共同反映。Strict Lean 9948/9948 SUCCESS | 仮定の全C60文脈での充足は未証明 |
| FI / [#2675](https://github.com/itakura-hidetoshi/KuuOS/pull/2675) | 全入れ子`post/pre`→終端`assoc`の構成子列・深さを任意有限AQ文脈で無条件保存。非可換自由群の構成子列準同型の自然性および $\ker(\tau_w)\subseteq\ker(S_{\mathrm{orig}})$ を証明。Strict Lean 9949/9949 SUCCESS | 同一構成子列のraw17D引数復元や全核分類は未証明 |
| FI 完全反映 / [#2676](https://github.com/itakura-hidetoshi/KuuOS/pull/2676) | `assoc/post/pre`全依存型生成子に対する帰納法により、可変の内側18D生成子・raw17D両端点・途中境界を等式反映。任意有限文脈で `Injective(f_w) ↔ Injective(C_w) ↔ Injective(τ_w)`、空語は無条件単射、全有限語条件は2 singleton `mapTotal`の単射性と同値。9950/9950 SUCCESS | FI自体は具体的frameの成否を仮定しない。FJ旧frameは非空語で非単射、FM新frameは全有限語で単射。幾何19D充填と旧全核正規生成表示は未証明 |
| FJ / [#2679](https://github.com/itakura-hidetoshi/KuuOS/pull/2679) | 真正C60 `nativeK5AQWhiskerCell` は、元15D `conservative(refl R)` と `conservative(atom rfl rfl)` の**異なるType値証拠**を同一の保守的atomへ送る。proof-bearing base AX Total、元raw16D identityを含む17D singletonを経由し、全**非空**有限物理AQ文脈で非単射。抽象FIを使い、選択物理モデルで `Injective(τ_w) ↔ w=[]`。**同一の非自明2文字元z**が全非空wで`τ_w(z)=1`。9951/9951 SUCCESS | 元14D幾何的whiskering単独の非単射性、任意抽象frameでの非単射性、全kernel正規生成表示、元の19D Type値幾何充填は主張しない |
| FK / [#2681](https://github.com/itakura-hidetoshi/KuuOS/pull/2681) | 既存`nativeK5AQWhiskerCell`を上書きせず、同じ14D幾何作用上の別の保守的15D構成子保存whiskeringとAX frameを構成。元14D左右raw whiskeringの単射性、新旧frameの`onObj`一致、FJの元15D`refl/atom`証拠の新輸送での区別を証明。全依存型raw15D経路hについて**`old(h)=forget(new(h))`**、逆の後処理復元不能性、全有限語で新輸送はFJ証拠を区別し非空語で旧輸送は衝突することを証明。9952/9952 SUCCESS | FK段階では全Hom単射性未証明だったが、後続FLで解決。FK当時未証明だった新17D/18D忠実性は後続FMで解決。元のFJの障害、DS no-go、19D幾何充填や全核の分類は不変 |
| FL / [#2683](https://github.com/itakura-hidetoshi/KuuOS/pull/2683) | 保守的core`refl/atom/symm/trans`、独立exchange添字、外側`symm/trans`を元14D依存境界ごと等式反映。可変中間14Dを`Sigma`で復元し、exchange添字は`Option`射影と`HEq`で復元。FKの別15D輸送は全Homファイバー・全有限AQ語・新frame `onCell`で単射。9953/9953 SUCCESS | 当時未証明だった全`mapTotal`・17D文脈・18D自由群忠実性は後続FMで別frameについて証明済み。元FJ非単射性は保持 |
| FM / [#2685](https://github.com/itakura-hidetoshi/KuuOS/pull/2685) | 新15D `onObj/onCell`から元AX `mapTotal`単射性を導出。真の16D raw `atom/refl/symm/trans`の全構成子等式反映は、元generator provenanceの単射性と可変中間15D Type値の`Sigma`反映による。17D真正singletonと全有限文脈の単射性を証明し、FIの同値から新18D完全コード・非可換自由群輸送の全有限AQ語単射性と自明核を証明。9954/9954 SUCCESS | FJ旧輸送の非単射性・旧全核分類未解決は保持。新旧高次証拠を比較する自然な射、元の幾何19D充填、全strict n圏・hyperdescentは未証明 |
| FN / [#2687](https://github.com/itakura-hidetoshi/KuuOS/pull/2687) | 元14D依存境界を保持する完全15D AX Totalの構成子忘却写像を定義し、冪等・非単射・各frameと全有限語の忘却自然性・非空有限語の厳密`old=forget∘new`因子化を証明。旧新の別17D identity／18D assoc-refl完全コードの元同一15D証拠ペアについて、旧非空語の衝突・新全語の分離、旧受信18Dコードからの新受信両像の後処理復元不能、旧2文字欠損の共通核・新2文字欠損の全有限語生存を証明。9955/9955 SUCCESS | 別旧新高次signatureの全生成子をつなぐ比較関手は未構成。旧全kernel正規生成・元幾何19D充填・大域strict 3/n・hyperdescentは未証明 |
| FO / [#2689](https://github.com/itakura-hidetoshi/KuuOS/pull/2689) | 任意の文字写像 `f:A→B` に対し `ker(FreeGroup.map f)` は `f(a)=f(b)` の全衝突差語 `[a][b]⁻¹` の正規閉包と**厳密に等しい**。元の完全依存18D DV輸送へ移し、核所属条件・2語像一致 iff 差語所属・受信器降下 iff 全コード衝突で一致を証明。旧FJ全非空文脈の全核非自明と別FK/FL/FM全有限文脈の全核自明を保持。9956/9956 Strict Lean SUCCESS、11新規定理 | 単一の既知FJ欠損で全核を正規生成するとは言えず、衝突族の有限性・最小性、19D幾何充填も未証明 |
| FP / [#2690](https://github.com/itakura-hidetoshi/KuuOS/pull/2690) | FOの全衝突正規閉包による商群と元の実DV輸送の**像部分群**との第一同型定理、商代表元の輸送像一致、全衝突での受信器一致 iff 実像上の**一意な因子化**を証明。全射なら全標的拡張が一意、非全射 `Empty→Bool` では標的全体への拡張が非一意となる反例を証明。独立FJ/FK/FL/FMの核境界を再確認。PR #2690 exact-head Strict Lean 9032 scoped jobs SUCCESS、11宣言の公理監査、Governance 30/30 SUCCESS | 正規商の同型先は**実際の像**であり標的全体ではない。無条件の全射性・有限/最小正規生成集合・真正19D Type値幾何充填は主張しない |
| FQ / [#2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692) | 任意 `f:A→B` について**実際の像各ファイバーから元source文字代表元を選び**、元の全コード衝突差語の正規閉包＝各 `a` と代表元 `r_f(a)` の2文字差語の正規閉包を証明。真正C60完全18DではFGの構成子タグ輸送を使い、全衝突対は3つの元`assoc/post/pre`同一セクター内で完全に分類され、3族和集合の正規閉包＝元DV全核。根付き根のタグ保存、根付き商≃真正輸送像、セクター内3受信器一致 iff 実像上の一意な因子化を証明。9033 scoped Strict Lean SUCCESS、13宣言公理監査、Governance SUCCESS | 根代表元は選択的・非構成的。1関係/元source文字という表示は、有限・独立・最小正規生成や全標的の同型／一意性を意味しない。再帰的内側生成子のセクター内部分類、単一FJ欠損の全核生成、元の真正19D幾何充填は未証明 |

主な正本Leanソース：

- [FC: CompleteCodeFiberKernel](formal/Kuu/F112/PolygonNativeC60AQFullPentagonCodeFiberKernel.lean)、[FD: SeventeenContextFiberObstruction](formal/Kuu/F112/PolygonNativeC60AQFullPentagonSeventeenContextFiberObstruction.lean)、[FE: SeventeenExactFiberGate](formal/Kuu/F112/PolygonNativeC60AQFullPentagonSeventeenExactFiberGate.lean)。
- [FF: RawSeventeenPathReflection](formal/Kuu/F112/PolygonNativeC60AQFullPentagonRawSeventeenPathReflection.lean)、[FF: EighteenObjectReflectionGate](formal/Kuu/F112/PolygonNativeC60AQFullPentagonEighteenObjectReflectionGate.lean)。
- [FH: RecursiveGeneratorReflection](formal/Kuu/F112/PolygonNativeC60AQFullPentagonRecursiveGeneratorReflection.lean)、[FI: DeepConstructorSpineObstruction](formal/Kuu/F112/PolygonNativeC60AQFullPentagonDeepConstructorSpineObstruction.lean)。
- [FJ: PhysicalWhiskerNoninjectivity](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalWhiskerNoninjectivity.lean) — 実物理AQ `conservative(refl/atom)` 構文衝突、全非空有限文脈での非単射性、共通の非自明2文字欠損。
- [FK: ConstructorPreservingWhisker](formal/Kuu/F112/PolygonNativeC60AQFullPentagonConstructorPreservingWhisker.lean) — 14D境界一致の別15D輸送、原保守的構成子履歴の保存、旧輸送への厳密忘却因子化、有限文脈でのFJ証拠分離。
- [FL: FullDependentWhiskerReflection](formal/Kuu/F112/PolygonNativeC60AQFullPentagonFullDependentWhiskerReflection.lean) — 保守的4構成子・独立exchange・外側2構成子の全依存型Hom等式反映、可変中間14D Sigma復元、任意有限文脈と代替frame onCell単射性。
- [FM: AlternativeFullFaithfulness](formal/Kuu/F112/PolygonNativeC60AQFullPentagonAlternativeFullFaithfulness.lean) — 真正15D `mapTotal`・全有限AQ文脈、17D閉包raw16D証拠の全構成子反映、元18D完全コード・非可換自由群輸送の全有限語単射性、自明核。
- [FN: OldNewTypedFaithfulnessComparison](formal/Kuu/F112/PolygonNativeC60AQFullPentagonOldNewTypedFaithfulnessComparison.lean) — 全15D構成子忘却の冪等性／自然性／非空語因子化、新旧別17D・18D選択Type値証拠ペアの衝突対照・復元不能、旧／新非可換欠損の消失／生存。
- [FO: CompleteKernelNormalClosure](formal/Kuu/F112/PolygonNativeC60AQFullPentagonCompleteKernelNormalClosure.lean) — 任意FreeGroup.mapの全コード衝突差語正規閉包による全核等式、真正18Dの非可換核判定・受信器降下条件・FJ旧核とFK/FM別核の厳密比較。
- [FP: CompleteKernelImageFirstIsomorphism](formal/Kuu/F112/PolygonNativeC60AQFullPentagonCompleteKernelImageFirstIsomorphism.lean) — 原の18D全核正規商と実DV輸送像の群同型、代表元可換性、実像上受信器の一意因子化、全射の場合の標的拡張一意性と非全射反例。
- [FQ: RootedSectorKernelClassification](formal/Kuu/F112/PolygonNativeC60AQFullPentagonRootedSectorKernelClassification.lean) — FO全衝突核から像ファイバー根代表元への正規生成縮約、真正18D `assoc/post/pre` 衝突3族の厳密和集合分解、根付き同型と3セクター受信器降下 iff。
- [FG: GeneratorFaithfulnessGate](formal/Kuu/F112/PolygonNativeC60AQFullPentagonGeneratorFaithfulnessGate.lean)、[FG: ConstructorSectorSeparation](formal/Kuu/F112/PolygonNativeC60AQFullPentagonConstructorSectorSeparation.lean)、[FG: ConstructorPathInjectivity](formal/Kuu/F112/PolygonNativeC60AQFullPentagonConstructorPathInjectivity.lean)。

### 0A.2 数学的な論理境界（何が必要十分で、何が未充足か）

元の完全18Dコードを、元の非可換自由群の生成子アルファベットとして用いる。別途構成した文脈閉包18D受信器への写像を `f_w`、誘導自由群準同型を `τ_w` とする。このとき、証明済みの**無条件の同値**は

$$
\operatorname{Injective}(\tau_w)
\iff\operatorname{Injective}(f_w)
\iff I_{\mathrm{assoc}}(w)\land I_{\mathrm{post}}(w)\land I_{\mathrm{pre}}(w).
$$

FIはさらに全入れ子構成子列から非可換FreeGroupへの準同型 $S_{\mathrm{orig}}$、文脈閉包先 $S_{\mathrm{closed}}$ を構成し、**$S_{\mathrm{closed}}\circ\tau_w=S_{\mathrm{orig}}$** と **$\ker(\tau_w)\subseteq\ker(S_{\mathrm{orig}})$** を無条件に証明した。元raw17D引数を消す補助observerであり、FIの包含は全核分類・全コード単射性を意味しない。

ここで各 `I` は元18D構成子セクター内の完全依存型コードの単射性を表す。後続FI [#2676](https://github.com/itakura-hidetoshi/KuuOS/pull/2676)で、**$\operatorname{Injective}(\tau_w)\iff\operatorname{Injective}(f_w)\iff\operatorname{Injective}(C_w)$** を証明した。これは元`assoc/post/pre`全帰納法と元の両端点・中間raw17D Type値を保持した定理であり、FGの仮定付き固定端点generator gateを閉じる。**$C_w$自体の単射性は任意の実C60 frameで未証明**。元証拠とDX選択相対商、元raw経路と商クラス、17D対象と18D生成子を同一視しない。

**FO–FPで閉じた全核・第一同型定理（2026-10-29）：** 任意の元18D完全コード文字写像 `f_w:A_w→B_w`、その非可換自由群輸送 `τ_w=FreeGroup.map f_w` に対し、全衝突差語正規閉包 `N_w=⟪ [a][b]⁻¹ | f_w(a)=f_w(b) ⟫` は **`ker τ_w=N_w`**（FO）。さらに **`FreeGroup(A_w)/N_w ≃* range(τ_w)`**（FP）で、各元語の商クラスは輸送像に対応する。群受信器 `ρ:FreeGroup(A_w)→*G` は元の全コード衝突を同一視することと、`range(τ_w)` 上の一意な群準同型へ因子化することが必要十分。全標的 `FreeGroup(B_w)` への拡張は存在し得るが、`f_w` が非全射なら一意性は一般に従わない。これらは厳密な代数定理であり、元の依存型コード衝突の有限分類・19D幾何充填は未証明。

**FQで追加した衝突生成族の縮約・分類（2026-10-29）：** 像 `im f_w` の各受信コードから元source完全18Dコードを一つ選ぶ代表元写像 `r_w` とすると、**`ker(τ_w) = ⟪[a][r_w(a)]⁻¹ : a ∈ A_w⟫`** を無条件に証明した。任意衝突対 `f_w(a)=f_w(b)` は根を共有し、`[a][b]⁻¹=([a][r_w(a)]⁻¹)·([b][r_w(b)]⁻¹)⁻¹` と非可換順序を守って表せる。さらにFGの実コンストラクタタグ保存から、元の**全コード衝突集合が `assoc/post/pre` の3つの同セクター衝突集合の和集合**に等しく、3族の正規閉包が全DV核に等しいことをLean証明。根代表元自体も元18Dセクターを保つ。群受信器の実輸送像上への**一意な因子化**は、3セクターそれぞれでコード衝突時に受信器の値が一致することと必要十分である。ここではセクター間の可換性も全標的への全射も仮定していない。



`\operatorname{Injective}(\tau_w)\Rightarrow\operatorname{Injective}(C_w)` はFF/FDの必要条件、逆向きはFI #2676で証明済み。**FJ #2679では、具体的`S=nativeK5AXKuuSignature W`、`F=nativeK5BCFrame W`において `Injective(τ_w) ↔ w=[]` を証明**。ここで保守的15D証拠の元の`refl`と`atom`を区別したまま、真のwhiskeringが両者を同じ`atom`へ再構成することが衝突の原因である。一般抽象frameについてのFI同値と、選択物理presentationについてのFJ非単射性は矛盾しない。FCの「非自明核 iff コード衝突」とFGの「異種構成子間の衝突なし」は両立する。原pentagonは元のDV自由群像で非零のまま残り、選択したDX相対商では消える。**DSの完全証拠保存no-goを維持**する。

### 0A.3 次に形式化すべきこと — F112-P94D3FR（仮称）

1. **同一セクター内部の真正依存型衝突の分類**：FQでは3つの先頭`assoc/post/pre`タグを完全分離した。次は元17D source/target・raw16D証拠・可変再帰内側18D生成子・各AQ frameの具体的同値条件に沿い、どの同一セクターコードが衝突するかを分類する。異なる生成子セクターの衝突や全域の無条件単射性は捏造しない。
2. **根付き生成族の独立性・冗長性・最小性と有限性**：FQの代表元選択は同じ受信コードの全衝突対から根付き関係へ縮約するが、根付き集合の有限性・既約性・最小性は帰結しない。**必要なら追加の有限性・効果的代表元選択・衝突同値類の構造仮定を明示**し、条件付き定理や反例を証明する。単一の既知FJ二文字欠損で全核を正規生成することは未証明。
3. **受信器の像と全標的の継続的境界**：FP/FQで確立した実像上の一意性に対して、対象が非全射の場合に使用されない標的文字の群値は自由であり得る。実輸送像上の降下と標的自由群上の任意拡張を別問題として扱う。
4. **元19Dと高次比較の独立した証明義務**：真正C60 19D Type値幾何充填、異なる旧新17D/18D閉包signature全生成子間の比較射、局所大域strict 3/n圏およびhyperdescentは未解決。FJ・FN・DSの元のno-go、独立Kuuとstrict空のpresentation区別、107公開root、Gray非再導入を保持。

**完了判定：** 新Lean宣言の全型・依存境界、`#print axioms`、`sorryAx`なし、固定環境、changed Lean file全文・import閉包・pinned mathlib APIの照合、PR exact-headでworkflow/job/Lean stepがすべて`completed SUCCESS`。**queued / in_progressをSUCCESSとしない。** CI緑は数学的な追加仮定を消さない。docs-only編集は必要な文書・root検査を通すが、新しいLean定理を変更していないのにStrict Leanを再実行することを要件にはしない。

## 1. 最初から存在する一般理論を研究の幹として継承する

KuuOSの原初の問いは、C60の60頂点・90辺・32面ではなく、**関係や文脈の変化に沿う縁起、presentationを越える普遍性、局所大域整合性、障害、非実体化**です。これらの一般構成は後のC60以前から前進していました。

### 1.1 既存の形式的成果（C60を必要としない数学的骨格）

| 時系列 | 代表的な実装・証明 | 到達範囲／言い換えてはいけないこと |
| --- | --- | --- |
| v0–v1.7 | [FunctorialTransport v0.1](formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean)、[ContextualCore v1.0](formal/KUOS/DependentOriginationContextualCoreV1_0.lean)、[CoreSpine v1.7](formal/KUOS/DependentOriginationCoreSpineV1_7.lean) | 文脈圏上の状態の関手的transport、不変意味、refinementと2-cell、operadic複数入力。選択した構造の定理であり、任意の臨床・物理的因果の実証ではない。 |
| v1.21–v1.40 | [GlobalDuskinScaledNerve v1.21](formal/KUOS/DependentOriginationGlobalDuskinScaledNerveV1_21.lean)、[ScaledHornHomotopyDescent v1.33](formal/KUOS/DependentOriginationScaledHornHomotopyDescentV1_33.lean) | 高次simplicial比較、horn/homotopyとrectificationの厳密な分離。`horn homotopy`だけからstrict fillerを捏造しない。 |
| v2.0 | [PresentationUniversality v2.0](formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean) | `W`局所化の普遍因子化と普遍的carrier間の圏同値。`W`を同型へ送るという明示的な仮定が必要。 |
| v2.1–v2.7 | [WJCategoryEquivalence v2.7](formal/KUOS/DependentOriginationWJCategoryEquivalenceV2_7.lean) | `W`-invertingな文脈系の`J`-descentと局所化上のType値sheaf圏の同値。一般`H`は別課題。 |
| v2.8–v2.13 | [HigherStackDescent v2.8](formal/KUOS/DependentOriginationHigherStackDescentV2_8.lean)、[StrictHigherUniversality v2.13](formal/KUOS/DependentOriginationStrictHigherUniversalityV2_13.lean) | Cat値stackの被覆descentの同値判定と、強い`W.IsInvertedBy`下でのCat値局所化普遍性。任意弱擬関手の高次局所化や`(∞,3)`-hyperdescentまで証明したわけではない。 |
| v4.00–v5.36 | [旧ROADMAP §2](docs/legacy/ROADMAP-v5.291.md#2-obstruction-localization-and-exact-classification-foundations--v400v536) | 明示的な非因子化・capacity/incidence障害、presentation-sensitive descent、exact-universal分類、actual-liftへ進む一般的条件。結果の有効範囲は各Lean型に相対的。 |
| v5.37–v5.101 | [CoherentBiadjunctionActualLift v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) | 元の`F,G,η,ε`、前後triangulatorとswallowtailの両方を**同一original datum**で証明。これは任意のrawソースのstrict 3圏への自動的な昇格ではない。 |
| v5.102–v5.153 | [F44交換類 v5.141](formal/KUOS/DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.lean)、[F55高次cell v5.152](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152.lean)、[F56非忠実性 v5.153](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153.lean) | 選択した2軸のraw/quotient、有限高次証拠、normal form、異なるrawの観測像一致と非復元を証明。Gray的なweak合成をstrict 3圏の完成と読まない。 |

**重要な継承規則：** これらを再証明してからC60へ進む必要はありません。歴史的な証明の原型・依存・文脈を維持し、**新たなstrict 3/n圏に移すために必要な比較・保存定理だけ**を追加します。既存のGray/Bicategoryに依存する証明はその型で正当な歴史的成果ですが、将来のstrict 3圏の未証明公理を代行しません。

### 1.2 以前からの一般化の骨格

明示する文脈圏`C`、許容presentation変更`W`、被覆位相`J`、高次coherence`H`に対し、研究対象は概念的に

\[
\mathrm{DO}(C,W,J,H)
\]

です。`W`の局所化、`J`のsheaf/stack、`H`の高次比較は**それぞれ異なる義務**です。v2.0やv2.7に既証明の性質を、`H`全体やhyperdescentの無条件な存在へ飛躍させません。

また、空の空に従って`\mathrm{DO}`それ自体も唯一のpresentationにはしません。異なる`(C,W,J,H)`の間の輸送・同値・障害を研究対象に含めます。

## 2. C60という後発の具体的検証：成果と不足を明確化する

### C60グラフ主体の表示からゲージ表示への移行（F112・Qi v3.4）

[移行監査と数学的区別](docs/C60_GAUGE_PRESENTATION_MIGRATION.md)を参照。真正C60の60/90/32/360有限幾何、歴史的グラフ・Quiver、全no-goは保存する。前向きcoherence／descentをグラフ一致から導くことは禁止。[C60のゲージ接続と曲率](formal/Kuu/F112/PolygonNativeC60PhysicalGaugeAtlas.lean)、[真正P92Bから得たK₅非可換ゲージと旧形式的9面語の自然性数+1](formal/Kuu/F112/PolygonNativeC60K5TypedGaugeCoherence.lean)、[五行群ゲージ](formal/KUOS/Architecture/QiWuxingNativeC60GaugeV3_4.lean)は現在の比較presentationである。[PR #2510](https://github.com/itakura-hidetoshi/KuuOS/pull/2510)はMERGED。元の9面形式的語（+1）と、証明済みの補正後真正Type値9面閉路（+3）を同一視しない。4DのType値interchange・global strict 3/n・hyperdescentは未解決。

### 2026-10-24時点の歴史的厳密境界：F112-P94D3Q–T（main統合済み）

| PR | 真正な数学的成果 | 引き続き未証明の境界 |
| --- | --- | --- |
| [#2519 P94D3Q](https://github.com/itakura-hidetoshi/KuuOS/pull/2519) | 最後のsquare2の元P92B `symm` 証拠をF54構造的seamで保持。文脈深さ列が構造的seam全生成子で保存されること、旧shellingに必要な逆向きseamが存在しないことをLean証明。 | 元の9面shellingのType値貼り合わせ・P92Bへの新seam降下。 |
| [#2520 P94D3R](https://github.com/itakura-hidetoshi/KuuOS/pull/2520) | 既存8面の真正Type値貼り合わせとsquare2が同じF54境界を持つ平行3-cellであることを構成。自然性数+2と−1、群語の非同一性、旧構造的9面datumのno-goを証明。 | 同じ群語や高次4-cellの存在を影の一致から推定しない。 |
| [#2521 P94D3S](https://github.com/itakura-hidetoshi/KuuOS/pull/2521) | square2の3-cellだけを正しく反転して、元の面順序で実Type値9面閉路を構成。完全非可換群語を保ち `ν_N(W_typed)=3`、旧形式的 `ν_N(W_old)=1`、`W_typed W_old⁻¹=S q⁻² S⁻¹` をLeanで証明。旧full shadowは双方0。 | `W_old`をそのままType値化したという主張は禁止。旧P94A/P94C2充填も不可能。 |
| [#2522 P94D3T](https://github.com/itakura-hidetoshi/KuuOS/pull/2522) | 真正 `W_typed` を境界とする別のType値独立4-cell生成子を宣言。元の全typed 4-cell relatorと新語のmathlib正規閉包で、真の拡大・旧shadow降下・N非降下・共役作用・境界同変性・代数的Peiffer crossed-moduleを証明。 | 生成子の宣言≠任意Type値4-cell whiskering/interchangeのcoherence証明。これは次の独立課題。 |

**P94D3T当時の次段階の記録（P94D3U以降はその後進展済み）：** 当時の課題は、正規核の代数的Peifferと実Type値4-cell生成子を区別し、左右whiskeringのsource・高次coherenceを形式化することだった。以後の進展は本書§0AのEX–FIに更新した。**旧形式的自然性数1と真正補正後のType値自然性数3を同一視しない**という境界、旧P92BおよびP87/P88/P89の各presentation差異、一般W/J/H、局所・大域strict 3/n、`(∞,3)`-hyperdescentへの長期目標は引き続き有効。



真正C60幾何は原正二十面体から導いた60 Dart、90 Edge、32 Polygon（12五角形・20六角形）、360入射flagsを持ちます。一般的に進めていた高次法則・descent・障害の議論を、**見せかけの任意の例ではなく、検証可能な有限物理的入射上で試す**ために選んだpresentationです。

| 具体的な到達段階 | 本当にある成果 | なお必要なもの |
| --- | --- | --- |
| 独立基礎`Kuu.Presentation`、`Kuu.Strict`、`Kuu.Incidence` | 選択した自由経路の指定関係商・観測因子化、functor/natural transformationの**strict 2次元法則**、文脈切片・総圏。 | 証明関連3射を保持した局所strict 3圏の全公理。 |
| F112 P1–P26 | 原幾何とF69 zigzag・局所化、整数chain/ホモロジー、raw証拠の非降下、別位相への非一意性を実際のC60に構成。 | 類似した観測結果から全raw高次証拠の復元を仮定しない。 |
| F112 P27–P53 | [統合済み親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)で歴史的ソースの独立比較と真正面relatorを整理。P53は全32原面relatorを用いる原F42面商→F69の無条件因子化に到達。 | 別presentationの原3-Hom全体を勝手に同型としない。 |
| F112 P54–P57 | [P55 #2417](https://github.com/itakura-hidetoshi/KuuOS/pull/2417)、[P56 #2418](https://github.com/itakura-hidetoshi/KuuOS/pull/2418)、[P57 #2419](https://github.com/itakura-hidetoshi/KuuOS/pull/2419)・[#2420](https://github.com/itakura-hidetoshi/KuuOS/pull/2420)：raw F55の九生成子、完全source transport、水平自然性、選んだshadowの忠実な圏関手、非復元と別位相のobstruction。 | chosen shadowが唯一の空であることや、raw 3-cellがすでにstrict 3圏であること。 |
| **F112 P58** [#2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421) | **raw F55のliteral単位律・結合律の失敗**を構文の数え上げで証明し、mathlib自由経路圏を別途構成。 | raw証拠とstrict経路の同一視は禁止。 |
| **F112 P59** [#2423](https://github.com/itakura-hidetoshi/KuuOS/pull/2423) | ９構成子の垂直正規化：raw単位→空経路、raw垂直合成→連結、その他７構成子→個別生成辺。 | 垂直strict化から水平単位・交換は導けない。 |
| **F112 P60** [#2424](https://github.com/itakura-hidetoshi/KuuOS/pull/2424)・[#2425](https://github.com/itakura-hidetoshi/KuuOS/pull/2425)・[修復 #2428](https://github.com/itakura-hidetoshi/KuuOS/pull/2428) | mathlib自由経路正規化関手と、選択された`(ℤ×ℤ)×ℤ/2ℤ` shadowへの整合性。raw証明履歴が一般に非復元であることを区別。 | 数値shadow商をstrict 3圏の完成形にしない。 |
| **F112 P61** [#2426](https://github.com/itakura-hidetoshi/KuuOS/pull/2426) | 水平合成の垂直正規形は２辺。raw単位同士を水平合成すると長さ２で、空経路とはliteralに異なる。selected shadowでは値0。 | P61は現presentationの障害であり、大域strict 3圏no-goではない。 |
| **F112 P62** [#2429](https://github.com/itakura-hidetoshi/KuuOS/pull/2429) | ９構成子の再帰的な**単位生成構文**から、同じ型付きF54両端を持つ自由経路の関係を生成。反射・対称・推移・垂直合成の合同性、選択された観測への健全性、P61水平単位と空経路の**関係上の同値**をLean4で証明。真正C60 pentagon/hexagon生成子は単位生成構文から除外。 | 水平合成の任意の代表元に対する合同性、結合律、全interchange、global strict 3/nは未証明。 |
| **F112 P63** [#2431](https://github.com/itakura-hidetoshi/KuuOS/pull/2431) | 全９構成子に対して単位生成raw証明のF54始終経路が同じになることを再帰的に証明。左右contextをmathlib自由経路関手として構成し、垂直合成と原raw生成元の輸送、`unitOnly`保存、左右context付き単位セルのP62関係を証明。 | raw context自由経路関手がP62の**全ての**合同関係を保存することはまだ未証明。選択shadowの等号では代用しない。 |
| **F112 P64** [#2432](https://github.com/itakura-hidetoshi/KuuOS/pull/2432) | P62関係に対しmathlibの`Congruence`実装と`CategoryTheory.Quotient`を構成。`Q(f)=Q(g) ↔ f∼unit g`という等号反映、P61水平単位の商圏での等号、既存chosen shadowへの因子化と生成元観測の保存を証明。 | これは**垂直**商圏であり、水平の代表元独立性、全interchange、globular strict 3/n圏はまだ成立としない。 |
| **F112 P65** [#2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434) | raw `ident`生成辺とP59正規化後のunit-only単一生成辺を区別する`NativeF55UnitWord`を構成。全９構成子の正規化、typed unit wordのP62関係上の単位性、左右contextによるword保存、**P62の全５生成規則の左右context保存**を証明。mathlibの商圏`Quotient.lift`で左右作用をP64最小商圏へ降下させ、正確な因子化等式を得た。 | 左右各１変数の降下は完了。ただし**２変数の水平双関手性、水平合成の結合律、真のinterchange、strict 3/n圏**は未証明。 |
| **F112 P66** [#2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436) | P64の商関手は元の型付きF54経路**対象に単射**であり、任意の真正F54局所回転対の左先・右先交換経路は商圏でも異なる対象。真正C60六角形についても非同一性を証明。一方で両対象を結ぶF55 disjointSquare 3射は残り、その選択された交換位相は非零。 | **F54対象の厳密interchangeはP62–P65の3射単位合同だけでは導出不能**。適切な2-route比較、必要条件、その新たな関係で何が失われるかを先に定理化する。global strict 3/n不可能性とは言わない。 |
| **F112 P67** [#2438](https://github.com/itakura-hidetoshi/KuuOS/pull/2438) | ４構成子（単位・対称・推移・真正disjoint-square）の**Type値F54経路比較証拠**を構成。各証拠から真正F55 raw cellへ写像できる。比較の存在命題だけをSetoid化し、商クラス等号の必要十分性、実C60での左右順序同一視、同一視する任意の目標写像の非単射性、元の非零交換位相とraw履歴の存続を証明。 | クラス等号は具体的raw証明を一意に選ばない。P67関係が全contextに閉じることや全Hom輸送は未証明。 |
| **F112 P68** [#2439](https://github.com/itakura-hidetoshi/KuuOS/pull/2439) | ９構成子を検査し、五角形原始生成元を除く**squareOnlyの証明依存Type値rawセル**からcontext閉包比較商を構成。P67商→P68商、左右F54 contextのwell-definedな写像と代表元整合、真正C60交換比較を証明。 | P67商との同値・忠実性は未証明。route対象の商だけでは3-Homのtransport・globular strict 3圏・全interchangeを得ない。 |
| **F112 P69** [#2441](https://github.com/itakura-hidetoshi/KuuOS/pull/2441) | P68比較クラス上のF54代表経路とType値F55 raw 3-cellを保持する高次射の依存型構造。元raw証明項保存と、クラス等号から得られるsquareOnly証拠の存在を証明。 | クラス等号から証明項を正準に選ぶこと・高次Homの代表元独立な合成は未証明。 |
| **F112 P70** [#2442](https://github.com/itakura-hidetoshi/KuuOS/pull/2442) | 両端squareOnly証拠で選択した代表元変更と、中間比較証拠付きの高次射の合成を構成。原raw履歴と選択shadowの加法公式。実C60の恒等射（位相0）は交換正方形に沿って輸送すると位相1となり、両端の比較クラスは同じ。 | 合成は比較証拠の**選択依存**。原shadowを経路クラス等号だけから一意に復元してはならない。 |
| **F112 P71** [#2444](https://github.com/itakura-hidetoshi/KuuOS/pull/2444) | P70の選択証拠付き代表元変更から輸送同値・Setoid・商を構成。商等号の必要十分条件、同値な高次射でraw shadowが異なる場合には無補正のshadow readoutが全代表元上で商へ降下しないという一般的必要条件/no-goを証明。真正C60の輸送同値と位相差を確認。 | **原shadowの無補正な因子化に関する限定no-go**。補正付き・gradedな輸送、全Homの高次coherence、strict 3/n圏は未証明であり不可能とも主張しない。 |
| **F112 P72** [#2446](https://github.com/itakura-hidetoshi/KuuOS/pull/2446) | 比較証拠付き代表元変更・bridge付き縦合成によるshadow付加項を実際のF55 raw証明から導出し、補正公式、２段階輸送cocycle、真正C60交換正方形の補正前非零・補正後位相0を証明。 | 補正は証拠を選ぶgraded presentationの情報であり、P71の無補正商で全shadowが降下したとは言わない。 |
| **F112 P73** [#2447](https://github.com/itakura-hidetoshi/KuuOS/pull/2447) | 全９構成子にわたる`squareOnly`証明セルの五角形整数charge 0、P70左右輸送・bridge合成の五角形charge保存、P71輸送同値の全４規則での保存を証明。P71商上に五角形charge readoutを実際に`Quotient.lift`で構成。 | 全shadowは非降下、選択された交換位相は変更可能。五角形chargeの降下をすべての高次情報の復元と同一視しない。 |
| **F112 P74** [#2448](https://github.com/itakura-hidetoshi/KuuOS/pull/2448) | 元の符号付き整数線形観測`aP+bS`について、交換整数chargeを1だけ変化させる輸送同値対が存在する**固定されたP71商**では、全元代表値と一致する無補正商readoutの存在が`b=0`と必要十分と証明。真正C60の恒等F55 raw証明の交換charge0→交換正方形沿い輸送で1を検証。 | 分類対象は選択した２整数線形観測。補正付き/graded/torsor Hom、高次合成全体、strict 3/n・hyperdescentはまだ未証明。 |
| **F112 P75** [#2450](https://github.com/itakura-hidetoshi/KuuOS/pull/2450) | 既存P71輸送４生成規則を真正F55 Type値証拠を保持したshadow-grade付き輸送履歴に持ち上げた。健全性（終点shadow＝始点shadow＋grade）、同一raw両端のgrade一意性、閉路grade0、P71のProp輸送関係とgraded履歴のNonemptyの必要十分性、真正C60整数交換charge+1と非零奇位相を証明。 | gradeの唯一性はraw履歴の等号・証拠の標準選択ではない。真正bridge合成・高次interchangeのcoherenceと局所strict 3圏は未証明。 |
| **F112 P76** [#2451](https://github.com/itakura-hidetoshi/KuuOS/pull/2451) | 元のsquareOnly比較証拠をType値で縦合成し、二段階代表元輸送の正規化経路・全shadowの整合性、bridge移行時の正確なfull-shadow差分を証明。**明示的なbridge正規化経路一致の条件下**で全合成経路が一致する定理。実C60のraw履歴非同一と正規化同値を区別。 | bridge経路の一致やraw4-cellの存在を無条件には導いていない。局所・大域strict 3/nは未証明。 |
| **F112 P77** [#2452](https://github.com/itakura-hidetoshi/KuuOS/pull/2452) | 8規則の真正Type値raw F55 vertical 4-cell、縦単位・結合・左右whisker、P59正規化経路と全shadowへの各独立健全性、P62単位合同への片方向射、明示証拠存在を正確なkernelとするSetoid・Quotientを構成。実C60のraw非同一なsource履歴を4-cellで比較。 | 単なるshadow等号やpath等号から4-cell証拠が得られるという逆は未証明。水平interchangeも未証明。 |
| **F112 P78** [#2453](https://github.com/itakura-hidetoshi/KuuOS/pull/2453) | P77 source4-cell合同への縦合成の適合性から、元のF54 route上のHomをP77商とする**明示的Mathlib Category**を構成。原raw単位・合成および真正4-cell結合証拠による厳密な縦単位・結合法則。P59正規化自由経路とfull shadowの厳密加法性も証明。 | 既存Categoryインスタンスを置換しない独立presentation。水平二変数合成・interchange、4-cell間coherence、大域strict 3/n・hyperdescentは未証明。 |
| **F112 P79** [#2455](https://github.com/itakura-hidetoshi/KuuOS/pull/2455) | 元のF55水平恒等合成と合成後恒等のP59経路長が２対０であることから、P77 Type値raw4-cell**非存在**と厳密商クラス非同一性を証明。左右F54 context単位も１対０の障害。全shadowの一致だけではraw4-cellが得られず、P62の構文由来単位合同では各対を比較できる。真正C60六角形の独立左右F54回転を用いて具体化。 | P77の厳密path等号を保つ4-cell拡張で水平単位律を満たすことは不可能。P80で別のP62-relative Type値4-cell候補を構成済み。大域strict 3/nやhyperdescentの不可能性とは異なる。 |
| **F112 P80** [#2457](https://github.com/itakura-hidetoshi/KuuOS/pull/2457) | 旧P77の真正Type値4-cellを保持したうえで、水平単位・左右context単位を**新たなType値4-cell生成規則**として明示し、反射/対称/推移/左右縦whisker閉包を構成。全生成規則のP62構文的unit-path合同への健全性と原full F55 shadow保存、縦合成適合性、実証拠存在をexact kernelとするSetoid商・shadow因子化を証明。真正C60で旧P77商の非同一性と新P80商の同一性を併記。 | 新しい比較は選択されたpresentationであり、旧P77 path equalityのno-goを覆さない。P81で新商上の局所縦Categoryを完成。一方、一般水平2変数合成はP82で現P80商への非降下を証明。interchange、大域strict 3/n・hyperdescentは未証明。 |
| **F112 P81** [#2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459) | 新P80のType値4-cellに基づく縦合成well-definednessと厳密な局所Mathlib `Category`を構成。原F55 full shadowの合成保存・単位零、旧P77→P80の実証拠由来全射・縦合成/全shadow保存、真正C60での非単射性、P59厳密自由経路readoutの新商への非降下をLeanで証明。 | 単一公開KuuOSFormalへ直接import。旧P77・P79の障害を保持。水平双変数合成についてP82で現P80商への非降下を証明。interchange、4-cell間coherence、大域strict 3/n・hyperdescentは未証明。 |
| **F112 P82** [#2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461) | 元F55 raw構文から独立したNat値不変量を定義し、旧P77の8生成規則とP80の全9種類のType値4-cell生成規則すべてで保存することを証明。旧P77の縦左単位4-cell `id ≫ f ~ f` に元の水平合成（右側は同じ恒等3-cell）を施すと、非単位・非`trans`の`f`では不変量が**1対2**となり、**P80の4-cell非存在と商クラス非同一性**を証明。真正C60北五角形のpentagon 3-cellと型付き右恒等経路で実現。 | **現P80商には元F55水平合成が一般には降下しない**ことが確定。P80以外の比較presentation、P62合同一般、strict 3圏一般のno-goではない。今後のcontext輸送・高次比較証拠・その健全性とstrict interchangeは未証明。 |
| **F112 P83** [#2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463) | mathlib `Quiver.Path.addWeight`によりP82 raw Nat不変量を元F55型付きP59 free pathへ拡張。原raw 9構成子と正規化の適合性、P62 unit-only合同の5生成規則すべての保存をLeanで証明した。P82で見つけたP80旧左単位4-cellの水平合成後の2つの真正raw証明は不変量が1と2で、**P62経路合同でも関係せず、P62のMathlib商でも非同一**とexact kernelから証明。真正C60北五角形へ具体化。 | **追加context 4-cellを旧P62に健全と主張することは、この例では不可能。** P80だけでなく、必要な比較について旧P62合同も不足。P62の全関係が無効という意味ではなく、P84で新しいpath合同とCategory商、旧P62からの比較関手、full shadow保存を形式化済み。ただし新Type値4-cellの一般context輸送は未証明。strict 3圏一般や縁起一般理論のno-goではない。 |
| **F112 P84** [#2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465) | **P62とP80を変更しない別presentation**として、旧P62合同証拠・同値/縦合成合同・任意の真正P80 Type値4-cellの左右水平whiskeringを生成規則とする新型付きfree-path合同を構成。全7生成規則についてF55原full shadowを保存し、Mathlib `Congruence`・局所`CategoryTheory.Quotient`・**exact source-witness kernel**・shadowへの厳密因子化を形式化。旧P62商→新P84商の比較関手と原pathとの可換三角形、P82/P83比較の**旧商非同一・新商同一**を証明。真正C60北五角形で真の拡張。 | これは**path合同とその局所Category商**であり、P81のP80 4-cell商上の縦Categoryとは異なる。P85で旧P80 4-cellの左右水平作用をType値新4-cellとして証明しP84 path合同への健全性を検証。ただし新P85 4-cell自体の全context輸送、新P85同士の水平関手性、strict interchange、高次coherence、大域strict 3/n・hyperdescentは未証明。P83の旧P62 no-goを変更しない。 |
| **F112 P85** [#2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467) | 旧P80のType値4-cellを明示埋込みし、左右水平whiskeringを真正F55 raw証拠付き生成規則とする**新しいType値4-cell言語**を構成。全8生成規則の**新P84 path合同健全性**と原F55 full shadow保存、実証拠exact kernelのSetoid/商、元F54経路上の**厳密な局所縦Mathlib Category**を構成。旧P80→新P85全射と、元F55水平合成の**旧P80商×旧P80商→新P85商**への代表元に依存しない二入力降下を左右真正4-cell証拠で証明。C60北五角形で旧P80商非同一・新P85商同一。 | **二入力のwell-definednessのみ**であり、新P85商×新P85商への全水平関手性、縦合成とのstrict interchange、旧P85証拠に沿ったpre/post・左右context輸送はP86でP85→P86商として証明済み。新P86自身の全4-cell輸送は未証明。旧P62やP80のno-goを覆さず、新しいP84 path合同を比較の証拠層とする。局所strict 3圏全法則・大域strict 3/n・hyperdescent未証明。 |
| **F112 P86** [#2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469) | 元P84経路合同と元P85 Type値4-cellを変更せず、P85の実証拠を使う左右F55 context・前後F54 route・左右水平whiskeringの6操作を新生成規則とする**P86型付きfree-path合同（11規則）**と、同じ6作用をType値ソースに備えた**P86 4-cell言語（12規則）**を構成。全生成規則のF55 full shadow保存、新P86 Type値4-cellから新経路合同への健全性、経路側Mathlib Category商とfull shadow因子化・exact kernel、Type側Setoid/Quotientのexact kernelと厳密局所縦Categoryを証明。旧P84→P86経路商比較関手、旧P85→P86の全射・縦合成保存、**旧P85商から新P86商への左右context・pre/post代表元独立輸送**、さらに**旧P85商×旧P85商→新P86商の二入力水平降下**を真正Type値4-cellで構成。北側C60五角形の実証拠を追加の左contextへ輸送したP86証拠と商等号も証明。 | 旧P82/P83の否定定理は元presentationについてそのまま保持。**P86自身を固定した同一商での水平閉包は示していないが、別presentation P87において自身の再帰的Type値閉包とP87×P87→P87の水平二入力演算・水平単位を証明。元F55 strict interchange、4-cell高次coherence、大域strict 3/n・(∞,3)-hyperdescentは未証明**。P86局所縦Categoryを局所strict 3圏完成と混同しない。 |
| **F112 P87** [#2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471) | 旧P86 Type値4-cellを保持し、新P87の**自身の真正Type値4-cell証拠**を左右context・pre/post F54 route・左右水平whiskeringに再帰的に作用させる12生成規則の新ソースpresentation。新P87型付きfree-path合同（11生成規則）も同じ原P87 Type値証拠を直接保持。両者のfull shadow健全性・Type値証拠の新経路合同への健全性、exact witness kernelのType商・Mathlib局所経路Category商、旧P86→P87経路商比較関手をLeanで証明。新P87 Type値商の**厳密局所縦Category**、旧P86からの全射/縦合成保存、**P87→P87の左右context/pre・post演算、P87×P87→P87の元F55水平二入力演算と真正P80単位4-cellによる水平単位**、full shadow水平加法保存を証明。元F55 interchange両辺のfull shadowは一致（必要条件）と形式化。 | **水平二入力演算が閉じることとstrict bifunctor/strict interchangeを混同しない**。元F55 interchange両辺を結ぶType値4-cell存在と縦合成保存、元F54異なる経路対象の比較・高次coherenceは未証明。P66のC60 disjoint square別経路/odd phase、P82/P83旧presentation no-goは保存。局所strict 3/n全公理・大域strict 3/n・hyperdescentも未証明。 |
| **F112 P88** [#2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473) | **P88A**：原F55の9構成子に非可換`List Bool`語を付与し、縦合成＝連結、左右F54 context＝`false`/`true`の各語とする。P77(8)/P80(9)/P85(8)/P86(12)/P87(12)の全真正Type値4-cell生成規則に対する語保存、P87商等号からの語等号、構文的`unitOnly`と空語の必要十分性を証明。**P88B**：型付き`f₂,g₁`が非単位のとき、元F55のinterchange二辺の非可換語が異なることを示し、**その間のP87 Type値4-cell非存在とP87商での非等号**を形式化。真正C60北pentagonとhexagon disjoint squareの原始語も確認。 | このno-goは**選択したP87 presentationに対する条件付き命題**。strict 3圏一般や任意のC60 4因子の不可能性ではない。原full shadow一致はsource証拠を与えない。新P89でinterchange比較を追加する場合、P88非可換語は一般に保存されないことを明示し、型付きF54 route objects・奇位相・4-cell高次coherenceを別途追跡する。 |
| **F112 P89A** [#2475](https://github.com/itakura-hidetoshi/KuuOS/pull/2475) | 旧P87証拠を単一のbase生成子として埋め込み、13生成規則（新たな型付き原F55 interchange 4-cell生成子を含む）の**別の真正Type値P89 presentation**を構成。元F55 full shadowの全生成子保存、source証拠のexact kernel商、旧P87商→P89商の全射、raw interchange新商等号、非単位中間因子での旧P88非可換語の非保存を証明。 | **新比較は新P89の明示的生成子**であり、旧P87 4-cellが存在したという意味ではない。P88 no-goを維持。F54 route objectsの比較や厳密な高次全法則を証明したものではない。 |
| **F112 P89B** [#2476](https://github.com/itakura-hidetoshi/KuuOS/pull/2476) | 新P89証拠の再帰閉包から**厳密局所縦Mathlib Category**、左右context/pre・post降下、P89×P89→P89の代表元独立な原F55水平合成、真正P80水平単位、全full shadow保存を構成。**任意の4つの型付きP89商クラスについてstrict interchangeの等号をLeanで証明**。旧P87非等号・新P89等号という条件付き商の厳密拡張を証明。 | globular strict 3圏全公理の完了ではない。特に水平結合律のF54 tree bracketing、route object比較、源4-cell間高次coherence、C60での特定の4中間因子の同時実現、大域strict 3/n・hyperdescentは未証明。 |
| **F112 P90A** [#2478](https://github.com/itakura-hidetoshi/KuuOS/pull/2478) | F45内部節点/左根節点不変量、原F19/F28両Nat cast保存、任意6深さでの三項原F45木の厳密不等性・全sector一致、真正F54一回転associator route、C60北五角形実例をLeanで証明。 | 原木のraw不等性は一般strict 3圏のno-goではなく、別のhigher比較presentationの必要性を示す。 |
| **F112 P90B** [#2479](https://github.com/itakura-hidetoshi/KuuOS/pull/2479) | 元F55由来の正しい二経路水平演算、任意3本の原F54経路に対する左右assoc自然性routeを同一F45始点・終点へ構成。原始回転数一致、firstPastingTagが1対0によるraw route不等性を証明。元F55比較`PresentedCell`のType slotを定義。 | **slotは未充足**。F55 3-cell存在も4-cell coherenceも未証明。P89 interchangeから水平結合律を捏造しない。 |
| **F112 P91A** [#2481](https://github.com/itakura-hidetoshi/KuuOS/pull/2481) | 原F55九構成子に対する原F54回転数差＝F55五角形整数電荷を帰納証明。P90自然性比較slotのinhabitantには五角形電荷0が必要、square整数chargeのparityがodd phaseを決める必要full shadow形状を形式化。 | 存在証明・無条件natural transformation・4-cell coherenceではない。C60 odd phaseを零化しない。 |
| **F112 P91B** [#2482](https://github.com/itakura-hidetoshi/KuuOS/pull/2482) | 真正原F55 Type値証拠存在によるF54 route-object exact kernel Setoid/商。P67 square-only商からの全射、旧P67では回転数保存・新P91B商では真正pentagon 3対2同一視による回転数非降下、C60北pentagonのraw非同一・新商同一を証明。P90二自然性routeの新商等号iff真正F55比較証拠存在を形式化。 | **P90比較slotのinhabitantと新商等号はどちらも未証明**。原F54回転数喪失を明示し、旧P89 3-Hom商と混同しない。 |

P58–P91の新規ソースは**canonical mainに存在**します。[P58](formal/Kuu/F112/PolygonNativeF55RawStrictificationBoundary.lean)、[P59](formal/Kuu/F112/PolygonNativeF55RawVerticalNormalizationP59.lean)、[P60正規化関手](formal/Kuu/F112/PolygonNativeF55RawPathNormalizerFunctorP60.lean)、[P61](formal/Kuu/F112/PolygonNativeF55HorizontalStrictPathBoundaryP61.lean)、[P62](formal/Kuu/F112/PolygonNativeF55TypedUnitCongruenceP62.lean)、[P63](formal/Kuu/F112/PolygonNativeF55ContextPathActionsP63.lean)、[P64](formal/Kuu/F112/PolygonNativeF55StructuralUnitQuotientP64.lean)。追加[P65](formal/Kuu/F112/PolygonNativeF55ContextUnitDescentP65.lean)・[P66](formal/Kuu/F112/PolygonNativeF55C60InterchangeRouteObstructionP66.lean)・[P67](formal/Kuu/F112/PolygonNativeF55TypedSquareRouteComparisonP67.lean)・[P68](formal/Kuu/F112/PolygonNativeF55ContextSquareComparisonP68.lean)もmainにある。raw Type値の歴史、経路対象、単位合同関係、square比較クラス、選択shadowの役割と等号を混同しない。 追加[P69](formal/Kuu/F112/PolygonNativeF55HigherHomTransportBoundaryP69.lean)・[P70](formal/Kuu/F112/PolygonNativeF55HigherHomRepresentativeTransportP70.lean)・[P71](formal/Kuu/F112/PolygonNativeF55HigherTransportQuotientP71.lean)・[P72](formal/Kuu/F112/PolygonNativeF55TransportShadowCocycleP72.lean)・[P73](formal/Kuu/F112/PolygonNativeF55PentagonChargeTransportDescentP73.lean)・[P74](formal/Kuu/F112/PolygonNativeF55LinearChargeDescentP74.lean)・[P75](formal/Kuu/F112/PolygonNativeF55GradedTransportCoherenceP75.lean)もmain統合済み。 追加[P76](formal/Kuu/F112/PolygonNativeF55BridgeTransportPathCoherenceP76.lean)・[P77](formal/Kuu/F112/PolygonNativeF55RawVerticalFourCellP77.lean)・[P78](formal/Kuu/F112/PolygonNativeF55RawFourVerticalCategoryP78.lean)もmain統合済み。 追加[P79](formal/Kuu/F112/PolygonNativeF55RawFourHorizontalUnitObstructionP79.lean)もmainへ統合済み。 追加[P80](formal/Kuu/F112/PolygonNativeF55P62RelativeUnitFourCellP80.lean)もmain統合済み。 追加[P81](formal/Kuu/F112/PolygonNativeF55P80UnitFourVerticalCategoryP81.lean)もmainに存在し、単一公開`KuuOSFormal`から直接import済み。 追加[P82](formal/Kuu/F112/PolygonNativeF55P80HorizontalContextObstructionP82.lean)もmainに存在し、P80水平合成の非降下定理と真正C60実例を収録している。 追加[P83](formal/Kuu/F112/PolygonNativeF55P62HorizontalContextObstructionP83.lean)もmainに統合され、P62 path合同の不変量保存とC60の非比較定理を保管する。 追加[P84](formal/Kuu/F112/PolygonNativeF55P80HorizontalPathCongruenceP84.lean)もmainにあり、P80 4-cell証拠による新経路合同、正しいMathlib商、旧P62比較関手、真正C60 strict enlargementを含む。 追加[P85](formal/Kuu/F112/PolygonNativeF55P84HorizontalFourCellP85.lean)もmainへ統合され、新しいType値4-cellの水平証拠・P84 soundness・局所縦Category・旧P80からの二入力演算とC60 strict enlargementを収録する。 追加[P86経路合同](formal/Kuu/F112/PolygonNativeF55P86ContextPathCongruence.lean)と[P86真正Type値4-cell](formal/Kuu/F112/PolygonNativeF55P86ContextFourCell.lean)もmain統合済みで、両者を単一公開KuuOSFormalから直接importする。 追加[P87再帰的4-cell](formal/Kuu/F112/PolygonNativeF55P87ClosedFourCellCore.lean)・[P87型付き経路合同](formal/Kuu/F112/PolygonNativeF55P87ClosedPathCongruence.lean)・[P87内部水平Category](formal/Kuu/F112/PolygonNativeF55P87ClosedHorizontalCategory.lean)もmainに存在し、単一公開KuuOSFormalから直接importする。 追加[P88A原ソース語](formal/Kuu/F112/PolygonNativeF55P88InterchangeWordInvariant.lean)・[P88B厳密obstruction](formal/Kuu/F112/PolygonNativeF55P88InterchangeObstruction.lean)もmain統合済み。追加[P89A新Type値interchange証拠](formal/Kuu/F112/PolygonNativeF55P89InterchangeFourCell.lean)・[P89B厳密水平–縦interchange](formal/Kuu/F112/PolygonNativeF55P89StrictHorizontalCategory.lean)もmainに存在。追加[P90A三項木境界](formal/Kuu/F112/PolygonNativeF55P90AssociatorSourceBoundary.lean)・[P90B三経路自然性境界](formal/Kuu/F112/PolygonNativeF55P90TripleRouteNaturalityBoundary.lean)もmainに統合され、すべて単一公開`KuuOSFormal`に直接import。追加[P91A原回転数defect](formal/Kuu/F112/PolygonNativeF55P91RotationDefectConstraint.lean)・[P91B原F55 full-witness F54経路商](formal/Kuu/F112/PolygonNativeF55P91FullWitnessRouteQuotient.lean)もmain統合済みで、元の107公開rootを保全する。

## 3. 最優先の新規数学：局所proof-relevant strict 3圏

**目標:** C60を一つの具体例として含み得る一般的な高次source`\mathcal K`に、globularな`0,1,2,3`射の型付き境界と合成を設け、**strict 3圏の全公理をLean4で証明**する。

必要な義務：

1. **境界とglobularity**：全射の`source/target`、2/3射の平行性、各方向の合成可能性を型で保証する。
2. **合成・単位・結合律**：`\circ_i`を定義し、すべての定義可能な段階でstrictな左右単位・結合の等式を証明する。元のraw語のliteralな等式とは混同しない。
3. **全interchange**：異なる`i<j`方向の合成について、弱いinterchanger 3射ではなく厳密な等式を証明する。Gray圏のcoherenceを証明の代用品にしない。
4. **非自明性・source情報**：raw証拠、原F54/F55履歴、位相・曲率・障害を失うか否かを**個別の保存/非保存定理**で記載する。単に全3射を同一視した圏ではこの研究目標を達成しない。
5. **最小の整合関係またはno-go**：P77のraw4-cell/P78旧縦CategoryではP59自由経路等号を保存するため、P79で元水平単位律の障害が確定した。P80はそれを維持した別presentationとして水平・左右context単位のType値4-cellを明示的に追加し、P62構文的合同に健全。P81は新P80商上で厳密な局所縦Categoryを構成し、P77→P80全射・C60非単射性とP59厳密path readoutの新商への非降下を証明した。P82では元水平合成がP80合同を保存しないことを旧縦左単位の実4-cellと独立raw構文不変量で形式的に示し、真正C60北五角形で具体化した。P83ではその不足するcontext比較が元P62 unit-only path合同でも成立しないことをmathlibの加法的free-path不変量により証明した。P84では元P62/P80を改竄せず、新しいpath合同を真正P80 Type値4-cellの左右水平作用を生成規則として構成し、shadow保存・Mathlib Category商・exact kernel・旧P62比較関手・真正C60真拡張を証明した。P85では旧P80 Type値4-cellの任意の左右水平whiskeringを新しいType値4-cell証拠として構成し、P84 path合同への健全性、full shadow保存、局所厳密縦Category、旧P80商×旧P80商→新P85商の二入力well-definednessを証明。P86では旧P85 4-cellの左右context・pre/postルート・左右水平輸送を別のP86 path合同とType値4-cellで実装し、全生成規則のshadow保存・path健全性、二つの局所商/Category、および**P85×P85→P86の水平二入力降下**を実証した。P87では旧P86を変更しない別presentationとして、P87自身のType値4-cellの再帰的context/pre・post/水平閉包を確立し、初めて同一P87商×P87商→P87商で閉じる元F55水平合成と水平単位を真正4-cellで証明した。interchange二辺のfull shadow一致は確認したが源4-cell証拠存在を意味しない。P88では非可換原F55ソース語を導入し、P87の全真正4-cellで語保存を証明し、非単位の中間因子に対する厳密interchange 4-cellの不存在とP87商非等号を確定した。P89A/P89Bでは**旧P87を改変せず、型付き原F55 interchangeを新しいType値4-cell生成子として明示する別presentationを構成し**、full shadow保存と非可換語の非保存・厳密局所縦Category・自己閉包水平合成・任意4クラスのstrict interchangeを証明した。P90以降はF54 route対象の異なるbracketing・水平結合律・4-cell間高次coherenceを検証する。

**完了基準:** 本物の3-cellと全globular境界、合成・単位・結合・交換のLean定理、`#print axioms`、情報保存/損失定理、exact-head CI。**自由path 1圏を作っただけ、2次元のstrict interchangeだけ、Gray圏の可逆interchangerだけでは未完了**です。

## 4. 既存の一般的W/J/H定理とstrict 3圏の接続

局所strict 3圏を構成した後に初めて一般理論を「開始」するのではありません。すでにある一般的な`W/J/H`とstrict高次ソースの間に**比較の橋**を追加します。

- `W`を尊重する実際の高次source-change・localizationの存在と普遍性を示す。`W`-同値とraw同一性を区別する。
- `J`の被覆・refinementのもとで、2/3射を保つrestrictionとoverlap比較を構成する。既存のType値sheafやCat値stackの定理は、その**正確な範囲だけ**で再利用する。
- `H`には既存のbicategorical/scaled-horn・original actual-lift/swallowtailの定理を参照し、strict 3/n圏への比較が存在する場合にのみ移送する。すでに存在するweak-to-strict等価を仮定しない。
- あるpresentationで証明済みの法則が別のpresentationへ移る必要十分条件、あるいは明示的obstructionを求める。

**完了基準:** 少なくとも二つの具体的・異なるpresentation間に実際の型付き比較写像があり、既存の普遍性・降下条件について保存される範囲と失われる範囲がLeanで証明されていること。

## 5. 大域strict 3圏の構成：有限Čechから大域の証明へ

文脈site`(\mathcal C,J)`上の局所strict 3圏`\mathcal K_3(U)`と重なりへのrestrictionを与え、実際の大域対象を構成します。

1. 2つの局所表示のoverlap上の**sourceの証拠に忠実な比較**。同じ観測値だけでは原3射を同一視しない。
2. 三重以上のoverlapで、局所合成とtransportのstrict整合を証明。曲率・非零cocycleを消してしまう形式的な貼り合わせは禁止。
3. 局所データと大域データの比較`\mathcal K_3(U)\to Desc(\{U_i\})`について、対象だけでなく高次mapping層の完全性・忠実性・実効性を検証する。
4. 障害がある場合、exact obstruction class・補正の要否・補正を選んだ場合の非一意性を明示する。既存のC60曲率や非liftを一律にゼロと扱わない。

**完了基準:** 対象から3射までの大域的な厳密合成、cover/refinement下の制限、必要なdescent・glue定理、または正確なno-go。C60の有限ČechやCat値stackの結果の言い換えだけでは未完了です。

## 6. 大域strict n圏：nを変えても証明が保たれる構造

固定3次元での証明を出発点とし、任意有限`n≥3`に対するglobular `n`-categoryの定義、すべての方向の合成`\circ_i`、単位・結合・交換の帰納的な証明を目指します。

- 次元`n`で追加される境界・高次合成・交換を、先行次元の整合性と矛盾せず定義する。
- `n`に関する帰納法のstepで必要なcoherenceを**公理の単純な仮定ではなく**、構成・定理にする。
- 構成を特定のC60幾何へ閉じ込めず、選択した文脈、局所化、被覆、presentation変更に相対化する。
- strictnessのために非自明なsourceをすべて殺す構成は採用せず、保存量・反例・障害を報告する。

**完了基準:** 指定したソースの種類について`n`を自由に変えられるLean構造・合成定理・具体例との非退化な比較が存在すること。「3圏の定義を形式的に複製しただけ」では未完了。

## 7. (∞,3)-圏への比較：strict n圏からの飛躍を禁止する

一般の`(∞,3)`圏では4次以上の射は可逆です。strict n圏の列を作れば**そのまま一般の`(∞,3)`圏になる**とも、任意の弱い高次圏を完全strict化できるとも主張しません。

- 対象とモデル（例：適切な高次Segal/nerveモデル）を明確に選び、何を`(\infty,3)`-equivalenceと呼ぶか定義する。
- 0〜3次のstrictデータを保つ比較構成、4次以上の可逆/coherentデータの生成と整合性を明示する。
- モデル変更とpresentation変更の間でtransportされる情報、失われる情報、obstructionを証明する。
- 過去のDuskin/scaled-horn成果を再利用できる部分と、strict 3/nからは自動的に導けない部分を区別する。

**完了基準:** 選んだモデル内の`(\infty,3)`圏の証人と、strictソースに関する型付き比較・本質的性質のLean定理。Gray圏で代用しない。

## 8. (∞,3)-hyperdescent：最終的な新規証明目標

適切なsite`(\mathcal C,J)`と`(\infty,3)`圏値の文脈系`\mathcal F`を厳密に定義し、任意の対象`U`と対象とするhypercover`U_\bullet\to U`について、

\[
\boxed{\quad
\mathcal F(U)\;\simeq\;
\operatorname*{holim}_{[n]\in\Delta}\mathcal F(U_n)
\quad}
\]

を、使用する高次圏モデルの意味で証明することを目標とします。

必要な区別と義務：

- 普通の`W`局所化・`J`のsheaf・Cat値stack・有限Čech descentと、**hypercover全体に対する高次hyperdescent**は異なる。
- rootからdescent-dataへの比較が`(\infty,3)`-equivalenceであることを、対象側の実効性と高次mapping`(\infty,2)`の同値性の両方で確認する。
- hypercoverのrefinement、presentation変更、localizationに沿う不変性・比較・障害を示す。
- 必要な条件（site、hypercompleteness、modelの存在、局所glue条件等）を**仮定として明記**するか、実際の対象で証明する。条件を空の普遍法則として密輸入しない。

**完了基準:** 独立した`(\infty,3)`-hyperdescent定理、正確な全仮定、非自明なsource例、仮定を外した際の明確なobstructionまたは境界。単なる名前・interface・`sorry`のない公理化では未完了。

## 9. その先：縁起の一般化と「空の空」

この最終目標は、C60についてだけhyperdescentを成立させることではありません。任意に選択した一定のクラスの`(\mathcal C,W,J,H)`について**何が一般的に成立し、何が追加条件に依存し、何が不可能なのか**を証明することです。

- C60以外の文脈とpresentationsにも定理を移し、各適用範囲を明示する。
- 複数presentationの間のtransport/coherence/descentの比較定理を証明する。
- obstructionを消去せず、成立しない条件やnon-liftも一般化の一部として保持する。
- **独立Kuu、strict 3/n圏、`(\infty,3)`-hyperdescentそのものも一つの数学的presentationに相対的**という問いを研究から排除しない。「空の空」を特別な唯一の公理・固定対象に置き換えない。

この一連の数学的成果から中観の哲学全体の「証明」を自動的に結論しません。同時に、哲学的な問いと数学的構成を切り離してしまうのでもありません。

## 10. 実装優先順位、CI、既存成果の保存

**次の証明作業の優先順位（2026-10-29）：F112-P94D3FO（仮称）。** FN [#2687](https://github.com/itakura-hidetoshi/KuuOS/pull/2687)までmainにMERGED。非空全有限AQ語で`old15D=forget∘new15D`（完全AX Total）を証明し、元15D `refl/atom` の同じソース証拠を旧新それぞれの真正17D identityと18D完全reflexive-associatorコードに保持して、旧出力衝突／新出力分離・18D後処理復元不能・異なる2文字非可換欠損の旧消失／新生存を証明。次は**全閉包生成子での比較の正確な可否**と、**旧全kernelの正規生成表示**を検討する。FJ旧非空語no-goとFM新全語忠実性、DS、F45/F54/F55/P92B、真正自然性数3、W/J/H一般理論、strict 3/n・hyperdescent未解決を維持し、Gray圏再導入や独立Kuuを唯一の空とすることを避ける。

**絶対に行わないこと:** Gray圏でstrict 3圏の未証明法則を置換して完了と言うこと、旧約107公開rootの一括削除、歴史的な数学を`legacy/`だけに押し込むこと、strict性を得るために全raw証拠を無条件に潰すこと、未証明の存在条件を新公理へ置くこと、exact-head CIと公理監査を通さず未検証成果をmainに統合すること。

**証明と検証:** `formal/KuuOSFormal.lean`を通常の公開入口として維持。部分ビルドは同一パッケージの開発時の時間短縮だけです。対象ファイル全文・import閉包・mathlib定理・Lean形式の原因を調べ、正本コミットのexact-head CIと`#print axioms`を確認します。共有cacheと重複ジョブ削減を進めても、必要な公理監査・検証を抜きません。

~~~bash
python3 scripts/check_public_proof_roots.py
python3 scripts/run_kuu_foundation_check.py
lake exe cache get   # キャッシュが本当に不足する場合だけ
lake build KuuOSFormal # warningAsErrorはlakefile.toml既定。sorryAxは#print axiomsで確認。
~~~

`KuuOSStrict`は内部import集約にすぎず、旧定理やmathlibを使わない特殊な「空の正本」ではありません。Lean4の証明／runtime／AI入出力／権限・行為／実証データはそれぞれ異なる保証範囲です。

## 11. 継承用の参照先

- [現行README](README.md) — 研究の目的・全体像・成果の入り口
- [旧README v5.291](docs/legacy/README-v5.291.md)、[旧ROADMAP v5.291](docs/legacy/ROADMAP-v5.291.md) — 長い一般的・歴史的証明台帳と原型
- [F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339) — 移行済み履歴（MERGED）。公開正本はmain。
- [F112-P58 #2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421) — raw strict-law obstructionと別の自由path envelope
- [F112-P61 #2426](https://github.com/itakura-hidetoshi/KuuOS/pull/2426) — 水平単位の非strictな自由経路境界
- [F112-P62 #2429](https://github.com/itakura-hidetoshi/KuuOS/pull/2429) — identity-generated typed path relation
- [F112-P63 #2431](https://github.com/itakura-hidetoshi/KuuOS/pull/2431) — genuine left/right typed context free-path functors（9671/9671 Lean SUCCESS）
- [F112-P64 #2432](https://github.com/itakura-hidetoshi/KuuOS/pull/2432) — minimal typed structural-unit quotient category（9672/9672 Lean SUCCESS）
- [F112-P65 #2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434) — two-sided contextual congruence preservation and exact quotient descent（9673/9673 Lean SUCCESS）
- [F112-P66 #2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436) — genuine C60 disjoint-square F54 route objects remain distinct and odd 3-cell survives（9674/9674 Lean SUCCESS）
- [F112-P67 #2438](https://github.com/itakura-hidetoshi/KuuOS/pull/2438) — Type-valued F54 square witness and exact comparison class / noninjective strict-target boundary（9675/9675 SUCCESS）
- [F112-P68 #2439](https://github.com/itakura-hidetoshi/KuuOS/pull/2439) — context-closed squareOnly Type witness and exact F54 class context actions（9676/9676 SUCCESS）
- [F112-P69 #2441](https://github.com/itakura-hidetoshi/KuuOS/pull/2441) — original proof-relevant F55 3-cell package over F54 comparison classes（9677/9677 SUCCESS）
- [F112-P70 #2442](https://github.com/itakura-hidetoshi/KuuOS/pull/2442) — witness-indexed higher-arrow transport and genuine C60 phase change（9678/9678 SUCCESS）
- [F112-P71 #2444](https://github.com/itakura-hidetoshi/KuuOS/pull/2444) — transport quotient and exact original chosen-shadow no-factor theorem（9679/9679 SUCCESS）
- [F112-P72 #2446](https://github.com/itakura-hidetoshi/KuuOS/pull/2446) — chosen-witness shadow correction and two-stage cocycle（9680/9680 SUCCESS）
- [F112-P73 #2447](https://github.com/itakura-hidetoshi/KuuOS/pull/2447) — pentagon integer charge descends through transport quotient（9681/9681 SUCCESS）
- [F112-P74 #2448](https://github.com/itakura-hidetoshi/KuuOS/pull/2448) — integer-linear signed charge descent iff square coefficient zero under true unit-square shift（9682/9682 SUCCESS）
- [F112-P75 #2450](https://github.com/itakura-hidetoshi/KuuOS/pull/2450) — source-history-retaining Type-valued graded transport, unique full charge and true C60 odd increment（9683/9683 SUCCESS）
- [F112-P76 #2451](https://github.com/itakura-hidetoshi/KuuOS/pull/2451) — genuine F55 bridge transport, conditional strict-path coherence, true C60 raw inequality（9684/9684 SUCCESS）
- [F112-P77 #2452](https://github.com/itakura-hidetoshi/KuuOS/pull/2452) — raw Type-valued 4-cell certificates and exact source-witness quotient（9685/9685 SUCCESS）
- [F112-P78 #2453](https://github.com/itakura-hidetoshi/KuuOS/pull/2453) — strictly associative local vertical category on actual raw 4-cell classes（9686/9686 SUCCESS）
- [F112-P79 #2455](https://github.com/itakura-hidetoshi/KuuOS/pull/2455) — original raw F55 horizontal-unit obstruction for P77 four-cell quotient, positive P62-relative witness and physical C60 specialization（9687/9687 SUCCESS）
- [F112-P80 #2457](https://github.com/itakura-hidetoshi/KuuOS/pull/2457) — Type-valued P62-relative horizontal/context unit 4-cell presentation, original source shadow conservation, exact witness quotient and real C60 strict enlargement（9688/9688 SUCCESS）
- [F112-P81 #2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459) — P62-relative P80 source four-cell strict local vertical category, surjective P77→P80 comparison, genuine C60 noninjectivity and no exact free-path readout（9689/9689 SUCCESS）
- [F112-P82 #2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461) — independent source-syntactic Nat invariant conserved by eight P77 and nine P80 Type-valued 4-cell constructors; genuine C60 north-pentagon horizontal counterexample to P80 quotient descent（9690/9690 SUCCESS、axioms 10/10、sorryAxなし）
- [F112-P83 #2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463) — mathlib additive path weight invariant sound for all five P62 congruence generators; actual C60 contextual horizontal counterexample survives original P62 quotient（9691/9691 SUCCESS、公理監査10/10、sorryAxなし）
- [F112-P84 #2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465) — distinct P80 horizontal-four-cell-witness-generated typed path congruence, exact Mathlib quotient, full shadow factorization, P62-to-P84 comparison functor, and strict C60 path quotient enlargement（9692/9692 SUCCESS、公理監査18/18、sorryAxなし）
- [F112-P85 #2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467) — proof-relevant Type-valued horizontal P80 4-cell transport sound for P84 path congruence, full shadow, local strict vertical Category and genuine C60 noninjective P80→P85 comparison（9693/9693 SUCCESS、公理監査18/18、sorryAxなし）
- [F112-P86 #2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469) — P85-witness-generated typed context/pre-post/horizontal P86 path congruence (11 rules) and P86 Type-valued four-cell (12 rules), both original full-shadow sound, exact local quotients, strict local vertical Category, P85 context actions and P85×P85→P86 horizontal descent, genuine C60 contextual witness（9695/9695 SUCCESS、新規公理監査37/37、sorryAxなし）
- [F112-P87 #2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471) — recursively closed proof-relevant P87 Type four-cell grammar and exact typed path congruence, full shadow soundness, strict local vertical Category, self-contained original F55 horizontal P87×P87→P87, genuine horizontal unit certificate and necessary raw interchange shadow equation（9698/9698 SUCCESS、公理監査39/39、sorryAxなし）
- [F112-P88 #2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473) — independent noncommutative original F55 source-word invariant, exact P87 Type-valued interchange four-cell nonexistence and quotient inequality for typed nonunit middle factors, true C60 primitive-word checks（9700/9700 SUCCESS、公理監査18/18、sorryAxなし）
- [F112-P89A #2475](https://github.com/itakura-hidetoshi/KuuOS/pull/2475) — alternate genuine Type-valued interchange four-cell presentation, 13 generator full-shadow proof, exact quotient and P87→P89 surjection, P88 word non-preservation（9701/9701 SUCCESS、公理監査10/10、sorryAxなし）
- [F112-P89B #2476](https://github.com/itakura-hidetoshi/KuuOS/pull/2476) — strict local vertical Category, self-closed original F55 horizontal, genuine horizontal unit, strict interchange on four arbitrary P89 quotient classes, conditional strict P87→P89 enlargement（9702/9702 SUCCESS、公理監査13/13、sorryAxなし）
- [F112-P90A #2478](https://github.com/itakura-hidetoshi/KuuOS/pull/2478) — arbitrary-depth original F45 triple bracketing nonidentity, exact ordered sectors, genuine F54 one-rotation associator, north C60 example（9703/9703 SUCCESS、axioms 7/7）
- [F112-P90B #2479](https://github.com/itakura-hidetoshi/KuuOS/pull/2479) — exact triple-route associator naturality source paths, equal primitive counts but distinct F54 tags, unfilled Type-valued F55 comparison slot（9704/9704 SUCCESS、axioms 7/7）
- [F112-P91A #2481](https://github.com/itakura-hidetoshi/KuuOS/pull/2481) — nine original F55 generators conserve source F54 rotation-count difference as pentagon charge; P90 naturality slot has necessary zero pentagon charge and original square-parity shadow（9705/9705 SUCCESS、公理監査4/4）
- [F112-P91B #2482](https://github.com/itakura-hidetoshi/KuuOS/pull/2482) — full original F55 Type-witness route-object quotient with exact kernel, P67 comparison surjection, pentagon 3-vs-2 rotation-count non-descent, P90 unfilled naturality slot exact equality iff existence（9706/9706 SUCCESS、公理監査13/13）
- [EX #2663](https://github.com/itakura-hidetoshi/KuuOS/pull/2663)・[EY #2664](https://github.com/itakura-hidetoshi/KuuOS/pull/2664)・[EZ #2665](https://github.com/itakura-hidetoshi/KuuOS/pull/2665)・[FA #2666](https://github.com/itakura-hidetoshi/KuuOS/pull/2666) — 完全18D欠損の非可換積、有限19D候補・正規閉包・相対商、真正DV文脈輸送と生成子別障害。
- [FB #2667](https://github.com/itakura-hidetoshi/KuuOS/pull/2667)・[FC #2668](https://github.com/itakura-hidetoshi/KuuOS/pull/2668) — 元pentagon自由群証拠のDV輸送後非自明性、選択DX商、完全コード/自由群核のexact iff。
- [FD #2669](https://github.com/itakura-hidetoshi/KuuOS/pull/2669)・[FE #2670](https://github.com/itakura-hidetoshi/KuuOS/pull/2670) — 17D対象文脈fiber衝突と18D反射的associatorコード、2文字核、単独frame条件。
- [FF #2671](https://github.com/itakura-hidetoshi/KuuOS/pull/2671) — 実17D raw証拠の等式反映と完全18D対象単射性の明示的条件。
- [FG #2672](https://github.com/itakura-hidetoshi/KuuOS/pull/2672) — 18D全コードと固定端点generator gate・3構成子セクターの正確な同値、異種セクター衝突の排除、元17D `assoc/pre/post`経路引数単射性（9947/9947 Strict Lean SUCCESS、39 Checks SUCCESS / 1 SKIPPED）。
- [FH #2674](https://github.com/itakura-hidetoshi/KuuOS/pull/2674) — 条件付き可変inner-generator反映（9948/9948 Strict Lean SUCCESS）。
- [FI #2675](https://github.com/itakura-hidetoshi/KuuOS/pull/2675) — 全再帰構成子列保存と全DV核の非可換spine-kernelへの包含（9949/9949 Strict Lean SUCCESS）。
- [FI 完全反映 #2676](https://github.com/itakura-hidetoshi/KuuOS/pull/2676) — 元18D生成子全帰納法、`Injective(f_w) ↔ Injective(C_w) ↔ Injective(τ_w)`、全有限文脈と2 singleton frameの同値（9950/9950 Strict Lean SUCCESS、5 Checks SUCCESS / 1 SKIPPED）。
- [FJ #2679](https://github.com/itakura-hidetoshi/KuuOS/pull/2679) — 真正物理AQ15D保守的`refl/atom`のType値衝突、17D文脈・全18D非可換自由群への伝播、`Injective(τ_w) ↔ w=[]`、全非空wの共通2文字核（9951/9951 Strict Lean SUCCESS）。
- [FK #2681](https://github.com/itakura-hidetoshi/KuuOS/pull/2681) — 元の14D境界を保つ15D構成子保存whiskering、元14D raw作用単射性、旧輸送への忘却因子化、逆復元不能性、FJ証拠の全有限語保存（9952/9952 Strict Lean SUCCESS、12 Checks SUCCESS / 1 SKIPPED）。
- [FL #2683](https://github.com/itakura-hidetoshi/KuuOS/pull/2683) — 元14D境界を維持するFKの構成子保存15D全Homファイバー単射性、全有限AQ文脈単射性、代替frame `onCell`単射性（9953/9953 Strict Lean SUCCESS、40 Checks SUCCESS / 1 SKIPPED、Governance SUCCESS、`sorryAx`なし）。
- [FM #2685](https://github.com/itakura-hidetoshi/KuuOS/pull/2685) — FK/FL別frameから真正17D・18D非可換完全輸送へ単射性を転送。9954/9954 Strict Lean SUCCESS、40 Checks SUCCESS / 1 SKIPPED、Governance SUCCESS、`sorryAx`なし。
- [FN #2687](https://github.com/itakura-hidetoshi/KuuOS/pull/2687) — 完全15D AX Totalと選択17D/18D Type値ペアの新旧相対比較、全非空語忘却因子化、18D no-recovery、非可換2文字欠損対照（9955/9955 Strict Lean SUCCESS、40 Checks SUCCESS / 1 SKIPPED、Governance SUCCESS、`sorryAx`なし）。
- [FO #2689](https://github.com/itakura-hidetoshi/KuuOS/pull/2689) — `ker(FreeGroup.map f)`＝全コード衝突差語の正規閉包、元の完全18D輸送の全核正規表示・受信器因子化判定、旧FJ核非自明／新FM核自明（9956/9956 Strict Lean SUCCESS、Governance SUCCESS、11新規定理・標準3公理のみ）。
- [FP #2690](https://github.com/itakura-hidetoshi/KuuOS/pull/2690) — `FreeGroup(A)/N≃*im(τ)`、真正DV輸送像上の受信器一意因子化、標的全射時の一意性と非全射での非一意反例、FJ/FM境界を保持（[Strict Lean #40869674642](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40869674642) 9032 scoped jobs SUCCESS、Governance 30/30完了、11宣言の標準3公理監査、sorryAxなし）。
- [FQ #2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692) — 真正完全18Dの像ファイバー根付き生成系、元`assoc/post/pre`の完全衝突集合3セクター分解、根付き商≃実像、3セクター受信器一致 iff 像上の一意降下をLean形式化。[Strict Lean #40872152257](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40872152257) 9033 scoped jobs SUCCESS、13公理監査は標準3公理のみ、Governance 30/30 completed SUCCESS、warning/error 0/0、sorryAxなし。
- [`AGENTS.md`](AGENTS.md) — 現行のpublic root・mathlib・Gray依存・ビルド境界
- [`formal/KUOS/`](formal/KUOS/) — 過去から継続する一般的なLean数学
- [`formal/Kuu/`](formal/Kuu/) — 現在の独立Kuuの具体的な構成

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
