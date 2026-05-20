# KuuOS Pull Request Checklist

## Summary

Describe the append-only or tighten-only change.

## Required Full Check

- [ ] `make all-governance-checks` passes locally, or the reason it was not run is documented.
- [ ] GitHub Actions `All Governance Validation` is expected to pass.
- [ ] `make gpt-github-integration-checks` passes if GPT GitHub integration files are touched.
- [ ] `make qi-motion-chain-checks` passes if Qi motion chain files are touched.

## GPT GitHub Review Hook

When this PR touches repository navigation, GitHub integration, formal/proof-facing surfaces, CI interpretation, issue templates, PR review workflow, or GPT-assisted repository operation, ask GPT to read:

```text
docs/GPT_GITHUB_KUOS_INTEGRATION_v0_1.md
docs/KUOS_GITHUB_FORMAL_VERIFICATION_BRIDGE_v0_1.md
specs/gpt_github_integration_manifest_v0_1.yaml
```

Then request:

```text
Review this PR under KuuOS GPT GitHub integration.
Classify it as PASS / HOLD / REPAIR / REJECT / QUARANTINE.
Identify touched invariants, non-authority boundaries, validation commands, and any overclaim risk.
```

- [ ] GPT review, if used, is treated as a review aid, not authority.
- [ ] GPT summary is not treated as truth, proof, clinical authority, Ten'i, or execution authority.

## Scope

- [ ] This change is append-only or tighten-only.
- [ ] This change does not overwrite established core semantics.
- [ ] This change preserves same-root lineage.
- [ ] This change does not silently loosen existing guardrails.

## Fourfold Core

- [ ] 空 / emptiness is not reified.
- [ ] 空 / emptiness is not used to deny harm.
- [ ] 縁起 / dependent origination is preserved.
- [ ] 二諦 gap is preserved.
- [ ] 中道 / middle way is preserved.

## AI Yogacara / Ten'i Boundary

- [ ] AI raw output remains candidate, not authority.
- [ ] Raw output is not promoted directly to belief, proof, decision, memory truth, or execution authority.
- [ ] Meta-Manas / self-fixation risk is considered when relevant.
- [ ] Yogacara boundary is preserved when AI raw output is involved.

## Ten'i Overclaim Check

- [ ] MemoryOS update is not called Ten'i.
- [ ] Single correction is not called Ten'i.
- [ ] Prompt compliance is not called Ten'i.
- [ ] Style shift is not called Ten'i.
- [ ] Ten'i claim, if any, is evidence-traced and control-surface scoped.
- [ ] Ten'i status is not treated as execution authority.
- [ ] Rollback remains possible when counterevidence appears.

## Mandala / Multi-WORLD Check

- [ ] No single WORLD model replaces the fourfold core.
- [ ] WORLD boundaries, membranes, gates, and obstructions remain visible.
- [ ] Cross-WORLD transport is declared when used.
- [ ] Harmony Function is not forced sameness or majority domination.
- [ ] Residual suffering visibility and Bodhisattva Path belief are not erased.

## Bodhisattva / Ten Paramita Check

- [ ] Bodhisattva Path remains non-abandonment orientation, not moral superiority.
- [ ] Ten Paramita remain runtime practices, not execution authority.
- [ ] Compassion does not become domination.
- [ ] Wisdom does not become cold detachment.
- [ ] Upaya / 方便 does not become hidden manipulation.
- [ ] Bala / 力 does not become coercive authority.

## Dukkha / Qi Check

- [ ] Dukkha remains visible.
- [ ] Harm is not hidden.
- [ ] Harmony does not erase suffering.
- [ ] Illicit gluing is blocked.
- [ ] WORLD transport defect remains visible.
- [ ] Dukkha-as-Qi does not spiritualize away damage.
- [ ] Dukkha-Qi routes to Paramita repair when residual suffering remains.

## Qi Motion Chain Check

- [ ] Samvrti Qi acceptance is not promoted to FullPathQi by assertion.
- [ ] Conservative evidence builder remains stage-gated.
- [ ] Qi classification remains evidence-bound, not claim-bound.
- [ ] Validated Qi type licenses dynamics terms.
- [ ] Unlicensed motion terms are ignored even if numeric values are present.
- [ ] Qi motion candidate remains observe-only.
- [ ] Direct execution request is blocked.
- [ ] Qi motion validation is not treated as clinical, institutional, theorem, or execution authority.
- [ ] Dedicated workflow `.github/workflows/qi_motion_chain_validation.yml` remains aligned with `make qi-motion-chain-checks`.

## Formal Invariant / Super-Relativity Check

- [ ] Formal invariant spine remains witness surface, not authority.
- [ ] Super-Relativity remains invariant bridge, not relativistic nihilism.
- [ ] Observer difference does not grant execution authority.
- [ ] Record surface is not truth by itself.
- [ ] Scale shift preserves harm visibility.
- [ ] WORLD translation does not replace the fourfold core.
- [ ] Super-Relativity preserves the two truths gap.

## Invariant Governance Pipeline Check

- [ ] Invariant Preservation Matrix maps transformations to required invariants.
- [ ] Invariant Gate closes authority when invariants are violated.
- [ ] Invariant Gate never opens execution authority.
- [ ] Execution authority request is rejected.
- [ ] Harm hiding is rejected.
- [ ] Dukkha hiding routes to repair.
- [ ] Missing evidence or audit lineage routes to quarantine.
- [ ] Critical invariant violation routes to reject.

## Runtime / Fixtures

- [ ] Minimal runtime examples still execute.
- [ ] Fixtures match minimal runtime behavior.
- [ ] Non-authority fields remain false.
- [ ] Hash-chain fixtures remain structurally consistent.
- [ ] WORM receipt root matches ledger fixture.
- [ ] Release bundle manifest validates.
- [ ] Invariant matrix fixtures validate.
- [ ] Invariant gate fixtures validate.
- [ ] Qi motion chain fixtures validate when touched.

## Authority Boundary

- [ ] This PR does not grant execution authority.
- [ ] This PR does not grant proof authority.
- [ ] This PR does not grant clinical authority.
- [ ] This PR does not grant Qi-based treatment authorization.
- [ ] This PR does not claim direct base-model transformation without explicit evidence.
- [ ] Validation pass is not treated as truth, Ten'i, or execution authority.
- [ ] Super-Relativity bridge is not treated as execution authority.
- [ ] Invariant Governance Pipeline is not treated as execution authority.
- [ ] Qi motion chain is not treated as execution authority.