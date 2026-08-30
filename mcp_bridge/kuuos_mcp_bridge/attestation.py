from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class DeploymentAttestationError(RuntimeError):
    """Raised when a deployment health receipt cannot be trusted."""


@dataclass(frozen=True)
class DeploymentExpectation:
    canonical_sha: str
    backend: str | None = None
    oauth_mode: str | None = None
    oauth_enabled: bool | None = None
    write_ready: bool | None = None
    mode: str | None = None


REQUIRED_HEALTH_FIELDS = (
    "ok",
    "mode",
    "backend",
    "version",
    "oauth_enabled",
    "oauth_mode",
    "write_ready",
    "canonical_sha",
)

SAFE_HEALTH_FIELDS = REQUIRED_HEALTH_FIELDS
MAX_HEALTH_BYTES = 64 * 1024


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def _is_localhost(hostname: str | None) -> bool:
    return hostname in {"localhost", "127.0.0.1", "::1"}


def build_health_url(base_url: str, *, allow_http_localhost: bool = False) -> str:
    raw = base_url.strip()
    parsed = urlparse(raw)
    if not parsed.scheme or not parsed.netloc:
        raise DeploymentAttestationError("deployment URL must be absolute")
    if parsed.username is not None or parsed.password is not None:
        raise DeploymentAttestationError("deployment URL must not contain credentials")
    if parsed.query or parsed.fragment:
        raise DeploymentAttestationError("deployment URL must not contain query or fragment")
    if parsed.scheme != "https":
        if not (allow_http_localhost and parsed.scheme == "http" and _is_localhost(parsed.hostname)):
            raise DeploymentAttestationError("deployment attestation requires HTTPS")

    path = parsed.path.rstrip("/")
    if path.endswith("/healthz"):
        health_path = path
    else:
        health_path = f"{path}/healthz" if path else "/healthz"
    return parsed._replace(path=health_path, params="", query="", fragment="").geturl()


def _origin(url: str) -> tuple[str, str, int | None]:
    parsed = urlparse(url)
    return parsed.scheme, parsed.hostname or "", parsed.port


def validate_health_payload(
    payload: Mapping[str, Any],
    expectation: DeploymentExpectation,
) -> dict[str, Any]:
    missing = [field for field in REQUIRED_HEALTH_FIELDS if field not in payload]
    if missing:
        raise DeploymentAttestationError(
            "health receipt is missing required fields: " + ", ".join(missing)
        )

    if payload["ok"] is not True:
        raise DeploymentAttestationError("health receipt does not report ok=true")

    mode = payload["mode"]
    if mode not in {"read-only", "read-write"}:
        raise DeploymentAttestationError("health mode must be read-only or read-write")

    backend = payload["backend"]
    if not isinstance(backend, str) or not backend:
        raise DeploymentAttestationError("health backend must be a non-empty string")

    version = payload["version"]
    if isinstance(version, bool) or not isinstance(version, int) or version < 0:
        raise DeploymentAttestationError("health version must be a non-negative integer")

    oauth_enabled = payload["oauth_enabled"]
    if not isinstance(oauth_enabled, bool):
        raise DeploymentAttestationError("oauth_enabled must be boolean")

    oauth_mode = payload["oauth_mode"]
    if oauth_mode is not None and (not isinstance(oauth_mode, str) or not oauth_mode):
        raise DeploymentAttestationError("oauth_mode must be null or a non-empty string")
    if oauth_enabled != (oauth_mode is not None):
        raise DeploymentAttestationError(
            "oauth_enabled and oauth_mode are internally inconsistent"
        )

    write_ready = payload["write_ready"]
    if not isinstance(write_ready, bool):
        raise DeploymentAttestationError("write_ready must be boolean")

    canonical_sha = payload["canonical_sha"]
    if not isinstance(canonical_sha, str) or not canonical_sha:
        raise DeploymentAttestationError("canonical_sha must be a non-empty string")

    if oauth_mode == "embedded" and backend != "PostgresStateStore":
        raise DeploymentAttestationError(
            "embedded OAuth is only valid with PostgresStateStore"
        )

    if mode == "read-write" and not write_ready:
        raise DeploymentAttestationError("read-write mode must report write_ready=true")
    if write_ready and (
        mode != "read-write" or backend != "PostgresStateStore" or not oauth_enabled
    ):
        raise DeploymentAttestationError(
            "write_ready=true requires read-write Postgres with OAuth enabled"
        )

    if canonical_sha != expectation.canonical_sha:
        raise DeploymentAttestationError(
            f"canonical SHA mismatch: expected {expectation.canonical_sha}, observed {canonical_sha}"
        )
    if expectation.backend is not None and backend != expectation.backend:
        raise DeploymentAttestationError(
            f"backend mismatch: expected {expectation.backend}, observed {backend}"
        )
    if expectation.oauth_mode is not None and oauth_mode != expectation.oauth_mode:
        raise DeploymentAttestationError(
            f"OAuth mode mismatch: expected {expectation.oauth_mode}, observed {oauth_mode}"
        )
    if expectation.oauth_enabled is not None and oauth_enabled != expectation.oauth_enabled:
        raise DeploymentAttestationError(
            f"oauth_enabled mismatch: expected {expectation.oauth_enabled}, observed {oauth_enabled}"
        )
    if expectation.write_ready is not None and write_ready != expectation.write_ready:
        raise DeploymentAttestationError(
            f"write_ready mismatch: expected {expectation.write_ready}, observed {write_ready}"
        )
    if expectation.mode is not None and mode != expectation.mode:
        raise DeploymentAttestationError(
            f"mode mismatch: expected {expectation.mode}, observed {mode}"
        )

    return {field: payload[field] for field in SAFE_HEALTH_FIELDS}


def fetch_health_payload(
    base_url: str,
    *,
    timeout: float = 10.0,
    allow_http_localhost: bool = False,
) -> tuple[str, Mapping[str, Any]]:
    health_url = build_health_url(
        base_url, allow_http_localhost=allow_http_localhost
    )
    request = Request(
        health_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "kuuos-mcp-attestation/1",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        status = getattr(response, "status", None)
        if status != 200:
            raise DeploymentAttestationError(
                f"health endpoint returned HTTP {status}"
            )
        final_url = response.geturl()
        if _origin(final_url) != _origin(health_url):
            raise DeploymentAttestationError(
                "health endpoint redirected to a different origin"
            )
        content_type = response.headers.get("content-type", "")
        if not content_type.lower().startswith("application/json"):
            raise DeploymentAttestationError(
                "health endpoint did not return application/json"
            )
        raw = response.read(MAX_HEALTH_BYTES + 1)

    if len(raw) > MAX_HEALTH_BYTES:
        raise DeploymentAttestationError("health receipt exceeds size limit")
    try:
        decoded = raw.decode("utf-8")
        payload = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DeploymentAttestationError("health receipt is not valid UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise DeploymentAttestationError("health receipt must be a JSON object")
    return health_url, payload


def attest_deployment(
    base_url: str,
    expectation: DeploymentExpectation,
    *,
    timeout: float = 10.0,
    allow_http_localhost: bool = False,
) -> dict[str, Any]:
    health_url, payload = fetch_health_payload(
        base_url,
        timeout=timeout,
        allow_http_localhost=allow_http_localhost,
    )
    observed = validate_health_payload(payload, expectation)
    return {
        "ok": True,
        "health_url": health_url,
        "observed": observed,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail-closed attestation of a deployed KuuOS MCP health receipt."
    )
    parser.add_argument("base_url", help="Deployment base URL or /healthz URL")
    parser.add_argument("--expected-canonical-sha", required=True)
    parser.add_argument("--expected-backend")
    parser.add_argument("--expected-oauth-mode")
    parser.add_argument("--expected-oauth-enabled", type=_parse_bool)
    parser.add_argument("--expected-write-ready", type=_parse_bool)
    parser.add_argument("--expected-mode", choices=["read-only", "read-write"])
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument(
        "--allow-http-localhost",
        action="store_true",
        help="Permit plain HTTP only for localhost/loopback testing.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    expectation = DeploymentExpectation(
        canonical_sha=args.expected_canonical_sha,
        backend=args.expected_backend,
        oauth_mode=args.expected_oauth_mode,
        oauth_enabled=args.expected_oauth_enabled,
        write_ready=args.expected_write_ready,
        mode=args.expected_mode,
    )
    try:
        receipt = attest_deployment(
            args.base_url,
            expectation,
            timeout=args.timeout,
            allow_http_localhost=args.allow_http_localhost,
        )
    except Exception as exc:
        print(
            json.dumps({"ok": False, "error": str(exc)}, sort_keys=True),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
