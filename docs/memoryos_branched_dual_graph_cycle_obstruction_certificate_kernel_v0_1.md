# MemoryOS v0.76 — branched dual graph, spanning-tree transport, and cycle obstruction

## Scope

MemoryOS v0.76 extends the finite v0.75 dual-cell chain to the smallest
branched-and-recombined dual graph: a four-vertex diamond with two distinct
root-to-target routes.

The layer is finite, exact, future-only, read-only, and advisory. It does not
rank, prune, or select candidates; synthesize or activate plans; issue decision
receipts; execute actions; mutate source MemoryOS, DecisionOS, or persistent
WORLD state; claim verification; or grant truth authority.

The implementation uses the finite group `S3`. It does not claim a continuum
dual-graph bundle, universal route independence, or physical gauge-field
inference.

## Source binding

The runtime regenerates and validates the accepted MemoryOS v0.75 certificate
before deriving v0.76. It binds the v0.75 certificate digest, dual-cell-chain
profile digest, path-ordered composition digest, single-defect localization
digest, dual-cycle holonomy digest, all collection digests and record counts,
and all retained candidate, history, probe, review, dissent, and minority sets.

Any source change is rejected fail-closed.

## Diamond dual graph

The dual vertices are:

- `cell-0`: root;
- `cell-1`: upper branch;
- `cell-2`: lower branch;
- `cell-3`: recombination target.

The edge transports are `J_01`, `J_13`, `J_02`, and `J_23`. Define

\[
P_{\mathrm{up}}=J_{01}J_{13},
\qquad
P_{\mathrm{low}}=J_{02}J_{23}.
\]

The upper route is the selected spanning-tree transport. The lower route is
retained as an alternative path; no source record is deleted.

## Cycle obstruction

The root-based route-cycle obstruction is

\[
C=P_{\mathrm{up}}P_{\mathrm{low}}^{-1}.
\]

For every group,

\[
P_{\mathrm{up}}=P_{\mathrm{low}}
\quad\Longleftrightarrow\quad
C=1.
\]

Lean theorem:

- `paths_agree_iff_cycle_obstruction_identity`

Thus route agreement is an exact group identity, not a claim derived from one
frame-dependent coordinate.

## Routed target defect

For a target defect `D` at `cell-3`, define

\[
D_{\mathrm{up}}
=P_{\mathrm{up}}DP_{\mathrm{up}}^{-1},
\]

\[
D_{\mathrm{low}}
=P_{\mathrm{low}}DP_{\mathrm{low}}^{-1}.
\]

The exact route relation is

\[
\boxed{
D_{\mathrm{up}}=C D_{\mathrm{low}} C^{-1}
}.
\]

Lean theorems:

- `upper_lower_localizations_related`
- `path_agreement_implies_localization_agreement`

A nontrivial cycle can therefore produce different exact routed
representatives while preserving their conjugacy class.

## Gauge covariance

Assign independent frames `g_0`, `g_1`, `g_2`, and `g_3` to the four vertices.
Then

\[
P_{\mathrm{up}}\mapsto g_0^{-1}P_{\mathrm{up}}g_3,
\qquad
P_{\mathrm{low}}\mapsto g_0^{-1}P_{\mathrm{low}}g_3,
\]

and

\[
C\mapsto g_0^{-1}Cg_0.
\]

A target defect transforms in the `g_3` frame, while either root-localized
defect transforms by conjugation in the `g_0` frame.

Lean theorems:

- `upper_path_gauge_covariant`
- `lower_path_gauge_covariant`
- `cycle_obstruction_gauge_covariant`
- `upper_localized_defect_gauge_covariant`
- `lower_localized_defect_gauge_covariant`

## Wilson signatures and resolution limit

Every class function of `C` is gauge invariant:

- `cycle_obstruction_wilson_gauge_invariant`

Because the routed defect representatives are conjugate,

\[
\chi(D_{\mathrm{up}})=\chi(D_{\mathrm{low}})
\]

for every class function `χ`:

- `route_wilson_signature_equal`

This is recorded as a resolution limit. A class-function signature is frame
independent but cannot distinguish exact representatives inside one conjugacy
class.

## Canonical exact S3 profiles

### Flat diamond

\[
J_{01}=(01),\quad
J_{13}=(12),\quad
J_{02}=1,\quad
J_{23}=(01)(12).
\]

Then

\[
P_{\mathrm{up}}=P_{\mathrm{low}}=(012),
\qquad C=1.
\]

The cycle permutation trace is `3`.

### Cycle-obstructed diamond

\[
J_{01}=1,\quad J_{13}=1,\quad J_{02}=(01),\quad J_{23}=1.
\]

Then

\[
P_{\mathrm{up}}=1,
\qquad P_{\mathrm{low}}=(01),
\qquad C=(01).
\]

The target defect inherited from v0.75 is

\[
D=(021).
\]

Hence

\[
D_{\mathrm{up}}=(021),
\qquad D_{\mathrm{low}}=(012).
\]

These exact representatives differ but are conjugate and both have permutation
trace `0`. The cycle trace is `1`.

Canonical Lean theorems include:

- `canonical_flat_paths_agree`
- `canonical_flat_cycle_obstruction`
- `canonical_obstructed_paths_disagree`
- `canonical_obstructed_cycle_obstruction`
- `canonical_obstructed_route_representatives_differ`
- `canonical_obstructed_route_wilson_limitation`

## Advisory confidence convention

The source confidence remains

\[
C_0=\frac13.
\]

Define

\[
P_{\mathrm{route}}
=\frac{3-\chi_{\mathrm{perm}}(C)}{18},
\qquad
C_{\mathrm{diamond}}=C_0-P_{\mathrm{route}}.
\]

Canonical values are:

- flat diamond: penalty `0`, adjusted confidence `1/3`;
- cycle-obstructed diamond: penalty `1/9`, adjusted confidence `2/9`.

This is not a posterior probability, universal statistical optimum, physical
action, decision rule, or truth authority.

## Exact runtime ledger

The certificate emits:

- 5 literature records;
- 8 incidence records;
- 2 graph profiles;
- 8 edge-transport records;
- 2 spanning-tree route records;
- 2 alternative-path comparison records;
- 2 cycle-obstruction records;
- 4 target-defect routing records;
- 2 route-conjugacy records;
- 4 route-Wilson records;
- 2 cycle-Wilson records;
- 2 confidence records;
- 2 memory-fusion records;
- 8 full-rank retention records;
- 4 singular atomic retention records;
- 3 rank-one source boundaries.

All group values are exact permutation triples and all confidence values are
exact rationals.

## Fail-closed checks

The checker rejects modified source digests, edge transports, path-agreement
claims, cycle obstructions, routed defects, route-equality claims, confidence
values, candidate-selection claims, unexpected truth claims, collection digest
mismatches, and source count mismatches.

## Literature grounding

The finite structure remains grounded in:

1. arXiv:2604.16252 — dual incidence graphs, spanning structures, and
   Wilson-loop composition.
2. arXiv:1006.2059 — gauge-invariant discrete transport on glued simplicial
   complexes.
3. arXiv:hep-lat/0309023 — ordered non-Abelian lattice holonomy composition.
4. arXiv:1011.0371 — gauge-covariant defect and cycle interpretation.
5. arXiv:2605.26697 — path-ordered transport and conjugacy-invariant holonomy
   comparison.

These references ground the mathematical organization. They are not sources
for the MemoryOS confidence convention or authority policy.
