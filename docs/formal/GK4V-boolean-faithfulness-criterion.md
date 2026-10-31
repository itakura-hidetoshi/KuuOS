# F112-P94D3GK4V — genuine Boolean structural faithfulness criterion and categorical factorization

**2026-10-31 JST** — `itakura-hidetoshi/KuuOS`, canonical `main`.
[Theorem PR #2777](https://github.com/itakura-hidetoshi/KuuOS/pull/2777) **MERGED**.
Theorem squash SHA `77c70548e85aa55d1fb958d9d1a4c8bb40b148a9` independently equaled the exact authoritative `main` HEAD immediately after theorem merge.
Exact final PR source HEAD `c62b8e8194d5b2cf583eb8b21d17e5990938fd59`.
[Exact-source Strict Lean and Governance run #41169230707](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41169230707): **3728/3728 scoped Strict Lean SUCCESS**, **all five Governance jobs and required steps completed SUCCESS**. All **16** new `#print axioms` declarations have dependencies at most `propext`, `Classical.choice`, `Quot.sound`, no `sorryAx`, changed Lean warning/error **0/0**.

## Authoritative mathematical carriers

- [GK4V core Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4VBooleanFaithfulnessCriterion.lean) — eight explicit definitions and theorems, each printed for axioms.
- [GK4V categorical/C60 Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4VBooleanFunctorSectionCriterion.lean) — eight additional declarations and theorems, each printed for axioms.

Both are NEW append-only files, importing compiled GK4U/GK4V and Mathlib.Tactic, not replacements of any existing GK4T/GK4U/H/F54 proof source. The fully original D/E categorical objects, all four Blocks, two Nat depths, actual F45 source/target trees, and genuinely Type-valued F54/P92B proof histories remain distinct. We do NOT change the 107 public roots or introduce Gray.

The three distinct existence-quotient authorities are:

- `Q`: original P92B comparison EXISTENCE quotient of genuine F54 routes, not equality of raw original Type-valued 3-cells;
- `S`: independent GK4E extended F54 structural-comparison existence quotient, assembled into a true Mathlib category by GK4I;
- `K_Bool`: GK4S's SECOND observational quotient of Q by equality of its actual Boolean observations, a separate genuine Boolean kernel category from GK4U.

At every actual typed original F45 boundary, let `F:S→K_Bool` denote the GK4T canonical comparison of GK4U. Define the actual `gradeK:K_Bool→Bool` by `Quotient.lift` on the original P92B Boolean observation. It is well-defined, INJECTIVE, and compatible with witnessed units and GK4U's genuine observed-kernel composition (without any source Q associativity).

Prove for every `u,v:S`:

```text
gradeK (F u) = structuralGrade u
F u = F v  iff  structuralGrade u = structuralGrade v
Injective F  iff  Injective structuralGrade
```

Thus the exact equality-kernel of F is known, and the exact necessary and sufficient condition for **per-Hom** faithfulness is identified. This is NOT a claim that F is either faithful or nonfaithful at all homs.

Construct a TRUE Mathlib Functor `nativeGK4VKernelGradeFunctor` from GK4U's separate Boolean kernel category to GK4I's one-object Boolean category. Its hom map is injective for ALL fully typed F45 boundaries. Its object map and its arrow map composed with `nativeGK4UBoolKernelComparisonFunctor` agree pointwise with GK4I's previously proven `nativeGK4IGradingFunctor`. Source Q's missing identity law is not repaired or assumed.

## Actual C60 north faithful-vs-nonfaithful boundary

GK4F supplies a genuine original 2-edge physical rotation backtrack, and GK4G supplies a genuine zero-edge unit tower. Their independent structural classes are DISTINCT because they have DIFFERENT Boolean grades; GK4G constructs an explicit `Bool→S` section using these two types of routes, and proves `structuralGrade(section b)=b` (a right inverse of grading). It does NOT prove that every genuine structural class is one of those two classes.

GK4V now proves at any real LocalRotation self-Hom:

```text
(∀s:S, section (structuralGrade s) = s)
  iff Injective (structuralGrade:S→Bool).
```

At the actual C60 north F45 triple, the same statement is equivalent to the genuine GK4U structural-to-Boolean-kernel comparison functor's injectivity on that structural self-Hom. The two original Bool values are shown to have DISTINCT actual kernel quotient images, so the functor is nonconstant. Since their grades differ, that explicit pair CANNOT witness nonfaithfulness.

**UNPROVED OBSTRUCTION:** No source proof yet supplies two genuinely DIFFERENT structural classes `u≠v` with `structuralGrade u=structuralGrade v`; nor proves all structural classes are reconstructed by the above two-value section. Therefore the unconditional decision of actual north structural functor faithfulness or nonfaithfulness is NOT justified. The established noninjectivity of the earlier original Q→K_Bool map (GK4S) must NEVER be conflated with the distinct S→K_Bool map.

## CI elaboration repairs and strict exclusions

The initial theorem PR version `e8530d10cc6071bf3164391dca77661a32185ae7` failed in `nativeGK4VKernelGrade_compose`. Lean did not automatically rewrite a raw `Quotient.mk` presented by `Quotient.inductionOn₂` to the explicit `nativeGK4SKernelClass` theorem pattern under `simp only`. Repair: explicitly `change` the post-induction goal to the genuinely typed canonical quotient class projections, then use GK4U's certified composition projection and GK4H's original P92B Boolean multiplication law.

The intermediate source `1a141467ba69227b7c2248143a2b17ea75b748fe` compiled the core theorem, but the physical C60 nonconstant-image theorem failed at `Functor.map` implicit source/target elaboration: the original local rotation's dependent tree cast was not inferred from an unconstrained functor-map Hom binder. Repair: formulate the witness with the exact GK4T Boolean comparison at explicitly typed F45 first/last; this IS the map defined by GK4U's comparison functor on that Hom. The final exact source `c62b8e8194d5b2cf583eb8b21d17e5990938fd59` passed BOTH new files, printed all 16 axioms, had no sorryAx and no changed-source warning/error. The two earlier failing runs do NOT support theorem authority.

Not proved: original P92B associativity or left/right units, alternative original source multiplication, new original P92B Type-valued 3-cell from observed equality, historical full P92B/F19/F28/F54/F55 typed equivalence, unconditional genuine 14D Countable, genuine 19D filler, global strict n or hyperdescent. Strict 空 remains central and independent Kuu is a presentation, no Gray. Append-only/tighten-only/same-root, public roots 107, Lean v4.30.0-rc2 / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Protected #1558 Draft/open/unmerged.

**GK4W proposed (NOT proved):** Construct a new genuine same-grade structurally unequal pair to prove nonfaithfulness, OR prove that the explicit two-valued GK4G section exhausts the entire structural self-Hom to establish faithfulness. These are currently alternative unresolved research directions; do not treat either as demonstrated.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
