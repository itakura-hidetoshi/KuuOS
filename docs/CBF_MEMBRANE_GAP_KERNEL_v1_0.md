# CBF Membrane–Gap Kernel v1.0

CBF Membrane–Gap Kernel v1.0 fixes Control Barrier Functions as a KuuOS membrane-license surface.

It does not treat a CBF pass as truth, execution authority, theorem authority, medical authority, institutional authority, or final commitment.

## One-sentence definition

```text
IntegratedCBFMembraneKernel = a safety-gap-preserving membrane kernel that projects nominal actions into declared membrane-permeable candidates across state, belief, history, learning, gluing, noncommutative, and spectral surfaces.
```

In KuuOS language:

```text
CBF is not a wall that kills action. It is a membrane that harmonizes an action into a non-breaching candidate. Passing the membrane is only a membrane license, not truth and not execution.
```

## Authority boundary

The following invariants are fixed:

```text
CBF pass != truth pass
CBF pass != execute
CBF fail != falsity
CBF license == membrane license only
```

CBF may emit a receipt, a projected candidate, a hold reason, an observation request, a redecomposition request, a recovery-mode request, or a handover request.

CBF must not silently grant:

- execution authority
- truth authority
- final commitment authority
- memory overwrite authority
- theorem authority
- clinical authority
- institutional authority

## Layer summary

### v0.1: membrane and gap

`h(x) > 0` means safe gap.  
`h(x) = 0` means membrane.  
`h(x) < 0` means unsafe-sector breach.

### v0.2: pre-execution membrane filter

A nominal action is either passed as-is or projected into the permeability set.

```text
a_safe = Proj_{Pi(s)}(a_nom)
```

Projection distortion must be recorded. Excessive distortion means the original action intent is not preserved.

### v0.3: membrane stack

The global feasible set is the intersection of grave and hard membrane constraints. Soft slack may be used only for soft membranes and must be recorded as residue.

Hard or grave membrane failure cannot be offset by score, usefulness, majority, or average margin.

### v0.4: temporal membrane

The membrane may depend on internal membrane state and history:

```text
h = h(x, z, H)
```

The state may be safe but non-recoverable. That state is not a strong pass.

### v0.5: belief membrane

CBF usually sees belief, not true state. Uncertainty is subtracted from effective membrane thickness.

Observation absence is not pass evidence.

### v0.6: learning membrane

Learned membranes are advisory or shadow until calibrated and promoted. Hard and grave membranes are tighten-only by default. Relaxation requires proof, authority, and same-root revision.

False pass is more severe than false block.

### v0.7: gauge/sheaf membrane

Local pass is not global pass. Global pass requires overlap compatibility, cocycle consistency, and obstruction checks.

Local repair success is not global safety; repair requires gluing recheck.

### v0.8: noncommutative membrane

A noncommutative membrane uses a self-adjoint observable `H`, density state `rho`, and CPTP channel `E`.

```text
gap = Tr(rho H)
channel_gap = Tr(E(rho) H)
```

CPTP pass is not membrane pass.

### v0.9: spectral/PVM membrane

A self-adjoint membrane operator is split into positive, zero, and negative spectral sectors.

Positive expectation cannot mask negative spectral mass.

Unbounded operator domain, form domain, and trace-integrability uncertainty must block strong pass.

### v1.0: integrated membrane license

The integrated kernel emits membrane licenses with explicit release strength. It remains non-authoritative.

## Required release strengths

```text
NO_LICENSE
LOCAL_MEMBRANE_LICENSE
BELIEF_MEMBRANE_LICENSE
PROJECTED_MEMBRANE_LICENSE
GLOBAL_GLUED_MEMBRANE_LICENSE
ROBUST_SPECTRAL_MEMBRANE_LICENSE
```

## Required decisions

```text
PASS_NOMINAL
PASS_PROJECTED
PASS_WITH_RESIDUE
PASS_BUT_THIN
PASS_WITH_UNCERTAINTY
LOCAL_PASS_GLOBAL_HOLD
REOBSERVE_REQUIRED
REDECOMPOSE_REQUIRED
RECOVERY_MODE_REQUIRED
HOLD_MEMBRANE_THIN
HOLD_DOMAIN_UNCLEAR
BLOCK_MEMBRANE_BREACH
BLOCK_NEGATIVE_SPECTRAL_MASS
BLOCK_AUTHORITY_BOUNDARY
HANDOVER_REQUIRED
```

## Receipt discipline

Every CBF receipt must preserve at least:

- state carrier kind
- action candidate kind
- grave/hard/soft membrane stack
- gap bundle
- uncertainty discount
- projection and projection distortion
- gluing state
- spectral/domain state if used
- learning calibration state if used
- release strength
- decision
- reason codes
- authority flags set to false
- same-root marker
- append-only marker

## Final invariant

```text
CBF gives a membrane license, not a final action command.
```
