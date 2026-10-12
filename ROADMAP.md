# KuuOS / 空OS — Formal Roadmap

**Current formal snapshot / 研究正本：2026-10-12 JST · v5.204 / F59-F55-A/B · [PR #2211 MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2211) · theorem-bearing merge SHA `8a32f06d846edd95f33b048e8f7986066398533e`.**

**現在地：** KuuOSの元のF/G/η/ε・swallowtail、F19/F28の独立履歴、実C60の60頂点/90辺/12五角形/20六角形、元F42/F43の高次射と独立F54/F55回転源を保持します。v5.202で元F42証明項に依存するF52商圏の真の3射五角形・三角形、v5.203で元F43自然変換・右先行Mathlib 3-Hom関手および180実局所混合F54/F55比較を証明済み。**v5.204/F59-F55-A/B**では、元のF47新設四境界混合圏の面選択移送が4対象位置で全単射、**あらゆる混合3-Homで全射かつ忠実**であること、両方向のMathlib面選択関手を構成。にもかかわらず、全90辺×両隣接面における元のF54左右回転境界を持つ任意の元F55 9生成子語は、新設 `Δ=(0,1;0)` を与えられず、**元F55場は大域的な頂点ゲージに降下しない**とLean証明しました。北五角形の符号付き第二整数電荷 `−5`・位相0と非平坦性は保持。元F42/F54原構文同一視も大域非退化Gray 3-圏も未証明です。

**Proven does not mean globally complete.** Local F43/F44/F51 categories, original F55 `PresentedCell`, added mixed comparisons and the grade-completed Gray target have **different source types**. The F46 native calibration `Δ=(0,1;0)` is newly adjoined in the mixed source; its absence from the original nine-generator F55 source is a proved boundary. The genuine F55 edge field remains nonflat on the true north pentagon even when the oriented full 32-face surface sum vanishes. Neither an unbounded-scale convergence theorem nor AI runtime/model correctness follows from formal Lean declarations.

## 0. Canonical authority / 正本・ツールチェーン・検証

| Item | Exact theorem-bearing authority |
| --- | --- |
| Repository / branch | **[itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS) / `main`** |
| Latest theorem-bearing MERGED PR | **[#2211 — v5.204 F59-F55-A/B](https://github.com/itakura-hidetoshi/KuuOS/pull/2211)** |
| Theorem-bearing merge SHA | **`8a32f06d846edd95f33b048e8f7986066398533e`** |
| Exact-head source SHA | `2854abd4230e9c603ece0ee4602ed131bf1142ef` |
| Exact-head CI | [**#38243833256 — completed SUCCESS**](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38243833256) |
| Strict Lean | Job `114792792654`, **9006/9006**, **0 changed-file Lean warnings / 0 errors** |
| Axiom inspection | **11 `#print axioms`** across two v5.204 modules; no new `sorryAx` or axioms, inherited C60 `native_decide` dependencies separate |
| Governance and receipts | Governance `114793486988`, MCP Lean `114793487115`, MCP CI `114793566592` — **all SUCCESS** |
| Toolchain | [Lean `v4.30.0-rc2`](lean-toolchain), [mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`](lake-manifest.json) |
| Protected experimental lane | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Lean 4.31 — **OPEN / DRAFT / NOT MERGED** |

**Authority precedence:** freshly read canonical GitHub `main` SHA → exact Lean declarations/dependencies → README/ROADMAP → matching exact-head CI/Governance/MCP receipts → history. The v5.204/F55-A/B theorem SHA was re-observed as `main` immediately after #2211; this docs-only merge will legitimately advance `main` without adding Lean theorems. Do not confuse a docs merge SHA with a new theorem-bearing merge.

## 1. Formal truth table / 証明と未証明の境界

| Topic / stage | Precisely established | Still unproved or explicitly different |
| --- | --- | --- |
| F1–F5, v5.93–v5.101 | Unchanged original actual `F/G/η/ε`, fixed chosen equivalences, **forward and reverse swallowtails**, one coherent actual-lift biadjunction carrier | Unrestricted biequivalence over arbitrary independently chosen presentations |
| F6–F39, v5.102–v5.136 | Native selected adjunction/mates, original F19 presentation category, independent genuine F28 compression-kernel quotient, 2-sided nonstrict coherence | Automatic inversion of potentially noninvertible `G.toOplax`, universal presentation-independent equivalence |
| F40–F46, v5.137–v5.143 | Proof-relevant original F19/F28 histories, original independent-axis adjacent swaps, complete quotient normal form | Equality of different histories on the same axis without a proved relation |
| F47–F57, v5.144–v5.154 | Finite original F45/F54 rotations, F55 3-vs-2 pentagon and contextual square, conditional higher interpreter/no-faithful-observation theorem, genuine C60 cyclic flag gluing | External full original-F55 higher semantics merely from F44 quotient/flag agreement |
| v5.155–v5.193 / F58–F59 | Native braided `GrayGrade` with full two integer charges and phase, C60 signed cellular cochains/H¹/H², nonflat F55 physical face field, source F42/F43 2/3-cell and local quotient/whiskering machinery | Identifying the real incidence K2,2 flag square with a C60 quadrilateral polygon; inferring local flatness from global surface cancellation |
| v5.194 / F59-F46 | 90-edge actual four flags joined locally to ORIGINAL F55 3-arrows; exact face exchange (0,0;1) vs F55 (0,1;1); unique ambient `Δ=(0,1;0)` | Existence of `Δ` in original F55 nine-constructor PresentedCell grammar |
| v5.195–v5.196 / F59-F47–F48 | Adjoined mixed four-boundary categorical 3-Hom, faithful Gray functor, all 90 edges and both actual incident faces, face-choice transport, exact local curvature | Original-source 2-cell identity across unrelated F42 and F54 types; unconditional global descent |
| v5.197 / F59-F49 | **Real 60-object C60 0/1-path graded Gray 3-category envelope**, Mathlib braided/3-Hom tensor coherence including nonidentity odd exchange | Global original raw 2-cell presentation: its 2-cell object is a **grade**, not a faithful F42/F54 raw term |
| v5.198 / F59-F50 | Original F42 proof-relevant face-2-cell local 3-Hom, fully source-decorated object category and faithful 3-morphism Gray lift, actual left/right 1-path whiskering and 90-edge original F43/F55 comparison | Injectivity on all original F42 source 2-cell **objects** into grades; raw term identity from equal grade |
| **v5.199 / F59-F51** | **NEW explicitly adjoined original-F42-indexed horizontal and vertical-context 3-cell source generators**, genuine Mathlib source 3-Hom category, faithful original F43 inclusion, source horizontal/vertical bifunctors and Gray tensor compatibility | Original source associators/unitors and pentagon/triangle not established by F51 alone; F54/F55 gluing open |
| **v5.200 / F59-F52-A** | **New, explicitly ADJOINED** F42-path-indexed associator and left/right unitor source 3-cells with genuine C60 `comp_assoc`/`nil_comp`/`comp_nil` transport; Mathlib 3-Hom kernel quotient, faithful F51 inclusion, F52 horizontal bifunctor, **associator and unitor naturality on all F52 3-arrows**, full Gray charge and original odd F43 north exchange retained | Original four-factor pentagon and triangle pasting **not proved**, source 3-Hom quotient equality is not raw F42 word equality, and a globally faithful F42/F54/F55 Gray 3-category remains open |
| **v5.201 / F59-F53-A** | Actual four-factor C60 1-path pentagon (two routes) and unit triangle (two routes), equality lifted to original F42 proof terms and every F52 typed 3-arrow by dependent transport; faithful reindexing Mathlib functor; adjoined source-aware associator and left/right unitor **isomorphisms** | **Original 3-arrow pentagon and triangle pasting remain OPEN**. Path-equality proof irrelevance is NOT the missing source-3-arrow coherence. F54/F55 global gluing remains open. |
| **v5.202 / F59-F53-B/C** | **ACTUAL source-typed original-F42 four-face 3-associator pentagon and unit 3-arrow triangle** with exact real C60 1-path reindexing, explicit 2-step/3-step raw routes, retained distinct original F42 witness objects, and equality in **F52 full-native-kernel quotient 3-Hom**, preserving the entire Int×Int/ZMod2 native evaluation | **Not** equality of distinct raw 3-cell syntax trees or globally faithful F42/F54/F55 Gray 3-category; original F55 nonflat curvature and new mixed `Δ` provenance are preserved |
| **v5.203 / F59-F54** | Genuine source F43 exchange iso and natural transformation between left-first and new right-first **Mathlib F52 3-Hom bifunctors**, original north phase-one exchange, F53 pentagon/triangle contextual compatibility. At all 90 actual C60 edges × both actual incident faces, source-typed original F52 F43 interchange and separate original F54/F55 square are connected by old F47 four-boundary category and uniquely calibrated `Δ=(0,1;0)` | **NOT** equality of original F42 and F54 source types, an original F55 Δ generator, all-original nondegenerate Gray 3-category or flat global descent. Original north local curvature charge remains `-5`. |
| **v5.204 / F59-F55-A/B** | The F48 one-way faithfully transported **ADJOINED F47 mixed source four-boundary** presentation is now proved bijective on all four tagged objects and fully faithful on ALL parallel native-kernel 3-Homs. Genuine reverse face-choice functor and transported source square at each of 90 C60 edges. On all 180 actual edge-face pairs **no original nine-constructor F55 PresentedCell** at the exact F54 left/right rotation-square boundaries can supply mixed calibration `Δ`. Full local categorical compatibility explicitly coexists with nonzero north signed curvature and **NO exact global original-F55 vertex gauge**. | This is NOT source word equality between differently typed original F42/F54 terms, a direct Mathlib Equivalence instance for unquotiented raw sources, original F55 Δ, or a global nondegenerate Gray 3-category/descent. |
| Runtime / AI | KuuOS reasoning method and formal proof repository; versioned CI checks of selected formal source | Model weight replacement, runtime loading/completeness of all KuuOS, universal output correctness, automatic or unauthorized actions |
| Infinite/Stage-II/universal mapping | Several specifically conditional or one-way factorization and descent statements | Unconditional infinite convergence, uniform normalization bound, global universal mapping equivalence without typed admissibility hypotheses |

**Historical sections 2–11** retain the precise earlier theorem references through v5.154; their earlier “next” descriptions are **historical**, not the current research frontier. The live proof frontier is in **sections 12–14 below**. A declared theorem type and its dependencies are the authority, not a version suffix, a PR title, or an uncited narrative. The v5.57 triangle-level certificate predates the separately verified actual swallowtail closure at v5.101.

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

## 11. F47–F57 CLOSED — finite original F45 paths, concrete C60 pentagon/square collar and F44 boundaries

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
| **F55-A / v5.152 / [#2120](https://github.com/itakura-hidetoshi/KuuOS/pull/2120)** | [Type-valued depth-aware pentagon routes](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45RotationDepthRoutesV5_152.lean): real F54 `RotationChain` edges retained within `DepthRotationRoute` and independently cast F19/F28 Nat depths; long actual **3**-edge and short actual **2**-edge five-vertex paths, proven RAW Type-valued inequality `pentagonLong_ne_short`; 9/9 `#print axioms`, 8855/8855 exact-head SUCCESS |
| **F55-B / v5.152 / [#2121](https://github.com/itakura-hidetoshi/KuuOS/pull/2121)** | [Original rotation square and presented cells](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152.lean): independent left-first/right-first contextual F54 paths (two rotations each); **free Type-valued** `PresentedCell` generators for concrete pentagon and square plus identity, inverse, transitive and contextual/pasting operations; 7/7 `#print axioms`, 8856/8856 GREEN. This is a presentation, not an imported Gray 3-cell equality |
| **F55-C1 / v5.152 / [#2122](https://github.com/itakura-hidetoshi/KuuOS/pull/2122)** | [Actual double-depth invariants](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationInvariantsV5_152.lean): `depthEq`, `toExchangeClass_eq`, `axisHistories_eq` for ALL five original DepthRotationRoute constructors, 3/2 pentagon class consequences and both freely presented path-cell F44 boundaries; 6/6 `#print axioms`, 8857/8857 GREEN |
| **F55-C2/C3 / v5.152 / [#2123](https://github.com/itakura-hidetoshi/KuuOS/pull/2123)** | [Original chosen mate](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationMatesV5_152.lean), [actual η/ε](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftDepthRotationV5_152.lean): original F19 right mate vs independent genuine F28 quotient, cast/functor commutation, both whole mapped primitive histories, freely presented cell endpoint certificates, unchanged source η/target ε; 7/7 `#print axioms`, 8861/8861 exact-head GREEN, new-file warning/error 0/0 |
| **F56-A / v5.153 / [#2125](https://github.com/itakura-hidetoshi/KuuOS/pull/2125)** | [Conditional target semantics](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ConditionalHigherCellTargetV5_153.lean): independently specified `HigherCellTarget` with typed pentagon, square, inverses and context/pasting structure; actual inductively defined `PresentedCell.interpret` for all constructors |
| **F56-B / v5.153 / [#2126](https://github.com/itakura-hidetoshi/KuuOS/pull/2126)** | [Pasting equations and count obstruction](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45HigherCellPastingObstructionV5_153.lean): exact left/right contextual and pre/postcomposition interpreter laws, and `HigherCellTarget.no_global_rotationCount` from original 3-versus-2 pentagon witness |
| **F56-C / v5.153 / [#2127](https://github.com/itakura-hidetoshi/KuuOS/pull/2127)** | [Concrete F44 observation](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ConcreteF44CellTargetV5_153.lean): Type-valued `F44ObservedCell` of four separate original F44 and both fully typed F19/F28 axis-history certificates; constructed `HigherCellTarget.originalF44`; final exact-head [CI #38106999972 SUCCESS](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38106999972). Only observational truncation, not external Gray 3-cells |
| **F56-D / v5.153 / [#2128](https://github.com/itakura-hidetoshi/KuuOS/pull/2128)** | [Exact observational information loss](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153.lean): observational fibers are `Subsingleton`, `F44ObservedCell ≃ PUnit`; raw `PresentedCell.ident route` differs from double identity paste, but their observations are equal, so original F44 observation is non-injective; 6/6 axioms, [CI #38107624498](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38107624498) GREEN |
| **F56-E / v5.153 / [#2129](https://github.com/itakura-hidetoshi/KuuOS/pull/2129)** | [Universal conditional factorization no-go](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellFactorizationNoGoV5_153.lean): any function from the raw free PresentedCell type factoring through original F44 observations is constant on fixed parallel-route boundaries, non-injective on its reflexive endomorphism fiber, and cannot have a reconstruction left inverse; applies to every chosen `HigherCellTarget` satisfying this exact factorization; 4/4 axioms, [CI #38107828541](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38107828541) GREEN |
| **F57-A / v5.154 / [#2131](https://github.com/itakura-hidetoshi/KuuOS/pull/2131)** | [Real C60 four-flag squares](formal/KUOS/DependentOriginationTruncatedIcosahedralFlagSquaresV5_154.lean): all 90 actual edges carry two distinct darts and two incident polygonal faces; four distinct vertex–face flags; around-vertex edges join actual pentagon and hexagon boundaries; each original five-edge pentagon edge carries a geometric square. [CI #38109064983](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38109064983): 8511/8511, 12/12 axioms, no changed-file warnings/errors |
| **F57-B / v5.154 / [#2132](https://github.com/itakura-hidetoshi/KuuOS/pull/2132)** | [Genuine C60-to-F55 pentagon labels](formal/KUOS/DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154.lean): all FIVE original geometric sides assigned exact typed original F55 rotation paths and F53 five different bracket vertices; first three forward, last two backward relative to C60 cyclic boundary, retaining original F19/F28 double Nat casts, 3+2 actual count and attached pentagon–hexagon four-flag squares. Actual F55 Type-valued pentagon cell and conditional HigherCellTarget interpreter. [CI #38109672930](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38109672930): 8860/8860, 15/15 axioms |
| **F57-C / v5.154 / [#2133](https://github.com/itakura-hidetoshi/KuuOS/pull/2133)** | [Independent original depth-aware squares](formal/KUOS/DependentOriginationCoherentBiadjunctionOriginalF45IndependentDepthSquaresV5_154.lean) and [C60 flag-square attachment](formal/KUOS/DependentOriginationTruncatedIcosahedralPentagonIndependentSquarePastingV5_154.lean): ANY two independently typed F55 finite depth-aware paths actually compose in left-first vs right-first order with equal genuine rotation counts, original F44 generated quotient equality and BOTH full F19/F28 histories; attach both paths to each C60 real pentagon/hexagon edge-local square. [CI #38110046529](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38110046529): 8862/8862, 12/12 axioms |
| **F57-D / v5.154 / [#2134](https://github.com/itakura-hidetoshi/KuuOS/pull/2134)** | [True cyclic geometric-square flag-corner gluing](formal/KUOS/DependentOriginationTruncatedIcosahedralCyclicSquareCollarGluingV5_154.lean): adjacent real four-flag squares share BOTH the same original endpoint dart and the same pentagonal seed face; the actual (dart,face) corner flag matches, is incident, and slot s4 closes to s0. The same shared-corner equation holds for F57-C path-square attachments, while signed original F55 labels retain their precisely typed matching intermediate trees. [CI #38110300250](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38110300250): 8863/8863, 7/7 axioms, warning/error 0/0 |

**Mathematical boundary through F57:** F55 gives distinct proof-relevant finite pentagon and square paths and a freely presented Type-valued higher generator, while F56 shows F44/whole-axis-history observation alone is NOT faithful to raw high-dimensional witnesses. F57 constructs actual C60 pentagon-edge incidence flags, geometric-to-F55 signed route labelling, two independent finite depth-aware square route orders and **5-cycle corner-flag gluing**. C60 has no quadrilateral polygon faces; these square flags are in the vertex–face incidence carrier. Shared corner flags do not imply equal adjacent hexagon faces, nor actual external Gray/tricategory 3-cell coherences. Separate original right mate/η/ε realization and independent higher target comparison remain open.

## 12. v5.155–v5.204: C60 / F58–F59 completed local theorem ledger

The F58/F59 programme has multiple **independent verified theorem scopes**. “Completed” below means the exact named Lean construction, not closure of the unbounded original-Gray 3-category research agenda. Physical C60 has **60V / 90E / 32F = 12 pentagons + 20 hexagons**; its edge-local 2-by-2 incidence **flag squares are not extra polygon faces**.

| Version / source | Verified theorem scope | Exact Lean representative |
| --- | --- | --- |
| **v5.155–v5.157** | Real C60 5/6-face signed incidence/Gray construction; native Mathlib braided category `GrayGrade`, phase-independent full F58 integer pair and ZMod2 exchange; actual physical C60 90 F55 square labels and cyclic pasting | [native braided Gray](formal/KUOS/DependentOriginationGrayNativeBraidedCategoryV5_156.lean), [all 90 edge pasting](formal/KUOS/DependentOriginationGrayC60AllNinetyEdgePastingV5_157.lean) |
| **v5.158–v5.168** | Original C60 physical oriented cellular chains, H¹/H²/potential and face-cochain descent under precisely stated conditions; original F55 uniform edge label produces genuine nonzero north-pentagon signed curvature; exact repair and support bounds remain separate from original unmodified source | [cochain descent](formal/KUOS/DependentOriginationGrayC60CochainDescentV5_166.lean), [genuine original F55 curvature](formal/KUOS/DependentOriginationGrayC60ActualF55CurvatureRepairV5_167.lean) |
| **v5.169–v5.175** | Source-aware yin/yang, complex/four-image, six-qi, Wang Bi and phase-locked original-F55 value subgroup; global oriented 32-face sum can vanish with **nonzero local curvature** | [Yin–Yang four-image](formal/KUOS/DependentOriginationGrayC60YinYangFourImagesV5_170.lean), [Wang Bi global descent](formal/KUOS/DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174.lean), [phase-locked original atlas](formal/KUOS/DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175.lean) |
| **v5.176–v5.189** | Original F55 graded source lifts, curved/flat repair and geometric Gray comparisons in the precise declared subfamilies; original C60 60-object directed edge-path Mathlib category rather than artificial singleton | [native physical path functor](formal/KUOS/DependentOriginationGrayC60NativePathFunctorV5_189.lean), [typed original F55 lift](formal/KUOS/DependentOriginationGrayC60TypedF55LiftV5_183.lean) |
| **v5.190–v5.193** | ORIGINAL proof-relevant F42 face 2-cell grammar indexed by actual parallel C60 paths; F43 interchange 3-cell with genuine phase; F44 native-evaluation quotient 3-Hom categories; real C60 left/right path whiskering functors | [F42 faces](formal/KUOS/DependentOriginationGrayC60PresentedFaceTwoCellsV5_190.lean), [F43 exchange](formal/KUOS/DependentOriginationGrayC60PresentedInterchangerV5_191.lean), [F44 3-Hom](formal/KUOS/DependentOriginationGrayC60ThreeHomCategoriesV5_192.lean), [F45 whiskering](formal/KUOS/DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193.lean) |
| **v5.194 / F59-F46 / [#2194](https://github.com/itakura-hidetoshi/KuuOS/pull/2194)** | Actual 90 four-flag carriers connected locally to ORIGINAL F54/F55 typed rotations, non-projected native F43 exchange and exact **unique** calibration `(0,0;1)+(0,1;0)=(0,1;1)`. `Δ` has no source in original nine-constructor F55 terms | [90 flag bridge](formal/KUOS/DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194.lean), [calibrated F55](formal/KUOS/DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194.lean) |
| **v5.195 / F59-F47 / [#2195](https://github.com/itakura-hidetoshi/KuuOS/pull/2195)** | NEW four-boundary typed mixed source 3-Hom category, complete-native-kernel faithful Mathlib functor, original north F55 square, left/right original path and F54 context whiskering | [adjoined typed mixed Hom](formal/KUOS/DependentOriginationGrayC60MixedBoundaryThreeHomV5_195.lean), [real north square](formal/KUOS/DependentOriginationGrayC60OriginalNorthMixedSquareV5_195.lean) |
| **v5.196 / F59-F48 / [#2196](https://github.com/itakura-hidetoshi/KuuOS/pull/2196)** | Both **actual distinct incident faces** of every original C60 edge have their own source-typed mixed square. Real face-choice transport between mixed Hom categories, sitewise Gray agreement, but original signed north curvature not erased; `Δ` north second charge `-5` / phase `0` | [all 90 mixed faces](formal/KUOS/DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196.lean), [obstruction](formal/KUOS/DependentOriginationGrayC60MixedComparisonObstructionV5_196.lean), [transport](formal/KUOS/DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196.lean) |
| **v5.197 / F59-F49 / [#2197](https://github.com/itakura-hidetoshi/KuuOS/pull/2197)** | Original physical **60-object and real C60 path** carrier for a **graded Gray 3-category envelope**; grade-completed 2-Hom, genuine typed full-charge/phase 3-Hom, all displayed Mathlib higher composition/braiding pentagon/triangle/hexagon coherences, and all 90 local mixed F55 square receivers on physical doubled face paths | [Gray 3-category envelope](formal/KUOS/DependentOriginationGrayC60GradedGrayThreeCategoryV5_197.lean), [coherence certificate](formal/KUOS/DependentOriginationGrayC60GrayThreeCategoryCoherenceV5_197.lean), [3-Hom composition functors](formal/KUOS/DependentOriginationGrayC60GrayThreeCategoryCompositionFunctorsV5_197.lean) |
| **v5.198 / F59-F50 / [#2198](https://github.com/itakura-hidetoshi/KuuOS/pull/2198)** | ORIGINAL F42 witness-carrying object category, F43 source 3-Hom with proven endpoint degree equality and fully faithful morphism-level Gray evaluation on the F44 quotient; original north left/right horizontal 2-cell terms **different**, their degree images equal, exchange 3-cell nontrivial | [original F43 faithful lift](formal/KUOS/DependentOriginationGrayC60OriginalFaceTypedThreeHomLiftV5_198.lean), [decorated original source](formal/KUOS/DependentOriginationGrayC60OriginalFaceDecoratedThreeHomV5_198.lean), [original whiskering](formal/KUOS/DependentOriginationGrayC60OriginalFaceWhiskeringNaturalityV5_198.lean) |
| **v5.199 / F59-F51 / [#2199](https://github.com/itakura-hidetoshi/KuuOS/pull/2199)** | Existing original F43 source grammar did **not** contain arbitrary horizontal 3-cell composition, so a new exactly F42-boundary-indexed horizontal/vertical-context original 3-cell presentation is **explicitly adjoined**. Its kernel-quotient 3-Hom category, genuine horizontal and vertical Mathlib product bifunctors, original-F43 faithful inclusion, full-charge/phase Gray coherence and real nonidentity north interchanger are proved | [new typed source](formal/KUOS/DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199.lean), [source 3-Hom](formal/KUOS/DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199.lean), [composition](formal/KUOS/DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199.lean), [coherence](formal/KUOS/DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199.lean) |
| **v5.200 / F59-F52-A / [#2202](https://github.com/itakura-hidetoshi/KuuOS/pull/2202)** | Original F42 witness retained under **both** actual path-endpoint transports; newly **adjoined** typed associator/left/right unit comparison 3-cells, original F51/F43 faithful inclusion in new source category, full-native kernel quotient, Mathlib horizontal 3-Hom bifunctor and arbitrary-morphism source associator/unitor naturality; real odd north F43 exchange phase remains nonidentity. Does **not** include source pentagon/triangle or original F54/F55 global gluing | [transport/source](formal/KUOS/DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200.lean), [3-Hom/faithful lift](formal/KUOS/DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200.lean), [naturality](formal/KUOS/DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200.lean) |
| **v5.201 / F59-F53-A / [#2204](https://github.com/itakura-hidetoshi/KuuOS/pull/2204)** | Two genuine four-path C60 pentagon equality proofs and two C60 unit-triangle equality proofs, separately acting on BOTH original F42 boundary paths and on ALL F52 source-aware typed 3-arrows; faithful Mathlib reindex functor; adjoined original-source associator / left/right unit **isomorphisms**. Still not full source-3-arrow pentagon/triangle pasting. | [path transports and isos](formal/KUOS/DependentOriginationGrayC60OriginalFacePentagonTransportV5_201.lean) |
| **v5.202 / F59-F53-B/C / [#2206](https://github.com/itakura-hidetoshi/KuuOS/pull/2206)** | Original four F42 face proof witnesses over the two real C60 paths: two-associator/three-associator **actual parallel source 3-arrow pentagon routes** and independent genuine **unit triangle** built from existing adjoined F52 source associator/unitors and typed transports, proved equal in F52 full-native-kernel quotient. No original raw source terms collapsed, F43 odd interchanger unchanged. | [original 3-arrow pentagon](formal/KUOS/DependentOriginationGrayC60OriginalFaceFourAssociatorPentagonV5_202.lean), [original 3-arrow triangle](formal/KUOS/DependentOriginationGrayC60OriginalFaceUnitTriangleV5_202.lean) |
| **v5.203 / F59-F54 / [#2208](https://github.com/itakura-hidetoshi/KuuOS/pull/2208)** | Proof-relevant original F43 exchange kept as typed F52 source iso and genuine natural transformation to a derived right-first horizontal Mathlib 3-Hom bifunctor; odd/odd interchanger remains nontrivial. Exact F43/F52 original face arrow maps into local F47 mixed category for each of 180 actual edge/adjacent-polygon sites, with original F54/F55 route independent; fully native unique `Δ` calibration, old-nine F55 nonrepresentability, signed north nonflat curvature and second-charge `-5` preserved. | [F43 right-first](formal/KUOS/DependentOriginationGrayC60OriginalF43RightHorizontalV5_203.lean), [typed F55 mix](formal/KUOS/DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203.lean) |
| **v5.204 / F59-F55-A/B / [#2211](https://github.com/itakura-hidetoshi/KuuOS/pull/2211)** | Fully faithful, objectwise bijective transport between F47 FOUR original-boundary-position mixed 3-Hom quotient categories of the two actual incident C60 faces. Actual reverse Mathlib functor and four-boundary square transport. Original raw F55 nine-constructor no-lift from either actual physical face of any of the 90 edges, at the exact F54 square-left/right route types, despite the unique adjoined comparison; local category compatibility and original-F55 nontrivial C60 no-vertex-gauge obstruction proved simultaneously. North signed calibration second charge `−5`, independent phase `0`, and odd original F43 exchange remain. | [full F47 mixed transport](formal/KUOS/DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204.lean), [actual original F55 non-descent](formal/KUOS/DependentOriginationGrayC60F55MixedDescentObstructionV5_204.lean) |

**Important naming:** v5.148’s earlier “F51” finite stage statement and v5.199’s **F59-F51** horizontal source three-Hom stage are different phases. Always cite **version + exact PR + declaration/file**, not the label alone.

**Source/target calculus:** The actual F43 interchange between distinct left-first/right-first original F42 face 2-cell words is a **nontrivial typed 3-arrow**, not an equation erasing those witnesses. In v5.199 new horizontal and vertical 3-arrow constructors were **added**, not recovered as if they had existed in the earlier F43 language. The complete target is an additive native Gray 3-cell with `Int×Int` charges and separate `ZMod 2` phase. Equality only after forgetting raw original F42 evidence is **not** a proof of source-level identical witnesses.

## 13. Next formal frontier: v5.205 / F59-F56 (source mixed face-change cocycle and contextual gluing)

**Goal:** continue from **v5.204/F55-A/B [#2211 MERGED]**: four-boundary adjoined F47 local mixed presentation transport is full/faithful, bijective on four tagged objects, and valid in both directions on every original physical C60 edge. The old F55 source nine-generator grammar lacks `Δ` at all 180 sites, and geometric signed original-F55 curvature still blocks global descent. Next prove source-typed two-direction/three-chart transport **cocycle** and interaction with independent original F42/F54 context functors, while retaining typed obstruction rather than inferring unproved globally faithful raw F42/F54/F55 gluing.

1. **Source associator/unitor — FIRST STAGE PROVED in #2202.** Newly adjoined comparison generators have exactly indexed original F42 source/target face witnesses and genuine C60 path `comp_assoc`/`nil_comp`/`comp_nil` reindexing. Further work: typed interaction with every original F42 whiskering context and the independent F54/F55 generators. These constructions are not old F43 cells and are not grade-only equalities.
2. **Associator and both unitor naturalities — PROVED in #2202 on F52 3-Hom.** Naturality holds for every F52 morphism under the new horizontal Mathlib bifunctor and dependent 1-path reindexing, hence includes the faithful F51 image; exact proof uses `Quot.inductionOn` / `Quot.sound` and independent full Gray charge/phase. The additional 2-context vertical interchange and mixed F54/F55 effects require their own correctly typed comparison data.
3. **Pentagon and triangle — SOURCE-3-ARROW QUOTIENT COHERENCE PROVED in #2206.** The four F42 face 2-cell terms are genuine proof-relevant objects, and the two-vs-three associator 3-arrow routes and associator/left-unitor vs right-unitor triangle are explicitly built with correct dependent C60 boundaries. Their equalities are established **in F52's full-native-kernel 3-Hom quotient**, not as raw source 3-word syntactic equalities. Full global original F54/F55 compatibility remains unproved.
4. **Gray interchange/whiskering — F43 NATURAL TRANSFORMATION PROVED in #2208.** Original F43 interchange iso, naturality and right-first F52 horizontal Mathlib bifunctor retain the nonidentity north phase; F53 pentagon and triangle are preserved in the right-first context. Further mixed two-dimensional context/whiskering with the original F54/F55 source still requires typed global coherence and cannot be inferred from equality of native target values.
5. **Mixed F54/F55 original boundaries — 180 LOCAL ORIGINAL BRIDGES PROVED in #2208.** Each original C60 physical edge and both independently typed incident polygon faces admits the existing F47 mixed source square: the F52 arrow is truly the old original F43 source interchange; the separate original F54/F55 rotation source arrow has the uniquely calibrated native value through newly adjoined `Δ=(0,1;0)`. Further target-level transport, higher naturality, and global coherent source gluing remain OPEN; the original F55 nine-generator source still cannot express `Δ`.
6. **C60 all-edge locality and descent.** Preserve every genuine four flag at each physical edge, distinct incident faces, signed pentagon/hexagon boundary, and **nonzero** north local curvature; distinguish a global 32-face cancellation from genuine local flatness/descent.
7. **v5.205 F56 cocycle and contextuality — OPEN.** Show true F47 four-boundary mixed functorial face-choice round trips and triple-composition coherence as source categorical equations, then verify compatibility with actual original F42 and F54 context whiskerings. Respect each physical 5/6 face incidence and nonzero north signed curvature. These obligations do not follow merely from hom-set bijectivity in the current quotient.

**Exit criteria:** exact Lean declarations with correct raw original indices; zero `sorryAx`/new axioms; full inherited axiom list; successful strict exact-head imported-closure CI and Governance/MCP receipts; no extra assumptions hidden in the raw source grammar. When an obligation is impossible, record the exact obstruction rather than weakening the theorem statement into grade-only equivalence.

## 14. Other open mathematical / runtime commitments

The following statements are **NOT** current unconditional Lean theorems: a full original globally nondegenerate C60/F42/F54/F55 Gray 3-category or equivalence to an external tricategory; arbitrary higher naturality/pentagon of *all* original generating 3-cells; unrestricted presentation-independent descent across varying original atlases; a uniform infinite-depth normalization bound or continuum limit; an unconditional higher universal mapping equivalence; correctness of a deployed interactive KuuOS LLM runtime.

The intended higher universal mapping schema remains a **research target**, not a proved generic equivalence:

~~~text
AdmissibleContextualSystems(C, X) ~ Fun(DO(C,W,J,H), X)
~~~

The v5.153 F56 original observation factorization no-go and v5.196 original phase-locked `Δ` obstruction must not be discarded by silently changing source types. Compare multiple presentations using actual transports, prove compatibility and descent only where hypotheses hold, otherwise retain the obstruction.

Interpretations of original five-elements (五行), three-yin-three-yang/six-qi, four-image (四象), three powers (三才), 10 heavenly stems, 12 earthly branches, 24 solar terms, 64 hexagrams, He Tu/Luo Shu, Wang Bi and classical philosophical notions remain **model-specific formal maps or research programmes**; a symbolic correspondence alone does not establish unrestricted native tricategorical functoriality or medical validity. Verify individual Lean declarations and domain-specific evidence.

## 15. Engineering discipline / exact-head workflow

- Re-observe fresh exact authoritative `main` SHA and PR source HEAD. **Docs-only** commits move `main` but do not add theorem statements.
- Keep pinned Lean `v4.30.0-rc2` and mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. **Never merge** protected Lean-4.31-only PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558).
- Distinguish actual `F/G/η/ε`, F19 chosen mates, independent F28 quotient, real C60 flag squares, original F42/F43 source, original F54/F55 source, **adjoined** F47/F51 generators and the F49 grade-completed target.
- In dependent Lean 4 constructions use exact types, explicit symbolic Nat transports, correctly oriented mate/whiskering equalities, `Quot.inductionOn`/`Quot.sound` **only after exposing raw representatives**, and typed `congrArg` projection equalities. Review **whole changed files**, not only the first CI error.
- Avoid `sorry`/`admit`/new axioms. Count `#print axioms` and differentiate the ordinary Lean trio from inherited `native_decide` dependencies. Zero changed-file warnings/errors is a separate gate.
- Cache and rebuild only selected affected imported closure where safe. A selected Strict Lean CI result does **not** prove unrelated runtime, UX, GitHub search index completeness or an entire LLM's behavior.
- Merge only after **exact-head GREEN** and full Governance, MCP Lean and MCP CI receipts. Verify actual PR CLOSED/MERGED, merge SHA, re-observed `main` and intact protected #1558. Failure/obstruction stays Draft with factual explanation.

## 16. Reproduction / 再現

The latest theorem-bearing baseline is **v5.204 / F59-F55-A/B**, [PR #2211](https://github.com/itakura-hidetoshi/KuuOS/pull/2211), theorem-bearing merge SHA `8a32f06d846edd95f33b048e8f7986066398533e`. v5.203/F54 is an ancestor, while [#2210](https://github.com/itakura-hidetoshi/KuuOS/pull/2210) changed the repository LICENSE to Apache-2.0 without new Lean declarations. Later docs-only merges are not theorem-bearing SHA updates.

~~~bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git KuuOS-repro
cd KuuOS-repro
git checkout 8a32f06d846edd95f33b048e8f7986066398533e
cat lean-toolchain
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204 \
  KUOS.DependentOriginationGrayC60F55MixedDescentObstructionV5_204
~~~

[Exact-head CI #38243833256](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38243833256) confirmed **9006/9006**, changed Lean warnings/errors **0/0**, **11 `#print axioms`** with no `sorryAx`/new axioms; Strict Lean, Governance and both MCP Lean/CI receipts **all SUCCESS**. This proves only the stated mixed-source F47/F55 local transport/no-go, not global all-original Gray 3-category, source-term gluing or unconditional descent.

~~~bash
# Independent broader build / runtime smoke test, NOT implied by the selected CI:
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
~~~

See [README.md](README.md), [GOVERNANCE.md](GOVERNANCE.md), [CITATION.cff](CITATION.cff), [LICENSE](LICENSE), [NOTICE](NOTICE), and [COPYRIGHT.md](COPYRIGHT.md). **Copyright © 2026 Hidetoshi Itakura / 板倉英俊; licensed under Apache-2.0.** Covered material may be adapted, redistributed and used commercially under Apache 2.0; these copyright permissions do not certify proof correctness or authorize medical, institutional, or runtime actions.
