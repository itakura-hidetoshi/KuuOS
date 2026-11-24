# CodeAI repository-wide prior-proof library index v0.3

The v0.2 subject catalog covers a curated set of six themes and 67 anchors.
That must not become the research boundary. v0.3 adds a reproducible
read-only index of every Lean source file in the live formal/ and lean/
subtrees. The source parser reuses the original full-source repair scanner's
declaration pattern and import extraction and the sandbox's nested-comment
and string masker. Existing theorem bodies, public roots, pins, curated
anchors and repair memory are unchanged.

## Source identity

The caller first obtains the current canonical commit, its root tree and
all direct root entries from GitHub MCP. The script accepts this explicit
observation JSON or the GitHub Actions read-only API observation of its
exact checkout. It reconstructs Git tree object IDs (names, modes, contents)
for both source subtrees, and checks the actual toolchain, manifest and
lakefile blobs. Added, removed or changed files fail closed. An external
observation of the commit-to-tree association remains mandatory: a local
digest or caller-supplied SHA is not authentication. The CI scope distinguishes
canonical main, research branch and PR test merge.

## Retrieval and limits

The compressed index includes each actual Lean source path/blob, module-path
hint, source-line declarations, bounded lexical signature previews,
lexical imports and existing print-axiom requests. It is rebuilt rather than
reusing stale snapshots after a change. The workflow regenerates an artifact
on canonical source changes. The export is a retrieval aid, not an elaborated
Lean environment or a proof-history certificate. Anonymous/macro-generated
declarations, actual dependent types and constant dependencies require real
Lean/MCP inspection; lexical parser gaps remain explicit. The catalog does
not claim completeness of semantic retrieval.

The search accepts ordinary research language or explicit translated concept
terms, with deterministic all/any matching against declaration, signature
and path. No name need be supplied. Japanese not covered by a lexical query
must be translated/expanded explicitly or use the existing subject catalog.
A search miss, truncated result or unresolved parse gap is HOLD, not novelty.
The actual-CI regression uses LEC source-aware overlap descent (outside the
curated C60 catalog) and Peiffer context history without naming their prior
theorems in the queries.

## Research admission

Recompute the catalog and library receipt against the fresh observed main.
Record a per-declaration relation, exact source blob/signature preview digest,
reason, assumptions comparison and conclusion comparison, plus explicit
review of parser gaps. All selected hits must be dispositioned. A duplicate
blocks a new-result proposal even if other lexical matches are distinct.
`build_library_research_synthesis` adds this check before the prior v0.2
subject gate (when applicable) or v0.1 exact source review for additional
subjects; complete relevant source text must reach the original CodeAI
provider. It never grants proof or execution authority. Review assertions,
literal signatures, and graph/import candidates are not kernel comparisons.
Read full declarations, section hypotheses, imports, actual proof terms and
pinned Lean types before claiming an unproved difference.

The first registry registration retains full Governance and Strict Lean.
No existing audit-control rule, root, pin or theorem is weakened.
