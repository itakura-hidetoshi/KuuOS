"""Verified GitHub Actions OIDC sender admission: genuine source, never CI proof.

This is a distinct, opt-in ingress, NOT a way to assert a workflow completed.
It accepts GitHub-signed identities for the exact reviewed source workflow on
the test branch. The identity and the submitted push parameters must agree.
A real signed receipt is append-only, with no Dot subscription or CI verdict.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from starlette.requests import Request
from starlette.responses import JSONResponse

from .db_schema_mode import schema_is_preprovisioned, verify_preprovisioned_schema
from .state_store import PostgresStateStore

ISSUER = "https://token.actions.githubusercontent.com"
JWKS_URI = "https://token.actions.githubusercontent.com/.well-known/jwks"
AUDIENCE = "api://kuuos/KuuOS/mcp-source-oidc-v1"
REPO = "itakura-hidetoshi/KuuOS"
REPOSITORY_ID = "1235298309"
OWNER_ID = "216274897"
FEATURE_BRANCH = "feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120"
FEATURE_REF = "refs/heads/" + FEATURE_BRANCH
WORKFLOW_FILE = ".github/workflows/kuuos-mcp-github-oidc-source.yml"
WORKFLOW_REF = REPO + "/" + WORKFLOW_FILE + "@" + FEATURE_REF
WORKFLOW_NAME = "KuuOS MCP Authentic OIDC Source"
CI_WORKFLOW_NAME = "KuuOS MCP Bridge Python Validation"
CI_WORKFLOW_REF = (
    REPO + "/.github/workflows/mcp-bridge-python-validation.yml@" + FEATURE_REF
)
_SHA = re.compile(r"^[0-9a-f]{40}$")
_MAX_TOKEN = 16384
_MAX_BODY = 4096


class GitHubOIDCSourceError(ValueError):
    """Sanitized source-admission error: no input or token in the message."""


@dataclass(frozen=True)
class VerifiedSource:
    identity: str
    repository: str
    workflow_ref: str
    ref: str
    head_sha: str
    run_id: int
    run_attempt: int
    jti_hash: str
    kind: str = "push_observed"


def _number(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise GitHubOIDCSourceError("oidc_numeric_claim_invalid")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise GitHubOIDCSourceError("oidc_numeric_claim_invalid") from exc
    if parsed <= 0 or str(parsed) != str(value):
        raise GitHubOIDCSourceError("oidc_numeric_claim_invalid")
    return parsed


def verify_oidc_push(
    id_token: str,
    submitted: Mapping[str, Any],
    *,
    signing_key_resolver: Any | None = None,
) -> VerifiedSource:
    """Validate the actual GitHub-issued signature, then exact branch claims.

    The only test seam is an explicit key resolver. Production always reads
    public signing keys from GitHub's fixed JWKS HTTPS endpoint and limits the
    signing algorithm to RS256. No request field chooses a JWKS URL.
    """
    if not isinstance(id_token, str) or not 1 <= len(id_token) <= _MAX_TOKEN:
        raise GitHubOIDCSourceError("github_oidc_bearer_invalid")
    if not isinstance(submitted, Mapping) or set(submitted) != {
        "kind", "repository", "ref", "head_sha", "run_id", "run_attempt",
    }:
        raise GitHubOIDCSourceError("github_oidc_body_shape_invalid")
    kind = submitted.get("kind")
    if kind == "push_observed":
        workflow_ref, workflow_name = WORKFLOW_REF, WORKFLOW_NAME
    elif kind == "ci_jobs_observed":
        # This is a real *post-gates* source signal, not a terminal
        # conclusion or independent CI proof. The receiver/ChatGPT must
        # re-fetch the specific GitHub job and step statuses itself.
        workflow_ref, workflow_name = CI_WORKFLOW_REF, CI_WORKFLOW_NAME
    else:
        raise GitHubOIDCSourceError("github_oidc_kind_not_allowlisted")
    try:
        import jwt
        header = jwt.get_unverified_header(id_token)
        if (
            header.get("alg") != "RS256"
            or not isinstance(header.get("kid"), str)
            or not header["kid"]
        ):
            raise GitHubOIDCSourceError("github_oidc_algorithm_not_allowlisted")
        resolver = (signing_key_resolver if signing_key_resolver is not None
                    else jwt.PyJWKClient(JWKS_URI, timeout=8))
        key = resolver.get_signing_key_from_jwt(id_token)
        claims = jwt.decode(
            id_token, key.key, algorithms=["RS256"],
            issuer=ISSUER, audience=AUDIENCE,
            options={"require": [
                "iss", "aud", "sub", "iat", "nbf", "exp", "jti",
                "repository", "repository_id", "repository_owner_id",
                "ref", "sha", "workflow", "workflow_ref",
                "event_name", "run_id", "run_attempt",
            ]},
        )
    except GitHubOIDCSourceError:
        raise
    except Exception as exc:
        raise GitHubOIDCSourceError("github_oidc_signature_or_claim_invalid") from exc

    exact = {
        "repository": REPO,
        "repository_id": REPOSITORY_ID,
        "repository_owner_id": OWNER_ID,
        "ref": FEATURE_REF,
        "workflow_ref": workflow_ref,
        "workflow": workflow_name,
        "event_name": "push",
        "sub": "repo:" + REPO + ":ref:" + FEATURE_REF,
    }
    if any(str(claims.get(k)) != value for k, value in exact.items()):
        raise GitHubOIDCSourceError("github_oidc_source_not_allowlisted")
    sha = claims.get("sha")
    if not isinstance(sha, str) or _SHA.fullmatch(sha) is None:
        raise GitHubOIDCSourceError("github_oidc_sha_invalid")
    run_id = _number(claims["run_id"])
    attempt = _number(claims["run_attempt"])
    if (
        submitted.get("kind") != kind
        or submitted.get("repository") != REPO
        or submitted.get("ref") != FEATURE_REF
        or submitted.get("head_sha") != sha
        or type(submitted.get("run_id")) is not int
        or submitted["run_id"] != run_id
        or type(submitted.get("run_attempt")) is not int
        or submitted["run_attempt"] != attempt
    ):
        raise GitHubOIDCSourceError("github_oidc_signed_payload_mismatch")
    jti = claims["jti"]
    if not isinstance(jti, str) or not 8 <= len(jti) <= 512:
        raise GitHubOIDCSourceError("github_oidc_jti_invalid")
    identity = hashlib.sha256(
        json.dumps([REPO, workflow_ref, run_id, attempt],
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return VerifiedSource(
        identity="oidc_" + identity, repository=REPO, workflow_ref=workflow_ref,
        ref=FEATURE_REF, head_sha=sha, run_id=run_id, run_attempt=attempt,
        jti_hash=hashlib.sha256(jti.encode("utf-8")).hexdigest(),
        kind=kind,
    )


class PostgresOIDCSourceReceiptStore:
    """Append-only, unique-by-source-run provenance, not a CI truth ledger."""

    TABLE = "kuuos_mcp_github_oidc_source_v1"

    def __init__(self, dsn: str):
        if not isinstance(dsn, str) or not dsn:
            raise RuntimeError("github_oidc_postgres_required")
        import psycopg
        self._dsn = dsn
        self._psycopg = psycopg
        with self._psycopg.connect(self._dsn) as conn:
            if schema_is_preprovisioned():
                verify_preprovisioned_schema(
                    conn, table=self.TABLE,
                    columns={
                        "id": ("text", True), "repository": ("text", True),
                        "workflow_ref": ("text", True), "ref": ("text", True),
                        "head_sha": ("text", True),
                        "run_id": ("bigint", True),
                        "run_attempt": ("integer", True),
                        "jti_hash": ("text", True),
                        "received_at": ("timestamp with time zone", True),
                    },
                    constraints={
                        "kuuos_mcp_github_oidc_source_v1_pkey": "p",
                        "kuuos_mcp_oidc_source_run_unique": "u",
                    },
                    constraint_definitions={
                        "kuuos_mcp_github_oidc_source_v1_pkey": "PRIMARY KEY (id)",
                        "kuuos_mcp_oidc_source_run_unique":
                            "UNIQUE (repository, workflow_ref, run_id, run_attempt)",
                    },
                )
                return
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE} (
                    id TEXT PRIMARY KEY,
                    repository TEXT NOT NULL,
                    workflow_ref TEXT NOT NULL,
                    ref TEXT NOT NULL,
                    head_sha TEXT NOT NULL,
                    run_id BIGINT NOT NULL,
                    run_attempt INTEGER NOT NULL,
                    jti_hash TEXT NOT NULL,
                    received_at TIMESTAMPTZ NOT NULL,
                    CONSTRAINT kuuos_mcp_oidc_source_run_unique
                      UNIQUE(repository, workflow_ref, run_id, run_attempt)
                )
            """)

    def append(self, item: VerifiedSource) -> bool:
        """Return True on first insert, False on identical duplicate.

        A conflicting record is an obstruction, never overwritten.
        """
        with self._psycopg.connect(self._dsn) as conn:
            row = conn.execute(
                f"INSERT INTO {self.TABLE} "
                "(id, repository, workflow_ref, ref, head_sha, run_id, "
                "run_attempt, jti_hash, received_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                "ON CONFLICT DO NOTHING RETURNING id",
                (item.identity, item.repository, item.workflow_ref, item.ref,
                 item.head_sha, item.run_id, item.run_attempt, item.jti_hash,
                 datetime.now(timezone.utc)),
            ).fetchone()
            if row is not None:
                return True
            existing = conn.execute(
                f"SELECT repository, workflow_ref, ref, head_sha, "
                f"run_id, run_attempt FROM {self.TABLE} WHERE id=%s",
                (item.identity,),
            ).fetchone()
            if existing != (item.repository, item.workflow_ref, item.ref,
                            item.head_sha, item.run_id, item.run_attempt):
                raise GitHubOIDCSourceError("github_oidc_existing_receipt_conflict")
            return False


def install_oidc_source_route(mcp: Any, store: PostgresStateStore) -> None:
    """Optional path, independent of the GitHub Webhook HMAC secret."""
    if not isinstance(store, PostgresStateStore):
        raise RuntimeError("github_oidc_postgres_backend_required")
    if os.environ.get("KUUOS_MCP_GITHUB_OIDC_AUDIENCE") != AUDIENCE:
        raise RuntimeError("github_oidc_audience_not_pinned")
    receipts = PostgresOIDCSourceReceiptStore(store.database_url)

    @mcp.custom_route("/github/oidc", methods=["POST"], include_in_schema=False)
    async def github_oidc_source(request: Request) -> JSONResponse:
        # Never echo bearer, request body, identity/issuer errors or claim data.
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or len(auth) > _MAX_TOKEN + 7:
            return JSONResponse({"error": "github_oidc_unauthorized"}, status_code=401)
        try:
            raw = await request.body()
            if not 0 < len(raw) <= _MAX_BODY:
                raise GitHubOIDCSourceError("github_oidc_body_size_invalid")
            submitted = json.loads(raw)
            source = verify_oidc_push(auth[7:], submitted)
            inserted = await __import__("asyncio").to_thread(receipts.append, source)
        except (GitHubOIDCSourceError, ValueError, TypeError):
            return JSONResponse({"error": "github_oidc_unauthorized"}, status_code=401)
        except Exception:
            return JSONResponse({"error": "github_oidc_unavailable"}, status_code=503)
        return JSONResponse({
            "accepted": True,
            "github_oidc_signature_verified": True,
            "receipt_id": source.identity,
            "new_source_receipt": inserted,
            "repository": source.repository,
            "ref": source.ref,
            "head_sha": source.head_sha,
            "run_id": source.run_id,
            "run_attempt": source.run_attempt,
            "github_event_kind": source.kind,
            "signal_is_success_evidence": False,
            "fresh_mcp_reobservation_required": True,
            "dots_callback_received": False,
            "merge_authority_granted": False,
            "write_authority_granted": False,
        }, status_code=202)
