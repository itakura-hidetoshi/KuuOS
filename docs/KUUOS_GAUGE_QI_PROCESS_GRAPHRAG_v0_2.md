# KuuOS Gauge–Qi Process GraphRAG v0.2

Gauge–Qi Process GraphRAG v0.2 makes the v0.1 query-specific evidence evaluation restart-safe and explicitly connects it to BeliefOS and the v0.21 Mission Cycle without allowing an evidence receipt to become belief, decision, or execution authority.

```text
persistent evidence != persistent global context graph
evidence ledger != belief authority
GraphRAG CANDIDATE != committed belief
BeliefOS commit != decision commit
Replan adoption != execution permission
snapshot != ledger authority
replay != duplicate evidence event
repair != history rewrite
```

## 1. Position

```text
Gauge–Qi Process GraphRAG v0.1
  finite patches + declared paths + declared cycles
  gauge transport + Qi-history-conditioned evaluation
        ↓
Gauge–Qi Process GraphRAG v0.2
  append-only query evidence ledger
  restart recovery and idempotent replay
  evidence / holonomy / observation-debt chains
        ↓
BeliefOS evidence packet
  candidate input for contextualize / trace / weigh / challenge
        ↓
BeliefOS COMMIT
        ↓
v0.21 Replan-only adoption receipt
        ↓
next Plan evidence basis
```

v0.2 preserves the fixed KuuOS separation:

```text
memory is not belief authority
belief release is not decision commit
plan success is not execution permission
DecisionOS remains the action-boundary owner
```

## 2. Persistent query lineage

A v0.2 store belongs to one declared `lineage_id` and one `query_id`. It does not become a corpus-wide graph. Every accepted event stores one complete v0.1 evidence bundle and one evaluated receipt.

Persistent state records:

- event and run counts;
- processed bundle digests;
- latest v0.1 and v0.2 receipt digests;
- latest advisory route;
- an evidence-chain digest;
- a holonomy-chain digest;
- an observation-debt-chain digest;
- compact receipt history;
- predecessor and current state digests;
- unchanged non-authority boundaries.

A bundle from another query is rejected. A previously committed bundle is replayed idempotently without a second ledger append.

## 3. Durable store

```text
graph-rag-genesis.json
graph-rag-ledger.jsonl
graph-rag-snapshot.json
.graph-rag.lock
```

`graph-rag-ledger.jsonl` is append-only authority. `graph-rag-snapshot.json` is a derived cache. Every commit binds:

- predecessor commit digest;
- predecessor GraphRAG-state digest;
- the full source bundle;
- persistent receipt digest;
- result-state digest;
- commit digest.

Recovery re-evaluates every committed bundle with the v0.1 kernel. A malformed line, broken digest, query mismatch, stale predecessor, changed evaluation result, or state-chain mismatch fails closed. Snapshot repair is allowed only from verified genesis plus ledger.

## 4. Three history chains

### Evidence chain

The evidence chain commits the ordered sequence of persistent receipts and routes.

```text
E_(n+1) = H(E_n, receipt_n, route_n, source_bundle_n)
```

It proves ordering and lineage, not truth.

### Holonomy chain

The holonomy chain commits the visible cycle diagnostics and admissible paths.

```text
H_(n+1) = H(H_n, cycle_results_n, admissible_paths_n)
```

It preserves path dependence without granting curvature veto authority.

### Observation-debt chain

The observation-debt chain commits the next-observation target, maximum path action, and minimum evidence sufficiency.

```text
D_(n+1) = H(D_n, next_observation_target_n,
            max_path_action_n, minimum_evidence_sufficiency_n)
```

Debt is not punishment and is not a hidden scalar. It identifies unresolved observation work for later Observe / Verify phases.

## 5. BeliefOS evidence packet

The latest persistent receipt can be exported as a `belief_evidence_packet`. The packet includes:

- GraphRAG state and receipt digests;
- query lineage;
- current route;
- evidence, holonomy, and observation-debt chain digests;
- next-observation target;
- whether the packet is a candidate for BeliefOS weighing;
- `belief_authority_granted = false`;
- `truth_authority_granted = false`;
- `future_only = true`;
- `memory_overwrite = false`.

The packet is input evidence. BeliefOS must independently contextualize, trace, weigh, challenge, Qi-condition, apply Two Truths, pass the Middle Way gate, and commit.

## 6. Replan-only adoption

A GraphRAG lineage may enter a next-plan evidence basis only when all of the following are explicit:

```text
latest GraphRAG route = CANDIDATE
BeliefOS route = CANDIDATE
BeliefOS state digest present
BeliefOS commit receipt digest present
mission cycle phase = replan
mission cycle state digest present
replan receipt digest present
next plan basis digest present
future_only = true
memory_overwrite = false
```

The adoption receipt still records:

```text
decision_commit_granted = false
execution_authority_granted = false
clinical_authority_granted = false
theorem_authority_granted = false
```

Thus GraphRAG cannot bypass BeliefOS, and BeliefOS cannot bypass Replan or DecisionOS.

## 7. Restart semantics

On restart, recovery performs:

```text
genesis
  -> verify ledger commit 1
  -> replay v0.1 evaluation
  -> verify receipt and state digests
  -> ...
  -> verify final derived snapshot
```

A stale or corrupted snapshot does not become authority. It may be replaced only by the exact verified recovered state.

## 8. Mission Cycle mapping

```text
Plan
  declares finite retrieval/evidence paths
Act
  performs only separately licensed retrieval effects
Observe
  commits a v0.2 evidence event
Verify
  checks provenance, gauge covariance, holonomy, and chain integrity
Learn
  creates a future-only BeliefOS evidence packet
Replan
  may adopt only a BeliefOS-committed CANDIDATE basis
```

No phase is skipped. The v0.2 store does not itself perform retrieval, network access, shell access, clinical action, or decision commit.

## 9. Formal surface

`formal/KUOS/GraphRAG/GaugeQiProcessGraphRAGV0_2.lean` proves:

- every accepted persistent transition appends exactly one event;
- retained history cannot exceed committed history;
- ledger recovery and snapshot counts agree;
- evidence, holonomy, and debt histories are append-only;
- a BeliefOS evidence packet grants neither belief nor truth authority;
- accepted Replan adoption requires both GraphRAG and BeliefOS CANDIDATE states;
- accepted adoption requires Replan;
- adoption grants neither decision nor execution authority;
- learning remains future-only and non-overwriting.

## 10. Validation

```bash
python -m runtime.v02_gauge_qi_process_graphrag
python scripts/check_gauge_qi_process_graphrag_v0_2.py
```

The validation covers:

- persistent application and exact restart recovery;
- idempotent replay without duplicate ledger append;
- snapshot mismatch fail-closed and ledger-derived repair;
- query-lineage mismatch rejection;
- BeliefOS evidence packet non-authority;
- Replan-only adoption;
- rejection of non-CANDIDATE GraphRAG or BeliefOS routes;
- ledger digest corruption fail-closed.

## 11. Public boundary

v0.2 is a structural, evidence-memory, governance, and proof-facing layer. It is not a production retrieval service, global knowledge graph, autonomous web crawler, belief authority, decision authority, clinical decision system, theorem authority, treatment authorization system, or unrestricted execution engine.
