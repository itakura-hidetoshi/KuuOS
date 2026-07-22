from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_schema_v0_1 import SCHEMA_COLUMNS
from scripts.build_codeai_external_corpus_acquisition_freeze_receipt_fixture_v0_1 import (
    ARTIFACT_SHA256,
    ARTIFACT_SIZE_BYTES,
    EXPECTED_ROW_COUNT,
    build_fixture,
)
from scripts.project_codeai_external_corpus_acquisition_freeze_receipt_fixture_v0_1 import manifest_projection

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_external_corpus_acquisition_freeze_receipt_v0_1.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_external_corpus_acquisition_freeze_receipt_v0_1.json"


def verify_external_artifact(path: Path) -> None:
    data = path.read_bytes()
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if actual_sha256 != ARTIFACT_SHA256:
        raise SystemExit(f"external artifact sha256 mismatch: {actual_sha256}")
    if len(data) != ARTIFACT_SIZE_BYTES:
        raise SystemExit(f"external artifact size mismatch: {len(data)}")
    try:
        import pyarrow.parquet as pq
    except ImportError as exc:
        raise SystemExit("pyarrow is required for --artifact verification") from exc
    parquet_file = pq.ParquetFile(path)
    if parquet_file.metadata.num_rows != EXPECTED_ROW_COUNT:
        raise SystemExit(f"external artifact row count mismatch: {parquet_file.metadata.num_rows}")
    actual_columns = tuple(parquet_file.schema_arrow.names)
    if actual_columns != SCHEMA_COLUMNS:
        raise SystemExit(f"external artifact schema mismatch: {actual_columns!r}")
    print(
        "external artifact verified: "
        f"sha256={actual_sha256} size={len(data)} rows={parquet_file.metadata.num_rows} columns={len(actual_columns)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path)
    args = parser.parse_args()

    expected = build_fixture()
    actual_example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    actual_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if actual_example != expected:
        raise SystemExit("example projection mismatch")
    if actual_manifest != manifest_projection(expected):
        raise SystemExit("manifest projection mismatch")
    pack = expected["freeze_pack"]
    if pack["freeze_decision"] != "external_corpus_freeze_admitted":
        raise SystemExit("reference freeze not admitted")
    if pack["row_count"] != EXPECTED_ROW_COUNT:
        raise SystemExit("reference row count mismatch")
    if pack["artifact_sha256"] != ARTIFACT_SHA256:
        raise SystemExit("reference artifact digest mismatch")
    if args.artifact is not None:
        verify_external_artifact(args.artifact)
    print("CodeAI external corpus acquisition and freeze receipt v0.1: OK")


if __name__ == "__main__":
    main()
