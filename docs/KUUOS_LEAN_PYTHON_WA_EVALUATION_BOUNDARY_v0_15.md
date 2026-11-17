# Lean → Python v0.15 — independent local Wa float-score derivation

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Accepted baseline and scope

Canonical repository: itakura-hidetoshi/KuuOS, main.
Baseline: 69bd75f4ae14e912b45f520636ffd8a400067d36 (PR #3575).

v0.14 checked false-harmony classification, plurality and final gate conditions
against already supplied, bounded Wa scores. It deliberately did not
recompute scores. In its retained positive limitation test, changing an
in-range weighted interval and resealing the native state can still pass.
v0.15 closes that *local numerical derivation* gap by comparing the original
native Python evaluation against independently recomputed finite inputs.
The existing Lean proofs, all v0.1-v0.14 adapters, stores and CI are unchanged.

The new pure entrypoint is:

    checked_apply_wa_evaluation_event(state, event)

It first checks a copied pre-state, calls the original v0.14 gate adapter
exactly once using defensive copies, then checks the returned copied
post-state. The native result is returned unchanged only if it passes.

## Original computation and exact stored checks

The primary source is runtime/kuuos_decision_os_wa_kernel_v0_3.py,
specifically the original _evaluate_profile body. The new module never
calls that helper, but independently reproduces its Python-float semantics.

For the original ordered seven positive dimensions and seven alert dimensions:

    weighted_lower = sum(weight[i] * positive[i].lower)
    weighted_upper = sum(weight[i] * positive[i].upper)
    weakest_lower = min(positive[i].lower)
    weakest_upper = min(positive[i].upper)
    relational_lower = (1.0-beta)*weighted_lower + beta*weakest_lower
    relational_upper = (1.0-beta)*weighted_upper + beta*weakest_upper
    alert_lower = max(alert[j].lower)
    alert_upper = max(alert[j].upper)
    wa_lower = relational_lower * (1.0-alert_upper)
    wa_upper = relational_upper * (1.0-alert_lower)

All numeric values are cast to native Python float, and the original
generator and built-in sum/min/max order is preserved. The original validity
boundary is 0.0 <= wa_lower <= wa_upper <= 1.0+1e-12.
The *stored* upper is min(1.0,wa_upper), and stored width is
min(1.0,wa_upper)-wa_lower with native rounded subtraction.

At phase evaluate and later, every record must match all ten original
fields and the profile sequence order. No tolerance is added for a
one-ULP difference in an in-range derived interval. Before evaluate,
the previous v0.14 adapter enforces the absence of premature records.
All earlier v0.13 finite-unit, interval-order, width, and native weight
tolerance checks continue. No value, digest, classification or route is
changed or automatically resealed.

## Lean proof authority retained

The original formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean
defines real-valued UnitInterval, ConvexWeight, mixedLower and mixedUpper,
and proves inequalities under explicit hypotheses. Those formal statements
do not prove the native evaluator, Python float representation, or an
implementation-level refinement. Their philosophical naming layer is
interpretive, not a theorem. No Lean source is edited and a Python/docs
Strict Lean SKIPPED result is not a new formal proof.

## Native child and source protection

The new wrapper surrounds the unchanged v0.14 child, temporarily
replacing only its imported pure gate-adapter binding in a fresh Python
interpreter. The complete original eight-OS fixture, selected Act pre-host
check and v0.9 append-only evidence remain unchanged. An exact positive
integer evaluation counter must match the nested gate, numeric and Wa
state guard counters. Blocked attempts are not counted as successful.

The new static checker reuses v0.14's 83 retained source pins and adds
all seven v0.14 file blobs, for 90 prerequisite pins. It requires exactly
seven newly added files and AST direct test-method declarations. AST
declarations are not execution. Acceptance additionally requires the
actual new test IDs and outcomes from independent PR Runtime, exact
source / PR test-merge / integrated Git tree comparison, and postmerge
main Runtime + Governance. No old loader or CI is altered.

## Explicit remaining obstructions

This is local finite Python-float score derivation against supplied
normalized profiles, weights, and thresholds, **not** external source or
issuer authenticity. A coherently altered profile and rebuilt profile
digest may still pass if all computed scores are locally consistent.
Real-number/Python-float or Lean/Python refinement, global Wa truth,
historical guard execution, all store writes/initialization, all host
effects, host rollback, cross-run monotonicity and host/store atomicity
remain unverified. The fixed older loader does not guarantee future
automatic detection if every new test is removed; CI source/test-tree
inspection is necessary for this exact release.

CI success validates only the precise tested boundary. It grants no
truth, theorem, institutional, clinical, execution or Git merge authority.
Protected Draft/Open PR #1558 is excluded and remains unmerged.
