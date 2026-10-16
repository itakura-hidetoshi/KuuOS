# F112: independent Kuu migration ledger (2026-10-17 JST)

## Authority and meaning

Old 19-stage F112 theorem history (v5.273 through v5.291) is preserved in
`legacy/v5.291/formal/KUOS/`. Those theorems involve old source definitions,
including proof-relevant F42/F54/F55, F47, F51/F77, signed original F68
curvature and F69 incidence. Compiling the frozen history does **not** prove
the same statements in the new independent `Kuu.*` mathematics.

New current code must use boundary-typed generation and declared congruences,
not an old Gray evaluation kernel, a surrogate Bool site or an asserted
exchange/naturality axiom.

## Exact transfer accounting

| F112 historical stage | Current independent formal obligations | Current proof status |
|---|---|---|
| 1–2 (v5.273–274) | Physical C60 restriction towers; independent pentagon/hexagon F42 source cells | **New independent** actual 5/6-sided closed boundaries, Type-valued face sectors, cone-fan disk soundness and full 32-polygon source atlas proved. Historical F42 source-type equivalence and refinement towers **not transferred** |
| 3–4 (v5.275–276) | Original four-boundary F54/F55 cell grammar and faithful mixed source base change | **Not transferred** |
| 5–7 (v5.277–279) | Genuine cross-edge physical intersection witnesses, finite overlap paths, original F69 forward/backward zigzag | **Proved** independent authentic overlap witnesses, finite paths, forward/backward raw zigzags and localization factors. Historical proof-relevant F47 transport remains unported |
| 8–11 (v5.280–283) | Raw inversion/noncollapse, actual F69 localization, kernel quotient to original FreeGroupoid | **Proved** genuine physical F69 kernel-quotient/FreeGroupoid equivalences, full/faithful/essentially surjective. Old F47 source-specific factorization still unported |
| 12 (v5.284) | 360 authentic vertex–edge–face 2-simplices and raw two-step versus diagonal distinction | **Genuine geometry, all 360 flags, raw two-step ≠ diagonal, nerve diagonal equality and exact localization/kernel quotient equality now proved on independent source** |
| 13–15 (v5.285–287) | Original F42/F54/F55 Beck–Chevalley NatIso on real polygon sources, crossed physical edges and paths | **New independent F42-like** typed physical sector/disk source and kernel-sound fan proved. Historical F42/F54/F55 original mixed source and Beck–Chevalley NatIso **not transferred** |
| 16 (v5.288) | Diagram-level NatIso induces base-preserving Grothendieck total Cat isomorphism and equivalence | **General theorem mechanism re-proved**, but actual old F47 source diagrams not yet realized |
| 17 (v5.289) | Localization of that original mixed-source total equivalence and retention of complete native phase | **General quotient NatIso mechanism re-proved; specific localization and phases not yet realized** |
| 18 (v5.290) | Exact signed curvature and necessary nonzero north-pentagon repair +5, and conditional descent | **Not transferred; historical F68 observation not identified with new invariant** |
| 19 (v5.291) | True full original 60/90/32 incidence diagram and 90 independent Kuu source observers | **Proved** authentic incidence poset, 360 flags, 32 independent polygon presentations, 180 actual polygon-side incidences and exact double-boundary incidence for all 90 edges. Historical 90 F47 fibers and source equivalence **not transferred** |

## Current theorem-bearing units

`formal/Kuu/F112/Physical.lean` constructs the actual truncated-icosahedral
incidence geometry using an explicit original icosahedron (12 vertices,
30 edges, 20 triangular faces), endpoint darts (60), 30 cross plus 60
around-vertex edges (90), and 12 pentagon plus 20 hexagon polygon sites
(32). The ordered around-vertex darts define the original triangular
corners. The actual derived vertex-edge-face incidence partial order and
360 composable physical flags are constructed with decidable finite
proofs. This is neither an invented square surface nor an arbitrary
180/182-element proxy. It supplies geometry **only**; historical F47
source functors and physical curvature are not smuggled in.

`formal/Kuu/F112/TotalChange.lean` proves actual Cat-valued diagram
source-change transport, unit/composition, exact index preservation,
strict Cat isomorphism and total equivalence, plus quotient natural-isomorphism
descent for separately supplied observers respecting Kuu's declared
relations. These are mathematical mechanisms shared with former F112
parts 16–17. **Input diagrams and old proof-related source change remain
to be constructed and proved**, so this is not an old theorem by renaming.

## Certified independent polygon higher-source carrier (F112-A through D3)

The current `formal/Kuu/F112/` layers all enter the standard
`KuuOSStrict` and `KuuOSFormal` Lean roots, WITHOUT importing frozen
`KUOS.*`, Gray, F51 or F77.

- `FaceRewrite.lean` (F112-A): genuine C60 vertex-edge-polygon
  triangle two-cell source as a Type-valued proof tree with inverses,
  vertical composition, both contexts and proven localization/kernel
  soundness. Raw witnesses remain distinct from unit-prefixed ones.
- `PolygonBoundary.lean` (F112-B): each of the 12 true pentagons has
  five cyclically closed real edges and each of the 20 true hexagons
  has six. Each edge is incident to the actual polygon and joins its
  two real darts; physical face-side labels are checked.
- `PolygonRawLoop.lean` (F112-C): the dependent finite-prefix
  construction glues **one genuine closed raw zigzag per actual face**,
  with **10 / 12 noncancelled original incidence legs**, proven
  different from raw nil.
- `PolygonFan.lean` (F112-D1): each physical boundary edge span
  `dart -> edge <- dart` has a genuinely typed Type-valued sector
  comparison to `dart -> actual face <- dart`. The comparison is
  **proved** sound in the actual Gabriel-Zisman localization and exact
  kernel quotient, not postulated as a charge/Gray evaluation.
- `PolygonDisk.lean` (F112-D2): exact source-level common-face spokes
  and the generalized telescoping proof give
  `polygonRawLoop_localized_id` and `polygonRawLoop_kernel_id`
  **for all 32 original polygons**. The new `PolygonDiskRewrite`
  is a Type-valued face-disk generator with separately proved
  localization/kernel soundness. This does NOT imply raw-loop equality
  to nil or any historical F68/F77 obstruction vanishing.
- `PolygonSource.lean` (F112-D3): `PolygonSourcePresentation p`
  independently records all 5/6 raw proof-relevant fan sector witnesses
  PLUS the certified face-disk term. Canonical and unit-prefixed
  presentations are **provably unequal** for every real face.
  `originalEdge_polygonBoundary_iff` establishes the precise TWO
  physical neighboring polygons of each of all 90 edges; there are
  precisely `180 = 12 * 5 + 20 * 6 = 2 * 90` original boundary-side
  occurrences. A canonical atlas on all 32 original polygon sites
  is defined.

**Authority limit:** these new types are genuinely independent, but
their **historical F42 source equality/equivalence has not been shown**;
neither has the original F54 full rotation syntax, F55 3-cell source,
F47 typed mixed boundary comparison or Beck-Chevalley NatIso, or the
signed F68/F77 obstructions. A disk loop becomes identity ONLY
after a particular localization/kernel quotient; its raw proof
witness and possible enriched historical charge must not be erased.

## Fresh exact-head certified formal status

Latest **theorem-bearing** PR #2339 source HEAD:
`f2960e10b71af70400e00c1cf0567862348e85b0`.
The exact-head [Independent Kuu Foundation run 38963171275](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38963171275)
completed **SUCCESS** with `lake build KuuOSFormal` **1416 / 1416**,
and [PR Governance Gate run 38963171258](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38963171258)
completed **SUCCESS**, including Strict Lean, independent foundation,
legacy preservation and both MCP completion receipts.

The new `PolygonSource.lean` reports **9** explicit
`#print axioms` declarations in Lean. Each depends only on standard
`propext`, `Classical.choice`, `Quot.sound` or fewer: **no
`sorryAx`**. The changed Lean file has no warning/error.
The previously certified independent F112-A/B/C/D1/D2 results were
recompiled by the exact full build and preserved.

The independent F69 categorical result remains:
`ZigzagKernelQuotient ≌ PhysicalLocalization ≌ PhysicalFreeGroupoid`.

This exact CI is evidence for the HEAD above, not a promise
that a subsequently edited HEAD has passed. The PR remains
**Draft / OPEN / unmerged**; canonical `main` remains
`a5b48eb60b0f400183af1cc2736857181a87d1d0`.

## Remaining work — no false completion certificate

1. Bridge the new *independent* real 5/6-sided sector/disk source with
   the historical F42 source only by an explicit faithful typed
   presentation comparison, not by silently renaming source types.
   Construct F54's ORIGINAL polygon rotation paths and 2-cell
   naturality, then genuine F55 proof-relevant 3-cells with globularity,
   horizontal/vertical pasting and **proved**, not asserted, interchange.
2. Realize all physical source face sites, prove real F69 F47 fibre
   consistency, then build face-change Beck–Chevalley NatIso and Čech
   transport along arbitrary genuine witnessed paths.
3. **Geometric F69 raw zigzag/localization/kernel quotient is now proved**
   (including fullness and essential surjectivity), so construct the separately
   missing original F47 source-specific localization factorization and prove
   compatibility with real F69 overlap-site functors.
4. Identify and compare (not blindly inherit) historical F55 Delta
   nonlift, F77 phase loss, and original signed F68 curvature; retain
   any nonzero physical obstruction instead of erasing it.
5. Prove only the original-source global descent actually licensed by
   those constructions; do not confuse Kuu quotient descent with
   raw original F47 source 3-stack effectivity.

No original Gray imports, new axioms, `sorry`, `admit`, or
`native_decide` are permitted in new core proofs. Lean v4.30.0-rc2
and pinned mathlib manifest are unchanged. PR #1558 stays validation only.
