# Independent Kuu integration — evidence and remaining acceptance

The source at `fe9d720a36025a9fc259b70bf43b9f33b45891f2` passed Independent Kuu Foundation run `38827903551` (47 is not the count at that older head: it ran 45 tests). Lean built 644 jobs; 21 printed declarations used no sorryAx. The exact legacy tree and pinned inputs passed integrity checks.

The follow-up patch explicitly scopes the ten historical read-only manifests v0.86–v0.95 to `legacy-v5.291`, without setting `repository_autorepair_contract` or changing any execution, approval, rollback or write-permission field. Together with the previously scoped v0.78–v0.85 contracts, all 18 recorded historical formal contracts now declare their package.

The two new tests first reported 10 missing package fields. After the metadata correction, these tests plus the existing v0.86–v0.95 subsystem suites passed locally: 324 tests, zero failures. The local copy of the ten input manifests was checked byte-for-byte against their fresh MCP blob SHAs; the observer used in the tests matched blob `05a66a8a7a0a0f260e76f60bf986dc1ff4711245`.

The independent foundation runner now includes the two new tests (47 total) and the extra scope check is registered with Governance. Current Kuu source, Lake roots, Lean toolchain and all frozen historical source/configuration objects are unchanged by this patch. The fixed 196-consumer migration remains bounded; the ten additional read-only contracts have a separate regression guard. Future current Kuu contracts are not automatically reclassified.

Integration acceptance still requires the new exact-head Lean, runtime, static, shard and required-gate results. This record does not declare a merge or a successful check that has not yet been observed.

Mathematical scope remains the independent presentation quotient, strict two-dimensional comparison and given-context incidence construction. Proof-relevant global strict 3-cells, all original F112 raw-source ports and the full genuine C60 incidence reconstruction are not consequences of these integration checks.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Original licensing applies.
