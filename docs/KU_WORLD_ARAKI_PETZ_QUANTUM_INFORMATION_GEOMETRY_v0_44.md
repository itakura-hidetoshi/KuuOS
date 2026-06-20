# WORLD Araki–Petz Quantum Information Geometry v0.44

v0.44 connects the finite information-geometric sidecar of v0.43 to the Araki-relative-entropy and Petz-recovery spine of v0.34–v0.35.

```text
Araki relative entropy
  → finite Hessian shadow
  → quantum Fisher metric
  → coarse tangent channel
  → Petz tangent recovery
  → recovered tangent projection
  → orthogonal residual
  → information loss / data-processing defect
```

The exact WORLD state is not replaced by an entropy Hessian, a quantum Fisher metric, or a Petz information projection.

## Finite Hessian shadow

Each WORLD patch carries a finite bilinear form

```text
H_Araki^shadow(θ; u, v)
```

with the typed identifications

```text
H_Araki^shadow = g_QF = g_Fisher(v0.43).
```

Lean therefore derives symmetry, positivity, definiteness, and gauge covariance of the quantum Fisher form from the already validated v0.43 Fisher geometry.

This is a finite observational shadow. The existence of the genuine second Fréchet derivative of Araki relative entropy and its identification with the Bogoliubov–Kubo–Mori metric remain external analytic receipts.

## Coarse tangent channel and Petz recovery

For every patch and parameter, v0.44 records linear maps

```text
C_θ : T_θ → T_θ
R_θ : T_θ → T_θ
```

and defines the recovered tangent channel

```text
Π_θ = R_θ ∘ C_θ.
```

Lean checks

```text
Π_θ² = Π_θ
C_θ Π_θ = C_θ
```

and links these finite maps to the operator-algebraic maps of v0.35:

```text
Obs(C_θ u) = Φ(Obs(u))
Obs(R_θ u) = R_Petz(Obs(u))
Obs(Π_θ u) = R_Petz(Φ(Obs(u))).
```

## Orthogonal decomposition

The residual

```text
u_loss = u - Π_θ u
```

is quantum-Fisher orthogonal to the recovered tangent space. The corresponding Pythagorean identity is

```text
g_QF(u,u)
  = g_QF(u_loss,u_loss)
  + g_QF(Π_θu,Π_θu).
```

This yields the finite information loss

```text
L_QF(u) = g_QF(u - Π_θu, u - Π_θu) ≥ 0.
```

Lean proves

```text
L_QF(u) = 0 ↔ Π_θu = u.
```

Thus zero finite information loss means recoverability inside the analytic sidecar. It does not establish ontological identity of WORLD states or branches.

## Data-processing defect

The quantum-Fisher data-processing defect is

```text
Δ_QF(u)
  = g_QF(u,u) - g_QF(C_θu,C_θu).
```

Monotonicity gives `Δ_QF(u) ≥ 0`, and the supplied finite equality-case receipt gives

```text
Δ_QF(u) = 0 ↔ Π_θu = u.
```

The full theorem that BKM quantum Fisher information is monotone under arbitrary normal UCP maps, and that equality is equivalent to Petz sufficiency, remains external.

## Higher-gauge covariance

The Araki-Hessian shadow, quantum Fisher metric, coarse tangent channel, Petz tangent recovery, recovered projection, and information loss are transported covariantly across the v0.43 WORLD patch atlas.

Gauge-equivalent information coordinates do not identify WORLD branches. Higher-gauge holonomy from v0.42–v0.43 remains intact.

## Lean-direct surface

Lean directly verifies:

- `arakiHessianShadow = quantumFisherMetric = fisherMetric`;
- quantum Fisher symmetry, positivity, and definiteness;
- recovered tangent idempotence;
- recovered tangents are fixed points;
- residual orthogonality;
- the quantum-Fisher Pythagorean identity;
- nonnegative information loss;
- zero information loss iff Petz recoverability;
- nonnegative data-processing defect;
- zero defect iff Petz recoverability;
- operator-level `R_Petz ∘ Φ` compatibility;
- gauge invariance of quantum Fisher information and information loss;
- runtime and representation-boundary packages.

## External analytic receipts

The following remain external:

- twice differentiability of Araki relative entropy;
- identification of its Hessian with the BKM/Kubo–Mori metric;
- construction and uniqueness properties of the BKM metric;
- quantum Fisher monotonicity for normal UCP maps;
- Petz recovery as the genuine orthogonal information projection;
- equality in data processing iff recoverability/sufficiency;
- information geometry of sufficient von Neumann subalgebras;
- noncommutative exponential-family realization;
- continuum and higher-stack quantum information geometry.

## Runtime boundary

Runtime validates only a hash-bound, fail-closed receipt. It does not:

```text
differentiate Araki relative entropy
compute a physical quantum Fisher metric
construct a BKM metric
execute a Petz information projection
infer operator-algebraic sufficiency
optimize a WORLD state
update WORLD
```

The fixed boundary is

```text
WORLD ≠ Araki Hessian
WORLD ≠ quantum Fisher metric
WORLD ≠ Petz projection
metric recoverability ≠ ontological identity
candidate ≠ authority
validation ≠ truth
```

The complete v0.44 layer remains a read-only quantum-information-geometric sidecar preserving noncommutativity, non-Markovian history, multi-world noncollapse, and the two-truths gap.
