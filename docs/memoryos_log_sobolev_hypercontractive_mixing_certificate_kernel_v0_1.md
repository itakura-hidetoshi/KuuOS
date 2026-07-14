# MemoryOS v0.59 — logarithmic Sobolev bridge, hypercontractivity, and exact mixing time

## Scope

MemoryOS v0.59 extends the reversible three-state Markov semigroup from v0.58 with a finite logarithmic Sobolev inequality, exact bounded hypercontractive schedules, and total-variation mixing certificates. The layer is future-only, read-only, and advisory. It does not rank, prune, select, commit, synthesize, activate, execute, mutate source state, mutate WORLD state, claim verification, or grant truth authority.

## Source bindings

The runtime independently validates and binds:

- the accepted MemoryOS v0.58 certificate;
- the v0.58 kernel-power and semigroup-composition digests;
- the v0.58 detailed-balance and eigenmode digests;
- the v0.58 entropy-trajectory and entropy-production digests;
- the v0.58 full-rank transport and singular atomic entropy digests;
- an independently supplied accepted MemoryOS v0.57 certificate;
- the v0.57 stochastic-kernel and data-processing digests;
- all retained DecisionOS candidate identifiers;
- both PlanOS history identifiers;
- all nine quotient-coordinate probe identifiers;
- relational-frontier, required-review, dissent, and minority-protection sets.

Source substitution, changed exact masses, altered entropy trajectories, false mixing thresholds, false density recovery, and forbidden authority claims are rejected fail-closed.

## Logarithmic entropy bridge

For a positive likelihood ratio `x`, Mathlib gives

\[
\log x\le x-1.
\]

Multiplication by `x` yields

\[
x\log x\le x(x-1).
\]

For three positive likelihood ratios `r0`, `r1`, `r2` with uniform mean one,

\[
r_0+r_1+r_2=3,
\]

the formal package sums the cellwise inequalities and proves

\[
D_{\mathrm{KL}}(p\|\pi)
\le \chi^2(p\|\pi).
\]

This is an actual logarithmic entropy theorem rather than a renamed quadratic witness.

## Dirichlet form and log-Sobolev constant

In the slow and fast probability-mode coordinates `(a,b)`, v0.58 gives

\[
\chi^2(a,b)=6a^2+18b^2.
\]

The reversible Dirichlet form is

\[
\mathcal E(a,b)=\frac32a^2+\frac{27}{2}b^2.
\]

Therefore

\[
4\mathcal E(a,b)-\chi^2(a,b)=36b^2\ge0,
\]

and hence

\[
D_{\mathrm{KL}}(p\|\pi)
\le \chi^2(p\|\pi)
\le4\mathcal E(p,p).
\]

The certified constant is `4`. It is a valid finite-state bound; v0.59 does not claim that this convention-dependent constant is globally optimal.

## One-step L2 to L4 hypercontractivity

For the centered observable mode vector

\[
g(a,b)=(a+b,-2b,-a+b),
\]

define

\[
\|g\|_{2,\pi}^2=\frac23a^2+2b^2,
\qquad
\|g\|_{4,\pi}^4=\frac23(a^2+3b^2)^2.
\]

One Markov step maps

\[
(a,b)\mapsto(3a/4,b/4).
\]

Lean proves directly that

\[
\|Kg\|_{4,\pi}^4\le\|g\|_{2,\pi}^4.
\]

The auxiliary rational envelope is

\[
3(9/16)^2=243/256<1.
\]

## Two-step L2 to Linfinity hypercontractivity

After two steps the centered coordinates are

\[
\left(\frac{9a+b}{16},-\frac b8,\frac{-9a+b}{16}\right).
\]

The formal package proves each coordinate square is bounded by the initial uniform mean square. Therefore

\[
\|K^2g\|_\infty\le\|g\|_{2,\pi}.
\]

The same exact squared envelope coefficient is `243/256`.

## Total-variation bridge

For three deviations `x`, `y`, `z`, Lean proves

\[
(|x|+|y|+|z|)^2
\le3(x^2+y^2+z^2).
\]

Consequently,

\[
\|p-\pi\|_{\mathrm{TV}}^2
\le\frac14\chi^2(p\|\pi).
\]

Every probability distribution on three states satisfies

\[
\chi^2(p\|\pi)\le2.
\]

Combined with the v0.58 sharp coefficient `9/16`, this yields the worst-case bound

\[
\|pK^n-\pi\|_{\mathrm{TV}}^2
\le\frac12\left(\frac9{16}\right)^n.
\]

## Exact mixing thresholds

The runtime checks the threshold and the immediately preceding bound.

- worst-case `TV <= 1/4`: certified at `n=4`; the `n=3` envelope is insufficient;
- worst-case `TV <= 1/8`: certified at `n=7`; the `n=6` envelope is insufficient;
- reference `P` and `Q`, `TV <= 1/20`: exact at `n=4`; the exact `n=3` value is still larger.

The reference total-variation trajectory is

| time | total variation |
|---:|---:|
| 0 | `3/20` |
| 1 | `9/80` |
| 2 | `27/320` |
| 3 | `81/1280` |
| 4 | `243/5120` |

## KL expression ledger

For both reference distributions and all five v0.58 timepoints, the runtime retains:

- all three exact masses;
- all three exact likelihood ratios against `pi=(1/3,1/3,1/3)`;
- the symbolic terms `mass * Real.log(likelihood_ratio)`;
- the exact chi-square upper envelope;
- positivity and normalization witnesses.

This produces ten KL-envelope records without replacing logarithms by floating-point approximations.

## Transport and singular boundaries

Across four full-rank quotient-metric transitions and both reference distributions, the log-Sobolev envelope, hypercontractive schedule, and mixing bounds commute with the retained mass-level transport, producing eight records.

Across two full-rank-to-rank-one transitions and both reference distributions, the entropy and mixing ledgers are retained as singular atomic evidence, producing four records. No two-dimensional target density or lost antisymmetric information is reconstructed.

## Runtime counts

- log-Sobolev records: 1
- reference KL-envelope records: 10
- hypercontractive schedule records: 2
- reference total-variation records: 10
- worst-case mixing records: 9
- mixing-threshold records: 3
- full-rank transport/log-Sobolev/mixing records: 8
- singular atomic log-Sobolev/mixing records: 4
- rank-one source boundaries: 3

## Files

- `formal/KUOS/OpenHorizon/MemoryOSLogSobolevHypercontractiveMixingV0_59.lean`
- `formal/KuuOSMemoryOSV0_59.lean`
- `runtime/kuuos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check.py`
