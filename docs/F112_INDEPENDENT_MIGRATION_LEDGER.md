# F112: independent Kuu migration ledger (2026-10-16)

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
| 1–2 (v5.273–274) | Physical C60 restriction towers; independent pentagon/hexagon F42 source cells | **Not transferred** |
| 3–4 (v5.275–276) | Original four-boundary F54/F55 cell grammar and faithful mixed source base change | **Not transferred** |
| 5–7 (v5.277–279) | Genuine cross-edge physical intersection witnesses, finite overlap paths, original F69 forward/backward zigzag | **Original typed forward/backward zigzag proved; actual common-original-cell witness and arbitrary finite overlap-path functor implemented in `Overlap` (new head CI pending); original proof-relevant F47 transport remains unported** |
| 8–11 (v5.280–283) | Raw inversion/noncollapse, actual F69 localization, kernel quotient to original FreeGroupoid | **New genuine physical F69 zigzag/kernel-quotient localization equivalence proved in Lean at `31894075` (1408/1408, no sorryAx); old F47 source-specific factorization still unported** |
| 12 (v5.284) | 360 authentic vertex–edge–face 2-simplices and raw two-step versus diagonal distinction | **Genuine geometry, all 360 flags, raw two-step ≠ diagonal, nerve diagonal equality and exact localization/kernel quotient equality now proved on independent source** |
| 13–15 (v5.285–287) | Original F42/F54/F55 Beck–Chevalley NatIso on real polygon sources, crossed physical edges and paths | **Not transferred** |
| 16 (v5.288) | Diagram-level NatIso induces base-preserving Grothendieck total Cat isomorphism and equivalence | **General theorem mechanism re-proved**, but actual old F47 source diagrams not yet realized |
| 17 (v5.289) | Localization of that original mixed-source total equivalence and retention of complete native phase | **General quotient NatIso mechanism re-proved; specific localization and phases not yet realized** |
| 18 (v5.290) | Exact signed curvature and necessary nonzero north-pentagon repair +5, and conditional descent | **Not transferred; historical F68 observation not identified with new invariant** |
| 19 (v5.291) | True full original 60/90/32 incidence diagram and 90 independent Kuu source observers | **Original finite incidence graph/poset rebuilt; Kuu observer/source equivalence still needed** |

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

## Freshly verified independent F112 geometric proof carrier

Exact PR source head `31894075fdeb3b2b5e5018df22d99d2882e065c4`
passed [Independent Kuu Foundation run 38910660394](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38910660394)
with Lean **1408 / 1408**, and [PR Governance run 38910660642](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38910660642)
completed SUCCESS. All new `#print axioms` declarations in
`TotalChange`, `Physical`, `Zigzag`, `Nerve`, `Localization`,
`KernelEquivalence` depend only on Lean's standard
`propext` / `Classical.choice` / `Quot.sound` (or fewer); no `sorryAx`.

The core equivalence is a theorem of the **new independently typed physical
Site**, not an import of historical `KUOS.*`:

`ZigzagKernelQuotient ≌ PhysicalLocalization ≌ PhysicalFreeGroupoid`

It uses actual physical incidence, exact localization-kernel relation and
mathlib's source generator decoding. Raw paths remain distinct until
quotiented. The new `Overlap` unit adds proof-carrying real shared physical
sites and arbitrary finite chains of witnesses; the new HEAD containing it
must pass exact CI separately before its results are considered certified.

## Remaining work — no false completion certificate

1. Independently define full F42/F54/F55 *raw boundary-typed* proof-relevant
   terms and allowed generating relations, then prove source-side 3-cell
   globularity, horizontal/vertical pasting and strict interchange without
   assuming any desired coherence equations.
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
