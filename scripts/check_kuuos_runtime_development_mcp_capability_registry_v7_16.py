#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import pathlib
import sys

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from runtime.kuuos_runtime_development_mcp_capability_registry_v7_16 import (
    BLOCKED,
    PARTIAL,
    READY,
    build_development_mcp_profile,
    validate_registry,
)

REGISTRY_PATH = (
    REPOSITORY_ROOT
    / "manifests"
    / "kuuos_development_mcp_capability_registry_v7_16.json"
)


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def env_core(*, with_write_authority: bool = False) -> dict:
    return {
        "available_requirements": [
            "uv",
            "git",
            "lake",
            "lean_project_built",
            "node",
            "browser_runtime",
            "chrome",
            "docker",
        ],
        "connected_services": ["github", "vercel", "supabase", "neon"],
        "network_allowed": True,
        "repository_root_bound": True,
        "sentry_project_configured": False,
        "github_write_authority_ready": with_write_authority,
        "workspace_write_authority_ready": with_write_authority,
        "browser_effect_authority_ready": with_write_authority,
        "mcp_orchestration_authority_ready": with_write_authority,
        "vercel_write_authority_ready": with_write_authority,
        "supabase_write_authority_ready": with_write_authority,
        "neon_write_authority_ready": with_write_authority,
    }


def states_by_id(result) -> dict[str, dict]:
    return {item["server_id"]: item for item in result.server_states}


def test_registry_valid_and_broad() -> None:
    registry = load_registry()
    errors = validate_registry(registry)
    assert errors == [], errors
    assert len(registry["servers"]) >= 14
    maximal = set(
        registry["profiles"]["kuuos_maximal_repository_development"]
    )
    required = {
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
    assert required.issubset(maximal)


def test_core_repo_profile_ready_with_lean_experimental() -> None:
    registry = load_registry()
    result = build_development_mcp_profile(
        registry=registry,
        profile_name="kuuos_core_repo_development",
        environment=env_core(),
        request_write_capabilities=False,
    )
    assert result.status == READY, result.to_dict()
    states = states_by_id(result)
    assert states["github_official"]["activation_state"] == "ready"
    assert states["git_reference"]["activation_state"] == "ready"
    assert states["filesystem_reference"]["activation_state"] == "ready"
    assert states["lean_lsp"]["activation_state"] == "experimental_ready"
    assert states["context7"]["activation_state"] == "ready"
    assert states["lean_lsp"]["effective_mode"] == "read_only"


def test_write_request_routes_to_independent_authorities() -> None:
    registry = load_registry()
    result = build_development_mcp_profile(
        registry=registry,
        profile_name="kuuos_core_repo_development",
        environment=env_core(with_write_authority=False),
        request_write_capabilities=True,
    )
    assert result.status == PARTIAL, result.to_dict()
    states = states_by_id(result)
    assert states["github_official"]["activation_state"] == "authority_required"
    assert states["git_reference"]["activation_state"] == "authority_required"
    assert states["filesystem_reference"]["activation_state"] == "authority_required"
    assert states["lean_lsp"]["activation_state"] == "authority_required"
    assert states["context7"]["activation_state"] == "ready"
    assert states["context7"]["effective_mode"] == "read_only"

    ready = build_development_mcp_profile(
        registry=registry,
        profile_name="kuuos_core_repo_development",
        environment=env_core(with_write_authority=True),
        request_write_capabilities=True,
    )
    assert ready.status == READY, ready.to_dict()
    ready_states = states_by_id(ready)
    for server_id in (
        "github_official",
        "git_reference",
        "filesystem_reference",
        "lean_lsp",
    ):
        assert ready_states[server_id]["effective_mode"] == "write_candidate"


def test_maximal_profile_degrades_locally_when_optional_provider_missing() -> None:
    registry = load_registry()
    result = build_development_mcp_profile(
        registry=registry,
        profile_name="kuuos_maximal_repository_development",
        environment=env_core(),
        request_write_capabilities=False,
    )
    assert result.status == PARTIAL, result.to_dict()
    states = states_by_id(result)
    assert states["sentry"]["activation_state"] == "optional_unconfigured"
    assert states["github_official"]["activation_state"] == "ready"
    assert states["playwright"]["activation_state"] == "ready"
    assert states["chrome_devtools"]["activation_state"] == "ready"
    assert states["docker_mcp_gateway"]["activation_state"] == "ready"
    assert states["vercel_existing"]["activation_state"] == "ready"
    assert states["supabase_existing"]["activation_state"] == "ready"
    assert states["neon_existing"]["activation_state"] == "ready"


def test_github_toolsets_cover_current_repo_development() -> None:
    registry = load_registry()
    github = next(
        server
        for server in registry["servers"]
        if server["server_id"] == "github_official"
    )
    toolsets = set(github["recommended_toolsets"])
    assert {
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
        "governance",
    }.issubset(toolsets)
    assert (
        github["activation"]
        == "reuse_existing_kuuos_github_mcp_bridge"
    )


def test_lean_lsp_is_high_value_but_not_auto_enabled_as_stable() -> None:
    registry = load_registry()
    lean = next(
        server
        for server in registry["servers"]
        if server["server_id"] == "lean_lsp"
    )
    assert lean["status"] == "experimental_high_value"
    assert lean["activation"] == "explicit_project_opt_in"
    assert "lake" in lean["runtime_requirements"]
    assert "lean_project_built" in lean["runtime_requirements"]
    assert "lean_diagnostics" in lean["capability_families"]
    assert "loogle" in lean["capability_families"]
    assert "lean_hammer_premise_search" in lean["capability_families"]


def test_browser_servers_are_complementary_and_isolated() -> None:
    registry = load_registry()
    by_id = {server["server_id"]: server for server in registry["servers"]}
    playwright = by_id["playwright"]
    chrome = by_id["chrome_devtools"]

    assert "functional_web_verification" in playwright["capability_families"]
    assert "performance_trace_analysis" in chrome["capability_families"]
    assert "isolated" in playwright["isolation"]
    assert "isolated" in chrome["isolation"]

    result = build_development_mcp_profile(
        registry=registry,
        profile_name="kuuos_browser_validation",
        environment=env_core(),
        request_write_capabilities=False,
    )
    assert result.status == READY
    states = states_by_id(result)
    assert states["playwright"]["effective_mode"] == "inspection_only"
    assert states["chrome_devtools"]["effective_mode"] == "inspection_only"


def test_plaintext_credentials_are_rejected() -> None:
    registry = load_registry()
    modified = copy.deepcopy(registry)
    modified["servers"][0]["token"] = "plaintext-secret"
    errors = validate_registry(modified)
    assert any(error.startswith("credential_material_present:") for error in errors)


def test_unknown_profile_blocks_without_launching_anything() -> None:
    registry = load_registry()
    result = build_development_mcp_profile(
        registry=registry,
        profile_name="not-a-real-profile",
        environment=env_core(),
        request_write_capabilities=False,
    )
    assert result.status == BLOCKED
    assert result.selected_server_count == 0


def main() -> int:
    test_registry_valid_and_broad()
    test_core_repo_profile_ready_with_lean_experimental()
    test_write_request_routes_to_independent_authorities()
    test_maximal_profile_degrades_locally_when_optional_provider_missing()
    test_github_toolsets_cover_current_repo_development()
    test_lean_lsp_is_high_value_but_not_auto_enabled_as_stable()
    test_browser_servers_are_complementary_and_isolated()
    test_plaintext_credentials_are_rejected()
    test_unknown_profile_blocks_without_launching_anything()
    print("PASS: KuuOS Development MCP Capability Registry v7.16")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
