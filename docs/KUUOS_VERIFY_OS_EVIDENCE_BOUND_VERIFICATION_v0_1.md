# KuuOS VerifyOS Evidence-Bound Verification v0.1

VerifyOS v0.1 converts a committed ObserveOS evidence record into an auditable operational verification verdict. It verifies satisfaction of an explicit criterion under bounded evidence, challenge, independence, and reproducibility conditions. It does not establish absolute truth, unrestricted causality, clinical certainty, legal fact, theorem proof, or execution authority.

```text
committed ObserveOS record
  + exact ActOS verification criterion digest
  + immutable evidence packet
  + provenance and quality reports
  + explicit falsification attempts
  + counterevidence preservation
  + independent assessor receipts
  + corroboration assessment
        ↓
VerifyOS v0.1
        ↓
VERIFICATION_PASSED
VERIFICATION_FAILED
VERIFICATION_INDETERMINATE
```

## 1. Boundary

```text
verification != absolute truth
criterion satisfied != ontology proven
criterion failed != complete causal explanation
falsifier triggered != unrestricted causal attribution
passed != plan completed
failed != automatic rollback
indeterminate != evidence deletion
```

VerifyOS judges only whether a declared verification criterion is satisfied by the bound evidence under the declared verification method and challenge surface.

## 2. Strict phases

```text
BIND
  ↓
CRITERION
  ↓
CHALLENGE
  ↓
CORROBORATE
  ↓
ADJUDICATE
  ↓
COMMIT
```

Phase skipping, stale-state application, digest substitution, criterion substitution, evidence substitution, assessor identity collision, missing falsification attempts, counterevidence erasure, unsupported conclusiveness, and authority escalation are rejected.

## 3. Source binding

VerifyOS accepts only a committed ObserveOS state satisfying:

```text
current_phase = commit
route != PENDING
observation_recorded = true
verification_required = true
comparison receipt canonical
source effect identity preserved
```

It binds the exact:

- ObserveOS state digest;
- source ActOS state digest;
- host receipt and invocation digests;
- evidence packet digest;
- provenance and quality digests;
- comparison receipt digest;
- expected observation digest;
- ActOS verification criterion digest.

## 4. Criterion packet

The criterion packet declares:

```text
verification_criterion_digest
criterion_type
evaluation_method_digest
success_condition_digest
failure_condition_digest
falsification_condition_digest
evidence_requirements_digest
minimum_independent_assessors
permits_causal_attribution = false
```

The criterion digest must exactly equal the digest inherited through ActOS and ObserveOS. CRITERION cannot redefine the verification target after observing the evidence.

## 5. Challenge packet

CHALLENGE requires:

```text
counterevidence_digests
falsification_attempt_digests
independent_assessor_ids
assessor_receipt_digests
conflict_disclosure_digest
falsifier_triggered
challenge_complete = true
counterevidence_preserved = true
```

At least one explicit falsification attempt is required. The declared minimum number of independent assessors must be visible, and assessor IDs must be unique. Counterevidence may be empty only when the packet explicitly preserves the empty set rather than omitting the field.

## 6. Corroboration

The corroboration report records bounded scores for:

```text
evidence_sufficiency
assessor_independence
provenance_integrity
method_reproducibility
criterion_coverage
```

It also records `unresolved_conflict` and a method digest. A conclusive verdict requires:

- a directional ObserveOS result (`MATCHED` or `DIVERGENT`);
- discharged observation debt;
- no unresolved reobservation debt;
- sufficient evidence;
- sufficient independent assessment;
- preserved provenance;
- adequate reproducibility;
- adequate criterion coverage;
- no unresolved conflict.

## 7. Adjudication

Allowed verdicts:

- `PASSED`
- `FAILED`
- `INDETERMINATE`

### PASSED

Requires:

```text
source observation = MATCHED
corroboration admissible = true
criterion_satisfied = true
falsifier_triggered = false
```

### FAILED

Requires conclusive corroboration and at least one of:

```text
source observation = DIVERGENT
criterion_satisfied = false
falsifier_triggered = true
```

### INDETERMINATE

Requires a non-admissible corroboration surface, including insufficient evidence, unresolved conflict, non-directional observation, or open reobservation debt.

## 8. Debt semantics

### PASSED

```text
verification_recorded = true
verification_debt_discharged = true
verification_required = false
reobservation_required = false
corrective_action_required = false
learning_required = true
```

### FAILED

```text
verification_recorded = true
verification_debt_discharged = true
verification_required = false
reobservation_required = false
corrective_action_required = true
learning_required = true
```

### INDETERMINATE

```text
verification_recorded = true
verification_debt_discharged = false
verification_required = true
reobservation_required = true
corrective_action_required = false
learning_required = true
```

All routes preserve:

```text
automatic_truth_promotion = false
automatic_belief_update = false
automatic_plan_completion = false
automatic_rollback = false
automatic_causal_attribution = false
```

## 9. Mission Cycle adapter

VerifyOS emits a Verify-phase receipt for the fixed v0.21 Mission Cycle:

```text
Mission → Plan → Act → Observe → Verify → Learn → Replan
```

The receipt contains:

```text
mission_cycle_phase = verify
verdict = passed | failed | indeterminate
verification_evidence_digest
verification_not_truth = true
causal_attribution_not_granted = true
learning_required = true
```

## 10. Persistence

```text
verify-genesis.json
verify-ledger.jsonl
verify-snapshot.json
.verify-os.lock
```

The ledger is append-only authority. The snapshot is derived and repairable. The store provides exclusive writer locking, digest chains, fsync, atomic snapshot replacement, exact event replay idempotence, restart reconstruction, corruption detection, and ledger-derived snapshot repair.

## 11. Formal surface

The Lean surface proves:

- strict phase progression and event-index growth;
- exact ObserveOS and criterion binding;
- challenge requires falsification and independent assessment;
- counterevidence preservation;
- PASSED requires criterion satisfaction and no triggered falsifier;
- FAILED requires criterion failure, divergence, or triggered falsifier;
- INDETERMINATE preserves verification and reobservation debt;
- verification never grants truth or causal authority;
- no route grants execution, final, clinical, legal, institutional, theorem, or memory-overwrite authority;
- append-only recovery count equals committed VerifyOS record count.

## 12. Public boundary

VerifyOS v0.1 is an operational evidence-adjudication kernel. It is not a substitute for domain-specific scientific validation, clinical diagnostic standards, legal fact finding, institutional authorization, safety certification, or theorem proving.
