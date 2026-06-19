# Research Basis for the KuuOS Adaptive Agent Reference Architecture v1.0

This note records why the architecture is organized as a fixed reference model rather than as an indefinitely growing sequence of PlanOS patches.

## MORPH

MORPH separates behavior adaptation from configuration adaptation and coordinates them through explicit interfaces. KuuOS adopts this split as:

- Deliberation Plane: behavior, sequencing, and replanning;
- Authority Plane: capability, binding, lease, renewal, escalation, and re-rotation.

Reference: Victor Braberman, Nicolas D'Ippolito, Jeff Kramer, Daniel Sykes, and Sebastian Uchitel, “MORPH: A Reference Architecture for Configuration and Behaviour Self-Adaptation,” arXiv:1504.08339.

## Runtime megamodels

Runtime models become difficult to manage when their relations are encoded by scattered ad-hoc checks. KuuOS therefore declares the runtime model inventory and relation vocabulary explicitly and validates the complete relation set.

Reference: Thomas Vogel, Andreas Seibel, and Holger Giese, “The Role of Models and Megamodels at Runtime,” arXiv:1805.07396.

## ActivFORMS

Correct adaptation requires correctness of the feedback-loop behavior, not only correctness of the selected adaptation result. KuuOS therefore defines one finite global event and transition model and verifies its common post-state invariant.

Reference: Danny Weyns and M. Usman Iftikhar, “ActivFORMS: A Formally-Founded Model-Based Approach to Engineer Self-Adaptive Systems,” arXiv:1908.11179.

## Simplex runtime assurance

A flexible advanced controller should be separated from a small assurance mechanism that can block unsafe operation. KuuOS therefore separates Deliberation from Assurance and restricts the Assurance Plane to monitoring, classification, suspension, and safe halt.

Reference: Usama Mehmood, Sanaz Sheikhi, Stanley Bak, Scott A. Smolka, and Scott D. Stoller, “The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS,” arXiv:2102.12981.

## KuuOS-specific extension

KuuOS adds four constraints not supplied merely by adopting those reference architectures:

1. observation and verification remain distinct;
2. learning updates future behavior only;
3. no planner, monitor, router, evidence packet, or runtime model acquires undeclared authority;
4. a terminal session is never resumed, and nonterminal recovery requires a fresh lineage, activation, and session.

## Development consequence

The architecture changes the development question from:

```text
What should PlanOS v0.18 add?
```

to:

```text
Which declared global transition, relation, invariant, or refinement obligation remains uncovered?
```

A new local version is justified only when it implements an already declared gap or when a separately reviewed architecture revision extends the global model.
