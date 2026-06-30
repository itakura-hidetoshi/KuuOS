# KuuOS Repository Checkpoint Atomic CAS Transition v1.16

v1.16 follows the merged v1.15 checkpoint CAS authorization decision.

It models one atomic checkpoint compare-and-swap transition together with one atomic authorization-nonce consumption transition.

The v1.15 authorization certificate is independently recomputed from its original v1.13 coherence receipt, v1.14 request and policy, v1.15 decision policy, external decision receipt, and nonce-status receipt.

The modeled execution also requires an allowlisted executor, a valid transition policy, a fresh direct checkpoint-reference state sourced from the reference store, a fresh nonce registry bound to the v1.15 nonce-status snapshot, an unused and non-revoked nonce, a valid execution time window, and a current OID equal to the authorized expected OID.

When every precondition holds, the modeled reference state changes from the expected OID to the proposed OID and the modeled nonce registry records the nonce as consumed. Both sequence numbers advance in the same logical transition.

When any precondition fails, including an OID conflict, stale evidence, consumed or revoked nonce, denied authorization, or tampered authorization evidence, the transition aborts. The exact source reference-state digest and source nonce-registry digest are preserved as the final digests.

This layer changes only immutable modeled values. It invokes no live Git command, mutates no live repository, writes no object, index, working tree, or reflog, performs no signing, deletes no reference, performs no force update, and performs no push.
