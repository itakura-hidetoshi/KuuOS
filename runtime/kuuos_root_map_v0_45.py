#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass

VERSION = "kuuos_root_map_v0_45"
DEPENDS_ON = "kuuos_overview_index_v0_44"
CURRENT_CHECK = "runtime/kuuos_current_check.py"


@dataclass(frozen=True)
class RootMapNode:
    node_id: str
    path: str
    layer: str
    upstream: tuple[str, ...]


ROOT_MAP_NODES: tuple[RootMapNode, ...] = (
    RootMapNode("current-check", "runtime/kuuos_current_check.py", "root", ()),
    RootMapNode("sequence", "runtime/kuuos_current_root_sequence_v0_41.py", "ordering", ("current-check",)),
    RootMapNode("manifest-index", "runtime/kuuos_manifest_index_v0_42.py", "metadata", ("sequence",)),
    RootMapNode("docs-index", "runtime/kuuos_docs_index_v0_43.py", "documentation", ("manifest-index",)),
    RootMapNode("overview-index", "runtime/kuuos_overview_index_v0_44.py", "overview", ("docs-index",)),
    RootMapNode("root-map", "runtime/kuuos_root_map_v0_45.py", "map", ("overview-index",)),
)


def node_ids() -> tuple[str, ...]:
    return tuple(node.node_id for node in ROOT_MAP_NODES)


def node_paths() -> tuple[str, ...]:
    return tuple(node.path for node in ROOT_MAP_NODES)


def upstream_ids() -> tuple[str, ...]:
    seen: list[str] = []
    for node in ROOT_MAP_NODES:
        seen.extend(node.upstream)
    return tuple(seen)


def root_map_issues() -> tuple[str, ...]:
    issues: list[str] = []
    ids = node_ids()
    if len(ids) != len(set(ids)):
        issues.append("duplicate_node_id")
    if len(node_paths()) != len(set(node_paths())):
        issues.append("duplicate_node_path")
    if not ROOT_MAP_NODES:
        issues.append("empty_root_map")
    known = set(ids)
    root_nodes = [node.node_id for node in ROOT_MAP_NODES if not node.upstream]
    if root_nodes != ["current-check"]:
        issues.append("invalid_root_node:" + ",".join(root_nodes))
    for node in ROOT_MAP_NODES:
        if not node.path:
            issues.append("missing_path:" + node.node_id)
        if not node.layer:
            issues.append("missing_layer:" + node.node_id)
        for upstream in node.upstream:
            if upstream not in known:
                issues.append("unknown_upstream:" + node.node_id + ":" + upstream)
            if upstream == node.node_id:
                issues.append("self_upstream:" + node.node_id)
    required = {"current-check", "sequence", "manifest-index", "docs-index", "overview-index", "root-map"}
    missing = required.difference(known)
    if missing:
        issues.append("missing_root_map_node:" + ",".join(sorted(missing)))
    return tuple(issues)


def verify_root_map() -> bool:
    return not root_map_issues()


def as_markdown() -> str:
    rows = ["| Node | Path | Layer | Upstream |", "|---|---|---|---|"]
    for node in ROOT_MAP_NODES:
        upstream = ", ".join(node.upstream) if node.upstream else "root"
        rows.append(f"| {node.node_id} | `{node.path}` | {node.layer} | {upstream} |")
    return "\n".join(rows)


if __name__ == "__main__":
    problems = root_map_issues()
    if problems:
        for item in problems:
            print(item)
        raise SystemExit(1)
    print(as_markdown())
    raise SystemExit(0)
