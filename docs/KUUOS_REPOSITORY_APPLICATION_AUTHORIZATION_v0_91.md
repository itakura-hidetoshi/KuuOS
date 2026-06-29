# KuuOS Repository Application Authorization v0.91

v0.91 converts one accepted v0.90 external-approval certificate into a finite, single-use repository application authorization.

The authorization binds one exact external-approval certificate, admission certificate, authorization policy, patch bundle, source commit, source snapshot, allowed path set, expected changed path set, nonce, issuance time, and expiry time.

The current source state must be observed from the Git object database. Working-tree observations are not admissible. The observed source commit and snapshot must still match the authorized source exactly.

The expected changed paths must be canonical, nonempty, contained within the allowed scope, outside protected paths, and within the policy path-count bound. The patch count must remain within the policy bound.

Single-use status is established through an independent nonce-registry receipt. The nonce authority must be authorized, the registry snapshot must be bound to the exact scope and nonce, and the nonce must be unused and unrevoked.

The source-state receipt and nonce-status receipt must be fresh. Evidence must follow the order:

```text
external approval evaluation
≤ authorization issuance
≤ source observation
≤ nonce-status check
≤ authorization evaluation
< authorization expiration
```

Operational failures such as source drift, stale evidence, path-scope violation, protected-path inclusion, excessive patch count, nonce reuse, nonce revocation, unauthorized nonce authority, or expiration produce `REPOSITORY_APPLICATION_AUTHORIZATION_REJECTED`.

Digest corruption and mismatched approval, admission, policy, scope, nonce, or source-state bindings fail closed.

A valid assessment produces `REPOSITORY_APPLICATION_AUTHORIZATION_GRANTED` and marks the exact scope as eligible for one later application attempt.

This layer does not apply a patch, create a commit, or mutate a reference. Those effects remain reserved for later stages.
