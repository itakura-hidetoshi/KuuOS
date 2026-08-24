# Dependent Origination Finite Transfer Word — Formal v0.4

## Purpose

This note records the v0.4 extension of the KuuOS dependent-origination
transport spine from one- and two-step positive-time transfer to arbitrary
finite transfer histories.

The central object is a finite word

```text
[t₀, t₁, ..., tₙ₋₁],   tᵢ ∈ ℝ≥0,
```

interpreted as a finite ordered history of composable positive-time transfers.

The formal carrier is intentionally minimal:

```lean
abbrev TransferWord := List NNReal
```

The word is syntax.  Its semantics is supplied by the already existing linear
transfer realization of the v0.3 dependent-origination transport spine.

---

## 1. Why finite words belong to the dependent-origination layer

The v0.1 principle is

```text
Dependent Origination = functorial composable transport.
```

The v0.2 and v0.3 positive-time specializations instantiate this with an
additive one-parameter semigroup and, optionally, a linear transfer operator.

A finite transfer word makes the composition structure explicit:

```text
x
  --T_t(n-1)--> ...
  --T_t1------> ...
  --T_t0------> final state.
```

With the convention already used by the KuuOS semigroup spine,

```text
T_(s+t) = T_s ∘ T_t,
```

the list head acts after the recursively evaluated tail.

This is not merely notation.  It separates two logically different layers:

1. **history syntax** — the ordered finite word is retained;
2. **semigroup semantics** — in the present one-parameter model the word's
   denotation factors through total elapsed time.

That distinction becomes essential when KuuOS later moves from Markovian
semigroup semantics to non-Markovian/process-tensor semantics.

---

## 2. Total time

For a word `w`, define

```text
τ(w) = Σ tᵢ.
```

Formally:

```lean
def wordTotalTime (word : TransferWord) : NNReal := word.sum
```

Concatenation is additive:

```text
τ(u ++ v) = τ(u) + τ(v).
```

Thus concatenation of finite histories maps to addition in the positive-time
parameter monoid.

---

## 3. Word evaluation

Given a linear transfer realization `L`, the word evaluation is recursive:

```text
Eval([] , x) = x,
Eval(t :: w, x) = T_t(Eval(w, x)).
```

The empty word is therefore the identity history.

Concatenation is composition:

```text
Eval(u ++ v, x) = Eval(u, Eval(v, x)).
```

This is the finite-word form of dependent origination as composable transport.

---

## 4. Total-time factorization

The main structural theorem is

```text
Eval(w, x) = T_{τ(w)} x.
```

This is proved by induction on the finite word using only

```text
T_0 = id
```

and

```text
T_(s+t) = T_s ∘ T_t.
```

Consequently, if two words have equal total time,

```text
τ(u) = τ(v),
```

then the present semigroup realization gives

```text
Eval(u, x) = Eval(v, x).
```

This theorem must be interpreted carefully.

It does **not** say that KuuOS histories are intrinsically determined only by a
single scalar duration.  It says that this particular one-parameter additive
semigroup specialization forgets the finer word history at the semantic level.

The syntax remains available for later history-sensitive realizations.

---

## 5. The Markov/non-Markov boundary

The finite-word layer exposes a clean boundary:

```text
ordered word history
      |
      | current semigroup factorization
      v
total elapsed time
      |
      v
single transfer T_total
```

For a Markovian one-parameter semigroup this factorization is expected.

For a genuinely non-Markovian process tensor, one should instead allow a
history-sensitive denotation

```text
Eval([t₀, ..., tₙ₋₁], history/context)
```

that need not factor through

```text
Σ tᵢ.
```

Therefore v0.4 deliberately retains `TransferWord` as a list rather than
replacing it by a single `NNReal` value.

This is a KuuOS architectural point:

```text
syntax remembers relation history;
semantics may or may not quotient that history.
```

---

## 6. Exponential gap weights along words

The v0.2 abstract gap supplies a per-time decay factor

```text
q(t) = exp(-m t).
```

For a finite word define the product weight

```text
Q(w) = ∏ᵢ q(tᵢ).
```

The formal theorem is

```text
Q(w) = q(τ(w)).
```

This follows from

```text
q(s+t) = q(s) q(t).
```

Thus the exponential gap weight is multiplicative under word composition and
simultaneously factors through total elapsed time.

---

## 7. Connected/vacuum-subtracted readout along a word

The v0.3 layer supplies

```text
centeredState(x) = x - Ω
```

and a connected scalar readout after one transfer:

```text
R(T_t x - Ω).
```

The v0.4 word version is

```text
R(Eval(w, x) - Ω).
```

Using total-time factorization, one obtains exactly

```text
connectedWordReadout(w, x)
  = connectedReadout(τ(w), x).
```

Hence every centered excitation satisfying the abstract v0.2 exponential gap
obeys

```text
|connectedWordReadout(w, x)|
  ≤ C_R exp(-m τ(w)) ‖x - Ω‖.
```

Equivalently,

```text
|connectedWordReadout(w, x)|
  ≤ C_R (∏ᵢ exp(-m tᵢ)) ‖x - Ω‖.
```

This is the arbitrary-finite-word extension of the one-step and two-step
connected-readout decay proved in v0.3.

---

## 8. Relation to transfer-operator language

The conceptual dictionary is now:

| KuuOS concept | finite-word formalization |
| --- | --- |
| conditioned appearance | state `x` |
| one dependent relation | one transfer letter `t` |
| finite dependent history | `TransferWord = List NNReal` |
| composition of relations | list concatenation / recursive evaluation |
| semigroup quotient | factorization through `wordTotalTime` |
| vacuum/reference | `Ω` |
| nontrivial component | `x - Ω` |
| gap weight | `exp(-m t)` |
| word gap weight | product of per-letter factors |
| observable appearance | bounded connected readout |

This makes precise the slogan

```text
Dependent origination = composition-compatible transport before object-substance.
```

A finite transfer word is the corresponding finite relational sentence.

---

## 9. Reversible gauge words versus positive-time transfer words

KuuOS already has an action-groupoid/Čech branch where arrows are invertible.
The v0.4 transfer word is deliberately different:

```text
gauge word:
  reversible arrows / groupoid composition

positive-time transfer word:
  generally non-invertible transfers / semigroup composition
```

Both are instances of the common functorial transport principle, but neither is
identified with the other.

This separation prevents the formal architecture from falsely imposing
invertibility on Euclidean transfer or irreversibility on gauge change.

---

## 10. Physical authority boundary

This KuuOS layer is structural only.

It does not prove or assert:

- existence of a Yang--Mills Hamiltonian;
- self-adjointness of such a Hamiltonian;
- a physical vacuum-orthogonal Hilbert sector;
- a Yang--Mills spectral measure;
- a physical mass gap;
- a Clay-level Yang--Mills theorem.

The repository `itakura-hidetoshi/4d-mass-gap` remains authoritative for
physical Yang--Mills transfer-operator, Hamiltonian, and mass-gap obligations.

KuuOS imports only the mathematical pattern:

```text
finite composable transfer history
→ semigroup composition
→ vacuum subtraction
→ exponential decay
→ connected readout decay.
```

---

## 11. Current formal spine

After v0.4 the KuuOS transport hierarchy is

```text
Dependent Origination
= functorial composable transport
        |
        +-- reversible branch
        |     |
        |     +-- action groupoid
        |           |
        |           +-- Čech descent
        |
        +-- positive-time branch
              |
              +-- additive semigroup
                    |
                    +-- contractive vacuum-fixed transport
                          |
                          +-- abstract exponential gap
                                |
                                +-- bounded readout decay
                                      |
                                      +-- linear transfer realization
                                            |
                                            +-- connected readout
                                                  |
                                                  +-- finite transfer word
                                                        |
                                                        +-- total-time factorization
                                                        +-- product decay factor
                                                        +-- finite-word connected decay
```

The next natural extension is not to erase the word into total time more
aggressively, but to preserve the word as a first-class history carrier so that
a future non-Markovian/process-tensor realization can replace the current
factorization theorem by genuinely history-sensitive semantics.
