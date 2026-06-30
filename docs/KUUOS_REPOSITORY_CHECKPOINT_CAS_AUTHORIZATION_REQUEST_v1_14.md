# KuuOS Repository Checkpoint CAS Authorization Request v1.14

v1.14 follows the merged v1.13 checkpoint CAS coherence receipt.

It converts a coherent READY receipt into a bounded, single-use authorization request candidate. It does not grant authorization.

A coherent CONFLICT receipt is preserved as an explicit denial. Invalid, incoherent, expired-at-issue, overlong, unbound, or nonce-free input is rejected.

The request policy binds the allowed repository and checkpoint reference, requires a valid v1.13 receipt, limits request lifetime, requires a future single-use authorization, and marks the artifact as request-only.

The v1.13 receipt is rechecked for digest validity, evidence bindings, local coherence claims, forbidden-operation flags, status and reason consistency, compare-and-swap meaning, and the direct observed-versus-expected OID relation.

The expected, observed, and proposed OIDs must each be lowercase 40-character hexadecimal values and must be nonzero. The expected and proposed OIDs must be distinct.

A READY request records the repository identity, Git-directory fingerprint, checkpoint reference, expected OID, observed OID, proposed OID, requester, nonce, issue time, and expiry time. These fields are descriptive inputs to a later authorization layer.

This layer grants no authorization, performs no execution, invokes no live Git command, and does not mutate a reference.
