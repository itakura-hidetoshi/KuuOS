# KuuOS CodeAI GitHub CLI Capability v0.1

## Status

Additive operational capability bootstrap.

This surface makes the GitHub CLI (`gh`) directly usable from KuuOS GitHub
Actions and local CodeAI execution environments without storing a repository
secret. GitHub-hosted runners provide `gh`; the workflow binds the ephemeral
`github.token` to `GH_TOKEN` and fixes `GH_REPO` to the current repository.

## Boundary

The wrapper is deliberately read-only. It supports exactly:

- `probe`
- `repo-view`
- `pr-list`
- `pr-view <positive-pr-number>`
- `pr-checks <positive-pr-number>`
- `run-view <positive-run-id>`

It does not accept arbitrary `gh` arguments, shell fragments, write operations,
secret inspection, token display, branch mutation, PR mutation, merge,
deployment, or repository selection outside `GH_REPO`.

This capability does not replace CodeAI Autonomous Git Lifecycle v0.1. A later
write adapter must consume the exact one-effect lifecycle lease before mapping a
write operation to `gh` or `git`.

## GitHub Actions use

GitHub-hosted runners already contain the GitHub CLI. Each step that calls the
wrapper must provide `GH_TOKEN` and `GH_REPO`:

```yaml
env:
  GH_TOKEN: ${{ github.token }}
  GH_REPO: ${{ github.repository }}
```

The dedicated workflow grants only:

```yaml
permissions:
  contents: read
  pull-requests: read
  actions: read
```

No personal access token or repository secret is needed for these read-only
operations.

## Local use

Install and authenticate `gh`, then bind the repository:

```bash
gh auth login
export GH_TOKEN="$(gh auth token)"
export GH_REPO="itakura-hidetoshi/KuuOS"
bash scripts/kuuos_codeai_gh_v0_1.sh probe
```

Examples:

```bash
bash scripts/kuuos_codeai_gh_v0_1.sh pr-list
bash scripts/kuuos_codeai_gh_v0_1.sh pr-view 1299
bash scripts/kuuos_codeai_gh_v0_1.sh pr-checks 1299
```

The token is read only from the environment and is never appended to the command
arguments or emitted by the wrapper.

## Artifacts

- wrapper: `scripts/kuuos_codeai_gh_v0_1.sh`
- tests: `tests/test_kuuos_codeai_gh_v0_1.py`
- workflow: `.github/workflows/codeai-github-cli-capability-v0-1.yml`

## Validation

The dedicated workflow checks shell syntax, runs the fail-closed unit tests, and
executes a real authenticated `probe` plus `pr-list` against the current KuuOS
repository using the workflow token.
