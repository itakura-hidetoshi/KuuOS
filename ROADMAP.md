# KuuOS / 空OS Roadmap

**基準日：2026年8月28日 JST**

この Roadmap は、authoritative `main` に統合済みの formal theorem surface と、現在の未完 frontier を分離します。queued / in-progress CI、未merge branch、将来構想を integrated baseline として扱いません。

## Authoritative baseline

```text
branch: main
latest integrated formal milestone SHA: 9d8d9be1c001f0a6f7dbd0b30922c42066c9b21d
latest integrated formal PR: #1535
latest integrated local scaled frontier: v1.120
runtime dependent-origination executable surface: #1386 adapter v0.1
```

PR #1534 / v1.119 **Formalize the standard/canonical orthogonality diamond** により、standard A/B/C presentation `S` と canonical KuuOS presentation `C` の full generated left/right theories は incomparable であることが確定しました。

PR #1535 / v1.120 **Prove terminal fibrancy does not faithfully reflect presentation order** は、その strict presentation distinction が terminal-map semantics では collapse し得ることを証明しました。

現在の mathematical baseline は

```text
L_standard || L_canonical
R_standard || R_canonical
S || C

        S ⊔ C
        /   \
       S     C
        \   /
        S ⊓ C

all four edges strict
```

であり、一方 terminal objects では

```text
Fib_C ⊊ Fib_S

U := S ⊔ C
C < U
Fib_U = Fib_C
```

です。

したがって現在の frontier は standard/canonical equality を再び目指すことではなく、**full orthogonality semantics から terminal/fibrant-object semantics への restriction が何を保持し、何を忘却するかを構造化すること**です。

## State labels

| 表記 | 意味 |
|---|---|
| Integrated | authoritative `main` に存在する |
| Formal integrated | strict Lean theorem surface が `main` に統合済み |
| Current root | deterministic / effect-free runtime root から検証される |
| Dedicated CI | subsystem 固有 workflow で検証される |
| Live verified | separately authorized live transaction が completed evidence で閉じた |
| Open theorem frontier | theorem-level に未完で、current baseline へ昇格していない |
| Retired theorem frontier | 後続 theorem により最終目標として不可能または不要と確定した旧 frontier |
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

### D. Generated-presentation invariant and complete lattice — integrated

The literal generator family is not the invariant carrier. Presentations are quotiented by mutual orthogonal generation and then identified with orthogonally saturated fixed points.

```text
v1.81  GeneratedScaledAnodynePresentation quotient
v1.83  posetal reflection
v1.84  order reflection
v1.85  saturated left/right fixed-point order isomorphisms
v1.86  complete lattice
v1.87  standard/canonical lower and upper envelopes
```

For every presentation `P`:

```text
L_P := generatedAnodyneClass P
R_P := generatedFibrationClass P

L_P.rlp = R_P
R_P.llp = L_P

P ≤ Q
↔ L_P ≤ L_Q
↔ R_Q ≤ R_P
```

The right coordinate is therefore a faithful full-theory invariant. Equality of full generated right classes implies equality of quotient presentations.

For arbitrary joins:

```text
R_(⨆ i, P_i) = ⨅ i, R_(P_i)
```

This formula is the order-theoretic input used by v1.120.

### E. Standard/canonical comparison — resolved, not open

The old comparison program asked whether one generated theory contains the other. It is now theorem-level closed in the negative.

Two independent separators are integrated:

```text
canonical not ≤ standard:
  atomic scaling enrichment
  + concrete B^2 N standard-right terminal witness
  -> v1.107 separation

standard not ≤ canonical:
  degree-three Type-A horn Λ[3,1] -> Δ[3]
  + canonical-right relative rigidity
  + failure of self-lifting
  -> v1.118 separation
```

v1.119 packages the consequence:

```text
L_standard || L_canonical
R_standard || R_canonical
S || C

S ⊓ C < S
S ⊓ C < C
S < S ⊔ C
C < S ⊔ C
```

The old positive/reverse comparison structures are provably uninhabited.

Frozen conclusion:

```text
remaining Type-A or Type-C geometry
cannot restore
a globally refuted standard/canonical inclusion or equality
```

### F. Terminal/fibrant-object semantics — integrated through v1.120

v1.115 proves the terminal slice is strictly one-sided:

```text
Fib_C ⊊ Fib_S
```

This does not contradict full right-class incomparability because terminal maps are only a special slice of all morphisms.

For `U := S ⊔ C`, v1.120 proves

```text
R_U = R_S ∩ R_C

Fib_U(X)
↔ Fib_S(X) ∧ Fib_C(X)
↔ Fib_C(X)
```

while v1.119 gives `C < U`.

Hence

```text
C < U
but
fibrantObjectSemantics C = fibrantObjectSemantics U
```

and the formal surface includes

```text
fibrantObjectSemantics_not_injective
fibrantObjectSemantics_not_orderReflecting
```

This is the new starting point.

## Immediate mathematical program

The next work should be treated as coherent mathematical units, not as isolated micro-lemmas.

### Milestone 1 — separate faithful full-right semantics from terminal restriction

The full generated right class already separates presentations:

```text
P = Q
↔ R_P = R_Q.
```

Terminal restriction does not.

Define and package the restriction explicitly:

```text
terminalRestriction(R)
  := { X | R (toPoint X) }

fullRightSemantics(P) := R_P
fibrantObjectSemantics(P)
  = terminalRestriction(fullRightSemantics(P))
```

Target theorem package:

```text
fullRightSemantics is faithful / order-reflecting
terminalRestriction ∘ fullRightSemantics is not injective
terminalRestriction ∘ fullRightSemantics is not order-reflecting
```

Use the existing `C < U` and `Fib_C = Fib_U` as the concrete witness, rather than constructing a new separator.

Exit criterion: the precise locus of information loss is a named map from full morphism semantics to terminal-object semantics.

### Milestone 2 — generalize terminal join absorption

v1.120 is not specific to standard/canonical geometry at the order-theoretic level.

For arbitrary generated presentations `P,Q`, prove first

```text
Fib_(P ⊔ Q)(X)
↔ Fib_P(X) ∧ Fib_Q(X).
```

Then derive the absorption theorem

```text
(∀ X, Fib_Q(X) -> Fib_P(X))
->
∀ X, Fib_(P ⊔ Q)(X) ↔ Fib_Q(X).
```

The standard/canonical theorem becomes the specialization

```text
P = S
Q = C
```

using v1.115.

Exit criterion: terminal semantic collapse is an intrinsic lattice theorem, not only a binary standard/canonical fact.

### Milestone 3 — fibrant-object semantic equivalence and quotient

Define

```text
P ≈_Fib Q
:
↔ ∀ X, Fib_P(X) ↔ Fib_Q(X).
```

Formalize:

1. `≈_Fib` is an equivalence relation;
2. `C ≈_Fib U` but `C ≠ U`;
3. the quotient forgets strictly more than generated-presentation equivalence;
4. presentation order descends only through the contravariant semantic order actually justified by inclusion of fibrant-object sets.

Do not call this quotient a localization or homotopy theory until an appropriate universal property is proved.

Exit criterion: the non-faithfulness theorem is promoted from one witness to an explicit semantic quotient structure.

### Milestone 4 — determine which lattice operations survive terminal semantics

Join behavior is exact because full right classes turn joins into intersections:

```text
Fib_(P ⊔ Q) = Fib_P ∩ Fib_Q.
```

Meet behavior is subtler because

```text
R_(P ⊓ Q)
```

is obtained by right orthogonal closure of an ambient join and need not reduce to a simple union of terminal object sets.

Study, without assuming an answer:

```text
which joins/meets descend to the Fib quotient?
which inequalities become equalities after terminal restriction?
which additional hypotheses make meet semantics computable?
```

Exit criterion: a theorem-level description of the algebraic structure retained by terminal semantics.

### Milestone 5 — optional geometry after comparison closure

Type-A and Type-C geometry may continue when it yields intrinsic structure, explicit fillers, minimal generators, or reusable lifting theorems.

It must no longer be framed as a route to

```text
S ≤ C
C ≤ S
S = C
```

because all three possibilities requiring comparability/equality are already ruled out by v1.119.

## Retired theorem program

The long endpoint boundary-prism / A-B residual program was a genuine historical prerequisite for the later comparison spine, but it is no longer the current roadmap frontier.

Historical stages included:

```text
v1.59  standard A/B/C cellular certificate interface
v1.69  fixed Δ[3] A/B residual table
subsequent dependent-cell / filtration / endpoint lifting progression
```

Likewise the old global target

```text
canonical attachment family
<-> standard A/B/C presentation
```

is retired as an equality/inclusion frontier. v1.119 proves the full generated theories are incomparable.

These results remain useful internal geometry; they are not deleted or downgraded as theorems. Only their status as the active final objective is retired.

## Secondary formal directions

These remain valid but are lower priority than structuralizing the terminal semantic restriction.

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

The runtime dependent-origination profile still validates the #1386 executable/spec adapter. Formal theorem authority through #1535 is supplied by Lean, not by Python runtime checks.

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
| Generated-presentation lattice | quotient / posetal reflection / complete lattice v1.86 | Formal integrated |
| Standard/canonical full orthogonality | strict diamond / left-right incomparability v1.119 | Formal integrated |
| Terminal fibrant-object semantics | strict `Fib_C ⊊ Fib_S`, non-faithful order v1.120 | Formal integrated |
| Semantic restriction / Fib quotient | not yet packaged generically | Open theorem frontier |

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

full right-class semantics
!= terminal-map restriction

same fibrant-object semantics
!= equal generated presentation

presentation inequality
!= terminal-semantic inequality

Type-C geometric refinement
!= restoration of a globally refuted presentation inclusion

Fib semantic quotient
!= localization until a universal property is proved

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
completed workflow + all jobs + exact Lean-step + manifest + governance evidence before merge
```

These are status criteria, not decorative documentation conventions.
