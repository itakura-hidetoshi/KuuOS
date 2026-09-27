#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

VERSION = "kuuos_runtime_development_mcp_capability_routing_v7_24"
REGISTRY_VERSION = "kuuos_development_mcp_capability_registry_manifest_v7_16"

READY = "KUUOS_DEVELOPMENT_MCP_ROUTING_READY"
PARTIAL = "KUUOS_DEVELOPMENT_MCP_ROUTING_PARTIAL"
BLOCKED = "KUUOS_DEVELOPMENT_MCP_ROUTING_BLOCKED"

USABLE_STATUSES = {"verified_compatible", "integrated_existing"}
READ_ONLY_PRIVILEGES = {"read_only", "read_only_network", "diagnostic_read_mostly"}
WRITE_CAPABLE_PRIVILEGES = {
    "mixed_read_write",
    "analysis_plus_optional_local_execution",
    "browser_effect",
    "orchestrator",
}

TASK_KINDS = {
    "lean_ci_repair",
    "remote_repository_observation",
    "local_worktree_review",
    "external_library_docs",
    "mcp_spec_research",
    "browser_functional_validation",
    "browser_debugging",
    "deployment_debugging",
    "database_debugging",
    "multi_mcp_orchestration",
}

AUTHORITY_KEYS = {
    "github_official": "github_write_authority_ready",
    "git_reference": "workspace_write_authority_ready",
    "filesystem_reference": "workspace_write_authority_ready",
    "lean_lsp": "workspace_write_authority_ready",
    "playwright": "browser_effect_authority_ready",
    "chrome_devtools": "browser_effect_authority_ready",
    "docker_mcp_gateway": "mcp_orchestration_authority_ready",
    "vercel_existing": "vercel_write_authority_ready",
    "supabase_existing": "supabase_write_authority_ready",
    "neon_existing": "neon_write_authority_ready",
}

FACT_AUTHORITIES = {
    "github_official": "remote_repository_and_ci_state",
    "git_reference": "local_revision_and_diff_state",
    "filesystem_reference": "current_working_bytes",
    "lean_lsp": "lean_semantic_state_for_bound_bytes",
    "context7": "current_external_library_documentation",
    "mcp_docs": "current_mcp_specification",
    "mcp_fetch": "generic_external_content",
    "playwright": "functional_browser_observation",
    "chrome_devtools": "browser_console_network_performance_observation",
    "docker_mcp_gateway": "mcp_orchestration_surface",
    "vercel_existing": "vercel_deployment_state",
    "supabase_existing": "supabase_project_state",
    "neon_existing": "neon_project_state",
    "sentry": "instrumented_runtime_diagnostic_state",
}


@dataclass(frozen=True)
class DevelopmentMCPRoutingResult:
    version: str
    status: str
    task_id: str
    task_kind: str
    route_count: int
    required_route_count: int
    unavailable_required_count: int
    authority_required_count: int
    degraded: bool
    routes: list[dict[str, Any]]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _registry_servers(registry: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    raw = registry.get("servers", [])
    if not isinstance(raw, list):
        return {}
    return {
        str(item.get("server_id")): item
        for item in raw
        if isinstance(item, Mapping) and item.get("server_id")
    }


def _server_available(
    server_id: str,
    server: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> bool:
    unavailable = set(_strings(environment.get("unavailable_server_ids")))
    if server_id in unavailable:
        return False
    status = str(server.get("status", ""))
    if status in USABLE_STATUSES:
        return True
    if server_id == "sentry" and status == "optional_when_instrumented":
        return environment.get("sentry_project_configured") is True
    return False


def _authority_ready(server_id: str, environment: Mapping[str, Any]) -> bool:
    key = AUTHORITY_KEYS.get(server_id)
    return True if key is None else environment.get(key) is True


def _route(
    *,
    server_id: str,
    role: str,
    fact_plane: str,
    purpose: str,
    required: bool,
    server: Mapping[str, Any],
    environment: Mapping[str, Any],
    request_write: bool,
) -> dict[str, Any]:
    privilege = str(server.get("privilege_class", ""))
    available = _server_available(server_id, server, environment)
    write_capable = privilege in WRITE_CAPABLE_PRIVILEGES
    authority_ready = _authority_ready(server_id, environment)

    if not available:
        activation_state = "unavailable"
        effective_mode = "unavailable"
    elif request_write and write_capable and not authority_ready:
        activation_state = "authority_required"
        effective_mode = "candidate_without_write_authority"
    elif request_write and write_capable and authority_ready:
        activation_state = "ready"
        effective_mode = "write_candidate"
    elif privilege == "browser_effect":
        activation_state = "ready"
        effective_mode = "inspection_only"
    elif privilege == "orchestrator":
        activation_state = "ready"
        effective_mode = "orchestration_plan_only"
    else:
        activation_state = "ready"
        effective_mode = "read_only"

    return {
        "server_id": server_id,
        "role": role,
        "fact_plane": fact_plane,
        "purpose": purpose,
        "required": required,
        "registry_status": server.get("status"),
        "activation_state": activation_state,
        "effective_mode": effective_mode,
        "fact_authority": FACT_AUTHORITIES.get(server_id, "provider_specific_state"),
        "write_capability_present": write_capable,
        "write_authority_ready": authority_ready if write_capable else True,
        "source_authority_transferred": False,
    }


def _add(
    routes: list[dict[str, Any]],
    servers: Mapping[str, Mapping[str, Any]],
    environment: Mapping[str, Any],
    *,
    server_id: str,
    role: str,
    fact_plane: str,
    purpose: str,
    required: bool = True,
    request_write: bool = False,
) -> None:
    server = servers.get(server_id)
    if server is None:
        routes.append(
            {
                "server_id": server_id,
                "role": role,
                "fact_plane": fact_plane,
                "purpose": purpose,
                "required": required,
                "registry_status": "missing",
                "activation_state": "unavailable",
                "effective_mode": "unavailable",
                "fact_authority": FACT_AUTHORITIES.get(
                    server_id, "provider_specific_state"
                ),
                "write_capability_present": False,
                "write_authority_ready": False,
                "source_authority_transferred": False,
            }
        )
        return
    routes.append(
        _route(
            server_id=server_id,
            role=role,
            fact_plane=fact_plane,
            purpose=purpose,
            required=required,
            server=server,
            environment=environment,
            request_write=request_write,
        )
    )


def route_development_mcp_task(
    *,
    registry: Mapping[str, Any],
    request: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> DevelopmentMCPRoutingResult:
    blockers: list[str] = []
    warnings: list[str] = []

    if registry.get("version") != REGISTRY_VERSION:
        blockers.append("registry_version_invalid")
    if registry.get("repository") != "itakura-hidetoshi/KuuOS":
        blockers.append("registry_repository_invalid")

    task_id = str(request.get("task_id", "")).strip()
    task_kind = str(request.get("task_kind", "")).strip()
    if not task_id:
        blockers.append("task_id_missing")
    if task_kind not in TASK_KINDS:
        blockers.append("task_kind_invalid")

    target_path = str(request.get("target_path", "")).strip()
    provider = str(request.get("provider", "")).strip().lower()
    needs_external_docs = request.get("needs_external_docs") is True
    needs_mcp_spec = request.get("needs_mcp_spec") is True
    needs_browser_diagnostics = request.get("needs_browser_diagnostics") is True
    request_write = request.get("request_write") is True

    servers = _registry_servers(registry)
    routes: list[dict[str, Any]] = []

    if not blockers:
        if task_kind == "lean_ci_repair":
            _add(
                routes,
                servers,
                environment,
                server_id="github_official",
                role="primary",
                fact_plane="remote_ci",
                purpose="observe exact PR/head/workflow failure before editing",
                request_write=False,
            )
            _add(
                routes,
                servers,
                environment,
                server_id="filesystem_reference",
                role="primary",
                fact_plane="working_bytes",
                purpose="read and edit the exact current Lean source bytes",
                request_write=request_write,
            )
            _add(
                routes,
                servers,
                environment,
                server_id="lean_lsp",
                role="primary",
                fact_plane="lean_semantics",
                purpose="obtain goals diagnostics hover and local theorem search for current bytes",
                request_write=request_write,
            )
            _add(
                routes,
                servers,
                environment,
                server_id="git_reference",
                role="corroborating",
                fact_plane="local_diff",
                purpose="review local revision and diff without replacing GitHub remote truth",
                request_write=request_write,
            )
            if needs_external_docs:
                _add(
                    routes,
                    servers,
                    environment,
                    server_id="context7",
                    role="corroborating",
                    fact_plane="external_docs",
                    purpose="consult current external library/API documentation",
                    required=False,
                )
            if needs_mcp_spec:
                _add(
                    routes,
                    servers,
                    environment,
                    server_id="mcp_docs",
                    role="corroborating",
                    fact_plane="mcp_spec",
                    purpose="consult current official MCP specification",
                    required=False,
                )

        elif task_kind == "remote_repository_observation":
            _add(
                routes,
                servers,
                environment,
                server_id="github_official",
                role="primary",
                fact_plane="remote_repository",
                purpose="observe canonical remote branch PR Actions and collaboration state",
                request_write=request_write,
            )

        elif task_kind == "local_worktree_review":
            _add(
                routes,
                servers,
                environment,
                server_id="git_reference",
                role="primary",
                fact_plane="local_revision",
                purpose="inspect local HEAD status staged and unstaged differences",
                request_write=request_write,
            )
            _add(
                routes,
                servers,
                environment,
                server_id="filesystem_reference",
                role="corroborating",
                fact_plane="working_bytes",
                purpose="inspect current file bytes inside repository root",
                request_write=request_write,
            )
            if target_path.endswith(".lean"):
                _add(
                    routes,
                    servers,
                    environment,
                    server_id="lean_lsp",
                    role="corroborating",
                    fact_plane="lean_semantics",
                    purpose="check semantic freshness of selected Lean bytes",
                    required=False,
                )

        elif task_kind == "external_library_docs":
            _add(
                routes,
                servers,
                environment,
                server_id="context7",
                role="primary",
                fact_plane="external_docs",
                purpose="retrieve current version-specific external library/API documentation",
            )
            _add(
                routes,
                servers,
                environment,
                server_id="mcp_fetch",
                role="fallback",
                fact_plane="external_content",
                purpose="fetch public source material when indexed documentation is insufficient",
                required=False,
            )

        elif task_kind == "mcp_spec_research":
            _add(
                routes,
                servers,
                environment,
                server_id="mcp_docs",
                role="primary",
                fact_plane="mcp_spec",
                purpose="query the current official Model Context Protocol specification",
            )
            _add(
                routes,
                servers,
                environment,
                server_id="context7",
                role="corroborating",
                fact_plane="external_docs",
                purpose="retrieve current SDK examples without replacing official spec authority",
                required=False,
            )
            _add(
                routes,
                servers,
                environment,
                server_id="mcp_fetch",
                role="fallback",
                fact_plane="external_content",
                purpose="fetch exact upstream public source when needed",
                required=False,
            )

        elif task_kind == "browser_functional_validation":
            _add(
                routes,
                servers,
                environment,
                server_id="playwright",
                role="primary",
                fact_plane="functional_browser",
                purpose="perform deterministic functional navigation and accessibility validation",
                request_write=request_write,
            )
            if needs_browser_diagnostics:
                _add(
                    routes,
                    servers,
                    environment,
                    server_id="chrome_devtools",
                    role="corroborating",
                    fact_plane="browser_diagnostics",
                    purpose="inspect console network or performance diagnostics",
                    required=False,
                )

        elif task_kind == "browser_debugging":
            _add(
                routes,
                servers,
                environment,
                server_id="chrome_devtools",
                role="primary",
                fact_plane="browser_diagnostics",
                purpose="inspect console network performance and live Chrome state",
                request_write=request_write,
            )
            _add(
                routes,
                servers,
                environment,
                server_id="playwright",
                role="corroborating",
                fact_plane="functional_browser",
                purpose="reproduce deterministic browser behavior",
                required=False,
            )

        elif task_kind == "deployment_debugging":
            if provider == "vercel":
                _add(
                    routes,
                    servers,
                    environment,
                    server_id="vercel_existing",
                    role="primary",
                    fact_plane="deployment",
                    purpose="inspect deployment build runtime logs and deployment state",
                    request_write=request_write,
                )
            else:
                blockers.append("deployment_provider_unsupported")
            _add(
                routes,
                servers,
                environment,
                server_id="github_official",
                role="corroborating",
                fact_plane="remote_ci",
                purpose="correlate deployment state with repository exact head and Actions",
                required=False,
            )

        elif task_kind == "database_debugging":
            db_server = {
                "supabase": "supabase_existing",
                "neon": "neon_existing",
            }.get(provider)
            if db_server is None:
                blockers.append("database_provider_unsupported")
            else:
                _add(
                    routes,
                    servers,
                    environment,
                    server_id=db_server,
                    role="primary",
                    fact_plane="database",
                    purpose="inspect provider project schema query logs and runtime state",
                    request_write=request_write,
                )
                if needs_external_docs:
                    _add(
                        routes,
                        servers,
                        environment,
                        server_id="context7",
                        role="corroborating",
                        fact_plane="external_docs",
                        purpose="consult current provider SDK/API documentation",
                        required=False,
                    )

        elif task_kind == "multi_mcp_orchestration":
            _add(
                routes,
                servers,
                environment,
                server_id="docker_mcp_gateway",
                role="primary",
                fact_plane="orchestration",
                purpose="isolate aggregate and route multiple local MCP servers",
                request_write=request_write,
            )

    required_routes = [r for r in routes if r.get("required") is True]
    unavailable_required = [
        r for r in required_routes if r.get("activation_state") == "unavailable"
    ]
    authority_required = [
        r for r in routes if r.get("activation_state") == "authority_required"
    ]
    degraded = bool(
        unavailable_required
        or authority_required
        or any(
            r.get("role") == "fallback" and r.get("activation_state") == "ready"
            for r in routes
        )
    )

    if blockers or unavailable_required:
        status = BLOCKED
    elif authority_required:
        status = PARTIAL
    else:
        status = READY

    if any(r.get("server_id") == "sentry" for r in routes):
        warnings.append("sentry_is_optional_instrumented_runtime_only")

    if task_kind == "lean_ci_repair" and target_path and not target_path.endswith(".lean"):
        warnings.append("lean_ci_repair_target_path_is_not_lean_file")

    return DevelopmentMCPRoutingResult(
        VERSION,
        status,
        task_id,
        task_kind,
        len(routes),
        len(required_routes),
        len(unavailable_required),
        len(authority_required),
        degraded,
        routes,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
