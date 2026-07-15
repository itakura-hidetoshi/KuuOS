# MemoryOS v0.79 — free-group Nielsen words and mixed Wilson separation

## Scope

MemoryOS v0.79 extends the finite four-route atlas of v0.78 with a formal free-group word layer. The new layer treats the three route-0 cycle coordinates and the route-0 localized target defect as four labeled generators, evaluates arbitrary words in any target group, formalizes the v0.78 rooted rebase as an involutive Nielsen substitution, and introduces a mixed cycle-defect Wilson word that resolves the canonical ordered-AB / ordered-BA ambiguity left by the cycle-only class signature.

The layer remains future-only, read-only, and advisory. It does not rank, prune, select, commit, activate, execute, mutate, verify, or grant truth authority.

The implementation is a finite exact `S3` certificate plus arbitrary-group Lean algebra. It does not claim a universal classification of free-group representations, a universal separating family of Wilson words, a continuum gauge-field theorem, or a physical inference result.

## Source binding

The runtime regenerates and validates the accepted MemoryOS v0.78 certificate before deriving v0.79. It binds:

- the complete v0.78 certificate digest,
- all v0.78 collection digests and record counts,
- the four canonical profile order,
- route-0 rooted coordinates,
- the complete six-cycle trace signatures,
- the route-0 localized target defect,
- exact source confidence values,
- candidate, history, probe, review, dissent, and minority-retention sets,
- the v0.78 authority boundary.

Any source digest edit, collection edit, canonical-coordinate edit, target-defect edit, confidence edit, retention edit, or authority-boundary reversal is rejected fail-closed.

## Formal free-group generators

The rooted word atlas retains four labeled generators:

\[
X_1=C_{01},\qquad
X_2=C_{02},\qquad
X_3=C_{03},\qquad
D=D_0.
\]

Here

\[
D_0=P_0 D_{\mathrm{target}}P_0^{-1}
\]

is the target defect localized at the common root along route 0.

Lean defines:

- `AtlasWordGenerator.cycle01`,
- `AtlasWordGenerator.cycle02`,
- `AtlasWordGenerator.cycle03`,
- `AtlasWordGenerator.defect0`,
- `atlasWordAssignment`,
- `evalAtlasWord`.

The evaluation map is the canonical homomorphism

\[
\operatorname{ev}_{A,D}:F(X_1,X_2,X_3,D)\longrightarrow G
\]

constructed with `FreeGroup.lift`.

Lean theorem:

- `eval_atlas_word_generator`.

## Canonical retained words

The exact runtime retains ten words:

1. \(X_1\),
2. \(X_2\),
3. \(X_3\),
4. \(D\),
5. \(X_1D\),
6. \(X_2D\),
7. \(X_3D\),
8. \(DX_3\),
9. \([X_1,X_2]=X_1X_2X_1^{-1}X_2^{-1}\),
10. \([X_2,X_1]=X_2X_1X_2^{-1}X_1^{-1}\).

Exact group representatives are retained even when a class function identifies them. Exact representatives are frame-dependent; their class-function values are gauge invariant.

## Elementary Nielsen decomposition

The v0.78 rooted-coordinate change is

\[
T(a,b,c)=\left(a^{-1},a^{-1}b,a^{-1}c\right).
\]

v0.79 decomposes this into three elementary moves:

\[
(a,b,c)
\xrightarrow{I_1}
(a^{-1},b,c)
\xrightarrow{L_{12}}
(a^{-1},a^{-1}b,c)
\xrightarrow{L_{13}}
(a^{-1},a^{-1}b,a^{-1}c).
\]

Lean definitions:

- `nielsenInvertFirst`,
- `nielsenLeftMultiplySecond`,
- `nielsenLeftMultiplyThird`.

Lean theorem:

- `rebase_at_first_eq_elementary_nielsen_moves`.

## Universal Nielsen substitution

The corresponding substitution on free generators is

\[
\begin{aligned}
X_1&\longmapsto X_1^{-1},\\
X_2&\longmapsto X_1^{-1}X_2,\\
X_3&\longmapsto X_1^{-1}X_3,\\
D&\longmapsto D.
\end{aligned}
\]

Lean defines the generator substitution `nielsenRebaseGenerator` and extends it uniquely to the homomorphism

\[
N:F(X_1,X_2,X_3,D)\to F(X_1,X_2,X_3,D)
\]

using `FreeGroup.lift`.

Lean proves the global identity

\[
\boxed{N\circ N=\operatorname{id}}
\]

on the entire free group, not only on the ten retained runtime words.

Lean theorems:

- `nielsen_rebase_hom_generator`,
- `nielsen_rebase_hom_comp_self`,
- `nielsen_rebase_word_involutive`.

## Evaluation compatibility

For rooted coordinates \(A=(a,b,c)\), rooted defect \(d\), and any free-group word \(w\), Lean proves

\[
\boxed{
\operatorname{ev}_{A,d}(Nw)
=
\operatorname{ev}_{T(A),d}(w).
}
\]

Thus word substitution before evaluation agrees exactly with evaluating the same word under the rebased generator assignment.

Lean theorem:

- `nielsen_rebase_evaluation_compatibility`.

The runtime checks this relation for all ten retained words in all four canonical profiles, producing 40 exact compatibility records.

## Arbitrary-word gauge covariance

Suppose every root observable transforms by the same root frame:

\[
A(x)\longmapsto g_0^{-1}A(x)g_0.
\]

For every free-group word \(w\), Lean proves

\[
\boxed{
\operatorname{ev}_{g_0^{-1}Ag_0}(w)
=
g_0^{-1}\operatorname{ev}_{A}(w)g_0.
}
\]

This is proved by identifying both sides as homomorphisms out of the free group and applying free-group extensionality on generators.

The four atlas generators satisfy the common root-frame transformation because v0.78 already proves covariance for `cycle01`, `cycle02`, `cycle03`, and `localizedDefect0`.

Lean theorems:

- `free_word_evaluation_conjugation_covariant`,
- `atlas_word_assignment_gauge_covariant`,
- `eval_atlas_word_gauge_covariant`.

For any class function \(\chi\),

\[
W_{\chi,w}(A,D)=\chi(\operatorname{ev}_{A,D}(w))
\]

is gauge invariant.

Lean theorem:

- `atlas_word_wilson_gauge_invariant`.

## Resolution hierarchy

### Level 1: cycle-only class signature

v0.78 records the complete six-cycle trace signature

\[
\left(
\chi(C_{01}),\chi(C_{02}),\chi(C_{03}),
\chi(C_{12}),\chi(C_{13}),\chi(C_{23})
\right).
\]

For both canonical mirrored profiles this equals

\[
(1,1,0,0,1,1).
\]

Therefore the cycle-only class signature does not separate ordered AB from ordered BA.

Lean theorem:

- `canonical_cycle_only_signature_limit`.

### Level 2: exact commutator representative

For the commutator word

\[
K=[X_1,X_2],
\]

Lean proves

\[
\operatorname{ev}_{AB}(K)=(021),
\qquad
\operatorname{ev}_{BA}(K)=(012).
\]

The exact representatives differ. However both are 3-cycles, so their permutation traces are both zero. A single commutator class trace still does not separate the two profiles.

Lean theorems:

- `canonical_ordered_commutator_values`,
- `canonical_ordered_commutator_exactly_differs`,
- `canonical_ordered_commutator_wilson_limit`.

### Level 3: mixed cycle-defect Wilson word

Define

\[
M=X_3D.
\]

For ordered AB,

\[
X_3=(021),\qquad D=(012),
\]

hence

\[
\operatorname{ev}_{AB}(M)=1,
\qquad
\chi_{\mathrm{perm}}(\operatorname{ev}_{AB}(M))=3.
\]

For ordered BA,

\[
X_3=(012),\qquad D=(012),
\]

hence

\[
\operatorname{ev}_{BA}(M)=(021),
\qquad
\chi_{\mathrm{perm}}(\operatorname{ev}_{BA}(M))=0.
\]

Therefore

\[
\boxed{
W_{\mathrm{perm},X_3D}(AB)=3\ne0=W_{\mathrm{perm},X_3D}(BA).
}
\]

This separator is gauge invariant because it is the class function of a jointly conjugated mixed word.

Lean theorems:

- `canonical_ordered_mixed_word_values`,
- `canonical_ordered_ab_mixed_wilson`,
- `canonical_ordered_ba_mixed_wilson`,
- `canonical_ordered_mixed_wilson_separates`.

This is a finite exact canonical separation only. v0.79 does not claim that this word separates arbitrary representations or arbitrary route atlases.

## Canonical exact S3 profiles

The mixed signature uses the ordered word list

\[
(X_1D,\ X_2D,\ X_3D,\ [X_1,X_2]).
\]

### Flat four-route atlas

Mixed traces:

\[
(0,0,0,3).
\]

Source adjusted confidence remains

\[
\frac13.
\]

### Single-support atlas

Mixed traces:

\[
(1,0,0,3).
\]

Source adjusted confidence remains

\[
\frac5{18}.
\]

### Ordered AB atlas

Mixed traces:

\[
(1,1,3,0).
\]

Source adjusted confidence remains

\[
\frac{11}{54}.
\]

### Ordered BA atlas

Mixed traces:

\[
(1,1,0,0).
\]

Source adjusted confidence remains

\[
\frac{11}{54}.
\]

## Confidence policy

v0.79 introduces no new confidence penalty:

\[
P_{\mathrm{word}}=0.
\]

For every canonical profile,

\[
C_{v0.79}=C_{v0.78}.
\]

The mixed-word separator is diagnostic and review-oriented. It is not converted into a ranking score, posterior probability, decision criterion, physical action, universal optimum, or truth authority.

## Exact runtime ledger

The certificate contains:

- 6 literature records,
- 4 free-group generator records,
- 10 canonical word records,
- 3 elementary Nielsen-move records,
- 4 generator-substitution records,
- 10 word-involution records,
- 40 exact word-evaluation records,
- 40 Nielsen evaluation-compatibility records,
- 40 gauge-covariance records,
- 4 mixed Wilson signatures,
- 2 order-separation records,
- 4 source-confidence preservation records,
- 4 memory-fusion records,
- 8 full-rank transport records,
- 4 singular atomic records,
- 3 rank-one source boundaries.

All group values are exact permutation triples. All confidence values are exact rationals. All words are explicit signed-generator lists with deterministic free reduction.

## Fail-closed checks

The checker rejects:

- edited v0.78 source certificates,
- source schema, digest, collection, or count changes,
- canonical rooted-coordinate changes,
- source target-defect or route-0 localization changes,
- Nielsen substitution edits,
- involution edits,
- word-evaluation edits,
- evaluation-compatibility edits,
- gauge-covariance edits,
- mixed-signature edits,
- order-separation edits,
- confidence mutation,
- authority-boundary reversals,
- unexpected truth claims,
- collection digest or record-count mismatches.

## Retention behavior

All v0.78 decision candidates, histories, quotient-coordinate probes, review sets, dissent records, and minority-protection records are retained.

For full-rank transport records, v0.79 records that free-word evaluation, Nielsen substitution, and mixed Wilson signatures commute with the existing transport layer.

For singular atomic records, v0.79 retains atomic free-word and mixed-word signatures without emitting a two-dimensional target density or reconstructing a lost coordinate.

## Authority boundary

MemoryOS v0.79 remains:

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
