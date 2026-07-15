# MemoryOS v0.77 — rank-two dual cycle bases and spanning-tree change

## Scope

MemoryOS v0.77 extends the finite v0.76 branched-diamond certificate to a finite theta-shaped dual graph with three root-to-target routes and cycle rank two. The layer remains future-only, read-only, and advisory. It does not rank, prune, or select candidates; synthesize or activate plans; issue decision receipts; mutate MemoryOS, DecisionOS, or persistent WORLD state; claim verification; or grant truth authority.

The implementation is a finite exact `S3` certificate. It does not claim a theorem for arbitrary continuum graphs, a universal physical gauge-field interpretation, or a universal statistical optimum.

## Source binding

The runtime regenerates and validates the accepted MemoryOS v0.76 certificate before deriving v0.77. It binds:

- the complete v0.76 certificate digest,
- the branched-dual-graph profile digest,
- the cycle-obstruction digest,
- the target-defect-routing digest,
- the branched-graph-confidence digest,
- all v0.76 source collection counts and authority-boundary fields.

Any source digest, source count, target defect, source confidence, retention set, review set, or authority-boundary change is rejected fail-closed.

## Finite theta dual graph

The graph has root `cell-0`, branch vertices `cell-1`, `cell-2`, and `cell-3`, recombination vertex `cell-4`, six directed dual edges, and three two-edge root-to-target routes.

The route transports are

\[
P_0=J_{01}J_{14},
\qquad
P_1=J_{02}J_{24},
\qquad
P_2=J_{03}J_{34}.
\]

With five vertices and six edges, the connected finite graph has cycle rank

\[
6-5+1=2.
\]

This is a finite certificate statement only.

## Pairwise cycle holonomies

The three pairwise route-comparison holonomies are

\[
C_{01}=P_0P_1^{-1},
\qquad
C_{02}=P_0P_2^{-1},
\qquad
C_{12}=P_1P_2^{-1}.
\]

Only two are independent. Lean proves

\[
\boxed{C_{12}=C_{01}^{-1}C_{02}}
\]

and

\[
\boxed{C_{02}=C_{01}C_{12}}.
\]

Lean theorems:

- `cycle12_eq_cycle01_inv_mul_cycle02`
- `cycle02_eq_cycle01_mul_cycle12`

## Global route agreement

All three paths agree exactly when both route-0 fundamental cycles are trivial:

\[
\boxed{
P_0=P_1=P_2
\iff
C_{01}=1\ \land\ C_{02}=1.
}
\]

Lean theorem:

- `all_paths_agree_iff_fundamental_cycles_identity`

## Spanning-tree cycle bases

When route 0 is selected as the tree route,

\[
B_0=(C_{01},C_{02}).
\]

When route 1 is selected,

\[
B_1=(C_{01}^{-1},C_{12}).
\]

Lean proves the exact finite basis-change rule

\[
\boxed{
B_1=(a^{-1},a^{-1}b)
\quad\text{for}\quad
B_0=(a,b).
}
\]

Lean theorems:

- `tree1_basis_exact_change`
- `tree0_basis_reconstructs_cycle12`
- `tree1_basis_reconstructs_cycle02`

The complete set \((C_{01},C_{02},C_{12})\) is retained so that no selected spanning-tree route becomes truth-authoritative.

## Defect routing over three paths

For a target defect \(D\) at `cell-4`, transport to the common root along each route:

\[
D_i=P_iDP_i^{-1}.
\]

Lean proves

\[
\boxed{D_0=C_{01}D_1C_{01}^{-1}}
\]

\[
\boxed{D_0=C_{02}D_2C_{02}^{-1}}
\]

\[
\boxed{D_1=C_{12}D_2C_{12}^{-1}}.
\]

Lean theorems:

- `localization0_eq_cycle01_conjugate_localization1`
- `localization0_eq_cycle02_conjugate_localization2`
- `localization1_eq_cycle12_conjugate_localization2`

Exact route representatives may differ, while every class-function route signature remains equal to the class signature of the target defect.

## Gauge covariance

The theta graph carries independent frames at all five vertices. Each edge transforms by its source and target frames. Every root-to-target path transforms as

\[
P_i\mapsto g_0^{-1}P_i g_4.
\]

Every pairwise cycle transforms at the root:

\[
C_{ij}\mapsto g_0^{-1}C_{ij}g_0.
\]

Every root-localized target defect transforms as

\[
D_i\mapsto g_0^{-1}D_i g_0.
\]

Lean proves path covariance, cycle covariance, localized-defect covariance, and class-function gauge invariance. The runtime also checks that the spanning-tree basis-change relation commutes with root conjugation.

Key theorems:

- `path0_gauge_covariant`
- `path1_gauge_covariant`
- `path2_gauge_covariant`
- `cycle01_gauge_covariant`
- `cycle02_gauge_covariant`
- `cycle12_gauge_covariant`
- `localized_defect0_gauge_covariant`
- `complete_pairwise_cycle_signature_gauge_invariant`

## Complete pairwise signature

The frame-independent finite signature is

\[
\left(
\chi(C_{01}),
\chi(C_{02}),
\chi(C_{12})
\right).
\]

It is not reduced to the two cycles selected by one spanning tree. Both retained tree bases reconstruct the omitted pairwise cycle exactly. The signature is advisory and does not determine a candidate, action, truth value, or physical field.

## Canonical exact S3 profiles

### Flat theta

\[
P_0=P_1=P_2=(012).
\]

Therefore

\[
C_{01}=C_{02}=C_{12}=1.
\]

Pairwise traces are \((3,3,3)\), the trace sum is `9`, the penalty is `0`, and adjusted confidence is

\[
\frac13.
\]

### Rank-one cycle theta

\[
P_0=1,
\qquad
P_1=(01),
\qquad
P_2=1.
\]

Therefore

\[
C_{01}=(01),
\qquad
C_{02}=1,
\qquad
C_{12}=(01).
\]

The route-0 basis has one nontrivial independent generator. Pairwise traces are \((1,3,1)\), the trace sum is `5`, the penalty is

\[
\frac{2}{27},
\]

and adjusted confidence is

\[
\frac{7}{27}.
\]

### Rank-two noncommuting theta

\[
P_0=1,
\qquad
P_1=(01),
\qquad
P_2=(12).
\]

Therefore

\[
C_{01}=(01),
\qquad
C_{02}=(12),
\qquad
C_{12}=(012).
\]

The route-0 basis is

\[
B_0=((01),(12)),
\]

and the route-1 basis is

\[
B_1=((01),(012)).
\]

The independent basis elements do not commute:

\[
C_{01}C_{02}=(012),
\qquad
C_{02}C_{01}=(021).
\]

Lean theorem:

- `canonical_rank_two_basis_noncommutative`

Pairwise traces are \((1,1,0)\), the trace sum is `2`, the penalty is

\[
\frac{7}{54},
\]

and adjusted confidence is

\[
\frac{11}{54}.
\]

## Advisory confidence convention

The source base confidence remains

\[
C_0=\frac13.
\]

Using the full pairwise cycle signature,

\[
P_\theta
=
\frac{
9-\left[
\chi_{\mathrm{perm}}(C_{01})
+\chi_{\mathrm{perm}}(C_{02})
+\chi_{\mathrm{perm}}(C_{12})
\right]
}{54}.
\]

The adjusted confidence is

\[
C_\theta=C_0-P_\theta.
\]

The symmetric use of all three pairwise cycles prevents the confidence convention from privileging one spanning-tree route. It is not a posterior probability, physical action, universal optimum, decision rule, or truth authority.

Lean theorems:

- `theta_adjusted_confidence_gauge_invariant`
- `theta_adjusted_confidence_mem_unit_interval`
- `canonical_flat_theta_confidence`
- `canonical_rank_one_theta_confidence`
- `canonical_rank_two_theta_confidence`

## Exact runtime ledger

The certificate contains:

- 5 literature records,
- 11 theta-graph incidence records,
- 3 canonical profile records,
- 18 edge-transport records,
- 9 path-transport records,
- 6 spanning-tree cycle-basis records,
- 9 pairwise cycle-holonomy records,
- 3 spanning-tree basis-change records,
- 3 cycle-basis relation records,
- 9 target-defect routing records,
- 9 route-conjugacy relation records,
- 9 route Wilson-signature records,
- 3 complete pairwise cycle-signature records,
- 3 confidence records,
- 3 memory-fusion records,
- 8 full-rank retention records,
- 4 singular atomic retention records,
- 3 rank-one source boundaries.

All group elements are exact permutation triples. All confidence values are exact rationals.

## Fail-closed checker

The checker rejects:

- a modified v0.76 certificate digest,
- modified theta edge transports,
- modified pairwise cycle holonomies,
- a false spanning-tree basis-change claim,
- a false route-conjugacy relation,
- modified confidence values,
- candidate-selection claims,
- unexpected truth claims,
- collection digest mismatches,
- source count mismatches,
- source target-defect changes,
- source authority-boundary changes.

## Retention and authority boundary

The layer preserves all decision candidates, PlanOS histories, quotient-coordinate probes, relational frontier entries, required-review visibility, dissent visibility, minority visibility, full-rank transport records, and singular atomic records.

The layer does not perform candidate ranking, candidate pruning, candidate selection, decision commit, decision receipt issuance, plan synthesis, activation, execution, source deletion, source MemoryOS mutation, DecisionOS mutation, persistent WORLD mutation, verification-result claims, or truth-authority grants.

## Literature grounding

The finite structural choices remain grounded in the primary references already bound by v0.76:

1. arXiv:2604.16252 — dual incidence structures and Wilson-loop composition.
2. arXiv:1006.2059 — gauge-invariant discrete transport on glued simplicial structures.
3. arXiv:hep-lat/0309023 — ordered non-Abelian lattice composition.
4. arXiv:1011.0371 — gauge-covariant defects and holonomy comparison.
5. arXiv:2605.26697 — path-ordered transport and conjugacy-invariant signatures.

These references do not supply the MemoryOS confidence convention or its governance boundary.
