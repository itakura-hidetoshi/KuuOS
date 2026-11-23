# CodeAI prior-proof recall gate v0.1 — 2026-11-24

Problem: PR #3637's six independently checked declarations provide a typed
north-C60 sector bridge, but they do not establish the mathematical novelty of
the five-phase/physical-slot correspondence. Prior proof and repair memory must
be consulted before candidate generation, not only after a failure.

Canonical source observation: 61a75099b6f989b7b68a977af2c264b3820cd2b6. Source anchors:

- QiWuxingNativeC60GaugeV3_4.lean (836a0cccc0263e33d652da6b9391e4d5c07cb368):
  nativeC60GaugeSlot_injective/surjective, nativeC60Gauge_sheng_ke_distinct.
- QiWuxingPentagonUnifiedV3_5.lean (c1b8a0997804efc10cccc44bc8432a2441e37f58):
  fivefoldSlotEquiv, fivefoldSide_endpoints, fivefoldPhysicalEdge_joins.
- QiWuxingGK5AFPhysicalCategoricalObstructionV3_9.lean
  (8af5aec40f0e26c104602171048752359b3d0602): fivefoldOriginalDart_phase_injective.
- QiWuxingGK5AGOriginalNorthHistoryDescentV4_0.lean
  (da532424d1331294d9f1f137e97da55eea4b271e): fivefoldGK5AGNorthRotationCount_noPhysicalP92Descent.
- PolygonNativeF55P94DK5FiveStageTypedShell.lean
  (8fe81aefb66486a906fee90c53a835eb99b8dccf): northK5TypedVertex_physical_five_sectors.
- PR #3637 source b4a06764bad407d521ead9b7ceaeba6598ff568b on
  173f5e1da69d4385f358251691d81835f5e2535c: new carrier type, not evidence of
  new phase-to-slot mathematics. Keep Draft/HOLD on novelty. The exact
  slot-to-sector adapter may be useful if an actual downstream consumer needs it.

## Required research path

Fresh canonical GitHub MCP HEAD and source -> prior-proof search across all live
Lean families, past PRs, workbench and version-bound MemoryOS -> read complete
relevant source, imports, theorem signatures and obstructions -> classify
single target statement -> only necessary bridge or unproved delta may reach
candidate generation -> direct pinned Lean and real Lean MCP -> separate
independent CI -> conditional memory update. Revalidate source blob and actual
dependencies rather than discarding old proofs merely because HEAD changed.

Use `python3 scripts/codeai_prior_proof_recall_gate_v0_1.py --head <observed-sha>
--term fivefoldSlotEquiv --term fivefoldSide_endpoints > recall.json` against
the exact materialized canonical source. Search terms must include relevant
synonyms and known names from the workbench, not merely the proposed new name.
The receipt includes actual source inventory digest, every literal hit and
Git blob. Add a review JSON with receipt_digest, target, assumptions, reviewer,
request (reuse/bridge/new), comparisons (one per hit file: path, blob, line,
declaration, relation, reason), delta (unproved obligation) and consumer (for
bridge). Relations: equivalent, specialization, direct_derivation,
prerequisite, obstruction, distinct, irrelevant, unresolved.
Run the same tool with --head, --receipt recall.json --review review.json.
All prior source hits must be dispositioned. Stale, missing or unresolved
evidence holds. Duplicate + new holds. A necessary typed adapter is not
novelty. Positive admission is only an advisory delta proposal, never proof.

The Python scan covers literal matches in the local formal/ and lean/ roots;
it does not prove completeness of semantic retrieval, establish Git checkout
identity, inspect other branches by itself, compare Lean types in the kernel,
or grant authority. GitHub MCP pins/reads and actual source/type comparisons
remain mandatory. A search miss is not evidence of novelty. The tool does
not retroactively alter or require reproving previously certified Lean.
