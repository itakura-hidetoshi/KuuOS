# MemoryOS v0.65: finite Legendre–Fenchel optimizer and optimized envelope

## Scope

MemoryOS v0.65 extends the accepted v0.64 finite log-MGF and Chernoff
certificate with a finite optimization layer.  The optimization domain is the
exact finite tilt grid

\[
G=\{0,1,2,3,4\}.
\]

For a three-state observable \(f\), threshold \(a\), and stationary log-MGF
\(\Lambda_f(\lambda)\), define the grid objective

\[
J_f(\lambda,a)=\lambda a-\Lambda_f(\lambda),
\qquad \lambda\in G,
\]

the finite Legendre–Fenchel rate

\[
I_G(f,a)=\max_{\lambda\in G}J_f(\lambda,a),
\]

and the optimized envelope

\[
B_G(f,a)=\exp(-I_G(f,a)).
\]

This is a finite-grid certificate.  It does not claim a continuous-tilt
optimizer or an asymptotic large-deviation principle.

## Formal theorem package

`formal/KUOS/OpenHorizon/MemoryOSFiniteLegendreOptimizerV0_65.lean`
contains actual Lean theorems for:

1. exact construction of the nonempty finite tilt grid;
2. nonnegativity and the upper bound \(\lambda\le4\) for every grid tilt;
3. existence of a maximizing tilt by `Finset.max'`;
4. domination of every grid objective by the chosen finite rate;
5. nonnegativity of the finite rate, using the zero tilt;
6. equality between the optimized envelope and the envelope at the chosen
   maximizer;
7. the optimized envelope bound for the slow and fast finite upper tails;
8. antitonicity of the Chernoff envelope in the tilt whenever the complete
   support lies below the threshold;
9. exact identification of tilt \(4\) as an optimizer for the four accepted
   tail-extinction profiles.

The last item covers:

| profile | threshold | certified horizon | optimizer |
|---|---:|---:|---:|
| slow | \(1/2\) | 3 | 4 |
| slow | \(1/4\) | 5 | 4 |
| fast | \(1/2\) | 1 | 4 |
| fast | \(1/4\) | 2 | 4 |

For these four profiles every support point is strictly below the threshold.
Consequently every envelope exponent coefficient
\(4(x_i-a)\) is strictly negative, and the largest grid tilt minimizes the
Chernoff envelope.

## Exact symbolic runtime

`runtime/kuuos_memoryos_finite_legendre_optimizer_certificate_kernel_v0_1.py`
does not evaluate `exp` or `log` numerically.  It stores:

- all five exact rational tilts;
- 44 finite rate profiles: two modes, eleven horizons, and two thresholds;
- every symbolic log-MGF candidate and every symbolic envelope exponent;
- the formal finite-argmax witness mode;
- four explicit extinct-profile optimizer records;
- retained Marton inputs;
- full-rank transport records and singular atomic retention records.

The four selected-tilt exponent ledgers are:

### Slow, threshold \(1/2\), horizon 3

\[
(-5/16,-2,-59/16).
\]

### Slow, threshold \(1/4\), horizon 5

\[
(-13/256,-1,-499/256).
\]

### Fast, threshold \(1/2\), horizon 1

\[
(-1,-1,-4).
\]

### Fast, threshold \(1/4\), horizon 2

\[
(-3/4,-3/4,-3/2).
\]

## Fail-closed source binding

The runtime accepts only an accepted and digest-valid MemoryOS v0.64
certificate.  It binds:

- the finite log-MGF digest;
- the finite Chernoff-transform digest;
- the exact tail-extinction digest;
- the Marton–Chernoff input digest;
- all retained candidate, history, probe, review, dissent, and minority sets;
- all full-rank and singular atomic source collections.

The checker rejects source substitution, source digest tampering, a modified
optimizer tilt, a continuous-optimizer claim, an unexpected claim, or any
candidate-selection or execution-authority claim.

## Mathematical boundary

The certificate proves a finite Legendre–Fenchel maximum and a finite optimized
Chernoff envelope.  It does not claim:

- minimization over all nonnegative real tilts;
- differentiability or strict convexity of the log-MGF;
- a Cramér theorem;
- a Gärtner–Ellis theorem;
- a path-space Gaussian theorem;
- an asymptotic large-deviation principle.

## Authority boundary

MemoryOS v0.65 remains future-only, read-only, and advisory.  It does not
perform candidate ranking, pruning, or selection; issue decisions; synthesize
plans; activate or execute actions; mutate source certificates, DecisionOS, or
persistent WORLD state; claim verification truth; or grant truth authority.

## Current-root connection

The checker is connected as the 26th active MemoryOS step:

`memoryos-v0-65-finite-legendre-fenchel-optimized-envelope`

through `runtime/kuuos_current_check.py`.
