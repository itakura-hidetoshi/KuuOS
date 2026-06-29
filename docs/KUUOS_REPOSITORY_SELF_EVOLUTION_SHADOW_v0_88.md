# KuuOS Repository Self-Evolution Shadow v0.88

v0.88 binds the abstract portfolio selected by v0.87 to concrete repository repair candidates and evaluates every selected candidate in a shadow snapshot.

Each realization binds one v0.87 candidate to one frontier commit, one Git object-database snapshot, one repository observation, and one v0.79 repair candidate. The proposal digest, source commit, source snapshot, source observation, changed paths, and baseline score must agree exactly.

The concrete repair candidate is applied only to an in-memory shadow snapshot. The resulting repository is reobserved, its weighted defect score is compared with the predicted score, and its v0.80 alignment normal form is recertified.

Prediction error must remain within the declared tolerance. Observed score must strictly decrease. Protected paths must remain preserved. Reconstructing the changed paths from the source snapshot must restore the exact source snapshot digest.

A complete and admissible realization set receives `REPOSITORY_SELF_EVOLUTION_SHADOW_PASS`. A complete set with failed empirical conditions receives `REPOSITORY_SELF_EVOLUTION_SHADOW_REJECT`. An empty v0.87 fixed-point portfolio receives `REPOSITORY_SELF_EVOLUTION_SHADOW_STABLE_NO_CHANGE`.

Structural binding failures are fail-closed errors rather than negative empirical assessments.

The certificate grants no patch-application authority, commit authority, or reference-mutation authority.
