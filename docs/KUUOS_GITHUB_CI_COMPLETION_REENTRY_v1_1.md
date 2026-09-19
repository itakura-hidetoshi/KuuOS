# KuuOS GitHub CI Completion Reentry v1.1

## Purpose

This layer turns a completed GitHub Actions event into a bounded KuuOS re-entry signal. The event is not CI truth and is not merge authority.

```text
GitHub workflow completion event
→ completion-event intake
→ exact event identity packet
→ status re-observation request
→ fresh GitHub MCP observation
→ exact repository / run / workflow / head SHA comparison
→ jobs and required steps re-observed
→ verified success or verified non-success re-entry
```

Core invariant:

```text
event observed != CI verified
event conclusion == success != success evidence
fresh MCP re-observation + exact identity + completed required surfaces = verified observation re-entry
verified observation re-entry != merge authority
verified observation re-entry != write authority
```

## Runtime carrier

`runtime/kuuos_github_ci_completion_reentry_v1_1.py` accepts same-repository `workflow_run` completion events and cross-repository `repository_dispatch` events of type `kuuos_ci_completion_v1_1`.

The intake binds repository, run ID, workflow name, exact 40-hex head SHA, branch, status and terminal conclusion. A cross-repository payload may additionally bind `required_job_names` and `required_step_names`; this is intended for repositories such as `itakura-hidetoshi/4d-mass-gap`, where an exact Lean step can be required.

A sender must use independently configured cross-repository authority such as a GitHub App installation token or a fine-grained token allowed to dispatch to KuuOS. The source repository's ordinary `GITHUB_TOKEN` is not silently treated as cross-repository authority.

## Output packets

A valid event emits `qi_github_actions_ci_completion_event_packet.json` and `qi_github_actions_status_reobserve_request.json`. The request is compatible with the existing Qi GitHub Actions Status Reobserver v5.8 `workflow_run_jobs` surface.

The event packet always records `signal_is_success_evidence = false` and `fresh_mcp_reobservation_required = true`.

## Fresh MCP verification

`verify_fresh_reobservation(...)` requires a fresh observation to match repository, workflow run ID, workflow name, exact head SHA, completed status and conclusion. It also requires fresh jobs and, when configured, exact required job and step names to be present and completed.

A successful workflow routes to `verified_success`. A completed non-success workflow routes to `verified_non_success`; this is a failure/triage re-entry, not a success promotion. Both preserve `merge_authority_granted = false` and `write_authority_granted = false`.

## Formal boundary

`formal/KuuOSGitHubMCPServerBridgeV0_1/V1_1.lean` defines `CICompletionReentryGate.Admitted`. Lean proves that event-only admission, wrong-head admission, pending-workflow admission, pending-required-step admission, event-as-success-evidence admission, merge-authority derivation and write-authority derivation are all impossible.

## GitHub Actions ingress

`.github/workflows/kuuos-github-ci-completion-reentry-v1-1.yml` listens to selected KuuOS `workflow_run: completed` events and the cross-repository `repository_dispatch` event `kuuos_ci_completion_v1_1`. It does not add a second pull-request gate; PR validation remains in `pr-governance-gate.yml` and the check registry.

The retained workflow publishes a bounded handoff artifact containing the event packet and MCP re-observation request.

## MCP / wake-up boundary

MCP is used for the authoritative fresh observation after an event signal. A stateless MCP server is not an unsolicited notification bus, so this repository layer deliberately separates event ingress from MCP client/runtime activation.

An external KuuOS runtime, ChatGPT task runner, GitHub App, or another authorized consumer can pick up the bounded signal and then invoke the GitHub MCP observation path. This version adds no implicit external credential, no automatic merge, and no automatic write action.
