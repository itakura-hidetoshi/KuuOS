#!/usr/bin/env python3
"""Read-only exact-tree catalog export, using GitHub observation or supplied MCP receipt."""
from __future__ import annotations

import argparse
import gzip
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.kuuos_codeai_prior_proof_library_index_v0_3 import (
    REPOSITORY, SCOPES, SHA, build_catalog, search_catalog,
)


def github_observation(head: str, scope: str) -> dict:
    if not SHA.fullmatch(head) or scope not in SCOPES or scope == "fixture":
        raise ValueError("invalid exact GitHub source request")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "KuuOS-source-recall-v03"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token

    def fetch(suffix):
        url = "https://api.github.com/repos/" + REPOSITORY + suffix
        with urlopen(Request(url, headers=headers), timeout=45) as response:
            return json.load(response)

    commit = fetch("/git/commits/" + head)
    if commit["sha"] != head or not SHA.fullmatch(commit["tree"]["sha"]):
        raise ValueError("GitHub commit binding mismatch")
    if scope == "canonical_main":
        branch = fetch("/branches/main")
        if branch["commit"]["sha"] != head:
            raise ValueError("canonical main changed; reobserve before recall")
    tree = fetch("/git/trees/" + commit["tree"]["sha"])
    if tree["sha"] != commit["tree"]["sha"] or tree.get("truncated") is not False:
        raise ValueError("GitHub tree incomplete or mismatched")
    return {"repository": REPOSITORY, "source_head": head, "source_tree": tree["sha"],
            "scope": scope, "truncated": False,
            "root_entries": [{k: row[k] for k in ("path", "mode", "sha")} for row in tree["tree"]]}


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--source-head")
    p.add_argument("--scope", choices=sorted(SCOPES))
    p.add_argument("--observation", type=Path, help="Exact externally observed GitHub commit/tree JSON")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    if args.observation:
        if args.source_head or args.scope:
            p.error("use either explicit observation or source head and scope")
        observation = json.loads(args.observation.read_text())
    elif args.source_head and args.scope:
        observation = github_observation(args.source_head, args.scope)
    else:
        p.error("exact GitHub source observation required")
    out = args.out.resolve()
    if any(out.is_relative_to((args.root / name).resolve()) for name in ("formal", "lean")):
        raise ValueError("catalog output must not modify proof sources")
    out.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog(args.root, observation)
    # Save the actual source catalog with an external SHA/tree binding.
    with gzip.open(out / "catalog.json.gz", "wt", encoding="utf-8", compresslevel=6) as stream:
        json.dump(catalog, stream, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    write_json(out / "observation.json", observation)
    summary = {k: v for k, v in catalog.items() if k != "files"}
    write_json(out / "summary.json", summary)
    # Real corpus regression: do not provide historical theorem names to the
    # search. One subject is outside the manually indexed C60/GK5 topics.
    queries = {
        "living-engi": "source aware overlap descent",
        "higher-cell": "peiffer normal kernel",
        "c60-gauge": "c60 gauge covariant",
    }
    for name, query in queries.items():
        result = search_catalog(catalog, query, limit=500)
        write_json(out / (name + ".json"), result)
        print("LIBRARY_RECALL_QUERY", name, result["total_hits"], result["status"], flush=True)
    print("LIBRARY_CATALOG_SUMMARY", json.dumps(summary, sort_keys=True), flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
