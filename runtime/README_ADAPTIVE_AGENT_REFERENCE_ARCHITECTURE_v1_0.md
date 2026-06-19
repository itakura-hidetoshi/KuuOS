# Adaptive Agent Reference Runtime v1.0

The Python files in this directory are an executable reference model, not an execution authority.

- `kuuos_adaptive_agent_reference_types_v1_0.py` fixes the planes, stages, recovery algebra, and refinement map.
- `kuuos_adaptive_agent_runtime_megamodel_v1_0.py` fixes the runtime-model inventory and relation set.
- `kuuos_adaptive_agent_transition_kernel_v1_0.py` implements the finite global transition function and validates the common post-state invariant.
- `kuuos_adaptive_agent_reference_scenarios_v1_0.py` supplies nominal and fault scenarios.

New implementations should refine this model rather than add undeclared transitions.