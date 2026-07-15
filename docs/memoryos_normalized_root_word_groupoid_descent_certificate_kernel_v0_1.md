# MemoryOS v0.81 — normalized root-word pair groupoid and Wilson descent

## Scope

MemoryOS v0.81 descends the redundant five-generator all-root chart of v0.80 to a normalized four-generator word model at each route root.

For every selected root, the self-coordinate is removed and the remaining chart contains:

- three ordered route slots,
- one root-localized defect generator,
- exact reversible word transport to every other root,
- path-independent evaluation,
- gauge-covariant representatives,
- root-independent class-function Wilson values.

The finite exact model is implemented for the canonical `S3` profiles and supported by arbitrary-group Lean algebra. It remains future-only, read-only, advisory, non-ranking, non-selecting, non-executing, and non-truth-authoritative.

The implementation does not claim a universal free-groupoid presentation, a universal character-variety classification, a continuum gauge-groupoid theorem, or physical gauge-field inference.

## Source binding

The runtime validates the complete accepted MemoryOS v0.80 certificate before deriving v0.81. It binds:

- the complete v0.80 certificate digest,
- every v0.80 collection digest and record count,
- all source true and false authority flags,
- all four canonical profiles,
- all four transported mixed-separator records,
- exact source confidence values,
- retained candidates, histories, probes, review sets, dissent, and minority visibility.

Any source digest edit, collection edit, separator edit, confidence edit, retention edit, or authority-boundary reversal is rejected fail-closed.

## Normalized route slots

Let the route set be

\[
\mathcal R=\{0,1,2,3\}.
\]

For each selected root \(i\), the normalized chart deletes the trivial self-coordinate \(C_{ii}=1\). The remaining routes are placed into three deterministic slots:

\[
S_i=(r_i^{(1)},r_i^{(2)},r_i^{(3)})
=\mathcal R\setminus\{i\},
\]

ordered by route index.

| root | slot 1 | slot 2 | slot 3 |
|---|---|---|---|
| route 0 | route 1 | route 2 | route 3 |
| route 1 | route 0 | route 2 | route 3 |
| route 2 | route 0 | route 1 | route 3 |
| route 3 | route 0 | route 1 | route 2 |

Lean definitions:

- `NormalizedRouteSlot`,
- `slotRoute`,
- `NormalizedRootWordGenerator`.

## Four-generator normalized free group

At root \(i\), the normalized generators are

\[
Y_1=C_{i,r_i^{(1)}},\qquad
Y_2=C_{i,r_i^{(2)}},\qquad
Y_3=C_{i,r_i^{(3)}},\qquad
D=D_i.
\]

The deleted self-coordinate is represented by the identity word. Every physical route coordinate has a normalized word representation

\[
W_i(k)=
\begin{cases}
1,&k=i,\\
Y_s,&r_i^{(s)}=k.
\end{cases}
\]

Lean definitions and theorem:

- `normalizedCoordinateWord`,
- `normalizedRootWordAssignment`,
- `evalNormalizedRootWord`,
- `eval_normalized_coordinate_word_of_normalized`.

## Defect-aware pair-groupoid transport

A word written in target chart \(j\) is transported to source chart \(i\) by

\[
Y_s^{(j)}\longmapsto
W_i(j)^{-1}W_i(r_j^{(s)}),
\]

and

\[
D_j\longmapsto W_i(j)^{-1}D_iW_i(j).
\]

The substitution extends to a free-group homomorphism

\[
T_{i\leftarrow j}:F_j\longrightarrow F_i.
\]

Lean definitions:

- `normalizedTransitionGenerator`,
- `normalizedTransitionHom`.

The physical coordinate words obey

\[
T_{i\leftarrow j}(W_j(k))
=W_i(j)^{-1}W_i(k).
\]

Lean theorem:

- `normalized_transition_coordinate_word`.

## Pair-groupoid laws

The normalized transports satisfy exact identity, composition, and inverse laws on the complete free group.

### Identity

\[
\boxed{T_{i\leftarrow i}=\operatorname{id}}
\]

Lean theorem:

- `normalized_transition_hom_identity`.

### Composition

\[
\boxed{
T_{i\leftarrow j}\circ T_{j\leftarrow k}
=T_{i\leftarrow k}
}
\]

Lean theorems:

- `normalized_transition_hom_comp`,
- `normalized_transition_word_comp`.

### Inverse

\[
\boxed{
T_{i\leftarrow j}\circ T_{j\leftarrow i}
=\operatorname{id}
}
\]

Lean theorems:

- `normalized_transition_hom_inverse`,
- `normalized_transition_word_round_trip`.

Unlike the target-projector absorption law of the redundant five-generator model, the normalized transport is reversible. Removing the identity coordinate converts the transport system into a finite pair groupoid.

## Evaluation and Wilson descent

For every normalized chart \(\mathcal C_i\), target root \(j\), and free word \(w\),

\[
\boxed{
\operatorname{ev}_{\mathcal C_i}
\bigl(T_{i\leftarrow j}(w)\bigr)
=
\operatorname{ev}_{\mathcal C_j}(w)
}
\]

where \(\mathcal C_j\) is the exact defect-aware rebase of \(\mathcal C_i\).

Lean theorems:

- `normalized_transition_evaluation_compatibility`,
- `normalized_atlas_word_transport_exact`.

Composition gives transport-path independence:

\[
\operatorname{ev}_{\mathcal C_i}
\bigl(T_{i\leftarrow j}(T_{j\leftarrow k}(w))\bigr)
=
\operatorname{ev}_{\mathcal C_i}
\bigl(T_{i\leftarrow k}(w)\bigr).
\]

Lean theorem:

- `normalized_atlas_word_transport_path_independent`.

For a common root frame \(g\), every normalized word transforms by conjugation:

\[
\operatorname{ev}_{g^{-1}\mathcal Cg}(w)
=g^{-1}\operatorname{ev}_{\mathcal C}(w)g.
\]

Lean theorem:

- `normalized_root_word_evaluation_conjugation_covariant`.

For any class function \(\chi\),

\[
W_{\chi,w}(\mathcal C)
=\chi\bigl(\operatorname{ev}_{\mathcal C}(w)\bigr)
\]

is gauge invariant and obeys exact root descent:

\[
\boxed{
W_{\chi,T_{i\leftarrow j}(w)}(\mathcal C_i)
=W_{\chi,w}(\mathcal C_j)
}.
\]

Lean definitions and theorems:

- `normalizedRootWordWilson`,
- `normalized_root_word_wilson_gauge_invariant`,
- `normalized_atlas_word_wilson_transport_exact`.

## Canonical mixed separator

In the route-0 normalized chart, slot 3 is physical route 3. Define

\[
M=Y_3D.
\]

Lean proves this is exactly the v0.80 route-3/defect mixed word:

- `normalized_route0_third_defect_matches_v080`.

Transporting \(M\) to any source root gives:

### Ordered AB

\[
\operatorname{ev}(T_{i\leftarrow0}(M))=1,
\qquad
\chi_{\mathrm{perm}}=3.
\]

Lean theorem:

- `canonical_ordered_ab_normalized_groupoid_mixed_wilson`.

### Ordered BA

\[
\operatorname{ev}(T_{i\leftarrow0}(M))=(021),
\qquad
\chi_{\mathrm{perm}}=0.
\]

Lean theorem:

- `canonical_ordered_ba_normalized_groupoid_mixed_wilson`.

Therefore the separator remains exact in every source chart:

- `canonical_normalized_groupoid_mixed_wilson_separates`.

This is a finite exact canonical separator only. It is not asserted to separate arbitrary representations or arbitrary free-groupoid characters.

## Canonical `S3` reconstruction

The runtime reconstructs every normalized chart from route-0 coordinates using

\[
C_{ik}=C_{0i}^{-1}C_{0k},
\qquad
D_i=C_{0i}^{-1}D_0C_{0i}.
\]

The retained profiles are:

- flat four-route atlas,
- single-support atlas,
- ordered AB atlas,
- ordered BA atlas.

All group values are exact permutation triples. No floating-point group calculation is used.

## Confidence policy

MemoryOS v0.81 introduces no new confidence penalty:

\[
P_{\mathrm{groupoid}}=0,
\qquad
C_{v0.81}=C_{v0.80}.
\]

The exact values remain:

- flat: \(1/3\),
- single-support: \(5/18\),
- ordered AB: \(11/54\),
- ordered BA: \(11/54\).

The groupoid and descent records are diagnostic and review-oriented. They are not posterior probabilities, decision rules, ranking scores, physical actions, universal optima, or truth authorities.

## Exact runtime ledger

The certificate contains:

- 6 inherited literature records,
- 12 normalized route-slot records,
- 16 normalized root-chart records,
- 48 normalized coordinate records,
- 16 normalized defect records,
- 64 generator-substitution records,
- 16 identity-law records,
- 256 composition-law records,
- 64 inverse-law records,
- 640 transition/evaluation compatibility records,
- 256 transport-path-independence records,
- 160 word gauge-covariance records,
- 4 normalized mixed-separator records,
- 4 source-confidence preservation records,
- 4 memory-fusion records,
- 8 full-rank transport records,
- 4 singular atomic records,
- 3 rank-one source boundaries.

All confidence values are exact rationals. All free words are deterministic signed-generator lists with exact free reduction.

## Fail-closed checks

The checker rejects:

- edited v0.80 source certificates,
- source schema, digest, collection, or count changes,
- source separator changes,
- route-slot mapping edits,
- identity, composition, or inverse-law edits,
- transition-substitution edits,
- word-evaluation descent edits,
- transport-path-independence edits,
- gauge-covariance edits,
- normalized separator edits,
- confidence edits,
- authority-boundary reversals,
- unexpected truth claims,
- collection digest or record-count mismatches.

## Retention and authority boundary

All v0.80 candidates, histories, quotient-coordinate probes, review sets, dissent records, and minority-protection records are retained.

Full-rank records retain commuting normalized transport and Wilson descent. Singular atomic records retain atomic normalized-chart and groupoid-word signatures without emitting a two-dimensional target density or reconstructing a lost coordinate.

MemoryOS v0.81 remains:

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
