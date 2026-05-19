# Qi Bensho Treatment Route Candidate v0.2J

`KuOS.QiBenshoTreatmentRouteCandidate.v0_2J` adds the non-executing route layer after `QiFieldBundle` and `QiBenshoReadout`.

This layer treats treatment language as a bounded transport hypothesis over a Qi field. It does not diagnose, prescribe, select a formula, execute an intervention, or grant clinical authority.

## Definition

A treatment route is a non-executing, non-prescriptive, non-diagnostic field-deformation candidate constructed from a Qi field bundle and a Bensho readout.

```text
QiFieldBundle
  -> QiBenshoReadout
  -> QiTreatmentRouteCandidate
  -> DecisionOS safety-evaluable candidate
```

## Route semantics

Route families such as `harmonize`, `supplement`, `drain`, `warm`, `cool`, `moisten`, `dry`, `raise`, `descend`, `disperse`, `consolidate`, `open`, `close`, `transform`, `stabilize`, `reobserve_only`, and `abstain` are non-authoritative symbolic route families.

They are not prescriptions, not formula selections, and not execution instructions.

## Required gates

- source Qi field bundle is required
- source Bensho readout is required
- recoverability gate is required before route commitment
- contradiction gate is required
- barrier conditions are required
- stop conditions are required
- reobservation plan is required
- DecisionOS safety evaluation is required before any downstream release
- MemoryOS records are append-only

## Authority boundary

The route candidate grants no execution, commit, belief-root commit, memory overwrite, world-root rewrite, clinical, diagnosis, prescription, formula-selection, proof, truth, ontology, safety-override, or Ten'i authority.

## Forbidden collapses

- pattern to treatment execution
- pattern to prescription
- route to formula selection
- route to clinical instruction
- route to truth authority
- route to safety override
- local symptom to route certainty
- recoverability to execution permission
- smooth route to commit authority
- traditional label to action authority

## Canonical outcome

`QiTreatmentRouteCandidate` remains candidate-only. Valid outputs include route candidate, hold, reobserve, abstain, and handover to a safety-governed surface.
