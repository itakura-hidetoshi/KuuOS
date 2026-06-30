# KuuOS Checkpoint Candidate Validation v1.11

v1.11 follows the v1.10 CAS contract specification and adds a complete validation receipt for any future adapter or authorization layer that consumes a v1.09 checkpoint candidate.

It does not modify the already-defined v1.10 contract. Instead, it closes the trust-boundary gap identified in v1.10 by independently replaying the candidate derivation before later operational layers are introduced.

The validator does not rely on the candidate digest alone. It replays the complete v1.09 candidate validation against the original namespace-gate decision, repair route, discrepancy-review record, stability certificate, observation, policies, context, and evaluation times.

It then checks the ready state, repository binding, checkpoint reference binding, and distinct nonzero expected and proposed OIDs.

A valid receipt performs no repository operation, invokes no Git command, and grants no update authority. It records only that the upstream derivation chain and local trust-boundary conditions were revalidated.

A candidate whose own digest is internally consistent but whose content no longer matches the upstream derivation is rejected.
