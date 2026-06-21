# v0.33 Acceptance Matrix

| Case | Expected result |
|---|---|
| Exact v0.32 feedback, evidence and finite protocol | Single-use VerifyOS request is materialized |
| Protocol not yet valid or expired | Request construction is rejected |
| Protocol rebound to another feedback/evidence chain | Exact-binding rejection |
| Same protocol used for a second distinct request | Rejected |
| Exact request replay | No second ledger append |
| Verification completed before request or at/after expiry | Rejected |
| Primary and independent assessor identities are equal | Rejected |
| Source marked both matched and divergent | Rejected |
| `PASSED` with open conflict, falsifier, inadmissibility or missing independence | Rejected |
| Valid `PASSED` | Verification debt discharged; no truth/adoption authority |
| `FAILED` without conclusive failure basis | Rejected |
| Valid `FAILED` | Corrective-action debt; no automatic rejection |
| `INDETERMINATE + DEFER` | Verification debt remains open; `DEFER_CANDIDATE` |
| `INDETERMINATE + REOBSERVE` | Verification debt remains open; `REOBSERVE_CANDIDATE` |
| `PASSED + WORLD_UPDATE_CANDIDATE` | `ADOPT_CANDIDATE`; proposed fragment selected, no commit |
| `PASSED + REOBSERVE` | `REOBSERVE_CANDIDATE`; no promotion to adoption |
| `FAILED` | `REJECT_CANDIDATE`; prior fragment preserved |
| Same VerifyOS request used for a second receipt | Rejected |
| Same verification receipt used for a second disposition | Rejected |
| Feedback/receipt lineage mismatch | Rejected |
| Candidate or receipt body tampering | Digest rejection |
| Core-only receipt or disposition in official ledger | Rejected before append |
| Every disposition route | Governance review and separate WORLD commit remain required |
