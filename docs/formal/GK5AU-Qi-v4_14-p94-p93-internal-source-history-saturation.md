# F112-P94D3GK5AU / Qi v4.14 — 全P94A/P93C構成子の真正内部 source-history と北C60の降下境界

**Formal proof record / 2026-11-03 JST.** Repository: \`itakura-hidetoshi/KuuOS\`. Canonical theorem branch \`main\`; direction of authority **independent Kuu → Qi**. Strict 空 is NOT identified with a selected proof presentation, its raw Type-valued witness, a quotient/shadow, a numerical C60 label, or a physical gauge frame.

GK5AT/Qi v4.13 was completed by PRs #3007–#3009; GK5AU and Qi v4.14 extend its **actual selected P94A two-stage intermediate source-image gate** to recursively inspected full P94A/P93C proof-term histories. All original F54 two-Nat typed route histories, F55/P89/P92B/P93C/P94A declarations, and existing theorem statements are preserved. Only new Lean modules, additive public imports and this documentation were introduced. Public root **107** is maintained, and protected PR **#1558 Draft/OPEN/unmerged** remains separate.

## 1. Immutable verification record

| Item | Exact verified evidence |
| --- | --- |
| GK5AU independent theorem PR | [#3010](https://github.com/itakura-hidetoshi/KuuOS/pull/3010), MERGED |
| GK5AU final exact-source HEAD | \`9fe7562a408e51fd2def120f188b237ac94ecaf4\` |
| GK5AU squash/main commit | \`01ebcca7ef6e68228194f8161498814c036a55d2\` |
| GK5AU CI | [Governance #41574525281](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41574525281), **30/30 SUCCESS** |
| GK5AU Strict Lean | **9246 / 9246 jobs built successfully** |
| GK5AU \`#print axioms\` | **13 entries**; only standard \`propext\`, \`Classical.choice\`, \`Quot.sound\`, or none |
| Qi v4.14 north physical integration PR | [#3011](https://github.com/itakura-hidetoshi/KuuOS/pull/3011), MERGED |
| Qi final exact-source HEAD | \`378bc6ddd7703b6ec1b4b12ae3acb7419ba7320d\` |
| Qi squash/main commit | \`9fb56f1ca945dafb5b4fd89153108da1bca15dfe\` |
| Qi CI | [Governance #41575239368](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41575239368), **30/30 SUCCESS** |
| Qi Strict Lean | **10173 / 10173 jobs built successfully** |
| Qi \`#print axioms\` | **3 entries**; standard allowable axioms only |

Exact-source Lean output has **no sorryAx**, no new logical axioms, no failed changed-file compiler lines/warnings. The initial failed GK5AU intermediate revisions were fixed BEFORE the green exact-source HEAD; only the final green source is merged. Pinned Lean: **v4.30.0-rc2**. Pinned mathlib: **5450b53e5ddc75d46418fabb605edbf36bd0beb6**.

## 2. The precise typed source-image boundary

Let \`φ = nativeGK5AIOriginalToP92Structural\`, a genuine dependent, nine-constructor structural map from original F55 Type-valued 3-proof terms to selected P92B Type-valued 3-proof terms. It is NOT a quotient-class map or signed shadow.

For a selected proof term \`q : P92B(p,r,s)\` at its *exact original F54 typed endpoints*, GK5AT defines

\`\`\`text
PhiImage(q) := ∃ m : OriginalF55(p,r,s), φ(m) = q
PhiFiber(q) := {m : OriginalF55(p,r,s) // φ(m) = q}
PhiImage(q) ↔ Nonempty (PhiFiber(q)).
\`\`\`

Crucially, a historical P93C \`.old\` node is not automatically claimed to have raw endpoints equal to the recursive φ-image of its original F55 arguments. The old P93C constructor indexes \`P92B.original\` terms, whereas \`φ\` *recursively* translates original F55 constructors. Keeping that distinction prevents an invalid reflection.

## 3. All P93C **16** and P94A **19** constructors inspected

Two new structurally recursive, *proof-history-sensitive* predicates are defined:

\`\`\`text
nativeGK5AUP93CSourceHole : P93C(f,g) → Prop
nativeGK5AUP94SourceHole : P94A(f,g) → Prop
nativeGK5AUP94SourceSaturated(w) := ¬ nativeGK5AUP94SourceHole(w)
\`\`\`

For each actual four-proof term, its exact P92B endpoints are examined. Its recursive child four-proofs and any separately supplied P92B proof arguments are then checked.

**All 16 P93C constructors:** \`old\`, \`refl\`, \`symm\`, \`trans\`, \`verticalLeftUnit\`, \`verticalRightUnit\`, \`verticalAssoc\`, \`leftWhisker\`, \`rightWhisker\`, \`leftContext\`, \`rightContext\`, \`precompose\`, \`postcompose\`, \`horizontalLeft\`, \`horizontalRight\`, \`interchange\`.

**All 19 P94A constructors:** the same sixteen forms, plus \`horizontalUnit\`, \`leftContextUnit\`, and \`rightContextUnit\`. The P94A \`.old\` case opens the REAL embedded P93C source history, rather than merely checking outer P94A endpoints.

A **source hole** is an actual raw typed P92B witness in that particular proof history with no original F55 φ-preimage. This is strictly a source-saturation obstruction; it is *not* itself a proof of original P89 nonreflection or P89→P94A noninjectivity. Conversely, source saturation does not alone prove that a selected four-proof globally reflects to original P89: independently chosen P93C/P94A generators can still require four-dimensional reflection arguments.

The new theorems include:
- \`nativeGK5AUP93C_hole_embeds\`: a real P93C hole remains visible in P94A \`.old\`.
- \`nativeGK5AUP94_hole_of_missing_left/right\`: lack of an original source at either actual typed outer endpoint is necessarily a source hole.
- \`nativeGK5AUP94_saturated_endpoint_images\`: saturation implies both endpoints genuinely in φ-image.
- \`nativeGK5AU_clean_trans_middle_fiber\`: a saturated REAL \`.trans left right\` yields a genuine original dependent φ-fiber over the exact intermediate P92B proof.
- \`nativeGK5AU_trans_nonimage_middle_hole\`: source-nonimage of the actual trans midpoint forces an internal hole.

## 4. Conditional P89 descent and exact remaining obstruction

Take actual original F55 proof terms \`f,g\` and a true selected P94A two-stage comparison

\`\`\`text
left  : P94A(φ(f), q)
right : P94A(q, φ(g))
w     : P94A(φ(f), φ(g)) := trans left right.
\`\`\`

Under the theorem's explicitly supplied hypothesis \`SourceSaturated(w)\`, the genuine \`q\` has an original dependent preimage \`m\`. Applying GK5AT's earlier exact two-stage gate yields

\`\`\`text
Nonempty (P89(f,g))
OR
∃ (m : OriginalF55), φ(m) = q ∧
    (GK5AQBadPair(f,m) OR GK5AQBadPair(m,g)).
\`\`\`

This is \`nativeGK5AU_clean_trans_reflect_or_local_bad\`. If every original \`m\` over \`q\` avoids both authentic local BadPairs, \`nativeGK5AU_clean_trans_descends\` constructs \`Nonempty(P89(f,g))\`.

No arbitrary selected 19-constructor proof normalization into a GK5AS source-vertex chain has been assumed or proved. The theorem is **conditional on the supplied selected trans, its actual recursively audited saturation, and the exact local reflection gate**. It distinguishes: (1) a P92B source hole; (2) an original-F55-typed genuine four-cell nonreflection BadPair; (3) true original P89 descent. Shadow/left-right parity equality cannot replace any of these hypotheses.

## 5. Concrete nested P93C-in-P94A counterexample to parity-based recovery

For the real north C60 first-three-F45-unit stages, GK5AI's new selected P92B \`assocNaturality\` witness \`q_N\` exists but has no original F55 preimage. GK5AU constructs an actual P94A four-proof term *embedding a P93C proof*:

\`\`\`text
w_N := P94A.old (P93C.refl q_N) : P94A(q_N, q_N)
¬ PhiImage(q_N)
P94SourceHole(w_N)
(leftCount(w_N), rightCount(w_N)) mod 2 = (0, 0).
\`\`\`

This explicitly locates missing original source evidence **inside the P93C proof history under the P94A old wrapper**. GK5AT already had an explicit double-reflexive \`P94A.trans\` midpoint; GK5AU strengthens the structural location to nested P93C.

This example is NOT an original GK5AQ BadPair: the corresponding original F55 proof slot is empty, so no two original F55 witnesses for a noninjectivity assertion exist.

## 6. Qi v4.14 original north C60 physical integration

Qi's new additive Lean module proves three theorems:
1. \`fivefoldGK5AUNorthCleanTwoStep_reflect_or_localBad\`: specialize the source-saturated trans dichotomy to the ORIGINAL north four-stage F54/F55 long/short pentagon with all original indices retained.
2. \`fivefoldGK5AUNorthCleanTwoStep_descends\`: derive a genuine original north P89 witness if the actual source-saturated midpoint has no local original BadPair.
3. \`fivefoldGK5AUNorthNestedPhysicalSourceGate\`: simultaneously maintain the nested P93C-in-P94A source hole with left/right parity \`(0,0)\`; true north physical fifth Dart closure; the exact physical-versus-categorical 04/43 direction inequalities; and Qi v4.10's still **conditional** physical P94A noninjectivity iff original source reflection obstruction.

The physical gauge frame supplies neither the missing F55 witness nor an unconditional source BadPair. Independent Kuu remains theorem authority; Qi specializes it to a genuine, finite north C60 physical presentation.

## 7. Lean4 error diagnosis and exact-source correction trail

The first GK5AU CI revision failed: recursive calls to \`SourceHole inner\` were implicitly instantiated at the *parent* P93C/P94A indices, while child proofs (\`symm\`, \`trans\`, whiskers, contexts, horizontal etc.) genuinely have different dependent endpoints. **Correction:** explicitly quantify \`p\`, categorical blocks, F45 source/target trees and two-Nat depths, \`r,s,f,g\` for EACH recursive predicate, so child calls infer their own indices. This eliminated the dependent-type recursion mismatch errors.

The second revision reduced the remaining diagnostics to four goals. At a variable proof \`w\`, Lean4 cannot reduce the recursive \`match w\` definition to a visible \`Or\` disjunction, so directly supplying \`Or.inl\` / \`Or.inr\` was not accepted. **Correction:** derive endpoint-source-hole helper lemmas by genuine \`cases w\` over all 19 constructors and \`simp\` on each resulting branch; reuse those helpers in trans/endpoint lemmas. This resolves the *structural* reason for the elaboration failure rather than weakening theorem hypotheses or adding assumptions.

The final **third** GK5AU source revision and the independent Qi integration are both green under the fixed Lean/mathlib toolchain. The final axiom audits show **no sorryAx**. Original Lean files/import authority and historical theorem statements were never rewritten.

## 8. Next exact research boundary — GK5AV (provisional)

GK5AU identifies the genuinely source-saturated internal proof histories and resolves the two-step local reflection boundary. It does **not** construct an unconditional decomposition of EVERY P94A four-proof into local original-source-vertex comparisons, nor a universal normalization of P93C generator histories. The next useful theorem would give an **explicit constructor-wise sufficient condition** for building an original F55 source-vertex chain from a selected P94A proof, identify which P93C unit/interchange generators require independent original P89 lifts, and state a necessary/sufficient *conditional* descent gate with exact obstructions. Never equate absence of φ-holes with unconditional P89 reflection and never infer noninjectivity without a true source-typed GK5AQ BadPair.

**Sources:** [GK5AU Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AUP94FullInternalSourceHistory.lean), [Qi v4.14 Lean](../../formal/KUOS/Architecture/QiWuxingGK5AUNorthNestedSourceHistoryV4_14.lean), [GK5AT/Qi v4.13 proof record](GK5AT-Qi-v4_13-internal-phi-image-north-physical-descent.md), [GK5AS/Qi v4.12 proof record](GK5AS-Qi-v4_12-source-vertex-localization-zero-grade-no-descent.md).
