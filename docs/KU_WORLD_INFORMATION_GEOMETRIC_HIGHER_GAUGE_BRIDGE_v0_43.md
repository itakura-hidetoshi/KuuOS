# WORLD Information-Geometric Higher Gauge Bridge v0.43

v0.43 equips the v0.42 gauge-categorical Indra net with a finite information-geometric observation sidecar. The exact WORLD state is not replaced by a probability distribution or statistical manifold. Each WORLD patch carries an observational statistical representation whose Fisher geometry is transported by the higher gauge connection.

```text
exact WORLD
  → WORLD patch atlas
  → observational statistical point
  → score covectors
  → Fisher metric
  → primal / dual affine connections
  → α-connection family
  → divergence / information projection
  → information holonomy and curvature
```

## Local information-geometric fiber

For every patch `U_i`, v0.43 records:

- a finite observational probability model `p_i(o | θ)`;
- score covectors with zero expectation;
- the Fisher metric as score covariance;
- primal and dual affine connections satisfying metric duality;
- an Amari–Chentsov cubic tensor;
- primal and dual curvature;
- a canonical divergence from dual entropy potentials;
- exponential and mixture geodesic endpoints;
- an information projection with a Pythagorean identity.

The α-connection is defined algebraically by

```text
∇^(α) = ((1+α)/2) ∇ + ((1-α)/2) ∇*
```

so Lean proves directly:

```text
∇^(1)  = ∇
∇^(-1) = ∇*
∇^(0)  = (∇ + ∇*) / 2
```

## Higher gauge transport

Statistical points, tangent vectors, and observations have identity, inverse, and higher-coherent transports. Composition is not flattened:

```text
T_jk(T_ij θ)
  = α_ijk ▹ T_ik θ
```

where `α_ijk` is the v0.42 GaugePhase 2-cell. The same transport preserves:

- probability masses;
- scores;
- Fisher metric;
- primal and dual connections;
- primal and dual curvature;
- information divergence;
- information projection;
- branch-to-statistical-point embeddings.

Thus chart changes may be gauge equivalent while WORLD branches remain ontologically distinct.

## Information holonomy and curvature

The information-geometric holonomy of a triangle is the GaugePhase action on a statistical point. Identity triangles are flat. Nontrivial coherence phases remain visible as information curvature rather than being normalized away.

The finite Lean layer does not claim smooth manifold curvature tensors or continuum differential geometry. Those remain explicit receipts.

## Araki–Petz shadow

The local divergence is linked to a finite observational shadow of Araki relative entropy. The full Hessian realization, quantum Fisher monotonicity, and Petz orthogonal-projection interpretation remain external analytic receipts.

## Lean-direct results

Lean directly verifies:

- probability normalization and score expectation zero;
- Fisher score-covariance formula;
- Fisher symmetry, positivity, and definiteness;
- metric duality of primal and dual connections;
- α-connection special values;
- divergence nonnegativity and separation;
- idempotence and Pythagorean law of information projection;
- injectivity of statistical and tangent transports;
- gauge invariance of Fisher metric and divergence;
- gauge covariance of information projection;
- composition up to higher coherence 2-cells;
- flatness of identity information triangles;
- branch-preserving information transport;
- bundled formal, runtime, and representation-boundary receipts.

Transport injectivity is not assumed separately. Lean derives it from the explicit reverse transport: applying `T_ji` to an equality `T_ij(x) = T_ij(y)` and using both inverse laws recovers `x = y`.

## External receipts

The following are not claimed as Lean-constructed analytic objects:

- smooth statistical-manifold realization;
- Chentsov uniqueness;
- Levi–Civita existence;
- smooth α-connections;
- global geodesic existence and uniqueness;
- quantum Fisher monotonicity;
- Araki relative-entropy Hessian realization;
- Petz recovery as orthogonal information projection;
- higher-stack information geometry;
- continuum information geometry.

## Runtime boundary

Runtime only validates a hash-bound, fail-closed receipt. It does not:

```text
construct a statistical manifold
compute a Fisher metric
perform information projection
optimize a belief state
execute a policy
claim Chentsov's theorem
update WORLD
```

The fixed boundary is:

```text
WORLD ≠ statistical manifold
WORLD ≠ probability distribution
WORLD ≠ Fisher metric
WORLD ≠ information projection
information distance ≠ ontological distance
gauge-equivalent coordinates ≠ WORLD identity
candidate ≠ authority
validation ≠ truth
```

The information-geometric layer is a read-only analytic sidecar preserving nonlinearity, noncommutativity, non-Markovianity, multi-world noncollapse, and the two-truths gap.
