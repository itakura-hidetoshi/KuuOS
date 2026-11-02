# F112-P94D3GK5AB — Two-stage index composition for five genuinely independent recursive Φ

**Date:** 2026-11-02 JST  
**Canonical theorem repository:** `itakura-hidetoshi/KuuOS`, `main`  
**Theorem PR:** [#2953](https://github.com/itakura-hidetoshi/KuuOS/pull/2953) — **MERGED**  
**Final exact-source HEAD:** `678c34881fe6e3c0bef52a1866d4d10f81a9557e`  
**Theorem squash SHA / canonical main after merge:** `d47347cdc571f68a9853cc0559de651451602c66`  
**Exact-source Git tree = merged Git tree:** `562bd210549f9feb1daef27c08eae32110d378e1`  
**Lean source blob (identical on exact source and merged main):** `7ed1cf73a8e81a724fee90a6b193f0a84e9ac84e`  
**Final exact-source CI:** [#41425340984](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41425340984) — **terminal SUCCESS**, Strict Lean **3849/3849**.

## Statement and real equality transports

Fix arbitrary index maps `f : I → J` and `g : J → K` (both may be **noninjective**), five indexed true Mathlib categories `C,D,E,F,G : K → Cat.{vC,uC}`, and four genuine indexed Mathlib equivalences `e₁,e₂,e₃,e₄`. None of their chosen inverses, units, counits, or compositors are strictified. Fix an arbitrary **finite, heterogeneously typed** GK5D tree `t` over the pullback family `C ∘ g ∘ f`; unit, atom, paste are all included.

The already proved GK5F identity and composition for genuine typed-tree reindexing provide

```lean
nativeGK5FTreeReindex_comp f g C t :
  nativeGK5FTreeReindex g C
    (nativeGK5FTreeReindex f (fun j => C (g j)) t) =
  nativeGK5FTreeReindex (fun i => g (f i)) C t
```

GK5AB proves the **whole NatIso cocycle** for GK5Z's true fourfold source comparison, not merely the existence of an isomorphism:

```lean
nativeGK5ABSourceIso_comp_whole
```

Its two source transports compose with `eqToIso` of the real GK5F fusion equality to yield `nativeGK5ZSourceIso (g ∘ f) ... t`. The proof uses `eqToIso_trans` and type-correct equality proof irrelevance, without equating distinct typed-tree index universes.

For any independently constructed whole witness on the K-indexed tree, GK5AB proves a genuine source/target square under the GK5F fusion certificate:

```lean
nativeGK5ABPhi_tree_transport
nativeGK5ABTwoStagePhi_comp_whole
```

Crucially, the mathematical composition problem is not resolved by defining the I-indexed `Φ` as a transported J-indexed `Φ`. GK5AA instead separately recursively constructed all five I- and J-indexed direct witnesses, and GK5AB composes their **two genuine naturality squares** with source/target `eqToIso` boundaries.

## All five independent direct recursive Φ comparisons

For each of the **five actual** Mathlib `Equivalence.trans` parenthesizations `P0..P4`, the proof distinguishes:

1. `nativeGK5XDirectPhiq` independently constructed over the original I pullback family;
2. `nativeGK5XDirectPhiq` independently constructed over J and transported along the first source/target equality;
3. the independently constructed K witness at `g_*(f_*t)`;
4. the K witness at `(g ∘ f)_*t`, linked by the real typed-tree equality and `eqToIso`.

These are formalized by two families of **genuine whole NatIso equalities**:

```lean
nativeGK5ABFourDirectPhi0_indexComp_whole
nativeGK5ABFourDirectPhi1_indexComp_whole
nativeGK5ABFourDirectPhi2_indexComp_whole
nativeGK5ABFourDirectPhi3_indexComp_whole
nativeGK5ABFourDirectPhi4_indexComp_whole

nativeGK5ABFourDirectPhi0_recursiveComp_whole
nativeGK5ABFourDirectPhi1_recursiveComp_whole
nativeGK5ABFourDirectPhi2_recursiveComp_whole
nativeGK5ABFourDirectPhi3_recursiveComp_whole
nativeGK5ABFourDirectPhi4_recursiveComp_whole
```

The first family establishes coherence of **transported** whole direct witnesses. The second family is stronger: it applies GK5AA's `nativeGK5AAFourDirectPhi0..4_reindex_whole` twice, composes the squares by `nativeGK5ABComposeSquares` with explicit `Iso.trans_assoc`, and then uses the first family to establish path independence of the **I/J independently recursively constructed** witnesses.

In schematic form (omitting only the displayed equality proofs for readability),

```text
Phi^I_q(t) ≪≫ eqToIso(T_f) ≪≫ eqToIso(T_g) ≪≫ eqToIso(T_fusion)
  =
SourceIso_(g ∘ f)(t) ≪≫ Phi^K_q((g ∘ f)_*t),
q ∈ {0,1,2,3,4}.
```

There are no injectivity assumptions on `f` or `g`; there is no assertion that whole Mathlib equivalence **records** become strictly equal or that the original higher Type-valued source evidence is recovered.

## Full-file Lean diagnosis and pinned mathlib

The only theorem change was a new **512-line-content + trailing newline (513 line-split entries)** file, [PolygonNativeC60AQFullPentagonPhysicalNativeGK5ABTwoStageIndexPhiCoherence.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5ABTwoStageIndexPhiCoherence.lean). All dependent theorem files were retained. Full-source examination included GK5D, GK5F, GK5G, GK5P, GK5X, GK5Z, GK5AA and their relevant true Mathlib `Iso.trans_assoc` / `eqToIso_trans` operations.

Initial [CI #41424823654](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41424823654) reported a single Lean error, `No goals to be solved` at original line 60. This arose because `simp only [nativeGK5ZSourceIso, eqToIso_trans]` had **already closed** the equality goal; the following `exact congrArg eqToIso (Subsingleton.elim _ _)` was redundant, rather than evidence of a missing coercion or weakened theorem. The surplus tactic was removed. The file was simultaneously extended to the five independent recursive composition squares. The corrected exact-source file compiled successfully at the original fixed pins.

**Final [CI #41425340984](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41425340984):**

- Strict Lean **3849/3849 SUCCESS**; new file rebuilt on the exact PR commit.
- Public `#print axioms` **12/12**: each depends only on `propext`, `Classical.choice`, `Quot.sound`; **no `sorryAx`**.
- Changed-file Lean errors / warnings: **0 / 0**.
- Independent Kuu foundation/API, workflow integrity and governance: **terminal SUCCESS**.
- Exact-source and merged main Git **tree SHA identical**; GK5AB Lean **blob SHA identical**.

## Authority boundaries and next research

One canonical theorem-bearing `main`, one public `KuuOSFormal` aggregate and 107 retained public roots. Lean **v4.30.0-rc2**, mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**, append-only/tighten-only/overwrite-forbidden, strict 空 centered; independent Kuu remains one presentation. Protected validation-only PR **#1558 remains Draft/open/unmerged**.

The theorem is about fixed-universe true Mathlib categories and **finite GK5D typed trees**. It does not give arbitrary hyperdescent, Gray reconstruction, source-Q equivalence, unconditional source faithfulness, or an identity of the distinct raw F54/F55/P92B higher evidence.

**Next F112-P94D3GK5AC:** explicitly promote the already proven GK5F reindex identity together with GK5AA/GK5AB whole NatIso naturality into coherent identity-and-composition reclassification action, and test compatibility with the Qi v3.5 common FivePhase interface without identifying physical C60 edges and categorical NatIsos by mere cardinality.
