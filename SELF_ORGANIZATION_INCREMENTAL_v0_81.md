# KuuOS Incremental Preservation v0.81

v0.81 compares repository scope fingerprints after an update.

Unchanged scopes reuse their previous result.

Changed contract scopes are checked locally.

Shared root, workflow, or contract-set changes trigger a full check.

A stale previous certificate is rejected.
