# F112-P94D3GK5AI / Qi v4.2 — structural original F55 3-cell proof histories and genuine physical/categorical truncation

**Research date:** 2026-11-02 JST.
**Canonical source:** `itakura-hidetoshi/KuuOS` `main`, sole public Lean aggregate `KuuOSFormal`, 107 original public roots retained.
**Toolchain:** Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
**Authority:** strict 空 boundary preserved; independent Kuu is a presentation; Qi imports independent Kuu only. Protected PR #1558 Draft/OPEN/unmerged.
**Append-only/tighten-only** without rewriting prior theorem assumptions or historical F54/F55 data.

## Exact-source confirmation

| Item | Independent F112 GK5AI | Qi v4.2 |
| --- | --- | --- |
| Theorem PR | [#2973](https://github.com/itakura-hidetoshi/KuuOS/pull/2973) MERGED | [#2974](https://github.com/itakura-hidetoshi/KuuOS/pull/2974) MERGED |
| Exact-source HEAD | `5f9c14bd29c266474ba996bee3249053e126cb74` | `c3d5aab0752a61dda159eed03deb0f443dbd79c0` |
| Squash merge SHA | `8fb0641cd5c8e61d205ee4922232aa90f7106114` | `00be5b12e2ebc2e925c19e35f00763cb58ed6b1e` |
| Source / squash common Git tree | `61477b023c4431439e2a6560fb8d795095ec6530` | `6de09c82a164f2cf8c1ce0b5a9cb32e9ae48833c` |
| Strict Lean exact-source CI | [#41459203872](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41459203872) SUCCESS | [#41460152297](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41460152297) SUCCESS |
| Lean build | **9222 / 9222 SUCCESS**, `KuuOSFormal` | **10149 / 10149 SUCCESS**, `KuuOSFormal` |
| New source `#print axioms` | **12 / 12**, each within expected set | **7 / 7**, each within expected set |
| Errors/warnings/sorryAx in new source | **0 / 0 / 0** | **0 / 0 / 0** |
| Independent Kuu / Governance | SUCCESS / SUCCESS | SUCCESS / SUCCESS |
| Change | one new native Lean module + one aggregate import | one new Qi Lean module + one aggregate import |

**Axiom boundary:** All 19 new `#print axioms` records were checked from the actual CI logs; the reported dependencies are subsets of `{propext, Classical.choice, Quot.sound}` (the new 9-constructor structural translation itself reported NO axioms). These statements do not erase unrelated older Qi v2.5/v3.7 `native_decide` dependencies.

## GK5AI — structural, proof-relevant original F55 to P92B

**New Lean:** [GK5AI structural F55 whole-cell bridge](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AIStructuralF55WholeCellBridge.lean)

GK5AH retained all original **F54 route** data. GK5AI distinguishes an additional layer: the *free original nine-constructor Type-valued F55 3-cell proof term itself*. Define

```text
nativeGK5AIOriginalToP92Structural :
  PresentedCell_original_F55(p, r, s) →
  NativeF55P92AssocComparison(p, r, s)
```

by actual induction on all **nine** original F55 constructors:
- `ident ↦ refl`;
- `pentagon` and `disjointSquare ↦ original` of the genuinely constructed original cells;
- `symm ↦ symm`, `trans ↦ trans`;
- `leftContext ↦ leftContext`, `rightContext ↦ rightContext`;
- `precompose ↦ precompose`, `postcompose ↦ postcompose`.

`nativeGK5AINorthStructural_trans` and `nativeGK5AINorthStructural_symm` prove the chosen structural mapping preserves actual original source composition and reversal definitionally on the north dependent F54 routes. This is NOT a proof of all 4-cell coherence or of a global 2/3-pseudofunctor.

For genuine north C60, let `c` be the original F55 pentagon between **raw F54 long-3 and short-2**. The different Type-valued cell `trans c (ident short)` has the **same original F54 endpoints** but remains a distinct original F55 proof term. The structurally mapped P92B Type-valued proofs remain distinct too:

```text
c ≠ trans c (ident short)               : ORIGINAL F55 Type evidence
map_struct(c) ≠ map_struct(trans c id) : SELECTED P92B Type evidence
class(long) = class(short)             : P92B QUOTIENT equality
```

`nativeGK5AINorthAddedUnitAssoc_strictBoundary` gives the real P92B `assocNaturality` cell on three original north-C60 F45 *unit routes*, while `nativeGK5AINorthAddedUnitAssoc_noOriginalPreimage` uses the earlier P92A no-go to refute any *original* F55 preimage. This is a **precise non-surjectivity obstruction for the newly adjoined generator**, not a claim that P92B naturality was present in the original nine.

### Local genuine Mathlib whole-NatIso evidence

`NativeGK5AIOriginalWholeCellPacket` holds three **different types** of evidence simultaneously:
1. the complete original F55 Type-valued 3-proof between actual long/short F54 routes;
2. its structurally translated P92B Type-valued 3-proof, together with an exact agreement proof;
3. the genuine whole Mathlib NatIso equality of GK5AF `01;12;23` versus `04;43`.

`nativeGK5AILocalWholePacket` is a constructed LOCAL comparison for every original north F55 cell *at that fixed pentagon boundary*. `nativeGK5AILocalWholePacket_injective` preserves proof identity because the original F55 term is retained. `nativeGK5AILocalWholeEqProofs_equal` and `nativeGK5AIWholeEqProofMap_not_injective` prove that **any map of those original F55 proofs to merely the Mathlib whole NatIso equality proof type is nonfaithful**. Equality proofs live in `Prop` and therefore cannot encode these distinct original Type-valued 3-cell histories.

This does NOT assert a general history-sensitive F54→whole NatIso functor, an arbitrary original F55 3-cell→categorical higher-filler semantics, or a physical Edge=NatIso equality.

## Qi v4.2 — actual physical C60 high-order witness obstruction

**New Lean:** [Qi v4.2 original F55 3-cell readout](../../formal/KUOS/Architecture/QiWuxingGK5AIPhysicalThreeCellHistoryV4_2.lean)

The genuine north-C60 `FivefoldIndex=FivePhase=ZMod 5` physical fifth-around-edge Dart pair and the *actual original F54 long and short full-history fiber objects* enter the physical comparison. The `FivefoldGK5AITruncatedThreeCellBoundary` retains physical Darts, both full F54 boundary histories, the selected P92B class, actual whole categorical NatIso, and proof-irrelevant P92B/categorical equalities constructed from the original cell.

`fivefoldGK5AITruncatedThreeCell_two_equal` proves the two **different original F55 3-cells** produce identical truncated data. This yields `fivefoldGK5AITruncatedThreeCell_not_injective` and `fivefoldGK5AINoTruncatedThreeCellRecovery` (no left inverse), **even though both F54 endpoint histories are retained fully**. This is one higher level of proof-historical information loss than GK5AH.

In contrast, the real `fivefoldGK5AIPhysicalStructuralP92Cell` retains the **P92B Type-valued structural image** and separates those two specific F55 proofs, while `fivefoldGK5AIPhysicalProofRelevantWhole_injective` retains the full original F55 term in a whole-NatIso packet and is injective. No global injectivity of the structural F55→P92B map is claimed beyond the exhibited distinction.

`fivefoldGK5AIStructuralAndOrientationWitnesses` also maintains the actual genuine physical C60 positive-orientation obstruction for categorical edges **04 and 43**; their physical Dart endpoints are reversed. These are NOT declared categorical NatIso arrows or fabricated higher fillers.

## Next frontier — GK5AJ

Build and check actual **proof-relevant 4-cell / relation-level compatibility** of the structural F55→P92B map, testing identity/vertical cancellation, context whiskering and separate P92B `assocNaturality`. Determine exact conditions for comparison reflection, possible faithful lift of higher-cell data, and orientation-aware categorical/physical gluing; prove nonexistence where original P92A/P93 no-go applies. Do NOT assume global F54-to-NatIso interpretation, unqualified higher filler, frozen old KUOS F54 equivalence, unrestricted descent/hyperdescent, or Gray reconstruction.

All historical formal results, same public 107 roots, frozen toolchain and protected PR #1558 remain unchanged.
