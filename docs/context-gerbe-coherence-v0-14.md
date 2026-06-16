# Context Gerbe Coherence v0.14

## Position in the runtime stack

Context Gerbe Coherence v0.14 is an additive higher-gauge layer above Context Gauge Atlas v0.13.

It does not replace pairwise chart transitions, atlas curvature, cocycle residue, or atlas holonomy. It promotes the already-observed cocycle residue into explicit local coherence data on higher overlaps.

The stack is:

- v0.14 Context Gerbe Coherence: triple-overlap coherence, fourfold coherence residue, surface holonomy
- v0.13 Context Gauge Atlas: pairwise chart overlap, transition functions, atlas curvature, cocycle defect, atlas holonomy
- v0.12 Horizon Gauge Arbitration: time-horizon connection and curvature
- v0.11 Delayed Multi-Horizon Credit
- v0.10-v0.2 existing runtime spine

## Geometric interpretation

For local charts U_alpha, U_beta, U_gamma and transition functions g_alpha_beta, v0.13 retains the discrepancy between direct and composite transport.

v0.14 represents this discrepancy by a local coherence 2-cell on the triple overlap:

h_alpha_beta_gamma : g_alpha_gamma => g_beta_gamma composed with g_alpha_beta

The 2-cell is defined only where the triple overlap is sufficiently supported. It is not a global correction and does not trivialize the atlas.

On a fourfold overlap, two compositions of local 2-cells can disagree. That disagreement is retained as a higher cocycle defect rather than removed.

## Finite overlap model

Pairwise overlap remains the bounded v0.13 overlap score.

Triple overlap is the minimum of the three pairwise overlap scores among two source charts and the target chart. Its value lies in the closed unit interval.

Fourfold overlap is the minimum of all six pairwise overlap scores among three source charts and the target chart. Its value lies in the closed unit interval.

A minimum triple-overlap threshold controls whether a coherence 2-cell is defined. A separate minimum fourfold-overlap threshold controls whether a higher coherence witness is recorded.

## Coherence 2-cells

For each supported triple overlap, v0.14 preserves both:

- direct transport from a source chart to the target chart
- composite transport through a compatible mediator chart

Their bounded section distance is the local coherence residue.

The mean of all local coherence residues is the gerbe two-curvature.

Neither a local coherence residue nor gerbe two-curvature is an execution veto.

## Higher cocycle defect

For a supported fourfold overlap, v0.14 compares two mediator orders connecting the same local source section to the target context.

The maximum bounded disagreement is the higher cocycle defect.

The higher cocycle defect is observational residue. It is not a hard gate, execution prohibition, global winner, or authority escalation.

## Classification

Each target context receives one of three local classifications:

- no_triple_overlap: no supported coherence 2-cell exists
- coherent_gerbe_transport: supported 2-cells exist and both two-curvature and higher cocycle defect remain below their plurality thresholds
- plural_gerbe_transport: supported local coherence remains genuinely plural because at least one higher residue reaches its threshold

No global gerbe winner is generated.

## Local lift to v0.13

The endpoints of supported direct and composite transports are aggregated with their local overlap support while preserving the horizon plurality floor.

The resulting local section is lifted only into the three v0.13 base horizon weights:

- lifted short component to v0.13 base short-horizon weight
- lifted medium component to v0.13 base medium-horizon weight
- lifted long component to v0.13 base long-horizon weight

The lifted weights remain normalized and retain the positive plurality floor.

v0.14 does not alter v0.13 licenses, hard gates, child-cycle cardinality, replay rules, or execution authority.

## Surface holonomy

Each completed v0.14 cycle appends one surface-holonomy record containing:

- target context
- gerbe classification
- number of local 2-cells
- number of fourfold coherence witnesses
- gerbe two-curvature
- higher cocycle defect
- decision digest

Surface holonomy is append-only. Reprocessing the same decision digest is idempotent and must not append a second record.

## Required boundaries

The implementation must preserve all of the following:

- pairwise atlas transitions remain owned by v0.13
- coherence 2-cells are local to supported triple overlaps
- higher coherence witnesses are local to supported fourfold overlaps
- two-cell residue is not a veto
- higher cocycle defect is not a veto
- global trivialization is forbidden
- one v0.13 local lift is permitted per v0.14 cycle
- v0.13 authority is preserved
- surface holonomy is append-only
- deterministic replay is required
- graph semantics remain forbidden

## Formal obligations

The Lean surface should prove:

- bounded triple overlap is between zero and one
- bounded fourfold overlap is between zero and one
- gerbe two-curvature is between zero and one
- higher cocycle defect is between zero and one
- a positive plurality floor prevents any single horizon component from becoming one
- coherence witnesses remain local to their declared overlap
- appending one completed cycle strictly increases the surface-holonomy record count

## Initial kernel acceptance cases

The first kernel should cover:

1. Three mutually compatible observed charts produce three local coherence 2-cells around one target chart.
2. The same three charts produce one fourfold coherence witness with the target chart.
3. Non-identical chart outcomes produce observable two-curvature and higher cocycle residue.
4. Lifted horizon weights sum to one and preserve the configured floor.
5. A committed decision appends exactly one surface-holonomy record.
6. Recommitting the same decision digest is an idempotent replay.
7. No node, edge, graph, or dependency vocabulary appears in the runtime packet.
