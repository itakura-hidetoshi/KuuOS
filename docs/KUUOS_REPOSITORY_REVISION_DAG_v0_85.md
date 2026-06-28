# KuuOS Repository Revision DAG v0.85

v0.85 integrates the linear certificate records from v0.82 and the two-parent merge certificates from v0.84 into one finite revision DAG.

A valid DAG requires:

- exactly one genesis record and one root revision
- one shared chain identity and root binding
- every non-genesis record to reference an included predecessor record
- exact predecessor commit, snapshot, sequence, chain-bound, and history bindings
- every merge certificate to reference two included and distinct parent records
- recomputation of the merge fork, common prefix, and branch suffixes
- no repeated source certificate, revision node, or edge
- exact parent arity: zero for the root, one for linear revisions, and two for merge revisions
- every node to be reachable from the root
- a complete deterministic topological order
- explicit finite node and edge bounds
- score-zero normal-form preservation at every certified revision

The certificate records all source certificate digests, revision nodes, edge digests, topological order, terminal tips, bounds, and graph invariants.

The DAG layer does not resolve merge conflicts, write repository content, infer omitted history, or convert CI success into external authority.

No external approval is required.
