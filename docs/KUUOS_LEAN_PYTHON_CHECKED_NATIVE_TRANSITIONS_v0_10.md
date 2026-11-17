# KuuOS Lean→Python v0.10 — checked native state transitions

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Baseline and purpose

Canonical repository: https://github.com/itakura-hidetoshi/KuuOS
Baseline main: `8b855cf1f1c2296dbe0d8d3057cd391729d572d1` (v0.9).
Lean v4.30.0-rc2 and mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6` remain fixed.

The selected conditional Lean statements already name phase order,
event-index advance and authority boundaries. v0.1 exposes Python
projections of those conditions. v0.9 checks a completed local fixture.
v0.10 makes those projections participate in the original six-core
Python event route before a store appends a commit.

This is a Python implementation and test increment. It does not prove
Lean/Python semantic refinement, formal descent, external issuer
authenticity, history, truth, execution permission or Git merge authority.
The correspondence of formal structures with 空 and 縁起 remains an
interpretation, not a new theorem.

## Design and alternatives

The selected design adds a fixed-dispatch `checked_apply_event` adapter
and uses it in a fresh local child process. The child temporarily binds
the six original store modules to this adapter, calls the unchanged native
v1.3/v0.8 fixture route and retains the v0.9 evidence format and audit.
The parent process never changes these bindings.

An all-ledger read-only replay would extend post-run inspection but would
not put a check before the store commit. A signed issuer design needs a
separate, real trust and key model. Neither supplies this specific state
transition integration. The selected adapter is additive and permits
source-byte pins for all original direct dependencies.

No original kernel, store, native builder, Lean theorem, v0.1–v0.9 adapter,
public formal root, cumulative runner or workflow is changed. The only
existing file extension registers new tests in the existing v0.5 suite.
Protected PR #1558 and other Lean repair branches are outside this change.

## Interfaces and coverage

- `runtime/kuuos_lean_python_checked_transition_v0_10.py`:
  `checked_apply_event(os_name, state, event)` returns the native result
  without promoting its status. It raises `CheckedTransitionError` when
  required input is absent or a checked condition fails.
- `runtime/kuuos_lean_python_guarded_native_cycle_v0_10.py`:
  `build_guarded_native_fixture(root)` explicitly constructs a bounded
  local test fixture in a separate child, then independently audits the
  persisted v0.9 evidence. Its per-OS counts describe checked calls in
  that invocation, including recovery replays, not unique new commits.
  `audit_local_evidence(root)` reads existing evidence and rejects
  symlinks in the fixture. This later audit does not prove that a past
  run used the new guards.

| Guarded OS | Original function | Native fixture store |
| --- | --- | --- |
| DecisionOS | apply_decision_event | decision |
| PlanOS | apply_plan_event | plan |
| ActOS | apply_act_event | act |
| ObserveOS | apply_observe_event | downstream/observe |
| VerifyOS | apply_verify_event | downstream/verify |
| LearnOS | apply_learn_event | downstream/learn |

Native BeliefOS is Gerbe v0.3, not the BeliefOS v0.1 schema of the core
projection. Plural and Wa retain the existing edge-based checks. These
three, WORLD, MemoryOS and CodeAI do not acquire six-core transition
coverage from this implementation.

## Checked transition conditions

The adapter copies finite exact built-in JSON, validates the full input
state using the original validator, invokes the fixed original pure
kernel once and checks its exact result envelope. It checks status,
native result and event digests, input/output bindings, full output
state, exact integer event indices, phase order, append-only histories,
predecessor binding and unchanged source identity. Caller input is not
mutated. A REPLAYED or REJECTED result retains its native status and must
leave the state unchanged; structural acceptance never turns it into
APPLIED.

An observed v0.1 projection gap is closed in this new route: a present
`status=None` bypassed its status-specific branches. The new adapter
requires an exact known string before calling that projection. Python
numeric equality is also insufficient for a Nat-like event index: bool
and float aliases must not substitute for exact integer indices. An old
event ID cannot validate a replay whose event body has changed.

## State-commit boundary and host effects

Original store `apply()` calls its imported kernel function before
appending a journal commit or replacing its saved snapshot. Raising in
the added wrapper stops those state writes for that invocation. Store
recovery also calls that binding, so earlier events are checked again.

The original ActOS fixture calls `build_authorized_invoke_event`, which
runs the bounded test host tick before `store.apply`. This gate cannot
undo that earlier tick and is not pre-host-effect authorization. It
grants no host capability. The fixture builder is explicitly effectful
local test code; the event adapter and evidence audit are separate.

## Evidence limits

The persisted evidence remains the exact v0.9 format. Guard counts are
the child output observed by the builder, bound to the resulting v0.9
record digest. They are not an independently signed historical receipt.
The read-only evidence audit alone never certifies past guard execution.
Quiescent trusted local fixture roots and a trusted Python interpreter
are required; concurrent hostile filesystem writers are out of scope.
The added local audit refuses symlinks, including inside `act`, before
reading inherited ledger paths. It does not create an external root ID.

## Implementation and verification plan

1. Add failure tests for strict native result/status/type/history/event
   bindings; implement the adapter without editing originals.
2. Exercise all six store bindings in the real child-process fixture;
   assert parent bindings stay original, and rejection stops journal
   and snapshot writes. Check restoration on child-local failure.
3. Add exact direct-source byte pins and AST test-registration checks.
   Keep the existing v0.1–v0.9 checks and runner unchanged.
4. Run the new tests and the existing Lean→Python regression suites.
   Review the complete new source and result contracts independently.
5. Submit the verified source through GitHub MCP. Observe actual
   workflow, job and test step completion on its exact HEAD, compare
   source/test-merge Git trees, then reobserve any formal integration
   and its independent main push checks. Python-only Strict Lean is
   skipped; no new formal proof is claimed.

Review focus: null/missing status, bool/float aliases, coherently resealed
history/identity changes, altered replay bodies, unexpected mutation,
unsupported native schemas and Act host-effect ordering.

## Local validation and reproducible commands

The v0.10 tests contain 34 adapter cases, 17 real native child/store cases
and 21 static-source/discovery cases. Together with the retained v0.1–v0.9
tests, the selected Lean→Python regression run executed 292 tests with no
failures or skips. The cumulative v0.5 entry now executes 201 tests; its
previous 129 cases are retained. These numbers are scoped to these suites,
not a count of all unique tests in the repository.

```sh
python3 scripts/check_kuuos_lean_python_checked_transition_sources_v0_10.py
python3 -m unittest -v tests.test_kuuos_lean_python_os_registry_v0_5
```

The unchanged `scripts/run_kuuos_runtime_full_check_v0_55.py` runs the
full existing cumulative route in the complete GitHub checkout. Independent
CI must be judged from its actual completed workflow/job/steps and test
logs for the submitted SHA. A local partial snapshot is not that CI.

The checked adapter can be explicitly used as follows, with real native
state and event objects supplied by the caller:

```python
from runtime.kuuos_lean_python_checked_transition_v0_10 import checked_apply_event

native_result = checked_apply_event("PlanOS", before_state, native_event)
```

Its successful return preserves the native status, including REJECTED and
REPLAYED. Any persistence belongs after the call. The guarded fixture
builder demonstrates this ordering in the original six stores without
changing their source files.
