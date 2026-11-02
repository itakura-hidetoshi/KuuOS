# F112-P94D3GK5AJ / Qi v4.3 — original vertical 4-cell structural translation, exact reflection gate, genuine C60 physical orientation

**Date:** 2026-11-03 JST.
**Canonical repository:** `itakura-hidetoshi/KuuOS`; canonical theorem-bearing branch `main`.
**Authority:** independent Kuu is one presentation; Qi imports Kuu only; strict 空 retains its separate authority. No unconditional equivalence with the historical frozen KUOS F54/F55 implementation.
**Pins:** Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
**Governance:** append-only/tighten-only, no existing theorem/assumption weakened; sole public aggregate `KuuOSFormal`, root107; protected PR #1558 Draft/OPEN/unmerged.

## Exact-source verified provenance

| Evidence | Independent native GK5AJ | Qi v4.3 |
| --- | --- | --- |
| Formal PR | [#2976](https://github.com/itakura-hidetoshi/KuuOS/pull/2976) MERGED | [#2977](https://github.com/itakura-hidetoshi/KuuOS/pull/2977) MERGED |
| Exact-source PR HEAD | `c57a201102c497f75b201e5d1a73de5d2338802a` | `9aad8b1f59bc0768597d8feacc37d211a5ef52a7` |
| Squash merge commit | `e2c0d5dd80f8083b1809861a375dfd5aafe59110` | `13339194a6045a543ef91d63d4a97b82a445ee46` |
| Exact-source / squash identical Git tree | `b4191589309ad3f56a2fbecf434bdd8f1c27b39c` | `1c91de9c1565f4ae72b8ffa64bb605c34de95453` |
| Terminal exact-source PR Governance | [#41487658464](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41487658464) SUCCESS | [#41488714265](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41488714265) SUCCESS |
| Strict Lean | **9224/9224**, `KuuOSFormal` SUCCESS | `KuuOSFormal` + Qi v4.3 SUCCESS (10151-target graph) |
| New `#print axioms` outputs | **12/12**, within allowed set | **6/6**, within allowed set |
| Lean errors/warnings/new sorryAx | **0/0/0** | **0/0/0** |
| Independent Kuu / Governance | SUCCESS / SUCCESS | SUCCESS / SUCCESS |
| Changed source | New native Lean module + one aggregate import | New Qi Lean module + one aggregate import |

The actual exact-source Lean job logs were inspected for successful compilation of the changed modules and `KuuOSFormal`, 18 new theorem/definition axiom records, and absence of Lean errors or warnings. The new records depend only on subsets of `{propext, Classical.choice, Quot.sound}`. Specifically, the original P77→P93 four-cell structural witness map and the original F55 horizontal composition-compatibility theorem report **NO axioms**. These statements do **not** claim that older Qi v2.5/v3.7 `native_decide` dependencies vanished globally.

## GK5AJ — structural translation preserves actual vertical 4-cell witnesses

**New Lean source:** [GK5AJ actual F55 four-cell and reflection](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AJFourCellComparisonReflection.lean)

The old, independently reconstructed F54-shaped grammar has the two original independent Nat depth indices, real F45 Blocks, and fully dependent Type-valued route endpoints. GK5AI gave a structural (not merely `.original`-wrapping) map on **all nine** original F55 3-cell constructors into P92B selected Type-valued comparison terms,

```text
φ : OriginalF55ThreeCell(r,s) → SelectedP92BThreeCell(r,s)
```

GK5AJ constructs a witness-preserving lift for every one of the **eight actually existing P77 raw vertical 4-cell generators**,

```text
Ψ : OriginalP77FourCell(f,g) → SelectedP93FourCell(φ f, φ g)
```

by induction on refl, symm, trans, left/right vertical whiskering, left/right vertical unit, and vertical associativity. All eight target witnesses are real constructors of the P93 Type-valued four-cell source. No shadow equality is used to invent a four-cell. Horizontal 3-cell composition also commutes **definitionally** with φ because both F55 and selected P92B horizontal operations are derived from the same typed original F54 left/right-context and pre/post path structure:

```text
φ(horizontal(f,g)) = horizontal(φ(f),φ(g)).
```

The theorem `nativeGK5AJStructuralShadow` proves for **every original F55 3-cell term**, not only the primitive pentagon/square, that the entire three-coordinate signed C60 shadow (pentagon Int charge, square Int charge, odd ZMod2 exchange phase) is unchanged. This includes the actual original north-C60 pentagon charge `((1,0),0)` and actual north top-hexagon nonzero square phase `1 : ZMod 2`.

### Exact 4-cell quotient map and conditional reflection

P77 and selected P93 have separate quotient objects induced by *existence of actual Type-valued four-cell witnesses*. The genuine induced quotient map

```text
F : (Original F55 ThreeCell)/P77FourCell
      → (Selected P92B ThreeCell)/P93FourCell
```

is well-defined by Ψ, rather than by an assumed numerical or untyped equality.

**Central necessary-and-sufficient theorem:** for each genuine original F54 dependent pair of routes `r,s`,

```text
Injective(F)  ↔
  ∀ f g : OriginalF55ThreeCell(r,s),
    Nonempty(P93FourCell(φ f,φ g))
       → Nonempty(P77FourCell(f,g)).
```

This is `nativeGK5AJFourClassInjective_iff_reflect`; it does NOT assert that every P93 comparison reflects into P77. P93's extra generators, including horizontal/interchange and the separately selected P92B `assocNaturality`, are NOT silently promoted to old P77 or old F55.

`nativeGK5AJFourClassShadow_commutes` certifies the entire signed/odd-phase shadow commutative square after both actual 4-cell quotients.

### North-C60 original 3-proof historical boundary

Let `c` be the genuine original F55 3-cell witnessing the three-vs-two native F54 north pentagon comparison, and let `c · id` be its true original F55 identity-postcomposite. They remain **distinct as raw Type-valued three-proofs**, by GK5AI, but a genuine original P77 right-unit four-cell

```text
P77FourCell(c · id, c)
```

exists, and Ψ constructs the corresponding chosen P93 vertical right-unit 4-cell. Therefore **both quotient classes coincide**, justified by these actual higher witnesses. This is NOT a claim `c · id = c` as original raw three-proof terms.

## Qi v4.3 — exact physical C60 four-cell gate

**New Lean source:** [Qi v4.3 physical four-cell reflection](../../formal/KUOS/Architecture/QiWuxingGK5AJPhysicalFourCellReflectionV4_3.lean)

On the original `FivefoldIndex = FivePhase = ZMod 5` north C60 gauge, use the genuine fifth around-edge and its actual `Dart × Dart` endpoints, the original F54 long/short routes, P77 original and selected P93 actual 4-cell quotient classes.

Define `PhysicalFourClassMap(q) = (physicalFifthDarts, F(q))`. Since the physical Dart pair at a fixed frame/phase is independent of the original F55 proof class, Qi proves **exactly**:

```text
Injective(PhysicalFourClassMap)
  ↔ ∀ original f,g,
       P93FourCell(φ f,φ g) is inhabited
           → P77FourCell(f,g) is inhabited.
```

This is a proved iff of actual mathlib/Lean types, not a conjecture and not proof that the right-hand reflection condition holds. It shows physical C60 endpoint data alone adds no arbitrary 4-cell reflection authority.

Qi further proves the source-original F55 3-proof readout to the genuine `(Dart × Dart) × P93FourClass` is **not injective**: the two distinct native pentagon raw proofs `c` and `c · id` have equal selected P93 four-classes via the actual 4-cell witness. The new real parallel evidence theorem retains north-C60 physical fifth closure, source P77 and selected P93 four-cell witnesses, original 3-proof inequivalence, and the **physical reverse directions of categorical edges 04/43** simultaneously, as different properly typed data.

No physical C60 Edge is identified with a Mathlib whole NatIso. No global higher physical/categorical filler, unconditional source-to-whole pseudofunctor, Gray reconstruction, unrestricted descent, or hyperdescent is asserted.

## Next formal frontier: GK5AK (working title)

The natural next step is to examine **P89 original horizontal interchange** and selected **P93 horizontal/interchange 4-cell** compatibility, in addition to the P77 vertical constructors now handled. Determine the precise conditions under which source interchange 4-cell witnesses, their horizontally whiskered contexts, and the selected P93 four-cells can be compared or reflected. The selected P92B additional assocNaturality is not a theorem of original nine-constructor F55. Any actual obstruction must be proved on original typed witnesses, not inferred from shadows, quotient-existence or phase-five numerology.

Strict 空 authority, full original F54/F55 Type histories, fixed toolchain, no rewriting, same public root107, and the untouched protected draft #1558 remain mandatory.
