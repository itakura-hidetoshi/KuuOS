# KuuOS / 空OS Roadmap

**基準日：2026年7月7日 JST**

**`main`の統合済み到達点：self-organization candidate receipt v0.91**

**`main`の最新基準commit：`1b5b008cd2c54e784cf6d28266a132f632eededa`**

**現在のDraft frontier：PR #1052、self-organization selection policy v0.92**

**Draft branch：`feature-selection-policy-v0-92`**

この文書は、統合済み基盤、完了系列、現在のDraft frontier、次期候補を分離します。

v1.24で閉じたrepository mutation roadmapは、後続権限を自動生成しません。

Apoptosis Lifecycle Governanceは、repository mutation roadmap v1.25以降ではありません。

v0.92はpolicy-only artifactです。

selection execution、runtime effect、repository state changeを許可しません。

## 状態分類

| 表記 | 意味 |
|---|---|
| 統合済み | `main`に存在し、正式なruntimeまたはLean surfaceから参照される |
| Draft frontier | 現在の`main`を基準とする未mergeの研究枝 |
| 継続検証 | 統合済みだが、依存更新時に専用rootとaggregate rootを再検証する |
| 完了系列 | 定義済みの終端へ到達し、後続権限を自動生成しない |
| 次期候補 | 独立した次段階として検討できる候補 |
| 外部receipt | runtimeまたはLean内部だけでは生成しない入力 |
| Frozen boundary | 破壊的変更を行わず、additiveまたはtighten-onlyで維持する境界 |

## 固定境界

```text
candidate != authority
validation != truth
CI pass != external theorem acceptance

observation != verification
verification != truth
learning != present-cycle mutation
memory != belief sovereignty
selection != execution
selection policy != selection execution
receipt != successor authority
receipt composition != receipt construction

WORLD sidecar != exact WORLD
WORLD candidate != empirical fact
WORLD commit != truth
WORLD intake != WORLD update
analytic vacuum != exact WORLD
Kū != zero vector
modular time != physical time

modeled repository transition != live Git mutation
object candidate != object materialization
reference authorization != reference update
checkpoint creation != checkpoint overwrite
checkpoint reflog record != checkpoint reference update
dedicated index != canonical index
sandbox reflection != repository-root working-tree write
local checkpoint != remote push authority
roadmap completion != successor mutation authority

active self-organization state != unbounded mutation authority
current root execution != production deployment
runtime success != external truth
README public status != authority grant
current surface CLI != authority grant
current surface index != authority grant
current surface artifact != authority grant
README surface exposure != authority grant
selection policy artifact != authority grant

Apoptosis Lifecycle Governance != repository mutation roadmap v1.25
lifecycle completion != successor route
terminal completion != future authority inheritance
```

## 現在の統合済み基準

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Horizon / Context Gauge | v0.12 / v0.13 | 統合済み |
| Finite-cycle agent | v0.20からv0.27 | 統合済み |
| Qi diagnostic lineage | v0.28 / v0.29 | 統合済み |
| MemoryOS foundational line | v0.35、v0.37、v0.38、v0.39 | 統合済み |
| Qi-WORLD | v2.3 | 統合済み |
| WORLD mathematical sidecar | v0.27からv0.59、v14.0 bridge | 統合済み、継続検証 |
| Current status surface | v0.70からv0.78 | 統合済み、継続検証 |
| Repository self-evolution | v0.79からv1.24 | 統合済み、継続検証 |
| Staged repository mutation | v1.19からv1.24 | 完了系列 |
| Apoptosis Lifecycle Governance | v0.1からv0.36 | 独立完了系列 |
| Self-organization cycle | v0.79からv0.91 | `main`へ統合済み |
| Self-organization selection policy | v0.92 | PR #1052 Draft frontier |
| Lean aggregate root | `formal/KuuOSFormal.lean` / target `KuuOSFormal` | strict build surface |
| Current runtime root | `runtime/kuuos_current_check.py` | この枝では`kuuos_current_root_sequence_v0_92`を実行 |
| Closed repository mutation runtime root | `runtime/kuuos_v124_check.py` | v1.24 cumulative surface |
| Legacy compatibility runtime root | `scripts/run_kuuos_runtime_full_check_v0_55.py` | compatibility surface |

## Current self-organization line

```text
README Surface Exposure v0.78
→ candidate queue v0.79
→ candidate receipt v0.80
→ selection policy v0.81
→ selected next action v0.82
→ execution plan v0.83
→ next request v0.84
→ review packet v0.85
→ bounded-action transition v0.86
→ bounded repository change v0.87
→ completion receipt v0.88
→ next cycle seed v0.89
→ candidate queue v0.90
→ candidate receipt v0.91 on main
→ selection policy v0.92 Draft frontier
```

v0.92のpolicy artifactは、v0.91 receiptに存在する候補、PR path preservation、Governance Gate requirement、single next-stage scopeをranking ruleとして保持します。

v0.92の`effect_authorized`と`selection_authorized`はfalseです。

## Current runtime root

標準runtime rootは次です。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

v0.92 Draft branchでは、このrootは次のsequenceへ接続されます。

```text
runtime/kuuos_current_check.py
→ runtime.kuuos_current_root_sequence_v0_92
→ tests.test_kuuos_self_organization_selection_policy_v0_92
→ tests.test_kuuos_current_root_sequence_v0_92
```

current surfaceは次の入口から読めます。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_surface.py
```

## 次期候補

| 候補 | 条件 | 境界 |
|---|---|---|
| v0.93 selected next action artifact | v0.92 policy-only artifactがcurrent rootで検証される | selection record only |
| current surface refresh | v0.92をsurfaceへ露出する必要がある場合 | surface != authority |
| ROADMAP/CITATION sync receipt | 文書同期をreceipt化する場合 | document sync != successor authority |

## Governance Gate

PR merge前に少なくとも次を確認します。

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
PYTHONPATH=. python3 runtime/kuuos_self_organization_selection_policy_v0_92.py
PYTHONPATH=. python3 -m unittest tests.test_kuuos_self_organization_selection_policy_v0_92
PYTHONPATH=. python3 -m unittest tests.test_kuuos_current_root_sequence_v0_92
```

Gateの成功は、対象surfaceの整合性receiptです。

外部定理受理、臨床承認、組織承認、無制限repository mutation権限ではありません。
