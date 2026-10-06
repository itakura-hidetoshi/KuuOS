# KuuOS / 空OS Roadmap

**Theorem snapshot: 2026-10-07 JST · integrated through v5.57**

**現在地：actual-lift 分類双圏 (L) と exact-universal 分類双圏 (E) の同じ (F,G,eta,eps) について、両方向の実際の三角貼り合わせと native な可逆 modification を完成し、v5.57 で Whitehead データと一つの統合証明書に格納した。以前の「global unit/counit と triangle coherence が未完成」という残件は閉じた。**

This roadmap distinguishes integrated Lean constructions from proposed research obligations. It does not upgrade the proved native StrongTrans/modification package into a stronger unnamed tricategorical structure.

## 0. Exact theorem baseline and evidence

| Role | Reference |
| --- | --- |
| Repository / canonical branch | `itakura-hidetoshi/KuuOS` / **main** |
| Latest theorem-bearing merge | **`d6b2b2055ac9a797d5569ab30591eeabfeac319c`** |
| Theorem PR | [#2013](https://github.com/itakura-hidetoshi/KuuOS/pull/2013), v5.57, merged |
| Validated exact PR head | `e6f4aa998effe96a1edd0dcdc9e1dfd050b8cd0c` |
| Validation run | [37546110315](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37546110315), attempt 1, success |
| Strict Lean / governance | `112550485327` / `112551238667`, success |
| Lean / terminal receipts | `112551238701` / `112551307761`, success |
| Actual validation checkout | synthetic PR merge `7f1b58050c50acc86e94c12124cf0dea0ab7e2cd` |
| Build | `8684/8684`; passed; return code `0` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| Mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |

Latest endpoint: [v5.57 integrated certificate](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean).

Artifact `11450747190`, `audit-check-lean-formal-37546110315-1`, SHA-256:

~~~text
408b5fcef7e2b5e58454b90c794530c54c38e9a37150369e1afc0bf45b6c7617
~~~

The complete inspected check log has 2,629 lines. The v5.57 target has zero Lean errors, zero target warnings, and no `sorryAx` / `uses 'sorry'`. All 28 queried declarations report only `propext`, `Classical.choice`, and `Quot.sound`. Existing dependencies retain 116 warnings across 37 files.

Authority remains:

~~~text
fresh exact canonical GitHub SHA
  > formal Lean theorem artifacts at that SHA
  > README / ROADMAP
  > exact-head CI/runtime receipts
  > history / conversation memory
~~~

**Protected lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) remains Lean 4.31 validation-only, **open / draft / unmerged**, head `3a09839782ea82661ddbf8e13a0fd08e893079b4`. It is outside canonical theorem authority.

## 1. Three distinct equivalence interfaces

| Interface | Integrated data | Boundary |
| --- | --- | --- |
| Exact-universal raw source -> ambient DO₂ completion | v5.09-v5.16: coverage, Whitehead data, section, unit/counit, coherent triangle package | No stronger unnamed tricategorical object is asserted |
| Exact-universal classification -> localized classification | v5.21-v5.31: labelled bicategories, local equivalence, coverage, section, unit/counit, coherent triangle package | External labels remain explicit |
| Actual-lift exact-liftable classification -> exact-universal classification | **v5.40-v5.57: bicategory, strict F, Whitehead data, non-strict G, unit/counit, both actual triangles, both invertible modifications, integrated certificate** | Arbitrary raw morphisms and stronger higher coherence are not added |

The first two interfaces remain valid. They are not substitutes for the third, and the third no longer has unit/counit or triangle modifications on its open-task list.

## 2. Retained foundations — v4.00-v5.36

| Versions | Integrated content |
| --- | --- |
| v4.00-v4.12 | Exact C2 nonfactorization and nonzero Stage-II obstruction in ZMod 2 |
| v4.13-v4.48 | Incidence/capacity obstructions, recursive and inverse-limit carriers, exact Cantor dimension, switch/orientation descent |
| v4.49-v4.89 | Presentation descent, exact universal targets, source bicategory, strict realization, hom equivalences, labelled global package |
| v4.90-v5.08 | Restriction universality and coherent StrongTrans extension through localization |
| v5.09-v5.16 | Ambient Whitehead/section/unit/counit and coherent triangle package |
| v5.17-v5.31 | Label-sensitive exact-universal/localized classification and coherent certificate |
| v5.32-v5.35 | Aligned exact-liftability and coherent presentation witnesses |
| v5.36 | Coherent exact-universal target on the original raw system, with fixed-raw mutual coherent uniqueness |

The positive implication chain remains:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

The converse is false in general.

## 3. Actual-lift bicategory and forward map — v5.37-v5.45

v5.37 gives the exact raw-morphism liftability criterion. v5.38-v5.39 bundle liftable maps and form local hom categories.

v5.40 refines a 1-cell to carry:

~~~text
raw        : prescribed label-preserving raw one-cell
actualLift : ExactUniversalClassificationOneCell (F X) (F Y)
raw_eq     : actualLift.map.raw = raw.map
~~~

This is the key global-composition refinement: identity and composition use the stored exact-universal lifts rather than independently chosen lifts.

v5.41 constructs the actual-lift bicategory. v5.42 constructs the strict projection `F`. v5.43-v5.44 prove local hom equivalence and label-preserving object coverage. v5.45 packages `WhiteheadBiequivalenceData`.

## 4. Explicit non-strict quasi-inverse — v5.46-v5.48

For each `Y : E`, fix once:

~~~text
G.obj Y := Y.toExactLiftable
eY : F(GY) ~ Y
~~~

For `k : Y -> Z`, the actual lift of `G(k)` is:

~~~text
(eY.hom ; k) ; eZ.inv
~~~

v5.47 proves horizontal naturality for arbitrary 2-cells. v5.48 proves associator and both unitor coherence laws and assembles the native `Pseudofunctor` without replacing its original `mapId` or `mapComp`.

## 5. Native unit and counit — v5.49-v5.50

### v5.49 — target counit

`actualLiftTargetRoundtripCounit` constructs:

~~~text
G ; F => Id_E
~~~

using the already fixed object equivalences.

### v5.50 — source unit

`actualLiftSourceRoundtripUnit` constructs:

~~~text
Id_L => F ; G
~~~

with native StrongTrans coherence. `actualLiftSourceUnitComponentEquivalence` records the corresponding objectwise equivalences.

These are the unit and counit used by all later triangle constructions. They are not replaced by a new pair.

## 6. Forward triangle — v5.51-v5.52

v5.51 constructs pointwise contractions for both directions.

v5.52 builds the **actual forward triangle** as the native vertical paste of the unit projected through `F` and the restricted counit. Its contraction becomes the global invertible modification:

~~~text
actualLiftForwardTriangleModificationIso
~~~

Thus the forward triangle is not merely represented by another transformation with equal components.

## 7. Reverse triangle for non-strict G — v5.53-v5.56

This is the main coherence extension after the previous documentation snapshot.

### v5.53 — first factor

Construct:

~~~text
eta_G : G => G ; (F ; G)
~~~

without assuming `G` strict. The proof uses the actual `G.mapId` and `G.mapComp`.

### v5.54 — second factor and reassociation

Apply the original counit through the original non-strict `G`:

~~~text
(G ; F) ; G => G
~~~

and reconcile the source with `G ; (F ; G)` through explicit triple-comparison lemmas. The object component and naturality remain unchanged; only the source comparison coherence is reconciled.

### v5.55 — actual reverse triangle

The two factors are pasted with native `StrongTrans.vcomp`:

~~~text
T_G(Y) = eta_(G Y) ; G(eps_Y)
~~~

and its component is definitionally the old v5.51 pointwise triangle.

### v5.56 — global reverse modification

The v5.51 contraction family is proved natural for this exact v5.55 paste. The proof keeps the relevant object equivalences independent and reduces the diagram using the original compositor, counit cancellation, and the original adjoint-equivalence triangle identities.

The result is:

~~~text
actualLiftQuasiInverseTriangleModificationIso :
  T_G ~= Id_G
~~~

This is a native invertible modification with the original pointwise contractions as components.

## 8. Integrated actual-lift certificate — v5.57

v5.57 introduces:

~~~text
exactLiftableActualLiftUnitCounitCertificate
exactLiftableActualLiftCoherentBiequivalenceCertificate
~~~

The first stores the same v5.45 Whitehead datum, v5.42 `F`, v5.48 `G`, v5.50 `eta`, and v5.49 `eps`.

The second additionally stores the actual v5.52 forward triangle/modification and actual v5.55/v5.56 reverse triangle/modification.

Whole-record projection equations verify that the stored triangle transformations are the original native `StrongTrans.vcomp` constructions and that the stored modifications are the original native isomorphisms. The original local equivalence, label preservation, same-label coverage, raw-witness boundary, and unit/counit component equivalences remain exposed.

The generic certificate type is intentionally representative-based. The **concrete v5.57 value** establishes that its representatives are the actual pastes. This closes integration at the currently proved native level without manufacturing a stronger coherence structure.

## 9. Current frontier

### A. Higher coherence beyond the current certificate

First specify the desired target notion. If an adjoint-biequivalence or tricategorical structure stronger than the current package is intended, formalize its additional cells/laws explicitly and prove them for the existing (F,G,eta,eps). Do not rename the current certificate as a stronger theorem.

### B. Broader mapping principle

A schematic principle such as

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C, W, J, H), X)
~~~

is not yet an unrestricted theorem. Any extension must state the higher source/target, variance, atlas alignment, labels, permitted morphisms, and exact-liftability boundary. The obstruction theory prevents replacing exact presentation by weak admissibility.

### C. Descent across presentations

Continue separating:

~~~text
fixed-presentation equivalence
coherent transport between presentations
descent / gluing
presentation-independent invariant content
~~~

Equivalent carriers do not by themselves identify provenance or chosen presentations.

### D. AI-facing integration

Use the formal layer to constrain contextual reasoning, retrieval, and transport while keeping observation, provenance, authorization, and re-observation explicit. Runtime usefulness and theorem authority remain separate.

## 10. Lean proof-engineering lessons

**Preserve non-strict comparison data.** The reverse triangle required explicit `G.mapId` / `G.mapComp`; objectwise formulas alone were insufficient.

**Reassociation is coherence, not equality by assertion.** v5.54 keeps `app` and `naturality` fixed while reconciling source comparison fields through explicit triple-comparison lemmas.

**Use the original contraction family.** v5.56 proves naturality for the actual paste rather than transporting to a replacement identity family.

**Expose native hom categories when inference stops.** In v5.57, projections through a certificate hid enough endpoint information that Lean could not synthesize `StrongTrans.homCategory`. The repair explicitly bound the existing mathlib instance at the typed endpoints; it did not create a new global category structure.

**Avoid overloaded local notation at universe-sensitive projection boundaries.** A regular typed abbreviation was more robust than a notation quotation carrying explicit universe applications. Lean's identifier and generalized-field-notation resolution is type-directed, so make the structure value explicit before projecting fields.

**Separate root errors from cascades.** Read the whole source and full CI log. Fix independent elaboration/typeclass failures first; downstream unknown identifiers or `sorryAx` may be consequences.

**Validation is not authority.** Match the exact PR head to the successful run and receipts, and distinguish it from the synthetic merge actually compiled and the final main merge.

## 11. Reproduction and document maintenance

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout d6b2b2055ac9a797d5569ab30591eeabfeac319c

lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57
~~~

Useful endpoints:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16 \
  KUOS.DependentOriginationClassificationCoherentBiequivalenceV5_31 \
  KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45 \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48 \
  KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56 \
  KUOS.DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57
~~~

Aggregate/runtime commands remain separate entry points:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

Keep [README.md](README.md) and this roadmap aligned on the same theorem-bearing snapshot. A later docs-only merge may advance `main` without changing the theorem-bearing baseline.
