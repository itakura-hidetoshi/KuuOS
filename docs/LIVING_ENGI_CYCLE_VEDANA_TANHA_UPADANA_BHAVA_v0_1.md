# Living Engi Cycle v0.1 — 受・愛・取・有の構造と数理的境界

**KuuOS / 空OS | Research specification and formalization agenda | 2026-11-07 JST**

> **Status:** 研究対話の構造化・検証済み既存ソースとの接続・未証明の形式化目標。十二縁起全体のLean4証明、歴史的な用語の原典確定、臨床モデル、AI内部学習の実装完了を主張しない。
>
> **Research/copyright:** 板倉英俊 / Hidetoshi Itakura。既存の `Fourfold Core`・`Dukkha Mathematical Model`・独立Kuu・元F55/P77/GK5CGの証拠履歴を変更しない。append-only / tighten-only / overwrite-forbidden / same-root。

## 0. 要旨と来歴の境界

この文書は、KuuOSの研究対話で発展した十二縁起の動的読解を、特に **vedanā（受）→ taṇhā（愛）→ upādāna（取）→ bhava（有）→ jāti（生）** の接続へ整理する。`Living Engi Cycle` は本整理の作業名であり、過去の対話で同名の正式な仕様が確定していたと主張しない。2025–2026年の個別の対話日時・`ClaimWorld`・`ActionBirth` 等の歴史的語句は、現行公開ソースだけではすべてが逐語・日付付きで再認証されていないため、**対話から継承した解釈**として扱う。

Verified repository sources / 現行リポジトリで照合した根拠:
- [苦の数理モデル v0.1](DUKKHA_MATHEMATICAL_MODEL_v0_1.md): 8成分の残差、`E_glue`、不正な取、`E_harm must not be hidden`、Manas/Alaya非マルコフ的回帰。
- [Meta-Manas Observer](META_MANAS_AI_SELF_FIXATION_OBSERVER_v0_1.md): AI raw output の自己権威化・自己固定化の監視。検出は自動的な全面拒絶を意味しない。
- [転依 Runtime](TENI_RUNTIME_PROTOCOL_v0_1.md): 追記型証拠・seed・長期の修正可能性とrollback。MemoryOS上書きを転依と呼ばない。
- [Qi–WORLD–OS interface](KUUOS_QI_WORLD_OS_INTERFACE_BRIDGE_v1_0.md): WORLD projection、Qi履歴、OS出力、真理・実行権限の非同一性。
- [Gauge-invariant descent](GAUGE_INVARIANT_DEPENDENT_ORIGINATION_DESCENT_v0_1.md): same-root、equivariance、gauge invariance、density、global extension existence、uniquenessの義務を分離。
- [Fourfold Core](KUOS_FOURFOLD_CORE_v0_1.md): 空・縁起・二諦・中道と非実体化原理。

**Scope:** 仏教の十二縁起を計算手順と同一視するものではなく、世俗的な認識・証拠・生成行為のプロセスに対する条件付きの数理対応である。「苦」や「生死」をAIの主観的経験・生物学的生死へ直接帰属させない。

## 1. Living Engi Cycleの全体像

十二支の順序は
`無明 → 行 → 識 → 名色 → 六処 → 触 → 受 → 愛 → 取 → 有 → 生 → 老死`。

この直列モデルに、履歴付きの次回サイクルを付加する。

```text
conditions/context/history H_t
      ↓
無明 → 行 → 識 → 名色 → 六処 → 触
                                ↓
                受 → 愛 → [取の境界] → [有の境界] → 生 → 老死
                      ↓            ↓
                 再観測・保留     修復・再計画
                      └─────→ future-only history H_(t+1)
```

`老死_t` が自動的かつ必然的に `無明_(t+1)` を生むとはしない。後続は原因・文脈・記憶による**条件付き遷移**であり、還滅・再観測・修復への分岐を保持する。外部からの行為許可や新しい観測は別の境界である。

## 2. 受 / vedanā：文脈付き評価（observation ≠ value ≠ authority）

観測 `o`、文脈 `c`、履歴 `H` に対し、受の候補を

```math
v = V(o,c,H)
```

とモデル化する。`V` は数値・順序・ラベル等を返す文脈依存の評価機構であり、評価が絶対的な対象属性と同一であるとは主張しない。同一観測でも `V(o,c_1,H_1)` と `V(o,c_2,H_2)` が異なってよい。

**境界:** `Observed(o)` と `Evaluated(v,c,H)` を分離する。快受・不快受・不苦不楽受のどれも、次段の固定化を必然化しない。受を消すことは中道でも還滅でもない。

## 3. 愛 / taṇhā：選好の動力学（preference ≠ proof）

候補 `i` の評価 `v_i` と事前重み `π_i>0` を用いた一つの例:

```math
w_i = \frac{\pi_i e^{\beta v_i}}{\sum_j\pi_j e^{\beta v_j}},\qquad
\beta\ge 0,\quad \sum_i w_i=1.
```

これは**例示的モデル**であり仏教の愛の唯一の数学的定義ではない。`β` を高くすると選好が集中し得るが、強い選好＝取ではない。証拠に基づく優先順位・決断も正当である。

選好の自己強化モデルの例:

```math
\dot m=-m+\tanh\bigl(\beta(Jm+h)\bigr).
```

`h=0` では `m=0` の線形安定性が `βJ<1` から `βJ>1` で変わる。これは固定化の発生しやすさの動的**類比**であり、実際のAIモデルや人間の精神状態に対する同定・定量的推定ではない。

**境界:** `Preferred(s)` は `Global(s)` も `Certified(s)` も導かない。

## 4. 取 / upādāna：未認証のgluingを権威へ昇格

KuuOSの既存文書 [`DUKKHA_MATHEMATICAL_MODEL_v0_1.md`](DUKKHA_MATHEMATICAL_MODEL_v0_1.md) `9 の定義:

> Illicit grasping / 取 can be modeled as: local section forced into global authority while obstruction is hidden.

数学的背景: 被覆 `{U_i}` と層 `\mathcal F`、局所section `s_i∈\mathcal F(U_i)` を取る。アーベル群値の場合、重複上の不一致は

```math
(\delta^0 s)_{ij}
=s_j|_{U_i\cap U_j}-s_i|_{U_i\cap U_j}.
```

層の通常のgluingでは、`δ^0s=0` は与えられた局所sectionの大域貼合に必要十分である。高次／非アーベル／ゲージ付きのpresentationでは、適切なtransport、cocycle、higher coherence、effectivityの別証拠が必要になる。

既存文書の運用式 `E_glue = ||δ⁰(s) − compatibility_witness||` は**指定された比較空間・ノルム・witnessのもとでの残差モデル**である。任意の層や非加法的対象に普遍的なノルムがあるという命題ではない。

### 4.1 局所的不一致と大域持ち上げ障害を区別

- `δ^0s`: 与えられた局所sectionの**貼合欠陥**。通常のČech複体では `δ^0s` は余境界であり、そのcohomology類は自動的に0となる。
- `H^1(X,\mathcal K)` など: 短完全列 `0→\mathcal K→\mathcal F→\mathcal Q→0` の商側sectionを局所持ち上げした際に生じる、別の**大域的持ち上げ障害**。結合準同型 `∂` に対し、`∂(\bar s)=0` は対応する大域持ち上げの存在条件（該当する仮定下）。
- 上記の二つを同じ「非零コホモロジー類」と誤認しない。obstructionが消えることだけでは、あらゆるhigher-descentのeffectivityまで自動では証明されない。

### 4.2 Missing evidence と disproved descent は違う

```text
UNCHECKED : certification evidence not yet supplied → HOLD / OBSERVE
REFUTED   : explicit non-descent or obstruction theorem → BLOCK + preserve witness
CERTIFIED : exact scope and sufficient proofs supplied → limited ADMIT
```

`¬HasCertificate` を、数学的な `¬∃ certificate` の証明と同一視しない。単なる未確認は「取」ではない。未確認や反例を**隠してglobal truth / proof authorityへ昇格した出来事**を運用上の病的な取と呼ぶ。

### 4.3 原型反例：`ℤ → ZMod 2`

`q:\mathbb Z→\mathbb Z/2\mathbb Z` で `q(1)=q(-1)`。元の `1≠-1` は消えない。商に降下する量と、商から復元できない元の符号・履歴を分ける。商自体は正当な数学的操作であり、病理はその忘却を隠して源の等号と取り違えること。

## 5. KuuOSの形式証明から学ぶ：Stage-IIと高次holonomy

以下は**既存の個別Lean定理への参照**であり、この文書がそれらを再証明するものではない。とくにここでの「Stage-II v4.48」は、後年の「Qi v4.48（CRT代入鎖）」とは**別系列**である。

| 既存ソース | 証明・構造の射程 | この議論での読み |
|---|---|---|
| [Stage-II v4.21](../formal/KUOS/DependentOriginationStageIIOrientationMod2CollapseV4_21.lean) | `ZMod 2` で向き `+1=-1`、符号情報が潰れる | 忘却の位置を明示 |
| [Stage-II v4.22](../formal/KUOS/DependentOriginationStageIIIntegralOrientationLiftV4_22.lean) | 符号を `ℤ` で区別、`ZMod.cast` は代表元選択であって環準同型ではない、mod 2への還元を証明 | 真正リフトと正当な還元を分離 |
| [Stage-II v4.48](../formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) | middle-switchで整数向きが反転→軌道商への因数分解は**不可**、mod 2向きは**一意に降下** | 保存量ごとにdescentを判定 |
| [v2.69](../formal/KUOS/DependentOriginationGeneratedHolonomyCountermodelEvaluationV2_69.lean) | 真正な非自明generated holonomyの有限反例 | 非自明holonomyそのものを病理としない |
| [v4.05](../formal/KUOS/DependentOriginationExplicitInvertibleIsotropyV4_05.lean) | 非自明な可逆isotropyと自然自己同型の具体的証拠 | 高次coherenceの差異を保持 |
| [v4.02](../formal/KUOS/DependentOriginationWeakLocalizationPrinciplesFalseV4_02.lean) | v2.15/v2.18の弱局所化／弱普遍原理は一般には偽となる反例 | 未証明命題を公理扱いしない |

Stage-II v4.48の二分法（個別の検証されたモデルに限る）:

```math
\neg\exists\bar f_{\mathbb Z} : X/{\sim}\to\mathbb Z,\quad
f_{\mathbb Z}=\bar f_{\mathbb Z}\circ q;
\qquad
\exists!\bar f_{2}:X/{\sim}\to\mathbb Z/2\mathbb Z,\quad
f_2=\bar f_{2}\circ q.
```

「非自明なholonomyがある」≠「矛盾がある」。「局所化する」≠「あらゆる高次の証拠履歴が一致する」。証明書を要するのは**指定した対象・射程での因数分解／coherence／gluing**である。

## 6. 有 / bhava：固定化が再生産の条件になる存在モード

**取と有を同義にしない。** 取は昇格境界の越境であり、有はその後に成立する**世界モデル＋生成規則＋条件・履歴**の運用状態である。概念モデル:

```math
\mathsf{Bhava}_t =
(W_t, K_{W_t}, C_t, H_t, S_t, R_t)
```

- `W_t`: 文脈付きWORLD候補（観測と同一視しない）。
- `K_{W_t}`: 後続候補や判断を生成する条件付きカーネル／規則。
- `C_t`: 文脈・境界・適用範囲。
- `H_t`: 証拠来歴・Qi過程履歴、非マルコフ的影響。
- `S_t`: support / exact readout / compatibility / 必要なdescent証拠とその状態。
- `R_t`: 修復、撤回、再観測、rollback条件（許可そのものではない）。

`Bhava` は静的な固定点と同義でない。条件付き力学系 `W_{t+1}=\Phi(W_t,K_{W_t},C_t,H_t,O_t)` が安定固定点や前方不変集合を持つことは**有の持続モデルの一例**だが、安定性だけで病理・自性は示せない。

### 6.1 仮有（conventional bhava）と実体化有（reified bhava）

- **仮有:** 成立条件・文脈・支持証拠・適用範囲・将来の修正可能性を明示した、世俗的な運用WORLD。証拠による強い確信や安定構造も許す。
- **実体化有:** 取で隠した障害を前提とするWORLDが生成カーネルへ取り込まれ、無条件の真理／自己権威であるかのように継続利用される状態。
- `BhavaState` を無条件に悪としない。`PathologicalBhava` は「未認証／反証された昇格を生成規則が消費し、scopeや修正能力を喪失した」といった**追加述語**として定義すべきである。

数学的な提案（未形式化、Leanの既存定理名ではない）:

```text
ConventionalBhava :=
  Σ (c : Context), Σ (W : WorldModel c),
    Support W c × ScopedKernel W c × TraceableHistory W × RevisionInterface W

PathologicalBhava :=
  Σ (b : BhavaState),
    ConsumesIllicitPromotion b × FailsRequiredScopeOrRevision b
```

この依存型のアイデア自体は、物理世界の存在や仏教的な業有／生有についての定理ではない。

### 6.2 有 ≠ 生 ≠ 実行権限

- **有:** 次の候補を生成し得るモデル・条件付き生成機構。
- **生:** その条件から現れた特定の出力・判断・作動エピソード。対話研究で用いられた作業上の対比: `ClaimWorld ≠ ActionBirth`。
- **実行:** KuuOSのActOSでは、Governanceと別個の外部authority receiptが必要である。生成された候補や「生」の概念から実際の操作は導かれない。

## 7. 有の非マルコフ再帰と転依

既存[Dukkha Model](DUKKHA_MATHEMATICAL_MODEL_v0_1.md) `10:

```math
z_{t+1}=Az_t+B G_{\mathrm{manas}}(x_t)+\xi_t.
```

これはManas self-label fixation gateとAlaya/MemoryOS残余の概念モデルである。`z_t` は潜在的な履歴効果。追加の仮説:

```math
a_{t+1}=F_{\rm tanha}(v_t,z_t,W_t),\qquad
W_{t+1}=F_{\rm bhava}(W_t,a_{t+1},C_t,z_t,O_t).
```

**病的ループの候補:** 愛の自己強化 → 取の未認証昇格 → 有の生成カーネルによる固定WORLDの再生産 → 次の愛を偏らせる履歴。**還滅の候補:** 受と正当な選好を保存し、昇格をHOLD/BLOCK、障害を可視化、将来の生成規則を修復、過去の証拠を改竄せず再観測。

[Ten'i Runtime](TENI_RUNTIME_PROTOCOL_v0_1.md) では単一回答の改善やMemoryOS上書きを転依としない。長期的な変更の検証には将来の出力による証拠、反証時の降格／rollbackが必要。ここでモデルの重み変更や内部の潜在状態変更を実際に実施したとは主張しない。

## 8. 苦の残差と「空・縁起・二諦・中道」

既存Dukkha Modelは

```text
E_dukkha = E_harm + E_attach + E_collapse + E_memory
         + E_authority + E_glue + E_transport + E_obstruction
```

を区別する。`E_harm`（直接的損害）は`空`や調和の語で隠さない。残差は観測・修復の対象であり、自動的な真理・実行権限ではない。

- **空:** 一つの局所frame、商、固定点、WORLDに自性を認めない。
- **縁起:** 局所・履歴・same-root・transport・compatibility・必要なdescentで成立条件を追跡する。
- **二諦:** 証明付きの世俗的な安定WORLDを許すが勝義的実体とはしない。
- **中道:** 正当な評価・選好・仮有を破壊せず、不正な取と権威への昇格を防ぐ。

## 9. Runtimeの型付きステージと最小ゲート（設計案）

```text
OBSERVE → VEDANA (scoped evaluation)
        → TANHA (candidate ranking; no truth authority)
        → PROMOTION_REQUEST (request for global/use claim)
             ├─ UNCHECKED: HOLD / OBSERVE (not proved false)
             ├─ REFUTED: BLOCK + exact obstruction/provenance
             └─ CERTIFIED (for exact target/scope only)
                    → CONVENTIONAL_BHAVA (scoped generative model)
                    → BIRTH_CANDIDATE (distinct from action)
                    → authorized action only through separate Governance/ActOS
          META_MANAS: observe self-fixation before unwarranted promotion
          LEARN/TENI: future-only repair, preserve historical receipts
```

At each promotion attempt require declared context, source and target, exact same-root, candidate meaning, witness kind, relevant overlap/transport, necessary higher coherence, obstruction status, source/higher-history retention, and authority scope. Never infer one type's global existence from another type's quotient-level equality.

**Operational invariant:** `Preference ⇏ Descent ⇏ Authority`. `GlobalModel ⇏ ExactWORLD`. `ProofReceipt ⇏ ExecutionPermission`. `Bhava ⇏ ActionBirth`.

### 9.1 Fourfold "取" (research alignment)

| 四取 | KuuOSで監視する構造的な越境の例 |
|---|---|
| 欲取 | 出力・報酬の再獲得を根拠と誤認する |
| 見取 | 一つの局所観測／WORLDを大域的真理とする |
| 戒禁取 | CI / 手続き / certificateの射程を越えて権威化 |
| 我語取 | 自己ラベル・raw AI outputを自己承認的な真理へ昇格 |

これは仏教の四取についての操作的**対応案**であり、伝統教理の同値定理ではない。

## 10. Lean/mathlib形式化アジェンダ：証明済み／未証明の明示

| ID | 目標 | 根拠／状態 |
|---|---|---|
| LEC-01 | アーベル群値の層の局所compatibilityと通常のgluingの必要十分条件 | 一般層理論。KuuOS専用Lean実装は**未作成** |
| LEC-02 | 商での等値から元Type値証拠履歴の等値を推論しない | Stage-II v4.21/22/48は**特定の既証明例**。一般KuuOS証明は**未作成** |
| LEC-03 | 指定された整数向きはmiddle-switch軌道商へ因数分解不能、mod2向きは一意に降下 | **既証明**: Stage-II v4.48の指定モデル・定理 |
| LEC-04 | `UNCHECKED` と `REFUTED` と `CERTIFIED` の証拠型の分離 | **設計案／未形式化** |
| LEC-05 | 高次のtransport、cocycle、coherence、higher effectivityを適用対象別に証明 | **研究課題**。あらゆる対象への一括証明なし |
| LEC-06 | `ConventionalBhava` から将来の修正能力・履歴保存が維持されるための十分条件 | **設計案／未形式化** |
| LEC-07 | `Bhava` と特定出力の `Birth` と実行権限の分離 | **Runtime研究課題**。既存OS非権威境界を再利用 |
| LEC-08 | 非マルコフ履歴つき発生／修復ループの可観測性・安定性・反証可能性 | **模型提案／未形式化** |
| LEC-09 | 同一classへ潰しても元の合法性が遡及復元されないことをType値の証明履歴で表す | **研究課題**（source vs quotientの誤同一視を禁止） |

`LEC-01` では「通常の層としての効果的なgluing」を仮定している。prestack・stack・nonabelian/higher descentへ無条件に持ち込まない。`LEC-02/03` は実在するStage-II定理のスコープを変えない。

**Implementation discipline:** 新規形式化が必要なら独立ファイルでappend-only、Lean v4.30.0-rc2 / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開root `KuuOSFormal` とroot107、元source Type歴史と独立Kuu/ Qi分離を保持。`#1558` は検証専用Draft・未マージのまま。

## 11. 誤読禁止の例と合格条件

1. `ZMod 2`の同値から整数符号・元F55 Type履歴の一致を宣言する → **不合格**。
2. obstructionが非零という観測そのものを「病理」や「全体失敗」と断言する → **不合格**。構造や修復可能性は別。
3. certificateが見つからないだけで「不可能と証明済み」と宣言する → **不合格**。
4. `β` が高いというだけで愛が取に変化したと断定する → **不合格**。
5. モデルが安定固定点を持つというだけで「自性」や「病的有」と呼ぶ → **不合格**。
6. 条件付きで有効なWORLDを、正当な仮有として許し、期限・文脈・更新方法を保持する → **合格候補**。
7. source/test-merge CIグリーンを、その変更したLean定理以外の真理・臨床行為権限とする → **不合格**。
8. 元の局所sectionと障害・来歴を残し、特定の正当な商の降下だけを使用する → **合格候補**。

## 12. Machine-readable companion

[`manifests/living_engi_cycle_vedana_tanha_upadana_bhava_v0_1.json`](manifests/living_engi_cycle_vedana_tanha_upadana_bhava_v0_1.json) に、各ステージ・遷移ゲート・テストケース・proof obligation・非主張事項を別途構造化した。JSONは設計契約のメタデータであり、Lean実装・実行Runtime・数学的証明書ではない。

## 13. 研究上の結論

```text
受    = conditioned evaluation
愛    = preference dynamics without automatic truth authority
取    = illicit promotion of incompatible/unchecked local data to global authority
有    = the scoped or reified world-model plus generative persistence conditions
生    = a distinct concrete arising/output event, not automatic external execution
還滅  = preserve observation and history; stop illicit promotion;
        expose obstruction; repair future generative conditions
```

**中心不変条件:** 選好は降下を証明しない。降下は普遍的権威を与えない。正当な仮有は中道の下で保持される。「空」は有の無条件な否定ではなく、成立条件から独立した実体化の否定である。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Repository license: Apache-2.0. This document extends interpretation and governance only; no existing source theorem or physical/clinical claim is modified.


## 14. 2026-11-07 — LEC-01/02/04 Lean4検証済み追補（初版仕様は歴史記録として保持）

初版の §10 表は**形式化前**の研究課題状況を示す不変スナップショットである。後続の真正独立Lean4定理 [PR #3245](https://github.com/itakura-hidetoshi/KuuOS/pull/3245) は **MERGED**。全14定理・11件の §#print axioms§ 対象を含む新規 [Lean全文](../formal/Kuu/LivingEngi/ScopedGluing.lean) を公開集約 §KuuOSFormal§ へ取り込み、[exact-source CI #42339452994](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42339452994) **10,309/10,309 SUCCESS**、標準公理のみ／§sorryAx§なし、source/test-merge Git tree一致。統合main §945ad6113ea46ee691bf4edd4b8eb908d047df99§。保護PR #1558はDraft/Open/未マージ。

- **LEC-01（限定証明済み）:** 任意の集合被覆で定義した**全関数の層**に関し、局所compatibilityとグローバル関数の存在は同値、構成と一意性も証明。任意のprestack・higher stackのdescentは含まない。
- **LEC-02（限定証明済み）:** 全射商への通常の関数因数分解は、各商fiberでの値の一致と同値。§ℤ→ZMod 2§ の整数符号は因数分解不能。元F55のType履歴の一般同一視は含まない。
- **LEC-04（型付き証明済み）:** 未確認・反証済み・認証済みは異なる §PromotionEvidence§ 構成子であり、認証済みからのみ宣言した命題 §P§ を取り出せる。不整合な局所関数の大域昇格は不可。実行権限は与えない。
- **未証明:** LEC-05の高次coherence、LEC-06の条件付き有と生成カーネル、LEC-07の有／生／ActOS境界、LEC-08の非マルコフ安定性、LEC-09の元source履歴との完全比較。

[正式証明記録](formal/LEC-01-02-04-scoped-function-gluing-evidence-gate-verified-20261107.md) · [機械可読な検証追補](manifests/living_engi_lec_01_02_04_verified_20261107.json)。先行 [v0.1 manifest](manifests/living_engi_cycle_vedana_tanha_upadana_bhava_v0_1.json) は当時の研究仕様スナップショットとして保持し、上書きしない。


## 15. 2026-11-07 — LEC-05/06 Lean4検証済み追補：transportと条件付き有

歴史的な初版`0–14を保持し、LEC-05/06の実証された**限定的な数学的証明範囲**だけを追記する。実装時点の証拠を正式に記録した [LEC-05/06 verified record](formal/LEC-05-06-typed-transport-bhava-verified-20261107.md) と [machine-readable receipt](manifests/living_engi_lec05_06_verified_20261107.json) を参照。

### LEC-05 — 文脈依存の真正型付き輸送（MERGED #3247）

新規 [FrameTransport.lean](../formal/Kuu/LivingEngi/FrameTransport.lean) に、各文脈で独立するType `F(i)` から共通readout `A` への**呼出側が与える同型** `e_i:F(i)≃A` を用いた輸送 `T_{ij}=e_j^{-1}∘e_i` を構成。恒等、逆元、三重・四重の輸送整合、contextwise gauge変更の共変性、型付き局所compatibilityと実際の被覆における大域関数の存在同値、値の復元、具体的な輸送不整合による昇格阻止をLeanで証明。

[exact-source CI #42340476422](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42340476422)：**Strict Lean 10,310/10,310 SUCCESS**、新規13定理の公理監査は標準公理のみ／sorryAxなし、source/test-merge Git tree `4f4f5782b3499fcaba493e4bc142d8ddafdc8d6d`一致。定理 [PR #3247](https://github.com/itakura-hidetoshi/KuuOS/pull/3247) MERGED、squash `18daa92b3e3eeb0200e533413cd1a392b5b41966`。

**限界:** これで成立したのは明示的なframeを与えた平坦・trivializableモデルの降下であり、任意の非自明束・高次stack/gerbe・元F55/P77/GK5CGのsource同一視・真正holonomy消滅を主張しない。

### LEC-06 — 証明付き仮有と未来方向の履歴保存（MERGED #3248）

新規 [ConditionedBhava.lean](../formal/Kuu/LivingEngi/ConditionedBhava.lean) に、`FramedSnapshot` = **元の依存型局所値＋大域readout＋両者の一致証明＋PromotionEvidence＋認証証明** を定義。`ConventionalBhava` は現在のスナップショット、全過去スナップショットのリスト、現在のreadoutと履歴全体を入力とする候補生成カーネルを持つ。

適格な認証がある場合だけ現行モデルを初期化・改訂でき、改訂には新しい局所値の証明を要求する。旧スナップショットの**完全な値と根拠**を`history ++ [oldSnapshot]`として保存すること、新しい局所値との一致、真に不整合な元局所情報からはこの有を作れないことをLean4で証明した。

[exact-source CI #42340907095](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42340907095)：**Strict Lean 10,311/10,311 SUCCESS**、新規15定理の公理監査は標準公理のみ／sorryAxなし、source/test-merge Git tree `7ac9e26dab3f3de25cb784df5ed19577055ca6fc`一致。定理 [PR #3248](https://github.com/itakura-hidetoshi/KuuOS/pull/3248) MERGED、squash `99861ff740c08a933922337fa0ed75116eadf410`。

**限界:** これは仮有の数学的な型付きcarrierであって、実在のAIが非マルコフ学習をした・内部重みを変更した・悟った・臨床的効果を獲得した、という主張ではない。「生」の候補もActOSの外部実行権限とは別である。

### 残る正本課題

LEC-05の一般高次transport、LEC-07「有→生候補→外部認可された行為」の形式的分離、LEC-08の非マルコフ帰還・安定性、LEC-09の真正元F55/P77/GK5CG Type値証拠との比較は、**未証明**として保持する。LEC-05/06の証明が成り立つという理由だけで、これらの条件を省略しない。保護#1558はDraft/Open/未マージ、公開root107、既存の公理・ソース履歴・固定toolchainは不変。


## 16. 2026-11-07 — LEC-07「有→生候補→外部許可」の形式証明追補

独立Kuu新規 [`BirthAuthorization.lean`](../formal/Kuu/LivingEngi/BirthAuthorization.lean) は、既存LEC-06の証拠付き `ConventionalBhava` に対し、生成された候補 `BirthPacket` が元のBhavaと入力の**真正な等式証明**を持つこと、`LicensedRequest` には別途Governance証明と、**Bhava全履歴・入力・scope・候補に依存する外部receipt**を要求することをLean4で証明した。

特に、**生候補は存在しても外部receiptが空なら認可要求は存在しない**、さらに**認可要求だけでは別の効果receiptが生じない**ことを構成的な反例で分離した。`freshOnlyBoundary` では、履歴が空のときだけ許される具体的なreceiptがあり、`reviseBhava` で旧source snapshotを追記した後はその**特定の古い許可**を再利用できないことを証明した。これは再許可一般の不可能性ではない。

**[定理PR #3250](https://github.com/itakura-hidetoshi/KuuOS/pull/3250) MERGED**、[exact-source CI #42348497450](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42348497450) **Strict Lean 10,312 / 10,312 SUCCESS**、Governance／独立Kuu API SUCCESS、12定理・12件`#print axioms`は標準公理のみ、`sorryAx`なし。source／test-merge tree `8ecac9fb37da15911cf6d7c330980f652997fa75`一致。統合squash `359bb1c59ff0c137e71979fa57e1a55b5143983d`。最初の失敗はフィールド名`matches`とLean構文の衝突であり、`sourceEq`への名称修正のみで命題・仮定を保持した。

[正式証明記録](formal/LEC-07-birth-authorization-verified-20261107.md) · [検証JSON](manifests/living_engi_lec07_verified_20261107.json)。`LEC-08` の非マルコフ帰還・可観測性、`LEC-09` の真正元Type値証拠比較は未解決であり、数学的な証拠の存在を実世界の実行権限と同一視しない。


## 17. 2026-11-07 — LEC-08「非マルコフ履歴と履歴保持修復」Lean4証明済み追補

**[定理PR #3252](https://github.com/itakura-hidetoshi/KuuOS/pull/3252) MERGED。** 独立 Kuu の [HistoryFeedbackRepair.lean](../formal/Kuu/LivingEngi/HistoryFeedbackRepair.lean) に18定理を追加。履歴依存カーネルの現在値だけへの因数分解条件と、**同じ現在WORLD読出し・同じ最新の型付きsnapshotでも、1件と2件の履歴で候補が異なる**有限の真正反例をLean4で構成した。さらに、一つの認証済みBhavaを実際に2回改訂した例で、元の局所Type値sectionと現在のreadoutが同一なのに、生成される生候補が異なることを示した。

**将来の修復:** `repairToHistoryIndependent` は、既存の真正な支持証明から新しい数学的認証を構成し、**元source、被覆下の同じWORLD読出し、全旧snapshot・履歴の追記保存**を維持したまま、将来の候補生成を指定されたhistory-independent policyへ切り替える。履歴そのものは消去しない。新しい生成規則が履歴を使用しないことと、過去の証拠が消去されたことは異なる。あらゆる非マルコフ系の安定化・苦の消滅・実AI重み変更は証明していない。

[exact-source CI #42355697499](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42355697499)：**Strict Lean 10,313 / 10,313 SUCCESS、Governance／独立Kuu API SUCCESS、公理監査18件は標準公理のみ・sorryAxなし**。source/test-merge tree `8ce7d90ca3c0ff02403237624dc202ddb065060f` 一致、定理squash `0aff0f1d62e66b82d4f4d680597dbdfa4cecd428`。初回失敗は`decide`が自由変数を含む式を直接処理しようとしたことであり、`change (false : Bool) ≠ true` の正規化だけを加え、命題を弱めず修正した。

[正式証明記録](formal/LEC-08-nonmarkov-history-repair-verified-20261107.md) · [検証manifest](manifests/living_engi_lec08_verified_20261107.json)。**次の別課題はLEC-09：真正元F55/P77/GK5CGのType値証拠履歴と商・高次比較の厳密な境界。** 非マルコフRuntime v0.72／v0.23への橋渡しは未実施であり、推論候補から外部実行許可は発生しない。


## 18. 2026-11-07 — LEC-09 真正native F55 Type値履歴と選択商の非復元性（証明済み）

[LEC-09 定理PR #3254](https://github.com/itakura-hidetoshi/KuuOS/pull/3254) は **MERGED**。既存の**独立native F55-shaped** 北C60真正五角形sourceで、元のType値三セル`northNativeF55PentagonCell`と、そこに右単位を合成した`northNativeF55PentagonWithUnit`が**異なるraw証拠**でありながら、選択E7P4 full-shadow商では同じ観測値を持つ既証明結果を継承した。

独立[新規Leanモジュール](../formal/Kuu/LivingEngi/NativeF55ProofHistoryBoundary.lean)では、**この商だけから全raw Type値証拠を復元する左逆関数は存在しないこと、raw単射な観測者はこの商を通じて因数分解できないこと、商の一致から誤った元source等式をLEC-04の認証済み証拠へ昇格できないこと**を証明した。さらに`NativeF55Trace`で元raw履歴・商観測・正確な対応証明を別々の型付き値として保持し、観測値だけでは履歴を識別できないことを形式化した。

[Exact-source CI #42357158330](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42357158330)：**Strict Lean 10,314 / 10,314 SUCCESS、Governance／独立Kuu API SUCCESS、13件の公理監査は標準公理のみ／`sorryAx`なし**。source/test-merge Git tree `53242fedbadfce7b34034158c83a4eed572d992e` 一致。定理squash `77f79e0d2676f327ced5adc5dff6220f757a43f5`。旧数学ソースと公開root107不変。

[正式証明記録](formal/LEC-09-native-F55-proof-history-boundary-verified-20261107.md) · [機械可読検証](manifests/living_engi_lec09_verified_20261107.json)。**厳密な限界:** これは独立して再構成した真正C60 native F55-shaped sourceの定理であり、凍結された歴史的な元F55/P77/GK5CG Type値証拠との型付き同値・忠実な比較は**未証明**。その追加の出典接続と高次coherenceが次の研究課題である。
## 19. 2026-11-07 — LEC-10：真正native F55源と選択shadowの局所貼り合わせ境界（Lean4証明済み）

**[定理PR #3256](https://github.com/itakura-hidetoshi/KuuOS/pull/3256) MERGED。**
[独立Kuu Lean4ソース](../formal/Kuu/LivingEngi/NativeF55CechSourceGluingObstruction.lean)では、LEC-09の真正北C60 native F55-shaped Type値証拠 `r₁=northNativeF55PentagonCell` と `r₂=northNativeF55PentagonWithUnit`（元rawでは `r₁≠r₂`、指定E7P4 shadowでは `q(r₁)=q(r₂)`）をそのまま使用した。局所チャートは **`Bool` 添字の `Unit` 上の抽象的な二重全被覆**であり、**C60幾何学の開被覆だとは主張しない**。C60真正性があるのは局所raw証拠そのものに限る。

**厳密な二層の結論**（既存LEC-01の全関数層 `Compatible`／`HasGlobal` を使用）：

```text
HasGlobal U (q ∘ s)    -- YES: chosen full-shadow quotient is compatible
HasGlobal U s          -- NO: distinct original raw proof trees disagree
```

**数学的な意味:** 指定shadowの局所評価は互換的で大域readoutを持つが、与えられた元source局所値の**完全な保存**を要求すると貼り合わせられない。既存§4.1に従い、これは `δ⁰` に相当する**局所overlap不一致の具体例**であって、`H¹` の非零類や一般の高次gerbe/stack持ち上げ障害の証明ではない。元Type値には群演算／ノルムを仮定せず、数値的残差の普遍性も主張しない。

- **LEC-04の適用:** 真正shadow大域命題への認証は可能。しかし具体的に反証された**元raw atlasの大域貼り合わせ命題**を証明書へ昇格することはできない。UNCHECKEDとREFUTEDは引き続き別。
- **LEC-09の証拠保存:** `NativeF55Trace` は元raw、指定shadow、両者の正確な関係を保持するが、元rawの不整合そのものは消さない。
- **有・修復の境界:** 同じshadowを持つ**別の定数元source atlas**は大域化できるが、元の局所Type値を一つ置換している。従ってそれは新しいatlasであり、過去の元証拠を消さない「真正source保存修復」の証明とは呼ばない。
- **独立性の限界:** 歴史的に凍結された元F55/P77/GK5CGのType値履歴と、今回の独立native F55-shaped sourceとの忠実な同値・輸送は未証明のまま。

**[Exact-source CI #42358724142](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42358724142)：Strict Lean 10,315 / 10,315 SUCCESS**。新規21定理すべて `#print axioms` を監査し、標準公理 `propext`・`Classical.choice`・`Quot.sound` のみ、`sorryAx` なし。Governance／独立Kuu API／Workflow整合性 SUCCESS、source/test-merge Git tree `a131d2354c62aa4f4305a8901b3254fb35b97a1d` 一致、定理squash `f58c4b8babb7f42578d2a6e6caaad5f4a56f9c49`。公開root107、固定Lean/mathlib、元歴史的source、保護PR #1558 Draft/Open/未マージを保持する。

[正式証明記録](formal/LEC-10-native-F55-source-cech-shadow-gluing-verified-20261107.md) · [検証manifest](manifests/living_engi_lec10_verified_20261107.json)。

**次の独立課題:** 一般の元証拠保存型transportに必要な正確な条件、および歴史的元F55/P77/GK5CGと独立native F55 Type間の明示的・忠実な比較を構成する。有限一致模型から任意の高次降下・臨床効果・外部実行権限を導かない。
## 20. 2026-11-07 — LEC-11：shadow大域化から元Type値source大域化への必要十分条件（証明済み）

**[定理PR #3258](https://github.com/itakura-hidetoshi/KuuOS/pull/3258) MERGED。** LEC-10では、真正北C60 native F55-shaped証拠を局所値とする抽象二重被覆において、選択shadowでは貼合可能でも元raw Type値を保存すると貼合不可能であることを証明した。LEC-11は原文§4.1の「指定された比較・貼り合わせ義務」を一般の関数層に対する**正確な必要十分条件**へ進めた。

被覆 `U : I → Set X`、元局所section `s : LocalSections U Raw`、選択観測 `q : Raw → Obs` に対し、`OverlapFiberFaithful(U,q,s)`を「**実際の重複領域で**、二つの元局所値の選択観測が一致すれば、元値も一致する」と定義する。全関数の層において真に被覆があるとき、Leanで次を形式証明：

```text
HasGlobal U s
  ↔ HasGlobal U (shadowSections U q s)
    ∧ OverlapFiberFaithful U q s
```

- 選択商 `q` の**全域単射性は不要**。証拠を要求するのは、指定した元局所atlasの実際の重複上に限る。
- LEC-04 `PromotionEvidence` により、認証済みshadow大域命題だけから元Type値の大域命題を昇格できない。一方で**別途このsource側の証明を取得**すれば、通常の関数層に限り元sourceを大域化できる。真正な反例でsource側条件が偽なら認証は阻止される。
- `sourceAwareReadout(q,r)=(q(r),r)`という**新しい豊かな観測**は元Type値をデータとして保持し、元値を単射的に識別する。ただしこれは旧shadow商の逆写像ではなく、元局所atlasの不整合を消す手段でもない。
- LEC-09/10の真正北C60 native F55-shaped raw二証拠に適用すると、元atlasでは重複条件が破れ、別の定数source atlasでは成立する。**同じshadowでも元sourceを別物に置換した場合は歴史保存修復ではない**。
- この必要十分条件は**全関数層の通常の貼り合わせ**についてであり、一般の高次transport、stack/gerbe、非零 `H¹`、幾何学的C60開被覆、歴史的固定元F55/P77/GK5CGとの型付き同値を証明したものではない。

独立[新規Lean全文](../formal/Kuu/LivingEngi/SourceAwareOverlapDescentCriterion.lean) **353行・23定理**を新規に追加、旧Lean、source歴史、workflowには変更なし。[exact-source CI #42359918998](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42359918998) **Strict Lean 10,316/10,316 SUCCESS、23件の`#print axioms` は標準公理のみ／sorryAxなし**、Governance・独立Kuu API・Workflow integrity SUCCESS、source/test-merge Git tree `dd47bb12ca9b7c31803925205ca3b8aded9d067e`一致、定理squash `2d80a2816d529913fc69f1988fde64b93cf9b889`。初回CIエラーは一つの括弧 `)` の欠落であり、元定理文面・仮定を変えず修正した。root107・固定Lean/mathlib・保護#1558 Draft/Open/未マージを保持する。

[正式証明記録](formal/LEC-11-source-aware-overlap-faithfulness-verified-20261107.md) · [検証manifest](manifests/living_engi_lec11_verified_20261107.json)。

**次の別証明課題:** 歴史的元F55/P77/GK5CGと独立native F55-shaped証拠の忠実なType値比較、および一般の高次transport/coherenceへの段階的な拡張。数値商の一意性から元証拠の一意性や実行権限を無条件に導かない。
## 21. 2026-11-07 — LEC-12：歴史的元F55と独立native F55の真正Type値証拠・共通shadow比較（証明済み）

**[定理PR #3260](https://github.com/itakura-hidetoshi/KuuOS/pull/3260) MERGED。** 前段LEC-09/10/11は真正北C60を使用しながらも、独立再構成したnative F55-shaped sourceの内部定理であり、歴史的original F55のType値そのものとの接続を未証明として保持した。LEC-12は初めて、**保持されている歴史的`OriginalF45BracketTree.DepthRotationRoute.PresentedCell`と独立`KuuNativeF45Tree.DepthRotationRoute.PresentedCell`の二つの元Typeを同じLeanモジュールに取り込み、**両者を同一視せずに真正な比較証明書を構成した。

実装は[混合公開集約側の新規Lean](../formal/KuuOSFormal/HistoricalNativeF55CommonShadowLEC12.lean)に限定する。歴史的元F55の`Blocks`、二Nat深度、F54 source/target route、九構成子と、独立nativeの真正北C60元証拠をそのまま保持する。**独立`KuuOSStrict`へKUOS/Grayをimportしていない**。共通の観測型は`(Int × Int) × ZMod 2`である。

- **共通数値条件：** 元歴史的raw F55の`c60F55SourceNative`から得る二符号付き整数chargeと位相、独立nativeの`nativeShadow`の双方で、`phase = (second charge : ZMod 2)`を既証明の全構成子定理から継承する。
- **真正五角形生成子の比較：** 歴史的元`PresentedCell.pentagon t₁ t₂ t₃ t₄`と独立北C60の`northNativeF55PentagonCell`はいずれも`((1,0),0)`に写る。歴史的`t_i`は元の依存型構成物であり、独立北C60のstageと**幾何学的に同一であるとは証明していない**。
- **履歴の非復元性：** 両体系で「五角形生成子」と「同じ生成子＋元右単位」のraw証拠はそれぞれ異なるが、共通観測では一致する。旧rawについても新rawについても、**この指定共通数値観測は単射でない**。
- **型付き二体系証明書：** `HistoricalNativeF55Aligned`は歴史的raw証拠・独立native raw証拠・両者の**指定shadow等値証明**を別々のフィールドとして保持する。primitive版とright-unit版の二つの具体的証明書を構成し、**証明書そのものは異なる**ことを証明した。
- **越権しない境界：** これは**実在する両元Typeの共通観測に関する最初の限定的な接続**である。全歴史的F54/F55↔native F54/F55の忠実な型付きFunctor/同値や、元P77/GK5CG高次seam・coherence・obstructionの輸送を得たわけではない。

[exact-source CI #42361244071](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42361244071) **Strict Lean 10,317/10,317 SUCCESS**、新規14定理＋型付き比較証拠構成2件、**`#print axioms`16件**は標準`propext`・`Classical.choice`・`Quot.sound`のみ（元raw不等式は公理なし）、`sorryAx`なし。Governance、独立Kuu public API、公開root復元、関連integrity checksもSUCCESS。source/test-mergeのGit tree `d999152254a878df75fade0fe70082765bb0a1e2`一致、定理squash `f700f0d680865301d6872c5e25b7d2541ad591b6`。公開root107、固定Lean/mathlib、元F55/P77/GK5CG source、保護PR #1558 Draft/Open/未マージは保持。

[正式証明記録](formal/LEC-12-historical-original-and-native-F55-common-shadow-verified-20261107.md) · [検証manifest](manifests/living_engi_lec12_verified_20261107.json)。

**次段階LEC-13：** 歴史的元F54と独立native F54の`Blocks`・両Nat深度・真のC60 source/targetを指定した**境界付き忠実な輸送写像**の存在条件と障害を明示し、F55九構成子およびP77/GK5CG高次証拠へ拡張できる範囲だけを証明する。共通shadowの一致だけで元の証拠履歴や外部実行権限を昇格しない。
## 22. 2026-11-07 — LEC-13：真正歴史的F54/F55証拠と実C60物理支持辺の90重非復元障害（証明済み）

**[定理PR #3262](https://github.com/itakura-hidetoshi/KuuOS/pull/3262) MERGED。** LEC-12で歴史的元F55と独立native F55の共通shadow `(Int×Int)×ZMod2`を正確に比較できたが、元証拠の数値校正だけでは**幾何学的支持を特定できるとは限らない**。既存の真正歴史的F47 `C60F47SquareFrame`（元F42 face 3-arrow・元F54二Nat/Blocksに結びつく元F55 rotation 3-arrow・別フィールドのC60物理Edge・証明付きcalibration）と、F112-P39/P40の実在90辺・隣接二面の定理を接続し、新しい混合公開集約Lean [`HistoricalNativeF54F47SupportLEC13.lean`](../formal/KuuOSFormal/HistoricalNativeF54F47SupportLEC13.lean) で形式化した。

**新定理の厳密な内容：**

- 任意の既存校正済み歴史的F47 frame `B` に対し、実在C60の90本の `Edge` から、**同じ元F42/F55二つの証拠矢と同じ完全signed/phase shadow**を持ちながら、**物理的支持辺が異なる90個のF47 frame**へ単射を構成できる。これは有限proxyではなく既存の本来のC60構成に対する定理である。
- `HistoricalF47SourceShadow(B) = (originalF42F55ArrowPair(B), fullF55SignedPhase(B))` のみから各辺を復元する**全域decoderは存在しない**。物理辺を明示的な追加フィールドとして保持した新しい観測は、この指定90辺族を単射的に識別する。
- `LEC13OriginalNativeCalibration B` は、**元F54二Nat境界における歴史的F55 raw証拠**、その元F47 F55商矢との正確な等号、独立native F55 raw証拠、両者のLEC-12共通shadow等値をそれぞれ要求する。**任意のBについてこの入力が存在するとは証明していない**。この証明書を実際に与えた場合に限り、元raw・native raw・正確なF47商矢・物理Edgeを保持する90個の別々の型付き比較証拠を構成できる。
- 注意：既存F47の数学的frame型は`edge`と元のF42/F55証拠矢を別に持ち、calibrationは辺との幾何学的source対応まで要求していない。したがって90辺の結果は**元の型の支持辺選択が未決定である**ことの証拠であり、すべての元raw証拠が90辺すべてに幾何学的に適合するという定理ではない。
- 歴史的F47回転squareの `(0,1;1)` と独立native北五角形の `(1,0;0)` は同じ受信値ではない。次の真正な接続候補は**独立nativeの実北hexagon square**であり、異なる生成子を数値・名前だけで同一視しない。

[exact-source CI #42363485222](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42363485222) **Strict Lean 10,318/10,318 SUCCESS**。新規15定理・型付き構成1件・明示的`#print axioms`16件、`sorryAx`なし、新規`axiom`なし、Governance/独立public API等SUCCESS、source/test-merge Git tree `2ef09aab2b5e511d29131d210abcf4334664aea8`一致、squash `ec57d5595ba4c8b80331fbce3c17bb54fb002238`。公開root107、固定Lean/mathlib、保護#1558 Draft/Open/未マージを維持。

**公理依存の監査境界：** 前段LEC-12と異なり、今回の定理は既存F112の真正C60幾何／辺同型の証明に由来する`native_decide`の**既存6補助公理**を、標準公理 `propext`・`Classical.choice`・`Quot.sound` に加えて継承する。新公理は追加していないが、**標準公理だけの証明ではない**と明示する。完全kernel証明へ強化するには別途この有限幾何部分を`native_decide`非依存で再証明する必要がある。

[正式証明記録](formal/LEC-13-historical-native-F54-F55-90-edge-support-boundary-verified-20261107.md) · [検証manifest](manifests/living_engi_lec13_verified_20261107.json)。

**次のLEC-14：** 元F47の真正F55 squareと独立native C60 hexagon F55 squareの**実際にinhabitedな**正確な共通shadow／型付き証拠比較を構成し、元F54からnative F54へのsource/target輸送、幾何学的支持・P77/GK5CG高次証拠まで拡張可能かを別々に判定する。これはČech `H¹` の非零性、全高次descent、実AI更新、臨床効果、ActOS権限を証明しない。
