# Reproducibility Matrix v0.1

| Surface | Publicly Reproducible | Notes |
|---|---|---|
| Governance validators | Yes | Runnable through Makefile and scripts |
| Packet consistency checks | Yes | Public packet surfaces only |
| Manifest validation | Yes | YAML and JSON manifest validation included |
| Workflow entrypoints | Yes | GitHub Actions workflows exposed |
| Architecture documentation | Yes | Public docs included |
| Non-authority boundary review | Yes | Governance documents included |
| Lean theorem closure | Partial | Canonical theorem repo separated |
| Full MGAP4D theorem closure | No | Canonical proof authority remains external boundary |
| Clinical systems | No | Not included in public repository |
| Private research kernels | No | Reserved surface |
| Operational credentials | No | Excluded from repository |
| Institutional deployment stack | No | Out of scope |

## Interpretation

KuuOS intentionally separates:

- publicly reviewable governance surfaces
- formal proof references
- operational deployment layers
- private or institutional infrastructure

This separation is part of the repository governance design.

## Reviewer Guidance

Reviewers should distinguish:

1. structural reproducibility
2. formal proof reproducibility
3. operational reproducibility
4. institutional deployment reproducibility

KuuOS currently emphasizes structural reproducibility of governance and validation surfaces.
