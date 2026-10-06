# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS / 空OS** is a public research architecture for dependent origination (縁起), contextual transport, higher coherence, descent, obstruction, exact presentation, universal properties, and bounded AI operation. Founder: **Hidetoshi Itakura / 板倉英俊**.

> Which structure survives justified changes of context and presentation, how can compatible local information be transported and glued, and which universal property characterizes the invariant content?

## Current formal status — v5.57

**2026-10-07 JST：v5.57 / PR #2013 まで canonical main に統合済み。**

The current actual-lift classification layer now has one integrated Lean certificate built from the **same** forward pseudofunctor, quasi-inverse, unit, counit, actual triangle pastes, and native invertible modifications.

~~~text
L = ExactLiftableClassificationObject
    with actual-lift-carrying 1-cells
E = ExactUniversalClassificationObject

F : L -> E
G : E -> L

eta : Id_L => F ; G
eps : G ; F => Id_E

T_F : F => F
T_G : G => G

C_F : T_F ~= Id_F
C_G : T_G ~= Id_G
~~~

The integrated endpoint is `exactLiftableActualLiftCoherentBiequivalenceCertificate` in [v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean). It reuses the generic universe-explicit certificate **types** from the earlier classification layer, but stores the actual-lift constructions themselves. It does not substitute the older localized-classification triangles.

## Reproducible theorem snapshot

| Role | Exact reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Latest theorem-bearing merge | **`d6b2b2055ac9a797d5569ab30591eeabfeac319c`** |
| Theorem PR | [#2013 — v5.57](https://github.com/itakura-hidetoshi/KuuOS/pull/2013), merged |
| Validated PR head | `e6f4aa998effe96a1edd0dcdc9e1dfd050b8cd0c` |
| Validation run | [37546110315](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37546110315), attempt 1, success |
| Strict Lean / governance | `112550485327` / `112551238667`, success |
| Lean / terminal receipts | `112551238701` / `112551307761`, success |
| Actual CI checkout | synthetic merge `7f1b58050c50acc86e94c12124cf0dea0ab7e2cd` |
| Build | `8684/8684`; return code `0` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

The inspected v5.57 target has zero Lean errors, zero target warnings, and no `sorryAx` / `uses 'sorry'`. Its 28 queried declarations report only `propext`, `Classical.choice`, and `Quot.sound`. Existing dependencies still contribute 116 warnings across 37 files; this is **not** a repository-wide warning-free claim.

Authority order:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

The separate [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Lean 4.31 validation lane remains **open / draft / unmerged**, head `3a09839782ea82661ddbf8e13a0fd08e893079b4`. It is outside canonical theorem authority. Do not merge it, mark it ready for review, or enable auto-merge.

## What 空 means here

空 is not “nothing exists.” Its operational role is non-reification: a chosen presentation is not intrinsic substance, a local observation is not global truth, equivalent carriers do not erase provenance or world binding, and successful execution is not theorem authority.

KuuOS separates observation from inference, identifies the active context, retains multiple presentations, tracks relations and history, checks local compatibility and descent, exposes obstructions, respects authority boundaries, performs only justified actions, and re-observes afterward.

The formal program uses systems, mappings, transformations between mappings, bicategorical coherence, descent, obstruction classes, exact presentations, and universal properties. These structures organize reasoning; they do not make an LLM automatically correct or authorize external actions.

## Exact-liftability boundary

The positive classification chain uses the aligned atlas specialization:

~~~text
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

and keeps external world and presentation labels explicit. The obstruction boundary remains:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility

converse: false in general
~~~

The actual-lift layer therefore does **not** assert arbitrary raw-morphism liftability, arbitrary atlas-universe reindexing, equality of independently chosen presentations, or strict preservation of a conjugated raw map.

## Current classification chain

| Stage | Integrated result | Source |
| --- | --- | --- |
| v4.00-v4.48 | Nonfactorization, Stage-II obstruction, recursive/inverse-limit carriers, orientation/descent | [v4.48](formal/KUOS/DependentOriginationStageIIOrbitOrientationDescentV4_48.lean) |
| v4.49-v5.16 | Exact-universal source, realization, hom equivalences, ambient section/unit/counit and coherent triangles | [v5.16](formal/KUOS/DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16.lean) |
| v5.17-v5.31 | Label-sensitive classification, global unit/counit, triangle representatives and modifications | [v5.31](formal/KUOS/DependentOriginationClassificationCoherentBiequivalenceV5_31.lean) |
| v5.32-v5.36 | Aligned exact-liftability, coherent presentation witnesses, coherent universalization | [v5.36](formal/KUOS/DependentOriginationExactLiftableCoherentUniversalizationV5_36.lean) |
| v5.37-v5.42 | Morphism liftability, actual-lift 1-cells, bicategory, strict projection `F` | [v5.42](formal/KUOS/DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42.lean) |
| v5.43-v5.48 | Local hom equivalence, object coverage, Whitehead data, explicit non-strict `G` | [v5.48](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean) |
| v5.49-v5.50 | Native target counit `eps` and source unit `eta` | [v5.49](formal/KUOS/DependentOriginationExactLiftableActualLiftTargetCounitV5_49.lean), [v5.50](formal/KUOS/DependentOriginationExactLiftableActualLiftSourceUnitV5_50.lean) |
| v5.51-v5.52 | Both pointwise contractions; actual forward triangle and global invertible modification | [v5.52](formal/KUOS/DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52.lean) |
| v5.53-v5.56 | Non-strict reverse factors, reassociation, actual reverse triangle and global invertible modification | [v5.56](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56.lean) |
| **v5.57** | **One certificate containing the same Whitehead/F/G/eta/eps, both actual triangles, and both native invertible modifications** | [v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean) |

## Actual-lift pair and its roundtrips

The v5.40 1-cell stores a prescribed label-preserving raw one-cell, an actual exact-universal lift, and equality of the actual lift's raw map with the prescribed raw map. Identity and composition use the stored lifts directly; no equality of independently chosen lifts is required.

For `Y : E`, the quasi-inverse uses `G(Y) := Y.toExactLiftable` and one fixed adjoint equivalence `eY : F(GY) ~ Y`. For `k : Y -> Z`, its stored actual lift is the conjugated map:

~~~text
(eY.hom ; k) ; eZ.inv
~~~

The later roundtrip construction does not make this `G` strict.

v5.49-v5.57 close the frontier that was open in the previous README:

- **v5.49:** native `G ; F => Id_E` counit.
- **v5.50:** native `Id_L => F ; G` unit and its object equivalences.
- **v5.51:** pointwise contractions of both actual triangle composites.
- **v5.52:** actual forward triangle plus global invertible modification.
- **v5.53-v5.54:** reverse factors for non-strict `G`, including explicit reassociation coherence.
- **v5.55:** actual reverse triangle `eta_(G Y) ; G(eps_Y)`.
- **v5.56:** global invertible modification for that actual reverse paste.
- **v5.57:** one integrated certificate storing all of the above with the v5.45 Whitehead data.

The generic certificate type permits triangle representatives. The v5.57 concrete value proves that its representatives are the actual native pastes by whole-record equations. KuuOS does **not** infer a stronger unnamed tricategorical adjoint-biequivalence structure beyond these proved fields.

## Current research frontier

The old “construct unit/counit and triangle modifications” frontier is closed. The next work is:

1. **Higher coherence interface:** specify and formalize any additional adjoint-biequivalence / tricategorical coherence genuinely intended beyond the current StrongTrans/modification package.
2. **Broader mapping principle:** determine the exact hypotheses under which the exact-sector classification extends further. Weak admissibility alone is insufficient.
3. **Descent and presentation independence:** continue separating fixed-presentation equivalence, coherent transport, and genuine descent across presentation changes.
4. **AI-facing use:** connect the formal contextual/coherence layer to reasoning and retrieval while preserving provenance, authority, and re-observation boundaries.

These are research directions, not theorem claims.

## Validation and reproduction

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout d6b2b2055ac9a797d5569ab30591eeabfeac319c

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57
~~~

Useful earlier endpoints:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16 \
  KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31 \
  KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45 \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48 \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56
~~~

Aggregate/runtime entry points remain separate:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

The successful v5.57 receipt is evidence for the selected target-and-dependency build, not a claim that every aggregate/runtime command was rerun in this documentation update.

See [ROADMAP.md](ROADMAP.md) for the detailed milestone ledger, validation evidence, remaining obligations, and Lean proof-engineering lessons.
