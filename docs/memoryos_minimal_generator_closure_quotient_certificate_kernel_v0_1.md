# MemoryOS v0.93 — Minimal-Generator Closure Quotient Certificate Kernel

## Scope

MemoryOS v0.92 proved that refining by every finite support recovers the complete proper closed-context family. That saturation is exact but premise-redundant: many different supports generate the same closure context.

MemoryOS v0.93 quotients finite supports by exact closure equivalence and retains only inclusion-minimal representatives of each closure class.

For finite supports `S,T ⊆ I`, define

\[
S \sim_r T
\quad\Longleftrightarrow\quad
\operatorname{cl}_r(S)=\operatorname{cl}_r(T).
\]

By the v0.89 kernel-closure theorem,

\[
\boxed{
S\sim_r T
\iff
K_r^S=K_r^T.
}
\]

A support `M` is a closure-minimal generator when every sub-support with the same closure is equal to `M`:

\[
\operatorname{MinGen}_r(M)
\quad\Longleftrightarrow\quad
\forall T\subseteq M,\ 
\operatorname{cl}_r(T)=\operatorname{cl}_r(M)
\Rightarrow T=M.
\]

The construction is finite, deterministic at the level of the complete family of minimal generators, read-only, and advisory.

## Literature alignment

The immediate 2026 trigger remains:

- **arXiv:2607.01773 (2026)** — retrieval-grounded Formal Concept Analysis with iterative implication validation and inspectable counterexamples.

The exact reduction layer is aligned with:

- **arXiv:2404.12229** — the distinction between minimal and direct implication bases and their different computational roles;
- **arXiv:1503.09025** — closure-query learning and its relation to the Guigues–Duquenne basis;
- **arXiv:1411.6432** — survey of pure Horn functions, canonical bases, direct bases, and closure systems;
- **arXiv:1205.2881** — refinements of canonical implicational bases and the limits of optimization;
- **arXiv:1110.5805** — ordered direct bases for finite closure systems;
- **Guigues–Duquenne (1986)** — canonical implication bases for finite closure systems.

MemoryOS imports only the finite closure-class and minimal-generator pattern. It does not claim that the minimal-generator family is a Guigues–Duquenne basis, a D-basis, an optimum Horn representation, or an optimal query schedule.

## Closure quotient

`ClosureEquivalent` is proved reflexive, symmetric, and transitive. It is exactly kernel equality:

\[
\boxed{
\operatorname{cl}_r(S)=\operatorname{cl}_r(T)
\iff
K_r^S=K_r^T.
}
\]

Hence the quotient is observationally exact: no support-kernel information is lost inside an equivalence class.

## Existence of minimal representatives

For every finite support `S`, Lean proves

\[
\boxed{
\exists M\subseteq S,\quad
\operatorname{cl}_r(M)=\operatorname{cl}_r(S)
\quad\text{and}\quad
\operatorname{MinGen}_r(M).
}
\]

The proof uses strong induction over finite supports. If `S` is not minimal, a strict sub-support with the same closure is selected and the induction hypothesis is applied. Finiteness guarantees termination.

Equivalently,

\[
K_r^M=K_r^S.
\]

## Proper minimal-generator family

Define

\[
\mathcal M_r^\circ
=
\left\{
M\subseteq I
\;\middle|\;
\operatorname{MinGen}_r(M),
\ \operatorname{cl}_r(M)\neq I
\right\}.
\]

Every proper closed context has at least one generator in this family:

\[
\forall C\in\mathcal C_r^\circ,\quad
\exists M\in\mathcal M_r^\circ,\ 
M\subseteq C,\ 
\operatorname{cl}_r(M)=C.
\]

Therefore,

\[
\boxed{
\left\{
\operatorname{cl}_r(M)\mid M\in\mathcal M_r^\circ
\right\}
=
\mathcal C_r^\circ.
}
\]

No uniqueness is claimed. In the inherited `parity + parity` profile, the universal closure class has two incomparable minimal generators, providing an exact finite non-uniqueness witness.

## Reduced saturation

Refining the empty context family by only the proper minimal generators gives

\[
\boxed{
\operatorname{BatchRefine}_r
\left(\varnothing,\mathcal M_r^\circ\right)
=
\mathcal C_r^\circ.
}
\]

Combining this with v0.92 yields

\[
\boxed{
\operatorname{BatchRefine}_r
\left(\varnothing,\mathcal M_r^\circ\right)
=
\operatorname{BatchRefine}_r
\left(\varnothing,\mathcal P(I)\right).
}
\]

Thus all-support saturation can be replaced by closure-class minimal representatives without changing any proper context or consequence.

Singleton and finite-support completeness remain exact:

\[
i\in\operatorname{cl}_r(S)
\iff
S\models_{\mathcal C_r^\circ}i,
\]

\[
T\subseteq\operatorname{cl}_r(S)
\iff
S\models_{\mathcal C_r^\circ}T.
\]

## Root independence

Closure equivalence, minimal-generator status, the proper minimal-generator family, and the reduced saturation result are independent of the chosen route root.

The four-root runtime records are consistency repetitions, not separate physical claims.

## Canonical finite profiles

Across the eight inherited finite `S₃` profiles:

| Profile | All supports | Closure classes | All minimal generators | Proper minimal generators |
|---|---:|---:|---:|---:|
| empty | 1 | 1 | 1 | 0 |
| identity | 2 | 2 | 2 | 1 |
| parity | 2 | 2 | 2 | 1 |
| terminal | 2 | 1 | 1 | 0 |
| identity + parity | 4 | 3 | 3 | 2 |
| parity + terminal | 4 | 2 | 2 | 1 |
| identity + parity + terminal | 8 | 3 | 3 | 2 |
| parity + parity | 4 | 2 | 3 | 1 |

The all-support premise population is reduced from 27 supports to 8 proper minimal generators while preserving all 8 proper closed contexts.

## Exact runtime ledger

- literature records: 7
- profile records: 8
- support records: 27
- closure-class records: 16
- minimal-generator records: 17
- proper minimal-generator records: 8
- support-to-minimal-representative records: 27
- proper-context coverage records: 8
- nonminimal reduction records: 3
- closure/kernel equivalence records: 125
- root-independence records: 432
- non-unique minimal-class records: 1
- confidence-preservation records: 4

## Confidence policy

The inherited adjusted confidence values remain exactly

\[
\frac13,\qquad
\frac5{18},\qquad
\frac{11}{54},\qquad
\frac{11}{54}.
\]

The v0.93 penalty is zero.

Generator counts, reduction counts, closure-class sizes, and non-uniqueness counts are diagnostic only. They are not used for ranking, pruning, selection, confidence adjustment, decision commit, or truth authority.

## Fail-closed source binding

The v0.93 runtime binds exactly to the merged v0.92 artifacts by Git blob identity:

- v0.92 runtime blob: `c228a7708c7608ef96f77f82b1ae3cdfaddfc498`
- v0.92 manifest blob: `0e290bb0cda185eeb8d1956c13a93be97d9e8adf`

Generated uncompressed source hashes:

- v0.93 runtime SHA-256: `8a10359c7535772f6109fd1d090e941f3e9cd6cf4ace05e86342e415eea4fc88`
- v0.93 checker SHA-256: `726f47ebb7a7351715cfbeaf590e2cb00a56fd6a2b30ced8fecfd729e05df511`

The checker performs fail-closed mutation tests over acceptance, source binding, record counts, proper-context coverage, confidence penalty, uniqueness authority, and execution authority.

## Authority boundary

MemoryOS v0.93 does not grant or claim:

- uniqueness of minimal generators;
- a globally minimum implication basis;
- a canonical implication basis;
- a D-basis or ordered-direct basis;
- an optimal query order;
- external-oracle or retrieval-result authority;
- candidate ranking, pruning, or selection;
- decision commit, plan activation, or execution;
- source or persistent-state mutation;
- verification or truth authority.
