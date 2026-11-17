# KuuOS Lean→Python v0.11: Act checks before the native host call

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Baseline, problem and scope

The canonical baseline is main
`3da68503b6be1f6ef02d6100b730fa5ab9b92498`, the merged v0.10
PR #3571, tree `68a4277ff91556c073eb32cc5ebeef51352c0436`.
The observed local source snapshot matched 260/260 canonical Git blobs before
this change. GitHub source and independent CI, rather than this document, are
the authority for the submitted and integrated bytes.

v0.10 gates six original state transitions before their stores append a
commit. The original Act fixture creates its host tick before `store.apply`.
Consequently, that state gate cannot reject a bad invocation before its host
call. The original invocation builder checks the project state and bundle,
but does not repeat the earlier Act authorization check at invocation time.
The lower host checks its own license; it does not receive the complete Act
authorization. In addition, projection/job/operation ID agreement does not
by itself bind the real operation input to the Act-authorized input digest.

v0.11 adds a stricter caller around the original invocation builder, then
uses it in the same explicit, isolated, local native fixture. It retains the
original builder, host implementation, all six v0.10 store checks, and the
v0.9 write-once evidence format. Existing unguarded entry points remain as
they were. This is scoped executable Python checking, not a new Lean theorem
or a claim that all KuuOS effects have acquired a pre-host gate.

## Design choices and implementation sequence

The candidates considered were a pre-host Act gate, extending the phase
adapter to Plural/Wa, and a separate Belief Gerbe packet adapter. Plural/Wa
have phase/event-index models suitable for a later increment. Gerbe v0.3
has packet/receipt-history semantics and requires a distinct contract. This
increment addresses the concrete ordering gap before expanding OS coverage.

1. Exercise original native Act inputs and reproduce the missing current-time
   authorization and actual-input bindings without external side effects.
2. Add a finite-data, strict-input preflight before exactly one original
   invocation-builder call. Preserve original returned event/tick data.
3. Validate the returned event with the existing v0.10 transition guard.
   Record failures after entering the builder as possibly post-host failures.
4. Replace only the native fixture caller's imported builder binding inside
   a new child process; compose the existing v0.10 child route and restore the
   binding on both success and failure.
5. Add direct source pins and an additive `unittest.load_tests` hook so the
   unchanged cumulative CI runner executes all previous and new tests.
6. Verify the exact submitted head, test-merge tree and independent PR CI;
   after integration verify the actual main head and independent push CI.

## Added boundary

Independent reproduction against the original builder, with a harmless
in-memory executor, identified the following concrete ordering/binding gaps.
These reproductions establish behavior of the supplied snapshots, not the
authenticity of their asserted Plan or authorization provenance.

| Supplied condition | Original behavior observed | Added gate requirement |
| --- | --- | --- |
| Act authorization expired; host license still valid | One executor call, then APPLIED | Reject before builder/host entry |
| `single_use=False` or required human approval receipt empty | One executor call, then APPLIED | Revalidate authorization at invocation time |
| Act-authorized input differs from the actual job input | One executor call, then APPLIED | Bind actual input body, job digest, state and authorization |
| Invocation time precedes state time | One executor call, then event REJECTED | Reject time regression before the host call |
| Cached outer projection digest differs from its packet | One executor call, then event REJECTED | Check nested packet and cached digest together |
| License and policy allow two steps | Two executor calls in one slice | Require effective single-step scope |

`checked_build_authorized_invoke_event` takes the original builder's keyword
arguments and returns its original `(event, tick)` shape. Its JSON inputs
are copied using the existing bounded finite, exact-built-in JSON copier.
Registry functions are not JSON: a separate plain registry copy retains
trusted callable identities without authenticating those implementations.

The preflight rechecks current authorization, nested packet digests,
state/authorization/license/projection/job bindings, actual operation input,
strict numeric and authority fields, and the selected single-step slice
scope. The original lower host still performs its own checks. A successful
preflight is not an authorization issuer and cannot expand a license.

Explicit `null`, a missing key, or a non-string cached digest must not disable
any digest binding check. An omitted optional implementation argument and a
provided JSON `null` are distinct cases, covered by negative regressions.

The added single-step restriction concerns the **effective** lower-host
policy. The existing Lean `BoundedInvocation` is about at most one job and
one slice, not at most one step. The tighter Python step restriction must
not be presented as an already-proved step bound in that theorem.

`PreHostCheckError.host_call_attempted` distinguishes two boundaries:

| Value | Meaning |
| --- | --- |
| `False` | The added preflight rejected before entering the original invocation builder; the host was not called through this invocation. |
| `True` | The original invocation builder was entered; the host may already have run. Neither rollback nor absence of effects is inferred. |

The marker is deliberately conservative. A failure inside the original
builder may occur before or after its host call. An after-call validation
failure is never described as a proof of no effects, and is not retried.

## Native route and evidence

The new public builder requires a fresh existing directory and checks
selected source bytes before spawning `sys.executable -m ... --fixture-child`.
It passes argv directly without a shell. In that child only,
`runtime.v01_act_os_authority_bound_invocation.build_authorized_invoke_event`
is temporarily wrapped. The original kernel function and host function are
not replaced by this route. The parent retains its original bindings.

The wrapper composes v0.10's child, which invokes the original v1.3/v0.8/v0.9
native cycle and records the original evidence once. It reports one completed
Act pre-host-checked invocation and positive counts for all six state routes.
State counts include recovery replay calls; they are not new commit counts.
The parent independently rereads the evidence and validates the exact report
inventory, source, scope, counts and record digest.

The report is current unsigned child stdout, not a durable external
attestation. The separate read-only evidence audit does not execute the gate
and cannot establish that v0.11 ran historically. It retains v0.10's refusal
of nested symlinks and special files and v0.9's original ledger checks.

## Source preservation and cumulative execution

Seven new files contain the two runtime adapters, three test modules, one
source checker and this document. The only existing-file change appends a
`load_tests(loader, tests, pattern)` definition immediately before the
existing unittest entry point. It adds the new classes to the incoming suite
and returns that same suite. All original top-level imports remain intact,
including the exact imports required by the unchanged v0.10 source checker.

The v0.11 source checker verifies that removing exactly the added registration
block restores the original registry-test Git blob
`e9c88df079f8eed8dcd1852636ee1098f666ead4`. This checks preservation rather
than replacing an older checker or relaxing its expectations. Selected
original direct dependencies are pinned by Git blob digest; missing,
nonregular, linked or changed sources fail closed. This is not a transitive
source-closure or Python interpreter authentication claim.

Lean remains `leanprover/lean4:v4.30.0-rc2`, with the committed mathlib revision
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`. The canonical formal root,
theorem names/bodies, OS kernels/stores, old adapters, CI workflows and
cumulative runner are unchanged. Protected PR #1558 stays Draft and OPEN.

## Verification commands and acceptance criteria

```bash
python3 scripts/check_kuuos_lean_python_pre_host_sources_v0_11.py
python3 scripts/check_kuuos_lean_python_checked_transition_sources_v0_10.py
python3 -m unittest tests.test_kuuos_lean_python_pre_host_guard_v0_11 -v
python3 -m unittest tests.test_kuuos_lean_python_pre_host_native_cycle_v0_11 -v
python3 -m unittest tests.test_kuuos_lean_python_pre_host_sources_v0_11 -v
python3 -m unittest tests.test_kuuos_lean_python_os_registry_v0_5 -v
```

Acceptance requires actual original native execution, an expired authorization
rejected through the real native caller with zero host calls and no changes
to store bytes, preservation of original return data, distinct pre/post-host
failures, child-only binding replacement, source preservation, all retained
Lean→Python tests, and independent exact-head GitHub Runtime/Governance.
Local results were observed on 2026-11-18 JST before submission:

| Check | Observed result |
| --- | --- |
| New pre-host guard tests | 19/19 passed |
| New actual-child/native boundary tests | 17/17 passed |
| New source/registration tests | 27/27 passed |
| New v0.11 total | 63/63 passed |
| Retained v0.5–v0.10 cases | 201 retained |
| Updated v0.5–v0.11 cumulative suite | 264 cases |
| Retained v0.1–v0.4 cases | 91 retained |
| Fresh combined selected regression | 355/355 passed, 8.944 seconds, no failures/skips |
| Direct source pins versus canonical GitHub tree | 49/49 matched |
| Existing v0.10 source checker | 33 pins and original imports passed unchanged |

The combined command selected the six original v0.1–v0.4 test modules and
`tests.test_kuuos_lean_python_os_registry_v0_5`. The latter uses the additive
hook; there are no duplicate test IDs. Initial negative tests failed before
implementation. Review then exposed the null-cached-digest and ticket
identifier coercion cases; added regressions failed before those corrections
and passed afterward. Native test function-identity storage was corrected to
avoid Python binding a stored class function as a test-instance method.

PR and postmerge main certification are separate gates. Their receipts are
recorded in the GitHub PR, including exact source/merge/tree/run IDs. No full
repository or independent CI success is inferred from the local selected
snapshot alone.

## Uncertified boundaries retained

- The caller supplies a trusted, quiescent state/bundle snapshot and registry.
  The API cannot establish that a detached state is the current store state,
  arbitrate concurrent writers, or authenticate executable registry code.
  `now_ms` is supplied data, not an attestation of the current wall-clock time.
  Preflight cost checks use supplied estimates; they do not prove actual
  executor cost or constrain arbitrary external effects of trusted code.
- Digests and source references do not authenticate an external authorization
  issuer, a human approval, or the original committed Plan. At this boundary
  the complete Plan packet is absent; reference consistency is checked.
- The gate does not make host execution and journal commit atomic, guarantee
  exactly-once effects across repeated old snapshots, or undo a host effect
  after an exception, timeout, failed event check or failed store commit.
- `HostReceiptSemantics.blocked_records_no_effect` uses an explicit
  `blockedNoEffect` hypothesis. It does not prove that a Python host returning
  BLOCKED after entering an executor has produced no effects.
- The existing `FivefoldBinding`, `SelectedActStep` and
  `AuthorizationBoundary` Lean theorems expose fields required by their
  structures. The added Python checks have no proved refinement to them.
- Native Belief Gerbe v0.3, Plural/Wa, WORLD, MemoryOS and CodeAI do not gain
  transition coverage from this increment. Six existing state routes and the
  selected native Act invocation remain the exact tested scope.
- No truth, clinical, legal, institutional, unrestricted tool or Git merge
  authority follows from a successful check or a fluent explanation.
