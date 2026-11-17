# KuuOS Lean→Python v0.12 — Plural/Wa native event boundaries

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Baseline and scope

The source baseline is main commit
`dacc6fb5ae3cd85b9afee48d53348e6cc0a8dcc7` (v0.11, PR #3572).
This additive Python extension checks the original DecisionOSPlural v0.2
and DecisionOSWa v0.3 event results. An explicit local native test builder
composes those two store bindings with v0.11's six core event gates and its
selected Act invocation input check. The original Lean declarations,
kernel/type/store code, host implementation, native v1.3 fixture, previous
adapters, and CI runner/workflows are retained.

The event-result gate runs before the original store uses that result to
append a commit and update its snapshot. Recovery through the wrapped store
also checks replayed ledger events. Original store initialization still
writes genesis, an empty ledger, and an initial snapshot using its existing
validation. This extension does not guard every store write or make the
filesystem and host effects transactional.

## Pure checked transition

`runtime/kuuos_lean_python_mediator_transition_v0_12.py` exports
`checked_apply_mediator_event(os_name, state, event)` for exactly
`DecisionOSPlural` and `DecisionOSWa`.

It takes bounded finite built-in JSON copies, validates the supplied state,
calls the original pure kernel once, and validates the returned native result.
It writes no store and invokes no host. Missing prerequisites produce
`MediatorTransitionError` with `NO_DATA`; malformed data or failed conditions
produce `BLOCKED`. A native `REJECTED` result remains a rejection and does not
become an applied transition. Successful `APPLIED` and `REPLAYED` events need
strict event types, exact Boolean flags, a body digest, and history binding.
Native rejected inputs may retain their native diagnostic representation.

| Boundary | Conditions checked |
| --- | --- |
| Native envelope | Exact eight-field inventory; original version; strict APPLIED/REPLAYED/REJECTED status; errors and status aligned; original state/event/result digests bound |
| State structure | Original pre/post validators; exact integer counters/timestamps; original phase order and index; exact authority/boundary Booleans; local history and processed-digest alignment |
| Applied event | One phase step and one index step; event timestamp bound to result; predecessor and identity bound; one exact appended event/history row |
| Unchanged fields | All fields outside the original target phase's write set remain canonically unchanged, including source references, thresholds, and inert extra JSON fields |
| Plural receipt | `source_binding_receipt_digest` may be set at stakeholder registration and must equal that event's receipt; it stays unchanged at other phases |
| Plural history | Existing appeal prefix preserved; appended appeals bound to the incoming data; future-only/non-overwrite flags remain exact Booleans |
| Commit | Original terminal commit count and summary alignment; one appended summary; committed digest and original summary fields bound |
| Wa identity | Endorsements and retained/review options stay within supplied source options; an ENDORSE result preserves the selected source option identity |
| Replay/rejection | Result state remains canonically unchanged; a successful replay also binds the supplied event body to the prior processed digest and corresponding history row |

Selected record construction is checked against the original pure
normalization helpers on defensive copies: stakeholder registration,
appended appeals, and Wa profiles remain bound to their event payloads.
This does not call `apply_*_event` a second time or reimplement the numerical
scoring and route-selection algorithms.

Plural has nine phases, with eight advancing events from `bind_v01` to
terminal `commit`. Wa has seven phases, with six advancing events from
`bind` to terminal `commit`. They retain their own phase names and commit
summary schemas; this extension does not modify the prior six-core adapter.

Input validity is local to the supplied self-consistent state. A digest
reference does not authenticate an external receipt, stakeholder, source
decision, or issuer. The adapter does not reconstruct an absent external
source state or prove the full past event bodies from history rows alone.

## Native process composition and evidence

`runtime/kuuos_lean_python_mediated_native_cycle_v0_12.py` exports
`build_mediated_native_fixture(root)` and read-only `audit_local_evidence(root)`.
The builder requires an existing, empty, nonlinked trusted local directory.
It checks selected source bytes before launching a fresh Python interpreter
with the explicit `--fixture-child ROOT` mode. The child temporarily wraps
only the original store modules' imported `apply_plural_event` and
`apply_wa_event` bindings, then invokes the existing v0.11 child route.
Original kernel functions and host bindings remain intact. Context cleanup
restores bindings, including partial setup failure; parent-process function
replacements are not inherited by the new interpreter.

The complete checked fixture path contains these eight state routes:

1. DecisionOS
2. DecisionOSPlural
3. DecisionOSWa
4. PlanOS
5. ActOS
6. ObserveOS
7. VerifyOS
8. LearnOS

The inherited selected Act pre-host input check must complete once. Counts
include recovery replays and are not a count of distinct persisted commits.
They are observations in a local child's unsigned stdout report. The parent
requires all eight strict positive integer counters, one exact pre-host
counter, the current source/version, narrow-scope flags, and the same native
evidence record hash as its independent read-only audit.

The v0.9 write-once evidence record and its inventory are unchanged. The new
report is not inserted into or substituted for that record. A later audit
reads the original evidence and does not rerun or prove historical use of
the v0.12 guards. Child failure is not retried; partial output is retained
for inspection; an existing fixture is never overwritten by the builder.

This covers a bounded local fixture under a trusted, quiescent checkout and
root. Process separation does not establish an OS sandbox or defend against
a concurrent hostile process rewriting the checkout or fixture directories.

## Existing Lean artifacts and the boundary of the claim

The source checker retains the original artifacts:

- `formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean`
- `formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean`

Their phase, index, and history statements have explicit model hypotheses.
Plural's history/count theorems do not by themselves prove prefix identity
for Python JSON arrays. The runtime extension checks that prefix identity
directly. Several decision properties are witness/structure conditions;
passing a Python check is not a proof that every such premise holds.

Wa also has real-number interval and weight theorems. They do not establish
that Python floating-point normalization, tolerances, rounding, or clipping
refine the Lean real-number model. The v0.12 boundary does not certify that
numerical correspondence or the semantic correctness of Plural/Wa scoring.
Even a structurally checked route must not promote an accepted native
numeric result to a Lean-proved real-number result.

No Lean declaration or proof is added here. A Python-only PR's skipped
Strict Lean job does not confer a new formal proof. The fixed Lean and
Mathlib pins remain unchanged, as do the protected Draft PR #1558 and
unrelated proof-repair work.

## Source preservation and test registration

`scripts/check_kuuos_lean_python_mediator_sources_v0_12.py` checks 66 selected
direct original Git blobs at the baseline, retaining all 49 previous pins
and adding the mediator and inherited v0.11 dependencies. It additionally
checks the fixed new extension loader, the eight new required files, and
the one additive test registration block. These are selected byte checks,
not authentication of the transitive import graph or arbitrary test code.

The previous v0.5 cumulative test module and v0.10/v0.11 source checkers
remain byte-for-byte unchanged. The existing runner already selects
`tests.test_kuuos_lean_python_plan_act_native_v0_4`; this module gains only
one `load_tests` hook before its main entrypoint. Removing precisely that
block must recover its original baseline Git blob. The hook adds the
extension suite to the incoming native suite and returns the same suite.
All original seven native tests remain in the ordinary runner.

The helper in `tests/lean_python_extensions/__init__.py` runs static source
preflight before standard `unittest` discovery of `test_*.py` in that fixed
package. It requires ordinary test IDs from each of the three v0.12 modules,
rejects duplicate extension IDs, and preserves ordinary import failures as
failing tests. Missing files, an empty required module, or an import-time
skip cannot silently certify the required extension suite. Additional
extension test modules can be discovered without editing the fixed runner
or the byte-pinned older cumulative module. General whole-repository
discovery may also select these modules independently; global deduplication
is not claimed.

The standard protocol is documented in Python's
[unittest load_tests documentation](https://docs.python.org/3.12/library/unittest.html#load-tests-protocol).
The relevant validation is the unchanged repository runner's invocation,
not merely a separate manual selection of the new tests.

## Reproducible checks

From the repository root:

```sh
python3 scripts/check_kuuos_lean_python_mediator_sources_v0_12.py
python3 scripts/check_kuuos_lean_python_pre_host_sources_v0_11.py
python3 scripts/check_kuuos_lean_python_checked_transition_sources_v0_10.py
python3 -m unittest tests.test_kuuos_lean_python_plan_act_native_v0_4 -v
python3 -m unittest tests.test_kuuos_lean_python_os_registry_v0_5 -v
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

The new tests use original native fixtures and kernels, structurally
resealed corrupt results, real mediator stores, a real fresh child process,
and source/registration negative cases. They verify that an added check
failure after a real kernel result leaves both mediator ledgers and
snapshots unchanged, and that native replay/rejection append no extra
commit. Test counts and independent run identifiers belong to the PR's
observed CI record; this document does not predeclare a pending CI success.

## Explicitly unverified

`MediatedNativeRun` keeps all of the following claims false:

- Every store write is guarded.
- Wa real-number/Python numerical refinement is proved.
- Every failure prevents all prior effects; host rollback is guaranteed;
  the store commit is atomic with host effects.
- An external issuer is authenticated or past guard execution is proved.
- Lean/Python implementation refinement is proved.
- Execution, truth, or Git merge authority is granted by the receipt.

The other OS/packet routes remain outside this new event-gate scope. In
particular, eight checked state routes do not certify all registered OS
models, WORLD, Memory, CodeAI, or the Belief/Gerbe packet semantics. Existing
native rejection, missing-data states, and failed conditions remain visible.
