# KuuOS / 空OS — Formal Roadmap

**2026-10-14 JST / latest VERIFIED theorem-bearing frontier: `v5.261 / F107`.** [PR #2281](https://github.com/itakura-hidetoshi/KuuOS/pull/2281) is **MERGED**, theorem-bearing merge SHA `62f878a739a3288174e8d1b68a754f8d9e239d73`, exact tested PR source HEAD `cc8e26d5049b849a403eb76b9878e2a89000cb9f`. [CI #38571374255](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38571374255) **completed SUCCESS**: Strict Lean **9073/9073**, changed-file warnings/errors **0/0**, **10 `#print axioms`**, no `sorryAx`; Governance, MCP Lean completion and MCP CI completion all **SUCCESS**.

**研究の現行方針：** 元の非自明なGray交換構造の復元を、新しい形式化ルートの前提にしません。**空＝指定された文脈・型・保存量のもとでの表現交代可能性**として、F94–F107では正確な局所商圏、普遍因子化、二方向の合成、自然同型と高次整合性、有限アトラスおよび実物理入射重なりの条件付きdescent、原F42/F51語からの意味論的関手を証明しています。元F55曲率・非整合は観測商圏の整合性によって消えません。

この文書では**(a) 現在のLeanで実際に証明済みの定理、(b) 過去に証明されたソース由来の歴史、(c) 追加条件を明示した定理、(d) 未証明の今後の課題、(e) ランタイム・実証研究**を区別します。GitHubのdocumentation-only更新は、Leanの新定理を証明しません。

## 0. Canonical authority / 正本と証跡

| 項目 | 正確な根拠 |
| --- | --- |
| Canonical repository | [`itakura-hidetoshi/KuuOS`](https://github.com/itakura-hidetoshi/KuuOS)、branch `main` |
| Latest verified theorem-bearing merge | [PR #2281 — v5.261 F107, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2281) |
| **Theorem-bearing SHA** | **`62f878a739a3288174e8d1b68a754f8d9e239d73`**（F107統合時に`main`との一致を確認） |
| Exact tested source HEAD | `cc8e26d5049b849a403eb76b9878e2a89000cb9f` |
| Exact-head formal CI | [run #38571374255](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38571374255) — **completed SUCCESS** |
| Strict Lean | Job `115877256162`, **9073/9073 SUCCESS** |
| Governance / MCP completion | Governance job `115878488116`、MCP Lean job `115878488494`、MCP CI job `115878598524` — **all SUCCESS** |
| F107 source diagnostics | **0 errors / 0 warnings**; **10 `#print axioms`**, no `sorryAx` |
| Toolchain | [`leanprover/lean4:v4.30.0-rc2`](lean-toolchain); [mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`](lake-manifest.json) |
| Separate validation-only lane | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) (Lean 4.31) — **OPEN / DRAFT / UNMERGED**; **do not merge** |
| Copyright and license | 板倉英俊 / Hidetoshi Itakura · [Apache-2.0](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT.md](COPYRIGHT.md) |

**Authority priority:** live exact `main` SHA → exact Lean declarations/imported proof artifacts → documentation as index → matching PR exact-source-head CI and completion receipts → historical notes. `main` SHA will move after this docs-only update; the theorem-bearing F107 SHA above remains the pinned reproduction reference until a NEW verified theorem lands.

**CI and axiom boundary:** successful selected `lake build` is evidence for its selected Lean target/dependency closure, **not** the entire repository/runtime/model. `#print axioms` can include ordinary `propext`/`Classical.choice`/`Quot.sound` and inherited finite-geometric `native_decide` axioms. Neither `sorryAx` nor a new unreviewed assumption is permitted in accepted theorem-bearing changes. Keep physical assertions tied to the original source type; do not infer raw F42/F55 equality from an F77 quotient equality.

## 1. Live formal truth table / 現在の成立範囲と未証明の境界

| 数学的範囲 | VERIFIED in Lean (at its exact stated types/hypotheses) | NOT established |
| --- | --- | --- |
| `v4.00–v5.101` | Presentation/label-sensitive localization, explicit obstructions, original actual-lift `F/G/η/ε` and two separately proved swallowtails; [one coherent biadjunction carrier](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean) | Arbitrary source strictification, removal of original choices |
| `v5.102–v5.154` | Native mates, independent original F19/F28 histories, finite higher-pasting presentations, original F45/F54/F55 paths | Automatically lifting all adjoined mixed 3-cells back into the old source grammar |
| `v5.155–v5.228` | Actual C60 60/90/32 incidence, 360 real flags, typed original F42/F51/F55, signed curvature, geometric nerve, finite atlas and conditional higher comparisons | Global raw original faithful Gray three-category, unconstrained physical hyperdescent |
| **F75–F79 / v5.229–233** | New strict-charge target, genuine `CategoryTheory.Quotient` forgetting only phase, real path-indexed grade-completed F78 globular certificate, equivalence to charge groupoid | Original odd/odd braiding is identity before projection; strict equality of distinct raw F42 |
| **F80–F93 / v5.234–247** | Quotient tensor and middle-four, separately constructed monoidal structures, exact comparison tensorators, phase-zero section and F93 proved equality | Individual gauge terms necessarily zero, or original Gray phase recovered |
| **F94–F99 / v5.248–253** | `f ~ g ⇔ Qf = Qg ⇔ charge(f)=charge(g)`, genuine F95 universal quotient, horizontal/vertical quotient bifunctors, F98 observed mixed `NatIso`, F99 left/right whiskering descent | Source-wide raw F42/F55 collapse or physical global gluing |
| **F100–F102 / v5.254–256** | Two-sided C60 context-order `NatIso`, four-input contextual horizontal/vertical natural square, double-context order-vs-exchange commuting square | Unquotiented original Gray interchanger restored or all F55 physical curvature erased |
| **F103 / v5.257** | F77 zero-additional-charge `NatTrans` uniqueness, observed four-path pentagon, three-step path context vs bundled path, F102 route uniqueness | Nontrivial source-level Mac Lane pentagon for every raw F42/F55 presentation |
| **F104 / v5.258** | A finite `Fin n` family of genuine two-sided contexts on **one fixed original path pair**, normalized Čech 1-cocycle, inverse, arbitrary finite history independence and zero-charge gluing criterion | Descent over arbitrary physical patches with different F95 local source types |
| **F105 / v5.259** | Finite family of **different actual physical edge patches**: given common overlap category/restrictions, exact `Int×Int` charge-difference cocycle, conditional observed gluing and nonzero obstruction; F68 north curvature stays `−5` | Existence of a canonical overlapping incidence category or its F95 restriction semantics without extra data |
| **F106 / v5.260** | Genuine F69 physical incidence-star finite intersections and subset restriction functors, actual shared-endpoint/shared-face witnesses, conditional `NatIso`/cocycle on these intersections | Constructing original F42/F51 words or arbitrary singleton-star→F95 semantics merely from incidence |
| **F107 / v5.261** | **Given** original F42 labels and boundary-typed F51 raw word labels, two-charge identity/composition coherence **constructs** true physical singleton-star→F95 functors and derived multi-overlap semantics. Separately phase-coherent input yields full-native F51 functor. Degree mismatch and nonzero phase defect obstruct specified source lifts. | Unconditional existence of those source labels/words from 360 flags, or F55 boundary compatibility/global source descent |

### Read this before claiming descent

For correctly typed parallel ORIGINAL F51 arrows `f,g`, the true F94/F95 categorical relation is

\[
f\sim_{\mathrm{kuu}} g
\iff Q(f)=Q(g)
\iff \operatorname{charge}(f)=\operatorname{charge}(g)\in\mathbb{Z}^2.
\]

The two original integer-charge components are retained and `ZMod 2` Gray phase is intentionally forgotten **only at the named quotient**. F95's universal factorization `F = \bar F \circ Q` requires `F` to RESPECT this exact relation. Arbitrary source objects/words are not made equal.

**Physical curvature boundary:** C60 has 60 actual vertex darts, 90 edges, 12 original pentagons + 20 original hexagons. The `K₂,₂` around an edge is an incidence square, not an extra original quadrilateral face. F68 proves a signed original north-pentagon curvature component **`−5`**, while the total oriented fundamental 32-face signed boundary cancels. Hence local nonflatness and necessary nonzero correction survive F77/F95 observer gluing. Original independently adjoined mixed `Δ` is not an old nine-constructor F55 expression.

**Historical ledger:** Sections **2–12** preserve the exact v4.00–v5.212 origin of the current construction. Statements there about previously “next” work are historical; **current closed and open frontier is Sections 13–15**. Identify a theorem by full version/PR/Lean file, because F-labels were also used in earlier sub-programmes.

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

## 12. v5.155–v5.212: C60 / F58–F61 historical original-source theorem ledger

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
| **v5.204 / F59-F55-A/B / [#2211](https://github.com/itakura-hidetoshi/KuuOS/pull/2211)** | F47 mixed four-boundary bijective object/Hom transport for real two original incident C60 faces; authentic original F54 square-route F55 nine-constructor nonlift on 90×2 local source frames and original F55 vertex-gauge no-go despite local full/faithful compatibility. | [full F47 mixed transport](formal/KUOS/DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204.lean), [original F55 non-descent](formal/KUOS/DependentOriginationGrayC60F55MixedDescentObstructionV5_204.lean) |
| **v5.205 / F59-F56-A/B / [#2213](https://github.com/itakura-hidetoshi/KuuOS/pull/2213)** | Same original F54 route-type local four-boundary transport: source 3-Hom identity/round-trip/three-frame cocycle and Mathlib natural isomorphisms; NEW genuine cross-original F42/F54 left/right contextual F47 mixed functors retaining each original 2-cell and F54 route type plus mixed-square coherence. | [typed F47 cocycle](formal/KUOS/DependentOriginationGrayC60F55MixedCocycleV5_205.lean), [original contextuality](formal/KUOS/DependentOriginationGrayC60F55MixedOriginalContextV5_205.lean) |
| **v5.206 / F59-F57-A/B / [#2215](https://github.com/itakura-hidetoshi/KuuOS/pull/2215)** | Cross-original F42 face path and F54 rotation-source three-chart F47 mixed context: object and every source mixed 3-Hom bijection; two-sided and three-chart source 3-Hom cocycle with actual Mathlib NatIso even when all three original F54 route types differ. Both independently typed original F42/F54 left/right source contexts full & faithful with true mixed four-boundary categorical source squares, while original F55 nine-constructor source nonlift persists after every contextual whisker. | [cross-original cocycle](formal/KUOS/DependentOriginationGrayC60F55CrossRotationCocycleV5_206.lean), [whiskered F55 nonlift](formal/KUOS/DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206.lean) |
| **v5.207 / F59-F58-A/B / [#2217](https://github.com/itakura-hidetoshi/KuuOS/pull/2217)** | Explicit source-dependent Hom casts and genuine left/right original F42 path + original F54/F55 tree context **Beck–Chevalley NatIso** comparing context and F47 face-choice in both orders. Full typed source 3-Hom identities in the native-kernel mixed quotient. Physically instantiated at the two DIFFERENT original 5/6-sided adjacent polygon faces of EACH real C60 physical edge; their actual loop base darts and all four vertex/face incidences are retained. After both original contexts, the mixed correction `Δ` still has no original nine-constructor F55 source. | [general BC source](formal/KUOS/DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207.lean), [real C60 incidence BC](formal/KUOS/DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207.lean) |
| **v5.208 / F59-F59-A/B / [#2219](https://github.com/itakura-hidetoshi/KuuOS/pull/2219)** | Typed Mathlib two-context source Beck–Chevalley pasting with explicit 3 functor associators and iso whiskerings, LEFT and RIGHT original F42/F54 two-stage source contexts, complete intermediate F43/F55 native equality, all 90 real C60 edge/two face bases, persistent original F55 nine-constructor Δ nonlift after two contexts. Direct-composite raw syntax and 3-context coherence remain OPEN. | [left two-step source](formal/KUOS/DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208.lean), [right physical two-step](formal/KUOS/DependentOriginationGrayC60F55TwoContextPhysicalV5_208.lean) |
| **v5.209 / F59-F60-A/B / [#2221](https://github.com/itakura-hidetoshi/KuuOS/pull/2221)** | Actual original-F42 concatenated left/right C60 Quiver.Path source with exact `comp_assoc` index casts; actual original-F54/F55 `node` and two-depth `Nat.add_assoc` rebracketing; LEFT/RIGHT source F47 direct-vs-nested full-Hom comparison and Mathlib NatIso. ALL real 90 physical edges and each true incident polygonal face; old nine-constructor F55 correction Δ no-lift survives direct source composition. Higher direct BC vs pasted BC natural-isomorphism equality remains OPEN. | [direct left and original indices](formal/KUOS/DependentOriginationGrayC60F55DirectCompositeContextV5_209.lean), [right and real incidence](formal/KUOS/DependentOriginationGrayC60F55DirectCompositePhysicalV5_209.lean) |
| **v5.210 / F59-F60-C / [#2223](https://github.com/itakura-hidetoshi/KuuOS/pull/2223)** | Four-tag rank on ORIGINAL F47 raw mixed 3-cells, nonidentity generator rank increase, equal-rank native-zero theorem and full-native-kernel source endomorphism rigidity; LEFT and RIGHT direct-vs-two-stage original F42/F54 Beck–Chevalley NatIso equalities after F60 typed original path/tree normalization. Both specialized to all 90 C60 physical edges/two genuinely distinct incident polygon bases. Raw unquotiented original Gray 3-category and unrestricted descent NOT established. | [F47 endomorphism rigidity](formal/KUOS/DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210.lean), [left source BC](formal/KUOS/DependentOriginationGrayC60F55DirectPastedBeckChevalleyV5_210.lean), [right source BC](formal/KUOS/DependentOriginationGrayC60F55DirectPastedPhysicalV5_210.lean), [all physical incidences](formal/KUOS/DependentOriginationGrayC60F55PhysicalDirectPastedBCV5_210.lean) |
| **v5.211 / F59-F61-A / [#2225](https://github.com/itakura-hidetoshi/KuuOS/pull/2225)** | Original F42 Quiver.Path three-successive context dependent associativity/face degree/native Gray preservation, original F54/F55 three genuine bracket-node trees with two F19/F28 depth `Nat.add_assoc` transports. | [three original context](formal/KUOS/DependentOriginationGrayC60F55ThreeOriginalContextV5_211.lean) |
| **v5.212 / F59-F61-B1–B4 / [#2227](https://github.com/itakura-hidetoshi/KuuOS/pull/2227)** | Two original three-step source BC parenthesizations with Mathlib associators/whiskering. LEFT and RIGHT independently original F42/F54/F55 context source NatIso equality in F47 full-native-kernel four-tag 3-Hom. All true 90 C60 physical edges/two distinct incident faces. Four-context pentagon and neighbor patch descent still OPEN. | [abstract source](formal/KUOS/DependentOriginationGrayC60F55ThreeContextBeckChevalleyV5_212.lean), [left original source](formal/KUOS/DependentOriginationGrayC60F55ThreeOriginalLeftBeckChevalleyV5_212.lean), [right original source](formal/KUOS/DependentOriginationGrayC60F55ThreeOriginalRightBeckChevalleyV5_212.lean), [physical incidence](formal/KUOS/DependentOriginationGrayC60F55ThreeContextPhysicalV5_212.lean) |

**Important naming:** v5.148’s earlier “F51” finite stage statement and v5.199’s **F59-F51** horizontal source three-Hom stage are different phases. Always cite **version + exact PR + declaration/file**, not the label alone.

**Source/target calculus:** The actual F43 interchange between distinct left-first/right-first original F42 face 2-cell words is a **nontrivial typed 3-arrow**, not an equation erasing those witnesses. In v5.199 new horizontal and vertical 3-arrow constructors were **added**, not recovered as if they had existed in the earlier F43 language. The complete target is an additive native Gray 3-cell with `Int×Int` charges and separate `ZMod 2` phase. Equality only after forgetting raw original F42 evidence is **not** a proof of source-level identical witnesses.



## 13. Verified quotient/replaceability programme — v5.213–v5.261

### 13.1 From finite C60 context to an intentional phase quotient (v5.213–v5.233)

| Verified release | Distinct mathematical contribution | PR |
| --- | --- | --- |
| `v5.213–v5.217` | Actual original F47 dependent pasting; native quasicategories/Duskin-nerve bridges, C60 face-choice map and adjoining face-category equivalences with genuine finite incidence | [#2229](https://github.com/itakura-hidetoshi/KuuOS/pull/2229), [#2230](https://github.com/itakura-hidetoshi/KuuOS/pull/2230), [#2232](https://github.com/itakura-hidetoshi/KuuOS/pull/2232), [#2233](https://github.com/itakura-hidetoshi/KuuOS/pull/2233), [#2234](https://github.com/itakura-hidetoshi/KuuOS/pull/2234), [#2235](https://github.com/itakura-hidetoshi/KuuOS/pull/2235) |
| `v5.218–v5.222` | Real signed C60 cochains/curvature and curvature-aware descent; 90-edge atlases, higher Čech coherence (including finite chains), and exact flatness/repair criteria | [#2236](https://github.com/itakura-hidetoshi/KuuOS/pull/2236), [#2237](https://github.com/itakura-hidetoshi/KuuOS/pull/2237), [#2238](https://github.com/itakura-hidetoshi/KuuOS/pull/2238), [#2239](https://github.com/itakura-hidetoshi/KuuOS/pull/2239), [#2240](https://github.com/itakura-hidetoshi/KuuOS/pull/2240) |
| `v5.223–v5.227` | 360 actual flag incidence, Grothendieck/nerve and conditional C60 transport comparisons; **revised original typed 3-arrow-first F73** (the earlier F73 draft [#2245](https://github.com/itakura-hidetoshi/KuuOS/pull/2245) was not merged) | [#2241](https://github.com/itakura-hidetoshi/KuuOS/pull/2241)–[#2244](https://github.com/itakura-hidetoshi/KuuOS/pull/2244), [#2246](https://github.com/itakura-hidetoshi/KuuOS/pull/2246) |
| **`v5.228 / F74`** | Actual original F43 interchange as source-level typed three-arrow `Iso` and naturality, retained as historical/source comparison evidence | [#2247](https://github.com/itakura-hidetoshi/KuuOS/pull/2247) |
| **`v5.229 / F75`** | Deliberately forget original independent Gray exchange phase in an **explicit strict-charge target**, preserving original `Int × Int` charges and nontrivial curvature | [#2248](https://github.com/itakura-hidetoshi/KuuOS/pull/2248) |
| **`v5.230 / F76`** | Strict charge horizontal 3-arrow product and strict middle-four interchange | [#2249](https://github.com/itakura-hidetoshi/KuuOS/pull/2249) |
| **`v5.231 / F77`** | Genuine Mathlib categorical **kernel congruence quotient** and universal phase-killing factorization, not merely a charge-only metaphor | [#2250](https://github.com/itakura-hidetoshi/KuuOS/pull/2250) |
| **`v5.232 / F78`** | Real C60 60-vertex and directed `Quiver.Path` 0/1 carrier; grade-completed 2-cells/charge-sensitive 3-cells with proved strict **globular coherence certificate** | [#2251](https://github.com/itakura-hidetoshi/KuuOS/pull/2251) |
| **`v5.233 / F79`** | Genuine `CategoryTheory.Equivalence` between the F77 native quotient and strict-charge groupoid | [#2252](https://github.com/itakura-hidetoshi/KuuOS/pull/2252) |

These results explicitly distinguish: (a) original C60 proof terms; (b) adjoined mixed or higher source generators; (c) the grade-completed model; (d) the purposeful **new quotient**. Nothing in this programme claims that a nonidentity old Gray braiding was already an identity in its original domain.

### 13.2 Genuine quotient tensor and canonical comparison (v5.234–v5.247)

| Stage | Proved object and morphism data | PR |
| --- | --- | --- |
| **F80 · v5.234** | Quotient-Hom tensor defined by `Quot.liftOn₂`, both representative-independence proofs, real bifunctor and strict middle-four | [#2253](https://github.com/itakura-hidetoshi/KuuOS/pull/2253) |
| **F81 · v5.235** | Mathlib quotient monoidal coherence, associator/unit equations | [#2254](https://github.com/itakura-hidetoshi/KuuOS/pull/2254) |
| **F82 · v5.236** | Genuine transported-vs-direct quotient tensor `NatIso`, naturality in every quotient Hom | [#2255](https://github.com/itakura-hidetoshi/KuuOS/pull/2255) |
| **F83 · v5.237** | Independent `MonoidalCategory` on the direct quotient, pentagon/triangle | [#2256](https://github.com/itakura-hidetoshi/KuuOS/pull/2256) |
| **F84 · v5.238** | Strong-monoidal quotient-to-charge comparison over F79 equivalence | [#2257](https://github.com/itakura-hidetoshi/KuuOS/pull/2257) |
| **F85 · v5.239** | Monoidal equivalence of separately built transported/direct quotient monoidal structures | [#2258](https://github.com/itakura-hidetoshi/KuuOS/pull/2258) |
| **F86–F89 · v5.240–v5.243** | Comparison tensorator/obstruction on *actual* quotient Hom, transport charge identities, full four `ZMod 2 × ZMod 2` grade-pair classification | [#2259](https://github.com/itakura-hidetoshi/KuuOS/pull/2259)–[#2262](https://github.com/itakura-hidetoshi/KuuOS/pull/2262) |
| **F90 · v5.244** | Explicit zero-phase section of native quotient-charge equivalence, object and Hom roundtrip | [#2263](https://github.com/itakura-hidetoshi/KuuOS/pull/2263) |
| **F91 · v5.245** | Genuine selected-vs-canonical inverse `NatIso` and explicit gauge comparison | [#2264](https://github.com/itakura-hidetoshi/KuuOS/pull/2264) |
| **F92 · v5.246** | Selected-unit gauge, additive coboundary and mediated-correction charge decomposition; do not assume chosen gauge vanishes | [#2265](https://github.com/itakura-hidetoshi/KuuOS/pull/2265) |
| **F93 · v5.247** | Actual F85 mediated tensorator charge calculation and **comparison tensorator equality** on all original F77 quotient objects; zero total obstruction without setting each gauge term to zero | [#2266](https://github.com/itakura-hidetoshi/KuuOS/pull/2266) |

Core proof API: `c60F77Projection_exactKernel`, `c60F80QuotientThreeTensor_middleFour`, `c60F82TransportedVsF80TensorNatIso`, `c60F90Section_rightMap`, `c60F93AllTensorators_agree`. Read the fully qualified Lean declarations in the corresponding source files before relying on their assumptions and domains.

### 13.3 空 as genuine Kuu replacement and composition (v5.248–v5.253)

| Stage / file | Proved real categorical statement | PR |
| --- | --- | --- |
| **F94 / [`DependentOriginationC60KuuReplacementInterchangeV5_248.lean`](formal/KUOS/DependentOriginationC60KuuReplacementInterchangeV5_248.lean)** | `c60F94Replaceable_iff_charges`; replacement equivalence on correctly typed original F51 3-Homs and source horizontal/vertical categorical stability, F78/F93 comparisons | [#2267](https://github.com/itakura-hidetoshi/KuuOS/pull/2267) |
| **F95 / [`DependentOriginationC60KuuLocalUniversalDescentV5_249.lean`](formal/KUOS/DependentOriginationC60KuuLocalUniversalDescentV5_249.lean)** | `C60F95LocalKuuQuotient`, `c60F95Universal_existsUnique`; real local category quotient with universal factorization for any **replaceability-respecting** observer | [#2268](https://github.com/itakura-hidetoshi/KuuOS/pull/2268) |
| **F96 / [`DependentOriginationC60KuuLocalHorizontalFunctorV5_250.lean`](formal/KUOS/DependentOriginationC60KuuLocalHorizontalFunctorV5_250.lean)** | `c60F96LocalHorizontalFunctor`; genuine local-quotient **horizontal** bifunctor with middle-four; exact F77 tensor observation | [#2269](https://github.com/itakura-hidetoshi/KuuOS/pull/2269) |
| **F97 / [`DependentOriginationC60KuuLocalVerticalFunctorV5_251.lean`](formal/KUOS/DependentOriginationC60KuuLocalVerticalFunctorV5_251.lean)** | `c60F97LocalVerticalFunctor`; independently constructed local-quotient **vertical two-context** bifunctor with strict Hom functoriality and F77/F78 observation | [#2270](https://github.com/itakura-hidetoshi/KuuOS/pull/2270) |
| **F98 / [`DependentOriginationC60KuuObservedMixedInterchangeV5_252.lean`](formal/KUOS/DependentOriginationC60KuuObservedMixedInterchangeV5_252.lean)** | `c60F98ObservedMixedNatIso`; four-input **observed** horizontal/vertical mixed interchange, with `c60F98ObservedMixedNatIso_charge_zero`, retaining distinct raw F42 output presentations | [#2271](https://github.com/itakura-hidetoshi/KuuOS/pull/2271) |
| **F99 / [`DependentOriginationC60KuuContextWhiskeringDescentV5_253.lean`](formal/KUOS/DependentOriginationC60KuuContextWhiskeringDescentV5_253.lean)** | `c60F99LeftWhiskerFunctor` and `c60F99RightWhiskerFunctor` by F95 universal descent; separate genuine observed left/right `NatIso` with zero *additional* `Int × Int` charge | [#2272](https://github.com/itakura-hidetoshi/KuuOS/pull/2272) |

The observation hierarchy, not raw proof-term equality, is the constructive result:

```text
REAL C60 original F51 path-indexed 3-Hom presentations
        |  exact F94 kernel: equality of both integer charges
        v
F95 real local Kuu categorical quotient + universal factorization
        |                     |
        | F96 horizontal      | F97 vertical 2-context
        +-----------+---------+
                    v
          F77/F78 observable typed quotient
                    |
              F98 observed mixed NatIso
                    |
         F99 left/right context functors + observed NatIso
```

**Positive information is retained.** The original 3-arrow charge pair is not zeroed. F98's and F99's *comparison* isomorphisms contribute **zero extra charge**. This is not the same as forcing all physical C60 curvature or all source generators to vanish.


### 13.4 F100–F103 CLOSED — actual C60 context order, mixed exchange and observed pentagon (v5.254–v5.257)

| Stage / exact source | Verified mathematical content | PR |
| --- | --- | --- |
| **F100 / v5.254** — [`DependentOriginationC60KuuTwoSidedContextCoherenceV5_254.lean`](formal/KUOS/DependentOriginationC60KuuTwoSidedContextCoherenceV5_254.lean) | Actual left→right and right→left path-context functors observed at their **separately typed original F42 presentations**. `c60F100ObservedTwoSidedNatIso` and preserved arbitrary `Int × Int` Hom charge, zero added comparison charge. | [#2274](https://github.com/itakura-hidetoshi/KuuOS/pull/2274) |
| **F101 / v5.255** — [`DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255.lean`](formal/KUOS/DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255.lean) | Four independent local-quotient inputs contextualized by genuine C60 paths; actual F98 H/V exchange after context, `c60F101MixedSquare_natTrans` and zero-additional-charge comparisons. | [#2275](https://github.com/itakura-hidetoshi/KuuOS/pull/2275) |
| **F102 / v5.256** — [`DependentOriginationC60KuuFourInputDoubleContextCoherenceV5_256.lean`](formal/KUOS/DependentOriginationC60KuuFourInputDoubleContextCoherenceV5_256.lean) | Both typed two-sided context orders for each of four source factors and both H/V pasting orders; `c60F102OrderMixedSquare_natTrans` equates the two genuine F77 natural-transformation routes. Oppositely oriented bridge paths are distinct, not assumed inverse. | [#2276](https://github.com/itakura-hidetoshi/KuuOS/pull/2276) |
| **F103 / v5.257** — [`DependentOriginationC60KuuObservedContextPentagonV5_257.lean`](formal/KUOS/DependentOriginationC60KuuObservedContextPentagonV5_257.lean) | Unique **zero-added-charge** F77 natural comparison, transitive path-context `NatIso`, five authentic path brackets and `c60F103ObservedPentagon_natTrans`, sequential versus bundled path context, F102 higher comparison uniqueness. | [#2277](https://github.com/itakura-hidetoshi/KuuOS/pull/2277) |

**Boundary:** `NatIso` and pentagon are at the F77 **observer** level. They do not identify unequal raw F42 proof trees or prove flatness of the unquotiented F55 source.

### 13.5 F104–F107 CLOSED — conditional finite/physical incidence descent and original-word semantics (v5.258–v5.261)

| Stage / exact source | Verified mathematical content | PR |
| --- | --- | --- |
| **F104 / v5.258** — [`DependentOriginationC60KuuFiniteContextCechDescentV5_258.lean`](formal/KUOS/DependentOriginationC60KuuFiniteContextCechDescentV5_258.lean) | `c60F104AtlasTransition_cocycle` and normalized identity/inverse; arbitrary length finite `List (Fin n)` histories compare to direct transition in F77; base cone compatibility; arbitrary natural comparison glues iff its **added** integer charge vanishes. **One fixed original path pair**, arbitrary genuine prefix/suffix contexts. | [#2278](https://github.com/itakura-hidetoshi/KuuOS/pull/2278) |
| **F105 / v5.259** — [`DependentOriginationC60KuuPhysicalOverlapObstructionV5_259.lean`](formal/KUOS/DependentOriginationC60KuuPhysicalOverlapObstructionV5_259.lean) | Different original physical edge patch path pairs; **given** shared overlap category and restrictions, F77 observers, skew and additive charge defect cocycle, conditional `NatIso` iff all Hom defects zero **when observed objects match**; arbitrary finite comparison history; nonzero defect obstruction. `c60F105ObservedGlue_retainsNorthCurvature` keeps original second charge `−5`. | [#2279](https://github.com/itakura-hidetoshi/KuuOS/pull/2279) |
| **F106 / v5.260** — [`DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260.lean`](formal/KUOS/DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260.lean) | `C60F106PhysicalOverlap` of actual F69 physical-incidence stars, restriction `J⊆I : O_I → O_J`, shared actual vertex or polygon face witnesses, `c60F106PhysicalChargeDefect_cocycle` and conditional `c60F106PhysicalTransition_cocycle`. **Singleton-star→F95 semantics is still explicit extra input.** | [#2280](https://github.com/itakura-hidetoshi/KuuOS/pull/2280) |
| **F107 / v5.261** — [`DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261.lean`](formal/KUOS/DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261.lean) | `C60F107OriginalF42Labels` + `C60F107OriginalF51Words` **given** on real physical-star incidence Hom, with `C60F107ChargeCoherence`, yield `c60F107SingletonKuuFunctor` and derived finite-overlap Kuu semantics; replacement iff both integer charges equal. Independent `C60F107PhaseCoherence` yields `c60F107NativeF51Functor` with `c60F107NativeProjection_equalsKuu`. Boundary degree mismatch and nonzero composition-phase defect are **obstructions**, not silently removed. | **[#2281](https://github.com/itakura-hidetoshi/KuuOS/pull/2281)** |

### 13.6 Exact current logical hierarchy

```text
Genuine physical geometry: 60 vertices / 90 edges / 32 original faces
              |                                 |
       F69 incidence category            F68 physical curvature != 0
              |                            north second charge = -5
       F106 actual incidence stars                  |
              |                                     +--> keep obstruction
       F107 original F42 labels + F51 typed source words (INPUT)
              |            |
       Int×Int charge     independent ZMod2 Gray phase
       coherence          coherence (STRICTER, separate)
              |            |
              v            v
     F95 Kuu quotient     F51 native-source functor
     functor (proved)     (conditional lift only)
              |            |
              +---- if phase-coherent: projection recovers F95 semantics
              v
F77 quotient observations, F98-F103 natural coherence
              |
F104 fixed-pair finite context Cech
              |
F105 different-edge overlaps with GIVEN common category + restrictions
              |
F106 actual geometric overlap/refinement + GIVEN singleton semantics
              |
F107 derivation of singleton semantics from GIVEN original typed words
              |
no unconditional global physical F55 glue / hyperdescent
```

The **only** gluing comparison asserted for heterogeneous original physical patches is conditional on **explicitly given** overlap semantics and observed-object equality plus zero charge difference for every relevant Hom. The difference

\[
\omega_{ij}(f)=Q_i(f)-Q_j(f)\in\mathbb Z^2,\qquad
\omega_{ij}(f)+\omega_{jk}(f)=\omega_{ik}(f)
\]

is a genuine signed charge 1-cocycle (additive even when no glue exists). A witness with `\omega_{ij}(f)\ne0` obstructs a zero-added-charge comparison, rather than being “repaired” without authority.

## 14. Active theorem frontier — F108 and successors (OPEN / not yet proven)

**F108 — actual C60 flag-to-original-word construction.** F107 does **not** construct its original F42 object labels and F51 raw words from incidence alone. Take the real F69 incidence triangles `vertex → edge → genuine pentagon/hexagon` and F46's actual four flags at each of the 90 physical edges. Attempt to build a **non-vacuous** typed F42/F51 source assignment with the correct original `Quiver.Path` endpoints and source/target F42 witnesses; prove charge identity/composition equations from the chosen generators, rather than assuming them. Preserve the distinction between an inserted F51 horizontal/vertical generator and an OLD F43/F55 source constructor. If construction is impossible for some boundary, state the exact **F42 face-degree** or unliftable-source obstruction; never inhabit a missing object by silently replacing it with an arbitrary Gray grade.

**F109 — geometrically controlled compatibility across physical intersections.** Determine when separately constructed F108 singleton-star source semantics agree on the ACTUAL F106 intersections. Prove observed-object compatibility and `Int × Int` charge-zero defect on all incidence arrows only if the relevant F42/F51 boundary evidence supplies it. Use F105/F106 to obtain honest Čech `NatIso` and independence of finite refinement routes. If independent chosen word labels have nonzero charge difference, retain `\omega_{ij}\neq0` as a proved witness. Relate to F71's full incidence `Cat`-valued extension **as a conditional interface**, not a known existing global extension.

**F110 — phase/cohomology and physical obstruction in one typed comparison.** Distinguish original F51 full-native `ZMod 2` phase coherence from F95 charge-only coherence. Explicitly compare local mixed/F55 source boundaries, original F68 signed 2-cochain and corrected-versus-uncorrected 60-vertex gauge descent; keep the real north-pentagon charge `−5` and the necessary nonzero affine correction. Establish a conditional source-level lift only when all separately identified phase and curvature conditions are met.

**F111+ — higher finite-patch coherence, effectivity and runtime boundary.** After proving genuine semantic inputs, study finite multiple-overlap refinements and higher Čech comparisons (including F47/F55 2-/3-cell source). Show a fully typed global/effective construction only with an explicitly established topology, restriction diagram, descent object and genuine source boundary compatibility. A full global original F42/F54/F55 `(∞,3)` or unrestricted hyperdescent is NOT a current theorem. Runtime integration remains a separate experimental programme.

**Progression / proof authority gate:** **F108 is OPEN**, as are F109–F111+. Existing F103 observed pentagon and F104 finite context Čech do not by themselves establish F108 original-source choice, nor F109 real cross-edge compatibility. Any new theorem must be sourced from an exact merged Lean file, strict CI and axiom receipt; do not promote a proposal to CLOSED merely because its code has been drafted.

## 15. Explicit mathematical and implementation boundaries

- **Original source:** No unconditional equality of arbitrary original F42/F43/F54/F55 witnesses; no claimed restoration of full original Gray phase; no full global faithful raw original 3-category and no unrestricted lifting of the mixed `Δ` into the old F55 constructors. F51 new horizontal/vertical generators are tagged *additions* and must not be presented as historical F43 constructors.
- **Actual physical geometry:** The F69 finite incidence category is not a supplied Grothendieck topology or a physical cover with a complete original `Cat`-valued sheaf. F71's full incidence extension is a **conditional data structure**, not an existence theorem. F106's incidence-star “overlap” is a concrete poset intersection; its semantics is a separate issue.
- **Curvature:** F68 nonzero north-pentagon signed source curvature (second integer charge `−5`) cannot be set to zero by F77/F95 observed NatIso. Even when the global oriented 32-face sum vanishes, local flatness does not follow. Only an explicit, proved nonzero repair may address the associated vertex-potential obstruction in its stated cochain model.
- **Cross-domain models:** 陰陽、五行、四象、三陰三陽・六気、三才、十干・十二支、二十四節気、64卦、河図洛書、内経、王弼・老子などに対応する個別のモデル・歴史的証明は、各Lean宣言と資料ごとに評価します。直ちに宇宙的・臨床的法則や普遍的な圏同値が確立したとは主張しません。
- **AI/runtime:** `LLM + KuuOS reasoning runtime + formal authority layer` は実装・統合の研究目標であり、Leanビルドのみではモデルの重み、ローカル会話、エージェント設定、完全なリポジトリ取り込み、実アプリの正確性、医療安全性や外部操作権限は確証されません。
- **Foundational one-way rule:** `exact DO₂ presentation ⇒ higher stack-localization factorization ⇒ higher localization factorization ⇒ weak W-admissibility` は、古いローカライゼーション定理の条件付き**片方向**の記述です。一般的な逆向き成立を追加しません。

## 16. Engineering workflow, proof audit and reproduction

**正本への変更とCIの手続き：**

1. Fresh `main` SHAと対象ファイルblob SHAを取得し、実際の依存宣言・mathlib API・Leanバージョンを確認する。`main`と古いmemory/文書が違えば実リポジトリを優先する。
2. `leanprover/lean4:v4.30.0-rc2` / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` に固定。Lean 4.31 [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) は **検証専用Draft、マージ禁止**。
3. 依存する原`Quiver.Path`と原F42/F51/F55の型を保ち、F95商圏の相違とF77観測後の同値を区別する。射の単位律・合成律と位相条件を必要に応じて別々に証明する。`sorry`、`admit`、新規の審査されていない`axiom`を使用しない。
4. exact source HEADで`warningAsError=true`、`sorryAsError=true`を指定して変更モジュールとその依存閉包をビルド。主定理の`#print axioms`を検査し、`native_decide`由来の既存公理依存を開示する。CIキャッシュの利用を新しい証明と混同しない。
5. **Strict Lean / Governance / MCP Lean完了証跡 / MCP CI完了証跡** が同じPR source HEADに対してGREENであることを確認してからマージし、事後のcanonical `main`とmerge SHAの一致を再観測する。**docs-only PRのマージは新たなtheorem-bearing SHAではない**。

**Reproduce exact F107 theorem-bearing baseline:**

```bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git
cd KuuOS
git checkout 62f878a739a3288174e8d1b68a754f8d9e239d73
cat lean-toolchain
lake exe cache get  # 必要な場合のみ
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261
```

[Exact F107 PR source CI #38571374255](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38571374255): **completed SUCCESS, 9073/9073**, ten printed axiom lists without `sorryAx`, F107 changed-file diagnostics 0/0 and all governance/MCP receipts SUCCESS. The pinned theorem-bearing merge SHA differs from the exact CI-tested source SHA (`cc8e26d5049b849a403eb76b9878e2a89000cb9f`), as expected for a squash merge.

**Independent broader checks** (not implied by F107 selected-target CI):

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

See [README](README.md) · [GOVERNANCE](GOVERNANCE.md) · [CITATION](CITATION.cff) · [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md).

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Licensed under Apache-2.0.** Proof acceptance, empirical truth, clinical permission and authorization to act are separate questions.
