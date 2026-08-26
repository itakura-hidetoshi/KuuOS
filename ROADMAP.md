# KuuOS / 空OS Roadmap

**基準日：2026年8月27日 JST**

この Roadmap は、authoritative `main` に統合済みの formal theorem surface と、現在の未完 frontier を分離します。queued / in-progress CI、未merge branch、将来構想を integrated baseline として扱いません。

## Authoritative baseline

```text
branch: main
latest integrated formal milestone SHA: 4e273f0d958b5ac4c27bb4f2b430a29ea6760968
latest integrated formal PR: #1483
latest integrated local scaled frontier: v1.69
runtime dependent-origination executable surface: #1386 adapter v0.1
```

PR #1483 は fixed `Δ[3]` 上の complete A/B residual table を統合しました。`main` HEAD は documentation / governance-only synchronizationでこの formal milestone より先へ進み得ますが、それだけで theorem frontier が進んだとは扱いません。現在の mathematical frontier は、その fixed table を actual dependent boundary-prism cells に categorical transport し、その後 scaled rank filtration と v1.59 cellular certificate を構成することです。

## State labels

| 表記 | 意味 |
|---|---|
| Integrated | authoritative `main` に存在する |
| Formal integrated | strict Lean theorem surface が `main` に統合済み |
| Current root | deterministic / effect-free runtime root から検証される |
| Dedicated CI | subsystem 固有 workflow で検証される |
| Live verified | separately authorized live transaction が completed evidence で閉じた |
| Open theorem frontier | theorem-level に未完で、current baseline へ昇格していない |
| Frozen boundary | append-only / tighten-only / overwrite-forbidden / same-root を維持する責任境界 |

## Formal architecture map

現在の formal development は一つの version counter ではなく、次の層に分けて読むのが正確です。

### A. Contextual dependent-origination parent — integrated

```text
context-valued relation
-> state-valued functor
-> composable transport
-> semantic descent under refinement
-> directed / filtered cofinal invariance
-> two-cell and bicategorical coherence
```

主要 milestones:

```text
#1416-#1420  contextual parent v1.0-v1.4
#1422         two-cell refinement coherence v1.5
#1423         native bicategorical coherence + operadic axis
#1424-#1427   higher multicategory / monoidal / causal / no-signalling layers
#1428         enriched / stack / infinity-coherence optional layers
#1429         category-of-elements nerve: strict Segal + quasicategory
```

Frozen distinction:

```text
semantic invariance != root-state existence
optional stack descent != parent contextual descent
operadic joint dependence != tensor-factor independence
```

### B. Higher realization and presentation-independent invariants — integrated

```text
#1430-#1431  2-Yoneda / native mapping quasicategories / complete-Segal interface
#1432         global scaled Duskin nerve
#1433-#1435  scaled-horn coherence + local/global 1-2 cell comparison
#1436         intrinsic presentation-independent invariant kernel
#1437         transport across bicategorical model equivalence
#1440-#1441  strictly-unitary Duskin transport + normalization-choice invariance
#1442-#1451  scaled horn presentation equivalence, global prisms,
              homotopy-class invariance, conditional strictification
```

The invariant direction is

```text
presentation -> intrinsic bicategorical carrier -> observable
```

not selection of one privileged presentation.

### C. Canonical `ScaledSSet` WFS — integrated

```text
#1452-#1454  cylinder/attachment lifting -> terminal RLP
#1455         canonical attachment generators T and T.rlp.llp
#1456         orthogonal universality and WFS interface
#1458         Mathlib small-object interface
#1459         explicit colimits + finite presentability -> unconditional WFS
#1460         external generator comparison interface
#1461         external presentation -> global Duskin fibrancy
```

Integrated theorem-level state:

```text
canonicalGeneratedScaledAnodyne = T.rlp.llp
canonicalGeneratedScaledFibration = T.rlp
(T.rlp.llp, T.rlp) is a native weak factorization system
```

### D. Standard A/B/C scaled-anodyne presentation — integrated infrastructure

```text
#1462  factor canonical attachments through induced scaling
#1463  standard type-(A) scaled inner horns
#1464-#1469
       endpoint pushout-product / Leibniz mate /
       interval cylinder / source enrichment /
       categorical scaled Leibniz pushout
#1470  standard type-(B) scaling pushouts
#1471  q12/q23 B three-simplex completions
#1472  standard type-(C) collapsed-edge generators
#1473  standard A/B/C cellular closure and certificate interface
```

Integrated target objects include:

```text
standardScaledAnodyneGeneratorsABC
standardGeneratedScaledAnodyneABC = ABC.rlp.llp
standardABCCellularClosure
StandardABCTypeAEndpointLeibnizCellularCertificate
```

The certificate structure exists; the theorem constructing the required certificate is still open.

Frozen distinction:

```text
canonical KuuOS arbitrary-scaling family
!= standard A/B/C generator family
```

### E. Endpoint boundary-prism geometry — integrated through v1.69

```text
#1474  endpoint -> full interval-boundary prism factorization
#1475  ordinary inner relative cell complex
#1476  exact scaled cells; outside-horn residual only in N=2/3
#1477  attached dimension N = n or n+1
#1478  top cells have canonical staircase normal form
#1479  exact pure-A cobase-change criterion
#1480  A-compatibility for every cell
#1481  n=2 actual target is maximal; N=2 pure A
#1482  q12/q23 B-completed Δ[3] scalings are maximal
#1483  complete fixed Δ[3] A/B residual table
```

Current fixed three-simplex table:

```text
index 1:
  missing face 023
  horn-saturated A = q12 base
  q12 completion = maximal Δ[3]

index 2:
  missing face 013
  horn-saturated A = q23 base
  q23 completion = maximal Δ[3]
```

For `g.n = 2, N = 3`, the actual cell target scaling is already proved maximal.

## Immediate mathematical program

The next work should be treated as coherent mathematical units, not as isolated micro-lemmas.

### Milestone 1 — close the actual cellwise A/B classification

Goal:

```text
every boundary-prism rank cell
=
pure standard A
or
standard A followed by exactly one q12/q23 B completion
```

Required chain:

1. Construct the canonical reindexing/transport from an actual `N=3` dependent cell carrier to fixed `Δ[3]`.
2. Prove transported actual A-pushout scaling equals the intrinsic fixed horn-saturated A scaling at `CellIndex3`.
3. In the equal branch `g.n = N = 3`, use first-coordinate surjectivity to obtain an epi finite-ordinal endomorphism, hence identity; deduce the cell index is the original `g.i` and the cell is pure A.
4. In the top branch `g.n = 2, N = 3`, combine actual maximality with the fixed residual table to obtain literal A -> q12 or A -> q23 factorization.
5. Recover the staircase display theorem

```text
r = 0 -> q23
r = 1 -> q23
r = 2 -> q12
```

6. Package an exhaustive cellwise theorem usable directly by rank successor pushouts.

Exit criterion: no unresolved local scaling geometry remains in the boundary prism.

### Milestone 2 — construct the scaled rank filtration

The ordinary Mathlib `RelativeCellComplex` from #1475 lives in bare `SSet`; it cannot directly prove membership in the `ScaledSSet` cellular closure.

Construct a genuine scaled filtration:

```text
stage j carrier  = ordinary rank filtration stage
stage j scaling  = pullback of ambient cylinder scaling
```

For each rank successor, factor the scaled attachment into two phases:

```text
A phase:
  coproduct of standard type-(A) cell pushouts

B phase:
  only exceptional n=2,N=3 cells,
  using q12/q23 identity-underlying completion pushouts
```

High-dimensional and equal-dimensional cells stop after the A phase.

The preferred indexing may interleave the two phases over `Nat`, for example:

```text
stage 0
A(rank 0)
B(rank 0)
A(rank 1)
B(rank 1)
...
```

Exit criterion: each successor morphism belongs to pushouts of coproducts of standard A/B generators in `ScaledSSet`.

### Milestone 3 — pass to the transfinite/cellular closure

Use the scaled filtration to prove:

1. the colimit/union of stages is the full scaled boundary prism;
2. successor maps lie in the standard A/B cellular closure;
3. the boundary-prism-to-cylinder map lies in `standardABCCellularClosure`;
4. the endpoint-to-boundary first factor is the opposite-endpoint copy of a standard type-(A) attachment and also lies in the closure;
5. composition gives every standard type-(A) endpoint Leibniz generator in the cellular closure.

Construct the target theorem:

```text
standardABCTypeAEndpointLeibnizCellularCertificate :
  StandardABCTypeAEndpointLeibnizCellularCertificate
```

Exit criterion: v1.59 certificate is theorem-level, not merely an interface.

### Milestone 4 — consume the certificate

Once the certificate exists:

```text
certificate
-> standardABCTypeAEndpointLeibnizCellularCertificate.toLeibnizStability
-> standard type-(A) endpoint Leibniz stability
-> lifting against standardGeneratedScaledFibrationABC
-> standard type-(A) induced attachments lie in standardGeneratedScaledAnodyneABC
```

This closes the standard endpoint-prism theorem.

### Milestone 5 — return to the full canonical/external comparison

Do not conflate this with Milestone 4.

After standard A/B/C endpoint stability, the remaining full comparison obligations must still be discharged explicitly, including the arbitrary-scaling canonical family components isolated by the v1.46-v1.48 interfaces.

Target shape:

```text
canonical attachment family T
<-> generated closure comparison <->
standard/external A/B/C presentation
```

only after both required closure inclusions are theorem-level.

## Secondary formal directions

These remain valid but are lower priority than closing the current endpoint-prism certificate.

### Standard categorical finality bridge

The v1.4 explicit objectwise cofinal condition should be related to standard categorical finality only after comma-category nonemptiness/connectedness hypotheses are formalized.

```text
explicit KuuOS cofinal witness
+ required connectivity
-> standard final/cofinal certificate
```

Do not relabel the existing condition as Mathlib finality prematurely.

### Optional universal semantic carrier

A colimit-like or quotient-like semantic carrier should be added only after an actual universal property is proved.

```text
unique invariant semantic value
!= categorical colimit object
```

### Parent bridges

Continue explicit specialization bridges:

```text
action groupoid / Cech -> contextual parent
free history -> contextual parent
memory-lifted state -> history specialization
process tensor -> operational realization
Choi/comb -> finite-dimensional quantum realization
```

No specialization may silently add assumptions to the parent.

## Runtime and repository program

### Runtime root

Canonical effect-free entrypoint remains:

```bash
PYTHONPATH=. python3 runtime/kuuos_current_check.py
```

The runtime dependent-origination profile still validates the #1386 executable/spec adapter. Formal theorem authority through #1483 is supplied by Lean, not by Python runtime checks.

### GitHub MCP CI re-entry

The preferred durable path is the integrated event-driven v1.3 inbox from #1439:

```text
CI completion
-> bounded repository_dispatch
-> durable deduplicated Issue receipt
-> later MCP fresh re-observation
-> acknowledgement only after exact verification
```

A durable Issue is not itself CI success authority.

### CodeAI

The frozen cohort / prediction-pack / execution-shard contract remains separate from the formal dependent-origination theorem frontier. External benchmark execution must preserve cohort isolation, provenance, shard failures, and the distinction between completed comparison and approved performance claim.

## Integrated subsystem map

| 系列 | 到達点 | 状態 |
|---|---|---|
| Core governance | v0.1 | Frozen boundary |
| Repository self-organization root | v0.113 | Integrated / Current root |
| ObserveOS | v0.7 | Integrated / Dedicated CI |
| VerifyOS | v0.15 | Integrated / Dedicated CI |
| PlanOS | v1.23 | Integrated / Current root |
| DecisionOS | v0.6 | Integrated / Current root |
| MemoryOS | v1.00 | Integrated / Current root |
| Qi Wuxing/Fibonacci history geometry | v2.5 | Integrated / Current root + Dedicated CI |
| CodeAI external benchmark | frozen cohort / prediction-pack / execution-shard contract v0.1 | Integrated / Current root |
| GitHub MCP | durable reentry v1.3 / parent cross-observation v1.1 | Integrated |
| Dependent origination runtime | #1386 adapter v0.1 | Integrated / Current root |
| Contextual parent formal | contextual semantics + bicategorical/enriched/quasicategorical extensions | Formal integrated |
| Presentation-independent higher realization | global scaled Duskin / horn invariants / model transport | Formal integrated |
| Canonical scaled WFS | explicit small-object WFS | Formal integrated |
| Standard A/B/C comparison | explicit generators + cellular interface | Formal integrated |
| Endpoint-prism local frontier | fixed Δ[3] A/B residual table v1.69 | Formal integrated |
| Endpoint-prism scaled cellular certificate | not yet constructed | Open theorem frontier |

Subsystem versions remain independent; they are not one linear maturity scale.

## Frozen boundaries

The following remain tighten-only unless a new versioned authority root explicitly supersedes them:

```text
candidate != authority
observation != verification
validation != truth
formal compilation != external theorem acceptance
receipt != successor authority
selection != execution

contextual transport != substance ontology
semantic descent != state descent
semantic invariance != presentation immobility
cofinal semantic invariance != root-state existence
filtered indexing != categorical colimit
objectwise cofinality != standard final-functor theorem

reversible groupoid specialization != parent dependent origination
quantum realization != parent dependent origination
presentation-independent invariant != preferred presentation

canonical arbitrary-scaling KuuOS family
!= standard A/B/C generator family

fixed Δ[3] residual table
!= actual dependent cellwise factorization

actual cellwise factorization
!= scaled rank filtration

scaled rank filtration
!= cellular certificate until transfinite closure is proved

standard endpoint cellular certificate
!= full canonical/external comparison

KuuOS structural theorem != physical Yang-Mills theorem authority

write accepted != effect verified
compensation != success
MCP write capability != Git authority

one benchmark sample != population performance
contract admitted != execution ready
comparison complete != performance claim approved
```

## Governance rule

Repository evolution at the current frontier remains:

```text
append-only
tighten-only
overwrite-forbidden where frozen
same-root where theorem/receipt requires it
exact-base branch / Draft-first
no sorry / admit / axiom / placeholder constants in formal proof work
no writes to queued/in-progress exact PR heads
completed workflow + job + exact Lean-step evidence before merge
```

These are status criteria, not decorative documentation conventions.
