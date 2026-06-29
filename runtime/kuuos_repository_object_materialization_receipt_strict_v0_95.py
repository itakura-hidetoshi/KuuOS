#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_object_materialization_receipt_v0_95 import (
    certify_repository_object_materialization_receipt as _certify,
    repository_object_materialization_receipt_issues as _issues,
)


def certify_repository_object_materialization_receipt(*args, **kwargs):
    receipt = _certify(*args, **kwargs)
    issues = _issues(receipt, *args, **kwargs)
    if issues:
        raise ValueError(f"object_materialization_receipt_invalid:{issues[0]}")
    return receipt


def repository_object_materialization_receipt_issues(receipt, *args, **kwargs):
    return _issues(receipt, *args, **kwargs)
