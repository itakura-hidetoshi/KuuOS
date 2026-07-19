#!/usr/bin/env bash
set -euo pipefail

readonly KUUOS_GH_PROFILE="CodeAI GitHub CLI Capability v0.1"
readonly GH_BIN="${KUUOS_GH_BIN:-gh}"
readonly OPERATION="${1:-probe}"
readonly TARGET="${2:-}"

fail() {
  printf 'kuuos-gh: %s\n' "$1" >&2
  exit 2
}

[[ -n "${GH_TOKEN:-}" ]] || fail "GH_TOKEN is required"
[[ -n "${GH_REPO:-}" ]] || fail "GH_REPO is required"
[[ "${GH_REPO}" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || \
  fail "GH_REPO must use owner/repository form"
command -v "${GH_BIN}" >/dev/null 2>&1 || fail "GitHub CLI executable not found: ${GH_BIN}"

export GH_PAGER=cat
export GH_PROMPT_DISABLED=1
export NO_COLOR=1

positive_integer() {
  [[ "$1" =~ ^[1-9][0-9]*$ ]]
}

case "${OPERATION}" in
  probe)
    "${GH_BIN}" --version >&2
    "${GH_BIN}" auth status --active --hostname github.com >&2
    exec "${GH_BIN}" repo view "${GH_REPO}" \
      --json nameWithOwner,defaultBranchRef,isPrivate,url
    ;;
  repo-view)
    [[ -z "${TARGET}" ]] || fail "repo-view accepts no target"
    exec "${GH_BIN}" repo view "${GH_REPO}" \
      --json nameWithOwner,defaultBranchRef,isPrivate,url
    ;;
  pr-list)
    [[ -z "${TARGET}" ]] || fail "pr-list accepts no target"
    exec "${GH_BIN}" pr list --repo "${GH_REPO}" --limit 20 \
      --json number,title,state,isDraft,headRefName,baseRefName,url
    ;;
  pr-view)
    positive_integer "${TARGET}" || fail "pr-view requires a positive PR number"
    exec "${GH_BIN}" pr view "${TARGET}" --repo "${GH_REPO}" \
      --json number,title,state,isDraft,headRefName,baseRefName,mergeStateStatus,url,statusCheckRollup
    ;;
  pr-checks)
    positive_integer "${TARGET}" || fail "pr-checks requires a positive PR number"
    exec "${GH_BIN}" pr checks "${TARGET}" --repo "${GH_REPO}" \
      --json name,state,bucket,link
    ;;
  run-view)
    positive_integer "${TARGET}" || fail "run-view requires a positive workflow run id"
    exec "${GH_BIN}" run view "${TARGET}" --repo "${GH_REPO}" \
      --json databaseId,status,conclusion,event,headSha,workflowName,url
    ;;
  *)
    fail "unsupported read-only operation: ${OPERATION}"
    ;;
esac
