# MemoryOS v0.89 — Sensor-Support Closure Operator Certificate Kernel

## Scope

MemoryOS v0.89 advances the v0.88 exact-core layer from individual redundancy certificates to a closure operator on finite sensor supports.

For a finite homogeneous sensor family

\[
\sigma_i:G\to H,
\qquad i\in I,
\]

and a retained support \(S\subseteq I\), let

\[
K_r^S=\bigcap_{i\in S}K_r^{\sigma_i}
\]

be the invisible kernel at root \(r\). Define the support closure by

\[
\operatorname{cl}_r(S)
=
\{i\in I\mid K_r^S\le K_r^{\sigma_i}\}.
\]

A sensor lies in the closure exactly when its invisibility condition is already implied by the retained support.

The construction is finite, exact, read-only, and advisory. Closure size and closed-support counts are diagnostic metadata only.

## Closure laws

The Lean layer proves the standard closure-operator laws.

### Extensivity

\[
\boxed{S\subseteq\operatorname{cl}_r(S)}
\]

Every retained sensor is implied by the support containing it.

### Monotonicity

If \(S\subseteq T\), then

\[
\boxed{\operatorname{cl}_r(S)\subseteq\operatorname{cl}_r(T)}.
\]

Adding sensors shrinks the invisible kernel and can only increase the set of implied sensors.

### Kernel invariance

\[
\boxed{K_r^{\operatorname{cl}_r(S)}=K_r^S.}
\]

Closing a support adds only sensors whose constraints were already present.

### Idempotence

\[
\boxed{
\operatorname{cl}_r(\operatorname{cl}_r(S))
=
\operatorname{cl}_r(S)
}.
\]

Thus the closed supports are exactly the fixed points of the operator.

## Kernel classes and closed supports

Two supports have the same exact invisible kernel precisely when they have the same closure:

\[
\boxed{
K_r^S=K_r^T
\iff
\operatorname{cl}_r(S)=\operatorname{cl}_r(T)
}.
\]

The closure is therefore a canonical representative of an exact observable-kernel class. Quotients by a support and by its closure are multiplicatively equivalent.

## Redundancy criterion

For \(i\in S\), v0.88 redundancy was defined by

\[
K_r^S=K_r^{S\setminus\{i\}}.
\]

The closure formulation is

\[
\boxed{
i\text{ is redundant in }S
\iff
i\in\operatorname{cl}_r(S\setminus\{i\}).
}
\]

Thus redundancy can be tested by asking whether the erased support already implies the removed sensor.

Duplicate- and dominated-sensor removal from v0.88 become special cases of closure membership.

## Exact cores

If \(C\subseteq S\) is an exact sensor core, then

\[
K_r^C=K_r^S
\]

and consequently

\[
\boxed{
\operatorname{cl}_r(C)=\operatorname{cl}_r(S).
}
\]

Different minimum cores may generate the same closure. The duplicated-parity profile remains the canonical finite example: either duplicate coordinate can be chosen as a minimum core, but both generate the closed support containing both parity coordinates.

## Root independence

The support kernel and support closure do not depend on the selected root chart:

\[
K_r^S=K_s^S,
\qquad
\operatorname{cl}_r(S)=\operatorname{cl}_s(S).
\]

All closure records are therefore repeated at the four roots as consistency checks rather than as distinct physical claims.

## Canonical finite profiles

The exact runtime enumerates every index support of the eight v0.88 canonical families.

| Family | Closed supports |
|---|---|
| empty | \(\varnothing\) |
| identity | \(\varnothing,\{0\}\) |
| parity | \(\varnothing,\{0\}\) |
| terminal | \(\{0\}\) |
| identity + parity | \(\varnothing,\{1\},\{0,1\}\) |
| parity + terminal | \(\{1\},\{0,1\}\) |
| identity + parity + terminal | \(\{2\},\{1,2\},\{0,1,2\}\) |
| parity + parity | \(\varnothing,\{0,1\}\) |

Interpretation:

- identity implies parity and terminal sensing;
- parity implies terminal sensing;
- terminal adds no constraint beyond the empty support;
- duplicate parity coordinates imply one another;
- closed supports classify the exact finite kernel classes in these listed profiles.

No universal matroid exchange property or unique-basis theorem is claimed.

## Exact runtime ledger

- literature records: 6
- closure profiles: 8
- support-closure records: 108
- extensivity records: 108
- kernel-invariance records: 108
- idempotence records: 108
- monotonicity records: 256
- kernel/closure equivalence records: 500
- redundancy/closure records: 108
- exact-core closure records: 32
- closed-support records: 64
- closure quotient-equivalence records: 108
- closure root-independence records: 432
- confidence-preservation records: 4
- memory-fusion records: 4
- full-rank transport records: 8
- singular atomic records: 4
- rank-one source boundaries: 3

## Confidence policy

The v0.88 adjusted confidence values are preserved exactly:

\[
\frac13,
\qquad
\frac5{18},
\qquad
\frac{11}{54},
\qquad
\frac{11}{54}.
\]

The new closure penalty is zero.

## Fail-closed source binding

The runtime reissues and validates the accepted v0.88 certificate, including:

- acceptance, schema, and complete certificate digest;
- all required and forbidden claims;
- exact source record counts and collection digests;
- canonical profile order, coordinates, cores, and minimum-cardinality records;
- candidate, history, probe, review, dissent, and minority retention;
- exact confidence preservation.

It then exhaustively enumerates every support of every canonical family and verifies closure membership, extensivity, monotonicity, idempotence, kernel invariance, kernel/closure equivalence, redundancy, exact-core closure equality, quotient preservation, and root independence.

Mutation of source data, closure records, confidence, or authority boundaries blocks issuance.

## Authority boundary

MemoryOS v0.89 does not claim:

- a universal classification of sensor closures;
- matroid exchange axioms;
- uniqueness of minimum sensor bases;
- an infinite-family or continuum limit;
- physical measurement sufficiency;
- candidate ranking, pruning, or selection;
- decision commit or receipt issuance;
- plan synthesis, activation, or execution;
- source or persistent state mutation;
- verification or truth authority.
