# KuuOS Checkpoint Candidate Validation v1.11

v1.11 inserts an explicit validation boundary between the v1.09 checkpoint candidate and the v1.10 CAS contract.

The validator does not rely on the candidate digest alone. It replays the complete v1.09 candidate validation against the original namespace-gate decision, repair route, discrepancy-review record, stability certificate, observation, policies, context, and evaluation times.

It then checks the ready state, repository binding, checkpoint reference binding, and distinct nonzero expected and proposed OIDs.

A valid receipt performs no repository operation, invokes no Git command, and grants no update authority. It records only that the upstream derivation chain and local trust-boundary conditions were revalidated.

A candidate whose own digest is internally consistent but whose content no longer matches the upstream derivation is rejected.
