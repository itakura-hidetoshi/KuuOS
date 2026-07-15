# MemoryOS v0.80 — all-root charts and defect-aware free-word transport

## Scope

MemoryOS v0.80 extends the v0.79 rooted free-group word layer from one distinguished route-0 chart to all four route charts of the finite dual atlas. Each chart retains:

- four exact route-comparison coordinates,
- the target defect localized at the selected root route,
- a five-generator free-group evaluation map,
- exact word transport to every other root chart,
- gauge-covariant representatives and class-function invariants.

The layer remains finite, exact, future-only, read-only, and advisory. It does not rank, prune, select, commit, activate, execute, mutate, verify, or grant truth authority.

The implementation does not claim a universal character-variety classification, a universally separating Wilson-word family, a continuum gauge groupoid theorem, or physical gauge-field inference.

## Source binding

The runtime validates the accepted MemoryOS v0.79 certificate before deriving v0.80. It binds:

- the complete v0.79 certificate digest,
- every v0.79 collection digest and record count,
- all source true and false authority flags,
- the four canonical profile order,
- the v0.79 mixed-word signatures,
- the canonical ordered-AB / ordered-BA separator values,
- exact source confidence values,
- candidate, history, probe, review, dissent, and minority-retention sets.

Any source digest edit, source collection edit, mixed-signature edit, separator edit, confidence edit, retention edit, or authority-boundary reversal is rejected fail-closed.

## Four route labels

Lean introduces the finite route type

\[
\mathcal R=\{0,1,2,3\}.
\]

For a four-route atlas with path transports \(P_i\), `routePath` selects the exact path attached to route \(i\).

Every path obeys the same endpoint-covariant transformation law:

\[
P_i\longmapsto g_0^{-1}P_i g_5.
\]

Lean theorem:

- `route_path_gauge_covariant`.

## Root charts

The chart based at route \(i\) is

\[
\mathcal C_i=(C_{i0},C_{i1},C_{i2},C_{i3},D_i),
\]

where

\[
C_{ij}=P_iP_j^{-1},
\qquad
D_i=P_iD_{\mathrm{target}}P_i^{-1}.
\]

Lean definitions:

- `RouteLabel`,
- `RootChart`,
- `atlasRootChart`,
- `RootChart.NormalizedAt`.

Every chart is normalized at its own root:

\[
C_{ii}=1.
\]

Lean theorem:

- `atlas_root_chart_normalized`.

## Defect-aware root transition

Given a chart \(\mathcal C_i=(C_{ik},D_i)\), rebasing to route \(j\) is

\[
C'_{jk}=C_{ij}^{-1}C_{ik},
\]

and the root-localized defect changes by

\[
D_j=C_{ij}^{-1}D_iC_{ij}.
\]

This corrects the purely coordinate-only viewpoint: the defect generator is not held fixed when the geometric root route changes.

Lean definition:

- `rebaseRootChart`.

Lean theorems:

- `atlas_root_chart_rebase_exact`,
- `atlas_root_defect_transition`.

## Transition composition and round trip

For any intermediate root \(j\) and target root \(k\),

\[
T_k(T_j(\mathcal C))=T_k(\mathcal C).
\]

Thus the direct target chart and the chart obtained through any intermediate root are exactly equal, including the defect field.

For a chart normalized at route \(i\),

\[
T_i(\mathcal C)=\mathcal C,
\]

and therefore

\[
T_i(T_j(\mathcal C))=\mathcal C.
\]

Lean theorems:

- `rebase_root_chart_composition`,
- `rebase_root_chart_self_of_normalized`,
- `rebase_root_chart_round_trip`.

## Gauge covariance of the full chart

Simultaneous conjugation by the common root frame is

\[
C_{ij}\mapsto g_0^{-1}C_{ij}g_0,
\qquad
D_i\mapsto g_0^{-1}D_ig_0.
\]

Root transition commutes with this conjugation:

\[
T_j(g_0^{-1}\mathcal Cg_0)
=
g_0^{-1}T_j(\mathcal C)g_0.
\]

Lean definitions and theorems:

- `conjugateRootChart`,
- `rebase_root_chart_conjugation_covariant`,
- `atlas_root_chart_gauge_covariant`.

## Five-generator free group

Each root chart assigns five generators:

\[
X_0=C_{i0},\quad
X_1=C_{i1},\quad
X_2=C_{i2},\quad
X_3=C_{i3},\quad
D=D_i.
\]

Lean defines the universal homomorphism

\[
\operatorname{ev}_{\mathcal C_i}:
F(X_0,X_1,X_2,X_3,D)\longrightarrow G.
\]

Lean definitions:

- `RootChartWordGenerator`,
- `rootChartWordAssignment`,
- `evalRootChartWord`.

Lean theorem:

- `eval_root_chart_word_generator`.

## Defect-aware word transition

Transition to target root \(j\) substitutes

\[
X_k\longmapsto X_j^{-1}X_k,
\]

for every route generator, and

\[
D\longmapsto X_j^{-1}DX_j.
\]

The substitution extends uniquely to a free-group homomorphism \(N_j\).

Lean definitions:

- `rootTransitionGenerator`,
- `rootTransitionHom`.

Lean theorem:

- `root_transition_hom_generator`.

## Absorption law

For every pair of roots \(i,j\),

\[
N_i\circ N_j=N_j.
\]

This is proved on the complete free group by extensionality on the five generators. The defect case uses the full conjugating substitution.

Lean theorems:

- `root_transition_hom_absorbing`,
- `root_transition_word_absorbing`.

## Evaluation compatibility

For every chart, target root, and free-group word \(w\),

\[
\boxed{
\operatorname{ev}_{\mathcal C}(N_jw)
=
\operatorname{ev}_{T_j(\mathcal C)}(w).
}
\]

Evaluation through an intermediate root is therefore identical to direct target-root evaluation:

\[
\operatorname{ev}_{T_i(\mathcal C)}(N_jw)
=
\operatorname{ev}_{T_j(\mathcal C)}(w).
\]

Lean theorems:

- `root_transition_evaluation_compatibility`,
- `root_transition_evaluation_via_intermediate`.

The runtime checks this relation for ten retained words, four source roots, four target roots, and four canonical profiles, producing 640 exact compatibility records.

## Arbitrary-word gauge covariance

For every root-chart word \(w\),

\[
\operatorname{ev}_{g^{-1}\mathcal Cg}(w)
=
g^{-1}\operatorname{ev}_{\mathcal C}(w)g.
\]

Hence every class-function Wilson observable

\[
W_{\chi,w}(\mathcal C)
=
\chi(\operatorname{ev}_{\mathcal C}(w))
\]

is gauge invariant.

Lean definitions and theorems:

- `rootChartWordWilson`,
- `root_chart_word_evaluation_conjugation_covariant`,
- `root_chart_word_wilson_gauge_invariant`.

## Root-independent transported comparison

For actual atlas charts,

\[
\operatorname{ev}_{\mathcal C_i}(N_jw)
=
\operatorname{ev}_{\mathcal C_j}(w).
\]

The same equality holds after applying any class function. A reference word may therefore be evaluated from any available source root chart after exact transport, without privileging that source root as an authority.

Lean theorems:

- `transported_atlas_root_word_exact`,
- `transported_atlas_root_word_wilson_exact`.

## Canonical mixed separator across all roots

The v0.79 separator is represented in the route-0 chart by

\[
M=X_3D.
\]

v0.80 proves that its transported version gives the same exact values from every source root chart.

For ordered AB:

\[
W_{\mathrm{perm},N_0M}(\mathcal C_i^{AB})=3
\]

for every \(i\in\mathcal R\).

For ordered BA:

\[
W_{\mathrm{perm},N_0M}(\mathcal C_i^{BA})=0
\]

for every \(i\in\mathcal R\).

Therefore

\[
\boxed{
W_{\mathrm{perm},N_0M}(\mathcal C_i^{AB})
\ne
W_{\mathrm{perm},N_0M}(\mathcal C_i^{BA})
}
\]

for all source roots.

Lean definitions and theorems:

- `routeDefectWord`,
- `eval_route_defect_word`,
- `route0_chart_cycle03_defect_matches_v079`,
- `canonical_ordered_ab_all_root_mixed_wilson`,
- `canonical_ordered_ba_all_root_mixed_wilson`,
- `canonical_all_root_mixed_wilson_separates`.

This is a finite exact canonical result. It does not assert universal separation of arbitrary representations.

## Canonical all-root mixed-trace rows

Each row is ordered as

\[
(\chi(X_0D),\chi(X_1D),\chi(X_2D),\chi(X_3D)).
\]

### Flat profile

All four root rows are

\[
(0,0,0,0).
\]

### Single-support profile

- route 0: \((0,1,0,0)\),
- route 1: \((1,0,1,1)\),
- route 2: \((0,1,0,0)\),
- route 3: \((0,1,0,0)\).

### Ordered AB profile

- route 0: \((0,1,1,3)\),
- route 1: \((1,0,3,1)\),
- route 2: \((1,0,0,1)\),
- route 3: \((0,1,1,0)\).

### Ordered BA profile

- route 0: \((0,1,1,0)\),
- route 1: \((1,0,0,1)\),
- route 2: \((1,3,0,1)\),
- route 3: \((3,1,1,0)\).

These rows are chart-dependent exact representatives. The transported reference separator is the root-independent comparison object.

## Confidence policy

v0.80 introduces no new confidence penalty:

\[
P_{\mathrm{chart}}=0.
\]

For every canonical profile,

\[
C_{v0.80}=C_{v0.79}.
\]

The retained exact values are:

- flat: \(1/3\),
- single-support: \(5/18\),
- ordered AB: \(11/54\),
- ordered BA: \(11/54\).

The chart and word-transport data are diagnostic and review-oriented. They are not posterior probabilities, decision rules, ranking scores, physical actions, universal optima, or truth authorities.

## Exact runtime ledger

The certificate contains:

- 6 inherited literature records,
- 4 route-label records,
- 16 all-root chart records,
- 64 root-coordinate records,
- 16 root-defect records,
- 64 direct chart-transition records,
- 256 transition-composition records,
- 5 free-group generator records,
- 10 canonical word records,
- 20 generator-substitution records,
- 16 transition-absorption records,
- 640 transition/evaluation compatibility records,
- 160 word gauge-covariance records,
- 4 transported separator records,
- 4 source-confidence preservation records,
- 4 memory-fusion records,
- 8 full-rank transport records,
- 4 singular atomic records,
- 3 rank-one source boundaries.

All group values are exact permutation triples. All confidence values are exact rationals. All words are explicit signed-generator lists with deterministic free reduction.

## Fail-closed checks

The checker rejects:

- edited v0.79 source certificates,
- source schema, digest, collection, or count changes,
- source mixed-signature or separator changes,
- root-coordinate edits,
- root-defect transition edits,
- chart-composition edits,
- generator-substitution edits,
- absorption-law edits,
- word/evaluation compatibility edits,
- gauge-covariance edits,
- transported separator edits,
- confidence edits,
- authority-boundary reversals,
- unexpected truth claims,
- collection digest or record-count mismatches.

## Retention behavior

All v0.79 decision candidates, histories, quotient-coordinate probes, review sets, dissent records, and minority-protection records are retained.

For full-rank transport records, v0.80 records that all-root chart construction, defect-aware word transition, and root-independent Wilson comparison commute with the existing transport layer.

For singular atomic records, v0.80 retains atomic chart and defect-word signatures without emitting a two-dimensional target density or reconstructing a lost coordinate.

## Authority boundary

MemoryOS v0.80 remains:

- future-only,
- read-only,
- advisory,
- non-ranking,
- non-pruning,
- non-selecting,
- non-committing,
- non-activating,
- non-executing,
- non-mutating,
- non-verifying,
- non-truth-authoritative.
