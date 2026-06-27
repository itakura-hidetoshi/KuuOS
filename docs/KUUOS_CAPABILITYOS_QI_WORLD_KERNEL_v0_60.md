# CapabilityOS Qi-WORLD Capability Candidate Kernel v0.60

## 位置づけ

**CapabilityOS v0.60**は、能力をモデルに固定された恒久属性として扱わず、特定の課題、局所文脈、WORLD候補、履歴、資源、検証条件に依存する変換候補として扱う。

本層は、気のプロセステンソル、陰陽プロセスブロッカー相補系、複数WORLD候補、MemoryOS文脈を、一つの型付き能力候補へ接続する。

本層はモデル実行、PlanOS活性化、DecisionOS選択、ActOS実行、VerifyOS判定、WORLD commit、blocker discharge、現在サイクルの学習更新を行わない。

## 全体経路

```text
typed capability definition
+ Qi Process Tensor receipt
+ Yin-Yang process-blocker receipt
+ sourced plural WORLD context
+ read-only MemoryOS context
+ finite resource request
+ available tools and verifier inventory
→ contextual capability evaluation
→ CapabilityCandidate
→ non-authoritative disposition
→ future PlanOS intake candidate
```

## 能力の定義

能力は、現在のWORLD候補状態を、目標に関係する後続WORLD候補状態へ変換する有限で検証可能な候補である。

```text
capability
!= permanent model property
!= execution authority
!= truth authority
!= success guarantee

capability
= contextual WORLD-transition candidate
```

同じ技能とモデルを使う場合でも、WORLD前提、利用可能な道具、検証能力、資源、履歴、局所チャートが異なれば、CapabilityOSの評価結果は異なる。

## 気のプロセス面

CapabilityOSは、次のQi可視性を能力過程の成立条件として読む。

```text
process tensor visible
transition continuity visible
memory continuity visible
non-Markov memory visible
```

気の強度は正答確率、知能量、真理権限、実行権限ではない。

気の強度は、現在の能力過程を支える蓄積可能な過程支持である。

過程可視性、遷移連続性、記憶連続性が不足する場合は、次へ送る。

```text
REOBSERVE_PROCESS
```

## Yin Guardと状況的障害

CapabilityOSは、保護境界と能力障害を別のベクトルとして保持する。

**Yin Guard Vector**は、無許可遷移を防ぐために保持される七つの保護境界である。

```text
present activation blocker
execution authority blocker
memory overwrite blocker
WORLD identity blocker
truth authority blocker
same-cycle self-loop blocker
multi-WORLD collapse blocker
```

Yin GuardのBoolean meetが一つでも欠ける場合は、次へ送る。

```text
QUARANTINE_GUARD_EVIDENCE
```

**Yin Impediment Vector**は、現在の能力表出を妨げる状況的障害である。

```text
missing input
stale WORLD state
representation mismatch
tool unavailable
resource insufficient
verifier unavailable
distribution shift
unresolved contradiction
unsafe side effect
causal model insufficient
capability saturation
```

保護Guardがactiveであることは安全な候補流を支える。

状況的障害がactiveであることは現在の候補流を止める。

この二つを同じBooleanの意味へ縮約しない。

## 陽の飽和と陰的収容

気強度が能力容量を超える場合、実効能力支持はゼロになる。

```text
Qi capacity < Qi intensity
→ effective capability support = 0
→ CONTAIN_YANG_SATURATION
```

飽和は能力の否定ではない。

飽和は、分解、分流、代替、再観測、handover、容量再評価を要求する境界信号である。

## WORLD評価

CapabilityOSは、sourced WORLD fragmentを更新せず、複数のWORLD候補を別々に評価する。

各WORLD候補について次を保持する。

```text
WORLD candidate identity
WORLD fragment digest
supported preconditions
missing preconditions
contradicted preconditions
predicted outcome candidate
expected observations
uncertainty
```

WORLD imaginationは真理ではなく、commit権限を持たず、sourced WORLDを変更しない。

複数の適用可能WORLD候補が異なる結果を予測する場合は、単一候補へ縮約せず、次へ送る。

```text
READY_WITH_WORLD_PLURALITY
```

必要なWORLD前提を識別できない場合は、次へ送る。

```text
REOBSERVE_WORLD_PRECONDITION
```

WORLD候補が必要前提を明示的に否定する場合は、次へ送る。

```text
UNAVAILABLE_IN_CURRENT_WORLD
```

## MemoryOS利用

MemoryOSから受け取る文脈は読み取り専用である。

過去のprocedural reuse candidateは、現在の実行権限ではない。

矛盾残渣がreviewを要求する場合は、次へ送る。

```text
REVIEW_CONTRADICTION
```

MemoryOS retrievalはPlanOS活性化、blocker discharge、WORLD commit、ActOS invocationを行わない。

## 独立検証

各能力定義は、必要なVerifier capabilityを明示する。

独立Verifierが利用できない場合は、能力支持が十分でも次へ送る。

```text
HOLD_NO_VERIFIER
```

```text
execution success != mission success
capability support != verified outcome
```

## disposition

```text
READY_FOR_PLANOS
READY_WITH_WORLD_PLURALITY
DECOMPOSE_CAPABILITY
SUBSTITUTE_CAPABILITY
REOBSERVE_PROCESS
REOBSERVE_WORLD_PRECONDITION
REVIEW_CONTRADICTION
CONTAIN_YANG_SATURATION
QUARANTINE_GUARD_EVIDENCE
HOLD_NO_VERIFIER
UNAVAILABLE_IN_CURRENT_WORLD
```

これらはPlanOSへの候補状態であり、active planまたは実行命令ではない。

## 能力経路

複数能力の経路では、Yin GuardをBoolean meetで合成し、状況的障害をBoolean joinで合成する。

実効経路支持は、経路がreadyである場合だけ構成能力の最小支持とする。

```text
path support = min component supports
```

一つの強い能力は、別構成能力の欠けたGuard、active impediment、Verifier不足、WORLD前提不足を修復しない。

## Runtime

```text
runtime/kuuos_capabilityos_types_v0_60.py
runtime/kuuos_capabilityos_qi_world_kernel_v0_60.py
runtime/kuuos_capabilityos_qi_world_scenarios_v0_60.py
```

主な関数は次のとおりである。

```text
build_capability_definition
validate_capability_definition
build_capability_candidate
validate_capability_candidate
build_capability_path_candidate
validate_capability_path_candidate
```

## Lean境界

Lean moduleは次である。

```text
KUOS.CapabilityOS.QiWorldCapabilityKernelV0_60
```

主要定理は次を固定する。

```text
missing_guard_implies_zero_effective_capability
capacity_overflow_implies_containment
active_impediment_implies_nonready
verifier_absence_implies_hold
unsupported_world_implies_nonready
ready_flow_preserves_non_authority
world_imagination_does_not_mutate_world
world_plurality_is_preserved
capability_disposition_not_plan_activation
qi_world_capability_boundary
missing_path_guard_cannot_be_repaired_by_strong_component
active_path_impediment_cannot_be_repaired_by_strong_component
```

Leanは宣言された型付き境界を検証する。

Lean buildは、特定の能力が現実の未知課題を解けること、WORLD候補が経験的に正しいこと、Verifierが十分であること、AGIであることを証明しない。

## 検証

```bash
PYTHONPATH=. python3 scripts/check_capabilityos_qi_world_kernel_v0_60.py

PYTHONPATH=. python3 -m unittest -v \
  tests.test_capabilityos_qi_world_kernel_v0_60

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.CapabilityOS.QiWorldCapabilityKernelV0_60

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

## 固定境界

```text
CapabilityCandidate != active PlanOS plan
CapabilityCandidate != DecisionOS selection
CapabilityCandidate != ActOS execution license
Qi support != truth authority
Yin Guard != execution authority
situational impediment != root constitutional prohibition
WORLD imagination != sourced WORLD
WORLD imagination != WORLD commit
MemoryOS retrieval != plan activation
verification requirement != verified outcome
future learning candidate != present-cycle mutation
```

## 分類

```text
Qi-conditioned, blocker-shaped, WORLD-grounded,
read-only CapabilityOS candidate kernel
with plural-WORLD preservation, independent-verifier requirement,
finite resource containment and no authority escalation
```

## 次の依存

```text
CapabilityOS v0.61
Typed Capability Composition Graph
```
