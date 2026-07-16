# MemoryOS v0.91 — Counterexample-Guided Closed-Context Refinement Certificate Kernel

## Scope

MemoryOS v0.91 advances the v0.90 full closed-support truth-region representation into an exact finite refinement loop.

For a finite homogeneous sensor family

\[
\sigma_i:G\to H,
\qquad i\in I,
\]

v0.89 defined the exact support closure

\[
\operatorname{cl}_r(S)
=
\{i\in I\mid K_r^S\le K_r^{\sigma_i}\}.
\]

v0.90 represented consequence by all closed supports

\[
\mathcal C_r
=
\{C\subseteq I\mid \operatorname{cl}_r(C)=C\}.
\]

For a selected family of closed contexts \(\mathcal A\subseteq\mathcal C_r\), write

\[
S\models_{\mathcal A} i
\]

when every selected closed context containing \(S\) also contains \(i\).

A reduced context family remains sound but may contain false positive implications. v0.91 gives every failed implication a canonical closed counterexample and proves that adding this one context repairs the queried implication exactly.

The construction is finite, deterministic, read-only, and advisory.

## Literature alignment

The immediate literature trigger is:

- **arXiv:2607.01773 (2026)** — retrieval-grounded Formal Concept Analysis for verifiable knowledge expansion. Its verification loop asks whether a proposed implication is accepted or receives an inspectable counterexample.
- **arXiv:2205.15714** — attribute exploration with multiple partial and potentially contradicting experts.
- **arXiv:1202.4824** — a general form of attribute exploration as knowledge completion.
- **arXiv:1503.09025** — learning definite Horn theories from closure and equivalence queries.
- **arXiv:2404.12229** — the distinction between minimal and direct implication bases.
- **arXiv:1110.5805** — ordered direct implicational bases for finite closure systems.

MemoryOS imports only the finite mathematical pattern:

1. test an implication against a selected closed-context family;
2. retain every sound implication;
3. when the implication is false, add an explicit counterexample;
4. re-evaluate without granting the counterexample source truth authority.

No retrieval model, language-model score, empirical ontology claim, expert authority, or external oracle is imported.

## Proper closed contexts

The universal context is

\[
\top_I=I.
\]

It contains every sensor and therefore cannot refute any implication. Define the proper closed-context family

\[
\mathcal C_r^\circ
=
\{C\in\mathcal C_r\mid C\ne I\}.
\]

The Lean layer proves that \(I\) is closed and that removing it preserves both singleton and finite-support consequence:

\[
\boxed{
i\in\operatorname{cl}_r(S)
\iff
S\models_{\mathcal C_r^\circ}i
}
\]

and

\[
\boxed{
T\subseteq\operatorname{cl}_r(S)
\iff
S\models_{\mathcal C_r^\circ}T.
}
\]

Thus the full family from v0.90 always contains one consequence-redundant context.

This is not a global minimum-context theorem. Other closed contexts may also be redundant in a particular finite profile.

## Selected-context consequence

For any selected family \(\mathcal A\) consisting only of closed supports,

\[
i\in\operatorname{cl}_r(S)
\Longrightarrow
S\models_{\mathcal A}i.
\]

Hence selected closed contexts never reject a true closure consequence.

If

\[
\mathcal A\subseteq\mathcal B,
\]

then

\[
S\models_{\mathcal B}i
\Longrightarrow
S\models_{\mathcal A}i.
\]

Adding contexts can only remove implications. It cannot create a new implication.

This antitone law is the formal boundary that prevents counterexample enrichment from silently increasing authority.

## Canonical counterexample

Suppose

\[
i\notin\operatorname{cl}_r(S).
\]

Define

\[
C_{S,i}
=
\operatorname{cl}_r(S).
\]

Then

\[
\boxed{
\operatorname{cl}_r(C_{S,i})=C_{S,i},
\qquad
S\subseteq C_{S,i},
\qquad
i\notin C_{S,i}.
}
\]

Therefore \(C_{S,i}\) is a closed counterexample to \(S\Rightarrow i\).

Because \(i\notin C_{S,i}\), the context is necessarily proper:

\[
C_{S,i}\ne I.
\]

No search for a counterexample is needed. The premise closure itself is canonical.

## One-step exact query repair

For a selected closed-context family \(\mathcal A\), define

\[
\operatorname{refine}_r(\mathcal A,S)
=
\mathcal A\cup\{\operatorname{cl}_r(S)\}.
\]

The refined family still consists only of closed contexts.

For the queried implication \(S\Rightarrow i\),

\[
\boxed{
i\in\operatorname{cl}_r(S)
\iff
S\models_{\operatorname{refine}_r(\mathcal A,S)}i.
}
\]

Thus one canonical insertion makes the selected family exact for that query.

The two cases are exact:

- if \(i\in\operatorname{cl}_r(S)\), soundness preserves the implication after enrichment;
- if \(i\notin\operatorname{cl}_r(S)\), the inserted context contains \(S\) and omits \(i\), so the implication is immediately refuted.

The refinement does not claim that the selected family becomes globally complete after one insertion. Exactness is query-local.

## Idempotence

Repeating the same refinement changes nothing:

\[
\boxed{
\operatorname{refine}_r(
  \operatorname{refine}_r(\mathcal A,S),
  S
)
=
\operatorname{refine}_r(\mathcal A,S).
}
\]

The same counterexample is never duplicated.

## Root independence

The proper closed-context family is root independent:

\[
\mathcal C_r^\circ=\mathcal C_s^\circ.
\]

The canonical counterexample and refinement are also root independent:

\[
\operatorname{cl}_r(S)=\operatorname{cl}_s(S),
\]

\[
\operatorname{refine}_r(\mathcal A,S)
=
\operatorname{refine}_s(\mathcal A,S).
\]

All four-root runtime records are consistency repetitions rather than distinct physical claims.

## Canonical finite profiles

For the eight inherited finite \(S_3\) profiles, the proper closed contexts are:

| Sensor family | Full closed contexts | Proper closed contexts |
|---|---:|---:|
| empty | 1 | 0 |
| identity | 2 | 1 |
| parity | 2 | 1 |
| terminal | 1 | 0 |
| identity + parity | 3 | 2 |
| parity + terminal | 2 | 1 |
| identity + parity + terminal | 3 | 2 |
| parity + parity | 2 | 1 |

In every profile exactly one universal context is removed.

The empty and terminal profiles may have no proper contexts. Completeness still holds:

- the empty profile has no sensor query to refute;
- in the terminal profile every singleton consequence is already true.

## Exact exhaustive runtime

The runtime enumerates:

- all supports of each canonical sensor index set;
- all singleton and finite-support consequence queries;
- all subfamilies of proper closed contexts;
- every selected-context false positive;
- every canonical refinement;
- all ordered source/target root pairs.

For each selected query it verifies:

\[
\text{repaired consequence}
=
\text{exact closure consequence}.
\]

It also checks that:

- true consequences are preserved;
- false consequences are refuted;
- every false positive disappears after one canonical insertion;
- repeated insertion is idempotent;
- root transport changes no proper context or canonical counterexample.

## Exact runtime ledger

- literature records: 6
- profile records: 8
- proper-context membership records: 32
- proper singleton-consequence records: 216
- proper finite-support consequence records: 500
- canonical counterexample records: 60
- selected-context family records: 72
- selected-consequence records: 680
- false-positive records: 84
- one-step repair records: 680
- true-consequence preservation records: 488
- false-consequence refutation records: 192
- refinement-idempotence records: 300
- proper-context root-independence records: 128
- refinement root-independence records: 432
- confidence-preservation records: 4

## Confidence policy

The inherited adjusted confidence values remain exactly

\[
\frac13,
\qquad
\frac5{18},
\qquad
\frac{11}{54},
\qquad
\frac{11}{54}.
\]

The v0.91 penalty is zero.

Context counts, false-positive counts, counterexample counts, and refinement counts are diagnostic only. They are not used for ranking, pruning, selection, confidence adjustment, decision commit, or truth authority.

## Fail-closed source binding

The runtime binds exactly to the merged v0.90 artifacts by Git blob identity:

- v0.90 runtime blob:
  `71611b1309f7154efac11dce7f97d4191d769e74`
- v0.90 manifest blob:
  `e8a3e4108b2eabd9112834ae0620c1731c68978d`

It also validates the v0.90 representation laws, zero-penalty confidence policy, and importability before issuing v0.91.

The v0.91 checker rebuilds the full certificate and performs fail-closed mutation tests over:

- acceptance;
- canonical counterexample records;
- one-step repair records;
- confidence penalty;
- external-oracle authority;
- execution authority;
- source-runtime binding.

## Authority boundary

MemoryOS v0.91 does not grant:

- external oracle authority;
- retrieval-result authority;
- universal expert authority;
- a globally minimum context basis;
- universal attribute-exploration completeness;
- empirical ontology correctness;
- candidate ranking, pruning, or selection;
- decision commit or receipt issuance;
- plan synthesis, activation, or execution;
- source or persistent-state mutation;
- verification or truth authority.

The literature informs the refinement pattern. Lean and the exact finite runtime determine only the stated certificate laws.
