"""Explicit PostgreSQL schema authority boundary for KuuOS MCP bridge.

The default mode performs the existing additive bootstrap DDL.
The opt-in preprovisioned mode performs SELECT-only catalog verification,
so an application role need not own tables or hold schema CREATE privileges.
This does not grant an application permission to mutate the database schema.
"""
from __future__ import annotations

import os
from typing import Mapping

SCHEMA_MODE_ENV = "KUUOS_MCP_SCHEMA_MODE"


def schema_is_preprovisioned() -> bool:
    mode = os.environ.get(SCHEMA_MODE_ENV, "migrate")
    if mode not in {"migrate", "preprovisioned"}:
        raise RuntimeError("KUUOS_MCP_SCHEMA_MODE must be 'migrate' or 'preprovisioned'")
    return mode == "preprovisioned"


def verify_preprovisioned_schema(
    conn,
    *,
    table: str,
    columns: Mapping[str, tuple[str, bool]],
    indexes: tuple[str, ...] = (),
    constraints: Mapping[str, str] | None = None,
) -> None:
    """Fail closed against absent/mistyped or weakened real PostgreSQL tables.

    Expected columns map a name to (information_schema data_type, NOT NULL).
    All queries are SELECT-only. The role must already have table DML grants;
    an event receipt and source metadata are never produced by this check.
    """
    if not isinstance(table, str) or not table.startswith("kuuos_mcp_"):
        raise RuntimeError("preprovisioned_schema_table_unrecognized")
    qualified = "public." + table
    with conn.cursor() as cursor:
        cursor.execute("SELECT current_schema()")
        if cursor.fetchone()[0] != "public":
            raise RuntimeError("preprovisioned_schema_namespace_mismatch")
        cursor.execute(
            "SELECT column_name, data_type, is_nullable "
            "FROM information_schema.columns "
            "WHERE table_schema = 'public' AND table_name = %s",
            (table,),
        )
        observed = {name: (kind, nullable == "NO")
                    for name, kind, nullable in cursor.fetchall()}
        missing_or_wrong = [
            name for name, expected in columns.items()
            if observed.get(name) != expected
        ]
        if missing_or_wrong:
            raise RuntimeError("preprovisioned_schema_columns_invalid:" +
                               ",".join(sorted(missing_or_wrong)))

        cursor.execute(
            "SELECT indexname FROM pg_indexes "
            "WHERE schemaname = 'public' AND tablename = %s", (table,)
        )
        observed_indexes = {row[0] for row in cursor.fetchall()}
        if not set(indexes).issubset(observed_indexes):
            raise RuntimeError("preprovisioned_schema_indexes_missing")

        cursor.execute(
            "SELECT conname, contype FROM pg_constraint "
            "WHERE conrelid = to_regclass(%s)", (qualified,)
        )
        actual_constraints = dict(cursor.fetchall())
        for name, expected_type in (constraints or {}).items():
            if actual_constraints.get(name) != expected_type:
                raise RuntimeError("preprovisioned_schema_constraint_invalid:" + name)

        privileges = ("SELECT", "INSERT", "UPDATE", "DELETE")
        cursor.execute(
            "SELECT " + ", ".join(
                "has_table_privilege(current_user, %s, %s)" for _ in privileges
            ),
            tuple(item for privilege in privileges
                  for item in (qualified, privilege)),
        )
        rights = cursor.fetchone()
        if rights is None or not all(value is True for value in rights):
            raise RuntimeError("preprovisioned_schema_role_dml_missing")
