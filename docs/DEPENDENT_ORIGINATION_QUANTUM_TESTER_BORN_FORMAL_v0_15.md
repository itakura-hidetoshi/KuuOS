# Dependent Origination Quantum Tester / Born Layer v0.15

## Purpose

v0.14 introduced a direct all-leg response for an arbitrary open deterministic
`QuantumCombChoi`.  That response is complex-linear in every intervention slot,
but an arbitrary open comb is not automatically a normalized scalar
probability tester.

v0.15 makes the distinction explicit and formal.

## 1. Positive Choi slot words

A fixed-length `ChoiSlotWord d n` is positive when every slot Choi matrix is
positive semidefinite.  The full history tensor is recursively

```text
slotTensor(nil) = I
slotTensor(J :: past) = slotTensor(past) ⊗ₖ J.
```

Using Mathlib's positive-semidefinite Kronecker theorem, v0.15 proves

```text
all slot Choi matrices PSD
=>
slotTensor PSD.
```

## 2. Tester pairing

For a tester matrix `W` and a complete slot word `slots`, define

```text
testerPairing W slots
  = Tr (W * slotTensor slots).
```

This is exactly the same bilinear all-leg pairing used by the v0.14 direct
open-comb response when `W` is an open-comb Choi matrix.

The file proves the finite-dimensional positivity lemma

```text
A PSD, B PSD => 0 <= Tr(A B)
```

in the canonical complex order.  Hence a positive tester matrix assigns a
nonnegative complex weight to every positive Choi-slot history.

## 3. Deterministic tester normalization

A deterministic closed tester must respond with one to every word of
trace-preserving intervention Choi matrices.  This is recorded as

```text
TesterNormalized W :=
  forall slots,
    TracePreserving slots ->
      testerPairing W slots = 1.
```

`QuantumProcessTesterChoi d n` bundles

```text
choi     : Matrix (CombIndex d n) (CombIndex d n) C
positive : choi PSD
normalized : TesterNormalized choi.
```

This is intentionally a separate carrier from `QuantumCombChoi`.

## 4. Born weights

For a closed tester `T`,

```text
T.weight slots      = testerPairing T.choi slots
T.probability slots = Re (T.weight slots).
```

For positive selected slots:

```text
T.weight slots >= 0
T.probability slots >= 0.
```

For deterministic trace-preserving slot words:

```text
T.weight slots = 1
T.probability slots = 1.
```

## 5. Finite quantum instruments

`InstrumentSlotSchedule d Outcome n` is a fixed-length schedule of the native
v0.12 quantum instruments.

Each instrument supplies

```text
outcomeChoi o >= 0

totalChoi = sum_o outcomeChoi o

partialTraceOutput totalChoi = I.
```

The schedule's `totalChoiWord` is therefore deterministic in every slot.

The file also constructs the explicit recursively iterated all-outcome tensor

```text
outcomeTensorSum schedule
```

and proves

```text
outcomeTensorSum schedule
  = slotTensor (totalChoiWord schedule).
```

Thus the finite tensor-level sum over all outcome branches has tester weight
exactly one.

## 6. Selected histories

`SelectedInstrumentHistory d Outcome n` records one concrete instrument and
one selected outcome at every slot.  Its Choi word is positive because every
outcome map is Mathlib completely positive and v0.10 identifies complete
positivity with Choi positivity.

Therefore every selected finite outcome history has nonnegative Born
probability.

## 7. Total probability

For a tester `T` and finite instrument schedule `S`, define

```text
T.totalInstrumentWeight S
  = Tr (T.choi * S.outcomeTensorSum).
```

Since the explicit iterated outcome tensor equals the deterministic total-Choi
word, tester normalization yields

```text
T.totalInstrumentWeight S = 1
T.totalInstrumentProbability S = 1.
```

Hence the v0.15 closed tester supports a normalized finite-history quantum
Born law.

## 8. Architectural boundary

The hierarchy is now

```text
open QuantumCombChoi
  -> general process response
  -> may be history-sensitive
  -> not automatically a scalar probability law

QuantumProcessTesterChoi
  -> positive closed tester
  -> deterministic normalization
  -> CP histories have nonnegative weights
  -> finite instrument outcome total = 1.
```

v0.15 does not assert that every `QuantumCombChoi` canonically determines a
`QuantumProcessTesterChoi`.  A closure/duality construction is additional
structure and remains explicit.

The matrix recursive dual partial-trace characterization of
`TesterNormalized` is also not silently assumed here; the present layer uses
the operationally exact deterministic-tester condition.  Establishing its
matrix-recursive equivalence is a subsequent formal theorem layer.

No physical Yang--Mills authority is promoted into this KuuOS structural
formalization.
