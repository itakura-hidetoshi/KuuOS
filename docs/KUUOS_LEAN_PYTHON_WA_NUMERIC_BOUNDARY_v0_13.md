# KuuOS Lean→Python v0.13 — Wa numeric interval boundary

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Source and observed obstruction

Baseline: main `a866f5841e8f324133928eed101cec405d67ac76` (v0.12,
PR #3573). This extension adds Python checks; it changes no original Lean
theorem, OS kernel/type/store, prior adapter, fixture, runner, workflow,
toolchain, Mathlib pin, or existing test/loader file.

The original native Wa evaluator can return an inverted interval while
its validator and the v0.12 structural gate both accept the result. A
reproducible fixture starts with the original committed Plural source and
the original Wa weights, adds `5e-13` to the `inclusion` weight, and uses
`[1,1]` for every positive profile axis and `[0,0]` for every alert axis.
The original `bottleneck_weight=0.35` stays unchanged.

| Quantity after the original profile→evaluate event | Observed value |
| --- | --- |
| Python weight sum | `1.0000000000005` |
| Weighted lower and upper | `1.0000000000005` |
| Relational lower and upper | `1.000000000000325` |
| Stored Wa lower | `1.000000000000325` |
| Stored Wa upper | `1.0` |
| Stored Wa width | `-3.2507330161024584e-13` |
| Original kernel and v0.12 result | `APPLIED` |
| Original post-state validator | `[]` |
| Replay through v0.12 | `REPLAYED`, retaining the inverted interval |

The cause is a composition of existing local rules:

1. `validate_wa_weights` accepts an absolute weight-sum discrepancy up to
   `1e-9`, without renormalizing the weights.
2. `_evaluate_profile` accepts its pre-clipped upper bound up to `1+1e-12`.
3. It then clips only the upper endpoint to 1 and calculates width from that
   clipped endpoint and the unchanged lower endpoint.
4. `validate_wa_state` does not recheck the numeric schema of every stored
   profile or derived interval.

The v0.13 gate rejects this result before the calling Wa store appends that
event or updates its snapshot. It also refuses an already-invalid numeric
pre-state, including an attempted replay. It does not repair, clip, replace,
or silently renormalize the original numeric values.

## Added runtime contract

`runtime/kuuos_lean_python_wa_numeric_guard_v0_13.py` exports
`checked_apply_wa_numeric_event(state, event)` and
`WaNumericBoundaryError(status, issues)`.

The adapter makes defensive bounded finite built-in JSON copies, checks the
pre-state numbers, calls the v0.12 pure mediator adapter once for
`DecisionOSWa`, and checks the resulting state's numbers. The inherited
adapter still performs the original kernel call and the structural,
digest, history, source, and authority checks. Native successful result
values are returned unchanged. Native `REJECTED` diagnostics remain
rejections; a malformed numeric pre-state cannot bypass the boundary by
requesting a rejected or replayed event.

| Data | Added conditions |
| --- | --- |
| Known seven weights and five thresholds | Exact built-in `int`/`float`, excluding bool and numeric strings; finite; between 0 and 1 |
| Each profile's positive and alert axes | Known seven axes in each map; finite numeric endpoints; `0 ≤ lower ≤ upper ≤ 1` |
| Each derived record's five intervals | Weighted, weakest, relational, alert, and Wa intervals all satisfy the same strict endpoint conditions |
| Wa width | Finite numeric value, nonnegative, and equal to the original Python `upper - lower` operation on those stored endpoints |
| False-harmony alert interval | Numerically valid and equal to the corresponding Wa record's alert interval |
| Successful profile event payload | Raw numeric values satisfy the added schema before accepting the successful normalized result; this also applies to successful replay |

There is no epsilon in the endpoint range/order checks and no `isclose`
substitute. Missing required numeric prerequisites remain `NO_DATA`;
malformed or violated conditions are `BLOCKED`.

The original weight-sum tolerance is retained. In particular, this gate
does **not** require that the exact binary rational values of all seven
weights sum to exactly 1. For the ordinary native fixture, Python's sum is
`1.0`, but the sum of those represented rational values is
`1 + 1/36028797018963968`. Requiring exact rational equality would reject
the unchanged normal fixture and would be a different contract.

Width is checked against the native Python subtraction, not against an
unrounded real-number difference. For example, a normal native evaluation
can produce lower `0.1`, upper `0.9000000000000001`, and width
`0.8000000000000002`. The width equals Python's subtraction even though its
exact rational value differs from the exact rational endpoint difference.
Both distinctions have positive regression cases.

## Relation to the retained Lean model

The unchanged `formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean` defines
`UnitInterval` with real-number hypotheses `0 ≤ lower ≤ upper ≤ 1`, and
`ConvexWeight` with `0 ≤ beta ≤ 1`. Its `relationalInterval` and `waInterval`
constructions prove preservation of those bounds under the stated real
arithmetic hypotheses. The weighted, weakest, relational, and alert inputs
are already `UnitInterval` values in those statements.

The new Python boundary checks corresponding inequalities for the finite
numbers actually represented in the selected native packets. The relation
between these runtime checks and the Lean model is an explicit design
correspondence; no Lean/Python refinement theorem is added. The Lean file
does not prove the Python seven-weight summation, floating-point rounding,
the original clipping operation, or a Python `width` field.

Python documents that a finite float can be represented by its exact
integer ratio, and that a `Fraction` constructed from a float preserves
that represented value rather than its intended decimal spelling:
[floating-point representation](https://docs.python.org/3.12/tutorial/floatingpoint.html)
and [Fraction](https://docs.python.org/3.12/library/fractions.html).
Using this representation for range/order checks does not recover a lost
decimal input or prove the full numeric evaluator.

## Native child and preservation of prior evidence

`runtime/kuuos_lean_python_wa_numeric_native_cycle_v0_13.py` exports
`build_wa_numeric_native_fixture(root)` and the inherited read-only
`audit_local_evidence(root)` behavior.

The builder requires an empty existing trusted root, runs source preflight,
and launches an explicit fresh Python child. Only the v0.12 native module's
imported `checked_apply_mediator_event` binding is temporarily wrapped.
Wa calls use the new numeric adapter; Plural calls keep the original v0.12
structural adapter. The original store and kernel functions remain intact,
so the existing original-binding checks continue to apply.

All eight previously checked state routes remain present, and the selected
Act pre-host input gate must still complete once. The new numeric counter
must equal the inherited Wa state-check counter exactly. Counts include
recovery replays. The new report nests the actual unchanged v0.12 report;
the parent revalidates it against an independent read-only evidence audit.
It also checks the new report identity, numeric coverage, and narrow-scope
flags. This is unsigned local stdout observation, not historical attestation.

The persisted v0.9 write-once record keeps the same format. The later audit
does not execute the new numeric gate or establish that past Wa numerics
passed it. Initialization and every store write are not newly guarded.
Failure never retries or deletes partial output; an existing root is not
overwritten. These assumptions cover a trusted, quiescent checkout/root,
not concurrent hostile filesystem changes or an OS sandbox.

## Source checks and ordinary CI discovery

All additions are in seven new files. The fixed v0.12 extension loader
already discovers `test_*.py` in `tests/lean_python_extensions`; the original
v0.4 native test entrypoint therefore also discovers the three v0.13 test
modules without changing the runner, loader, registration hook, or old tests.

The new source checker retains the prior 66 selected source pins and adds
the eight v0.12 files, current v0.4 registration module, and original Belief
numeric helper types: **76 selected direct baseline blobs**. When this
checker is executed, it requires all seven new files and ordinary test
declarations in the three new test classes. Its AST inventory is a declared
test list for comparison with actual CI execution; it does not execute tests
or establish that an arbitrary declaration cannot skip itself.

The unchanged older loader requires its three v0.12 modules. It cannot
independently guarantee failure if every v0.13 test file is removed in a
later changed tree. Acceptance of this version therefore also requires the
submitted Git tree/file inventory and actual CI test IDs/counts to agree.
No universal future test-deletion guarantee is claimed. Pins cover selected
source bytes, not the complete transitive import graph or arbitrary test code.

From the repository root:

```sh
python3 scripts/check_kuuos_lean_python_wa_numeric_sources_v0_13.py
python3 scripts/check_kuuos_lean_python_mediator_sources_v0_12.py
python3 -m unittest tests.test_kuuos_lean_python_plan_act_native_v0_4 -v
python3 -m unittest tests.test_kuuos_lean_python_os_registry_v0_5 -v
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
```

The real-store regression preserves a successfully stored profile, attempts
the known inverted evaluate event through the new boundary, and verifies
that the ledger and snapshot remain unchanged after rejection. A separate
case checks refusal of replay on an already-invalid numeric state. Real
child tests verify process isolation, all prior gates, exact numeric coverage,
binding restoration, original evidence format, and read-only audit behavior.
Exact independent CI results and counts are recorded in the PR after the
runs finish, not assumed in advance here.

## Explicitly unverified after a successful numeric check

A result may satisfy the numeric schema while still containing an incorrect
in-range value. This extension does not independently recompute all scores,
establish weighted/relational/Wa evaluation equivalence, prove threshold or
route-selection semantics, or prove comparative monotonicity across runs.
The seven-weight exact-real normalization and full Lean/Python refinement
remain unverified. It also grants no external issuer authentication,
source-history authenticity, new execution/truth/Git authority, all-OS
certificate, host rollback, or host/store atomicity.

Strict Lean may be skipped for this Python-only change; a skip is not a new
proof. Existing Lean declarations and their original assumptions remain
unchanged, and protected validation-only PR #1558 remains separate.
