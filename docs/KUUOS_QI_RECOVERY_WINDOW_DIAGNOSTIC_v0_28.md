# KuuOS Qi Recovery-Window Diagnostic Candidate v0.28

## Purpose

v0.28 adds a bounded diagnostic-candidate layer after v0.27 finite-cycle continuity.

```text
v0.27 state
+ Qi Process Tensor receipt
+ observation candidate
+ multi-time response history
+ plural hypotheses
→ candidate report
→ recovery-window interval
→ reobserve / preserve plurality / evaluate window / review handoff
```

The recovery-window interval is the runtime representation of healing potential. It is conditional evidence, not a guarantee.

## Separation rules

```text
diagnostic support != recovery-window potential
severity != irreversibility
positive response != guaranteed healing
negative response != permanent closure of future recovery
red flag != automatic action
```

Severity remains visible inside each hypothesis but is excluded from the recovery-window formula.

## Process history

Each history item binds:

- time index and observation identity
- recoverability and coherence margins
- transport distortion and tail residue
- memory gain
- bounded response delta
- adaptive stability
- intervention burden
- visible backaction and source trace

The current snapshot never replaces process history. At least three history points are required for a process-based classification stronger than `INSUFFICIENT_EVIDENCE`.

## Interval construction

Support combines recoverability, coherence, positive response history, stability, memory gain, low distortion, low residue, and trajectory reopening credit.

Burden combines intervention burden, distortion, residue, negative response history, and instability.

```text
center = clamp01(support_score - 0.35 * burden_score)
```

Interval width expands when history length, source coverage, temporal coverage, or contradiction visibility are limited.

## Classes

```text
INSUFFICIENT_EVIDENCE
HEALING_POTENTIAL_VISIBLE
HEALING_POTENTIAL_UNCERTAIN
HEALING_POTENTIAL_CONSTRAINED
CLINICIAN_REVIEW_REQUIRED
```

`HEALING_POTENTIAL_CONSTRAINED` describes the present evidence and does not establish irreversibility.

## Hypothesis plurality

Every candidate preserves support, counterevidence, uncertainty, severity, and source traces.

```text
leading candidate != truth
ranked first != final diagnosis
plural set remains visible
```

## Routes

```text
REOBSERVE
PRESERVE_PLURAL_HYPOTHESES
EVALUATE_RECOVERY_WINDOW
CLINICIAN_REVIEW_HANDOFF
HOLD
```

Routes are review surfaces. This kernel does not generate a treatment route.

## Persistence

```text
qi-diagnostic-candidate-ledger-v0-28.jsonl
```

The ledger is append-only. Duplicate reports replay idempotently. A second report for the same source packet is rejected.

## Formalization

```text
KUOS.OpenHorizon.QiHealingPotentialDiagnosticKernelV0_28
```

Key theorems:

```lean
plural_diagnostic_candidates_remain_nonfinal
healing_potential_preserves_open_future
red_flags_open_review_without_auto_triage
diagnostic_history_remains_append_only
v027_continuity_remains_bounded_under_diagnostic_projection
qi_healing_potential_diagnostic_boundary
```

## Validation

```bash
PYTHONPATH=. python scripts/check_qi_healing_potential_diagnostic_v0_28.py
PYTHONPATH=. python -m unittest -v tests.test_qi_process_diagnostic_v0_28
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.QiHealingPotentialDiagnosticKernelV0_28
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```
