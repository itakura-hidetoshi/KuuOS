# KuuOS / 空OS Roadmap

**Theorem baseline: 2026-09-25 JST · integrated through v4.19**

This roadmap records proved results, explicit hypotheses, countermodel scope, carrier/refinement scope, and theorem-sized exit criteria. It is subordinate to fresh GitHub theorem authority.

## 0. Authority and current canonical state

Repository:

```text
itakura-hidetoshi/KuuOS
```

Canonical branch:

```text
main
```

Current theorem-bearing baseline:

```text
c63c20c8f7726d45ac419a4d4b6a8b794e54f1db
```

This is the merge commit of [PR #1807](https://github.com/itakura-hidetoshi/KuuOS/pull/1807), **Embed middle-switch parity pairs into seed face incidences v4.19**.

Validated v4.19 PR head:

```text
dc19c0d738c853dc648e54f12709387953031203
```

Exact-head governance run:

```text
36145319284
```

All required theorem receipts were successful.

Authority order remains:

```text
1. fresh exact GitHub canonical SHA
2. formal Lean theorem artifacts at that SHA
3. README / ROADMAP
4. exact-head CI/runtime receipts
5. history / memory
```

A documentation-only merge may advance `main` beyond the theorem-bearing SHA without changing mathematical authority.

Pinned formal environment:

```text
Lean    leanprover/lean4:v4.30.0-rc2
Mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

Protected Lean 4.31 validation-only PR:

```text
#1558
open
Draft = true
merged = false
head = 3a09839782ea82661ddbf8e13a0fd08e893079b4
base = validation/lean431-v131-explicit-E-v6
```

#1558 remains outside theorem authority and must not be merged, marked Ready for review, or auto-merged.

## 1. Long-range target

The long-range target remains a dependent-origination carrier with a genuine mapping property:

```text
eta : C ⟶ DO(C, W, J, H)

AdmissibleContextualSystems(C, X)
  ≃ Fun(DO(C, W, J, H), X)
```

Required ingredients include:

- correct higher variance;
- coherent factorization;
- essential uniqueness;
- naturality;
- descent compatibility;
- presentation invariance;
- explicit obstruction/correction semantics;
- explicit separation between formal theorem authority and runtime/operational authority.

A localization, quotient, recursive combinatorial carrier, one successful factorization, or one obstruction witness is not promoted to the final universal object without the required mapping property.

## 2. Major status change since the old v3.73 roadmap

The old frontier asked whether an arbitrary `HigherLocalizationFactorization` might absorb the octahedral `C2` parity class.

That question is now closed.

### v4.00 — direct abstract nonfactorization

Canonical result:

```lean
IsEmpty
  (HigherLocalizationFactorization
    (W := allMorphisms) counterSystem)
```

Thus the concrete finite `C2` countermodel has **no abstract higher-localization factorization at all**.

The old neutrality between:

```text
global cancellation
or
explicit absorbing arbitrary factorization
```

is no longer open for this countermodel. The direct parity/coboundary/compositor line selects nonfactorization.

### Consequence for the roadmap

The center of gravity has moved from:

```text
prove the obstruction exists
```

to:

```text
understand the proved obstruction class
and transport it through larger recursive carriers
without inventing non-authoritative structure
```

## 3. Direct arbitrary-factorization closure — v3.74 through v4.00

The direct closure line after v3.73 performs the following reductions:

1. package the full raw octahedral parity residual;
2. express source-object variation through explicit coboundaries;
3. transport middle-switch naturality through the full localization;
4. align endpoints and source connectors;
5. expand the residual into controlled middle-switch terms;
6. bridge raw restricted-lift compositors with full-localization compositors;
7. cancel the complete residual in `ZMod 2`;
8. derive contradiction for arbitrary source objects;
9. use essential surjectivity of the comparison equivalences to obtain those objects;
10. conclude that `HigherLocalizationFactorization counterSystem` is empty.

The theorem-level closure is v4.00.

This is the primary mathematical baseline for all subsequent countermodel statements.

## 4. v4.01–v4.03 — weak localization principles fail on the finite truth test

### v4.01

The countermodel is weakly `allMorphisms`-admissible but has no arbitrary factorization.

Therefore:

```text
weak admissibility
  !=>
HigherLocalizationFactorization
```

already on the finite octahedral context.

### v4.02

The same witness refutes the unrestricted finite-context forms of:

```text
HigherWeakLocalizationExistence
HigherWeakLocalizationUniversalPrinciple
```

and the countermodel has no weak higher-localization universal-property datum.

### v4.03

The v2.31 three-stage gap decomposition is located exactly:

```text
Stage I: factorization existence      FAILS
Stage II: universal candidate         never reached
Stage III: essential uniqueness       never reached
```

The coherent v2.19 universal principle and the full v2.31 gap-completion package are likewise refuted on this finite context.

## 5. v4.04–v4.06 — structural and gauge-independent source of the obstruction

### v4.04 — sufficient-condition failures

Because the countermodel is admissible but nonfactorizable, it lies outside all previously proved sufficient sectors:

```text
IsFiberFunctorTwoThin
IsFiberHomThin
IsFiberFunctorIsoThin
IsFiberCoreThin
IsFiberAutomorphismTrivial
CanonicalGeneralWGaugeTrivializable
```

These conditions remain sufficient in general; v4.04 does not claim they are necessary. It only classifies the concrete truth-test model.

### v4.05 — explicit invertible isotropy

The structural source is made concrete:

- the unique `CounterFiber` object has the nonidentity automorphism `zeta`;
- the identity endofunctor carries the nonidentity natural automorphism `scalarIdNatIso zeta`;
- every composition-coordinate quotient-gauge fiber is nontrivial.

Thus the obstruction lives in the invertible two-dimensional coherence sector isolated earlier by v2.64–v2.66.

### v4.06 — gauge independence

For every pointwise equivalence datum `D` and every base pointwise choice `L0`:

```text
not FiveDefectGaugeTrivializable ... D L0
```

Equivalently, the entire gauge orbit misses the zero-five-defect locus.

This is the correct global obstruction statement. The recursive program must transport this class, not one arbitrarily chosen bad gauge.

## 6. v4.07 — authority boundary after nonfactorization

The v3.91–v3.97 hexagram scalar/seam files are conditional on:

```lean
H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem
```

but v4.00 proves no such `H` exists.

Therefore:

### Nonvacuous on counterSystem

- truncated-icosahedral / pentagram / hexagram combinatorics;
- quotient-gauge data;
- coherent quotient transport;
- comparison obstruction;
- generated correction coboundary obstruction;
- gauge-independent five-defect obstruction.

### Vacuous on counterSystem

- any scalar/seam object indexed by a hypothetical `H : HigherLocalizationFactorization counterSystem`.

This authority boundary is permanent unless the base theorem context changes.

## 7. v4.08–v4.11 — exact location of the pre-factorization obstruction

### v4.08 — full generated coboundary is unsolvable

For every pointwise equivalence datum:

```text
not GeneratedCorrectionCoboundarySolvable
```

No generated pointwise gauge satisfies all five correction equations.

### v4.09 — any quotient solution is nonliftable

For every actual solved quotient gauge:

```text
not GeneratedComparisonGaugeLiftSolvable
```

### v4.10 — quotient stage succeeds, comparison lift fails

For the canonical datum `counterD`:

```text
coherent quotient transport                         EXISTS
minimal quotient-gauge coboundary solution          EXISTS
comparison-gauge lift                               DOES NOT EXIST
full generated correction coboundary                DOES NOT EXIST
HigherLocalizationFactorization                     DOES NOT EXIST
```

This is the exact Stage-I obstruction location.

### v4.11 — two formal presentations of the same Stage-II failure

For every coherent quotient transport `T`:

```text
not HasCoherentPresentationComparisonData ... T
and
not GeneratedComparisonLiftOverCoherentTransport ... T
```

The first is the original v3.69 parity/cocycle language.
The second is the generated-gauge lifting language.

Future carrier transport should target this transport-independent Stage-II comparison obstruction.

## 8. v4.12 — scalar obstruction class

Source:

```text
formal/KUOS/DependentOriginationStageIIObstructionClassV4_12.lean
```

Canonical scalar representative:

```text
omega(T) = 1 in ZMod 2
```

for every coherent quotient transport `T`.

A comparison would force `omega(T)=0`.

This `omega` is the current algebraic class to be transported through the recursive carrier program.

## 9. v4.13 — local pentagram/hexagram parity contrast

Uniform placement gives:

```text
pentagram crossing set: 5 * omega = omega
hexagram crossing set:  6 * omega = 0
```

Thus the local five-versus-six contrast is formal.

This is a local statement only.

## 10. v4.14 — uniform global truncated-icosahedral transport vanishes

The seed carrier has:

```text
12 pentagonal faces
20 hexagonal faces
```

Uniform face-type support yields:

```text
12 * omega = 0
20 * 0     = 0
global     = 0
```

Therefore uniform local parity does not produce a nonzero global obstruction.

### Exit criterion

Any global recursive theorem must introduce at least one of:

- nonuniform distinguished support;
- orientation-sensitive incidence data;
- a nonconstant cocycle;
- a richer coefficient system.

## 11. v4.15 — nonuniform singleton support preserves the obstruction algebraically

A singleton seed-face decoration can preserve `omega` exactly.

This proves:

```text
nonuniformity is algebraically sufficient
```

but not:

```text
the chosen face is canonical
```

The north-pentagon witness is a construction, not an authority-bearing selection rule.

## 12. v4.16 — explicit eight-face Stage-II carrier

The octahedral Stage-II parity data are represented by an explicit eight-element labeled carrier.

Two questions are separated:

### Algebraic truth

- transport contribution has even total;
- raw/transport mismatch is nonzero;
- the mismatch equals the Stage-II obstruction class.

### Geometric transport

Where should the eight labels live on a larger recursive carrier?

v4.16 does not answer that semantic-placement question.

## 13. v4.17 — global seed capacity is sufficient

The eight Stage-II labels inject into the 12 pentagonal seed faces.

Therefore:

```text
8 <= 12
```

is realized by an explicit Lean embedding.

This removes global finite-capacity as an obstruction.

It does not establish canonical placement or semantic transport.

## 14. v4.18 — one local recursive star is too small

One pentagram has 5 inner crossings.
One hexagram has 6 inner crossings.

Therefore no injective placement of all 8 source labels exists in either local star.

Canonical result:

```text
no eight-label embedding into one pentagram
no eight-label embedding into one hexagram
```

### Consequence

A faithful recursive transport must do at least one of:

1. spread the eight labels over several faces/stars;
2. aggregate source labels by a proved coherence relation;
3. use richer local data than one label per crossing.

## 15. v4.19 — middle-switch pair incidence embedding

Source:

```text
formal/KUOS/DependentOriginationMiddleSwitchPairIncidenceV4_19.lean
```

The eight Stage-II source labels carry middle-switch mate pairs.

v4.19 constructs an injective global placement into seed faces such that:

```text
each mate pair
  -> adjacent pentagon / hexagon seed faces
  -> opposite face kinds
```

This advances the carrier bridge from pure cardinality to genuine incidence compatibility.

### Still missing

v4.19 does not prove:

- canonicality or uniqueness of the placement;
- an orientation/sign convention for scalar pushforward;
- that the placement preserves the nonzero Stage-II class;
- that recursive refinement preserves the class.

These are the immediate next targets.

## 16. Immediate frontier after v4.19

The next proof sequence should be organized around **authority-bearing transport**, not around arbitrary face choices.

### F1 — attach source values to v4.19 incidence placement

Define a pushforward of the eight labeled Stage-II face values along:

```text
octahedralStageIIPairIncidencePlacement
```

with explicit source-label provenance.

Exit criterion:

```text
each source parity value has a typed target seed face
and mate-pair incidence is preserved
```

### F2 — orientation / sign / coefficient rule

Define and justify the coefficient attached to each target incidence.

For `ZMod 2`, orientation signs may collapse, but that must be a theorem rather than an assumption.

Exit criterion:

```text
pushforward total is expressed entirely in carrier incidence data
```

### F3 — nonzero seed-carrier obstruction

Prove that the v4.19 authority-bounded pushforward retains:

```text
omega != 0
```

or prove that the chosen coefficient/incidence rule necessarily cancels.

Either result is legitimate.

### F4 — recursive refinement step

Transport the seed-carrier class through one pentagram/hexagram inner refinement.

Because one local star cannot carry all eight labels injectively, the theorem must explicitly track multi-face support or a proved aggregation rule.

Exit criterion:

```text
one-step recursive obstruction preservation or one-step obstruction loss
```

### F5 — finite-depth recursion

Only after a one-step theorem should finite-depth induction be attempted.

### F6 — metric questions later

Do not infer a metric fractal theorem from incidence recursion alone.

## 17. Carrier interpretation boundary

Currently proved:

```text
finite combinatorial carrier
face kinds
crossing counts
seed-face incidence
pentagon/hexagon adjacency
finite recursive combinatorial refinement
```

Not currently proved:

```text
Euclidean embedding theorem
canonical metric scale
self-similar metric contraction
Hausdorff dimension
infinite-limit convergence
metric fractality
```

Use “recursive combinatorial/incidence self-similarity” unless a metric theorem is added.

## 18. Positive sufficient-condition program remains valid

The counterexample does not invalidate earlier positive theorems under explicit stronger assumptions.

Still valid are sufficient sectors such as:

- fiber hom-thinness;
- fiber functor 2-thinness;
- fiber functor iso-thinness;
- thin fiber cores;
- trivial automorphism groups;
- canonical five-defect gauge trivialization;
- other explicit coherence/separation/descent hypotheses.

What v4.00–v4.05 prove is that the concrete countermodel lies outside those sectors.

The general research question becomes:

> Which minimal additional hypotheses exclude the octahedral obstruction while retaining useful nontrivial models?

## 19. Proof-engineering constraints

### P1 — fresh authority

Re-observe the exact current branch and SHA before branch creation, writes, CI judgment, and merge.

### P2 — import is not open

Use explicit `open` or qualified names.

### P3 — modules are not namespaces

Do not infer namespace names from filenames.

### P4 — local attributes remain local

Imported `@[local simp]` attributes do not propagate.

### P5 — expected types for tactic terms

A bare `by ...` in function position may not elaborate without an expected type. Introduce a typed `have` first.

### P6 — structure projections before AC normalization

Normalize constructors/projections with `simp only` before `ac_rfl`.

### P7 — dependent transport

Prefer `eqToIso` / `eqToHom`.

### P8 — categorical-to-scalar pipeline

Use:

```text
Cat.Hom₂
-> NatTrans
-> component
-> exact target fiber
-> scalar
```

### P9 — do not scalarize too early

Keep categorical composition until the dependent carrier is fixed.

### P10 — `SingleObj` convention

Track:

```text
f ≫ g = g * f
```

### P11 — characteristic-two algebra

First prove the ordinary additive relation, then use `2=0` in `ZMod 2`.

### P12 — exact-head CI only

Every write invalidates previous-head receipts.

Merge only the validated current head SHA.

## 20. Verification commands

Focused current theorem targets:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationAbstractNonfactorizationV4_00

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationComparisonObstructionTwoPresentationsV4_11

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationStageIIObstructionClassV4_12

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationTruncatedIcosahedralGlobalParityV4_14

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationOctahedralStageIIFaceCarrierV4_16

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationParityCarrierCapacityV4_17

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationLocalStarCapacityObstructionV4_18

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.DependentOriginationMiddleSwitchPairIncidenceV4_19
```

Current v4.19 exact validation:

```text
head:
dc19c0d738c853dc648e54f12709387953031203

run:
36145319284

merge:
c63c20c8f7726d45ac419a4d4b6a8b794e54f1db
```

Aggregate formal target:

```bash
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

Runtime validation remains separate:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

## 21. No-go rules

Do not promote these implications without theorem-level support:

```text
import -> namespace opened
module filename -> namespace name
local simp in imported file -> local simp here
Classical.choice -> coherence

weak admissibility -> HigherLocalizationFactorization
weak admissibility -> weak universal property

nontrivial holonomy -> quotient transport failure
one bad fixed gauge -> every gauge fails

H-indexed scalar/seam theorem -> nonvacuous counterSystem datum

pentagram odd parity -> global obstruction
hexagram even parity -> no possible nonuniform obstruction
uniform global cancellation -> all carrier transports cancel

single-face support -> canonical support
8-to-12 injection -> semantic transport
one-star capacity failure -> no multi-face transport
v4.19 incidence-compatible embedding -> canonical embedding
pentagon-hexagon adjacency -> obstruction preservation

finite combinatorial recursion -> metric fractal theorem

Stage-I factorization -> Stage-II universality
runtime success -> theorem authority
docs-only CI -> theorem validation
history/memory -> fresh GitHub authority
```

## 22. Current completion boundary

Canonically proved:

```text
v4.00
abstract HigherLocalizationFactorization for counterSystem is impossible

v4.01-v4.03
weak localization existence/universality principles fail on the finite truth test

v4.04-v4.06
the obstruction is invertible-isotropy-bearing and gauge-independent

v4.07
post-factorization H-indexed recursive scalar data are vacuous for counterSystem

v4.08-v4.11
the pre-factorization obstruction is exactly at the transport-independent
comparison-lift stage

v4.12
a nonzero transport-independent Stage-II ZMod-2 obstruction class is explicit

v4.13-v4.14
local pentagram/hexagram parity contrast is formal, but uniform global transport vanishes

v4.15
nonuniform support can preserve the obstruction algebraically

v4.16
the octahedral obstruction has an explicit eight-label face carrier

v4.17
global truncated-icosahedral seed capacity is sufficient

v4.18
one local pentagram or hexagram star is insufficient for injective eight-label transport

v4.19
an injective global placement exists preserving middle-switch mate
pentagon-hexagon incidence
```

Immediate open problem:

```text
upgrade the v4.19 incidence-compatible placement
from a combinatorial existence result
to an authority-bearing obstruction pushforward
with proved coefficient/orientation semantics
and then test one recursive refinement step
```

That is the canonical next theorem frontier.
