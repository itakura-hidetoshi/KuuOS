# Governance Release Gate v0.1

## 1. Gate Doctrine

KuuOS treats release as a governed transition, not as a mere file update.

A file, theorem, validator, module, or policy is not promoted merely because it exists. Promotion requires a release gate.

## 2. Canonical Status Values

| Status | Meaning |
|---|---|
| DRAFT | Work in progress. Not authoritative. |
| REVIEW | Ready for internal or external review. |
| HOLD | Insufficient support, unresolved uncertainty, or pending evidence. |
| PASS | Local criteria satisfied for the declared scope. |
| CONDITIONAL | Usable only under stated assumptions and boundaries. |
| FAIL | Criteria not satisfied. |
| RELEASED | Publicly released for the declared non-execution scope. |
| SUPERSEDED | Replaced by a later additive or tightening artifact. |

## 3. Required Gate Conditions

A release candidate should include:

- clear scope,
- version,
- provenance,
- copyright status,
- assumptions,
- known limitations,
- validation or proof status,
- public/private boundary check,
- non-execution statement.

## 4. Non-Execution Lock

Release does not grant direct execution authority. KuuOS public-core releases are specification and review surfaces unless a separate runtime deployment contract explicitly states otherwise.

## 5. Additive / Tightening Updates

Future changes should be:

- additive-only when expanding scope,
- tighten-only when changing governance,
- never silently weakening a prior safety or attribution boundary,
- never overwriting historical lineage.

## 6. Default Failure Mode

If the gate cannot determine safety, attribution, scope, or proof status, it returns HOLD.
