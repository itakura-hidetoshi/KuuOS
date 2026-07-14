# MemoryOS v0.64 — finite log-MGF, Chernoff transform, and exact tail thresholds

## Scope

MemoryOS v0.64 extends the accepted MemoryOS v0.63 observable-side transport package. It adds a finite, explicit concentration layer for the same three-state reversible Markov semigroup:

- strict positivity of every finite stationary moment-generating function;
- exact finite log-MGF definitions and exponentiation identities;
- exact slow and fast mode log-MGF formulas;
- actual Chernoff upper-tail bounds for both finite eigenmodes;
- exact support-tail extinction thresholds at fixed rational levels;
- exact-rational runtime ledgers for symbolic Chernoff terms;
- Marton-input retention without claiming a general Gaussian or large-deviation theorem;
- full-rank transport commutation and singular atomic retention.

The certificate remains future-only, read-only, and advisory. It does not rank, prune, or select candidates; commit decisions; synthesize plans; activate or execute actions; mutate source or WORLD state; claim verification; or grant truth authority.

## Finite stationary log-MGF

For a three-state observable `f`, v0.63 defined

\[
M_f(t)=\frac{e^{t f_E}+e^{t f_M}+e^{t f_L}}3.
\]

v0.64 defines

\[
\Lambda_f(t)=\log M_f(t).
\]

Lean proves that `M_f(t)` is strictly positive for every real `t`, hence

\[
e^{\Lambda_f(t)}=M_f(t),
\qquad
\Lambda_f(0)=0.
\]

No numerical approximation to logarithms or exponentials is used in the runtime certificate. The runtime stores rational weights and rational exponent coefficients as symbolic terms.

## Exact slow and fast formulas

For the slow mode scaled by `r`, with values `(r,0,-r)`,

\[
\Lambda_{\mathrm{slow},r}(t)
=
\log\!\left(\frac{e^{tr}+1+e^{-tr}}3\right).
\]

For the fast mode scaled by `r`, with values `(r,r,-2r)`,

\[
\Lambda_{\mathrm{fast},r}(t)
=
\log\!\left(\frac{2e^{tr}+e^{-2tr}}3\right).
\]

The Markov semigroup amplitudes are

\[
r_n^{\mathrm{slow}}=\left(\frac34\right)^n,
\qquad
r_n^{\mathrm{fast}}=\left(\frac14\right)^n.
\]

## Chernoff transform

For threshold `a`, v0.64 defines

\[
C_f(t,a)=\Lambda_f(t)-ta
\]

and the corresponding envelope

\[
B_f(t,a)=e^{-ta}M_f(t).
\]

Lean proves the exact identity

\[
e^{C_f(t,a)}=B_f(t,a).
\]

For every nonnegative `t`, it proves the actual finite-mode bounds

\[
\Pr\{rS\ge a\}
\le e^{-ta}M_{rS}(t)
\]

for the slow support `S∈{1,0,-1}`, and

\[
\Pr\{rF\ge a\}
\le e^{-ta}M_{rF}(t)
\]

for the fast support `F∈{1,1,-2}` under uniform stationary weights.

The proof uses the explicit finite support. It does not invoke or claim a general Cramér theorem, Gärtner–Ellis theorem, path-space Gaussian theorem, or asymptotic large-deviation principle.

## Exact support-tail extinction thresholds

For fixed positive threshold, the finite upper tail becomes exactly zero once the semigroup amplitude falls below the threshold.

The certified first extinction times are:

| mode | threshold | previous nonzero time | first zero time |
|---|---:|---:|---:|
| slow | `1/2` | 2 | 3 |
| slow | `1/4` | 4 | 5 |
| fast | `1/2` | 0 | 1 |
| fast | `1/4` | 1 | 2 |

At the preceding time, the exact tail masses are `1/3` for the slow mode and `2/3` for the fast mode. At the certified time they are exactly zero.

## Runtime records

The runtime records:

- finite log-MGF records: 22;
- finite Chernoff-transform records: 44;
- exact tail-extinction threshold records: 4;
- Marton–Chernoff input records: 22;
- full-rank transport records: 8;
- singular atomic records: 4;
- rank-one source boundaries: 3.

Each Chernoff record contains exact stationary weights, exact support values, exact upper-tail mass, rational exponent coefficients for the symbolic envelope, and the formal-proof boundary. It does not store floating-point transcendental approximations.

## Source binding and fail-closed behavior

The runtime independently validates and binds the accepted MemoryOS v0.63 certificate, including:

- the v0.63 certificate digest;
- Kantorovich dual witness digest;
- Lipschitz semigroup profile digest;
- reference observable-gap digests;
- finite symbolic MGF digest;
- Marton MGF-input digest;
- all DecisionOS candidate identifiers;
- both PlanOS history identifiers;
- all quotient-coordinate probes;
- relational-frontier, required-review, dissent, and minority-protection sets.

It rejects altered source MGF records, changed tail-extinction times, false Chernoff claims, unexpected claims, source substitution, digest tampering, and forbidden candidate-selection or execution authority claims.

## Transport and singular boundaries

Across full-rank quotient-metric transitions, finite log-MGF, Chernoff-transform, and exact-tail evidence commute with retained mass-level evidence.

Across full-rank-to-rank-one transitions, the certificate retains atomic symbolic log-MGF terms, Chernoff terms, and tail thresholds. It does not emit a two-dimensional target density or reconstruct a lost coordinate.

## Files

- `formal/KUOS/OpenHorizon/MemoryOSFiniteLogMGFChernoffTailV0_64.lean`
- `formal/KuuOSMemoryOSV0_64.lean`
- `runtime/kuuos_memoryos_finite_log_mgf_chernoff_tail_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_finite_log_mgf_chernoff_tail_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_finite_log_mgf_chernoff_tail_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check.py`
