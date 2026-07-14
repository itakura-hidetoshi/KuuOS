# MemoryOS v0.74 — Dual 2-complex shared-face gluing and lattice Stokes certificate

## Status

This layer advances the finite non-Abelian MemoryOS gauge line from one
tetrahedral cell to two tetrahedral cells glued across a shared oriented face.

The implementation is finite, exact, read-only, and advisory. It uses the
finite group `S3`; it does not claim a continuum dual complex, a physical
Yang–Mills model, or a universal non-Abelian Stokes theorem.

## Source frontier

- source: MemoryOS v0.73
- source runtime:
  `runtime/kuuos_memoryos_tetrahedral_bianchi_curvature_certificate_kernel_v0_1.py`
- source formal root:
  `formal/KuuOSMemoryOSV0_73.lean`
- inherited curved-cell confidence: `1/3`

The source certificate is regenerated and validated before the v0.74
certificate can be issued. Source collection digests, record counts, candidate
IDs, history IDs, quotient probes, dissent sets, review sets, and minority
protection sets remain bound.

## Literature grounding

The implementation is informed by:

1. `arXiv:2604.16252`, *Universal dualities for Wilson loops in lattice
   Yang-Mills*: dual incidence graphs, decorated spanning surfaces, and
   Wilson-loop composition.
2. `arXiv:1006.2059`, *A simplicial gauge theory*: gauge-invariant discrete
   actions on glued simplicial meshes.
3. `arXiv:hep-lat/0309023`, *On the non-Abelian Stokes theorem for SU(2)
   gauge fields*: ordered lattice surface composition.
4. `arXiv:1011.0371`, *Non abelian Bianchi identities, monopoles and gauge
   invariance*: gauge-covariant defect interpretation.
5. `arXiv:2605.26697`, *A Gauge-Covariant Theoretical Framework for
   Non-Abelian Holonomy Estimation*: path-ordered transport and conjugacy
   invariance.

These references motivate the mathematical organization. The exact MemoryOS
penalty and confidence update are local certificate conventions.

## Dual 2-complex

The primal complex consists of two oriented tetrahedral 3-cells:

- `cell-left`
- `cell-right`

They meet on one shared primal 2-face. The corresponding dual complex has:

- two dual vertices, one for each tetrahedral cell;
- one dual edge crossing the shared primal face.

The dual edge carries a seam transport `J`. It compares the two cell
basepoints without identifying their local frames.

## Cell boundary data

For one tetrahedral connection `U`, define

\[
O(U)=H_{012}(U)H_{023}(U)H_{031}(U)
\]

and

\[
S(U)=U_{01}H_{123}(U)U_{01}^{-1}.
\]

MemoryOS v0.73 proves the cellwise Bianchi identity

\[
O(U)=S(U).
\]

For a glued pair `(L,R,J)`, transport the right data to the left basepoint:

\[
O_R^J=J O(R) J^{-1},
\qquad
S_R^J=J S(R) J^{-1}.
\]

## Shared-face gluing

Opposite-orientation compatibility is

\[
S_R^J=S(L)^{-1}.
\]

The seam gluing defect is

\[
D_{\mathrm{seam}}=S(L)S_R^J.
\]

Thus a compatible seam has

\[
D_{\mathrm{seam}}=1.
\]

The certificate does not delete either shared-face record. It retains both
local holonomies and the dual-edge transport.

## Lattice Stokes composition

The outer boundary holonomy of the glued two-cell complex is

\[
H_{\partial}=O(L)O_R^J.
\]

Using the two cellwise Bianchi identities,

\[
\boxed{
H_{\partial}=D_{\mathrm{seam}}.
}
\]

This is the exact defect-propagation theorem of v0.74. Local cell Bianchi
defects can remain trivial while a seam mismatch appears on the global outer
boundary.

For an opposite-orientation compatible seam,

\[
H_{\partial}=1.
\]

This finite closure is called lattice Stokes composition in this certificate.

## Gauge covariance

Let the left and right tetrahedra have independent local gauge frames. The
dual-edge transport transforms as

\[
J\mapsto g_L^{-1}Jg_R.
\]

Then

\[
D_{\mathrm{seam}}\mapsto
g_L^{-1}D_{\mathrm{seam}}g_L
\]

and

\[
H_{\partial}\mapsto
g_L^{-1}H_{\partial}g_L.
\]

Therefore any class-function Wilson observable of the global boundary is
frame independent.

## Canonical exact profiles

Both cells use the v0.73 curved `S3` tetrahedron, whose transported shared
face and outer boundary are

\[
S(L)=S(R)=O(L)=O(R)=(012).
\]

### Compatible curved profile

Choose

\[
J=(01).
\]

Conjugation reverses the 3-cycle:

\[
J(012)J^{-1}=(021)=(012)^{-1}.
\]

Hence

\[
D_{\mathrm{seam}}=1,
\qquad
H_{\partial}=1.
\]

The permutation-representation boundary trace is `3`.

### Mismatched curved profile

Choose

\[
J=1.
\]

Then

\[
D_{\mathrm{seam}}=(012)^2=(021),
\]

and exact defect propagation gives

\[
H_{\partial}=(021).
\]

Both individual tetrahedral Bianchi defects remain the identity. The global
defect comes only from the shared-face mismatch.

The permutation-representation boundary trace is `0`.

## Confidence convention

The inherited v0.73 confidence is

\[
C_0=\frac13.
\]

Define the class-function gluing penalty

\[
P_{\mathrm{glue}}
=
\frac{3-\chi_{\mathrm{perm}}(H_{\partial})}{18}.
\]

Therefore:

- compatible curved profile:
  \[
  P_{\mathrm{glue}}=0,\qquad C=\frac13;
  \]
- mismatched curved profile:
  \[
  P_{\mathrm{glue}}=\frac16,\qquad C=\frac16.
  \]

The penalty is gauge invariant because it depends only on a class function of
the propagated boundary defect. It is not a posterior probability or a
universal statistical optimum.

## Exact runtime ledgers

The runtime emits:

- 5 literature records;
- 3 dual-incidence records;
- 4 glued-cell records;
- 4 shared-face records;
- 2 dual-edge transport records;
- 2 shared-face gluing records;
- 2 lattice Stokes records;
- 2 Bianchi-defect propagation records;
- 2 dual-boundary Wilson records;
- 2 confidence records;
- 2 memory-fusion records;
- 8 full-rank transport records;
- 4 singular atomic records;
- 3 rank-one source boundaries.

All group elements are exact permutation triples. All confidence values are
exact rationals.

## Fail-closed checks

The checker rejects:

- source v0.73 digest changes;
- dual-edge transport changes;
- altered propagated boundary holonomy;
- a mismatched seam falsely marked compatible;
- altered confidence values;
- candidate selection claims;
- unexpected claims.

## Authority boundary

This layer does not:

- rank, prune, or select candidates;
- delete or rewrite source records;
- synthesize plans;
- commit decisions or issue decision receipts;
- activate tools;
- execute actions;
- mutate persistent WORLD state;
- claim verification authority;
- claim truth authority.

The layer is future-only, read-only, and advisory.
