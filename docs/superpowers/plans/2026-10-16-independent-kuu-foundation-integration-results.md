# Independent Kuu integration — evidence and acceptance

Source `fe9d720a36025a9fc259b70bf43b9f33b45891f2` passed Independent Kuu Foundation run `38827903551`: 45 tests, 644 Lean build jobs and 21 printed declarations without sorryAx. The exact legacy tree and fixed inputs passed integrity checks.

The follow-up patch scopes the ten historical read-only manifests v0.86–v0.95 to `legacy-v5.291`, without setting `repository_autorepair_contract` or changing any execution, approval, rollback or write-permission field. All 18 recorded historical repository formal contracts now declare their package.

The scope regression first reported ten missing fields. After correction, the two scope tests and existing v0.86–v0.95 subsystem suites passed locally: 324 tests, no failures. The ten input manifests were matched byte-for-byte to fresh MCP blob SHAs; the observer used in these tests matched blob `05a66a8a7a0a0f260e76f60bf986dc1ff4711245`.

A further regression demonstrated that the actual Lake library lacked warningAsError in its leanOptions. The library now sets `leanOptions = { warningAsError = true }`; the regression passes. Lake's -K flags are configuration inputs, not an automatic forwarding mechanism for Lean compiler arguments. Reference: the official Lake configuration documentation, https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/ .

The foundation runner now includes all three additional tests (48 total). The fixed 196-consumer migration remains bounded, with a separate guard for the additional read-only contracts. No future current Kuu contract is automatically reclassified. Current definitions, public roots, Lean version and frozen historical source/configuration objects are otherwise unchanged.

Final integration acceptance requires the new exact-head Lean, runtime, static, shard, required-gate and completion results on PR #2338. This record is not a substitute for those CI results and does not predeclare a merge.

Mathematical scope remains the independent presentation quotient, strict two-dimensional comparison and given-context incidence construction. Proof-relevant global strict 3-cells, all original F112 raw-source ports and full genuine C60 incidence reconstruction are separate obligations.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Original licensing applies.
