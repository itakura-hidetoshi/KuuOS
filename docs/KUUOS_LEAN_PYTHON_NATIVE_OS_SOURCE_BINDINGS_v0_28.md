# KuuOS Lean→Python v0.28 — genuine original OS-state → Lean-condition bindings

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical source, boundaries and reason for this stage

Repository: `itakura-hidetoshi/KuuOS`, canonical `main`.
Parent main HEAD: `bf2eda97f843093b3be538495839b08c1b45d298`
(v0.27 — 12 OS-specific Python obligation modules formally merged).
Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only, tighten-only, overwrite-forbidden, same-root.
Protected #1558 remains Draft/Open/unmerged.

**Original research aim:** Convert actual Lean-proven logical conditions
into executable Python structures *in each KuuOS OS*, preserving source,
scope, provenance and missing evidence. v0.27 added 12 distinct Python
OS theorem-data obligation modules but relied on separately supplied
witness dictionaries. This stage connects selected modules to the
**actual original stored KuuOS native states, step DAG and receipts**.

No original Lean file, Python OS kernel, state type, store, event, source
registry, or existing CI runner is changed. This is a Python-only additive
stage and should not trigger Strict Lean for a docs/runtime-only diff.

## Native source validation sequence

1. Copy only bounded, exact built-in finite JSON. Never execute a
   user-defined serialization hook or mutate the original state.
2. Call the original OS validator through the already-merged v0.27
   registry. Any failure is a real blocker; missing history is NO_DATA.
3. Require a genuine committed source phase before claiming completed
   transition-dependent data.
4. For ObserveOS, VerifyOS and LearnOS, also run the original typed
   Act→Observe→Verify→Learn edge checker on both supplied source states;
   an omitted upstream state cannot be silently reconstructed.
5. Read exact original field names and compare original hashes/digests,
   source identities and appropriate enum values.
6. Pass only these projected values to the existing v0.27 per-OS
   `audit_witness` implementation.
7. A final `SOURCE_BOUND_LOCAL_CHECKED` result means a **local
   validated native-state Python projection** of selected theorem
   conditions, not proof of universal interpreter semantics or an
   externally issued receipt.

Implementation code remains separated by OS:

| OS | New native binding module | Source and selected Lean consequence |
|---|---|---|
| PlanOS | `runtime/kuuos_lean_python_plan_native_binding_v0_28.py` | original committed `steps`, `guard_summary` and `checkpoint_summary`; for each effectful step, rollback-or-escalation, stop conditions, future observe/verify dependency |
| ActOS | `runtime/kuuos_lean_python_act_native_binding_v0_28.py` | exact Plan-step identity, actual original authorization, host license, projection, host receipt, and historical authorization event; numeric host-job count stays NO_DATA |
| ObserveOS | `runtime/kuuos_lean_python_observe_native_binding_v0_28.py` | actual committed source Act, ready host receipt and source Act→Observe typed edge, original `comparison_receipt` and observation debt |
| VerifyOS | `runtime/kuuos_lean_python_verify_native_binding_v0_28.py` | source Observe→Verify typed edge, native corroboration and adjudication receipts, verdict/criterion/falsifier and exact verification-debt flags |
| LearnOS | `runtime/kuuos_lean_python_learn_native_binding_v0_28.py` | source Verify→Learn typed edge, native `learning_delta` source digest, future-only/no-overwrite/no-activation and visible reversal/expiry conditions |

The shared bounded helper lives in
`runtime/kuuos_lean_python_native_os_source_binding_v0_28.py`.
It never writes any runtime file or replaces any KuuOS OS.

### Intentionally retained ActOS obstruction

The genuine host v0.17 receipt contains
`one_job_claimed_at_most = True` and
`one_bounded_slice_run_at_most = True`. The license records
`max_jobs_per_invocation = 1`. These are **source claims and an
authorization bound** — they are not a Lean-certified observed numeric
`BoundedInvocation.jobsClaimed` and `slicesRun`.

The ActOS checker validates the stored authorization and license against
the original source and a **historical** authorization-event timestamp,
not the current time or a new host license. It returns **NO_DATA**, with
the missing actual numeric evidence explicitly preserved, even if the
local receipt checks pass. The result grants no host permission. An
ActOS source projection cannot be labeled fully certified simply
because `max_jobs_per_invocation = 1`.

### Native fixture and test provenance

Tests use the **original**
`runtime.kuuos_qi_world_native_full_cycle_v1_3.build_native_full_cycle_receipt`
in an isolated temporary directory. It constructs the original
Belief→Decision→Plural→Wa→Plan→Act→Observe→Verify→Learn source chain,
with genuine original Python state validators, store commits and
receipts. No synthetic successful `audit_edge` monkey-patch is used.

The test suite checks that real source projections pass for Plan,
Observe, Verify and Learn; the ActOS numeric obstruction remains
NO_DATA; data remain byte-identity-preserving; missing upstream
records, incorrect source digests, false authority flags, invalid
evaluation conditions and altered stored original receipts are blocked
or kept NO_DATA. A separate source integrity test retains the v0.27
proof registry and exact-pins 15 unchanged original Lean/source files.

## Formal status: keep proven Lean separate from Python

Original Lean sources and their selected theorem names are inherited
unchanged. The compiled Lean statements prove implications about
well-formed original Lean structures under their own proof fields.
The Python data projections check corresponding explicitly named
fields but **do not construct those proof fields** and are not
a whole-program Lean↔CPython refinement theorem.

Local Python state and source digest matching is not proof of external
issuer authenticity, historical completeness, hardware semantics,
execution permission, medical/legal authority or downstream correctness.
Successful local path checks do not establish global descent.

The other OSs (BeliefOS, DecisionOS, DecisionOSPlural, DecisionOSWa,
MemoryOS, CodeAI and WORLD) retain their v0.27 per-OS modules and
original validator/mediator-source contracts, but have **no invented**
native v0.28 full binding. Source-typed field projection for these
is a subsequent research obligation, not presumed completed.

## Release gate — same exact HEAD

```sh
python3 scripts/check_kuuos_lean_python_native_os_source_bindings_v0_28.py
python3 -m unittest -v tests.lean_python_extensions.test_native_os_source_bindings_v0_28
python3 -m unittest -v tests.lean_python_extensions.test_native_os_source_bindings_sources_v0_28
```

The 10 new files, old pinned sources, exact-head source/test merge Git
tree, independent cumulative Python Runtime and final all-job Governance
must pass for **the same source HEAD** before merge. Do not call a
skipped Lean CI a successful new theorem certification. Do not weaken
or overwrite original runtime/Lean files or expand authority.
