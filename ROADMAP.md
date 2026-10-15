# KuuOS / 空OS — Formal Roadmap

**2026-10-15 JST / latest VERIFIED theorem-bearing frontier: `v5.281 / F112 part 9`.** [PR #2316](https://github.com/itakura-hidetoshi/KuuOS/pull/2316) **MERGED**; theorem-bearing squash SHA `c1d14ee9746df642dfff102918ec8f6f9e5b1404` independently reobserved equal to canonical `main`, exact tested source HEAD `41c92bacecfbc136e8c0018a9d3ffe4265117681`. [CI #38721458745](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38721458745) **9093/9093 SUCCESS**, changed-file warning/error 0/0, eleven `#print axioms` without `sorryAx`, Strict Lean, Governance and MCP Lean/CI completion receipts all SUCCESS. Prior F112 parts 1–8 through #2314 already exact-head GREEN/MERGED.

**研究の現行方針：** 空を**元の境界型・実物理交差文脈・完全Gray保存量に相対的な表現交代可能性**として使用します。第6段階v5.278はF69/F106実交差証人を保持する任意有限長の物理辺の自由経路圏と原F42/F54/F55混合F47ソースCat値関手・Grothendieck総圏を実装。第7段階v5.279は、元のF69の真正の前向き入射不等式または**形式的逆向き**だけから生成した別のzigzag圏と、実物理交差経路の幾何学的関手を構成。**第8段階v5.280では、交差証人の物理サイトを保存する経路反転と二重反転、連結逆順則、元F69ジグザグの形式的な逆向き操作**を実装しました。証明済みの原F47関手では任意有限経路とその逆の**左右往復が厳密な恒等関手**になりますが、元の自由交差経路そのものの往復は空ではありません。これはF47ソース商圏で完全二整数荷電＋独立ZMod2位相を保持して得た同値で、元のF69逆射、原F42/F54原語の等置、F77位相復元を主張しません。原F55九生成子Δ non-lift、F68北五角形第2荷電`−5`、大域的実効ソースdescent未証明は独立のobstructionとして維持します。

**F112 part 9 / v5.281の厳密な成果：** 本来のF69入射**半順序圏**を変更せず、その全真正入射射についてmathlib Gabriel–Zisman局所化と一意な普遍因子化を構成。真正F69前向き／形式的逆向き射からなる**独立な自由zigzag圏**の局所化への関手を証明し、raw反射的一歩は非空だが局所化後には恒等となることを証明。**別の**証人付きC60物理交差経路圏の局所化を通して、完全なInt×Int荷電と独立ZMod2位相を保存する原F47 Cat値図式が**厳密かつ一意に因子化**することを証明。自由zigzag自体と局所化の圏同値、F69全サイト上の原F47 Cat値図式、F42/F54/F55大域実効三次descentは未証明。F55 Δ non-lift、F110位相非復元、F68北五角形の原曲率`−5`は保持。


この文書では**(a) 現在のLeanで実際に証明済みの定理、(b) 過去に証明されたソース由来の歴史、(c) 追加条件を明示した定理、(d) 未証明の今後の課題、(e) ランタイム・実証研究**を区別します。GitHubのdocumentation-only更新は、Leanの新定理を証明しません。

## 0. Canonical authority / 正本と証跡

| 項目 | 正確な根拠 |
| --- | --- |
| Canonical repository | [`itakura-hidetoshi/KuuOS`](https://github.com/itakura-hidetoshi/KuuOS)、branch `main` |
| Latest verified theorem-bearing merge | [PR #2316 — v5.281 F112 part 9, MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2316) |
| **Theorem-bearing SHA** | **`c1d14ee9746df642dfff102918ec8f6f9e5b1404`**（theorem-bearing squash merge SHA reverified equal to canonical `main`） |
| Exact tested source HEAD | `41c92bacecfbc136e8c0018a9d3ffe4265117681` |
| Exact-head formal CI | [run #38721458745](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38721458745) — completed SUCCESS |
| Strict Lean | Job `116376837328`, **9093/9093 SUCCESS** |
| Governance / MCP completion | All SUCCESS in [run #38721458745](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38721458745) |
| F112 v5.281 source diagnostics | **0 warnings / 0 errors**, **11 `#print axioms`**, no `sorryAx` |
| Toolchain | [`leanprover/lean4:v4.30.0-rc2`](lean-toolchain); [mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`](lake-manifest.json) |
| Separate validation-only lane | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) (Lean 4.31) — **OPEN / DRAFT / UNMERGED**; **do not merge** |
| Copyright and license | 板倉英俊 / Hidetoshi Itakura · [Apache-2.0](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT.md](COPYRIGHT.md) |

**Authority priority:** fresh exact canonical `main` SHA → Lean source declarations and imported formal artifacts → README/ROADMAP verified indices → same exact tested source HEAD CI and completion receipts → historical records. Subsequent docs-only merges may change canonical `main` SHA but not the verified theorem-bearing v5.281 squash SHA `c1d14ee9746df642dfff102918ec8f6f9e5b1404` until a new verified theorem-bearing PR is merged.

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
| **F108 part 1 / v5.262** | Genuine face-generator F42 labels of parity 1, original F51 identity-word physical star functor, and separate F43-derived **nonidentity** F51 interchanger with `charge=(0,0); phase=1` on actual flag triangles, given typed prior/suffix paths. | No canonical context paths from incidence alone; the nonidentity interchanger is not a full-star functor. |
| **F108 part 2 / v5.263** | Construct actual oriented-path reversals and root-to-all 60 original C60 dart paths, hence `Nonempty (Quiver.Path a b)` for any darts; supply F108 prior/suffix from original graph for ALL 90 physical edge charts and derive conservative F95 semantics. | No all-star nontrivial F51 source functor, cross-patch original compatibility or unconditional global physical F55 descent. |
| **F108 part 3 / v5.264** | A two-stratum monotone functor from actual F69/F106 physical incidence stars to Bool walking arrow, then a **native original F51 functor on every star Hom**. True original vertex→edge morphisms map to the genuinely typed F43/F51 nonidentity interchanger, `charge=(0,0), phase=1`, for **all 90 real physical edge stars**. | The two original adjacent face sites share one CHOSEN polygon's two F42 horizontal-pasting terms; independently two-face-typed F42/F55 transport and cross-patch original descent remain open. |
| **F108 part 4 / v5.265** | Both DISTINCT actual adjacent C60 polygon generators in one original typed path pair, with genuine source F51 nonidentity phase-one interchanger on all 90 stars. | Separate original F42 object assignment at each face site remains open. |
| **F109 part 1–2 / v5.266–267** | All real F106 finite patch overlap charges vanish AND all actual F77 observed objects agree for the constructed two-face semantic family; authentic NatIso and strict finite Čech cocycle. | Arbitrary heterogeneous raw F42/F54/F55 source descent and nonzero F68 curvature flattening remain open. |
| **F110 part 1 / v5.268** | Actual two-face original F51 C60 vertex→edge arrows have independent Gray phase ONE but become F77 equality transport. F109 zero-added-charge observed NatIso coexists with F68 physical north curvature second charge `−5`, nonzero curvature map, no uncorrected 60-vertex gauge, and a necessary nonzero physical correction. | No equality of F109 observed 1-cocycle with F68 physical 2-cochain or original F54/F55 global source gluing. |
| **F110 part 2 / v5.269** | F77 projects distinct native phase-one and original identity endomorphisms to the SAME arrow; thus not injective, no complete native ZMod2 phase readout from the F77 quotient Hom and NO functorial left inverse reconstructing all original native Gray morphisms (`c60F77Projection ⋙ lift ≠ 𝟭 GrayGrade`). | Extra original source phase data may still support local lifts; no broad non-existence of every right-side lift. |
| **F111 part 1 / v5.270** | Proof-carrying actual real physical chart indices on a SAME F106 finite incidence-star intersection; Mathlib arbitrary finite history comparison proves exact path independence, normalized identity and inverse, loop identity, naturality, zero ADDED Int×Int charge, concatenation/subdivision and all-ninety-edge specialization. | No global F42/F54/F55 effective descent, physical intersection nonempty guarantee, or original F68 curvature flattening. |
| **F111 part 2 / v5.271** | Genuine `J⊆I` physical overlap refinement `O_I→O_J` preserves F77 observed functors on objects AND all incidence Homs; F109 transition components and arbitrary DIFFERENT histories remain equal after refinement, with zero added integer charge. | This is for one explicit original two-face semantic family; not a global original face-site F42/F54/F55 3-sheaf or raw higher equivalence. |
| **F111 part 3 / v5.272** | Exact geometric double restriction `O_I→O_J→O_K = O_I→O_K` on real F69 physical site objects and all incidence Homs for `K⊆J⊆I`. Source-derived F77 observed double-refinement object equality, comparison NatIso components, two successive genuinely typed arbitrary-history comparisons (independently chosen lengths and intermediates in K,J,I), zero added Int×Int charge, and all-ninety specialization. | Still NOT original F42/F54/F55 effective 3-sheaf descent, a Grothendieck topology or global source curvature cancellation. |
| **F112 part 1 / v5.273** | Proof-indexed arbitrary finite chains of ACTUAL F106 incidence-star restrictions. Their recursively composed physical functor equals the direct endpoint restriction on all sites and Homs; any two finite towers are strictly path-independent and append correctly. Genuine two-face F109 F77 observed functors and Čech history components remain compatible, using heterogeneous Hom equality `HEq` when their types differ definitionally; all 90 actual physical edge cases and zero ADDED Int×Int charge. | Still not a Grothendieck topology, full original F42/F54/F55 effective global source descent, restored Gray phase, or cancellation of original F68 north `−5`. |
| **F112 part 2 / v5.274** | Two independent original F42 face 2-cell slots with ACTUAL separately typed C60 polygon-base boundary loops; all odd-degree choices have honest F43/F51 interchange with native `(charge=(0,0), phase=1)` that is nonidentity before F77 but identity after the intended projection. Separately typed true original F54-rotation-route F55 edge square, physical F68 north second charge `−5`, non-flatness, no uncorrected vertex gauge, F112 arbitrary-tower observed comparison and all 90 original edges are retained simultaneously. | **No** equality of F51 and F55 source 3-Hom types, source-wide effective original F42/F54/F55 global descent, recovery of erased phase, or cancellation of curvature. |
| **F112 part 3 / v5.275** | CONSTRUCTED actual local **mixed F47 four-boundary categorical frame** from independently selected odd-degree original F42 cells at two distinct physical polygon sites and their real connecting C60 paths. Its original face side is a real original F43/F44 arrow, matching the full native prior F51 image; the rotation side is an ACTUAL original F54 route-boundary F55 physical square. Full source-level F47 comparison square COMMUTES, the unique complete-native receiver is `Δ=(0,1;phase 0)`, and no original F55 nine-constructor word can realize that receiver on the same original F54 route endpoints. All ninety physical edges covered. | The bridge arrows are **adjoined F47 constructors**, not ORIGINAL F55 constructors; no equality of F42 and F54 raw source types, no effective global F42/F54/F55 three-descent or curvature flattening. |
| **F112 part 4 / v5.276** | On ONE true physical C60 edge, source change functors across independently original F42 face/path presentations preserve ALL original F47 three-Hom two-integer charges and exchange phase, retain faithful mixed source squares and typed LEFT/RIGHT F42/F54 Beck–Chevalley NatIso; three independent presentations satisfy `HEq` Čech coherence and no original F55 nine-constructor comparison source lift. | Still not an unconditional comparison between DIFFERENT actual physical edges or global original F42/F54/F55 effective source descent. |
| **F112 part 5 / v5.277** | A certificate of TWO DISTINCT physical edges plus a TRUE F69/F106 incidence-star intersection site (original shared dart vertex or original pentagonal/hexagonal polygon face) guards a new local F47 source reindexing functor. Full original F43/F44 and original F54/F55 native equality is **PROVED** across edges; all F47 Hom charge/phase preserved, source faithfulness and original mixed square transport established. A REAL three-edge common F69/F106 incidence site yields triple `HEq` Čech coherence; original F55 comparison non-lift and F68 north second charge `−5` remain. | This is a geometrically guarded LOCAL four-boundary reindexing, not a global F69 incidence diagram/functor, Grothendieck topology or effective original F42/F54/F55 global three-descent. |
| **F112 part 6 / v5.278** | Proof-relevant induction over arbitrary finite sequences of REAL C60 distinct-edge shared F69/F106 vertex/polygon-face sites defines a new witnessed-overlap FREE PATH CATEGORY, with actual identity/associative composition. Its original independently chosen odd F42 face-site cells induce a strictly functorial mixed F47 source Cat-valued diagram, native 2-integer charge plus ZMod2 phase-preserving faithful ALL-Hom transport, and an honest Mathlib Grothendieck TOTAL CATEGORY. Two arbitrary paths between equal endpoints induce identical complete F47 source functors (and therefore HEq on dependent Homs), and arbitrary route splicing agrees with functor composition. | Original F69 poset does NOT have nonidentity edge→edge arrows: a new witnessed path functor preserving original F69 edge locations is explicitly NO-GO when distinct physical edges share a site. This is NOT F69-wide incidence descent, a global raw original F42/F54/F55 3-sheaf, original F55 Delta lifting or F68 curvature flattening. |
| **F112 part 7 / v5.279** | A SECOND, typed FREE ZIGZAG CATEGORY is constructed with site wrappers over ORIGINAL F69 60/90/32 vertex/edge/face cells; original F69 `site ≤ site` relations are arrows forward or deliberately FORMALLY reversed. Each witnessed DISTINCT physical edge pair overlap has an ACTUAL common old F69 site and gives precisely TWO correctly oriented old F69 incidence legs through it; arbitrary proof-carrying overlap paths map functorially to these zigzags, preserving concatenation. The full original F42/F54/F55 F47 Grothendieck total category has a genuine geometric-support functor into this zigzag category. A site-IDENTITY functor from zigzag category back to the ORIGINAL F69 incidence poset is formally impossible once a true distinct-edge overlap is given. | Does NOT turn formal reverse zigzag legs into genuine old F69 arrows, invent an original edge_i→edge_j hom, produce a global F69 incidence action/3-sheaf, flatten F68 signed `−5`, or restore F110/F77-lost phase. |
| **F112 part 8 / v5.280** | An involutive swap of proof-carrying genuine F106/F69 physical overlap sites for **distinct actual C60 edges**, and reverse of arbitrary finite witnessed-overlap free paths, are constructed. Reversal of concatenation and double reversal are PROVED; a separately typed formal reversal exists for the true original-F69-incidence-generated zigzag with raw additive leg count. A nonempty witness path followed by its reverse is **NOT** the empty RAW physical route. On the other hand, fully source-typed original mixed F47 transport functors for EVERY such path and its reverse are strict LEFT and RIGHT inverses; all original F47 Hom identities hold with `HEq`, preserving BOTH integer charges and nontrivial ZMod2 phase without applying F77. | A F47 mixed quotient functor equality does NOT invert old F69 partial-order arrows or identify original F42/F54 syntactic path expressions; original F55 Delta nonlift, F77 lost phase and north F68 curvature -5 persist. |
| **F112 part 9 / v5.281** | TRUE mathlib Gabriel–Zisman localization of ORIGINAL F69 vertex/edge/face incidence poset at its genuine forward arrows: strict universal factorization/uniqueness. True F69 forward inequalities and their formally backwards legs in the distinct FREE zigzag category map functorially to the localization; raw reflexive one-step incidence is nonempty but becomes identity only in the quotient localization. **Separately**, witnessed C60 physical overlap-path category admits localization at all arrows, and its original F47 Cat-valued diagram sends every path to an iso (via proven F114 strict left/right inverses) and factors through this localization **strictly and uniquely**, preserving BOTH integer charges plus independent ZMod2 phase. | No claimed equivalence of the raw zigzag category with old F69 localization, no global original F69 Cat-valued source action, no global F42/F54/F55 effective descent. F55 Δ non-lift, F110 phase non-reconstruction and F68 signed curvature `−5` survive. |

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



## 13. Verified quotient/replaceability programme — v5.213–v5.281

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

### 13.5 F104–F107 CLOSED; F108–F112 part 9 VERIFIED (v5.258–v5.281)

| Stage / exact source | Verified mathematical content | PR |
| --- | --- | --- |
| **F104 / v5.258** — [`DependentOriginationC60KuuFiniteContextCechDescentV5_258.lean`](formal/KUOS/DependentOriginationC60KuuFiniteContextCechDescentV5_258.lean) | `c60F104AtlasTransition_cocycle` and normalized identity/inverse; arbitrary length finite `List (Fin n)` histories compare to direct transition in F77; base cone compatibility; arbitrary natural comparison glues iff its **added** integer charge vanishes. **One fixed original path pair**, arbitrary genuine prefix/suffix contexts. | [#2278](https://github.com/itakura-hidetoshi/KuuOS/pull/2278) |
| **F105 / v5.259** — [`DependentOriginationC60KuuPhysicalOverlapObstructionV5_259.lean`](formal/KUOS/DependentOriginationC60KuuPhysicalOverlapObstructionV5_259.lean) | Different original physical edge patch path pairs; **given** shared overlap category and restrictions, F77 observers, skew and additive charge defect cocycle, conditional `NatIso` iff all Hom defects zero **when observed objects match**; arbitrary finite comparison history; nonzero defect obstruction. `c60F105ObservedGlue_retainsNorthCurvature` keeps original second charge `−5`. | [#2279](https://github.com/itakura-hidetoshi/KuuOS/pull/2279) |
| **F106 / v5.260** — [`DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260.lean`](formal/KUOS/DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260.lean) | `C60F106PhysicalOverlap` of actual F69 physical-incidence stars, restriction `J⊆I : O_I → O_J`, shared actual vertex or polygon face witnesses, `c60F106PhysicalChargeDefect_cocycle` and conditional `c60F106PhysicalTransition_cocycle`. **Singleton-star→F95 semantics is still explicit extra input.** | [#2280](https://github.com/itakura-hidetoshi/KuuOS/pull/2280) |
| **F107 / v5.261** — [`DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261.lean`](formal/KUOS/DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261.lean) | `C60F107OriginalF42Labels` + `C60F107OriginalF51Words` **given** on real physical-star incidence Hom, with `C60F107ChargeCoherence`, yield `c60F107SingletonKuuFunctor` and derived finite-overlap Kuu semantics; replacement iff both integer charges equal. Independent `C60F107PhaseCoherence` yields `c60F107NativeF51Functor` with `c60F107NativeProjection_equalsKuu`. Boundary degree mismatch and nonzero composition-phase defect are **obstructions**, not silently removed. | **[#2281](https://github.com/itakura-hidetoshi/KuuOS/pull/2281)** |
| **F108 part 1 / v5.262** — [`DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262.lean`](formal/KUOS/DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262.lean) | `C60F108FaceContextFamily` with typed **input paths**; concrete contextual original F42 polygon label has face-degree **1**; singleton star local F95/F51 identity-arrow functors constructed. Separately original F43/F51 interchanger has two distinct face-pasting F42 boundaries, original charge `(0,0)` and phase `1`, and a typed original three-arrow on actual F71 flag triangle. **This arrow is not the global star functor assignment.** | [#2283](https://github.com/itakura-hidetoshi/KuuOS/pull/2283) |
| **F108 part 2 / v5.263** — [`DependentOriginationC60KuuAllPhysicalSourcePathsV5_263.lean`](formal/KUOS/DependentOriginationC60KuuAllPhysicalSourcePathsV5_263.lean) | `c60F109EveryDartToDart_nonempty`: REAL original Quiver.Path between ANY original C60 darts via actual north/upper/lower/south physical edges, with reversal of original directed arrows (not raw backtracking identity). `c60F109CanonicalContextExists`, `c60F109AllNinetyF95Semantics`, and `c60F109AllNinetyPhysicalInterchanger_nonzero_phase` eliminate path-existence input and cover all 90 genuine edges. No unconditional original F55 patch gluing. | [#2284](https://github.com/itakura-hidetoshi/KuuOS/pull/2284) |
| **F108 part 3 / v5.264** — [`DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264.lean`](formal/KUOS/DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264.lean) | `c60F108OriginalIncidenceStage_monotone` on the REAL vertex→edge/face F69 order; true `Bool ⥤ C60F51OriginalTwo` walking-arrow functor with original full native F43/F51 interchanger; `c60F108NontrivialPhysicalStarSourceFunctor` and F95 projection on every genuine singleton-star morphism. `c60F108StarActualVertexEdge_nativeComponents`, `c60F108AllNinetyNontrivial_nativePhase` prove original charge `(0,0)` with **phase 1 on every true physical edge endpoint**. Both upper face sites deliberately use the selected face's two F42 proof-relevant horizontal orders; two-face-specific boundaries OPEN. | [#2286](https://github.com/itakura-hidetoshi/KuuOS/pull/2286) |
| **F108 part 4 / v5.265** — [TwoActualFaceInterchange](formal/KUOS/DependentOriginationC60KuuTwoActualFaceInterchangeV5_265.lean) | Both physically DISTINCT incident C60 pentagon/hexagon F42 generators, joined via genuine typed source path; two original horizontal orders, source F43/F51 interchanger charge=(0,0), phase=1; all 90 physical-star F51/F95 functors, both-side flag triangles. Upper face sites still share one combined source object. | [#2288](https://github.com/itakura-hidetoshi/KuuOS/pull/2288) |
| **F109 part 1 / v5.266** — [TwoFacePhysicalOverlapCompatibility](formal/KUOS/DependentOriginationC60KuuTwoFacePhysicalOverlapCompatibilityV5_266.lean) | For this concrete both-face source, EVERY original physical finite-overlap Hom has zero Int×Int charge defect, even though its native source exchange phase may equal one. Both primitive degrees 1 combine to degree 0. | [#2289](https://github.com/itakura-hidetoshi/KuuOS/pull/2289) |
| **F109 part 2 / v5.267** — [TwoFaceObservedObjectCech](formal/KUOS/DependentOriginationC60KuuTwoFaceObservedObjectCechV5_267.lean) | Every F77 observed physical overlap object is the SAME neutral actual quotient grade; both F106 compatibility conditions discharged. Native Mathlib physical-overlap NatIso and STRICT Čech triple cocycle for all 90 edge charts. This is NOT raw original F42/F55 global descent. | [#2290](https://github.com/itakura-hidetoshi/KuuOS/pull/2290) |
| **F110 part 1 / v5.268** — [`DependentOriginationC60KuuObservedGluingOriginalPhaseCurvatureV5_268.lean`](formal/KUOS/DependentOriginationC60KuuObservedGluingOriginalPhaseCurvatureV5_268.lean) | `c60F110ActualFlag_phaseOne_observedIdentity`: true two-face original F51 flag phase1 projects to actual F77 eqToHom; `c60F110ObservedCech_withNonflatPhysicalCurvature` combines real F109 observed NatIso zero ADDED charge with F68 north second charge `−5`, nonzero original signed curvature and required nonzero repair; `c60F110ObservedPhysicalGlue_doesNotSupplyVertexGauge` proves strict observed Čech despite no uncorrected vertex gauge. | [#2292](https://github.com/itakura-hidetoshi/KuuOS/pull/2292) |
| **F110 part 2 / v5.269** — [`DependentOriginationC60KuuPhaseReconstructionObstructionV5_269.lean`](formal/KUOS/DependentOriginationC60KuuPhaseReconstructionObstructionV5_269.lean) | `c60F110UnitNativeExchange_projection_equal_identity` and `c60F110UnitNativeExchange_ne_identity` witness F77 noninjectivity; `c60F110NoCompletePhaseReadout_from_F77` and `c60F110NoFullNativeLeftInverseFunctor` prove no exact recovery of ALL original native Gray phases/functor via intentional F77 projection. `c60F110ActualPhysicalFlag_unrecoverable_phase` connects this to genuine C60 source phase-one flags. | [#2293](https://github.com/itakura-hidetoshi/KuuOS/pull/2293) |
| **F111 part 1 / v5.270** — [`DependentOriginationC60KuuActualPhysicalFiniteCechHistoriesV5_270.lean`](formal/KUOS/DependentOriginationC60KuuActualPhysicalFiniteCechHistoriesV5_270.lean) | `C60F111PhysicalChart I` encodes proof of membership in the actual F106 overlap. `c60F111PhysicalTransitionChain_eq_direct` proves ALL finite histories yield exactly the direct F77 natural transformation; `..._loop` equals genuine identity, `..._charge_zero`, `..._append`, `..._natural` and 90-edge specialization prove robust original source-derived Čech coherence. No arbitrary original F55 source equality. | [#2295](https://github.com/itakura-hidetoshi/KuuOS/pull/2295) |
| **F111 part 2 / v5.271** — [`DependentOriginationC60KuuActualPhysicalRefinementCechV5_271.lean`](formal/KUOS/DependentOriginationC60KuuActualPhysicalRefinementCechV5_271.lean) | `c60F111Refinement_observed_functor` proves actual C60 `O_I→O_J` geometric restriction preserves the entire F77 observed functor (objects and morphisms) under `J⊆I`. `..._transition_app` and `..._anyHistory_app` prove component equality even for two independently chosen finite histories of DIFFERENT lengths and intermediate charts, with exact zero added charge and all-ninety-edge specialization. Uses proof-relevant original physical source and F77 charge-faithful equality; no old F42/F54/F55 global effective lift. | [#2296](https://github.com/itakura-hidetoshi/KuuOS/pull/2296) |
| **F111 part 3 / v5.272** — [`DependentOriginationC60KuuDoublePhysicalRefinementCechV5_272.lean`](formal/KUOS/DependentOriginationC60KuuDoublePhysicalRefinementCechV5_272.lean) | `c60F111PhysicalDoubleRefinement_obj` and `..._map` apply ACTUAL F106 `K⊆J⊆I` composable physical restrictions on real site/Hom. `c60F111PhysicalDoubleRefinement_observed_obj`, `..._transition_app`, `..._anyHistories` certify exact F77-observed double-refinement and TWO individually typed comparisons between independently chosen arbitrary-length histories in K, J and I. `..._historyCharge_zero` and `c60F111AllNinetyPhysicalDoubleRefinement_anyHistories` preserve zero added integer charge on 90 authentic edges. No raw F42/F54/F55 global source glue or north-F68 curvature cancellation. | [#2297](https://github.com/itakura-hidetoshi/KuuOS/pull/2297) |
| **F112 part 1 / v5.273** — [`DependentOriginationC60KuuArbitraryPhysicalRefinementTowersV5_273.lean`](formal/KUOS/DependentOriginationC60KuuArbitraryPhysicalRefinementTowersV5_273.lean) | `C60F112PhysicalTower` is an inductive type of actual physical finite-incidence chart family inclusions, with a recursively composed genuine `c60F112TowerRestrict`, not a postulated endpoint map. `c60F112TowerRestrict_eq_direct`, `..._pathIndependent` and `c60F112TowerAppend_functor` establish strict direct restriction and splicing. `c60F112TowerObserved_functor`, `...Transition_app`, `...AnyHistories_app`, `...TwoTowersAnyHistories_app` and `...HigherCech_cocycle` establish exact F77 observed transport across arbitrary different-length towers and Čech paths; `HEq` is required before proof transport makes the Hom types equal. Charge-zero, F110 no-full-phase-inverse coexistence and all 90 original physical C60 edge specialization. **No original F42/F54/F55 source gluing, phase recovery or F68 `−5` flattening.** | [#2300](https://github.com/itakura-hidetoshi/KuuOS/pull/2300) |
| **F112 part 2 / v5.274** — [`DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274.lean`](formal/KUOS/DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274.lean) | `C60F112IndependentOddFacePair` has TWO independent original F42 labels with each real C60 face base and original non-constant polygon boundary path. The actual F69/F106 physical sites are proved distinct. `c60F112IndependentPairExchangeHom` transports only the second source face with the original C60 bridge and constructs a true typed F43/F51 interchange; `..._components`, `..._native_nonidentity` and `..._F77_identity` certify both zero integer charges and **native phase 1**, strictly nonidentity before F77 and collapsed only afterwards. Source-side F54/F55 original flag-square arrow remains a distinct well-typed object on that same real C60 edge; arbitrary F112 refinement-tower observed agreement coexists with F68 curvature `−5`, nonflatness and no uncorrected gauge. Canonical 90-edge specialization. **No global original F42/F54/F55 source effectivity claimed.** | [#2302](https://github.com/itakura-hidetoshi/KuuOS/pull/2302) |
| **F112 part 3 / v5.275** — [`DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275.lean`](formal/KUOS/DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275.lean) | For arbitrary independently chosen odd-degree ORIGINAL F42 cells at two genuine adjacent C60 polygon sites, `c60F112IndependentFaceOriginalF43` constructs the real raw F43 source exchange on the correct open physical edge Quiver.Path; its full Gray native image matches the preexisting F51 counterpart exactly. **`c60F112IndependentFaceOriginalMixedFrame` actually constructs a fully typed ORIGINAL F42/F54/F55 `C60F47SquareFrame`**, with source F43 face arrow and real original F55 source square on the same physical edge. `c60F112IndependentFaceOriginalMixedSquare` proves the F47 mixed categorical source square commutes; `...Receiver_unique` classifies its calibration `Δ=(0,1;phase 0)`, and `..._noF55Lift` shows NO original F55 nine-constructor source word at its exact ORIGINAL F54 boundaries can realize it. The independent native F51 phase is one and only collapses after F77. All ninety physical C60 edges. **This is local ADJOINED F47 source comparison, not global effective original F42/F54/F55 three-descent.** | [#2304](https://github.com/itakura-hidetoshi/KuuOS/pull/2304) |
| **F112 part 4 / v5.276** — [`DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276.lean`](formal/KUOS/DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276.lean) | `c60F112MixedPhysicalFace_native_eq` and `...Rotation_native_eq` derive the native match for independently old F42 odd site cells and genuinely old F54/F55 source arrows at the same original physical edge. `c60F112MixedPhysicalSourceChange` gives a true F47 source functor, preserving full Int×Int+ZMod2 native data on ALL Hom and source faithfulness; `...ThreeChanges_cocycle` is `HEq` for different dependent Hom types. LEFT/RIGHT real original C60 path and F54/F55 bracket-tree Beck–Chevalley Mathlib NatIso and old F55 no-lift, plus all ninety real-edge specialization. **No cross-physical-edge comparison or global effective source descent asserted.** | [#2306](https://github.com/itakura-hidetoshi/KuuOS/pull/2306) |
| **F112 part 5 / v5.277** — [`DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277.lean`](formal/KUOS/DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277.lean) | `C60F112DistinctEdgeOverlap` carries proof that two original C60 physical edges differ and an actual inhabited `C60F106PhysicalOverlap` at those two true F69 incidence stars. Constructed explicit shared original pentagon/hexagon face or dart vertex; no direct edge→edge incidence morphism exists. Proved original F43/F44 and F54/F55 *complete* native equality for independently old F42 odd source cells even at different physical edges. `c60F112CrossEdgeMixedSourceChange` reindexes the original 4-tag F47 source category ONLY with a physical overlap witness, preserving all Int×Int charges and native ZMod2 phase on every Hom, categorical faithfulness and mixed source-square transport. `c60F112CrossEdgeTriplePhysicalCech` requires an ACTUAL shared F69 site of THREE distinct edge stars and proves triple source comparison as `HEq`. Both old original F55 comparison lifts are obstructed and F68 north second charge `−5` nonzero persists. **No global original F42/F54/F55 effective three-descent or incidence-wide F47 semantic functor.** | [#2308](https://github.com/itakura-hidetoshi/KuuOS/pull/2308) |
| **F112 part 6 / v5.278** — [`DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278.lean`](formal/KUOS/DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278.lean) | `C60F112WitnessedOverlapPath` is an INDUCTIVE, actual F69/F106 intersection-site-witness-preserving sequence of distinct-original-edge steps; `...Append` proves both identity laws and associative concatenation, yielding a real Mathlib `Category` on original C60 edge indices with proof-carrying multi-edge paths. Every edge has independent original F42 odd source cells and actual original F43/F54/F55 four-boundary frame. `c60F112WitnessedF47Transport` recursively composes true guarded cross-edge comparison functors over arbitrary finite paths, retains Int×Int charge and independent ZMod2 phase on ALL mixed F47 Homs, and is faithful. `c60F112WitnessedF47AnyPaths_functor` proves strict F47 functor path independence; its dependent Hom `HEq` requires the correct `Functor.ext` eqToHom boundary conjugation and zero-native equality-cast lemma. `...Transport_append` proves route splicing respects Mathlib functor composition. `...WitnessedF47Diagram` and `...Grothendieck` construct a genuine Cat-valued free witnessed-overlap path diagram and true total category, NOT a diagram over original full F69 incidence category. `...NoIncidenceEdgePreservingFunctor` proves the impossibility of retaining original F69 edge positions under arbitrary cross-edge witness-path morphisms. The original F55 nine-constructor Delta non-lift and signed F68 north physical charge `−5` survive. **No global effective source F42/F54/F55 descent.** | [#2310](https://github.com/itakura-hidetoshi/KuuOS/pull/2310) |
| **F112 part 7 / v5.279** — [`DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279.lean`](formal/KUOS/DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279.lean) | `C60F113IncidenceZigzag` is a proof-relevant finite original F69 incidence arrow path with genuine `site ≤ site` forward generators and FORMALLY inverted reverse generators; a NEW site-wrapper category ensures the original F69 partial order is unchanged. Raw append is associative with identities. `c60F113EdgeToCommonSite` and `...CommonSiteToEdge` turn each ACTUAL F106 common real vertex/edge/pentagon/hexagon site witness into TWO ORIGINAL direction-preserving F69 legs. `c60F113RealOverlapTwoLegZigzag` realizes an actual distinct-edge overlap as that two-leg zigzag, and `c60F113WitnessedToZigzag_append` with `c60F113WitnessedToF69Zigzag` gives a TRUE Mathlib functor from arbitrary REAL witnessed overlap-path category to original-incidence-generated zigzags. `c60F113F47TotalToPhysicalZigzag` pairs the full old F42/F54/F55 source F47 Grothendieck total projection with the new physical geometry, and complete Int×Int plus ZMod2 native phase preservation persists. `c60F113NoOriginalIncidenceProjection` proves no FUNCTOR into original F69 can fix all old sites if a distinct edge overlap is present; reverse old incidence is NOT an old original arrow. No effective original source 3-descent or original F68 curvature flattening asserted. | [#2312](https://github.com/itakura-hidetoshi/KuuOS/pull/2312) |
| **F112 part 8 / v5.280** — [`DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280.lean`](formal/KUOS/DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280.lean) | `c60F114SwapActualOverlap` reverses two distinct genuine C60 edge certificates while preserving the exact original F69 shared physical cell; `...involutive` certifies their original proof-level double reversal. `c60F114ReverseWitnessedPath`, `..._append`, `..._involutive` construct and certify arbitrary finite physical witness path reversal with full original raw site witnesses. `c60F114ReverseF69Zigzag` formally reverses true old forward and deliberately formal backward F69 incidence legs; raw length has additive concatenation. `c60F114RoundTripRawWitnesses_nontrivial` proves a genuine physical witness followed by its reverse is NOT the free empty path. **Nevertheless `c60F114WitnessedF47RoundTrip_rightInverse` and `...leftInverse` prove strict original F47 four-boundary source FUNCTOR identities** in both orders for arbitrary witnessed paths, with Hom-level `HEq` and combined nonempty-raw/identity-F47 certificate. This preserves full original Int×Int charge and independent ZMod2 phase, not the erasing F77 observer. No old F69 reverse Hom is fabricated, no original F42/F54 raw syntax equated; F55 Delta nonlift and F68 north charge `−5` still obstruct unrepaired global descent. | [#2314](https://github.com/itakura-hidetoshi/KuuOS/pull/2314) |
| **F112 part 9 / v5.281** — [`DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281.lean`](formal/KUOS/DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281.lean) | `C60F115OriginalF69Localization` is the honest mathlib localization of the unmodified original F69 site poset at all genuine arrows; `c60F115OriginalF69Localization_universal`, `_factor`, `_unique` prove strict universality. `c60F115F69ZigzagLocalizationFunctor` interprets every genuinely typed forward or formally backwards old incidence leg in that localization without introducing a spurious original F69 backward arrow. `c60F115RawF69IdentityLeg_nonempty` versus `c60F115OriginalF69ReflexiveLeg_localized` separates raw words from localized categorical identity. `c60F115WitnessedToOriginalF69Localization` retains real two-leg C60 geometry. Separately the witnessed C60 physical-overlap category is localized, its original full Int×Int-plus-independent-ZMod2 F47 Cat-valued diagram `...Diagram_inverts` maps every arrow to an iso using verified F114 round trips, and `...OriginalF47Localization_factors` / `_unique` prove strict unique factorization. No equivalence of free raw zigzag with localized F69, F69-wide Cat-valued F47 source, global original F42/F54/F55 effectivity, or F68 curvature repair is claimed. | [#2316](https://github.com/itakura-hidetoshi/KuuOS/pull/2316) |

### 13.6 Exact current logical hierarchy

```text
Genuine physical geometry: 60 vertices / 90 edges / 32 original faces
              |                                 |
       F69 incidence category            F68 physical curvature != 0
              |                            north second charge = -5
       F106 actual incidence stars                  |
              |                                     +--> keep obstruction
       F107 original F42 labels + F51 typed source words (INPUT)
              |
       F108 part 1: contextual physical face F42 labels (degree 1)
              |\--- original F43/F51 interchanger: (0,0; phase 1)
       F108 part 2: typed genuine paths for all 60 darts / 90 edges
              |
       F108 part 3: physical site stages -> Bool walking arrow -> native F51
              |\--- actual vertex->edge arrow: charge (0,0), phase 1
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
F108 face-derived F42 + conservative identity-arrow star functors
              |
F108 part 3 nonidentity NATIVE F51 all-star functors (one chosen polygon)
              |
F108 part 4: BOTH distinct adjacent polygon generators in one typed F42 composite
              |
F109: real finite-overlap observed F77 NatIso + exact strict Cech 1-cocycle
              |
F110 part 1: original F51 phase ONE -> F77 equality transport;
              |           original F68 north curvature -5, repair != 0
F110 part 2: F77 phase quotient NOT faithful; no complete native inverse
              |
F111 part 1: true physical finite-overlap chart histories of ARBITRARY length
              |\--- loop identity, zero ADDED charge, path independence
F111 part 2: true F106 geometric refinement preserves F77 observer functors
              |
F111 part 3: K⊆J⊆I REAL double restrictions and three independent histories
              |\--- ANY pair of different finite histories match on refined sites
              |
F112 part 1: ARBITRARY FINITE physical-restriction towers, not just two steps
              |\--- independently chosen towers and Cech histories agree in F77
              |\--- all 90 actual C60 edges; zero ADDED charge; preserve F110/F68
              |
F112 part 2: INDEPENDENT original F42 sites on two distinct physical faces
              |\--- odd F43/F51 phase 1 retained; F77 image alone becomes identity
              |\--- ORIGINAL F54/F55 separately typed boundary and north curvature -5
              |
F112 part 3: ACTUAL local F47 four-boundary mixed SOURCE square from these faces
              |\--- unique Delta=(0,1;phase 0); NO-LIFT to old nine-generator F55
              |\--- original F43/F44 face Hom and F54/F55 route Hom kept typed
              |
F112 part 4: same-physical-edge mixed F47 source change + full phase Cech
              |\--- LEFT/RIGHT independently typed F42/F54 Beck–Chevalley NatIso
              |
F112 part 5: DISTINCT physical-edge witnessed original incidence overlap
              |\--- shared real C60 face/dart; guarded full-native F47 change
              |\--- real triple F106 intersection + source HEq Cech, F68 -5 persists
              |
F112 part 6: free REAL-overlap witness PATH CATEGORY, arbitrary finite length
              |\--- all-Hom full-native F47 route invariance; strict source functor equality
              |\--- Cat diagram and Grothendieck total; NO original F69 edge path functor
              |
F112 part 7: separate ORIGINAL F69 directed-incidence ZIGZAG path category
              |\--- each REAL two-edge common site → two genuine F69 incidence legs
              |\--- all witness paths map by FUNCTOR to directed F69 zigzags
              |\--- F47 Grothendieck geometry projection; original F69 site-fixing no-go
              |
F112 part 8: reverse actual witnessed C60 overlap paths and formal F69 zigzags
               |
 F112 part 9: TWO distinct actual mathlib localizations (original F69 and witnessed paths)
               |\--- original F69 raw zigzags map into original F69 localization
               |\--- old raw reflexive step nonempty; localized image is identity
               |\--- original F47 full-phase Cat transports invert witnessed routes
               |\--- F47 strict UNIQUE factorization; F68 physical charge -5 remains
              |\--- RAW physical paths retain nonempty backtracks; no old inverse edge Hom
              |\--- original F47 whole-source functors have LEFT/RIGHT identity round trips
              |\--- complete Int×Int and ZMod2 phase retained; F68 north -5 persists
              |
OPEN: independent FACE-SITE F42/F54/F55 source gluing and effectivity
              |
no unconditional global physical F55 glue / hyperdescent
```

For GENERAL heterogeneous physical patches, gluing remains conditional on genuine overlap semantics, observed objects and charge. For the SPECIFIC two-face original F42/F51 source construction, F109 proves real finite F77 Čech isomorphisms; F111 v5.270–272 proves all-length physical chart histories and one-/two-step refinement compatibility, and F112 v5.273 strengthens this to **arbitrary finite chains of true geometric restriction functors, independent tower paths and exact observed F77 higher Čech comparisons** (with `HEq` across propositionally identified Hom types). This does not imply original raw-source effectivity. The general signed overlap charge defect

\[
\omega_{ij}(f)=Q_i(f)-Q_j(f)\in\mathbb Z^2,\qquad
\omega_{ij}(f)+\omega_{jk}(f)=\omega_{ik}(f)
\]

is a genuine signed charge 1-cocycle (additive even when no glue exists). A witness with `\omega_{ij}(f)\ne0` obstructs a zero-added-charge comparison, rather than being “repaired” without authority.

## 14. Active theorem frontier — F112 part 10+ zigzag congruence and curvature-aware higher spans (OPEN)

**F108 — four verified stages, later independently typed F112 source refinement now verified.** F108 original two-face physical F42/F51 source context began as one common horizontal composite for both upper face sites; F112 v5.274–277 has since constructed two independently original F42 face site types and old F43/F54/F55 mixed four-boundary frames, then genuine source F47 reindexing on same edges and on DISTINCT physical edges only when a TRUE F69 overlap is supplied. No identification of original face-base path types, global F69-to-F47 source diagram, or effective original F42/F54/F55 global three-descent is proved.

**F109 — observed finite physical descent VERIFIED for one genuine model.** v5.266 proves zero original integer charge discrepancy on every Hom of true physical F106 overlaps; v5.267 proves all observed F77 objects equal the nested quotient grade zero, giving actual physical NatIso and strict Čech triple cocycle. This holds only for the explicit two-face original F51 semantic family, not arbitrary raw F42/F54/F55 labels; F105/F106 obstructions still govern those.

**F110 — first TWO stages VERIFIED; stronger original F54/F55 source boundary is OPEN.** v5.268 constructs a precise original two-face C60 flag source exchange whose native F51 phase is `1 : ZMod 2`, but whose F77 image is equality transport between the same neutral observed objects. It proves genuine F109 physical finite-overlap NatIso/cocycle with zero ADDED integer charge while F68 original physical north-pentagon curvature has second charge `−5`, the full signed 2-cochain is nonzero, uncorrected vertex gauge descent impossible and canonical physical repair nonzero. v5.269 proves original Gray unit identity and phase-one generator are DISTINCT but the deliberate F77 projection identifies them; no complete phase readout or full native left-inverse functor exists. This does **not** rule out local reconstruction retaining independent original data. OPEN: separately indexed original F42 objects at both original polygon sites, full F54/F55 source-boundary compatibility, real signed-curvature-aware corrected source descent and higher original-source effectivity.

**F111 — THREE STAGES VERIFIED; effective original source descent remains OPEN.** v5.270 constructs the actual C60 proof-carrying physical incidence intersection chart type and true Mathlib F77 natural transformations for all finite histories; every history equals direct F109 `NatIso`, has trivial observed closed holonomy, zero added charge, actual incidence naturality and arbitrary concatenation coherence. v5.271 constructs the genuine F106 `O_I→O_J` restriction for `J⊆I`, proving entire F77 observed functors and all different-length physical histories compatible with it. v5.272 establishes `K⊆J⊆I` double physical restriction compatibility on objects and all Homs, and proves BOTH independently typed K→J and J→I comparisons among arbitrary distinct finite histories, preserving zero added integer charge for all 90 original physical edges. **This remains observed F77 finite physical-intersection coherence**, NOT a new topology, effective raw F42/F54/F55 global three-descent object or restoration of erased Gray phase.

**F112 — NINE stages VERIFIED; effective global original F69-incidence source descent remains OPEN.** v5.273–277 construct genuine F106 C60 intersections, independent original F42 source boundaries, actual F43/F54/F55 mixed F47 source Hom and physically guarded cross-edge changes. v5.278 proves arbitrary finite witnessed physical paths and full-phase F47 Cat diagrams, v5.279 true original-incidence-oriented raw formal zigzags, and v5.280 witness-preserving reverse paths with original-F47 strict left/right inverse transports. **v5.281 constructs the TRUE original F69 localization, a typed free-zigzag-to-localization functor, and a distinct localization of the witnessed physical-overlap path category, through which the original full-phase F47 Cat diagram factors STRICTLY and UNIQUELY.** The needed raw-zigzag congruence/equivalence, genuine higher span/two-simplex comparison, F68-aware source three-descent and effective raw F42/F54/F55 global gluing remain OPEN. Old F55 Δ non-lift, F77 phase erasure and north original curvature charge `−5` are unchanged.

**Progression / proof authority gate:** **F108 parts 1–4, F109 parts 1–2, F110 parts 1–2, F111 parts 1–3, F112 parts 1–9 MERGED/verified Lean.** Next: the universal equivalence of the F69 free zigzag after precisely specified unit/composition/inverse relations with original F69 localization, genuine C60 F69 flag span/two-simplex Beck–Chevalley comparisons, and curvature-aware criteria for original source effectivity. Do not assert literal inverses for original F69 arrows or equality of raw F42/F54 two-cell words from the witnessed F47 factorization; F55 Δ non-lift, F110 lost phase, and signed physical F68 north `−5` persist.

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

**Reproduce exact F112 v5.281 theorem-bearing baseline:**

```bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git
cd KuuOS
git checkout c1d14ee9746df642dfff102918ec8f6f9e5b1404
cat lean-toolchain
lake exe cache get  # 必要な場合のみ
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationC60KuuOriginalIncidenceLocalizationF47FactorizationV5_281
```

[Exact F112 v5.281 PR source CI #38721458745](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38721458745): **9093/9093 SUCCESS**, eleven `#print axioms` with no `sorryAx`, changed-file warning/error 0/0, Strict Lean, Governance and MCP Lean/CI completion receipts SUCCESS. Tested exact source HEAD `41c92bacecfbc136e8c0018a9d3ffe4265117681`, theorem-bearing squash merge SHA `c1d14ee9746df642dfff102918ec8f6f9e5b1404`. Earlier F112 parts 1–8 through [#2314](https://github.com/itakura-hidetoshi/KuuOS/pull/2314) are exact-head GREEN/MERGED.

**Independent broader checks** (not implied by F107 selected-target CI):

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

See [README](README.md) · [GOVERNANCE](GOVERNANCE.md) · [CITATION](CITATION.cff) · [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md).

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Licensed under Apache-2.0.** Proof acceptance, empirical truth, clinical permission and authorization to act are separate questions.
