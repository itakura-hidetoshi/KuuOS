# Prior-proof kernel recall v0.4 — selected original-source pilot

Parent research head 486bca5c48dc35c48c6faf301ec50010aef39ea9 (PR #3639), unchanged canonical source
subtrees of bb77a15334187b1a4a1fa7acd21934308e8d1338.

Rebuild v0.3's exact-tree lexical index and select three original theorem
declarations from actual concept-query results: Living Engi's source-aware
descent iff and obstruction iff, and Qi v3.4 physical Slot injectivity.
Check source blob and lexical declaration identity. Build the original
selected modules. Re-elaborate byte-identical copies of the original
sources with appended read-only metaprogram observations, retaining all
original imports. The disposable file module name may differ.

Observe ConstantInfo.type, universe parameters, raw expression
representation, direct Expr.getUsedConstants occurrences in type and
proof value, and source-local collectAxioms plus #print axioms reports.
Require expected direct lemma references derived from original bodies.
No missing proof values, diagnostics, or unexpected axioms admitted.
Only after direct green use real lean-lsp-mcp 0.30.0 on separate
imported probes for diagnostics, hover and lean_verify. Preserve actual
responses, hold on disagreement or partial result. A fresh runner is
needs-gated on direct+MCP success and compares exact type expression
hash, direct constant lists, axiom reports, source and catalog evidence.

Checked pinned Lean v4.30.0-rc2 APIs:
src/Lean/Declaration.lean (3934023d7fce1054be48d71057c45d0ccada97b8),
src/Lean/Util/FoldConsts.lean (2bb5be3893dc1daca2e14a6434244920b9784316),
src/Lean/Util/CollectAxioms.lean (dc9897059a4463dfd143a2b3f8fbb4f4a3c3f154).
collectAxioms can use precomputed imported axiom data. Upstream
https://github.com/leanprover/lean4/issues/15226 reports an imported-inductive
under-reporting limitation in the v4.30 series; applicability to the exact
pin is not established here. Agreement of reports is not exhaustive
axiom analysis. Direct expression constant lists are not a transitive
or minimal proof dependency graph (FoldConsts does not collect projection
names). No theorem-equivalence, novelty, new proof, or authority claim.

Separate pilot branch preserves #3639's pending governance. No source
under formal/ or lean/, public root, pins or protected PR changes.
