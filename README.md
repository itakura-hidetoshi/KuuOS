# KuuOS / 空OS

![KuuOS PR Governance Gate](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/pr-governance-gate.yml/badge.svg)
![Core Governance](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/core_governance_validation.yml/badge.svg)
![KuuOS Runtime Full Check](https://github.com/itakura-hidetoshi/KuuOS/actions/workflows/kuuos_runtime_full_check.yml/badge.svg)

**KuuOS (空OS)** is a research architecture for **dependent origination (縁起), emptiness (空), replaceability of presentations, context-sensitive reasoning, higher categorical composition, exact universal properties, and obstruction-aware descent**. It is both a mathematical formalization project in Lean 4 and a separate research programme for reasoning/runtime integration.

**Founder and copyright holder:** Hidetoshi Itakura / 板倉英俊. **License:** [Apache License 2.0](LICENSE) (`Apache-2.0`); see [NOTICE](NOTICE) and [COPYRIGHT.md](COPYRIGHT.md). Open-source permission does not confer proof, scientific, medical, or execution authority.

> **空 is needed because a description or representative must be replaceable without losing what is structurally justified.** Preservation is proved in a specified quotient and context; it is not an assertion that every raw description is identical.

日本語：KuuOSは、観測や表現を実体視せず、**何を保存したまま表現を交代できるか**を型付きの関手・商圏・自然同型・普遍性で検証する研究体系です。合成・貼り合わせの整合性が成立する範囲を証明し、成立しない原表示に関してはその相違・曲率・障害を残します。

## Current verified formal status / Lean4正本 — v5.253 · F99 · 2026-10-14 JST

| Item | Exact verified authority |
| --- | --- |
| Repository / canonical branch | [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS) / `main` |
| **Latest theorem-bearing PR** | **[#2272: v5.253 F99 — MERGED](https://github.com/itakura-hidetoshi/KuuOS/pull/2272)** |
| **Theorem-bearing merge SHA** | **`07d09c67eea1e49714248535465929da606ac618`** (verified as `main` immediately after merge) |
| Exact tested PR source HEAD | `b8886ed66dd58212c4c5a6c541cb55a5a0452bb5` |
| Exact-head CI | [run #38536067934](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38536067934), **completed SUCCESS** |
| Lean target | `KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253`, **9065/9065** build jobs |
| Strict Lean / governance / MCP receipts | Strict job `115759230335`, governance `115760073452`, MCP Lean `115760073353`, MCP CI `115760132127`: **all SUCCESS** |
| Audit of new module | **12 `#print axioms`**; `sorryAx` absent; changed Lean file warning/error **0/0**. Inherited native `native_decide` axioms for C60 finite geometry are disclosed, not classified as new axioms. |
| Pinned toolchain | [Lean `v4.30.0-rc2`](lean-toolchain); mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` in [`lake-manifest.json`](lake-manifest.json) |
| Separate validation-only lane | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558): Lean 4.31, **OPEN / DRAFT / NOT MERGED**; do not merge into the authoritative lane |

**Important SHA rule:** This is the **last theorem-bearing** merge verified when this documentation was written. A subsequent documentation-only merge will move `main`, without proving a new theorem. Always observe the live canonical HEAD and the exact imported Lean declarations before asserting newer mathematical results. A CI SUCCESS is for the *selected target/dependency closure*, not proof that every repository module or deployed runtime works.

## Core mathematical idea / 空・縁起・交代可能性

Let `Q` be an authentic categorical quotient and let `f,g` be **parallel, correctly source- and target-typed original C60 three-arrows** in F51. The F94/F95 replaceability criterion is:

\[
  f\sim_{\mathrm{kuu}}g
  \quad\Longleftrightarrow\quad Q(f)=Q(g)
  \quad\Longleftrightarrow\quad
  \operatorname{charge}(f)=\operatorname{charge}(g)\in\mathbb Z\times\mathbb Z.
\]

This is **not** an equality of all original raw F42/F43 or F54/F55 words. The two independent integer charge coordinates survive; the independent exchange phase is intentionally forgotten **only after** taking F77's genuine kernel-congruence quotient. Neither the original source's historical Gray data nor its nonzero physical curvature is retroactively set to zero.

F95 makes this a real Mathlib categorical universal property. For each original C60 pair of parallel paths `p,q`, write `\mathcal P(p,q)` for the F51 source three-Hom category and `\mathcal K(p,q)` for its Kuu quotient. Every functor `F` that respects F94-replaceability factors **uniquely**:

\[
  Q_{p,q}:\mathcal P(p,q)\to\mathcal K(p,q),
  \qquad
  F=\overline F\circ Q_{p,q},\qquad \exists!\,\overline F .
\]

The hypothesis “`F` respects replaceability” matters. Universality is **not** unconditional agreement among arbitrary representations, nor is local descent already global geometric gluing.

### C60: actual geometry, distinct raw sources, strict quotient target

- The truncated-icosahedral C60 carrier has **60 actual vertices, 90 physical edges and 32 polygon faces** (**12 pentagons, 20 hexagons**). A physical edge's four vertex/incident-face flags are *incidence data*, **not** a fabricated quadrilateral C60 face. Actual `Quiver.Path` endpoints and original F42 face witness terms remain typed.
- Original F42/F43 faces, original F54/F55 bracket-tree rotation paths, and newly **adjoined** F47 mixed comparisons/F51 source generators are distinct constructions. Do not silently equate different raw source types.
- F55's original signed north-pentagon curvature is **nonzero**, and the calibration `Δ=(0,1;0)` is an adjoined mixed comparison not produced by its original nine constructors. The relevant north mixed comparison has second integer charge **−5**. Global oriented face-sum cancellation does not establish local flatness.
- The F75–F83 *new phase-forgetting quotient* supports strict middle-four and monoidal coherence on its stated graded/quotient carriers. F78's four-level globular certificate preserves real C60 0/1-paths while its 2-cell carrier is **grade-completed**; it does not claim a globally faithful unquotiented original F42/F54/F55 strict or Gray 3-category.

### Proof milestones / 現在の定理階層

| Versions / PRs | What Lean actually proves |
| --- | --- |
| **v4.00–v5.101** | Presentation-sensitive obstructions/exact localization, original actual `F/G/η/ε` and *separately proved* forward and reverse swallowtails; the F5 coherent biadjunction carrier in [v5.101](formal/KUOS/DependentOriginationCoherentBiadjunctionActualLiftV5_101.lean). |
| **v5.102–v5.154** | Native adjunction/mates, independent F19/F28 histories, finite multi-axis interchanges and chosen-mate normal forms; F45/F54 rotation paths and independent F55 three-cell presentation. |
| **v5.155–v5.212** | Real C60 incidence/cochain and physical obstructions, F42/F43 and F54/F55 source-aware constructions; conditional F47 mixed comparisons, genuinely typed source Hom and earlier Beck–Chevalley higher pasting. These remain historical theorems and do not require restoring Gray. |
| **v5.213–v5.228** | Finite C60 atlases and Čech/categorical nerve/face-choice developments, curved/descent conditions, graded original-source interchanger; see [ROADMAP](ROADMAP.md) for the verified local/conditional scope. |
| **v5.229–v5.233 · [#2248–#2252](https://github.com/itakura-hidetoshi/KuuOS/pull/2248)** | **F75–F79**: explicit strict charge target, original-source phase-forgetting relation, genuine Mathlib `CategoryTheory.Quotient`, real C60 path-indexed globular certificate, equivalence of the quotient and charge groupoid. |
| **v5.234–v5.239 · [#2253–#2258](https://github.com/itakura-hidetoshi/KuuOS/pull/2253)** | **F80–F85**: horizontal product of genuine quotient Hom classes (independent of representatives), middle-four, transported and direct `MonoidalCategory` coherence and monoidal equivalence. |
| **v5.240–v5.247 · [#2259–#2266](https://github.com/itakura-hidetoshi/KuuOS/pull/2259)** | **F86–F93**: independently constructed comparison tensorators, exact charge-obstruction classification, explicit phase-zero section, selected inverse gauge, coboundary calculation, and F93's proved **tensorator equality**. No unjustified assumption that the selected gauge is zero. |
| **v5.248 / F94 · [#2267](https://github.com/itakura-hidetoshi/KuuOS/pull/2267)** | Original F51 source three-arrow **replaceability iff both integer charges agree**; stability under categorical/2-context horizontal composition and connection to F78/F93. |
| **v5.249 / F95 · [#2268](https://github.com/itakura-hidetoshi/KuuOS/pull/2268)** | **Local universal quotient** of every actual C60 path-indexed F51 three-Hom: exact kernel, real Mathlib congruence/quotient, unique factorization into arbitrary target categories for replaceability-respecting functors. |
| **v5.250 / F96 · [#2269](https://github.com/itakura-hidetoshi/KuuOS/pull/2269)** | Genuine **horizontal bifunctor** on two F95 local Kuu quotient categories, unit/middle-four, agreement with F80. |
| **v5.251 / F97 · [#2270](https://github.com/itakura-hidetoshi/KuuOS/pull/2270)** | Genuine **vertical 2-context bifunctor** on local Kuu quotients, unit/middle-four, agreement with F77/F78. |
| **v5.252 / F98 · [#2271](https://github.com/itakura-hidetoshi/KuuOS/pull/2271)** | Four independently indexed local quotient inputs: horizontal-after-vertical versus vertical-after-horizontal yield a genuine **Mathlib `NatIso` after F77 observation**; comparison adds zero integer charge. Distinct raw F42 output objects are *not* identified. |
| **v5.253 / F99 · [#2272](https://github.com/itakura-hidetoshi/KuuOS/pull/2272)** | Real LEFT/RIGHT C60 path whiskering **descends to local Kuu quotient functors** through F95 universality. Both resulting F77 observation comparisons are genuine natural isomorphisms of **zero additional charge**, for arbitrary typed quotient morphisms. |

The F94–F99 proof-bearing files, in increasing order, are:

- [F94: replaceability](formal/KUOS/DependentOriginationC60KuuReplacementInterchangeV5_248.lean)
- [F95: universal local quotient](formal/KUOS/DependentOriginationC60KuuLocalUniversalDescentV5_249.lean)
- [F96: horizontal bifunctor](formal/KUOS/DependentOriginationC60KuuLocalHorizontalFunctorV5_250.lean)
- [F97: vertical bifunctor](formal/KUOS/DependentOriginationC60KuuLocalVerticalFunctorV5_251.lean)
- [F98: mixed observable NatIso](formal/KUOS/DependentOriginationC60KuuObservedMixedInterchangeV5_252.lean)
- [F99: path-context whiskering descent](formal/KUOS/DependentOriginationC60KuuContextWhiskeringDescentV5_253.lean)

## Reasoning architecture / LLMへの接続は別途検証

The intended reasoning discipline is:

```text
observation -> local presentation(s) -> alternative compatible inferences
            -> typed transport/whiskering -> comparison (2-/3-cells)
            -> descent test
                 coherent: glue (only within proved assumptions)
                 not coherent: retain obstruction and provenance
                 inadequate authority: re-observe / abstain
```

The proposed application stack is **LLM + KuuOS reasoning runtime + formal authority layer**. The Lean repository is a versioned authority for *specified formal mathematics*, not proof that model weights have changed, that an app has loaded the whole repository, or that all generated answers/real-world actions are correct. The actual runtime, consent boundaries, retrieval/composition with pinned artifacts and end-to-end tests are independent engineering obligations.

## Reproduce the current formal result / 正本の再検証

The following is the exact **theorem-bearing** baseline, not a later documentation-only `main` merge:

```bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git
cd KuuOS
git checkout 07d09c67eea1e49714248535465929da606ac618
cat lean-toolchain
lake exe cache get   # needed when pinned Mathlib cache is not already present
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253
```

The selected v5.253 exact-head [CI #38536067934](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38536067934) successfully compiled **9065/9065** dependency jobs; the final changed file had **zero warning/error** and its twelve printed axiom dependencies contained **no `sorryAx`**. Some inherited C60 finite-geometry results rely on Lean-generated `native_decide` axioms; disclose them when making foundational claims.

Independently, the broader repository target and runtime smoke test may be run as separate checks (their success is **not implied** by the selected CI):

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

## Active frontier / 次の証明と実装

1. **F100 — two-sided path-context coherence**: compare applying actual left and right whiskering in both orders, with genuine dependent C60 path casts, functor/natural-isomorphism coherence and zero *additional* `Int × Int` charge **after appropriate F77 observation**.
2. **F101+ — contextual mixed interchange / finite-patch gluing**: connect F98's four-input observed exchange with F99/F100 contextual actions; construct finite atlas comparisons with exact path/source indices. Preserve meaningful F55 signed-curvature and Δ non-lift obstructions instead of assuming unconditional flatness.
3. **Formal/runtime boundary**: make any claimed interactive reasoning integration reproduce the pinned Lean authorities, justify context transport and preserve rejection/obstruction states; evaluate empirically before claiming deployed behavior.

**Explicit non-goal:** **do not restore original Gray merely for its own sake**. The original Gray work remains a historical/source diagnostic; the current constructive route is the **Kuu quotient's representation replaceability, its exact universal property, and compositional coherence**. A full raw F42/F54/F55 equivalence, unrestricted global higher descent, infinite-depth convergence and runtime correctness are **not** established by the present theorems.

Further evidence: [ROADMAP](ROADMAP.md) · [GOVERNANCE](GOVERNANCE.md) · [CITATION](CITATION.cff) · [LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md).

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Licensed under Apache-2.0.**
