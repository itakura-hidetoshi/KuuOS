# KuuOS / 空OS — Formal Roadmap

**Snapshot / 最終確認：2026-10-11 JST · theorem-bearing canonical `main` v5.151 · [PR #2118 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2118) · merge SHA `195b9fd68a7f9923eced96e9c6ddce536981cd1f`**

**現在地：F1–F54 are CLOSED only within their individual precise original KuuOS Lean theorem statements.** The fixed actual-lift swallowtails and chosen F/G/η/ε data (F1–F5), chosen mates and original distinct categories (F6–F39), complete proof-relevant F19/F28 histories and F44 independent-axis adjacent-swap quotient (F40–F46), original F45 typed path/composition/bracketing and five-vertex F53 quotient pentagon (F47–F53) remain fixed. **F54 adds concrete Type-valued local F45 associativity rotations and arbitrarily long finite reversible chains**, contextual whiskering, preservation of F44 classes and both complete typed axis histories, original chosen right-mate and actual source η / target ε specialization.

**Boundaries are part of the result.** No F19 and F28 Hom identification, no unjustified inversion of potentially noninvertible `G.toOplax` cells, no global tricategorical/Gray-category biequivalence, no infinite convergence theorem, and no verified AI runtime follows from these Lean artifacts.

## 0. Canonical authority, pinned toolchain and exact-head receipt

| Item | Freshly verified baseline |
| --- | --- |
| Repository and branch | **[itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS) / `main`** |
| Latest theorem-bearing canonical `main` | **`195b9fd68a7f9923eced96e9c6ddce536981cd1f`**, [PR #2118 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2118) |
| F54 source PR HEAD | **`2a633aa2844e59db9e4f7aa7c7816884f24105df`** |
| Exact-head validated GitHub run | [**38101255425 — SUCCESS**](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38101255425) |
| Strict Lean validation | Job **114357548574 — SUCCESS**, selected dependency closure **8856 / 8856** |
| Governance audit | Job **114358006078 — SUCCESS** |
| MCP Lean / MCP CI completion receipts | Jobs **114358006017 / 114358040926 — SUCCESS** |
| F54 changed files / declaration audit | **5 new Lean files**, **0 warnings / 0 errors**, **27/27 `#print axioms`**, no `sorryAx`, `sorry`, `admit`, new axiom |
| Permitted axiom dependencies observed | `propext`, `Classical.choice`, `Quot.sound` only |
| Pinned Lean | **v4.30.0-rc2** — [lean-toolchain](lean-toolchain) |
| Pinned mathlib | **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`** — [lake-manifest.json](lake-manifest.json) |

**Mathematical authority:** freshly observed exact SHA → actual Lean file declarations/proofs → README/ROADMAP → exact-head CI/governance/MCP receipts → conversation/history/memory. A documentation-only merge moves live `main` but does **not** add mathematical theorems or replace the latest theorem-bearing baseline. Re-observe the HEAD at the start of each future step.

**Do not touch protected validation lane:** [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) (Lean 4.31 independent validation) is **OPEN / DRAFT / not merged**, outside canonical theorem authority; never mark ready, auto-merge or merge.

## 1. Formal truth table / 証明済みと未証明を分離

| Scope | Result at the referenced exact Lean versions |
| --- | --- |
| Original F/G, η/ε, chosen equivalences, non-strict comparison data | **Constructed**, unchanged from original actual-lift artifacts; label/presentation-sensitive |
| Forward and reverse swallowtail | **PROVED:** v5.93 F3 and v5.100 F4, combined on one fixed datum v5.101 F5 |
| Objectwise native adjunctions/mates and corrected non-strict composition | **PROVED under their original chosen data:** F6–F18; not a global equivalence with all higher-adjunction formalisms |
| Original chosen mate presentation and genuine compression-kernel quotient | **PROVED under explicit original categories:** F19–F39; F28 genuine quotient, not an F26 comparison-chain Hom substitute |
| F19/F28 full primitive path traces and generated exchange quotient | **PROVED:** F40–F45, with only genuine independent-axis adjacent exchanges generating the relation |
| Quotient-to-complete-histories classification | **PROVED:** F46 `ExchangeClass ≃ (AxisTrace n × AxisTrace m)` at fixed source/target/axis depths; no two different same-axis histories are identified |
| Actual old F45 casts, original mates and η/ε | **PROVED:** F47–F49, including genuine `Nat.zero_add`/`Eq.mp` transports |
| Two-stage sequential composition and arbitrary finite-stage associativity/units | **PROVED:** F50–F51; two symbolic Nat-index casts explicit; finite not infinite |
| Arbitrary binary-tree bracketing and its original chosen-mate descent | **PROVED:** F52; class-level equality when full original F19/F28 histories agree |
| Fourfold five-vertex pentagon | **PROVED:** F53 on the **specific original F44 generated quotient**, its independent type-correct symbolic depth casts, both actual F45 tree routes and chosen right mate |
| Concrete contextual finite rotation chains | **PROVED:** F54 `OriginalF45BracketTree.LocalRotation`, `RotationEdge`, `RotationChain`; forward/reverse moves, composition, reversal, length, both contexts, F44 quotient and original full F19/F28 histories, right-mate and η/ε preservation |
| Relations between DISTINCT RotationChain witnesses | **NOT YET PROVED:** F44 endpoint-class equality alone is not Type-valued higher path coherence |
| External tricategorical/Gray-categorical 3-cell pentagon | **NOT PROVED**; equalities of F44 `Quot` classes do not automatically provide arbitrary higher 3-cell coherence |
| Arbitrary presentation-independent lifting/descent, global biadjunction equivalence, runtime/AI correctness, infinite limit | **NOT PROVED** without additional exact hypotheses and separate independent tests |

**Historical caution:** the earlier v5.57 triangle-level “coherent biequivalence certificate” predates the actual v5.101 swallowtail closure; the latter is a specific KuuOS coherent carrier. `Bicategory.Adjunction` at selected objectwise data does not automatically imply a global pseudofunctor-level adjunction.

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

The original F, G, η, ε and triangles are **not reselected**, neither in the v5.64–v5.101 swallowtail proof program nor the v5.102–v5.106 native mate interfaces (historical early layer).

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


## 8. F11–F18 CLOSED — native mate identity, corrections and arbitrary modifications

F11–F18 (v5.107–v5.115) are **not current unproved candidates**. The previous roadmap’s “F11 mapId not proved” was correct in its earlier v5.106 snapshot but was closed by [PR #2071 / v5.107](https://github.com/itakura-hidetoshi/KuuOS/pull/2071).

- **F11/F12 (v5.107–v5.108):** original source/target `mapId`-corrected right-mate identity and arbitrary original 2-cell naturality, with original chosen objectwise adjunctions.
- **F13/F14 (v5.109–v5.110):** original source `mapComp` correction, right-mate lax transformations and unmate/orientation preservation.
- **F15 (v5.111–v5.112):** original unit/counit right-triangle modifications and native swallowtail-exchange compatibility.
- **F16–F18 (v5.113–v5.115):** arbitrary source modification mate transport, automatic mate naturality, and inverse mate/2-Hom interfaces. No false premise that the original nonstrict lax comparison cells are invertible.

Representative exact Lean files:
[NativeMatesIdentityV5_107](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107.lean),
[NativeRightMateLaxTransV5_110](formal/KUOS/DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110.lean),
[ArbitraryModificationMatesV5_113](formal/KUOS/DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.lean).

## 9. F19–F39 CLOSED — genuine original F19/F28 axes and nonstrict mate geometry

| Stage range | Actual proved original-category content |
| --- | --- |
| **F19–F21 / v5.116–v5.118** | Original chosen right-mate presentation categories, genuine contravariant functors, forgetful functor/whiskering, global mate modification naturality |
| **F22–F27 / v5.119–v5.124** | Simultaneous nonstrict two-sided modification mate naturality, finite comparison paths, independent factorization and stage pasting, authentic finite-chain compression functors |
| **F28–F31 / v5.125–v5.128** | Actual compression-kernel **quotient-category** Hom, original mate boundary descent, nonstrict horizontal quotient functors, coherent associators and unitors |
| **F32–F35 / v5.129–v5.132** | Original pentagon/triangle, mixed associator-hexagon, quotient mate and two-stage vertical horizontal-exchange coherence; F35 has two merged PRs |
| **F36–F39 / v5.133–v5.136** | Original horizontal quotient exchange naturality, finite hexagon, genuine finite StrongTrans.Modification vcomp and original mixed two-axis split/bracketing |

Representative exact Lean:
[F19 categories](formal/KUOS/DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.lean),
[F28 quotient category](formal/KUOS/DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.lean),
[F30 horizontal quotient](formal/KUOS/DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.lean),
[F35 nonstrict hexagon](formal/KUOS/DependentOriginationCoherentBiadjunctionMixedAssociatorHexagonV5_132.lean).

**Important:** the F28 genuine quotient Hom carrier is not the F26 finite comparison-chain category. Results retain the underlying original source/target boundaries and the forward, potentially noninvertible G comparison maps.

## 10. F40–F46 CLOSED — original two-axis Type-valued exchange and complete normal forms

| Version / PR | Precisely established layer |
| --- | --- |
| **F40 / v5.137 / [#2103](https://github.com/itakura-hidetoshi/KuuOS/pull/2103)** | Original F19/F28 independent finite rectangular re-subdivision, intermediate `Blocks` and mate naturality |
| **F41 / v5.138 / [#2104](https://github.com/itakura-hidetoshi/KuuOS/pull/2104)** | Constructive two-axis block refinements and original forward lax-mate coherence |
| **F42 / v5.139 / [#2105](https://github.com/itakura-hidetoshi/KuuOS/pull/2105)** | Fully typed primitive finite-depth `OneStep` refinement traces and source/right-mate naturality |
| **F43 / v5.140 / [#2106](https://github.com/itakura-hidetoshi/KuuOS/pull/2106)** | Arbitrary exact-depth `Interleaving` and functorial primitive refinement interchange |
| **F44 / v5.141 / [#2107](https://github.com/itakura-hidetoshi/KuuOS/pull/2107)** | `Type`-valued `OrderedInterleaving`; original actual adjacent independent-axis square; generated `ExchangeEqv` (reflexive/symmetric/transitive closure); **`ExchangeClass` as Quot**, compatible path concatenation |
| **F45 / v5.142 / [#2108](https://github.com/itakura-hidetoshi/KuuOS/pull/2108)** | Native independent F19 and F28 `AxisTrace` histories extracted from a full path, preserved by the exact F44 generators; genuine functorial descent and both original chosen execution orders |
| **F46 / v5.143 / [#2109](https://github.com/itakura-hidetoshi/KuuOS/pull/2109)** | **F28-first exact class normal form**, finite primitive exchange bubbling, inverse reconstruction and exact equivalence `ExchangeClass ≃ (AxisTrace n × AxisTrace m)`, complete iff criterion and genuine chosen right-mate specialization |

**F46 completeness criterion** (all endpoints/depths typed and fixed):

~~~text
ExchangeEqv p q
  ↔ p.modificationTrace = q.modificationTrace
    ∧ p.comparisonTrace   = q.comparisonTrace
~~~

This does **not** identify two different F19 or two different F28 primitive histories. Equality of evaluated Hom composites alone is weaker than equality in this generated quotient.

Representative Lean:
[F44](formal/KUOS/DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.lean),
[F45](formal/KUOS/DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142.lean),
[F46](formal/KUOS/DependentOriginationCoherentBiadjunctionExchangeAxisPairEquivalenceV5_143.lean).

## 11. F47–F54 CLOSED — original F45 paths, finite composition, quotient pentagon and contextual rotations

| Milestone / exact proof artifact | Verified theorem content |
| --- | --- |
| **F47 / v5.144 / [#2110](https://github.com/itakura-hidetoshi/KuuOS/pull/2110)** | Original F19-first/F28-first normal execution classes; F44 full `AxisTrace.append` compatibility and original η/ε six normal-history cases: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionModificationNormalFormV5_144.lean) |
| **F48 / v5.145 / [#2111](https://github.com/itakura-hidetoshi/KuuOS/pull/2111)** | Resolve actual historical F45 `Nat.zero_add` / dependent `Eq.mp` casts, prove both COMPLETE axis histories of each ORIGINAL path, exchange-class equality to the F46/F47 normal forms: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionF45TransportedHistoryReconciliationV5_145.lean) |
| **F49 / v5.146 / [#2112](https://github.com/itakura-hidetoshi/KuuOS/pull/2112)** | ACTUAL old F45 order selection injected into F44 exchange quotient, original right mates, nonstrict mapId/mapComp, and **six actual source η/target ε endpoint cases**: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45OrderedClassV5_146.lean) |
| **F50 / v5.147 / [#2113](https://github.com/itakura-hidetoshi/KuuOS/pull/2113)** | Genuine **two-stage sequential concatenation** of independent ORIGINAL F45 path classes, functoriality for two honest functors and right-mate preservation; all six original η/ε cases: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45SequentialCoherenceV5_147.lean) |
| **F51 / v5.148 / [#2114](https://github.com/itakura-hidetoshi/KuuOS/pull/2114)** | F44 quotient associativity **up to two explicit Nat casts**, genuine left/right unit, Type-valued inductive `OriginalF45Stages` with **arbitrarily many finite** old F45 stages, complete history and right-mate naturality: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionArbitraryFiniteOriginalF45StagesV5_148.lean) |
| **F52 / v5.149 / [#2115](https://github.com/itakura-hidetoshi/KuuOS/pull/2115)** | Arbitrary **finite full binary** old F45 bracketing (`OriginalF45BracketTree`); exact 3-subtree reassociation, snoc-stage regrouping and functorial/chosen right-mate/η/ε compatibility: [Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionArbitraryBracketTreeV5_149.lean) |
| **F53 / v5.150 / [#2116](https://github.com/itakura-hidetoshi/KuuOS/pull/2116)** | ALL **five vertices** and five typed associativity edges for four arbitrary F52 subtrees. Original F44 **3-edge long** and **2-edge short** routes reach identical final exchange classes after independent F19/F28 depth casts. Transported through actual original F45 trees, chosen right mate and 12 source/target endpoint boundary cases: [Pentagon Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionFourfoldPentagonV5_150.lean), [mate Lean](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalRightMatePentagonV5_150.lean) |
| **F54 / v5.151 / [#2118](https://github.com/itakura-hidetoshi/KuuOS/pull/2118)** | Arbitrary original F45 Type-valued `LocalRotation` with both symbolic-depth index casts and nested left/right contexts; genuine forward/backward `RotationEdge`; finite `RotationChain` (length/append/reverse/contextual whiskering). Preserves the precise F44 class, full F19/F28 native histories, original chosen right mate and actual source η / target ε. [Local rotations](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45LocalRotationV5_151.lean), [chains](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45FiniteRotationChainsV5_151.lean), [contexts](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45RotationContextsV5_151.lean), [right mates](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151.lean), [actual η/ε](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftRotationV5_151.lean) |

**What the F53 pentagon does and does not say:** it is a *path quotient-level* Mac Lane pentagon: both genuine original F44 class compositions after correct double depth casts agree. Equality proofs of quotient classes live in `Prop`, so their proof irrelevance is not an independently constructed tricategorical 3-cell. This is compatible with noninvertible G-side lax comparisons and does not establish a global bicategorical biequivalence.

## 12. Immediate mathematical frontier — F55 / v5.152 (NOT YET PROVED at this snapshot)

**F54 is closed only within its verified theorem scopes.** It constructs concrete Type-valued finite rotation chains preserving original F44 classes and both full native axis histories. It does not identify different RotationChain witnesses. F53's pentagon is an equality in the generated quotient, not a nontrivial higher cell relating actual rotation paths.

F55 research targets (none asserted as proved until new Lean proofs and exact-head CI receipts):

1. **Concrete chain pentagon.** Construct the five F53 vertices and their five genuine F54 local rotation edges, and explicitly exhibit the three-edge long path versus the two-edge short path, with their different lengths and all original indexed F19/F28 casts retained.
2. **Independent contextual square.** Construct parallel finite chains consisting of independent rotations in opposite orders and introduce a separately typed witness relating those chains; endpoint equality in F44 is insufficient.
3. **2-dimensional relation.** Define precisely a Type-valued or Prop-valued relation between parallel RotationChain witnesses generated by pentagon and disjoint-context square, closed under legitimate whiskering, composition and inverses as needed; do not assume unrestricted tricategorical 3-cell semantics.
4. **Chosen mate and actual η/ε compatibility.** Transport the constructed typed relation along genuine original F19 right-mate and independent F28 kernel quotient operations, then specialize actual source η and target ε, keeping original potentially noninvertible G.toOplax comparisons noninvertible.
5. **Explicit proof boundary.** Separate quotient endpoint equality from first-dimensional path evidence and newly constructed two-dimensional witnesses. No global coherence/biequivalence, contractibility or presentation-independent descent is implied.

### Other open mathematical frontiers

An external specification comparison must explicitly define the ambient tricategory/Gray category, orientations of η/ε, 2/3-cells and modification horizontal/vertical pastings. Present KuuOS's fixed-original-carrier theorem as a candidate for a conditional comparison, **not** as an already proved unrestricted equivalence.

The higher universal mapping principle

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C,W,J,H), X)
~~~

remains a *schematic research program*, **NOT** a universally quantified Lean theorem. Additional exact admissibility, descent and presentation/label conditions are necessary.

Earlier nonfactorization and Stage-II results remain one-way; the specific F19/F28 finite-quotient coherence does not make an arbitrary incompatible presentation suddenly liftable. Infinite-stage convergence, effective normalization complexity, a global uniform depth bound, and empirical AI/MCP/website correctness remain separate problems.

## 13. Engineering / exact-head review discipline

- **Pinned exact toolchain:** Lean v4.30.0-rc2; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. PR #1558 (Lean 4.31) is a protected validation-only lane.
- **Original F/G/η/ε are binding:** no replacement of chosen object equivalences, native F mapId/mapComp ISOs, the genuine nonstrict G.toOplax cells, F19 modification Hom or genuine F28 quotient Hom.
- **Lean 4 dependent indices are mathematics:** `Nat.zero_add` for symbolic `n` is not generally definitionally equal; use explicit Eq.mp / single equality-of-types casts and prove that axis-history extraction respects the transport (F48). `Nat.add_assoc` of several symbolic depths needs both F19/F28 casts (F51–F54).
- **Distinct namespaces:** F44 primitive `ExchangeClass` and F44-B `ExchangeClass.append` sit in precise Lean namespaces; open the specific F44-B namespace or qualify its full declaration. Do not assume a file name is a namespace.
- **Quotient congruence:** `Relation.EqvGen` of independent-axis adjacent exchanges; proof-relevant `Type`-valued histories and genuine `Quot` elimination, not an arbitrary same-axis equivalence or a proposition-only shortcut.
- **Mathlib bicategorical APIs:** compose with correct whisker interchange, associator/unitor and right-mate orientation. No implicit G-side inverse.
- **No proof holes:** fail on `sorry`, `admit`, `sorryAx` and new axioms. Review the ENTIRE changed Lean file, including warnings, all `#print axioms` receipts and unrelated elaboration problems; fix causes rather than only reported lines.
- **GREEN is not merged:** separately verify exact PR source HEAD, selected Lean build and warnings, all governance/receipt jobs, actual merge SHA and freshly observed authoritative `main`. Docs-only merges are not theorem-bearing changes.
- **Runtime/UI separation:** GitHub/MCP searchable declarations and an interactive chat site are engineering projects requiring independent coverage, version provenance, access controls, integration tests and UX reviews. Neither this document nor a selected Lean CI run certifies the weights or output behavior of an LLM.

## 14. Reproduction / 再現

The newest verified theorem-bearing baseline is the **v5.151 F54 merge SHA**, not the old F10 SHA and not a later documentation-only merge.

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 195b9fd68a7f9923eced96e9c6ddce536981cd1f
cat lean-toolchain

lake -KleanArgs=-DwarningAsError=true \
     -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45LocalRotationV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45FiniteRotationChainsV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationContextsV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationMatesV5_151 \
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftRotationV5_151
~~~

[Exact-head CI #38101255425](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38101255425) built the selected imported Lean dependency closure **8856/8856** with all five new F54 Lean files, zero changed-file warnings/errors, **27/27 `#print axioms`**, only `propext`, `Classical.choice` and `Quot.sound`, no proof holes/new axioms; Governance and both MCP receipts SUCCESS. This does not certify the whole repository or runtime.

~~~bash
# Broader checks — run separately; not implied by the F54 exact-head receipt:
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

See [README.md](README.md), [GOVERNANCE.md](GOVERNANCE.md), [LICENSE](LICENSE), [COPYRIGHT.md](COPYRIGHT.md) and [CITATION.cff](CITATION.cff). **Copyright © 2026 Hidetoshi Itakura / 板倉英俊; all rights reserved.** This roadmap does not grant new rights for adaptation, redistribution, commercial use or AI model training.
