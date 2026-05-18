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

    Q[Canonical theorem repository boundary] -.reference only.-> P
```

## Interpretation

This governance flow emphasizes:

- candidate-versus-authority separation
- runtime admissibility
- rollback visibility
- abstention legitimacy
- provenance preservation

The theorem repository boundary is reference-only unless explicitly elevated by external processes.
