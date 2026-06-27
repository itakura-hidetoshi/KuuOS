#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from runtime.kuuos_module_contract_v0_60 import canonical_digest


class DependencyGraphError(ValueError):
    """Raised when the module dependency graph is invalid."""


@dataclass(frozen=True)
class DependencyGraph:
    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]

    @classmethod
    def build(
        cls,
        nodes: Iterable[str],
        edges: Iterable[tuple[str, str]],
    ) -> "DependencyGraph":
        node_tuple = tuple(dict.fromkeys(nodes))
        edge_tuple = tuple(dict.fromkeys(edges))
        graph = cls(node_tuple, edge_tuple)
        errors = graph.validation_errors()
        if errors:
            raise DependencyGraphError(";".join(errors))
        return graph

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        node_set = set(self.nodes)
        for source, target in self.edges:
            if source not in node_set or target not in node_set:
                errors.append(f"edge_references_missing_node:{source}->{target}")
            if source == target:
                errors.append(f"self_dependency_forbidden:{source}")
        try:
            self.topological_order()
        except DependencyGraphError as exc:
            errors.append(str(exc))
        return errors

    def topological_order(self) -> tuple[str, ...]:
        adjacency: dict[str, set[str]] = {node: set() for node in self.nodes}
        indegree: dict[str, int] = {node: 0 for node in self.nodes}
        for source, target in self.edges:
            if source not in adjacency or target not in adjacency:
                raise DependencyGraphError("graph_references_missing_node")
            if target not in adjacency[source]:
                adjacency[source].add(target)
                indegree[target] += 1

        ready = sorted(node for node, degree in indegree.items() if degree == 0)
        result: list[str] = []
        while ready:
            node = ready.pop(0)
            result.append(node)
            for target in sorted(adjacency[node]):
                indegree[target] -= 1
                if indegree[target] == 0:
                    ready.append(target)
                    ready.sort()

        if len(result) != len(self.nodes):
            blocked = sorted(node for node, degree in indegree.items() if degree > 0)
            raise DependencyGraphError("dependency_cycle:" + ",".join(blocked))
        return tuple(result)

    def predecessors(self, node: str) -> tuple[str, ...]:
        if node not in self.nodes:
            raise DependencyGraphError("node_not_found")
        return tuple(sorted(source for source, target in self.edges if target == node))

    def successors(self, node: str) -> tuple[str, ...]:
        if node not in self.nodes:
            raise DependencyGraphError("node_not_found")
        return tuple(sorted(target for source, target in self.edges if source == node))

    def to_dict(self) -> dict[str, object]:
        return {
            "nodes": list(self.nodes),
            "edges": [[source, target] for source, target in self.edges],
            "topological_order": list(self.topological_order()),
        }

    @property
    def digest(self) -> str:
        return canonical_digest(self.to_dict())


def graph_from_provider_map(
    consumer_requirements: Mapping[str, tuple[str, ...]],
    providers: Mapping[str, str],
) -> DependencyGraph:
    nodes = tuple(consumer_requirements)
    edges: list[tuple[str, str]] = []
    for consumer, requirements in consumer_requirements.items():
        for requirement in requirements:
            provider = providers.get(requirement)
            if provider is None:
                raise DependencyGraphError(f"missing_provider:{requirement}")
            if provider not in consumer_requirements:
                raise DependencyGraphError(f"provider_not_registered:{provider}")
            edges.append((provider, consumer))
    return DependencyGraph.build(nodes, edges)
