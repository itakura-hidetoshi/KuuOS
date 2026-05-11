# KuuOS Pull Request Checklist

## Summary

Describe the append-only or tighten-only change.

## Required Full Check

- [ ] `make all-governance-checks` passes locally, or the reason it was not run is documented.
- [ ] GitHub Actions `All Governance Validation` is expected to pass.

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

## Runtime / Fixtures

- [ ] Minimal runtime examples still execute.
- [ ] Fixtures match minimal runtime behavior.
- [ ] Non-authority fields remain false.
- [ ] Hash-chain fixtures remain structurally consistent.
- [ ] WORM receipt root matches ledger fixture.
- [ ] Release bundle manifest validates.

## Authority Boundary

- [ ] This PR does not grant execution authority.
- [ ] This PR does not grant proof authority.
- [ ] This PR does not grant clinical authority.
- [ ] This PR does not claim direct base-model transformation without explicit evidence.
- [ ] Validation pass is not treated as truth, Ten'i, or execution authority.
