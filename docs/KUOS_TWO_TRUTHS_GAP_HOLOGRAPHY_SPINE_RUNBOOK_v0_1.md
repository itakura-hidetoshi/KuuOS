# KuuOS Two-Truth Gap-Holography Spine Runbook v0.1

Status: **baseline runbook / append-only**

This runbook explains how to review and validate the KuuOS Two-Truth Gap-Holography Spine v0.1.

The validator checks repository-surface consistency. A **PASS is a consistency receipt**, not theorem authority, truth authority, execution authority, medical authority, institutional authority, or ultimate-exhaustion authority.

---

## 1. Scope

This runbook covers:

```text
docs/KUOS_TWO_TRUTHS_GAP_HOLOGRAPHY_SPINE_v0_1.md
specs/kuos_two_truths_gap_holography_spine_v0_1.yaml
lean/KSTHolo/TwoTruthGapHolographySpine_v0_1.lean
manifests/kuos_two_truths_gap_holography_spine_manifest_v0_1.json
validation_cases/kuos_two_truths_gap_holography_spine_validation_cases_v0_1.yaml
chain_indexes/kuos_two_truths_gap_holography_spine_chain_index_v0_1.yaml
validators/validate_kuos_two_truths_gap_holography_spine_v0_1.py
```

---

## 2. Core invariant under review

The spine fixes this KuuOS baseline:

```text
positive gap
+ positive visible spectral weight
+ gap holonomy zero
=> unique non-vacuous stable conventional record
=> scoped prediction sufficiency
!= ultimate exhaustion
```

Japanese baseline:

```text
gap から記録へ
記録から安定へ
安定から予測へ
ただし予測から勝義尽尽へは進ませない
```

---

## 3. Run the validator

From the repository root:

```bash
python3 validators/validate_kuos_two_truths_gap_holography_spine_v0_1.py
```

Expected output:

```text
PASS: KuuOS Two-Truth Gap-Holography Spine v0.1 validation succeeded
NOTE: PASS is a consistency receipt, not truth/theorem/execution/ultimate-exhaustion authority.
```

---

## 4. What the validator checks

The validator checks that required files exist and contain the required baseline surfaces:

```text
canonical sentence
positive gap / visible weight / non-vacuous record chain
scaled correlation limit as record coefficient
image non-vacuity != kernel collapse
gap holonomy zero -> gap-visible stability
prediction sufficiency != ultimate exhaustion
append-only / overwrite-forbidden update policy
```

It also checks that the Lean-facing spine does not contain placeholder proof markers:

```text
sorry
admit
False.elim
```

---

## 5. What a PASS does not mean

A validator PASS does not mean:

```text
truth authority
theorem authority
ultimate-exhaustion authority
kernel-zero authority
ultimate-identity authority
full-flatness authority
execution authority
medical authority
institutional authority
```

It only means:

```text
The repository surfaces for this baseline spine are present and internally aligned.
```

---

## 6. Reviewer checklist

Reviewers should confirm:

- The documentation states that stable conventional prediction does not imply ultimate exhaustion.
- The YAML spec lists forbidden claims: kernel_zero, ultimate_identity, ultimate_exhaustion, residue_erasure.
- The manifest is append-only and overwrite-forbidden.
- The Lean spine exposes `fullAnalyticGap_theorem_local` as a safe functor-local theorem spine.
- The validation cases include both PASS and FAIL scenarios.
- The validator uses only standard Python library dependencies.

---

## 7. Update policy

Future changes must be:

```text
append-only
tighten-only by default
same-root required
destructive replacement forbidden
overwrite forbidden
```

Any update that weakens the no-kernel-collapse, no-ultimate-identity, no-ultimate-exhaustion, or no-residue-erasure guardrails must fail review.
