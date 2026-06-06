# Regge Zero Governance Runbook v0.1

Status: additive runbook  
Authority: non-authoritative governance support  
Parent: `docs/REGGE_ZERO_GOVERNANCE_v0_1.md`

---

## 1. Purpose

This runbook describes how to operate the Regge Zero Governance validation lane.

The lane enforces the following principle:

```text
consistency-mandated nulls only;
no extra blocker without witness;
no single-scalar authority collapse.
```

It is a governance check, not a physics proof, not an execution engine, and not a medical authorization layer.

---

## 2. Local Commands

Run the dedicated lane:

```bash
python3 validators/validate_regge_zero_governance_v0_1.py
python3 scripts/run_regge_zero_governance_checks_v0_1.py
make regge-zero-governance-checks
```

Run the lane through the full governance surface:

```bash
python3 scripts/run_all_governance_full_checks_v0_1.py
make all-governance-checks
```

---

## 3. Expected Pass Output

The direct validator should print:

```text
REGGE_ZERO_GOVERNANCE_VALIDATION: PASS
```

The runner should print:

```text
REGGE_ZERO_GOVERNANCE_CHECKS: PASS
```

---

## 4. Failure Classes

### 4.1 Missing authority boundary

A failure here means that one of the following non-authority locks was removed or weakened:

```text
candidate_not_authority
validation_not_truth
ci_pass_not_theorem_authority
runtime_tick_not_autonomous_execution_authority
qi_readout_not_intervention_license
memory_persistence_not_belief_sovereignty
reflection_summary_not_root_rewrite
audit_not_infinite_escalation
```

Repair: restore the lock. Do not replace it with a weaker prose statement.

### 4.2 Missing minimal-null invariant

A failure here means one of the core Regge-Zero governance invariants is missing:

```text
minimal_null_constraint_only
nested_null_inheritance
no_extra_blocker_without_witness
no_single_scalar_authority_collapse
cyclic_consistency_required_for_promotion
```

Repair: restore the invariant and ensure the validation cases still cover it.

### 4.3 Extra blocker without witness

A failure here means a soft concern such as novelty, complexity, unfamiliarity, or nonstandard framing was promoted into a blocker without a blocker witness.

Repair: downgrade the outcome to `ADVISORY_ONLY`, or add a legitimate witness such as boundary violation, provenance gap, authority shortcut, cyclic inconsistency, harm visibility gap, or runtime license failure.

### 4.4 Silent inherited-null erasure

A failure here means a lower-tier null condition was not preserved in a higher-tier validation or release surface.

Repair: carry the inherited null into the higher-tier receipt until explicitly repaired or superseded.

### 4.5 Single-scalar authority collapse

A failure here means a scalar score was treated as proof, belief, risk, Qi, plan, decision, runtime, or medical authority.

Repair: split the scalar into vector evidence, provenance, boundary, temporal validity, uncertainty, and module-specific witness.

---

## 5. CI Lane

The dedicated GitHub Actions workflow is:

```text
.github/workflows/regge_zero_governance_validation.yml
```

It runs:

```text
python3 scripts/run_regge_zero_governance_checks_v0_1.py
```

The full governance workflow also advertises this lane and the all-governance runner executes it.

---

## 6. Non-Claims

This runbook does not claim:

```text
KuuOS does not prove string theory.
KuuOS derives physical scattering amplitudes.
KuuOS creates autonomous execution authority.
KuuOS creates medical authorization.
KuuOS turns CI success into theorem authority.
KuuOS turns validation into truth.
```

---

## 7. Update Rule

Future updates are:

```text
append-only
same-root required
tighten-only default
overwrite forbidden
authority expansion forbidden
```
