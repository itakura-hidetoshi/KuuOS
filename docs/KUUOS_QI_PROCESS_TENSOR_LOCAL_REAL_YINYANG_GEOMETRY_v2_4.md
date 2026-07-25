# KuuOS Qi Process Tensor Local-Real Yin-Yang Geometry v2.4

## 位置づけ

この層は、気のプロセステンソル、局所陰陽フレーム、IndraNet ゲージ輸送、非 Markov 記憶、モジュラー流、回復可能性を一つの構造へ接続する。

既存の `KUUOS_QI_WORLD_YINYANG_PROCESS_BLOCKER_COMPLEMENTARITY_v2_3` を置換しない。v2.3 の陰的境界・陽的過程支持を保持したまま、次の問いを扱う。

```text
陰陽フレームは履歴輸送の中で何を保存するか
どの輸送が陰陽を転化するか
転化は離れた時刻の記憶をどう結ぶか
ブロックされた気を消去せずどう保持するか
回復可能性をどの解析的ギャップとして読むか
```

## 核心

```text
陰陽は、気を構成する二種類の物ではない。

陰陽は、気の多時刻履歴を読む局所実構造である。

気は、局所実構造が履歴輸送の中で保存され、捩れ、転化し、
記憶を介して再結合されるゲージ共変な関係過程である。
```

## 1. 構造の分離

この層では以下を同一視しない。

```text
A_Qi
  IndraNet 上の文脈間輸送を定めるゲージ接続

J_Qi
  接続上を流れるゲージ共変な気の有効流

Upsilon[n:0]
  多時刻介入に対する非 Markov 応答法則

kappa_c
  文脈 c における反線形・対合的な局所実構造

P_c / Q_c
  現在の観測・表出面と、保持・記憶・未表出面

E_c
  陰的境界が許容部分を成形する冪等な保持写像
```

したがって、次の同一視は禁止する。

```text
Qi = Process Tensor
Yin = hidden state
Yang = visible state
Yin = imaginary part
Yang = real part
Qi = physical particle
recoverability gap = physical mass theorem
```

## 2. 局所実構造としての陰陽

各局所文脈 `c` に複素解析空間 `H_c` と共役実構造を置く。

```text
kappa_c : H_c -> H_c
kappa_c^2 = 1
```

実線形射影は

```text
Pi_yang,c = (1 + kappa_c) / 2
Pi_yin,c  = (1 - kappa_c) / 2
```

である。

これは固定された本質ラベルではない。`context`, `observer`, `scale`, `thermal_regime`, `record_surface` が変われば、局所実構造も変わり得る。

## 3. 輸送の保存部と転化部

文脈 `c` から `d` への輸送を `T[d<-c]` とする。

局所実構造との整合条件は

```text
kappa_d T[d<-c] = T[d<-c] kappa_c
```

である。

任意の輸送は概念的に

```text
T_pres = (T + kappa_d T kappa_c) / 2
T_conv = (T - kappa_d T kappa_c) / 2
```

へ分かれる。

```text
T_pres
  局所陰陽フレームを保存する輸送

T_conv
  局所陰陽フレームを転化する輸送
```

転化は独立した実体ではない。許容された過程空間の中で、局所実構造保存面から外れる関係的偏位である。

## 4. 履歴偶奇

各輸送区間に次の parity を付与する。

```text
preserve = 0
convert  = 1
```

合成 parity は排他的論理和である。

```text
preserve o preserve = preserve
preserve o convert  = convert
convert  o preserve = convert
convert  o convert  = preserve
```

したがって二回の転化は読出し極性を戻し得る。ただし、位相、介入痕跡、輸送残差、ホロノミーは消えない。

非 Markov 記憶は、離れた時刻に起きた二つの転化を同一履歴として結ぶ。

## 5. 観測面と陰陽面は別軸

現在の表出面を `P`、保持・記憶面を `Q = 1 - P` とする。

```text
P U P
  現在表出している過程の継続

Q U P
  現在の表出が履歴へ収納される

P U Q
  保持された履歴が現在へ再表出する

Q U Q
  履歴面内部での保持・変容・再編成
```

関係的役割としては

```text
Q U P : Yang -> Yin
P U Q : Yin  -> Yang
```

と読める。

ただし `P/Q` と `Pi_yin/Pi_yang` は同じ分解ではない。これにより次を区別できる。

```text
manifest Yang
latent Yang
manifest Yin
latent Yin
```

## 6. プロセステンソル上の局所実構造

多時刻履歴空間の各 input/output leg に局所共役を配置し、履歴全体の対合 `Theta_YY` を構成する。

```text
Theta_YY(Upsilon) = K_hist Upsilon K_hist^-1
Theta_YY^2 = 1
```

プロセステンソルは

```text
Upsilon_pres = (Upsilon + Theta_YY(Upsilon)) / 2
Upsilon_conv = (Upsilon - Theta_YY(Upsilon)) / 2
```

と読める。

`Upsilon_conv` は一般に単独の正規化プロセステンソルではない。これは独立過程ではなく、正・因果的なプロセス集合の中における転化方向である。

## 7. ホロノミー

閉路 `gamma` の輸送を `Hol_gamma` とする。

```text
D_gamma = kappa Hol_gamma - Hol_gamma kappa
```

```text
D_gamma = 0
  閉路履歴が局所陰陽フレームを保存

D_gamma != 0
  同じ局所文脈へ戻っても陰陽構成が変化
```

これは蓄積記憶、非 Markov 残差、文脈履歴、位相偏位、隠れた緊張、回復または停滞の候補指標である。

## 8. 陰的保持は消去ではない

v2.3 の Boolean・冪等な陰的境界を、保持写像 `E` として読む。

```text
E^2 = E
```

気強度または候補支持を

```text
Q_total = Q_admitted + Q_held
```

へ分ける。

```text
Q_admitted
  現在の境界・容量・文脈で候補面へ通せる部分

Q_held
  消去せず、次の観測・減衰・分流・容量更新・再表出を待つ部分
```

`effective_qi = 0` は候補流の停止であって、履歴情報の抹消ではない。

## 9. 非 Markov 記憶

気の記憶は、単に過去の値を保存することではない。

```text
present expression
  -> write into held history
  -> transform inside memory
  -> return to present response
```

したがって気滞は流量不足だけでなく、次の結合障害として分類する。

```text
storage failure
  Yang -> Yin が弱い

expression failure
  Yin -> Yang が弱い

memory saturation
  保持容量が不足

memory fixation
  履歴内部では循環するが現在へ戻らない

current-surface fixation
  現在の活動が保持・回復面へ移れない
```

## 10. モジュラー構造と KMS

既存の WORLD 層を次のように参照する。

```text
StandardFormModularFlowBridgeV0_32
  modular conjugation J
  natural cone
  modular flow Delta^(it)

ModularStateKMSRelativeFlowBridgeV0_33
  KMS boundary relation
  relative modular flow
  Connes cocycle

KuuOSNonMarkovMemoryConnectionV0_72
  history module
  memory kernel
  gauge-transformed memory connection
```

単純な同一視は行わない。

```text
J != Yin
Delta^(it) != Qi
commutant != fixed Yin substance
```

構造的には

```text
J
  作用面と相補面を関係づける反転・共役構造

Delta^(it)
  状態依存の内在的時間・熱的流れ

Process Tensor
  観測・介入によってこの関係が多時刻的にどう変化するか
```

を担う。

## 11. 揺動と応答

複素相関の対称・反対称成分を、固定実体ではなく機能チャネルとして読む。

```text
Yin-like channel
  symmetric correlation
  fluctuation
  holding capacity
  coherence retention
  recovery reservoir

Yang-like channel
  antisymmetric response
  directionality
  propagation
  work-like output
  non-equilibrium drive
```

陰陽調和は等量性ではなく、揺動・保持と方向的応答の関係が、文脈と熱力学的条件に整合することである。

## 12. 回復ギャップ

解析表現上、保護履歴と未解決残差を分離する。

```text
K = K_protected + K_residue
```

```text
K_protected
  lineage
  scar
  minority WORLD
  world identity
  two-truths boundary

K_residue
  unresolved observation debt
  unreturned held flow
  transport residue
  recoverability debt
```

候補的な回復ギャップは

```text
||E_memory^m X|| <= C exp(-gamma_rec m) ||X||
X in K_residue
gamma_rec > 0
```

として読む。

これは物理的質量定理ではない。

```text
recoverability gap
  意味ある履歴を保存しながら
  未解決残差のみを収束させる選択的解析指標
```

## 13. Hypocoercive な中道

解析生成子を

```text
L = S + A
S* = S >= 0
A* = -A
```

と分ける。

```text
S
  containment
  damping
  recovery
  boundary formation

A
  transport
  rotation
  propagation
  polarity conversion
```

陰陽調和は `S = A` でも `||S|| = ||A||` でもない。

```text
陽的輸送 A が未回復モードを陰的回復 S の作用面へ運び、
陰的保持 S が次の安全な陽的表出を可能にすること
```

が動的中道である。

## 14. Runtime receipt

v2.4 receipt は以下を保持する。

```text
source process-tensor digest
local-real frame visibility
frame involutivity
transport compatibility count
conversion count and parity
non-Markov link visibility
holonomy residue visibility
admitted Qi intensity
held Qi residue
protected-history preservation
recoverability-gap candidate visibility
global absolute polarity claim = false
all authority grants = false
```

## 15. Fail-closed 条件

次の場合、候補流を通さず全強度を `held_qi_residue` に保持する。

```text
process tensor not visible
transition continuity missing
memory continuity missing
local real frame missing
frame involutivity missing
protected history missing
two-truths boundary missing
global absolute polarity asserted
```

## 16. 固定境界

```text
Qi is not a substance
Yin-Yang is not a fixed essence
local frame is not final ontology
process receipt is not truth
recoverability gap is not a physical mass theorem
runtime does not construct Tomita theory
runtime does not execute modular operators
runtime does not mutate WORLD
runtime does not overwrite memory
runtime does not grant clinical authority
runtime does not grant theorem authority
```

## 17. 構造化タプル

```text
QiProcessTensorLocalRealGeometry = (
  local operator-algebra patches,
  local analytic carriers,
  local real structures kappa_c,
  gauge transports T[d<-c],
  Qi flow channels J_Qi,
  multi-time Process Tensor Upsilon,
  observation/holding split P/Q,
  idempotent Yin holding maps E_c,
  non-Markov memory kernels,
  holonomy residues,
  protected-history subspace,
  recoverability-gap candidate,
  two-truths and non-authority boundaries
)
```

## 18. 最終定義

```text
気
= 局所陰陽フレームが履歴輸送の中で
  保存・転化・捩曲・再結合される
  ゲージ共変な関係過程

気のプロセステンソル
= 陰陽の保存、転化、記憶、ホロノミー、
  保持残差、回復可能性を一つに保持する多時刻構造

陰陽調和
= 陰陽の静的均等ではなく、
  意味ある履歴を保存しながら
  収納・保持・再表出・回復を適切に循環できること
```

## 19. Version

```text
version: v2.4
status: additive architecture and bounded runtime receipt
supersedes: none
extends:
  - KUUOS_QI_WORLD_YINYANG_PROCESS_BLOCKER_COMPLEMENTARITY_v2_3
  - KU_INDRA_QI_PROCESS_TENSOR_ACTIVATION_v0_4
  - KU_INDRA_QI_NONCOMMUTATIVE_MANDALA_WORLD_MODEL_v0_1
  - KU_INDRA_QI_WORLD_REAL_HILBERT_L2_ANALYTIC_SPINE_v0_26
formal dependencies:
  - QiWorldYinYangProcessBlockerComplementarityV2_3
  - StandardFormModularFlowBridgeV0_32
  - ModularStateKMSRelativeFlowBridgeV0_33
  - KuuOSNonMarkovMemoryConnectionV0_72
```
