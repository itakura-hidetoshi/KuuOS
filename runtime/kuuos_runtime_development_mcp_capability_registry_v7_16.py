#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence

VERSION = "kuuos_runtime_development_mcp_capability_registry_v7_16"
REGISTRY_VERSION = "kuuos_development_mcp_capability_registry_manifest_v7_16"

READY = "KUUOS_DEVELOPMENT_MCP_PROFILE_READY"
PARTIAL = "KUUOS_DEVELOPMENT_MCP_PROFILE_PARTIAL"
BLOCKED = "KUUOS_DEVELOPMENT_MCP_PROFILE_BLOCKED"

VALID_SOURCE_KINDS = {
    "official",
    "official_reference",
    "official_vendor",
    "vendor_open_source",
    "community_research",
    "existing_kuuos_connector",
}
VALID_STATUSES = {
    "integrated_existing",
    "recommended_sandboxed",
    "experimental_high_value",
    "verified_compatible",
    "recommended_read_only",
    "recommended_orchestration",
    "optional_when_instrumented",
}
VALID_PRIVILEGES = {
    "read_only",
    "read_only_network",
    "mixed_read_write",
    "analysis_plus_optional_local_execution",
    "browser_effect",
    "orchestrator",
    "diagnostic_read_mostly",
}


@dataclass(frozen=True)
class DevelopmentMCPProfileResult:
    version: str
    status: str
    profile_name: str
    selected_server_count: int
    ready_server_count: int
    experimental_server_count: int
    authority_required_count: int
    environment_missing_count: int
    optional_unconfigured_count: int
    blockers: list[str]
    server_states: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _contains_secret_material(value: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            lowered = str(key).lower()
            if lowered in {
                "token",
                "password",
                "secret",
                "api_key",
                "access_token",
                "personal_access_token",
            } and child not in ("", None):
                errors.append("credential_material_present:" + child_path)
            errors.extend(_contains_secret_material(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_contains_secret_material(child, f"{path}[{index}]"))
    return errors


def validate_registry(registry: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("version") != REGISTRY_VERSION:
        errors.append("registry_version_invalid")
    if registry.get("repository") != "itakura-hidetoshi/KuuOS":
        errors.append("registry_repository_invalid")

    boundary = _m(registry.get("boundaries"))
    required_false = (
        "registry_entry_is_authority",
        "registry_entry_auto_starts_server",
        "source_authority_transferred",
        "credentials_persisted",
        "provider_failure_blocks_other_servers",
        "capability_overlap_implies_semantic_identity",
        "experimental_server_auto_enabled",
    )
    for key in required_false:
        if boundary.get(key) is not False:
            errors.append(key + "_must_be_false")
    if boundary.get("write_capability_requires_independent_authority") is not True:
        errors.append("write_capability_independent_authority_not_true")
    if boundary.get("multiple_mcp_servers_may_present_overlapping_capabilities") is not True:
        errors.append("overlapping_capability_presentations_not_true")

    profiles = registry.get("profiles")
    servers = registry.get("servers")
    if not isinstance(profiles, Mapping) or not profiles:
        errors.append("profiles_missing")
        profiles = {}
    if not isinstance(servers, list) or not servers:
        errors.append("servers_missing")
        servers = []

    seen: set[str] = set()
    by_id: dict[str, Mapping[str, Any]] = {}

    for index, raw in enumerate(servers):
        if not isinstance(raw, Mapping):
            errors.append(f"server_{index}_not_object")
            continue
        server_id = str(raw.get("server_id", "")).strip()
        if not server_id:
            errors.append(f"server_{index}_id_missing")
            continue
        if server_id in seen:
            errors.append("duplicate_server_id:" + server_id)
            continue
        seen.add(server_id)
        by_id[server_id] = raw

        if str(raw.get("source_kind", "")) not in VALID_SOURCE_KINDS:
            errors.append("invalid_source_kind:" + server_id)
        if str(raw.get("status", "")) not in VALID_STATUSES:
            errors.append("invalid_status:" + server_id)
        if str(raw.get("privilege_class", "")) not in VALID_PRIVILEGES:
            errors.append("invalid_privilege_class:" + server_id)
        if not _strings(raw.get("capability_families")):
            errors.append("capability_families_missing:" + server_id)
        if not _strings(raw.get("transport")):
            errors.append("transport_missing:" + server_id)
        if not str(raw.get("activation", "")).strip():
            errors.append("activation_missing:" + server_id)

        privilege = str(raw.get("privilege_class", ""))
        if privilege in {
            "mixed_read_write",
            "analysis_plus_optional_local_execution",
            "browser_effect",
            "orchestrator",
        } and not str(raw.get("write_authority_path", "")).strip():
            errors.append("write_authority_path_missing:" + server_id)

        if server_id == "github_official":
            toolsets = set(_strings(raw.get("recommended_toolsets")))
            required = {
                "context",
                "repos",
                "git",
                "issues",
                "pull_requests",
                "actions",
                "code_quality",
                "code_security",
                "dependabot",
                "secret_protection",
            }
            missing = sorted(required.difference(toolsets))
            if missing:
                errors.append(
                    "github_required_toolsets_missing:" + ",".join(missing)
                )
            if raw.get("activation") != "reuse_existing_kuuos_github_mcp_bridge":
                errors.append("github_must_reuse_existing_bridge")

        if server_id == "filesystem_reference":
            if raw.get("isolation") != "explicit_allowed_repository_root":
                errors.append("filesystem_repository_root_isolation_missing")
            if raw.get("status") == "verified_compatible":
                evidence = _m(raw.get("compatibility_evidence"))
                expected = {
                    "manifest": "manifests/kuuos_local_repository_mcp_compatibility_v7_18.json",
                    "package_version": "2026.8.31",
                    "upstream_main_sha": "f46d9578190b476b3501923ea8977d899e8db2cb",
                }
                for key, value in expected.items():
                    if str(evidence.get(key, "")) != value:
                        errors.append("filesystem_compatibility_evidence_invalid:" + key)
                if not str(evidence.get("initial_green_probe_head", "")).strip():
                    errors.append("filesystem_green_probe_head_missing")
                if not isinstance(evidence.get("initial_green_probe_run_id"), int):
                    errors.append("filesystem_green_probe_run_id_missing")

        if server_id == "git_reference" and raw.get("status") == "verified_compatible":
            evidence = _m(raw.get("compatibility_evidence"))
            expected = {
                "manifest": "manifests/kuuos_local_repository_mcp_compatibility_v7_18.json",
                "package_version": "0.6.2",
                "upstream_main_sha": "f46d9578190b476b3501923ea8977d899e8db2cb",
                "mcp_sdk_pin": "1.29.0",
            }
            for key, value in expected.items():
                if str(evidence.get(key, "")) != value:
                    errors.append("git_compatibility_evidence_invalid:" + key)
            if not str(evidence.get("initial_green_probe_head", "")).strip():
                errors.append("git_green_probe_head_missing")
            if not isinstance(evidence.get("initial_green_probe_run_id"), int):
                errors.append("git_green_probe_run_id_missing")

        if server_id == "context7" and raw.get("status") == "verified_compatible":
            evidence = _m(raw.get("compatibility_evidence"))
            expected = {
                "manifest": "manifests/kuuos_context7_mcp_compatibility_v7_20.json",
                "package_version": "4.1.1",
                "upstream_master_sha": "e275a848a420e0d11c2822f61201ee005bfd1133",
            }
            for key, value in expected.items():
                if str(evidence.get(key, "")) != value:
                    errors.append("context7_compatibility_evidence_invalid:" + key)
            if evidence.get("api_key_used") is not False:
                errors.append("context7_probe_api_key_boundary_invalid")
            if not str(evidence.get("initial_green_probe_head", "")).strip():
                errors.append("context7_green_probe_head_missing")
            if not isinstance(evidence.get("initial_green_probe_run_id"), int):
                errors.append("context7_green_probe_run_id_missing")

        if server_id == "lean_lsp":
            lean_status = str(raw.get("status", ""))
            if lean_status not in {"experimental_high_value", "verified_compatible"}:
                errors.append("lean_lsp_status_invalid")
            if lean_status == "verified_compatible":
                evidence = _m(raw.get("compatibility_evidence"))
                expected = {
                    "manifest": "manifests/kuuos_lean_lsp_mcp_compatibility_v7_17.json",
                    "package_version": "0.30.0",
                    "upstream_main_sha": "bb176c58a4f895061561685318e92b8db446f1b5",
                    "lean_toolchain": "leanprover/lean4:v4.30.0-rc2",
                    "mathlib_sha": "5450b53e5ddc75d46418fabb605edbf36bd0beb6",
                }
                for key, value in expected.items():
                    if str(evidence.get(key, "")) != value:
                        errors.append("lean_lsp_compatibility_evidence_invalid:" + key)
                if not str(evidence.get("initial_green_probe_head", "")).strip():
                    errors.append("lean_lsp_green_probe_head_missing")
                if not isinstance(evidence.get("initial_green_probe_run_id"), int):
                    errors.append("lean_lsp_green_probe_run_id_missing")
            requirements = set(_strings(raw.get("runtime_requirements")))
            for required in ("lake", "lean_project_built", "local_repository"):
                if required not in requirements:
                    errors.append("lean_lsp_requirement_missing:" + required)

        if server_id in {"playwright", "chrome_devtools"}:
            if "isolated" not in str(raw.get("isolation", "")):
                errors.append("browser_isolation_missing:" + server_id)
            if raw.get("status") == "verified_compatible":
                evidence = _m(raw.get("compatibility_evidence"))
                expected = (
                    {
                        "manifest": "manifests/kuuos_browser_mcp_compatibility_v7_21.json",
                        "package_version": "0.0.82",
                        "upstream_main_sha": "e87bb897e15a6f2af402afb0f10b45eced9e1f9b",
                    }
                    if server_id == "playwright"
                    else {
                        "manifest": "manifests/kuuos_browser_mcp_compatibility_v7_21.json",
                        "package_version": "1.10.1",
                        "upstream_main_sha": "ae0aaef884c41445d83f86f099ef211f4584b791",
                    }
                )
                for key, value in expected.items():
                    if str(evidence.get(key, "")) != value:
                        errors.append(server_id + "_compatibility_evidence_invalid:" + key)
                if evidence.get("localhost_only") is not True:
                    errors.append(server_id + "_compatibility_scope_invalid")
                if not str(evidence.get("initial_green_probe_head", "")).strip():
                    errors.append(server_id + "_green_probe_head_missing")
                if not isinstance(evidence.get("initial_green_probe_run_id"), int):
                    errors.append(server_id + "_green_probe_run_id_missing")
                if server_id == "chrome_devtools":
                    if evidence.get("usage_statistics_disabled") is not True:
                        errors.append("chrome_usage_statistics_boundary_invalid")
                    if evidence.get("performance_crux_disabled") is not True:
                        errors.append("chrome_crux_boundary_invalid")

        if server_id == "docker_mcp_gateway" and raw.get("status") == "verified_compatible":
            evidence = _m(raw.get("compatibility_evidence"))
            expected = {
                "manifest": "manifests/kuuos_docker_mcp_gateway_compatibility_v7_22.json",
                "upstream_main_sha": "a34df45d4ec0e941a9853ad768c4f6cd818966b3",
            }
            for key, value in expected.items():
                if str(evidence.get(key, "")) != value:
                    errors.append("docker_gateway_compatibility_evidence_invalid:" + key)
            for key in (
                "real_gateway_tool_discovery",
                "real_gateway_tool_forwarding",
                "network_disabled_fixture",
            ):
                if evidence.get(key) is not True:
                    errors.append("docker_gateway_compatibility_evidence_invalid:" + key)
            if not str(evidence.get("initial_green_probe_head", "")).strip():
                errors.append("docker_gateway_green_probe_head_missing")
            if not isinstance(evidence.get("initial_green_probe_run_id"), int):
                errors.append("docker_gateway_green_probe_run_id_missing")

    for profile_name, members in profiles.items():
        if not isinstance(members, list) or not members:
            errors.append("profile_empty:" + str(profile_name))
            continue
        for server_id in members:
            if str(server_id) not in by_id:
                errors.append(
                    "profile_unknown_server:"
                    + str(profile_name)
                    + ":"
                    + str(server_id)
                )

    maximal = set(_strings(profiles.get("kuuos_maximal_repository_development")))
    required_maximal = {
        "github_official",
        "git_reference",
        "filesystem_reference",
        "lean_lsp",
        "context7",
        "playwright",
        "chrome_devtools",
        "docker_mcp_gateway",
        "sentry",
        "mcp_fetch",
        "mcp_docs",
        "vercel_existing",
        "supabase_existing",
        "neon_existing",
    }
    missing_maximal = sorted(required_maximal.difference(maximal))
    if missing_maximal:
        errors.append(
            "maximal_profile_missing:" + ",".join(missing_maximal)
        )

    errors.extend(_contains_secret_material(registry))
    return sorted(set(errors))


def _requirements_missing(
    server: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> list[str]:
    missing: list[str] = []
    available = set(_strings(environment.get("available_requirements")))
    connected = set(_strings(environment.get("connected_services")))

    for requirement in _strings(server.get("runtime_requirements")):
        if requirement.endswith("_connection"):
            service = requirement[: -len("_connection")]
            if service not in connected:
                missing.append(requirement)
        elif requirement == "sentry_project":
            if environment.get("sentry_project_configured") is not True:
                missing.append(requirement)
        elif requirement == "browser_runtime":
            if "browser_runtime" not in available and "chrome" not in available:
                missing.append(requirement)
        elif requirement not in available and requirement not in {
            "network",
            "local_repository",
        }:
            missing.append(requirement)
        elif requirement == "network" and environment.get("network_allowed") is not True:
            missing.append(requirement)
        elif requirement == "local_repository" and environment.get("repository_root_bound") is not True:
            missing.append(requirement)
    return sorted(set(missing))


def _authority_ready(
    server: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> bool:
    server_id = str(server.get("server_id", ""))
    if server_id == "github_official":
        return environment.get("github_write_authority_ready") is True
    if server_id in {"git_reference", "filesystem_reference", "lean_lsp"}:
        return environment.get("workspace_write_authority_ready") is True
    if server_id in {"playwright", "chrome_devtools"}:
        return environment.get("browser_effect_authority_ready") is True
    if server_id == "docker_mcp_gateway":
        return environment.get("mcp_orchestration_authority_ready") is True
    if server_id == "vercel_existing":
        return environment.get("vercel_write_authority_ready") is True
    if server_id == "supabase_existing":
        return environment.get("supabase_write_authority_ready") is True
    if server_id == "neon_existing":
        return environment.get("neon_write_authority_ready") is True
    return True


def _server_state(
    server: Mapping[str, Any],
    *,
    environment: Mapping[str, Any],
    request_write_capabilities: bool,
) -> dict[str, Any]:
    server_id = str(server.get("server_id", ""))
    missing = _requirements_missing(server, environment)
    status = str(server.get("status", ""))
    privilege = str(server.get("privilege_class", ""))

    if missing:
        activation_state = (
            "optional_unconfigured"
            if status == "optional_when_instrumented"
            else "environment_missing"
        )
    elif status == "experimental_high_value":
        activation_state = "experimental_ready"
    else:
        activation_state = "ready"

    supports_write = privilege in {
        "mixed_read_write",
        "analysis_plus_optional_local_execution",
        "browser_effect",
        "orchestrator",
    }
    authority_ready = (
        _authority_ready(server, environment) if request_write_capabilities else True
    )

    if (
        request_write_capabilities
        and supports_write
        and not missing
        and not authority_ready
    ):
        activation_state = "authority_required"

    effective_mode = "read_only"
    if request_write_capabilities and supports_write and authority_ready and not missing:
        effective_mode = "write_candidate"
    elif privilege == "browser_effect" and not request_write_capabilities:
        effective_mode = "inspection_only"
    elif privilege == "orchestrator" and not request_write_capabilities:
        effective_mode = "orchestration_plan_only"

    launch = _m(server.get("launch_template"))
    return {
        "server_id": server_id,
        "display_name": server.get("display_name"),
        "source_repository": server.get("source_repository"),
        "source_kind": server.get("source_kind"),
        "registry_status": status,
        "activation_state": activation_state,
        "effective_mode": effective_mode,
        "missing_requirements": missing,
        "capability_families": _strings(server.get("capability_families")),
        "transport": _strings(server.get("transport")),
        "isolation": server.get("isolation"),
        "write_authority_path": server.get("write_authority_path", ""),
        "launch_template_digest": _sha(launch) if launch else "",
        "credentials_persisted": False,
        "registry_entry_is_authority": False,
        "source_authority_transferred": False,
    }


def build_development_mcp_profile(
    *,
    registry: Mapping[str, Any],
    profile_name: str,
    environment: Mapping[str, Any],
    request_write_capabilities: bool = False,
) -> DevelopmentMCPProfileResult:
    blockers = validate_registry(registry)
    profiles = _m(registry.get("profiles"))
    profile_members = profiles.get(profile_name)
    if not isinstance(profile_members, list) or not profile_members:
        blockers.append("profile_not_found_or_empty:" + profile_name)

    servers_raw = registry.get("servers")
    servers = (
        {
            str(item.get("server_id")): item
            for item in servers_raw
            if isinstance(item, Mapping)
        }
        if isinstance(servers_raw, list)
        else {}
    )

    states: list[dict[str, Any]] = []
    if not blockers:
        for server_id in profile_members:
            states.append(
                _server_state(
                    servers[str(server_id)],
                    environment=environment,
                    request_write_capabilities=request_write_capabilities,
                )
            )

    counts = {
        "ready": sum(
            1
            for state in states
            if state["activation_state"] == "ready"
        ),
        "experimental": sum(
            1
            for state in states
            if state["activation_state"] == "experimental_ready"
        ),
        "authority": sum(
            1
            for state in states
            if state["activation_state"] == "authority_required"
        ),
        "missing": sum(
            1
            for state in states
            if state["activation_state"] == "environment_missing"
        ),
        "optional": sum(
            1
            for state in states
            if state["activation_state"] == "optional_unconfigured"
        ),
    }

    if blockers:
        status = BLOCKED
    elif counts["authority"] or counts["missing"] or counts["optional"]:
        status = PARTIAL
    else:
        status = READY

    return DevelopmentMCPProfileResult(
        VERSION,
        status,
        profile_name,
        len(states),
        counts["ready"],
        counts["experimental"],
        counts["authority"],
        counts["missing"],
        counts["optional"],
        sorted(set(blockers)),
        states,
    )
