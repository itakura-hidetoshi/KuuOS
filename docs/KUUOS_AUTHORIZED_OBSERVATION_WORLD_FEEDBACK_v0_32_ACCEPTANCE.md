# v0.32 Acceptance Matrix

| Case | Expected result |
|---|---|
| Ready v0.31 observation candidate with exact finite authorization | Single-use ObserveOS request is materialized |
| Authorization not yet valid or expired | Request construction is rejected |
| Capability-discovery or non-ready report | Authorization is rejected |
| Report/candidate/channel/tool/root mismatch | Exact-binding rejection |
| Exact request replay | No second request-ledger append |
| Same authorization reused for a different request | Rejected |
| Evidence collected inside authorization window | Provenance-complete receipt is accepted |
| Evidence collection reaches or exceeds expiry | Rejected |
| Same request reused for different evidence | Rejected |
| `SUPPORTS` | WORLD update candidate; no truth or mission-completion authority |
| `CONTRADICTS` | Contradicted update candidate; counterevidence and uncertainty preserved |
| `INCONCLUSIVE` | `REOBSERVE` route |
| `CONFLICTED` | `REOBSERVE` route |
| Report/evidence lineage mismatch or tampering | Rejected |
| Same evidence reused for different WORLD feedback | Rejected |
| Every evidence relation | Verification debt remains open |
