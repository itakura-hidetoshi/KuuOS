#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any, Mapping, Sequence

from runtime.kuuos_connection_candidate_receipt_v0_62 import (
    ConnectionCandidatePolicy,
    ConnectionCandidateReceipt,
    VERSION,
    evaluate_connection_candidate,
)
from runtime.kuuos_discrete_gauge_connection_v0_60 import ChartPair, KuuConnection
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import (
    SignedPermutation,
    canonical_digest,
)
from runtime.kuuos_os_curvature_holonomy_v0_61 import OSGaugeBundle


@dataclass(frozen=True)
class ConnectionCandidateProposal:
    source_bundle_digest: str
    route: str
    evaluated_candidates: int
    admissible_candidates: int
    selected_connection: KuuConnection | None
    selected_receipt: ConnectionCandidateReceipt | None
    candidate_only: bool = True
    state_write_performed: bool = False
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "source_bundle_digest": self.source_bundle_digest,
            "route": self.route,
            "evaluated_candidates": self.evaluated_candidates,
            "admissible_candidates": self.admissible_candidates,
            "selected_connection": (
                None if self.selected_connection is None
                else self.selected_connection.to_dict()
            ),
            "selected_receipt": (
                None if self.selected_receipt is None
                else self.selected_receipt.to_dict()
            ),
            "candidate_only": self.candidate_only,
            "state_write_performed": self.state_write_performed,
        }


def _domain(connection: KuuConnection) -> tuple[ChartPair, ...]:
    return tuple(sorted(connection.transports))


def _deduplicate(
    source: SignedPermutation,
    replacements: Sequence[SignedPermutation],
    bundle: OSGaugeBundle,
) -> tuple[SignedPermutation, ...]:
    result: list[SignedPermutation] = []
    seen: set[str] = set()
    for element in (source, *replacements):
        bundle.group.require_admissible(element)
        digest = canonical_digest(element.to_dict())
        if digest not in seen:
            seen.add(digest)
            result.append(element)
    return tuple(result)


def search_connection_candidates(
    source_bundle: OSGaugeBundle,
    replacement_catalog: Mapping[ChartPair, Sequence[SignedPermutation]],
    *,
    policy: ConnectionCandidatePolicy = ConnectionCandidatePolicy(),
) -> ConnectionCandidateProposal:
    source_domain = _domain(source_bundle.connection)
    unknown_pairs = set(replacement_catalog).difference(source_domain)
    if unknown_pairs:
        raise ValueError("replacement_catalog_outside_connection_domain")

    option_sets: list[tuple[SignedPermutation, ...]] = []
    catalog_product = 1
    for pair in source_domain:
        options = _deduplicate(
            source_bundle.connection.transports[pair],
            replacement_catalog.get(pair, ()),
            source_bundle,
        )
        option_sets.append(options)
        catalog_product *= len(options)
        if catalog_product > policy.max_catalog_product:
            raise ValueError("replacement_catalog_product_limit_exceeded")

    evaluated = 0
    admissible: list[
        tuple[
            tuple[float, int, str],
            KuuConnection,
            ConnectionCandidateReceipt,
        ]
    ] = []
    for elements in product(*option_sets):
        connection = KuuConnection(
            source_bundle.group,
            dict(zip(source_domain, elements, strict=True)),
        )
        receipt = evaluate_connection_candidate(
            source_bundle,
            connection,
            policy=policy,
        )
        evaluated += 1
        if receipt.admissible:
            score = (
                receipt.candidate_curvature.total_curvature,
                len(receipt.changed_links),
                receipt.candidate_connection_digest,
            )
            admissible.append((score, connection, receipt))

    source_digest = canonical_digest(source_bundle.to_dict())
    if not admissible:
        return ConnectionCandidateProposal(
            source_bundle_digest=source_digest,
            route="PRESERVE_SOURCE_CONNECTION",
            evaluated_candidates=evaluated,
            admissible_candidates=0,
            selected_connection=None,
            selected_receipt=None,
        )

    _, connection, receipt = min(admissible, key=lambda item: item[0])
    return ConnectionCandidateProposal(
        source_bundle_digest=source_digest,
        route="PROPOSE_CONNECTION_UPDATE",
        evaluated_candidates=evaluated,
        admissible_candidates=len(admissible),
        selected_connection=connection,
        selected_receipt=receipt,
    )
