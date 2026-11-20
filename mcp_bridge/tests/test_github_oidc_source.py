"""Actual RSA signature and GitHub claim verification for OIDC source ingress."""
from __future__ import annotations

import base64
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from kuuos_mcp_bridge.github_oidc_source import (
    AUDIENCE, FEATURE_REF, ISSUER, OWNER_ID, REPO, REPOSITORY_ID,
    WORKFLOW_NAME, WORKFLOW_REF, GitHubOIDCSourceError,
    verify_oidc_push,
)


@pytest.fixture
def signed():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key()
    now = int(datetime.now(timezone.utc).timestamp())
    claims = {
        "iss": ISSUER, "aud": AUDIENCE, "sub": "repo:" + REPO + ":ref:" + FEATURE_REF,
        "iat": now, "nbf": now, "exp": now + 300,
        "jti": "synthetic-test-jti-1234567",
        "repository": REPO, "repository_id": REPOSITORY_ID,
        "repository_owner_id": OWNER_ID, "ref": FEATURE_REF,
        "sha": "a" * 40, "workflow": WORKFLOW_NAME,
        "workflow_ref": WORKFLOW_REF, "event_name": "push",
        "run_id": "98765544001", "run_attempt": "1",
    }
    body = {
        "kind": "push_observed", "repository": REPO, "ref": FEATURE_REF,
        "head_sha": "a" * 40, "run_id": 98765544001, "run_attempt": 1,
    }
    resolver = SimpleNamespace(
        get_signing_key_from_jwt=lambda _: SimpleNamespace(key=public)
    )
    def mint(c):
        return jwt.encode(c, key, algorithm="RS256", headers={"kid": "test-key"})
    return mint, claims, body, resolver


def test_verified_rsa_signed_source_claims_no_certification(signed):
    mint, claims, body, resolver = signed
    out = verify_oidc_push(mint(claims), body, signing_key_resolver=resolver)
    assert out.identity.startswith("oidc_")
    assert out.head_sha == "a" * 40
    assert out.run_id == body["run_id"]


@pytest.mark.parametrize("claim,value", [
    ("repository", "attacker/other"),
    ("repository_id", "0"),
    ("repository_owner_id", "0"),
    ("workflow_ref", "attacker/other/.github/workflows/no.yml@refs/heads/main"),
    ("event_name", "pull_request"),
    ("ref", "refs/heads/main"),
    ("sub", "repo:attacker/other:ref:refs/heads/main"),
    ("sha", "invalid"),
    ("aud", "api://wrong-audience"),
    ("iss", "https://evil.example"),
])
def test_oidc_trust_scope_is_not_a_guess(signed, claim, value):
    mint, claims, body, resolver = signed
    claims[claim] = value
    with pytest.raises(GitHubOIDCSourceError):
        verify_oidc_push(mint(claims), body, signing_key_resolver=resolver)


def test_claim_subject_and_body_cannot_diverge(signed):
    mint, claims, body, resolver = signed
    body["head_sha"] = "b" * 40
    with pytest.raises(GitHubOIDCSourceError, match="signed_payload_mismatch"):
        verify_oidc_push(mint(claims), body, signing_key_resolver=resolver)


def test_oidc_expiry_and_wrong_rsa_key_fail(signed):
    mint, claims, body, resolver = signed
    claims["exp"] = claims["iat"] - 1
    with pytest.raises(GitHubOIDCSourceError):
        verify_oidc_push(mint(claims), body, signing_key_resolver=resolver)
    claims["exp"] = claims["iat"] + 300
    wrong_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    wrong_resolver = SimpleNamespace(
        get_signing_key_from_jwt=lambda _: SimpleNamespace(key=wrong_key.public_key())
    )
    with pytest.raises(GitHubOIDCSourceError):
        verify_oidc_push(mint(claims), body, signing_key_resolver=wrong_resolver)


def test_untrusted_algorithm_and_missing_token_refused(signed):
    mint, claims, body, resolver = signed
    with pytest.raises(GitHubOIDCSourceError):
        verify_oidc_push("", body, signing_key_resolver=resolver)
    bad_alg = jwt.encode(claims, "public-invalid", algorithm="HS256",
                         headers={"kid": "test-key"})
    with pytest.raises(GitHubOIDCSourceError, match="algorithm"):
        verify_oidc_push(bad_alg, body, signing_key_resolver=resolver)


def test_extra_or_missing_body_fields_and_invalid_run_numbers_rejected(signed):
    mint, claims, body, resolver = signed
    token = mint(claims)
    with pytest.raises(GitHubOIDCSourceError):
        verify_oidc_push(token, dict(body, extra=True), signing_key_resolver=resolver)
    with pytest.raises(GitHubOIDCSourceError):
        verify_oidc_push(token, dict(body, run_id=False), signing_key_resolver=resolver)
    claims["run_id"] = "1234567"
    with pytest.raises(GitHubOIDCSourceError):
        verify_oidc_push(mint(claims), body, signing_key_resolver=resolver)


def test_actual_ci_gate_workflow_oidc_identity_is_tightly_pinned(signed):
    """CI gate-source identity is genuine but still not a CI verdict."""
    from kuuos_mcp_bridge.github_oidc_source import (
        CI_WORKFLOW_NAME, CI_WORKFLOW_REF,
    )
    mint, claims, body, resolver = signed
    claims["workflow"] = CI_WORKFLOW_NAME
    claims["workflow_ref"] = CI_WORKFLOW_REF
    body["kind"] = "ci_jobs_observed"
    result = verify_oidc_push(
        mint(claims), body, signing_key_resolver=resolver
    )
    assert result.kind == "ci_jobs_observed"
    assert result.workflow_ref == CI_WORKFLOW_REF
    assert result.identity.startswith("oidc_")
    # The name does not imply that a GH result has been certified.


def test_ci_gate_source_cannot_impersonate_push_workflow(signed):
    from kuuos_mcp_bridge.github_oidc_source import (
        CI_WORKFLOW_NAME, CI_WORKFLOW_REF,
    )
    mint, claims, body, resolver = signed
    body["kind"] = "ci_jobs_observed"
    with pytest.raises(GitHubOIDCSourceError, match="source_not_allowlisted"):
        verify_oidc_push(mint(claims), body, signing_key_resolver=resolver)
    claims["workflow_ref"] = CI_WORKFLOW_REF
    claims["workflow"] = CI_WORKFLOW_NAME
    body["kind"] = "push_observed"
    with pytest.raises(GitHubOIDCSourceError, match="source_not_allowlisted"):
        verify_oidc_push(mint(claims), body, signing_key_resolver=resolver)
