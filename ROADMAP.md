# KuuOS / 空OS — Formal Roadmap

**Snapshot: 2026-10-08 JST · canonical theorem-bearing main through v5.85 · [PR #2043 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2043)**

**現在地：** actual-lift 分類双圏の同じ F、G、unit η、counit ε と、元の両三角形の contraction を保持したまま、swallowtail の型付き述語、v5.68 の元の四セル、v5.82 の中間 StrongTrans 全体の自然性、v5.83 のグローバル可逆 modification、および v5.85 の汎用五段輸送計算と元の四セルの二因子成分一致まで Lean で構築・証明した。**グローバル Iso と元の成分の完全同定、および forward / reverse swallowtail 等式は未証明である。**

This is a milestone ledger, not a claim that every anticipated higher-coherence equation has been closed. Construction of an invertible modification and proof of a swallowtail law are different mathematical assertions.

## 0. Authority, pinned environment, and exact receipt

| Item | Verified value |
| --- | --- |
| Canonical repository and branch | **itakura-hidetoshi/KuuOS**, **main** |
| Latest theorem-bearing merge | **4b1a117ded213562f37e5b5d3627bbf28410b05c** |
| Integrated theorem PR | [#2043 — v5.85](https://github.com/itakura-hidetoshi/KuuOS/pull/2043), merged |
| Exact validated PR HEAD | **a1d66d8d9ab164527a2b00fb43c43a0018a50eea** |
| Exact PR workflow | [37773980229](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37773980229), completed / success |
| Strict Lean job | **113300216620**, success; **8712/8712** jobs |
| Governance gate | **113301429843**, success |
| MCP Lean completion receipt | **113301429847**, success |
| MCP CI completion receipt | **113301499488**, success |
| Lean compiler | **leanprover/lean4:v4.30.0-rc2** |
| mathlib revision | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** |
| Theorem endpoint | [DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean) |

The exact-head Strict Lean target plus its dependencies passed with warning/sorry checks enabled. Do not infer that all aggregate formal targets, repository workflows, or external AI runtimes were also rerun.

A later docs-only merge will change the fresh canonical main SHA but **not** this theorem-bearing baseline. Always re-observe main. Evidence priority is **fresh exact SHA → Lean theorem artifacts → README/ROADMAP → matching exact-head CI receipts → historical summaries**.

**Protected validation lane:** [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) is Lean 4.31 **validation-only**, currently **open / draft / not merged** (head 3a09839782ea82661ddbf8e13a0fd08e893079b4). It is explicitly outside theorem authority: do not merge it, mark it ready for review, or enable auto-merge.

## 1. Formal truth table — what the current endpoint does and does not prove

| Mathematical claim | Current status | Exact source |
| --- | --- | --- |
| F, non-strict G, η, ε, two actual triangle contractions with native invertible modifications | Constructed and proved earlier | [v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean), [v5.58](formal/KUOS/DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.lean) |
| Forward and reverse swallowtail **predicates** | Defined, not proved | [v5.65](formal/KUOS/DependentOriginationForwardSwallowtailPredicateV5_65.lean), [v5.66](formal/KUOS/DependentOriginationReverseSwallowtailPredicateV5_66.lean) |
| Original forward four-cell pointwise interchanger | Constructed | [v5.68](formal/KUOS/DependentOriginationForwardSwallowtailComponentInterchangerV5_68.lean) |
| Forward modification obstruction made explicit | Specified | [v5.70](formal/KUOS/DependentOriginationForwardSwallowtailModificationObstructionV5_70.lean) |
| Middle naturality of the two native StrongTrans factors, as a **whole-record** equation | Proved | [v5.82](formal/KUOS/DependentOriginationForwardMiddleNaturalityPasteV5_82.lean) |
| Native invertible **global** forward interchanger with fixed boundary transport adapters | Constructed | [v5.83](formal/KUOS/DependentOriginationGlobalForwardSwallowtailInterchangerV5_83.lean) |
| Generic component projection for eqToIso, inverse transport, and Iso composition | Proved | [v5.84](formal/KUOS/DependentOriginationForwardTransportComponentsV5_84.lean) |
| Generic five-stage component formulas, with explicit equality transport | Proved | [v5.85](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean) |
| Original **four-cell** component equals the **v5.78 global mapComp component followed by v5.77 three-cell component** | **Proved**: actualLiftForwardSwallowtailTwoFactor_hom_app | [v5.85](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean) |
| Original four-cell equals the component of the **full v5.83 five-stage global Iso** | **Open**: ActualLiftGlobalCanonicalComponentAgreement is a Prop, not a theorem | [v5.85](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean) |
| Actual forward and reverse swallowtail coherence laws | **Open** | v5.65 / v5.66 |
| A new stronger swallowtail-coherent biadjunction / biadjoint biequivalence certificate | **Not claimed** | Await both higher equations |

In particular, "middle naturality proved" is not "swallowtail proved", and "generic transport calculus proved" is not "all concrete transport adapters eliminated."

## 2. Retained obstruction and localization foundations — v4.00–v5.36

| Versions | Integrated mathematical content |
| --- | --- |
| v4.00–v4.12 | Exact C₂ nonfactorization and nonzero Stage-II obstruction over ZMod 2; distinction between possible and impossible coherent comparison |
| v4.13–v4.48 | Incidence/capacity obstructions, recursive and inverse-limit carriers, exact Cantor dimension, switch/orientation and descent analysis |
| v4.49–v4.89 | Presentation descent and exact-universal targets; source bicategories, strict realization, hom equivalences, label-sensitive global packages |
| v4.90–v5.08 | Restriction universality and coherent StrongTrans extension through localization |
| v5.09–v5.16 | Ambient exact-universal Whitehead/section/unit/counit and coherent triangle package |
| v5.17–v5.31 | Label-sensitive exact-universal/localized classification, global unit/counit, coherent triangle and modification package |
| v5.32–v5.36 | Aligned exact liftability, coherent presentation witnesses, coherent universalization |

The positive implication remains strictly one-way:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

**The converse is false in general.** Neither a presentation equivalence nor a successful local computation automatically grants descent, provenance erasure, or arbitrary raw-lift existence.

## 3. Actual-lift data — v5.37–v5.57

The aligned source is built over:

~~~lean
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

WorldLabel and PresentationLabel remain explicit.

- **v5.37–v5.42:** raw-morphism liftability criterion, local categories, actual-lift-carrying 1-cells, bicategory L, and strict projection F : L -> E.
- **v5.43–v5.45:** local hom equivalences, label-preserving object coverage, Whitehead biequivalence data.
- **v5.46–v5.48:** one fixed object equivalence eY : F(GY) ≃ Y; explicit non-strict quasi-inverse G with actual-lift formula **(eY.hom ; k) ; eZ.inv** and its mapId/mapComp coherence.
- **v5.49–v5.52:** native counit ε and unit η, actual forward triangle T_F, and its global invertible modification C_F.
- **v5.53–v5.56:** non-strict reverse triangle T_G built from η_G and G(ε), respecting native reassociation, with invertible modification C_G.
- **v5.57:** integrated certificate retaining the exact same Whitehead/F/G/η/ε and both contractions.

The historical v5.57 certificate name is preserved for API compatibility. It must **not** be interpreted as a proof of the higher swallowtail compatibility laws.

## 4. Non-strict triangulator infrastructure — v5.58–v5.63

| Version / PR | Closed milestone |
| --- | --- |
| v5.58 | Interpret T_F/C_F and T_G/C_G as native functor-bicategory triangulators |
| v5.59 | Package the original data as **IncoherentBiadjunctionDatum**; absence of a swallowtail field is intentional |
| v5.60 | Generalize the non-strict reverse triangle's horizontal whiskering and reassociation |
| v5.61 | Precompose StrongTrans values, modifications, invertible modifications, and triangulators |
| v5.62 | Postcompose StrongTrans values, modifications, and Iso modifications, preserving H.mapComp |
| v5.63 | Compare postcomposition of identity with native identity via **H.mapId**; complete non-strict triangulator postcomposition |

Do not replace any original G.mapId or G.mapComp data by strict identities.

## 5. Forward/reverse swallowtail foundations — v5.64–v5.70

| Version / PR | Integrated result |
| --- | --- |
| [v5.64 / #2022](https://github.com/itakura-hidetoshi/KuuOS/pull/2022) | Generic horizontal paste interface for the stored triangulators |
| [v5.65 / #2023](https://github.com/itakura-hidetoshi/KuuOS/pull/2023) | Typed **forward swallowtail predicate**; equation still open |
| [v5.66 / #2024](https://github.com/itakura-hidetoshi/KuuOS/pull/2024) | Typed **reverse swallowtail predicate**; equation still open |
| [v5.67 / #2025](https://github.com/itakura-hidetoshi/KuuOS/pull/2025) | Unit self-naturality comparison core |
| [v5.68 / #2026](https://github.com/itakura-hidetoshi/KuuOS/pull/2026) | Exact **original forward four-cell pointwise** interchanger using G.mapComp, inverse associator, unit self-naturality, final associator |
| [v5.69 / #2027](https://github.com/itakura-hidetoshi/KuuOS/pull/2027) | Unit self-naturality exchange |
| [v5.70 / #2028](https://github.com/itakura-hidetoshi/KuuOS/pull/2028) | Explicit original forward-modification naturality obstruction |

The v5.68 component is not replaced by a newly chosen interchanger. The intended higher comparison must use exactly this four-cell formula.

## 6. From pointwise cells to globally natural factors — v5.71–v5.78

| Version / PR | Integrated result |
| --- | --- |
| [v5.71 / #2029](https://github.com/itakura-hidetoshi/KuuOS/pull/2029) | Global postcomposition vertical-composition coherence |
| [v5.72 / #2030](https://github.com/itakura-hidetoshi/KuuOS/pull/2030) | Native-source unit postcomposition |
| [v5.73 / #2031](https://github.com/itakura-hidetoshi/KuuOS/pull/2031) | Isolate unit self-interchanger boundary |
| [v5.74 / #2032](https://github.com/itakura-hidetoshi/KuuOS/pull/2032) | Prove global unit self-interchanger naturality |
| [v5.75 / #2033](https://github.com/itakura-hidetoshi/KuuOS/pull/2033) | Specialize global η/η interchanger to actual-lift datum |
| [v5.76 / #2034](https://github.com/itakura-hidetoshi/KuuOS/pull/2034) | Global counit-whiskered η/η interchanger |
| [v5.77 / #2035](https://github.com/itakura-hidetoshi/KuuOS/pull/2035) | Paste both native associators around counit-whiskered η/η modification; component is exactly the original **three-cell** suffix |
| [v5.78 / #2036](https://github.com/itakura-hidetoshi/KuuOS/pull/2036) | Global G.mapComp left-whiskered by η; component is exactly the original **first cell** |

Together v5.78 and v5.77 provide the two factors underlying the four original pointwise cells. They are global values; that alone does not remove the endpoint/middle equality transports subsequently used in v5.83.

## 7. Native middle comparison and global Iso — v5.79–v5.84

| Version / PR | Integrated result |
| --- | --- |
| [v5.79 / #2037](https://github.com/itakura-hidetoshi/KuuOS/pull/2037) | Objectwise boundary identifications; isolate the nontrivial middle StrongTrans **naturality** obstruction; right endpoint whole-record equality |
| [v5.80 / #2038](https://github.com/itakura-hidetoshi/KuuOS/pull/2038) | Preserve native non-strict quasi-inverse compositor in middle bridge |
| [v5.81 / #2039](https://github.com/itakura-hidetoshi/KuuOS/pull/2039) | Compare postcomposed unit/counit middle-factor naturalities |
| [v5.82 / #2040](https://github.com/itakura-hidetoshi/KuuOS/pull/2040) | Prove **middleStrongTrans_eq** as a whole-record equality, including naturality, from the original factor comparison; close **actualLiftMiddleNaturalityAgreement** |
| [v5.83 / #2041](https://github.com/itakura-hidetoshi/KuuOS/pull/2041) | Construct native global invertible forward interchanger using both global factors and three proved equality transports |
| [v5.84 / #2042](https://github.com/itakura-hidetoshi/KuuOS/pull/2042) | Generic eqToIso hom/inverse app and vertical-Iso composition formulas at original StrongTrans components |

The v5.83 forward global Iso has the actual shape:

~~~text
(eqToIso left-equation)^-1
  ; v5.78 global G.mapComp
  ; eqToIso middleStrongTrans_eq
  ; v5.77 global three-cell counit reassociation
  ; eqToIso right-equation
~~~

These adapters are **proved equalities between entire StrongTrans values**, not newly selected coherence 2-cells. However, their actual **component-level cancellation against the original four-cell expression** is a separate remaining comparison.

## 8. v5.85 — exact proven boundary

[PR #2043](https://github.com/itakura-hidetoshi/KuuOS/pull/2043) added [DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85.lean).

**Proved generic lemmas:**

- Generic.eqToIso_inv_app_of_app_eq
- Generic.fiveStage_hom_app
- Generic.fiveStage_hom_app_of_iso_eq
- Generic.fiveStage_hom_app_of_iso_eq_and_component

**Proved concrete component lemmas:**

- middleEqToHom_app_is_id and middleEqToHom_self_app_is_id, for specified reflexive middle-component transports;
- leftEqToHom_app_is_id and rightEqToHom_app_is_id, at the two endpoint components;
- **actualLiftForwardSwallowtailTwoFactor_hom_app**: exactly the v5.68 old four-cell component equals the two-factor composite of v5.78 and v5.77 components.

The following is a **definition of Prop**, **not** a proven theorem:

~~~lean
ActualLiftGlobalCanonicalComponentAgreement (W) A : Prop
~~~

It states that for **all source objects X**, the component of **actualLiftForwardSwallowtailGlobalIso** from v5.83 equals the hom of the original **actualLiftForwardSwallowtailComponentInterchanger X** from v5.68.

The current result does not silently infer that universal proposition from the generic calculus or from the two-factor identity. Formal compatibility of the actual three equality transports with that exact composite remains to be established.

## 9. Immediate next proof obligations — ordered

### F1. Close the *actual* global-to-canonical component comparison

Start from the exact v5.83 Iso and original v5.68 component. Reuse v5.82 **middleStrongTrans_eq**, v5.84's eqToIso component lemmas, and the v5.85 generic five-stage theorem. Prove precisely the proposition **ActualLiftGlobalCanonicalComponentAgreement**, with all original η, ε, F, G, labels, and whiskerings unchanged.

The critical point is the nontrivial *actual-lift specialization*, not the already-proved abstract five-stage theorem. Never replace a difficult equality by an unproved assertion, an alternate instance-dependent 2-cell, or a new axiom.

**Suggested proof-engineering path:** retain the same native hom-category instance and fixed universe parameters; pass exact component equality proofs in the same named representation; normalize the three eqToHom transports at separate generic boundaries; then compose via a well-typed pointwise equation. Limit expensive whnf/isDefEq expansion of the entire actual-lift source.

### F2. Descend original pointwise data into modification naturality

Once F1 is available, use the naturality already possessed by the v5.83 global invertible modification to transport that result back to the **unchanged** canonical v5.68 family and discharge the remaining v5.70 naturality obstruction.

Pointwise equality must have a verified connection to the globally natural modification; merely having global naturality of a *different representation* is not by itself the old naturality theorem.

### F3. Complete the forward swallowtail

Prove the **v5.65 forward swallowtail predicate** against its specified triangulator contraction paste. A forward interchanger (even when global and natural) is not automatically the swallowtail equation itself.

### F4. Complete the reverse swallowtail

Construct/compare the corresponding reverse-oriented pastes and prove **v5.66** for the same non-strict quasi-inverse G and the same stored data. Do not confuse reverse triangle contraction with reverse swallowtail coherence.

### F5. Stronger package only after both laws

Only after verified forward and reverse equations should the formal layer introduce a structure whose specification asserts swallowtail-coherent biadjunction or a correspondingly stronger biadjoint biequivalence. If a mathematically necessary triangulator adjustment is discovered, formalize the adjustment explicitly and prove what data it preserves.

## 10. Other frontiers — separate from the current theorem authority

### Higher universal mapping principle

The schematic expression

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C, W, J, H), X)
~~~

is **not** currently an unrestricted theorem. Any extension must specify its source/target bicategories, variance, admissibility, labels, presentation alignment, morphism scope, and exact-liftability conditions.

### Descent across representations

Preserve the distinctions:

~~~text
fixed-presentation equivalence
  != coherent transport between presentations
  != justified descent/gluing
  != presentation-independent invariant with tracked provenance
~~~

Continue connecting obstruction, refinement, finite/inverse-limit carriers, and localization without equating independently chosen representations.

### AI-facing and runtime integration

The KuuOS reasoning route can constrain contextual retrieval and decision support by marking observation, inference, provenance, compatibility, obstruction, authority, minimal action, and re-observation. This is a **research/software integration frontier**, not a Lean theorem that any LLM must use the route correctly or that permission to execute actions is implied.

The runtime, website, MCP bridge, and benchmarks have distinct validation receipts and are not automatically certified by the selected v5.85 Lean build.

## 11. Lean/mathlib proof-engineering ledger

- **Preserve non-strict data:** never replace G.mapId, G.mapComp, genuine associators or unitors with strict identities.
- **Keep source, target, and universes explicit:** a typed StrongTrans Hom category may need a fully specified Mathlib **Pseudofunctor.StrongTrans.homCategory** to prevent underconstrained universe inference.
- **Objectwise equality is not record equality:** v5.79 isolated the middle naturality obstruction; v5.82 closed it by proving the actual naturality fields.
- **Use native component APIs:** v5.84's eqToIso_hom_app / eqToIso_inv_app / isoTrans_hom_app are preferable to expanding the entire modification record.
- **Do not assume a generic lemma closes a large specialization:** v5.85 closes generic transport but keeps the actual global-canonical proposition open.
- **Equality witnesses and transports matter in elaboration:** use the same named equality proof when needed; a printed goal can hide different category instances or universe arguments.
- **Proof irrelevance is not a replacement for a typed equality:** it permits identification of proofs of a fixed Prop, but does not justify changing endpoints or erasing actual naturality data.
- **Control simplification scope:** prefer targeted simp only, rw, conv, congrArg, typed have statements, and exact at a small interface. Avoid whnf/isDefEq expansion of enormous actual-lift terms.
- **Read all Lean diagnostics:** unused simp arguments are real linter issues when warningAsError is active; sorryAx on a failed declaration is a failure, not proof evidence.
- **Hold theorem authority to exact SHA:** changed-file CI, governance, head receipts, merge commit, and subsequent docs-only commits are distinct historical objects.

## 12. Reproduction and documentation maintenance

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 4b1a117ded213562f37e5b5d3627bbf28410b05c

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true \
     build KUOS.DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_85
~~~

Additional source endpoints:

~~~bash
lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationForwardSwallowtailPredicateV5_65 \
  KUOS.DependentOriginationReverseSwallowtailPredicateV5_66 \
  KUOS.DependentOriginationForwardSwallowtailComponentInterchangerV5_68 \
  KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70 \
  KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82 \
  KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83 \
  KUOS.DependentOriginationForwardTransportComponentsV5_84
~~~

Broader formal and operational validations are separate commands and have independent evidence requirements:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

Keep the [README](README.md), this roadmap, the actual Lean files, [GOVERNANCE.md](GOVERNANCE.md), [LICENSE](LICENSE), and exact-head receipts consistent. **Copyright © 2026 Hidetoshi Itakura / 板倉英俊; all rights reserved.** A documentation update must never imply an unproved theorem or a broader permission to reuse the repository.
