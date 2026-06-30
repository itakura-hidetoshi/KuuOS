# KuuOS Repository Checkpoint CAS Authorization Decision v1.15

v1.15 follows the merged v1.14 checkpoint CAS authorization request.

It accepts a complete v1.14 request, the original v1.13 coherence receipt and v1.14 request policy, an external authorization decision receipt, a nonce-registry status receipt, and a local decision policy.

A grant is accepted only when the v1.14 request is independently recomputed as READY, every request and evidence digest is exactly bound, both authorities are allowlisted, the external signature-verification and identity claims are positive, the decision is not revoked, the decision remains inside the request lifetime, the nonce status is fresh, and the nonce is unused and not revoked.

A valid external denial is preserved as DENIED. A CONFLICT request cannot be upgraded by an external grant. Invalid, stale, expired, future-dated, consumed, revoked, unsigned, unauthorized, unbound, or self-consistently tampered evidence is REJECTED.

The signature-verification and revocation fields are externally supplied receipt claims. This runtime verifies their structure and binding; it does not perform cryptography or independently query an authority service.

GRANTED means only that the exact request is eligible for one later compare-and-swap attempt. This layer does not consume the nonce, execute a Git command, update a checkpoint reference, mutate another reference, or grant push authority.
