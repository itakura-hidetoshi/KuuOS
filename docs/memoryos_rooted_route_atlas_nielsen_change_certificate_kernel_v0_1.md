# MemoryOS v0.78 — rooted route atlases and Nielsen change

## Scope

MemoryOS v0.78 extends the finite v0.77 theta graph from three routes and cycle rank two to a finite four-route dual atlas with cycle rank three. The layer is future-only, read-only, and advisory. It does not rank, prune, or select candidates; synthesize or activate plans; issue decision receipts; mutate source MemoryOS, DecisionOS, or persistent WORLD state; claim verification; or grant truth authority.

The formal group identities are proved for arbitrary groups. Canonical profiles and the runtime certificate remain finite exact `S3` constructions. No continuum graph theorem, universal fundamental-group theorem, physical gauge-field inference, or statistical optimality claim is made.

## Source binding

The runtime regenerates and validates the accepted MemoryOS v0.77 certificate before deriving v0.78. It binds the complete v0.77 certificate digest, source collection digests and counts, the theta profile order, target defect, base confidence, retention sets, review sets, and authority-boundary fields.

Any source digest, source count, source profile, source target defect, source confidence, retention set, or authority-boundary change is rejected fail-closed.

## Four-route dual atlas

The finite graph has:

- root `cell-0`,
- branch vertices `cell-1` through `cell-4`,
- recombination vertex `cell-5`,
- eight directed dual edges,
- four two-edge root-to-target routes.

The path transports are

\[
P_0=J_{01}J_{15},\quad
P_1=J_{02}J_{25},\quad
P_2=J_{03}J_{35},\quad
P_3=J_{04}J_{45}.
\]

Its finite graph cycle rank is

\[
8-6+1=3.
\]

Lean theorem:

- `four_route_cycle_rank`

## Route-cycle cocycle

For route transports \(P_i\), define

\[
C_{ij}=P_iP_j^{-1}.
\]

Lean proves for arbitrary groups:

\[
C_{ik}=C_{ij}C_{jk},
\qquad
C_{ji}=C_{ij}^{-1},
\qquad
C_{ii}=1.
\]

Key theorem:

- `route_cycle_cocycle`
- `route_cycle_symm`
- `route_cycle_refl`

For the four-route atlas:

\[
C_{12}=C_{01}^{-1}C_{02},
\]

\[
C_{13}=C_{01}^{-1}C_{03},
\]

\[
C_{23}=C_{02}^{-1}C_{03}.
\]

## Rooted coordinates

With route 0 as root, retain the three coordinates

\[
A_0=(C_{01},C_{02},C_{03})=(a,b,c).
\]

With route 1 as root, ordered toward routes 0, 2, and 3,

\[
A_1=(C_{10},C_{12},C_{13}).
\]

Lean proves the exact Nielsen-type root-change rule

\[
\boxed{
(a,b,c)\longmapsto
(a^{-1},a^{-1}b,a^{-1}c)
}
\]

through:

- `root1_coordinates_exact_change`

The same transformation is involutive:

\[
T(T(a,b,c))=(a,b,c).
\]

Lean theorem:

- `rebase_at_first_involutive`

No rooted atlas is treated as authoritative. Both rooted coordinate records and all six pairwise cycle holonomies are retained.

## Global path agreement

Lean proves

\[
P_0=P_1=P_2=P_3
\iff
C_{01}=C_{02}=C_{03}=1.
\]

Lean theorem:

- `all_four_paths_agree_iff_root0_coordinates_identity`

## Defect routing

For a target defect \(D\), define

\[
D_i=P_iDP_i^{-1}.
\]

For any two routes,

\[
D_i=C_{ij}D_jC_{ij}^{-1}.
\]

Lean proves the generic identity and the route-0 specializations:

- `localized_defect_relation`
- `localization0_eq_cycle01_conjugate_localization1`
- `localization0_eq_cycle02_conjugate_localization2`
- `localization0_eq_cycle03_conjugate_localization3`

Every class-function route signature equals the target-defect class signature. Exact representatives remain frame-dependent and are retained.

## Gauge covariance

The six graph vertices carry independent local frames. Every route transforms as

\[
P_i\mapsto g_0^{-1}P_i g_5.
\]

Every pairwise route cycle transforms at the root:

\[
C_{ij}\mapsto g_0^{-1}C_{ij}g_0.
\]

Every rooted defect transforms as

\[
D_i\mapsto g_0^{-1}D_i g_0.
\]

The rooted Nielsen change commutes with this common root conjugation. Lean proves all four path covariance theorems, all six pairwise cycle covariance theorems, rooted-defect covariance, complete class-signature invariance, and advisory confidence invariance.

## Complete six-cycle signature

The retained frame-independent class signature is

\[
\bigl(
\chi(C_{01}),
\chi(C_{02}),
\chi(C_{03}),
\chi(C_{12}),
\chi(C_{13}),
\chi(C_{23})
\bigr).
\]

It is never reduced to a selected tree basis. The exact rooted coordinate records are retained alongside the class signature, because class functions cannot resolve all noncommutative word order.

Lean theorem:

- `complete_pairwise_cycle_signature_gauge_invariant`

## Canonical exact S3 profiles

### Flat four-route atlas

\[
P_0=P_1=P_2=P_3=(012).
\]

Rooted coordinates:

\[
(1,1,1).
\]

All six cycle traces are `3`; trace sum is `18`; penalty is `0`; adjusted confidence is

\[
\frac13.
\]

### Single-support atlas

\[
(P_0,P_1,P_2,P_3)=(1,(01),1,1).
\]

Rooted coordinates:

\[
((01),1,1).
\]

The six cycle traces are

\[
(1,3,3,1,1,3).
\]

Trace sum is `12`; penalty is

\[
\frac1{18};
\]

adjusted confidence is

\[
\frac5{18}.
\]

### Ordered AB atlas

\[
(P_0,P_1,P_2,P_3)=(1,(01),(12),(012)).
\]

Rooted coordinates are

\[
((01),(12),(021)).
\]

The first two coordinates do not commute:

\[
(01)(12)=(012)\neq(021)=(12)(01).
\]

The six cycle traces are

\[
(1,1,0,0,1,1).
\]

Trace sum is `4`; penalty is

\[
\frac7{54};
\]

adjusted confidence is

\[
\frac{11}{54}.
\]

### Ordered BA atlas

\[
(P_0,P_1,P_2,P_3)=(1,(12),(01),(021)).
\]

Rooted coordinates are

\[
((12),(01),(012)).
\]

The exact rooted coordinate record differs from the ordered AB atlas, while the complete six-cycle class trace signature is again

\[
(1,1,0,0,1,1).
\]

This is the explicit class-function resolution limit recorded by v0.78.

Lean theorems:

- `canonical_ordered_exact_coordinates_differ`
- `canonical_ordered_ab_noncommutative`
- `canonical_ordered_class_signature_limit`

## Advisory confidence

Using the complete six-cycle trace sum,

\[
P_{\mathrm{atlas}}
=
\frac{
18-\sum_{0\le i<j\le3}\chi_{\mathrm{perm}}(C_{ij})
}{108}.
\]

The adjusted confidence is

\[
C_{\mathrm{atlas}}=\frac13-P_{\mathrm{atlas}}.
\]

This convention is symmetric over all six pairwise route cycles and does not privilege a root route. It is not a posterior probability, decision rule, physical action, universal optimum, or truth authority.

Lean theorems:

- `route_atlas_adjusted_confidence_gauge_invariant`
- `route_atlas_adjusted_confidence_mem_unit_interval`
- `canonical_flat_confidence`
- `canonical_single_support_confidence`
- `canonical_ordered_ab_confidence`
- `canonical_ordered_ba_confidence`

## Exact runtime ledger

The certificate contains:

- 5 literature records,
- 14 incidence records,
- 4 canonical profile records,
- 32 edge-transport records,
- 16 path-transport records,
- 8 rooted-coordinate records,
- 24 pairwise-cycle records,
- 4 Nielsen-rebase records,
- 4 cocycle-relation records,
- 16 target-defect routing records,
- 12 route-defect relation records,
- 16 route-Wilson records,
- 4 complete six-cycle signatures,
- 4 confidence records,
- 4 fusion records,
- 8 full-rank transport records,
- 4 singular atomic records,
- 3 rank-one source boundaries.

All permutations are exact triples and all confidence values are exact rationals.

## Fail-closed checks

The checker rejects:

- edited v0.77 source certificates,
- source digest or source collection changes,
- rooted-coordinate edits,
- Nielsen rebase edits,
- pairwise-cycle signature edits,
- confidence edits,
- authority-boundary reversals,
- unexpected truth claims,
- collection digest or record-count mismatches.

## Authority boundary

MemoryOS v0.78 remains:

- future-only,
- read-only,
- advisory,
- non-ranking,
- non-pruning,
- non-selecting,
- non-activating,
- non-executing,
- non-mutating,
- non-verifying,
- non-truth-authoritative.
