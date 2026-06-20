# KuuOS Observation–Belief State Kernel v0.21

## Purpose

v0.21 adds the first persistent epistemic layer above the v0.20 mission contract and the durable execution substrate.

```text
mission contract
→ provenance-bound observation
→ chart-local claim state
→ contradiction / staleness residue
→ observation request
→ replay-safe persistence
```

The kernel distinguishes evidence from inference, absence from negation, and belief from truth authority.

## Epistemic classes

Each claim is kept in exactly one visible state:

- `observed_positive`
- `observed_negative`
- `unknown`
- `contradicted`
- `stale`

The core rules are:

```text
unknown != false
missing evidence != negative evidence
belief != truth authority
tool output != verified world truth
```

An `unknown` observation records uncertainty without creating opposing evidence. Opposing evidence does not overwrite supporting evidence; it creates a contradiction residue and a new observation request. Expired evidence does not silently remain current; the claim becomes `stale` while retaining its previous status.

## Observation packet

Every observation is digest-bound to:

- mission and lineage identity
- exact mission-contract and mission-state digests
- local chart
- claim identifier and proposition
- evidence relation (`supports`, `opposes`, or `unknown`)
- source identity and source kind
- raw artifact digest
- provenance chain
- observation and validity times
- confidence
- optional inference-rule digest

Observation packets grant no execution, tool, network, shell, truth, memory-overwrite, commitment, or self-modification authority.

## Local belief state

The state contains chart-local claims, append-only observation history, processed observation digests, contradiction residues, staleness residues, observation requests, exact mission bindings, and non-authority boundaries.

A claim from another chart is rejected rather than silently promoted into a global belief.

## Persistence and replay

The store writes:

```text
initial.json
snapshot.json
observation-ledger.jsonl
```

Recovery reconstructs the state from the immutable initial packet and append-only observation ledger. A mismatching snapshot fails closed. Snapshot repair is explicit and reconstructs only from the validated ledger.

Replaying an already processed observation returns `REPLAYED` and appends no duplicate ledger row, claim evidence, residue, or request.

## Boundary

v0.21 does not plan, authorize, or execute an effect. It does not declare mission success and does not overwrite MemoryOS roots.

```text
observation != truth
belief update != execution permission
contradiction != automatic veto
staleness != falsity
observation request != connector authority
```

## Validation

```bash
PYTHONPATH=. python scripts/check_observation_belief_state_v0_21.py
PYTHONPATH=. python -m unittest -v tests.test_observation_belief_state_v0_21
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.ObservationBeliefStateKernelV0_21
```

## Next dependency

```text
v0.22 Semantic Planner / Replanner
+ Independent Outcome Verifier
```
