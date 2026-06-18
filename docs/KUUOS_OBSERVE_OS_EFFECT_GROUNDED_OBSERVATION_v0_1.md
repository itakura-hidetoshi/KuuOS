# KuuOS ObserveOS Effect-Grounded Observation v0.1

ObserveOS v0.1 converts the observation debt left by a committed ActOS effect record into a provenance-bound, append-only observation evidence record. It does not verify the effect, promote a belief to truth, complete a plan, or issue any new execution authority.

```text
committed ActOS EFFECT_RECORDED
  + canonical v0.17 host receipt
  + exact host invocation / selected step / operation
  + expected observation digest
  + explicit observation scope
  + raw evidence digests
  + collector and provenance chains
  + quality assessment
  + expectation comparison receipt
        ↓
ObserveOS v0.1
        ↓
OBSERVATION_MATCHED
OBSERVATION_DIVERGENT
OBSERVATION_INCONCLUSIVE
OBSERVATION_CONFLICTED
        ↓
verification_required = true
```

## 1. Boundary

```text
host receipt != observed real-world outcome
observation != verification
comparison class != truth verdict
MATCHED != effect proven true
DIVERGENT != causal attribution proven
INCONCLUSIVE != evidence deletion
CONFLICTED != forced collapse
```

ObserveOS records what was observed, how it was collected, how it is bound to the effect, and how it compares with the expected observation. VerifyOS or the Mission Cycle Verify phase remains responsible for any verification verdict.

## 2. Strict phases

```text
BIND
  ↓
SCOPE
  ↓
COLLECT
  ↓
TRACE
  ↓
ASSESS
  ↓
COMPARE
  ↓
COMMIT
```

Phase skipping, stale state, digest mismatch, time regression, effect substitution, target substitution, channel substitution, evidence identity collision, out-of-window evidence, incomplete provenance, quality report substitution, and comparison-receipt substitution are rejected.

## 3. Effect binding

ObserveOS accepts only a committed ActOS state satisfying:

```text
route = EFFECT_RECORDED
effect_recorded = true
observation_required = true
current_phase = commit
host receipt status = READY
host receipt digest canonical
host invocation digest present
selected act_candidate digest present
expected observation digest present
verification criterion digest present
```

The observation record binds the exact:

- ActOS state digest;
- ActOS committed record;
- host receipt digest;
- host invocation digest;
- selected PlanOS step digest;
- operation ID;
- expected observation digest;
- verification criterion digest.

## 4. Observation scope

The scope packet declares:

```text
observation_target_digest
observation_protocol_digest
window_start_ms
window_end_ms
channels
minimum_evidence_items
independence_required
observer_context_digest
baseline_digest
```

The target digest must equal the expected observation digest inherited from ActOS. The observation window is explicit and immutable after SCOPE.

## 5. Evidence item

Every evidence item contains:

```text
evidence_id
channel_id
source_kind
collector_id
independent_source_id
collected_at_ms
raw_artifact_digest
value_digest
uncertainty_digest
calibration_digest
context_digest
tamper_evidence_digest
provenance_hop_digests
```

ObserveOS stores digests and lineage, not an unrestricted interpretation of the raw artifact. Evidence outside the declared channels or time window is rejected. Duplicate evidence IDs are rejected.

## 6. Provenance trace

TRACE requires:

```text
evidence_chain_complete = true
source_identity_preserved = true
raw_artifacts_immutable = true
no_unbound_evidence = true
provenance_receipt_digest present
```

If independent evidence is required, the declared minimum number of independent sources must be visible before TRACE can complete.

## 7. Quality assessment

The quality report records bounded scores for:

```text
coverage
freshness
provenance
calibration
completeness
conflict
```

Quality assessment is advisory evidence metadata. It is not a truth authority. Low-quality evidence cannot be classified as MATCHED or DIVERGENT; it must remain INCONCLUSIVE or CONFLICTED.

## 8. Comparison receipt

The comparison receipt binds:

```text
expected observation digest
evidence packet digest
quality report digest
comparison method digest
comparison verdict
```

Allowed verdicts:

- `MATCHED`
- `DIVERGENT`
- `INCONCLUSIVE`
- `CONFLICTED`

The receipt classifies the evidence relative to an expected observation. It does not perform causal verification and does not discharge verification debt.

## 9. Debt semantics

### MATCHED / DIVERGENT

```text
observation_recorded = true
observation_debt_discharged = true
reobservation_required = false
verification_required = true
```

### INCONCLUSIVE / CONFLICTED

```text
observation_recorded = true
observation_debt_discharged = false
reobservation_required = true
verification_required = true
```

All routes preserve:

```text
automatic_truth_promotion = false
automatic_belief_update = false
automatic_plan_completion = false
automatic_causal_attribution = false
```

## 10. Mission Cycle adapter

ObserveOS emits an Observe-phase receipt suitable for the fixed v0.21 Mission Cycle:

```text
Mission → Plan → Act → Observe → Verify → Learn → Replan
```

The receipt states explicitly:

```text
mission_cycle_phase = observe
observation_not_verification = true
verification_debt_preserved = true
source_effect_identity_preserved = true
```

## 11. Persistence

```text
observe-genesis.json
observe-ledger.jsonl
observe-snapshot.json
.observe-os.lock
```

The ledger is append-only authority. The snapshot is derived and repairable. The store provides exclusive writer locking, digest chains, fsync, atomic snapshot replacement, exact event replay idempotence, restart reconstruction, corruption detection, and ledger-derived snapshot repair.

## 12. Formal surface

The Lean surface proves:

- strict phase progression and event-index growth;
- exact source-effect binding;
- observation target cannot replace the ActOS expected target;
- evidence requires collector, raw digest, time, uncertainty, calibration, and provenance;
- comparison is not verification;
- MATCHED does not imply truth;
- DIVERGENT does not imply causal attribution;
- INCONCLUSIVE and CONFLICTED preserve reobservation debt;
- all routes preserve verification debt;
- no execution, truth, clinical, legal, institutional, theorem, or memory-overwrite authority is granted;
- append-only recovery count equals committed ObserveOS record count.

## 13. Public boundary

ObserveOS v0.1 is an evidence-lineage and observation-audit kernel. It is not a clinical measurement standard, medical diagnosis, treatment authorization, legal finding, institutional decision, theorem proof, or unrestricted autonomous sensing authority.
