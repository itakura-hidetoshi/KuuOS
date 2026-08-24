# Dependent Origination History-Sensitive Transport — Formal v0.5

## Purpose

This layer lifts KuuOS dependent-origination transport above the current
one-parameter positive-time semigroup specialization.

The central design choice is:

> finite history is primary; total-time collapse is an additional theorem, not
> the definition of dependent origination.

This keeps the v0.1–v0.4 transfer/operator development intact while making room
for genuinely history-sensitive and non-Markov semantics.

## Parent structure

For an event type `Event` and state carrier `State`, v0.5 introduces

```text
HistoryTransport Event State
```

with a denotation

```text
eval : List Event -> State -> State
```

satisfying only

```text
eval [] x = x

eval (left ++ right) x = eval left (eval right x).
```

Thus finite words form the free compositional history syntax.  No map from a
word to a scalar duration, no Markov property, and no one-parameter semigroup is
required at this level.

## Genuine history sensitivity

Two histories are distinguished when there exists a state on which their
denotations differ.

For additive time letters, v0.5 calls a transport genuinely history-sensitive
when there exist words `left` and `right` such that

```text
left.sum = right.sum
```

but

```text
eval left x != eval right x
```

for some state `x`.

This is a deliberately structural definition.  It does not claim that every
non-Markov process tensor must be represented exactly by this object; rather, it
records the minimal algebraic phenomenon that a total elapsed-time summary can
fail to determine history semantics.

## Total-time factorization

The current v0.4 positive-time transfer word has more structure.  v0.5 records
that extra structure by an explicit certificate

```text
TotalTimeFactorization H
```

containing an additive one-parameter transport `T` and the theorem

```text
H.eval word x = T_(word.sum) x.
```

From this certificate KuuOS proves:

```text
left.sum = right.sum
=> H.eval left x = H.eval right x
```

and therefore every ordinary readout also agrees on equal-total-time words.

Consequently:

```text
TotalTimeFactorization H
=> not (GenuinelyHistorySensitive H).
```

This gives a clean formal boundary between the free-history parent semantics and
the Markov/semigroup specialization.

## Existing transfer operator as specialization

The v0.4 finite transfer evaluator

```text
wordOperatorApply
```

is embedded as a `HistoryTransport NNReal State`.

Its existing theorem

```text
wordOperatorApply word x = T_(word.sum) x
```

constructs the `TotalTimeFactorization` certificate.  Thus no v0.4 theorem is
weakened or reinterpreted; the same mathematics is now recognized as a special
case of a broader history semantics.

## Relation to KuuOS process-tensor / non-Markov architecture

KuuOS already contains history-bearing process-tensor and non-Markov modules
whose governance receipts explicitly preserve non-Markov memory and protected
history.  v0.5 supplies a small proof-facing algebraic interface that those
layers may specialize in future work.

No existing process-tensor module is claimed to satisfy the new structure merely
by naming similarity.  A bridge must provide the actual `eval_nil` and
`eval_append` witnesses, and genuine history sensitivity requires an explicit
same-summary/different-denotation witness.

## Dependent-origination reading

The transport spine now has the hierarchy

```text
空
  -> no individual presentation is granted independent semantic substance

縁起
  -> composable relations / finite histories carry transport semantics

history-sensitive transport
  -> a finite relational path can retain information beyond a coarse summary

semigroup specialization
  -> history semantics factors through total elapsed time

linear transfer operator
  -> the semigroup is represented linearly on a state carrier

vacuum/gap/readout layer
  -> nontrivial centered components contract and observable readouts decay
```

The mathematical construction is an interpretation interface for KuuOS.  It is
not a historical claim that Buddhist dependent origination is literally a
specific category, semigroup, or process tensor.

## Physical authority boundary

This file and its Lean companion do **not** construct or assert:

- a Yang–Mills Hamiltonian,
- a Yang–Mills spectral measure,
- a physical vacuum-orthogonal Hilbert sector,
- a Clay-level mass gap,
- or a process tensor for the physical Yang–Mills theory.

The repository `itakura-hidetoshi/4d-mass-gap` remains authoritative for its own
physical transfer-operator and mass-gap proof obligations.

## Update discipline

v0.5 is additive / tighten-only relative to the v0.4 spine.  Existing groupoid,
Čech, semigroup, gap, linear-transfer, connected-readout, and finite-word
results remain unchanged.
