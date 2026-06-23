# PlanOS Compiler Materialization v0.22

## 位置づけ

PlanOS v0.22は、PlanOS v0.21でcommitされた次周期plan basisを既存のPlanOS v0.3 compiler adapterへ接続する。

この層は候補routeをcompiler routeへ射影し、v0.1 structured compilerを再利用してtemplate materialization receiptを生成する。

materializationはplan activationでもActOS executionでもない。

## 接続経路

```text
PlanOS v0.21 committed next-plan basis
→ exact selected-candidate binding
→ ReplanAdapterRoute
→ AdapterRoute projection
→ ExactNextCycleGate
→ v0.1 structured compiler reuse
→ template materialization
→ single-use receipt
→ replay-safe adapter history
```

## 候補route

```text
continuePlan, strengthen
→ nextPlanCandidate

repair, slowDown
→ repairPlanCandidate

reobserve
→ reobservationPlanCandidate

reroute
→ reroutePlanCandidate

hold
→ hold

terminateCandidate
→ terminationPlanCandidate
→ handoverPlan
```

複数候補が同じcompiler routeへ射影される場合でも、元のDecisionOS selected candidate identityは別のdigest bindingで保持する。

route projectionは候補identityの置換ではない。

## 正確な次周期境界

```text
previousCycle = source currentCycle
activeFromCycle = source activeFromCycle
missionCycle = previousCycle + 1
mission phase is PlanOS = true
```

旧周期はactive cycleと一致しない。

## compiler再利用

新しいstructured compilerは導入しない。

```text
structured compiler is v0.1 = true
dependency validation reused = true
resource validation reused = true
effect guard reused = true
checkpoint validation reused = true
verification reused = true
```

## template materialization

```text
materialized template count = expected template count
exact order preserved = true
exact template identity preserved = true
selected candidate preserved = true
observation coverage = true
verification coverage = true
stop coverage = true
rollback coverage = true
```

## hold境界

selected candidateがholdの場合は次を要求する。

```text
executable step count = 0
withheld template count = expected template count
```

holdは空の成功planや暗黙の実行許可へ変換されない。

withheld templateは可視のまま残る。

## lineageとdigest

```text
Wa authorization bound = true
replan identity bound = true
Wa identity used as replan identity = false
lineage collapse detected = false
replan receipt preserved = true
next-plan basis preserved = true
selected candidate preserved = true
Qi condition preserved = true
decision receipt preserved = true
synthesis packet preserved = true
```

## single-useとreplay

```text
replan receipt consumed = true
next-plan basis consumed = true
conflicting replay accepted = false
exact replay idempotent = true
```

同一receiptの正確なreplayは冪等である。

競合する別materializationは受理しない。

## event lineage

```text
v0.21 commit index
< materialization index
< materialization receipt index
```

adapter historyにはmaterializationとreceiptの2 recordを追加する。

## 所有権

```text
materialization owner = PlanOS
execution owner = ActOS
```

## 非権限境界

```text
compiler route != selected candidate identity
materialization != plan activation
materialization != execution permission
materialization != host licence
materialization != truth authority
materialization != clinical authority
materialization != legal authority
materialization != memory overwrite
materialization != WORLD update
```

## Lean定理

```text
hold_candidate_compiler_route
termination_candidate_compiler_route
materialization_requires_committed_next_plan_basis
compiler_route_is_exact_and_projected
hold_selection_projects_to_hold
termination_selection_projects_to_handover
exact_next_cycle_gate_matches_synthesis
exact_next_cycle_gate_uses_source_active_cycle
compiler_reuses_v01_and_all_guards
materialization_preserves_templates_identity_and_recovery
hold_materializes_zero_executable_steps
materialization_preserves_dual_lineage_and_digest_bindings
materialization_is_single_use_and_replay_safe
materialization_events_append_strictly
materialization_history_appends_two_records
materialization_bridge_preserves_ownership
materialization_bridge_grants_no_activation_or_execution
materialization_digest_is_exact
```

## Honest classification

```text
an exact PlanOS-owned compiler materialization receipt over a committed v0.21
next-cycle basis, reusing the v0.1 structured compiler and v0.3 adapter,
with explicit route projection, preserved selected identity, zero executable
steps for hold, single-use consumption and idempotent exact replay,
but without plan activation, execution authority, host licensing,
memory overwrite or WORLD update
```
