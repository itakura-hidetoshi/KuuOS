# MemoryOS v0.73 — Tetrahedral Plaquette, Bianchi, and Curvature Certificate

## Purpose

MemoryOS v0.73 extends the finite non-Abelian `S3` gauge layer from one three-chart loop to a bounded multi-plaquette lattice cell.

The cell is an oriented tetrahedron with four vertices, six independently stored oriented edges, and four triangular plaquettes. The certificate derives gauge-covariant plaquette holonomies, exact Wilson-loop composition, a finite discrete Bianchi identity, an identity Bianchi defect, a gauge-invariant bounded curvature action, and a curvature-adjusted advisory confidence.

The layer remains future-only, read-only, and advisory.

## Literature grounding

The certificate binds five primary-source directions:

1. `arXiv:2604.16252` — central plaquette actions, Wilson loops, and exact lattice composition.
2. `arXiv:2602.02436` — Wilson-loop observables constructed through gauge-equivariant layers.
3. `arXiv:2501.16955` — gauge-covariant link transport and invariant contractions.
4. `arXiv:1011.0371` — non-Abelian Bianchi identities and gauge-invariant defect interpretation.
5. `arXiv:2605.26697` — path-ordered non-Abelian holonomy and frame covariance.

MemoryOS does not reproduce the physical theories of those papers. It imports only finite algebraic principles that can be checked exactly in `S3`.

## Tetrahedral lattice cell

The vertices are

\[
V=\{0,1,2,3\}.
\]

The six stored oriented edges are

\[
U_{01},\ U_{12},\ U_{23},\ U_{30},\ U_{02},\ U_{13}\in S_3.
\]

Reverse transport is represented by the inverse group element. A local frame is

\[
g=(g_0,g_1,g_2,g_3)\in S_3^4.
\]

Each edge transforms by

\[
U'_{ij}=g_i^{-1}U_{ij}g_j.
\]

For `U30`, the source is vertex `3` and the target is vertex `0`:

\[
U'_{30}=g_3^{-1}U_{30}g_0.
\]

## Plaquette holonomies

The four oriented triangular faces are

\[
\begin{aligned}
H_{012}&=U_{01}U_{12}U_{02}^{-1},\\
H_{023}&=U_{02}U_{23}U_{30},\\
H_{031}&=U_{30}^{-1}U_{13}^{-1}U_{01}^{-1},\\
H_{123}&=U_{12}U_{23}U_{13}^{-1}.
\end{aligned}
\]

The first three are based at vertex `0`; the fourth is based at vertex `1`.

Lean proves

\[
\begin{aligned}
H'_{012}&=g_0^{-1}H_{012}g_0,\\
H'_{023}&=g_0^{-1}H_{023}g_0,\\
H'_{031}&=g_0^{-1}H_{031}g_0,\\
H'_{123}&=g_1^{-1}H_{123}g_1.
\end{aligned}
\]

Thus representatives are frame-dependent, while conjugacy classes and class-function observables are frame-independent.

## Common-basepoint transport

The fourth face is transported from vertex `1` to vertex `0`:

\[
\widetilde H_{123}=U_{01}H_{123}U_{01}^{-1}.
\]

It transforms by conjugation at vertex `0`:

\[
\widetilde H'_{123}=g_0^{-1}\widetilde H_{123}g_0.
\]

## Finite non-Abelian discrete Bianchi identity

The exact tetrahedral identity is

\[
H_{012}H_{023}H_{031}=\widetilde H_{123}.
\]

Expanding the left side gives

\[
\begin{aligned}
&\left(U_{01}U_{12}U_{02}^{-1}\right)
 \left(U_{02}U_{23}U_{30}\right)
 \left(U_{30}^{-1}U_{13}^{-1}U_{01}^{-1}\right)\\
&\qquad=U_{01}U_{12}U_{23}U_{13}^{-1}U_{01}^{-1}\\
&\qquad=U_{01}H_{123}U_{01}^{-1}.
\end{aligned}
\]

The cancellation is order-sensitive and is not an Abelian sum rule. Lean proves this identity for every group-valued tetrahedron connection.

## Bianchi defect

The closed ordered defect is

\[
D_B=H_{012}H_{023}H_{031}\widetilde H_{123}^{-1}.
\]

Lean proves

\[
D_B=e
\]

and

\[
D'_B=g_0^{-1}D_Bg_0.
\]

The runtime records both original and transformed defects and fails closed if either differs from the identity.

## Wilson composition

For any class function

\[
\chi(g^{-1}hg)=\chi(h),
\]

define

\[
W_B=\chi(H_{012}H_{023}H_{031}).
\]

The Bianchi identity and conjugacy invariance imply

\[
W_B=\chi(H_{123}).
\]

Lean proves this for every group and every class function.

## Canonical finite profiles

### Flat profile

All six edge variables are the identity. All plaquettes, the Bianchi product, the transported fourth face, and the Bianchi defect are the identity. The curvature action is zero.

### Curved profile

The canonical non-Abelian profile is

\[
U_{01}=(01),\quad U_{12}=(12),\quad U_{23}=(01),\quad
U_{30}=U_{02}=U_{13}=e.
\]

Its four face holonomies are

\[
H_{012}=(012),\quad H_{023}=(01),\quad H_{031}=(01),\quad H_{123}=(021).
\]

The ordered product and transported fourth face are both

\[
H_{012}H_{023}H_{031}=\widetilde H_{123}=(012).
\]

The Bianchi defect remains the identity even though every individual face is nontrivial. The permutation-representation traces are `(0,1,1,0)`.

## Identity-class curvature action

The formal certificate uses the bounded class function

\[
\chi_{\mathrm{id}}(h)=
\begin{cases}
3,&h=e,\\
0,&h\ne e.
\end{cases}
\]

For each face,

\[
P_f=\frac{3-\chi_{\mathrm{id}}(H_f)}{18}.
\]

The tetrahedral action is

\[
A_{\mathrm{tet}}=\frac{P_{012}+P_{023}+P_{031}+P_{123}}{4}.
\]

Lean proves

\[
A_{\mathrm{tet}}(U^g)=A_{\mathrm{tet}}(U).
\]

Canonical values:

- flat profile: `0`;
- curved profile: `1/6`.

This is a bounded MemoryOS certificate convention, not the physical Yang–Mills action, a continuum field theory, or a universal statistical optimum.

## Curvature-adjusted confidence

The source confidence inherited from v0.72 is

\[
C_0=\frac12.
\]

The advisory confidence is

\[
C_{\mathrm{tet}}=C_0-A_{\mathrm{tet}}.
\]

Canonical values:

- flat profile: `1/2`;
- curved profile: `1/3`.

Lean proves gauge invariance and proves membership in `[0,1]` under explicit nonnegativity and bounded-action assumptions. The action does not rank, prune, or select candidates.

## Exact runtime ledgers

- literature records: `5`
- tetrahedron vertex-frame records: `4`
- oriented edge records: `12`
- transformed edge records: `12`
- plaquette holonomy records: `8`
- tetrahedral Bianchi records: `2`
- Wilson composition records: `2`
- curvature action records: `2`
- tetrahedral fusion records: `2`
- full-rank transport records: `8`
- singular atomic records: `4`
- rank-one source boundaries: `3`

## Fail-closed checks

The checker rejects:

- v0.72 certificate-digest tampering;
- modified plaquette holonomies;
- a nonidentity Bianchi defect;
- false Wilson-composition values;
- modified curvature action or adjusted confidence;
- physical Yang–Mills action claims;
- candidate-selection claims;
- unexpected claims.

Every emitted collection has a canonical SHA-256 digest.

## Singular boundary

The layer preserves atomic plaquette signatures, atomic Bianchi-boundary receipts, all rank-one source boundaries, all retained candidate IDs, both PlanOS histories, all nine quotient-coordinate probes, and all review/dissent/minority-protection sets.

It does not reconstruct lost coordinates or emit a two-dimensional target density at a singular boundary.

## Authority boundary

The layer does not rank, prune, or select candidates; synthesize plans; commit decisions; issue receipts; activate tools; execute actions; delete source records; mutate DecisionOS or persistent WORLD state; claim a continuum lattice gauge field; claim a physical Yang–Mills action; claim a universal Bianchi theorem beyond the finite tetrahedral model; or claim verification/truth authority.

## Formal root

`formal/KuuOSMemoryOSV0_73.lean`

## Runtime root

`runtime/kuuos_memoryos_tetrahedral_bianchi_curvature_certificate_kernel_v0_1.py`

## Checker

`scripts/check_planos_memoryos_tetrahedral_bianchi_curvature_certificate_kernel_v0_1.py`
