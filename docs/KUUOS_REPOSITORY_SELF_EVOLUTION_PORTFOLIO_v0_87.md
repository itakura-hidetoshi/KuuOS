# KuuOS Repository Self-Evolution Portfolio v0.87

v0.87 connects the certified repository frontier to a bounded self-evolution planning layer.

Each candidate is bound to one frontier revision and records changed paths, baseline score, predicted score, risk, reversibility, protected-path preservation, and normal-form preservation.

Admissibility requires strict score improvement, risk within policy, bounded changed paths, protected-path preservation, normal-form preservation, and reversibility when required. Candidates requiring external approval remain inadmissible.

All candidate subsets up to the selection bound are enumerated. A coherent portfolio contains at most one candidate per frontier revision and no equal, ancestor, or descendant path conflicts. The deterministic optimum maximizes aggregate score improvement, then minimizes aggregate risk, changed-path count, portfolio size, and candidate digest order.

When no candidate is admissible, the empty portfolio is certified as a stable no-change fixed point.

The certificate does not apply patches, create commits, move references, or grant execution authority.
