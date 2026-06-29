#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_repository_checkpoint_creation_receipt_v1_03 import (
    certify_repository_checkpoint_creation_receipt as _certify,
    repository_checkpoint_creation_receipt_issues as _issues,
)


def certify_repository_checkpoint_creation_receipt(*args, **kwargs):
    receipt = _certify(*args, **kwargs)
    if args:
        issues = _issues(receipt, *args[1:], **kwargs)
    else:
        issue_kwargs = dict(kwargs)
        issue_kwargs.pop("receipt_id", None)
        issues = _issues(receipt, **issue_kwargs)
    if issues:
        raise ValueError(f"checkpoint_creation_receipt_invalid:{issues[0]}")
    return receipt


def repository_checkpoint_creation_receipt_issues(*args, **kwargs):
    return _issues(*args, **kwargs)
