# CodeAI Repair Cycle Admission Consumption v0.1

## Status

Additive, fail-closed CodeAI boundary.

This stage consumes one sealed, non-reusable
`CodeAI Repair Cycle Continuation Admission v0.1` receipt and converts its
five reserved resource dimensions into one active, one-shot, externally
consumable bounded repair-cycle execution input.

It does not execute the repair cycle.

## Route

```text
sealed continuation-admission receipt
+ fresh consumption request
+ deny-by-default consumption policy
+ sealed replay/consumption registry
  -> exact admission and lineage correspondence
  -> replay exclusion
  -> monotone registry transition
  -> exact five-dimensional budget mapping
  -> one active non-reusable bounded execution input
  -> sealed consumption receipt
  -> sealed next registry
```

## Inputs

### Continuation-admission receipt

The source receipt must:

- be sealed with the canonical continuation-admission receipt digest;
- use the supported profile, disposition, and operating mode;
- admit exactly `current_cycle_index + 1`;
- remain within the source cycle limit;
- carry conserved candidate, provider-call, command, timeout-second, and
  output-byte reservations;
- be non-reusable, unconsumed, inactive, and future-only;
- have performed no cycle, runner, repository, Git, network, secret, merge, or
  deployment action;
- grant no prior execution or general successor authority.

### Consumption request

The request binds:

- the exact admission receipt digest;
- admitted cycle index;
- source cycle and selected-candidate lineage;
- repair receipt, regeneration receipt, repair candidate set, and verification
  plan digests for the admitted cycle;
- one execution session ID;
- one execution nonce digest;
- the consuming actor;
- a freshness epoch.

### Consumption policy

The policy fixes all expected lineage, cycle, downstream input, and actor
values. It also bounds registry capacity and requires network, secret, live
repository, Git, and automatic execution permissions to remain false.

### Consumption registry

The sealed registry records previously consumed admission receipt digests and
execution nonce digests in parallel histories. The stage rejects:

- admission replay;
- execution nonce replay;
- malformed or divergent parallel histories;
- exhausted registry capacity;
- non-monotone cycle consumption.

The returned next registry increments its revision and consumed-admission count
by exactly one.

A registry transition receipt is not itself proof that an external store
persisted the update atomically. The caller must commit the returned registry
through its own atomic storage boundary before using the execution input.

## Execution input

The issued execution input is:

- active;
- limited to one admitted cycle;
- one-shot and non-reusable;
- initially unconsumed;
- bound to the exact source and downstream digests;
- bound to the exact execution session and nonce;
- bounded by exactly the reserved candidate, provider-call, command,
  timeout-second, and output-byte budgets.

It grants only the bounded authority needed by an external isolated repair-cycle
executor to generate/select candidates, apply a patch to an isolated snapshot,
and execute verification within those budgets.

It grants no:

- automatic execution;
- network access;
- secret access;
- live repository access;
- Git operation;
- merge;
- deployment;
- general successor-stage authority.

## Output artifacts

The runtime returns:

1. a sealed active bounded execution input;
2. a sealed next consumption registry;
3. a sealed admission-consumption receipt.

The consumption receipt records exact budget correspondence and registry
transition but remains inactive and future-only. No provider, runner, cycle,
patch, verification, repository, Git, network, secret, merge, or deployment
action is performed by this stage.

## Fixed semantics

- admission consumption != cycle execution
- admission consumption != correctness
- admission consumption != successful repair
- reservation != resource consumption
- execution input issuance != provider invocation
- execution input issuance != candidate generation or selection
- execution input issuance != patch application
- execution input issuance != verification
- one-shot input != reusable capability
- replay-registry receipt != external atomic persistence
- bounded cycle authority != automatic execution authority
- bounded cycle authority != live repository or Git authority
- consumption receipt != merge, deployment, or general successor authority

## Fail-closed conditions

The stage blocks on any malformed shape, missing or extra field, invalid type,
digest mismatch, unsupported source profile, invalid source authority state,
cycle mismatch, lineage mismatch, stale request/registry, actor mismatch,
replay, registry-capacity exhaustion, non-monotone registry frontier, or
budget-conservation violation.

## Artifacts

- runtime:
  `runtime/kuuos_codeai_repair_cycle_admission_consumption_v0_1.py`
- checker:
  `scripts/check_codeai_repair_cycle_admission_consumption_v0_1.py`
- tests:
  `tests/test_kuuos_codeai_repair_cycle_admission_consumption_v0_1.py`
- example:
  `examples/codeai_repair_cycle_admission_consumption_v0_1.json`
- manifest:
  `manifests/kuuos_codeai_repair_cycle_admission_consumption_v0_1.json`
- formal kernel:
  `formal/KUOS/CodeAI/RepairCycleAdmissionConsumptionV0_1.lean`
- formal root:
  `formal/KuuOSCodeAIRepairCycleAdmissionConsumptionV0_1.lean`
- workflow:
  `.github/workflows/codeai-repair-cycle-admission-consumption-v0-1.yml`

## Validation

The dedicated workflow checks:

- Python syntax;
- example and manifest JSON;
- end-to-end integration;
- 25 fail-closed unit tests;
- canonical `lake-manifest.json`;
- strict Lean compilation with warnings and `sorry` treated as errors;
- the full `KuuOSFormal` baseline.
