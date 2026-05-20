# Governance Diagram v0.1

```mermaid
flowchart TD
    A[Candidate generation] --> B[Boundary checks]
    B --> C[Governance validators]
    C --> D[BeliefOS]
    C --> E[PlanOS]
    C --> F[MemoryOS]

    D --> G[DecisionOS]
    E --> G
    F --> G

    G --> H[RuntimeGovernance]

    H --> I[Proceed]
    H --> J[Hold]
    H --> K[Abstain]
    H --> L[Rollback]
    H --> M[Reobserve]

    H --> N[Audit chain]
    H --> O[Provenance tracking]
    H --> P[Validator surface]

    C --> R[Samvrti Qi Runtime]
    R --> S[Conservative evidence builder]
    S --> T[Evidence-bound Qi classification]
    T --> U[Licensed Qi dynamics]
    U --> V[Observe-only Qi motion candidate]
    V --> N
    V --> P
    V -.no direct execution.-> J

    Q[Canonical theorem repository boundary] -.reference only.-> P
```

## Interpretation

This governance flow emphasizes:

- candidate-versus-authority separation
- runtime admissibility
- rollback visibility
- abstention legitimacy
- provenance preservation
- Qi motion candidate non-authority

The Qi motion chain routes bounded motion candidates to validation and audit surfaces. It remains observe-only and does not create clinical, institutional, theorem, or execution authority.

The theorem repository boundary is reference-only unless explicitly elevated by external processes.