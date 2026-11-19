# Lean→Python v0.38 — Five original persisted OS stores, four typed local edges

## Authoritative scope

Repository `itakura-hidetoshi/KuuOS`, canonical branch `main`.
This Python-only stage is based on the v0.37 certified merge
`d0340d150312696b508595d9c24a864c0f7bae11`.

Lean v4.30.0-rc2; mathlib fixed at
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.

No original Lean theorem, OS kernel, store, fixture, or previously
certified Lean→Python adapter is modified. Protected PR #1558 is not
merged. Continue append-only/tighten-only/overwrite-forbidden/same-root,
using GitHub MCP. Do not launch Strict Lean for Python/docs-only edits.

## What is actually checked

This covers **one selected five-node suffix**, not the whole KuuOS
system and not a global theorem:

```text
PlanOS --[original Plan activation receipt]--> ActOS
       --[committed effect + host record]--> ObserveOS
       --[committed observation + evidence]--> VerifyOS
       --[committed verification + learning debt]--> LearnOS
```

The plan is still conditioned on its upstream Wa and DecisionOS
context. No direct shortcut past them is asserted.

1. The five supplied original native final states and five named
   persisted roots are accepted as a single fixed input. Unknown
   names, duplicate roots, custom path coercions, nonfinite/invalid
   JSON and incompatible sources are blocked.
2. The original PlanStore genesis, append-only ledger and snapshot
   are independently replayed, with exact final state, chain
   indices and source lineage checked. It is not enough that the
   supplied PlanOS state has a plausible digest.
3. The original v0.34 Plan→Act adapter binds the genuine Plan
   activation receipt to the original ActStore genesis and final
   committed host record; the explicit **numeric jobs/slices witness
   and external issuer obstructions** remain unproved.
4. The original v0.35 Act→Observe, v0.36 Observe→Verify, and v0.37
   Verify→Learn adapters each replay their original stores and
   check the original source→receiver genesis and final native
   evidence/debt state. Every intermediate native state is the
   same exact supplied object on its incoming and outgoing edge.
5. The original `audit_typed_path(..., start="PlanOS", end="LearnOS")`
   separately checks all four registered typed edges, the
   Plan→Act receipt, global **contextual equality** of lineage
   and mission contract fields in this bounded path, and
   nonregression of observed local timestamps. This is runtime
   compatibility, **not** formal descent or a global snapshot.
6. All fifteen persisted genesis, ledger and snapshot files are
   checked before and after the read-only audit. This detects a
   locally observed change but does **not** establish an atomic
   multi-store transaction, a cryptographic signature, or
   concurrency-free cross-store history.

The positive status `SCOPED_FIVE_STORE_CHAIN_COMPATIBLE` is returned
only when *every* local auditor and the typed path auditor succeed
on the same supplied snapshot. Observed incompatible sources are
`BLOCKED`; genuinely missing source remains `NO_DATA`.
When both exist, `BLOCKED` takes precedence and the issues
are preserved rather than erased.

## Lean source hierarchy and interpretation

Original pinned Lean sources, **not edited** in this stage:

- `formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean`
- `formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean`
- `formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean`
- `formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean`
- `formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean`

The registered source fields, original receipts, and previous
Lean-premise Python projections are checked as **conditional,
local predicates** only. The mapping from these Lean structures to
Python names and state fields is an interpretation/implementation
layer. A Python `True` does not construct a Lean proof term.

In particular, conditional verification does not mean absolute
truth and an admissible future-only learning candidate does not
activate itself or authorize execution.

## New files

- `runtime/kuuos_lean_python_five_store_chain_compat_v0_38.py`
- `scripts/check_kuuos_lean_python_five_store_chain_sources_v0_38.py`
- `tests/lean_python_extensions/test_five_store_chain_compat_v0_38.py`
- `tests/lean_python_extensions/test_five_store_chain_sources_v0_38.py`
- `docs/KUUOS_LEAN_PYTHON_FIVE_STORE_CHAIN_COMPAT_v0_38.md`

Seventeen original Lean/native Git blobs are pinned exactly; all
v0.37-and-earlier source pin tests remain active. Tests use the
real original native v1.3 full-cycle fixture and the original
Plan activation constructor with the original fixture values.
That generated fixture is **not** externally issued authority.

## Open obstructions not discharged

- ActOS actual `jobsClaimed` and `slicesRun` vs Lean numerical witnesses.
- External activation and host receipt issuer authenticity.
- BeliefOS gerbe v0.3 vs formal v0.1 correspondence.
- Complete Lean/Python semantic refinement.
- Global descent/gluing from independent or partial contexts.
- Multi-store atomic snapshot, independent WORLD truth and
  authority to execute, change clinical/legal policy, overwrite
  memory, merge Git, or activate learning.

## Merge gate

PR remains Draft/Open/NO MERGE until its exact HEAD has independent
cumulative Python Runtime and Governance completed/SUCCESS, full
paginated job audit, all source pins, exact submitted-head/test-merge
Git tree equality and exact-head terminal SUCCESS.

Repair any failure **in the same PR**, after inspecting the entire
modified source, imported dependencies, typed signatures and root
cause. Existing core source files are never overwritten.
