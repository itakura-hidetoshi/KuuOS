# Lean → Python v0.14: Wa classification, plurality and gate boundary

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Baseline and accepted scope

Canonical repository: itakura-hidetoshi/KuuOS, main.

This additive extension starts from main
`05693ef17179ebddb974f23021be2e7d352b4fbb`
(v0.13, PR #3574). Its baseline Git tree is
`1e03355070ae99539c29eee3faeafb9e28df0db5`.

v0.13 checks finite, ordered unit intervals and native endpoint width
consistency. It does not establish that the derived intervals were computed
correctly from the original profiles. v0.14 retains that limitation and checks
how the supplied local scores, profiles, source projection and thresholds
determine false-harmony classification, plurality and the final route.

The new pure entrypoint is:

```python
checked_apply_wa_gate_event(state, event) -> dict
WaGateBoundaryError(status, issues)
```

It calls the unchanged v0.13 numeric adapter once, which retains the v0.12
structural adapter and one original native kernel call. The state and event are
copied as bounded finite built-in JSON. The original result is returned only
when both the supplied and resulting state satisfy the added local conditions.
No score, profile, classification, route or digest is repaired or resealed.

## Concrete gaps in the prior boundary

These are coherently modified local states/results, not a claim that the
unchanged native classifier normally erases its own output.

1. A genuine profile with minority preservation False normally produces
   confirmed false harmony and an ESCALATE route. Replacing the classification
   with confirmed=False, suspected=False and an empty reason list, then
   coherently resealing the result, passes v0.13. From that invalid state the
   original plurality and gate functions can produce ENDORSE.
2. A genuine profile with dissent consideration False normally leads to
   suspected false harmony and REOBSERVE. Erasing its classification in the
   same way can also lead to ENDORSE under the original later kernel calls.
3. A genuine gate with Wa lower `0.18000000000000002` below floor
   `0.55` and weakest lower `0.2` below floor `0.4` normally
   selects REPAIR. A coherently resealed ENDORSE state, including the original
   basis projection, can pass a genuine old-event replay under v0.13 and then
   pass the original commit.
4. Existing strict Boolean validation checks the type of plurality flags but
   does not reconstruct them from the actual local sets and digest fields.

v0.14 rejects these inconsistencies. It checks current pre-state conditions even
when the incoming event is a replay or will be natively rejected; an already
inconsistent state does not gain acceptance by using a non-writing event.

## Relationship to the retained Lean artifact

The primary formal source is
[WaRelationalHarmonyV0_3.lean](../formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean).
Its statements and proofs are unchanged.

| Retained formal structure | Original hypotheses / conclusions | Added runtime connection |
| --- | --- | --- |
| UnitInterval and ConvexWeight | Real-number interval and weight hypotheses | Retain v0.13's checks on represented numeric fields; no real/float refinement is asserted |
| WaEndorsementGate | confirmed=False, minority=True, dissent=True, Wa/weakest floors passed, source identity preserved | Reconstruct local classification and gate choice from stored records, thresholds and source option identity before accepting ENDORSE |
| endorsedWa_has_no_confirmed_false_harmony | Projection of confirmedForbidden | A confirmed local classification must not be bypassed by an ENDORSE route |
| endorsedWa_preserves_minority / endorsedWa_considers_dissent | Projections of required profile flags | Classification remains bound to the actual local profile flags |
| endorsedWa_preserves_plural_selected_identity | Projection of identityRequired | Endorsement targets exactly the supplied selected source option |
| WaPluralityBoundary | Count, retained bound, stakeholder/history Boolean and no-substitution hypotheses | Reconstruct source/profile set conditions and the original digest-presence flags |

The Lean gate theorems are projections from structures whose conditions have
already been supplied. They do not prove the native classifier or floating-point
evaluator correct. The names "Wa", "harmony" and their philosophical
interpretation are not extra conclusions of these proofs.

The original Python gate also refuses endorsement on suspected false harmony.
That stronger native condition remains in force even though
WaEndorsementGate does not itself require suspected=False.

No new Lean file, declaration, axiom, proof or formal acceptance is added.
A Python/docs-only Strict Lean skip must not be reported as a new proof.

## Classification and plurality checks

Classification is checked for every profiled option once the current phase
reaches false_harmony_check. The original ordering and exact reason list are
retained:

- alert lower >= confirmed threshold adds confirmed_alert_floor_reached;
- minority_preserved=False adds minority_not_preserved and confirms the case;
- only if unconfirmed, alert upper >= suspected threshold adds suspicion;
- only if unconfirmed, dissent_considered=False adds dissent_not_considered.

Confirmed cases retain suspected=False. Profiles determine the row order;
source option order need not be the same as profile order. The copied alert
interval and profile Boolean fields remain bound to their corresponding records.

At and after plurality_check, the guard reconstructs all_source_options_profiled,
retained_alternatives_preserved and selected_identity_preserved from the local
source/profile option sets. Stakeholder and veto/appeal flags retain the original
nonempty-digest conditions. The original silent_substitution_detected=False
condition is retained.

Matching those presence flags does not authenticate the contents represented by
the digests. Matching source/profile IDs does not attest an external source state.

Before each generating phase, derived fields must retain their original initial
values: no premature classification, plurality result or endorsement is accepted.

## Gate priority and field binding

The original branch priority is retained:

1. An invalid plurality gate selects QUARANTINE.
2. Direct source routes use the original mapping below.
3. For CONSENSUS_CANDIDATE, missing selected records quarantine; confirmed false
   harmony escalates, suspicion reobserves, either missed floor repairs, and only
   the remaining case endorses.

| Source route | Direct Wa route |
| --- | --- |
| NEGOTIATE / APPEAL | REOBSERVE |
| HANDOVER | ESCALATE |
| HOLD / REJECT / QUARANTINE | Same named route |

Direct routes keep the original retained-alternative order in review_option_ids.
The selected consensus branches preserve exactly the selected option identity.

Alert comparisons use >=; a floor fails only on <. Equality at a floor therefore
passes. No epsilon, threshold correction or value normalization is added.
pending_replan_activation is False only for REJECT and QUARANTINE; native HOLD
still has pending=True.

The route, endorsed/review lists, pending flag and wa_basis_digest are checked
together. The basis uses exactly the original 18-field projection; adding weights,
thresholds or wa_gate_rule_digest to that projection would change native semantics.
Successful gate events also retain the native requested_route constraint
(None, empty string or the calculated route).

These are bindings to supplied local state, not a new license to execute or an
assertion that the chosen option is objectively correct.

## Native subprocess and evidence composition

[The native wrapper](../runtime/kuuos_lean_python_wa_gate_native_cycle_v0_14.py)
runs the explicit fixture in a fresh Python process. It temporarily wraps only
the numeric-adapter binding imported by the v0.13 native module. The new pure
module independently holds the original v0.13 numeric adapter, so the composition
does not recurse or replace original kernel/store bindings.

The child retains the existing eight guarded routes: DecisionOS,
DecisionOSPlural, DecisionOSWa, PlanOS, ActOS, ObserveOS, VerifyOS and LearnOS,
plus the inherited selected Act check before its host call.

The actual v0.13 child report is nested unchanged and validated with its original
validator. The new exact positive integer gate count must equal the inherited
numeric count, which already equals the Wa state-guard count. Counts include
recovery replays and successful guarded returns; a blocked attempt does not
increment the success counter.

The original v0.9 write-once record inventory and read-only audit are unchanged.
The trusted empty-root requirement, binding restoration, parent-patch isolation,
single child invocation and retained partial output on failure remain in force.
There is no automatic retry or overwrite.

The later audit does not rerun these conditions or prove historical execution.
Child stdout counters are unsigned local observations. Store initialization and
every possible store write are not newly guarded. Host rollback, host/store
atomicity, all-effects prevention and a security sandbox are not supplied.

## Source preservation and test acceptance

The new source checker pins 83 prerequisite Git blobs: all 76 v0.13 pins plus
all seven files introduced in v0.13. It requires the seven v0.14 files and uses
AST to inspect the three ordinary test classes and directly declared methods.
It does not import or execute runtime or test modules.

The old extension loader and existing registration remain unchanged. New tests
are discovered by the existing test_*.py pattern. The new checker only enforces
its required inventory when called; the old loader does not unconditionally
detect a future deletion of every v0.14 test file.

Accordingly, acceptance also requires a complete non-truncated Git tree diff
and exact comparison of declared new test IDs with actual successful CI IDs.
AST declarations alone do not establish discovery, execution, inheritance,
decoration, rebinding or absence of skips.

Focused validation:

```sh
python3 -B scripts/check_kuuos_lean_python_wa_gate_sources_v0_14.py
python3 -B -m unittest tests.lean_python_extensions.test_wa_gate_guard_v0_14 tests.lean_python_extensions.test_wa_gate_native_cycle_v0_14 tests.lean_python_extensions.test_wa_gate_sources_v0_14 -v
```

Cumulative selected regression:

```sh
python3 -B -m unittest tests.test_kuuos_lean_python_contract_bridge_v0_1 tests.test_kuuos_lean_python_lineage_handoff_v0_2 tests.test_kuuos_lean_python_decision_plan_handoff_v0_3 tests.test_kuuos_lean_python_plan_act_admission_v0_4 tests.test_kuuos_lean_python_plan_act_checker_v0_4 tests.test_kuuos_lean_python_plan_act_native_v0_4 tests.test_kuuos_lean_python_os_registry_v0_5 -v
```

Real-store tests must demonstrate that inconsistent classification and forced
endorsement are refused before ledger/snapshot writes, while genuine native
replay and rejection preserve their original results and stored bytes.
Actual-child tests must establish all eight routes, inherited pre-host coverage
and exact numeric/gate counter equality.

CI success is recorded only after the relevant jobs finish. The PR record must
distinguish local tests, PR test-merge CI and postmerge main CI, with actual
checkout HEADs and source/test-merge/integration tree identity.

## Explicitly unverified

The weighted sum, weakest/alert reduction, relational blend and Wa score
derivation are not recomputed by this extension. In-range but incorrectly
derived scores can remain acceptable if all local classifications and routes
are consistent with them. Tests preserve this limitation as a positive example;
it must not be described as full evaluation equivalence.

Full numeric correctness, real-number/Python-float and Lean/Python refinement,
cross-run monotonicity, external issuer/source authenticity, historical guard
attestation, every store write, and new execution/truth/merge authority remain
unverified.

All earlier Lean theorem bodies/names, OS kernels/types/stores, adapters and
tests, native fixture, loader/registration and CI runner/workflows are retained.
Lean remains leanprover/lean4:v4.30.0-rc2 with mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Protected PR #1558 remains validation-only, Draft/Open/unmerged.

