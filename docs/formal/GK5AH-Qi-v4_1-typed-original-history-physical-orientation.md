# F112-P94D3GK5AH / Qi v4.1 — Original Type-valued history fiber, typed F55 comparison, genuine physical C60 orientation

**Verification date:** 2026-11-02 JST
**Canonical repository / branch:** `itakura-hidetoshi/KuuOS`, `main`.
**Authority:** independently reconstructed native Kuu F54-shaped source; Qi imports independent Kuu, never reversely. This does NOT assert an equivalence to the frozen historical KUOS F54/F55 implementation.
**Pinned toolchain:** Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
**Governance:** append-only/tighten-only; preserved public aggregate `KuuOSFormal`, root107; protected PR #1558 Draft/open/unmerged; strict 空 authority boundary.

## Exact-source formal verification, source and Git object provenance

| Receipt | Independent F112 GK5AH | Qi v4.1 integration |
| --- | --- | --- |
| Theorem PR | [#2970](https://github.com/itakura-hidetoshi/KuuOS/pull/2970) MERGED | [#2971](https://github.com/itakura-hidetoshi/KuuOS/pull/2971) MERGED |
| Exact-source PR HEAD | `c3c30a08fdc11a305ebe94e3e619c7b5ce6e6b43` | `c4d44c8786ebd89a314fb3f0add7e542000bd752` |
| Squash merged main SHA | `b1af53d23b72be3b3c70a7256da4f3cd1e117afd` | `3ac191a4e7a851d0a70615d898f7c47c885a2b30` |
| Source and squash identical Git tree | `701b4b52118caad84c927878b49b5a1e969d5469` | `691cf902f3c0d27f693d62ca75a75abbe48d7fe6` |
| New Lean blob SHA | `29c3b821509e20e54e94c896906631e522a940de` | `d421ee0450ff27241f0320c458f7b163b4cdb976` |
| Exact-source PR governance CI | [#41455439373](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41455439373) completed SUCCESS | [#41456275350](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41456275350) completed SUCCESS |
| Strict Lean, `KuuOSFormal` | **9220/9220 SUCCESS** | **10147/10147 SUCCESS** |
| New theorem `#print axioms` | **10/10**, each subset of allowed axioms | **6/6**, each subset of allowed axioms |
| Lean source error/warning | **0/0** | **0/0** |
| Independent Kuu audit (within Governance) | SUCCESS | SUCCESS |
| Source changes | New native Lean file + one aggregate import | New Qi Lean file + one aggregate import |

Both full exact-source CI log artifacts and receipts were independently read: `audit-check-lean-formal-41455439373-1` and `audit-check-lean-formal-41456275350-1`. Compilation used `-DwarningAsError=true` and `-DsorryAsError=true`; no new `sorryAx` appears in the 16 source theorem audit records. Each of the 16 `#print axioms` outputs is contained in `{propext, Classical.choice, Quot.sound}`. This is **not** a global claim that historical Qi v2.5/v3.7 `native_decide` axioms have disappeared.

## GK5AH: actual history-sensitive fiber

**Lean source:**
[`PolygonNativeC60AQFullPentagonPhysicalNativeGK5AHTypedHistoryComparisonInterface.lean`](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AHTypedHistoryComparisonInterface.lean)

Use the EXACT native GK5AG north-C60 original four-stage F45 endpoints and its doubly Nat-dependent, two-category Type-valued F54-shaped route `H`, with existing P92B proof-existence quotient `q : H → Q`. Define the *fully typed* fiber

```text
Fiber := { rawHistory : H,
           comparisonClass : Q,
           comparisonAgrees : comparisonClass = q rawHistory }
```

The constructed `nativeGK5AHNorthHistoryEquiv : H ≃ Fiber` proves full history can be retained without claiming any section `Q → H` of `q`. It retains two Nat depth boundaries, F45 Blocks, AxisTrace and native F54 source/target in the actual `rawHistory` value.

The structure `NativeGK5AHOriginalComparison x y` contains a REAL `PresentedCell` witness of original native F55 **nine-constructor** presentation and its separately chosen P92B `.original` image, with typed proof of the chosen embedding. This is NOT an interpretation of P92B's independently adjoined `.assocNaturality` as if derivable in original F55.

A genuine north-C60 original F55 pentagon cell compares the raw long/short histories, while the two raw fibers themselves remain distinct, and their chosen P92B classes agree:

```text
OriginalF55Cell(longFiber, shortFiber) is inhabited
longFiber != shortFiber
class(longFiber) = class(shortFiber)
rotationCount(long) = 3; rotationCount(short) = 2
```

Thus, unlike a naive equality quotient, the proof-relevant comparison survives **without destroying** raw history. `nativeGK5AHNorthNoP92FiberRetraction` proves there is NO full-history recovery from only the chosen P92B class. `nativeGK5AHNorthFiberFactor_iff` is the exact iff for any readout `Fiber → T` to descend through the actual P92B comparison-existence quotient.

`nativeGK5AHOriginalEqPolicy_not_injective` says any function from full history fiber to equality-valued target that forces equality on every real original F55 3-cell is not injective. Its P92B analog is `nativeGK5AHP92EqPolicy_not_injective`.

The honest `NativeGK5AHWholeCandidate` stores a **supplied** full-history-to-actual-GK5AF-whole-NatIso interpretation and explicitly supplies both required long and short path matches. This is **not** an existence proof. Under these named conditions, `nativeGK5AHWholeCandidate_not_injective`, `nativeGK5AHWholeCandidate_joint_not_injective`, and `nativeGK5AHWholeCandidate_descent_iff` give exact compatibility and obstruction results. The real categorical `01;12;23` and `04;43` Mathlib whole NatIso paths remain distinct from raw history and from physical C60 Edge/Dart.

## Qi v4.1: true physical C60 and orientation-sensitive comparison

**Lean source:**
[`QiWuxingGK5AHTypedNorthHistoryBridgeV4_1.lean`](../../formal/KUOS/Architecture/QiWuxingGK5AHTypedNorthHistoryBridgeV4_1.lean)

Using the EXISTING `FivefoldIndex = FivePhase = ZMod 5` north-C60 gauge, actual physical fifth `around Edge` and its `Dart × Dart` endpoints, show:

- `fivefoldGK5AHNorthPhysicalFiber_injective`: pairing the genuine fifth-edge Dart pair with **complete typed original history fiber** is injective.
- `fivefoldGK5AHNorthPhysicalP92_not_injective` and `fivefoldGK5AHNorthNoPhysicalP92FiberRecovery`: forgetting full history in favor of selected P92B class remains noninjective and has no left inverse, even after adding true physical endpoints.
- `fivefoldGK5AHTypedNorthOrientationEvidence`: genuine fifth Edge/Dart closure, F55 original typed comparison, distinct raw route histories, identical selected P92B class and physical **reverse** direction of categorical edges `04` and `43` are simultaneously available as separately typed witnesses.
- Conditional `FivefoldGK5AHNorthWholeCandidate` preserving the exact GK5AF whole-NatIso carrier gives `fivefoldGK5AHNorthPhysicalP92Whole_not_injective` and `fivefoldGK5AHNorthNoPhysicalP92WholeRecovery` **only for the explicitly path-matched candidate**. No existence of candidate or higher physical-to-categorical filler is asserted.

## Remaining actual proof obligations / next GK5AI

Not proven here: unconditional equivalence of independent native F54-shaped grammar to frozen historical KUOS F54/F55, a general history-sensitive `F54 → GK5AF NatIso` comparison or functor, preservation of all original F55 9 constructors by such a functor, treating P92B's *additional* assocNaturality as old F55, a genuine orientation-aware physical Edge-to-NatIso higher filler, unrestricted descent/hyperdescent, global gluing or Gray reconstruction. In particular an equality-valued interpretation cannot be faithful under the original F55 witness policy; this does NOT rule out a proof-relevant higher interpretation.

**GK5AI target:** first formulate local proof-relevant `F54/F55 → categorical` interpretation data with explicitly typed source/target, compositional/naturality compatibility and proof-relevant cells; check physical `04/43` direction via existing C60 Dart endpoints; prove an actual constructor or a precise obstruction. Preserve strict 空 authority boundaries, actual typed historical witnesses, pins, independent-Kuu → Qi and public root107.
