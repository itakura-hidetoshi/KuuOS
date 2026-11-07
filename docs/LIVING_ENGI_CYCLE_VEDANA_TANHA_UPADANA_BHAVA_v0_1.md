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
| [v2.69](../formal/KUOS/DependentOriginationGeneratedHolonomyCountermodelCarrierV2_69.lean) | 真正な非自明generated holonomyの有限反例 | 非自明holonomyそのものを病理としない |
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

[`manifests/living_engi_cycle_vedana_tanha_upadana_bhava_v0_1.json`](../manifests/living_engi_cycle_vedana_tanha_upadana_bhava_v0_1.json) に、各ステージ・遷移ゲート・テストケース・proof obligation・非主張事項を別途構造化した。JSONは設計契約のメタデータであり、Lean実装・実行Runtime・数学的証明書ではない。

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
