# PlanOS v1.23 — finite Physical Quantum Qi coherence kernel and partial dephasing certificate v0.1

## Purpose

PlanOS v1.21 retained the complete finite path-history ensemble. PlanOS v1.22 added exact `Z4` phase, Gaussian integer amplitudes, homotopy-class amplitudes, and the fully coherent and fully homotopy-block-dephased endpoint cases.

PlanOS v1.23 fills the exact finite interval between those cases. It constructs a finite Hermitian coherence kernel over retained path histories and evaluates a bounded rational partial-dephasing trajectory without selecting, ranking, pruning, activating, or executing any history.

The structural intent is:

```text
uncertainty is not reduced to one best branch
interference is not reduced to one scalar score
decoherence is not treated as deletion
mixedness is retained as an exact finite observable
```

## Retained history amplitude

Each retained history `gamma` carries a positive integer weight numerator, a phase in `Z4`, terminal state, homotopy class, coherence block, source v1.22 history digest, source plan digest, and source homotopy witness digest.

The exact Gaussian amplitude is

\[
a_\gamma=w_\gamma i^{\phi_\gamma}\in\mathbb Z[i].
\]

No floating-point complex arithmetic is used.

## Endpoint-coherent Gram kernel

For two retained histories,

\[
G_{\gamma\eta}=
\begin{cases}
a_\gamma\overline{a_\eta},&\text{when terminal states agree},\\
0,&\text{otherwise}.
\end{cases}
\]

This preserves terminal alternatives as distinct sectors while retaining phase relations among histories reaching the same terminal state. Every real and imaginary matrix entry is recomputed.

Hermiticity is checked exactly:

\[
G_{\gamma\eta}=\overline{G_{\eta\gamma}}.
\]

The kernel is constructed endpoint-wise as a Gram kernel. Positivity is therefore carried by construction rather than inferred from floating-point eigenvalues.

## Homotopy-block kernel

Let `Delta(G)` retain entries only when both histories have the same terminal state and the same coherence block, and set all other entries to zero.

The certificate requires a one-to-one binding between finite homotopy-class labels and coherence-block labels. This is a digest-bound finite partition, not a global homotopy classification theorem.

## Exact rational partial dephasing

Choose a positive integer denominator `d` and a strictly decreasing finite sequence

\[
d=n_0>n_1>\cdots>n_r=0.
\]

At numerator `n`, define

\[
H_n=nG+(d-n)\Delta(G),
\qquad
K_n=\frac{H_n}{d}.
\]

Equivalently:

```text
same terminal and same block: scale by d
same terminal and different block: scale by n
different terminal: zero
```

The sequence begins at the endpoint-coherent Gram kernel and ends at the homotopy-block kernel. No physical-time interpretation is attached to `n/d`.

## Trace, purity, and mixedness

Let

\[
M=\sum_\gamma |a_\gamma|^2=\sum_\gamma w_\gamma^2.
\]

Every step has trace numerator `dM`, and the normalized finite kernel uses denominator `dM`.

Let

\[
B=\sum_{\text{endpoint, block}}
\left(\sum_{\gamma\in\text{block}}|a_\gamma|^2\right)^2
\]

and

\[
C=\sum_{\text{endpoint}}
\left(\sum_{\gamma\to\text{endpoint}}|a_\gamma|^2\right)^2-B.
\]

The exact Hilbert–Schmidt purity numerator is

\[
P_n=d^2B+n^2C,
\]

with common squared denominator

\[
(dM)^2.
\]

The exact quadratic mixedness numerator is

\[
Q_n=(dM)^2-P_n.
\]

This is not von Neumann entropy and evaluates no logarithm.

For a decreasing numerator sequence, the checker verifies:

```text
trace is constant
cross-block coherence is nonincreasing
purity is nonincreasing
quadratic mixedness is nondecreasing
```

## Coarse readout intensity

For each terminal sector, let `I_pre` be fully coherent intensity and `I_post` be homotopy-block-dephased intensity. At numerator `n`,

\[
R_n=nI_{\mathrm{pre}}+(d-n)I_{\mathrm{post}}.
\]

Its denominator is `d`. This is an interference observable, not candidate utility, preference, ranking, or execution authority.

## Reference fixture

The four v1.22 histories remain unchanged:

```text
alpha direct: weight 2, phase 0, amplitude 2
beta direct:  weight 2, phase 2, amplitude -2
alpha rejoin: weight 1, phase 1, amplitude i
beta rejoin:  weight 1, phase 3, amplitude -i
```

They all reach the same terminal state. The homotopy-block amplitudes are

\[
A_\alpha=2+i,
\qquad
A_\beta=-2-i.
\]

The incoherent mass is

\[
M=2^2+2^2+1^2+1^2=10.
\]

The endpoint Gram Hilbert–Schmidt numerator is `100`. Each homotopy block has mass five, so

\[
B=5^2+5^2=50,
\qquad
C=100-50=50.
\]

For

\[
d=2,
\qquad
n\in[2,1,0],
\]

the exact trajectory is:

| `n/d` | purity | quadratic mixedness | cross-block coherence numerator | readout numerator / denominator |
|---|---:|---:|---:|---:|
| `2/2` | `400/400 = 1` | `0/400 = 0` | `200` | `0/2` |
| `1/2` | `250/400 = 5/8` | `150/400 = 3/8` | `50` | `10/2` |
| `0/2` | `200/400 = 1/2` | `200/400 = 1/2` | `0` | `20/2` |

All four histories remain present at every step.

## Fail-closed checks

The checker rejects invalid or duplicate history IDs, missing source digests, invalid `Z4` phase, invalid weight numerator, weight-denominator mismatch, invalid dephasing denominator, a trajectory not starting at `n=d`, a trajectory not ending at `n=0`, non-strict or out-of-range numerators, a homotopy class split across blocks, a block mixing classes, incorrect kernel or trajectory claims, and false selection, ranking, pruning, activation, or execution claims.

## Mathlib theorem surface

The strict Lean package contains:

```text
exact Gaussian Gram real symmetry
exact Gaussian Gram imaginary antisymmetry
diagonal squared-norm identity
nonnegative convex Gram quadratic witness
trace preservation
purity–mixedness denominator partition
reference purity values 400, 250, 200
reference mixedness values 0, 150, 200
reference cross-coherence values 200, 50, 0
reference readout values 0, 10, 20
reference monotonicity
non-authority theorem
bounded read-only future-only theorem
```

## Fixed boundaries

```text
finite coherence kernel != complete physical density operator
exact rational dephasing parameter != physical time
quadratic mixedness != von Neumann entropy
kernel diagonal != empirical probability
purity != plan quality
mixedness != indecision defect
coherence loss != plan deletion
homotopy block != semantic equivalence class
readout intensity != candidate ranking
partial dephasing trajectory != activation trajectory
all histories retained != all histories activated
PQQPI evidence != execution authority
WORLD-conditioned history != WORLD mutation
```

The v1.22 certificate, Physical Quantum Qi definition, source histories, source plans, homotopy witnesses, and persistent WORLD state remain unchanged.
