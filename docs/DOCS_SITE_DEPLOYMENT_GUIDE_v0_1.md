# Docs Site Deployment Guide v0.1

## Purpose

This document explains the intended GitHub Pages deployment surface for the KuuOS public documentation site.

## Components

| Component | Role |
|---|---|
| `mkdocs.yml` | MkDocs site configuration |
| `docs/index.md` | Public documentation landing page |
| `.github/workflows/docs_pages.yml` | Automated GitHub Pages deployment workflow |

## Deployment Model

```text
main branch updates
    ↓
GitHub Actions workflow
    ↓
MkDocs build
    ↓
GitHub Pages deployment
```

## Trigger Conditions

The documentation deployment workflow triggers on:

- updates inside `docs/`
- updates to `mkdocs.yml`
- updates to the deployment workflow itself

## Build Command

```bash
mkdocs build --strict
```

## Intended Public Outcome

The resulting site provides:

- reviewer onboarding
- governance navigation
- architecture diagrams
- validation documentation
- terminology references
- reproducibility guidance

## Important Boundary

The documentation site is a public governance and review surface.

It does not automatically imply:

- theorem authority
- deployment authorization
- institutional approval
- clinical authority
