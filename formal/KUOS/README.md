# 現役のKuuOS Lean定理群 / Current published KUOS mathematics

`formal/KUOS/` contains the existing Lean theorem sources, not discarded or merely historical examples. The canonical public aggregate `formal/KuuOSFormal.lean` imports `KUOS` and the other existing public theorem modules along with the new `Kuu` modules. The 107 original Lake roots are retained. These proofs keep their original statements, assumptions and established status.

Some versioned declarations use Gray, F51 or F77 concepts. Those results remain available **at their own mathematical scope**, but this does not require making Gray the primitive definition of the independent Kuu presentation. Check actual transitive imports and mathematical hypotheses; neither `KUOS.*` names nor `import Mathlib` establish a Gray dependency.

`formal/KuuOSStrict.lean` is an internal compatibility/import aggregate, not a separate proof world or a separate published Lake root. There is one canonical user-facing build: `lake build` (the target is `KuuOSFormal`). Focused compilation of individual modules is an optional performance optimization, never a separate source of theorem authority.

`legacy/v5.291/` is a frozen reproducibility snapshot only. Its existence does not demote the current live proofs, require their re-proof, or authorize silent identification of old/new theorem source types.
