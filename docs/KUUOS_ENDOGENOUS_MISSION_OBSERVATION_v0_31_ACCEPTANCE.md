# v0.31 Acceptance Matrix

| Case | Expected result |
|---|---|
| Unresolved WORLD evidence | Deterministic mission candidate is generated |
| Counterevidence present | `DISAMBIGUATE` mission is generated and counterevidence is retained |
| Multiple compatible channels | Multiple observation candidates remain explicit |
| No compatible channel | `CAPABILITY_DISCOVERY` route with no self-authorization |
| No unresolved items | `NO_NEW_MISSION` with empty portfolios |
| Paused v0.30 source | `HOLD` while candidates and open horizons are preserved |
| Terminated or handed-over source | `HANDOVER` with successor-readable candidate traces |
| Source-state mismatch | Report construction is rejected |
| Packet or report tampering | Digest validation rejects the artifact |
| Exact replay | No second ledger append |
| Same packet identity, different report | Rejected |
| Candidate ranking | Priority only; no truth, PlanOS activation, tool invocation or ActOS authority |
