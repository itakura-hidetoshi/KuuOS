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

## R1 observed failure and correction (2026-11-24)

Run 45332533402, job 138236826466, source 80500c64544178355b5843dc65c2025f7c375b59:
6/6 parser tests and selected original module build (8408 jobs) succeeded.
The direct stage failed in read_direct; real MCP and independent runner
were skipped. Recovered actual artifact 14892767172, direct-0.log: both
LEC targets emitted elaborated types, expected direct proof references,
and the kernel Name list [Classical.choice]. Original #print axioms
reported [Classical.choice]; the appended report with pp.universes true
reported [Classical.choice.{u}]. This is a display mismatch, not proof
failure or an unauthorized axiom. Qi direct observation was not reached.
Scope pp.universes false to the appended #print axioms command only,
retain all detailed type/universe fields and exact strict comparison.
Do not silently normalize arbitrary axiom strings. Add two regressions,
including the actual decorated-name failure shape. The old failure
artifact is retained; the new source must pass direct Lean, actual MCP
and independent runner before any positive admission.

## R2: original canonical Lake compiler options (2026-11-24)

R1 run 45333970598, job 138241578635: 8/8 tests, original module
build 8408/8408 SUCCESS. Direct LEC reports now agree. Downloaded artifact
14892769483 includes direct-0.log and direct-1.log and both complete
scratch sources. All three selected observations were emitted. For the
R1 source-local report: LEC iff type/proof constants 8/13, LEC obstruction
iff 8/10 (the exact current observation supersedes earlier counts for
this run), Qi Slot injectivity 6/17. LEC reports Classical.choice only;
Qi reports the three standard axioms. Qi scratch exited 1 on original
later theorem nativeC60GaugeSlot_surjective, line 124: unnecessarySimpa.
Neither MCP nor independent runner ran. Do not treat partial output as
admitted.

Root cause: canonical lakefile.toml blob
947bac41f9535a7ba2ef03a93081cdfbc1b946f7 explicitly sets
linter.unnecessarySimpa=false in its pre-existing KuuOSFormal leanOptions
for preserved source. Lake's module setup passes library leanOptions;
plain lake env lean does not reproduce that library setup. Pinned Lean
Lake Config/LeanLib.lean and Build/Module.lean confirm the mechanism.
R2 verifies the exact existing Lake blob, reads its fixed eight options,
and passes precisely those plus the existing weak.sorryAsError=true to
the direct scratch compilation. Strict warningAsError=true remains.
No additional linter exemption, proof rewrite, source trim, root or pin
change is made. Canonical config drift fails closed. Record the actual
options in both runner receipts, compare them on independent observation.

## R3: TOML dotted-key decoding (2026-11-24)

R2 run 45340724005, job 138263468065 completed FAILURE at the
Python fixture gate (8/9 passed). Lean, MCP and independent stages
were skipped. Actual exception: NO_DATA: canonical library options differ.
The exact lakefile blob guard passed, but TOML's unquoted dotted keys
are decoded by tomllib as nested dictionaries, not flat option names.
Flatten recursively, reject invalid leaf values and duplicate flattened
keys, then compare the identical fixed canonical eight options. Retain
exact lakefile blob guard, strict checks and all original Lean sources.
Add a regression for nested dotted keys, duplicate keys and wrong types.
This is a config decoding correction, not proof or policy relaxation.
