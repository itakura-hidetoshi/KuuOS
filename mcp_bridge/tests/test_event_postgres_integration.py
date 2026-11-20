"""Actual PostgreSQL integration, run only with a disposable CI service database.

No application/user database is used. This test does not prove live Dots event
delivery: it certifies only the SQL/transaction/encryption behavior observed
inside the GitHub Actions PostgreSQL service container.
"""
from __future__ import annotations

import base64
import os
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor

import pytest
import psycopg

from kuuos_mcp_bridge.event_outbox import PostgresOutboxStore
from kuuos_mcp_bridge.event_subscriptions import (
    PostgresSubscriptionStore, SubscriptionManager, ROTATION_WINDOW_SECONDS,
)
from kuuos_mcp_bridge.github_event_contract import (
    CI_EVENT, MGAP_REPO, EventContractError, compile_ci_completed,
)

DSN = os.environ.get("KUUOS_MCP_TEST_POSTGRES_DSN")
pytestmark = pytest.mark.skipif(
    not DSN, reason="requires isolated GitHub Actions PostgreSQL service DSN"
)
NOW = datetime(2026, 11, 20, 14, tzinfo=timezone.utc)
KEY = base64.b64encode(b"k" * 32).decode()
ONE = "whsec_" + base64.b64encode(b"a" * 32).decode()
TWO = "whsec_" + base64.b64encode(b"b" * 32).decode()


@pytest.fixture(scope="module")
def stores():
    # Hard boundary: the test never runs on an unknown or non-CI database.
    if not DSN:
        pytest.skip("no disposable postgres service configured")
    conninfo = psycopg.conninfo.conninfo_to_dict(DSN)
    if conninfo.get("dbname") != "kuuos_events_ci" or conninfo.get("user") != "kuuos_ci":
        pytest.fail("isolated CI PostgreSQL database identity mismatch")
    return PostgresSubscriptionStore(DSN, KEY), PostgresOutboxStore(DSN)


def _manager(store, *, owner="owner-fixture"):
    return SubscriptionManager(
        store, authorize=lambda p, n, a: p == owner,
        verify_callback=lambda url, secret, identity: True,
        now=lambda: NOW,
    )


def _params(secret=ONE):
    return {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {
            "mode": "webhook",
            "url": "https://receiver.example.org/ci-postgres",
            "secret": secret,
        },
    }


def _event(run_id=980001):
    return compile_ci_completed({
        "action": "completed",
        "repository": {"full_name": MGAP_REPO},
        "workflow_run": {
            "id": run_id, "run_attempt": 1,
            "name": "PR Lean Fast Check", "event": "pull_request",
            "status": "completed", "conclusion": "failure",
            "head_sha": "a" * 40,
        },
    })


def test_real_postgres_subscribe_rotation_and_encrypted_secret_storage(stores):
    subs, _ = stores
    manager = _manager(subs)
    first = manager.subscribe("owner-fixture", _params())
    assert first["id"].startswith("sub_")
    assert subs.get(first["id"]).secret == ONE
    manager.subscribe("owner-fixture", _params(TWO))
    current = subs.get(first["id"])
    assert current.secret == TWO
    assert current.previous_secret == ONE
    assert current.previous_secret_until == NOW + timedelta(seconds=ROTATION_WINDOW_SECONDS)
    assert current.id == first["id"]
    assert ONE not in repr(current) and TWO not in repr(current)
    with psycopg.connect(DSN) as conn:
        row = conn.execute(
            "SELECT secret_blob, previous_secret_blob FROM "
            "kuuos_mcp_event_subscriptions_v1 WHERE id = %s", (first["id"],),
        ).fetchone()
    assert row is not None
    assert ONE.encode() not in bytes(row[0]) and TWO.encode() not in bytes(row[0])
    assert ONE.encode() not in bytes(row[1]) and TWO.encode() not in bytes(row[1])


def test_real_postgres_outbox_claim_settle_and_idempotent_replay(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    event = _event(980001)
    first = outbox.enqueue(sub, event, NOW)
    same = outbox.enqueue(sub, event, NOW)
    assert first.id == same.id
    assert first.state == same.state == "pending"
    claimed = outbox.claim(NOW)
    assert claimed is not None
    assert claimed.id == first.id
    assert claimed.state == "leased" and claimed.attempts == 1
    assert claimed.lease_token
    assert outbox.claim(NOW) is None
    completed = outbox.settle(claimed.id, claimed.lease_token, 202, NOW)
    assert completed.state == "delivered"
    assert outbox.claim(NOW + timedelta(hours=1)) is None
    assert outbox.enqueue(sub, event, NOW).state == "delivered"


def test_real_postgres_reclaim_expired_lease_rejects_stale_completion(stores):
    from kuuos_mcp_bridge.github_event_contract import EventContractError
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    row = outbox.enqueue(sub, _event(980002), NOW)
    first = outbox.claim(NOW)
    assert first is not None and first.id == row.id
    second = outbox.claim(NOW + timedelta(seconds=31))
    assert second is not None and second.id == row.id
    assert second.lease_token != first.lease_token
    with pytest.raises(EventContractError, match="outbox_lease_mismatch"):
        outbox.settle(first.id, first.lease_token, 200, NOW + timedelta(seconds=32))
    done = outbox.settle(second.id, second.lease_token, 200, NOW + timedelta(seconds=32))
    assert done.state == "delivered"


def test_real_postgres_two_workers_claim_only_one_pending_event(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    row = outbox.enqueue(sub, _event(980003), NOW)
    another = PostgresOutboxStore(DSN)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(outbox.claim, NOW)
        b = pool.submit(another.claim, NOW)
        results = [a.result(), b.result()]
    claimed = [item for item in results if item is not None]
    assert len(claimed) == 1, results
    assert claimed[0].id == row.id
    outbox.settle(claimed[0].id, claimed[0].lease_token, 200, NOW)


def test_real_postgres_revoked_subscription_unsubscribe_is_owner_bound(stores):
    subs, _ = stores
    # Use an isolated subscriber: previous tests intentionally rotated
    # owner-fixture's key and must not silently reset that live rotation.
    owner = "owner-revocation-fixture"
    manager = _manager(subs, owner=owner)
    receipt = manager.subscribe(owner, _params())
    args = {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {"mode": "webhook", "url": "https://receiver.example.org/ci-postgres"},
    }
    with pytest.raises(EventContractError, match="event_scope_not_authorized"):
        manager.unsubscribe("different-owner", args)
    assert subs.get(receipt["id"]) is not None
    manager.unsubscribe(owner, args)
    assert subs.get(receipt["id"]) is None


def test_real_postgres_migrates_legacy_subscription_without_losing_old_secret(stores):
    """Test additive migrations against an actual pre-rotation table schema."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from psycopg.types.json import Jsonb
    from kuuos_mcp_bridge.event_subscriptions import _identity

    # Use a separate synthetic table so neither the existing test subscription
    # nor any user state is touched. The service database is itself ephemeral.
    class LegacyStore(PostgresSubscriptionStore):
        _TABLE = "kuuos_mcp_event_subscriptions_legacy_ci"

    owner = "owner-legacy-fixture"
    arguments = {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"}
    callback = "https://receiver.example.org/ci-postgres"
    sub_id = _identity(owner, CI_EVENT, arguments, callback)
    key = base64.b64decode(KEY, validate=True)
    nonce = b"l" * 12  # Synthetic test-only nonce, not a production pattern.
    old_ciphertext = nonce + AESGCM(key).encrypt(
        nonce, ONE.encode("utf-8"), sub_id.encode("ascii")
    )
    with psycopg.connect(DSN) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS kuuos_mcp_event_subscriptions_legacy_ci (
                id TEXT PRIMARY KEY,
                principal TEXT NOT NULL,
                name TEXT NOT NULL,
                arguments JSONB NOT NULL,
                callback_url TEXT NOT NULL,
                secret_blob BYTEA NOT NULL,
                expires_at TIMESTAMPTZ NOT NULL,
                verified_at TIMESTAMPTZ NOT NULL
            )
        """)
        conn.execute("""
            INSERT INTO kuuos_mcp_event_subscriptions_legacy_ci
              (id, principal, name, arguments, callback_url, secret_blob, expires_at, verified_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING
        """, (
            sub_id, owner, CI_EVENT, Jsonb(arguments), callback, old_ciphertext,
            NOW + timedelta(days=1), NOW,
        ))

    upgraded = LegacyStore(DSN, KEY)
    restored = upgraded.get(sub_id)
    assert restored is not None
    assert restored.secret == ONE
    assert restored.previous_secret is None
    assert restored.previous_secret_until is None

    manager = _manager(upgraded, owner=owner)
    assert manager.subscribe(owner, _params(ONE))["id"] == sub_id
    assert manager.subscribe(owner, _params(TWO))["id"] == sub_id
    active = upgraded.get(sub_id)
    assert active.secret == TWO
    assert active.previous_secret == ONE
    with psycopg.connect(DSN) as conn:
        row = conn.execute("""
            SELECT secret_blob, previous_secret_blob, previous_secret_until
            FROM kuuos_mcp_event_subscriptions_legacy_ci WHERE id = %s
        """, (sub_id,)).fetchone()
    assert row is not None and row[1] is not None and row[2] is not None
    assert ONE.encode() not in bytes(row[1])


def test_real_postgres_specific_claim_prioritizes_fresh_event_and_prevents_replay(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    old = outbox.enqueue(sub, _event(980101), NOW)
    fresh = outbox.enqueue(sub, _event(980102), NOW)
    claim = outbox.claim_specific(fresh.id, NOW)
    assert claim is not None and claim.id == fresh.id
    assert outbox.claim_specific(fresh.id, NOW) is None
    assert outbox.claim_specific(old.id, NOW) is not None
    done = outbox.settle(claim.id, claim.lease_token, 202, NOW)
    assert done.state == "delivered"
    assert outbox.claim_specific(fresh.id, NOW + timedelta(minutes=2)) is None


def test_real_postgres_specific_claim_competing_workers_only_one_wins(stores):
    subs, outbox = stores
    sub = subs.active(CI_EVENT, NOW)[0]
    row = outbox.enqueue(sub, _event(980103), NOW)
    second = PostgresOutboxStore(DSN)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(outbox.claim_specific, row.id, NOW)
        b = pool.submit(second.claim_specific, row.id, NOW)
        result = [a.result(), b.result()]
    claimed = [c for c in result if c is not None]
    assert len(claimed) == 1
    assert claimed[0].id == row.id
    outbox.settle(row.id, claimed[0].lease_token, 200, NOW)


def test_preprovisioned_schema_with_real_postgres_narrow_dml_role(
    stores, monkeypatch,
):
    """A non-owner DML-only CI role starts all three preprovisioned stores.

    Test credentials and test database are disposable per GitHub Actions job.
    We never connect to an external, user, production, or Neon database.
    """
    import secrets as crypto_secrets
    from psycopg import sql
    from kuuos_mcp_bridge.state_store import PostgresStateStore

    # Migration authority stays with the disposable CI database owner.
    PostgresStateStore(DSN)
    role = "kuuos_mcp_ci_" + crypto_secrets.token_hex(5)
    password = crypto_secrets.token_urlsafe(32)
    with psycopg.connect(DSN) as admin:
        admin.execute(sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
            sql.Identifier(role), sql.Literal(password)
        ))
        admin.execute(sql.SQL("GRANT USAGE ON SCHEMA public TO {}").format(
            sql.Identifier(role)
        ))
        admin.execute(sql.SQL(
            "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE "
            "public.kuuos_mcp_state, "
            "public.kuuos_mcp_event_subscriptions_v1, "
            "public.kuuos_mcp_event_outbox_v1 TO {}"
        ).format(sql.Identifier(role)))

    dsn = psycopg.conninfo.make_conninfo(DSN, user=role, password=password)
    with psycopg.connect(dsn) as limited:
        grants = limited.execute(
            "SELECT current_user, has_schema_privilege(current_user,"
            "'public','CREATE')"
        ).fetchone()
        assert grants == (role, False)
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            limited.execute(
                "CREATE TABLE IF NOT EXISTS kuuos_mcp_no_ddl_permitted "
                "(id INTEGER)"
            )
        limited.rollback()

    monkeypatch.setenv("KUUOS_MCP_SCHEMA_MODE", "preprovisioned")
    state = PostgresStateStore(dsn)
    assert state.read()["version"] >= 0
    subscriptions = PostgresSubscriptionStore(dsn, KEY)
    outbox = PostgresOutboxStore(dsn)
    assert outbox is not None
    principal = "preview-" + role
    manager = _manager(subscriptions, owner=principal)
    receipt = manager.subscribe(principal, _params())
    assert receipt["id"].startswith("sub_")
    assert subscriptions.get(receipt["id"]).principal == principal
    assert manager.unsubscribe(principal, {
        "name": CI_EVENT,
        "arguments": {"repository": MGAP_REPO, "workflow_name": "PR Lean Fast Check"},
        "delivery": {
            "mode": "webhook", "url": "https://receiver.example.org/ci-postgres"
        },
    }) == {}
    assert subscriptions.get(receipt["id"]) is None


def test_preprovisioned_schema_missing_required_column_fails_closed(
    stores, monkeypatch,
):
    from kuuos_mcp_bridge.db_schema_mode import verify_preprovisioned_schema

    monkeypatch.setenv("KUUOS_MCP_SCHEMA_MODE", "preprovisioned")
    with psycopg.connect(DSN) as conn:
        with pytest.raises(RuntimeError, match="columns_invalid"):
            verify_preprovisioned_schema(
                conn, table="kuuos_mcp_event_subscriptions_v1",
                columns={
                    "id": ("text", True),
                    "missing_column": ("bytea", False),
                },
            )


def test_real_postgres_preprovisioned_oauth_with_narrow_dml_role(
    stores, monkeypatch,
):
    """Embedded OAuth must start with a DML-only role and verified schema.

    Credentials and tokens used here exist only in the disposable CI database.
    """
    import secrets as crypto_secrets
    from psycopg import sql
    from kuuos_mcp_bridge.embedded_oauth import EmbeddedPostgresOAuthProvider

    issuer = "https://oauth-ci-only.example.org"
    resource = "https://oauth-ci-only.example.org/api/mcp"
    owner_secret = "ci-fixture-secret-not-used-outside-disposable-tests"

    # The disposable CI database owner performs the additive migration first.
    EmbeddedPostgresOAuthProvider(
        DSN, issuer=issuer, resource_url=resource, owner_secret=owner_secret
    )
    role = "kuuos_mcp_ci_" + crypto_secrets.token_hex(5)
    password = crypto_secrets.token_urlsafe(32)
    with psycopg.connect(DSN) as admin:
        admin.execute(sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
            sql.Identifier(role), sql.Literal(password)
        ))
        admin.execute(sql.SQL("GRANT USAGE ON SCHEMA public TO {}").format(
            sql.Identifier(role)
        ))
        admin.execute(sql.SQL(
            "GRANT SELECT, INSERT, UPDATE, DELETE "
            "ON TABLE public.kuuos_mcp_oauth TO {}"
        ).format(sql.Identifier(role)))

    dsn = psycopg.conninfo.make_conninfo(DSN, user=role, password=password)
    with psycopg.connect(dsn) as limited:
        assert limited.execute(
            "SELECT has_schema_privilege(current_user,'public','CREATE')"
        ).fetchone() == (False,)

    monkeypatch.setenv("KUUOS_MCP_SCHEMA_MODE", "preprovisioned")
    provider = EmbeddedPostgresOAuthProvider(
        dsn, issuer=issuer, resource_url=resource,
        owner_secret=owner_secret, owner_subject="ci-owner",
    )
    assert provider.owner_subject == "ci-owner"
    assert provider.resource_url == resource
    with psycopg.connect(dsn) as limited:
        assert limited.execute(
            "SELECT count(*) FROM public.kuuos_mcp_oauth"
        ).fetchone()[0] >= 0


def test_real_postgres_preprovisioned_constraint_definition_requires_exact(
    stores, monkeypatch,
):
    """The same UNIQUE name cannot silently swap event and subscription keys."""
    from kuuos_mcp_bridge.db_schema_mode import verify_preprovisioned_schema

    monkeypatch.setenv("KUUOS_MCP_SCHEMA_MODE", "preprovisioned")
    with psycopg.connect(DSN) as conn:
        with pytest.raises(RuntimeError, match="constraint_definition_invalid"):
            verify_preprovisioned_schema(
                conn,
                table="kuuos_mcp_event_outbox_v1",
                columns={"id": ("text", True)},
                constraint_definitions={
                    "kuuos_mcp_event_outbox_v1_subscription_id_event_id_key":
                        "UNIQUE (event_id, subscription_id)",
                },
            )


def test_public_client_token_revocation_http_route_with_explicit_empty_secret(
    stores, monkeypatch,
):
    """Actual SDK /revoke route on disposable PG16/18; never a real account.

    A public client has no secret; pinned MCP 2.3.0 requires the *empty*
    client_secret form field to be present. Authentication still uses the
    registered client_id; both access and refresh credentials must be revoked.
    """
    import asyncio
    import secrets
    from mcp.server.auth.routes import create_auth_routes
    from mcp.server.auth.settings import ClientRegistrationOptions, RevocationOptions
    from mcp.shared.auth import OAuthClientInformationFull
    from pydantic import AnyHttpUrl
    from starlette.applications import Starlette
    from starlette.testclient import TestClient
    from kuuos_mcp_bridge.embedded_oauth import EmbeddedPostgresOAuthProvider

    issuer = "https://synthetic-only-oauth.example.org"
    resource = issuer + "/api/mcp"
    provider = EmbeddedPostgresOAuthProvider(
        DSN, issuer=issuer, resource_url=resource,
        owner_secret="synthetic-only-credential-not-real-user",
    )
    client_id = "synthetic-ci-" + secrets.token_hex(10)
    registered = OAuthClientInformationFull(
        client_id=client_id,
        redirect_uris=["https://synthetic-only-client.example.org/callback"],
        token_endpoint_auth_method="none",
        grant_types=["authorization_code", "refresh_token"],
        response_types=["code"],
    )
    asyncio.run(provider.register_client(registered))
    issued = asyncio.run(provider._issue_pair(
        client_id=client_id, scopes=["kuuos:read"],
        resource=resource, subject="synthetic-ci",
    ))
    assert issued.refresh_token is not None
    assert asyncio.run(provider.load_access_token(issued.access_token)) is not None
    assert asyncio.run(
        provider.load_refresh_token(registered, issued.refresh_token)
    ) is not None

    app = Starlette(routes=create_auth_routes(
        provider=provider,
        issuer_url=AnyHttpUrl(issuer),
        client_registration_options=ClientRegistrationOptions(enabled=True),
        revocation_options=RevocationOptions(enabled=True),
    ))
    with TestClient(app) as http:
        response = http.post("/revoke", data={
            "token": issued.access_token,
            "client_id": client_id,
            "client_secret": "",
            "token_type_hint": "access_token",
        })
        assert response.status_code == 200, response.text

    assert asyncio.run(provider.load_access_token(issued.access_token)) is None
    assert asyncio.run(
        provider.load_refresh_token(registered, issued.refresh_token)
    ) is None


def test_real_postgres_github_oidc_source_append_only(stores, monkeypatch):
    """Actually persist only verified identity metadata in disposable CI PG16/18."""
    from dataclasses import replace
    from kuuos_mcp_bridge.github_oidc_source import (
        GitHubOIDCSourceError, PostgresOIDCSourceReceiptStore, VerifiedSource,
        REPO, WORKFLOW_REF, FEATURE_REF,
    )

    monkeypatch.delenv("KUUOS_MCP_SCHEMA_MODE", raising=False)
    source_store = PostgresOIDCSourceReceiptStore(DSN)
    observed = VerifiedSource(
        identity="oidc_" + "1" * 64,
        repository=REPO, workflow_ref=WORKFLOW_REF, ref=FEATURE_REF,
        head_sha="a" * 40, run_id=990000124, run_attempt=1,
        jti_hash="b" * 64,
    )
    assert source_store.append(observed) is True
    assert source_store.append(observed) is False
    # Identity rotates each OIDC token; one source run remains unique.
    assert source_store.append(replace(observed, jti_hash="c" * 64)) is False
    with pytest.raises(GitHubOIDCSourceError, match="existing_receipt_conflict"):
        source_store.append(replace(observed, head_sha="f" * 40))
    with psycopg.connect(DSN) as connection:
        count = connection.execute(
            "SELECT count(*)::int FROM kuuos_mcp_github_oidc_source_v1 "
            "WHERE run_id=990000124"
        ).fetchone()[0]
    assert count == 1


def test_real_postgres_oidc_receipt_preprovisioned_and_no_ddl_role(stores, monkeypatch):
    """Actual read/write-only role may append one signed-source receipt,
    but cannot run SQL schema migrations or overwrite existing evidence."""
    from kuuos_mcp_bridge.github_oidc_source import (
        PostgresOIDCSourceReceiptStore, VerifiedSource,
        REPO, WORKFLOW_REF, FEATURE_REF,
    )
    import secrets as local_secrets
    from psycopg import sql

    monkeypatch.delenv("KUUOS_MCP_SCHEMA_MODE", raising=False)
    PostgresOIDCSourceReceiptStore(DSN)
    role = "kuuos_oidc_ci_" + local_secrets.token_hex(4)
    password = local_secrets.token_urlsafe(32)
    with psycopg.connect(DSN) as conn:
        conn.execute(sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
            sql.Identifier(role), sql.Literal(password)
        ))
        conn.execute(sql.SQL("GRANT USAGE ON SCHEMA public TO {}").format(
            sql.Identifier(role)
        ))
        conn.execute(sql.SQL(
            "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE "
            "public.kuuos_mcp_github_oidc_source_v1 TO {}"
        ).format(sql.Identifier(role)))
    dsn = psycopg.conninfo.make_conninfo(DSN, user=role, password=password)
    with psycopg.connect(dsn) as conn:
        can_ddl = conn.execute(
            "SELECT has_schema_privilege(current_user, 'public', 'CREATE')"
        ).fetchone()[0]
    assert can_ddl is False
    monkeypatch.setenv("KUUOS_MCP_SCHEMA_MODE", "preprovisioned")
    read_write = PostgresOIDCSourceReceiptStore(dsn)
    source = VerifiedSource(
        identity="oidc_" + "2" * 64, repository=REPO,
        workflow_ref=WORKFLOW_REF, ref=FEATURE_REF,
        head_sha="c" * 40, run_id=990000125, run_attempt=1,
        jti_hash="d" * 64,
    )
    assert read_write.append(source)
    assert not read_write.append(source)


def test_real_postgres_verified_oidc_gates_delivery_outbox_idempotence(stores):
    """Check an OIDC-authenticated source's durable route on real PG16/18.

    JWT cryptographic admission is tested independently. This exercises
    the resulting typed identity, encrypted subscription, durable event
    packet, source-run replay and exact outbox lease on disposable PG.
    It is NOT Dots and does not certify an actual CI conclusion.
    """
    from kuuos_mcp_bridge.github_oidc_source import (
        VerifiedSource, CI_WORKFLOW_REF, FEATURE_REF,
        stage_verified_oidc_ci_gates,
    )
    from kuuos_mcp_bridge.github_event_contract import (
        CI_GATES_EVENT, CI_GATES_WORKFLOW, KUUOS_REPO,
    )
    from kuuos_mcp_bridge.event_pipeline import deliver_one
    from kuuos_mcp_bridge.event_delivery import PostResult

    subs, outbox = stores
    owner = "oidc-ci-gates-disposable-owner"
    manager = SubscriptionManager(
        subs,
        authorize=lambda principal, name, args: (
            principal == owner and name == CI_GATES_EVENT
            and args.get("repository") == KUUOS_REPO
        ),
        verify_callback=lambda *args: True,
        now=lambda: NOW,
    )
    arguments = {"repository": KUUOS_REPO, "workflow_name": CI_GATES_WORKFLOW}
    callback = "https://synthetic-oidc-pg-receiver.example.org/callback"
    receipt = manager.subscribe(owner, {
        "name": CI_GATES_EVENT,
        "arguments": arguments,
        "delivery": {"mode": "webhook", "url": callback, "secret": ONE},
    })
    source = VerifiedSource(
        identity="oidc_" + "f"*64, repository=KUUOS_REPO,
        workflow_ref=CI_WORKFLOW_REF, ref=FEATURE_REF,
        head_sha="c"*40, run_id=998102321, run_attempt=1,
        jti_hash="d"*64, kind="ci_jobs_observed",
    )
    event, ids = stage_verified_oidc_ci_gates(source, manager, outbox)
    _, repeated = stage_verified_oidc_ci_gates(source, manager, outbox)
    assert len(ids) == 1 and ids == repeated
    assert event["data"]["ci_terminal_conclusion_verified"] is False
    assert event["data"]["signal_is_success_evidence"] is False
    assert event["data"]["fresh_mcp_reobservation_required"] is True

    class SyntheticPoster:
        def __init__(self):
            self.calls = []
        def post(self, url, body, headers):
            self.calls.append((url, body, headers))
            return PostResult(200, b'{"accepted":true}')

    poster = SyntheticPoster()
    moment = datetime.now(timezone.utc)
    result = deliver_one(manager, outbox, poster=poster,
                         now=moment, outbox_id=ids[0])
    assert result["state"] == "delivered"
    assert len(poster.calls) == 1
    assert deliver_one(manager, outbox, poster=poster,
                       now=moment, outbox_id=ids[0])["state"] == "no_due_events"
    assert len(poster.calls) == 1
    with psycopg.connect(DSN) as conn:
        row = conn.execute(
            "SELECT state, attempts, last_http_status "
            "FROM kuuos_mcp_event_outbox_v1 WHERE id=%s", (ids[0],)
        ).fetchone()
    assert row == ("delivered", 1, 200)
    manager.unsubscribe(owner, {
        "name": CI_GATES_EVENT, "arguments": arguments,
        "delivery": {"mode": "webhook", "url": callback},
    })
    assert subs.get(receipt["id"]) is None
