# KuuOS Checkpoint Candidate Validation v1.11

v1.11 inserts an explicit validation boundary between the v1.09 candidate and the v1.10 CAS contract.

The validator checks the immutable candidate digest, ready status, repository binding, checkpoint reference binding, and distinct nonzero OIDs.

A valid result does not update a reference and does not invoke Git. It only records that the candidate satisfies the local trust-boundary checks required before a later contract is consumed.

Rejected results identify a failed digest, readiness, repository, reference, or OID condition.
