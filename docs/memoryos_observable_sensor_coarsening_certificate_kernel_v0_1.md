# MemoryOS v0.85 — Observable Sensor Coarsening and Quotient Functoriality

## Scope

MemoryOS v0.84 constructed the exact root-independent observable quotient

\[
Q_i=\Gamma(F)^\times/\ker(E_i)
\]

and identified it with the exact range of the global evaluation homomorphism.
MemoryOS v0.85 studies what happens when this exact group-valued observable is
post-processed by another group homomorphism, interpreted as a finite sensor.

This remains a finite, read-only certificate layer. It does not assign truth,
rank candidates, prune records, make decisions, activate plans, or execute actions.

## Sensor evaluation

For a group homomorphism

\[
\sigma:G\longrightarrow H,
\]

define

\[
E_i^\sigma=\sigma\circ E_i.
\]

Its invisible kernel and visible range are

\[
K_i^\sigma=\ker(E_i^\sigma),\qquad
R_i^\sigma=\operatorname{range}(E_i^\sigma).
\]

Because the v0.84 evaluation homomorphism is root independent,

\[
E_i^\sigma=E_j^\sigma,
\]

and therefore both `K_i^sigma` and `R_i^sigma` are independent of the selected
root chart.

## Monotone information loss

Every exactly invisible section remains invisible after sensor post-processing:

\[
K_i\le K_i^\sigma.
\]

For a second sensor `tau : H -> I`,

\[
K_i^\sigma\le K_i^{\tau\circ\sigma}.
\]

Thus post-processing can merge exact observable classes but cannot recover a
distinction already removed by an earlier sensor.

If `sigma` is injective, no information is lost:

\[
K_i^\sigma=K_i.
\]

## Quotient functoriality

Kernel inclusion induces a canonical quotient homomorphism

\[
\Gamma(F)^\times/K_i
\longrightarrow
\Gamma(F)^\times/K_i^\sigma,
\qquad
[s]_{K_i}\longmapsto[s]_{K_i^\sigma}.
\]

The sensor quotient itself satisfies the first isomorphism theorem:

\[
\Gamma(F)^\times/K_i^\sigma
\simeq_{\mathrm{mul}}
R_i^\sigma.
\]

For injective sensors, the source and sensor quotients are multiplicatively
equivalent.

## Wilson pullback

For a class function `chi : H -> R`, define

\[
(\sigma^*\chi)(g)=\chi(\sigma(g)).
\]

The sensor-level Wilson observable is exactly the pullback observable:

\[
W_\chi^\sigma(s)=W_{\sigma^*\chi}(s).
\]

It remains root independent.

## Canonical finite S3 sensor profiles

The canonical section is the v0.84 mixed section extending `slot-3 defect`.

### Identity S3 sensor

The identity sensor is injective. It preserves the exact quotient and the
ordered-AB / ordered-BA separator:

- ordered AB maps to the identity and remains in the invisible kernel;
- ordered BA maps to `(021)` and remains outside the kernel.

### Parity C2 sensor

The parity sensor is not injective. Both the identity and the 3-cycle `(021)`
are even permutations, hence both map to `0` in `C2`.

The exact AB/BA distinction is therefore lost after parity-only sensing.
This is recorded as sensor information loss, not as evidence that the source
classes were equal.

### Terminal sensor

The terminal sensor maps every value to the unique group element. Every section
becomes sensor-invisible, so all canonical distinctions collapse.

## Runtime ledger

The exact runtime records:

- 6 literature bindings;
- 3 sensor profiles;
- 12 exact-kernel-to-sensor-kernel inclusions;
- 48 root-independence comparisons;
- 16 sensor-composition laws;
- 12 quotient-functoriality records;
- 4 injective-sensor quotient equivalences;
- 12 Wilson-pullback records;
- 12 canonical visibility records;
- 4 confidence-preservation records;
- retained memory-fusion, full-rank, singular-atomic, review, dissent, minority,
  candidate, history, and quotient-probe ledgers.

The checker rejects source digest changes, record mutations, altered sensor
visibility, confidence changes, unexpected claims, and authority-boundary
violations.

## Confidence and authority boundary

MemoryOS v0.85 preserves the v0.84 advisory confidences exactly:

\[
\frac13,\qquad\frac5{18},\qquad\frac{11}{54},\qquad\frac{11}{54}.
\]

No new confidence penalty is introduced. Sensor resolution is descriptive of
observable information loss only. It is not a candidate ranking, decision rule,
verification result, physical measurement claim, or truth authority.
