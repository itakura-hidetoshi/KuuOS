# F112-P94D3GK4U — compositional observer kernel comparison and true Boolean functor

**2026-10-31 JST.** Repository `itakura-hidetoshi/KuuOS`, authoritative branch `main`.
[Theorem PR #2775](https://github.com/itakura-hidetoshi/KuuOS/pull/2775) **MERGED**.
Theorem squash SHA `cee82f700c0040c179bacc7b586c6abfa8e3f806` equals canonical main HEAD immediately after theorem merge.
Exact final PR source HEAD: `a55d680488c5c9ac277fa9c5517eb821e845ea72`.
[Exact-source Strict Lean/Governance CI #41167812738](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41167812738):
**3726/3726 scoped Lean build SUCCESS**, **5/5 Governance jobs completed SUCCESS**. All **19** new declarations explicitly inspected by `#print axioms`; only `propext`, `Classical.choice`, and `Quot.sound` where present; **no `sorryAx`**, changed Lean warning/error **0/0**.

## Genuine typed theorem-carrier

[GK4U Lean source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4UCompositionalKernelFunctor.lean) is one new append-only F112 file, importing exact compiled GK4T plus `Mathlib.Tactic`. Original D/E categories, all four original Blocks, both Nat depth axes, true original F45 stages and original Type-valued witness histories are retained.

Distinguish THREE different authorities at every actual F45 source and target:

- `Q` — actual ORIGINAL P92B Type-valued comparison-existence quotient; `nativeGK4H_p92Compose` exists, but no source associativity/identity is assumed or proved.
- `S` — separately extended GK4E structural comparison-existence quotient; `nativeGK4H_structuralCompose` is genuinely associative and unital, so GK4I packages S as a Mathlib Category.
- `K_O` — GK4S's SECOND quotient of Q by observational equalities; its composition is transported from the actual GK4Q observation image under GK4P's real typed observation laws.

Let `π:Q→S` be GK4E's genuine surjection and `κ:Q→K_O` GK4S's projection. At any actual typed three-stage source/middle/target `t₁,t₂,t₃`, for **ANY** three maps `F₁₂, F₂₃, F₁₃` that satisfy all three commuting equations `Fᵢⱼ(π q)=κ q`, prove:

```text
 F₁₃(structuralCompose u v)
    = kernelCompose (F₁₂ u) (F₂₃ v)
```

because each structural class has a true original P92B representative, GK4H's π preserves original composition, and GK4S's κ does as well under GK4P laws. This implication does NOT need original P92B associativity or unitality, or a fabricated original Type-valued P92B comparison 3-cell.

The comparison maps exist and preserve composition at all three boundaries **iff** the original P92B observer satisfies the full GK4N genuine F54 structural seam invariance condition at EACH of these three boundaries. This is a theorem about the three true source/target pairs; it is NOT an assertion that a fixed-boundary observer automatically has all cross-context congruences without GK4P laws. Mapping the GK4I genuine structural unit yields exactly the K_O class of the actual original P92B zero-edge route.

## Boolean target category and actual functor

For the true GK4G Boolean zero/positive original physical rotation observation:
- Define `nativeGK4UBoolKernelUnit` as the double-quotient image of the genuine original P92B zero-route `nativeGK4H_p92Unit`.
- Define `nativeGK4UBoolKernelCompose` as GK4S's exact true image-transport composition under `Bool.and` and `nativeGK4P_boolean_laws`.
- Prove associativity from `Bool.and`, and left/right units by **actual** GK4R image-level unit theorems transported via GK4S's proved equivalence. All laws live in the second quotient, NOT the original Q.
- Wrap each actual GK4I dependent stage in `NativeGK4UBoolKernelStage`, thereby avoiding an illegal second Category instance on the same original object type. Instantiate a TRUE Mathlib Category with genuine `K_Bool` homs.
- Construct `nativeGK4UBoolKernelComparisonFunctor` from the GK4I independent structural category to this separately wrapped Boolean kernel category. The functor maps are GK4T's canonical lift, preserve actual structural identity and composition by GK4U proofs.
- Prove every typed Hom map is SURJECTIVE (`nativeGK4UBoolKernelFunctor_surjective_hom`); **faithfulness or equivalence is NOT inferred**.

The GK4K `Option Nat` observer fails the genuine F54 left-unit seam, distinguishing `some 2` from `some 1`, so it admits NO such compositional S→K comparison triple at any actually inhabited F45 self-stage. True original physical C60 north F45 triple gives an unconditional paired Boolean-full/Option-obstruction theorem.

## CI correction and authority boundary

Initial PR source HEAD `c9ac18754ba25ed4aa2620cd49216d03b27397ac` failed exactly at the application of `nativeGK4SKernelCompose_assoc`. Lean's **elaborated argument order** places all four explicit typed F45 stages `t₁ t₂ t₃ t₄` before the local Boolean associativity proof `hassoc`. The initial call supplied that proof before the four stages, producing an `Application type mismatch` and the dependent `introN failed` tactic error. After reading the full changed file, the GK4S signature, imports and relevant dependent Mathlib/Lean behavior, the repaired call uses:

```lean
nativeGK4P_boolean_laws t₁ t₂ t₃ t₄
  (by intro x y z; cases x <;> cases y <;> cases z <;> rfl)
  u v w
```

The exact final source `a55d680488c5c9ac277fa9c5517eb821e845ea72` independently passed the complete strict gate. Do not cite the first failed attempt as a success. The proof requires no new axioms or sorry.

**Unproved:** original P92B quotient associativity and left/right identity laws, alternative original P92B composition, unqualified structural vs observer-kernel equivalence/faithfulness, historical complete P92B/F19/F28/F54/F55 typed equivalence, unconditional genuine 14D Countable, original 19D filler, global strict n and hyperdescent. Strict 空 remains central and independent Kuu is ONE presentation; no Gray. Append-only/tighten-only/same-root, 107 public roots. Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Protected validation-only PR #1558 stays Draft/open/unmerged.

**GK4V proposed, NOT proven:** construct actual different structural homs of equal Boolean grade to test GK4U comparison-functor faithfulness and relate it precisely to GK4I's one-object Boolean grading functor.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
