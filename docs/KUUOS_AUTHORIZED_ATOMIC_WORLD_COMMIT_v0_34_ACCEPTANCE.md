# v0.34 Acceptance Matrix

| Case | Expected result |
|---|---|
| Exact v0.33 `ADOPT_CANDIDATE` plus matching authorization | Commit request is materialized |
| `REJECT_CANDIDATE`, `DEFER_CANDIDATE`, or `REOBSERVE_CANDIDATE` | Authorization construction is rejected |
| Local authorization is finite and single-use | Accepted |
| Any global cycle, generation, or time limit is introduced | Rejected as open-horizon shrinkage |
| Request time before not-before or at/after expiry | Rejected |
| Disposition, authorization, and request cannot be reconstructed exactly | Rejected before store mutation |
| Store identity or constitutional root lineage differs | Rejected |
| Current generation differs from expected generation | Rejected |
| Last receipt digest differs from expected prior receipt | Rejected |
| Current WORLD fragment differs from expected prior fragment | Rejected |
| Fencing token is not strictly newer | Rejected |
| Lease epoch is older | Rejected |
| New commit finishes at/after authorization expiry | Rejected |
| Exact replay of an already committed request after expiry | Existing receipt returned; no new generation |
| Same authorization used by a second distinct request | Rejected |
| Same disposition submitted under another authorization | Rejected |
| Successful commit | Current pointer advances once; receipt appended atomically |
| Two valid successive commits | Fragment and receipt chains remain exact and append-only |
| Receipt contains rollback reference | Accepted; rollback remains separately authorized |
| Automatic rollback or history deletion flag | Rejected |
| Constitutional root rewrite or memory-history overwrite flag | Rejected |
| Receipt or store body tampering | Envelope or chain validation fails |
| Temporary-file crash before replace | Prior store remains authoritative |
| Successful atomic replace | No temporary state file remains |
| WORLD commit interpreted as truth, causality, PlanOS activation, or ActOS invocation | Rejected by boundary flags |
