# Diagram Export Guide v0.1

## Purpose

This document explains the intended Mermaid diagram export surface for KuuOS.

## Source Documents

| Document | Role |
|---|---|
| `docs/ARCHITECTURE_DIAGRAM_v0_1.md` | Architecture flow diagram |
| `docs/GOVERNANCE_DIAGRAM_v0_1.md` | Governance flow diagram |
| `docs/VALIDATOR_GRAPH_v0_1.md` | Validator dependency graph |

## Export Workflow

Workflow:

```text
.github/workflows/export_diagrams.yml
```

## Export Model

```text
Mermaid markdown
    ↓
Mermaid extraction
    ↓
Mermaid CLI export
    ↓
SVG artifact generation
```

## Generated Artifacts

The workflow exports:

- `architecture.svg`
- `governance.svg`
- `validator_graph.svg`

These artifacts are uploaded as GitHub Actions artifacts.

## Intended Use

Generated SVG files may be used for:

- reviewer onboarding
- documentation sites
- release bundles
- architecture posters
- governance presentations
- whitepaper integration

## Boundary

Diagram export artifacts visualize repository governance and architecture surfaces.

They do not automatically imply:

- theorem closure
- institutional approval
- deployment authorization
- execution authority
