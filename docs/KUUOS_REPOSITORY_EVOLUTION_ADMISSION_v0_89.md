# KuuOS Repository Evolution Admission v0.89

v0.89 converts repeated v0.88 shadow results into a governed admission proposal.

An admission proposal is not patch application, commit authority, or reference mutation authority.

At least two independent shadow replay receipts are required. Every replay must bind to the same portfolio, selected candidate set, source commit and snapshot bindings, shadow snapshots, and normal-form certificates.

Every replay receipt carries an issuance time. Receipts issued in the future or older than the configured maximum age are rejected.

The current Git object-database observations must cover the same source commits and must reproduce the source snapshot digests used by the shadow replays. Working-tree observations are not admissible.

If all technical conditions hold, v0.89 emits `REPOSITORY_EVOLUTION_ADMISSION_PROPOSED`.

This status means that the evidence may be submitted to the external approval boundary. It does not authorize repository mutation.

If a technical condition is not satisfied, v0.89 emits `REPOSITORY_EVOLUTION_ADMISSION_REJECTED` with the failed predicates recorded in the certificate.

Repeated stable v0.88 receipts with no selected candidates emit `REPOSITORY_EVOLUTION_ADMISSION_STABLE_NO_CHANGE`.

Digest corruption, invalid nested certificates, mixed stable and nonstable replay modes, and duplicate current revision observations fail closed.

Every admission certificate requires external approval and records that external approval has not been granted. Patch application, commit, and reference mutation authority remain false.
