# Validator Graph v0.1

```mermaid
flowchart TD
    A[core-governance-checks]
    B[ai-yogacara-checks]
    C[invariant-pipeline-checks]
    D[physical-quantum-qi-runtime-checks]
    M[qi-motion-chain-checks]
    E[physical-quantum-qi-deepening-checks]
    F[superstring-emptiness-sbm-checks]

    A --> G[all-governance-checks]
    B --> G
    C --> G
    D --> G
    M --> G
    E --> G
    F --> G

    C --> H[Formal invariant preservation]
    D --> I[Qi runtime validation]
    M --> N[Samvrti Qi to conservative evidence]
    N --> O[Evidence-bound Qi classification]
    O --> P[Licensed Qi dynamics]
    P --> Q[Observe-only Qi motion candidate]
    E --> J[IndraNet transport validation]
    F --> K[String-brane-membrane validation]

    G --> L[Public governance validation surface]
```

## Interpretation

The aggregate governance surface depends on multiple validator families.

Each edge represents one canonical prerequisite invocation.

Bundle checkers own preparation already encoded by their bundle builders.

Attestation, closure, and finality layers call only their direct prerequisite checker.

Sibling wrappers must not repeat a prerequisite already invoked by the destination checker.

`qi-motion-chain-checks` validates the bridge from Samvrti Qi observation to conservative evidence, evidence-bound classification, licensed dynamics, and observe-only Qi motion candidate output.

Validator success indicates structural consistency of exposed governance surfaces.

Validator success does not automatically imply theorem closure, clinical authority, execution authority, or deployment readiness.
