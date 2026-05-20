# Public Audit Checklist v0.1

## Governance Surface

- [ ] README is present
- [ ] governance index is reachable
- [ ] quickstart document is reachable
- [ ] external review guide is reachable
- [ ] architecture overview is reachable

## Boundary Visibility

- [ ] non-authority policy exists
- [ ] theorem boundary is explicit
- [ ] deployment boundary is explicit
- [ ] medical-modality-neutral Qi boundary is explicit
- [ ] candidate-versus-authority distinction is explicit

## Validation Surface

- [ ] Makefile exists
- [ ] validator scripts exist
- [ ] workflow entrypoints exist
- [ ] validation coverage matrix exists
- [ ] reproducibility matrix exists

## Qi Motion Chain Surface

- [ ] `docs/QI_MOTION_CHAIN_RUNBOOK_v0_1.md` is reachable
- [ ] `docs/MEDICAL_MODALITY_NEUTRAL_QI_BOUNDARY_v0_1.md` is reachable
- [ ] `make qi-motion-chain-checks` is documented
- [ ] `scripts/run_qi_motion_chain_checks_v0_1.py` is reachable
- [ ] `.github/workflows/qi_motion_chain_validation.yml` is reachable
- [ ] Samvrti Qi acceptance is not treated as FullPathQi promotion
- [ ] conservative evidence building is explicit
- [ ] evidence-bound classification is explicit
- [ ] validated type licenses dynamics terms
- [ ] unlicensed motion terms are ignored
- [ ] Qi motion candidate remains observe-only
- [ ] Qi motion chain does not grant execution, standalone diagnosis, standalone treatment authorization, medical act authorization, institutional, or theorem authority
- [ ] Qi medical wording does not imply that biomedicine is superior, Qi is false, or East Asian medical reasoning is invalid

## Reproducibility

- [ ] validators can be run locally
- [ ] public scripts are reachable
- [ ] manifests are inspectable
- [ ] packet chains are inspectable
- [ ] Qi motion chain is reproducible through local Makefile and GitHub Actions

## Governance Integrity

- [ ] append-only orientation is documented
- [ ] fail-closed orientation is documented
- [ ] provenance orientation is documented
- [ ] rollback visibility is documented

## Canonical Separation

- [ ] canonical theorem repository is identified
- [ ] KuuOS does not claim replacement authority
- [ ] governance validation is separated from theorem closure
- [ ] Qi motion validation is separated from standalone diagnosis, standalone treatment authorization, medical act authorization, and execution authority

## Reviewer Recommendation

A reviewer should treat successful completion of this checklist as evidence of:

- structural governance maturity
- explicit boundary awareness
- public reviewability

A reviewer should not treat this checklist alone as evidence of:

- theorem correctness
- production safety
- institutional approval
- standalone diagnosis authority
- standalone treatment authorization
- medical act authorization
- Qi-based execution authorization