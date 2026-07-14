# MemoryOS v0.60 — modified entropy decay, symbolic Hellinger, and exact separation

## Scope

MemoryOS v0.60 extends the reversible three-state Markov semigroup frontier with three connected mathematical surfaces:

1. a modified logarithmic entropy-decay envelope inherited from the sharp chi-square SDPI coefficient;
2. a Hellinger-square profile whose radicals remain symbolic and exact;
3. an exact rational separation-distance trajectory with first-passage threshold certificates.

The layer is future-only, read-only, and advisory. It grants no ranking, pruning, selection, decision, planning, activation, execution, mutation, verification, or truth authority.

## Source binding

The runtime accepts only a correctly signed accepted MemoryOS v0.59 certificate. It rechecks the source schema, certificate digest, future-only and read-only flags, complete candidate/history/probe retention, relational frontier, required review set, dissent visibility, and minority visibility.

## Modified logarithmic entropy decay

MemoryOS v0.59 proved the actual logarithmic bridge

\[
D_{\mathrm{KL}}(p\|\pi)\le \chi^2(p\|\pi).
\]

The v0.58 reversible semigroup has the sharp chi-square coefficient

\[
\chi^2(pK\|\pi)\le \frac9{16}\chi^2(p\|\pi).
\]

Therefore v0.60 certifies the iterated envelope

\[
D_{\mathrm{KL}}(pK^n\|\pi)
\le
\left(\frac9{16}\right)^n\chi^2(p\|\pi).
\]

This is a genuine logarithmic entropy upper bound. It does not assert a convention-independent globally optimal modified log-Sobolev constant or a KL-to-KL equality.

## Symbolic Hellinger profile

For likelihood ratios `r_i = p_i / pi_i` against the uniform three-state stationary law, define

\[
H^2(p,\pi)=\frac16\sum_{i=0}^2(\sqrt{r_i}-1)^2.
\]

Lean proves cellwise, for `x >= 0`,

\[
(\sqrt{x}-1)^2\le(x-1)^2,
\]

and hence

\[
H^2(p,\pi)\le\frac12\chi^2(p\|\pi).
\]

The runtime retains all radicals as symbolic `Real.sqrt` expressions. No decimal or floating-point square-root approximation is emitted.

## Exact separation profile

For both reference distributions, the middle coordinate remains stationary and the slow antisymmetric mode contracts by `3/4`. The separation distance is therefore

\[
\operatorname{sep}(pK^n,\pi)
=
\frac9{20}\left(\frac34\right)^n.
\]

The exact trajectory through time seven is:

| time | separation |
|---:|---:|
| 0 | `9/20` |
| 1 | `27/80` |
| 2 | `81/320` |
| 3 | `243/1280` |
| 4 | `729/5120` |
| 5 | `2187/20480` |
| 6 | `6561/81920` |
| 7 | `19683/327680` |

First-passage witnesses:

- `separation <= 3/20` first holds at `n=4`; the exact `n=3` value remains larger;
- `separation <= 1/16` first holds at `n=7`; the exact `n=6` value remains larger.

## Runtime records

- modified entropy-decay records: 16;
- symbolic Hellinger profile records: 16;
- exact separation profile records: 16;
- separation threshold records: 2;
- full-rank transport/entropy-metric records: 8;
- singular atomic entropy-metric records: 4;
- rank-one source boundaries: 3.

Across full-rank quotient-metric transports, mass-level entropy envelopes and metric profiles commute. Across full-rank-to-rank-one collapse, the atomic ledger is retained without inventing a two-dimensional target density or reconstructing lost antisymmetric information.

## Files

- `formal/KUOS/OpenHorizon/MemoryOSModifiedLogSobolevHellingerSeparationV0_60.lean`
- `formal/KuuOSMemoryOSV0_60.lean`
- `runtime/kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.py`
- `scripts/check_planos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.py`
- `manifests/kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1.json`
- `runtime/kuuos_current_check.py`
