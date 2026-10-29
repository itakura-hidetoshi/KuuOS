# KuuOS / 空OS

**空・縁起・関係・文脈・presentationの交代可能性・高次圏論・obstruction-aware descent** を研究する数学体系、およびそのLean 4形式化・AI推論runtimeの研究です。

> **KuuOSの縁起の一般理論は、C60の導入以前から構築されてきました。C60から一般化を一から始めるのではありません。**
>
> 空は、異なる表示を無条件に同一視することでも、一つの数学的構造を「空そのもの」と固定することでもありません。数学・構成・観測・比較の方法自体も縁によって成立するという「空の空」を問い続けます。

English: KuuOS develops a general mathematical program for dependent origination, contextual transport, presentation localization, effective descent, higher coherence, and explicit obstructions. The later C60 geometry is a concrete testbed, **not the origin or unique model of the general theory**.

**研究・著作権者 / Founder and copyright holder:** 板倉英俊 / Hidetoshi Itakura. [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md) · [CITATION](CITATION.cff).

## 最新の研究状態 — 2026-10-30 JST / F112-P94D3FZ

**C60は縁起一般理論の起点ではなく、原証拠・非可換ゲージ・descentの検証場です。** FJ旧輸送の真正有限非空AQ文脈での非忠実性と、別presentation FK–FMの全有限文脈での忠実性を共存させます。FO [#2689](https://github.com/itakura-hidetoshi/KuuOS/pull/2689)は全衝突核、FP [#2690](https://github.com/itakura-hidetoshi/KuuOS/pull/2690)は核商≃実像、FQ [#2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692)はファイバー代表元への根付き正規生成、FR [#2694](https://github.com/itakura-hidetoshi/KuuOS/pull/2694)は完全再帰spine、FS [#2696](https://github.com/itakura-hidetoshi/KuuOS/pull/2696)は証拠保持boundary keyと有限active support下の有限正規生成、FT [#2698](https://github.com/itakura-hidetoshi/KuuOS/pull/2698)は受信18Dキーの完全単射性・元DV像一致 iff キー等号を証明。**新たにFU [#2700](https://github.com/itakura-hidetoshi/KuuOS/pull/2700)は、旧FJの元の異なる15D Type値証拠を、真正17D境界を保つ `(.post)^n (.assoc refl refl refl)` という任意深さの元18D構文へ実際に持ち上げ、全ての非空有限AQ文脈で元18Dコード2字は区別されながら受信コード像が一致することをLean4証明しました。** 各深さ `n` に原の完全再帰深さ `n+1` の非自明なFQ根付き元コードが存在し、自然数から真正FS active-root source字母のSubtypeへの単射を構成したため、**旧FJ真正物理輸送の任意非空有限文脈でactive-root元字母型が無限**です。これは有限正規生成不可能や最小・独立正規生成の証明ではありません。元19D幾何充填や大域strict高次構造・hyperdescentも未証明です。

**FV [#2702](https://github.com/itakura-hidetoshi/KuuOS/pull/2702) の更新：** FUの「無限個の非自明な根付き元文字」という結果から、**核の非有限正規生成性**まで独立の一般群論的証明によって到達しました。任意の有限群語集合が使用する有限source字母の外から非自明rooted核元を一つ選ぶと、その文字の整数座標群準同型は全有限関係語と正規閉包を消しますが、この核元を消せません。よって任意の有限個の非可換群語では全核を正規生成できません。**旧FJ真正物理文脈の全非空有限AQ語について確定した結論**であり、元18D証拠を整数に置き換えたわけではありません。元のsigned非可換自由群と完全Type値18D証拠は保持しています。

**FW [#2704](https://github.com/itakura-hidetoshi/KuuOS/pull/2704) の更新：** 非可換自由群写像の像ファイバー根 `r_f` の冪等性を利用し、全active文字 `D_f={a | a≠r_f(a)}` の根付き差語 `d_a=[a][r_f(a)]⁻¹` を整数座標で対角・非対角分離しました。任意の元文字添字集合 `T` が根付き差語族で**全kernelを正規生成 iff `D_f⊆T`** と証明し、FSの正規生成族が全てのactive元について**正規閉包の意味で非冗長**かつ相異なることを確立。さらに任意の非可換群語集合 `R` が全kernelを正規生成するなら、各active文字を検出する群語が必ず `R` に存在します。任意群語の元字母有限支持から、**全kernelは可算正規生成 iff `D_f` は可算**という追加の必要十分条件も証明しました。FV/FUの旧FJ真正全非空物理AQ文脈での非有限正規生成性は保持。一方、真正物理active元文字型の可算性・最小正規生成濃度の正確値・核自身の自由基底・元19D幾何充填は未証明です。
**FX [#2706](https://github.com/itakura-hidetoshi/KuuOS/pull/2706) の新規到達：** 任意の元文字写像 `f:A→B` の元の非可換自由群写像について、全kernelを正規生成する任意の**群語集合R**の濃度は、非自明rooted source文字集合 `D_f={a | a≠r_f(a)}` の濃度以上であると証明しました。元のSource FreeGroup全体から `D_f→₀ℚ`（有理数有限支持自由加群）の乗法表示へ実際の群準同型を構成し、真のrooted元語を各標準基底へ写します。全核を正規生成する任意Rの像を線形に張った部分空間で割ると、Rを消す群準同型は全normal closureも消し、根付き差語からすべての標準基底が部分空間に属することを強制します。固定mathlibのrank定理から**`#D_f ≤ #R`**を有限・無限を問わず証明。FWで証明済みの根付きrelator単射性により、**濃度ちょうど`#D_f`の正規生成集合が実在**します。従って**全kernelの最小正規生成濃度=`#D_f`**が確定。旧FJ真正物理18Dで`D_f`が無限というFUの結論と組み合わせると最小濃度は無限ですが、元の依存型active文字型の正確な濃度（可算か非可算か）や元kernel自身の自由基底、真正19D幾何充填は未証明です。
**FY [#2708](https://github.com/itakura-hidetoshi/KuuOS/pull/2708) の新規到達：** FQで選んだ「同じ実像ファイバー内の代表元」が冪等であることから、任意の元source文字写像 `f:A→B` に対し **元のType値アルファベットそのものの同値** `A ≃ D_f ⊕ Set.range f` をLean4で構成しました。ここで `D_f={a | a≠r_f(a)}` は元の非root source文字であり、右項は全targetではなく**実際に受信される像ファイバーの集合**です。両文字型が同一universeの場合、**`#A = #D_f + #(range f)`**が成立し、さらに**`Countable A ↔ Countable D_f ∧ Countable (range f)`**を形式化。真正旧FJ元18D依存Type値コードの全てのAQ文脈へ特殊化し、FUの全非空物理AQ文脈におけるactive字母無限性とFXの最小正規生成Cardinalを接続しました。**元の完全18D source alphabetがCountableという明示的追加仮定の下で**、全元18D非可換DV kernelの最小正規生成濃度が正確に`ℵ₀`と証明されました。有限なC60幾何だけから元14D–18D証拠の可算性は従わず、**真正物理active字母の無条件の正確な濃度はまだ未決定**です。
**FZ [#2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710) の到達：** 真の依存型raw17D経路totalが可算となる十分条件を、元17D対象Typeの可算性と**各raw17D証拠ファイバー**の可算性からLean4形式化し、実際の18D層オブジェクトTypeへ伝播しました。続いて元18D `assoc/post/pre` 生成子の**各依存型ファイバーも可算という別条件**から、元の完全18D sourceコードType全体の可算性を証明しました。これらの条件を真正FJ物理18Dへ直接特殊化し、全非空AQ文脈の最小正規生成濃度`ℵ₀`を条件付きで導出。さらに一般写像`f:A→B`で、実受信像が可算かつactive source文字が無限なら、**元source Typeが可算 iff 任意非可換群語の全kernel正規生成集合で濃度ちょうど`ℵ₀`のものが存在**をFXの鋭い下界とFYのsource型同値から証明しました。受信像が可算で元sourceが非可算なら、active文字も非可算という障害も証明。**18D再帰生成子ファイバーの可算性を下位の全14D–17D元構文から自動導出することは未証明**です。


| 項目 | 2026-10-30に確認した状態 |
| --- | --- |
| 定理の正本 | [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。公開統合入口は [`formal/KuuOSFormal.lean`](formal/KuuOSFormal.lean)（既存107公開rootを維持） |
| 直近の定理統合点 | **F112-P94D3FZ / [PR #2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710) MERGED**。定理squash SHA `99ccc5b7a6aaeb4166715a2b75a5fc14053dd103`。元17Dの依存型raw証拠totalから元18D object Type、各18D生成子ファイバーの可算性から完全original 18D文字Typeへの可算性伝播をLean4で証明。真正FJ物理18Dの全非空AQ文脈について、下位証拠Type可算条件から**最小正規生成濃度`ℵ₀`**を導出。別に**元source可算 iff 全kernelにexact countably infinite正規生成集合が存在**を、実受信像可算かつactive無限の条件下で証明。無条件の元18D再帰生成子可算性や元kernel自由群基底は未証明。 |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| PR #2710の証明検証 | [exact-source-head Strict Lean #40972305445](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40972305445) **9042/9042 SUCCESS**、Governance **30/30 completed SUCCESS**、FZ新規9宣言の`#print axioms`は標準`propext`・`Classical.choice`・`Quot.sound`のみ、`sorryAx`なし、変更Lean warning/error **0/0**。source HEAD `69a43dc33565356209fbdda018b388f16c7f6d00`のGit tree `3df1e01acc21c5e9cd8ab358942a6264250898f8`はmerge-test treeと完全一致。FY #2708（9041）、FX #2706（9040）など既存receipt維持。 |
| 基礎・presentation | strict空を中心に据えるが、独立Kuuも空の一つのpresentation。`KuuOSStrict`は**内部import集約**であり、別の正本でも「唯一の空」でもない。Gray圏を新しいstrict証明の根拠として再導入しない |
| 次の定理作業 | **F112-P94D3GA（仮称）**：FZはraw17D経路ファイバーおよび18D `assoc/post/pre`生成子ファイバーの可算性を**明示的な前提**にして正確なsource Countable伝播を証明した。次は真正17D `NativeC60AXStep` の`atom/refl/symm/trans`有限文法と18D `assoc/post/pre`再帰文法を、元14D–16D primitive generator Typeの可算性からCountableと導く**型依存構文符号化／induction**を完成する。`Countable`のunconditional自動導出は利用しない。既存の非可換kernel、厳密物理Type証拠、真正19D filler・global strict/hyperdescent未証明を保持。 |

### 現行のC60 Type値証拠・非可換核の到達点

| 系列・統合PR | Leanで確立したこと | 越えていない境界 |
| --- | --- | --- |
| EX–FA [#2663](https://github.com/itakura-hidetoshi/KuuOS/pull/2663)–[#2666](https://github.com/itakura-hidetoshi/KuuOS/pull/2666) | 元の完全18D非可換pentagon欠損、有限符号付き19D**候補経路**の順序付き積、正規閉包・相対商、実際のDV 17D文脈輸送に沿う生成子別降下条件 | 相対19D presentationと元のC60幾何における実在19D充填を同一視しない |
| FB–FC [#2667](https://github.com/itakura-hidetoshi/KuuOS/pull/2667)–[#2668](https://github.com/itakura-hidetoshi/KuuOS/pull/2668) | 完全pentagon自由群証拠はDV輸送後も非自明。一方、明示的DX相対商では消える。完全コード関数`f_w`と自由群準同型`τ_w`の単射性同値、非自明核とコード衝突の同値 | 元の完全証拠の非自明性と選択相対商での零化を混同しない |
| FD–FE [#2669](https://github.com/itakura-hidetoshi/KuuOS/pull/2669)–[#2670](https://github.com/itakura-hidetoshi/KuuOS/pull/2670) | 真正17D対象の文脈衝突から元18Dコード衝突と非自明2文字核を構成。反射的associatorコード族で衝突の必要十分条件を証明。全有限文脈対象作用の単射性は2つの単独frame作用の単射性と同値。各`onObj/onCell`単射性は十分条件 | 任意のC60 frameで単射性が成立するとは証明していない |
| FF [#2671](https://github.com/itakura-hidetoshi/KuuOS/pull/2671) | `C_w`の単射性を**明示的な仮定**として、原raw17D全構成子の等式反映、元の両端点とraw17D証拠を含む18D**対象**全体の単射性を証明。空文脈の18D対象写像は無条件に単射 | 18D対象の単射性は18D**生成子**コードの単射性とは別 |
| FG [#2672](https://github.com/itakura-hidetoshi/KuuOS/pull/2672) | 元の18D生成子の`assoc/post/pre`タグは任意のDV文脈で保存され、異種セクター間のコード衝突と対応する2文字核が存在しない。完全コード・元の非可換自由群輸送の単射性は3セクター各々の忠実性と同値。17D文脈作用が単射なら、`assoc`の3経路および固定内側生成子に対する`pre/post`の17D引数が単射 | 可変な再帰的内側生成子の全単射性、および3セクターの忠実性の無条件成立は未証明 |
| FH [#2674](https://github.com/itakura-hidetoshi/KuuOS/pull/2674) | 可変な内側18D生成子と外側`pre/post`の元raw17D経路を同時に扱い、実17D文脈対象作用および固定内側ファイバーの忠実性を**仮定した場合**の共同単射性を証明。新規Lean定理の`#print axioms`は`propext`のみ | 元のすべての内側生成子ファイバーでこの仮定が成立すると断言しない |
| FI [#2675](https://github.com/itakura-hidetoshi/KuuOS/pull/2675) | 元18D生成子の入れ子`pre/post`から終端`assoc`までの**全再帰構成子列・深さ**は任意の真正有限C60文脈で無条件に保存。完全自由群上の非可換構成子列準同型の自然性と**全DV核の包含**を証明。Strict Lean 9949/9949 SUCCESS | 全構成子列は元raw17D引数まで記録するものではない。**同一列内のコード衝突・完全核分類はなお未証明** |
| FI（完全反映）[#2676](https://github.com/itakura-hidetoshi/KuuOS/pull/2676) | 元`assoc/post/pre`全帰納法で可変内側18D生成子・raw17D両端点・途中境界を保持し、`Injective(f_w) ↔ Injective(C_w) ↔ Injective(τ_w)`を証明。空文脈と2つのsingleton frameの忠実性判定。9950/9950 SUCCESS | この一般同値の物理的成否はframeの選択に依存。FJ旧frameは非空文脈で非単射、FMの別frameは全有限文脈で単射。元の幾何19D充填・旧核全分類は未証明 |
| FJ [#2679](https://github.com/itakura-hidetoshi/KuuOS/pull/2679) | 真正物理AQ `nativeK5AQWhiskerCell` が元15D保守的`refl`と`atom rfl rfl`の異なるType値証拠を同一像へ写すことを構成。元proof-bearing AX・17D singletonへ明示的に持ち上げ、任意の元Wと有限語wについて **`Injective(τ_w) ↔ w=[]`**、同じ非自明2文字欠損zが**すべての非空w**で`τ_w(z)=1`となることを証明。 | この非単射性は**選択された元15D AQ証拠構文・真正物理frame**の定理。任意の抽象F、別presentation、元14D幾何作用一般の非単射性や19D fillerの存在を主張しない |
| FK [#2681](https://github.com/itakura-hidetoshi/KuuOS/pull/2681) | 同じ元14D依存境界の上に、新しい保守的15D証拠の`refl/atom/symm/trans`構成子保存whiskeringおよび別のAX frameを構成。元の14D左右raw-whiskering単射性、FJの2証拠の新輸送による分離、**旧輸送 = 構成子忘却 ∘ 新輸送** の全raw15D経路についての同値、逆の復元不能性をLean証明。新輸送は全有限AQ語でFJ証拠の区別を保つ | FK段階で未証明だった全依存型Hom単射性はFLで証明済み。元のFJ非単射性・全核・19D幾何の障害は残る |
| FL [#2683](https://github.com/itakura-hidetoshi/KuuOS/pull/2683) | FKの別15D輸送で保守的core全構成子・独立`exchange`添字・外側`symm/trans`を型付きで等式反映。可変14D中間境界を`Sigma`で復元し、交換は`Option`射影と`HEq`で復元。全Homファイバー・任意有限AQ語・代替frame `onCell`単射性を証明。9953/9953 SUCCESS | FL時点で未解決だった新frameの`mapTotal`と17D/18Dへの忠実性は後続FM [#2685](https://github.com/itakura-hidetoshi/KuuOS/pull/2685)で解決。FJ旧no-goを保持 |
| FM [#2685](https://github.com/itakura-hidetoshi/KuuOS/pull/2685) | FK・FL別AQ輸送に対し、元14D `onObj`と全15D `onCell`の単射性を合成して`mapTotal`単射性を証明。16D raw構文の`atom/refl/symm/trans`を真の依存型中間境界・元generator provenanceを保って反映し、DR 17Dの全有限AQ文脈作用の単射性を確立。FIの同値から完全18Dコード・非可換自由群輸送の全有限文脈単射性と自明核を証明。9954/9954 SUCCESS | 旧FJ frameの非空文脈非単射性は変更なし。旧核の完全正規生成表示、旧新17D/18D間の自然比較、幾何19D充填・全strict高次構造は未証明 |
| FN [#2687](https://github.com/itakura-hidetoshi/KuuOS/pull/2687) | 保守的15D構成子忘却の冪等性・非単射性、全proof-bearing AX Total上での旧frame＝忘却∘新frame、全有限文脈での忘却の自然性、**非空全有限語での旧文脈＝忘却∘新文脈**をLean証明。17D identity・18D `assoc(refl,refl,refl)`の選択した真正Type値2証拠について旧像衝突／新像分離、旧受信18Dコードだけから新受信両像を復元する関数の不可能性、別々の非可換2文字元の旧核消滅／新全有限文脈生存を証明。9955/9955 SUCCESS | 旧新**全17D/18D閉包生成子**間の自然な比較関手は未構成。旧全kernelの正規生成表示・元19D幾何充填・全strict高次構造も未証明 |
| FO [#2689](https://github.com/itakura-hidetoshi/KuuOS/pull/2689) | 任意の `f:A→B` で `ker(FreeGroup.map f)` と全ソース文字の同じ像を持つ対の差語の正規閉包が一致。実際の完全18D DV輸送で全核を厳密表示し、任意非可換語の核所属・差語判定、受信器降下 iff 全コード衝突一致、非空FJ全核非自明／別FK/FL/FM全核自明を証明。9956/9956 Strict Lean SUCCESS、11定理公理監査 | 単一FJ欠損による全核正規生成、有限・最小生成集合、元の幾何的19D充填は未証明 |
| FP [#2690](https://github.com/itakura-hidetoshi/KuuOS/pull/2690) | FO全核正規閉包で割った非可換自由群と**実際の完全18D DV輸送像**の第一同型定理、代表元可換性、全コード衝突を尊重する受信器の像上への一意な群準同型因子化を証明。全射で標的全体の拡張が一意、非全射 `Empty→Bool` で全標的拡張が非一意という区別を形式化。9032 scoped jobs Strict Lean SUCCESS、11宣言公理監査 | 同型は**像部分群**についてで、全標的への無条件の全射・一意性、コード衝突の有限分類、真正19D Type値幾何充填を主張しない |
| FQ [#2692](https://github.com/itakura-hidetoshi/KuuOS/pull/2692) | 任意の `f:A→B` で全コード衝突対の正規閉包は、**実際の像の各ファイバーから選んだ根代表元と各source文字の差語**の正規閉包に一致。真正18Dの衝突対を元の`assoc/post/pre`3セクター内へ厳密分類し、原非可換自由群で3セクター関係和集合の正規閉包＝全核、根代表元のタグ保存、根付き正規商≃実輸送像、受信器の3セクター内一致 iff 像上の一意因子化をLean4証明。9033/9033 scoped Strict Lean SUCCESS、13公理監査 | 代表元の選択は非構成的であり、生成関係が有限・最小・独立とは未証明。異なる構成子セクター間の可換性も仮定しない。旧FJ欠損1元の全核生成、真正19D幾何充填は未証明 |
| FR [#2694](https://github.com/itakura-hidetoshi/KuuOS/pull/2694) | FG/FIの真正18D**全再帰spine保存**から、FO全コード衝突対＝全有限再帰spine同種衝突の和集合、全核＝その和集合の元の非可換群内正規閉包を証明。FQ代表元の全spine保存、根付き関係の全spine分割、受信器の実像上への一意な因子化 iff spine内の衝突一致 iff 各コードとファイバー根の一致。FHの真正依存型 `post/pre` 内側抽出により、外側衝突は内側輸送像の一致を必要とし、内側像の相違は外側衝突を排除。9034 scoped Strict Lean SUCCESS、12公理監査 | 全spineの種類と衝突関係の数は有限とは限らず、同一spine内の元17D引数の完全な一致分類や、有限・最小正規生成・真正19D充填は未証明。セクター間可換性も未仮定 |
| FS [#2696](https://github.com/itakura-hidetoshi/KuuOS/pull/2696) | 真正18D完全再帰spine、輸送後の元17D raw経路を含む始域/終域、全`post/pre`内側完全18Dコードを記録する実依存型境界キーを構成。全実コード衝突の同一キー局所化、全核＝同一キー衝突差語の正規閉包、異なるキーからの2文字核の排除、像上受信器のキー別一意降下必要十分条件を形式化。一般の`FreeGroup.map f`でファイバー根と一致する元の恒等関係を除外した全核の厳密正規表示、非自明根付き元集合が有限なら有限正規生成という十分条件を証明。9035 scoped Strict Lean SUCCESS／14公理監査 | **境界キー一致はDV像一致の十分条件とは未証明**。真正物理18D非自明根付き集合の有限性、最小/独立生成、単一既知FJ欠損の全核生成、元19D幾何充填も未証明 |
| FT [#2698](https://github.com/itakura-hidetoshi/KuuOS/pull/2698) | 真正context-CLOSED 18D受信生成子コードに対し、FSのType値境界キーの**無条件単射性**を証明。原17D raw `trans(trans f g)h`による`assoc`全3経路の復元、全依存端点可変の`post/pre`内側18Dコード＋source raw pathのsuffix/prefix復元、異種再帰spine分離を使う。従って真正元DVコードの輸送像一致 iff 境界キー一致を証明し、**元18D全非可換核＝キー等号のみで生成する最小正規閉包**、像上受信器のキー等号尊重 iff 一意因子化を確立。9036 scoped Strict Lean SUCCESS、FT11宣言の公理監査、核となる7宣言は公理依存なし | **元original17D raw証拠の一致を導いたわけではない。** 非自明rooted支持の物理的有限性／独立性／最小性、FJ既知1元の全核生成、幾何的19D充填は依然未証明。 |
| FU [#2700](https://github.com/itakura-hidetoshi/KuuOS/pull/2700) | 元の真正DR依存型18D構文上で、各元17D対象から `(.post)^n (.assoc refl refl refl)` 完全コードを任意の自然数深さに構成。元コードは17D元対象を保持し、再帰spine深さが厳密に `n+1`。元17D文脈対象に衝突があれば、同じ深さの異なる元コードの実DV受信像が一致。真正FJの元15D `conservative refl/atom`ペアに適用し、**全ての非空物理AQ文脈で、任意深さの異なる元コード衝突・各深さの非自明active-root元が存在**し、Nat→真正active-root source字母Subtypeの単射をLean証明。9037 scoped Strict Lean SUCCESS・11宣言公理監査 | active-root元字母型の無限性を確立。**全核が有限正規生成不可能であること、最小・独立正規生成数、FJ単一欠損の全核生成は未証明**。幾何19D充填も未証明 |
| FV [#2702](https://github.com/itakura-hidetoshi/KuuOS/pull/2702) | 任意 `f:A→B` について固定mathlib `Subgroup.IsNormalClosureFG` の厳密な必要十分条件：**`ker(FreeGroup.map f)` が有限正規生成 iff `{a | a ≠ r_f(a)}` が有限**。各元source字母の整数座標群準同型を`FreeGroup.lift`で構成し、任意1群語／有限群語集合の元字母有限支持を一般の非可換自由群で証明。有限関係語をすべて消す整数座標で支持外の非自明根付き核関係を検出し、任意の有限群語正規生成を否定。FUの実物理無限active元へ適用し、**旧FJの全非空有限AQ文脈の真正元18D DV全核が非有限正規生成**。9038 scoped Strict Lean SUCCESS／FV10宣言公理監査 | 最小正規ランクの正確な濃度・独立な正規生成基底、旧新presentation全対応、真正19D Type値幾何充填、大域strict高次構造は未証明 |
| FW [#2704](https://github.com/itakura-hidetoshi/KuuOS/pull/2704) | 選択した像ファイバー根の冪等性から、各active根付き差語に対する整数座標は対角+1・非対角0。従ってactive差語は他のrooted差語族の正規閉包の外にあり、全FS rooted familyはnormal-irredundantかつ単射。**`normalClosure({d_t : t∈T})=ker(FreeGroup.map f) ↔ D_f⊆T`**、任意の非可換正規生成関係語集合は各active座標を必ず検出し、**可算正規生成 iff `D_f` が可算**をLean証明。9039/9039 scoped Strict Lean SUCCESS、12宣言標準3公理内、Governance 30/30 SUCCESS | 元18D Type値・signed非可換核は保持。根付き添字族の非冗長性を、任意の群語集合の最小**Cardinal**や核自身の自由基底と取り違えない。真正旧FJ物理active source字母の可算性、単一FJ欠損での全核生成、元19D幾何充填・大域高次整合は未証明 |
| FX [#2706](https://github.com/itakura-hidetoshi/KuuOS/pull/2706) | 真正元source文字の非root集合 `D_f` を基底とする有理数有限支持自由加群 `D_f→₀ℚ` を構成。元のsigned非可換自由群からの群準同型で各rooted差語を厳密に標準基底へ写し、任意の群語集合Rのnormal closure＝全kernelなら、その座標像の線形span＝全自由加群。固定mathlibの自由加群rankとspan rank上界によって**任意Rの濃度`#R≥#D_f`（有限・無限とも）**を形式化し、FWのrooted map単射性による**ちょうど`#D_f`の正規生成族の存在**と統合。9040/9040 Strict Lean SUCCESS、7宣言の標準3公理監査、Governance 30/30 SUCCESS | 元kernelは非可換のまま、有理数座標は証明検出器。一般の最小正規生成濃度は確定したが、**旧FJ真正物理18D active元文字型の濃度が可算か非可算か**は別の未証明問題。核自身の自由基底、真正19D幾何充填・global strict/hyperdescentも未証明 |
| FY [#2708](https://github.com/itakura-hidetoshi/KuuOS/pull/2708) | 真のFQ像代表元を保持し、元sourceアルファベットの**型同値`A ≃ D_f ⊕ Set.range f`**、同一universeの正確な**Cardinal和`#A=#D_f+#(range f)`**、`Countable A ↔ Countable D_f ∧ Countable(range f)`を証明。元の真正18D DV source Type値コードへ同値と濃度境界を実際に特殊化し、全非空物理AQ文脈でのFU無限active文字＋FX exact正規生成Cardinalと接続。**元18D sourceコード型が可算という明示的条件の下で**最小正規生成濃度`ℵ₀`を厳密に導出。9041/9041 Strict Lean SUCCESS、10公理監査、Governance 30/30 SUCCESS | `Countable`は元14D–17D証拠の濃度からまだ無条件には証明していない。有限幾何≠有限・可算Type値証拠。真正19D filler・元kernel自由基底・大域strict/hyperdescentは未証明 |
| FZ [#2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710) | 真正17D endpoint型と各raw17D `NativeC60AXStep`証拠ファイバーの可算性から実18D層object Typeの可算性を証明。さらに依存18D `assoc/post/pre`生成子ファイバーの可算性を加えると、元18D完全source文字Typeが可算になることを形式化。真正FJ物理18Dへ具体化し、全非空AQ語で最小正規生成Cardinal`ℵ₀`を明示的下位型条件下で証明。実受信像が可算でactive字母無限なら、**元source可算 iff exact`ℵ₀`の任意群語正規生成集合が存在**、実受信像可算でsource非可算ならactiveも非可算という障害を確立。9042/9042 Strict Lean SUCCESS、FZ9公理監査、Governance 30/30 SUCCESS | raw17D構文および18D再帰生成子ファイバーが実際に可算であるための元14D–16D primitive typeの十分条件はまだ閉じていない。有限C60幾何から可算性を推測しない。真正19D Type値幾何充填、kernel自由基底、strict高次化は未証明 |

実際のDV完全コード写像を `f_w`、その非可換自由群準同型を `τ_w`、17D文脈対象作用を `C_w` とすると、証明済みの**条件の分離**は次です。

$$
\operatorname{Injective}(\tau_w)
\iff \operatorname{Injective}(f_w)
\iff I_{\mathrm{assoc}}(w)\land I_{\mathrm{post}}(w)\land I_{\mathrm{pre}}(w).
$$

さらに先行FI [#2675](https://github.com/itakura-hidetoshi/KuuOS/pull/2675)では、元の完全18D非可換自由群から**全入れ子構成子列**への自由群準同型 $S_{\mathrm{orig}}$ と、文脈閉包先の対応写像 $S_{\mathrm{closed}}$ を構成し、$S_{\mathrm{closed}}\circ\tau_w=S_{\mathrm{orig}}$ および **$\ker(\tau_w)\subseteq\ker(S_{\mathrm{orig}})$** を無条件に証明しました。この必要条件は最上位の3セクター判別より強い一方、同じ再帰列の元raw17D引数や生成子ファイバーの忠実性は保証しません。

後続FI [#2676](https://github.com/itakura-hidetoshi/KuuOS/pull/2676)で、この三セクター条件を元の17D文脈対象作用の単射性へ正確に還元しました。すなわち任意の固定有限文脈 $w$ について **$\operatorname{Injective}(\tau_w)\iff\operatorname{Injective}(f_w)\iff\operatorname{Injective}(C_w)$**。後続FJ [#2679](https://github.com/itakura-hidetoshi/KuuOS/pull/2679)は、具体的に`S=nativeK5AXKuuSignature W`、`F=nativeK5BCFrame W`とした**選択物理AQモデル**で、`C_w`（従って`τ_w`）は任意の**非空**有限語で**非単射**と証明しました。一方、空語での単射性はFIから従います。

**依然として未証明：** FNで選んだ17D identity・18D reflexive-associatorの**2証拠以外**について、旧新の異なる閉包生成子Type値全体をつなぐ構成子保存比較関手や自然性・higher coherence、旧FJの非可換自由群核の完全な正規生成表示、任意の別presentationでの忠実性、元のC60幾何での真正19D Type値充填、異なる高次証拠の同一性、大域strict 3/n圏、`(∞,3)`-hyperdescent。**DSの完全証拠保存no-go**と旧P62/P77/P80/P87/P88の各presentation固有の障害を維持します。

より具体的な優先順位とLeanファイルへの導線は[ROADMAP](ROADMAP.md)を参照してください。以下の長いP58–P91記録は歴史的な検証台帳として保持しており、**現在の最終段階ではありません**。

## 研究の全体像：一般理論が先、C60は後から導入した検証の場

研究は二つの相互に照らし合う方向から進みます。

1. **既存の一般理論を継承・深化する。** C60以前からのcontext、transport、refinement、presentation-independent localization、sheaf/stack descent、bicategorical・simplicial coherence、operadicな複数条件、obstruction、普遍性、およびactual-lift / biadjunctionの形式的成果を、その原型・仮定・定理名のまま保持します。
2. **真正C60と独立Kuuで具体的に検証する。** 有限だが非自明な入射幾何・raw高次証拠・位相・曲率・非降下を使い、一般理論の仮定が実際に成立するか、何を失うか、どの厳密法則が障害に遭うかを調べます。独立Kuuはこの作業に便利な一つのpresentationであって、「唯一の空」ではありません。

~~~text
C60以前からの縁起の一般理論（v0 → v1 → v2 → v4/v5）
  context / transport / W-localization / J-descent / higher coherence
  universality / obstructions / biadjunction / proof-relevant paths
                      ⇅ 具体化・反例・比較・一般理論への反映
真正C60・独立Kuu（後から導入した有限幾何による検証）
  incidence / paths / raw 2・3-cell / quotient / phase / obstruction
                      ↓ 未証明部分を厳密に追究
非自明な証拠を保持する局所strict 3圏 → 大域strict 3圏 → strict n圏
                      ↓ 別途必要な比較・モデル化の証明
                 (∞,3)-hyperdescent
                      ↓ 適用範囲と仮定を明確に一般化
                  縁起の一般理論の深化
~~~

この図は**研究上の証明計画**であり、後半の矢印がすでにLeanで成立したという主張ではありません。一般理論はC60からしか得られないものではなく、C60の成果が一般理論へ逆向きに検証・修正を促します。

## C60以前に構築した縁起の一般理論（生きた定理群）

以下は新しい独立Kuuの前史として退けるものではなく、**現在も同じ公開Leanパッケージに属する数学的成果**です。それぞれのソースに明示された条件の範囲で扱います。

| 系列 | 数学的到達点と正確な範囲 | 代表的なLeanソース |
| --- | --- | --- |
| **v0–v1：縁起と関係のtransport** | Contextの圏、状態関手、合成に沿うtransport、不変readout、文脈的descent、複数条件のoperadic構成・高次比較の入口。物理的因果の実証は含まない。 | [FunctorialTransport v0.1](formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean) · [CoreSpine v1.7](formal/KUOS/DependentOriginationCoreSpineV1_7.lean) |
| **v1：nerve・scaled horn・homotopy** | Duskin nerveとhigher coherence。v1.33はhorn境界のhomotopyとstrict fillerを区別し、homotopyからstrict fillerへのrectificationを明示的な追加条件として切り分けた。 | [ScaledHornHomotopyDescent v1.33](formal/KUOS/DependentOriginationScaledHornHomotopyDescentV1_33.lean) |
| **v2.0：presentationの普遍性** | 許容する変更`W`の局所化`C[W⁻¹]`、`W`を同型へ送る関手の普遍的因子化、および同一普遍性を持つcarrier間の圏同値。`W`以外のすべての表示変更を自動的に反転するわけではない。 | [PresentationUniversality v2.0](formal/KUOS/DependentOriginationPresentationUniversalityV2_0.lean) |
| **v2.1–v2.7：descentとW+J分類** | Grothendieck topology `J`、sheafの局所大域条件、局所化後のsheafと元の適合する文脈系との**圏同値**。`H`まで含む最終完成を意味しない。 | [WJCategoryEquivalence v2.7](formal/KUOS/DependentOriginationWJCategoryEquivalenceV2_7.lean) |
| **v2.8–v2.13：Cat値stackと高次局所化** | Cat値擬関手の被覆に対する実効stack descent、precoverageの閉包条件下での特徴付け。厳密に`W`を反転する`C ⥤ Cat`に対する局所化の存在・一意性を証明。任意の弱い擬関手の普遍的高次局所化やhyperdescentは未証明。 | [HigherStackDescent v2.8](formal/KUOS/DependentOriginationHigherStackDescentV2_8.lean) · [StrictHigherUniversality v2.13](formal/KUOS/DependentOriginationStrictHigherUniversalityV2_13.lean) |
| **v4.00–v5.101：obstructionと高次普遍性** | 非因子化・局所化・明示的障害・exact-universal比較、実際の`F,G,η,ε`・triangulator・前後swallowtailを積み上げ、**同じoriginal actual-lift datum**上でcoherent biadjunction carrierを構成。一般のstrict 3圏を完成させたわけではない。 | [CoherentBiadjunctionActualLift v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) |
| **v5.102–v5.153：高次の具体的証明構文** | mates、二軸のType値履歴・交換類・完全normal form、任意有限長の回転木、五角形・正方形3-cell提示。**raw証拠を観測商へ写すと非忠実になる**実際の反例と復元不可能性を証明。 | [F55 raw cells](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152.lean) · [F56 observation nonfaithfulness](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153.lean) |

これらは**縁起の一般化がC60以前から実際に進んでいた証拠**です。「C60でstrict 3圏を証明してから初めて一般理論に着手する」という順序にはしません。一方、それぞれをそのまま厳密な大域3圏や`(∞,3)`-hyperdescentの完成証明とも呼びません。

歴史的な詳細・定理の成立範囲・原型を残した[旧README v5.291](docs/legacy/README-v5.291.md)と[旧ROADMAP v5.291](docs/legacy/ROADMAP-v5.291.md)も参照してください。**歴史的定理は`formal/KUOS/`の現行ソースでも生きています。`legacy/`への隔離・一括廃止ではありません。**

## 空の空・presentation・Grayの位置づけ

- **どのpresentationも空そのものではありません。** 古いF94/F95の荷電と位相を伴う商、現在の独立Kuu商、Qiの経路観測合同、C60のraw証拠も、それぞれ特定の関係と観測に相対的です。異なる表示が交換可能なら保存量と比較写像を証明し、交換できないなら差異とobstructionを保持します。
- **Gray圏をstrict 3圏の代替にしません。** Gray圏が与える弱いinterchange/coherenceは、KuuOSが次に要求するstrictな3次元合成律・交換律を証明したことにはなりません。研究上のstrict 3圏目標を「Gray圏ならできる」と弱めて完了扱いしません。
- **過去のGray・bicategoricalな数学を消しません。** 既存の証明は元の型と仮定のまま保存・利用します。ただし独立Kuuの原始構成や、これからのstrict 3/n圏の証明根拠としてGray固有の公理を密輸入しません。
- **strict 3圏の証明も空の唯一性の証明ではありません。** それは現在の研究経路に設定した不可欠な数学的到達目標です。成立を証明できなければ不足条件・no-go・非零obstructionをそのまま提示し、証拠を消す商や法則のすり替えで解決済みにしません。
- **mathlibを積極的に使用します。** 高次圏・局所化・sheaf・simplicial/homotopy・代数的トポロジーなどの定理を再利用します。Gray非依存とmathlib非依存は無関係です。

## 真正C60・独立Kuuの構成履歴とstrict 3圏の未解決境界

### C60の現在の前向き表示：入射グラフよりゲージ接続と真正Type値証拠を優先

[ゲージ移行方針・数学的監査](docs/C60_GAUGE_PRESENTATION_MIGRATION.md)を研究規則とする。真正C60の60 Dart・90 Edge・32 Polygon・360 flagsを変更せず、入射グラフの隣接やK₅の組合せ論的貼り合わせを高次coherenceの証明と取り違えない。[真正C60ゲージ場と32面曲率](formal/Kuu/F112/PolygonNativeC60PhysicalGaugeAtlas.lean)、[真正P92Bの非可換ゲージ障害](formal/Kuu/F112/PolygonNativeC60K5TypedGaugeCoherence.lean)、[Qi v3.4の位相枠](formal/KUOS/Architecture/QiWuxingNativeC60GaugeV3_4.lean)を比較表示として使う（[PR #2510](https://github.com/itakura-hidetoshi/KuuOS/pull/2510) MERGED）。有限グラフや歴史的Quiver、旧no-go、非零曲率は保存する。元のK₅形式的9面語と、実際のF54依存型境界を貼り合わせた3-cellを混同しない。

### 2026-10-24の証明履歴：真正K₅九面の向き・非可換境界・独立4次元生成子

[P94D3Q #2519](https://github.com/itakura-hidetoshi/KuuOS/pull/2519)・[P94D3R #2520](https://github.com/itakura-hidetoshi/KuuOS/pull/2520)は、P92Bの反転した自然性square2の真正F54構造的seamと、従来の全球shellingの向きの不整合を明示した。既存shellingに必要な構造的seamを仮定で埋めず、文脈深さ列の保存不変量により、その構造的presentationでの不可能性をLeanで証明した。8面の実Type値貼り合わせと反転square2は同じ始終F54経路を持つ平行3-cellであり、自然性数はそれぞれ+2、−1。

[P94D3S #2521](https://github.com/itakura-hidetoshi/KuuOS/pull/2521)は**square2の3-cell向きを明示的に再反転**し、元の面順序を保った真正Type値9面閉路を別の構造的presentation上に構成した。旧形式的9面語を `W_old`、最初の7面の群語を `S`、旧反転square2の語を `q` とすると、`W_old` の自然性数は1、真正貼り合わせ `W_typed` は3である。さらに非可換順序を保持して `W_typed · W_old⁻¹ = S · q⁻² · S⁻¹`、相対自然性数+2を証明した。**元の自然性数1の語自体が貼り合わせ可能になったとは主張しない。**

[P94D3T #2522](https://github.com/itakura-hidetoshi/KuuOS/pull/2522)は、この**実際に構成した**自然性数3の9面Type値3-cellを境界に持つ、別の独立4-cell生成子を宣言し、その完全な非可換語と旧P94A四射relatorの正規閉包をmathlibで構成した。旧核の真の拡大、旧F55 signed/odd shadowの降下、自然性数の非降下、共役作用・境界同変性・**正規核の代数的Peiffer恒等式**をLeanで証明した。生成子の宣言とその正規核の代数的Peifferは、**新しい4-cell Type値文法の任意whiskering/interchange coherenceの証明ではない**。旧P92Bへのdescent、元の形式的 `W_old` の真正4次元充填、局所・大域strict 3/n圏、`(∞,3)`-hyperdescentは未解決として残る。



C60では元の正二十面体に由来する**60 Dart、90 Edge、32 Polygon（12五角形・20六角形）、360 incidence flags**を用います。この有限幾何は、以前に構築した高次理論を**具体的・真正な境界と証拠のもとで試験する場**です。

- [`Kuu.Presentation`](formal/Kuu/Presentation.lean)：選ばれた境界付き自由経路と明示的な関係に相対的な商、核、観測関手の因子化。
- [`Kuu.Strict`](formal/Kuu/Strict.lean)：関手・自然変換の結合律、単位律、2次元のstrict interchange。**これはglobal proof-relevant strict 3圏の証明ではありません。**
- [`Kuu.Incidence`](formal/Kuu/Incidence.lean)：文脈に沿う切片図式とGrothendieck総圏。
- [F112親PR #2339](https://github.com/itakura-hidetoshi/KuuOS/pull/2339)：Grayを原始基礎としない真正C60のF42/F54/F55、局所化、型付き高次証拠の移行。**MERGED：現在はmainに統合済み**。
- [F112-P56 #2418](https://github.com/itakura-hidetoshi/KuuOS/pull/2418)–[P57 #2420](https://github.com/itakura-hidetoshi/KuuOS/pull/2420)：独立F55九生成子のraw輸送、水平自然性、selected shadowのfaithfulnessと失われるraw情報を区別。
- [F112-P58 #2421](https://github.com/itakura-hidetoshi/KuuOS/pull/2421)：raw F55構文はそのままでは**strictな左右単位律・結合律を満たさない**ことをnode-countで証明。mathlibの自由経路圏を別途構成。
- [F112-P59 #2423](https://github.com/itakura-hidetoshi/KuuOS/pull/2423)、[P60 #2424](https://github.com/itakura-hidetoshi/KuuOS/pull/2424)・[#2425](https://github.com/itakura-hidetoshi/KuuOS/pull/2425)、[修復 #2428](https://github.com/itakura-hidetoshi/KuuOS/pull/2428)：垂直raw単位・合成を自由経路の空経路・連結へ正規化し、残る７種を証明依存生成辺として保持。自由経路の正規化関手と選択されたshadow観測への因子化を証明。数値観測からraw履歴は一般には復元できない。
- [F112-P61 #2426](https://github.com/itakura-hidetoshi/KuuOS/pull/2426)：垂直正規化された水平合成は２辺の経路。２つのraw単位セルを水平合成しても空経路にはならないという**限定された水平単位律obstruction**を示す。大域strict 3圏の不可能性ではない。
- [F112-P62 #2429](https://github.com/itakura-hidetoshi/KuuOS/pull/2429)：９構成子を再帰的に検査した**単位生成raw構文**だけを対象に、型付き自由経路合同関係を生成。垂直経路合成との整合性と選択されたshadowへの健全性を証明し、P61の水平単位経路と空経路がこの関係で結ばれることを証明。真正C60の五角形・六角形生成元は単位構文から除外。**水平合成の全関手性・交換律・大域strict 3圏はなお未証明。**
- [F112-P63 #2431](https://github.com/itakura-hidetoshi/KuuOS/pull/2431)：９構成子の再帰から`unitOnly`のF54始終点が同一であることを証明。mathlibの`Paths.lift`で左右contextの**証明依存raw自由経路関手**を構成し、垂直合成と単位生成構文の保存、context付きraw単位とstrict単位のP62関係を証明。raw生成履歴は消去しない。
- [F112-P64 #2432](https://github.com/itakura-hidetoshi/KuuOS/pull/2432)：P62の明示的な型付き合同関係をmathlibの`Congruence`・`CategoryTheory.Quotient`で**実際の垂直商圏**として構成。商圏の射の等号とP62関係の必要十分性、P61水平単位の商圏上の単位等式、選択されたshadow観測の因子化、raw生成元の観測量保存を証明。**選択shadowと一致するraw証明項を一括同一視する商ではない。**
- [F112-P65 #2434](https://github.com/itakura-hidetoshi/KuuOS/pull/2434)：P59によって**単一の生成辺として残る**unit-only raw証明セルを明示的に区別し、真正C60の証明履歴を保持する型付きunit wordを構成。P62関係の全５規則がP63の左右context関手で保存されることを証明し、mathlib `CategoryTheory.Quotient.lift`によりP64の最小商圏へ**左右２つの関手を実際に降下**させた。商関手との等式を双方で証明。raw `ident`生成辺全体の無条件消去やshadow値による同一視は行わない。
- [F112-P66 #2436](https://github.com/itakura-hidetoshi/KuuOS/pull/2436)：P64の単位生成合同商は**3射の射集合に作用し、F54の経路対象を同一視しない**ことを一般の２軸Nat深さで証明。実C60六角形の左右順序の異なるF54回転経路は商圏上でも異なる対象であり、それらを結ぶ真正F55交換正方形3射は残存する。選択されたshadowの交換位相`1 : ZMod 2`も非零のまま保存。これはP62〜P65だけから**厳密なinterchange等式を導けない**という現在のpresentationの具体的障害であり、一般的strict 3圏の不可能性定理ではない。
- [F112-P67 #2438](https://github.com/itakura-hidetoshi/KuuOS/pull/2438)：真正F54のdisjoint-square比較を**Type値の証拠**として構成し、各比較証拠から元の型付きF55 raw 3-cellを復元。比較クラスの等号はこの証拠の`Nonempty`と同値であり、具体的証明履歴を選ぶ操作ではない。実C60の左先・右先回転順序が比較クラスで等しくなる一方、元のF54経路は異なり、**その同一視を行う任意の写像は単射になれない**ことを証明。選択された非零交換位相とraw証明履歴は別データとして保持。
- [F112-P68 #2439](https://github.com/itakura-hidetoshi/KuuOS/pull/2439)：全９構成子を再帰的に検査し、真正五角形生成元を含まない**squareOnly**なF55 raw証拠をType値で保持するcontext閉包比較を構成。P67比較クラスから新クラスへの写像、**左右F54 contextの商上の作用**と元の経路への正確な整合、実C60六角形の交換比較をLean4で証明。五角形生成元はsquareOnlyの原始生成元から除外。P67とP68が同値であることや全3-Homの輸送までは主張しない。
- [F112-P69 #2441](https://github.com/itakura-hidetoshi/KuuOS/pull/2441)：P68のF54比較クラスを始点・終点に持つ型付きF55高次射パッケージを構成。元の２つのF54代表経路と真正F55 raw 3-cellをType値で保持し、元の履歴保存と比較クラス等号から得られる比較証拠の存在を証明。**代表元の一意な選択・新しい高次圏の全合成は未証明。**
- [F112-P70 #2442](https://github.com/itakura-hidetoshi/KuuOS/pull/2442)：選択された真正squareOnly比較証拠による**両端代表元の輸送**と、中間比較証拠を指定した**高次射の合成**をType値raw F55構文で実装。選択shadowの加法公式を証明。実C60六角形では同じ商クラスを両端に持つ恒等3射（位相0）が交換正方形で輸送されると、元のraw証明項の位相が1に変化することを証明。**選択証拠に依存した合成を、代表元独立な全合成と混同しない。**
- [F112-P71 #2444](https://github.com/itakura-hidetoshi/KuuOS/pull/2444)：P70代表元変更から生成する高次射の輸送同値関係と商を構成し、商での等号の必要十分性を証明。輸送同値な元の高次射でraw shadowが異なれば、**元の数値shadowを全代表元で保つ商への因子化は不可能**という限定されたno-goを証明。真正C60の位相差と輸送同値を接続。ただし補正付き・gradedな高次Homは否定しない。
- [F112-P72 #2446](https://github.com/itakura-hidetoshi/KuuOS/pull/2446)：P70の**選択された真正比較証拠**による代表元輸送・中間経路のbridge合成で、元raw shadowに加わる成分を明示して補正。２段階の輸送で補正値が整合する加法cocycle公式と、真正C60交換正方形で補正前位相1・補正後位相0を証明。補正は証拠選択に依存し、P71無補正shadowの商への因子化ではない。
- [F112-P73 #2447](https://github.com/itakura-hidetoshi/KuuOS/pull/2447)：P68の`squareOnly`判定を全９raw構成子で帰納的に解析し、比較証拠の**五角形chargeが0**であることを証明。P70の左右代表元変更とbridge付き合成、P71輸送同値の全４生成規則で元の五角形整数chargeが保存されることを示し、P71商上の真正なcharge観測関数を構成。真正C60の非零交換位相とは独立に成立。
- [F112-P74 #2448](https://github.com/itakura-hidetoshi/KuuOS/pull/2448)：元の整数線形観測`a×五角形charge + b×交換charge`について、**元の交換chargeを1だけ変化させる輸送が存在する固定されたP71商では、全代表元と一致する無補正readoutが存在する必要十分条件は`b=0`**と証明。十分性はP73の五角形chargeから構成し、必要性は実際の輸送同値と加法性から導出。真正C60交換正方形で交換charge 0→1を確認。すべてのgraded高次観測を分類したとは主張しない。
- [F112-P75 #2450](https://github.com/itakura-hidetoshi/KuuOS/pull/2450)：P71の輸送４生成規則を**真正のType値graded輸送履歴**として持ち上げ、元F55 shadow全３座標（五角形整数・交換整数・奇偶位相）の加法gradeを保持。輸送履歴に対するshadow加法の健全性、固定raw両端でのgrade一意性、閉路grade0、Prop値P71輸送関係とgraded証拠の存在の必要十分性を証明。真正C60の交換正方形でgradeの交換整数+1・奇位相非零を確認。**raw履歴の同一視、全3-Hom構成、strict interchangeを主張しない。**
- [F112-P76 #2451](https://github.com/itakura-hidetoshi/KuuOS/pull/2451)：真正F55 squareOnly比較証拠の縦合成、二段階代表元輸送と合成比較の**正規化自由経路・全選択shadowでの整合性**を証明。旧bridgeと新bridgeの差分を実証拠の加法として正確に記録し、**比較経路の等号を明示的に仮定した場合に限り**合成経路等号を導出。真正C60交換正方形のraw履歴は単位左合成と異なるが、正規化経路・shadowは一致。raw 4-cellの無条件存在やstrict interchangeは未証明。
- [F112-P77 #2452](https://github.com/itakura-hidetoshi/KuuOS/pull/2452)：真正九構成子F55 raw 3証明間に**Type値の八生成規則による縦4-cell証拠**（反射・対称・推移・左右whisker・左右単位・結合）を構成。P59正規化経路と選択shadowへの健全性を**別々に証明**し、P62単位合同と接続。4-cell証拠の存在だけを関係とする正確なSetoid・商を作り、実C60のraw非同一な二証明間の4-cellを構成。全ての同値shadow・同値経路から証拠が得られるとは言わない。
- [F112-P78 #2453](https://github.com/itakura-hidetoshi/KuuOS/pull/2453)：P77の**真正4-cell合同による縦合成のwell-definedness**を証明し、元のF54経路上に、P77商をHomとする別の明示的Mathlib `Category`構造を実装。単位・結合はP77のraw4-cell証拠から証明し、正規化経路と全shadow観測の合成保存を証明。**局所的な厳密な縦合成のみ**であり、水平interchange・大域strict 3/nは未証明。
- [F112-P79 #2455](https://github.com/itakura-hidetoshi/KuuOS/pull/2455)：**P77のraw4-cell合同では水平単位律を満たせないことを証明**。元F55の真の恒等3射２つを水平合成したraw証明のP59正規化経路長は２、結果経路のraw恒等3射は０。したがってP77のType値4-cellは存在せず、その厳密商クラスも非同一。左右contextの単位も同様に長さ１対０で障害がある。一方、P62の構文由来`unitOnly`経路合同ではすべて関係すること、両raw証明のfull shadowは一致することを示し、真正C60六角形の二つの独立F54 associatorで具体化。**P77の厳密な経路等号を保ったまま水平単位4-cellを追加することは不可能**だが、より弱いP62相対の証拠付きcoherenceは排除しない。
- [F112-P80 #2457](https://github.com/itakura-hidetoshi/KuuOS/pull/2457)：P79の厳密P59経路等号に関するno-goを保持したまま、**新しいType値raw4-cell presentation**に、旧P77証拠の明示的埋込み・水平単位・左右context単位の３生成規則を追加し、反射・対称・推移・左右縦whiskerへ閉じた。全証拠についてP62の構文由来単位経路**合同への健全性**と、F55原full shadow保存を独立に証明。実証拠存在によるSetoid・商のexact kernel、縦合成の4-cell適合性、shadow readoutの因子化を構成。真正C60で**旧P77商は非同一、新P80商は同一**と証明。P80は選択された新presentationであり、元raw歴史やP77 no-goを消してはいない。
- [F112-P81 #2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459)：P80の**新しいP62相対Type値4-cell商**について、実際の左右whisker証拠から縦合成のwell-definednessを証明。旧P77の単位・結合4-cellをP80へ明示的に埋め込み、F54原経路上に**別の厳密な局所縦Mathlib Category**を構成した。選択F55 full shadowの加法性・単位零を証明。旧P77商から新P80商への**raw履歴を変えない全射**を定義し、縦合成・shadowの保存、真正C60での**非単射性**と、新P80商へのP59証明ラベル付き自由経路の厳密readout**非降下**を証明。P77合同は変更せず、P62相対coherenceとP59経路等号を混同しない。

- [F112-P82 #2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461)：P80の**全9種類のType値4-cell生成規則**に保存される、元F55 raw構文由来の独立Nat不変量を構成（旧P77の8生成規則についても別に保存を証明）。元の**縦左単位4-cell** `id ≫ f ~ f` の両代表元を同じ右raw恒等3-cellと元F55の方法で水平合成すると、非単位・非`trans`原証明について不変量が**1対2**となる。したがって水平合成後の**P80 Type値4-cellは存在せず、P80商クラスも異なる**ことを、実際の北側C60五角形のpentagon 3-cellを用いてLean4で証明。これにより、**選択したP80商へ元F55水平合成は一般には降下しない**。これはP80 presentationの不足を示すものであり、P62の構文的合同やstrict 3圏一般の不可能性ではない。

- [F112-P83 #2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463)：mathlibの`Quiver.Path.addWeight`を利用し、P82の**raw構文由来Nat不変量**を元F55の型付きP59自由経路全体へ拡張した。元F55の9構成子に沿った正規化の厳密保存と、**P62単位経路合同の全5生成規則**に対する保存を証明。そのため、P82の真正縦左単位4-cellを左右の同じ恒等証明と水平合成して得た2つのfree pathは、不変量**1対2**によって**P62でも比較不能**であり、P62 Mathlib商でも異なることをそのexact kernelから証明。真正C60北五角形の原pentagonを用いた実例も形式化。**既存P62の健全性を維持したまま、不足するcontext 4-cellを単純追加することはこの実例で不可能**。これは既存P62/P80の選択についてのobstructionであり、一般のstrict 3圏や空の不可能性ではない。

- [F112-P84 #2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465)：旧P62のunit-only経路合同とP80のType値raw4-cell証拠を**変更せず**、別の**P84水平4-cell証拠付きType依存free-path合同**を構成した。旧P62証拠、同値律、縦経路合成の合同に加え、**任意の真正P80 Type値4-cellを左右から原F55 raw 3-cellで水平whiskerする2つの比較規則**を明示。全7生成規則で元F55 full shadowが保存されることを証明し、mathlibのCongruence・厳密な局所CategoryTheory.Quotient・**商のexact witness kernel**・原shadowへの因子化を完成。旧P62商から新P84商への自然な比較関手と、原P59自由経路→旧P62商→新P84商の厳密な可換三角形も形式化した。P82/P83の比較は**旧P62商で非同一、新P84商では同一**となることを両商のexact kernelから証明し、真正C60北五角形でstrict enlargementを確認。旧P62/P80のobstructionは消去していない。

- [F112-P85 #2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467)：旧P80 Type値4-cellと原F55 raw証明履歴を保持し、**左右の水平whiskeringを証拠付き生成規則とする別のType値4-cell presentation**を構成。旧P80埋込み・反射/対称/推移・左右縦whisker・左右水平whiskerの**全8生成規則**について、**新P84の真正typed path合同への健全性**とF55 full shadow保存を独立に証明。実証拠の存在だけをkernelとするSetoid/商を構成し、元F54 routeを対象とする別の厳密な**局所縦Mathlib Category**を旧P77の実単位・結合4-cellにより構成。旧P80商から新P85商への全射と、元F55水平合成の**P80商×P80商→P85商という代表元独立の二入力演算**を真正左右4-cell証拠で証明。真正C60北五角形で旧P80商は非同一、新P85商は同一。旧P82・P83のobstructionは否定されず、旧P62への全面的健全性は主張しない。

- [F112-P86 #2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469)：旧P84経路合同と旧P85のType値4-cellを**変更せず**、左右context・pre/post F54 route・左右水平whiskeringの6種類の真正P85証拠付き比較を持つ**新P86経路合同（11生成規則）**と、その上の**新P86 Type値raw4-cell（12生成規則）**を構成。両者について元F55 full shadow保存を別々に証明し、新Type値4-cellの新経路合同健全性・証拠存在に基づくSetoid/商のexact kernelを形式化。経路合同側では厳密な局所Mathlib Category商、旧P84→新P86経路商の比較関手と可換因子化を構成。Type値4-cell側では元F54経路上の別の厳密局所縦Category、旧P85→新P86商の全射・縦合成保存、**P85商→P86商の左右context・pre/postcomposeの4種類の代表元独立輸送**および**旧P85商×旧P85商→新P86商**の真正証拠付き水平二入力演算を実装。真正C60北五角形の旧P85 4-cellを実際の左F45 contextに輸送するType値証拠とP86商等号も証明した。P82/P83の旧presentationに関するno-goは保持する。

- [F112-P87 #2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471)：P86の「旧P85商×旧P85商→新P86商」という段階的輸送から進み、**P87の真正Type値4-cell自身に左右context・pre/post F54 route・左右水平whiskeringを再帰的に施せる新presentation**を構成した。旧P86証拠を保持する12生成規則で原F55 full shadow保存と二入力の真正4-cell証拠を証明。対応するP87型付き経路合同（11生成規則）のfull shadow健全性・厳密な局所Mathlib Category商・source witness exact kernel・旧P86経路商からの比較関手と可換因子化を形式化。P87 4-cellをP87経路合同に健全と証明し、実4-cell証拠をkernelとするSetoid商、**厳密局所縦Category**、旧P86 4-cell商からの全射・縦合成保存を証明。さらに、**P87商→P87商の左右context・pre/postcomposeの全4演算**と**P87商×P87商→P87商への元F55水平合成の代表元独立な自己閉包**を構成。水平単位は旧P80の真正Type値単位4-cellから導出し、全full shadowの水平加法性を検証。元F55のinterchange二辺のfull shadow一致も証明したが、これを4-cell証拠の存在やstrict interchangeと同一視しない。P66のC60 disjoint squareにおける元F54二経路の非同一性・odd phaseは保持される。

- [F112-P88 #2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473)：原F55の9構成子に対する非可換`List Bool`ソース語を構成。縦合成の連結・左右contextによる`false`/`true`ラベル化を記録し、P77/P80/P85/P86/P87の**全Type値4-cell生成規則**で保存されることをLeanで証明した。型付き中間因子`f₂`と`g₁`が構文上非単位（語が非空）なら、縦・水平二順序の語は`L(f₁)++L(f₂)++R(g₁)++R(g₂)`と`L(f₁)++R(g₁)++L(f₂)++R(g₂)`で一致せず、**真正P87 Type値4-cellの非存在とP87商での厳密な非等号**が成立する。`p88_word_nil_iff_unitOnly`と真正C60北五角形・六角形disjoint squareの原始語も検証。これは**現在のP87 presentationに対する条件付きno-go**であり、strict 3圏一般の不可能性やC60上の任意の4因子の実現を主張しない。原full shadow一致は依然必要条件のみ。

- [F112-P89A #2475](https://github.com/itakura-hidetoshi/KuuOS/pull/2475)：**旧P87/P88を不変のまま**、旧P87 Type値証拠を埋め込む新たな真正P89 Type値4-cell presentationを構成。元F55の型付きinterchange二辺を比較する新しい**明示的interchange生成子**と旧12操作の再帰閉包を備え、全13生成規則の原F55 full shadow（整数charge・非零交換位相を含む）保存、真正source証拠存在をexact kernelとするSetoid/Quotient、旧P87→P89全射、新P89商でのraw interchange等号を証明。P88非可換語は非単位中間因子に対し新比較で保存不能と証明。**旧P87でinterchangeを証明したことにはならない**。

- [F112-P89B #2476](https://github.com/itakura-hidetoshi/KuuOS/pull/2476)：新P89商自身の厳密局所縦Mathlib `Category`、左右context・pre/post、P89×P89→P89の代表元独立な原F55水平二入力合成、真正P80単位証拠からの水平単位、原full shadowの加法保存を形式化。**任意の4つの合成可能なP89商クラスに対して、縦・水平合成のstrict interchange等式を証明**。型付き中間因子が非単位のとき旧P87商では非同一・新P89商では同一という条件付きstrict enlargementを証明した。**F54経路対象の異なるものの同一視、水平結合律、高次coherence、大域strict 3/nやhyperdescentは未証明**。

- [F112-P90A #2478](https://github.com/itakura-hidetoshi/KuuOS/pull/2478)：原F45木の内部節点数・根の左部分木節点数という独立不変量を作り、任意6つのNat深さ・両軸F19/F28 Blocksで**両軸Nat.add_assoc cast後も三項bracketingの原F45木は不等**と証明。一方、全物理sector列は一致し、真正Type値F54 associator route（原始回転1）が存在する。真正C60北五角形でも不等を確認。これは元の木の等号や全水平結合律の証明ではない。

- [F112-P90B #2479](https://github.com/itakura-hidetoshi/KuuOS/pull/2479)：任意3本の型付き原F54経路について、`((u⊗v)⊗w) ≫ assoc(after)`と`assoc(before) ≫ (u⊗(v⊗w))`を**同じF45境界の真正Type値F54経路**として構成。原始回転数一致を証明したが、最初の原ソース合成規則は`1`対`0`で**raw経路は不等**。その間の真正F55 `PresentedCell`は未充足の**型付き比較slot**としてのみ定義。inhabitantやcoherenceは仮定していない。

- [F112-P91A #2481](https://github.com/itakura-hidetoshi/KuuOS/pull/2481)：原F55九構成子すべてについて**F54原始回転数の差＝F55五角形整数電荷**をLeanで証明。P90Bの未充足associator自然性比較slotに真正F55証拠が存在するなら、両経路は同回転数なので**五角形整数電荷は0**でなければならない。さらに原F55交換整数電荷と奇位相のparity制約から、必要なfull shadow形状を明示。これは証拠存在・全水平結合律を証明したものではない。

- [F112-P91B #2482](https://github.com/itakura-hidetoshi/KuuOS/pull/2482)：真正原F55九構成子の**Type値証拠の存在をexact kernelとする別のF54経路対象商**を構成。P67のsquare-only商→新P91B商の全射と、旧P67商では回転数が降下する一方、新商では真正五角形の**3回転と2回転が同一視されるため回転数が降下不能**なことを厳密証明。元のC60北五角形はraw非同一・新商同一、真正F55証拠の電荷は元ソースに残る。P90Bの二経路の新商等号は**未充足F55比較slotの証拠存在と同値**であり、どちらも未証明。

**P91A/P91Bで、P89 strict interchangeの先に残るF54水平結合の必要条件と情報損失を明示しました。** P91Aの回転数差＝五角形電荷から、P90の真正F55 associator自然性証拠が存在する場合の五角形電荷0・交換電荷parity制約を証明。P91Bでは原F55 Type値証拠の存在だけからF54経路商を作り、P67のsquare-only商では保存できた原回転数が、F55 pentagonを含む新商には降下できないことを証明。**P90比較slotのinhabitant、水平結合律、4-cell coherence、globularityはなお未証明**であり、商クラス等号・原raw等号・真正証拠の選択を混同しません。旧P87/P88のno-go、新P89 interchange、原C60の非零奇位相、C60以前のW/J/Hと空の空、独立Kuuは一つのpresentationという原則を保持。Grayには戻りません。

## 五行・Qiも別の具体的presentation

mainで統合済みのQi v3.1–v3.3では`FivePhase = ZMod 5`を用い、相生を`+1`、相剋を`+2`の作用として表現します。同じ到達位相と同じ生成履歴は同一ではありません。

[Qi v3.1 #2366](https://github.com/itakura-hidetoshi/KuuOS/pull/2366)は忠実な巡回作用と型付き自由経路、[v3.2 #2369](https://github.com/itakura-hidetoshi/KuuOS/pull/2369)は明示した観測合同、[v3.3 #2371](https://github.com/itakura-hidetoshi/KuuOS/pull/2371)は到達可能観測圏との圏同値を証明します。観測合同が元の全履歴を回復するとは言いません。五行群論は臨床・物理現象の因果的実証と混同しません。

## これからの証明目標：strict 3/n圏から(∞,3)-hyperdescentへ

**次のF112-P94D3GA（仮称）：** FZ [#2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710)で、真のraw17D依存型経路・元18D `assoc/post/pre`生成子ファイバーのそれぞれの可算性を仮定した元source可算性伝播、物理18Dの最小正規生成Cardinal`ℵ₀`、元source可算性とexact`ℵ₀`正規表示の条件付き同値を証明しました。次は下位primitive Typeの可算性から`NativeC60AXStep` raw17D四構成子と18D三構成子の**全再帰的Countable導出**を、型付き符号化と帰納法で構成します。実受信像の可算性も別条件であり、無条件の可算性は未証明。

1. **一般理論の継承と照合：** 上記の`W/J/H`、普遍性、stack、scaled-horn、obstruction、actual-liftの定理を保持し、strict化に必要な強化・比較条件を洗い出す。
2. **局所strict 3圏：** 真正C60を含む具体例および一般的な文脈ソースに対して、証明関連3射のデータと厳密なinterchangeを形式化する。raw自由構文・path envelope・選択した商を混同しない。
3. **大域strict 3圏、strict n圏：** 真正なoverlap上のtransport、制限、三重以上の整合、gluingと高次結合律を証明し、globular strict n構造へ拡張する。C60上の証明を他の文脈に無条件には外挿しない。
4. **`(∞,3)`への橋：** strict n圏の列が自動的に一般の`(∞,3)`圏になるとは仮定しない。4射以上の可逆性、coherentな比較、使用モデルでの普遍性を別途証明する。
5. **hyperdescent：** 適切な高次値`F`とhypercover `U• → U`に対して`F(U) ≃ holim F(U•)`を証明する。普通のsheaf/stack・有限Čech descentを言い換えるだけでは不十分。
6. **一般化と空の空：** 文脈・被覆・presentationを変えた際にどの定理が保存されるか、どの障害が残るかを分類する。完成した構造も絶対的な「空」として実体化しない。

より詳しい証明義務・完了条件は[ROADMAP](ROADMAP.md)を参照してください。

## 正本、ビルド、検証

- **最新の統合証明receipt（2026-10-30）：** [F112-P94D3FZ #2710](https://github.com/itakura-hidetoshi/KuuOS/pull/2710) squash MERGED、定理SHA `99ccc5b7a6aaeb4166715a2b75a5fc14053dd103`。PR exact-source-head [Strict Lean #40972305445](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/40972305445) **9042/9042 SUCCESS**、Governance **30/30 completed SUCCESS**。FZ新規9宣言の依存は標準3公理以内、`sorryAx`なし、変更Lean warning/error 0/0、sourceとmerge-test Git tree一致。歴史的FY #2708（9041）、FX #2706（9040）、FW #2704（9039）、FV #2702（9038）、FU #2700（9037）および前段階の独立receipt保持。
- **文書・CIのauthority境界：** theorem-carrierはcanonical `main`上のLean宣言とその型・公理依存であり、README/ROADMAPの到達点やCIの緑表示は証明そのものの代わりではありません。docs-only変更に不要なStrict Leanを再実行して数学の成立を水増ししません。歴史的CI数値は下記の時点別台帳として保存します。

- **以前の統合・CI履歴（P79以降、各時点のreceipt）：** [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main)。F112親PR #2339はMERGED。P79 #2455：Lean **9687/9687**・17宣言、P80 #2457：**9688/9688**・14宣言、P81 [#2459](https://github.com/itakura-hidetoshi/KuuOS/pull/2459)：**9689/9689**・13宣言を`KuuOSFormal`統合入口で検証し、いずれも新規`sorryAx`なし・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts 2/2 SUCCESS後にsquash MERGED。P81統合SHA `5c9925528d8a90239375104a2ac1a5e71e483559`。続くP82 [#2461](https://github.com/itakura-hidetoshi/KuuOS/pull/2461)は **9690/9690**・新規公理監査**10/10**（`sorryAx`なし）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P82統合SHA `f7a876996cebd940ea3d8bbacaa75e51ac781422`。P83 [#2463](https://github.com/itakura-hidetoshi/KuuOS/pull/2463)：**9691/9691**・公理監査**10/10**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P83統合SHA `7bd530e28551881198c3c61e22b6163c9025753e`。P84 [#2465](https://github.com/itakura-hidetoshi/KuuOS/pull/2465)は **9692/9692**・新規公理監査**18/18**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P84統合SHA `90be8065f5b4b682f239c7bfd220e48ab2c97f27`。P85 [#2467](https://github.com/itakura-hidetoshi/KuuOS/pull/2467)は **9693/9693**・新規公理監査**18/18**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P85統合SHA `19c787422a3c234c0a4e5e8777d1730deb56313e`。P86 [#2469](https://github.com/itakura-hidetoshi/KuuOS/pull/2469)は **9695/9695**・新規公理監査**37/37**（`sorryAx`なし、標準的`propext`・`Classical.choice`・`Quot.sound`のみ）・新規Leanエラー/警告0・107公開root保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P86数学統合SHA `2efbce7af262c9c8203bc7e3fc6c24a3c6139e73`。P87 [#2471](https://github.com/itakura-hidetoshi/KuuOS/pull/2471)は **9698/9698**・新規公理監査 **39/39**（`sorryAx`なし。`propext`・`Classical.choice`・`Quot.sound`のみ）・変更ファイルLeanエラー/警告0・107公開root全件保全・exact-head Governance・completion receipts **2/2 SUCCESS**後にsquash MERGED。P87数学統合SHA `32cbcd465a932d0b66524ab56026880d6fdf1227`。P87の3モジュールも単一公開入口`formal/KuuOSFormal.lean`から直接import。P88 [#2473](https://github.com/itakura-hidetoshi/KuuOS/pull/2473)は **9700/9700**・新規公理監査**18/18**（`sorryAx`なし）・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance [#39769469429](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/39769469429) SUCCESS・completion receipts **2/2 SUCCESS**後にsquash MERGED（SHA `2eef23640dcc4f30144d2a7b13489c0d72165d99`）。P88A/Bも同じ公開入口から直接import。P89A [#2475](https://github.com/itakura-hidetoshi/KuuOS/pull/2475)は **9701/9701**・公理監査**10/10**、P89B [#2476](https://github.com/itakura-hidetoshi/KuuOS/pull/2476)は **9702/9702**・公理監査**13/13**（いずれも`sorryAx`なし・変更ファイルLeanエラー/警告0・107公開root保全・exact-head Governance SUCCESS・completion receipts **2/2 SUCCESS**）。P89A統合SHA `cab73a59bae36824c3dcb9a4a1b9ab3bcd804b06`、P89B統合SHA `59fa3d761c8133c621114d01c9567d4e2d09ad99`。P90A [#2478](https://github.com/itakura-hidetoshi/KuuOS/pull/2478)は **9703/9703**・公理監査**7/7**・統合SHA `4f77b8e7043b62d9cd95ee2505f28f272fe5684b`、P90B [#2479](https://github.com/itakura-hidetoshi/KuuOS/pull/2479)は **9704/9704**・公理監査**7/7**・統合SHA `43de1eaf5676614b879517bf0ca0e24207fc0f83`。両方とも`sorryAx`なし・Lean警告/エラー0・107公開root保全・exact-head Governance・completion receipts 2/2 SUCCESS。全モジュールを公開`KuuOSFormal`に直接importし、`KuuOSStrict`は内部集約のみ。
- **F112-P91 exact-head数学：** P91A [#2481](https://github.com/itakura-hidetoshi/KuuOS/pull/2481)は **9705/9705 SUCCESS**・公理監査**4/4**・squash SHA `153361ebc9bf4303ed9c79e931c768fc99a885af`。P91B [#2482](https://github.com/itakura-hidetoshi/KuuOS/pull/2482)は **9706/9706 SUCCESS**・公理監査**13/13**・squash SHA `8fd61aad78943f6c9c630a585450eac2b5246f90`。両PRとも`#print axioms`に`sorryAx`なし、変更ファイルLeanエラー/警告0、107公開root保全、Governance・completion receipts **2/2 SUCCESS**。
- **唯一の通常ビルド入口：** `lake build` = `lake build KuuOSFormal`。既存**107公開root**と独立Kuu・Qiを一つのパッケージで保持。`KuuOSStrict`は内部import集約で、独立した権威や「唯一の空」ではありません。
- **ツールチェーン：** Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。PR #1558（Lean 4.31）はvalidation-only・未マージ。
- **証明の判定：** 実際のLean宣言とその型・仮定、`#print axioms`、対象commitのexact-head CIを根拠とします。`sorryAx`、`sorry`、`admit`や未証明の新公理で目標を埋めません。歴史的なmathlib/finite `native_decide`依存は正確に区別します。
- **CI高速化：** 共有cache、差分モジュールの部分ビルド、不要な重複実行の削減は可。ただし旧公開rootの削除や証明義務の弱化で高速化しません。

~~~bash
python3 scripts/run_kuu_foundation_check.py
lake exe cache get  # 初回・必要なキャッシュがないときだけ
lake build KuuOSFormal # warningAsErrorはlakefile.tomlで既定設定。sorryAxは#print axiomsで監査。
~~~

AI推論runtimeの方向は **観測 → 文脈・複数presentation → 輸送と2/3-cell比較 → 整合する場合のdescent/glue、しない場合のobstruction保持 → 権限確認 → 行為または再観測** です。この推論設計も実行保証・臨床的実証・全LLM出力の形式的正しさとは区別します。

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
