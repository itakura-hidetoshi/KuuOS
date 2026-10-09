# KuuOS / 空OS — Formal Roadmap

**Snapshot / 最終確認: 2026-10-10 JST · theorem-bearing canonical `main` v5.106 · [PR #2069 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2069)**

**現在地:** **F1–F10 CLOSED within their stated, actual-lift-specific KuuOS formal specifications.** F3 (v5.93) and F4 (v5.100) prove the unchanged forward/reverse swallowtails, and F5 (v5.101) packages both into the original `Generic.CoherentBiadjunctionDatum`. F6–F10 (v5.102–v5.106) connect chosen objectwise equivalences and the original η/ε naturality 2-cells to native mathlib `Bicategory.Adjunction` and `mateEquiv`; the final target-side right-mate composition **retains the genuine non-strict `R_E.mapComp` correction**.

This roadmap distinguishes **(a) actual mathematical constructions and typed Lean proofs, (b) unproved extensions, (c) independently tested software/runtime properties, and (d) exact-head CI evidence**. Native objectwise mathlib adjunctions and mates do not, by terminology alone, entail an unrestricted tricategorical/Gray-categorical biadjunction equivalence or a verified AI runtime.

## 0. Canonical authority, pinned environment and exact receipt

| Item | Verified theorem-bearing reference |
| --- | --- |
| Repository / canonical branch | **itakura-hidetoshi/KuuOS / main** |
| Last theorem-bearing merge before this docs update | **`1aac4e4fef8d3c7f500095cc7b047a7e8baf6782`** — [PR #2069 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2069) |
| F3 / forward swallowtail | [PR #2053, v5.93, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2053) |
| F4 / reverse swallowtail | [PR #2061, v5.100, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2061) |
| F5 / KuuOS coherent carrier | [PR #2062, v5.101, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) |
| F6 / native adjunction bridge | [PR #2065, v5.102, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2065) |
| F7 / lossless return | [PR #2066, v5.103, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2066) |
| F8 / mates and original naturality | [PR #2067, v5.104, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2067) |
| F9 / vertical/horizontal mate pasting | [PR #2068, v5.105, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2068) |
| F10 / compositor-corrected target right paste | [PR #2069, v5.106, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2069) |
| Exact validated v5.106 PR source HEAD | **`210814f700252163e4ae13794cae595625ff4ed4`** |
| Exact-head GitHub Actions | [Run 37999962448](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37999962448) — completed / success |
| Strict Lean | Job **114055427705 — SUCCESS**, **8732/8732** selected-module/dependency build |
| Governance / audit summary | Job **114055925178 — SUCCESS** |
| MCP Lean / MCP CI completion | Jobs **114055925139 / 114055968137 — SUCCESS** |
| v5.106 changed-file diagnostics | **0 warnings / 0 errors**; five `#print axioms` checks report no `sorryAx` |
| Compiler | **leanprover/lean4:v4.30.0-rc2** — [lean-toolchain](lean-toolchain) |
| mathlib | **5450b53e5ddc75d46418fabb605edbf36bd0beb6** — [lake-manifest.json](lake-manifest.json) |

The exact-head receipt validates the **selected v5.106 Lean module and its imported dependency build**, not a universal clean full-repository build, all workflows, or the deployed AI/website. Imported historical warnings are distinguished from zero diagnostics in the changed v5.106 file. The five terminal declarations list only conventional `propext`, `Classical.choice` and `Quot.sound` dependencies, with **no `sorryAx`** and no new axiom. A docs-only merge moves live `main` without changing this theorem-bearing baseline.

**Authority:** fresh canonical SHA → actual Lean definitions/theorems/proofs → README/ROADMAP → matching exact-head CI/governance/MCP receipts → historical summaries.

**Protected validation lane:** [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558), Lean 4.31 only, remains **OPEN / DRAFT / unmerged**, observed HEAD `3a09839782ea82661ddbf8e13a0fd08e893079b4`. It is not theorem authority. **Do not merge, mark ready or enable auto-merge**.

## 1. Formal truth table / 証明済みと未証明の境界

| Statement | Status now | Source of proof or interface |
| --- | --- | --- |
| Exact liftable bicategory L and exact-universal E, original F and non-strict G | **Constructed** | [v5.37–v5.48](formal/KUOS/DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48.lean) |
| Original global unit η, counit ε, forward and reverse triangle modifications | **Constructed / proved** | [v5.49–v5.57](formal/KUOS/DependentOriginationExactLiftableActualLiftCoherentBiequivalenceV5_57.lean) |
| KuuOS `IncoherentBiadjunctionDatum` with two stored native triangulators | **Constructed**; no swallowtail proof *at that historical stage* | [v5.58](formal/KUOS/DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.lean), [v5.59](formal/KUOS/DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.lean) |
| Original typed forward and reverse swallowtail predicates | **Defined in v5.65 / v5.66; both subsequently proved for actual lifts** | [v5.65](formal/KUOS/DependentOriginationForwardSwallowtailPredicateV5_65.lean), [v5.66](formal/KUOS/DependentOriginationReverseSwallowtailPredicateV5_66.lean) |
| F1 original global-to-canonical forward interchanger equality | **PROVED** | `actualLiftGlobalCanonicalComponentAgreement`, [v5.86](formal/KUOS/DependentOriginationForwardSwallowtailGlobalComponentAgreementV5_86.lean) |
| F2 original four-cell modification naturality | **PROVED** | `actualLiftForwardSwallowtailOriginalNaturality`, [v5.87](formal/KUOS/DependentOriginationForwardCanonicalNaturalityV5_87.lean) |
| F3 original forward pointwise, canonical and global swallowtail | **PROVED** | `actualLiftForwardSwallowtailPointwise`, `actualLiftForwardSwallowtail`, `actualLiftForwardGlobalSwallowtail`, [v5.93](formal/KUOS/DependentOriginationForwardSwallowtailActualLiftDescentV5_93.lean) |
| F4 original counit-centered reverse four-cell, pointwise and naturality | **PROVED** | `actualLiftReverseFourCell_hom_eq_generic`, `actualLiftReversePointwise`, `actualLiftReverseNaturality`, [v5.100](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean) |
| F4 native global reverse swallowtail predicate | **PROVED** | `actualLiftReverseSwallowtail`, [v5.100](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean) |
| F5 both original swallowtail laws carried on the *same original datum* | **PROVED** | `actualLiftCoherentBiadjunctionDatum` / `actualLiftCoherentBiadjunction_exists`, [v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) |
| F6 selected object equivalences → native mathlib `Adjunction` and `Adj.Hom` | **PROVED, objectwise** | `Generic.nativeAdjunctionOfEquivalence`, `actualLiftSourceNativeAdjHom`, `actualLiftTargetNativeAdjHom`, [v5.102](formal/KUOS/DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.lean) |
| F7 recovered source and target original equivalences, without re-choosing data | **PROVED** | `Generic.originalEquivalenceRoundtrip_eq`, `actualLiftSourceRecoveredEquivalence_eq`, `actualLiftTargetRecoveredEquivalence_eq`, [v5.103](formal/KUOS/DependentOriginationNativeAdjunctionLosslessReturnV5_103.lean) |
| F8 original η/ε naturality squares → right mates, unmate and 2-cell naturality | **PROVED** | `actualLiftSourceUnitRightMate_unmate`, `actualLiftTargetCounitRightMate_naturality₂`, [v5.104](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeMatesV5_104.lean) |
| F9 `mateEquiv_vcomp` and `mateEquiv_hcomp` with source-side `mapComp` correction | **PROVED** | `Generic.originalEquivalences_mate_hcomp`, `actualLiftSourceUnitMateComp_native`, [v5.105](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105.lean) |
| F10 target `R_E.mapComp` whisker and explicitly corrected right-mate composition | **PROVED** | `Generic.mateEquiv_precompose`, `actualLiftTargetCounitMateComp_correctedRight`, [v5.106](formal/KUOS/DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106.lean) |
| Arbitrary bicategory instantiation of F3/F4 without the actual-lift hypotheses | **NOT established by F1–F10** | Requires independent assumptions and a distinct theorem |
| Universal comparison to every conventional tricategorical/Gray-categorical biadjunction or unrestricted higher adjunction API | **OPEN / not claimed** | Specify source/target and coherence conventions first |
| Arbitrary cross-presentation descent, strong higher universal mapping principle, all AI/runtime behaviors | **OPEN / independent research & engineering** | Explicit hypotheses, implementation and separate receipts required |

**Historical caveat:** `v5.57` uses “CoherentBiequivalence” in a triangle-level API name, before the two higher swallowtails were proved. `v5.101` supplies the **KuuOS two-swallowtail certificate**; `v5.102–v5.106` extend it with selected mathlib adjunction/mate interfaces, not a retroactive reinterpretation of v5.57.

## 2. Obstruction, localization and exact classification foundations — v4.00–v5.36

| Versions | Retained theorem-bearing content |
| --- | --- |
| v4.00–v4.12 | Explicit nonfactorization, Stage-II obstructions and nonzero ZMod 2 comparisons |
| v4.13–v4.48 | Capacity/incidence obstructions, recursive and inverse-limit carriers, dimension, switch/orientation and descent |
| v4.49–v4.89 | Exact-universal targets, presentation-sensitive descent, source bicategories, strict realization and hom equivalences |
| v4.90–v5.08 | Restriction universality and StrongTrans coherence in the localization context |
| v5.09–v5.16 | Ambient exact-universal Whitehead/section/unit/counit and triangle coherence |
| v5.17–v5.31 | Label-aware exact-universal classification, unit/counit, coherent triangle modifications |
| v5.32–v5.36 | Aligned exact liftability and coherent universalization witnesses |

The following implication is *one-way*, not an equivalence:

~~~text
exact DO₂ presentation
  => higher stack-localization factorization
  => higher localization factorization
  => weak W-admissibility
~~~

It does not imply arbitrary raw-morphism lifting, equalities between independently chosen presentations or provenance-free descent.

## 3. Original actual-lift F/G, η/ε and triangulators — v5.37–v5.63

The aligned atlas and explicit label universes remain:

~~~lean
RefinementAtlas.{u, max u v, uH} (LocalizedContext W)
~~~

- **v5.37–v5.42:** local lift criterion, L with actual-lift-carrying 1-cells, E with exact-universal objects, original strict F.
- **v5.43–v5.45:** local hom equivalences, label-sensitive object coverage and Whitehead evidence.
- **v5.46–v5.48:** original **non-strict G** via fixed `eY : F(GY) ≃ Y`, with actual-lift 1-cell `(eY.hom ; k) ; eZ.inv`, native `mapId` and `mapComp`.
- **v5.49–v5.52:** actual counit ε, unit η, forward triangle and its native global invertible modification.
- **v5.53–v5.56:** actual reverse triangle built from η_G and G(ε), including reassociation and inverse modification.
- **v5.57:** one original triangle-level certificate retaining all chosen components.
- **v5.58–v5.59:** native triangulators and `IncoherentBiadjunctionDatum` without (at that historical stage) a swallowtail field.
- **v5.60–v5.63:** horizontal whiskering, StrongTrans modification pre/postcomposition, native G/F `mapId` comparisons and non-strict coherence.

The original F, G, η, ε and triangles are **not reselected**, neither in the v5.64–v5.101 swallowtail proof program nor the v5.102–v5.106 native mate interfaces.

## 4. Forward swallowtail F1–F3: exact path to closure — v5.64–v5.93

| Milestone | Formal progression |
| --- | --- |
| v5.64–v5.66 | Horizontal triangulator pastes; the **two typed** original swallowtail interfaces |
| v5.67–v5.70 | Unit self-naturality, original four-cell pointwise interchanger and its modification naturality obstruction |
| v5.71–v5.78 | Globally natural η/η, counit-whiskered and reassociated middle interchangers; original G.mapComp global factor |
| v5.79–v5.82 | Endpoint comparisons, whole-StrongTrans **middle naturality** and equality of the native source factor |
| v5.83–v5.85 | Native global invertible forward interchanger, equality-transport components and generic five-stage calculus |
| **v5.86 — F1 CLOSED** | Full component equality of native global Iso with unchanged original four-cell family |
| **v5.87 — F2 CLOSED** | Original family naturality and equality of canonical `isoMk` with native global Iso |
| v5.88 | Formal iff-reduction of forward predicate to original pointwise four-cell vs source triangulator-paste equation |
| v5.89–v5.91 | Unchanged non-strict `G.mapId`, exact original forward/reverse contractions, cancelled residual |
| v5.92 | Genuine two-distinct-equivalence conjugation four-cell coherence |
| **v5.93 — F3 CLOSED** | Original forward pointwise agreement and original canonical/global forward swallowtail predicates |

**F1:** [v5.86, PR #2045](https://github.com/itakura-hidetoshi/KuuOS/pull/2045) proves `actualLiftGlobalCanonicalComponentAgreement` for the original v5.68 four-cell and v5.83 global Iso. It uses the original whole StrongTrans equality transports, not a newly chosen cell.

**F2:** [v5.87, PR #2046](https://github.com/itakura-hidetoshi/KuuOS/pull/2046) proves `actualLiftForwardSwallowtailOriginalNaturality`, and the original `isoMk` equals the native global Iso.

**F3:** [v5.93, PR #2053](https://github.com/itakura-hidetoshi/KuuOS/pull/2053) proves `actualLiftForwardCancelledCore`, `actualLiftForwardSwallowtailPointwise`, `actualLiftForwardSwallowtail` and `actualLiftForwardGlobalSwallowtail`. It relies on the v5.92 generic equation for *distinct stored equivalences*, not on substituting a strict G.

The forward interchanger/triangulator equation was only an **iff boundary at v5.88**. It became an actual proof of equality in v5.93. Do not confuse an intermediate conditional reduction with the final result.

## 5. Reverse swallowtail F4: exact path to closure — v5.94–v5.100

| Version / PR | New proof layer and what it preserves |
| --- | --- |
| [v5.94 / #2054](https://github.com/itakura-hidetoshi/KuuOS/pull/2054) | Expand the original **target** triangulator horizontal paste |
| [v5.95 / #2056](https://github.com/itakura-hidetoshi/KuuOS/pull/2056) | Construct the original counit-centered reverse four-cell and its inverse |
| [v5.96 / #2057](https://github.com/itakura-hidetoshi/KuuOS/pull/2057) | Define original reverse pointwise condition, modification naturality and expanded residual |
| [v5.97 / #2058](https://github.com/itakura-hidetoshi/KuuOS/pull/2058) | Derive original modification naturality from the proven pointwise agreement |
| [v5.98 / #2059](https://github.com/itakura-hidetoshi/KuuOS/pull/2059) | Generic reverse conjugation four-cell for **two distinct** equivalences `e` and `d` |
| [v5.99 / #2060](https://github.com/itakura-hidetoshi/KuuOS/pull/2060) | Prove `reverseConjugationFourCell_cancelled` using the genuine left triangle |
| **[v5.100 / #2061](https://github.com/itakura-hidetoshi/KuuOS/pull/2061)** | **F4 CLOSED**: identify the original actual-lift four-cell with the generic one; prove the residual, pointwise equation, naturality and global reverse predicate |

Key v5.100 declarations in [DependentOriginationReverseSwallowtailActualLiftV5_100.lean](formal/KUOS/DependentOriginationReverseSwallowtailActualLiftV5_100.lean):

~~~text
actualLiftReverseFourCell_hom_eq_generic
actualLiftReverseExpandedResidual
actualLiftReversePointwise
actualLiftReverseNaturality
actualLiftReverseSwallowtail
~~~

**Mathematical boundary:** these are assertions about the actual original v5.95 counit-centered interchanger and v5.94 paste, not an arbitrary different interchanger or a replacement right triangle. `eps.naturality (eps.app Y)` is specialized through the actual chosen equivalences, and the strict F's native comparisons are only canceled where already justified.

The successful v5.100 proof separates bicategorical identity cancellation into **typed generic lemmas** before instantiating the concrete actual-lift labels/hom universes. It retains the original `d = e_(FGY)` and `e = e_Y` choices; they are not assumed equal. The exact-head [v5.100 PR #2061](https://github.com/itakura-hidetoshi/KuuOS/pull/2061) passed strict Lean (8,726/8,726) and was merged.

## 6. F5 CLOSED: one coherent KuuOS biadjunction carrier — v5.101

**[PR #2062 / v5.101](https://github.com/itakura-hidetoshi/KuuOS/pull/2062) is merged into canonical main.**

[DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) defines the following *generic record type*, parameterized by two bicategories:

~~~lean
structure CoherentBiadjunctionDatum (B) (C) where
  datum               : IncoherentBiadjunctionDatum B C
  forwardInterchanger : ForwardSwallowtailInterchanger datum
  reverseInterchanger : ReverseSwallowtailInterchanger datum
  forward_swallowtail : ForwardSwallowtailPredicate datum forwardInterchanger
  reverse_swallowtail : ReverseSwallowtailPredicate datum reverseInterchanger
~~~

The snippet abbreviates the **fully qualified predicate/interchanger namespaces**; the exact source supplies these names and their typeclass/universe parameters.

The actual-lift inhabitant, `actualLiftCoherentBiadjunctionDatum`, is built from:
- the **unchanged v5.59 base** `exactLiftableActualLiftIncoherentBiadjunctionDatum`;
- the original v5.87 **forward canonical interchanger**, proven coherent by **v5.93 F3**;
- the original v5.96 **reverse modification of the counit four-cell family**, natural by **v5.100**, proven coherent by **v5.100 F4**.

The source further proves `actualLiftCoherentBiadjunctionDatum_base` by `rfl` and `actualLiftCoherentBiadjunction_exists` via the constructed inhabitant. This certifies **both exact KuuOS swallowtail equations on one and the same fixed datum**.

**Theorem boundary:** This is a proved KuuOS coherent biadjunction carrier for actual lifts. Merely defining `CoherentBiadjunctionDatum` does not prove that every arbitrary incoherent datum admits such interchangers, or that it automatically satisfies some separately specified tricategorical definition. Such extensions require a separate comparison theorem and explicit coherence hypotheses.

## 7. F6–F10 CLOSED: native mathlib adjunction and mates — v5.102–v5.106

This is a **bridge from the same original actual-lift data**, not a replacement adjunction. The adjunctions here are attached to the **chosen objectwise unit/counit equivalences**. Native mate equivalences act on 2-morphism sets and do not automatically make arbitrary mates invertible.

| Stage | Merged theorem source | Mathematical content and exact boundary |
| --- | --- | --- |
| **F6 / v5.102 / [#2065](https://github.com/itakura-hidetoshi/KuuOS/pull/2065)** | [MathlibAdjunctionBridgeV5_102.lean](formal/KUOS/DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.lean) | Build `Generic.nativeAdjunctionOfEquivalence`, `Generic.nativeAdjHomOfEquivalence` and unchanged source/target adjuncts; retain original units/counits and both triangles |
| **F7 / v5.103 / [#2066](https://github.com/itakura-hidetoshi/KuuOS/pull/2066)** | [NativeAdjunctionLosslessReturnV5_103.lean](formal/KUOS/DependentOriginationNativeAdjunctionLosslessReturnV5_103.lean) | Recover exactly the stored framed equivalences from native adjunction data, including source and target specializations |
| **F8 / v5.104 / [#2067](https://github.com/itakura-hidetoshi/KuuOS/pull/2067)** | [NativeMatesV5_104.lean](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeMatesV5_104.lean) | `actualLiftSourceUnitRightMate`, `actualLiftTargetCounitRightMate`; unmate returns the **original** naturality squares; transport naturality with respect to 2-cells |
| **F9 / v5.105 / [#2068](https://github.com/itakura-hidetoshi/KuuOS/pull/2068)** | [NativeMatesCompositionV5_105.lean](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105.lean) | `mateEquiv_vcomp` and generic `mateEquiv_hcomp`, source compositor-corrected mate composition; target `mapComp` still visible on the left side |
| **F10 / v5.106 / [#2069](https://github.com/itakura-hidetoshi/KuuOS/pull/2069)** | [TargetCompositorCorrectedMatesV5_106.lean](formal/KUOS/DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106.lean) | Original target `R_E.mapComp` becomes a typed **right-adjoint left whisker** before the two original right mates are pasted; `actualLiftTargetCounitMateComp_correctedRight` |

**F10 exact structure:** for target `f : X ⟶ Y` and `g : Y ⟶ Z`, the original target counit naturality for `f ≫ g` mates to a composite of (i) the exact `R_E.mapComp f g` whiskered by the original right-adjoint leg at X, and (ii) `actualLiftTargetCounitMateVComp f g`. The real compositor is not erased or asserted to be an identity. This is stronger than F9's separate left-side compositor equation and bare mate `vcomp`.

The F10 generic lemma `Generic.mateEquiv_precompose` uses `Bicategory.whisker_exchange` for naturality of a 2-cell with the adjunction unit; `bicategory` alone normalizes associators/unitors but does not prove this interchange. The final instantiation uses a typed `congrArg` rather than a failed direct `rw` into a composite.

**Exact F10 verification:** PR source `210814f700252163e4ae13794cae595625ff4ed4`; [CI #37999962448 SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37999962448), Strict Lean **114055427705 SUCCESS, 8732/8732**, Governance **114055925178 SUCCESS**, MCP Lean/CI **114055925139 / 114055968137 SUCCESS**. Changed Lean file has **0 warning/error**; all five printed final declaration axiom sets have **no `sorryAx`**. The earlier failing head is superseded, not a theorem-bearing result.

## 8. Next mathematics — explicit frontiers after F1–F10

### 8.1 Candidate F11: target/source identity and `mapId` mate coherence — NOT PROVED

A bounded next task is to state and prove an identity/unit analogue of F9–F10 using the **original** `R_E.mapId` (and source counterpart where appropriate), preserving unitors and the chosen η/ε and right legs. Compare the native mate of the original StrongTrans `naturality_id` to a typed corrected right identity paste. This is a **proposal**, not an already established Lean declaration. Avoid any unsupported assertion of global pseudofunctor adjunction or strict `mapId`.



### 8.2 Compare with external higher-adjunction formalisms

State a target theorem relating this *specific* two-swallowtail KuuOS carrier to an explicit tricategorical/Gray-categorical biadjunction specification. Specify orientations of horizontal/vertical composition, modifications, unitors/associators, any required extra axioms and the precise preservation of chosen η/ε/triangulators. Do **not** infer this equivalence from similar terminology.

### 8.3 Higher universal mapping principle

The schematic equivalence

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C, W, J, H), X)
~~~

is **not** an unrestricted theorem. State the source/target bicategories, presentation/label universes, variance, morphism classes, admissibility and exact lift/descent assumptions before proving a more general mapping result.

### 8.4 Cross-presentation descent / obstruction transfer

Preserve the strict distinctions:

~~~text
fixed-presentation equivalence
  != compatible coherent transport between presentations
  != justified descent/gluing
  != presentation-independent invariant with tracked provenance
~~~

Potential extensions include transport of the completed actual-lift coherent carrier along compatible presentation changes and explicit obstructions when it cannot descend. Keep the existing nonfactorization and Stage-II results authoritative at their original hypotheses.

### 8.5 Runtime, GitHub/MCP and interactive AI

An AI dialogue or website may *use* the authority route and search/index formal declarations, but the present theorem does **not** certify an LLM's reasoning weights, permissions, retrieval completeness or operational behavior. Future engineering needs an exact GitHub SHA-aware retrieval/indexing layer, formal artifact links, dependency graphs, deterministic replay and independent runtime/UX validation.

## 9. Lean 4 / mathlib engineering and review ledger

- **Strict pinned environment:** Lean v4.30.0-rc2 / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. The independent Lean 4.31 validation PR #1558 remains protected and outside theorem authority.
- **Original data are binding:** preserve F, non-strict G, η, ε, eY/e_(FGY), and all genuine `mapId`, `mapComp`, associator and unitor data. Changing them changes the mathematical claim.
- **Two equations, not two assumptions:** F3 and F4 were established from the original interchangers, not by choosing the triangulator paste to make the equality tautological.
- **Objectwise vs global naturality:** v5.79–v5.87 prove whole-StrongTrans comparison/naturality for the forward cells, and v5.96–v5.100 do so for the reverse.
- **Typed bicategory lemmas first:** v5.100 exposed failing `rfl`, unifier and `rw` steps that were not definitional equalities. The successful route proves structural identities in an explicit generic bicategory and applies them to exact actual-lift endpoints.
- **Whiskering and associativity:** right whiskering of an identity 2-cell is distinct from ordinary category composition with the identity; parenthesization must be normalized deliberately. Avoid a concrete `bicategory` tactic call if the huge actual-lift hom type prevents synthesizing a bicategory context.
- **Universe constraints matter:** use the correctly ordered universe parameters for source and target and explicitly supply `Pseudofunctor.StrongTrans.homCategory` where Mathlib inference is ambiguous.
- **No proof holes:** `sorry`, `admit`, additional axioms or a surrogate strict G are prohibited. Read **all** new-file diagnostics, including unused simp arguments under `warningAsError`.
- **Authority receipts:** a GREEN job is not a merge SHA. Confirm exact PR head, changed-file diagnostics, printed axioms, governance, both MCP receipts, successful merge and freshly observed canonical main.
- **Document honest bounds:** preserve historical “open at version X” statements as history, but never present the now-closed F3–F10 as current open obligations.
- **F10 exact Lean 4 lesson:** use `Bicategory.whisker_exchange` for 2-cell interchange, not `bicategory` alone; replace unsuccessful rewriting within a composed mate by `congrArg (fun t => correction ≫ t)` with a typed intermediate equality. A failed compilation prints `sorryAx` for incomplete theorems; require a fresh, successful exact-head `#print axioms` receipt before claiming closure.

## 10. Reproduction / 再現

Checkout the **v5.106 theorem-bearing commit** rather than a later docs-only SHA:

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 1aac4e4fef8d3c7f500095cc7b047a7e8baf6782

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106
~~~

The F10 module imports F9 and its existing F1–F8 dependencies. For explicit independent verification of the original two swallowtail proof endpoints:

~~~bash
lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationForwardSwallowtailActualLiftDescentV5_93 \
  KUOS.DependentOriginationReverseSwallowtailActualLiftV5_100 \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101
~~~

Exact-head [run 37999962448](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/37999962448) validates the selected **v5.106** module and imported dependencies with **8732/8732 SUCCESS**, zero changed-file warnings/errors, and five declarations printed with **no `sorryAx`**.

Broader all-formal and runtime checks remain separate targets requiring independent receipts:

~~~bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~



Maintain [README.md](README.md), this roadmap, the Lean files, [GOVERNANCE.md](GOVERNANCE.md), [LICENSE](LICENSE) and all exact-head evidence in agreement. **Copyright © 2026 Hidetoshi Itakura / 板倉英俊; all rights reserved.** This roadmap grants no new reproduction, training, redistribution, adaptation or commercial-use rights.
