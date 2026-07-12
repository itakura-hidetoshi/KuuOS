# VerifyOS v0.10 Dukkha-Preserving Realized-Dukkha Verification Disposition Intake v0.1

## Purpose

VerifyOS v0.10 verifies whether an already bounded and causally attributed WORLD change produced an actually realized reduction in dukkha.

The layer begins only after three distinct receipts already exist:

```text
WORLD mutation application
!= post-application evidence
!= bounded WORLD fact confirmation
!= bounded causal-attribution verification
```

Its input state is:

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_realization_pending
```

The supported transition is:

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_realization_pending
->
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_reduction_realized_confirmed
```

The transition confirms only an exact bounded realized reduction under the supplied outcome-measure, assessment-window, uncertainty, calibration, provenance, durability, and nonexternalization contract.

## Source boundary

The runtime accepts a supported VerifyOS v0.9 WORLD causal-attribution verification receipt.

It revalidates the source receipt digest and the following nested artifacts:

- WORLD causal-attribution evidence packet;
- WORLD causal-attribution verification review certificate;
- causal-attribution verification record;
- causal-attribution verification debt-consumption record;
- bounded WORLD causal-attribution binding;
- dukkha-realization verification handoff envelope.

The source must establish:

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = false
```

The causal scope must remain exactly bounded.

The source handoff must keep realized dukkha in `pending_independent_verification` state.

## Independent realized-dukkha evidence

The evidence packet binds the complete source causal receipt and its bounded causal binding.

It also binds:

- candidate fact and relation digests;
- WORLD state and revision;
- persistent storage target;
- expected WORLD postcondition;
- causal model and causal query;
- intervention and counterfactual estimand;
- the previously observed realized-dukkha artifact;
- baseline dukkha assessment;
- post-intervention dukkha assessment;
- outcome-measure specification;
- assessment window;
- minimum clinically meaningful reduction threshold;
- effect estimate, direction, magnitude, and confidence interval;
- durability evidence;
- adverse-effect offset assessment;
- distributional impact assessment;
- protected-group impact;
- future-subject impact;
- uncertainty;
- calibration;
- provenance;
- tamper evidence.

The evidence collector and evidence source remain distinct.

The evidence collection performs no WORLD mutation.

The evidence packet does not preconfirm realized dukkha reduction.

## Independent review

The review verifies correspondence among the source causal binding, the outcome evidence, and the exact bounded dukkha claim.

It checks:

- source bounded fact confirmation;
- source bounded causal attribution;
- causal-binding correspondence;
- baseline correspondence;
- post-intervention outcome correspondence;
- measurement validity;
- assessment-window adequacy;
- clinically meaningful reduction threshold;
- effect direction and magnitude;
- durability;
- adverse-effect offset;
- distributional impact;
- uncertainty;
- calibration;
- provenance continuity;
- protected-group nonexternalization;
- future-subject nonexternalization;
- exact bounded scope.

The review may not reopen causal attribution.

The review may not preconfirm realized dukkha reduction.

The review may not generalize the benefit claim beyond the exact bound.

## Dispositions

The intake separates twenty routes:

1. `realized_dukkha_verification_supported`
2. `world_refresh_required`
3. `dukkha_realization_context_refresh_required`
4. `dukkha_realization_review_refresh_required`
5. `additional_realized_dukkha_evidence_required`
6. `baseline_dukkha_correspondence_repair_required`
7. `post_intervention_dukkha_correspondence_repair_required`
8. `dukkha_measurement_validity_repair_required`
9. `dukkha_assessment_window_repair_required`
10. `causal_binding_correspondence_repair_required`
11. `dukkha_effect_estimate_repair_required`
12. `dukkha_reduction_durability_review_required`
13. `adverse_effect_offset_review_required`
14. `distributional_impact_review_required`
15. `uncertainty_repair_required`
16. `calibration_repair_required`
17. `provenance_repair_required`
18. `nonexternalization_review_required`
19. `dukkha_realization_overclaim_rejected`
20. `replay_conflict_rejected`

## Supported route

The supported route issues exactly one realized-dukkha verification receipt.

It consumes the verification debt once.

It closes replay for:

- the source causal-attribution verification receipt;
- realized-dukkha evidence;
- realized-dukkha review;
- intake nonce;
- intake session.

It creates an exact bounded realized-dukkha confirmation binding.

It prepares a future-only learning handoff without activating learning or changing historical evidence.

The supported state establishes:

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = true
```

The confirmation remains limited to the supplied bounded fact, bounded relation, outcome measure, time window, effect estimate, uncertainty, calibration, provenance, and durability contract.

## Non-supported routes

Every non-supported route preserves:

```text
world_candidate_bounded_fact_causal_attribution_confirmed_dukkha_realization_pending
```

It also preserves:

```text
world_fact_confirmed = true
causal_attribution_confirmed = true
dukkha_reduction_realized_confirmed = false
realized_dukkha_verification_debt_open = true
```

A non-supported route does not close source-receipt replay.

## Fixed separation

```text
confirmed bounded WORLD fact
!= confirmed bounded causal attribution
!= realized-dukkha evidence packet
!= realized-dukkha verification receipt
!= generalized benefit claim
!= automatic plan completion
```

Realized dukkha confirmation is not a new WORLD mutation.

It does not reapply the WORLD patch.

It does not increment the WORLD revision.

It does not perform a tool invocation or external side effect.

It does not compensate, roll back, or complete a plan.

## Authority boundary

VerifyOS v0.10 has no:

- selection authority;
- plan-revision authority;
- dukkha-minimization authority;
- general execution authority;
- WORLD mutation authority.

DecisionOS retains selection ownership.

Evidence lineage and responsibility lineage grow monotonically.

## Runtime and formal connection

Runtime:

```text
runtime/kuuos_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_v0_1.py
```

Actual-chain checker:

```text
scripts/check_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_v0_1.py
```

Lean theorem package:

```text
formal/KUOS/VerifyOS/DukkhaPreservingRealizedDukkhaVerificationDispositionIntakeV0_10.lean
```

Formal root:

```text
formal/KuuOSVerifyOSV0_10.lean
```

Manifest:

```text
manifests/kuuos_verifyos_dukkha_preserving_realized_dukkha_verification_disposition_intake_v0_1.json
```

The cumulative Evidence Cycle runner executes the checker after VerifyOS v0.9.

## Natural successor

The next layer is a future-only learning or maintenance disposition intake over the confirmed bounded fact, bounded causal attribution, and bounded realized-dukkha confirmation.

That successor must not rewrite historical evidence or turn one bounded result into a universal policy claim.
