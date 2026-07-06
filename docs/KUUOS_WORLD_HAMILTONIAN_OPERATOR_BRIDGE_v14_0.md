# KuuOS v14.0 — Hamiltonian Operator Bridge

## 1. 目的

この文書は、KuuOS v14.0 Causal WorldModel OS に Hamiltonian operator layer を追加する。

追加対象は、完成済み R4 Hilbert-space handoff の下流に置かれる operator / Hamiltonian candidate layer である。

この layer は、物理的 self-adjoint Yang--Mills Hamiltonian の完成を主張しない。

## 2. 入力境界

Hamiltonian operator bridge は、次の Hilbert-space bridge を前提にする。

```text
R4CompletedHilbertSpaceAPI = completed
R4HilbertHandoffAPI = completed
DownstreamOSOperatorLayerHandoff = ready-for-internal-modeling
```

この前提により、WORLD モデルは Hamiltonian candidate を内部状態として扱える。

ただし、candidate と physical Hamiltonian は同一ではない。

## 3. WORLD variables

標準変数は次である。

```text
HamiltonianOperatorCandidateLayer = candidate-ready
HamiltonianOperatorHandoffAPI = pending-self-adjointness
SelfAdjointHamiltonianAPI = not-established
HamiltonianSpectralTheoremLayer = not-established
HamiltonianSpectralGapLayer = not-established
```

`HamiltonianOperatorCandidateLayer` は、Hilbert-space handoff から operator layer へ進む準備があることを示す。

`HamiltonianOperatorHandoffAPI` は、self-adjointness proof と spectral theorem proof がまだ必要であることを示す。

## 4. Protected boundaries

次の変数は protected variables として扱う。

```text
SelfAdjointHamiltonianAPI
HamiltonianSpectralTheoremLayer
HamiltonianSpectralGapLayer
PhysicalMassGapClaimBoundary
```

これらは、通常の observation / intervention によって `established` へ上書きしてはならない。

確立には、Lean 側で対応する定理層が追加され、source repository で replay され、その結果が別の proof-state input として WORLD model に取り込まれる必要がある。

## 5. Operator ladder

KuuOS WORLD model では、Hamiltonian への道筋を次の ladder として保持する。

```text
completed Hilbert-space API
  -> operator candidate layer
  -> densely defined operator boundary
  -> closed / closable operator boundary
  -> self-adjointness boundary
  -> spectral theorem layer
  -> spectral gap witness layer
```

この ladder は、何が完了し、何が未確立かを同時に保持するための状態構造である。

## 6. Non-claim

この bridge は Hamiltonian を WORLD モデルに追加する。

ただし、追加される Hamiltonian は operator candidate layer であり、物理的 self-adjoint Hamiltonian ではない。

この bridge は、spectral theorem、Hamiltonian spectral gap、または四次元 Yang--Mills mass-gap theorem を完成させるものではない。
