# KuuOS / 空OS — Formal Research Roadmap

**更新：2026-10-30 JST。最新のLean統合段階は F112-P94D3GJ2 / [PR #2730](https://github.com/itakura-hidetoshi/KuuOS/pull/2730) MERGED。** 定理squash SHA `3d0ec687d9e73784b13e9b6cfccb4754b13e692a`、PR exact-source HEAD `1b90257bb2f989c248014d5f0730b075ea38b447`、source/merge-test差分ファイル0。[Strict Lean/Governance #41050927061](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41050927061) **3695/3695 scoped SUCCESS**、Governance **5/5ジョブcompleted SUCCESS**、新規15宣言の公理依存は標準`propext`・`Classical.choice`・`Quot.sound`以内（無公理2件）、`sorryAx`なし、変更Lean warning/error **0/0**。GJは真正二本の元F54経路と元F55 pentagon/square原始証拠、GJ2は独立F112の真正元F55 `PresentedCell`**全9構成子**を元Type値のまま有限コードに保持。D/E objects、全Blocks、途中F45 Tree、両Nat深さ、途中F54経路・F55 3-cell履歴の型不一致を拒否する部分復号および厳密左逆を完成。一般D/Eで対象と**各HomファイバーのCountable**を前提に全元F55総体とindexed fiber Countableを証明、実C60 Site×Siteと全Polygonは無条件。ただし別定義`NativeF55StructuralComparison`、歴史的P92B/F55との型付き同型、真正元14D Countable、19D filler、global higher descentは未証明。

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
| 現在のF112検証範囲（2026-10-30） | **F112-P94D3GJ2 [#2730](https://github.com/itakura-hidetoshi/KuuOS/pull/2730)までmain統合済み。** 定理SHA `3d0ec687d9e73784b13e9b6cfccb4754b13e692a`、Strict Lean **3695/3695 scoped SUCCESS**、Governance 5/5、GJ2新規15宣言は標準3公理以内で`sorryAx`なし。GF:元Path/Blocks、GG:元OneStep/AxisTrace、GH:元F45 Tree、GI:元LocalRotation・Edge・Chain・DepthRoute、GJ:元F55 pentagon/square生成子、GJ2:**本来の独立F112 PresentedCell全9構成子の完全原証拠Countable**。一般D/Eの対象・各Hom可算性を明示し、実C60 Site×Siteでは無条件。GDの旧FJ exact`ℵ₀`が要求する元14D Countableは未証明。 |
| F112以前の確認範囲（2026-10-23時点の履歴） | **P91Bまでmain統合済み（当時）**。P89B：9702/9702・13/13公理監査、P90A：9703/9703・7/7、P90B：9704/9704・7/7、**P91A：9705/9705・4/4**、**P91B：9706/9706・13/13**。新規`sorryAx`なし、変更ファイルLeanエラー/警告0、107公開root保全、exact-head Governanceとcompletion receipts 2/2 SUCCESS。P91A統合SHA `153361ebc9bf4303ed9c79e931c768fc99a885af`、P91B統合SHA `8fd61aad78943f6c9c630a585450eac2b5246f90`。唯一の公開入口`KuuOSFormal`に両モジュールを直接import。 |
| 既存定理の証拠 | 実際のLean宣言・型と仮定・`#print axioms`・対応するexact-head CI。`sorryAx`、`sorry`、`admit`、新たな未証明公理による補完は禁止。 |
| 数学的区別 | raw Type-valued証拠、Prop証明、選択した商、観測、物理的解釈は互いに無条件には同一視しない。 |
| 公開入口・toolchain | `lake build KuuOSFormal`（`lake build`も同じ）。既存107公開rootは維持。Lean `v4.30.0-rc2`、pinned mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。 |
| 別レーン | PR #1558（Lean 4.31）はvalidation-only、Draft・未マージ。Lean/mathlibの正式な固定環境は上記のまま。 |

GitHub正本・Lean成果・README/ROADMAP・CI・歴史的スナップショットには異なる役割がある。**GJ2までの正本統合はMERGED SHA・exact-source HEAD Strict Lean/Governance SUCCESS・source/merge-test差分ファイル0で確認済み**。GJ2（3695 scoped）、GJ（3693）、GI（3692）、GH（3689）、GG（9049）、GF（9048）等はそれぞれ独立のexact-source CI receipt。有限C60 Site×SiteにおけるF55 PresentedCell Countableから任意D/E Homの可算性、真正元14D Type値fiberの無条件可算性、歴史的P92B/F55との同型は導けない。strict空中心、独立Kuuを一つのpresentation、Gray非再導入を維持。

## 0A. 2026-10-30現在の証明フロンティア：EX–GJ2

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
| FR / [#2694](https://github.com/itakura-hidetoshi/KuuOS/pull/2694) | FIの完全再帰spine不変性を用い、元の18D完全コードの全衝突対集合を任意有限の同一`post/pre/.../assoc`構成子列の局所衝突族の和集合に**厳密分解**し、FOの全核がこれらすべての局所衝突差語の正規閉包であることを証明。FQファイバーrootは完全spineを保存、根付き全関係も完全spineに分割され全核を生成。受信器はspine内の全衝突で一致することと実DV像への一意な因子化が同値であり、各sourceコードとその根との一致だけでも必要十分。FHの真の依存型内側コード抽出で固定17D境界の外側`post/pre`衝突→輸送された内側18Dコード一致、対偶の内側不一致→外側非衝突を無条件に証明。9034 scoped Strict Lean SUCCESS、12公理監査、Governance SUCCESS | 完全spineはraw17D引数や境界等号まで記録せず、同一spine内の衝突の完全な幾何学的分類は未証明。生成系の有限・独立・最小性、FJ既知1元による全核生成、元の幾何的19D Type値充填も未証明 |
| FS / [#2696](https://github.com/itakura-hidetoshi/KuuOS/pull/2696) | 元の完全18Dの**任意深さの再帰spine**と、実際に輸送された始域・終域（元17D raw pathを含む）および全`post/pre`内側の依存型18D完全コードを保持するboundary keyを新設。全実コード衝突が同一キーに局所化すること、同一キー内の**実衝突差語集合**の正規閉包＝全DV FreeGroup核、異なるキーでは実2文字核所属不能、実像上の受信器一意降下 iff 全キー内衝突一致を証明。FQのrooted relationsをさらに**元文字≠根の非恒等関係だけ**へ縮約しても任意 `FreeGroup.map f` の全核正規閉包は不変。非自明根付き元が有限なら有限正規生成となり、元文字型が有限な場合はその十分条件を充足。9035 scoped Strict Lean SUCCESS、14公理監査／Governance SUCCESS | **境界キー一致⇒完全コード像一致は未証明**。元物理C60完全18Dに対する有限なactive supportは未証明。生成族の独立性・最小性・単一FJ欠損の全核生成・元の真正19D Type値幾何充填は未証明 |
| FT / [#2698](https://github.com/itakura-hidetoshi/KuuOS/pull/2698) | 真正context-CLOSED 18D依存型生成子コードの完全復元：元17D raw `trans(trans f g)h` に格納した3本の経路と依存型端点で`assoc`を復元し、`post/pre`は完全内側18D受信コードと始域raw `trans` に保持された後置／前置17D経路から復元、再帰構成子spineで異種セクターを厳密分離。これによりFS境界キーの**無条件単射性**、真正元DV完全コードの**像一致 iff キー一致**を証明。元の非可換全核＝境界キー等号だけによる最小正規閉包、受信器の**実像**上一意因子化 iff キー等号を尊重すること、元ファイバー根等号 iff キー等号をLean証明。9036 scoped Strict Lean SUCCESS、11公理監査（うち受信コード復元とキー同値7宣言は無公理）、Governance 30/30 SUCCESS | 真正受信コードの復元は**元source17D raw証拠の復元ではない**。FJ旧物理frameの全有限非空文脈の非忠実性は残る。有限active support、正規生成系の最小・独立性、単一FJ欠損での全核生成と元の幾何19D充填は未証明 |
| FU / [#2700](https://github.com/itakura-hidetoshi/KuuOS/pull/2700) | 元の真正DR依存型18Dアルファベットで、各17D元対象`a`について`(.post)^n (.assoc refl refl refl)`を実際に生成し、全nで元の17D証拠保持・元コード単射と全再帰深さ`n+1`を証明。元17Dの真のAQ context-object衝突から任意nで異なる元18Dコードが実DV受信完全コード像で一致することを、FTの受信`post`内側コード/suffix等式と依存型に沿って証明。旧FJ物理15D `conservative refl`対`atom`を実例化し、**全非空物理AQ文脈で、各深さに根付き代表元と異なる元コードが存在**。その元コードを深さ別に選びNat→実際のactive root source型の単射を作り、**真正物理FJの非自明rooted字母Subtypeが無限**とLean証明。9037 scoped Strict Lean SUCCESS、11宣言公理監査（うち塔の元source単射・深さ・衝突の5宣言は無公理） | **無限active-root字母の存在だけでは核の有限正規生成は否定していない**。別の有限群語族が正規閉包として全核を生成する可能性の排除、最小独立正規ランク、単一FJ欠損全核生成、真正19D幾何充填は未証明 |
| FV / [#2702](https://github.com/itakura-hidetoshi/KuuOS/pull/2702) | 真正非可換自由群写像 `FreeGroup.map f` の**全kernelの有限正規生成 iff 非自明な像ファイバーrootと異なる元文字集合が有限**を証明。任意の全群語を4ケース自由群帰納法で有限の元文字支持に局所化し、任意有限個の群語の支持和集合は有限。支持外の非自明rooted核relatorを選び、特定の1 source字母だけ+1、その他0となる整数座標`FreeGroup.lift`群準同型で検出する。この準同型は任意の有限関係語とその**全正規閉包**を消す一方、選択したrooted核relatorを消さない。よって有限の任意群語ではkernel全体を正規生成できない。実DV18D版の厳密同値とFUの真正物理全非空文脈無限active根付き字母を接続し、**旧FJの全非空有限物理AQ文脈で元18D DV全核は非有限正規生成**。9038 scoped Strict Lean SUCCESS、10公理監査、Governance SUCCESS | 元noncommutative source kernelはそのまま。**最小正規生成数の正確な濃度・独立basisは未証明**。単一FJ欠損全kernel生成、真の19D Type値幾何充填・global strict n / hyperdescentも未証明 |
| FW / [#2704](https://github.com/itakura-hidetoshi/KuuOS/pull/2704) | 選択FQ像ファイバー根の冪等性・非active性、FV整数座標の**active根付き差語対角+1／非対角0**、任意の添字集合Tが根付き関係語で全kernel正規生成 iff `D_f⊆T` をLean証明。各active根付き関係語は他の全rooted関係語のnormal closureに属さず、全FS rooted familyは非冗長・単射。さらに任意の全kernel正規生成集合Rは全active元字母の座標を検出し、FV有限元字母支持を集計して**全核可算正規生成 iff `D_f` 可算**を証明。9039/9039 Strict Lean SUCCESS、12宣言公理監査、Governance 30/30 SUCCESS | 真正18D元Type値証拠と非可換自由群は不変。rooted familyの非冗長性を**任意群語生成族の正確な最小Cardinal**や核自身の自由基底と同一視しない。旧FJ物理active sourceの可算性、既知FJ単一欠損から全核を正規生成する定理、幾何的19D filler・global strict/hyperdescentは未証明 |
| FX / [#2706](https://github.com/itakura-hidetoshi/KuuOS/pull/2706) | 元の非可換自由群に対し、active元文字を基底にする有理数有限支持自由加群 `D_f→₀ℚ` への群準同型を構成。rooted差語は正確に標準基底に移る。全核を正規生成する任意の群語Rが、その座標像の線形spanで割った商空間を零化するため、全標準基底が元のspan内に入り、spanは全自由加群と等しい。**mathlib自由加群rankと生成span rankの上界から`#D_f≤#R`を有限・無限の全濃度で証明**。FWの根付き差語族単射性により `#R₀=#D_f` の上界を実際に達成し、**全kernelの最小正規生成Cardinal＝`#D_f`**を形式化。9040/9040 SUCCESS・7公理監査・Governance 30/30 SUCCESS | 座標像だけが可換で、元のsigned非可換自由群・Type値18D証拠は不変。旧FJ真正物理元文字の可算／非可算・元kernel自身の自由基底・既知1欠損による全核生成・真正幾何19D充填・global strict/hyperdescentは別の未証明問題 |
| FY / [#2708](https://github.com/itakura-hidetoshi/KuuOS/pull/2708) | FQ image-root代表元を保持し、元source文字型の**厳密同値 `A ≃ D_f ⊕ Set.range f`**、同一universeの**Cardinal和 `#A=#D_f+#(range f)`**、元source可算 iff `D_f`と実受信像が共に可算、をLeanで証明。元の真正旧FJ物理18D complete DV元コードTypeに型同値・濃度・可算性を実際に特殊化。FUの非空物理AQ文脈におけるactive字母無限性とFX exact最小正規生成Cardinalを接続し、**原18D sourceコード型がCountableという明示的仮定の下で**最小正規生成濃度`ℵ₀`を確立。9041/9041 Strict Lean SUCCESS、10定理の標準3公理以内監査、Governance 30/30 SUCCESS | 元14D–17Dの依存型証拠・Category Homの濃度は任意であり、有限C60幾何からCountableを無条件に導かない。原18D可算性の実際の十分条件と証明は次FZ。元核自身の自由基底・真正19D幾何充填・global strict/hyperdescentは未証明 |
| FZ / [#2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710) | 元17D対象のCountable・各raw17D `NativeC60AXStep`証拠ファイバーのCountableから、元の依存型raw17D path totalおよび真正18D layer object TypeのCountableを形式化。元18D `assoc/post/pre`生成子の各依存型ファイバーがCountableなら完全original 18D Type値source文字もCountableとなる。真正FJ物理モデルにその条件を具体化し、FUのactive無限性・FXのexact NormalRankによって、全非空AQ文脈の全非可換kernelの最小正規生成Cardinal`ℵ₀`を証明。受信像Countableかつactive無限の一般写像と物理モデルでは、**元source TypeがCountable iff exact`ℵ₀`正規生成表示が存在**。さらに受信像Countableで元source非可算ならactiveも非可算という障害を証明。9042/9042 Strict Lean SUCCESS、FZ9公理監査、Governance 30/30 SUCCESS | 下位raw証拠と18D recursive `assoc/post/pre`証拠ファイバーの可算性は明示的な前提であり、既存の依存添字付き帰納型に対する自動`Countable`導出は成立していない。真正input Category Homの濃度を勝手に仮定せず、次段GAで有限文法からの可算性伝播を証明する。元kernel自由基底・幾何19D filler・大域strict/hyperdescentは未証明 |
| GA / [#2712](https://github.com/itakura-hidetoshi/KuuOS/pull/2712) | 原`NativeC60AXStep`の`atom/refl/symm/trans`全有限構文木を、真の元source端点＋元証拠Genトークンを保持して符号化。部分復号は原dependent AXStep Sigmaへ戻り、不適合な合成は拒否。`decode(encode(p))=some(p)`を任意raw証拠に対し帰納証明。原layer object・各primitive GenファイバーのCountableから元raw proof total・全indexed pathファイバーのCountableを証明。有限Bool文脈閉包16D Gen・元raw16D・DQ17D object・元triangle17D Gen・元raw17D pathをすべて元lower AX primitive可算性から証明。真正旧FJ物理18Dに適用し、残る18D `assoc/post/pre` Genファイバー可算という明示条件下、全非空AQ文脈で元全核の最小正規生成Cardinal`ℵ₀`を確立。9968/9968 Strict Lean SUCCESS、13定理の標準3公理監査、Governance 3/3 selected SUCCESS | `assoc/post/pre`全再帰生成子ファイバーのCountableは未証明の明示的な前提。有限C60幾何・元入力category HomのCountableを暗黙に推論しない。元kernel自由基底、真の幾何19D filler、local/global strict高次構造・hyperdescentも未証明。別FK–FM忠実presentationを旧FJと同一視しない |
| GB / [#2714](https://github.com/itakura-hidetoshi/KuuOS/pull/2714) | 元18Dの`assoc/post/pre`再帰生成子を、元raw17D source/targetと元全証拠を保持する有限木へ符号化。部分復号器は型不一致のwhiskeringを拒否し、**任意の元18D生成子rで`decode(encode(r))=some(元source,target,r)`**と帰納法で証明。元raw17D証拠total Countableから**元18D再帰Gen total・全indexedファイバーCountable**を導出。GAの元lower AX primitive object/Gen Countable ⇒ 元16D閉包 ⇒ 元17D三角・raw paths Countableと連鎖させ、**元の完全18D source alphabet Countableが下位2条件だけから成立**。真正旧FJ物理18D非空全AQ文脈で最小正規生成Cardinal`ℵ₀`を同じ条件のみで証明。9044/9044 scoped Strict Lean SUCCESS、6定理の標準3公理監査、Governance 30/30 SUCCESS | 任意inputカテゴリー・元14D–15D型のCountableは無条件ではない。真正元lower AX base object totalと各primitive Genファイバーの可算性を実際の選択物理証拠型に対して証明できるかは次GC。旧FJ非忠実／別FK–FM忠実の区別、元kernel自由基底、幾何的19D充填、global strict/hyperdescentは未証明 |
| GC / [#2716](https://github.com/itakura-hidetoshi/KuuOS/pull/2716) | 実物理K5のprimitive `Gen x y`は元15D sourceと全元14D境界を保持したまま、Prop値endpoint等式だけを忘れる**AX base Totalへの単射**を持つ。従って**`Countable (nativeK5AXBaseLayer W).Total`だけで全元primitive GenファイバーCountable**。同前提で元完全18D source可算および旧FJ全非空AQ非可換核のexact最小正規生成Cardinal`ℵ₀`。元14D fiberと各indexed15D証拠fiber Countableからbase Total Countableも証明。9045/9045 SUCCESS・5公理監査・Governance 30/30 SUCCESS | 下位14Dおよび元15D証拠の可算性は前提。無条件の任意input Category Hom Countableを宣言しない |
| GD / [#2717](https://github.com/itakura-hidetoshi/KuuOS/pull/2717) | 元conservative 15D`atom/refl/symm/trans`と元AQ indexed 15D`conservative/exchange/symm/trans`を、**全元Type値証拠と依存型端点・元`List Bool` exchange添字を保存**して有限符号化。部分復号は不整合な合成を拒否し、任意の元dependent15D証拠に`decode(encode p)=some⟨(source,target),p⟩`をLean帰納証明。原core総体・元family総体・全indexed 15D証拠ファイバーを、原14D fiber CountableだけからCountableと証明。GC/GB/GAを合成し、**元14D fiber Countable ⇒ original AX Totalと完全18D source Countable ⇒ 旧FJ非空AQ全核 exact最小正規生成Cardinal`ℵ₀`**。9046/9046 Strict Lean SUCCESS・9公理監査標準3公理のみ・Governance 30/30 SUCCESS | **元14D Type値証拠fiber自身および任意source Category Homの可算性は未証明**。自由群核の自由基底・真正19D filler・大域strict/hyperdescentは独立未証明 |
| GE / [#2719](https://github.com/itakura-hidetoshi/KuuOS/pull/2719) | 元の真正F112物理C60のDart 60・Edge 90・Polygon 32・Site 182、すべての元Site incidence HomのCountable、元の依存型Zigzag全ファイバー＋full source/target total、およびC60 polygon bracket tree・typed primitive rotation・raw route＋full endpoint totalのCountableを証明。**有限のC60添字だけでなく任意有限長の元raw構文**を保持。9047/9047 Strict Lean SUCCESS、12公理監査標準3公理以内、Governance 30/30 | 元14D直接derivingは実7D–13D証拠のCountableインスタンスが未確立で失敗。今回GEで元14D Countableを宣言しない。sourceカテゴリーHomと原下位証拠の正確な条件がGF以降の課題。 |
| GF / [#2721](https://github.com/itakura-hidetoshi/KuuOS/pull/2721) | 元のsource/target・全実カテゴリーHomを保持する`KuuNativePath`と、各原射列に加え空blockを含む独立した原分割を保存する`KuuNativeBlocks`について、可算Objと全Hom可算を前提に有限構文符号化・部分依存型復号・厳密左逆、full original totalと全indexed fiber Countableを証明。**実F112 C60 `Site`についてはGEが証明済みのCountable/Homを使ってpath/blocksおよび元の独立二軸`PolygonNativeDualAxisFrame`全sector総体Countableを無条件に形式化**。9048/9048 Strict Lean SUCCESS、13宣言標準3公理監査、Governance 30/30 SUCCESS | 元7D–13Dの比較証拠・F45/F55・14D fiberおよび任意D/EカテゴリーHomのCountableは未証明。flattened pathと原block分割を同一視せず、旧FJ／別FK–FMの区別を保持。 |
| GG / [#2723](https://github.com/itakura-hidetoshi/KuuOS/pull/2723) | 元の`KuuNativeOneStep`三構成子（`split/insertNil/whisker`）と`KuuNativeAxisTrace`任意有限深さ（`refl/snoc`）を、全元カテゴリーHom・本当の中間Blocks・全始域終域・Nat深さ・全元Type値証拠を保存する有限コードへ符号化。型不整合なcompositionを拒否する部分復号と`decode∘encode`厳密左逆をLean証明。一般カテゴリーで**対象可算・各Hom可算を明示仮定**して元OneStep／AxisTrace totalと全indexed fiber Countable。実C60 SiteについてGE/GFから無条件に導出。**9049/9049 Strict Lean SUCCESS、12標準3公理監査、Governance 30/30 SUCCESS** | 元F45 Tree、F55、7D～14D Type値証拠のCountableは未証明。一般カテゴリーD/EのHomは有限C60から無条件に可算にならず、旧FJ exact`ℵ₀`の元14D Countable条件を保持。 |
| GH / [#2725](https://github.com/itakura-hidetoshi/KuuOS/pull/2725) | 真の元`KuuNativeF45Tree` `refl/leaf/node`について、実C60 sector・二種類の実行順序・独立D/Eカテゴリーの元AxisTrace・全中間Blocks・Nat深さ・完全bracketingを保持する有限再帰符号化。依存型不整合を拒否する部分復号／indexed全境界検査／厳密左逆。元Obj/Homが可算な一般D/E下で全F45元Type値totalと各fiber Countable、実C60 `Site×Site`と全Polygonで無条件。**3689/3689 scoped Strict Lean SUCCESS、8標準3公理監査、Governance gate SUCCESS** | 元`DepthRotationRoute`、F55、7D～14D全証拠型のCountableと任意D/E Homは未証明。GDの旧FJ exact`ℵ₀`に必要な元14D条件は残る。 |
| GI / [#2727](https://github.com/itakura-hidetoshi/KuuOS/pull/2727) | 元`KuuNativeF45Tree`の完全証拠を使い、元`LocalRotation`3構成子、`RotationEdge`の正逆、有限`RotationChain`の全構成子、`DepthRotationRoute`5構成子を元Type値境界・中間Tree・Nat輸送を保持して忠実に符号化。型不整合を拒否する部分復号と厳密左逆、一般D/E Obj・全Hom fiber可算条件下で全原total/fiber Countable。実C60 Site×Siteと全Polygonへ無条件特殊化。**3692/3692 scoped Strict Lean SUCCESS、24標準3公理以内監査、Governance 5/5 SUCCESS** | 元F55 PresentedCell/StructuralComparison、元4D～14Dの完全証拠可算性、任意D/E Hom可算性および旧FJ exact`ℵ₀`の14D条件除去は未証明。 |
| GJ / [#2729](https://github.com/itakura-hidetoshi/KuuOS/pull/2729) | 並行する2本の元F54 Type値経路、元F55のpentagon（4つの完全F45 stage）・disjointSquare（2つの完全LocalRotation）を全証拠保持のまま可算化。**3693/3693 scoped Strict Lean SUCCESS、11宣言公理監査、Governance SUCCESS** | 残る7再帰構成子はGJ2で閉じた |
| GJ2 / [#2730](https://github.com/itakura-hidetoshi/KuuOS/pull/2730) | 独立F112の元`KuuNativeF45Tree.DepthRotationRoute.PresentedCell`9構成子を**完全な原Type値F45/F54/F55歴史・D/E二軸・全Blocks・両Nat深さ**保存の有限コードへ符号化。途中F54 raw証拠・中間F45 Treeの一致まで検査する部分復号、厳密`decode(encode c)=some⟨元境界,c⟩`、一般D/EのObj・各Hom可算条件下で元F55証拠総体・各indexed fiberのCountable、実C60 Site×Site／全Polygonで無条件可算。**3695/3695 scoped Strict Lean SUCCESS、15宣言公理監査、Governance 5/5 SUCCESS** | 別定義`NativeF55StructuralComparison`、歴史的P92B/F55同型、元4D～14D証拠Countableは未証明 |

主な正本Leanソース：

- [FC: CompleteCodeFiberKernel](formal/Kuu/F112/PolygonNativeC60AQFullPentagonCodeFiberKernel.lean)、[FD: SeventeenContextFiberObstruction](formal/Kuu/F112/PolygonNativeC60AQFullPentagonSeventeenContextFiberObstruction.lean)、[FE: SeventeenExactFiberGate](formal/Kuu/F112/PolygonNativeC60AQFullPentagonSeventeenExactFiberGate.lean)。
- [FF: RawSeventeenPathReflection](formal/Kuu/F112/PolygonNativeC60AQFullPentagonRawSeventeenPathReflection.lean)、[FF: EighteenObjectReflectionGate](formal/Kuu/F112/PolygonNativeC60AQFullPentagonEighteenObjectReflectionGate.lean)。
- [FH: RecursiveGeneratorReflection](formal/Kuu/F112/PolygonNativeC60AQFullPentagonRecursiveGeneratorReflection.lean)、[FI: DeepConstructorSpineObstruction](formal/Kuu/F112/PolygonNativeC60AQFullPentagonDeepConstructorSpineObstruction.lean)。
- [FJ: PhysicalWhiskerNoninjectivity](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalWhiskerNoninjectivity.lean) — 実物理AQ `conservative(refl/atom)` 構文衝突、全非空有限文脈での非単射性、共通の非自明2文字欠損。
- [FK: ConstructorPreservingWhisker](formal/Kuu/F112/PolygonNativeC60AQFullPentagonConstructorPreservingWhisker.lean) — 14D境界一致の別15D輸送、原保守的構成子履歴の保存、旧輸送への厳密忘却因子化、有限文脈でのFJ証拠分離。
- [FL: FullDependentWhiskerReflection](formal/Kuu/F112/PolygonNativeC60AQFullPentagonFullDependentWhiskerReflection.lean) — 保守的4構成子・独立exchange・外側2構成子の全依存型Hom等式反映、可変中間14D Sigma復元、任意有限文脈と代替frame onCell単射性。
- [FM: AlternativeFullFaithfulness](formal/Kuu/F112/PolygonNativeC60AQFullPentagonAlternativeFullFaithfulness.lean) — 真正15D `mapTotal`・全有限AQ文脈、17D閉包raw16D証拠の全構成子反映、元18D完全コード・非可換自由群輸送の全有限語単射性、自明核。
- [FN: OldNewTypedFaithfulnessComparison](formal/Kuu/F112/PolygonNativeC60AQFullPentagonOldNewTypedFaithfulnessComparison.lean) — 全15D構成子忘却の冪等性／自然性／非空語因子化、新旧別17D・18D選択Type値証拠ペアの衝突対照・復元不能、旧／新非可換欠損の消失／生存。
- [GC: PhysicalLowerAXCountability](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalLowerAXCountability.lean) — 元base Totalから元primitive Gen全fiberのCountableと旧FJ exact `ℵ₀`。
- [GD: PhysicalFifteenSyntaxCountability](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalFifteenSyntaxCountability.lean) — 元15D構文の忠実reificationと元14D fiberからの完全18D source Countable。
- [FO: CompleteKernelNormalClosure](formal/Kuu/F112/PolygonNativeC60AQFullPentagonCompleteKernelNormalClosure.lean) — 任意FreeGroup.mapの全コード衝突差語正規閉包による全核等式、真正18Dの非可換核判定・受信器降下条件・FJ旧核とFK/FM別核の厳密比較。
- [FP: CompleteKernelImageFirstIsomorphism](formal/Kuu/F112/PolygonNativeC60AQFullPentagonCompleteKernelImageFirstIsomorphism.lean) — 原の18D全核正規商と実DV輸送像の群同型、代表元可換性、実像上受信器の一意因子化、全射の場合の標的拡張一意性と非全射反例。
- [FQ: RootedSectorKernelClassification](formal/Kuu/F112/PolygonNativeC60AQFullPentagonRootedSectorKernelClassification.lean) — FO全衝突核から像ファイバー根代表元への正規生成縮約、真正18D `assoc/post/pre` 衝突3族の厳密和集合分解、根付き同型と3セクター受信器降下 iff。
- [FR: RecursiveSpineKernelLocalization](formal/Kuu/F112/PolygonNativeC60AQFullPentagonRecursiveSpineKernelLocalization.lean) — 元の完全18D再帰構成子列による真の全衝突群・根付き生成族の正規核分割、像上受信器のspine別・根付き降下必要十分条件、FHの元依存型`post/pre`内側像による外側衝突障害。
- [FS: BoundaryKeyFiniteNormalGate](formal/Kuu/F112/PolygonNativeC60AQFullPentagonBoundaryKeyFiniteNormalGate.lean) — 元の全再帰spine、実輸送17D raw境界・内側post/pre完全18Dコードからなる依存型boundary key、同一キー衝突の全核正規閉包と相違障害、非自明root-relator supportによる厳密全核表示および有限支持なら有限正規生成の条件付き定理。
- [FT: ClosedBoundaryKeyExactReflection](formal/Kuu/F112/PolygonNativeC60AQFullPentagonClosedBoundaryKeyExactReflection.lean) — 真正context-CLOSED 18D生成子のType値raw17D始域/終域・inner post/preからの完全復元、FS boundary keyの単射性、元DVコード像一致 iff キー等号、元DV非可換全核のキー等号正規生成、像上受信器の必要十分条件。
- [FU: PhysicalInfiniteRootSupport](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalInfiniteRootSupport.lean) — 真正DR 18D `post` 再帰towerの任意自然数深さ構成、元17D文脈衝突からの型付き全深さDVコード衝突、旧FJ真正物理AQ全非空文脈での無限の元sourceファイバー根付き字母。
- [FV: PhysicalNonFiniteNormalKernel](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNonFiniteNormalKernel.lean) — 任意元free-group群語と有限群語集合のsupport検出器、正規閉包を消す整数値coordinate `FreeGroup.lift`、一般自由群核のfinite-normal iff finite-activeの正確な必要十分条件、旧FJ全非空真正物理18D kernelの非有限正規生成。
- [FW: PhysicalNormalRankIndependence](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNormalRankIndependence.lean) — 根付き正規生成系の非冗長性、任意正規生成族による全active文字検出、可算正規生成のexact iff。
- [FX: PhysicalExactNormalRank](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalExactNormalRank.lean) — 元の非可換全核の最小正規生成Cardinalを一般の `FreeGroup.map f` で正確に同定。
- [FY: PhysicalSourceCardinality](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalSourceCardinality.lean) — 元の真正物理18D sourceアルファベットのType同値・Cardinal和・可算性障害境界と、条件付き最小正規生成濃度`ℵ₀`。
- [FZ: PhysicalRawCountabilityGate](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalRawCountabilityGate.lean) — 元17D raw proof・18D indexed generatorの可算性伝播、真正FJ物理normal rankの条件付き`ℵ₀`、source/image濃度障害とexact`ℵ₀`正規生成同値。
- [GA: PhysicalTypedSyntaxCountability](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalTypedSyntaxCountability.lean) — 元のraw四構成子の有限構文と型付き部分復号、16D文脈閉包・17D三角形primitive・raw17D経路のCountable伝播、真正物理18Dへの明示的下位primitive・再帰Gen smallness条件。
- [GB: PhysicalRecursiveGenCountability](formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalRecursiveGenCountability.lean) — 元18D assoc/post/pre全再帰Genの型付き有限符号と厳密部分復号、元17D証拠totalから全18D indexed Gen Countable、元lower AX primitive2条件から完全original18D source Countableと真正物理kernel exact`ℵ₀`。
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

**FRによる完全再帰spineの局所化（2026-10-29）：** 真正18D元コードの任意深さの`post/pre/.../assoc`再帰列を`σ`とする。全衝突集合は `⋃_{σ} R_{w,σ}` に等しく、**`ker(τ_w)=⟪⋃_{σ}R_{w,σ}⟫`** を証明済み。ここで各 `R_{w,σ}` は完全に同じ元再帰列を持つコード対の実際の輸送像一致だけから定め、**正規閉包は同一の元非可換自由群で取る**。FQの実受信ファイバー根 `r_w(a)` は全spineを保存し、`[a][r_w(a)]⁻¹` による生成系も全spine別に分解できる。実像上の一意な受信器因子化は各spine内の全衝突一致と同値、また各元codeとその選択根での一致とも同値。FHの真正依存型`post/pre`内側コード抽出から、**固定された元17D型付き境界で外側code同士が衝突するなら内側18D輸送codeも一致する**。内側輸送像が異なるなら外側衝突不能。この条件は17D文脈作用の単射性を仮定しないが、同一spineの元raw17D引数までの無条件等号反映や、有限生成性を証明したものではない。

**FSで加えた依存型boundary keyと有限支持ゲート（2026-10-29）：** 真正18D元コード `a` に対して、その実DV輸送像から完全再帰spine、17D raw Type値経路を含む受信始域/終域、完全依存型 `post/pre` 内側18D受信コードを抽出して `K_w(a)` とする。実衝突 `f_w(a)=f_w(b)` は **`K_w(a)=K_w(b)` を必ず含意**し、全衝突集合は同一キー内の**実衝突集合**の和集合として正確に局所化する。元DV全核はその和集合から得られる差語の最小正規閉包である。**逆向き `K_w(a)=K_w(b)⇒f_w(a)=f_w(b)` は未証明**であり、境界キーだけで全元証拠を同一視しない。さらに任意の元文字写像 `f:A→B` とFQの根代表 `r_f(a)` に対して、`ker(FreeGroup.map f)=⟪[a][r_f(a)]⁻¹ | a≠r_f(a)⟫` を証明した。集合 `{a | a≠r_f(a)}` が有限なら全核は有限個の関係で正規生成されるが、**真正FJ物理18Dコードでこの集合が有限とは証明していない**。

**FTで閉じたFS boundary keyの必要十分条件（2026-10-30）：** 真正context-CLOSED 18Dコード `c` に対し、受信側全再帰spine・17D raw経路を含む始域と終域・`post/pre`の完全内側18Dコードからなる `K(c)` は**無条件に単射**である。理由は、`assoc`の始域 `trans(trans f g)h` が3本の元受信raw17D経路と依存型端点を保持し、`post/pre` は完全な内側18Dコードに加え始域のraw17D `trans` を復元するとsuffix/prefixの経路を一意に抽出できるからである。異種構成子は完全spineで分離する。従って任意の元DV完全コード `a,b` について **`f_w(a)=f_w(b) ⇔ K_w(a)=K_w(b)`** を証明した。FTの真の元非可換核は **`ker τ_w = ⟪ [a][b]⁻¹ | K_w(a)=K_w(b) ⟫`**（元の一つの非可換自由群における最小正規閉包）であり、像上受信器の一意因子化はキー等号を尊重することと必要十分。これは**受信側完全18Dコード**の復元であり、原17D証拠が潰れる旧FJ物理輸送の非忠実性を解消したり元source raw証拠の等号を反映したりする定理ではない。

**FUで初めて証明した旧FJ真正物理frameの無限active-root字母（2026-10-30）：** 旧FJの元15D保守的`refl`と`atom`は、元17D Type値証拠として区別されるが、任意の非空有限AQ文脈`w`で同じ17D文脈像を持つ。FUは元の真のDR18D `assoc(refl,refl,refl)` を元17Dの`refl`でn回`post`-whiskerした完全コード族`T_n(a)`を構成し、元17D証拠`a`を各sourceに保存し、**`depth(T_n(a))=n+1`**を証明した。任意の元文脈衝突`C_w(a)=C_w(b)`から **`f_w(T_n(a))=f_w(T_n(b))`** が全nで成立し、`a≠b`なら元`T_n(a)≠T_n(b)`。各実像ファイバーの選択根`r_w`はこの異なる2コードの両方とは一致できないため、**`T_n(a)`または`T_n(b)`の少なくとも一方が元のFS active supportに属し、深さn+1を持つ**。深さの一意性でNatをactive supportのSubtypeへ埋め込めるので、**旧FJの任意の非空物理wで `Infinite (FSActiveLetters f_w)`**。これは有限正規生成数の不可能性を示す定理ではない。FSの有限active-support⇒有限正規生成の十分条件の**対偶を使うだけでは**、無限active support⇒非有限正規生成とは言えない。

**FVで独立に完成した正規生成の有限性判定（2026-10-30）：** FQの実像ファイバーrootを`r_f(a)`とする任意の`f:A→B`に対し、FSは`ker(FreeGroup.map f)=⟪[a][r_f(a)]⁻¹:a≠r_f(a)⟫`を示し、非自明active集合の有限性なら有限正規生成という十分条件を証明していた。FVは**逆向きを形式化**した。任意の有限関係語集合`R⊂FreeGroup A`について、元source群語の有限支持を一般の非可換自由群帰納法で取り、共通の有限支持`S_R⊂A`を得る。active集合が無限なら`a∉S_R`かつ`a≠r_f(a)`を選べる。整数値座標群準同型`χ_a:FreeGroup A→Multiplicative ℤ`は`[a]`を+1、他の元source字母を0へ送り、**全`R`と最小正規閉包`⟪R⟫`を1に写すが、実rooted差語`[a][r_f(a)]⁻¹`は+1に写す**。この差語は真の`ker(FreeGroup.map f)`に属するため、核を任意の有限`R`で正規生成する仮定と矛盾する。従って **`IsNormalClosureFG(ker(FreeGroup.map f)) ↔ (Finite {a | a≠r_f(a)})`** が厳密成立。FUが証明した**旧FJ真正18D物理DV輸送の非空全有限AQ文脈でのactive字母集合の無限性**を代入し、**真正元18D kernelの非有限正規生成性**が得られる。これは単なる「選択rooted生成系が無限」という主張ではない。整数座標は非可換正規閉包の非所属証明にのみ使い、元source群の可換化を正本とみなさない。








`\operatorname{Injective}(\tau_w)\Rightarrow\operatorname{Injective}(C_w)` はFF/FDの必要条件、逆向きはFI #2676で証明済み。**FJ #2679では、具体的`S=nativeK5AXKuuSignature W`、`F=nativeK5BCFrame W`において `Injective(τ_w) ↔ w=[]` を証明**。ここで保守的15D証拠の元の`refl`と`atom`を区別したまま、真のwhiskeringが両者を同じ`atom`へ再構成することが衝突の原因である。一般抽象frameについてのFI同値と、選択物理presentationについてのFJ非単射性は矛盾しない。FCの「非自明核 iff コード衝突」とFGの「異種構成子間の衝突なし」は両立する。原pentagonは元のDV自由群像で非零のまま残り、選択したDX相対商では消える。**DSの完全証拠保存no-goを維持**する。

### 0A.3 次に形式化すべきこと — F112-P94D3GK（仮称）

1. **別定義の元F55 StructuralComparisonへ可算性を伝播**：GJ2 #2730で独立F112 `PresentedCell`全9構成子・全元Type値証拠total/fiberの条件付きCountable、実C60物理Site×Siteへの無条件適用を証明完了。GKでは異なる`NativeF55StructuralComparison`の全構成子と本来のF54始域終域・seam Type値証拠を正本から全文検査し、同じ原証拠保持有限構文・部分復号・厳密左逆を独立に構築。独立提示F55とStructuralComparison、歴史的P92Bは同一視しない。
2. **歴史的元P92B/F55との比較と4D～13Dへ**：GKのStructuralComparison可算性が成立しても、別物の歴史的元F19/F28/F54/F55との完全型付き比較・同型には新たな証明が必要。後続では7D～13D依存型証拠の構成子・入力Hom smallnessを解析し、真正14D `NativeK5FifteenFourteenFiber W`の可算性へ条件を弱めず接続する。
3. **旧FJ正規生成濃度のauthority境界**：GDの真正旧FJ非空AQ核exact最小正規生成Cardinal`ℵ₀`は元14D `NativeK5FifteenFourteenFiber W` Countableを明示仮定する。GE/GF/GG/GH/GI/GJ/GJ2により独立F112の物理C60上の元PathからF55提示3-cellまでType値Countableになっても、歴史的同型や元14D条件はまだ除去できない。一般D/Eの各Hom可算性も明示条件。
4. **独立した証明義務の維持**：GJ2は**独立F112の元F55 PresentedCell**の全Type値Countableであり、別定義`NativeF55StructuralComparison`、歴史的P92B/F19/F28/F54/F55との同型、元14D無条件Countable、旧FJ kernel自由群基底、真正19D filler、global strict n、`(∞,3)`-hyperdescentを証明しない。Lean v4.30.0-rc2 / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、107公開root、保護PR #1558 Draft/OPEN/未マージ、strict空中心・独立Kuu presentation、Gray非再導入を維持する。

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
- [FR #2694](https://github.com/itakura-hidetoshi/KuuOS/pull/2694) — 完全再帰`post/pre/.../assoc` spineによる真正18D衝突族の全和集合・元非可換全核正規閉包、根付き族のspine保存・分割、spine別／根付き受信器の実像上の一意降下、固定依存境界での外側`post/pre`衝突から内側18D輸送コード一致の必然性。[Strict Lean #40875118260](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40875118260) 9034 scoped jobs SUCCESS、Governance 30/30 complete SUCCESS、12公理監査（標準3公理以内、内側抽出4本は公理依存なし）、sorryAxなし・warning/error 0/0。
- [FS #2696](https://github.com/itakura-hidetoshi/KuuOS/pull/2696) — 真正18Dの元全再帰spine・実受信始域/終域・全post/pre内側コードからなるType値境界キー、全実衝突の同一キー局所化、差語正規閉包＝全核、キー相違時の2文字核障害、キー内受信器衝突一致 iff 実像上の一意因子化をLean形式化。任意FreeGroup.mapの非自明根付き差語による全核表示、有限active supportなら有限正規生成となる条件付き定理を含む。[Strict Lean #40877837402](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40877837402) 9035 scoped jobs SUCCESS、Governance 30/30 completed SUCCESS、14宣言公理監査は標準3公理以内・`sorryAx`なし、warning/error 0/0。
- [FT #2698](https://github.com/itakura-hidetoshi/KuuOS/pull/2698) — 真正context-CLOSED受信18DコードのFS依存型境界キーによる無条件忠実復元、元DV完全コードの実像一致 iff キー等号、元非可換全核＝キー等号差語の最小正規閉包、実DV像上の受信器のキー等号iff一意降下、ファイバー根等号による完全キー判定。[Strict Lean #40917866961](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40917866961) 9036 scoped jobs SUCCESS、Governance 30/30 completed SUCCESS、11宣言は標準3公理のみ／`sorryAx`なし、閉じた受信コード復元とキー同値7宣言は公理依存なし、変更Lean warning/error 0/0。
- [FU #2700](https://github.com/itakura-hidetoshi/KuuOS/pull/2700) — 真正元DR18D後置whiskeringの任意深さtower・元17D型付き対象の保持・再帰深さn+1、元context衝突から全深さで受信DVコードが等しくなることを形式化。旧FJの元15D保守的2証拠の衝突を全非空物理AQ文脈・任意post深さに持ち上げ、Nat→元18D非自明ファイバー根付き字母Subtypeの単射を証明し、実際の元active-root source字母型を無限と示した。[Strict Lean #40953562737](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40953562737) **9037 scoped jobs SUCCESS**、Governance 30/30 jobs completed SUCCESS、11宣言公理監査は標準3公理以内・sorryAxなし、変更Lean warning/error 0/0、元source等式・衝突の5宣言は公理依存なし。
- [FV #2702](https://github.com/itakura-hidetoshi/KuuOS/pull/2702) — 任意source元字母の整数座標FreeGroup.lift群準同型、全非可換group語の元source字母の有限支持と任意有限群語集合の共通有限支持、支持外のactive-rooted核元の検出、`FreeGroup.map` kernelの有限正規生成 iff active元字母集合の有限性。FUの全非空物理FJ 18D active支持無限性から**真正DV全kernel非有限正規生成**。 [Strict Lean #40957941544](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40957941544) **9038 scoped jobs SUCCESS**、Governance **30/30 completed SUCCESS**、新規10宣言公理依存標準3公理のみ・`sorryAx`なし、変更Lean error/warning 0/0。
- [`AGENTS.md`](AGENTS.md) — 現行のpublic root・mathlib・Gray依存・ビルド境界
- [`formal/KUOS/`](formal/KUOS/) — 過去から継続する一般的なLean数学
- [`formal/Kuu/`](formal/Kuu/) — 現在の独立Kuuの具体的な構成

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
