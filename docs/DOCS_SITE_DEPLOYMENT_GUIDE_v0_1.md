# Docs Site Deployment Guide v0.1

## Purpose

This document explains the intended GitHub Pages deployment surface for the KuuOS public documentation site.

## Components

| Component | Role |
|---|---|
| `mkdocs.yml` | MkDocs site configuration |
| `docs/index.md` | Public documentation landing page |
| `.github/workflows/docs_pages.yml` | Automated GitHub Pages deployment workflow |

## Required GitHub Repository Setting

GitHub Pages must be enabled in repository settings before `actions/deploy-pages` can create a deployment.

Required setting:

```text
Repository Settings
  -> Pages
  -> Build and deployment
  -> Source: GitHub Actions
```

Status note:

```text
GitHub Pages source has been enabled as GitHub Actions.
```

If this setting is not enabled, the workflow may build successfully and upload the Pages artifact, but deployment can fail with:

```text
Creating Pages deployment failed
HttpError: Not Found
Ensure GitHub Pages has been enabled
```

## Deployment Model

```text
main branch updates
    ↓
GitHub Actions workflow
    ↓
MkDocs build
    ↓
Pages artifact upload
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

## Manual Re-run

After enabling GitHub Pages, rerun:

```text
Actions
  -> Docs Pages
  -> Run workflow
```

or push a small documentation update to trigger the workflow again.

## Troubleshooting

| Symptom | Likely Cause | Action |
|---|---|---|
| `HttpError: Not Found` during deploy | GitHub Pages not enabled | Set Pages source to GitHub Actions |
| MkDocs strict build fails | Broken nav link or markdown issue | Fix `mkdocs.yml` or missing doc |
| Artifact upload succeeds but deploy fails | Pages deployment setting or permission issue | Check Pages setting and workflow permissions |

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
